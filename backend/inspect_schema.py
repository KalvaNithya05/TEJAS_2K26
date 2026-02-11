import requests
import json

URL = "https://zwblgqecoumpwkbmmlua.supabase.co/rest/v1/"
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inp3YmxncWVjb3VtcHdrYm1tbHVhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Njk3NDg2NzQsImV4cCI6MjA4NTMyNDY3NH0.-W00jf8MUkND_LtH_jr_O0j5mZk8HtFQ2JvcgLm53mw"

headers = {
    "apikey": KEY,
    "Authorization": f"Bearer {KEY}"
}

print("Fetching ALL Tables and Columns...")
r = requests.get(URL, headers=headers)
if r.status_code == 200:
    spec = r.json()
    definitions = spec.get('definitions', {})
    for table, defn in definitions.items():
        print(f"\nTABLE: {table}")
        props = defn.get('properties', {})
        print(f"COLUMNS: {list(props.keys())}")
else:
    print("Failed")
