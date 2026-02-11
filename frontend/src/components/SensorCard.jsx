import React from 'react';

const SensorCard = ({ title, value, unit, colorClass = "border-blue-500" }) => {
    return (
        <div className={`p-6 bg-white rounded-2xl shadow-sm border-l-4 ${colorClass} transition-all hover:shadow-md`}>
            <h3 className="text-gray-400 text-xs font-black uppercase tracking-widest mb-2">{title}</h3>
            <div className="flex items-baseline gap-1">
                <span className="text-3xl font-black text-black tracking-tighter">
                    {value !== null && value !== undefined && value !== '--' ? value : '--'}
                </span>
                <span className="text-black text-sm font-bold">{unit}</span>
            </div>
        </div>
    );
};

export default SensorCard;
