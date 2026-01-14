"""
Worker CRUD Operations - Database Version

Database operations for worker/employee management using SQLAlchemy.
"""

from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
import uuid

from ..L1_config.models import Worker as DBWorker


def create_worker(
    db: Session,
    ranch_id: str,
    full_name: str,
    position: Optional[str] = None,
    phone: Optional[str] = None,
    email: Optional[str] = None,
    salary_mxn: Optional[float] = None,
    hire_date: Optional[date] = None,
    notes: Optional[str] = None
) -> DBWorker:
    """Create new worker"""
    db_worker = DBWorker(
        id=str(uuid.uuid4()),
        ranch_id=ranch_id,
        full_name=full_name,
        position=position,
        phone=phone,
        email=email,
        salary_mxn=salary_mxn,
        hire_date=hire_date,
        is_active=True,
        notes=notes
    )
    
    db.add(db_worker)
    db.commit()
    db.refresh(db_worker)
    
    return db_worker


def get_worker(db: Session, worker_id: str) -> Optional[DBWorker]:
    """Get worker by ID"""
    return db.query(DBWorker).filter(DBWorker.id == worker_id).first()


def list_workers(
    db: Session,
    ranch_id: str,
    active_only: bool = True,
    limit: int = 100,
    offset: int = 0
) -> List[DBWorker]:
    """List workers with filters"""
    query = db.query(DBWorker).filter(DBWorker.ranch_id == ranch_id)
    
    if active_only:
        query = query.filter(DBWorker.is_active == True)
    
    return query.offset(offset).limit(limit).all()


def update_worker(
    db: Session,
    worker_id: str,
    **kwargs
) -> Optional[DBWorker]:
    """Update worker"""
    db_worker = get_worker(db, worker_id)
    if not db_worker:
        return None
    
    for key, value in kwargs.items():
        if value is not None and hasattr(db_worker, key):
            setattr(db_worker, key, value)
    
    db.commit()
    db.refresh(db_worker)
    
    return db_worker


def delete_worker(db: Session, worker_id: str) -> bool:
    """Delete worker (soft delete - set inactive)"""
    db_worker = get_worker(db, worker_id)
    if not db_worker:
        return False
    
    db_worker.is_active = False
    db.commit()
    
    return True
