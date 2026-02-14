import requests
from config.supabase_client import supabase
import os

THING_SPEAK_CHANNEL_ID = os.getenv("THINGSPEAK_CHANNEL_ID")
THING_SPEAK_READ_KEY = os.getenv("THINGSPEAK_READ_KEY")


def fetch_latest_thingspeak_data():
    if not THING_SPEAK_CHANNEL_ID or not THING_SPEAK_READ_KEY:
        print("Missing ThingSpeak Config")
        return None

    url = (
        f"https://api.thingspeak.com/channels/"
        f"{THING_SPEAK_CHANNEL_ID}/feeds.json"
        f"?api_key={THING_SPEAK_READ_KEY}&results=1"
    )

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()
        feeds = data.get("feeds", [])

        if not feeds:
            return None

        return feeds[0]
    except Exception as e:
        print(f"Error fetching from ThingSpeak: {e}")
        return None


def store_in_supabase(feed):
    if not supabase:
        return

    payload = {
        "device_id": os.getenv("DEVICE_ID", "MM-POLE-001"),
        "temperature": float(feed.get("field1") or 0),
        "humidity": float(feed.get("field2") or 0),
        "moisture": float(feed.get("field3") or 0),
        "soil_ph": float(feed.get("field4") or 0),
        "nitrogen": float(feed.get("field5") or 0),
        "phosphorus": float(feed.get("field6") or 0),
        "potassium": float(feed.get("field7") or 0),
        "latitude": None,
        "longitude": None
        # ❌ DO NOT send created_at? User said do not send. 
        # But Supabase usually needs created_at to match source time?
        # If we omit it, Supabase uses insertion time.
        # User code omitted it. I will follow user code.
    }

    try:
        supabase.table("sensor_readings").insert(payload).execute()
    except Exception as e:
        print(f"Error inserting to Supabase: {e}")


def get_last_supabase_timestamp():
    if not supabase:
        return None

    try:
        res = (
            supabase
            .table("sensor_readings")
            .select("created_at")
            .order("created_at", desc=True)
            .limit(1)
            .execute()
        )

        if res.data:
            return res.data[0]["created_at"]
    except Exception as e:
        print(f"Error fetching last timestamp: {e}")

    return None
