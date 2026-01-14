import React, { useRef } from 'react';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
    Filler
} from 'chart.js';
import { Line } from 'react-chartjs-2';

// Register Chart.js components
ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
    Filler
);

interface WeightMeasurement {
    date: string;
    weight_kg: number;
    type: 'weighing' | 'birth';
}

interface WeightChartProps {
    measurements: WeightMeasurement[];
    targetWeight?: number;
}

const WeightChart: React.FC<WeightChartProps> = ({ measurements, targetWeight }) => {
    const chartRef = useRef<ChartJS<'line'>>(null);

    if (measurements.length === 0) {
        return (
            <div style={{
                backgroundColor: 'white',
                borderRadius: '12px',
                padding: '40px',
                textAlign: 'center',
                boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
            }}>
                <div style={{ fontSize: '48px', marginBottom: '16px' }}>📊</div>
                <p style={{ color: '#666', margin: 0 }}>
                    No hay datos de peso disponibles
                </p>
            </div>
        );
    }

    // Sort measurements by date
    const sortedMeasurements = [...measurements].sort((a, b) =>
        new Date(a.date).getTime() - new Date(b.date).getTime()
    );

    // Prepare chart data
    const labels = sortedMeasurements.map(m =>
        new Date(m.date).toLocaleDateString('es-MX', {
            day: 'numeric',
            month: 'short',
            year: '2-digit'
        })
    );

    const weights = sortedMeasurements.map(m => m.weight_kg);

    // Calculate growth rate
    const calculateGrowthRate = (): number => {
        if (sortedMeasurements.length < 2) return 0;

        const first = sortedMeasurements[0];
        const last = sortedMeasurements[sortedMeasurements.length - 1];

        const weightDiff = last.weight_kg - first.weight_kg;
        const daysDiff = (new Date(last.date).getTime() - new Date(first.date).getTime()) / (1000 * 60 * 60 * 24);

        return daysDiff > 0 ? weightDiff / daysDiff : 0;
    };

    const growthRate = calculateGrowthRate();

    const data = {
        labels,
        datasets: [
            {
                label: 'Peso (kg)',
                data: weights,
                borderColor: '#4CAF50',
                backgroundColor: 'rgba(76, 175, 80, 0.1)',
                borderWidth: 3,
                pointRadius: 6,
                pointHoverRadius: 8,
                pointBackgroundColor: '#4CAF50',
                pointBorderColor: 'white',
                pointBorderWidth: 2,
                tension: 0.4,
                fill: true
            },
            ...(targetWeight ? [{
                label: 'Peso Objetivo',
                data: new Array(labels.length).fill(targetWeight),
                borderColor: '#FF9800',
                backgroundColor: 'transparent',
                borderWidth: 2,
                borderDash: [5, 5],
                pointRadius: 0,
                tension: 0
            }] : [])
        ]
    };

    const options = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                display: true,
                position: 'top' as const,
                labels: {
                    usePointStyle: true,
                    padding: 15,
                    font: {
                        size: 13,
                        weight: 500
                    }
                }
            },
            tooltip: {
                backgroundColor: 'rgba(0, 0, 0, 0.8)',
                padding: 12,
                titleFont: {
                    size: 14,
                    weight: 'bold' as const
                },
                bodyFont: {
                    size: 13
                },
                callbacks: {
                    label: function (context: any) {
                        let label = context.dataset.label || '';
                        if (label) {
                            label += ': ';
                        }
                        label += context.parsed.y + ' kg';
                        return label;
                    }
                }
            }
        },
        scales: {
            y: {
                beginAtZero: true,
                ticks: {
                    callback: function (value: any) {
                        return value + ' kg';
                    },
                    font: {
                        size: 12
                    }
                },
                grid: {
                    color: 'rgba(0, 0, 0, 0.05)'
                }
            },
            x: {
                ticks: {
                    font: {
                        size: 11
                    },
                    maxRotation: 45,
                    minRotation: 45
                },
                grid: {
                    display: false
                }
            }
        }
    };

    return (
        <div style={{
            backgroundColor: 'white',
            borderRadius: '12px',
            padding: '24px',
            boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
        }}>
            {/* Header */}
            <div style={{
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                marginBottom: '20px'
            }}>
                <h3 style={{ margin: 0, color: '#2c3e50', fontSize: '18px' }}>
                    📊 Progresión de Peso
                </h3>
                <div style={{
                    display: 'flex',
                    gap: '16px',
                    alignItems: 'center'
                }}>
                    <div style={{ textAlign: 'right' }}>
                        <div style={{ fontSize: '12px', color: '#999' }}>Ganancia Diaria</div>
                        <div style={{
                            fontSize: '18px',
                            fontWeight: 600,
                            color: growthRate >= 1.0 ? '#4CAF50' : growthRate >= 0.8 ? '#FF9800' : '#F44336'
                        }}>
                            {growthRate.toFixed(2)} kg/día
                        </div>
                    </div>
                </div>
            </div>

            {/* Stats Cards */}
            <div style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fit, minmax(120px, 1fr))',
                gap: '12px',
                marginBottom: '20px'
            }}>
                <div style={{
                    backgroundColor: '#f5f5f5',
                    padding: '12px',
                    borderRadius: '8px',
                    textAlign: 'center'
                }}>
                    <div style={{ fontSize: '12px', color: '#666', marginBottom: '4px' }}>Peso Inicial</div>
                    <div style={{ fontSize: '20px', fontWeight: 600, color: '#2c3e50' }}>
                        {sortedMeasurements[0].weight_kg} kg
                    </div>
                </div>
                <div style={{
                    backgroundColor: '#f5f5f5',
                    padding: '12px',
                    borderRadius: '8px',
                    textAlign: 'center'
                }}>
                    <div style={{ fontSize: '12px', color: '#666', marginBottom: '4px' }}>Peso Actual</div>
                    <div style={{ fontSize: '20px', fontWeight: 600, color: '#4CAF50' }}>
                        {sortedMeasurements[sortedMeasurements.length - 1].weight_kg} kg
                    </div>
                </div>
                <div style={{
                    backgroundColor: '#f5f5f5',
                    padding: '12px',
                    borderRadius: '8px',
                    textAlign: 'center'
                }}>
                    <div style={{ fontSize: '12px', color: '#666', marginBottom: '4px' }}>Ganancia Total</div>
                    <div style={{ fontSize: '20px', fontWeight: 600, color: '#2c3e50' }}>
                        +{(sortedMeasurements[sortedMeasurements.length - 1].weight_kg - sortedMeasurements[0].weight_kg).toFixed(1)} kg
                    </div>
                </div>
                <div style={{
                    backgroundColor: '#f5f5f5',
                    padding: '12px',
                    borderRadius: '8px',
                    textAlign: 'center'
                }}>
                    <div style={{ fontSize: '12px', color: '#666', marginBottom: '4px' }}>Mediciones</div>
                    <div style={{ fontSize: '20px', fontWeight: 600, color: '#2c3e50' }}>
                        {sortedMeasurements.length}
                    </div>
                </div>
            </div>

            {/* Chart */}
            <div style={{ height: '300px', position: 'relative' }}>
                <Line ref={chartRef} data={data} options={options} />
            </div>

            {/* Growth Rate Indicator */}
            <div style={{
                marginTop: '16px',
                padding: '12px',
                backgroundColor: growthRate >= 1.0 ? '#E8F5E9' : growthRate >= 0.8 ? '#FFF3E0' : '#FFEBEE',
                borderRadius: '8px',
                border: `1px solid ${growthRate >= 1.0 ? '#4CAF50' : growthRate >= 0.8 ? '#FF9800' : '#F44336'}`
            }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <span style={{ fontSize: '20px' }}>
                        {growthRate >= 1.0 ? '✅' : growthRate >= 0.8 ? '⚠️' : '❌'}
                    </span>
                    <div style={{ flex: 1 }}>
                        <strong style={{ fontSize: '14px', color: '#2c3e50' }}>
                            {growthRate >= 1.0 ? 'Excelente crecimiento' : growthRate >= 0.8 ? 'Crecimiento moderado' : 'Crecimiento bajo'}
                        </strong>
                        <p style={{ margin: '4px 0 0 0', fontSize: '13px', color: '#555' }}>
                            {growthRate >= 1.0
                                ? 'El animal está ganando peso por encima del objetivo (1.0 kg/día)'
                                : growthRate >= 0.8
                                    ? 'El animal está cerca del objetivo. Considera ajustar la alimentación.'
                                    : 'El animal está por debajo del objetivo. Revisa nutrición y salud.'}
                        </p>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default WeightChart;
