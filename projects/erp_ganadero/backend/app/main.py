"""
ERP Ganadero - FastAPI Main Application (L4 Synthesis)

Main FastAPI application with all routes.
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from sqlalchemy.orm import Session

from .L1_config.system_config import APP_NAME, APP_VERSION, API_PREFIX, CORS_ORIGINS
from .L1_config.database import get_db, init_db
from .L1_config.cattle_types import (
    Animal, AnimalCreate, AnimalUpdate,
    Event, EventCreate,
    HerdMetrics, HerdSummary,
    Status, Species
)
from .L1_config.auth_types import UserRegister, UserLogin, Token, UserResponse, RanchCreate, RanchResponse
from .L2_foundation.cattle_crud import get_cattle_crud, CattleCRUD
from .L2_foundation.event_crud import get_event_crud, EventCRUD
from .L2_foundation.auth_service import create_access_token, get_current_user
from .L2_foundation.user_crud import create_user, authenticate_user, get_user_ranches, create_ranch
from .L1_config.models import User
from .L3_analysis.kpi_calculator import get_kpi_calculator, KPICalculator
import structlog

logger = structlog.get_logger()

# Create FastAPI app
app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description="Cattle management ERP for Mexican ranchers"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for demo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    """Initialize database on application startup"""
    logger.info("app_starting", app=APP_NAME, version=APP_VERSION)
    init_db()
    logger.info("database_initialized")


# ============================================================================
# Health Check
# ============================================================================

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "app": APP_NAME,
        "version": APP_VERSION
    }


# ============================================================================
# Authentication Endpoints
# ============================================================================

@app.post(f"{API_PREFIX}/auth/register", response_model=Token)
async def register(user_data: UserRegister, db: Session = Depends(get_db)):
    """
    Register new user
    
    Creates user account and returns JWT token
    """
    try:
        # Create user
        user = create_user(db, user_data)
        
        # Create default ranch for user
        default_ranch = create_ranch(
            db,
            RanchCreate(name=f"{user.full_name}'s Ranch", location=""),
            owner_id=user.id
        )
        
        # Generate token
        access_token = create_access_token(
            data={"user_id": user.id, "email": user.email}
        )
        
        logger.info("user_registered", user_id=user.id, email=user.email)
        
        return Token(
            access_token=access_token,
            user={
                "id": user.id,
                "email": user.email,
                "full_name": user.full_name,
                "default_ranch_id": default_ranch.id
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error("registration_failed", error=str(e))
        raise HTTPException(status_code=500, detail="Registration failed")


@app.post(f"{API_PREFIX}/auth/login", response_model=Token)
async def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """
    Login user
    
    Validates credentials and returns JWT token
    """
    try:
        # Authenticate user
        user = authenticate_user(db, credentials.email, credentials.password)
        
        if not user:
            raise HTTPException(
                status_code=401,
                detail="Incorrect email or password"
            )
        
        # Get user's ranches
        ranches = get_user_ranches(db, user.id)
        default_ranch_id = ranches[0].id if ranches else None
        
        # Generate token
        access_token = create_access_token(
            data={"user_id": user.id, "email": user.email}
        )
        
        logger.info("user_logged_in", user_id=user.id, email=user.email)
        
        return Token(
            access_token=access_token,
            user={
                "id": user.id,
                "email": user.email,
                "full_name": user.full_name,
                "default_ranch_id": default_ranch_id
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error("login_failed", error=str(e))
        raise HTTPException(status_code=500, detail="Login failed")


@app.get(f"{API_PREFIX}/auth/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    """Get current authenticated user"""
    return current_user


@app.get(f"{API_PREFIX}/ranches", response_model=List[RanchResponse])
async def list_ranches(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all ranches accessible to current user"""
    ranches = get_user_ranches(db, current_user.id)
    return ranches


@app.post(f"{API_PREFIX}/ranches", response_model=RanchResponse)
async def create_new_ranch(
    ranch_data: RanchCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create new ranch for current user"""
    ranch = create_ranch(db, ranch_data, current_user.id)
    logger.info("ranch_created", ranch_id=ranch.id, user_id=current_user.id)
    return ranch


# ============================================================================
# Batch Import Endpoints
# ============================================================================

@app.post(f"{API_PREFIX}/batch/cattle")
async def batch_import_cattle(
    records: List[dict],
    ranch_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Batch import cattle records"""
    from .L2_foundation.batch_import import get_batch_importer
    
    importer = get_batch_importer(db)
    results = await importer.import_cattle(records, ranch_id)
    
    logger.info("batch_cattle_import", 
                total=results["total"],
                imported=results["imported"],
                failed=results["failed"])
    
    return results


@app.post(f"{API_PREFIX}/batch/costs")
async def batch_import_costs(
    records: List[dict],
    ranch_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Batch import cost records"""
    from .L2_foundation.batch_import import get_batch_importer
    
    importer = get_batch_importer(db)
    results = await importer.import_costs(records, ranch_id)
    
    logger.info("batch_cost_import",
                total=results["total"],
                imported=results["imported"],
                failed=results["failed"])
    
    return results


@app.post(f"{API_PREFIX}/batch/inventory")
async def batch_import_inventory(
    records: List[dict],
    ranch_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Batch import inventory records"""
    from .L2_foundation.batch_import import get_batch_importer
    
    importer = get_batch_importer(db)
    results = await importer.import_inventory(records, ranch_id)
    
    logger.info("batch_inventory_import",
                total=results["total"],
                imported=results["imported"],
                failed=results["failed"])
    
    return results


# ============================================================================
# AI Parsing Endpoints
# ============================================================================

@app.post(f"{API_PREFIX}/ai/parse-cost")
async def parse_cost_text(
    text: str,
    current_user: User = Depends(get_current_user)
):
    """Parse cost description using AI"""
    from .L4_synthesis.ai_provider import get_ai_provider
    from .L4_synthesis.data_parser import DataParser
    
    ai_provider = get_ai_provider()
    parser = DataParser(ai_provider)
    
    result = await parser.parse_cost_text(text)
    
    logger.info("ai_cost_parsing", confidence=result.get("confidence", 0))
    
    return result


@app.post(f"{API_PREFIX}/ai/parse-event")
async def parse_event_text(
    text: str,
    current_user: User = Depends(get_current_user)
):
    """Parse event description using AI"""
    from .L4_synthesis.ai_provider import get_ai_provider
    from .L4_synthesis.data_parser import DataParser
    
    ai_provider = get_ai_provider()
    parser = DataParser(ai_provider)
    
    result = await parser.parse_event_text(text)
    
    logger.info("ai_event_parsing", confidence=result.get("confidence", 0))
    
    return result


# ============================================================================
# Cattle Endpoints
# ============================================================================

@app.post(f"{API_PREFIX}/cattle", response_model=Animal)
async def create_animal(
    animal: AnimalCreate,
    crud: CattleCRUD = Depends(get_cattle_crud)
):
    """Create new animal"""
    try:
        return await crud.create(animal)
    except Exception as e:
        logger.error("create_animal_failed", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@app.get(f"{API_PREFIX}/cattle", response_model=List[Animal])
async def list_cattle(
    ranch_id: str,
    status: Optional[Status] = None,
    species: Optional[Species] = None,
    limit: int = 50,
    offset: int = 0,
    crud: CattleCRUD = Depends(get_cattle_crud)
):
    """List cattle with filters"""
    try:
        return await crud.list_by_ranch(
            ranch_id=ranch_id,
            status=status,
            species=species,
            limit=limit,
            offset=offset
        )
    except Exception as e:
        logger.error("list_cattle_failed", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@app.get(f"{API_PREFIX}/cattle/{{cattle_id}}", response_model=Animal)
async def get_animal(
    cattle_id: str,
    crud: CattleCRUD = Depends(get_cattle_crud)
):
    """Get animal by ID"""
    animal = await crud.get_by_id(cattle_id)
    if not animal:
        raise HTTPException(status_code=404, detail="Animal not found")
    return animal


@app.put(f"{API_PREFIX}/cattle/{{cattle_id}}", response_model=Animal)
async def update_animal(
    cattle_id: str,
    update: AnimalUpdate,
    crud: CattleCRUD = Depends(get_cattle_crud)
):
    """Update animal"""
    try:
        return await crud.update(cattle_id, update)
    except Exception as e:
        logger.error("update_animal_failed", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@app.delete(f"{API_PREFIX}/cattle/{{cattle_id}}")
async def delete_animal(
    cattle_id: str,
    crud: CattleCRUD = Depends(get_cattle_crud)
):
    """Delete animal (soft delete)"""
    try:
        await crud.delete(cattle_id)
        return {"status": "deleted"}
    except Exception as e:
        logger.error("delete_animal_failed", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# Event Endpoints
# ============================================================================

@app.post(f"{API_PREFIX}/events", response_model=Event)
async def create_event(
    event: EventCreate,
    crud: EventCRUD = Depends(get_event_crud)
):
    """Create new event"""
    try:
        return await crud.create(event)
    except Exception as e:
        logger.error("create_event_failed", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@app.get(f"{API_PREFIX}/events", response_model=List[Event])
async def list_events(
    cattle_id: Optional[str] = None,
    ranch_id: Optional[str] = None,
    event_type: Optional[str] = None,
    limit: int = 100,
    crud: EventCRUD = Depends(get_event_crud)
):
    """List events with optional filtering by cattle_id, ranch_id, or event_type"""
    try:
        if cattle_id:
            events = await crud.get_by_cattle(cattle_id)
        elif ranch_id:
            # Get all cattle for this ranch, then get their events
            from .L2_foundation.cattle_crud import get_cattle_crud
            cattle_crud = get_cattle_crud()
            animals = await cattle_crud.list_by_ranch(ranch_id, limit=1000)
            events = []
            for animal in animals:
                animal_events = await crud.get_by_cattle(animal.id)
                events.extend(animal_events)
        else:
            # No filter - return empty for safety
            events = []
        
        # Filter by event type if specified
        if event_type:
            events = [e for e in events if e.type == event_type]
        
        # Sort by date descending
        events.sort(key=lambda e: e.event_date, reverse=True)
        
        return events[:limit]
    except Exception as e:
        logger.error("list_events_failed", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


# NEW: Cattle-specific event endpoints for individual animal tracking
@app.get(f"{API_PREFIX}/cattle/{{cattle_id}}/events", response_model=List[Event])
async def get_cattle_events(
    cattle_id: str,
    event_type: Optional[str] = None,
    limit: int = 100,
    crud: EventCRUD = Depends(get_event_crud)
):
    """Get all events for a specific animal, sorted by date (newest first)"""
    try:
        events = await crud.get_by_cattle(cattle_id)
        
        # Filter by event type if specified
        if event_type:
            events = [e for e in events if e.type == event_type]
        
        # Sort by date descending (newest first)
        events.sort(key=lambda e: e.event_date, reverse=True)
        
        return events[:limit]
    except Exception as e:
        logger.error("get_cattle_events_failed", cattle_id=cattle_id, error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@app.get(f"{API_PREFIX}/cattle/{{cattle_id}}/weight-history")
async def get_cattle_weight_history(
    cattle_id: str,
    crud: EventCRUD = Depends(get_event_crud)
):
    """Get weight history for a specific animal (for charting)"""
    try:
        # Get all events for this animal
        all_events = await crud.get_by_cattle(cattle_id)
        
        # Filter to weighing and birth events (which have weight data)
        weight_events = []
        for event in all_events:
            if event.type == "weighing" and event.data.get("weight_kg"):
                weight_events.append({
                    "date": str(event.event_date),
                    "weight_kg": event.data["weight_kg"],
                    "type": "weighing"
                })
            elif event.type == "birth" and event.data.get("calf_weight_kg"):
                weight_events.append({
                    "date": str(event.event_date),
                    "weight_kg": event.data["calf_weight_kg"],
                    "type": "birth"
                })
        
        # Sort by date ascending (oldest first for chart)
        weight_events.sort(key=lambda e: e["date"])
        
        return {
            "cattle_id": cattle_id,
            "measurements": weight_events,
            "count": len(weight_events)
        }
    except Exception as e:
        logger.error("get_weight_history_failed", cattle_id=cattle_id, error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# Metrics Endpoints
# ============================================================================

@app.get(f"{API_PREFIX}/metrics/kpis", response_model=HerdMetrics)
async def get_kpis(
    ranch_id: str,
    calculator: KPICalculator = Depends(get_kpi_calculator)
):
    """Get herd KPIs"""
    try:
        return await calculator.calculate_herd_metrics(ranch_id)
    except Exception as e:
        logger.error("get_kpis_failed", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@app.get(f"{API_PREFIX}/metrics/summary", response_model=HerdSummary)
async def get_summary(
    ranch_id: str,
    crud: CattleCRUD = Depends(get_cattle_crud)
):
    """Get herd summary for dashboard"""
    try:
        total = await crud.count_by_ranch(ranch_id, Status.ACTIVE)
        productive = await crud.get_productive_count(ranch_id)
        unproductive = total - productive
        
        # Mock data for other fields
        return HerdSummary(
            total_animals=total,
            productive_count=productive,
            unproductive_count=unproductive,
            ready_to_wean_count=12,  # TODO: Calculate from events
            recent_births=5,  # TODO: Count recent birth events
            recent_deaths=1,  # TODO: Count recent death events
            week_cost_usd=1450.50  # TODO: Calculate from costs
        )
    except Exception as e:
        logger.error("get_summary_failed", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# Startup
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Startup tasks"""
    logger.info("app_starting", app=APP_NAME, version=APP_VERSION)


@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown tasks"""
    logger.info("app_shutting_down")




# ============================================================================
# AI Analytics Endpoints
# ============================================================================

from app.L4_synthesis.ai_analytics import AIAnalyticsService

# Initialize AI service
ai_service = AIAnalyticsService(provider_name="gemini")


@app.get(f"{API_PREFIX}/analytics/health")
async def get_health_insights(ranch_id: str = "ranch-1"):
    """Get AI-powered health insights"""
    try:
        # TODO: Get real metrics from database
        metrics = {
            "calf_mortality": 4.2,
            "recent_deaths": 3,
            "vaccination_rate": 85,
            "herd_size": 150
        }
        
        insights = await ai_service.analyze_health(metrics)
        return insights
    except Exception as e:
        logger.error("health_insights_failed", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@app.get(f"{API_PREFIX}/analytics/reproduction")
async def get_reproduction_insights(ranch_id: str = "ranch-1"):
    """Get AI-powered reproductive performance insights"""
    try:
        # TODO: Get real metrics from database
        metrics = {
            "pregnancy_rate": 78,
            "calving_interval": 385,
            "open_cows": 12,
            "herd_size": 150
        }
        
        insights = await ai_service.analyze_reproduction(metrics)
        return insights
    except Exception as e:
        logger.error("reproduction_insights_failed", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@app.get(f"{API_PREFIX}/analytics/financial")
async def get_financial_insights(ranch_id: str = "ranch-1"):
    """Get AI-powered financial insights"""
    try:
        # TODO: Get real metrics from database
        metrics = {
            "total_costs": 45000,
            "revenue": 62000,
            "margin": 27.4,
            "cost_per_kg": 2.85,
            "cost_trend": "increasing"
        }
        
        insights = await ai_service.analyze_financial(metrics)
        return insights
    except Exception as e:
        logger.error("financial_insights_failed", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@app.get(f"{API_PREFIX}/analytics/growth")
async def get_growth_insights(ranch_id: str = "ranch-1"):
    """Get AI-powered growth & production insights"""
    try:
        # TODO: Get real metrics from database
        metrics = {
            "avg_daily_gain": 0.8,
            "weaning_weight": 195,
            "feed_efficiency": "moderate",
            "herd_size": 150
        }
        
        insights = await ai_service.analyze_growth(metrics)
        return insights
    except Exception as e:
        logger.error("growth_insights_failed", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@app.get(f"{API_PREFIX}/analytics/cache-stats")
async def get_cache_stats():
    """Get AI cache statistics"""
    return ai_service.get_cache_stats()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)



# ============================================================================
# V2 Additional Endpoints (Costs, Inventory, Clients, Workers)
# ============================================================================

from .L1_config.v2_types import (
    InventoryItem, InventoryItemCreate,
    Client, ClientCreate,
    Worker, WorkerCreate
)
from datetime import datetime
from uuid import uuid4
from typing import Dict, List, Optional

# ============================================================================
# Costs Endpoints
# ============================================================================

@app.post(f"{API_PREFIX}/costs", status_code=201)
async def create_cost(
    ranch_id: str,
    category: str,
    amount_mxn: float,
    cost_date: str,
    description: Optional[str] = None,
    cattle_id: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create new cost entry"""
    from .L2_foundation.cost_crud_db import create_cost as db_create_cost
    from datetime import datetime
    
    cost = db_create_cost(
        db=db,
        ranch_id=ranch_id,
        category=category,
        amount_mxn=amount_mxn,
        cost_date=datetime.fromisoformat(cost_date).date(),
        description=description,
        cattle_id=cattle_id
    )
    
    logger.info("cost_created", cost_id=cost.id, ranch_id=ranch_id)
    
    return {
        "id": cost.id,
        "ranch_id": cost.ranch_id,
        "category": cost.category.value,
        "amount_mxn": cost.amount_mxn,
        "description": cost.description,
        "cost_date": cost.cost_date.isoformat(),
        "cattle_id": cost.cattle_id
    }


@app.get(f"{API_PREFIX}/costs")
async def list_costs(
    ranch_id: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    category: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List costs with filters"""
    from .L2_foundation.cost_crud_db import list_costs as db_list_costs
    from datetime import datetime
    
    costs = db_list_costs(
        db=db,
        ranch_id=ranch_id,
        start_date=datetime.fromisoformat(start_date).date() if start_date else None,
        end_date=datetime.fromisoformat(end_date).date() if end_date else None,
        category=category
    )
    
    return [
        {
            "id": cost.id,
            "ranch_id": cost.ranch_id,
            "category": cost.category.value,
            "amount_mxn": cost.amount_mxn,
            "description": cost.description,
            "cost_date": cost.cost_date.isoformat(),
            "cattle_id": cost.cattle_id
        }
        for cost in costs
    ]


@app.delete(f"{API_PREFIX}/costs/{{cost_id}}")
async def delete_cost(
    cost_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete cost"""
    from .L2_foundation.cost_crud_db import delete_cost as db_delete_cost
    
    success = db_delete_cost(db, cost_id)
    if not success:
        raise HTTPException(status_code=404, detail="Cost not found")
    
    return {"status": "deleted"}


@app.post(f"{API_PREFIX}/costs")
async def create_cost(cost: dict):
    """Create cost entry"""
    cost_id = f"cost-{uuid4().hex[:8]}"
    cost_data = {
        "id": cost_id,
        **cost,
        "created_at": datetime.now().isoformat()
    }
    _costs_store[cost_id] = cost_data
    return cost_data


# ============================================================================
# Inventory Endpoints  
# ============================================================================

@app.get(f"{API_PREFIX}/inventory")
async def list_inventory(
    ranch_id: str,
    category: Optional[str] = None,
    low_stock_only: bool = False,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List inventory items for ranch"""
    from .L2_foundation.inventory_crud_db import list_inventory as db_list_inventory
    
    items = db_list_inventory(
        db=db,
        ranch_id=ranch_id,
        category=category,
        low_stock_only=low_stock_only
    )
    
    return [
        {
            "id": item.id,
            "ranch_id": item.ranch_id,
            "category": item.category,
            "name": item.name,
            "quantity": item.quantity,
            "unit": item.unit,
            "unit_cost": item.unit_cost,
            "min_stock": item.min_stock,
            "supplier": item.supplier,
            "notes": item.notes
        }
        for item in items
    ]


@app.post(f"{API_PREFIX}/inventory", status_code=201)
async def create_inventory_item(
    ranch_id: str,
    category: str,
    name: str,
    quantity: float,
    unit: str,
    unit_cost: Optional[float] = None,
    min_stock: Optional[float] = None,
    supplier: Optional[str] = None,
    notes: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create inventory item"""
    from .L2_foundation.inventory_crud_db import create_inventory_item as db_create_item
    
    item = db_create_item(
        db=db,
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
    
    logger.info("inventory_item_created", item_id=item.id, ranch_id=ranch_id)
    
    return {
        "id": item.id,
        "ranch_id": item.ranch_id,
        "category": item.category,
        "name": item.name,
        "quantity": item.quantity,
        "unit": item.unit,
        "unit_cost": item.unit_cost,
        "min_stock": item.min_stock,
        "supplier": item.supplier,
        "notes": item.notes
    }


@app.delete(f"{API_PREFIX}/inventory/{{item_id}}")
async def delete_inventory_item(
    item_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete inventory item"""
    from .L2_foundation.inventory_crud_db import delete_inventory_item as db_delete_item
    
    success = db_delete_item(db, item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Inventory item not found")
    
    return {"status": "deleted"}


@app.put(f"{API_PREFIX}/inventory/{{item_id}}", response_model=InventoryItem)
async def update_inventory_item(item_id: str, update: dict):
    """Update inventory item"""
    if item_id not in _inventory_store:
        raise HTTPException(status_code=404, detail="Item not found")
    
    item = _inventory_store[item_id]
    for key, value in update.items():
        if hasattr(item, key) and key not in ["id", "ranch_id", "created_at"]:
            setattr(item, key, value)
    
    # Recalculate total value
    item.total_value = item.quantity * item.unit_cost
    return item


@app.delete(f"{API_PREFIX}/inventory/{{item_id}}")
async def delete_inventory_item(item_id: str):
    """Delete inventory item"""
    if item_id not in _inventory_store:
        raise HTTPException(status_code=404, detail="Item not found")
    del _inventory_store[item_id]
    return {"status": "deleted"}


# ============================================================================
# Client Endpoints
# ============================================================================

@app.get(f"{API_PREFIX}/clients")
async def list_clients(
    ranch_id: str,
    client_type: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List clients for ranch"""
    from .L2_foundation.client_crud_db import list_clients as db_list_clients
    
    clients = db_list_clients(
        db=db,
        ranch_id=ranch_id,
        client_type=client_type
    )
    
    return [
        {
            "id": client.id,
            "ranch_id": client.ranch_id,
            "name": client.name,
            "type": client.type,
            "contact_name": client.contact_name,
            "phone": client.phone,
            "email": client.email,
            "address": client.address,
            "payment_terms": client.payment_terms,
            "notes": client.notes
        }
        for client in clients
    ]


@app.post(f"{API_PREFIX}/clients", status_code=201)
async def create_client(
    ranch_id: str,
    name: str,
    client_type: Optional[str] = None,
    contact_name: Optional[str] = None,
    phone: Optional[str] = None,
    email: Optional[str] = None,
    address: Optional[str] = None,
    payment_terms: Optional[str] = None,
    notes: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create client"""
    from .L2_foundation.client_crud_db import create_client as db_create_client
    
    client = db_create_client(
        db=db,
        ranch_id=ranch_id,
        name=name,
        client_type=client_type,
        contact_name=contact_name,
        phone=phone,
        email=email,
        address=address,
        payment_terms=payment_terms,
        notes=notes
    )
    
    logger.info("client_created", client_id=client.id, ranch_id=ranch_id)
    
    return {
        "id": client.id,
        "ranch_id": client.ranch_id,
        "name": client.name,
        "type": client.type,
        "contact_name": client.contact_name,
        "phone": client.phone,
        "email": client.email,
        "address": client.address,
        "payment_terms": client.payment_terms,
        "notes": client.notes
    }


@app.put(f"{API_PREFIX}/clients/{{client_id}}", response_model=Client)
async def update_client(client_id: str, update: dict):
    """Update client"""
    if client_id not in _clients_store:
        raise HTTPException(status_code=404, detail="Client not found")
    
    client = _clients_store[client_id]
    for key, value in update.items():
        if hasattr(client, key) and key not in ["id", "ranch_id", "created_at"]:
            setattr(client, key, value)
    return client


@app.delete(f"{API_PREFIX}/clients/{{client_id}}")
async def delete_client(client_id: str):
    """Delete client"""
    if client_id not in _clients_store:
        raise HTTPException(status_code=404, detail="Client not found")
    del _clients_store[client_id]
    return {"status": "deleted"}


# ============================================================================
# Worker Endpoints
# ============================================================================

@app.get(f"{API_PREFIX}/workers")
async def list_workers(
    ranch_id: str,
    active_only: bool = True,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List workers for ranch"""
    from .L2_foundation.worker_crud_db import list_workers as db_list_workers
    
    workers = db_list_workers(
        db=db,
        ranch_id=ranch_id,
        active_only=active_only
    )
    
    return [
        {
            "id": worker.id,
            "ranch_id": worker.ranch_id,
            "full_name": worker.full_name,
            "position": worker.position,
            "phone": worker.phone,
            "email": worker.email,
            "salary_mxn": worker.salary_mxn,
            "hire_date": worker.hire_date.isoformat() if worker.hire_date else None,
            "is_active": worker.is_active,
            "notes": worker.notes
        }
        for worker in workers
    ]


@app.post(f"{API_PREFIX}/workers", status_code=201)
async def create_worker(
    ranch_id: str,
    full_name: str,
    position: Optional[str] = None,
    phone: Optional[str] = None,
    email: Optional[str] = None,
    salary_mxn: Optional[float] = None,
    hire_date: Optional[str] = None,
    notes: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create worker"""
    from .L2_foundation.worker_crud_db import create_worker as db_create_worker
    from datetime import datetime
    
    worker = db_create_worker(
        db=db,
        ranch_id=ranch_id,
        full_name=full_name,
        position=position,
        phone=phone,
        email=email,
        salary_mxn=salary_mxn,
        hire_date=datetime.fromisoformat(hire_date).date() if hire_date else None,
        notes=notes
    )
    
    logger.info("worker_created", worker_id=worker.id, ranch_id=ranch_id)
    
    return {
        "id": worker.id,
        "ranch_id": worker.ranch_id,
        "full_name": worker.full_name,
        "position": worker.position,
        "phone": worker.phone,
        "email": worker.email,
        "salary_mxn": worker.salary_mxn,
        "hire_date": worker.hire_date.isoformat() if worker.hire_date else None,
        "is_active": worker.is_active,
        "notes": worker.notes
    }


@app.put(f"{API_PREFIX}/workers/{{worker_id}}", response_model=Worker)
async def update_worker(worker_id: str, update: dict):
    """Update worker"""
    if worker_id not in _workers_store:
        raise HTTPException(status_code=404, detail="Worker not found")
    
    worker = _workers_store[worker_id]
    for key, value in update.items():
        if hasattr(worker, key) and key not in ["id", "ranch_id", "created_at"]:
            setattr(worker, key, value)
    return worker


@app.delete(f"{API_PREFIX}/workers/{{worker_id}}")
async def delete_worker(worker_id: str):
    """Delete worker"""
    if worker_id not in _workers_store:
        raise HTTPException(status_code=404, detail="Worker not found")
    del _workers_store[worker_id]
    return {"status": "deleted"}
