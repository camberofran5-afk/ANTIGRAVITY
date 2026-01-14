"""
Authentication Types and Models

Pydantic models for authentication requests/responses.
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class UserRegister(BaseModel):
    """User registration request"""
    email: EmailStr
    password: str = Field(..., min_length=8)
    full_name: str
    phone: Optional[str] = None


class UserLogin(BaseModel):
    """User login request"""
    email: EmailStr
    password: str


class Token(BaseModel):
    """JWT token response"""
    access_token: str
    token_type: str = "bearer"
    user: dict


class TokenData(BaseModel):
    """Data stored in JWT token"""
    user_id: str
    email: str


class UserResponse(BaseModel):
    """User data response"""
    id: str
    email: str
    full_name: Optional[str]
    phone: Optional[str]
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class RanchCreate(BaseModel):
    """Create ranch request"""
    name: str = Field(..., min_length=1, max_length=255)
    location: Optional[str] = None


class RanchResponse(BaseModel):
    """Ranch data response"""
    id: str
    owner_id: str
    name: str
    location: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True
