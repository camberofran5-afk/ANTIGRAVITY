import React, { useState } from 'react';
import { InventoryItem } from '../types';
import Button from './Button';
import Modal from './Modal';
import Input from './Input';
import Select from './Select';

const Inventory: React.FC = () => {
    const [items, _setItems] = useState<InventoryItem[]>([]);
    const [_loading, _setLoading] = useState(false);
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [_editingItem, setEditingItem] = useState<InventoryItem | null>(null);

    const [formData, setFormData] = useState({
        category: '' as 'feed' | 'medicine' | 'vaccine' | 'equipment' | '',
        name: '',
        quantity: 0,
        unit: '',
        unit_cost: 0,
        supplier: '',
        min_stock: 0
    });

    const resetForm = () => {
        setEditingItem(null);
        setFormData({
            category: '',
            name: '',
            quantity: 0,
            unit: '',
            unit_cost: 0,
            supplier: '',
            min_stock: 0
        });
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            const response = await fetch('http://localhost:8000/api/v1/inventory', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ ranch_id: 'ranch-1', ...formData, total_value: formData.quantity * formData.unit_cost })
            });
            if (response.ok) {
                alert('Item agregado exitosamente');
                setIsModalOpen(false);
            }
        } catch (err) {
            alert('Error al agregar item');
        }
        setIsModalOpen(false);
        resetForm();
    };

    const getCategoryIcon = (category: string) => {
        const icons: Record<string, string> = {
            feed: '🌾',
            medicine: '💊',
            vaccine: '💉',
            equipment: '🔧'
        };
        return icons[category] || '📦';
    };

    const isLowStock = (item: InventoryItem): boolean => {
        return item.min_stock !== undefined && item.quantity <= item.min_stock;
    };

    const isExpiringSoon = (item: InventoryItem): boolean => {
        if (!item.expiry_date) return false;
        const expiryDate = new Date(item.expiry_date);
        const today = new Date();
        const daysUntilExpiry = Math.ceil((expiryDate.getTime() - today.getTime()) / (1000 * 60 * 60 * 24));
        return daysUntilExpiry <= 30 && daysUntilExpiry >= 0;
    };

    const getDaysUntilExpiry = (expiryDate: string): number => {
        const expiry = new Date(expiryDate);
        const today = new Date();
        return Math.ceil((expiry.getTime() - today.getTime()) / (1000 * 60 * 60 * 24));
    };

    return (
        <div className="container">
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
                <h2 style={{ fontSize: '1.75rem', margin: 0 }}>📦 Inventario</h2>
                <Button variant="primary" onClick={() => { resetForm(); setIsModalOpen(true); }}>
                    ➕ Agregar Item
                </Button>
            </div>

            {items.length === 0 ? (
                <div className="card" style={{ textAlign: 'center', padding: '3rem' }}>
                    <p style={{ fontSize: '1.125rem', color: 'var(--text-secondary)' }}>
                        No hay items en inventario. Agrega el primer item.
                    </p>
                </div>
            ) : (
                <div style={{ display: 'grid', gap: '1rem' }}>
                    {items.map((item) => {
                        const lowStock = isLowStock(item);
                        const expiring = isExpiringSoon(item);

                        return (
                            <div key={item.id} className="card" style={{
                                borderLeft: lowStock ? '4px solid #f44336' : expiring ? '4px solid #ff9800' : undefined
                            }}>
                                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                                    <div style={{ flex: 1 }}>
                                        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.5rem' }}>
                                            <h3 style={{ margin: 0 }}>{getCategoryIcon(item.category)} {item.name}</h3>

                                            {/* Low Stock Badge */}
                                            {lowStock && (
                                                <span style={{
                                                    padding: '4px 8px',
                                                    backgroundColor: '#f44336',
                                                    color: 'white',
                                                    borderRadius: '12px',
                                                    fontSize: '12px',
                                                    fontWeight: 'bold'
                                                }}>
                                                    ⚠️ STOCK BAJO
                                                </span>
                                            )}

                                            {/* Expiry Warning Badge */}
                                            {expiring && item.expiry_date && (
                                                <span style={{
                                                    padding: '4px 8px',
                                                    backgroundColor: '#ff9800',
                                                    color: 'white',
                                                    borderRadius: '12px',
                                                    fontSize: '12px',
                                                    fontWeight: 'bold'
                                                }}>
                                                    ⏰ {getDaysUntilExpiry(item.expiry_date)} días
                                                </span>
                                            )}
                                        </div>

                                        <div style={{ color: '#666', fontSize: '14px' }}>
                                            <p style={{ margin: '4px 0' }}>
                                                <strong>Cantidad:</strong> {item.quantity} {item.unit}
                                                {lowStock && ` (Mínimo: ${item.min_stock} ${item.unit})`}
                                            </p>
                                            <p style={{ margin: '4px 0' }}>
                                                <strong>Costo:</strong> ${item.unit_cost.toFixed(2)}/unidad
                                                {' • '}
                                                <strong>Total:</strong> ${(item.quantity * item.unit_cost).toFixed(2)}
                                            </p>
                                            {item.supplier && (
                                                <p style={{ margin: '4px 0' }}>
                                                    <strong>Proveedor:</strong> {item.supplier}
                                                </p>
                                            )}
                                            {item.expiry_date && (
                                                <p style={{ margin: '4px 0' }}>
                                                    <strong>Vencimiento:</strong> {new Date(item.expiry_date).toLocaleDateString('es-MX')}
                                                </p>
                                            )}
                                        </div>
                                    </div>
                                    <div style={{ display: 'flex', gap: '0.5rem' }}>
                                        <Button variant="secondary" onClick={() => { }}>Editar</Button>
                                        <Button variant="danger" onClick={() => { }}>Eliminar</Button>
                                    </div>
                                </div>
                            </div>
                        );
                    })}
                </div>
            )}

            <Modal isOpen={isModalOpen} onClose={() => { setIsModalOpen(false); resetForm(); }} title="Nuevo Item de Inventario">
                <form onSubmit={handleSubmit}>
                    <Select
                        label="Categoría"
                        value={formData.category}
                        onChange={(val) => setFormData({ ...formData, category: val as any })}
                        options={[
                            { value: 'feed', label: 'Alimento' },
                            { value: 'medicine', label: 'Medicina' },
                            { value: 'vaccine', label: 'Vacuna' },
                            { value: 'equipment', label: 'Equipo' }
                        ]}
                        required
                    />
                    <Input
                        label="Nombre"
                        value={formData.name}
                        onChange={(val) => setFormData({ ...formData, name: val as string })}
                        required
                    />
                    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
                        <Input
                            type="number"
                            label="Cantidad"
                            value={formData.quantity}
                            onChange={(val) => setFormData({ ...formData, quantity: val as number })}
                            min={0}
                            required
                        />
                        <Input
                            label="Unidad"
                            value={formData.unit}
                            onChange={(val) => setFormData({ ...formData, unit: val as string })}
                            placeholder="kg, litros, piezas..."
                            required
                        />
                    </div>
                    <Input
                        type="number"
                        label="Costo Unitario (MXN)"
                        value={formData.unit_cost}
                        onChange={(val) => setFormData({ ...formData, unit_cost: val as number })}
                        min={0}
                        step={0.01}
                        required
                    />
                    <Input
                        label="Proveedor"
                        value={formData.supplier}
                        onChange={(val) => setFormData({ ...formData, supplier: val as string })}
                    />
                    <Input
                        type="number"
                        label="Stock Mínimo"
                        value={formData.min_stock}
                        onChange={(val) => setFormData({ ...formData, min_stock: val as number })}
                        min={0}
                    />
                    <div style={{ display: 'flex', gap: '0.5rem', marginTop: '1.5rem' }}>
                        <Button variant="secondary" onClick={() => { setIsModalOpen(false); resetForm(); }} type="button" fullWidth>
                            Cancelar
                        </Button>
                        <Button variant="primary" type="submit" fullWidth>
                            Guardar
                        </Button>
                    </div>
                </form>
            </Modal>
        </div>
    );
};

export default Inventory;
