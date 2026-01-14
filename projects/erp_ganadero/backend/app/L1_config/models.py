"""
SQLAlchemy Database Models for ERP Ganadero

All database tables defined using SQLAlchemy ORM.
"""

from sqlalchemy import Column, String, Integer, Float, Date, DateTime, Boolean, Text, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime, date
import uuid
import enum

from .database import Base


# ============================================================================
# Enums
# ============================================================================

class UserRole(str, enum.Enum):
    OWNER = "owner"
    MANAGER = "manager"
    WORKER = "worker"


class AnimalStatus(str, enum.Enum):
    ACTIVE = "active"
    SOLD = "sold"
    DEAD = "dead"
    REST = "rest"


class AnimalSpecies(str, enum.Enum):
    VACA = "vaca"
    TORO = "toro"
    BECERRO = "becerro"
    VAQUILLA = "vaquilla"


class Gender(str, enum.Enum):
    M = "M"
    F = "F"


class EventType(str, enum.Enum):
    BIRTH = "birth"
    DEATH = "death"
    SALE = "sale"
    VACCINATION = "vaccination"
    WEIGHING = "weighing"
    PREGNANCY_CHECK = "pregnancy_check"
    TREATMENT = "treatment"


class CostCategory(str, enum.Enum):
    FEED = "feed"
    VETERINARY = "veterinary"
    LABOR = "labor"
    INFRASTRUCTURE = "infrastructure"
    OTHER = "other"


# ============================================================================
# Helper Functions
# ============================================================================

def generate_uuid():
    """Generate UUID as string"""
    return str(uuid.uuid4())


# ============================================================================
# User & Authentication Models
# ============================================================================

class User(Base):
    __tablename__ = "users"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255))
    phone = Column(String(50))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    owned_ranches = relationship("Ranch", back_populates="owner", foreign_keys="Ranch.owner_id")
    user_ranches = relationship("UserRanch", back_populates="user")


class Ranch(Base):
    __tablename__ = "ranches"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    owner_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    name = Column(String(255), nullable=False)
    location = Column(Text)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    owner = relationship("User", back_populates="owned_ranches", foreign_keys=[owner_id])
    user_ranches = relationship("UserRanch", back_populates="ranch")
    cattle = relationship("Animal", back_populates="ranch")
    events = relationship("Event", back_populates="ranch")
    costs = relationship("Cost", back_populates="ranch")
    inventory = relationship("InventoryItem", back_populates="ranch")
    clients = relationship("Client", back_populates="ranch")
    workers = relationship("Worker", back_populates="ranch")


class UserRanch(Base):
    """Many-to-many relationship between users and ranches with role"""
    __tablename__ = "user_ranches"
    
    user_id = Column(String(36), ForeignKey("users.id"), primary_key=True)
    ranch_id = Column(String(36), ForeignKey("ranches.id"), primary_key=True)
    role = Column(SQLEnum(UserRole), default=UserRole.WORKER)
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="user_ranches")
    ranch = relationship("Ranch", back_populates="user_ranches")


# ============================================================================
# Cattle Management Models
# ============================================================================

class Animal(Base):
    __tablename__ = "cattle"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    ranch_id = Column(String(36), ForeignKey("ranches.id"), nullable=False, index=True)
    arete_number = Column(String(50), nullable=False, index=True)
    species = Column(SQLEnum(AnimalSpecies), nullable=False)
    gender = Column(SQLEnum(Gender), nullable=False)
    birth_date = Column(Date, nullable=False)
    weight_kg = Column(Float)
    photo_url = Column(Text)
    status = Column(SQLEnum(AnimalStatus), default=AnimalStatus.ACTIVE)
    mother_id = Column(String(36), ForeignKey("cattle.id"))
    notes = Column(Text)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    ranch = relationship("Ranch", back_populates="cattle")
    mother = relationship("Animal", remote_side=[id], backref="offspring")
    events = relationship("Event", back_populates="animal")


class Event(Base):
    __tablename__ = "events"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    ranch_id = Column(String(36), ForeignKey("ranches.id"), nullable=False, index=True)
    cattle_id = Column(String(36), ForeignKey("cattle.id"), nullable=False, index=True)
    type = Column(SQLEnum(EventType), nullable=False)
    event_date = Column(Date, nullable=False)
    data = Column(Text)  # JSON string for flexible data
    photo_url = Column(Text)
    notes = Column(Text)
    created_by = Column(String(36), ForeignKey("users.id"))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    ranch = relationship("Ranch", back_populates="events")
    animal = relationship("Animal", back_populates="events")


# ============================================================================
# Financial Models
# ============================================================================

class Cost(Base):
    __tablename__ = "costs"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    ranch_id = Column(String(36), ForeignKey("ranches.id"), nullable=False, index=True)
    category = Column(SQLEnum(CostCategory), nullable=False)
    amount_mxn = Column(Float, nullable=False)
    description = Column(Text)
    cost_date = Column(Date, nullable=False)
    cattle_id = Column(String(36), ForeignKey("cattle.id"))
    created_by = Column(String(36), ForeignKey("users.id"))
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    ranch = relationship("Ranch", back_populates="costs")


# ============================================================================
# Inventory Models
# ============================================================================

class InventoryItem(Base):
    __tablename__ = "inventory"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    ranch_id = Column(String(36), ForeignKey("ranches.id"), nullable=False, index=True)
    category = Column(String(50), nullable=False)
    name = Column(String(255), nullable=False)
    quantity = Column(Float, nullable=False)
    unit = Column(String(20), nullable=False)
    unit_cost = Column(Float)
    min_stock = Column(Float)
    supplier = Column(String(255))
    notes = Column(Text)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    ranch = relationship("Ranch", back_populates="inventory")


# ============================================================================
# Client Models
# ============================================================================

class Client(Base):
    __tablename__ = "clients"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    ranch_id = Column(String(36), ForeignKey("ranches.id"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    type = Column(String(50))  # feedlot, butcher, individual, etc.
    contact_name = Column(String(255))
    phone = Column(String(50))
    email = Column(String(255))
    address = Column(Text)
    payment_terms = Column(String(50))
    notes = Column(Text)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    ranch = relationship("Ranch", back_populates="clients")


# ============================================================================
# Worker Models
# ============================================================================

class Worker(Base):
    __tablename__ = "workers"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    ranch_id = Column(String(36), ForeignKey("ranches.id"), nullable=False, index=True)
    full_name = Column(String(255), nullable=False)
    position = Column(String(100))
    phone = Column(String(50))
    email = Column(String(255))
    salary_mxn = Column(Float)
    hire_date = Column(Date)
    is_active = Column(Boolean, default=True)
    notes = Column(Text)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    ranch = relationship("Ranch", back_populates="workers")
