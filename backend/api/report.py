from flask import Blueprint, jsonify, request, send_file
from datetime import datetime
from services.aggregation_service import AggregationService
import subprocess
import json
import os
import tempfile

report_bp = Blueprint('report', __name__)
agg_service = AggregationService()

@report_bp.route('/summary', methods=['GET'])
def get_summary_report():
    """
    Returns a unified soil health report based on aggregated data.
    """
    try:
        # Fetch 30-day aggregation
        stats = agg_service.get_30_day_average()
        
        report = {
            'report_id': f"RPT-{int(datetime.now().timestamp())}",
            'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'period': 'Last 30 Days',
            'soil_health_summary': stats,
            'overall_status': 'Good' # Logic to determine status could be added
        }
        
        return jsonify(report)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@report_bp.route('/download-pdf', methods=['POST'])
def download_pdf():
    """
    Generate and download PDF report with crop and fertilizer recommendations.
    Expects JSON body with: crops, fertilizer_recommendation, used_params
    """
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Call Node.js PDF service
        # Create temporary file for data
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(data, f)
            temp_file = f.name
        
        try:
            # Call Node.js script to generate PDF
            result = subprocess.run(
                ['node', 'generate_pdf.js', temp_file],
                cwd=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'services'),
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode != 0:
                print(f"PDF generation error: {result.stderr}")
                return jsonify({'error': 'PDF generation failed', 'details': result.stderr}), 500
            
            # Get the PDF file path from stdout
            pdf_path = result.stdout.strip()
            
            if os.path.exists(pdf_path):
                return send_file(
                    pdf_path,
                    mimetype='application/pdf',
                    as_attachment=True,
                    download_name=f'mitti-mitra-report-{datetime.now().strftime("%Y%m%d")}.pdf'
                )
            else:
                return jsonify({'error': 'PDF file not found'}), 500
                
        finally:
            # Clean up temp file
            if os.path.exists(temp_file):
                os.unlink(temp_file)
            
    except Exception as e:
        print(f"PDF download error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': 'Internal Server Error', 'details': str(e)}), 500
