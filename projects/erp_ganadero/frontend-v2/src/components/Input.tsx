import React from 'react';

interface InputProps {
    type?: 'text' | 'number' | 'date' | 'email' | 'tel';
    value: string | number;
    onChange: (value: string | number) => void;
    label?: string;
    placeholder?: string;
    required?: boolean;
    min?: number;
    max?: number;
    step?: number;
    disabled?: boolean;
}

const Input: React.FC<InputProps> = ({
    type = 'text',
    value,
    onChange,
    label,
    placeholder,
    required = false,
    min,
    max,
    step,
    disabled = false
}) => {
    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const newValue = type === 'number' ? parseFloat(e.target.value) || 0 : e.target.value;
        onChange(newValue);
    };

    const inputStyles: React.CSSProperties = {
        width: '100%',
        padding: '0.75rem',
        border: '2px solid var(--border)',
        borderRadius: 'var(--radius-md)',
        fontSize: '1rem',
        fontFamily: 'inherit',
        minHeight: '48px',
        transition: 'var(--transition-normal)',
        backgroundColor: disabled ? 'var(--bg-primary)' : 'white',
        cursor: disabled ? 'not-allowed' : 'text'
    };

    const labelStyles: React.CSSProperties = {
        display: 'block',
        marginBottom: '0.5rem',
        fontWeight: 500,
        color: 'var(--text-primary)',
        fontSize: '0.875rem'
    };

    const containerStyles: React.CSSProperties = {
        marginBottom: '1rem'
    };

    return (
        <div style={containerStyles}>
            {label && (
                <label style={labelStyles}>
                    {label}
                    {required && <span style={{ color: 'var(--danger)', marginLeft: '0.25rem' }}>*</span>}
                </label>
            )}
            <input
                type={type}
                value={value}
                onChange={handleChange}
                placeholder={placeholder}
                required={required}
                min={min}
                max={max}
                step={step}
                disabled={disabled}
                style={inputStyles}
                onFocus={(e) => {
                    e.target.style.borderColor = 'var(--primary)';
                    e.target.style.boxShadow = '0 0 0 4px rgba(46, 125, 50, 0.1)';
                }}
                onBlur={(e) => {
                    e.target.style.borderColor = 'var(--border)';
                    e.target.style.boxShadow = 'none';
                }}
            />
        </div>
    );
};

export default Input;
