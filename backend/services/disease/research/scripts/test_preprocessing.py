import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input as mobilenet_preprocess

# Load model
model_path = 'backend/models/plant_disease_model.keras'
classes_path = 'backend/models/plant_disease_classes.json'

if not os.path.exists(model_path):
    print("Model not found")
    exit()

model = tf.keras.models.load_model(model_path)
with open(classes_path, 'r') as f:
    import json
    classes = json.load(f)

# Use the test image created by verify_disease_logic.py or create a dummy one
img_path = 'test_leaf.jpg'
if not os.path.exists(img_path):
    # Create simple dummy image (green square)
    from PIL import Image
    img = Image.new('RGB', (224, 224), color = 'green')
    img.save(img_path)

# Load image
img = image.load_img(img_path, target_size=(224, 224))
img_array = image.img_to_array(img)
img_batch = np.expand_dims(img_array, axis=0)

print("\n--- Testing Preprocessing Methods ---")

# Method 1: rescale=1./255
rescaled = img_batch / 255.0
preds1 = model.predict(rescaled, verbose=0)
idx1 = np.argmax(preds1[0])
conf1 = np.max(preds1[0])
print(f"rescale 1./255: {classes[idx1]} ({conf1:.4f})")

# Method 2: mobilenet_preprocess
preprocessed = mobilenet_preprocess(img_batch.copy())
preds2 = model.predict(preprocessed, verbose=0)
idx2 = np.argmax(preds2[0])
conf2 = np.max(preds2[0])
print(f"mobilenet preprocess_input: {classes[idx2]} ({conf2:.4f})")

if idx1 == idx2:
    print("\n[Result] Both methods predict the same class.")
else:
    print("\n[Result] METHODS PREDICT DIFFERENT CLASSES!")

if conf2 > conf1 + 0.05:
    print("Recommend switching to preprocess_input for better confidence.")
elif conf1 > conf2 + 0.05:
    print("Recommend staying with 1./255 as it yields higher confidence.")
else:
    print("Pre-processing impact is minimal or inconclusive on this sample.")
