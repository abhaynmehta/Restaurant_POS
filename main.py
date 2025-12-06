"""Restaurant POS API - Main Application

This module defines all API endpoints for the Restaurant Point of Sale system.
It provides endpoints for retrieving order information with full payment details.

Endpoints:
    GET / - Welcome message
    GET /health - Health check  
    GET /api/v1/orders - Get all orders (requires auth)
    GET /api/v1/orders/{order_id} - Get specific order (requires auth)
"""

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session, joinedload, selectinload
from sqlalchemy import text

from database import get_db, engine, Base
from models import Order, OrderItem, Payment, MenuItem, Category
from schemas import OrderDetailSchema, OrderItemSchema, PaymentSchema, OrderSummarySchema
from security import get_api_key

# Create database tables if they don't exist
Base.metadata.create_all(bind=engine)

# Initialize FastAPI application
app = FastAPI(
    title="Restaurant POS API",
    description="A comprehensive REST API for managing restaurant orders, items, and payments",
    version="1.0.0",
    contact={"name": "Support"},
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Health"])
def root():
    """Welcome endpoint with API information."""
    return {
        "message": "Welcome to Restaurant POS API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "health": "/health",
            "orders": "/api/v1/orders",
            "order_detail": "/api/v1/orders/{order_id}"
        },
    }


@app.get("/health", tags=["Health"])
def health_check(db: Session = Depends(get_db)):
    """Check API and database health status.
    
    Performs a lightweight database query to verify connectivity.
    Returns immediately on success.
    
    Returns:
        dict: Status of API and database connection
    """
    try:
        # Lightweight query to test connection
        db.execute(text("SELECT 1"))
        db.close()  # Immediately release connection
        return {
            "status": "healthy",
            "database": "connected",
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "error",
            "error": str(e)[:100]  # Limit error message length
        }

def build_order_response(order: Order, db: Session) -> OrderDetailSchema:
    """Build complete order response with items and payments.
    
    Optimized to use selectinload and batch processing to minimize queries.
    Aggregates order data from multiple tables into a single response object.
    
    Args:
        order: Order model instance (should have items/payments pre-loaded)
        db: Database session
    
    Returns:
        OrderDetailSchema: Complete order details with items and payments
    """
    # Use order's pre-loaded relationships if available
    order_items = order.order_items if order.order_items else (
        db.query(OrderItem).filter(OrderItem.order_id == order.order_id)
        .options(selectinload(OrderItem.menu_item).selectinload(MenuItem.category))
        .all()
    )
    
    # Transform order items to schema - minimal data copying
    items = [
        OrderItemSchema(
            order_item_id=oi.order_item_id,
            item_id=oi.item_id,
            item_name=oi.menu_item.item_name,
            category_name=oi.menu_item.category.category_name,
            size=oi.size,
            quantity=oi.quantity,
            unit_price=oi.unit_price,
            line_total=oi.line_total
        )
        for oi in order_items
    ]
    
    # Fetch all payments - use pre-loaded relationships if available
    payments = order.payments if order.payments else (
        db.query(Payment).filter(Payment.order_id == order.order_id).all()
    )
    
    payment_list = [
        PaymentSchema(
            payment_id=p.payment_id,
            payment_date=p.payment_date,
            amount_due=p.amount_due,
            amount_paid=p.amount_paid,
            tips=p.tips,
            discount=p.discount,
            payment_type=p.payment_type,
            payment_status=p.payment_status
        )
        for p in payments
    ]
    
    # Calculate payment summary in single pass (optimized)
    total_paid = 0.0
    total_tips = 0.0
    total_discount = 0.0
    payment_count = 0
    
    for p in payments:
        if p.payment_status == "Completed":
            total_paid += p.amount_paid
            total_tips += p.tips
            total_discount += p.discount
        payment_count += 1
    
    outstanding = order.total_amount - total_paid
    
    # Create order summary
    summary = OrderSummarySchema(
        total_amount=order.total_amount,
        total_paid=total_paid,
        total_tips=total_tips,
        total_discount=total_discount,
        outstanding_balance=outstanding,
        payment_count=payment_count,
        is_fully_paid=abs(outstanding) < 0.01
    )
    
    return OrderDetailSchema(
        order_id=order.order_id,
        order_date=order.order_date,
        order_status=order.order_status,
        items=items,
        payments=payment_list,
        summary=summary
    )

@app.get("/api/v1/orders", tags=["Orders"])
def get_all_orders(db: Session = Depends(get_db), _: str = Depends(get_api_key)):
    """Get all orders with complete details.
    
    Returns all orders with eager-loaded relationships to minimize queries.
    Optimized to load orders with items and payments in minimal queries.
    
    Args:
        db: Database session
        _: API key validation (dependency injection)
    
    Returns:
        dict: All orders with their details
    
    Raises:
        HTTPException: 401 if API key is invalid or missing
    """
    # Eager load all relationships to avoid N+1 queries
    orders = db.query(Order).options(
        selectinload(Order.order_items).selectinload(OrderItem.menu_item).selectinload(MenuItem.category),
        selectinload(Order.payments)
    ).all()
    
    return {
        "success": True,
        "count": len(orders),
        "orders": [build_order_response(o, db) for o in orders]
    }


@app.get("/api/v1/orders/{order_id}", tags=["Orders"])
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    _: str = Depends(get_api_key)
) -> dict:
    """Get a specific order by ID.
    
    Retrieves complete order details with eager-loaded relationships.
    Optimized to fetch order with items and payments in minimal queries.
    
    Args:
        order_id: The ID of the order to retrieve (path parameter)
        db: Database session
        _: API key validation (dependency injection)
    
    Returns:
        dict: Order details with items and payments
    
    Raises:
        HTTPException: 404 if order not found (status_code=404)
        HTTPException: 401 if API key is invalid or missing (status_code=401)
    """
    # Eager load all relationships for single query performance
    order = db.query(Order).options(
        selectinload(Order.order_items).selectinload(OrderItem.menu_item).selectinload(MenuItem.category),
        selectinload(Order.payments)
    ).filter(Order.order_id == order_id).first()
    
    if not order:
        raise HTTPException(
            status_code=404, 
            detail=f"Order with ID {order_id} not found"
        )
    
    return {"success": True, "order": build_order_response(order, db)}


if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Restaurant POS API...")
    print("📖 API Documentation: http://localhost:8000/docs")
    print("🔐 Requires API Key: sk_test_restaurant_pos_2025_secure_key_12345")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)