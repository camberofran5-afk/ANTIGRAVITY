
import React, { useState } from 'react';

interface LoginProps {
  onLogin: (user: any) => void;
}

const Login: React.FC<LoginProps> = ({ onLogin }) => {
  const [isRegister, setIsRegister] = useState(false);
  const [email, setEmail] = useState('');
  const [pin, setPin] = useState('');
  const [ranchName, setRanchName] = useState('');
  const [state, setState] = useState('Jalisco');
  const [loading, setLoading] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    
    // Simulate API call
    setTimeout(() => {
      onLogin({
        user_id: '123',
        name: 'Carlos Ranchero',
        email: email,
        ranch_id: 'r1',
        ranch_name: ranchName || 'Rancho San José',
        role: 'owner'
      });
      setLoading(false);
    }, 1500);
  };

  return (
    <div className="min-h-screen bg-[#136372] flex items-center justify-center p-6">
      <div className="bg-white w-full max-w-md rounded-3xl shadow-2xl overflow-hidden">
        <div className="bg-[#32b8c6] p-8 text-center text-white">
          <div className="bg-white/20 w-16 h-16 rounded-2xl flex items-center justify-center mx-auto mb-4">
            <i className="fa-solid fa-cow text-3xl"></i>
          </div>
          <h1 className="text-3xl font-black tracking-tight">GanadoControl</h1>
          <p className="text-white/80 mt-2 font-medium">Tu ganadería en números reales</p>
        </div>
        
        <form onSubmit={handleSubmit} className="p-8 space-y-6">
          <h2 className="text-xl font-bold text-[#134252]">
            {isRegister ? 'Crear nueva cuenta' : 'Bienvenido de nuevo'}
          </h2>

          {isRegister && (
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-bold text-gray-600 mb-2">Nombre del Rancho</label>
                <input 
                  type="text" 
                  value={ranchName}
                  onChange={(e) => setRanchName(e.target.value)}
                  placeholder="Ej. Rancho San José"
                  className="w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-[#32b8c6] outline-none transition-all"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-bold text-gray-600 mb-2">Estado</label>
                <input 
                  type="text" 
                  value={state}
                  onChange={(e) => setState(e.target.value)}
                  className="w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-[#32b8c6] outline-none"
                  required
                />
              </div>
            </div>
          )}

          <div>
            <label className="block text-sm font-bold text-gray-600 mb-2">Correo Electrónico</label>
            <input 
              type="email" 
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="tu@email.com"
              className="w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-[#32b8c6] outline-none transition-all"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-bold text-gray-600 mb-2">PIN (4 dígitos)</label>
            <input 
              type="password" 
              maxLength={4}
              value={pin}
              onChange={(e) => setPin(e.target.value)}
              placeholder="••••"
              className="w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-[#32b8c6] outline-none transition-all tracking-widest"
              required
            />
          </div>

          <button 
            type="submit"
            disabled={loading}
            className="w-full bg-[#136372] text-white py-4 rounded-xl font-bold text-lg shadow-xl shadow-[#136372]/20 hover:bg-[#134252] transition-colors flex items-center justify-center gap-3"
          >
            {loading ? (
              <div className="w-6 h-6 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
            ) : (
              isRegister ? 'CREAR CUENTA' : 'INICIAR SESIÓN'
            )}
          </button>

          <button 
            type="button"
            onClick={() => setIsRegister(!isRegister)}
            className="w-full text-[#32b8c6] font-bold text-sm hover:underline"
          >
            {isRegister ? '¿Ya tienes cuenta? Inicia sesión' : '¿Primera vez? Crea tu cuenta'}
          </button>
        </form>
      </div>
    </div>
  );
};

export default Login;
