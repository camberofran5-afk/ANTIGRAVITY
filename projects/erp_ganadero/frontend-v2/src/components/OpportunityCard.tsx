import React from 'react';

interface OpportunityCardProps {
    title: string;
    currentValue: number;
    targetValue: number;
    opportunityAmount: number;
    recommendation: string;
    icon?: string;
}

const OpportunityCard: React.FC<OpportunityCardProps> = ({
    title,
    currentValue,
    targetValue,
    opportunityAmount,
    recommendation,
    icon = '💡'
}) => {
    const gap = targetValue - currentValue;
    const gapPercent = ((gap / targetValue) * 100).toFixed(1);

    const cardStyles: React.CSSProperties = {
        background: 'var(--bg-card)',
        border: '2px solid var(--border)',
        borderRadius: 'var(--radius-lg)',
        padding: '1.5rem',
        boxShadow: 'var(--shadow-sm)',
        transition: 'var(--transition-normal)',
        cursor: 'pointer'
    };

    const headerStyles: React.CSSProperties = {
        display: 'flex',
        alignItems: 'center',
        gap: '0.75rem',
        marginBottom: '1rem'
    };

    const iconStyles: React.CSSProperties = {
        fontSize: '2rem',
        background: 'var(--primary-light)',
        padding: '0.5rem',
        borderRadius: 'var(--radius-md)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        width: '3rem',
        height: '3rem'
    };

    const titleStyles: React.CSSProperties = {
        fontSize: '1.125rem',
        fontWeight: 600,
        color: 'var(--text-primary)',
        flex: 1
    };

    const metricsStyles: React.CSSProperties = {
        display: 'flex',
        justifyContent: 'space-between',
        marginBottom: '1rem',
        padding: '1rem',
        background: 'var(--bg-primary)',
        borderRadius: 'var(--radius-md)'
    };

    const metricStyles: React.CSSProperties = {
        textAlign: 'center'
    };

    const metricLabelStyles: React.CSSProperties = {
        fontSize: '0.75rem',
        color: 'var(--text-secondary)',
        textTransform: 'uppercase',
        marginBottom: '0.25rem'
    };

    const metricValueStyles: React.CSSProperties = {
        fontSize: '1.25rem',
        fontWeight: 600,
        color: 'var(--text-primary)'
    };

    const opportunityStyles: React.CSSProperties = {
        background: 'linear-gradient(135deg, var(--success) 0%, #388E3C 100%)',
        color: 'white',
        padding: '1rem',
        borderRadius: 'var(--radius-md)',
        marginBottom: '1rem',
        textAlign: 'center'
    };

    const opportunityLabelStyles: React.CSSProperties = {
        fontSize: '0.875rem',
        opacity: 0.9,
        marginBottom: '0.25rem'
    };

    const opportunityValueStyles: React.CSSProperties = {
        fontSize: '2rem',
        fontWeight: 700
    };

    const recommendationStyles: React.CSSProperties = {
        fontSize: '0.875rem',
        color: 'var(--text-secondary)',
        lineHeight: 1.5,
        padding: '0.75rem',
        background: '#FFF9E6',
        borderRadius: 'var(--radius-md)',
        borderLeft: '3px solid var(--warning)'
    };

    return (
        <div
            style={cardStyles}
            onMouseEnter={(e) => {
                e.currentTarget.style.borderColor = 'var(--primary)';
                e.currentTarget.style.boxShadow = 'var(--shadow-md)';
            }}
            onMouseLeave={(e) => {
                e.currentTarget.style.borderColor = 'var(--border)';
                e.currentTarget.style.boxShadow = 'var(--shadow-sm)';
            }}
        >
            <div style={headerStyles}>
                <div style={iconStyles}>{icon}</div>
                <div style={titleStyles}>{title}</div>
            </div>

            <div style={metricsStyles}>
                <div style={metricStyles}>
                    <div style={metricLabelStyles}>Actual</div>
                    <div style={metricValueStyles}>{currentValue}%</div>
                </div>
                <div style={metricStyles}>
                    <div style={metricLabelStyles}>Objetivo</div>
                    <div style={metricValueStyles}>{targetValue}%</div>
                </div>
                <div style={metricStyles}>
                    <div style={metricLabelStyles}>Brecha</div>
                    <div style={{ ...metricValueStyles, color: 'var(--danger)' }}>
                        {gapPercent}%
                    </div>
                </div>
            </div>

            <div style={opportunityStyles}>
                <div style={opportunityLabelStyles}>Oportunidad de Ingresos</div>
                <div style={opportunityValueStyles}>
                    ${opportunityAmount.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })} USD
                </div>
            </div>

            <div style={recommendationStyles}>
                <strong>💡 Recomendación:</strong> {recommendation}
            </div>
        </div>
    );
};

export default OpportunityCard;
