import os
import sys
import numpy as np

# Add project root and backend to path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.append(project_root)
if current_dir not in sys.path:
    sys.path.append(current_dir)

try:
    from ml.predictor import CropPredictor
except ImportError:
    from backend.ml.predictor import CropPredictor

def demo_predictions():
    predictor = CropPredictor()
    
    # Sample Test Cases: [N, P, K, Temp, Humidity, pH, Rainfall]
    test_cases = [
        {
            "name": "High Rainfall (Rice-friendly)",
            "features": [90, 42, 43, 20.9, 82.0, 6.5, 202.9]
        },
        {
            "name": "Arid/Low Rainfall (Mothbeans-friendly)",
            "features": [20, 40, 20, 28.5, 50.0, 7.5, 45.0]
        },
        {
            "name": "High Potassium (Grape/Banana friendly)",
            "features": [100, 80, 200, 25.0, 75.0, 6.0, 100.0]
        }
    ]
    
    print("="*60)
    print("NEWLY TRAINED CROP PREDICTOR DEMONSTRATION")
    print("="*60)
    
    for case in test_cases:
        print(f"\nScenario: {case['name']}")
        print(f"Inputs: {case['features']}")
        
        results = predictor.predict(case['features'], top_n=3)
        
        if not results:
            print("Prediction failed.")
            continue
            
        for i, res in enumerate(results):
            print(f"  Result {i+1}: {res['crop']} ({res['confidence']*100:.1f}% confidence)")
            print(f"  Reasoning: {' '.join(res['reasoning'])}")
    
    print("\n" + "="*60)

if __name__ == "__main__":
    demo_predictions()
