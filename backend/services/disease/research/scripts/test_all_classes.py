"""
Comprehensive test script for the fine-tuned disease prediction model.
Tests the model on all organized test images and generates a detailed report.
"""

import os
import sys
sys.path.append('backend')
from dl.disease_predictor import DiseasePredictor
import json

# Disease classes
CLASSES = [
    "Pepper__bell___Bacterial_spot", "Pepper__bell___healthy",
    "Potato___Early_blight", "Potato___Late_blight", "Potato___healthy",
    "Tomato_Bacterial_spot", "Tomato_Early_blight", "Tomato_Late_blight", 
    "Tomato_Leaf_Mold", "Tomato_Septoria_leaf_spot", 
    "Tomato_Spider_mites_Two_spotted_spider_mite", "Tomato__Target_Spot",
    "Tomato__Tomato_YellowLeaf__Curl_Virus", "Tomato__Tomato_mosaic_virus", 
    "Tomato_healthy"
]

TEST_BASE = r"test_images"

def test_all_classes():
    """Test the model on all organized test images."""
    
    print("=" * 80)
    print("DISEASE PREDICTION MODEL - COMPREHENSIVE TEST")
    print("=" * 80)
    print()
    
    predictor = DiseasePredictor()
    
    results = {
        "total_images": 0,
        "correct_predictions": 0,
        "incorrect_predictions": 0,
        "by_class": {}
    }
    
    for class_name in CLASSES:
        test_dir = os.path.join(TEST_BASE, class_name, "synthetic")
        
        if not os.path.exists(test_dir):
            print(f"⚠️  Directory not found: {class_name}")
            continue
        
        # Get all test images
        images = [f for f in os.listdir(test_dir) 
                 if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        
        if len(images) == 0:
            print(f"⚠️  No images in: {class_name}")
            continue
        
        class_results = {
            "total": len(images),
            "correct": 0,
            "predictions": []
        }
        
        print(f"\n{'─' * 80}")
        print(f"Testing: {class_name}")
        print(f"{'─' * 80}")
        
        for img_name in images:
            img_path = os.path.join(test_dir, img_name)
            result = predictor.predict(img_path)
            
            predicted_class = result['class']
            confidence = result['confidence']
            is_correct = predicted_class == class_name
            
            if is_correct:
                class_results["correct"] += 1
                results["correct_predictions"] += 1
                status = "✅ CORRECT"
            else:
                results["incorrect_predictions"] += 1
                status = "❌ INCORRECT"
            
            results["total_images"] += 1
            
            class_results["predictions"].append({
                "image": img_name,
                "predicted": predicted_class,
                "confidence": confidence,
                "correct": is_correct
            })
            
            print(f"  {status} | {img_name}")
            print(f"    Predicted: {predicted_class} ({confidence*100:.1f}%)")
            if not is_correct:
                print(f"    Expected:  {class_name}")
        
        accuracy = (class_results["correct"] / class_results["total"]) * 100
        print(f"\n  Class Accuracy: {class_results['correct']}/{class_results['total']} ({accuracy:.1f}%)")
        
        results["by_class"][class_name] = class_results
    
    # Overall summary
    print("\n" + "=" * 80)
    print("OVERALL RESULTS")
    print("=" * 80)
    
    overall_accuracy = (results["correct_predictions"] / results["total_images"]) * 100
    
    print(f"\nTotal Images Tested: {results['total_images']}")
    print(f"Correct Predictions: {results['correct_predictions']}")
    print(f"Incorrect Predictions: {results['incorrect_predictions']}")
    print(f"\n🎯 Overall Accuracy: {overall_accuracy:.2f}%")
    
    # Per-class summary
    print("\n" + "─" * 80)
    print("PER-CLASS ACCURACY")
    print("─" * 80)
    
    for class_name in CLASSES:
        if class_name in results["by_class"]:
            class_data = results["by_class"][class_name]
            acc = (class_data["correct"] / class_data["total"]) * 100
            print(f"{class_name:50s} {class_data['correct']}/{class_data['total']} ({acc:.1f}%)")
    
    # Save results to JSON
    output_file = "test_results_comprehensive.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print("\n" + "=" * 80)
    print(f"Detailed results saved to: {output_file}")
    print("=" * 80)
    
    return results

if __name__ == "__main__":
    test_all_classes()
