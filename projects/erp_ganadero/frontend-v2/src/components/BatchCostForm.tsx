/**
 * Batch Cost Form
 * 
 * Specialized batch form for cost entry
 */

import React from 'react';
import BatchForm from './BatchForm';
import { showSuccess, showError } from '../utils/toast';

interface BatchCostFormProps {
    ranchId: string;
    onComplete?: () => void;
}

const BatchCostForm: React.FC<BatchCostFormProps> = ({ ranchId, onComplete }) => {
    const columns = [
        {
            key: 'cost_date',
            label: 'Fecha',
            type: 'date' as const,
            required: true
        },
        {
            key: 'category',
            label: 'Categoría',
            type: 'select' as const,
            options: ['feed', 'veterinary', 'labor', 'infrastructure', 'other'],
            required: true
        },
        {
            key: 'amount_mxn',
            label: 'Monto (MXN)',
            type: 'number' as const,
            required: true
        },
        {
            key: 'description',
            label: 'Descripción',
            type: 'text' as const
        },
        {
            key: 'cattle_id',
            label: 'ID Ganado',
            type: 'text' as const
        }
    ];

    const handleSave = async (rows: any[]) => {
        try {
            const response = await fetch(`/api/v1/batch/costs?ranch_id=${ranchId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                },
                body: JSON.stringify({ records: rows, ranch_id: ranchId })
            });

            if (!response.ok) {
                throw new Error('Failed to import costs');
            }

            const result = await response.json();

            if (result.failed > 0) {
                showError(`${result.imported} importados, ${result.failed} fallidos`);
            } else {
                showSuccess(`${result.imported} costos importados exitosamente`);
            }

            if (onComplete) {
                onComplete();
            }
        } catch (error) {
            showError('Error al importar costos');
            throw error;
        }
    };

    return (
        <div>
            <h2 style={{ marginBottom: '1rem' }}>Entrada por Lotes - Costos</h2>
            <BatchForm
                columns={columns}
                onSave={handleSave}
                initialRows={10}
            />
        </div>
    );
};

export default BatchCostForm;
