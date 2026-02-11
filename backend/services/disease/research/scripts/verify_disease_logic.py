import requests
import os
import io

# URL for the disease prediction API
URL = "http://localhost:5000/api/disease/predict"

def test_single_image():
    print("\n--- Testing Single Image ---")
    # Using a dummy image (just a small png)
    img_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDATx\x9cc\xf8\xff\xff?\x00\x05\xfe\x02\xfe\xdcD\x05\xe8\x00\x00\x00\x00IEND\xaeB`\x82'
    files = [('images', ('test.png', io.BytesIO(img_data), 'image/png'))]
    
    response = requests.post(URL, files=files)
    print(f"Status: {response.status_code}")
    print(response.json())

def test_multiple_images():
    print("\n--- Testing Multiple Images (Aggregation) ---")
    img_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDATx\x9cc\xf8\xff\xff?\x00\x05\xfe\x02\xfe\xdcD\x05\xe8\x00\x00\x00\x00IEND\xaeB`\x82'
    
    # Send 3 copies to trigger majority voting (though mock is random, this verifies the flow)
    files = [
        ('images', ('test1.png', io.BytesIO(img_data), 'image/png')),
        ('images', ('test2.png', io.BytesIO(img_data), 'image/png')),
        ('images', ('test3.png', io.BytesIO(img_data), 'image/png'))
    ]
    
    response = requests.post(URL, files=files)
    print(f"Status: {response.status_code}")
    print(response.json())

if __name__ == "__main__":
    try:
        test_single_image()
        test_multiple_images()
    except Exception as e:
        print(f"Error: {e}")
