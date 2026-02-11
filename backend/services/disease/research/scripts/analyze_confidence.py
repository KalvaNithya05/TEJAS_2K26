import pickle
import numpy as np
import os
import sys
import pandas as pd
from sklearn.metrics import accuracy_score

# Adjust path to import local modules
sys.path.append(os.path.join(os.getcwd(), 'backend', 'ml'))
from data_handler import DataHandler

def analyze_model():
    model_path = 'backend/models/crop_recommendation_model.pkl'
    le_path = 'backend/models/label_encoder.pkl'
    scaler_path = 'backend/models/scaler.pkl'
    
    if not os.path.exists(model_path):
        print("Model not found.")
        return

    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    with open(le_path, 'rb') as f:
        le = pickle.load(f)
    with open(scaler_path, 'rb') as f:
        scaler = pickle.load(f)

    handler = DataHandler()
    df = handler.load_data()
    X = df.drop('label', axis=1)
    y = df['label']
    
    X_scaled = scaler.transform(X)
    y_encoded = le.transform(y)
    
    # Predict probabilities
    probs = model.predict_proba(X_scaled)
    max_probs = np.max(probs, axis=1)
    
    print("\n[Confidence Score Distribution]")
    print(f"Mean Confidence: {np.mean(max_probs):.4f}")
    print(f"Median Confidence: {np.median(max_probs):.4f}")
    print(f"Min Confidence: {np.min(max_probs):.4f}")
    print(f"Max Confidence: {np.max(max_probs):.4f}")
    
    bins = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    hist, _ = np.histogram(max_probs, bins=bins)
    print("\nHistogram:")
    for i in range(len(hist)):
        print(f"{bins[i]:.1f}-{bins[i+1]:.1f}: {hist[i]}")

    preds = model.predict(X_scaled)
    acc = accuracy_score(y_encoded, preds)
    print(f"\nOverall Accuracy on Full Dataset: {acc:.4f}")

if __name__ == "__main__":
    analyze_model()
