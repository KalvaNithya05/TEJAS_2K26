import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import joblib
import os

class RecoveryDecisionModel:
    def __init__(self, model_path='backend/models/recovery_model.pkl'):
        self.model_path = model_path
        self.model = None
        self.le_damage = LabelEncoder()
        self.le_target = LabelEncoder()
        self.decision_labels = [
            "REPLANT_SHORT_DURATION_CROP",
            "CONTINUE_WITH_RECOVERY_PLAN",
            "SOIL_RESTORATION_REQUIRED",
            "FINANCIAL_RELIEF_RECOMMENDED"
        ]
        # damage types for encoding
        self.damage_types = ["Flood", "Drought", "Pest Attack", "Disease", "Nutrient Deficiency", "Wind Damage"]
        self.le_damage.fit(self.damage_types)
        self.le_target.fit(self.decision_labels)

        self._load_or_train()

    def _generate_synthetic_data(self, n_samples=1000):
        # Generate synthetic data based on logical rules to bootstrap the model
        data = []
        for _ in range(n_samples):
            damage_pct = np.random.randint(0, 101)
            days_rem = np.random.randint(0, 120)
            soil_n = np.random.randint(20, 150)
            damage_type = np.random.choice(self.damage_types)
            
            # Logic for labelling (imitating expert knowledge)
            if damage_pct > 70 and days_rem < 45:
                decision = "FINANCIAL_RELIEF_RECOMMENDED"
            elif damage_pct > 50 and days_rem > 60:
                decision = "REPLANT_SHORT_DURATION_CROP"
            elif soil_n < 40 or damage_type == "Nutrient Deficiency":
                decision = "SOIL_RESTORATION_REQUIRED"
            else:
                decision = "CONTINUE_WITH_RECOVERY_PLAN"
                
            data.append([
                soil_n, 
                np.random.randint(20, 80), # P
                np.random.randint(20, 80), # K
                np.random.uniform(5.5, 8.5), # pH
                np.random.uniform(20, 90), # Moisture
                np.random.uniform(15, 35), # Temp
                np.random.uniform(30, 90), # Humidity
                np.random.uniform(0, 300), # Rainfall
                damage_type,
                damage_pct,
                np.random.randint(1, 5), # Growth Stage
                days_rem,
                decision
            ])
            
        columns = [
            'N', 'P', 'K', 'ph', 'moisture', 'temperature', 'humidity', 'rainfall',
            'damage_type', 'damage_percentage', 'growth_stage', 'days_remaining', 'decision'
        ]
        return pd.DataFrame(data, columns=columns)

    def _load_or_train(self):
        if os.path.exists(self.model_path):
            try:
                self.model = joblib.load(self.model_path)
                print("Recovery Model loaded from disk.")
            except Exception as e:
                print(f"Error loading model: {e}. Retraining...")
                self.train_new_model()
        else:
            print("Model not found. Training new model...")
            self.train_new_model()

    def train_new_model(self):
        df = self._generate_synthetic_data(2000)
        
        X = df.drop('decision', axis=1)
        y = df['decision']
        
        # Encode categorical features
        X['damage_type'] = self.le_damage.transform(X['damage_type'])
        y_encoded = self.le_target.transform(y)
        
        X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)
        
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.model.fit(X_train, y_train)
        
        # Save model
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        joblib.dump(self.model, self.model_path)
        print(f"Model trained and saved to {self.model_path}")

    def predict(self, features):
        """
        features: dict containing 'N', 'P', 'K', 'ph', 'moisture', 'temperature', 
                  'humidity', 'rainfall', 'damage_type', 'damage_percentage', 
                  'growth_stage', 'days_remaining'
        """
        if not self.model:
            self._load_or_train()
            
        # Prepare input dataframe with strict feature selection and ordering
        expected_features = [
            'N', 'P', 'K', 'ph', 'moisture', 'temperature', 'humidity', 'rainfall',
            'damage_type', 'damage_percentage', 'growth_stage', 'days_remaining'
        ]
        
        # Extract only expected features
        filtered_features = {k: features.get(k, 0) for k in expected_features}
        input_df = pd.DataFrame([filtered_features])[expected_features]
        
        # Validate/clean damage_type
        if filtered_features['damage_type'] not in self.damage_types:
            input_df.at[0, 'damage_type'] = self.damage_types[0] 
            
        input_df['damage_type'] = self.le_damage.transform(input_df['damage_type'])
        
        prediction_idx = self.model.predict(input_df)[0]
        probabilities = self.model.predict_proba(input_df)[0]
        
        predicted_class = self.le_target.inverse_transform([prediction_idx])[0]
        
        # Feature Importance
        importances = self.model.feature_importances_
        feature_names = input_df.columns
        feature_imp_dict = dict(zip(feature_names, importances))
        
        return {
            "prediction": predicted_class,
            "confidence": float(max(probabilities)),
            "probabilities": {cls: float(prob) for cls, prob in zip(self.decision_labels, probabilities)},
            "feature_importance": feature_imp_dict
        }
