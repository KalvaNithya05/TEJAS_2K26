import requests

URL = "https://zwblgqecoumpwkbmmlua.supabase.co/rest/v1/sensor_readings"
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inp3YmxncWVjb3VtcHdrYm1tbHVhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Njk3NDg2NzQsImV4cCI6MjA4NTMyNDY3NH0.-W00jf8MUkND_LtH_jr_O0j5mZk8HtFQ2JvcgLm53mw"

headers = {
    "apikey": KEY,
    "Authorization": f"Bearer {KEY}",
    "Range": "0-16"
}

print(f"URL: {URL}")
r = requests.get(URL, headers=headers)
print(f"Status: {r.status_code}")
print(f"Body: {r.text}")
