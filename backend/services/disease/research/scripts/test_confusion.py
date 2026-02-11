import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.efficientnet import preprocess_input
import json

def test_confusion():
    # Load predictor
    classes_path = 'backend/models/plant_disease_classes.json'
    model_path = 'backend/models/plant_disease_model.keras'
    
    with open(classes_path, 'r') as f:
        classes = json.load(f)
    
    model = tf.keras.models.load_model(model_path)
    print(f"Loaded model.")
    
    # Define classes to test
    target_classes = ['Tomato_Bacterial_spot', 'Tomato_Septoria_leaf_spot']
    
    results = {'total': 0, 'correct': 0, 'confused': 0}
    
    with open('confusion_results.txt', 'w', encoding='utf-8') as log_file:
        log_file.write(f"--- Testing Confusion: {target_classes[0]} vs {target_classes[1]} ---\n\n")
        
        for actual_class in target_classes:
            dir_path = os.path.join('backend/training/processed_data', actual_class)
            if not os.path.exists(dir_path):
                log_file.write(f"Missing directory: {dir_path}\n")
                continue
                
            # Get 20 random images from each
            files = [f for f in os.listdir(dir_path) if f.lower().endswith(('.jpg', '.png'))]
            test_files = files[:20] 
            
            log_file.write(f"\nTesting {actual_class} ({len(test_files)} images)...\n")
            
            for f in test_files:
                try:
                    img_path = os.path.join(dir_path, f)
                    img = image.load_img(img_path, target_size=(224, 224))
                    img_array = image.img_to_array(img)
                    img_array = np.expand_dims(img_array, axis=0)
                    img_array = preprocess_input(img_array)
                    
                    preds = model.predict(img_array, verbose=0)[0]
                    pred_idx = np.argmax(preds)
                    pred_class = classes[pred_idx]
                    conf = float(preds[pred_idx])
                    
                    results['total'] += 1
                    
                    if pred_class == actual_class:
                        results['correct'] += 1
                        status = "✅"
                    elif pred_class in target_classes:
                        results['confused'] += 1
                        status = "❌ (Swapped)"
                    else:
                        status = f"❌ (Predicted: {pred_class})"
                    
                    log_file.write(f"[{status}] {f} -> {pred_class} ({conf:.2f})\n")
                    
                except Exception as e:
                    log_file.write(f"Error processing {f}: {e}\n")

        log_file.write("\n--- Summary ---\n")
        log_file.write(f"Total: {results['total']}\n")
        log_file.write(f"Correct: {results['correct']}\n")
        log_file.write(f"Confused (Spot <-> Septoria): {results['confused']}\n")
        if results['total'] > 0:
            log_file.write(f"Accuracy on these tough cases: {results['correct']/results['total']*100:.1f}%\n")

    print("\n--- Summary ---")
    print(f"Total: {results['total']}")
    print(f"Correct: {results['correct']}")
    print(f"Confused (Spot <-> Septoria): {results['confused']}")
    print(f"Accuracy on these tough cases: {results['correct']/results['total']*100:.1f}%")

if __name__ == "__main__":
    test_confusion()
