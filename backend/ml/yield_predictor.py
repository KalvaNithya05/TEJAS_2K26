import os
import pickle
import numpy as np

class YieldPredictor:
    def __init__(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.model_dir = os.path.join(os.path.dirname(current_dir), 'models')
        
        self.model = self._load_model('yield_model.pkl')
        self.scaler = self._load_model('yield_scaler.pkl')
        self.encoders = self._load_model('yield_encoders.pkl')
        
    def _load_model(self, filename):
        path = os.path.join(self.model_dir, filename)
        if os.path.exists(path):
            try:
                with open(path, 'rb') as f:
                    return pickle.load(f)
            except Exception as e:
                print(f"Error loading {filename}: {e}")
                return None
        return None

    def predict(self, state, district, crop, season, rainfall, fertilizer, pesticide, soil_type=None):
        """
        Predicts yield.
        """
        if not self.model:
            return None
            
        try:
            # Prepare input array
            # Order: State, District, Crop, Season, Soil_Type (if exists), Ann_Rain, Fert, Pest
            
            # Helper to encode safely
            def encode(col_name, value):
                if col_name in self.encoders:
                    le = self.encoders[col_name]
                    # Handle unseen labels
                    if value in le.classes_:
                        return le.transform([value])[0]
                    else:
                        # Fallback for unseen labels: Use mode or specific defaults
                        # For now, just using 0 or a known valid index if available
                        print(f"Warning: Unseen label '{value}' for {col_name}. Using default.")
                        return 0
                return 0
                
            input_features = []
            
            # Smart defaults/mappings for user friendly names
            # Map standard state names to dataset names if slightly different
            # (Assuming model was trained on specific casing)
            
            # Categorical
            input_features.append(encode('State', state))
            input_features.append(encode('District', district))
            input_features.append(encode('Crop', crop))
            input_features.append(encode('Season', season))
            
            # Handle empty or missing soil type
            if 'Soil_Type' in self.encoders:
                st = soil_type if soil_type else 'Clayey' # Default assumption
                input_features.append(encode('Soil_Type', st))
                 
            # Numerical
            # Must scale
            raw_nums = np.array([[float(rainfall), float(fertilizer), float(pesticide)]])
            scaled_nums = self.scaler.transform(raw_nums)[0]
            
            input_features.extend(scaled_nums)
            
            # Reshape for prediction
            final_input = np.array([input_features])
            
            prediction = self.model.predict(final_input)[0]
            return round(prediction, 2)
            
        except Exception as e:
            print(f"Yield Prediction Error: {e}")
            return None
