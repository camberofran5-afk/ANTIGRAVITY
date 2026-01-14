import React, { useState, useEffect } from 'react';
import { calculations } from '../utils/calculations';

interface AlertBannerProps {
    unproductiveCount: number;
    onDismiss?: () => void;
}

const AlertBanner: React.FC<AlertBannerProps> = ({ unproductiveCount, onDismiss }) => {
    const [isDismissed, setIsDismissed] = useState(false);

    useEffect(() => {
        // Check if banner was previously dismissed
        const dismissed = localStorage.getItem('unproductive-alert-dismissed');
        if (dismissed === 'true') {
            setIsDismissed(true);
        }
    }, []);

    const handleDismiss = () => {
        setIsDismissed(true);
        localStorage.setItem('unproductive-alert-dismissed', 'true');
        if (onDismiss) {
            onDismiss();
        }
    };

    if (isDismissed || unproductiveCount === 0) {
        return null;
    }

    const costs = calculations.unproductiveCost(unproductiveCount);

    const bannerStyles: React.CSSProperties = {
        background: 'linear-gradient(135deg, #FF6F00 0%, #F57C00 100%)',
        color: 'white',
        padding: '1.5rem',
        borderRadius: 'var(--radius-lg)',
        marginBottom: '1.5rem',
        boxShadow: 'var(--shadow-md)',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'flex-start',
        border: '3px solid #F57C00'
    };

    const contentStyles: React.CSSProperties = {
        flex: 1
    };

    const titleStyles: React.CSSProperties = {
        fontSize: '1.25rem',
        fontWeight: 600,
        marginBottom: '0.75rem',
        display: 'flex',
        alignItems: 'center',
        gap: '0.5rem'
    };

    const statsStyles: React.CSSProperties = {
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))',
        gap: '1rem',
        marginTop: '1rem'
    };

    const statBoxStyles: React.CSSProperties = {
        background: 'rgba(255, 255, 255, 0.2)',
        padding: '0.75rem',
        borderRadius: 'var(--radius-md)',
        textAlign: 'center'
    };

    const statValueStyles: React.CSSProperties = {
        fontSize: '1.5rem',
        fontWeight: 700,
        marginBottom: '0.25rem'
    };

    const statLabelStyles: React.CSSProperties = {
        fontSize: '0.75rem',
        opacity: 0.9,
        textTransform: 'uppercase'
    };

    const closeButtonStyles: React.CSSProperties = {
        background: 'rgba(255, 255, 255, 0.2)',
        border: 'none',
        color: 'white',
        fontSize: '1.5rem',
        cursor: 'pointer',
        padding: '0.25rem 0.75rem',
        borderRadius: 'var(--radius-md)',
        marginLeft: '1rem',
        transition: 'var(--transition-normal)'
    };

    return (
        <div style={bannerStyles}>
            <div style={contentStyles}>
                <div style={titleStyles}>
                    <span>⚠️</span>
                    <span>¡Alerta de Vacas Improductivas!</span>
                </div>
                <p style={{ fontSize: '1rem', marginBottom: '0.5rem' }}>
                    Tienes <strong>{unproductiveCount}</strong> vaca{unproductiveCount !== 1 ? 's' : ''} improductiva{unproductiveCount !== 1 ? 's' : ''} que está{unproductiveCount !== 1 ? 'n' : ''} costando dinero sin generar ingresos.
                </p>
                <div style={statsStyles}>
                    <div style={statBoxStyles}>
                        <div style={statValueStyles}>${costs.weekly.toFixed(2)}</div>
                        <div style={statLabelStyles}>Costo Semanal (USD)</div>
                    </div>
                    <div style={statBoxStyles}>
                        <div style={statValueStyles}>${costs.monthly.toFixed(2)}</div>
                        <div style={statLabelStyles}>Costo Mensual (USD)</div>
                    </div>
                    <div style={statBoxStyles}>
                        <div style={statValueStyles}>${costs.annual.toFixed(2)}</div>
                        <div style={statLabelStyles}>Costo Anual (USD)</div>
                    </div>
                </div>
            </div>
            <button
                style={closeButtonStyles}
                onClick={handleDismiss}
                onMouseEnter={(e) => {
                    e.currentTarget.style.background = 'rgba(255, 255, 255, 0.3)';
                }}
                onMouseLeave={(e) => {
                    e.currentTarget.style.background = 'rgba(255, 255, 255, 0.2)';
                }}
            >
                ✕
            </button>
        </div>
    );
};

export default AlertBanner;
