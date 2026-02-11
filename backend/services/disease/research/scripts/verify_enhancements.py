
import requests
import json
import os

BASE_URL = "http://localhost:5000/api"

def test_chained_recommendations():
    print("\n--- Testing Chained Recommendations ---")
    payload = {
        "N": 90, "P": 42, "K": 43, 
        "temperature": 20.8, "humidity": 82, "ph": 6.5, "rainfall": 202,
        "state": "Andhra Pradesh", "season": "Kharif", "lang": "te"
    }
    try:
        response = requests.post(f"{BASE_URL}/predict/recommend", json=payload)
        data = response.json()
        if data.get('status') == 'success':
            recs = data.get('recommendations', [])
            print(f"Success! Received {len(recs)} recommendations.")
            for i, r in enumerate(recs):
                crop = r['crop']
                fert = r['fertilizer']
                y = r['yield']
                print(f"Rec {i+1}: {crop['translated_crop']} (Conf: {crop['confidence']})")
                print(f"  Fert: {fert['translated_name']} (Reasoning: {len(fert['reasoning'])} items)")
                print(f"  Yield: {y['predicted_yield']} {y['unit']}")
        else:
            print("Failed:", data)
    except Exception as e:
        print("Error:", e)

def test_multi_image_disease():
    print("\n--- Testing Multi-Image Disease Detection ---")
    # This assumes mock_leaf.jpg exists in current dir or we'll just mock it if needed
    # For verification, we'll try to find any image in the project
    img_path = "backend/models/mock_leaf.jpg" 
    if not os.path.exists(img_path):
        print(f"Warning: {img_path} not found. Test might fail if backend requires real image.")
    
    try:
        # Create a mock upload (multipart/form-data)
        # Using the same image twice to test aggregation
        files = [
            ('images', ('leaf1.jpg', open(img_path, 'rb'), 'image/jpeg')),
            ('images', ('leaf2.jpg', open(img_path, 'rb'), 'image/jpeg'))
        ]
        response = requests.post(f"{BASE_URL}/disease/predict", files=files)
        data = response.json()
        print("Response received.")
        print(f"Consensus Class: {data.get('class')}")
        print(f"Avg Confidence: {data.get('confidence')}")
        print(f"Samples Processed: {data.get('processed_images_count')}")
        print(f"Individual Results: {len(data.get('individual_results', []))}")
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    test_chained_recommendations()
    # Note: test_multi_image_disease depends on a physical file existing at the path
    # test_multi_image_disease() 
