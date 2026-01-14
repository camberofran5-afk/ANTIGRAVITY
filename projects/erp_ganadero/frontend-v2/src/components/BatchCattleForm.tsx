/**
 * Batch Cattle Form
 * 
 * Specialized batch form for cattle entry
 */

import React from 'react';
import BatchForm from './BatchForm';
import { showSuccess, showError } from '../utils/toast';

interface BatchCattleFormProps {
    ranchId: string;
    onComplete?: () => void;
}

const BatchCattleForm: React.FC<BatchCattleFormProps> = ({ ranchId, onComplete }) => {
    const columns = [
        {
            key: 'arete_number',
            label: 'Arete',
            type: 'text' as const,
            required: true
        },
        {
            key: 'species',
            label: 'Especie',
            type: 'select' as const,
            options: ['vaca', 'toro', 'becerro', 'vaquilla'],
            required: true
        },
        {
            key: 'gender',
            label: 'Género',
            type: 'select' as const,
            options: ['M', 'F'],
            required: true
        },
        {
            key: 'birth_date',
            label: 'Fecha Nacimiento',
            type: 'date' as const,
            required: true
        },
        {
            key: 'weight_kg',
            label: 'Peso (kg)',
            type: 'number' as const
        },
        {
            key: 'mother_id',
            label: 'ID Madre',
            type: 'text' as const
        },
        {
            key: 'notes',
            label: 'Notas',
            type: 'text' as const
        }
    ];

    const handleSave = async (rows: any[]) => {
        try {
            const response = await fetch(`/api/v1/batch/cattle?ranch_id=${ranchId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                },
                body: JSON.stringify({ records: rows, ranch_id: ranchId })
            });

            if (!response.ok) {
                throw new Error('Failed to import cattle');
            }

            const result = await response.json();

            if (result.failed > 0) {
                showError(`${result.imported} importados, ${result.failed} fallidos`);
            } else {
                showSuccess(`${result.imported} animales importados exitosamente`);
            }

            if (onComplete) {
                onComplete();
            }
        } catch (error) {
            showError('Error al importar ganado');
            throw error;
        }
    };

    return (
        <div>
            <h2 style={{ marginBottom: '1rem' }}>Entrada por Lotes - Ganado</h2>
            <BatchForm
                columns={columns}
                onSave={handleSave}
                initialRows={10}
            />
        </div>
    );
};

export default BatchCattleForm;
