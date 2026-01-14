import React, { useState, useEffect } from 'react';
import EventTimeline from './EventTimeline';
import WeightChart from './WeightChart';
import { calculations } from '../utils/calculations';

interface Animal {
    id: string;
    arete: string;
    name?: string;
    species: string;
    gender: string;
    birth_date: string;
    weight_kg?: number;
    status: string;
}

interface Event {
    id: string;
    type: string;
    event_date: string;
    data: any;
    notes?: string;
}

interface AnimalDetailProps {
    animalId: string;
    onBack: () => void;
}

const AnimalDetail: React.FC<AnimalDetailProps> = ({ animalId, onBack }) => {
    const [animal, setAnimal] = useState<Animal | null>(null);
    const [events, setEvents] = useState<Event[]>([]);
    const [weightHistory, setWeightHistory] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        loadAnimalData();
    }, [animalId]);

    const loadAnimalData = async () => {
        try {
            setLoading(true);
            setError(null);

            // Load animal details
            const animalRes = await fetch(`http://localhost:8000/api/v1/cattle/${animalId}`);
            if (!animalRes.ok) throw new Error('Failed to load animal');
            const animalData = await animalRes.json();
            setAnimal(animalData);

            // Load events
            const eventsRes = await fetch(`http://localhost:8000/api/v1/cattle/${animalId}/events`);
            if (eventsRes.ok) {
                const eventsData = await eventsRes.json();
                setEvents(eventsData);
            }

            // Load weight history
            const weightRes = await fetch(`http://localhost:8000/api/v1/cattle/${animalId}/weight-history`);
            if (weightRes.ok) {
                const weightData = await weightRes.json();
                setWeightHistory(weightData.measurements || []);
            }
        } catch (err: any) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    const calculateAge = (birthDate: string): string => {
        const birth = new Date(birthDate);
        const now = new Date();
        const diffMs = now.getTime() - birth.getTime();
        const years = Math.floor(diffMs / (1000 * 60 * 60 * 24 * 365));
        const months = Math.floor((diffMs % (1000 * 60 * 60 * 24 * 365)) / (1000 * 60 * 60 * 24 * 30));
        return `${years} años ${months} meses`;
    };

    // Helper functions removed - moved to EventTimeline component

    const calculateTotalCosts = (): number => {
        // Sum all costs from events
        return events.reduce((total, event) => {
            const cost = event.data.cost || event.data.treatment_cost || 0;
            return total + cost;
        }, 0);
    };

    const getSaleRevenue = (): number | null => {
        const saleEvent = events.find(e => e.type === 'sale');
        return saleEvent?.data.total_price || null;
    };

    const calculateFinancials = () => {
        const totalCosts = calculateTotalCosts();
        const revenue = getSaleRevenue();

        if (revenue === null) {
            return { totalCosts, revenue: null, profit: null, margin: null };
        }

        const profit = calculations.profit(revenue, totalCosts);
        const margin = calculations.marginPercent(profit, revenue);

        return { totalCosts, revenue, profit, margin };
    };

    if (loading) {
        return (
            <div style={{ padding: '20px', textAlign: 'center' }}>
                <p>Cargando...</p>
            </div>
        );
    }

    if (error || !animal) {
        return (
            <div style={{ padding: '20px' }}>
                <button onClick={onBack} style={{
                    padding: '10px 20px',
                    backgroundColor: '#4CAF50',
                    color: 'white',
                    border: 'none',
                    borderRadius: '4px',
                    cursor: 'pointer',
                    marginBottom: '20px'
                }}>
                    ← Volver a Ganado
                </button>
                <p style={{ color: 'red' }}>Error: {error || 'Animal no encontrado'}</p>
            </div>
        );
    }

    return (
        <div style={{ padding: '20px', maxWidth: '1200px', margin: '0 auto' }}>
            {/* Header */}
            <button onClick={onBack} style={{
                padding: '10px 20px',
                backgroundColor: '#4CAF50',
                color: 'white',
                border: 'none',
                borderRadius: '4px',
                cursor: 'pointer',
                marginBottom: '20px'
            }}>
                ← Volver a Ganado
            </button>

            {/* Animal Info Card */}
            <div style={{
                backgroundColor: 'white',
                borderRadius: '8px',
                padding: '24px',
                marginBottom: '24px',
                boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
            }}>
                <h1 style={{ margin: '0 0 20px 0', color: '#2c3e50' }}>
                    🐄 {animal.arete} {animal.name ? `- ${animal.name}` : ''}
                </h1>

                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '16px' }}>
                    <div>
                        <strong>Especie:</strong> {animal.species}
                    </div>
                    <div>
                        <strong>Género:</strong> {animal.gender === 'M' ? 'Macho' : 'Hembra'}
                    </div>
                    <div>
                        <strong>Edad:</strong> {calculateAge(animal.birth_date)}
                    </div>
                    <div>
                        <strong>Peso Actual:</strong> {animal.weight_kg ? `${animal.weight_kg} kg` : 'N/A'}
                    </div>
                    <div>
                        <strong>Estado:</strong>
                        <span style={{
                            marginLeft: '8px',
                            padding: '4px 8px',
                            borderRadius: '12px',
                            backgroundColor: animal.status === 'active' ? '#4CAF50' : '#999',
                            color: 'white',
                            fontSize: '12px'
                        }}>
                            {animal.status}
                        </span>
                    </div>
                </div>
            </div>

            {/* Financial Metrics */}
            {events.length > 0 && (() => {
                const financials = calculateFinancials();
                return (
                    <div style={{
                        backgroundColor: 'white',
                        borderRadius: '8px',
                        padding: '24px',
                        marginBottom: '24px',
                        boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
                    }}>
                        <h2 style={{ margin: '0 0 20px 0', color: '#2c3e50' }}>
                            💰 Análisis Financiero
                        </h2>

                        <div style={{
                            display: 'grid',
                            gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
                            gap: '16px'
                        }}>
                            {/* Total Costs */}
                            <div style={{
                                padding: '16px',
                                backgroundColor: '#fff3e0',
                                borderRadius: '8px',
                                border: '2px solid #ff9800'
                            }}>
                                <div style={{ fontSize: '14px', color: '#666', marginBottom: '8px' }}>
                                    Costos Totales
                                </div>
                                <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#ff9800' }}>
                                    ${financials.totalCosts.toFixed(2)}
                                </div>
                            </div>

                            {/* Revenue */}
                            {financials.revenue !== null && (
                                <div style={{
                                    padding: '16px',
                                    backgroundColor: '#e8f5e9',
                                    borderRadius: '8px',
                                    border: '2px solid #4caf50'
                                }}>
                                    <div style={{ fontSize: '14px', color: '#666', marginBottom: '8px' }}>
                                        Ingreso por Venta
                                    </div>
                                    <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#4caf50' }}>
                                        ${financials.revenue.toFixed(2)}
                                    </div>
                                </div>
                            )}

                            {/* Profit/Loss */}
                            {financials.profit !== null && (
                                <div style={{
                                    padding: '16px',
                                    backgroundColor: financials.profit >= 0 ? '#e8f5e9' : '#ffebee',
                                    borderRadius: '8px',
                                    border: `2px solid ${financials.profit >= 0 ? '#4caf50' : '#f44336'}`
                                }}>
                                    <div style={{ fontSize: '14px', color: '#666', marginBottom: '8px' }}>
                                        {financials.profit >= 0 ? 'Ganancia' : 'Pérdida'}
                                    </div>
                                    <div style={{
                                        fontSize: '24px',
                                        fontWeight: 'bold',
                                        color: financials.profit >= 0 ? '#4caf50' : '#f44336'
                                    }}>
                                        ${Math.abs(financials.profit).toFixed(2)}
                                    </div>
                                </div>
                            )}

                            {/* Margin % */}
                            {financials.margin !== null && (
                                <div style={{
                                    padding: '16px',
                                    backgroundColor: financials.margin >= 0 ? '#e3f2fd' : '#ffebee',
                                    borderRadius: '8px',
                                    border: `2px solid ${financials.margin >= 0 ? '#2196f3' : '#f44336'}`
                                }}>
                                    <div style={{ fontSize: '14px', color: '#666', marginBottom: '8px' }}>
                                        Margen
                                    </div>
                                    <div style={{
                                        fontSize: '24px',
                                        fontWeight: 'bold',
                                        color: financials.margin >= 0 ? '#2196f3' : '#f44336'
                                    }}>
                                        {financials.margin.toFixed(1)}%
                                    </div>
                                </div>
                            )}
                        </div>

                        {financials.revenue === null && (
                            <div style={{
                                marginTop: '16px',
                                padding: '12px',
                                backgroundColor: '#f5f5f5',
                                borderRadius: '4px',
                                fontSize: '14px',
                                color: '#666'
                            }}>
                                ℹ️ El análisis de ganancia/pérdida estará disponible cuando se registre la venta del animal.
                            </div>
                        )}
                    </div>
                );
            })()}

            {/* Weight Chart */}
            {weightHistory.length > 0 && (
                <div style={{ marginBottom: '24px' }}>
                    <WeightChart measurements={weightHistory} targetWeight={520} />
                </div>
            )}

            {/* Event Timeline */}
            <div style={{
                backgroundColor: 'white',
                borderRadius: '8px',
                padding: '24px',
                boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
            }}>
                <h2 style={{ margin: '0 0 20px 0', color: '#2c3e50' }}>
                    📅 Historial de Eventos
                </h2>
                <EventTimeline events={events} />
            </div>
        </div>
    );
};

export default AnimalDetail;

