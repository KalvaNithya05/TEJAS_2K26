from flask import Blueprint, request, jsonify
from services.recovery_manager import RecoveryManager

recovery_bp = Blueprint('recovery', __name__)
recovery_manager = RecoveryManager()

@recovery_bp.route('/predict', methods=['POST'])
def predict_recovery():
    try:
        data = request.json
        
        # Required fields check
        required_fields = ['damage_percentage', 'days_remaining', 'N', 'damage_type']
        missing = [f for f in required_fields if f not in data]
        if missing:
            return jsonify({"error": f"Missing required fields: {missing}"}), 400
            
        # Call the manager
        result = recovery_manager.get_recovery_plan(data)
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
