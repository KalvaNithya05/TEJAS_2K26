import requests
import json
import sys

# Define URL
url = 'http://localhost:5000/api/predict/recommend'

# Mock Data
data = {
    "N": 90, 
    "P": 42, 
    "K": 43, 
    "temperature": 25, 
    "humidity": 60, 
    "ph": 6.5, 
    "rainfall": 100, 
    "location": "Warangal",
    "lang": "en"
}

try:
    print("Sending request to:", url)
    response = requests.post(url, json=data, timeout=5)
    
    if response.status_code == 200:
        res = response.json()
        print("\n--- API RESPONSE SUCCESS ---")
        
        # Check Crops
        if 'crops' in res and len(res['crops']) > 0:
            print("[PASS] Crops returned")
            print(f"Top Crop: {res['crops'][0]['crop']} (Conf: {res['crops'][0]['confidence']})")
            if 'reasoning' in res['crops'][0]:
                print(f"[PASS] Crop Reasoning present: {res['crops'][0]['reasoning']}")
            else:
                print("[FAIL] Crop Reasoning missing")
        else:
             print("[FAIL] No crops returned")
             
        # Check Fertilizer
        if 'fertilizer_recommendation' in res:
             print("[PASS] Fertilizer returned")
             print(f"Fertilizer: {res['fertilizer_recommendation'].get('fertilizer')}")
        else:
             print("[FAIL] No fertilizer returned")
             
        # Check Yield
        if 'yield_prediction' in res:
             print("[PASS] Yield returned")
             print(f"Yield: {res['yield_prediction'].get('predicted_yield')} {res['yield_prediction'].get('unit')}")
        else:
             print("[FAIL] Yield prediction missing")
             
    else:
        print(f"Request failed with status: {response.status_code}")
        print(response.text)

except Exception as e:
    print(f"Error connecting to backend: {e}")
    print("Ensure the backend server is running on port 5000.")
