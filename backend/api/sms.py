from flask import Blueprint, request, jsonify
import requests
import os

sms_api = Blueprint('sms', __name__)

@sms_api.route('/send', methods=['POST'])
def send_sms():
    data = request.json
    phone = data.get('phone')
    message = data.get('message')
    api_key = os.getenv("FAST2SMS_API_KEY")

    if not phone or not message:
        return jsonify({"error": "Missing phone or message"}), 400

    if not api_key:
        return jsonify({"error": "Fast2SMS API Key missing"}), 500

    url = "https://www.fast2sms.com/dev/bulkV2"
    payload = {
        "message": message,
        "language": "english",
        "route": "q",
        "numbers": phone,
    }
    headers = {
        "authorization": api_key,
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500
