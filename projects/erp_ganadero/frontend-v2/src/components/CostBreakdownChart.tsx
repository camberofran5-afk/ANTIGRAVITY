import React from 'react';
import { Pie } from 'react-chartjs-2';
import {
    Chart as ChartJS,
    ArcElement,
    Tooltip,
    Legend
} from 'chart.js';

// Register Chart.js components
ChartJS.register(ArcElement, Tooltip, Legend);

interface CostBreakdown {
    feed: number;
    veterinary: number;
    labor: number;
    infrastructure: number;
    other: number;
}

interface CostBreakdownChartProps {
    breakdown: CostBreakdown;
}

const CostBreakdownChart: React.FC<CostBreakdownChartProps> = ({ breakdown }) => {
    const data = {
        labels: ['Alimento', 'Veterinario', 'Mano de Obra', 'Infraestructura', 'Otros'],
        datasets: [
            {
                label: 'Costos ($)',
                data: [
                    breakdown.feed,
                    breakdown.veterinary,
                    breakdown.labor,
                    breakdown.infrastructure,
                    breakdown.other
                ],
                backgroundColor: [
                    'rgba(255, 159, 64, 0.8)',  // Orange - Feed
                    'rgba(75, 192, 192, 0.8)',  // Teal - Vet
                    'rgba(54, 162, 235, 0.8)',  // Blue - Labor
                    'rgba(153, 102, 255, 0.8)', // Purple - Infrastructure
                    'rgba(201, 203, 207, 0.8)'  // Gray - Other
                ],
                borderColor: [
                    'rgba(255, 159, 64, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(201, 203, 207, 1)'
                ],
                borderWidth: 2
            }
        ]
    };

    const options = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: 'right' as const,
                labels: {
                    padding: 15,
                    font: {
                        size: 12
                    }
                }
            },
            tooltip: {
                callbacks: {
                    label: function (context: any) {
                        const label = context.label || '';
                        const value = context.parsed || 0;
                        const total = context.dataset.data.reduce((a: number, b: number) => a + b, 0);
                        const percentage = total > 0 ? ((value / total) * 100).toFixed(1) : '0';
                        return `${label}: $${value.toFixed(2)} (${percentage}%)`;
                    }
                }
            }
        }
    };

    const total = Object.values(breakdown).reduce((sum, val) => sum + val, 0);

    return (
        <div style={{
            backgroundColor: 'white',
            borderRadius: '8px',
            padding: '24px',
            boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
        }}>
            <h3 style={{ margin: '0 0 16px 0', color: '#2c3e50' }}>
                📊 Desglose de Costos
            </h3>

            {total > 0 ? (
                <>
                    <div style={{ height: '300px', marginBottom: '16px' }}>
                        <Pie data={data} options={options} />
                    </div>

                    <div style={{
                        padding: '12px',
                        backgroundColor: '#f5f5f5',
                        borderRadius: '4px',
                        textAlign: 'center'
                    }}>
                        <strong>Total: ${total.toFixed(2)}</strong>
                    </div>
                </>
            ) : (
                <div style={{
                    padding: '40px',
                    textAlign: 'center',
                    color: '#999',
                    backgroundColor: '#f9f9f9',
                    borderRadius: '8px'
                }}>
                    <p>📊 No hay datos de costos disponibles</p>
                    <p style={{ fontSize: '14px', marginTop: '8px' }}>
                        Los costos se mostrarán cuando se registren eventos con costos asociados.
                    </p>
                </div>
            )}
        </div>
    );
};

export default CostBreakdownChart;
