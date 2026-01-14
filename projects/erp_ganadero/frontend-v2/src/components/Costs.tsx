import React, { useState, useEffect } from 'react';
import Button from './Button';
import Modal from './Modal';
import CostForm from './CostForm';

interface Cost {
    id: string;
    category: string;
    sub_category?: string;
    amount_mxn: number;
    quantity?: number;
    unit_cost?: number;
    cost_date: string;
    supplier?: string;
    allocated_to?: string;
    description?: string;
}

const Costs: React.FC = () => {
    const [costs, setCosts] = useState<Cost[]>([]);
    const [_loading, _setLoading] = useState(false);
    const [isModalOpen, setIsModalOpen] = useState(false);

    const RANCH_ID = 'ranch-1'; // TODO: Get from auth context

    // Mock data for now - will integrate with backend
    useEffect(() => {
        // Load costs from backend when endpoint is ready
        setCosts([]);
    }, []);

    const handleSubmit = async (costData: any) => {
        try {
            // TODO: Call backend API when endpoint is ready
            // await api.createCost(costData);
            console.log('Cost data:', costData);

            // For now, add to local state
            const newCost: Cost = {
                id: `cost-${Date.now()}`,
                ...costData
            };
            setCosts([newCost, ...costs]);

            setIsModalOpen(false);
            alert('Costo guardado exitosamente');
        } catch (error) {
            console.error('Error saving cost:', error);
            alert('Error al guardar costo');
        }
    };

    const getCategoryLabel = (category: string) => {
        const labels: Record<string, string> = {
            feed: 'Alimento',
            veterinary: 'Veterinario',
            labor: 'Mano de Obra',
            infrastructure: 'Infraestructura',
            other: 'Otro'
        };
        return labels[category] || category;
    };

    const getCategoryIcon = (category: string) => {
        const icons: Record<string, string> = {
            feed: '🌾',
            veterinary: '💉',
            labor: '👷',
            infrastructure: '🏗️',
            other: '📦'
        };
        return icons[category] || '💰';
    };

    // Calculate totals by category
    const totalByCategory = costs.reduce((acc, cost) => {
        acc[cost.category] = (acc[cost.category] || 0) + cost.amount_mxn;
        return acc;
    }, {} as Record<string, number>);

    const totalCosts = costs.reduce((sum, cost) => sum + cost.amount_mxn, 0);

    return (
        <div className="container">
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
                <h2 style={{ fontSize: '1.75rem', margin: 0 }}>💰 Costos</h2>
                <Button variant="primary" onClick={() => setIsModalOpen(true)}>
                    ➕ Agregar Costo
                </Button>
            </div>

            {/* Summary Cards */}
            {costs.length > 0 && (
                <div className="grid grid-4" style={{ marginBottom: '2rem' }}>
                    <div className="card" style={{ background: 'linear-gradient(135deg, var(--danger) 0%, var(--danger-dark) 100%)', color: 'white' }}>
                        <div style={{ fontSize: '0.875rem', opacity: 0.9, marginBottom: '0.5rem' }}>TOTAL COSTOS</div>
                        <div style={{ fontSize: '2rem', fontWeight: 700 }}>
                            ${totalCosts.toLocaleString('es-MX', { minimumFractionDigits: 2 })}
                        </div>
                    </div>
                    {Object.entries(totalByCategory).slice(0, 3).map(([category, amount]) => (
                        <div key={category} className="card" style={{ background: 'var(--primary-light)' }}>
                            <div style={{ fontSize: '0.875rem', color: 'var(--text-secondary)', marginBottom: '0.5rem' }}>
                                {getCategoryIcon(category)} {getCategoryLabel(category).toUpperCase()}
                            </div>
                            <div style={{ fontSize: '1.5rem', fontWeight: 600, color: 'var(--primary)' }}>
                                ${amount.toLocaleString('es-MX', { minimumFractionDigits: 2 })}
                            </div>
                        </div>
                    ))}
                </div>
            )}

            {/* Costs List */}
            {costs.length === 0 ? (
                <div className="card" style={{ textAlign: 'center', padding: '3rem' }}>
                    <p style={{ fontSize: '1.125rem', color: 'var(--text-secondary)' }}>
                        No hay costos registrados. Agrega el primer costo.
                    </p>
                </div>
            ) : (
                <div className="card">
                    <h3 style={{ marginBottom: '1rem' }}>Registro de Costos</h3>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                        {costs.map((cost) => (
                            <div
                                key={cost.id}
                                style={{
                                    padding: '1rem',
                                    border: '2px solid var(--border)',
                                    borderRadius: 'var(--radius-md)',
                                    transition: 'var(--transition-normal)'
                                }}
                                onMouseEnter={(e) => {
                                    e.currentTarget.style.borderColor = 'var(--primary)';
                                    e.currentTarget.style.boxShadow = 'var(--shadow-sm)';
                                }}
                                onMouseLeave={(e) => {
                                    e.currentTarget.style.borderColor = 'var(--border)';
                                    e.currentTarget.style.boxShadow = 'none';
                                }}
                            >
                                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                                    <div style={{ flex: 1 }}>
                                        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.5rem' }}>
                                            <span style={{ fontSize: '1.5rem' }}>{getCategoryIcon(cost.category)}</span>
                                            <span style={{ fontWeight: 600, fontSize: '1.125rem' }}>
                                                {getCategoryLabel(cost.category)}
                                                {cost.sub_category && ` - ${cost.sub_category}`}
                                            </span>
                                        </div>
                                        <div style={{ fontSize: '0.875rem', color: 'var(--text-secondary)', marginBottom: '0.5rem' }}>
                                            {new Date(cost.cost_date).toLocaleDateString('es-MX')}
                                            {cost.supplier && ` • ${cost.supplier}`}
                                        </div>
                                        {cost.quantity && cost.unit_cost && (
                                            <div style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>
                                                {cost.quantity} × ${cost.unit_cost.toFixed(2)} = ${cost.amount_mxn.toFixed(2)}
                                            </div>
                                        )}
                                        {cost.description && (
                                            <div style={{ fontSize: '0.875rem', color: 'var(--text-secondary)', fontStyle: 'italic', marginTop: '0.5rem' }}>
                                                {cost.description}
                                            </div>
                                        )}
                                    </div>
                                    <div style={{ textAlign: 'right' }}>
                                        <div style={{ fontSize: '1.5rem', fontWeight: 700, color: 'var(--danger)' }}>
                                            ${cost.amount_mxn.toLocaleString('es-MX', { minimumFractionDigits: 2 })}
                                        </div>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            )}

            <Modal
                isOpen={isModalOpen}
                onClose={() => setIsModalOpen(false)}
                title="Nuevo Costo"
            >
                <CostForm
                    ranchId={RANCH_ID}
                    onSubmit={handleSubmit}
                    onCancel={() => setIsModalOpen(false)}
                />
            </Modal>
        </div>
    );
};

export default Costs;
