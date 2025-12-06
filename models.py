"""Database Models Module

This module defines all SQLAlchemy ORM models for the Restaurant POS API.
Models represent database tables and their relationships.

Optimizations:
- Strategic indexes on foreign keys and frequently queried columns
- Proper relationship configuration with lazy loading options
- Efficient cascade options for data integrity
"""

from sqlalchemy import Column, Integer, String, Date, Float, Boolean, ForeignKey, TIMESTAMP, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class Menu(Base):
    """Menu model - represents a restaurant menu (e.g., Food, Drinks)."""
    
    __tablename__ = "menus"
    
    menu_id = Column(Integer, primary_key=True)
    menu_name = Column(String(100), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    
    # Relationships
    categories = relationship("Category", back_populates="menu")
    menu_items = relationship("MenuItem", back_populates="menu")


class Category(Base):
    """Category model - represents item categories within menus."""
    
    __tablename__ = "categories"
    
    category_id = Column(Integer, primary_key=True)
    category_name = Column(String(100), nullable=False)
    menu_id = Column(Integer, ForeignKey("menus.menu_id"))
    display_order = Column(Integer, default=0)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    
    # Relationships
    menu = relationship("Menu", back_populates="categories")
    menu_items = relationship("MenuItem", back_populates="category")


class MenuItem(Base):
    """MenuItem model - represents individual items on the menu."""
    
    __tablename__ = "menu_items"
    
    item_id = Column(Integer, primary_key=True)
    item_name = Column(String(200), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.category_id"))
    menu_id = Column(Integer, ForeignKey("menus.menu_id"))
    has_sizes = Column(Boolean, default=False)
    size_options = Column(String(100))
    base_price = Column(Float)
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    
    # Relationships
    category = relationship("Category", back_populates="menu_items")
    menu = relationship("Menu", back_populates="menu_items")
    order_items = relationship("OrderItem", back_populates="menu_item")


class Order(Base):
    """Order model - represents a customer order."""
    
    __tablename__ = "orders"
    
    order_id = Column(Integer, primary_key=True)
    order_date = Column(Date, nullable=False)
    order_status = Column(String(50), default="Completed")
    total_amount = Column(Float)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    
    # Relationships
    order_items = relationship("OrderItem", back_populates="order")
    payments = relationship("Payment", back_populates="order")


class OrderItem(Base):
    """OrderItem model - represents individual items within an order."""
    
    __tablename__ = "order_items"
    __table_args__ = (
        Index('idx_order_id', 'order_id'),  # Fast lookups by order_id
        Index('idx_item_id', 'item_id'),    # Fast lookups by item_id
    )
    
    order_item_id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.order_id"), nullable=False)
    item_id = Column(Integer, ForeignKey("menu_items.item_id"), nullable=False)
    size = Column(String(20))
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    line_total = Column(Float, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    
    # Relationships - lazy loading optimized
    order = relationship("Order", back_populates="order_items")
    menu_item = relationship("MenuItem", back_populates="order_items")


class Payment(Base):
    """Payment model - represents payment transactions for orders."""
    
    __tablename__ = "payments"
    __table_args__ = (
        Index('idx_payment_order_id', 'order_id'),        # Fast lookups by order_id
        Index('idx_payment_status', 'payment_status'),    # Fast status filtering
    )
    
    payment_id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.order_id"), nullable=False)
    payment_date = Column(Date, nullable=False)
    amount_due = Column(Float, nullable=False)
    amount_paid = Column(Float, nullable=False)
    tips = Column(Float, default=0.0)
    discount = Column(Float, default=0.0)
    payment_type = Column(String(50), nullable=False)
    payment_status = Column(String(50), default="Completed")
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    
    # Relationships
    order = relationship("Order", back_populates="payments")


class APIKey(Base):
    """APIKey model - represents API keys for authentication."""
    
    __tablename__ = "api_keys"
    
    key_id = Column(Integer, primary_key=True, autoincrement=True)
    api_key = Column(String(64), unique=True, nullable=False)
    key_name = Column(String(100))
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())