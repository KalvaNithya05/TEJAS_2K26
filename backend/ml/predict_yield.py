import sys
import json
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
sys.path.append(project_root)
sys.path.append(current_dir)
from yield_predictor import YieldPredictor

def main():
    try:
        if len(sys.argv) < 8:
            print(json.dumps({"error": "Not enough arguments"}))
            return

        # Args: state, district, crop, season, rain, fert, pest, lang
        state = sys.argv[1]
        district = sys.argv[2]
        crop = sys.argv[3]
        season = sys.argv[4]
        # Skip soil_type for now unless passed? Assume passed or optional.
        # Let's align with what frontend sends. 
        # Frontend usually sends: State, District, Crop, Season...
        # Let's assume args order matches what we call from Node.
        
        rainfall = float(sys.argv[5])
        fertilizer = float(sys.argv[6])
        pesticide = float(sys.argv[7])
        
        # Language might be last arg?
        lang = 'en'
        if len(sys.argv) > 8:
            lang = sys.argv[8]

        predictor = YieldPredictor()
        
        # Note: soil_type is missing in args here but predictor uses it.
        # We can default it or pass it if frontend has it.
        # For Minimum Viable, pass None.
        
        result = predictor.predict(state, district, crop, season, rainfall, fertilizer, pesticide) # soil_type=None
        
        # Translate keys or result if needed? 
        # Typically yield is a number. 
        # Maybe return explanation string in lang?
        
        output = {
            "predicted_yield": result,
            "unit": "tons/hectare"
        }
        
        print(json.dumps(output))
        
    except Exception as e:
        print(json.dumps({"error": str(e)}))

if __name__ == "__main__":
    main()
