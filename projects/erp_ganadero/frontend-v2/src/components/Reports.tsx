import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import type { Animal, Event, InventoryItem, Client, Cost } from '../types';
import {
    generateInventoryReport,
    generateSalesReport,
    generateFinancialReport,
    generateKPIReport
} from '../utils/reportGenerators';

type ReportType = 'inventory' | 'sales' | 'financial' | 'kpi';

interface DateRange {
    start: string;
    end: string;
}

const Reports: React.FC = () => {
    const [activeTab, setActiveTab] = useState<ReportType>('inventory');
    const [dateRange, setDateRange] = useState<DateRange>({
        start: new Date(new Date().setMonth(new Date().getMonth() - 1)).toISOString().split('T')[0],
        end: new Date().toISOString().split('T')[0]
    });
    const [loading, setLoading] = useState(false);

    // Data states
    const [animals, setAnimals] = useState<Animal[]>([]);
    const [events, setEvents] = useState<Event[]>([]);
    const [inventory, setInventory] = useState<InventoryItem[]>([]);
    const [clients, setClients] = useState<Client[]>([]);
    const [costs, setCosts] = useState<Cost[]>([]);

    const RANCH_ID = 'ranch-1'; // TODO: Get from auth context

    // Fetch all data
    useEffect(() => {
        fetchAllData();
    }, []);

    const fetchAllData = async () => {
        setLoading(true);
        try {
            // Fetch all data in parallel for better performance
            const [animalsData, eventsData, inventoryData, clientsData, costsData] = await Promise.all([
                api.getAnimals(RANCH_ID),
                api.getEventsByRanch(RANCH_ID),
                api.getInventory(RANCH_ID),
                api.getClients(RANCH_ID),
                api.getCosts(RANCH_ID)
            ]);

            setAnimals(Array.isArray(animalsData) ? animalsData : []);
            setEvents(Array.isArray(eventsData) ? eventsData : []);
            setInventory(Array.isArray(inventoryData) ? inventoryData : []);
            setClients(Array.isArray(clientsData) ? clientsData : []);
            setCosts(Array.isArray(costsData) ? costsData : []);
        } catch (error) {
            console.error('Error fetching data:', error);
            // Set empty arrays on error to prevent crashes
            setAnimals([]);
            setEvents([]);
            setInventory([]);
            setClients([]);
            setCosts([]);
        } finally {
            setLoading(false);
        }
    };

    const handleGenerateReport = () => {
        switch (activeTab) {
            case 'inventory':
                generateInventoryReport(inventory);
                break;
            case 'sales':
                const salesEvents = events.filter(e => e.type === 'sale');
                generateSalesReport(salesEvents, animals, clients, dateRange);
                break;
            case 'financial':
                const salesForFinancial = events.filter(e => e.type === 'sale');
                generateFinancialReport(costs, salesForFinancial, dateRange);
                break;
            case 'kpi':
                generateKPIReport(animals, events, dateRange);
                break;
        }
    };

    const tabs = [
        { id: 'inventory' as ReportType, label: '📦 Inventario', icon: '📦' },
        { id: 'sales' as ReportType, label: '💰 Ventas', icon: '💰' },
        { id: 'financial' as ReportType, label: '📊 Financiero', icon: '📊' },
        { id: 'kpi' as ReportType, label: '📈 KPIs', icon: '📈' }
    ];

    const renderPreview = () => {
        switch (activeTab) {
            case 'inventory':
                return <InventoryPreview items={inventory} />;
            case 'sales':
                return <SalesPreview events={events.filter(e => e.type === 'sale')} dateRange={dateRange} />;
            case 'financial':
                return <FinancialPreview costs={costs} sales={events.filter(e => e.type === 'sale')} dateRange={dateRange} />;
            case 'kpi':
                return <KPIPreview animals={animals} events={events} dateRange={dateRange} />;
        }
    };

    if (loading) {
        return (
            <div style={{ padding: '40px', textAlign: 'center' }}>
                <div style={{ fontSize: '48px', marginBottom: '20px' }}>📊</div>
                <p style={{ color: '#666' }}>Cargando datos...</p>
            </div>
        );
    }

    return (
        <div style={{ padding: '20px', maxWidth: '1200px', margin: '0 auto' }}>
            <div style={{ marginBottom: '30px' }}>
                <h1 style={{ fontSize: '28px', marginBottom: '8px', color: '#333' }}>📊 Reportes</h1>
                <p style={{ color: '#666', margin: 0 }}>Genera y descarga reportes en PDF</p>
            </div>

            {/* Date Range Selector */}
            <div style={{
                background: 'white',
                padding: '20px',
                borderRadius: '12px',
                marginBottom: '20px',
                boxShadow: '0 2px 8px rgba(0,0,0,0.1)'
            }}>
                <div style={{ display: 'flex', gap: '20px', alignItems: 'center', flexWrap: 'wrap' }}>
                    <div>
                        <label style={{ display: 'block', fontSize: '12px', color: '#666', marginBottom: '4px' }}>
                            Fecha Inicio
                        </label>
                        <input
                            type="date"
                            value={dateRange.start}
                            onChange={(e) => setDateRange({ ...dateRange, start: e.target.value })}
                            style={{
                                padding: '8px 12px',
                                border: '1px solid #ddd',
                                borderRadius: '8px',
                                fontSize: '14px'
                            }}
                        />
                    </div>
                    <div>
                        <label style={{ display: 'block', fontSize: '12px', color: '#666', marginBottom: '4px' }}>
                            Fecha Fin
                        </label>
                        <input
                            type="date"
                            value={dateRange.end}
                            onChange={(e) => setDateRange({ ...dateRange, end: e.target.value })}
                            style={{
                                padding: '8px 12px',
                                border: '1px solid #ddd',
                                borderRadius: '8px',
                                fontSize: '14px'
                            }}
                        />
                    </div>
                    <button
                        onClick={() => {
                            const today = new Date().toISOString().split('T')[0];
                            const lastMonth = new Date(new Date().setMonth(new Date().getMonth() - 1)).toISOString().split('T')[0];
                            setDateRange({ start: lastMonth, end: today });
                        }}
                        style={{
                            padding: '8px 16px',
                            background: '#f5f5f5',
                            border: 'none',
                            borderRadius: '8px',
                            cursor: 'pointer',
                            fontSize: '14px',
                            marginTop: '18px'
                        }}
                    >
                        Último Mes
                    </button>
                </div>
            </div>

            {/* Tabs */}
            <div style={{
                display: 'flex',
                gap: '10px',
                marginBottom: '20px',
                borderBottom: '2px solid #f0f0f0',
                overflowX: 'auto',
                WebkitOverflowScrolling: 'touch',
                scrollbarWidth: 'thin'
            }}>
                {tabs.map(tab => (
                    <button
                        key={tab.id}
                        onClick={() => setActiveTab(tab.id)}
                        style={{
                            padding: '12px 20px',
                            background: activeTab === tab.id ? 'white' : 'transparent',
                            border: 'none',
                            borderBottom: activeTab === tab.id ? '3px solid #2196f3' : '3px solid transparent',
                            cursor: 'pointer',
                            fontSize: '15px',
                            fontWeight: activeTab === tab.id ? 'bold' : 'normal',
                            color: activeTab === tab.id ? '#2196f3' : '#666',
                            transition: 'all 0.2s',
                            whiteSpace: 'nowrap',
                            minWidth: '120px',
                            flexShrink: 0
                        }}
                    >
                        {tab.label}
                    </button>
                ))}
            </div>

            {/* Preview Section */}
            <div style={{
                background: 'white',
                padding: '30px',
                borderRadius: '12px',
                marginBottom: '20px',
                boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
                minHeight: '400px'
            }}>
                {renderPreview()}
            </div>

            {/* Download Button */}
            <div style={{ textAlign: 'center', padding: '0 20px' }}>
                <button
                    onClick={handleGenerateReport}
                    style={{
                        padding: '16px 48px',
                        background: 'linear-gradient(135deg, #2196f3 0%, #1976d2 100%)',
                        color: 'white',
                        border: 'none',
                        borderRadius: '12px',
                        fontSize: '16px',
                        fontWeight: 'bold',
                        cursor: 'pointer',
                        boxShadow: '0 4px 12px rgba(33, 150, 243, 0.3)',
                        transition: 'transform 0.2s',
                        width: '100%',
                        maxWidth: '400px'
                    }}
                    onMouseOver={(e) => e.currentTarget.style.transform = 'translateY(-2px)'}
                    onMouseOut={(e) => e.currentTarget.style.transform = 'translateY(0)'}
                >
                    📥 Descargar PDF
                </button>
            </div>
        </div>
    );
};

// Preview Components
const InventoryPreview: React.FC<{ items: InventoryItem[] }> = ({ items }) => {
    const totalValue = items.reduce((sum, item) => sum + item.total_value, 0);
    const lowStock = items.filter(i => i.min_stock && i.quantity <= i.min_stock).length;

    return (
        <div>
            <h2 style={{ fontSize: '20px', marginBottom: '20px', color: '#333' }}>Vista Previa - Inventario</h2>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '16px', marginBottom: '24px' }}>
                <div style={{ padding: '16px', background: '#f5f5f5', borderRadius: '8px' }}>
                    <div style={{ fontSize: '12px', color: '#666', marginBottom: '4px' }}>Total Artículos</div>
                    <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#2196f3' }}>{items.length}</div>
                </div>
                <div style={{ padding: '16px', background: '#f5f5f5', borderRadius: '8px' }}>
                    <div style={{ fontSize: '12px', color: '#666', marginBottom: '4px' }}>Valor Total</div>
                    <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#4caf50' }}>
                        ${totalValue.toLocaleString('es-MX', { minimumFractionDigits: 2 })}
                    </div>
                </div>
                <div style={{ padding: '16px', background: '#f5f5f5', borderRadius: '8px' }}>
                    <div style={{ fontSize: '12px', color: '#666', marginBottom: '4px' }}>Stock Bajo</div>
                    <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#f44336' }}>{lowStock}</div>
                </div>
            </div>
            <p style={{ color: '#666', fontSize: '14px' }}>
                El reporte incluirá una tabla detallada con todos los artículos, cantidades, valores y alertas.
            </p>
        </div>
    );
};

const SalesPreview: React.FC<{ events: Event[], dateRange: DateRange }> = ({ events, dateRange }) => {
    const filteredSales = events.filter(e => {
        const date = new Date(e.event_date);
        return date >= new Date(dateRange.start) && date <= new Date(dateRange.end);
    });

    const totalRevenue = filteredSales.reduce((sum, sale) => sum + (sale.data.total_price || 0), 0);
    const totalWeight = filteredSales.reduce((sum, sale) => sum + (sale.data.sale_weight_kg || 0), 0);

    return (
        <div>
            <h2 style={{ fontSize: '20px', marginBottom: '20px', color: '#333' }}>Vista Previa - Ventas</h2>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '16px', marginBottom: '24px' }}>
                <div style={{ padding: '16px', background: '#f5f5f5', borderRadius: '8px' }}>
                    <div style={{ fontSize: '12px', color: '#666', marginBottom: '4px' }}>Total Ventas</div>
                    <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#2196f3' }}>{filteredSales.length}</div>
                </div>
                <div style={{ padding: '16px', background: '#f5f5f5', borderRadius: '8px' }}>
                    <div style={{ fontSize: '12px', color: '#666', marginBottom: '4px' }}>Ingresos</div>
                    <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#4caf50' }}>
                        ${totalRevenue.toLocaleString('es-MX', { minimumFractionDigits: 2 })}
                    </div>
                </div>
                <div style={{ padding: '16px', background: '#f5f5f5', borderRadius: '8px' }}>
                    <div style={{ fontSize: '12px', color: '#666', marginBottom: '4px' }}>Peso Total</div>
                    <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#ff9800' }}>{totalWeight.toFixed(0)} kg</div>
                </div>
            </div>
            <p style={{ color: '#666', fontSize: '14px' }}>
                El reporte incluirá detalles de cada venta: fecha, animal, cliente, peso, precio y estado de pago.
            </p>
        </div>
    );
};

const FinancialPreview: React.FC<{ costs: Cost[], sales: Event[], dateRange: DateRange }> = ({ costs, sales, dateRange }) => {
    const filteredCosts = costs.filter(c => {
        const date = new Date(c.cost_date);
        return date >= new Date(dateRange.start) && date <= new Date(dateRange.end);
    });

    const filteredSales = sales.filter(s => {
        const date = new Date(s.event_date);
        return date >= new Date(dateRange.start) && date <= new Date(dateRange.end);
    });

    const totalCosts = filteredCosts.reduce((sum, c) => sum + c.amount_mxn, 0);
    const totalRevenue = filteredSales.reduce((sum, s) => sum + (s.data.total_price || 0), 0);
    const profit = totalRevenue - totalCosts;

    return (
        <div>
            <h2 style={{ fontSize: '20px', marginBottom: '20px', color: '#333' }}>Vista Previa - Resumen Financiero</h2>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '16px', marginBottom: '24px' }}>
                <div style={{ padding: '16px', background: '#f5f5f5', borderRadius: '8px' }}>
                    <div style={{ fontSize: '12px', color: '#666', marginBottom: '4px' }}>Ingresos</div>
                    <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#4caf50' }}>
                        ${totalRevenue.toLocaleString('es-MX', { minimumFractionDigits: 2 })}
                    </div>
                </div>
                <div style={{ padding: '16px', background: '#f5f5f5', borderRadius: '8px' }}>
                    <div style={{ fontSize: '12px', color: '#666', marginBottom: '4px' }}>Costos</div>
                    <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#ff9800' }}>
                        ${totalCosts.toLocaleString('es-MX', { minimumFractionDigits: 2 })}
                    </div>
                </div>
                <div style={{ padding: '16px', background: '#f5f5f5', borderRadius: '8px' }}>
                    <div style={{ fontSize: '12px', color: '#666', marginBottom: '4px' }}>Ganancia/Pérdida</div>
                    <div style={{ fontSize: '24px', fontWeight: 'bold', color: profit >= 0 ? '#4caf50' : '#f44336' }}>
                        ${profit.toLocaleString('es-MX', { minimumFractionDigits: 2 })}
                    </div>
                </div>
            </div>
            <p style={{ color: '#666', fontSize: '14px' }}>
                El reporte incluirá desglose detallado de costos por categoría y análisis de márgenes.
            </p>
        </div>
    );
};

const KPIPreview: React.FC<{ animals: Animal[], events: Event[], dateRange: DateRange }> = ({ animals, events, dateRange }) => {
    const activeAnimals = animals.filter(a => a.status === 'active').length;
    const births = events.filter(e =>
        e.type === 'birth' &&
        new Date(e.event_date) >= new Date(dateRange.start) &&
        new Date(e.event_date) <= new Date(dateRange.end)
    ).length;
    const deaths = events.filter(e =>
        e.type === 'death' &&
        new Date(e.event_date) >= new Date(dateRange.start) &&
        new Date(e.event_date) <= new Date(dateRange.end)
    ).length;

    return (
        <div>
            <h2 style={{ fontSize: '20px', marginBottom: '20px', color: '#333' }}>Vista Previa - KPIs</h2>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '16px', marginBottom: '24px' }}>
                <div style={{ padding: '16px', background: '#f5f5f5', borderRadius: '8px' }}>
                    <div style={{ fontSize: '12px', color: '#666', marginBottom: '4px' }}>Animales Activos</div>
                    <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#2196f3' }}>{activeAnimals}</div>
                </div>
                <div style={{ padding: '16px', background: '#f5f5f5', borderRadius: '8px' }}>
                    <div style={{ fontSize: '12px', color: '#666', marginBottom: '4px' }}>Nacimientos</div>
                    <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#4caf50' }}>{births}</div>
                </div>
                <div style={{ padding: '16px', background: '#f5f5f5', borderRadius: '8px' }}>
                    <div style={{ fontSize: '12px', color: '#666', marginBottom: '4px' }}>Muertes</div>
                    <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#f44336' }}>{deaths}</div>
                </div>
            </div>
            <p style={{ color: '#666', fontSize: '14px' }}>
                El reporte incluirá métricas clave como tasas de mortalidad, natalidad, peso promedio y más.
            </p>
        </div>
    );
};

export default Reports;
