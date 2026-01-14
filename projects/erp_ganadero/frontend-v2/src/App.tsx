import React, { useState } from 'react';
import { Toaster } from 'react-hot-toast';
import FinancialDashboard from './components/FinancialDashboard';
import Animals from './components/Animals';
import Events from './components/Events';
import Costs from './components/Costs';
import Inventory from './components/Inventory';
import Clients from './components/Clients';
import Workers from './components/Workers';
import Reports from './components/Reports';

type View = 'dashboard' | 'animals' | 'events' | 'costs' | 'inventory' | 'clients' | 'workers' | 'reports';

const App: React.FC = () => {
    const [currentView, setCurrentView] = useState<View>('dashboard');

    const navButtonStyles = (isActive: boolean): React.CSSProperties => ({
        padding: '0.75rem 1.5rem',
        background: isActive ? 'rgba(255, 255, 255, 0.3)' : 'rgba(255, 255, 255, 0.1)',
        border: 'none',
        color: 'white',
        borderRadius: 'var(--radius-md)',
        cursor: 'pointer',
        fontSize: '1rem',
        fontWeight: 500,
        transition: 'var(--transition-normal)',
        whiteSpace: 'nowrap'
    });

    return (
        <div className="app">
            {/* Header */}
            <header style={{
                background: 'var(--primary)',
                color: 'white',
                padding: '1rem 1.5rem',
                boxShadow: 'var(--shadow-sm)'
            }}>
                <div style={{
                    maxWidth: '1200px',
                    margin: '0 auto',
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center',
                    flexWrap: 'wrap',
                    gap: '1rem'
                }}>
                    <h1 style={{ fontSize: '1.5rem', fontWeight: 600, margin: 0 }}>
                        🐄 ERP Ganadero V2
                    </h1>

                    {/* Navigation */}
                    <nav style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
                        <button
                            style={navButtonStyles(currentView === 'dashboard')}
                            onClick={() => setCurrentView('dashboard')}
                            onMouseEnter={(e) => {
                                if (currentView !== 'dashboard') {
                                    e.currentTarget.style.background = 'rgba(255, 255, 255, 0.2)';
                                }
                            }}
                            onMouseLeave={(e) => {
                                if (currentView !== 'dashboard') {
                                    e.currentTarget.style.background = 'rgba(255, 255, 255, 0.1)';
                                }
                            }}
                        >
                            🏡 Dashboard
                        </button>
                        <button
                            style={navButtonStyles(currentView === 'animals')}
                            onClick={() => setCurrentView('animals')}
                            onMouseEnter={(e) => {
                                if (currentView !== 'animals') {
                                    e.currentTarget.style.background = 'rgba(255, 255, 255, 0.2)';
                                }
                            }}
                            onMouseLeave={(e) => {
                                if (currentView !== 'animals') {
                                    e.currentTarget.style.background = 'rgba(255, 255, 255, 0.1)';
                                }
                            }}
                        >
                            🐄 Ganado
                        </button>
                        <button
                            style={navButtonStyles(currentView === 'events')}
                            onClick={() => setCurrentView('events')}
                            onMouseEnter={(e) => {
                                if (currentView !== 'events') {
                                    e.currentTarget.style.background = 'rgba(255, 255, 255, 0.2)';
                                }
                            }}
                            onMouseLeave={(e) => {
                                if (currentView !== 'events') {
                                    e.currentTarget.style.background = 'rgba(255, 255, 255, 0.1)';
                                }
                            }}
                        >
                            🗓️ Eventos
                        </button>
                        <button
                            style={navButtonStyles(currentView === 'costs')}
                            onClick={() => setCurrentView('costs')}
                            onMouseEnter={(e) => {
                                if (currentView !== 'costs') {
                                    e.currentTarget.style.background = 'rgba(255, 255, 255, 0.2)';
                                }
                            }}
                            onMouseLeave={(e) => {
                                if (currentView !== 'costs') {
                                    e.currentTarget.style.background = 'rgba(255, 255, 255, 0.1)';
                                }
                            }}
                        >
                            💵 Costos
                        </button>
                        <button
                            style={navButtonStyles(currentView === 'inventory')}
                            onClick={() => setCurrentView('inventory')}
                            onMouseEnter={(e) => {
                                if (currentView !== 'inventory') {
                                    e.currentTarget.style.background = 'rgba(255, 255, 255, 0.2)';
                                }
                            }}
                            onMouseLeave={(e) => {
                                if (currentView !== 'inventory') {
                                    e.currentTarget.style.background = 'rgba(255, 255, 255, 0.1)';
                                }
                            }}
                        >
                            🌾 Inventario
                        </button>
                        <button
                            style={navButtonStyles(currentView === 'clients')}
                            onClick={() => setCurrentView('clients')}
                            onMouseEnter={(e) => {
                                if (currentView !== 'clients') {
                                    e.currentTarget.style.background = 'rgba(255, 255, 255, 0.2)';
                                }
                            }}
                            onMouseLeave={(e) => {
                                if (currentView !== 'clients') {
                                    e.currentTarget.style.background = 'rgba(255, 255, 255, 0.1)';
                                }
                            }}
                        >
                            🤝 Clientes
                        </button>
                        <button
                            style={navButtonStyles(currentView === 'workers')}
                            onClick={() => setCurrentView('workers')}
                            onMouseEnter={(e) => {
                                if (currentView !== 'workers') {
                                    e.currentTarget.style.background = 'rgba(255, 255, 255, 0.2)';
                                }
                            }}
                            onMouseLeave={(e) => {
                                if (currentView !== 'workers') {
                                    e.currentTarget.style.background = 'rgba(255, 255, 255, 0.1)';
                                }
                            }}
                        >
                            🧑‍🌾 Trabajadores
                        </button>
                        <button
                            style={navButtonStyles(currentView === 'reports')}
                            onClick={() => setCurrentView('reports')}
                            onMouseEnter={(e) => {
                                if (currentView !== 'reports') {
                                    e.currentTarget.style.background = 'rgba(255, 255, 255, 0.2)';
                                }
                            }}
                            onMouseLeave={(e) => {
                                if (currentView !== 'reports') {
                                    e.currentTarget.style.background = 'rgba(255, 255, 255, 0.1)';
                                }
                            }}
                        >
                            📈 Reportes
                        </button>
                    </nav>

                    <div style={{
                        padding: '0.5rem 1rem',
                        background: 'rgba(255, 255, 255, 0.2)',
                        borderRadius: 'var(--radius-xl)',
                        fontSize: '0.875rem'
                    }}>
                        Mi Rancho
                    </div>
                </div>
            </header>

            {/* Main Content */}
            <main>
                {currentView === 'dashboard' && <FinancialDashboard />}
                {currentView === 'animals' && <Animals />}
                {currentView === 'events' && <Events />}
                {currentView === 'costs' && <Costs />}
                {currentView === 'inventory' && <Inventory />}
                {currentView === 'clients' && <Clients />}
                {currentView === 'workers' && <Workers />}
                {currentView === 'reports' && <Reports />}
            </main>

            {/* Toast Notifications */}
            <Toaster />
        </div>
    );
};

export default App;
