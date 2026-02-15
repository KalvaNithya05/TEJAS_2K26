from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
import sys

# Ensure backend directory is in path
# Ensure backend directory and project root are in path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)
sys.path.append(os.path.dirname(current_dir))

load_dotenv(os.path.join(current_dir, '.env'))

def create_app():
    app = Flask(__name__)
    CORS(app)  # Allow Frontend to communicate

    # Import Blueprints (Assumes these files will be created next)
    # We use deferred imports inside create_app to avoid circular dependencies if any
    try:
        from api.predict import predict_bp
        from api.sensor_data import sensor_bp
        from api.report import report_bp
        from services.disease.api import disease_bp
        from api.sms import sms_api
        from api.recovery import recovery_bp

        app.register_blueprint(predict_bp, url_prefix='/api/predict')
        app.register_blueprint(sensor_bp, url_prefix='/api/sensor') # '/api/sensor' matches pi config
        app.register_blueprint(report_bp, url_prefix='/api/report')
        app.register_blueprint(disease_bp, url_prefix='/api/disease')
        app.register_blueprint(sms_api, url_prefix='/api/sms')
        app.register_blueprint(recovery_bp, url_prefix='/api/recovery')
    except ImportError as e:
        print(f"Warning: Could not import some API blueprints: {e}")
        print("Note: This is expected during initial generation phase.")

    @app.route('/')
    def health_check():
        return jsonify({
            "project": "Mitti Mitra",
            "status": "online",
            "version": "1.0.0"
        })

    return app

if __name__ == '__main__':
    from services.thingspeak_worker import run_thingspeak_ingestion
    import threading
    
    app = create_app()
    
    # Start background ThingSpeak worker
    print("Initiating ThingSpeak background worker thread...")
    t = threading.Thread(target=run_thingspeak_ingestion, daemon=True)
    t.start()
    
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
