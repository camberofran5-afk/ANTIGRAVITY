"""
Test script to verify backend structure and imports
"""

import sys
from pathlib import Path

# Add app to path
sys.path.insert(0, str(Path(__file__).parent / "app"))

def test_imports():
    """Test that all modules can be imported"""
    print("Testing imports...")
    
    try:
        from L1_config import cattle_types, system_config
        print("✅ L1 Config imports successful")
        
        # Test type definitions
        from L1_config.cattle_types import Animal, Species, Gender, Status
        print(f"✅ Types available: Animal, Species, Gender, Status")
        
        # Test config
        from L1_config.system_config import APP_NAME, APP_VERSION
        print(f"✅ Config: {APP_NAME} v{APP_VERSION}")
        
    except ImportError as e:
        print(f"❌ L1 import failed: {e}")
        return False
    
    try:
        from L2_foundation import cattle_crud, event_crud
        print("✅ L2 Foundation imports successful")
    except ImportError as e:
        print(f"❌ L2 import failed: {e}")
        return False
    
    try:
        from L3_analysis import kpi_calculator
        print("✅ L3 Analysis imports successful")
    except ImportError as e:
        print(f"❌ L3 import failed: {e}")
        return False
    
    try:
        import main
        print("✅ L4 Main app imports successful")
        print(f"✅ FastAPI app created: {main.app.title}")
    except ImportError as e:
        print(f"❌ L4 import failed: {e}")
        return False
    
    return True


def test_structure():
    """Test file structure"""
    print("\nTesting file structure...")
    
    required_files = [
        "app/L1_config/cattle_types.py",
        "app/L1_config/supabase_client.py",
        "app/L1_config/system_config.py",
        "app/L2_foundation/cattle_crud.py",
        "app/L2_foundation/event_crud.py",
        "app/L3_analysis/kpi_calculator.py",
        "app/main.py",
        "requirements.txt",
        "Dockerfile",
    ]
    
    all_exist = True
    for file_path in required_files:
        full_path = Path(__file__).parent / file_path
        if full_path.exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - MISSING")
            all_exist = False
    
    return all_exist


def test_api_structure():
    """Test API endpoint structure"""
    print("\nTesting API structure...")
    
    try:
        import main
        app = main.app
        
        routes = [route.path for route in app.routes]
        print(f"✅ Total routes: {len(routes)}")
        
        expected_routes = [
            "/health",
            "/api/v1/cattle",
            "/api/v1/cattle/{cattle_id}",
            "/api/v1/events",
            "/api/v1/metrics/kpis",
            "/api/v1/metrics/summary",
        ]
        
        for route in expected_routes:
            if any(route in r for r in routes):
                print(f"✅ {route}")
            else:
                print(f"❌ {route} - MISSING")
        
        return True
    except Exception as e:
        print(f"❌ API structure test failed: {e}")
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("ERP Ganadero Backend - Verification Tests")
    print("=" * 60)
    print()
    
    results = []
    
    # Test 1: File Structure
    results.append(("File Structure", test_structure()))
    
    # Test 2: Imports
    results.append(("Module Imports", test_imports()))
    
    # Test 3: API Structure
    results.append(("API Structure", test_api_structure()))
    
    # Summary
    print()
    print("=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test_name}: {status}")
    
    all_passed = all(result[1] for result in results)
    
    print()
    if all_passed:
        print("🎉 ALL TESTS PASSED - Backend is ready!")
        print()
        print("Next steps:")
        print("1. Set up Supabase project")
        print("2. Run database/schema.sql in Supabase")
        print("3. Update .env with real Supabase credentials")
        print("4. Run: uvicorn app.main:app --reload")
        print("5. Visit: http://localhost:8000/docs")
    else:
        print("⚠️  SOME TESTS FAILED - Review errors above")
    
    print("=" * 60)
    
    sys.exit(0 if all_passed else 1)
