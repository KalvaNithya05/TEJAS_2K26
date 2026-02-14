import requests
import json
import sys

BASE_URL = "http://localhost:5000/api"

def test_recommendation_count():
    with open("test_results_recomm.txt", "w", encoding='utf-8') as f:
        f.write("Testing Recommendation Count (Expect 5)...\n")
        
        payload = {
            "N": 50, "P": 40, "K": 30,
            "temperature": 25, "humidity": 60,
            "ph": 6.5, "rainfall": 100,
            "state": "Telangana",
            "season": "Kharif",
            "crop_type": "agriculture" 
        }
        
        try:
            resp = requests.post(f"{BASE_URL}/predict/recommend", json=payload)
            f.write(f"Status: {resp.status_code}\n")
            if resp.status_code == 200:
                data = resp.json()
                recs = data.get('recommendations', [])
                count = len(recs)
                f.write(f"Recommendation Count: {count}\n")
                f.write(json.dumps(recs, indent=2) + "\n")
                
                if count >= 3:
                    f.write("PASS: Received at least 3 recommendations.\n")
                else:
                    f.write("FAIL: Received fewer than 3 recommendations.\n")
            else:
                f.write(f"Error: {resp.text}\n")
                
        except Exception as e:
            f.write(f"Exception: {e}\n")

if __name__ == "__main__":
    test_recommendation_count()
