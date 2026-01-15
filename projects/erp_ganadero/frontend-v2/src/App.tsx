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
    const [menuOpen, setMenuOpen] = useState(false);

    // Mobile-first: Bottom navigation items (max 5)
    const primaryNavItems = [
        { id: 'dashboard' as View, label: 'Inicio', icon: '🏡' },
        { id: 'animals' as View, label: 'Ganado', icon: '🐄' },
        { id: 'events' as View, label: 'Eventos', icon: '🗓️' },
        { id: 'costs' as View, label: 'Costos', icon: '💵' },
        { id: 'reports' as View, label: 'Más', icon: '⋮' }
    ];

    // Secondary items (shown in menu)
    const secondaryNavItems = [
        { id: 'inventory' as View, label: 'Inventario', icon: '🌾' },
        { id: 'clients' as View, label: 'Clientes', icon: '🤝' },
        { id: 'workers' as View, label: 'Trabajadores', icon: '🧑‍🌾' },
        { id: 'reports' as View, label: 'Reportes', icon: '📈' }
    ];

    const handleNavClick = (view: View) => {
        if (view === 'reports') {
            setMenuOpen(!menuOpen);
        } else {
            setCurrentView(view);
            setMenuOpen(false);
        }
    };

    return (
        <div className="app">
            {/* Mobile Header */}
            <header className="mobile-header">
                <h1>🐄 ERP Ganadero</h1>
                <div style={{
                    padding: '0.5rem 1rem',
                    background: 'rgba(255, 255, 255, 0.2)',
                    borderRadius: 'var(--radius-xl)',
                    fontSize: '0.875rem'
                }}>
                    Mi Rancho
                </div>
            </header>

            {/* Secondary Menu Overlay (Mobile) */}
            {menuOpen && (
                <div style={{
                    position: 'fixed',
                    bottom: 'var(--bottom-nav-height)',
                    left: 0,
                    right: 0,
                    background: 'var(--bg-card)',
                    borderTop: '1px solid var(--border)',
                    boxShadow: '0 -4px 12px rgba(0, 0, 0, 0.1)',
                    zIndex: 99,
                    padding: 'var(--spacing-md)'
                }}>
                    <div style={{ display: 'grid', gap: 'var(--spacing-sm)' }}>
                        {secondaryNavItems.map(item => (
                            <button
                                key={item.id}
                                onClick={() => {
                                    setCurrentView(item.id);
                                    setMenuOpen(false);
                                }}
                                style={{
                                    display: 'flex',
                                    alignItems: 'center',
                                    gap: 'var(--spacing-md)',
                                    padding: 'var(--spacing-md)',
                                    background: currentView === item.id ? 'var(--primary-light)' : 'transparent',
                                    border: 'none',
                                    borderRadius: 'var(--radius-md)',
                                    fontSize: '1rem',
                                    textAlign: 'left',
                                    cursor: 'pointer',
                                    minHeight: 'var(--touch-target)'
                                }}
                            >
                                <span style={{ fontSize: '1.5rem' }}>{item.icon}</span>
                                <span>{item.label}</span>
                            </button>
                        ))}
                    </div>
                </div>
            )}

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

            {/* Bottom Navigation (Mobile) */}
            <nav className="bottom-nav">
                {primaryNavItems.map(item => (
                    <button
                        key={item.id}
                        className={`bottom-nav-item ${currentView === item.id ? 'active' : ''}`}
                        onClick={() => handleNavClick(item.id)}
                        style={{
                            background: 'none',
                            border: 'none',
                            padding: 0,
                            minWidth: 'auto'
                        }}
                    >
                        <span className="bottom-nav-icon">{item.icon}</span>
                        <span>{item.label}</span>
                    </button>
                ))}
            </nav>

            {/* Toast Notifications */}
            <Toaster position="top-center" />
        </div>
    );
};

export default App;
