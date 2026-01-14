"""
Cattle CRUD Operations - Database Version

Database operations for cattle management using SQLAlchemy.
"""

from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
import uuid

from ..L1_config.models import Animal as DBAnimal, AnimalStatus, AnimalSpecies, Gender
from ..L1_config.cattle_types import AnimalCreate, AnimalUpdate, Status, Species


def create_animal(db: Session, animal_data: AnimalCreate) -> DBAnimal:
    """
    Create new animal in database
    
    Args:
        db: Database session
        animal_data: Animal creation data
    
    Returns:
        Created animal
    """
    db_animal = DBAnimal(
        id=str(uuid.uuid4()),
        ranch_id=animal_data.ranch_id,
        arete_number=animal_data.arete_number,
        species=AnimalSpecies(animal_data.species.value),
        gender=Gender(animal_data.gender.value),
        birth_date=animal_data.birth_date,
        weight_kg=animal_data.weight_kg,
        photo_url=animal_data.photo_url,
        status=AnimalStatus(animal_data.status.value) if animal_data.status else AnimalStatus.ACTIVE,
        mother_id=animal_data.mother_id,
        notes=animal_data.notes
    )
    
    db.add(db_animal)
    db.commit()
    db.refresh(db_animal)
    
    return db_animal


def get_animal(db: Session, animal_id: str) -> Optional[DBAnimal]:
    """Get animal by ID"""
    return db.query(DBAnimal).filter(DBAnimal.id == animal_id).first()


def list_animals(
    db: Session,
    ranch_id: str,
    status: Optional[Status] = None,
    species: Optional[Species] = None,
    limit: int = 50,
    offset: int = 0
) -> List[DBAnimal]:
    """
    List animals with filters
    
    Args:
        db: Database session
        ranch_id: Ranch ID to filter by
        status: Optional status filter
        species: Optional species filter
        limit: Maximum number of results
        offset: Number of results to skip
    
    Returns:
        List of animals
    """
    query = db.query(DBAnimal).filter(DBAnimal.ranch_id == ranch_id)
    
    if status:
        query = query.filter(DBAnimal.status == AnimalStatus(status.value))
    
    if species:
        query = query.filter(DBAnimal.species == AnimalSpecies(species.value))
    
    return query.offset(offset).limit(limit).all()


def update_animal(
    db: Session,
    animal_id: str,
    animal_data: AnimalUpdate
) -> Optional[DBAnimal]:
    """
    Update animal
    
    Args:
        db: Database session
        animal_id: Animal ID
        animal_data: Update data
    
    Returns:
        Updated animal or None if not found
    """
    db_animal = get_animal(db, animal_id)
    if not db_animal:
        return None
    
    # Update fields if provided
    update_data = animal_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        if field == "status" and value:
            setattr(db_animal, field, AnimalStatus(value.value))
        else:
            setattr(db_animal, field, value)
    
    db.commit()
    db.refresh(db_animal)
    
    return db_animal


def delete_animal(db: Session, animal_id: str) -> bool:
    """
    Delete animal
    
    Args:
        db: Database session
        animal_id: Animal ID
    
    Returns:
        True if deleted, False if not found
    """
    db_animal = get_animal(db, animal_id)
    if not db_animal:
        return False
    
    db.delete(db_animal)
    db.commit()
    
    return True


def count_animals(db: Session, ranch_id: str, status: Optional[Status] = None) -> int:
    """Count animals by ranch and optional status"""
    query = db.query(DBAnimal).filter(DBAnimal.ranch_id == ranch_id)
    
    if status:
        query = query.filter(DBAnimal.status == AnimalStatus(status.value))
    
    return query.count()
