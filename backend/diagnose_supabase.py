import os
import requests
from dotenv import load_dotenv

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

if not url.endswith('/'):
    url += '/'

tables = ['sensor_readings', 'soil_data']

print(f"Testing URL: {url}")
print(f"Testing Key: {key[:15]}...")

headers = {
    "apikey": key,
    "Authorization": f"Bearer {key}"
}

for t in tables:
    try:
        test_url = f"{url}rest/v1/{t}?select=*"
        print(f"Checking table: {t}")
        r = requests.get(test_url, headers=headers, params={'limit': 1}, timeout=10)
        
        if r.status_code == 200:
            print(f"  ✅ SUCCESS: '{t}' is accessible. Rows: {len(r.json())}")
            if len(r.json()) > 0:
                print(f"  Sample Data: {r.json()[0]}")
        else:
            print(f"  ❌ FAILED: '{t}' (Status {r.status_code})")
            print(f"  Response: {r.text}")
    except Exception as e:
        print(f"  💥 ERROR: {e}")
