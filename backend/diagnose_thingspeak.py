import os
import requests
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

def test_thingspeak():
    print("--- ThingSpeak Connectivity Diagnostic ---")
    
    read_key = os.getenv("THINGSPEAK_READ_KEY")
    channel_id = os.getenv("THINGSPEAK_CHANNEL_ID")
    
    print(f"Checking credentials for Channel ID: {channel_id}")
    
    if not read_key or not channel_id:
        print("ERROR: THINGSPEAK_READ_KEY or THINGSPEAK_CHANNEL_ID not found in .env file.")
        return

    url = f"https://api.thingspeak.com/channels/{channel_id}/feeds/last.json?api_key={read_key}"
    print(f"Requesting URL: {url.replace(read_key, '********')}")
    
    try:
        response = requests.get(url, timeout=15)
        print(f"HTTP Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("\nSUCCESS: Connected to ThingSpeak!")
            print(f"Latest Entry ID: {data.get('entry_id')}")
            print(f"Created At: {data.get('created_at')}")
            
            print("\nField Data:")
            for i in range(1, 9):
                field_name = f'field{i}'
                val = data.get(field_name)
                if val:
                    print(f" - {field_name}: {val}")
        elif response.status_code == 404:
            print("ERROR: Channel not found. Please check your Channel ID.")
        elif response.status_code == 403:
            print("ERROR: Authentication failed. Please check your Read API Key.")
        else:
            print(f"ERROR: Received unexpected response: {response.text}")
            
    except Exception as e:
        print(f"ERROR: Network or request error occurred: {e}")

if __name__ == "__main__":
    test_thingspeak()
