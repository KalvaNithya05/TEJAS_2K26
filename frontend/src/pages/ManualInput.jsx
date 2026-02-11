import React, { useState } from 'react';
import { getRecommendations, getLatestSensorData } from '../services/api';
import RecommendationCard from '../components/RecommendationCard';

const IND_STATES = [
    "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh", "Goa", "Gujarat", "Haryana",
    "Himachal Pradesh", "Jharkhand", "Karnataka", "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur",
    "Meghalaya", "Mizoram", "Nagaland", "Odisha", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu",
    "Telangana", "Tripura", "Uttar Pradesh", "Uttarakhand", "West Bengal"
];

const SEASONS = ["Kharif", "Rabi", "Zaid"];

const ManualInput = ({ lang, t }) => {
    const [formData, setFormData] = useState({
        N: 50, P: 40, K: 30, ph: 6.5, temperature: 25, humidity: 60, rainfall: 100, state: '', season: '', crop_type: ''
    });
    const [loading, setLoading] = useState(false);
    const [fetchingWeather, setFetchingWeather] = useState(false);
    const [result, setResult] = useState(null);

    React.useEffect(() => {
        refreshWeather();
    }, []);

    const refreshWeather = async () => {
        setFetchingWeather(true);
        try {
            const data = await getLatestSensorData();
            if (data) {
                setFormData(prev => ({
                    ...prev,
                    temperature: data.temperature || prev.temperature,
                    humidity: data.humidity || prev.humidity,
                    rainfall: data.rainfall || prev.rainfall
                }));
            }
        } catch (e) {
            console.error("Failed to fetch weather", e);
        } finally {
            setFetchingWeather(false);
        }
    };

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        try {
            const recs = await getRecommendations({ ...formData, lang });
            if (recs && recs.status === 'success') {
                setResult(recs);
            }
        } catch (e) {
            alert("Error: " + e.message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="p-6 max-w-4xl mx-auto">
            <h1 className="text-3xl font-black mb-6 text-gray-900 tracking-tight">{t('manual_input')}</h1>

            {!result ? (
                <div className="bg-white p-8 rounded-3xl shadow-xl border border-gray-100">
                    <form onSubmit={handleSubmit} className="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div>
                            <label className="block text-sm font-bold text-gray-500 uppercase tracking-wider mb-1">{t('nitrogen')}</label>
                            <input type="number" name="N" value={formData.N} onChange={handleChange} className="mt-1 block w-full p-3 bg-gray-50 border-none rounded-xl focus:ring-2 focus:ring-green-500 font-bold" required />
                        </div>
                        <div>
                            <label className="block text-sm font-bold text-gray-500 uppercase tracking-wider mb-1">{t('phosphorus')}</label>
                            <input type="number" name="P" value={formData.P} onChange={handleChange} className="mt-1 block w-full p-3 bg-gray-50 border-none rounded-xl focus:ring-2 focus:ring-green-500 font-bold" required />
                        </div>
                        <div>
                            <label className="block text-sm font-bold text-gray-500 uppercase tracking-wider mb-1">{t('potassium')}</label>
                            <input type="number" name="K" value={formData.K} onChange={handleChange} className="mt-1 block w-full p-3 bg-gray-50 border-none rounded-xl focus:ring-2 focus:ring-green-500 font-bold" required />
                        </div>
                        <div>
                            <label className="block text-sm font-bold text-gray-500 uppercase tracking-wider mb-1">{t('ph')}</label>
                            <input type="number" step="0.1" name="ph" value={formData.ph} onChange={handleChange} className="mt-1 block w-full p-3 bg-gray-50 border-none rounded-xl focus:ring-2 focus:ring-green-500 font-bold" required />
                        </div>
                        <div className="md:col-span-2 grid grid-cols-1 md:grid-cols-3 gap-6 bg-blue-50 p-6 rounded-2xl border border-blue-100">
                            <div className="relative">
                                <label className="block text-sm font-bold text-blue-800 uppercase tracking-wider mb-1">{t('temp')}</label>
                                <input type="number" name="temperature" value={formData.temperature} onChange={handleChange} className="mt-1 block w-full p-3 bg-white border-none rounded-xl focus:ring-2 focus:ring-blue-500 font-bold" required />
                            </div>
                            <div className="relative">
                                <label className="block text-sm font-bold text-blue-800 uppercase tracking-wider mb-1">{t('humidity')}</label>
                                <input type="number" name="humidity" value={formData.humidity} onChange={handleChange} className="mt-1 block w-full p-3 bg-white border-none rounded-xl focus:ring-2 focus:ring-blue-500 font-bold" required />
                            </div>
                            <div className="relative">
                                <label className="block text-sm font-bold text-blue-800 uppercase tracking-wider mb-1 flex justify-between">
                                    {t('rainfall')}
                                    <button type="button" onClick={refreshWeather} className="text-blue-600 hover:text-blue-800 text-[10px] font-black flex items-center bg-white px-2 py-0.5 rounded-full shadow-sm">
                                        {fetchingWeather ? '...' : '🔄 REFRESH'}
                                    </button>
                                </label>
                                <input type="number" name="rainfall" value={formData.rainfall} onChange={handleChange} className="mt-1 block w-full p-3 bg-white border-none rounded-xl focus:ring-2 focus:ring-blue-500 font-bold" required />
                            </div>
                        </div>
                        <div>
                            <label className="block text-sm font-bold text-gray-500 uppercase tracking-wider mb-1">{t('season')} *</label>
                            <select name="season" value={formData.season} onChange={handleChange} className="mt-1 block w-full p-3 bg-gray-50 border-none rounded-xl focus:ring-2 focus:ring-green-500 font-bold" required>
                                <option value="">Select Season</option>
                                {SEASONS.map(s => <option key={s} value={s}>{s}</option>)}
                            </select>
                        </div>
                        <div>
                            <label className="block text-sm font-bold text-gray-500 uppercase tracking-wider mb-1">{t('state')} *</label>
                            <select name="state" value={formData.state} onChange={handleChange} className="mt-1 block w-full p-3 bg-gray-50 border-none rounded-xl focus:ring-2 focus:ring-green-500 font-bold" required>
                                <option value="">Select State</option>
                                {IND_STATES.map(s => <option key={s} value={s}>{s}</option>)}
                            </select>
                        </div>

                        <div>
                            <label className="block text-sm font-bold text-gray-500 uppercase tracking-wider mb-1">{t('crop_category')}</label>
                            <select name="crop_type" value={formData.crop_type} onChange={handleChange} className="mt-1 block w-full p-3 bg-gray-50 border-none rounded-xl focus:ring-2 focus:ring-green-500 font-bold">
                                <option value="">All Crops</option>
                                <option value="agriculture">Agriculture</option>
                                <option value="horticulture">Horticulture</option>
                            </select>
                        </div>

                        <div className="md:col-span-2 pt-4">
                            <button type="submit" disabled={loading} className="w-full bg-gradient-to-r from-green-600 to-emerald-600 text-white p-4 rounded-2xl font-black text-xl shadow-lg hover:shadow-green-200 transition-all active:scale-[0.98]">
                                {loading ? t('analyzing') : t('get_recom')}
                            </button>
                        </div>
                    </form>
                </div>
            ) : (
                <div className="animate-fade-in-up space-y-6">
                    <div className="flex justify-between items-center">
                        <button onClick={() => setResult(null)} className="flex items-center text-blue-600 font-black hover:underline px-4 py-2 bg-blue-50 rounded-full text-sm">
                            <span className="mr-1">←</span> {t('back')}
                        </button>
                        <span className="text-sm font-bold text-gray-400 uppercase tracking-widest">
                            {result.recommendations?.length || 0} {t('results')}
                        </span>
                    </div>

                    <div className="space-y-8 pb-12">
                        {result.recommendations?.map((rec, idx) => (
                            <RecommendationCard key={idx} recommendation={rec} index={idx} t={t} isManual={true} />
                        ))}
                    </div>

                    <div className="flex justify-center pt-8">
                        <button
                            onClick={async () => {
                                try {
                                    const bodyData = { ...result, lang };
                                    const response = await fetch('http://localhost:5000/api/report/download-pdf', {
                                        method: 'POST',
                                        headers: { 'Content-Type': 'application/json' },
                                        body: JSON.stringify(bodyData)
                                    });
                                    if (!response.ok) throw new Error('Failed to generate PDF');
                                    const blob = await response.blob();
                                    const url = window.URL.createObjectURL(blob);
                                    const a = document.createElement('a');
                                    a.href = url;
                                    a.download = `mitti-mitra-report-${new Date().toISOString().split('T')[0]}.pdf`;
                                    document.body.appendChild(a);
                                    a.click();
                                    window.URL.revokeObjectURL(url);
                                    document.body.removeChild(a);
                                } catch (e) {
                                    alert(`PDF Download Error: ${e.message}`);
                                }
                            }}
                            className="flex items-center gap-2 px-8 py-4 bg-gray-900 text-white rounded-2xl shadow-xl hover:bg-black transition-all font-black text-lg"
                        >
                            <span>Download Full PDF Report</span>
                        </button>
                    </div>
                </div>
            )}
        </div>
    );
};

export default ManualInput;
