"""
Database Configuration for ERP Ganadero

SQLAlchemy setup with SQLite for development, PostgreSQL for production.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Database URL from environment or default to SQLite
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./erp_ganadero.db"
)

# Create engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {},
    echo=False  # Set to True for SQL query logging
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


def get_db():
    """
    Dependency for FastAPI routes to get database session.
    
    Usage:
        @app.get("/items")
        def get_items(db: Session = Depends(get_db)):
            return db.query(Item).all()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Initialize database - create all tables.
    Call this on application startup.
    """
    Base.metadata.create_all(bind=engine)
