from flask import Blueprint, request, jsonify
import os
import uuid
import collections
from .predictor import DiseasePredictor

disease_bp = Blueprint('disease', __name__)
predictor = DiseasePredictor()

# Temp upload folder
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@disease_bp.route('/predict', methods=['POST'])
def predict_disease():
    try:
        # Support both 'images' (multiple) and 'image' (single)
        files = request.files.getlist('images') or request.files.getlist('image')
        
        if not files or all(f.filename == '' for f in files):
            return jsonify({'error': 'No image files provided'}), 400
        
        predictions = []
        saved_filepaths = []
        
        try:
            # 1. Collect predictions for ALL uploaded images
            for file in files:
                if file.filename == '': continue
                
                # Save file temporarily
                filename = f"{uuid.uuid4()}_{file.filename}"
                filepath = os.path.join(UPLOAD_FOLDER, filename)
                file.save(filepath)
                saved_filepaths.append(filepath)
                
                # Predict for this specific image
                result = predictor.predict(filepath)
                predictions.append({
                    'image_id': filename,
                    'disease_name': result['class'],
                    'confidence_score': result['confidence']
                })
            
            if not predictions:
                return jsonify({'error': 'Prediction failed for all images'}), 500

            # --- Aggregation Logic ---
            # 2. Count occurrences of each disease
            disease_counts = collections.Counter([p['disease_name'] for p in predictions])
            
            # 3. Use majority voting with tie-breaking
            # Get the diseases with the maximum count
            max_count = max(disease_counts.values())
            candidates = [disease for disease, count in disease_counts.items() if count == max_count]
            
            if len(candidates) > 1:
                # 4. Tie-breaking: Choose disease with highest average confidence
                candidate_metrics = []
                for cand in candidates:
                    confs = [p['confidence_score'] for p in predictions if p['disease_name'] == cand]
                    avg_conf = sum(confs) / len(confs)
                    # We round to 4 decimals to avoid floating point noise flipping the result
                    candidate_metrics.append({
                        'name': cand,
                        'avg_conf': round(avg_conf, 4)
                    })
                
                # Sort by avg_conf descending, then by name ascending (lexicographical) for absolute determinism
                candidate_metrics.sort(key=lambda x: (-x['avg_conf'], x['name']))
                final_disease = candidate_metrics[0]['name']
            else:
                final_disease = candidates[0]
            
            # 5. Calculate FINAL confidence (average confidence of selected disease)
            selected_confs = [p['confidence_score'] for p in predictions if p['disease_name'] == final_disease]
            final_confidence = sum(selected_confs) / len(selected_confs)
            
            # 6. Check uncertainty threshold (70%)
            if final_confidence < 0.70:
                response = {
                    "final_disease": "Uncertain",
                    "final_confidence": f"{round(final_confidence * 100, 2)}%",
                    "explanation": "Disease detection is uncertain. Please upload clearer images.",
                    "treatment_plan": "N/A",
                    "prevention_tips": ["Ensure images are well-lit", "Focus clearly on the affected leaf", "Capture multiple angles of the symptom"]
                }
            else:
                # 7. Use predefined expert knowledge base
                from .expert import get_disease_info
                info = get_disease_info(final_disease)
                
                # 8. Handle healthy/disease distinction for treatments/prevention
                is_healthy = 'healthy' in final_disease.lower()
                
                response = {
                    "final_disease": final_disease.replace('_', ' '),
                    "final_confidence": f"{round(final_confidence * 100, 2)}%",
                    "explanation": info['explanation'],
                    "treatment_plan": "N/A" if is_healthy else info['treatment'],
                    "prevention_tips": info['prevention']
                }

            # Clean up
            for path in saved_filepaths:
                if os.path.exists(path):
                    os.remove(path)
                    
            # Return strict JSON format as requested
            return jsonify(response)
            
        except Exception as e:
            # Clean up on error
            for path in saved_filepaths:
                if os.path.exists(path):
                    os.remove(path)
            raise e
                
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

