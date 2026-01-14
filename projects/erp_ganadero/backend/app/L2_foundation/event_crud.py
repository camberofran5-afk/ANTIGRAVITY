"""
ERP Ganadero - Event CRUD Operations (L2 Foundation)
"""

from typing import List, Optional
from datetime import datetime
from supabase import Client

from ..L1_config.cattle_types import Event, EventCreate, EventType
from ..L1_config.supabase_client import get_supabase
import structlog

logger = structlog.get_logger()


class EventCRUD:
    """CRUD operations for events"""
    
    def __init__(self, supabase: Optional[Client] = None):
        self.db = supabase or get_supabase()
    
    async def create(self, event: EventCreate, user_id: Optional[str] = None) -> Event:
        """Create new event"""
        data = event.model_dump()
        data["created_by"] = user_id
        data["created_at"] = datetime.utcnow().isoformat()
        data["updated_at"] = datetime.utcnow().isoformat()
        
        result = self.db.table("events").insert(data).execute()
        
        logger.info("event_created", 
                   type=event.type,
                   cattle_id=event.cattle_id)
        
        return Event(**result.data[0])
    
    async def get_by_cattle(
        self,
        cattle_id: str,
        event_type: Optional[EventType] = None,
        limit: int = 50
    ) -> List[Event]:
        """Get events for a specific animal"""
        query = self.db.table("events")\
            .select("*")\
            .eq("cattle_id", cattle_id)
        
        if event_type:
            query = query.eq("type", event_type.value)
        
        result = query\
            .order("event_date", desc=True)\
            .limit(limit)\
            .execute()
        
        return [Event(**row) for row in result.data]
    
    async def get_recent_by_ranch(
        self,
        ranch_id: str,
        days: int = 7,
        limit: int = 50
    ) -> List[Event]:
        """Get recent events for a ranch"""
        # Note: This requires joining with cattle table
        # Simplified version for now
        result = self.db.table("events")\
            .select("*, cattle!inner(ranch_id)")\
            .eq("cattle.ranch_id", ranch_id)\
            .order("event_date", desc=True)\
            .limit(limit)\
            .execute()
        
        return [Event(**row) for row in result.data]


def get_event_crud() -> EventCRUD:
    """Get event CRUD instance"""
    return EventCRUD()
