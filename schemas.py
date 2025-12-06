"""Pydantic Schemas Module

This module defines all request and response schemas for data validation and serialization.
Schemas ensure type safety and automatic API documentation.
"""

from pydantic import BaseModel
from typing import List, Optional
from datetime import date


class OrderItemSchema(BaseModel):
    """Schema for order items."""
    
    order_item_id: int
    item_id: int
    item_name: str
    category_name: str
    size: Optional[str] = None
    quantity: int
    unit_price: float
    line_total: float
    
    class Config:
        from_attributes = True


class PaymentSchema(BaseModel):
    """Schema for payment information."""
    
    payment_id: int
    payment_date: date
    amount_due: float
    amount_paid: float
    tips: float
    discount: float
    payment_type: str
    payment_status: str
    
    class Config:
        from_attributes = True


class OrderSummarySchema(BaseModel):
    """Schema for order summary with totals."""
    
    total_amount: float
    total_paid: float
    total_tips: float
    total_discount: float
    outstanding_balance: float
    payment_count: int
    is_fully_paid: bool


class OrderDetailSchema(BaseModel):
    """Schema for complete order details."""
    
    order_id: int
    order_date: date
    order_status: str
    items: List[OrderItemSchema]
    payments: List[PaymentSchema]
    summary: OrderSummarySchema
    
    class Config:
        from_attributes = True


class OrderListResponse(BaseModel):
    """Schema for orders list response."""
    
    success: bool
    count: int
    orders: List[OrderDetailSchema]


class SingleOrderResponse(BaseModel):
    """Schema for single order response."""
    
    success: bool
    order: OrderDetailSchema


class HealthCheckResponse(BaseModel):
    """Schema for health check response."""
    
    status: str
    database: str