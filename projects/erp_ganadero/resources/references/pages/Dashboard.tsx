
import React, { useState, useEffect } from 'react';
import DashboardCard from '../components/DashboardCard';
import AlertBanner from '../components/AlertBanner';
import { HerdSummary } from '../types';

const Dashboard: React.FC = () => {
  const [summary, setSummary] = useState<HerdSummary | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Simulate API fetch
    setTimeout(() => {
      setSummary({
        totalAnimals: 154,
        unproductiveCount: 23,
        readyToWeanCount: 12,
        weekCostUsd: 1450.50
      });
      setLoading(false);
    }, 800);
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-[#136372]"></div>
      </div>
    );
  }

  const unproductiveCostWeekly = (summary?.unproductiveCount || 0) * 15.42;
  const unproductiveCostMonthly = unproductiveCostWeekly * 4.33;
  const unproductiveCostAnnual = (summary?.unproductiveCount || 0) * 801.84;

  return (
    <div className="max-w-7xl mx-auto">
      <div className="flex justify-between items-end mb-8">
        <div>
          <h2 className="text-2xl font-bold text-[#134252]">Tu Hato Hoy</h2>
          <p className="text-gray-500">Resumen de producción al {new Date().toLocaleDateString()}</p>
        </div>
        <div className="flex gap-3">
          <button className="bg-[#32b8c6] text-white px-4 py-2 rounded-lg font-semibold shadow-sm hover:opacity-90 transition-opacity">
            <i className="fa-solid fa-plus mr-2"></i>Nuevo Animal
          </button>
          <button className="bg-white border border-gray-200 text-[#134252] px-4 py-2 rounded-lg font-semibold shadow-sm hover:bg-gray-50 transition-colors">
            <i className="fa-solid fa-calendar-check mr-2"></i>Evento
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <DashboardCard 
          title="Total de Animales"
          value={summary?.totalAnimals || 0}
          subtitle="Activos en el rancho"
          detail="7% más que el mes pasado"
          icon="fa-cow"
          backgroundColor="#e8f4f5"
        />
        <DashboardCard 
          title="Productivas"
          value={(summary?.totalAnimals || 0) - (summary?.unproductiveCount || 0)}
          subtitle="Preñadas o en lactancia"
          detail="Tasa de preñez: 82%"
          icon="fa-heart-pulse"
          backgroundColor="#e8f8e8"
        />
        <DashboardCard 
          title="Próximos a Destetar"
          value={summary?.readyToWeanCount || 0}
          subtitle="Listos en 2-4 semanas"
          detail={`Est. valor: $${((summary?.readyToWeanCount || 0) * 550).toLocaleString()}`}
          icon="fa-seedling"
          backgroundColor="#fff4e6"
        />
      </div>

      <AlertBanner 
        title="IMPRODUCTIVAS: ALERTA DE COSTO"
        count={summary?.unproductiveCount || 0}
        costWeekly={unproductiveCostWeekly}
        costMonthly={unproductiveCostMonthly}
        costAnnual={unproductiveCostAnnual}
        color="red"
      />

      <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6 mt-8">
        <h3 className="text-lg font-bold text-[#134252] mb-6">Acciones Rápidas</h3>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          {[
            { label: 'Palpar Vacas', icon: 'fa-hand-dots', color: 'text-blue-500', bg: 'bg-blue-50' },
            { label: 'Venta Lote', icon: 'fa-truck-ramp-box', color: 'text-green-500', bg: 'bg-green-50' },
            { label: 'Sanidad', icon: 'fa-kit-medical', color: 'text-red-500', bg: 'bg-red-50' },
            { label: 'Registrar Peso', icon: 'fa-weight-scale', color: 'text-purple-500', bg: 'bg-purple-50' },
          ].map((action, idx) => (
            <button key={idx} className={`${action.bg} p-4 rounded-xl flex flex-col items-center gap-3 transition-transform hover:scale-105`}>
              <i className={`fa-solid ${action.icon} ${action.color} text-2xl`}></i>
              <span className="font-semibold text-gray-700 text-sm">{action.label}</span>
            </button>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
