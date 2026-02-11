import React, { useState } from 'react';
import { getLatestSensorData, getRecommendations } from '../services/api';
import RecommendationCard from '../components/RecommendationCard';

const Predict = ({ lang = 'en', t }) => {
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState(null);
    const [error, setError] = useState(null);
    const [downloadingPDF, setDownloadingPDF] = useState(false);
    const [selectedCropType, setSelectedCropType] = useState('');

    const handlePredict = async () => {
        setLoading(true);
        setError(null);
        setResult(null);
        try {
            const sensorData = await getLatestSensorData();
            if (!sensorData) throw new Error("Could not fetch live sensor data.");

            const payload = {
                ...sensorData,
                N: sensorData.nitrogen,
                P: sensorData.phosphorus,
                K: sensorData.potassium,
                crop_type: selectedCropType,
                lang: lang
            };

            const recs = await getRecommendations(payload);

            if (recs && recs.status === 'success') {
                setResult(recs);
            } else {
                throw new Error("Prediction API Failed.");
            }
        } catch (e) {
            setError(e.message);
        } finally {
            setLoading(false);
        }
    };

    const handleDownloadPDF = async () => {
        if (!result) return;
        setDownloadingPDF(true);
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
            setError(`PDF Download Error: ${e.message}`);
        } finally {
            setDownloadingPDF(false);
        }
    };

    return (
        <div className="p-6 max-w-6xl mx-auto">
            <div className="text-center mb-10">
                <h1 className="text-5xl font-black text-green-900 mb-2 tracking-tight">
                    {t('predictor')}
                </h1>
                <p className="text-lg text-gray-500 font-medium">
                    {t('predictor_subtitle')}
                </p>
            </div>


            {error && (
                <div className="mb-8 p-4 bg-red-50 border-l-4 border-red-500 text-red-700 shadow-sm rounded-r-2xl font-bold">
                    {error}
                </div>
            )}

            <div className="flex flex-col md:flex-row items-center justify-center gap-6 mb-12">
                <div className="w-full max-w-xs">
                    <label className="block text-gray-500 font-bold mb-2 uppercase tracking-widest text-xs">
                        {t('crop_category')}
                    </label>
                    <select
                        value={selectedCropType}
                        onChange={(e) => setSelectedCropType(e.target.value)}
                        className="w-full p-4 bg-white border border-gray-100 rounded-2xl shadow-lg focus:ring-2 focus:ring-green-500 font-bold"
                    >
                        <option value="">{t('all_crops') || 'All Crops'}</option>
                        <option value="agriculture">Agriculture</option>
                        <option value="horticulture">Horticulture</option>
                    </select>
                </div>

                <div className="pt-6">
                    <button
                        onClick={handlePredict}
                        disabled={loading}
                        className={`px-12 py-5 rounded-2xl font-black text-xl shadow-2xl transition-all active:scale-95 ${loading ? 'bg-gray-200 text-gray-400 cursor-not-allowed' : 'bg-gradient-to-r from-green-600 to-emerald-600 text-white hover:shadow-green-100'}`}
                    >
                        {loading ? t('analyzing') : t('get_recom')}
                    </button>
                </div>
            </div>

            {result && (
                <div className="animate-fade-in-up space-y-8 pb-12">
                    <div className="flex justify-between items-center bg-white p-4 rounded-2xl shadow-sm border border-gray-50">
                        <span className="text-sm font-bold text-gray-400 uppercase tracking-widest px-4">
                            {result.recommendations?.length || 0} {t('results')}
                        </span>
                        <button
                            onClick={handleDownloadPDF}
                            disabled={downloadingPDF}
                            className="flex items-center gap-2 px-6 py-2 bg-gray-900 text-white rounded-xl shadow-lg hover:bg-black transition-colors text-sm font-bold"
                        >
                            {downloadingPDF ? "..." : t('download_pdf')}
                        </button>
                    </div>

                    <div className="space-y-8">
                        {result.recommendations?.map((rec, idx) => (
                            <RecommendationCard key={idx} recommendation={rec} index={idx} t={t} isManual={false} />
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
};

export default Predict;
