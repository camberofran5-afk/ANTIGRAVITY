"""
Inventory CRUD Operations - Database Version

Database operations for inventory management using SQLAlchemy.
"""

from sqlalchemy.orm import Session
from typing import List, Optional
import uuid

from ..L1_config.models import InventoryItem as DBInventoryItem


def create_inventory_item(
    db: Session,
    ranch_id: str,
    category: str,
    name: str,
    quantity: float,
    unit: str,
    unit_cost: Optional[float] = None,
    min_stock: Optional[float] = None,
    supplier: Optional[str] = None,
    notes: Optional[str] = None
) -> DBInventoryItem:
    """Create new inventory item"""
    db_item = DBInventoryItem(
        id=str(uuid.uuid4()),
        ranch_id=ranch_id,
        category=category,
        name=name,
        quantity=quantity,
        unit=unit,
        unit_cost=unit_cost,
        min_stock=min_stock,
        supplier=supplier,
        notes=notes
    )
    
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    
    return db_item


def get_inventory_item(db: Session, item_id: str) -> Optional[DBInventoryItem]:
    """Get inventory item by ID"""
    return db.query(DBInventoryItem).filter(DBInventoryItem.id == item_id).first()


def list_inventory(
    db: Session,
    ranch_id: str,
    category: Optional[str] = None,
    low_stock_only: bool = False,
    limit: int = 100,
    offset: int = 0
) -> List[DBInventoryItem]:
    """List inventory items with filters"""
    query = db.query(DBInventoryItem).filter(DBInventoryItem.ranch_id == ranch_id)
    
    if category:
        query = query.filter(DBInventoryItem.category == category)
    
    if low_stock_only:
        query = query.filter(DBInventoryItem.quantity <= DBInventoryItem.min_stock)
    
    return query.offset(offset).limit(limit).all()


def update_inventory_item(
    db: Session,
    item_id: str,
    quantity: Optional[float] = None,
    unit_cost: Optional[float] = None,
    min_stock: Optional[float] = None,
    notes: Optional[str] = None
) -> Optional[DBInventoryItem]:
    """Update inventory item"""
    db_item = get_inventory_item(db, item_id)
    if not db_item:
        return None
    
    if quantity is not None:
        db_item.quantity = quantity
    if unit_cost is not None:
        db_item.unit_cost = unit_cost
    if min_stock is not None:
        db_item.min_stock = min_stock
    if notes is not None:
        db_item.notes = notes
    
    db.commit()
    db.refresh(db_item)
    
    return db_item


def delete_inventory_item(db: Session, item_id: str) -> bool:
    """Delete inventory item"""
    db_item = get_inventory_item(db, item_id)
    if not db_item:
        return False
    
    db.delete(db_item)
    db.commit()
    
    return True
