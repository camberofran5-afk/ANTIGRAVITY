
import React, { useState } from 'react';

interface LayoutProps {
  children: React.ReactNode;
  activePage: string;
  setActivePage: (page: string) => void;
  user: any;
  onLogout: () => void;
}

const Layout: React.FC<LayoutProps> = ({ children, activePage, setActivePage, user, onLogout }) => {
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);

  const menuItems = [
    { id: 'dashboard', label: 'Dashboard', icon: 'fa-chart-pie' },
    { id: 'animals', label: 'Animales', icon: 'fa-cow' },
    { id: 'metrics', label: 'Métricas', icon: 'fa-gauge-high' },
    { id: 'costs', label: 'Costos', icon: 'fa-money-bill-wave' },
    { id: 'reports', label: 'Reportes', icon: 'fa-file-invoice' },
  ];

  return (
    <div className="flex h-screen bg-[#fcfcf9]">
      {/* Sidebar */}
      <aside className={`${isSidebarOpen ? 'w-64' : 'w-20'} bg-[#136372] text-white transition-all duration-300 flex flex-col`}>
        <div className="p-6 flex items-center gap-3 border-b border-white/10">
          <div className="bg-[#32b8c6] w-8 h-8 rounded flex items-center justify-center">
            <i className="fa-solid fa-cow text-white text-sm"></i>
          </div>
          {isSidebarOpen && <span className="font-bold text-lg tracking-tight">GanadoControl</span>}
        </div>

        <nav className="flex-1 mt-6 px-3 space-y-2">
          {menuItems.map((item) => (
            <button
              key={item.id}
              onClick={() => setActivePage(item.id)}
              className={`w-full flex items-center gap-4 px-4 py-3 rounded-lg transition-colors ${
                activePage === item.id ? 'bg-[#32b8c6] text-white' : 'hover:bg-white/10 text-white/70'
              }`}
            >
              <i className={`fa-solid ${item.icon} w-5 text-center`}></i>
              {isSidebarOpen && <span className="font-medium">{item.label}</span>}
            </button>
          ))}
        </nav>

        <div className="p-4 border-t border-white/10">
          <button 
            onClick={onLogout}
            className="w-full flex items-center gap-4 px-4 py-3 text-white/70 hover:text-white transition-colors"
          >
            <i className="fa-solid fa-right-from-bracket w-5 text-center"></i>
            {isSidebarOpen && <span className="font-medium">Cerrar Sesión</span>}
          </button>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 flex flex-col overflow-hidden">
        <header className="h-16 bg-white border-b border-gray-200 flex items-center justify-between px-8">
          <div className="flex items-center gap-4">
            <button 
              onClick={() => setIsSidebarOpen(!isSidebarOpen)}
              className="text-gray-500 hover:text-gray-700"
            >
              <i className="fa-solid fa-bars text-lg"></i>
            </button>
            <h1 className="text-xl font-semibold text-[#134252]">
              {menuItems.find(i => i.id === activePage)?.label}
            </h1>
          </div>
          <div className="flex items-center gap-4">
            <div className="text-right">
              <p className="text-sm font-semibold text-[#134252]">{user.name}</p>
              <p className="text-xs text-gray-500">{user.ranch_name}</p>
            </div>
            <div className="w-10 h-10 rounded-full bg-[#e8f4f5] flex items-center justify-center text-[#136372] font-bold">
              {user.name.charAt(0)}
            </div>
          </div>
        </header>

        <div className="flex-1 overflow-y-auto p-8">
          {children}
        </div>
      </main>
    </div>
  );
};

export default Layout;
