import os
import random
import numpy as np

class DiseasePredictor:
    def __init__(self):
        """
        Initializes the Disease Predictor.
        Loads the model if available, otherwise sets up for mock inference.
        """
        self.model = None
        self.classes = [
            'Apple_scab', 'Apple_Black_rot', 'Apple_Cedar_apple_rust', 'Apple_healthy',
            'Blueberry_healthy',
            'Cherry_Powdery_mildew', 'Cherry_healthy',
            'Corn_Cercospora_leaf_spot_Gray_leaf_spot', 'Corn_Common_rust', 'Corn_Northern_Leaf_Blight', 'Corn_healthy',
            'Grape_Black_rot', 'Grape_Esca_(Black_Measles)', 'Grape_Leaf_blight_(Isariopsis_Leaf_Spot)', 'Grape_healthy',
            'Orange_Haunglongbing_(Citrus_greening)',
            'Peach_Bacterial_spot', 'Peach_healthy',
            'Pepper_bell_Bacterial_spot', 'Pepper_bell_healthy',
            'Potato_Early_blight', 'Potato_Late_blight', 'Potato_healthy',
            'Raspberry_healthy',
            'Soybean_healthy',
            'Squash_Powdery_mildew',
            'Strawberry_Leaf_scorch', 'Strawberry_healthy',
            'Tomato_Bacterial_spot', 'Tomato_Early_blight', 'Tomato_Late_blight', 'Tomato_Leaf_Mold',
            'Tomato_Septoria_leaf_spot', 'Tomato_Spider_mites_Two-spotted_spider_mite', 'Tomato_Target_Spot',
            'Tomato_Yellow_Leaf_Curl_Virus', 'Tomato_mosaic_virus', 'Tomato_healthy'
        ]
        
        # Try to load classes JSON
        current_dir = os.path.dirname(os.path.abspath(__file__))
        classes_path = os.path.join(current_dir, 'models', 'plant_disease_classes.json')
        if os.path.exists(classes_path):
            try:
                import json
                with open(classes_path, 'r') as f:
                    self.classes = json.load(f)
                print(f"Loaded {len(self.classes)} disease classes from JSON.")
            except Exception as e:
                print(f"Error loading classes JSON: {e}")

        # Try to load model
        try:
            import tensorflow as tf
            # Path to backend/models/plant_disease_model.keras
            model_path = os.path.join(current_dir, 'models', 'plant_disease_model.keras')
            
            if os.path.exists(model_path):
                print(f"Loading Disease Module from {model_path}...")
                self.model = tf.keras.models.load_model(model_path)
                print("Disease Module Loaded Successfully.")
            else:
                print("Disease Model not found. Using Mock Mode.")
                
        except ImportError:
            print("TensorFlow not installed. Using Mock Mode.")
        except Exception as e:
            print(f"Error loading Disease Module: {e}. Using Mock Mode.")
            
        if self.model:
            print(f"DEBUG: Model Output Shape: {self.model.output_shape}")
            print(f"DEBUG: Classes count: {len(self.classes)}")

    def predict(self, image_path):
        """
        Predicts disease from image path.
        :param image_path: Path to the uploaded image file.
        :return: Dict {'class': str, 'confidence': float, 'remedy': str}
        """
        if self.model:
            return self._real_predict(image_path)
        else:
            return self._mock_predict(image_path)

    def _real_predict(self, image_path):
        try:
            import tensorflow as tf
            from tensorflow.keras.preprocessing import image
            from tensorflow.keras.applications.efficientnet import preprocess_input
            
            # Load and preprocess image (260x260 for EfficientNetB2)
            img = image.load_img(image_path, target_size=(260, 260))
            img_array = image.img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0)
            
            # Use EfficientNet's official preprocessing
            img_array = preprocess_input(img_array)

            # Inference
            predictions = self.model.predict(img_array, verbose=0)
            predicted_class_idx = np.argmax(predictions[0])
            confidence = float(np.max(predictions[0]))
            predicted_class = self.classes[predicted_class_idx]
            
            return {
                'class': predicted_class,
                'confidence': round(confidence, 2),
                'remedy': self._get_remedy(predicted_class)
            }
        except Exception as e:
            print(f"Inference Error: {e}")
            return self._mock_predict(image_path)

    def _mock_predict(self, image_path):
        """
        Returns a deterministic pseudo-random disease prediction for demonstration.
        The result is tied to the image content via hashing.
        """
        # Simulate processing time
        import time
        import hashlib
        time.sleep(0.5)
        
        # Create a deterministic seed from image content
        try:
            with open(image_path, "rb") as f:
                img_hash = hashlib.sha256(f.read()).hexdigest()
                seed = int(img_hash, 16) % (2**32)
        except Exception:
            seed = 42 # Fallback
            
        rng = random.Random(seed)
        
        predicted_class = rng.choice(self.classes)
        confidence = rng.uniform(0.70, 0.98)
        
        return {
            'class': predicted_class,
            'confidence': round(confidence, 2),
            'remedy': self._get_remedy(predicted_class)
        }

    def _get_remedy(self, disease_name):
        """
        Returns simple remedy text based on disease name.
        """
        if 'healthy' in disease_name.lower():
            return "Plant is healthy. Keep monitoring regularly."
        
        remedies = {
            'scab': "Apply fungicides like Captan or Myclobutanil. Remove infected leaves.",
            'rot': "Remove infected parts. Improve air circulation. Avoid overhead watering.",
            'rust': "Apply sulfur-based fungicides. Remove infected debris.",
            'mildew': "Apply Neem oil or mixture of baking soda and water.",
            'blight': "Apply copper-based fungicides. Crop rotation recommended.",
            'virus': "No cure. Remove and destroy infected plants to prevent spread. Control vector insects.",
            'spot': "Apply copper fungicide. Avoid wetting foliage.",
            'mite': "Apply miticides or Neem oil. Spray water to dislodge mites."
        }
        
        for key, remedy in remedies.items():
            if key in disease_name.lower():
                return remedy
                
        return "Consult a local agricultural expert for specific treatment."
