from flask import Flask, jsonify
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

app = Flask(__name__)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
print(f"DEBUG: URL={SUPABASE_URL}")
print(f"DEBUG: KEY_LEN={len(SUPABASE_KEY) if SUPABASE_KEY else 0}")

try:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    print(f"DEBUG: Client creation failed: {e}")
    supabase = None

@app.route('/test')
def test_connection():
    if not supabase:
        return jsonify({"error": "client_not_initialized"}), 500
    try:
        # Try both tables
        res1 = supabase.table('sensor_readings').select('*').limit(1).execute()
        res2 = supabase.table('soil_data').select('*').limit(1).execute()
        return jsonify({
            "sensor_readings": bool(res1.data),
            "soil_data": bool(res2.data)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 401

if __name__ == '__main__':
    app.run(port=5005)
