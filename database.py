"""Database Configuration Module

This module handles database connection setup, session management,
and SQLAlchemy configuration for the Restaurant POS API.
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database connection string
# Read from environment variable or use default
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "mysql+pymysql://root:Admin123@localhost:3306/restaurant_pos"
)

# Create database engine with connection pooling
# pool_pre_ping=True ensures connections are alive before use
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    echo=False,  # Set to True for SQL query logging
)

# Session factory for creating database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

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