import React, { useEffect, useState } from 'react';
import SensorCard from '../components/SensorCard';
import { getLatestSensorData, getSensorHistory, getAggregateData } from '../services/api';
import { supabase } from '../config/supabase';

const Dashboard = ({ lang = 'en', t }) => {
    const [data, setData] = useState(null);
    const [latest, setLatest] = useState(null);
    const [history, setHistory] = useState([]);
    const [loading, setLoading] = useState(true);
    const [isOnline, setIsOnline] = useState(false);

    const fetchData = async () => {
        const aggResult = await getAggregateData();
        const latestResult = await getLatestSensorData();
        const histResult = await getSensorHistory();

        if (aggResult) setData(aggResult);
        if (latestResult) {
            setLatest(latestResult);
            // Check if data is fresh (last 5 mins)
            const lastSeen = new Date(latestResult.timestamp);
            const now = new Date();
            const diffMins = (now - lastSeen) / 60000;
            setIsOnline(diffMins < 5);
        } else {
            setIsOnline(false);
        }

        if (histResult) setHistory(histResult);
        setLoading(false);
    };

    useEffect(() => {
        fetchData();

        const channel = supabase
            .channel('soil_updates')
            .on(
                'postgres_changes',
                { event: 'INSERT', schema: 'public', table: 'sensor_readings' },
                (payload) => {
                    const row = payload.new;
                    const mappedData = {
                        ...row,
                        nitrogen: row.nitrogen ?? row.N,
                        phosphorus: row.phosphorus ?? row.P,
                        potassium: row.potassium ?? row.K,
                        ph: row.soil_ph ?? row.ph ?? row.pH,
                        timestamp: row.created_at || row.timestamp
                    };
                    setLatest(mappedData);
                    setIsOnline(true);
                    setHistory(prev => [mappedData, ...prev.slice(0, 29)]);

                    // Trigger a re-fetch of aggregates for the main cards
                    fetchData();
                }
            )
            .subscribe();

        return () => {
            supabase.removeChannel(channel);
        };
    }, []);

    if (loading) return <div className="flex items-center justify-center min-h-[60vh] text-gray-400 font-bold uppercase tracking-widest">{t('analyzing')}...</div>;

    return (
        <div className="p-6 md:p-8 animate-fade-in max-w-7xl mx-auto">
            <header className="mb-12 relative">
                <div className="flex flex-col md:flex-row justify-between items-start md:items-end gap-6">
                    <div>
                        <h1 className="text-5xl font-black text-black tracking-tight mb-2">{t('sensor_status')}</h1>
                        <p className="text-black font-bold text-lg">{t('sensor_subtitle')}</p>
                    </div>
                    <div className="text-right hidden md:block">
                        <p className="text-[10px] font-black text-black uppercase tracking-widest mb-1">Last Updated</p>
                        <p className="font-mono text-black font-bold text-xl">
                            {latest?.timestamp ? new Date(latest.timestamp).toLocaleTimeString() : '--:--:--'}
                        </p>
                    </div>
                </div>

                <div className="mt-8 flex justify-center">
                    <div className={`px-6 py-2 rounded-full flex items-center gap-3 shadow-lg border-2 transition-all ${isOnline ? 'bg-green-50 border-green-200 text-green-600' : 'bg-red-50 border-red-200 text-red-600'}`}>
                        <span className={`w-3 h-3 rounded-full ${isOnline ? 'bg-green-500 animate-pulse' : 'bg-red-500'}`}></span>
                        <span className="text-sm font-black uppercase tracking-widest">
                            {isOnline ? 'Device Online' : 'Device Offline'}
                        </span>
                    </div>
                </div>
            </header>

            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-16">
                <SensorCard title={t('temp')} value={data?.temperature} unit="°C" colorClass="border-red-500" />
                <SensorCard title={t('humidity')} value={data?.humidity} unit="%" colorClass="border-blue-400" />
                <SensorCard title={t('ph')} value={data?.ph} unit="pH" colorClass="border-purple-400" />
                <SensorCard title={t('moisture')} value={data?.moisture} unit="%" colorClass="border-cyan-400" />

                <SensorCard title={t('nitrogen')} value={data?.N} unit="mg/kg" colorClass="border-green-500" />
                <SensorCard title={t('phosphorus')} value={data?.P} unit="mg/kg" colorClass="border-orange-400" />
                <SensorCard title={t('potassium')} value={data?.K} unit="mg/kg" colorClass="border-yellow-400" />
                <SensorCard title={t('rainfall')} value={data?.rainfall} unit="mm" colorClass="border-indigo-400" />
            </div>

            <div className="bg-white p-8 rounded-[2rem] border border-gray-100 shadow-sm transition-all hover:shadow-md">
                <h2 className="text-2xl font-black text-black mb-8 flex items-center gap-3">
                    {t('recent_recordings')}(Last {history.length})
                </h2>
                <div className="overflow-x-auto">
                    <table className="w-full text-left">
                        <thead>
                            <tr className="text-sm font-black text-black uppercase tracking-widest border-b border-gray-100 pb-4">
                                <th className="px-6 py-4">Time</th>
                                <th className="px-6 py-4">Temp</th>
                                <th className="px-6 py-4">Humidity</th>
                                <th className="px-6 py-4">N</th>
                                <th className="px-6 py-4">P</th>
                                <th className="px-6 py-4">K</th>
                                <th className="px-6 py-4">pH</th>
                                <th className="px-6 py-4">Moisture</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-gray-50">
                            {history.map((row, i) => (
                                <tr key={i} className="group hover:bg-green-50/40 transition-all">
                                    <td className="px-6 py-4 font-mono text-xs text-black">
                                        {row.timestamp ? new Date(row.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' }) : '--'}
                                    </td>
                                    <td className="px-6 py-4 font-bold text-black">{row.temperature}</td>
                                    <td className="px-6 py-4 font-bold text-black">{row.humidity}</td>
                                    <td className="px-6 py-4 font-bold text-black">{row.nitrogen}</td>
                                    <td className="px-6 py-4 font-bold text-black">{row.phosphorus}</td>
                                    <td className="px-6 py-4 font-bold text-black">{row.potassium}</td>
                                    <td className="px-6 py-4 font-bold text-black">{row.ph}</td>
                                    <td className="px-6 py-4 font-bold text-black">{row.moisture}</td>
                                </tr>
                            ))}
                            {history.length === 0 && (
                                <tr>
                                    <td colSpan="8" className="px-6 py-12 text-center text-gray-400 font-bold">No historical data found.</td>
                                </tr>
                            )}
                        </tbody>
                    </table>
                </div>
            </div>

            <footer className="mt-16 text-center">
                <p className="text-black font-bold text-xs uppercase tracking-widest">
                    Device ID: {latest?.device_id || 'MM-POLE-001'} | Last Update: {latest?.timestamp ? new Date(latest.timestamp).toLocaleTimeString() : '--'}
                </p>
            </footer>
        </div>
    );
};

export default Dashboard;
