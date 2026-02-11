import React from 'react';

const RecommendationCard = ({ recommendation, index, t, isManual = false }) => {
    const { crop, fertilizer, yield: yieldInfo } = recommendation;

    return (
        <div className={`bg-white rounded-3xl shadow-2xl overflow-hidden border-l-[12px] ${index === 0 ? 'border-emerald-500' : 'border-indigo-500'} transition-all duration-500 hover:scale-[1.01] hover:shadow-emerald-200/50`}>
            <div className="p-6 md:p-10">
                {/* Header: Crop Info */}
                <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-10 gap-6">
                    <div className="flex items-center gap-6">
                        <div className={`w-20 h-20 rounded-3xl flex items-center justify-center text-4xl shadow-lg transform transition-transform hover:rotate-6 ${index === 0 ? 'bg-gradient-to-br from-emerald-400 to-green-600 text-white' : 'bg-gradient-to-br from-indigo-400 to-blue-600 text-white'}`}>
                            {index === 0 ? '🥇' : index === 1 ? '🥈' : '🥉'}
                        </div>
                        <div>
                            <h2 className="text-2xl font-black text-gray-800 capitalize leading-none mb-1">
                                {crop.translated_crop || crop.crop}
                            </h2>
                        </div>
                    </div>

                    <div className="bg-slate-50/80 px-6 py-4 rounded-2xl border border-slate-200/50 flex items-center gap-8 backdrop-blur-sm shadow-sm group hover:border-blue-300 transition-colors">
                        <div className="flex flex-col">
                            <div className="text-[10px] font-black text-slate-400 uppercase tracking-[0.2em] mb-1">{t('expected_yield')}</div>
                            <div className="text-3xl font-black bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
                                {isManual ? yieldInfo.predicted_yield : '0'} <span className="text-sm font-normal text-slate-400">{yieldInfo.unit}</span>
                            </div>
                        </div>

                        {/* Confidence Bar Beside Yield (Manual) or as its own section */}
                        <div className="w-32 hidden md:block">
                            <div className="text-[10px] font-black text-slate-400 uppercase tracking-[0.2em] mb-2">{t('confidence')}</div>
                            <div className="h-3 w-full bg-slate-200 rounded-full overflow-hidden shadow-inner">
                                <div
                                    className={`h-full transition-all duration-1000 ease-out ${index === 0 ? 'bg-gradient-to-r from-emerald-400 to-green-500' : 'bg-gradient-to-r from-blue-400 to-indigo-500'}`}
                                    style={{ width: `${Math.round(crop.confidence * 100)}%` }}
                                ></div>
                            </div>
                            <div className="text-xs font-black text-slate-700 mt-2">{Math.round(crop.confidence * 100)}%</div>
                        </div>
                    </div>
                </div>

                {/* Mobile Confidence Bar */}
                <div className="md:hidden mb-6 bg-gray-50 p-3 rounded-xl border border-gray-100">
                    <div className="text-xs font-bold text-gray-400 uppercase tracking-tighter mb-1">{t('confidence')}</div>
                    <div className="flex items-center gap-3">
                        <div className="flex-1 h-2 bg-gray-200 rounded-full overflow-hidden">
                            <div
                                className={`h-full ${index === 0 ? 'bg-green-500' : 'bg-blue-400'}`}
                                style={{ width: `${Math.round(crop.confidence * 100)}%` }}
                            ></div>
                        </div>
                        <span className="text-xs font-black text-gray-700">{Math.round(crop.confidence * 100)}%</span>
                    </div>
                </div>

                <div className="grid lg:grid-cols-[1.5fr_1fr] gap-10 items-stretch">
                    {/* Fertilizer Recommendation Section - Matched to Photo */}
                    <div className="bg-gradient-to-br from-amber-50 to-orange-50/30 rounded-3xl overflow-hidden border border-amber-200 shadow-md flex flex-col hover:shadow-xl transition-all duration-500 hover:scale-[1.005]">
                        <div className="px-8 py-4 border-b border-amber-200 flex justify-between items-center bg-white/80 backdrop-blur-md">
                            <h3 className="text-amber-800 font-black flex items-center gap-3 uppercase tracking-widest text-xs">
                                <span className="text-2xl">🧪</span> {t('fertilizer_advice')}
                            </h3>
                            <div className="bg-gradient-to-r from-amber-500 to-orange-600 text-white text-[10px] font-black px-4 py-1.5 rounded-full shadow-lg tracking-wider">
                                {Math.round(fertilizer.confidence * 100)}% MATCH
                            </div>
                        </div>

                        <div className="p-6 md:p-8 bg-white/50 flex-1">
                            <div className="mb-8">
                                <h4 className="text-5xl font-black text-slate-800 tracking-tight capitalize inline-block relative">
                                    {fertilizer.translated_name || fertilizer.name}
                                    <div className="absolute -bottom-2 left-0 w-full h-3 bg-yellow-400/30 -skew-x-12 -z-10"></div>
                                </h4>
                            </div>

                            <div className="space-y-6">
                                {/* Reasoning */}
                                <div className="space-y-4">
                                    <div className="text-[10px] font-black text-amber-600/60 uppercase tracking-[0.25em] mb-2 flex items-center gap-2">
                                        <div className="w-4 h-[1px] bg-amber-200"></div>
                                        REASONING
                                    </div>
                                    <div className="space-y-3">
                                        {fertilizer.reasoning?.map((reason, i) => (
                                            <div key={i} className="flex items-start gap-4 text-sm text-slate-700 font-bold leading-relaxed group/item">
                                                <span className="text-amber-500 font-black mt-1 group-hover:rotate-12 transition-transform">✦</span>
                                                {reason}
                                            </div>
                                        ))}
                                    </div>
                                </div>

                                {/* Application Tips Box - High Glow Glassmorphism */}
                                {fertilizer.application_tips && fertilizer.application_tips.length > 0 && (
                                    <div className="bg-gradient-to-br from-blue-500/10 to-indigo-500/5 rounded-3xl p-8 border border-blue-200/50 hover:bg-blue-50/80 transition-all duration-500 shadow-inner relative overflow-hidden group">
                                        <div className="absolute top-0 right-0 w-32 h-32 bg-blue-400/10 rounded-full -mr-16 -mt-16 blur-3xl group-hover:bg-blue-400/20 transition-colors"></div>
                                        <div className="text-[10px] font-black text-blue-500 uppercase tracking-[0.3em] mb-5 flex items-center gap-2">
                                            <span className="w-2 h-2 rounded-full bg-blue-400 animate-pulse"></span>
                                            APPLICATION TIPS
                                        </div>
                                        <div className="space-y-4 relative z-10">
                                            {fertilizer.application_tips.map((tip, i) => (
                                                <div key={i} className="text-sm md:text-base text-blue-900 leading-relaxed font-black italic">
                                                    "{tip}"
                                                </div>
                                            ))}
                                        </div>
                                    </div>
                                )}
                            </div>
                        </div>
                    </div>

                    {/* Reasoning Box (Crop specific) */}
                    <div className="bg-gradient-to-b from-slate-50 to-white rounded-3xl p-8 border border-slate-200 shadow-sm flex flex-col hover:shadow-lg hover:border-emerald-200 transition-all duration-500">
                        <div className="text-[10px] font-black text-slate-400 uppercase tracking-[0.25em] mb-8 flex items-center gap-3">
                            <div className="w-8 h-[2px] bg-emerald-400"></div>
                            WHY {crop.translated_crop || crop.crop}?
                        </div>
                        <div className="space-y-4 flex-1">
                            {crop.reasoning?.map((reason, i) => (
                                <div key={i} className="bg-white p-5 rounded-2xl border border-slate-100 flex items-start gap-4 text-xs text-slate-700 font-bold shadow-sm hover:shadow-md hover:-translate-y-0.5 transition-all duration-300 group">
                                    <div className="w-2 h-2 rounded-full bg-emerald-500 mt-1.5 shrink-0 group-hover:scale-150 transition-transform shadow-[0_0_8px_rgba(16,185,129,0.5)]"></div>
                                    {reason}
                                </div>
                            ))}
                        </div>
                        <div className="mt-10 pt-6 border-t border-slate-100">
                            <div className="text-[10px] text-slate-400 italic font-bold tracking-tight">
                                * Recommendations optimized for {yieldInfo.season} season conditions through advanced agro-analysis.
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default RecommendationCard;
