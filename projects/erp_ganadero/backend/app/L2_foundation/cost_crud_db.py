"""
Cost CRUD Operations - Database Version

Database operations for cost tracking using SQLAlchemy.
"""

from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
import uuid

from ..L1_config.models import Cost as DBCost, CostCategory as DBCostCategory


def create_cost(
    db: Session,
    ranch_id: str,
    category: str,
    amount_mxn: float,
    cost_date: date,
    description: Optional[str] = None,
    cattle_id: Optional[str] = None
) -> DBCost:
    """Create new cost entry"""
    db_cost = DBCost(
        id=str(uuid.uuid4()),
        ranch_id=ranch_id,
        category=DBCostCategory(category),
        amount_mxn=amount_mxn,
        description=description,
        cost_date=cost_date,
        cattle_id=cattle_id
    )
    
    db.add(db_cost)
    db.commit()
    db.refresh(db_cost)
    
    return db_cost


def get_cost(db: Session, cost_id: str) -> Optional[DBCost]:
    """Get cost by ID"""
    return db.query(DBCost).filter(DBCost.id == cost_id).first()


def list_costs(
    db: Session,
    ranch_id: str,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    category: Optional[str] = None,
    limit: int = 100,
    offset: int = 0
) -> List[DBCost]:
    """List costs with filters"""
    query = db.query(DBCost).filter(DBCost.ranch_id == ranch_id)
    
    if start_date:
        query = query.filter(DBCost.cost_date >= start_date)
    
    if end_date:
        query = query.filter(DBCost.cost_date <= end_date)
    
    if category:
        query = query.filter(DBCost.category == DBCostCategory(category))
    
    return query.order_by(DBCost.cost_date.desc()).offset(offset).limit(limit).all()


def delete_cost(db: Session, cost_id: str) -> bool:
    """Delete cost"""
    db_cost = get_cost(db, cost_id)
    if not db_cost:
        return False
    
    db.delete(db_cost)
    db.commit()
    
    return True
