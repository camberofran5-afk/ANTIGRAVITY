"""
Mock Supabase Client for Testing Without Real Database

This allows the app to run and be tested without a real Supabase instance.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
import uuid


class MockResponse:
    """Mock Supabase response"""
    def __init__(self, data: List[Dict] = None, count: int = None):
        self.data = data or []
        self.count = count or len(self.data)


class MockTable:
    """Mock Supabase table"""
    def __init__(self, name: str, storage: Dict):
        self.name = name
        self.storage = storage
        self._query = {}
        self._filters = []
    
    def select(self, columns: str = "*", count: str = None):
        """Mock select"""
        self._query["select"] = columns
        self._query["count"] = count
        return self
    
    def insert(self, data: Dict):
        """Mock insert"""
        if "id" not in data:
            data["id"] = str(uuid.uuid4())
        self.storage[self.name].append(data)
        return MockResponse([data])
    
    def update(self, data: Dict):
        """Mock update"""
        # Find and update matching records
        updated = []
        for item in self.storage[self.name]:
            matches = all(
                item.get(k) == v 
                for k, v in self._filters
            )
            if matches:
                item.update(data)
                updated.append(item)
        return MockResponse(updated)
    
    def eq(self, column: str, value: Any):
        """Mock equality filter"""
        self._filters.append((column, value))
        return self
    
    def order(self, column: str, desc: bool = False):
        """Mock order"""
        self._query["order"] = (column, desc)
        return self
    
    def limit(self, count: int):
        """Mock limit"""
        self._query["limit"] = count
        return self
    
    def range(self, start: int, end: int):
        """Mock range"""
        self._query["range"] = (start, end)
        return self
    
    def execute(self):
        """Execute query"""
        results = self.storage[self.name]
        
        # Apply filters
        for column, value in self._filters:
            results = [r for r in results if r.get(column) == value]
        
        # Apply order
        if "order" in self._query:
            column, desc = self._query["order"]
            results = sorted(
                results, 
                key=lambda x: x.get(column, ""),
                reverse=desc
            )
        
        # Apply range/limit
        if "range" in self._query:
            start, end = self._query["range"]
            results = results[start:end+1]
        elif "limit" in self._query:
            results = results[:self._query["limit"]]
        
        # Reset for next query
        self._filters = []
        self._query = {}
        
        return MockResponse(results, len(results))


class MockSupabaseClient:
    """Mock Supabase client with in-memory storage"""
    
    def __init__(self):
        # In-memory storage
        self.storage = {
            "ranches": [
                {
                    "id": "ranch-1",
                    "name": "Rancho San José",
                    "owner_id": "user-1",
                    "created_at": datetime.now().isoformat()
                }
            ],
            "cattle": [
                {
                    "id": "cattle-1",
                    "ranch_id": "ranch-1",
                    "arete_number": "TX-452",
                    "species": "vaca",
                    "gender": "F",
                    "birth_date": "2020-05-15",
                    "weight_kg": 520.0,
                    "status": "active",
                    "created_at": datetime.now().isoformat(),
                    "updated_at": datetime.now().isoformat()
                },
                {
                    "id": "cattle-2",
                    "ranch_id": "ranch-1",
                    "arete_number": "TX-789",
                    "species": "toro",
                    "gender": "M",
                    "birth_date": "2019-02-10",
                    "weight_kg": 840.0,
                    "status": "active",
                    "created_at": datetime.now().isoformat(),
                    "updated_at": datetime.now().isoformat()
                },
                {
                    "id": "cattle-3",
                    "ranch_id": "ranch-1",
                    "arete_number": "BEC-102",
                    "species": "becerro",
                    "gender": "F",
                    "birth_date": "2024-01-20",
                    "weight_kg": 95.0,
                    "status": "active",
                    "mother_id": "cattle-1",
                    "created_at": datetime.now().isoformat(),
                    "updated_at": datetime.now().isoformat()
                }
            ],
            "events": [
                {
                    "id": "event-1",
                    "cattle_id": "cattle-3",
                    "type": "birth",
                    "event_date": "2024-01-20",
                    "data": {"weight_kg": 35, "mother_id": "cattle-1"},
                    "created_at": datetime.now().isoformat()
                },
                {
                    "id": "event-2",
                    "cattle_id": "cattle-1",
                    "type": "weighing",
                    "event_date": "2024-01-15",
                    "data": {"weight_kg": 520},
                    "created_at": datetime.now().isoformat()
                }
            ],
            "costs": [],
            "user_profiles": [],
            "sync_queue": []
        }
    
    def table(self, name: str):
        """Get table"""
        if name not in self.storage:
            self.storage[name] = []
        return MockTable(name, self.storage)


# Singleton instance
_mock_client = None


def get_mock_supabase():
    """Get mock Supabase client"""
    global _mock_client
    if _mock_client is None:
        _mock_client = MockSupabaseClient()
    return _mock_client
