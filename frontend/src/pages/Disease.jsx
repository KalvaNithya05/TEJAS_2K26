import React, { useState } from 'react';
import { detectDisease } from '../services/api';

const Disease = ({ lang, t }) => {
    const [selectedImages, setSelectedImages] = useState([]);
    const [previewUrls, setPreviewUrls] = useState([]);
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const handleImageChange = (e) => {
        if (e.target.files && e.target.files.length > 0) {
            const files = Array.from(e.target.files);
            if (files.length > 5) {
                alert("Please select up to 5 images.");
                return;
            }
            setSelectedImages(files);
            const urls = files.map(file => URL.createObjectURL(file));
            setPreviewUrls(urls);
            setResult(null);
            setError(null);
        }
    };

    const handlePredict = async () => {
        if (selectedImages.length === 0) return;

        setLoading(true);
        setError(null);

        const formData = new FormData();
        selectedImages.forEach(img => {
            formData.append('images', img);
        });
        formData.append('lang', lang);

        try {
            const data = await detectDisease(formData);
            if (data.error) throw new Error(data.error);
            setResult(data);
        } catch (err) {
            setError(err.message || "Failed to analyze images.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-green-50 to-blue-50 p-6 flex flex-col items-center">
            <h1 className="text-5xl font-black text-green-900 mb-2 tracking-tight">{t('disease_check')}</h1>
            <p className="text-gray-500 mb-8 text-center max-w-2xl font-medium">
                Upload clear photos of plant leaves to detect potential diseases using our consensus-based AI models.
            </p>

            <div className="w-full max-w-lg bg-white rounded-[40px] shadow-2xl overflow-hidden p-8 border border-white">

                {/* Upload Section */}
                <div className="border-4 border-dashed border-green-100 rounded-[32px] p-10 text-center cursor-pointer hover:bg-green-50 hover:border-green-300 transition-all relative group">
                    <input
                        type="file"
                        accept="image/*"
                        multiple
                        onChange={handleImageChange}
                        className="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-10"
                    />

                    {previewUrls.length === 0 ? (
                        <div className="flex flex-col items-center">
                            <div className="w-20 h-20 bg-green-50 rounded-3xl flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
                                <svg className="w-10 h-10 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                                </svg>
                            </div>
                            <span className="text-gray-400 font-black uppercase tracking-widest text-xs">{t('upload_leaf')}</span>
                        </div>
                    ) : (
                        <div className="grid grid-cols-3 gap-3">
                            {previewUrls.map((url, i) => (
                                <img key={url} src={url} alt={`Preview ${i}`} className="w-full h-24 object-cover rounded-2xl shadow-lg border-2 border-white" />
                            ))}
                            <div className="flex items-center justify-center bg-green-600 rounded-2xl text-white font-black text-xl shadow-lg">
                                +{previewUrls.length}
                            </div>
                        </div>
                    )}
                </div>

                {/* Action Button */}
                <div className="mt-8">
                    <button
                        onClick={handlePredict}
                        disabled={selectedImages.length === 0 || loading}
                        className={`w-full py-5 rounded-[24px] font-black text-white text-xl tracking-tight transition-all shadow-xl active:scale-95 ${selectedImages.length === 0 || loading
                            ? 'bg-gray-200 text-gray-400 cursor-not-allowed shadow-none'
                            : 'bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-700 hover:to-emerald-700'
                            }`}
                    >
                        {loading ? (
                            <span className="flex items-center justify-center uppercase tracking-widest text-sm">
                                <svg className="animate-spin h-5 w-5 mr-3 text-white" viewBox="0 0 24 24">
                                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                                </svg>
                                {t('analyzing')}
                            </span>
                        ) : t('run_check')}
                    </button>
                    {error && <p className="mt-4 text-red-500 font-bold text-center text-sm bg-red-50 p-3 rounded-xl">{error}</p>}
                </div>
            </div>

            {/* Results Section */}
            {result && (
                <div className="w-full max-w-2xl mt-12 animate-fade-in-up pb-20">
                    <div className="bg-white rounded-[48px] shadow-2xl overflow-hidden border-t-[16px] border-green-500 border-x border-b border-gray-100">
                        <div className="p-10 md:p-14">
                            <div className="flex flex-col md:flex-row justify-between items-start mb-10 gap-6">
                                <div>
                                    <div className="flex items-center gap-2 mb-3">
                                        <span className="bg-green-100 text-green-700 text-[10px] font-black uppercase tracking-[0.2em] px-3 py-1 rounded-full">Analysis Result</span>
                                    </div>
                                    <h2 className="text-5xl font-black text-gray-900 capitalize tracking-tighter leading-none mb-2">
                                        {result.final_disease}
                                    </h2>
                                    <p className="text-gray-500 font-medium mt-4 max-w-lg italic">
                                        {result.explanation}
                                    </p>
                                </div>

                                <div className="flex flex-col items-end">
                                    <div className={`text-6xl font-black tracking-tighter ${result.final_disease.toLowerCase().includes('healthy') ? 'text-green-600' : 'text-red-500'}`}>
                                        {result.final_confidence}
                                    </div>
                                    <div className="text-[10px] font-black text-gray-400 uppercase tracking-widest">{t('confidence')}</div>
                                </div>
                            </div>

                            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-10">
                                <div className="bg-blue-600 rounded-[32px] p-8 shadow-xl shadow-blue-100 relative overflow-hidden">
                                    <div className="absolute top-0 right-0 w-32 h-32 bg-white/10 rounded-full -mr-16 -mt-16 blur-3xl"></div>
                                    <h3 className="font-black text-white mb-4 flex items-center text-xl uppercase tracking-wider">
                                        <span className="text-2xl mr-3">🩺</span>
                                        {t('treatment')}
                                    </h3>
                                    <p className="text-blue-50 text-lg leading-relaxed font-medium">
                                        {result.treatment_plan}
                                    </p>
                                </div>

                                <div className="bg-emerald-600 rounded-[32px] p-8 shadow-xl shadow-emerald-100 relative overflow-hidden">
                                    <div className="absolute top-0 right-0 w-32 h-32 bg-white/10 rounded-full -mr-16 -mt-16 blur-3xl"></div>
                                    <h3 className="font-black text-white mb-4 flex items-center text-xl uppercase tracking-wider">
                                        <span className="text-2xl mr-3">🛡️</span>
                                        Prevention Tips
                                    </h3>
                                    <ul className="text-emerald-50 text-md leading-relaxed font-medium list-disc list-inside">
                                        {result.prevention_tips.map((tip, idx) => (
                                            <li key={idx} className="mb-1">{tip}</li>
                                        ))}
                                    </ul>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default Disease;
