from flask import Blueprint, request, jsonify
from config.supabase_client import supabase
from datetime import datetime
import random

sensor_bp = Blueprint('sensor', __name__)

def map_single_record(r):
    """
    Map Supabase column names to frontend expected names.
    Robust mapping for Nitrogen, Phosphorus, Potassium and pH (soil_ph).
    """
    if not r:
        return None
        
    nitrogen = r.get('nitrogen')
    if nitrogen is None: nitrogen = r.get('N')
    
    phosphorus = r.get('phosphorus')
    if phosphorus is None: phosphorus = r.get('P')
    
    potassium = r.get('potassium')
    if potassium is None: potassium = r.get('K')
    
    # User confirmed column is soil_ph
    ph = r.get('soil_ph')
    if ph is None: ph = r.get('ph')
    if ph is None: ph = r.get('pH')
        
    return {
        'id': r.get('id'),
        'timestamp': r.get('created_at') or r.get('timestamp'),
        'device_id': r.get('device_id', 'MM-POLE-001'),
        'temperature': r.get('temperature'),
        'humidity': r.get('humidity'),
        'ph': ph,
        'nitrogen': nitrogen,
        'phosphorus': phosphorus,
        'potassium': potassium,
        'moisture': r.get('moisture'),
        'rainfall': r.get('rainfall', 0.0)
    }

@sensor_bp.route('/data', methods=['POST'])
def receive_data():
    """
    Ingest data from Raspberry Pi / IoT / ESP32.
    """
    data = request.json
    if not data:
        return jsonify({'error': 'No data received'}), 400
        
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] TELEMETRY INGESTED: {data}")

    if supabase:
        try:
            ph_val = data.get('soil_ph') or data.get('ph') or data.get('pH') or data.get('ph_level')
            n_val = data.get('nitrogen') or data.get('N')
            p_val = data.get('phosphorus') or data.get('P')
            k_val = data.get('potassium') or data.get('K')
            
            record = {
                'device_id': data.get('device_id', 'MM-POLE-001'),
                'temperature': data.get('temperature'),
                'humidity': data.get('humidity'),
                'soil_ph': ph_val, # Use verified col name
                'nitrogen': n_val,
                'phosphorus': p_val,
                'potassium': k_val,
                'moisture': data.get('moisture'),
                'created_at': datetime.now().isoformat()
            }
            
            supabase.table('sensor_readings').insert(record).execute()
            return jsonify({'status': 'stored'}), 201
        except Exception as e:
            print(f"Insert Error: {e}")
            return jsonify({'error': 'db_error', 'message': str(e)}), 500
    else:
        return jsonify({'status': 'mock_stored'}), 200

@sensor_bp.route('/latest', methods=['GET'])
def get_latest():
    """
    Get the latest sensor reading.
    """
    if supabase:
        try:
            response = supabase.table('sensor_readings')\
                .select('*')\
                .order('created_at', desc=True)\
                .limit(1)\
                .execute()
            
            if response.data:
                return jsonify(map_single_record(response.data[0]))
        except Exception as e:
            print(f"Fetch Error: {e}")
            
    return jsonify({'error': 'no_data', 'message': 'No sensor readings found.'}), 404

from services.aggregator import get_aggregated_data

@sensor_bp.route('/aggregate', methods=['GET'])
def get_aggregate():
    """
    Get aggregated values (average of last 30 readings from ThingSpeak).
    """
    stats = get_aggregated_data(results=30)
    if not stats:
        return jsonify({'error': 'failed_to_fetch', 'message': 'Could not fetch data from ThingSpeak'}), 500
    return jsonify(stats)

@sensor_bp.route('/history', methods=['GET'])
def get_history():
    """
    Get the last 30 sensor readings.
    """
    if supabase:
        try:
            response = supabase.table('sensor_readings')\
                .select('*')\
                .order('created_at', desc=True)\
                .limit(30)\
                .execute()
            
            return jsonify([map_single_record(r) for r in response.data])
        except Exception as e:
            print(f"History Fetch Error: {e}")
            
    return jsonify([])
