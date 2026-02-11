import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import json

def test_on_training_data():
    # Load predictor
    classes_path = 'backend/models/plant_disease_classes.json'
    model_path = 'backend/models/plant_disease_model.keras'
    
    with open(classes_path, 'r') as f:
        classes = json.load(f)
    
    model = tf.keras.models.load_model(model_path)
    print(f"Loaded model and {len(classes)} classes.")
    
    # Test on a few Early Blight images from training set
    eb_dir = 'backend/training/processed_data/Tomato_Early_blight'
    if not os.path.exists(eb_dir):
        print(f"Directory {eb_dir} not found.")
        return
    
    files = [f for f in os.listdir(eb_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))][:10]
    
    from tensorflow.keras.applications.efficientnet import preprocess_input
    
    results = []
    for f in files:
        img_path = os.path.join(eb_dir, f)
        img = image.load_img(img_path, target_size=(224, 224))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)
        
        preds = model.predict(img_array, verbose=0)[0]
        pred_idx = np.argmax(preds)
        pred_class = classes[pred_idx]
        conf = float(preds[pred_idx])
        
        results.append({
            "file": f,
            "actual": "Tomato_Early_blight",
            "predicted": pred_class,
            "confidence": conf,
            "eb_score": float(preds[classes.index("Tomato_Early_blight")]),
            "lb_score": float(preds[classes.index("Tomato_Late_blight")])
        })
    
    with open('test_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    print("Results written to test_results.json")

if __name__ == "__main__":
    test_on_training_data()
