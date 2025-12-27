import React from 'react';

const FertilizerTips = ({ recommendation }) => {
    // Handle both old format (array) and new ML format (object)
    if (!recommendation) return null;
    
    // Check if it's the new ML-based format (object with fertilizer, confidence, reasoning)
    const isMLFormat = recommendation && typeof recommendation === 'object' && recommendation.fertilizer;
    
    if (isMLFormat) {
        const { fertilizer, confidence, reasoning } = recommendation;
        
        return (
            <div className="bg-white p-6 rounded-lg shadow-md mt-6">
                <h2 className="text-xl font-bold text-amber-700 mb-4 flex items-center">
                    <span className="mr-2">🌱</span> Fertilizer Recommendation
                </h2>

                {/* Fertilizer Name - Prominent Display */}
                <div className="mb-4 p-4 bg-gradient-to-r from-green-50 to-emerald-50 rounded-lg border-2 border-green-200">
                    <div className="text-sm text-gray-600 mb-1">Recommended Fertilizer:</div>
                    <div className="text-2xl font-bold text-green-700">{fertilizer}</div>
                    <div className="text-sm text-gray-500 mt-1">
                        Confidence: <span className="font-semibold text-green-600">{(confidence * 100).toFixed(1)}%</span>
                    </div>
                </div>

                {/* Reasoning */}
                {reasoning && reasoning.length > 0 && (
                    <div>
                        <h3 className="text-sm font-semibold text-gray-700 mb-2">Why this fertilizer?</h3>
                        <ul className="space-y-2">
                            {reasoning.map((reason, index) => (
                                <li key={index} className="flex items-start p-3 bg-amber-50 rounded-md border border-amber-100 text-gray-800 text-sm">
                                    <span className="text-amber-500 mr-2 text-lg font-bold">•</span>
                                    <span className="mt-0.5 leading-relaxed">{reason}</span>
                                </li>
                            ))}
                        </ul>
                    </div>
                )}

                <div className="mt-4 text-xs text-gray-500 text-center italic">
                    * Please consult a local agronomist before large-scale application.
                </div>
            </div>
        );
    }
    
    // Old format fallback (array of tips)
    const tips = Array.isArray(recommendation) ? recommendation : [];
    if (tips.length === 0) return null;
    
    return (
        <div className="bg-white p-6 rounded-lg shadow-md mt-6">
            <h2 className="text-xl font-bold text-amber-700 mb-4 flex items-center">
                <span className="mr-2">📝</span> Soil Health & Fertilizer Guide
            </h2>

            <ul className="space-y-3">
                {tips.map((tip, index) => (
                    <li key={index} className="flex items-start p-3 bg-amber-50 rounded-md border border-amber-100 text-gray-800 text-sm">
                        <span className="text-amber-500 mr-2 text-lg font-bold">•</span>
                        <span className="mt-0.5 leading-relaxed">{tip}</span>
                    </li>
                ))}
            </ul>

            <div className="mt-4 text-xs text-gray-500 text-center italic">
                * Please consult a local agronomist before large-scale application.
            </div>
        </div>
    );
};

export default FertilizerTips;
