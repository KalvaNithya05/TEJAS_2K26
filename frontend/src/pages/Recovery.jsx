import React, { useState, useEffect } from 'react';
import { getAggregateData, getRecoveryPrediction } from '../services/api';

const Recovery = ({ lang = 'en', t }) => {
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState(null);
    const [error, setError] = useState(null);
    const [formData, setFormData] = useState({
        crop_name: '',
        season_started: '',
        damage_type: 'Pest Attack',
        damage_percentage: 20,
        growth_stage: 30
    });

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: name === 'damage_percentage' || name === 'growth_stage' ? Number(value) : value
        }));
    };

    const handleGetRecoveryPlan = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError(null);
        setResult(null);
        try {
            const sensorData = await getAggregateData();
            if (!sensorData) throw new Error("Could not fetch aggregated sensor data.");

            // Standardize NPK keys if they differ between aggregate and latest
            const nitrogen = sensorData.nitrogen || sensorData.N || 0;
            const phosphorus = sensorData.phosphorus || sensorData.P || 0;
            const potassium = sensorData.potassium || sensorData.K || 0;

            // The backend expect days_remaining, but user inputs growth_stage (days).
            // Let's assume a typical crop duration of 120 days for fallback if not specified.
            const days_remaining = 120 - formData.growth_stage;

            const payload = {
                ...sensorData,
                N: nitrogen,
                P: phosphorus,
                K: potassium,
                damage_type: formData.damage_type,
                damage_percentage: formData.damage_percentage,
                days_remaining: days_remaining,
                growth_stage: formData.growth_stage,
                crop_grown: formData.crop_name,
                season: formData.season_started,
                lang: lang
            };

            const data = await getRecoveryPrediction(payload);
            if (data && !data.error) {
                setResult(data);
            } else {
                throw new Error(data?.error || "Failed to get recovery plan.");
            }
        } catch (err) {
            console.error("Recovery Error:", err);
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="p-6 max-w-6xl mx-auto">
            <div className="text-center mb-10">
                <h1 className="text-5xl font-black text-green-900 mb-2 tracking-tight">
                    {t('recovery_hub')}
                </h1>
                <p className="text-lg text-gray-500 font-medium">
                    {t('recovery_subtitle')}
                </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-12">
                {/* Input Form */}
                <div className="bg-white p-8 rounded-3xl shadow-xl border border-gray-100">
                    <form onSubmit={handleGetRecoveryPlan} className="space-y-6">
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                            <div>
                                <label className="block text-gray-500 font-bold mb-2 uppercase tracking-widest text-xs">
                                    {t('crop_name')}
                                </label>
                                <input
                                    type="text"
                                    name="crop_name"
                                    value={formData.crop_name}
                                    onChange={handleInputChange}
                                    className="w-full p-4 bg-gray-50 border-0 rounded-2xl focus:ring-2 focus:ring-green-500 font-bold"
                                    placeholder="e.g. Rice, Wheat"
                                    required
                                />
                            </div>
                            <div>
                                <label className="block text-gray-500 font-bold mb-2 uppercase tracking-widest text-xs">
                                    {t('season_started')}
                                </label>
                                <select
                                    name="season_started"
                                    value={formData.season_started}
                                    onChange={handleInputChange}
                                    className="w-full p-4 bg-gray-50 border-0 rounded-2xl focus:ring-2 focus:ring-green-500 font-bold"
                                    required
                                >
                                    <option value="">Select Season</option>
                                    <option value="Kharif">Kharif</option>
                                    <option value="Rabi">Rabi</option>
                                    <option value="Zaid">Zaid</option>
                                </select>
                            </div>
                        </div>

                        <div>
                            <label className="block text-gray-500 font-bold mb-2 uppercase tracking-widest text-xs">
                                {t('damage_type')}
                            </label>
                            <select
                                name="damage_type"
                                value={formData.damage_type}
                                onChange={handleInputChange}
                                className="w-full p-4 bg-gray-50 border-0 rounded-2xl focus:ring-2 focus:ring-green-500 font-bold"
                            >
                                <option value="Pest Attack">Pest Attack</option>
                                <option value="Nutrient Deficiency">Nutrient Deficiency</option>
                                <option value="Waterlogging">Waterlogging</option>
                                <option value="Drought">Drought</option>
                                <option value="Fungal Infection">Fungal Infection</option>
                            </select>
                        </div>

                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                            <div>
                                <label className="block text-gray-500 font-bold mb-2 uppercase tracking-widest text-xs">
                                    {t('damage_percentage')} ({formData.damage_percentage}%)
                                </label>
                                <input
                                    type="range"
                                    name="damage_percentage"
                                    min="0"
                                    max="100"
                                    value={formData.damage_percentage}
                                    onChange={handleInputChange}
                                    className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-green-600"
                                />
                            </div>
                            <div>
                                <label className="block text-gray-500 font-bold mb-2 uppercase tracking-widest text-xs">
                                    {t('growth_stage')} ({formData.growth_stage} days)
                                </label>
                                <input
                                    type="number"
                                    name="growth_stage"
                                    value={formData.growth_stage}
                                    onChange={handleInputChange}
                                    className="w-full p-4 bg-gray-50 border-0 rounded-2xl focus:ring-2 focus:ring-green-500 font-bold"
                                    min="1"
                                    max="365"
                                    required
                                />
                            </div>
                        </div>

                        <button
                            type="submit"
                            disabled={loading}
                            className={`w-full py-5 rounded-2xl font-black text-xl shadow-2xl transition-all active:scale-95 ${loading ? 'bg-gray-200 text-gray-400 cursor-not-allowed' : 'bg-gradient-to-r from-green-600 to-emerald-600 text-white hover:shadow-green-100'}`}
                        >
                            {loading ? t('analyzing') : t('get_recovery_plan')}
                        </button>
                    </form>
                </div>

                {/* Results Section */}
                <div className="space-y-6">
                    {error && (
                        <div className="p-6 bg-red-50 border-l-8 border-red-500 text-red-700 rounded-2xl shadow-lg font-bold">
                            {error}
                        </div>
                    )}

                    {!result && !loading && !error && (
                        <div className="h-full flex flex-col items-center justify-center text-center p-12 bg-gray-50 rounded-3xl border-2 border-dashed border-gray-200">
                            <div className="text-6xl mb-4">🩹</div>
                            <h3 className="text-xl font-bold text-gray-400">Enter details to generate recovery plan</h3>
                        </div>
                    )}

                    {loading && (
                        <div className="h-full flex flex-col items-center justify-center text-center p-12 bg-white rounded-3xl shadow-xl border border-gray-100">
                            <div className="animate-spin rounded-full h-16 w-16 border-t-4 border-b-4 border-green-500 mb-4"></div>
                            <h3 className="text-xl font-bold text-green-700 animate-pulse">Running AI Analysis...</h3>
                        </div>
                    )}

                    {result && (
                        <div className="space-y-6 animate-fade-in-up">
                            {/* Decision Card */}
                            <div className="bg-gradient-to-br from-green-600 to-emerald-700 p-8 rounded-3xl shadow-2xl text-white relative overflow-hidden">
                                <div className="absolute top-0 right-0 p-4 opacity-10 text-8xl">🌱</div>
                                <h3 className="text-xs font-black uppercase tracking-widest mb-2 opacity-80">{t('recommendation')}</h3>
                                <h2 className="text-3xl font-black mb-4">
                                    {(result.decision || 'PLAN_NOT_AVAILABLE').replace(/_/g, ' ')}
                                </h2>
                                <div className="flex items-center gap-4 bg-white/20 p-4 rounded-2xl backdrop-blur-sm">
                                    <div className="text-center">
                                        <div className="text-2xl font-black">{((result.confidence || 0) * 100).toFixed(0)}%</div>
                                        <div className="text-[10px] font-bold uppercase opacity-70">{t('confidence')}</div>
                                    </div>
                                    <div className="h-10 w-[1px] bg-white/30"></div>
                                    <p className="text-sm font-medium leading-relaxed">
                                        {result.reason}
                                    </p>
                                </div>
                            </div>

                            {/* LLM Explanation */}
                            {result.llm_explanation && (
                                <div className="bg-white p-8 rounded-3xl shadow-xl border border-blue-50 relative">
                                    <div className="absolute -top-3 -left-3 bg-blue-600 text-white p-2 rounded-xl text-xs font-black shadow-lg">AI ADVISOR</div>
                                    <div className="prose prose-green max-w-none text-gray-700">
                                        {(result.llm_explanation || '').split('\n').map((line, i) => (
                                            <p key={i} className="mb-2 leading-relaxed">
                                                {line.includes('**') ?
                                                    line.split('**').map((part, j) => j % 2 === 1 ? <strong key={j} className="text-green-800">{part}</strong> : part)
                                                    : line
                                                }
                                            </p>
                                        ))}
                                    </div>
                                </div>
                            )}

                            {/* Eco Advisory */}
                            {result.eco_advisory && result.eco_advisory.length > 0 && (
                                <div className="bg-emerald-50 p-8 rounded-3xl border border-emerald-100">
                                    <h3 className="text-green-800 font-black uppercase tracking-widest text-xs mb-4 flex items-center">
                                        <span className="mr-2">🍃</span> Eco-Friendly Solutions
                                    </h3>
                                    <div className="grid grid-cols-1 gap-4">
                                        {result.eco_advisory.map((adv, i) => (
                                            <div key={i} className="bg-white p-4 rounded-2xl shadow-sm border border-emerald-100">
                                                <div className="font-black text-emerald-800 text-sm mb-1">{(adv.issue || adv.condition || 'Condition')} Detected</div>
                                                <div className="text-gray-600 text-sm font-medium leading-relaxed">{adv.solution}</div>
                                            </div>
                                        ))}
                                    </div>
                                </div>
                            )}

                            {/* Government Schemes */}
                            {result.schemes && result.schemes.length > 0 && (
                                <div className="bg-orange-50 p-8 rounded-3xl border border-orange-100">
                                    <h3 className="text-orange-800 font-black uppercase tracking-widest text-xs mb-4 flex items-center">
                                        <span className="mr-2">🏛️</span> Eligible Gov. Support
                                    </h3>
                                    <div className="space-y-4">
                                        {result.schemes.map((scheme, i) => (
                                            <div key={i} className="bg-white p-5 rounded-2xl shadow-sm border border-orange-100 border-l-8 border-l-orange-500">
                                                <div className="font-black text-orange-950 text-base mb-1">{scheme.scheme_name}</div>
                                                <div className="text-gray-600 text-sm mb-3 mt-1 font-medium">{scheme.description || 'Government support scheme for farmers.'}</div>
                                                <div className="flex items-center justify-between gap-2 mt-4 pt-4 border-t border-orange-100">
                                                    <div className="flex flex-wrap gap-2">
                                                        {Array.isArray(scheme.benefits) ?
                                                            scheme.benefits.map((benefit, j) => (
                                                                <span key={j} className="text-[10px] font-black bg-orange-100 text-orange-700 px-3 py-1 rounded-full uppercase">
                                                                    {benefit}
                                                                </span>
                                                            ))
                                                            : scheme.benefits && (
                                                                <span className="text-[10px] font-black bg-orange-100 text-orange-700 px-3 py-1 rounded-full uppercase">
                                                                    {scheme.benefits}
                                                                </span>
                                                            )
                                                        }
                                                    </div>
                                                    {scheme.link && (
                                                        <a
                                                            href={scheme.link}
                                                            target="_blank"
                                                            rel="noopener noreferrer"
                                                            className="text-[10px] font-black text-orange-600 hover:text-orange-800 flex items-center gap-1 transition-colors whitespace-nowrap"
                                                        >
                                                            VISIT WEBSITE ↗
                                                        </a>
                                                    )}
                                                </div>
                                            </div>
                                        ))}
                                    </div>
                                </div>
                            )}
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default Recovery;
