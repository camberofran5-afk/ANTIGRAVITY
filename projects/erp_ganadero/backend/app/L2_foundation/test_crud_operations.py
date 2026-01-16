
import pytest
from unittest.mock import MagicMock, AsyncMock
from datetime import datetime
from app.L2_foundation.cattle_crud import CattleCRUD
from app.L1_config.cattle_types import AnimalCreate, AnimalUpdate, Status, Species, Gender

@pytest.fixture
def mock_supabase():
    client = MagicMock()
    
    # Common mock data that satisfies Pydantic validation
    base_animal = {
        "id": "test-uuid",
        "arete_number": "TEST-001",
        "ranch_id": "ranch-1",
        "species": "vaca",  # Matches Species.VACA.value
        "gender": "F",      # Matches Gender.F.value
        "status": "active",
        "birth_date": "2023-01-01",
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat(),
        "weight_kg": 100.0,
        "photo_url": None,
        "mother_id": None,
        "notes": None
    }

    # Mock the chain: table().insert().execute()
    client.table.return_value.insert.return_value.execute.return_value.data = [base_animal]
    
    # Mock Select
    client.table.return_value.select.return_value.eq.return_value.execute.return_value.data = [base_animal]
    
    # Mock Update
    updated_animal = base_animal.copy()
    updated_animal["status"] = "sold"
    client.table.return_value.update.return_value.eq.return_value.execute.return_value.data = [updated_animal]
    
    return client

@pytest.mark.asyncio
async def test_create_animal(mock_supabase):
    crud = CattleCRUD(supabase=mock_supabase)
    new_animal = AnimalCreate(
        arete_number="TEST-001",
        ranch_id="ranch-1",
        species=Species.VACA, # Corrected Enum
        gender=Gender.F,      # Corrected Enum
        birth_date="2023-01-01"
    )
    
    result = await crud.create(new_animal)
    
    assert result.arete_number == "TEST-001"
    assert result.id == "test-uuid"
    assert result.gender == Gender.F
    mock_supabase.table.assert_called_with("cattle")

@pytest.mark.asyncio
async def test_get_animal(mock_supabase):
    crud = CattleCRUD(supabase=mock_supabase)
    # Configure mock for specific call pattern if needed, or rely on fixture
    
    result = await crud.get_by_id("test-uuid")
    
    assert result is not None
    assert result.id == "test-uuid"
    assert result.species == Species.VACA

@pytest.mark.asyncio
async def test_update_animal(mock_supabase):
    crud = CattleCRUD(supabase=mock_supabase)
    update = AnimalUpdate(status=Status.SOLD)
    
    result = await crud.update("test-uuid", update)
    
    assert result.status == Status.SOLD
