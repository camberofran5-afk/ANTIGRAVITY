
import React from 'react';

interface DashboardCardProps {
  title: string;
  value: string | number;
  subtitle?: string;
  detail?: string;
  icon: string;
  backgroundColor: string;
}

const DashboardCard: React.FC<DashboardCardProps> = ({ 
  title, value, subtitle, detail, icon, backgroundColor 
}) => {
  return (
    <div 
      className="p-6 rounded-xl shadow-sm border border-gray-100 flex flex-col justify-between"
      style={{ backgroundColor }}
    >
      <div className="flex justify-between items-start mb-4">
        <div>
          <h3 className="text-sm font-medium text-gray-600 mb-1">{title}</h3>
          <p className="text-3xl font-bold text-[#134252]">{value}</p>
        </div>
        <div className="text-2xl text-[#136372]/50">
          <i className={`fa-solid ${icon}`}></i>
        </div>
      </div>
      <div>
        {subtitle && <p className="text-sm text-gray-500">{subtitle}</p>}
        {detail && <p className="text-xs font-semibold text-[#32b8c6] mt-1">{detail}</p>}
      </div>
    </div>
  );
};

export default DashboardCard;
