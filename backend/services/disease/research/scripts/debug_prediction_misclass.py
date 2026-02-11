import sys
import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import json

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from dl.disease_predictor import DiseasePredictor

def test_images(image_paths):
    predictor = DiseasePredictor()
    print(f"Classes used by predictor: {predictor.classes}")
    
    for img_path in image_paths:
        if not os.path.exists(img_path):
            print(f"Skipping {img_path} (not found)")
            continue
            
        print(f"\nTesting: {img_path}")
        result = predictor.predict(img_path)
        print(f"Result: {result}")
        
        # Manual check
        img = image.load_img(img_path, target_size=(224, 224))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = img_array / 255.0
        
        predictions = predictor.model.predict(img_array, verbose=0)[0]
        top_indices = predictions.argsort()[-3:][::-1]
        
        print("Top 3 Predictions:")
        for idx in top_indices:
            print(f"  {predictor.classes[idx]}: {predictions[idx]:.4f}")

if __name__ == "__main__":
    uploaded_images = [
        r"C:/Users/NITHYA/.gemini/antigravity/brain/77d3a3c2-ff01-4548-b83a-04f573b3329d/uploaded_image_0_1769016738717.jpg",
        r"C:/Users/NITHYA/.gemini/antigravity/brain/77d3a3c2-ff01-4548-b83a-04f573b3329d/uploaded_image_1_1769016738717.jpg",
        r"C:/Users/NITHYA/.gemini/antigravity/brain/77d3a3c2-ff01-4548-b83a-04f573b3329d/uploaded_image_2_1769016738717.jpg",
        r"C:/Users/NITHYA/.gemini/antigravity/brain/77d3a3c2-ff01-4548-b83a-04f573b3329d/uploaded_image_3_1769016738717.jpg",
        r"C:/Users/NITHYA/.gemini/antigravity/brain/77d3a3c2-ff01-4548-b83a-04f573b3329d/uploaded_image_4_1769016738717.jpg"
    ]
    
    # Store results
    results = []
    predictor = DiseasePredictor()
    
    for img_path in uploaded_images:
        if os.path.exists(img_path):
            res = predictor.predict(img_path)
            # Get top 3
            img = image.load_img(img_path, target_size=(224, 224))
            img_array = image.img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0) / 255.0
            preds = predictor.model.predict(img_array, verbose=0)[0]
            top_idx = preds.argsort()[-3:][::-1]
            top_3 = []
            for i in top_idx:
                top_3.append({"class": predictor.classes[i], "score": float(preds[i])})
            
            results.append({
                "path": img_path,
                "prediction": res,
                "top_3": top_3
            })
    
    with open('debug_results.json', 'w') as f:
        json.dump(results, f, indent=4)
    print("Results saved to debug_results.json")
