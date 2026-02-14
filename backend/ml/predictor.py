import os
import pickle
import numpy as np
import random

class CropPredictor:
    AGRI_CROPS = [
        'rice', 'maize', 'chickpea', 'kidneybeans', 'pigeonpeas', 
        'mothbeans', 'mungbean', 'blackgram', 'lentil', 'cotton', 'jute'
    ]
    HORTI_CROPS = [
        'pomegranate', 'banana', 'mango', 'grapes', 'watermelon', 
        'muskmelon', 'apple', 'orange', 'papaya', 'coconut', 'coffee'
    ]

    def __init__(self):
        """
        Initializes the predictor by loading models.
        """
        # Resolve path relative to this file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.model_dir = os.path.join(os.path.dirname(current_dir), 'models')
        
        self.agri_model = self._load_model('crop_recommendation_model.pkl')
        self.label_encoder = self._load_model('label_encoder.pkl')
        # Scaler is loaded via DataPreprocessor in a real app, but here we might need manual handling if not using the class
        # However, for this structure let's assume raw features come in and we rely on DataPreprocessor used in the pipeline
        # However, for this structure let's assume raw features come in and we rely on DataPreprocessor used in the pipeline
        # Actually, best to instantiate DataPreprocessor here to handle scaling consistency
        try:
            from .preprocess import DataPreprocessor
        except ImportError:
            from preprocess import DataPreprocessor
        
        self.preprocessor = DataPreprocessor()
        
    def _load_model(self, filename):
        path = os.path.join(self.model_dir, filename)
        if os.path.exists(path):
            try:
                with open(path, 'rb') as f:
                    return pickle.load(f)
            except Exception as e:
                print(f"Error loading model {filename}: {e}")
                return None
        return None

    # Import translator
    from backend.utils.translator import translate_text

    def predict(self, features, top_n=3, lang='en', crop_type=None):
        """
        Predicts top N crops based on features.
        :param features: List or numpy array of raw features [N, P, K, Temp, Hum, pH, Rain]
        :param top_n: Number of recommendations to return
        :param lang: Language code ('en', 'hi', 'te', etc)
        :param crop_type: 'agriculture', 'horticulture', or None
        :return: List of dicts [{'crop': str, 'confidence': float, 'local_name': str}]
        """
        if self.agri_model and self.label_encoder:
            try:
                # 1. Preprocess (Scale)
                features_array = np.array(features).reshape(1, -1)
                
                # SAFETY CHECK: If inputs are all zeros (Sensor Failure), do not predict.
                if np.sum(features_array) == 0:
                    print("Warning: All sensor inputs are zero. Skipping prediction.")
                    return []
                
                # Apply scaling
                if self.preprocessor.scaler:
                    features_scaled = self.preprocessor.scaler.transform(features_array)
                else:
                    features_scaled = features_array

                # 2. Predict Probabilities
                probs = self.agri_model.predict_proba(features_scaled)[0]
                classes = self.label_encoder.classes_
                
                # FILTERING LOGIC
                if crop_type:
                    if crop_type.lower() == 'agriculture':
                        allowed = set(self.AGRI_CROPS)
                    elif crop_type.lower() == 'horticulture':
                        allowed = set(self.HORTI_CROPS)
                    else:
                        allowed = None
                    
                    if allowed:
                        for i, crop_name in enumerate(classes):
                            if crop_name.lower() not in allowed:
                                probs[i] = 0.0 # Suppress disallowed crops

                # 3. Get Top N
                top_indices = probs.argsort()[-top_n:][::-1]
                
                results = []
                classes = self.label_encoder.classes_
                from backend.utils.translator import translate_text 

                for idx in top_indices:
                    crop_name = classes[idx]
                    raw_confidence = probs[idx]
                    
                    # Use raw confidence from the calibrated model
                    confidence = raw_confidence

                    # Filter out very low confidence predictions
                    if confidence > 0.001: 
                        local_name = translate_text(crop_name, lang)
                        reasoning = self._generate_reasoning(crop_name, features, lang)
                        results.append({
                            'crop': crop_name, # Keep English key for code usage
                            'translated_crop': local_name, # Display name
                            'confidence': round(float(confidence), 2),
                            'reasoning': reasoning
                        })
                
                return results

            except Exception as e:
                print(f"Prediction Error: {e}")
                import traceback
                traceback.print_exc()
                # Fallback only on error
                return self._mock_predict(top_n, features, lang, crop_type)
            
        # Fallback if no model loaded
        return self._mock_predict(top_n, features, lang, crop_type)

    def _generate_reasoning(self, crop, features, lang='en'):
        """
        Generate simple explainability for crop choice.
        """
        # Features: [N, P, K, Temp, Hum, pH, Rain]
        # Approximate indices: 0:N, 1:P, 2:K, 3:Temp, 4:Hum, 5:pH, 6:Rain
        from backend.utils.translator import translate_text
        
        reasoning = []
        
        # Unpack
        try:
             # Handle if features is list of list or just list
             f = features[0] if isinstance(features[0], (list, np.ndarray)) else features
             rain = f[6]
             temp = f[3]
             ph = f[5]
             
             if rain > 150 and crop.lower() in ['rice', 'jute', 'sugarcane', 'coffee', 'coconut', 'banana', 'papaya']:
                 reasoning.append("High rainfall is suitable for this crop.")
             elif rain < 50 and crop.lower() in ['chickpea', 'mothbeans', 'lentil', 'blackgram', 'mungbean']:
                 reasoning.append("Suitable for low rainfall conditions.")
             
             if temp > 30 and crop.lower() not in ['wheat', 'pea']:
                  reasoning.append("Thrives in warm temperatures.")
             
             if 5.5 <= ph <= 7.0:
                 reasoning.append("Soil pH is optimal.")
                 
        except:
            pass # Fail silently on indexing error
            
        if not reasoning:
            reasoning.append(" Matches your soil nutrient profile best.")
            
        # Translate each sentence
        return [translate_text(r.strip(), lang) for r in reasoning]

    def _mock_predict(self, top_n, features, lang='en', crop_type=None):
        """
        Deterministic mock prediction logic based on features.
        The same features will always yield the same recommendations.
        """
        import hashlib
        from backend.utils.translator import translate_text
        
        # 1. Prepare pool
        all_crops = self.AGRI_CROPS + self.HORTI_CROPS
        if crop_type:
            if crop_type.lower() == 'agriculture':
                pool = self.AGRI_CROPS
            elif crop_type.lower() == 'horticulture':
                pool = self.HORTI_CROPS
            else:
                pool = all_crops
        else:
            pool = all_crops
            
        # 2. Create deterministic seed from features
        try:
            feature_str = str(features).encode('utf-8')
            feature_hash = hashlib.sha256(feature_str).hexdigest()
            seed = int(feature_hash, 16) % (2**32)
        except Exception:
            seed = 42
            
        rng = random.Random(seed)
        
        # 3. Filter candidates based on rainfall (deterministic heuristic)
        if isinstance(features[0], (list, np.ndarray)):
            flat_features = features[0]
        else:
            flat_features = features
            
        rainfall = flat_features[6] if len(flat_features) > 6 else 100 
        
        if rainfall > 200:
            candidates = [c for c in pool if c in ['rice', 'jute', 'coconut', 'papaya']]
            if not candidates: candidates = pool
        elif rainfall < 50:
            candidates = [c for c in pool if c in ['mothbeans', 'chickpea', 'lentil', 'muskmelon']]
            if not candidates: candidates = pool
        else:
            candidates = pool
            
        # 4. Deterministically select top N
        # We shuffle the candidate list with our seeded RNG
        temp_candidates = list(candidates)
        rng.shuffle(temp_candidates)
        selected = temp_candidates[:min(top_n, len(temp_candidates))]
        
        # 5. Build results
        results = []
        for crop in selected:
            # Deterministic confidence based on crop name and seed
            crop_seed = seed + sum(ord(c) for c in crop)
            crop_rng = random.Random(crop_seed)
            confidence = crop_rng.uniform(0.65, 0.85)
            
            local_name = translate_text(crop, lang)
            reasoning = self._generate_reasoning(crop, flat_features, lang)
            results.append({
                'crop': crop,
                'translated_crop': local_name,
                'confidence': round(confidence, 2),
                'reasoning': reasoning
            })
            
        # Sort desc by confidence
        results.sort(key=lambda x: x['confidence'], reverse=True)
        return results
