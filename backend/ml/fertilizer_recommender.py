import os
import pickle
import numpy as np

class FertilizerRecommender:
    """
    ML-based fertilizer recommendation system.
    Uses trained Random Forest model to predict fertilizer based on:
    - Environmental factors (temperature, humidity, moisture)
    - Soil nutrients (N, P, K)
    - Soil type
    - Predicted crop type (from crop prediction model)
    """
    
    def __init__(self):
        """
        Initialize the recommender by loading the trained model and encoders.
        """
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.model_dir = os.path.join(os.path.dirname(current_dir), 'models')
        
        # Load model and encoders
        self.model = self._load_model('fertilizer_model.pkl')
        self.scaler = self._load_model('fertilizer_scaler.pkl')
        self.soil_encoder = self._load_model('soil_encoder.pkl')
        self.crop_encoder = self._load_model('crop_encoder.pkl')
        self.fertilizer_encoder = self._load_model('fertilizer_label_encoder.pkl')
        self.metadata = self._load_model('fertilizer_metadata.pkl')
        
    def _load_model(self, filename):
        """Load a pickled model or encoder."""
        path = os.path.join(self.model_dir, filename)
        if os.path.exists(path):
            try:
                with open(path, 'rb') as f:
                    return pickle.load(f)
            except Exception as e:
                print(f"Error loading {filename}: {e}")
                return None
        return None
    
    # Import translator
    from backend.utils.translator import translate_text

    def recommend(self, temperature, humidity, moisture, soil_type, crop_type, nitrogen, potassium, phosphorous, lang='en'):
        """
        Predict fertilizer recommendation using ML model.
        
        Args:
            temperature: Temperature in Celsius
            humidity: Humidity percentage
            moisture: Soil moisture percentage
            soil_type: Soil type (Sandy, Loamy, Black, Red, Clayey)
            crop_type: Predicted crop type from crop model
            nitrogen: Nitrogen content (mg/kg)
            potassium: Potassium content (mg/kg)
            phosphorous: Phosphorous content (mg/kg)
            
        Returns:
            dict with keys:
                - fertilizer: Recommended fertilizer name
                - confidence: Confidence score (0-1)
                - reasoning: List of explanation strings
        """
        if not self.model or not self.scaler:
            # Fallback to rule-based if model not loaded
            return self._rule_based_fallback(nitrogen, phosphorous, potassium, crop_type, lang)
        
        try:
            # Prepare features in correct order: Temparature, Humidity, Moisture, Soil Type, Crop Type, Nitrogen, Potassium, Phosphorous
            # Encode categorical variables
            
            # Handle soil type encoding
            if soil_type and soil_type in self.soil_encoder.classes_:
                soil_encoded = self.soil_encoder.transform([soil_type])[0]
            else:
                # Default to most common soil type if not recognized
                soil_encoded = 0  # Sandy (first in alphabet)
            
            # Handle crop type encoding
            # Map crop prediction to fertilizer dataset crop names
            crop_mapping = {
                'rice': 'Paddy',
                'paddy': 'Paddy',
                'maize': 'Maize',
                'wheat': 'Wheat',
                'cotton': 'Cotton',
                'sugarcane': 'Sugarcane',
                'barley': 'Barley',
                'millet': 'Millets',
                'millets': 'Millets',
                'pulses': 'Pulses',
                'tobacco': 'Tobacco',
                'groundnut': 'Ground Nuts',
                'oilseeds': 'Oil seeds',
                'chickpea': 'Pulses',
                'kidneybeans': 'Pulses',
                'pigeonpeas': 'Pulses',
                'mothbeans': 'Pulses',
                'mungbean': 'Pulses',
                'blackgram': 'Pulses',
                'lentil': 'Pulses',
                'jute': 'Cotton' # Jute has similar fiber-crop requirements to Cotton
            }
            
            # Try to map the crop
            mapped_crop = crop_mapping.get(crop_type.lower() if crop_type else '', 'Wheat')
            
            if mapped_crop in self.crop_encoder.classes_:
                crop_encoded = self.crop_encoder.transform([mapped_crop])[0]
            else:
                # Default to Wheat if crop not in training data
                crop_encoded = self.crop_encoder.transform(['Wheat'])[0]
            
            # Create feature array
            features = np.array([[
                temperature,
                humidity,
                moisture,
                soil_encoded,
                crop_encoded,
                nitrogen,
                potassium,
                phosphorous
            ]])
            
            # Scale features
            features_scaled = self.scaler.transform(features)
            
            # Predict
            prediction = self.model.predict(features_scaled)[0]
            probabilities = self.model.predict_proba(features_scaled)[0]
            
            # Get fertilizer name and confidence
            fertilizer_name = self.fertilizer_encoder.inverse_transform([prediction])[0]
            confidence = probabilities[prediction]
            
            # Generate reasoning and tips
            reasoning = self._generate_reasoning(
                fertilizer_name, crop_type, nitrogen, phosphorous, potassium,
                temperature, humidity, moisture, soil_type
            )
            
            tips = self._generate_application_tips(fertilizer_name, crop_type)
            
            # Translate
            from backend.utils.translator import translate_text
            
            trans_fertilizer = translate_text(fertilizer_name, lang)
            trans_reasoning = [translate_text(r, lang) for r in reasoning]
            trans_tips = [translate_text(t, lang) for t in tips]
            
            return {
                'fertilizer': fertilizer_name,
                'translated_fertilizer': trans_fertilizer,
                'confidence': round(float(confidence), 2),
                'reasoning': trans_reasoning,
                'application_tips': trans_tips
            }
            
        except Exception as e:
            print(f"Fertilizer prediction error: {e}")
            return self._rule_based_fallback(nitrogen, phosphorous, potassium, crop_type, lang)
    
    def _generate_reasoning(self, fertilizer, crop, n, p, k, temp, humidity, moisture, soil_type):
        """
        Generate human-readable reasoning for the fertilizer recommendation.
        """
        reasoning = []
        
        # Crop-specific reasoning
        if crop:
            crop_lower = crop.lower()
            if crop_lower in ['rice', 'paddy']:
                reasoning.append(f"{crop} requires high nitrogen for vegetative growth and tillering")
            elif crop_lower in ['wheat', 'maize']:
                reasoning.append(f"{crop} benefits from balanced NPK nutrition for grain development")
            elif crop_lower == 'cotton':
                reasoning.append(f"{crop} requires adequate potassium for fiber quality and disease resistance")
            elif crop_lower in ['pulses', 'legumes']:
                reasoning.append(f"{crop} requires phosphorus for root development and nitrogen fixation")
            else:
                reasoning.append(f"Fertilizer optimized for {crop} nutrient requirements")
        
        # Nutrient deficiency analysis
        if n < 30:
            reasoning.append(f"Low nitrogen level ({n} mg/kg) detected - nitrogen-rich fertilizer recommended")
        elif n > 50:
            reasoning.append(f"Adequate nitrogen level ({n} mg/kg) - balanced fertilizer recommended")
        
        if p < 20:
            reasoning.append(f"Low phosphorus level ({p} mg/kg) - phosphorus supplementation needed")
        elif p > 40:
            reasoning.append(f"Sufficient phosphorus level ({p} mg/kg)")
        
        if k < 30:
            reasoning.append(f"Low potassium level ({k} mg/kg) - potassium supplementation recommended")
        elif k > 50:
            reasoning.append(f"Adequate potassium level ({k} mg/kg)")
        
        # Environmental factors
        if moisture < 35:
            reasoning.append("Low soil moisture - consider water-soluble fertilizers for better uptake")
        elif moisture > 60:
            reasoning.append("High soil moisture - slow-release fertilizers recommended")
        
        # Soil type consideration
        if soil_type:
            if soil_type.lower() == 'sandy':
                reasoning.append("Sandy soil - frequent, smaller fertilizer applications recommended")
            elif soil_type.lower() == 'clayey':
                reasoning.append("Clayey soil - ensure good drainage for optimal nutrient uptake")
        
        # If no specific reasoning generated, add general statement
        if not reasoning:
            reasoning.append("Fertilizer recommendation based on soil nutrient analysis and crop requirements")
        
        return reasoning
    
    def _generate_application_tips(self, fertilizer, crop):
        """Generate specific application tips based on fertilizer and crop."""
        tips = []
        name = fertilizer.lower()
        
        if 'urea' in name:
            tips.append("Apply urea when soil is moist, preferably just before irrigation.")
            tips.append("Incorporate into soil within 24 hours to minimize nitrogen loss to atmosphere.")
        elif 'dap' in name:
            tips.append("Apply DAP at the time of sowing for better root development.")
            tips.append("Avoid contact between DAP and seeds; keep a 2-3 inch distance.")
        elif 'mop' in name:
            tips.append("MOP (Potash) should be applied in split doses for better efficacy.")
            tips.append("Effective for improving fruit quality and stress tolerance.")
        elif 'npk' in name:
            tips.append("NPK fertilizers work best when applied in the root zone.")
            tips.append("Standard application: half during sowing, remaining after 30-40 days.")
            
        # General crop tips
        if crop and crop.lower() in ['rice', 'paddy']:
            tips.append("For Paddy, apply fertilizers in standing water (shallow depth).")
        
        # Default tips if none generated
        if not tips:
            tips.append("Apply during early morning or late evening.")
            tips.append("Ensure uniform distribution across the field.")
            
        return tips

    def _rule_based_fallback(self, n, p, k, crop_type=None, lang='en'):
        """
        Fallback to simple rule-based recommendation if ML model fails.
        """
        recommendations = []
        fertilizer = "Balanced NPK"
        
        # Priority 1: Heavy deficiencies
        if n < 30:
            fertilizer = "Urea"
        elif p < 20:
            fertilizer = "DAP"
        elif k < 20:
            fertilizer = "MOP"
        
        # Priority 2: Crop specific adjustment if nutrients are borderline
        if 30 <= n <= 60:
            if crop_type and crop_type.lower() in ['rice', 'paddy', 'sugarcane']:
                fertilizer = "Urea (High N Required)"
            elif crop_type and crop_type.lower() in ['wheat', 'maize', 'millets']:
                fertilizer = "28-28-0 (Ammonium Phosphate)"
        
        # Generate custom reasoning
        reasoning = self._generate_reasoning(fertilizer, crop_type, n, p, k, 25, 60, 45, None)
            
        tips = self._generate_application_tips(fertilizer, crop_type)
        
        # Translate
        from backend.utils.translator import translate_text
        trans_fertilizer = translate_text(fertilizer, lang)
        trans_reasoning = [translate_text(r, lang) for r in reasoning]
        trans_tips = [translate_text(t, lang) for t in tips]
        
        return {
            'fertilizer': fertilizer,
            'translated_fertilizer': trans_fertilizer,
            'confidence': 0.75,
            'reasoning': trans_reasoning,
            'application_tips': trans_tips
        }

