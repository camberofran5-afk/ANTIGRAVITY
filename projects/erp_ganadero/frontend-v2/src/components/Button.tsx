import React from 'react';

interface ButtonProps {
    variant?: 'primary' | 'secondary' | 'danger' | 'success';
    onClick?: () => void;
    children: React.ReactNode;
    disabled?: boolean;
    type?: 'button' | 'submit' | 'reset';
    fullWidth?: boolean;
}

const Button: React.FC<ButtonProps> = ({
    variant = 'primary',
    onClick,
    children,
    disabled = false,
    type = 'button',
    fullWidth = false
}) => {
    const styles: React.CSSProperties = {
        padding: '0.75rem 1.5rem',
        border: 'none',
        borderRadius: 'var(--radius-md)',
        fontSize: '1rem',
        fontWeight: 500,
        cursor: disabled ? 'not-allowed' : 'pointer',
        transition: 'var(--transition-normal)',
        minHeight: '48px',
        width: fullWidth ? '100%' : 'auto',
        opacity: disabled ? 0.6 : 1,
        ...getVariantStyles(variant)
    };

    return (
        <button
            type={type}
            onClick={onClick}
            disabled={disabled}
            style={styles}
        >
            {children}
        </button>
    );
};

function getVariantStyles(variant: string): React.CSSProperties {
    switch (variant) {
        case 'primary':
            return {
                background: 'var(--primary)',
                color: 'white'
            };
        case 'secondary':
            return {
                background: 'white',
                color: 'var(--primary)',
                border: '2px solid var(--border)'
            };
        case 'danger':
            return {
                background: 'var(--danger)',
                color: 'white'
            };
        case 'success':
            return {
                background: 'var(--success)',
                color: 'white'
            };
        default:
            return {};
    }
}

export default Button;
