"""
ERP Ganadero - Type Definitions (L1 Configuration)

Pydantic models for all domain entities based on MVP analysis.
"""

from enum import Enum
from typing import Optional, Dict, Any, List
from datetime import date, datetime
from pydantic import BaseModel, Field, EmailStr, field_validator


class Species(str, Enum):
    """Cattle species"""
    VACA = "vaca"
    TORO = "toro"
    BECERRO = "becerro"
    VAQUILLA = "vaquilla"


class Gender(str, Enum):
    """Animal gender"""
    M = "M"
    F = "F"


class Status(str, Enum):
    """Animal status"""
    ACTIVE = "active"
    SOLD = "sold"
    DEAD = "dead"
    REST = "rest"


class EventType(str, Enum):
    """Event types"""
    BIRTH = "birth"
    DEATH = "death"
    SALE = "sale"
    VACCINATION = "vaccination"
    WEIGHING = "weighing"
    PREGNANCY_CHECK = "pregnancy_check"
    TREATMENT = "treatment"


class CostCategory(str, Enum):
    """Cost categories"""
    FEED = "feed"
    VETERINARY = "veterinary"
    LABOR = "labor"
    INFRASTRUCTURE = "infrastructure"
    OTHER = "other"


class UserRole(str, Enum):
    """User roles"""
    OWNER = "owner"
    MANAGER = "manager"
    WORKER = "worker"


# ============================================================================
# Base Models
# ============================================================================

class AnimalBase(BaseModel):
    """Base animal model"""
    arete_number: str = Field(..., min_length=1, max_length=50)
    species: Species
    gender: Gender
    birth_date: date
    weight_kg: Optional[float] = Field(None, gt=0)
    photo_url: Optional[str] = None
    status: Status = Status.ACTIVE
    mother_id: Optional[str] = None
    notes: Optional[str] = None


class AnimalCreate(AnimalBase):
    """Create animal"""
    ranch_id: str


class AnimalUpdate(BaseModel):
    """Update animal"""
    arete_number: Optional[str] = None
    weight_kg: Optional[float] = Field(None, gt=0)
    photo_url: Optional[str] = None
    status: Optional[Status] = None
    notes: Optional[str] = None


class Animal(AnimalBase):
    """Animal with ID"""
    id: str
    ranch_id: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ============================================================================
# Event Models
# ============================================================================

class EventBase(BaseModel):
    """Base event model"""
    type: EventType
    event_date: date
    data: dict = Field(default_factory=dict)
    photo_url: Optional[str] = None
    notes: Optional[str] = None


class EventCreate(EventBase):
    """Create event"""
    cattle_id: str


class Event(EventBase):
    """Event with ID"""
    id: str
    cattle_id: str
    created_by: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None  # Made optional to handle legacy data
    
    class Config:
        from_attributes = True


# ============================================================================
# Cost Models
# ============================================================================

class CostBase(BaseModel):
    """Base cost model"""
    category: CostCategory
    amount_mxn: float = Field(..., gt=0)
    description: Optional[str] = None
    cost_date: date
    cattle_id: Optional[str] = None


class CostCreate(CostBase):
    """Create cost"""
    ranch_id: str


class Cost(CostBase):
    """Cost with ID"""
    id: str
    ranch_id: str
    created_by: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


# ============================================================================
# Ranch Models
# ============================================================================

class RanchBase(BaseModel):
    """Base ranch model"""
    name: str = Field(..., min_length=1, max_length=255)
    location: Optional[str] = None


class RanchCreate(RanchBase):
    """Create ranch"""
    owner_id: str


class Ranch(RanchBase):
    """Ranch with ID"""
    id: str
    owner_id: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ============================================================================
# User Models
# ============================================================================

class UserProfileBase(BaseModel):
    """Base user profile"""
    full_name: Optional[str] = None
    phone: Optional[str] = None
    role: UserRole = UserRole.WORKER


class UserProfileCreate(UserProfileBase):
    """Create user profile"""
    ranch_id: str


class UserProfile(UserProfileBase):
    """User profile with ID"""
    id: str
    ranch_id: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ============================================================================
# Auth Models
# ============================================================================

class UserRegister(BaseModel):
    """User registration"""
    email: EmailStr
    password: str = Field(..., min_length=8)
    full_name: str
    ranch_name: str


class UserLogin(BaseModel):
    """User login"""
    email: EmailStr
    password: str


class Token(BaseModel):
    """JWT token"""
    access_token: str
    token_type: str = "bearer"
    user: dict


# ============================================================================
# Metrics Models
# ============================================================================

class HerdSummary(BaseModel):
    """Herd summary for dashboard"""
    total_animals: int
    productive_count: int
    unproductive_count: int
    ready_to_wean_count: int
    recent_births: int
    recent_deaths: int
    week_cost_usd: float


class HerdMetrics(BaseModel):
    """Herd KPIs"""
    pregnancy_rate: float
    calving_interval_days: float
    weaning_weight_avg: float
    calf_mortality_percent: float
    calculated_at: datetime
    source: str = "fresh"  # or "cache"


class MetricStatus(str, Enum):
    """Metric status"""
    OPTIMAL = "optimal"
    WARNING = "warning"
    CRITICAL = "critical"


# ============================================================================
# Sync Models
# ============================================================================

class SyncOperation(BaseModel):
    """Sync queue operation"""
    id: str
    operation: str  # create, update, delete
    table_name: str
    record_id: str
    payload: dict
    timestamp: datetime


class SyncRequest(BaseModel):
    """Request to sync data"""
    operations: List[SyncOperation]
    last_sync: Optional[datetime] = None


class SyncResponse(BaseModel):
    """Sync response"""
    synced: List[str]  # operation IDs
    conflicts: List[dict]
    server_changes: List[dict]
    server_timestamp: datetime
