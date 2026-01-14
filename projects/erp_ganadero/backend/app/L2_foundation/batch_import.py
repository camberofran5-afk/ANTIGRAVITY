"""
Batch Import API

Handle bulk data imports with validation and progress tracking
"""

from typing import List, Dict, Any
from sqlalchemy.orm import Session
from fastapi import HTTPException
import structlog

from ..L1_config.models import Animal, Cost, InventoryItem, Client, Worker
from .cattle_crud_db import create_animal
from .cost_crud_db import create_cost
from .inventory_crud_db import create_inventory_item
from .client_crud_db import create_client
from .worker_crud_db import create_worker

logger = structlog.get_logger()


class BatchImporter:
    """Handle batch imports for various entity types"""
    
    def __init__(self, db: Session):
        self.db = db
        self.results = {
            "success": [],
            "errors": [],
            "total": 0,
            "imported": 0,
            "failed": 0
        }
    
    async def import_cattle(self, records: List[Dict[str, Any]], ranch_id: str) -> Dict[str, Any]:
        """
        Import multiple cattle records
        
        Args:
            records: List of cattle data dictionaries
            ranch_id: Ranch ID for all records
        
        Returns:
            Import results with success/error counts
        """
        self.results["total"] = len(records)
        
        for index, record in enumerate(records):
            try:
                # Add ranch_id
                record["ranch_id"] = ranch_id
                
                # Validate required fields
                if not record.get("arete_number"):
                    raise ValueError("arete_number is required")
                if not record.get("species"):
                    raise ValueError("species is required")
                if not record.get("gender"):
                    raise ValueError("gender is required")
                if not record.get("birth_date"):
                    raise ValueError("birth_date is required")
                
                # Create animal
                animal = create_animal(self.db, **record)
                
                self.results["success"].append({
                    "index": index,
                    "id": animal.id,
                    "arete_number": animal.arete_number
                })
                self.results["imported"] += 1
                
            except Exception as e:
                logger.error("Batch cattle import error", index=index, error=str(e))
                self.results["errors"].append({
                    "index": index,
                    "record": record,
                    "error": str(e)
                })
                self.results["failed"] += 1
        
        return self.results
    
    async def import_costs(self, records: List[Dict[str, Any]], ranch_id: str) -> Dict[str, Any]:
        """Import multiple cost records"""
        self.results["total"] = len(records)
        
        for index, record in enumerate(records):
            try:
                # Add ranch_id
                record["ranch_id"] = ranch_id
                
                # Validate required fields
                if not record.get("category"):
                    raise ValueError("category is required")
                if not record.get("amount_mxn"):
                    raise ValueError("amount_mxn is required")
                if not record.get("cost_date"):
                    raise ValueError("cost_date is required")
                
                # Create cost
                cost = create_cost(self.db, **record)
                
                self.results["success"].append({
                    "index": index,
                    "id": cost.id,
                    "amount": cost.amount_mxn
                })
                self.results["imported"] += 1
                
            except Exception as e:
                logger.error("Batch cost import error", index=index, error=str(e))
                self.results["errors"].append({
                    "index": index,
                    "record": record,
                    "error": str(e)
                })
                self.results["failed"] += 1
        
        return self.results
    
    async def import_inventory(self, records: List[Dict[str, Any]], ranch_id: str) -> Dict[str, Any]:
        """Import multiple inventory records"""
        self.results["total"] = len(records)
        
        for index, record in enumerate(records):
            try:
                # Add ranch_id
                record["ranch_id"] = ranch_id
                
                # Validate required fields
                if not record.get("name"):
                    raise ValueError("name is required")
                if not record.get("quantity"):
                    raise ValueError("quantity is required")
                if not record.get("unit"):
                    raise ValueError("unit is required")
                
                # Create inventory item
                item = create_inventory_item(self.db, **record)
                
                self.results["success"].append({
                    "index": index,
                    "id": item.id,
                    "name": item.name
                })
                self.results["imported"] += 1
                
            except Exception as e:
                logger.error("Batch inventory import error", index=index, error=str(e))
                self.results["errors"].append({
                    "index": index,
                    "record": record,
                    "error": str(e)
                })
                self.results["failed"] += 1
        
        return self.results


def get_batch_importer(db: Session) -> BatchImporter:
    """Get batch importer instance"""
    return BatchImporter(db)
