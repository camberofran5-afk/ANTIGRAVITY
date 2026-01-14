import React from 'react';

interface MetricCardProps {
    label: string;
    value: string | number;
    variant?: 'primary' | 'warning' | 'danger' | 'success';
    icon?: string;
}

const MetricCard: React.FC<MetricCardProps> = ({
    label,
    value,
    variant = 'primary',
    icon
}) => {
    const gradients = {
        primary: 'linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%)',
        warning: 'linear-gradient(135deg, #f59e0b 0%, var(--warning-dark) 100%)',
        danger: 'linear-gradient(135deg, var(--danger) 0%, var(--danger-dark) 100%)',
        success: 'linear-gradient(135deg, var(--success) 0%, #388E3C 100%)'
    };

    const styles: React.CSSProperties = {
        background: gradients[variant],
        color: 'white',
        padding: '1.5rem',
        borderRadius: 'var(--radius-lg)',
        boxShadow: 'var(--shadow-md)',
        minHeight: '120px',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'space-between'
    };

    const labelStyles: React.CSSProperties = {
        fontSize: '0.875rem',
        opacity: 0.9,
        textTransform: 'uppercase',
        letterSpacing: '0.5px',
        fontWeight: 500
    };

    const valueStyles: React.CSSProperties = {
        fontSize: '2.5rem',
        fontWeight: 700,
        margin: '0.5rem 0',
        lineHeight: 1
    };

    return (
        <div style={styles}>
            <div style={labelStyles}>
                {icon && <span style={{ marginRight: '0.5rem' }}>{icon}</span>}
                {label}
            </div>
            <div style={valueStyles}>{value}</div>
        </div>
    );
};

export default MetricCard;
