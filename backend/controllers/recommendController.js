const weatherService = require('../services/weatherService');
const mlService = require('../services/mlService');
const pdfService = require('../services/pdfService');

exports.getRecommendation = async (req, res) => {
    try {
        const { n, p, k, ph, city, lang } = req.body;

        if (!n || !p || !k || !ph || !city) {
            return res.status(400).json({ error: 'All fields are required' });
        }

        // 1. Fetch Weather Data
        const weatherData = await weatherService.getWeather(city);

        // 2. Call ML Model
        const recommendations = await mlService.predictCrop({ n, p, k, ph, ...weatherData }, lang || 'en');

        // 3. Return Response
        res.json({
            recommendations,
            weather: weatherData
        });

    } catch (error) {
        console.error('Error in recommendation:', error);
        res.status(500).json({ error: 'Internal Server Error' });
    }
};

exports.getYieldRecommendation = async (req, res) => {
    try {
        const { state, district, crop, season, rainfall, fertilizer, pesticide, lang } = req.body;
        // Basic validation
        if (!state || !district || !crop) {
            return res.status(400).json({ error: 'State, District and Crop are required' });
        }

        const result = await mlService.predictYield({
            state, district, crop, season, rainfall, fertilizer, pesticide
        }, lang || 'en');

        res.json(result);
    } catch (error) {
        console.error('Error in yield prediction:', error);
        res.status(500).json({ error: 'Failed to predict yield' });
    }
};

exports.getFertilizerRecommendation = async (req, res) => {
    try {
        const { n, p, k, temp, humidity, moisture, soil_type, crop, lang } = req.body;

        // Validation handled by ML service failing mostly, but good to have check

        const result = await mlService.predictFertilizer({
            n, p, k, temp, humidity, moisture, soil_type, crop
        }, lang || 'en');

        res.json(result);
    } catch (error) {
        console.error('Error in fertilizer prediction:', error);
        res.status(500).json({ error: 'Failed to predict fertilizer' });
    }
};

exports.downloadReport = async (req, res) => {
    try {
        const { n, p, k, ph, city, lang } = req.body;

        if (!n || !p || !k || !ph || !city) {
            return res.status(400).json({ error: 'All fields are required' });
        }

        // Re-fetch data to ensure fresh report
        const weatherData = await weatherService.getWeather(city);
        const recommendations = await mlService.predictCrop({ n, p, k, ph, ...weatherData }, lang || 'en');

        const reportData = {
            n, p, k, ph, city,
            weather: weatherData,
            recommendations
        };

        pdfService.generateReport(reportData, res);

    } catch (error) {
        console.error('Error generating PDF:', error);
        res.status(500).json({ error: 'Failed to generate report' });
    }
};
