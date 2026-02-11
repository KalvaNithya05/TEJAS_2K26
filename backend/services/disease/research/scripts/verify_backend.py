import requests
import json
import sys

# Define URL
url = 'http://localhost:5000/api/predict/recommend'

# Base Data
base_data = {
    "N": 90, 
    "P": 42, 
    "K": 43, 
    "temperature": 25, 
    "humidity": 60, 
    "ph": 6.5, 
    "rainfall": 100, 
    "location": "Warangal",
    "season": "Rabi",
    "lang": "en"
}

# Test Cases
test_types = [None, 'agriculture', 'horticulture']

for c_type in test_types:
    print(f"\n==========================================")
    print(f"Testing Crop Type: {c_type if c_type else 'ALL'}")
    print(f"==========================================")
    
    payload = base_data.copy()
    if c_type:
        payload['crop_type'] = c_type
        
    try:
        response = requests.post(url, json=payload, timeout=5)
        
        if response.status_code == 200:
            res = response.json()
            
            # Check Crops
            if 'crops' in res and len(res['crops']) > 0:
                print(f"[PASS] Returned {len(res['crops'])} crops")
                for i, c in enumerate(res['crops']):
                    print(f" {i+1}. {c['crop']} ({c['confidence']})")
            else:
                 print("[FAIL] No crops returned")
                 
        else:
            print(f"Request failed with status: {response.status_code}")
            print(response.text)
    
    except Exception as e:
        print(f"Error connecting to backend: {e}")
