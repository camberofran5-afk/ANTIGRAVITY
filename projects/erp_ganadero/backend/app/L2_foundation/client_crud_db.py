"""
Client CRUD Operations - Database Version

Database operations for client management using SQLAlchemy.
"""

from sqlalchemy.orm import Session
from typing import List, Optional
import uuid

from ..L1_config.models import Client as DBClient


def create_client(
    db: Session,
    ranch_id: str,
    name: str,
    client_type: Optional[str] = None,
    contact_name: Optional[str] = None,
    phone: Optional[str] = None,
    email: Optional[str] = None,
    address: Optional[str] = None,
    payment_terms: Optional[str] = None,
    notes: Optional[str] = None
) -> DBClient:
    """Create new client"""
    db_client = DBClient(
        id=str(uuid.uuid4()),
        ranch_id=ranch_id,
        name=name,
        type=client_type,
        contact_name=contact_name,
        phone=phone,
        email=email,
        address=address,
        payment_terms=payment_terms,
        notes=notes
    )
    
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    
    return db_client


def get_client(db: Session, client_id: str) -> Optional[DBClient]:
    """Get client by ID"""
    return db.query(DBClient).filter(DBClient.id == client_id).first()


def list_clients(
    db: Session,
    ranch_id: str,
    client_type: Optional[str] = None,
    limit: int = 100,
    offset: int = 0
) -> List[DBClient]:
    """List clients with filters"""
    query = db.query(DBClient).filter(DBClient.ranch_id == ranch_id)
    
    if client_type:
        query = query.filter(DBClient.type == client_type)
    
    return query.offset(offset).limit(limit).all()


def update_client(
    db: Session,
    client_id: str,
    **kwargs
) -> Optional[DBClient]:
    """Update client"""
    db_client = get_client(db, client_id)
    if not db_client:
        return None
    
    for key, value in kwargs.items():
        if value is not None and hasattr(db_client, key):
            setattr(db_client, key, value)
    
    db.commit()
    db.refresh(db_client)
    
    return db_client


def delete_client(db: Session, client_id: str) -> bool:
    """Delete client"""
    db_client = get_client(db, client_id)
    if not db_client:
        return False
    
    db.delete(db_client)
    db.commit()
    
    return True
