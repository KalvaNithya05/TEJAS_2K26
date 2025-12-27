import pickle
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import LabelEncoder, StandardScaler

def test_fertilizer_model():
    """
    Test the trained fertilizer model to verify accuracy.
    """
    print("="*60)
    print("FERTILIZER MODEL VERIFICATION")
    print("="*60)
    
    # Load the dataset
    print("\nLoading dataset...")
    df = pd.read_csv('data/Fertilizer Prediction.csv')
    df.columns = df.columns.str.strip()
    df = df.dropna()
    
    print(f"Dataset: {df.shape[0]} rows, {df.shape[1]} columns")
    
    # Preprocess (same as training)
    X = df.drop('Fertilizer Name', axis=1)
    y = df['Fertilizer Name']
    
    # Encode categorical variables
    soil_encoder = LabelEncoder()
    X['Soil Type'] = soil_encoder.fit_transform(X['Soil Type'])
    
    crop_encoder = LabelEncoder()
    X['Crop Type'] = crop_encoder.fit_transform(X['Crop Type'])
    
    fertilizer_encoder = LabelEncoder()
    y_encoded = fertilizer_encoder.fit_transform(y)
    
    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Split data (same split as training)
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y_encoded,
        test_size=0.2,
        random_state=42,
        stratify=y_encoded
    )
    
    print(f"Test set size: {len(X_test)} samples")
    
    # Load the trained model
    print("\nLoading trained model...")
    with open('backend/models/fertilizer_model.pkl', 'rb') as f:
        model = pickle.load(f)
    
    with open('backend/models/fertilizer_metadata.pkl', 'rb') as f:
        metadata = pickle.load(f)
    
    print(f"Model type: {metadata['model_type']}")
    print(f"Fertilizer types: {metadata['fertilizer_types']}")
    
    # Make predictions
    print("\nMaking predictions on test set...")
    y_pred = model.predict(X_test)
    
    # Calculate accuracy
    accuracy = accuracy_score(y_test, y_pred)
    
    print("\n" + "="*60)
    print("MODEL PERFORMANCE")
    print("="*60)
    print(f"\nTest Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
    
    # Check if accuracy is in acceptable range
    if accuracy > 0.95:
        print("⚠ WARNING: Accuracy > 95% - Possible overfitting")
    elif accuracy < 0.85:
        print("⚠ WARNING: Accuracy < 85% - Possible underfitting")
    else:
        print("✓ Accuracy is within acceptable range (85-95%)")
    
    # Get probability predictions
    if hasattr(model, 'predict_proba'):
        y_proba = model.predict_proba(X_test)
        max_confidences = np.max(y_proba, axis=1)
        avg_confidence = np.mean(max_confidences)
        
        print(f"\nAverage confidence: {avg_confidence:.4f} ({avg_confidence*100:.2f}%)")
        print(f"Min confidence: {np.min(max_confidences):.4f} ({np.min(max_confidences)*100:.2f}%)")
        print(f"Max confidence: {np.max(max_confidences):.4f} ({np.max(max_confidences)*100:.2f}%)")
        
        # Check for 100% confidence predictions
        perfect_confidence = np.sum(max_confidences == 1.0)
        if perfect_confidence > 0:
            print(f"\n⚠ WARNING: {perfect_confidence} predictions have 100% confidence")
        else:
            print("\n✓ No predictions have 100% confidence")
    
    # Detailed classification report
    print("\n" + "="*60)
    print("CLASSIFICATION REPORT")
    print("="*60)
    print(classification_report(y_test, y_pred, target_names=fertilizer_encoder.classes_))
    
    # Test with sample prediction
    print("\n" + "="*60)
    print("SAMPLE PREDICTION TEST")
    print("="*60)
    
    # Get first test sample
    sample_idx = 0
    sample = X_test[sample_idx].reshape(1, -1)
    
    prediction = model.predict(sample)[0]
    predicted_fertilizer = fertilizer_encoder.inverse_transform([prediction])[0]
    actual_fertilizer = fertilizer_encoder.inverse_transform([y_test[sample_idx]])[0]
    
    if hasattr(model, 'predict_proba'):
        proba = model.predict_proba(sample)[0]
        confidence = np.max(proba)
        print(f"\nSample prediction:")
        print(f"  Predicted: {predicted_fertilizer} (confidence: {confidence:.2f})")
        print(f"  Actual: {actual_fertilizer}")
        print(f"  Match: {'✓' if predicted_fertilizer == actual_fertilizer else '✗'}")
    
    print("\n" + "="*60)
    print("VERIFICATION COMPLETE")
    print("="*60)

if __name__ == "__main__":
    test_fertilizer_model()
