"""
Script to organize test images from the training dataset.
This script copies 3 sample images from each disease class into the test_images folder
with a synthetic subfolder structure for easy testing.
"""

import os
import shutil
import random

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

# Paths
DATASET_BASE = r"backend\training\dataset\PlantVillage"
TEST_BASE = r"test_images"
IMAGES_PER_CLASS = 3

def organize_test_images():
    """Copy sample images from dataset to test_images folder."""
    
    print("=" * 60)
    print("Organizing Test Images")
    print("=" * 60)
    
    total_copied = 0
    
    for class_name in CLASSES:
        # Source directory in dataset
        source_dir = os.path.join(DATASET_BASE, class_name)
        
        # Destination directory in test_images
        dest_dir = os.path.join(TEST_BASE, class_name, "synthetic")
        
        # Create destination directory
        os.makedirs(dest_dir, exist_ok=True)
        
        # Check if source exists
        if not os.path.exists(source_dir):
            print(f"⚠️  Source not found: {class_name}")
            continue
        
        # Get all images from source
        all_images = [f for f in os.listdir(source_dir) 
                     if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        
        if len(all_images) == 0:
            print(f"⚠️  No images found in: {class_name}")
            continue
        
        # Randomly select images
        num_to_copy = min(IMAGES_PER_CLASS, len(all_images))
        selected_images = random.sample(all_images, num_to_copy)
        
        # Copy images
        for i, img_name in enumerate(selected_images, 1):
            source_path = os.path.join(source_dir, img_name)
            # Rename to test_1.jpg, test_2.jpg, test_3.jpg
            ext = os.path.splitext(img_name)[1]
            dest_name = f"test_{i}{ext}"
            dest_path = os.path.join(dest_dir, dest_name)
            
            shutil.copy2(source_path, dest_path)
            total_copied += 1
        
        print(f"✅ {class_name}: Copied {num_to_copy} images")
    
    print("=" * 60)
    print(f"Total images copied: {total_copied}")
    print(f"Total classes: {len(CLASSES)}")
    print(f"Expected: {len(CLASSES) * IMAGES_PER_CLASS}")
    print("=" * 60)
    print("\nTest images organized successfully!")
    print(f"Location: {os.path.abspath(TEST_BASE)}")

if __name__ == "__main__":
    organize_test_images()
