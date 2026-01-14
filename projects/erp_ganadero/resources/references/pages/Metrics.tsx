
import React, { useState, useEffect } from 'react';
import MetricCard from '../components/MetricCard';
import { HerdMetrics } from '../types';

const Metrics: React.FC = () => {
  const [metrics, setMetrics] = useState<HerdMetrics | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setTimeout(() => {
      setMetrics({
        pregnancy_rate: 78,
        calving_interval_days: 412,
        weaning_weight_avg: 185,
        calf_mortality_percent: 4.2,
        source: 'fresh'
      });
      setLoading(false);
    }, 800);
  }, []);

  if (loading) return <div className="animate-pulse flex items-center justify-center h-64">Cargando métricas...</div>;

  return (
    <div className="max-w-7xl mx-auto">
      <div className="mb-8">
        <h2 className="text-2xl font-bold text-[#134252]">Indicadores de Producción</h2>
        <p className="text-gray-500">Análisis comparativo vs. metas de la industria</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-12">
        <MetricCard 
          label="Tasa de Preñez"
          value={`${metrics?.pregnancy_rate}%`}
          target="85%"
          status={metrics?.pregnancy_rate && metrics.pregnancy_rate < 80 ? 'warning' : 'optimal'}
          description="Porcentaje de vacas gestantes sobre el total de vacas aptas."
          subtext="Si subes a 90%: +$3,000/año de ingresos adicionales"
        />
        <MetricCard 
          label="Intervalo entre Partos"
          value={`${metrics?.calving_interval_days} días`}
          target="365 días"
          status="critical"
          description="Promedio de días transcurridos entre dos partos consecutivos."
          subtext="Rango óptimo deseado: 330-380 días"
        />
        <MetricCard 
          label="Peso al Destete"
          value={`${metrics?.weaning_weight_avg} kg`}
          target="210 kg"
          status="warning"
          description="Peso promedio de los becerros al momento del destete."
          subtext="Si aumentas +15kg = +$1,200/año de ingresos"
        />
        <MetricCard 
          label="Mortalidad de Becerros"
          value={`${metrics?.calf_mortality_percent}%`}
          target="< 3%"
          status="critical"
          description="Porcentaje de becerros muertos antes del destete."
          subtext="Problema: >5% requiere revisión de protocolos sanitarios"
        />
      </div>

      <div className="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
        <div className="bg-[#136372] p-6 text-white">
          <h3 className="text-xl font-bold flex items-center gap-2">
            <i className="fa-solid fa-lightbulb"></i>
            Oportunidades de Mejora Económica
          </h3>
          <p className="text-white/70 text-sm mt-1">Potencial de ahorro e incremento de ingresos anuales</p>
        </div>
        
        <div className="p-8 space-y-6">
          {[
            { 
              id: 1, 
              title: 'Mejorar Reproducción a 90%', 
              impact: '+$4,500 USD/año', 
              action: 'Sincronización de celos y mejora nutricional pre-empadre.',
              icon: 'fa-arrow-trend-up'
            },
            { 
              id: 2, 
              title: 'Vender 23 Vacas Improductivas', 
              impact: 'Ahorro $12,480 USD/año', 
              action: 'Reducción inmediata de costos operativos y pastoreo.',
              icon: 'fa-piggy-bank'
            },
            { 
              id: 3, 
              title: 'Optimizar Sanidad Becerros', 
              impact: '+$1,800 USD/año', 
              action: 'Vacunación estratégica para reducir mortalidad de 4.2% a 2%.',
              icon: 'fa-shield-heart'
            },
          ].map((op) => (
            <div key={op.id} className="flex items-start gap-4 p-4 rounded-xl border border-gray-100 hover:bg-[#e8f8e8]/30 transition-colors">
              <div className="w-10 h-10 rounded-lg bg-[#e8f8e8] flex items-center justify-center text-[#22c55e]">
                <i className={`fa-solid ${op.icon}`}></i>
              </div>
              <div className="flex-1">
                <div className="flex justify-between items-center mb-1">
                  <h4 className="font-bold text-[#134252]">{op.id}. {op.title}</h4>
                  <span className="text-[#22c55e] font-black">{op.impact}</span>
                </div>
                <p className="text-sm text-gray-500">{op.action}</p>
              </div>
            </div>
          ))}
          
          <div className="mt-8 pt-8 border-t border-gray-100 flex items-center justify-between">
            <div>
              <p className="text-sm font-bold text-gray-400 uppercase tracking-widest">Potencial Total Anual</p>
              <p className="text-4xl font-black text-[#136372]">+$18,780 <span className="text-xl">USD</span></p>
            </div>
            <button className="bg-[#32b8c6] text-white px-8 py-3 rounded-xl font-bold shadow-lg shadow-[#32b8c6]/20 hover:scale-105 transition-transform">
              Descargar Reporte PDF
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Metrics;
