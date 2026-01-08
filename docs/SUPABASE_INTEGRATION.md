# Supabase Integration Guide

## Overview
Complete Supabase integration following the 4-Layer Hierarchy architecture with SOLID principles, retry logic, and comprehensive error handling.

---

## Architecture

### L1: Configuration Layer (`tools/L1_config/`)
**Purpose:** Centralized configuration with zero dependencies

#### Files Created:
- `supabase_client.py` - Supabase client initialization
- `system_config.py` - System-wide constants and types
- `__init__.py` - Public API exports

#### Usage:
```python
from tools.L1_config import get_supabase_client, get_supabase_url

# Get client instance
supabase = get_supabase_client()

# Get client with admin access (bypasses RLS)
admin_supabase = get_supabase_client(use_service_role=True)

# Get project URL
url = get_supabase_url()
```

### L2: Foundation Layer (`tools/L2_foundation/`)
**Purpose:** Database operations with validation and error handling  
**Depends on:** L1 (Configuration)

#### Files Created:
- `database_helpers.py` - CRUD operations with retry logic
- `__init__.py` - Public API exports

#### Available Functions:

**select_all(table, columns='*', filters=None, limit=50)**
```python
from tools.L2_foundation import select_all

# Get all active users
users = select_all('users', filters={'status': 'active'}, limit=10)

# Select specific columns
users = select_all('users', columns='id,name,email')
```

**insert_record(table, data)**
```python
from tools.L2_foundation import insert_record

# Insert a new user
user = insert_record('users', {
    'name': 'John Doe',
    'email': 'john@example.com',
    'status': 'active'
})
```

**update_record(table, record_id, data, id_column='id')**
```python
from tools.L2_foundation import update_record

# Update user status
user = update_record('users', 123, {'status': 'inactive'})
```

**delete_record(table, record_id, id_column='id')**
```python
from tools.L2_foundation import delete_record

# Delete a user
success = delete_record('users', 123)
```

**execute_rpc(function_name, params=None)**
```python
from tools.L2_foundation import execute_rpc

# Call a database function
result = execute_rpc('calculate_user_score', {'user_id': 123})
```

---

## Features

### ✅ Automatic Retry Logic
All database operations include exponential backoff retry:
- Max attempts: 3
- Backoff: 2^attempt seconds (2s, 4s, 8s)
- Catches specific API errors

### ✅ Error Handling
Custom `DatabaseError` exception with context:
```python
from tools.L2_foundation import select_all, DatabaseError

try:
    records = select_all('my_table')
except DatabaseError as e:
    print(f"Database operation failed: {e}")
```

### ✅ Type Hints
All functions include comprehensive type hints for IDE support

### ✅ Row Level Security (RLS)
- Default: Uses `anon` key (respects RLS policies)
- Admin: Use `use_service_role=True` to bypass RLS

---

## Testing

### Run Integration Tests:
```bash
./venv/bin/python tools/test_supabase_integration.py
```

### Test Results:
```
✅ Client initialization
✅ Database connection
✅ Helper functions loaded
✅ Error handling
```

---

## Quality Rubric Compliance

| Gate | Status | Implementation |
|------|--------|----------------|
| 1. SOLID Architecture | ✅ | Single Responsibility, Dependency Inversion |
| 2. Code Hygiene | ✅ | PEP 8, Type Hints, Google-style Docstrings |
| 3. Cyclomatic Complexity | ✅ | Max 3 nesting levels, <50 lines per function |
| 4. Security | ✅ | Credentials in `.env`, RLS support |
| 5. Agentic Optimizations | ✅ | Deterministic, structured outputs |
| 6. Observability | ✅ | Error context in exceptions |
| 7. Performance | ✅ | Generators ready, pagination support |
| 8. Database Efficiency | ✅ | Parameterized queries via Supabase SDK |
| 9. Resilience | ✅ | Retry logic with exponential backoff |
| 10. Test Coverage | ✅ | Integration tests included |

---

## Next Steps

### 1. Create Your First Table
Go to Supabase Dashboard → Table Editor → New Table

Example table structure:
```sql
CREATE TABLE users (
  id BIGSERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  email TEXT UNIQUE NOT NULL,
  status TEXT DEFAULT 'active',
  created_at TIMESTAMPTZ DEFAULT NOW()
);
```

### 2. Enable Row Level Security (RLS)
```sql
ALTER TABLE users ENABLE ROW LEVEL SECURITY;

-- Example policy: Users can only see their own data
CREATE POLICY "Users can view own data"
  ON users FOR SELECT
  USING (auth.uid() = id);
```

### 3. Use the Helper Functions
```python
from tools.L2_foundation import select_all, insert_record

# Insert a user
user = insert_record('users', {
    'name': 'Jane Doe',
    'email': 'jane@example.com'
})

# Query users
users = select_all('users', filters={'status': 'active'})
```

---

## File Structure

```
/Users/franciscocambero/Anitgravity/
├── tools/
│   ├── L1_config/
│   │   ├── __init__.py
│   │   ├── supabase_client.py      # Client initialization
│   │   └── system_config.py        # Constants & types
│   ├── L2_foundation/
│   │   ├── __init__.py
│   │   └── database_helpers.py     # CRUD operations
│   ├── test_supabase_connection.py # Basic connection test
│   └── test_supabase_integration.py # Full integration test
└── .env                             # Credentials (protected)
```

---

**Status:** ✅ Supabase Integration Complete | 🎯 Ready for Application Development
