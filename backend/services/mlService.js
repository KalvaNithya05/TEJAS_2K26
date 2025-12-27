const { spawn } = require('child_process');
const path = require('path');

exports.predictCrop = (inputData, lang = 'en') => {
    return new Promise((resolve, reject) => {
        // Path to python script
        const scriptPath = path.join(__dirname, '../../ml/predict.py');

        // Prepare arguments
        const args = [
            inputData.n,
            inputData.p,
            inputData.k,
            inputData.ph,
            inputData.temp,
            inputData.humidity,
            inputData.rainfall,
            lang
        ];

        console.log('Running Crop ML script with args:', args);

        const pythonProcess = spawn('python', [scriptPath, ...args]);

        let dataString = '';

        pythonProcess.stdout.on('data', (data) => {
            dataString += data.toString();
        });

        pythonProcess.stderr.on('data', (data) => {
            console.error(`ML Error: ${data}`);
        });

        pythonProcess.on('close', (code) => {
            if (code !== 0) {
                console.warn('ML script failed, returning fallback data');
                resolve([]);
                return;
            }

            try {
                const results = JSON.parse(dataString);
                resolve(results);
            } catch (e) {
                console.error('Failed to parse ML output');
                resolve([]);
            }
        });
    });
};

exports.predictYield = (inputData, lang = 'en') => {
    return new Promise((resolve, reject) => {
        const scriptPath = path.join(__dirname, '../../ml/predict_yield.py');

        // Args: state, district, crop, season, rain, fert, pest, lang
        const args = [
            inputData.state,
            inputData.district,
            inputData.crop,
            inputData.season,
            inputData.rainfall, // annual rainfall
            inputData.fertilizer,
            inputData.pesticide,
            lang
        ];

        console.log('Running Yield ML script with args:', args);

        const pythonProcess = spawn('python', [scriptPath, ...args]);

        let dataString = '';

        pythonProcess.stdout.on('data', (data) => {
            dataString += data.toString();
        });

        pythonProcess.stderr.on('data', (data) => {
            console.error(`Yield ML Error: ${data}`);
        });

        pythonProcess.on('close', (code) => {
            if (code !== 0) {
                resolve(null);
                return;
            }
            try {
                const result = JSON.parse(dataString);
                resolve(result);
            } catch (e) {
                console.error('Failed to parse Yield ML output');
                resolve(null);
            }
        });
    });
};
