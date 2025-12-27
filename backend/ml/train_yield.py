import pandas as pd
import numpy as np
import pickle
import os
import sys
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import LabelEncoder, StandardScaler

# Adjust path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from crop_yield_handler import CropYieldHandler

def train_yield_model():
    print("Loading yield data...")
    handler = CropYieldHandler()
    df = handler.load_data()
    
    if df is None or df.empty:
        print("No data available for training.")
        return

    # Features and Target
    # Target: Yield
    # Features: State, District, Crop, Season, Annual_Rainfall, Fertilizer, Pesticide, Soil_Type (if available)
    
    # Check available columns
    required_features = ['State', 'District', 'Crop', 'Season', 'Annual_Rainfall', 'Fertilizer', 'Pesticide']
    target_col = 'Yield'
    
    # Handle optional Soil_Type
    if 'Soil_Type' in df.columns:
        required_features.append('Soil_Type')
    
    # Filter
    df = df[required_features + [target_col]].dropna()
    
    X = df[required_features]
    y = df[target_col]
    
    # Encoders dict
    encoders = {}
    
    # Encode Categorical
    categorical_cols = ['State', 'District', 'Crop', 'Season']
    if 'Soil_Type' in X.columns:
        categorical_cols.append('Soil_Type')
        
    for col in categorical_cols:
        le = LabelEncoder()
        X[col] = le.fit_transform(X[col].astype(str))
        encoders[col] = le
        
    # Scale Numerical
    # Numerical cols: Annual_Rainfall, Fertilizer, Pesticide
    # Note: LabelEncoded cols are categorical but RF handles them okay as ordinal usually, 
    # but OneHot is better. For simplicity and RF robustness, LabelEncoding is often acceptable for high cardinality like District.
    
    numerical_cols = ['Annual_Rainfall', 'Fertilizer', 'Pesticide']
    scaler = StandardScaler()
    X[numerical_cols] = scaler.fit_transform(X[numerical_cols])
    
    # Train Test Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    print("Training Random Forest Regressor...")
    model.fit(X_train, y_train)
    
    # Evaluate
    predictions = model.predict(X_test)
    mse = mean_squared_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)
    
    print(f"Model MSE: {mse:.4f}")
    print(f"Model R2 Score: {r2:.4f}")
    
    with open("model_test_results.txt", "a") as log:
        log.write(f"\n[Yield Prediction] Random Forest Regressor - MSE: {mse:.4f}, R2 Score: {r2:.4f}\n")
    
    # Save
    current_dir = os.path.dirname(os.path.abspath(__file__))
    model_dir = os.path.join(os.path.dirname(current_dir), 'models')
    
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)
        
    # Standardize filenames
    model_path = os.path.join(model_dir, 'yield_model.pkl')
    scaler_path = os.path.join(model_dir, 'yield_scaler.pkl')
    encoders_path = os.path.join(model_dir, 'yield_encoders.pkl')
    
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
        
    with open(scaler_path, 'wb') as f:
        pickle.dump(scaler, f)
        
    with open(encoders_path, 'wb') as f:
        pickle.dump(encoders, f)
        
    print(f"Yield model saved to {model_path}")

if __name__ == "__main__":
    train_yield_model()
