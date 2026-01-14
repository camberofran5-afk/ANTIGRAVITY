import React from 'react';

interface SelectOption {
    value: string;
    label: string;
}

interface SelectProps {
    value: string;
    onChange: (value: string) => void;
    options: SelectOption[];
    label?: string;
    required?: boolean;
    placeholder?: string;
    disabled?: boolean;
}

const Select: React.FC<SelectProps> = ({
    value,
    onChange,
    options,
    label,
    required = false,
    placeholder = 'Seleccionar...',
    disabled = false
}) => {
    const handleChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
        onChange(e.target.value);
    };

    const selectStyles: React.CSSProperties = {
        width: '100%',
        padding: '0.75rem',
        border: '2px solid var(--border)',
        borderRadius: 'var(--radius-md)',
        fontSize: '1rem',
        fontFamily: 'inherit',
        minHeight: '48px',
        transition: 'var(--transition-normal)',
        backgroundColor: disabled ? 'var(--bg-primary)' : 'white',
        cursor: disabled ? 'not-allowed' : 'pointer'
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
            <select
                value={value}
                onChange={handleChange}
                required={required}
                disabled={disabled}
                style={selectStyles}
                onFocus={(e) => {
                    e.target.style.borderColor = 'var(--primary)';
                    e.target.style.boxShadow = '0 0 0 4px rgba(46, 125, 50, 0.1)';
                }}
                onBlur={(e) => {
                    e.target.style.borderColor = 'var(--border)';
                    e.target.style.boxShadow = 'none';
                }}
            >
                <option value="">{placeholder}</option>
                {options.map((option) => (
                    <option key={option.value} value={option.value}>
                        {option.label}
                    </option>
                ))}
            </select>
        </div>
    );
};

export default Select;
