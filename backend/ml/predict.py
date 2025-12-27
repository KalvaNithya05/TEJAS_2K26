import sys
import json
import os

# Adjust path to find modules
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
sys.path.append(project_root)
sys.path.append(current_dir)

from predictor import CropPredictor

def main():
    try:
        # Read args: N, P, K, pH, Temp, Hum, Rain
        if len(sys.argv) < 8:
            # Fallback/Debug
            print(json.dumps(["Error: Not enough arguments"]))
            return

        # Parse arguments
        features = [
            float(sys.argv[1]), # N
            float(sys.argv[2]), # P
            float(sys.argv[3]), # K
            float(sys.argv[4]), # pH -> This might need re-ordering if predictor expects Temp first
            float(sys.argv[5]), # Temp
            float(sys.argv[6]), # Humidity
            float(sys.argv[7])  # Rainfall
        ]
        
        # Check predictor expectation in predictor.py:
        # docstring says: [N, P, K, Temp, Hum, pH, Rain]
        # logic says: data.get("N"), ...
        # But `predict` method takes `features` array.
        # Let's align with predictor.py's `preprocess` method order if used, or just pass as array.
        # Predictor logic (Step 30/31) `DataPreprocessor.preprocess` expects dict but returns array [N, P, K, Temp, Hum, ph, Rain].
        # So order is N, P, K, Temp, Hum, pH, Rain.
        
        # Adjust input order from argv if needed.
        # argv: N, P, K, pH, Temp, Hum, Rain (from mlService.js)
        # N=1, P=2, K=3, pH=4, Temp=5, Hum=6, Rain=7
        
        # Target order: N, P, K, Temp, Hum, pH, Rain
        ordered_features = [
            features[0], # N
            features[1], # P
            features[2], # K
            features[4], # Temp
            features[5], # Humidity
            features[3], # pH
            features[6]  # Rainfall
        ]
        
        # Language arg
        lang = 'en'
        if len(sys.argv) > 8:
            lang = sys.argv[8]
        
        predictor = CropPredictor()
        
        # Get top 3
        results_dicts = predictor.predict(ordered_features, top_n=3, lang=lang)
        
        print(json.dumps(results_dicts))
        
    except Exception as e:
        # print(f"Error: {e}", file=sys.stderr)
        print(json.dumps([f"Error: {str(e)}"]))

if __name__ == "__main__":
    main()
