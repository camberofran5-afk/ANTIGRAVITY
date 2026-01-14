/**
 * CSV Upload Component
 * 
 * Drag & drop CSV file uploader with preview
 */

import React, { useState, useCallback } from 'react';
import { parseCSV, CSVParseResult } from '../utils/csvParser';
import { showSuccess, showError } from '../utils/toast';

interface CSVUploadProps {
    onDataParsed: (data: any[], headers: string[]) => void;
    acceptedFileTypes?: string;
}

const CSVUpload: React.FC<CSVUploadProps> = ({
    onDataParsed,
    acceptedFileTypes = '.csv'
}) => {
    const [isDragging, setIsDragging] = useState(false);
    const [parseResult, setParseResult] = useState<CSVParseResult | null>(null);
    const [loading, setLoading] = useState(false);

    const handleFile = useCallback(async (file: File) => {
        if (!file.name.endsWith('.csv')) {
            showError('Por favor selecciona un archivo CSV');
            return;
        }

        setLoading(true);
        try {
            const result = await parseCSV(file);

            if (result.errors.length > 0) {
                showError(`Errores en el archivo: ${result.errors[0]}`);
            } else {
                setParseResult(result);
                showSuccess(`${result.data.length} filas cargadas exitosamente`);
            }
        } catch (error) {
            showError('Error al leer el archivo CSV');
            console.error(error);
        } finally {
            setLoading(false);
        }
    }, []);

    const handleDrop = useCallback((e: React.DragEvent) => {
        e.preventDefault();
        setIsDragging(false);

        const file = e.dataTransfer.files[0];
        if (file) {
            handleFile(file);
        }
    }, [handleFile]);

    const handleDragOver = useCallback((e: React.DragEvent) => {
        e.preventDefault();
        setIsDragging(true);
    }, []);

    const handleDragLeave = useCallback(() => {
        setIsDragging(false);
    }, []);

    const handleFileInput = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0];
        if (file) {
            handleFile(file);
        }
    }, [handleFile]);

    const handleConfirm = () => {
        if (parseResult) {
            onDataParsed(parseResult.data, parseResult.headers);
            setParseResult(null);
        }
    };

    const handleCancel = () => {
        setParseResult(null);
    };

    return (
        <div style={{ padding: '1rem' }}>
            {!parseResult ? (
                <div
                    onDrop={handleDrop}
                    onDragOver={handleDragOver}
                    onDragLeave={handleDragLeave}
                    style={{
                        border: `2px dashed ${isDragging ? 'var(--primary)' : 'var(--border)'}`,
                        borderRadius: 'var(--radius-lg)',
                        padding: '3rem 2rem',
                        textAlign: 'center',
                        background: isDragging ? 'rgba(76, 175, 80, 0.05)' : 'var(--background-secondary)',
                        transition: 'all 0.3s ease',
                        cursor: 'pointer'
                    }}
                >
                    <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>
                        📁
                    </div>
                    <h3 style={{ margin: '0 0 0.5rem 0', color: 'var(--text-primary)' }}>
                        {loading ? 'Procesando archivo...' : 'Arrastra tu archivo CSV aquí'}
                    </h3>
                    <p style={{ margin: '0 0 1rem 0', color: 'var(--text-secondary)' }}>
                        o haz clic para seleccionar
                    </p>
                    <input
                        type="file"
                        accept={acceptedFileTypes}
                        onChange={handleFileInput}
                        disabled={loading}
                        style={{ display: 'none' }}
                        id="csv-file-input"
                    />
                    <label htmlFor="csv-file-input">
                        <button
                            onClick={() => document.getElementById('csv-file-input')?.click()}
                            disabled={loading}
                            style={{
                                padding: '0.75rem 1.5rem',
                                background: 'var(--primary)',
                                color: 'white',
                                border: 'none',
                                borderRadius: 'var(--radius-md)',
                                cursor: loading ? 'not-allowed' : 'pointer',
                                fontSize: '1rem',
                                fontWeight: 500,
                                opacity: loading ? 0.6 : 1
                            }}
                        >
                            {loading ? '⏳ Cargando...' : '📂 Seleccionar Archivo'}
                        </button>
                    </label>
                </div>
            ) : (
                <div>
                    <div style={{
                        background: 'var(--background-secondary)',
                        padding: '1rem',
                        borderRadius: 'var(--radius-md)',
                        marginBottom: '1rem'
                    }}>
                        <h3 style={{ margin: '0 0 0.5rem 0' }}>Vista Previa</h3>
                        <p style={{ margin: 0, color: 'var(--text-secondary)' }}>
                            {parseResult.data.length} filas • {parseResult.headers.length} columnas
                        </p>
                    </div>

                    <div style={{
                        overflowX: 'auto',
                        border: '1px solid var(--border)',
                        borderRadius: 'var(--radius-md)',
                        marginBottom: '1rem'
                    }}>
                        <table style={{
                            width: '100%',
                            borderCollapse: 'collapse',
                            minWidth: '600px'
                        }}>
                            <thead>
                                <tr style={{ background: 'var(--background-secondary)' }}>
                                    {parseResult.headers.map(header => (
                                        <th key={header} style={{
                                            padding: '0.75rem',
                                            textAlign: 'left',
                                            borderBottom: '2px solid var(--border)',
                                            fontWeight: 600
                                        }}>
                                            {header}
                                        </th>
                                    ))}
                                </tr>
                            </thead>
                            <tbody>
                                {parseResult.data.slice(0, 5).map((row, index) => (
                                    <tr key={index} style={{
                                        borderBottom: '1px solid var(--border)'
                                    }}>
                                        {parseResult.headers.map(header => (
                                            <td key={header} style={{
                                                padding: '0.75rem',
                                                color: 'var(--text-primary)'
                                            }}>
                                                {row[header]}
                                            </td>
                                        ))}
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>

                    {parseResult.data.length > 5 && (
                        <p style={{
                            textAlign: 'center',
                            color: 'var(--text-secondary)',
                            fontSize: '0.9rem',
                            marginBottom: '1rem'
                        }}>
                            Mostrando 5 de {parseResult.data.length} filas
                        </p>
                    )}

                    <div style={{
                        display: 'flex',
                        gap: '1rem',
                        justifyContent: 'flex-end'
                    }}>
                        <button
                            onClick={handleCancel}
                            style={{
                                padding: '0.75rem 1.5rem',
                                background: 'transparent',
                                color: 'var(--text-primary)',
                                border: '1px solid var(--border)',
                                borderRadius: 'var(--radius-md)',
                                cursor: 'pointer',
                                fontSize: '1rem'
                            }}
                        >
                            Cancelar
                        </button>
                        <button
                            onClick={handleConfirm}
                            style={{
                                padding: '0.75rem 1.5rem',
                                background: 'var(--success)',
                                color: 'white',
                                border: 'none',
                                borderRadius: 'var(--radius-md)',
                                cursor: 'pointer',
                                fontSize: '1rem',
                                fontWeight: 500
                            }}
                        >
                            ✓ Continuar con {parseResult.data.length} filas
                        </button>
                    </div>
                </div>
            )}
        </div>
    );
};

export default CSVUpload;
