"""
ERP Ganadero - Additional Type Definitions for V2
Pydantic models for Inventory, Clients, and Workers
"""

from enum import Enum
from typing import Optional
from datetime import date, datetime
from pydantic import BaseModel, Field, EmailStr


# ============================================================================
# Inventory Models
# ============================================================================

class InventoryCategory(str, Enum):
    """Inventory categories"""
    FEED = "feed"
    MEDICINE = "medicine"
    VACCINE = "vaccine"
    EQUIPMENT = "equipment"


class InventoryItemBase(BaseModel):
    """Base inventory item model"""
    category: InventoryCategory
    name: str = Field(..., min_length=1, max_length=255)
    quantity: float = Field(..., gt=0)
    unit: str = Field(..., min_length=1, max_length=50)
    unit_cost: float = Field(..., gt=0)
    supplier: Optional[str] = None
    expiry_date: Optional[date] = None
    min_stock: Optional[float] = Field(None, gt=0)
    location: Optional[str] = None


class InventoryItemCreate(InventoryItemBase):
    """Create inventory item"""
    ranch_id: str


class InventoryItem(InventoryItemBase):
    """Inventory item with ID"""
    id: str
    ranch_id: str
    total_value: float
    created_at: datetime
    
    class Config:
        from_attributes = True


# ============================================================================
# Client Models
# ============================================================================

class ClientType(str, Enum):
    """Client types"""
    FEEDLOT = "feedlot"
    BUTCHER = "butcher"
    EXPORT = "export"
    RANCHER = "rancher"


class PaymentTerms(str, Enum):
    """Payment terms"""
    CASH = "cash"
    DAYS_15 = "15_days"
    DAYS_30 = "30_days"
    DAYS_60 = "60_days"


class ClientBase(BaseModel):
    """Base client model"""
    name: str = Field(..., min_length=1, max_length=255)
    type: ClientType
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    payment_terms: PaymentTerms


class ClientCreate(ClientBase):
    """Create client"""
    ranch_id: str


class Client(ClientBase):
    """Client with ID"""
    id: str
    ranch_id: str
    created_at: datetime
    
    class Config:
        from_attributes = True


# ============================================================================
# Worker Models
# ============================================================================

class WorkerRole(str, Enum):
    """Worker roles"""
    VAQUERO = "vaquero"
    VETERINARIO = "veterinario"
    MANAGER = "manager"


class WorkerBase(BaseModel):
    """Base worker model"""
    name: str = Field(..., min_length=1, max_length=255)
    role: WorkerRole
    salary_monthly: float = Field(..., gt=0)
    hire_date: date


class WorkerCreate(WorkerBase):
    """Create worker"""
    ranch_id: str


class Worker(WorkerBase):
    """Worker with ID"""
    id: str
    ranch_id: str
    created_at: datetime
    
    class Config:
        from_attributes = True
