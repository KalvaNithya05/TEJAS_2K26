from flask import Blueprint, request, jsonify
from ml.predictor import CropPredictor
from ml.fertilizer_recommender import FertilizerRecommender
from ml.preprocess import DataPreprocessor
from services.weather_service import WeatherService
from services.prediction_storage_service import PredictionStorageService

predict_bp = Blueprint('predict', __name__)

# Initialize services once
predictor = CropPredictor()
fertilizer_recommender = FertilizerRecommender()
preprocessor = DataPreprocessor()
weather_service = WeatherService()
storage_service = PredictionStorageService()

@predict_bp.route('/recommend', methods=['POST'])
def recommend():
    """
    Cascaded ML Pipeline Endpoint:
    1. Predict crop using sensor data
    2. Store prediction in real_world_dataset
    3. Predict fertilizer using crop + sensor data
    4. Return crop predictions + fertilizer recommendation with reasoning
    
    Input JSON: { 
        N, P, K, ph, temperature?, humidity?, rainfall?, moisture?, 
        location?, device_id?, soil_type? 
    }
    """
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'No input data provided'}), 400

        # Auto-fill weather data if missing
        if 'humidity' not in data or 'rainfall' not in data or 'temperature' not in data:
            location = data.get('location', 'Hyderabad')
            weather = weather_service.get_current_weather(location)
            
            # Only fill missing fields
            if 'temperature' not in data: data['temperature'] = weather['temperature']
            if 'humidity' not in data: data['humidity'] = weather['humidity']
            if 'rainfall' not in data: data['rainfall'] = weather['rainfall']

        # Default moisture if not provided (assume moderate moisture)
        if 'moisture' not in data:
            data['moisture'] = 45.0  # Default moderate moisture

        # ========================================
        # STEP 1: CROP PREDICTION
        # ========================================
        # Preprocess features for crop model
        # Expects: N, P, K, temperature, humidity, ph, rainfall
        try:
            features = preprocessor.preprocess(data)
        except ValueError as e:
            return jsonify({'error': str(e)}), 400

        # Get crop predictions
        crop_predictions = predictor.predict(features, top_n=3)
        
        if not crop_predictions or len(crop_predictions) == 0:
            return jsonify({'error': 'Crop prediction failed'}), 500
        
        # Get top predicted crop
        top_crop = crop_predictions[0]
        predicted_crop_name = top_crop['crop']
        crop_confidence = top_crop['confidence']
        crop_reasoning = top_crop.get('reasoning', [])

        # ========================================
        # STEP 2: STORE PREDICTION DATA
        # ========================================
        # Store the prediction in real_world_dataset table
        sensor_data = {
            'N': data.get('N', 0),
            'P': data.get('P', 0),
            'K': data.get('K', 0),
            'temperature': data.get('temperature', 0),
            'humidity': data.get('humidity', 0),
            'moisture': data.get('moisture', 0),
            'ph': data.get('ph', 7.0),
            'rainfall': data.get('rainfall', 0),
            'soil_type': data.get('soil_type', None)
        }
        
        device_id = data.get('device_id', 'web_client')
        location = data.get('location', None)
        
        # Store Crop Prediction
        storage_service.store_crop_prediction(
            sensor_data=sensor_data,
            predicted_crop=predicted_crop_name,
            confidence=crop_confidence,
            device_id=device_id,
            location=location,
            translated_crop=top_crop.get('translated_crop')
        )

        # ========================================
        # STEP 3: FERTILIZER PREDICTION
        # ========================================
        # Use ML-based fertilizer recommendation with predicted crop as contextual feature
        fertilizer_result = fertilizer_recommender.recommend(
            temperature=float(data.get('temperature', 25)),
            humidity=float(data.get('humidity', 60)),
            moisture=float(data.get('moisture', 45)),
            soil_type=data.get('soil_type', 'Loamy'),
            crop_type=predicted_crop_name,  # Use predicted crop as contextual feature
            nitrogen=float(data.get('N', 0)),
            potassium=float(data.get('K', 0)),
            phosphorous=float(data.get('P', 0)),
            lang=data.get('lang', 'en')
        )
        
        # Store Fertilizer Prediction
        storage_service.store_fertilizer_prediction(
            input_data={
                'n': data.get('N', 0),
                'p': data.get('P', 0),
                'k': data.get('K', 0),
                'temp': data.get('temperature', 25),
                'humidity': data.get('humidity', 60),
                'moisture': data.get('moisture', 45),
                'soil_type': data.get('soil_type', 'Loamy'),
                'crop': predicted_crop_name
            },
            recommendation=fertilizer_result['fertilizer'],
            confidence=fertilizer_result['confidence'],
            reasoning=fertilizer_result['reasoning'],
            translated_fertilizer=fertilizer_result.get('translated_fertilizer')
        )

        # ========================================
        # STEP 4: YIELD PREDICTION (Integrated)
        # ========================================
        from ml.yield_predictor import YieldPredictor
        from datetime import datetime
        
        yield_predictor = YieldPredictor()
        
        # Auto-determine season
        month = datetime.now().month
        if 6 <= month <= 9:
            season = 'Kharif'
        elif 10 <= month <= 2:
            season = 'Rabi'
        else:
            season = 'Zaid'
            
        # Default estimtates for Yield inputs if not provided (Simplification for single-click)
        # In a real app, we might ask user or use historical averages for the region
        dist_avg_fert = 120.0 # kg/ha
        dist_avg_pest = 0.5   # kg/ha
        
        predicted_yield_val = yield_predictor.predict(
            state=data.get('state', 'Telangana'), 
            district=data.get('district', 'Warangal'),
            crop=predicted_crop_name,
            season=season,
            rainfall=float(data.get('rainfall', 100)),
            fertilizer=float(data.get('fertilizer_usage', dist_avg_fert)),
            pesticide=float(data.get('pesticide_usage', dist_avg_pest)),
            soil_type=data.get('soil_type', 'Loamy')
        )

        # ========================================
        # STEP 5: RETURN COMPLETE RESPONSE
        # ========================================
        return jsonify({
            'status': 'success',
            'crops': crop_predictions,
            'fertilizer_recommendation': {
                'fertilizer': fertilizer_result['fertilizer'],
                'confidence': fertilizer_result['confidence'],
                'reasoning': fertilizer_result['reasoning'],
                'translated_fertilizer': fertilizer_result.get('translated_fertilizer')
            },
            'yield_prediction': {
                'predicted_yield': predicted_yield_val,
                'unit': 'tons/ha',
                'season': season
            },
            'used_params': data,
            'data_stored': True  # Indicates prediction was stored in database
        })

    except Exception as e:
        print(f"Prediction API Error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': 'Internal Server Error', 'details': str(e)}), 500

