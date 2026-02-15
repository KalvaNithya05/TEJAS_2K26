import requests
import json

url = "http://localhost:5000/api/recovery/predict"

payload = {
    "N": 45,
    "P": 50,
    "K": 50,
    "ph": 6.5,
    "moisture": 85,
    "temperature": 25,
    "humidity": 80,
    "rainfall": 200,
    "damage_type": "Pest Attack",
    "damage_percentage": 40,
    "growth_stage": 3,
    "days_remaining": 50
}

try:
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print("Success!")
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

except Exception as e:
    print(f"Request failed: {e}")

payload_override = {
    "N": 45,
    "P": 50,
    "K": 50,
    "ph": 6.5,
    "moisture": 85,
    "temperature": 25,
    "humidity": 80,
    "rainfall": 200,
    "damage_type": "Flood",
    "damage_percentage": 85,
    "growth_stage": 3,
    "days_remaining": 30
}
print("\nTesting Override Logic:")
try:
    response = requests.post(url, json=payload_override)
    if response.status_code == 200:
        print("Success!")
        data = response.json()
        print(f"Decision: {data['decision']}")
        print(f"Reason: {data['reason']}")
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
except Exception as e:
    print(f"Request failed: {e}")
