from flask import Blueprint, request, jsonify
from ml.predictor import CropPredictor
from ml.fertilizer_recommender import FertilizerRecommender
from ml.preprocess import DataPreprocessor
from ml.yield_predictor import YieldPredictor
from services.weather_service import WeatherService
from services.prediction_storage_service import PredictionStorageService
from datetime import datetime

predict_bp = Blueprint('predict', __name__)

# Initialize services once
predictor = CropPredictor()
fertilizer_recommender = FertilizerRecommender()
yield_predictor = YieldPredictor()
preprocessor = DataPreprocessor()
weather_service = WeatherService()
storage_service = PredictionStorageService()

@predict_bp.route('/recommend', methods=['POST'])
def recommend():
    """
    Cascaded ML Pipeline Endpoint:
    1. Predict top N crops using sensor data
    2. For EACH crop, predict Fertilizer and Yield
    3. Return consolidated recommendations
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

        # Default moisture if not provided
        if 'moisture' not in data:
            data['moisture'] = 45.0

        # Preprocess features
        try:
            features = preprocessor.preprocess(data)
        except ValueError as e:
            return jsonify({'error': str(e)}), 400

        # Get crop predictions
        crop_type_input = data.get('crop_type')
        lang = data.get('lang', 'en')
        crop_predictions = predictor.predict(features, top_n=3, lang=lang, crop_type=crop_type_input)
        
        if not crop_predictions:
            return jsonify({'error': 'Crop prediction failed'}), 500
        
        # Determine season (User input > Auto-detect)
        season = data.get('season')
        if not season:
            month = datetime.now().month
            if 6 <= month <= 9: session = 'Kharif'
            elif 10 <= month <= 2: session = 'Rabi'
            else: session = 'Zaid'
            
        dist_avg_fert = 120.0 # kg/ha
        dist_avg_pest = 0.5   # kg/ha
        
        # Combined results
        final_recommendations = []
        
        for crop_info in crop_predictions:
            crop_name = crop_info['crop']
            
            # 1. Fertilizer Recommendation
            fertilizer_result = fertilizer_recommender.recommend(
                temperature=float(data.get('temperature', 25)),
                humidity=float(data.get('humidity', 60)),
                moisture=float(data.get('moisture', 45)),
                soil_type=data.get('soil_type', 'Loamy'),
                crop_type=crop_name,
                nitrogen=float(data.get('N', 0)),
                potassium=float(data.get('K', 0)),
                phosphorous=float(data.get('P', 0)),
                lang=lang
            )
            
            # 2. Yield Prediction
            predicted_yield_val = yield_predictor.predict(
                state=data.get('state', 'Telangana'), 
                district=data.get('district', 'Warangal'),
                crop=crop_name,
                season=season,
                rainfall=float(data.get('rainfall', 100)),
                fertilizer=float(data.get('fertilizer_usage', dist_avg_fert)),
                pesticide=float(data.get('pesticide_usage', dist_avg_pest)),
                soil_type=data.get('soil_type', 'Loamy')
            )
            
            # Store primary prediction only (top crop) if needed, 
            # but usually we want to store what the user finally selects.
            # For now, let's keep it simple and return all.
            
            final_recommendations.append({
                'crop': crop_info,
                'fertilizer': {
                    'name': fertilizer_result['fertilizer'],
                    'translated_name': fertilizer_result.get('translated_fertilizer'),
                    'confidence': fertilizer_result['confidence'],
                    'reasoning': fertilizer_result['reasoning'],
                    'application_tips': fertilizer_result.get('application_tips', [])
                },
                'yield': {
                    'predicted_yield': predicted_yield_val,
                    'unit': 'tons/ha',
                    'season': season
                }
            })

        # Storage logic (optional: store top recommendation)
        if final_recommendations:
            top = final_recommendations[0]
            storage_service.store_crop_prediction(
                sensor_data=data, # Simple pass through
                predicted_crop=top['crop']['crop'],
                confidence=top['crop']['confidence'],
                device_id=data.get('device_id', 'web_client'),
                location=data.get('location', None)
            )

        return jsonify({
            'status': 'success',
            'recommendations': final_recommendations,
            'used_params': data
        })

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': 'Internal Server Error', 'details': str(e)}), 500


    except Exception as e:
        print(f"Prediction API Error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': 'Internal Server Error', 'details': str(e)}), 500

