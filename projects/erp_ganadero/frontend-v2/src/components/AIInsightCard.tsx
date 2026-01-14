import React from 'react';

interface AIInsight {
    insight: string;
    recommendation: string;
    alert?: string | null;
    confidence: number;
    provider?: string;
    generated_at?: string;
}

interface AIInsightCardProps {
    title: string;
    insight: AIInsight;
    icon: string;
    loading?: boolean;
}

const AIInsightCard: React.FC<AIInsightCardProps> = ({ title, insight, icon, loading }) => {
    if (loading) {
        return (
            <div style={{
                backgroundColor: 'white',
                borderRadius: '12px',
                padding: '24px',
                boxShadow: '0 4px 6px rgba(0,0,0,0.1)',
                minHeight: '200px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center'
            }}>
                <div style={{ textAlign: 'center', color: '#666' }}>
                    <div style={{ fontSize: '32px', marginBottom: '12px' }}>🤖</div>
                    <p>Analizando datos...</p>
                </div>
            </div>
        );
    }

    const getConfidenceColor = (confidence: number): string => {
        if (confidence >= 80) return '#4CAF50';
        if (confidence >= 60) return '#FF9800';
        return '#F44336';
    };

    const getConfidenceLabel = (confidence: number): string => {
        if (confidence >= 80) return 'Alta';
        if (confidence >= 60) return 'Media';
        return 'Baja';
    };

    return (
        <div style={{
            backgroundColor: 'white',
            borderRadius: '12px',
            padding: '24px',
            boxShadow: '0 4px 6px rgba(0,0,0,0.1)',
            border: insight.alert ? '2px solid #FF9800' : '1px solid #e0e0e0',
            transition: 'all 0.3s ease'
        }}>
            {/* Header */}
            <div style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                marginBottom: '16px'
            }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                    <span style={{ fontSize: '32px' }}>{icon}</span>
                    <h3 style={{ margin: 0, color: '#2c3e50', fontSize: '18px' }}>{title}</h3>
                </div>
                <div style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '8px',
                    padding: '6px 12px',
                    borderRadius: '20px',
                    backgroundColor: `${getConfidenceColor(insight.confidence)}20`,
                    border: `1px solid ${getConfidenceColor(insight.confidence)}`
                }}>
                    <div style={{
                        width: '8px',
                        height: '8px',
                        borderRadius: '50%',
                        backgroundColor: getConfidenceColor(insight.confidence)
                    }} />
                    <span style={{
                        fontSize: '12px',
                        fontWeight: 600,
                        color: getConfidenceColor(insight.confidence)
                    }}>
                        {getConfidenceLabel(insight.confidence)} ({insight.confidence}%)
                    </span>
                </div>
            </div>

            {/* Alert (if present) */}
            {insight.alert && (
                <div style={{
                    backgroundColor: '#FFF3E0',
                    border: '1px solid #FF9800',
                    borderRadius: '8px',
                    padding: '12px 16px',
                    marginBottom: '16px',
                    display: 'flex',
                    alignItems: 'flex-start',
                    gap: '12px'
                }}>
                    <span style={{ fontSize: '20px' }}>⚠️</span>
                    <div style={{ flex: 1 }}>
                        <strong style={{ color: '#E65100', fontSize: '14px' }}>Alerta</strong>
                        <p style={{ margin: '4px 0 0 0', color: '#555', fontSize: '14px' }}>
                            {insight.alert}
                        </p>
                    </div>
                </div>
            )}

            {/* Insight */}
            <div style={{ marginBottom: '16px' }}>
                <div style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '8px',
                    marginBottom: '8px'
                }}>
                    <span style={{ fontSize: '18px' }}>💡</span>
                    <strong style={{ color: '#2c3e50', fontSize: '14px' }}>Análisis</strong>
                </div>
                <p style={{
                    margin: 0,
                    color: '#555',
                    fontSize: '15px',
                    lineHeight: '1.6',
                    paddingLeft: '26px'
                }}>
                    {insight.insight}
                </p>
            </div>

            {/* Recommendation */}
            <div>
                <div style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '8px',
                    marginBottom: '8px'
                }}>
                    <span style={{ fontSize: '18px' }}>📋</span>
                    <strong style={{ color: '#2c3e50', fontSize: '14px' }}>Recomendación</strong>
                </div>
                <p style={{
                    margin: 0,
                    color: '#555',
                    fontSize: '15px',
                    lineHeight: '1.6',
                    paddingLeft: '26px'
                }}>
                    {insight.recommendation}
                </p>
            </div>

            {/* Footer */}
            <div style={{
                marginTop: '16px',
                paddingTop: '16px',
                borderTop: '1px solid #e0e0e0',
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center'
            }}>
                <span style={{ fontSize: '12px', color: '#999' }}>
                    Powered by {insight.provider || 'AI'}
                </span>
                {insight.generated_at && (
                    <span style={{ fontSize: '12px', color: '#999' }}>
                        {new Date(insight.generated_at).toLocaleString('es-MX')}
                    </span>
                )}
            </div>
        </div>
    );
};

export default AIInsightCard;
