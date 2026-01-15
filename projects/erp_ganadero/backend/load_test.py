"""
Backend Performance Load Test
Tests API performance with 1000+ cattle records
"""

import asyncio
import time
import statistics
from typing import List, Dict
import httpx

API_BASE = "http://127.0.0.1:8000/api/v1"

async def create_test_cattle(count: int = 1000) -> List[str]:
    """Create test cattle records"""
    cattle_ids = []
    
    async with httpx.AsyncClient() as client:
        for i in range(count):
            data = {
                "ranch_id": "test-ranch-1",
                "tag_number": f"TEST-{i:04d}",
                "type": "cow" if i % 3 == 0 else "calf",
                "sex": "female" if i % 2 == 0 else "male",
                "birth_date": f"2023-{(i % 12) + 1:02d}-15",
                "status": "active"
            }
            
            try:
                response = await client.post(f"{API_BASE}/cattle", json=data)
                if response.status_code == 201:
                    cattle_ids.append(response.json()["id"])
            except Exception as e:
                print(f"Error creating cattle {i}: {e}")
    
    return cattle_ids


async def test_list_performance(iterations: int = 100) -> Dict:
    """Test list cattle endpoint performance"""
    response_times = []
    
    async with httpx.AsyncClient() as client:
        for _ in range(iterations):
            start = time.time()
            try:
                response = await client.get(
                    f"{API_BASE}/cattle",
                    params={"ranch_id": "test-ranch-1", "limit": 100}
                )
                elapsed = (time.time() - start) * 1000  # Convert to ms
                if response.status_code == 200:
                    response_times.append(elapsed)
            except Exception as e:
                print(f"Error in request: {e}")
    
    return {
        "endpoint": "GET /cattle",
        "iterations": len(response_times),
        "avg_ms": statistics.mean(response_times) if response_times else 0,
        "min_ms": min(response_times) if response_times else 0,
        "max_ms": max(response_times) if response_times else 0,
        "p95_ms": statistics.quantiles(response_times, n=20)[18] if len(response_times) > 20 else 0,
        "p99_ms": statistics.quantiles(response_times, n=100)[98] if len(response_times) > 100 else 0
    }


async def test_get_by_id_performance(cattle_ids: List[str], iterations: int = 100) -> Dict:
    """Test get cattle by ID performance"""
    response_times = []
    
    async with httpx.AsyncClient() as client:
        for i in range(iterations):
            cattle_id = cattle_ids[i % len(cattle_ids)]
            start = time.time()
            try:
                response = await client.get(f"{API_BASE}/cattle/{cattle_id}")
                elapsed = (time.time() - start) * 1000
                if response.status_code == 200:
                    response_times.append(elapsed)
            except Exception as e:
                print(f"Error in request: {e}")
    
    return {
        "endpoint": "GET /cattle/{id}",
        "iterations": len(response_times),
        "avg_ms": statistics.mean(response_times) if response_times else 0,
        "min_ms": min(response_times) if response_times else 0,
        "max_ms": max(response_times) if response_times else 0,
        "p95_ms": statistics.quantiles(response_times, n=20)[18] if len(response_times) > 20 else 0,
        "p99_ms": statistics.quantiles(response_times, n=100)[98] if len(response_times) > 100 else 0
    }


async def test_events_performance(cattle_ids: List[str], iterations: int = 100) -> Dict:
    """Test events endpoint performance"""
    response_times = []
    
    async with httpx.AsyncClient() as client:
        for i in range(iterations):
            start = time.time()
            try:
                response = await client.get(
                    f"{API_BASE}/events",
                    params={"ranch_id": "test-ranch-1", "limit": 50}
                )
                elapsed = (time.time() - start) * 1000
                if response.status_code == 200:
                    response_times.append(elapsed)
            except Exception as e:
                print(f"Error in request: {e}")
    
    return {
        "endpoint": "GET /events",
        "iterations": len(response_times),
        "avg_ms": statistics.mean(response_times) if response_times else 0,
        "min_ms": min(response_times) if response_times else 0,
        "max_ms": max(response_times) if response_times else 0,
        "p95_ms": statistics.quantiles(response_times, n=20)[18] if len(response_times) > 20 else 0,
        "p99_ms": statistics.quantiles(response_times, n=100)[98] if len(response_times) > 100 else 0
    }


async def run_load_tests():
    """Run all load tests"""
    print("🚀 Starting Backend Performance Load Tests")
    print("=" * 60)
    
    # Test 1: Create 1000 cattle records
    print("\n📊 Test 1: Creating 1000 test cattle records...")
    start = time.time()
    cattle_ids = await create_test_cattle(1000)
    elapsed = time.time() - start
    print(f"✅ Created {len(cattle_ids)} records in {elapsed:.2f}s")
    print(f"   Average: {(elapsed/len(cattle_ids))*1000:.2f}ms per record")
    
    # Test 2: List cattle performance
    print("\n📊 Test 2: Testing GET /cattle performance (100 iterations)...")
    list_results = await test_list_performance(100)
    print(f"✅ Results:")
    print(f"   Average: {list_results['avg_ms']:.2f}ms")
    print(f"   P95: {list_results['p95_ms']:.2f}ms")
    print(f"   P99: {list_results['p99_ms']:.2f}ms")
    print(f"   Min: {list_results['min_ms']:.2f}ms")
    print(f"   Max: {list_results['max_ms']:.2f}ms")
    
    # Test 3: Get by ID performance
    print("\n📊 Test 3: Testing GET /cattle/{id} performance (100 iterations)...")
    get_results = await test_get_by_id_performance(cattle_ids, 100)
    print(f"✅ Results:")
    print(f"   Average: {get_results['avg_ms']:.2f}ms")
    print(f"   P95: {get_results['p95_ms']:.2f}ms")
    print(f"   P99: {get_results['p99_ms']:.2f}ms")
    
    # Test 4: Events performance
    print("\n📊 Test 4: Testing GET /events performance (100 iterations)...")
    events_results = await test_events_performance(cattle_ids, 100)
    print(f"✅ Results:")
    print(f"   Average: {events_results['avg_ms']:.2f}ms")
    print(f"   P95: {events_results['p95_ms']:.2f}ms")
    print(f"   P99: {events_results['p99_ms']:.2f}ms")
    
    # Summary
    print("\n" + "=" * 60)
    print("📈 PERFORMANCE SUMMARY")
    print("=" * 60)
    
    results = {
        "list_cattle": list_results,
        "get_by_id": get_results,
        "list_events": events_results,
        "total_records": len(cattle_ids)
    }
    
    # Performance assessment
    print("\n🎯 Performance Assessment:")
    if list_results['avg_ms'] < 200:
        print("   ✅ List endpoint: EXCELLENT (<200ms)")
    elif list_results['avg_ms'] < 500:
        print("   ⚠️  List endpoint: ACCEPTABLE (200-500ms)")
    else:
        print("   ❌ List endpoint: NEEDS OPTIMIZATION (>500ms)")
    
    if get_results['avg_ms'] < 100:
        print("   ✅ Get by ID: EXCELLENT (<100ms)")
    elif get_results['avg_ms'] < 200:
        print("   ⚠️  Get by ID: ACCEPTABLE (100-200ms)")
    else:
        print("   ❌ Get by ID: NEEDS OPTIMIZATION (>200ms)")
    
    return results


if __name__ == "__main__":
    asyncio.run(run_load_tests())
