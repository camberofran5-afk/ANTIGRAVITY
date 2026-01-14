
import React from 'react';

interface AlertBannerProps {
  title: string;
  count: number;
  costWeekly: number;
  costMonthly: number;
  costAnnual: number;
  color: 'red' | 'yellow';
}

const AlertBanner: React.FC<AlertBannerProps> = ({ 
  title, count, costWeekly, costMonthly, costAnnual, color 
}) => {
  const isRed = color === 'red';
  const bgColor = isRed ? 'bg-[#fff5f5]' : 'bg-[#fffcf0]';
  const borderColor = isRed ? 'border-[#ff5459]' : 'border-[#f59e0b]';
  const textColor = isRed ? 'text-[#ff5459]' : 'text-[#f59e0b]';

  return (
    <div className={`${bgColor} border-l-4 ${borderColor} p-6 rounded-lg mb-6 shadow-sm`}>
      <div className="flex items-center gap-3 mb-4">
        <i className={`fa-solid fa-triangle-exclamation ${textColor} text-xl`}></i>
        <h3 className={`font-bold ${textColor} text-lg`}>{title}</h3>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <p className="text-4xl font-black text-gray-800">{count}</p>
          <p className="text-sm text-gray-500 uppercase font-semibold tracking-wider">Animales afectados</p>
        </div>
        
        <div className="space-y-2 border-t md:border-t-0 md:border-l border-gray-200 pt-4 md:pt-0 md:pl-6">
          <div className="flex justify-between items-center text-sm">
            <span className="text-gray-600">Costo semanal:</span>
            <span className="font-bold text-gray-800">${costWeekly.toFixed(2)}</span>
          </div>
          <div className="flex justify-between items-center text-sm">
            <span className="text-gray-600">Costo mensual:</span>
            <span className="font-bold text-gray-800">${costMonthly.toFixed(2)}</span>
          </div>
          <div className="flex justify-between items-center text-sm border-t border-gray-100 pt-2">
            <span className="text-gray-600 font-semibold">Costo anual proyectado:</span>
            <span className={`font-black ${textColor} text-base`}>${costAnnual.toFixed(2)}</span>
          </div>
        </div>
      </div>
      
      <div className="mt-6 flex gap-3">
        <button className={`px-4 py-2 rounded-lg text-white font-semibold transition-opacity hover:opacity-90 ${isRed ? 'bg-[#ff5459]' : 'bg-[#f59e0b]'}`}>
          Ver Listado
        </button>
        <button className="px-4 py-2 rounded-lg bg-white border border-gray-200 text-gray-700 font-semibold hover:bg-gray-50 transition-colors">
          Tomar Acción
        </button>
      </div>
    </div>
  );
};

export default AlertBanner;
