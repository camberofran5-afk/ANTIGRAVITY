// Core Types
export interface Animal {
    id: string;
    ranch_id: string;
    arete: string; // Changed from arete_number for consistency
    arete_number?: string; // Keep for backward compatibility
    name?: string; // Added optional name field
    species: 'vaca' | 'toro' | 'becerro';
    gender: 'M' | 'F';
    birth_date: string;
    weight_kg?: number;
    photo_url?: string;
    status: 'active' | 'sold' | 'dead';
    mother_id?: string;
    notes?: string;
    created_at: string;
    updated_at: string;
}

export interface AnimalCreate {
    ranch_id: string;
    arete_number: string;
    species: string;
    gender: string;
    birth_date: string;
    weight_kg?: number;
    status: string;
}

// Enhanced Event Types
export interface Event {
    id: string;
    cattle_id: string;
    type: EventType;
    event_date: string;
    data: EventData;
    notes?: string;
    created_at: string;
}

export type EventType = 'birth' | 'sale' | 'vaccination' | 'weighing' | 'treatment' | 'death';

export interface EventData {
    // Birth
    calf_weight_kg?: number;
    calf_gender?: 'M' | 'F';
    calf_arete?: string;
    complications?: string;
    birth_type?: 'natural' | 'assisted' | 'cesarean';
    calf_status?: 'alive' | 'stillborn';

    // Sale
    buyer_id?: string;
    sale_weight_kg?: number;
    price_per_kg?: number;
    total_price?: number;
    payment_terms?: 'cash' | 'credit' | 'installments';
    payment_status?: 'paid' | 'pending';
    transport_cost?: number;

    // Vaccination
    vaccine_type?: string;
    batch_number?: string;
    dose_ml?: number;
    cost?: number;
    next_due_date?: string;
    administered_by?: string;

    // Weighing
    weight_kg?: number;
    body_condition_score?: number;

    // Treatment
    diagnosis?: string;
    medicine?: string;
    dosage?: string;
    treatment_cost?: number;

    // Death
    reason?: string;
    age_months?: number;
    value_lost?: number;
}

// Cost Types
export interface Cost {
    id: string;
    ranch_id: string;
    category: CostCategory;
    sub_category?: string;
    amount_mxn: number;
    quantity?: number;
    unit_cost?: number;
    cost_date: string;
    supplier?: string;
    allocated_to?: 'all' | 'specific' | 'group';
    description?: string;
    created_at: string;
}

export type CostCategory = 'feed' | 'veterinary' | 'labor' | 'infrastructure' | 'other';

// Client Types
export interface Client {
    id: string;
    ranch_id: string;
    name: string;
    type: 'feedlot' | 'butcher' | 'export' | 'rancher';
    contact: {
        phone?: string;
        email?: string;
        address?: string;
    };
    payment_terms: 'cash' | '15_days' | '30_days' | '60_days';
    price_agreements?: {
        calves?: number;
        cows?: number;
    };
    created_at: string;
}

// Inventory Types
export interface InventoryItem {
    id: string;
    ranch_id: string;
    category: 'feed' | 'medicine' | 'vaccine' | 'equipment';
    name: string;
    quantity: number;
    unit: string;
    unit_cost: number;
    total_value: number;
    supplier?: string;
    expiry_date?: string;
    min_stock?: number;
    location?: string;
    created_at: string;
}

// Personnel Types
export interface Worker {
    id: string;
    ranch_id: string;
    name: string;
    role: 'vaquero' | 'veterinario' | 'manager';
    salary_monthly: number;
    hire_date: string;
    tasks_assigned?: string[];
    performance?: {
        events_logged: number;
        accuracy_rate: number;
    };
    created_at: string;
}

// Metrics Types
export interface HerdMetrics {
    pregnancy_rate: number;
    calving_interval_days: number;
    weaning_weight_avg: number;
    calf_mortality_percent: number;
}

export interface HerdSummary {
    total_animals: number;
    productive_count: number;
    unproductive_count: number;
    ready_to_wean_count: number;
    recent_births: number;
    recent_deaths: number;
    week_cost_usd: number;
}

// Financial Types
export interface FinancialMetrics {
    total_costs: number;
    total_revenue: number;
    profit: number;
    margin_percent: number;
    cost_per_kg: number;
    roi_percent: number;
}

// User Types
export interface User {
    id: string;
    email: string;
    ranch_name: string;
    state: string;
    pin: string;
    created_at: string;
}

export interface LoginCredentials {
    email: string;
    pin: string;
}

export interface RegisterData {
    email: string;
    ranch_name: string;
    state: string;
    pin: string;
}
