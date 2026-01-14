"""
ERP Ganadero - Database Schema (Supabase/PostgreSQL)

Complete database schema with RLS policies.
"""

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================================================
-- TABLES
-- ============================================================================

-- Ranches
CREATE TABLE ranches (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  name VARCHAR(255) NOT NULL,
  owner_id UUID NOT NULL REFERENCES auth.users(id),
  location GEOGRAPHY(POINT),
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_ranches_owner ON ranches(owner_id);

-- User Profiles
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

-- Cattle
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

-- Events
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

-- Costs
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

-- Sync Queue (for offline sync)
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

-- ============================================================================
-- ROW LEVEL SECURITY (RLS)
-- ============================================================================

-- Enable RLS on all tables
ALTER TABLE ranches ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE cattle ENABLE ROW LEVEL SECURITY;
ALTER TABLE events ENABLE ROW LEVEL SECURITY;
ALTER TABLE costs ENABLE ROW LEVEL SECURITY;
ALTER TABLE sync_queue ENABLE ROW LEVEL SECURITY;

-- Ranches Policies
CREATE POLICY "Users can view own ranch"
  ON ranches FOR SELECT
  USING (owner_id = auth.uid());

CREATE POLICY "Users can update own ranch"
  ON ranches FOR UPDATE
  USING (owner_id = auth.uid());

CREATE POLICY "Users can insert own ranch"
  ON ranches FOR INSERT
  WITH CHECK (owner_id = auth.uid());

-- User Profiles Policies
CREATE POLICY "Users can view own profile"
  ON user_profiles FOR SELECT
  USING (id = auth.uid());

CREATE POLICY "Users can update own profile"
  ON user_profiles FOR UPDATE
  USING (id = auth.uid());

-- Cattle Policies
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

CREATE POLICY "Users can delete ranch cattle"
  ON cattle FOR DELETE
  USING (ranch_id IN (
    SELECT ranch_id FROM user_profiles WHERE id = auth.uid()
  ));

-- Events Policies
CREATE POLICY "Users can view ranch events"
  ON events FOR SELECT
  USING (cattle_id IN (
    SELECT id FROM cattle WHERE ranch_id IN (
      SELECT ranch_id FROM user_profiles WHERE id = auth.uid()
    )
  ));

CREATE POLICY "Users can insert ranch events"
  ON events FOR INSERT
  WITH CHECK (cattle_id IN (
    SELECT id FROM cattle WHERE ranch_id IN (
      SELECT ranch_id FROM user_profiles WHERE id = auth.uid()
    )
  ));

-- Costs Policies
CREATE POLICY "Users can view ranch costs"
  ON costs FOR SELECT
  USING (ranch_id IN (
    SELECT ranch_id FROM user_profiles WHERE id = auth.uid()
  ));

CREATE POLICY "Users can insert ranch costs"
  ON costs FOR INSERT
  WITH CHECK (ranch_id IN (
    SELECT ranch_id FROM user_profiles WHERE id = auth.uid()
  ));

-- Sync Queue Policies
CREATE POLICY "Users can view own sync queue"
  ON sync_queue FOR SELECT
  USING (user_id = auth.uid());

CREATE POLICY "Users can insert own sync queue"
  ON sync_queue FOR INSERT
  WITH CHECK (user_id = auth.uid());

CREATE POLICY "Users can update own sync queue"
  ON sync_queue FOR UPDATE
  USING (user_id = auth.uid());

-- ============================================================================
-- TRIGGERS
-- ============================================================================

-- Update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_ranches_updated_at BEFORE UPDATE ON ranches
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_user_profiles_updated_at BEFORE UPDATE ON user_profiles
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_cattle_updated_at BEFORE UPDATE ON cattle
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_events_updated_at BEFORE UPDATE ON events
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
