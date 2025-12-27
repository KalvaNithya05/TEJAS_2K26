import sys
import json
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
sys.path.append(project_root)
sys.path.append(current_dir)
from fertilizer_recommender import FertilizerRecommender

def main():
    try:
        # Args: temp, hum, moisture, soil_type, crop_type, N, K, P, lang
        if len(sys.argv) < 9:
            print(json.dumps({"error": "Not enough arguments"}))
            return

        temp = float(sys.argv[1])
        hum = float(sys.argv[2])
        moist = float(sys.argv[3])
        soil = sys.argv[4]
        crop = sys.argv[5]
        n = float(sys.argv[6])
        k = float(sys.argv[7])
        p = float(sys.argv[8])
        
        lang = 'en'
        if len(sys.argv) > 9:
            lang = sys.argv[9]
            
        recommender = FertilizerRecommender()
        result = recommender.recommend(temp, hum, moist, soil, crop, n, k, p, lang)
        
        print(json.dumps(result))
        
    except Exception as e:
        print(json.dumps({"error": str(e)}))

if __name__ == "__main__":
    main()
