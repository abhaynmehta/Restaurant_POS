"""Database Configuration Module

This module handles database connection setup, session management,
and SQLAlchemy configuration for the Restaurant POS API.

Optimizations:
- Connection pooling with size optimization
- Pre-ping for connection health
- Statement caching for performance
- Proper resource cleanup
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool

# Database connection string - Read from environment variable
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "mysql+pymysql://root:Admin123@localhost:3306/restaurant_pos"
)

# Optimized engine configuration
# pool_size: Number of pre-created connections to keep in pool
# max_overflow: Additional connections beyond pool_size
# pool_recycle: Recycle connections after 3600 seconds (1 hour)
engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=5,              # Keep 5 connections active
    max_overflow=10,          # Allow up to 10 additional connections
    pool_recycle=3600,        # Recycle connections every hour
    pool_pre_ping=True,       # Test connection before use
    echo=False,               # Set to True for SQL query logging
    connect_args={"connect_timeout": 10}  # Connection timeout
)

# Session factory for creating database sessions
SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine,
    expire_on_commit=True  # Expire objects after commit
)

# Declarative base for ORM models
Base = declarative_base()


def get_db():
    """Get a database session.
    
    This function provides a dependency injection for FastAPI endpoints
    to access the database. It ensures proper session cleanup after use.
    
    Yields:
        SessionLocal: Database session
    
    Example:
        @app.get("/orders")
        def get_orders(db: Session = Depends(get_db)):
            return db.query(Order).all()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()