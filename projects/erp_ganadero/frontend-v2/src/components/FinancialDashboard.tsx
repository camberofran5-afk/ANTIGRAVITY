import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import { calculations } from '../utils/calculations';
import { HerdSummary } from '../types';
import MetricCard from './MetricCard';
import AlertBanner from './AlertBanner';
import OpportunityCard from './OpportunityCard';
import CostBreakdownChart from './CostBreakdownChart';

interface KPIData {
    pregnancy_rate: number;
    calving_interval_days: number;
    weaning_weight_avg: number;
    calf_mortality_percent: number;
}

const FinancialDashboard: React.FC = () => {
    const [summary, setSummary] = useState<HerdSummary | null>(null);
    const [kpis, setKpis] = useState<KPIData | null>(null);
    const [costBreakdown, setCostBreakdown] = useState<any>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    const RANCH_ID = 'ranch-1'; // TODO: Get from auth context
    const TARGET_PREGNANCY_RATE = 85; // Industry standard

    useEffect(() => {
        loadDashboard();
        // Auto-refresh every 30 seconds
        const interval = setInterval(loadDashboard, 30000);
        return () => clearInterval(interval);
    }, []);

    const loadDashboard = async () => {
        try {
            setLoading(true);
            setError(null);
            const [summaryData, kpisData] = await Promise.all([
                api.getSummary(RANCH_ID),
                api.getMetrics(RANCH_ID)
            ]);
            setSummary(summaryData);
            setKpis(kpisData);

            // Load cost breakdown (mock data for now - will be real API later)
            // TODO: Replace with actual API call when backend endpoint is ready
            setCostBreakdown({
                feed: 12500,
                veterinary: 3200,
                labor: 8500,
                infrastructure: 4100,
                other: 1800
            });
        } catch (err) {
            console.error('Error loading dashboard:', err);
            setError('Error al cargar el dashboard. Verifica que el backend esté corriendo.');
        } finally {
            setLoading(false);
        }
    };

    if (loading && !summary) {
        return (
            <div className="container">
                <div className="loading">
                    <p>Cargando dashboard financiero...</p>
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="container">
                <div className="error">
                    <strong>Error:</strong> {error}
                </div>
            </div>
        );
    }

    if (!summary) {
        return null;
    }

    // Calculate pregnancy rate (mock for now - will be real in Phase 3)
    const currentPregnancyRate = 75; // TODO: Calculate from actual data
    const pregnancyGap = TARGET_PREGNANCY_RATE - currentPregnancyRate;
    const hasPregnancyOpportunity = pregnancyGap > 0;

    // Calculate economic opportunity
    const pregnancyOpportunity = hasPregnancyOpportunity
        ? calculations.economicOpportunity(
            currentPregnancyRate,
            TARGET_PREGNANCY_RATE,
            summary.total_animals
        )
        : 0;

    return (
        <div className="container">
            <h2 style={{ marginBottom: '1.5rem', fontSize: '1.75rem' }}>
                📊 Dashboard Financiero
            </h2>

            {/* Unproductive Cow Alert */}
            {summary.unproductive_count > 0 && (
                <AlertBanner unproductiveCount={summary.unproductive_count} />
            )}

            {/* Key Metrics */}
            <div className="grid grid-4" style={{ marginBottom: '2rem' }}>
                <MetricCard
                    label="Total Animales"
                    value={summary.total_animals}
                    variant="primary"
                    icon="🐄"
                />
                <MetricCard
                    label="Productivos"
                    value={summary.productive_count}
                    variant="success"
                    icon="✅"
                />
                <MetricCard
                    label="Improductivos"
                    value={summary.unproductive_count}
                    variant="warning"
                    icon="⚠️"
                />
                <MetricCard
                    label="Nacimientos (30 días)"
                    value={summary.recent_births}
                    variant="primary"
                    icon="🍼"
                />
            </div>

            {/* Financial Metrics */}
            <div className="grid grid-3" style={{ marginBottom: '2rem' }}>
                <MetricCard
                    label="Costo Semanal"
                    value={`$${summary.week_cost_usd.toFixed(2)}`}
                    variant="danger"
                    icon="💰"
                />
                <MetricCard
                    label="Listos para Destete"
                    value={summary.ready_to_wean_count}
                    variant="success"
                    icon="🌾"
                />
                <MetricCard
                    label="Muertes Recientes"
                    value={summary.recent_deaths}
                    variant="danger"
                    icon="💀"
                />
            </div>

            {/* KPIs Section */}
            {kpis && (
                <div>
                    <h3 style={{ marginBottom: '1rem', fontSize: '1.5rem' }}>
                        📈 Indicadores de Rendimiento (KPIs)
                    </h3>
                    <div className="grid grid-4" style={{ marginBottom: '2rem' }}>
                        <div className="card" style={{ textAlign: 'center' }}>
                            <div style={{ fontSize: '0.875rem', color: 'var(--text-secondary)', marginBottom: '0.5rem' }}>
                                Tasa de Preñez
                            </div>
                            <div style={{ fontSize: '2rem', fontWeight: 700, color: kpis.pregnancy_rate >= 85 ? 'var(--success)' : 'var(--warning)' }}>
                                {kpis.pregnancy_rate.toFixed(1)}%
                            </div>
                            <div style={{ fontSize: '0.75rem', color: 'var(--text-secondary)' }}>
                                Meta: 85%
                            </div>
                        </div>
                        <div className="card" style={{ textAlign: 'center' }}>
                            <div style={{ fontSize: '0.875rem', color: 'var(--text-secondary)', marginBottom: '0.5rem' }}>
                                Intervalo entre Partos
                            </div>
                            <div style={{ fontSize: '2rem', fontWeight: 700, color: kpis.calving_interval_days <= 365 ? 'var(--success)' : 'var(--warning)' }}>
                                {kpis.calving_interval_days.toFixed(0)}
                            </div>
                            <div style={{ fontSize: '0.75rem', color: 'var(--text-secondary)' }}>
                                Meta: 365 días
                            </div>
                        </div>
                        <div className="card" style={{ textAlign: 'center' }}>
                            <div style={{ fontSize: '0.875rem', color: 'var(--text-secondary)', marginBottom: '0.5rem' }}>
                                Peso al Destete
                            </div>
                            <div style={{ fontSize: '2rem', fontWeight: 700, color: kpis.weaning_weight_avg >= 210 ? 'var(--success)' : 'var(--warning)' }}>
                                {kpis.weaning_weight_avg.toFixed(0)} kg
                            </div>
                            <div style={{ fontSize: '0.75rem', color: 'var(--text-secondary)' }}>
                                Meta: 210 kg
                            </div>
                        </div>
                        <div className="card" style={{ textAlign: 'center' }}>
                            <div style={{ fontSize: '0.875rem', color: 'var(--text-secondary)', marginBottom: '0.5rem' }}>
                                Mortalidad de Becerros
                            </div>
                            <div style={{ fontSize: '2rem', fontWeight: 700, color: kpis.calf_mortality_percent <= 3 ? 'var(--success)' : 'var(--danger)' }}>
                                {kpis.calf_mortality_percent.toFixed(1)}%
                            </div>
                            <div style={{ fontSize: '0.75rem', color: 'var(--text-secondary)' }}>
                                Meta: ≤3%
                            </div>
                        </div>
                    </div>
                </div>
            )}

            {/* Economic Opportunities */}
            {hasPregnancyOpportunity && (
                <div>
                    <h3 style={{ marginBottom: '1rem', fontSize: '1.5rem' }}>
                        💡 Oportunidades Económicas
                    </h3>
                    <div className="grid grid-2" style={{ marginBottom: '2rem' }}>
                        <OpportunityCard
                            title="Brecha en Tasa de Preñez"
                            currentValue={currentPregnancyRate}
                            targetValue={TARGET_PREGNANCY_RATE}
                            opportunityAmount={pregnancyOpportunity}
                            recommendation="Implementa un programa de sincronización de celos y mejora la nutrición durante la época de empadre para aumentar la tasa de preñez al 85%."
                            icon="🤰"
                        />
                        {/* More opportunity cards can be added here in future phases */}
                    </div>
                </div>
            )}

            {/* Cost Breakdown Chart */}
            {costBreakdown && (
                <div style={{ marginBottom: '2rem' }}>
                    <CostBreakdownChart breakdown={costBreakdown} />
                </div>
            )}

            {/* Info Section */}
            <div className="card" style={{ background: 'var(--primary-light)', border: 'none' }}>
                <h4 style={{ marginBottom: '0.5rem', color: 'var(--primary)' }}>
                    ℹ️ Acerca de este Dashboard
                </h4>
                <p style={{ fontSize: '0.875rem', color: 'var(--text-secondary)', lineHeight: 1.6 }}>
                    Este dashboard financiero te muestra las métricas clave de tu rancho y las oportunidades
                    económicas identificadas. Las vacas improductivas representan un costo significativo
                    ($15.42 USD/semana por vaca). Las oportunidades económicas se calculan comparando tus
                    métricas actuales con los estándares de la industria.
                </p>
            </div>
        </div>
    );
};

export default FinancialDashboard;
