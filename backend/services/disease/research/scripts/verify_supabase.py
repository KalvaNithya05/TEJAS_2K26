import sys
import os
from dotenv import load_dotenv

# Add backend to path to allow imports
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.join(current_dir, 'backend')
sys.path.append(backend_dir)

try:
    from config.supabase_client import get_supabase_client
except ImportError as e:
    print(f"Error importing modules: {e}")
    sys.exit(1)

def verify():
    print("--- Verifying Supabase Connection ---")
    
    # Load env again just to be sure for this script's checks
    dotenv_path = os.path.join(backend_dir, '.env')
    load_dotenv(dotenv_path)

    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")

    print(f"Loading env from: {dotenv_path}")
    print(f"Env file exists: {os.path.exists(dotenv_path)}")
    
    if url:
        print(f"URL found: {url[:10]}... (Len: {len(url)})")
    else:
        print("URL is None")

    if key:
        print(f"KEY found: {key[:10]}... (Len: {len(key)})")
    else:
        print("KEY is None")

    if not url or "your_supabase_url" in url:
        print("[FAIL] SUPABASE_URL is not set or contains default placeholder.")
        return
    
    if not key or "your_supabase_anon_key" in key:
        print("[FAIL] SUPABASE_KEY is not set or contains default placeholder.")
        return

    print(f"URL: {url[:15]}...")
    
    print("Initializing client...")
    client = get_supabase_client()
    
    if not client:
        print("[FAIL] Could not initialize client.")
        return

    try:
        print("Attempting to fetch from 'sensor_readings' table...")
        response = client.table('sensor_readings').select("*").limit(1).execute()
        print("[PASS] Connection successful!")
        if response.data:
            print(f"Data sample: {response.data}")
        else:
            print("Table is empty, but connection works.")
    except Exception as e:
        print(f"[FAIL] Query failed: {e}")
        print("Possible reasons:")
        print("1. Table 'sensor_readings' does not exist.")
        print("2. Network issues.")
        print("3. Invalid credentials.")

if __name__ == "__main__":
    verify()
