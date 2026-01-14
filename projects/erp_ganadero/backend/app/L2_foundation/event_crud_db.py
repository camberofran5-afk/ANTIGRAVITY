"""
Event CRUD Operations - Database Version

Database operations for event management using SQLAlchemy.
"""

from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
import uuid
import json

from ..L1_config.models import Event as DBEvent, EventType as DBEventType
from ..L1_config.cattle_types import EventCreate, EventType


def create_event(db: Session, event_data: EventCreate) -> DBEvent:
    """
    Create new event in database
    
    Args:
        db: Database session
        event_data: Event creation data
    
    Returns:
        Created event
    """
    # Get ranch_id from cattle
    from ..L1_config.models import Animal
    animal = db.query(Animal).filter(Animal.id == event_data.cattle_id).first()
    if not animal:
        raise ValueError(f"Animal {event_data.cattle_id} not found")
    
    db_event = DBEvent(
        id=str(uuid.uuid4()),
        ranch_id=animal.ranch_id,
        cattle_id=event_data.cattle_id,
        type=DBEventType(event_data.type.value),
        event_date=event_data.event_date,
        data=json.dumps(event_data.data) if event_data.data else "{}",
        photo_url=event_data.photo_url,
        notes=event_data.notes
    )
    
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    
    return db_event


def get_event(db: Session, event_id: str) -> Optional[DBEvent]:
    """Get event by ID"""
    return db.query(DBEvent).filter(DBEvent.id == event_id).first()


def list_events(
    db: Session,
    ranch_id: Optional[str] = None,
    cattle_id: Optional[str] = None,
    event_type: Optional[EventType] = None,
    limit: int = 100,
    offset: int = 0
) -> List[DBEvent]:
    """
    List events with filters
    
    Args:
        db: Database session
        ranch_id: Optional ranch ID filter
        cattle_id: Optional cattle ID filter
        event_type: Optional event type filter
        limit: Maximum number of results
        offset: Number of results to skip
    
    Returns:
        List of events
    """
    query = db.query(DBEvent)
    
    if ranch_id:
        query = query.filter(DBEvent.ranch_id == ranch_id)
    
    if cattle_id:
        query = query.filter(DBEvent.cattle_id == cattle_id)
    
    if event_type:
        query = query.filter(DBEvent.type == DBEventType(event_type.value))
    
    return query.order_by(DBEvent.event_date.desc()).offset(offset).limit(limit).all()


def delete_event(db: Session, event_id: str) -> bool:
    """
    Delete event
    
    Args:
        db: Database session
        event_id: Event ID
    
    Returns:
        True if deleted, False if not found
    """
    db_event = get_event(db, event_id)
    if not db_event:
        return False
    
    db.delete(db_event)
    db.commit()
    
    return True
