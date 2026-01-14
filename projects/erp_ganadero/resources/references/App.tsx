
import React, { useState } from 'react';
import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';
import Animals from './pages/Animals';
import Metrics from './pages/Metrics';
import Login from './pages/Login';

const App: React.FC = () => {
  const [user, setUser] = useState<any>(null);
  const [activePage, setActivePage] = useState('dashboard');

  const handleLogin = (userData: any) => {
    setUser(userData);
  };

  const handleLogout = () => {
    setUser(null);
    setActivePage('dashboard');
  };

  if (!user) {
    return <Login onLogin={handleLogin} />;
  }

  return (
    <Layout 
      activePage={activePage} 
      setActivePage={setActivePage} 
      user={user}
      onLogout={handleLogout}
    >
      {activePage === 'dashboard' && <Dashboard />}
      {activePage === 'animals' && <Animals />}
      {activePage === 'metrics' && <Metrics />}
      {['costs', 'reports'].includes(activePage) && (
        <div className="flex flex-col items-center justify-center h-full text-gray-400">
          <i className="fa-solid fa-hammer text-5xl mb-4"></i>
          <p className="text-xl font-bold">Módulo en Desarrollo</p>
          <p>Esta funcionalidad estará disponible pronto.</p>
        </div>
      )}
    </Layout>
  );
};

export default App;
