
export enum Species {
  VACA = 'vaca',
  TORO = 'toro',
  BECERRO = 'becerro',
  VAQUILLA = 'vaquilla'
}

export enum Gender {
  M = 'M',
  F = 'F'
}

export enum Status {
  ACTIVE = 'active',
  SOLD = 'sold',
  DEAD = 'dead',
  REST = 'rest'
}

export interface Animal {
  animal_id: string;
  ranch_id: string;
  arete_number: string;
  species: Species;
  gender: Gender;
  birth_date: string;
  weight_kg: number;
  photo_url?: string;
  status: Status;
  mother_id?: string;
  notes?: string;
  lastReproductionDate?: string;
  created_at: string;
}

export interface HerdSummary {
  totalAnimals: number;
  unproductiveCount: number;
  readyToWeanCount: number;
  weekCostUsd: number;
}

export interface HerdMetrics {
  pregnancy_rate: number;
  calving_interval_days: number;
  weaning_weight_avg: number;
  calf_mortality_percent: number;
  source: 'fresh' | 'cache';
  calculatedAgoHours?: number;
}

export type MetricStatus = 'optimal' | 'warning' | 'critical';
