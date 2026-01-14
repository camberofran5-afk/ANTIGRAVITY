import React, { useState, useEffect } from 'react';
import { CostCategory } from '../types';
import Input from './Input';
import Select from './Select';
import Button from './Button';

interface CostFormProps {
    ranchId: string;
    onSubmit: (data: {
        ranch_id: string;
        category: CostCategory;
        sub_category?: string;
        amount_mxn: number;
        quantity?: number;
        unit_cost?: number;
        cost_date: string;
        supplier?: string;
        allocated_to?: 'all' | 'specific' | 'group';
        description?: string;
    }) => void;
    onCancel: () => void;
}

const CostForm: React.FC<CostFormProps> = ({ ranchId, onSubmit, onCancel }) => {
    const [category, setCategory] = useState<CostCategory | ''>('');
    const [subCategory, setSubCategory] = useState('');
    const [quantity, setQuantity] = useState<number>(1);
    const [unitCost, setUnitCost] = useState<number>(0);
    const [totalAmount, setTotalAmount] = useState<number>(0);
    const [costDate, setCostDate] = useState(new Date().toISOString().split('T')[0]);
    const [supplier, setSupplier] = useState('');
    const [allocatedTo, setAllocatedTo] = useState<'all' | 'specific' | 'group' | ''>('all');
    const [description, setDescription] = useState('');

    // Auto-calculate total when quantity or unit cost changes
    useEffect(() => {
        if (quantity > 0 && unitCost > 0) {
            setTotalAmount(quantity * unitCost);
        }
    }, [quantity, unitCost]);

    // Calculate unit cost when total changes manually
    const handleTotalChange = (value: string | number) => {
        const numValue = typeof value === 'string' ? parseFloat(value) || 0 : value;
        setTotalAmount(numValue);
        if (quantity > 0) {
            setUnitCost(numValue / quantity);
        }
    };

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();

        if (!category) {
            alert('Por favor selecciona una categoría');
            return;
        }

        if (totalAmount <= 0) {
            alert('El monto total debe ser mayor a 0');
            return;
        }

        onSubmit({
            ranch_id: ranchId,
            category: category as CostCategory,
            sub_category: subCategory || undefined,
            amount_mxn: totalAmount,
            quantity: quantity > 0 ? quantity : undefined,
            unit_cost: unitCost > 0 ? unitCost : undefined,
            cost_date: costDate,
            supplier: supplier || undefined,
            allocated_to: allocatedTo as 'all' | 'specific' | 'group',
            description: description || undefined
        });
    };

    const categoryOptions = [
        { value: 'feed', label: 'Alimento' },
        { value: 'veterinary', label: 'Veterinario' },
        { value: 'labor', label: 'Mano de Obra' },
        { value: 'infrastructure', label: 'Infraestructura' },
        { value: 'other', label: 'Otro' }
    ];

    const allocationOptions = [
        { value: 'all', label: 'Todos los Animales' },
        { value: 'specific', label: 'Animal Específico' },
        { value: 'group', label: 'Grupo de Animales' }
    ];

    return (
        <form onSubmit={handleSubmit}>
            <Select
                label="Categoría"
                value={category}
                onChange={(val) => setCategory(val as CostCategory)}
                options={categoryOptions}
                required
            />

            <Input
                label="Sub-categoría"
                value={subCategory}
                onChange={(val) => setSubCategory(val as string)}
                placeholder="Ej: Alfalfa, Concentrado, Vacuna..."
            />

            <div style={{
                display: 'grid',
                gridTemplateColumns: '1fr 1fr',
                gap: '1rem',
                marginBottom: '1rem'
            }}>
                <Input
                    type="number"
                    label="Cantidad"
                    value={quantity}
                    onChange={(val) => setQuantity(val as number)}
                    min={0}
                    step={0.01}
                />

                <Input
                    type="number"
                    label="Costo Unitario (MXN)"
                    value={unitCost}
                    onChange={(val) => setUnitCost(val as number)}
                    min={0}
                    step={0.01}
                />
            </div>

            <Input
                type="number"
                label="Monto Total (MXN)"
                value={totalAmount}
                onChange={handleTotalChange}
                min={0}
                step={0.01}
                required
            />

            <div style={{
                padding: '0.75rem',
                background: 'var(--primary-light)',
                borderRadius: 'var(--radius-md)',
                marginBottom: '1rem',
                fontSize: '0.875rem',
                color: 'var(--text-secondary)'
            }}>
                💡 <strong>Cálculo automático:</strong> El monto total se calcula multiplicando cantidad × costo unitario.
                También puedes ingresar el total directamente y el costo unitario se calculará automáticamente.
            </div>

            <Input
                type="date"
                label="Fecha del Costo"
                value={costDate}
                onChange={(val) => setCostDate(val as string)}
                required
            />

            <Input
                label="Proveedor"
                value={supplier}
                onChange={(val) => setSupplier(val as string)}
                placeholder="Nombre del proveedor..."
            />

            <Select
                label="Asignación"
                value={allocatedTo}
                onChange={(val) => setAllocatedTo(val as any)}
                options={allocationOptions}
                required
            />

            <div style={{ marginBottom: '1rem' }}>
                <label style={{
                    display: 'block',
                    marginBottom: '0.5rem',
                    fontWeight: 500,
                    fontSize: '0.875rem'
                }}>
                    Descripción
                </label>
                <textarea
                    value={description}
                    onChange={(e) => setDescription(e.target.value)}
                    placeholder="Descripción adicional del costo..."
                    style={{
                        width: '100%',
                        padding: '0.75rem',
                        border: '2px solid var(--border)',
                        borderRadius: 'var(--radius-md)',
                        fontSize: '1rem',
                        fontFamily: 'inherit',
                        minHeight: '80px',
                        resize: 'vertical'
                    }}
                />
            </div>

            <div style={{ display: 'flex', gap: '0.5rem', marginTop: '1.5rem' }}>
                <Button variant="secondary" onClick={onCancel} type="button" fullWidth>
                    Cancelar
                </Button>
                <Button variant="primary" type="submit" fullWidth>
                    Guardar Costo
                </Button>
            </div>
        </form>
    );
};

export default CostForm;
