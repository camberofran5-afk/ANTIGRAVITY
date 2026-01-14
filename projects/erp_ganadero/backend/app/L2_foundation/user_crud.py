"""
User CRUD Operations

Database operations for user management.
"""

from sqlalchemy.orm import Session
from typing import Optional, List
from fastapi import HTTPException, status

from ..L1_config.models import User, Ranch, UserRanch, UserRole
from ..L1_config.auth_types import UserRegister, RanchCreate
from .auth_service import hash_password, verify_password


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Get user by email"""
    return db.query(User).filter(User.email == email).first()


def get_user_by_id(db: Session, user_id: str) -> Optional[User]:
    """Get user by ID"""
    return db.query(User).filter(User.id == user_id).first()


def create_user(db: Session, user_data: UserRegister) -> User:
    """
    Create new user
    
    Args:
        db: Database session
        user_data: User registration data
    
    Returns:
        Created user
    
    Raises:
        HTTPException: If email already exists
    """
    # Check if email exists
    if get_user_by_email(db, user_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create user
    db_user = User(
        email=user_data.email,
        password_hash=hash_password(user_data.password),
        full_name=user_data.full_name,
        phone=user_data.phone
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user


def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    """
    Authenticate user with email and password
    
    Args:
        db: Database session
        email: User email
        password: Plain text password
    
    Returns:
        User if authentication successful, None otherwise
    """
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user


def get_user_ranches(db: Session, user_id: str) -> List[Ranch]:
    """
    Get all ranches accessible to user (owned or member)
    
    Args:
        db: Database session
        user_id: User ID
    
    Returns:
        List of ranches
    """
    # Get owned ranches
    owned = db.query(Ranch).filter(Ranch.owner_id == user_id).all()
    
    # Get member ranches
    user_ranch_ids = db.query(UserRanch.ranch_id).filter(
        UserRanch.user_id == user_id
    ).all()
    ranch_ids = [ur[0] for ur in user_ranch_ids]
    member = db.query(Ranch).filter(Ranch.id.in_(ranch_ids)).all()
    
    # Combine and deduplicate
    all_ranches = {r.id: r for r in owned + member}
    return list(all_ranches.values())


def create_ranch(db: Session, ranch_data: RanchCreate, owner_id: str) -> Ranch:
    """
    Create new ranch
    
    Args:
        db: Database session
        ranch_data: Ranch creation data
        owner_id: Owner user ID
    
    Returns:
        Created ranch
    """
    db_ranch = Ranch(
        owner_id=owner_id,
        name=ranch_data.name,
        location=ranch_data.location
    )
    
    db.add(db_ranch)
    db.commit()
    db.refresh(db_ranch)
    
    return db_ranch


def add_user_to_ranch(
    db: Session,
    ranch_id: str,
    user_email: str,
    role: UserRole = UserRole.WORKER
) -> UserRanch:
    """
    Add user to ranch with specific role
    
    Args:
        db: Database session
        ranch_id: Ranch ID
        user_email: User email to add
        role: User role in ranch
    
    Returns:
        UserRanch association
    
    Raises:
        HTTPException: If user or ranch not found
    """
    user = get_user_by_email(db, user_email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    ranch = db.query(Ranch).filter(Ranch.id == ranch_id).first()
    if not ranch:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ranch not found"
        )
    
    # Check if already exists
    existing = db.query(UserRanch).filter(
        UserRanch.user_id == user.id,
        UserRanch.ranch_id == ranch_id
    ).first()
    
    if existing:
        # Update role
        existing.role = role
        db.commit()
        db.refresh(existing)
        return existing
    
    # Create new association
    user_ranch = UserRanch(
        user_id=user.id,
        ranch_id=ranch_id,
        role=role
    )
    
    db.add(user_ranch)
    db.commit()
    db.refresh(user_ranch)
    
    return user_ranch
