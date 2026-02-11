import sys
import os
sys.path.append('backend')
from dl.disease_predictor import DiseasePredictor

predictor = DiseasePredictor()
test_dir = 'backend/training/dataset/PlantVillage/Tomato_Early_blight'
images = [
    '0012b9d2-2130-4a06-a834-b1f3af34f57e___RS_Erly.B 8389.JPG',
    '0034a551-9512-44e5-ba6c-827f85ecc688___RS_Erly.B 9432.JPG',
    '004cbe60-8ff9-4965-92df-e86694d5e9ba___RS_Erly.B 8253.JPG'
]

for img_name in images:
    path = os.path.join(test_dir, img_name)
    if os.path.exists(path):
        result = predictor.predict(path)
        print(f"Image: {img_name}")
        print(f"Result: {result}")
        print("-" * 20)
    else:
        print(f"File not found: {path}")
