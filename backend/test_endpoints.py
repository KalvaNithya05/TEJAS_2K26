import requests
import json

URL_BASE = "http://localhost:5000/api/sensor"

print("Checking Local Backend Endpoints (Port 5000)...")

try:
    print("\n1. Testing /api/sensor/latest:")
    r = requests.get(f"{URL_BASE}/latest", timeout=5)
    print(f"Status: {r.status_code}")
    print(f"Response: {json.dumps(r.json(), indent=2)}")
except Exception as e:
    print(f"Error testing latest: {e}")

try:
    print("\n2. Testing /api/sensor/history:")
    r = requests.get(f"{URL_BASE}/history", timeout=5)
    print(f"Status: {r.status_code}")
    # Print first item only if list
    data = r.json()
    if isinstance(data, list) and len(data) > 0:
        print(f"Rows found: {len(data)}")
        print(f"First row: {json.dumps(data[0], indent=2)}")
    else:
        print(f"Response: {data}")
except Exception as e:
    print(f"Error testing history: {e}")
