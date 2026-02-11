import requests
import json
import os
import io
from PIL import Image

# Define URL
url = 'http://localhost:5000/api/disease/predict'

# Create a dummy image for testing
def create_dummy_image():
    img = Image.new('RGB', (224, 224), color = 'green')
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='JPEG')
    img_byte_arr.seek(0)
    return img_byte_arr

try:
    print(f"Sending request to: {url}")
    
    # Create dummy file
    img_data = create_dummy_image()
    files = {'image': ('test_leaf.jpg', img_data, 'image/jpeg')}
    
    response = requests.post(url, files=files, timeout=10)
    
    if response.status_code == 200:
        res = response.json()
        print("\n[PASS] API Call Successful")
        print(f"Predicted Class: {res.get('class')}")
        print(f"Confidence: {res.get('confidence')}")
        print(f"Remedy: {res.get('remedy')}")
        
        if res.get('class') and res.get('remedy'):
             print("[PASS] Result structure valid")
        else:
             print("[FAIL] Missing keys in response")
             
    else:
        print(f"[FAIL] Request failed with status: {response.status_code}")
        print(response.text)

except Exception as e:
    print(f"Error connecting to backend: {e}")
    print("Is the backend running?")
