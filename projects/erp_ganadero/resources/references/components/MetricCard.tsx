
import React from 'react';
import { MetricStatus } from '../types';

interface MetricCardProps {
  label: string;
  value: string;
  target: string;
  status?: MetricStatus;
  description: string;
  subtext?: string;
}

const MetricCard: React.FC<MetricCardProps> = ({ 
  label, value, target, status = 'optimal', description, subtext 
}) => {
  const statusConfig = {
    optimal: { bg: 'bg-[#e8f8e8]', border: 'border-[#22c55e]', text: 'text-[#22c55e]', icon: 'fa-circle-check' },
    warning: { bg: 'bg-[#fff4e6]', border: 'border-[#f59e0b]', text: 'text-[#f59e0b]', icon: 'fa-circle-exclamation' },
    critical: { bg: 'bg-[#ffe0e0]', border: 'border-[#ff5459]', text: 'text-[#ff5459]', icon: 'fa-circle-xmark' },
  };

  const config = statusConfig[status];

  return (
    <div className={`p-6 rounded-xl border-l-4 ${config.border} ${config.bg} shadow-sm transition-transform hover:scale-[1.01]`}>
      <div className="flex justify-between items-start mb-4">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <i className={`fa-solid ${config.icon} ${config.text}`}></i>
            <h4 className="text-xs font-bold text-gray-500 uppercase tracking-widest">{label}</h4>
          </div>
          <p className="text-2xl font-black text-[#134252]">{value}</p>
        </div>
        <div className="bg-white/50 px-3 py-1 rounded-full border border-white/20">
          <span className="text-[10px] font-bold text-gray-500">META: {target}</span>
        </div>
      </div>
      
      <p className="text-sm text-gray-700 mb-2">{description}</p>
      {subtext && (
        <p className={`text-xs font-semibold ${config.text} bg-white/40 inline-block px-2 py-1 rounded`}>
          {subtext}
        </p>
      )}
    </div>
  );
};

export default MetricCard;
