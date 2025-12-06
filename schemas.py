"""Pydantic Schemas Module

This module defines all request and response schemas for data validation and serialization.
Schemas ensure type safety and automatic API documentation.

Optimizations:
- Use ConfigDict for modern Pydantic v2 configuration
- Field validation with proper constraints
- Response models for automatic serialization
- Efficient JSON encoding
"""

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date


class OrderItemSchema(BaseModel):
    """Schema for order items with validation constraints."""
    
    order_item_id: int = Field(..., gt=0, description="Unique order item identifier")
    item_id: int = Field(..., gt=0, description="Menu item ID")
    item_name: str = Field(..., min_length=1, max_length=200, description="Item name")
    category_name: str = Field(..., min_length=1, max_length=100, description="Category name")
    size: Optional[str] = Field(None, max_length=20, description="Item size if applicable")
    quantity: int = Field(..., gt=0, description="Quantity ordered")
    unit_price: float = Field(..., ge=0, description="Price per unit")
    line_total: float = Field(..., ge=0, description="Total for this line")
    
    model_config = {"from_attributes": True}


class PaymentSchema(BaseModel):
    """Schema for payment information with validation."""
    
    payment_id: int = Field(..., gt=0, description="Unique payment identifier")
    payment_date: date = Field(..., description="Date of payment")
    amount_due: float = Field(..., ge=0, description="Amount due")
    amount_paid: float = Field(..., ge=0, description="Amount actually paid")
    tips: float = Field(default=0.0, ge=0, description="Tip amount")
    discount: float = Field(default=0.0, ge=0, description="Discount amount")
    payment_type: str = Field(..., min_length=1, max_length=50, description="Type of payment")
    payment_status: str = Field(..., min_length=1, max_length=50, description="Payment status")
    
    model_config = {"from_attributes": True}


class OrderSummarySchema(BaseModel):
    """Schema for order summary with totals - optimized for calculation."""
    
    total_amount: float = Field(..., ge=0, description="Total order amount")
    total_paid: float = Field(default=0.0, ge=0, description="Total amount paid")
    total_tips: float = Field(default=0.0, ge=0, description="Total tips received")
    total_discount: float = Field(default=0.0, ge=0, description="Total discount given")
    outstanding_balance: float = Field(..., description="Amount still owed")
    payment_count: int = Field(default=0, ge=0, description="Number of payments")
    is_fully_paid: bool = Field(default=False, description="Whether order is fully paid")


class OrderDetailSchema(BaseModel):
    """Schema for complete order details - main response model."""
    
    order_id: int = Field(..., gt=0, description="Unique order identifier")
    order_date: date = Field(..., description="Date order was placed")
    order_status: str = Field(..., min_length=1, max_length=50, description="Current order status")
    items: List[OrderItemSchema] = Field(default_factory=list, description="Order items")
    payments: List[PaymentSchema] = Field(default_factory=list, description="Payment records")
    summary: OrderSummarySchema = Field(..., description="Order summary")
    
    model_config = {"from_attributes": True}


class OrderListResponse(BaseModel):
    """Schema for orders list response - optimized for array responses."""
    
    success: bool = Field(..., description="Whether request was successful")
    count: int = Field(..., ge=0, description="Number of orders returned")
    orders: List[OrderDetailSchema] = Field(default_factory=list, description="List of orders")


class SingleOrderResponse(BaseModel):
    """Schema for single order response."""
    
    success: bool = Field(..., description="Whether request was successful")
    order: OrderDetailSchema = Field(..., description="Order details")


class HealthCheckResponse(BaseModel):
    """Schema for health check response."""
    
    status: str = Field(..., min_length=1, max_length=50, description="Health status")
    database: str = Field(..., min_length=1, max_length=50, description="Database status")
    error: Optional[str] = Field(None, max_length=200, description="Error message if any")