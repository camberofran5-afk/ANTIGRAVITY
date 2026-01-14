"""
ERP Ganadero - Cattle CRUD Operations (L2 Foundation)

Database operations for cattle management.
"""

from typing import List, Optional
from datetime import datetime
from supabase import Client

from ..L1_config.cattle_types import (
    Animal, AnimalCreate, AnimalUpdate, Status, Species
)
from ..L1_config.supabase_client import get_supabase
import structlog

logger = structlog.get_logger()


class CattleCRUD:
    """CRUD operations for cattle"""
    
    def __init__(self, supabase: Optional[Client] = None):
        self.db = supabase or get_supabase()
    
    async def create(self, animal: AnimalCreate) -> Animal:
        """Create new animal"""
        data = animal.model_dump()
        data["created_at"] = datetime.utcnow().isoformat()
        data["updated_at"] = datetime.utcnow().isoformat()
        
        result = self.db.table("cattle").insert(data).execute()
        
        logger.info("cattle_created", 
                   arete=animal.arete_number,
                   ranch_id=animal.ranch_id)
        
        return Animal(**result.data[0])
    
    async def get_by_id(self, cattle_id: str) -> Optional[Animal]:
        """Get animal by ID"""
        result = self.db.table("cattle")\
            .select("*")\
            .eq("id", cattle_id)\
            .execute()
        
        if not result.data:
            return None
        
        return Animal(**result.data[0])
    
    async def get_by_arete(self, ranch_id: str, arete_number: str) -> Optional[Animal]:
        """Get animal by arete number"""
        result = self.db.table("cattle")\
            .select("*")\
            .eq("ranch_id", ranch_id)\
            .eq("arete_number", arete_number)\
            .execute()
        
        if not result.data:
            return None
        
        return Animal(**result.data[0])
    
    async def list_by_ranch(
        self,
        ranch_id: str,
        status: Optional[Status] = None,
        species: Optional[Species] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[Animal]:
        """List animals by ranch with filters"""
        query = self.db.table("cattle")\
            .select("*")\
            .eq("ranch_id", ranch_id)
        
        if status:
            query = query.eq("status", status.value)
        
        if species:
            query = query.eq("species", species.value)
        
        result = query\
            .order("created_at", desc=True)\
            .range(offset, offset + limit - 1)\
            .execute()
        
        return [Animal(**row) for row in result.data]
    
    async def update(self, cattle_id: str, update: AnimalUpdate) -> Animal:
        """Update animal"""
        data = update.model_dump(exclude_unset=True)
        data["updated_at"] = datetime.utcnow().isoformat()
        
        result = self.db.table("cattle")\
            .update(data)\
            .eq("id", cattle_id)\
            .execute()
        
        logger.info("cattle_updated", cattle_id=cattle_id)
        
        return Animal(**result.data[0])
    
    async def delete(self, cattle_id: str) -> bool:
        """Delete animal (soft delete - set status to deleted)"""
        await self.update(cattle_id, AnimalUpdate(status=Status.DEAD))
        
        logger.info("cattle_deleted", cattle_id=cattle_id)
        return True
    
    async def count_by_ranch(
        self,
        ranch_id: str,
        status: Optional[Status] = None
    ) -> int:
        """Count animals by ranch"""
        query = self.db.table("cattle")\
            .select("id", count="exact")\
            .eq("ranch_id", ranch_id)
        
        if status:
            query = query.eq("status", status.value)
        
        result = query.execute()
        return result.count or 0
    
    async def get_productive_count(self, ranch_id: str) -> int:
        """Get count of productive animals (not unproductive)"""
        # This is a simplified version
        # Real implementation would check last calving date
        total = await self.count_by_ranch(ranch_id, Status.ACTIVE)
        # TODO: Filter by last_calving_date
        return total
    
    async def get_unproductive_cattle(self, ranch_id: str) -> List[Animal]:
        """Get list of unproductive cattle"""
        # TODO: Implement based on last calving date
        # For now, return empty list
        return []


def get_cattle_crud() -> CattleCRUD:
    """Get cattle CRUD instance"""
    return CattleCRUD()
