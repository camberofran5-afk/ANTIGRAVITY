# TEAM 3: Backend Architecture & Implementation

## 🎯 Backend Objective
Build a robust, offline-first backend that scales, never loses data, and supports all missing MVP features.

---

## 🏗️ SYSTEM ARCHITECTURE

### **Technology Stack**

**Frontend**:
- React Native 0.73+ (iOS + Android)
- TypeScript 5.8
- React Query (data fetching/caching)
- SQLite (local database)
- AsyncStorage (app state)

**Backend**:
- FastAPI 0.109+ (Python 3.11)
- Pydantic v2 (validation)
- SQLAlchemy 2.0 (ORM)
- Alembic (migrations)

**Database**:
- Supabase (PostgreSQL 15)
- Row Level Security (RLS)
- Realtime subscriptions
- Storage buckets (photos)

**Infrastructure**:
- Google Cloud Run (backend hosting)
- Supabase Cloud (database + auth + storage)
- GitHub Actions (CI/CD)
- Sentry (error tracking)

---

### **4-Layer Architecture**

```
┌─────────────────────────────────────────────┐
│ L4: SYNTHESIS (API Endpoints)               │
│ ├─ cattle_api.py (CRUD)                     │
│ ├─ events_api.py (birth, death, sale, etc.) │
│ ├─ metrics_api.py (KPI calculations)        │
│ ├─ sync_api.py (offline sync)               │
│ └─ auth_api.py (authentication)             │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│ L3: ANALYSIS (Business Logic)               │
│ ├─ kpi_calculator.py (pregnancy rate, etc.) │
│ ├─ inventory_manager.py (herd status)       │
│ ├─ cost_analyzer.py (financial metrics)     │
│ ├─ alert_engine.py (notifications)          │
│ └─ sync_orchestrator.py (conflict resolution)│
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│ L2: FOUNDATION (Helpers)                    │
│ ├─ cattle_crud.py (database operations)     │
│ ├─ event_logger.py (event tracking)         │
│ ├─ sync_manager.py (offline sync)           │
│ ├─ photo_uploader.py (image handling)       │
│ └─ supabase_helpers.py (DB utilities)       │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│ L1: CONFIG (Settings)                       │
│ ├─ supabase_client.py (DB connection)       │
│ ├─ cattle_types.py (enums, models)          │
│ ├─ system_config.py (constants)             │
│ └─ logging_config.py (structlog)            │
└─────────────────────────────────────────────┘
```

---

## 🗄️ DATABASE SCHEMA (Supabase/PostgreSQL)

### **Core Tables**

#### **ranches**
```sql
CREATE TABLE ranches (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  name VARCHAR(255) NOT NULL,
  owner_id UUID NOT NULL REFERENCES auth.users(id),
  location GEOGRAPHY(POINT),
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_ranches_owner ON ranches(owner_id);
```

---

#### **users** (extends Supabase auth.users)
```sql
CREATE TABLE user_profiles (
  id UUID PRIMARY KEY REFERENCES auth.users(id),
  ranch_id UUID REFERENCES ranches(id),
  role VARCHAR(50) NOT NULL CHECK (role IN ('owner', 'manager', 'worker')),
  full_name VARCHAR(255),
  phone VARCHAR(20),
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_user_profiles_ranch ON user_profiles(ranch_id);
```

---

#### **cattle**
```sql
CREATE TABLE cattle (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  ranch_id UUID NOT NULL REFERENCES ranches(id),
  arete_number VARCHAR(50) NOT NULL,
  species VARCHAR(20) NOT NULL CHECK (species IN ('vaca', 'toro', 'becerro', 'vaquilla')),
  gender VARCHAR(1) NOT NULL CHECK (gender IN ('M', 'F')),
  birth_date DATE NOT NULL,
  weight_kg DECIMAL(6,2),
  photo_url TEXT,
  status VARCHAR(20) NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'sold', 'dead', 'rest')),
  mother_id UUID REFERENCES cattle(id),
  notes TEXT,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  UNIQUE(ranch_id, arete_number)
);

CREATE INDEX idx_cattle_ranch ON cattle(ranch_id);
CREATE INDEX idx_cattle_status ON cattle(status);
CREATE INDEX idx_cattle_species ON cattle(species);
CREATE INDEX idx_cattle_mother ON cattle(mother_id);
```

---

#### **events**
```sql
CREATE TABLE events (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  cattle_id UUID NOT NULL REFERENCES cattle(id) ON DELETE CASCADE,
  type VARCHAR(50) NOT NULL CHECK (type IN ('birth', 'death', 'sale', 'vaccination', 'weighing', 'pregnancy_check', 'treatment')),
  event_date DATE NOT NULL,
  data JSONB NOT NULL DEFAULT '{}',
  photo_url TEXT,
  notes TEXT,
  created_by UUID REFERENCES auth.users(id),
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_events_cattle ON events(cattle_id);
CREATE INDEX idx_events_type ON events(type);
CREATE INDEX idx_events_date ON events(event_date);
```

**Event Data Structure** (JSONB):
```json
// Birth
{
  "calf_id": "uuid",
  "calf_weight_kg": 35,
  "calf_gender": "M",
  "calf_arete": "BEC-123"
}

// Death
{
  "reason": "disease",
  "details": "pneumonia"
}

// Sale
{
  "buyer": "Juan Pérez",
  "price_mxn": 8500,
  "weight_kg": 220
}

// Vaccination
{
  "vaccine": "Triple viral",
  "dose": "5ml",
  "next_date": "2026-04-15"
}

// Weighing
{
  "weight_kg": 185,
  "body_condition_score": 3.5
}
```

---

#### **costs**
```sql
CREATE TABLE costs (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  ranch_id UUID NOT NULL REFERENCES ranches(id),
  category VARCHAR(50) NOT NULL CHECK (category IN ('feed', 'veterinary', 'labor', 'infrastructure', 'other')),
  amount_mxn DECIMAL(10,2) NOT NULL,
  description TEXT,
  cost_date DATE NOT NULL,
  cattle_id UUID REFERENCES cattle(id),
  created_by UUID REFERENCES auth.users(id),
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_costs_ranch ON costs(ranch_id);
CREATE INDEX idx_costs_category ON costs(category);
CREATE INDEX idx_costs_date ON costs(cost_date);
```

---

#### **sync_queue** (for offline sync)
```sql
CREATE TABLE sync_queue (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID NOT NULL REFERENCES auth.users(id),
  operation VARCHAR(20) NOT NULL CHECK (operation IN ('create', 'update', 'delete')),
  table_name VARCHAR(50) NOT NULL,
  record_id UUID NOT NULL,
  payload JSONB NOT NULL,
  timestamp TIMESTAMP NOT NULL DEFAULT NOW(),
  synced BOOLEAN DEFAULT FALSE,
  error TEXT,
  retry_count INTEGER DEFAULT 0
);

CREATE INDEX idx_sync_queue_user ON sync_queue(user_id);
CREATE INDEX idx_sync_queue_synced ON sync_queue(synced);
```

---

### **Row Level Security (RLS) Policies**

```sql
-- Enable RLS on all tables
ALTER TABLE ranches ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE cattle ENABLE ROW LEVEL SECURITY;
ALTER TABLE events ENABLE ROW LEVEL SECURITY;
ALTER TABLE costs ENABLE ROW LEVEL SECURITY;

-- Ranches: Users can only see their own ranch
CREATE POLICY "Users can view own ranch"
  ON ranches FOR SELECT
  USING (owner_id = auth.uid());

CREATE POLICY "Users can update own ranch"
  ON ranches FOR UPDATE
  USING (owner_id = auth.uid());

-- Cattle: Users can only see cattle from their ranch
CREATE POLICY "Users can view ranch cattle"
  ON cattle FOR SELECT
  USING (ranch_id IN (
    SELECT ranch_id FROM user_profiles WHERE id = auth.uid()
  ));

CREATE POLICY "Users can insert ranch cattle"
  ON cattle FOR INSERT
  WITH CHECK (ranch_id IN (
    SELECT ranch_id FROM user_profiles WHERE id = auth.uid()
  ));

CREATE POLICY "Users can update ranch cattle"
  ON cattle FOR UPDATE
  USING (ranch_id IN (
    SELECT ranch_id FROM user_profiles WHERE id = auth.uid()
  ));

-- Events: Users can only see events for their ranch's cattle
CREATE POLICY "Users can view ranch events"
  ON events FOR SELECT
  USING (cattle_id IN (
    SELECT id FROM cattle WHERE ranch_id IN (
      SELECT ranch_id FROM user_profiles WHERE id = auth.uid()
    )
  ));

-- Similar policies for costs, sync_queue
```

---

## 🔄 OFFLINE SYNC PROTOCOL

### **Sync Strategy: Optimistic UI + Background Sync**

```
┌─────────────────────────────────────────────┐
│ MOBILE APP (React Native)                  │
│                                             │
│ 1. User Action (create/update/delete)      │
│    ↓                                        │
│ 2. Write to Local SQLite                   │
│    ↓                                        │
│ 3. Add to Sync Queue                       │
│    ↓                                        │
│ 4. Update UI Immediately (optimistic)      │
│    ↓                                        │
│ 5. Attempt Sync (if online)                │
│    ├─ Success → Mark as synced             │
│    └─ Failure → Retry later                │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│ BACKEND API (FastAPI)                      │
│                                             │
│ 1. Receive batch sync request              │
│    ↓                                        │
│ 2. Validate operations                     │
│    ↓                                        │
│ 3. Check for conflicts (timestamp)         │
│    ↓                                        │
│ 4. Apply operations to Supabase            │
│    ↓                                        │
│ 5. Return sync status + server changes     │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│ SUPABASE (PostgreSQL)                      │
│                                             │
│ 1. Data persisted                          │
│ 2. Triggers fire (updated_at, etc.)        │
│ 3. Realtime notifications (optional)       │
└─────────────────────────────────────────────┘
```

---

### **Conflict Resolution**

**Strategy**: Last-Write-Wins (timestamp-based)

```python
def resolve_conflict(local_record, server_record):
    """
    Compare timestamps and keep the most recent version.
    """
    if local_record['updated_at'] > server_record['updated_at']:
        return local_record  # Local wins
    else:
        return server_record  # Server wins
```

**Edge Cases**:
1. **Same timestamp**: Server wins (tie-breaker)
2. **Delete vs. Update**: Delete wins (explicit action)
3. **Critical fields** (arete_number): Manual resolution (notify user)

---

### **Sync API Endpoints**

```python
# POST /api/v1/sync/upload
{
  "operations": [
    {
      "id": "local-uuid-1",
      "operation": "create",
      "table": "cattle",
      "data": {...},
      "timestamp": "2026-01-15T10:30:00Z"
    },
    {
      "id": "local-uuid-2",
      "operation": "update",
      "table": "events",
      "record_id": "uuid",
      "data": {...},
      "timestamp": "2026-01-15T10:35:00Z"
    }
  ],
  "last_sync": "2026-01-15T09:00:00Z"
}

# Response
{
  "synced": ["local-uuid-1", "local-uuid-2"],
  "conflicts": [],
  "server_changes": [
    {
      "table": "cattle",
      "operation": "update",
      "record_id": "uuid",
      "data": {...},
      "timestamp": "2026-01-15T10:32:00Z"
    }
  ]
}
```

---

## 🚀 API ENDPOINTS (FastAPI)

### **Authentication** (`/api/v1/auth`)

```python
POST /auth/register
{
  "email": "rancher@example.com",
  "password": "SecurePass123",
  "full_name": "Roberto García",
  "ranch_name": "Rancho San José"
}

POST /auth/login
{
  "email": "rancher@example.com",
  "password": "SecurePass123"
}

POST /auth/logout
```

---

### **Cattle Management** (`/api/v1/cattle`)

```python
GET /cattle
  ?ranch_id=uuid
  &status=active
  &species=vaca
  &page=1
  &limit=50

POST /cattle
{
  "arete_number": "TX-452",
  "species": "vaca",
  "gender": "F",
  "birth_date": "2020-05-15",
  "weight_kg": 520,
  "mother_id": "uuid",
  "photo_url": "https://..."
}

GET /cattle/{id}

PUT /cattle/{id}
{
  "weight_kg": 530,
  "status": "active"
}

DELETE /cattle/{id}
```

---

### **Events** (`/api/v1/events`)

```python
POST /events
{
  "cattle_id": "uuid",
  "type": "birth",
  "event_date": "2026-01-20",
  "data": {
    "calf_weight_kg": 35,
    "calf_gender": "M"
  },
  "photo_url": "https://...",
  "notes": "Healthy calf"
}

GET /events
  ?cattle_id=uuid
  &type=birth
  &date_from=2026-01-01
  &date_to=2026-01-31

GET /events/{id}
```

---

### **Metrics** (`/api/v1/metrics`)

```python
GET /metrics/kpis
  ?ranch_id=uuid
  &date_from=2025-01-01
  &date_to=2026-01-31

Response:
{
  "pregnancy_rate": 78.5,
  "calving_interval_days": 412,
  "weaning_weight_avg": 185.3,
  "calf_mortality_percent": 4.2,
  "calculated_at": "2026-01-15T10:00:00Z"
}

GET /metrics/summary
  ?ranch_id=uuid

Response:
{
  "total_animals": 154,
  "productive_count": 131,
  "unproductive_count": 23,
  "ready_to_wean_count": 12,
  "recent_births": 5,
  "recent_deaths": 1
}
```

---

### **Costs** (`/api/v1/costs`)

```python
POST /costs
{
  "category": "feed",
  "amount_mxn": 1500.00,
  "description": "Alimento concentrado",
  "cost_date": "2026-01-15",
  "cattle_id": null
}

GET /costs
  ?ranch_id=uuid
  &category=feed
  &date_from=2026-01-01
  &date_to=2026-01-31

GET /costs/summary
  ?ranch_id=uuid
  &period=month

Response:
{
  "total_mxn": 45000.00,
  "by_category": {
    "feed": 25000.00,
    "veterinary": 8000.00,
    "labor": 12000.00
  },
  "cost_per_animal": 292.21
}
```

---

### **Sync** (`/api/v1/sync`)

```python
POST /sync/upload
{
  "operations": [...],
  "last_sync": "2026-01-15T09:00:00Z"
}

GET /sync/download
  ?since=2026-01-15T09:00:00Z
  &tables=cattle,events,costs

Response:
{
  "changes": [
    {
      "table": "cattle",
      "operation": "update",
      "record_id": "uuid",
      "data": {...},
      "timestamp": "2026-01-15T10:32:00Z"
    }
  ],
  "server_timestamp": "2026-01-15T11:00:00Z"
}
```

---

### **Photos** (`/api/v1/photos`)

```python
POST /photos/upload
Content-Type: multipart/form-data
{
  "file": <binary>,
  "type": "cattle" | "event",
  "record_id": "uuid"
}

Response:
{
  "url": "https://supabase-storage.../photo.jpg",
  "thumbnail_url": "https://supabase-storage.../photo_thumb.jpg"
}
```

---

## 📦 IMPLEMENTATION ROADMAP

### **Week 1-2: Foundation (L1 + L2)**

**L1: Config**
- ✅ Supabase client setup
- ✅ Type definitions (Pydantic models)
- ✅ Environment configuration
- ✅ Logging setup (structlog)

**L2: Foundation**
- ✅ CRUD helpers (cattle, events, costs)
- ✅ Supabase utilities
- ✅ Photo upload/compression
- ✅ Sync queue manager

---

### **Week 3-4: Business Logic (L3)**

- ✅ KPI calculator (pregnancy rate, calving interval, etc.)
- ✅ Inventory manager (herd status, counts)
- ✅ Cost analyzer (per animal, by category)
- ✅ Alert engine (unproductive cows, upcoming vaccinations)
- ✅ Sync orchestrator (conflict resolution)

---

### **Week 5-6: API Layer (L4) + Missing Features**

**L4: API Endpoints**
- ✅ Authentication (Supabase Auth integration)
- ✅ Cattle CRUD endpoints
- ✅ Events endpoints
- ✅ Metrics endpoints
- ✅ Costs endpoints
- ✅ Sync endpoints
- ✅ Photo upload endpoint

**Missing Features**:
- ✅ Event logging system
- ✅ Cost tracking module
- ✅ Reports generation (PDF)
- ✅ Multi-user access (RLS)

---

### **Week 7-8: Integration + Deployment**

- ✅ React Native app integration
- ✅ Offline sync testing
- ✅ Performance optimization
- ✅ Security audit
- ✅ Load testing (1000 concurrent users)
- ✅ Production deployment (Cloud Run)
- ✅ Monitoring setup (Sentry, Cloud Monitoring)

---

## 🔒 SECURITY CONSIDERATIONS

### **Authentication**
- ✅ Supabase Auth (JWT tokens)
- ✅ Password hashing (bcrypt)
- ✅ Email verification
- ✅ Password reset flow

### **Authorization**
- ✅ Row Level Security (RLS)
- ✅ Role-based access (owner, manager, worker)
- ✅ API key for mobile app

### **Data Protection**
- ✅ HTTPS only (TLS 1.3)
- ✅ SQL injection prevention (parameterized queries)
- ✅ XSS protection (input sanitization)
- ✅ CORS configuration (mobile app only)

### **Privacy**
- ✅ Data encryption at rest (Supabase default)
- ✅ Photo access control (signed URLs)
- ✅ GDPR compliance (data export/deletion)

---

## 📊 PERFORMANCE TARGETS

| Metric | Target | How to Achieve |
|--------|--------|----------------|
| API Response Time | < 200ms (p95) | Indexes, connection pooling |
| Database Queries | < 50ms (p95) | Proper indexing, query optimization |
| Photo Upload | < 3 seconds | Compression, CDN |
| Sync Time (100 records) | < 5 seconds | Batch operations, async processing |
| Concurrent Users | 1000+ | Horizontal scaling (Cloud Run) |
| Uptime | 99.9% | Health checks, auto-restart |

---

## 🧪 TESTING STRATEGY

### **Unit Tests** (pytest)
- All L2 helpers (CRUD operations)
- All L3 business logic (KPI calculations)
- Sync conflict resolution

### **Integration Tests**
- API endpoints (FastAPI TestClient)
- Database operations (test database)
- Photo upload flow

### **End-to-End Tests**
- Mobile app + backend (Detox)
- Offline sync scenarios
- Multi-user workflows

### **Load Tests** (Locust)
- 1000 concurrent users
- 10,000 requests/minute
- Sync queue processing

---

## 🚀 DEPLOYMENT

### **Infrastructure**

```yaml
# docker-compose.yml (local development)
version: '3.8'
services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - SUPABASE_URL=${SUPABASE_URL}
      - SUPABASE_KEY=${SUPABASE_KEY}
    volumes:
      - ./app:/app

# Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### **Cloud Run Deployment**

```bash
# Build and deploy
gcloud builds submit --tag gcr.io/PROJECT_ID/erp-ganadero-api
gcloud run deploy erp-ganadero-api \
  --image gcr.io/PROJECT_ID/erp-ganadero-api \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars SUPABASE_URL=$SUPABASE_URL,SUPABASE_KEY=$SUPABASE_KEY \
  --memory 512Mi \
  --cpu 1 \
  --max-instances 10
```

---

## ✅ DELIVERABLES SUMMARY

1. ✅ System Architecture (4-layer hierarchy)
2. ✅ Database Schema (Supabase/PostgreSQL with RLS)
3. ✅ Offline Sync Protocol (conflict resolution)
4. ✅ API Specification (REST endpoints)
5. ✅ Implementation Roadmap (8 weeks)
6. ✅ Security & Performance Standards
7. ✅ Deployment Guide (Cloud Run)

**Status**: COMPLETE
**Next**: Integration with React Native app

---

## 📋 HANDOFF NOTES FOR MOBILE TEAM

### **API Base URL**
- Development: `http://localhost:8000/api/v1`
- Production: `https://api.ganadocontrol.com/api/v1`

### **Authentication Flow**
1. User registers/logs in → Receives JWT token
2. Store token in AsyncStorage
3. Include in all API requests: `Authorization: Bearer {token}`
4. Refresh token every 24 hours

### **Offline Sync Implementation**
1. Use SQLite for local storage (mirror of Supabase schema)
2. All writes go to local DB first
3. Add to sync queue
4. Background task processes queue every 5 minutes (or when online)
5. Handle conflicts gracefully (show user notification if manual resolution needed)

### **Photo Handling**
1. Capture photo → Compress to < 500KB
2. Upload to `/photos/upload` endpoint
3. Receive URL → Store in local DB
4. Display from URL (cached by React Native Image)

**Ready for mobile integration!** 🚀
