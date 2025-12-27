import React, { useState } from 'react';
import { getLatestSensorData, getRecommendations } from '../services/api';
// Components not strictly needed if we inline the UI, but let's keep imports clean if we were using them. 
// However, the new design uses card layouts directly in this file for cohesion as requested.

const Predict = ({ lang = 'en' }) => {
    // State
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState(null);
    const [error, setError] = useState(null);
    const [downloadingPDF, setDownloadingPDF] = useState(false);

    const handlePredict = async () => {
        setLoading(true);
        setError(null);
        setResult(null);
        try {
            // 1. Get Live Data
            const sensorData = await getLatestSensorData();
            if (!sensorData) throw new Error("Could not fetch live sensor data. Check if Pi is online.");

            // 2. Prepare Payload
            const payload = {
                ...sensorData,
                N: sensorData.nitrogen,
                P: sensorData.phosphorus,
                K: sensorData.potassium,
                lang: lang // Pass language for backend translation
            };

            // 3. Get Recommendations (Now Unified)
            const recs = await getRecommendations(payload);

            if (recs && recs.status === 'success') {
                setResult(recs);
            } else {
                throw new Error("Prediction API Failed to return results.");
            }
        } catch (e) {
            setError(e.message || (lang === 'en' ? "An unexpected error occurred." : "एक अप्रत्याशित त्रुटि हुई।"));
        } finally {
            setLoading(false);
        }
    };

    const handleDownloadPDF = async () => {
        if (!result) return;
        setDownloadingPDF(true);
        try {
            // result already contains yield_prediction from backend now
            const bodyData = {
                ...result,
                lang: lang
            };

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
            setError(`PDF Download Error: ${e.message}`);
        } finally {
            setDownloadingPDF(false);
        }
    };

    // Helper for labels
    const t = (en, hi) => (lang === 'en' ? en : hi);

    return (
        <div className="p-6 max-w-6xl mx-auto">
            <div className="text-center mb-10">
                <h1 className="text-4xl font-extrabold text-green-900 mb-2">
                    {t('Smart Agriculture Analysis', 'स्मार्ट कृषि विश्लेषण')}
                </h1>
                <p className="text-lg text-gray-600">
                    {t('One Click for Crop, Fertilizer & Yield Insights', 'फसल, उर्वरक और उपज की जानकारी के लिए एक क्लिक')}
                </p>
            </div>

            {/* ERROR MESSAGE */}
            {error && (
                <div className="mb-8 p-4 bg-red-100 border-l-4 border-red-500 text-red-700 shadow-md rounded-r-lg">
                    <p className="font-bold">Error</p>
                    <p>{error}</p>
                </div>
            )}

            {/* ANALYZE BUTTON */}
            <div className="flex justify-center mb-12">
                <button
                    onClick={handlePredict}
                    disabled={loading}
                    className={`
                        relative px-10 py-5 rounded-full font-bold text-xl shadow-xl transition-all transform 
                        ${loading
                            ? 'bg-gray-400 cursor-not-allowed scale-100'
                            : 'bg-gradient-to-r from-green-600 to-green-500 text-white hover:scale-105 hover:shadow-2xl hover:from-green-500 hover:to-green-400'
                        }
                    `}
                >
                    {loading ? (
                        <span className="flex items-center gap-2">
                            <svg className="animate-spin h-5 w-5 mr-2" viewBox="0 0 24 24">
                                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                            </svg>
                            {t("Analyzing Soil...", "मिट्टी का विश्लेषण हो रहा है...")}
                        </span>
                    ) : (
                        t("Analyze Soil & Recommend", "मिट्टी का विश्लेषण और सिफारिश")
                    )}
                </button>
            </div>

            {/* RESULTS GRID */}
            {result && (
                <div className="animate-fade-in-up space-y-12">

                    {/* 1. ROW: CROP PREDICTION & YIELD PREDICTION */}
                    <div className="grid md:grid-cols-2 gap-8">
                        {/* Crop Prediction Card */}
                        <div className="bg-white rounded-2xl shadow-lg border border-green-100 overflow-hidden transform hover:-translate-y-1 transition-transform duration-300">
                            <div className="bg-green-50 p-4 border-b border-green-100">
                                <h2 className="text-xl font-bold text-green-800 flex items-center gap-2">
                                    🌾 {t("Recommended Crop", "सिफारिश की गई फसल")}
                                </h2>
                            </div>
                            <div className="p-6">
                                {result.crops && result.crops.length > 0 ? (
                                    <>
                                        <div className="flex items-center justify-between mb-4">
                                            <h3 className="text-3xl font-extrabold text-gray-800 capitalize">
                                                {result.crops[0].translated_crop || result.crops[0].crop}
                                            </h3>
                                            <span className="px-3 py-1 bg-green-100 text-green-800 text-sm font-bold rounded-full">
                                                {Math.round(result.crops[0].confidence * 100)}% {t("Confidence", "विश्वास")}
                                            </span>
                                        </div>

                                        {/* Reasoning */}
                                        <div className="mt-4 bg-gray-50 p-4 rounded-lg border border-gray-100">
                                            <h4 className="text-sm font-semibold text-gray-500 mb-2 uppercase tracking-wide">
                                                {t("Why this crop?", "यह फसल क्यों?")}
                                            </h4>
                                            <ul className="list-disc list-inside space-y-1 text-gray-700 text-sm">
                                                {result.crops[0].reasoning && result.crops[0].reasoning.map((reason, idx) => (
                                                    <li key={idx}>{reason}</li>
                                                ))}
                                                {(!result.crops[0].reasoning || result.crops[0].reasoning.length === 0) && (
                                                    <li>{t("Best match for your soil parameters.", "आपके मिट्टी के मापदंडों के लिए सबसे अच्छा मेल।")}</li>
                                                )}
                                            </ul>
                                        </div>
                                    </>
                                ) : (
                                    <p className="text-red-500">{t("No suitable crop found.", "कोई उपयुक्त फसल नहीं मिली।")}</p>
                                )}
                            </div>
                        </div>

                        {/* Yield Prediction Card */}
                        <div className="bg-white rounded-2xl shadow-lg border border-blue-100 overflow-hidden transform hover:-translate-y-1 transition-transform duration-300">
                            <div className="bg-blue-50 p-4 border-b border-blue-100">
                                <h2 className="text-xl font-bold text-blue-800 flex items-center gap-2">
                                    📈 {t("Predicted Yield", "अनुमानित उपज")}
                                </h2>
                            </div>
                            <div className="p-6 flex flex-col justify-center h-full">
                                {result.yield_prediction ? (
                                    <div className="text-center">
                                        <div className="text-5xl font-extrabold text-blue-600 mb-2">
                                            {result.yield_prediction.predicted_yield}
                                            <span className="text-lg text-blue-400 font-medium ml-2">tons/ha</span>
                                        </div>
                                        <p className="text-gray-500 mb-1">
                                            {t("Season", "मौसम")}: <span className="font-semibold text-gray-700">{result.yield_prediction.season}</span>
                                        </p>
                                        <p className="text-xs text-gray-400 mt-4">
                                            {t("Estimated based on crop and historical weather patterns.", "फसल और ऐतिहासिक मौसम के पैटर्न के आधार पर अनुमानित।")}
                                        </p>
                                    </div>
                                ) : (
                                    <p className="text-gray-400 italic text-center">{t("Yield data unavailable", "उपज डेटा अनुपलब्ध")}</p>
                                )}
                            </div>
                        </div>
                    </div>

                    {/* 2. FERTILIZER RECOMMENDATION (Large Card) */}
                    <div className="bg-white rounded-2xl shadow-lg border border-yellow-100 overflow-hidden">
                        <div className="bg-yellow-50 p-5 border-b border-yellow-100 flex justify-between items-center">
                            <h2 className="text-2xl font-bold text-yellow-800 flex items-center gap-2">
                                🧪 {t("Fertilizer Recommendation", "उर्वरक सिफारिश")}
                            </h2>
                            <span className="px-3 py-1 bg-yellow-200 text-yellow-800 text-xs font-bold rounded-full">
                                {Math.round(result.fertilizer_recommendation.confidence * 100)}% {t("Match", "मेल")}
                            </span>
                        </div>
                        <div className="p-8">
                            <div className="mb-6">
                                <h3 className="text-3xl font-extrabold text-gray-900 mb-2">
                                    {result.fertilizer_recommendation.translated_fertilizer || result.fertilizer_recommendation.fertilizer}
                                </h3>
                                <div className="h-1 w-20 bg-yellow-400 rounded"></div>
                            </div>

                            <div className="grid md:grid-cols-2 gap-8">
                                <div>
                                    <h4 className="text-sm font-bold text-gray-500 uppercase tracking-wider mb-3">
                                        {t("Reasoning", "तर्क")}
                                    </h4>
                                    <ul className="space-y-2">
                                        {result.fertilizer_recommendation.reasoning.map((r, i) => (
                                            <li key={i} className="flex items-start gap-2 text-gray-700">
                                                <span className="text-yellow-500 mt-1">➤</span>
                                                <span>{r}</span>
                                            </li>
                                        ))}
                                    </ul>
                                </div>
                                <div className="bg-gray-50 p-4 rounded-lg">
                                    <h4 className="text-sm font-bold text-gray-500 uppercase tracking-wider mb-2">
                                        {t("Application Tips", "आवेदन युक्तियाँ")}
                                    </h4>
                                    <p className="text-sm text-gray-600 italic">
                                        {t(
                                            "Apply fertilizer in split doses for better efficiency. Ensure soil moisture before application.",
                                            "बेहतर दक्षता के लिए विभाजित खुराक में उर्वरक लागू करें। आवेदन से पहले मिट्टी की नमी सुनिश्चित करें।"
                                        )}
                                    </p>
                                </div>
                            </div>
                        </div>
                    </div>

                    {/* DOWNLOAD BUTTON */}
                    <div className="flex justify-center pb-8">
                        <button
                            onClick={handleDownloadPDF}
                            disabled={downloadingPDF}
                            className="flex items-center gap-2 px-8 py-3 bg-gray-800 text-white rounded-lg shadow-lg hover:bg-gray-900 transition-colors"
                        >
                            {downloadingPDF ? (
                                t("Generating Report...", "रिपोर्ट जनरेट हो रही है...")
                            ) : (
                                <>
                                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
                                    {t("Download Full Report (PDF)", "पूरी रिपोर्ट डाउनलोड करें (PDF)")}
                                </>
                            )}
                        </button>
                    </div>
                </div>
            )}
        </div>
    );
};

export default Predict;
