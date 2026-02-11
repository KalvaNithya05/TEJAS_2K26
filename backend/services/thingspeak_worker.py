import os
import requests
import time
from datetime import datetime
from config.supabase_client import supabase

def fetch_thingspeak_data():
    read_key = os.getenv("THINGSPEAK_READ_KEY")
    channel_id = os.getenv("THINGSPEAK_CHANNEL_ID")
    
    if not read_key or not channel_id:
        # print("ThingSpeak Read Key or Channel ID missing. Skipping background ingestion.")
        return None

    url = f"https://api.thingspeak.com/channels/{channel_id}/feeds/last.json?api_key={read_key}"
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"ThingSpeak Fetch error: {e}")
    return None

def run_thingspeak_ingestion():
    """
    Background worker that polls ThingSpeak every 15 seconds 
    and syncs the latest data to Supabase if it's new.
    """
    last_entry_id = None
    
    while True:
        data = fetch_thingspeak_data()
        
        if data and data.get('entry_id') != last_entry_id:
            last_entry_id = data.get('entry_id')
            
            # Map ThingSpeak fields (Field1, Field2, etc.) to Supabase schema
            # Assuming standard mapping or using metadata if available
            record = {
                'device_id': 'TS_STATION_01',
                'temperature': float(data.get('field1', 0)),
                'humidity': float(data.get('field2', 0)),
                'moisture': float(data.get('field3', 0)),
                'soil_ph': float(data.get('field4', 0)),
                'nitrogen': float(data.get('field5', 0)),
                'phosphorus': float(data.get('field6', 0)),
                'potassium': float(data.get('field7', 0)),
                'timestamp': data.get('created_at', datetime.now().isoformat())
            }
            
            try:
                if supabase:
                    supabase.table('sensor_readings').insert(record).execute()
                    print(f"ThingSpeak synced entry {last_entry_id} to Supabase")
            except Exception as e:
                print(f"Sync error: {e}")

        time.sleep(15)
