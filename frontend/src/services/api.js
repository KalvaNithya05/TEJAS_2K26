const API_BASE_URL = 'http://localhost:5000/api';

export const getLatestSensorData = async () => {
    try {
        const response = await fetch(`${API_BASE_URL}/sensor/latest`);
        if (!response.ok) throw new Error('Network response was not ok');
        return await response.json();
    } catch (error) {
        console.error("Error fetching sensor data:", error);
        return null;
    }
};

export const getAggregateData = async () => {
    try {
        const response = await fetch(`${API_BASE_URL}/sensor/aggregate`);
        if (!response.ok) throw new Error('Network response was not ok');
        return await response.json();
    } catch (error) {
        console.error("Error fetching aggregate data:", error);
        return null;
    }
};

export const getRecommendations = async (inputData) => {
    try {
        const response = await fetch(`${API_BASE_URL}/predict/recommend`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(inputData),
        });
        if (!response.ok) throw new Error('Network response was not ok');
        return await response.json();
    } catch (error) {
        console.error("Error getting recommendations:", error);
        return null;
    }
};

export const getSoilReport = async () => {
    try {
        const response = await fetch(`${API_BASE_URL}/report/summary`);
        if (!response.ok) throw new Error('Failed to fetch report');
        return await response.json();
    } catch (error) {
        console.error("Error fetching report:", error);
        return null;
    }
}

// Disease Detection
export const detectDisease = async (formData) => {
    try {
        const response = await fetch(`${API_BASE_URL}/disease/predict`, {
            method: 'POST',
            body: formData, // FormData contains the file
        });
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error("Error detecting disease:", error);
        throw error;
    }
};

export const getSensorHistory = async () => {
    try {
        const response = await fetch(`${API_BASE_URL}/sensor/history`);
        if (!response.ok) throw new Error('Network response was not ok');
        return await response.json();
    } catch (error) {
        console.error("Error fetching sensor history:", error);
        return [];
    }
};
