/**
 * Batch Form Component
 * 
 * Spreadsheet-like interface for bulk data entry
 */

import React, { useState } from 'react';
import { showSuccess, showError } from '../utils/toast';

interface BatchRow {
    id: string;
    [key: string]: any;
}

interface BatchFormProps {
    columns: {
        key: string;
        label: string;
        type?: 'text' | 'number' | 'date' | 'select';
        options?: string[];
        required?: boolean;
    }[];
    onSave: (rows: any[]) => Promise<void>;
    initialRows?: number;
}

const BatchForm: React.FC<BatchFormProps> = ({
    columns,
    onSave,
    initialRows = 5
}) => {
    const [rows, setRows] = useState<BatchRow[]>(() =>
        Array.from({ length: initialRows }, (_, i) => ({
            id: `row-${i}`,
            ...Object.fromEntries(columns.map(col => [col.key, '']))
        }))
    );
    const [loading, setLoading] = useState(false);

    const addRow = () => {
        setRows([
            ...rows,
            {
                id: `row-${Date.now()}`,
                ...Object.fromEntries(columns.map(col => [col.key, '']))
            }
        ]);
    };

    const removeRow = (id: string) => {
        if (rows.length > 1) {
            setRows(rows.filter(row => row.id !== id));
        }
    };

    const duplicateRow = (index: number) => {
        const rowToDuplicate = { ...rows[index], id: `row-${Date.now()}` };
        const newRows = [...rows];
        newRows.splice(index + 1, 0, rowToDuplicate);
        setRows(newRows);
    };

    const updateCell = (rowId: string, columnKey: string, value: any) => {
        setRows(rows.map(row =>
            row.id === rowId ? { ...row, [columnKey]: value } : row
        ));
    };

    const handleSave = async () => {
        // Validate required fields
        const errors: string[] = [];
        rows.forEach((row, index) => {
            columns.forEach(col => {
                if (col.required && !row[col.key]) {
                    errors.push(`Fila ${index + 1}: ${col.label} es requerido`);
                }
            });
        });

        if (errors.length > 0) {
            showError(errors[0]);
            return;
        }

        setLoading(true);
        try {
            // Filter out empty rows
            const validRows = rows.filter(row =>
                columns.some(col => row[col.key])
            );

            await onSave(validRows);
            showSuccess(`${validRows.length} registros guardados exitosamente`);

            // Reset form
            setRows(Array.from({ length: initialRows }, (_, i) => ({
                id: `row-${i}`,
                ...Object.fromEntries(columns.map(col => [col.key, '']))
            })));
        } catch (error) {
            showError('Error al guardar los datos');
            console.error(error);
        } finally {
            setLoading(false);
        }
    };

    const handleKeyDown = (e: React.KeyboardEvent, rowIndex: number, colIndex: number) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            // Move to next row, same column
            const nextRow = document.querySelector(
                `input[data-row="${rowIndex + 1}"][data-col="${colIndex}"]`
            ) as HTMLInputElement;
            if (nextRow) {
                nextRow.focus();
            } else {
                // Add new row if at the end
                addRow();
                setTimeout(() => {
                    const newInput = document.querySelector(
                        `input[data-row="${rowIndex + 1}"][data-col="${colIndex}"]`
                    ) as HTMLInputElement;
                    newInput?.focus();
                }, 50);
            }
        } else if (e.key === 'Tab' && !e.shiftKey) {
            // Default tab behavior (next column)
        }
    };

    return (
        <div style={{ padding: '1rem' }}>
            <div style={{
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                marginBottom: '1rem'
            }}>
                <h3 style={{ margin: 0 }}>Entrada por Lotes</h3>
                <div style={{ display: 'flex', gap: '0.5rem' }}>
                    <button
                        onClick={addRow}
                        style={{
                            padding: '0.5rem 1rem',
                            background: 'var(--primary)',
                            color: 'white',
                            border: 'none',
                            borderRadius: 'var(--radius-md)',
                            cursor: 'pointer'
                        }}
                    >
                        ➕ Agregar Fila
                    </button>
                    <button
                        onClick={handleSave}
                        disabled={loading}
                        style={{
                            padding: '0.5rem 1.5rem',
                            background: 'var(--success)',
                            color: 'white',
                            border: 'none',
                            borderRadius: 'var(--radius-md)',
                            cursor: loading ? 'not-allowed' : 'pointer',
                            opacity: loading ? 0.6 : 1
                        }}
                    >
                        {loading ? '⏳ Guardando...' : '💾 Guardar Todo'}
                    </button>
                </div>
            </div>

            <div style={{
                overflowX: 'auto',
                border: '1px solid var(--border)',
                borderRadius: 'var(--radius-md)'
            }}>
                <table style={{
                    width: '100%',
                    borderCollapse: 'collapse',
                    minWidth: '800px'
                }}>
                    <thead>
                        <tr style={{ background: 'var(--background-secondary)' }}>
                            <th style={{ padding: '0.75rem', textAlign: 'left', width: '40px' }}>#</th>
                            {columns.map(col => (
                                <th key={col.key} style={{ padding: '0.75rem', textAlign: 'left' }}>
                                    {col.label}
                                    {col.required && <span style={{ color: 'var(--danger)' }}> *</span>}
                                </th>
                            ))}
                            <th style={{ padding: '0.75rem', textAlign: 'center', width: '100px' }}>Acciones</th>
                        </tr>
                    </thead>
                    <tbody>
                        {rows.map((row, rowIndex) => (
                            <tr key={row.id} style={{
                                borderBottom: '1px solid var(--border)',
                                background: rowIndex % 2 === 0 ? 'white' : 'var(--background-secondary)'
                            }}>
                                <td style={{ padding: '0.5rem', textAlign: 'center', color: 'var(--text-secondary)' }}>
                                    {rowIndex + 1}
                                </td>
                                {columns.map((col, colIndex) => (
                                    <td key={col.key} style={{ padding: '0.5rem' }}>
                                        {col.type === 'select' ? (
                                            <select
                                                value={row[col.key]}
                                                onChange={(e) => updateCell(row.id, col.key, e.target.value)}
                                                data-row={rowIndex}
                                                data-col={colIndex}
                                                style={{
                                                    width: '100%',
                                                    padding: '0.5rem',
                                                    border: '1px solid var(--border)',
                                                    borderRadius: 'var(--radius-sm)',
                                                    fontSize: '0.9rem'
                                                }}
                                            >
                                                <option value="">Seleccionar...</option>
                                                {col.options?.map(opt => (
                                                    <option key={opt} value={opt}>{opt}</option>
                                                ))}
                                            </select>
                                        ) : (
                                            <input
                                                type={col.type || 'text'}
                                                value={row[col.key]}
                                                onChange={(e) => updateCell(row.id, col.key, e.target.value)}
                                                onKeyDown={(e) => handleKeyDown(e, rowIndex, colIndex)}
                                                data-row={rowIndex}
                                                data-col={colIndex}
                                                style={{
                                                    width: '100%',
                                                    padding: '0.5rem',
                                                    border: '1px solid var(--border)',
                                                    borderRadius: 'var(--radius-sm)',
                                                    fontSize: '0.9rem'
                                                }}
                                                placeholder={col.label}
                                            />
                                        )}
                                    </td>
                                ))}
                                <td style={{ padding: '0.5rem', textAlign: 'center' }}>
                                    <button
                                        onClick={() => duplicateRow(rowIndex)}
                                        title="Duplicar fila"
                                        style={{
                                            padding: '0.25rem 0.5rem',
                                            background: 'transparent',
                                            border: 'none',
                                            cursor: 'pointer',
                                            fontSize: '1.2rem'
                                        }}
                                    >
                                        📋
                                    </button>
                                    <button
                                        onClick={() => removeRow(row.id)}
                                        title="Eliminar fila"
                                        disabled={rows.length === 1}
                                        style={{
                                            padding: '0.25rem 0.5rem',
                                            background: 'transparent',
                                            border: 'none',
                                            cursor: rows.length === 1 ? 'not-allowed' : 'pointer',
                                            fontSize: '1.2rem',
                                            opacity: rows.length === 1 ? 0.3 : 1
                                        }}
                                    >
                                        🗑️
                                    </button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>

            <div style={{
                marginTop: '1rem',
                padding: '1rem',
                background: 'var(--background-secondary)',
                borderRadius: 'var(--radius-md)',
                fontSize: '0.9rem',
                color: 'var(--text-secondary)'
            }}>
                <strong>💡 Atajos de teclado:</strong>
                <ul style={{ margin: '0.5rem 0', paddingLeft: '1.5rem' }}>
                    <li><kbd>Enter</kbd> - Siguiente fila (misma columna)</li>
                    <li><kbd>Tab</kbd> - Siguiente columna</li>
                    <li>📋 - Duplicar fila</li>
                    <li>🗑️ - Eliminar fila</li>
                </ul>
            </div>
        </div>
    );
};

export default BatchForm;
