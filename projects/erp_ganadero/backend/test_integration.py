"""
ERP Ganadero V2 - Integration Tests
Agent 7 (QA Specialist) - Comprehensive Testing Suite

Tests all API endpoints and Reports module integration
"""

import pytest
import httpx
from datetime import datetime, date

BASE_URL = "http://localhost:8000/api/v1"
RANCH_ID = "ranch-1"


class TestInventoryAPI:
    """Test Inventory CRUD operations"""
    
    @pytest.mark.asyncio
    async def test_create_inventory_item(self):
        async with httpx.AsyncClient() as client:
            data = {
                "ranch_id": RANCH_ID,
                "category": "feed",
                "name": "Alfalfa Premium",
                "quantity": 500,
                "unit": "kg",
                "unit_cost": 15.5,
                "min_stock": 100
            }
            response = await client.post(f"{BASE_URL}/inventory", json=data)
            assert response.status_code == 200
            result = response.json()
            assert result["name"] == "Alfalfa Premium"
            assert result["total_value"] == 7750  # 500 * 15.5
            return result["id"]
    
    @pytest.mark.asyncio
    async def test_list_inventory(self):
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{BASE_URL}/inventory?ranch_id={RANCH_ID}")
            assert response.status_code == 200
            items = response.json()
            assert isinstance(items, list)


class TestClientsAPI:
    """Test Clients CRUD operations"""
    
    @pytest.mark.asyncio
    async def test_create_client(self):
        async with httpx.AsyncClient() as client:
            data = {
                "ranch_id": RANCH_ID,
                "name": "Engorda del Norte",
                "type": "feedlot",
                "payment_terms": "30_days",
                "phone": "555-1234",
                "email": "contacto@engordadelnorte.com"
            }
            response = await client.post(f"{BASE_URL}/clients", json=data)
            assert response.status_code == 200
            result = response.json()
            assert result["name"] == "Engorda del Norte"
            assert result["type"] == "feedlot"
            return result["id"]
    
    @pytest.mark.asyncio
    async def test_list_clients(self):
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{BASE_URL}/clients?ranch_id={RANCH_ID}")
            assert response.status_code == 200
            clients = response.json()
            assert isinstance(clients, list)


class TestCostsAPI:
    """Test Costs CRUD operations"""
    
    @pytest.mark.asyncio
    async def test_create_cost(self):
        async with httpx.AsyncClient() as client:
            data = {
                "ranch_id": RANCH_ID,
                "category": "feed",
                "amount_mxn": 7750,
                "cost_date": "2026-01-13",
                "description": "Compra de alfalfa"
            }
            response = await client.post(f"{BASE_URL}/costs", json=data)
            assert response.status_code == 200
            result = response.json()
            assert result["amount_mxn"] == 7750
            return result["id"]
    
    @pytest.mark.asyncio
    async def test_list_costs(self):
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{BASE_URL}/costs?ranch_id={RANCH_ID}")
            assert response.status_code == 200
            costs = response.json()
            assert isinstance(costs, list)
    
    @pytest.mark.asyncio
    async def test_filter_costs_by_date(self):
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{BASE_URL}/costs?ranch_id={RANCH_ID}&start_date=2026-01-01&end_date=2026-01-31"
            )
            assert response.status_code == 200
            costs = response.json()
            assert isinstance(costs, list)


class TestEventsAPI:
    """Test Events API with ranch filtering"""
    
    @pytest.mark.asyncio
    async def test_list_events_by_ranch(self):
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{BASE_URL}/events?ranch_id={RANCH_ID}")
            assert response.status_code == 200
            events = response.json()
            assert isinstance(events, list)
    
    @pytest.mark.asyncio
    async def test_filter_events_by_type(self):
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{BASE_URL}/events?ranch_id={RANCH_ID}&event_type=sale"
            )
            assert response.status_code == 200
            events = response.json()
            assert isinstance(events, list)


class TestHealthCheck:
    """Test backend health"""
    
    @pytest.mark.asyncio
    async def test_health_endpoint(self):
        async with httpx.AsyncClient() as client:
            response = await client.get("http://localhost:8000/health")
            assert response.status_code == 200
            result = response.json()
            assert result["status"] == "healthy"
            assert result["app"] == "ERP Ganadero"


class TestReportsIntegration:
    """Integration tests for Reports module data flow"""
    
    @pytest.mark.asyncio
    async def test_reports_data_pipeline(self):
        """Test complete data pipeline for Reports module"""
        async with httpx.AsyncClient() as client:
            # Fetch all data like Reports component does
            animals = await client.get(f"{BASE_URL}/cattle?ranch_id={RANCH_ID}&limit=100")
            events = await client.get(f"{BASE_URL}/events?ranch_id={RANCH_ID}&limit=1000")
            inventory = await client.get(f"{BASE_URL}/inventory?ranch_id={RANCH_ID}")
            clients = await client.get(f"{BASE_URL}/clients?ranch_id={RANCH_ID}")
            costs = await client.get(f"{BASE_URL}/costs?ranch_id={RANCH_ID}")
            
            # Verify all endpoints respond
            assert animals.status_code == 200
            assert events.status_code == 200
            assert inventory.status_code == 200
            assert clients.status_code == 200
            assert costs.status_code == 200
            
            # Verify data structure
            assert isinstance(animals.json(), list)
            assert isinstance(events.json(), list)
            assert isinstance(inventory.json(), list)
            assert isinstance(clients.json(), list)
            assert isinstance(costs.json(), list)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--asyncio-mode=auto"])
