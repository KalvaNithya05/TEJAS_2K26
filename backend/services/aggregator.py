from dotenv import load_dotenv
import os
import requests
import pandas as pd

# Try to load if not already loaded (e.g. in test scripts)
env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
load_dotenv(env_path)

THING_SPEAK_CHANNEL_ID = os.getenv("THINGSPEAK_CHANNEL_ID")
THING_SPEAK_READ_KEY = os.getenv("THINGSPEAK_READ_KEY")

def get_aggregated_data(results=30):
    """
    Fetches the last N results from ThingSpeak and return averaged values.
    Standardizes fields for both crop predictor and recovery model.
    """
    if not THING_SPEAK_CHANNEL_ID or not THING_SPEAK_READ_KEY:
        print(f"DEBUG: Missing THING_SPEAK_CHANNEL_ID({THING_SPEAK_CHANNEL_ID}) or THING_SPEAK_READ_KEY")
        return None

    url = (
        f"https://api.thingspeak.com/channels/"
        f"{THING_SPEAK_CHANNEL_ID.strip()}/feeds.json"
        f"?api_key={THING_SPEAK_READ_KEY.strip()}&results={results}"
    )
    print(f"DEBUG: Fetching aggregator data from ThingSpeak: {url.replace(THING_SPEAK_READ_KEY.strip(), '***')}")

    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        data = response.json()
        feeds = data.get("feeds", [])

        if not feeds:
            return None

        df = pd.DataFrame(feeds)
        
        # ThingSpeak fields mapping:
        # field1: temperature
        # field2: humidity
        # field3: moisture
        # field4: soil_ph
        # field5: nitrogen
        # field6: phosphorus
        # field7: potassium
        
        # Convert to numeric, handle errors
        for i in range(1, 8):
            df[f'field{i}'] = pd.to_numeric(df[f'field{i}'], errors='coerce')

        agg = {
            'temperature': round(df['field1'].mean(), 2),
            'humidity': round(df['field2'].mean(), 2),
            'moisture': round(df['field3'].mean(), 2),
            'ph': round(df['field4'].mean(), 2),
            'N': round(df['field5'].mean(), 2),
            'P': round(df['field6'].mean(), 2),
            'K': round(df['field7'].mean(), 2),
            'rainfall': 100.0 # Default if not in TS
        }
        
        # also include original names for compatibility
        agg['soil_ph'] = agg['ph']
        agg['nitrogen'] = agg['N']
        agg['phosphorus'] = agg['P']
        agg['potassium'] = agg['K']
        
        return agg

    except Exception as e:
        print(f"Aggregator Error (ThingSpeak): {e}")
        import traceback
        traceback.print_exc()
        return None
