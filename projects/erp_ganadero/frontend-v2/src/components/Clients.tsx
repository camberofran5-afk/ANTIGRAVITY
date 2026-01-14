import React, { useState } from 'react';
import { Client } from '../types';
import Button from './Button';
import Modal from './Modal';
import Input from './Input';
import Select from './Select';

const Clients: React.FC = () => {
    // eslint-disable-next-line @typescript-script/no-unused-vars
    const [clients, _setClients] = useState<Client[]>([]);
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [expandedClient, setExpandedClient] = useState<string | null>(null);

    const [formData, setFormData] = useState({
        name: '',
        type: '' as 'feedlot' | 'butcher' | 'export' | 'rancher' | '',
        phone: '',
        email: '',
        address: '',
        payment_terms: '' as 'cash' | '15_days' | '30_days' | '60_days' | ''
    });

    const resetForm = () => {
        setFormData({
            name: '',
            type: '',
            phone: '',
            email: '',
            address: '',
            payment_terms: ''
        });
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            const response = await fetch('http://localhost:8000/api/v1/clients', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ ranch_id: 'ranch-1', ...formData })
            });
            if (response.ok) {
                alert('Cliente agregado exitosamente');
                setIsModalOpen(false);
                resetForm();
            }
        } catch (err) {
            alert('Error al agregar cliente');
        }
    };

    const getTypeLabel = (type: string): string => {
        const labels: Record<string, string> = {
            'feedlot': 'Engordador',
            'butcher': 'Carnicero',
            'export': 'Exportador',
            'rancher': 'Ganadero'
        };
        return labels[type] || type;
    };

    const getPaymentTermsLabel = (terms: string): string => {
        const labels: Record<string, string> = {
            'cash': 'Contado',
            '15_days': '15 días',
            '30_days': '30 días',
            '60_days': '60 días'
        };
        return labels[terms] || terms;
    };

    // Mock purchase history - in real app, fetch from API
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    const getPurchaseHistory = (_clientId: string) => {
        // TODO: Replace with actual API call
        return [
            { id: '1', date: '2024-01-15', animal_arete: 'A-123', weight_kg: 450, price_per_kg: 65, total: 29250 },
            { id: '2', date: '2024-02-20', animal_arete: 'A-456', weight_kg: 520, price_per_kg: 68, total: 35360 },
            { id: '3', date: '2024-03-10', animal_arete: 'A-789', weight_kg: 480, price_per_kg: 67, total: 32160 }
        ];
    };

    return (
        <div className="container">
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
                <h2 style={{ fontSize: '1.75rem', margin: 0 }}>👥 Clientes</h2>
                <Button variant="primary" onClick={() => { resetForm(); setIsModalOpen(true); }}>
                    ➕ Agregar Cliente
                </Button>
            </div>

            {clients.length === 0 ? (
                <div className="card" style={{ textAlign: 'center', padding: '3rem' }}>
                    <p style={{ fontSize: '1.125rem', color: 'var(--text-secondary)' }}>
                        No hay clientes registrados. Agrega el primer cliente.
                    </p>
                </div>
            ) : (
                <div style={{ display: 'grid', gap: '1rem' }}>
                    {clients.map((client) => {
                        const isExpanded = expandedClient === client.id;
                        const purchases = getPurchaseHistory(client.id);
                        const totalPurchases = purchases.reduce((sum, p) => sum + p.total, 0);

                        return (
                            <div key={client.id} className="card">
                                <div style={{ marginBottom: '1rem' }}>
                                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                                        <div style={{ flex: 1 }}>
                                            <h3 style={{ margin: '0 0 8px 0' }}>{client.name}</h3>
                                            <div style={{ display: 'flex', gap: '8px', marginBottom: '8px' }}>
                                                <span style={{
                                                    padding: '4px 12px',
                                                    backgroundColor: '#2196f3',
                                                    color: 'white',
                                                    borderRadius: '12px',
                                                    fontSize: '12px',
                                                    fontWeight: 'bold'
                                                }}>
                                                    {getTypeLabel(client.type)}
                                                </span>
                                                <span style={{
                                                    padding: '4px 12px',
                                                    backgroundColor: '#4caf50',
                                                    color: 'white',
                                                    borderRadius: '12px',
                                                    fontSize: '12px',
                                                    fontWeight: 'bold'
                                                }}>
                                                    {getPaymentTermsLabel(client.payment_terms)}
                                                </span>
                                            </div>
                                            <div style={{ color: '#666', fontSize: '14px' }}>
                                                {client.contact?.phone && <p style={{ margin: '4px 0' }}>📞 {client.contact.phone}</p>}
                                                {client.contact?.email && <p style={{ margin: '4px 0' }}>📧 {client.contact.email}</p>}
                                                {client.contact?.address && <p style={{ margin: '4px 0' }}>📍 {client.contact.address}</p>}
                                            </div>
                                        </div>
                                        <div style={{ textAlign: 'right' }}>
                                            <div style={{ fontSize: '12px', color: '#666', marginBottom: '4px' }}>
                                                Total Comprado
                                            </div>
                                            <div style={{ fontSize: '20px', fontWeight: 'bold', color: '#4caf50' }}>
                                                ${totalPurchases.toLocaleString('es-MX')}
                                            </div>
                                            <div style={{ fontSize: '12px', color: '#666' }}>
                                                {purchases.length} compra{purchases.length !== 1 ? 's' : ''}
                                            </div>
                                        </div>
                                    </div>
                                </div>

                                {/* Purchase History Toggle */}
                                <div style={{ borderTop: '1px solid #e0e0e0', paddingTop: '12px' }}>
                                    <Button
                                        variant="secondary"
                                        onClick={() => setExpandedClient(isExpanded ? null : client.id)}
                                        fullWidth
                                    >
                                        {isExpanded ? '▼ Ocultar' : '▶ Ver'} Historial de Compras
                                    </Button>

                                    {isExpanded && (
                                        <div style={{ marginTop: '12px' }}>
                                            {purchases.length === 0 ? (
                                                <p style={{ textAlign: 'center', color: '#999', padding: '20px' }}>
                                                    No hay compras registradas
                                                </p>
                                            ) : (
                                                <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                                                    <thead>
                                                        <tr style={{ backgroundColor: '#f5f5f5' }}>
                                                            <th style={{ padding: '8px', textAlign: 'left', fontSize: '12px' }}>Fecha</th>
                                                            <th style={{ padding: '8px', textAlign: 'left', fontSize: '12px' }}>Animal</th>
                                                            <th style={{ padding: '8px', textAlign: 'right', fontSize: '12px' }}>Peso (kg)</th>
                                                            <th style={{ padding: '8px', textAlign: 'right', fontSize: '12px' }}>$/kg</th>
                                                            <th style={{ padding: '8px', textAlign: 'right', fontSize: '12px' }}>Total</th>
                                                        </tr>
                                                    </thead>
                                                    <tbody>
                                                        {purchases.map((purchase) => (
                                                            <tr key={purchase.id} style={{ borderBottom: '1px solid #e0e0e0' }}>
                                                                <td style={{ padding: '8px', fontSize: '14px' }}>
                                                                    {new Date(purchase.date).toLocaleDateString('es-MX')}
                                                                </td>
                                                                <td style={{ padding: '8px', fontSize: '14px' }}>{purchase.animal_arete}</td>
                                                                <td style={{ padding: '8px', textAlign: 'right', fontSize: '14px' }}>
                                                                    {purchase.weight_kg}
                                                                </td>
                                                                <td style={{ padding: '8px', textAlign: 'right', fontSize: '14px' }}>
                                                                    ${purchase.price_per_kg}
                                                                </td>
                                                                <td style={{ padding: '8px', textAlign: 'right', fontSize: '14px', fontWeight: 'bold' }}>
                                                                    ${purchase.total.toLocaleString('es-MX')}
                                                                </td>
                                                            </tr>
                                                        ))}
                                                    </tbody>
                                                </table>
                                            )}
                                        </div>
                                    )}
                                </div>
                            </div>
                        );
                    })}
                </div>
            )}

            <Modal isOpen={isModalOpen} onClose={() => { setIsModalOpen(false); resetForm(); }} title="Nuevo Cliente">
                <form onSubmit={handleSubmit}>
                    <Input
                        label="Nombre"
                        value={formData.name}
                        onChange={(val) => setFormData({ ...formData, name: val as string })}
                        required
                    />
                    <Select
                        label="Tipo"
                        value={formData.type}
                        onChange={(val) => setFormData({ ...formData, type: val as any })}
                        options={[
                            { value: 'feedlot', label: 'Engordador' },
                            { value: 'butcher', label: 'Carnicero' },
                            { value: 'export', label: 'Exportador' },
                            { value: 'rancher', label: 'Ganadero' }
                        ]}
                        required
                    />
                    <Input
                        label="Teléfono"
                        value={formData.phone}
                        onChange={(val) => setFormData({ ...formData, phone: val as string })}
                    />
                    <Input
                        type="email"
                        label="Email"
                        value={formData.email}
                        onChange={(val) => setFormData({ ...formData, email: val as string })}
                    />
                    <Input
                        label="Dirección"
                        value={formData.address}
                        onChange={(val) => setFormData({ ...formData, address: val as string })}
                    />
                    <Select
                        label="Términos de Pago"
                        value={formData.payment_terms}
                        onChange={(val) => setFormData({ ...formData, payment_terms: val as any })}
                        options={[
                            { value: 'cash', label: 'Contado' },
                            { value: '15_days', label: '15 días' },
                            { value: '30_days', label: '30 días' },
                            { value: '60_days', label: '60 días' }
                        ]}
                        required
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

export default Clients;
