from config.supabase_client import supabase
from datetime import datetime

class PredictionStorageService:
    """
    Service to store real-world prediction data in the database.
    Standardized to use crop_predictions and created_at.
    """
    
    def store_crop_prediction(self, sensor_data, predicted_crop, confidence, device_id='web_client', location=None, translated_crop=None):
        """
        Store a crop prediction.
        """
        if not supabase:
            return None
        
        try:
            record = {
                'created_at': datetime.now().isoformat(),
                'device_id': device_id,
                'city': location,
                'nitrogen': float(sensor_data.get('nitrogen') or sensor_data.get('N', 0)),
                'phosphorus': float(sensor_data.get('phosphorus') or sensor_data.get('P', 0)),
                'potassium': float(sensor_data.get('potassium') or sensor_data.get('K', 0)),
                'ph': float(sensor_data.get('ph') or sensor_data.get('pH', 0)),
                'temperature': float(sensor_data.get('temperature', 0)),
                'humidity': float(sensor_data.get('humidity', 0)),
                'rainfall': float(sensor_data.get('rainfall', 0)),
                'predicted_crop': predicted_crop,
                'confidence': float(confidence),
                'translated_crop': translated_crop
            }
            
            response = supabase.table('crop_predictions').insert(record).execute()
            
            if response.data:
                print(f"✓ Crop prediction stored: {predicted_crop}")
                return response.data[0]
            else:
                print("✗ Failed to store crop prediction")
                return None
                
        except Exception as e:
            print(f"Error storing crop prediction: {e}")
            return None

    def store_fertilizer_prediction(self, input_data, recommendation, confidence, reasoning, translated_fertilizer=None):
        """
        Store a fertilizer prediction.
        """
        if not supabase:
            return None
            
        try:
            record = {
                'created_at': datetime.now().isoformat(),
                'nitrogen': float(input_data.get('nitrogen') or input_data.get('n', 0)),
                'phosphorus': float(input_data.get('phosphorus') or input_data.get('p', 0)),
                'potassium': float(input_data.get('potassium') or input_data.get('k', 0)),
                'temperature': float(input_data.get('temperature') or input_data.get('temp', 0)),
                'humidity': float(input_data.get('humidity', 0)),
                'moisture': float(input_data.get('moisture', 0)),
                'soil_type': input_data.get('soil_type'),
                'crop_type': input_data.get('crop'),
                'recommended_fertilizer': recommendation,
                'confidence': float(confidence),
                'reasoning': reasoning,
                'translated_fertilizer': translated_fertilizer
            }
            
            response = supabase.table('fertilizer_predictions').insert(record).execute()
            
            if response.data:
                 print(f"✓ Fertilizer prediction stored: {recommendation}")
                 return response.data[0]
            return None
            
        except Exception as e:
            print(f"Error storing fertilizer prediction: {e}")
            return None
    
    def get_recent_predictions(self, device_id='pi_01', limit=10):
        """
        Retrieve recent crop predictions for a device.
        """
        if not supabase:
            return []
        
        try:
            response = supabase.table('crop_predictions')\
                .select('*')\
                .eq('device_id', device_id)\
                .order('created_at', desc=True)\
                .limit(limit)\
                .execute()
            
            return response.data if response.data else []
            
        except Exception as e:
            print(f"Error retrieving predictions: {e}")
            return []
    
    def get_crop_statistics(self, days=30):
        """
        Get statistics on predicted crops over the last N days.
        """
        if not supabase:
            return {}
        
        try:
            from datetime import timedelta
            cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()
            
            response = supabase.table('crop_predictions')\
                .select('predicted_crop')\
                .gte('created_at', cutoff_date)\
                .execute()
            
            if not response.data:
                return {}
            
            crop_counts = {}
            for record in response.data:
                crop = record['predicted_crop']
                crop_counts[crop] = crop_counts.get(crop, 0) + 1
            
            return crop_counts
            
        except Exception as e:
            print(f"Error getting crop statistics: {e}")
            return {}
