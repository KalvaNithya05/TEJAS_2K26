import os
import zipfile
import shutil
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import EfficientNetB2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout, Input, BatchNormalization
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
import json
import traceback
import numpy as np
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, CSVLogger, TensorBoard
from tensorflow.keras.applications.efficientnet import preprocess_input

# Configuration
# ==========================================
# Dataset Structure Assumption:
# The ZIP file should contain folders corresponding to class names.
# (e.g., /dataset/Tomato_Bacterial_spot/, /dataset/Tomato_healthy/, etc.)
# ==========================================

TRAIN_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_PATH = os.path.join(TRAIN_DIR, 'dataset') # Extracted folder
PROCESSED_DIR = os.path.join(TRAIN_DIR, 'processed_data') # Filtered target classes
ZIP_PATH = None # Will search for first zip in this dir

# Model Paths
MODELS_DIR = os.path.join(TRAIN_DIR, 'models')
MODEL_SAVE_PATH = os.path.join(MODELS_DIR, 'plant_disease_model.keras')
CLASSES_SAVE_PATH = os.path.join(MODELS_DIR, 'plant_disease_classes.json')

# Training Config
IMG_SIZE = (260, 260)  # Optimal for EfficientNetB2
BATCH_SIZE = 32
EPOCHS = 15  # Initial training with frozen base
FINE_TUNE_EPOCHS = 30  # Extended fine-tuning for better convergence
LEARNING_RATE = 0.001  # Initial learning rate for frozen stage
FINE_TUNE_LR = 1e-5  # Lower LR for fine-tuning to preserve pretrained features

# Target Classes
TARGET_CLASSES = [
    'Pepper__bell___Bacterial_spot', 'Pepper__bell___healthy',
    'Potato___Early_blight', 'Potato___Late_blight', 'Potato___healthy',
    'Tomato_Bacterial_spot', 'Tomato_Early_blight', 'Tomato_Late_blight', 'Tomato_Leaf_Mold',
    'Tomato_Septoria_leaf_spot', 'Tomato_Spider_mites_Two_spotted_spider_mite', 'Tomato__Target_Spot',
    'Tomato__Tomato_YellowLeaf__Curl_Virus', 'Tomato__Tomato_mosaic_virus', 'Tomato_healthy'
]

def setup_directories():
    """Ensure necessary directories exist."""
    if not os.path.exists(MODELS_DIR):
        os.makedirs(MODELS_DIR)
        print(f"Created models directory: {MODELS_DIR}")

def find_and_extract_zip():
    """
    Finds the first .zip file in the directory and extracts it.
    ALWAYS performs a clean extraction to ensure no stale data.
    """
    global ZIP_PATH
    
    # 1. Find zip file
    files = [f for f in os.listdir(TRAIN_DIR) if f.endswith('.zip')]
    if not files:
        print("Error: No ZIP file found in backend/training/")
        return False
    
    ZIP_PATH = os.path.join(TRAIN_DIR, files[0])
    print(f"Found dataset archive: {ZIP_PATH}")
    
    # 2. Clean previous extraction if exists
    if os.path.exists(DATASET_PATH):
        print("Cleaning up old extracted dataset...")
        shutil.rmtree(DATASET_PATH)
    
    # 3. Extract
    print("Extracting dataset (this may take a moment)...")
    try:
        with zipfile.ZipFile(ZIP_PATH, 'r') as zip_ref:
            zip_ref.extractall(DATASET_PATH)
        print("Extraction complete.")
        return True
    except Exception as e:
        print(f"Error during extraction: {e}")
        # Clean up partial extraction
        if os.path.exists(DATASET_PATH):
            shutil.rmtree(DATASET_PATH)
        return False

def organize_dataset():
    """
    Scans the extracted dataset for class folders and
    copies them to a clean 'processed_data' directory.
    If TARGET_CLASSES is empty, it uses all valid subdirectories found.
    """
    print("Organizing dataset for training...")
    global TARGET_CLASSES
    
    # 1. Clean previous processed data
    if os.path.exists(PROCESSED_DIR):
        print("Cleaning up old processed data...")
        shutil.rmtree(PROCESSED_DIR)
    os.makedirs(PROCESSED_DIR)
    
    # 2. Identify classes
    valid_classes = []
    source_root = None
    
    # Exclude system folders
    EXCLUDE = {'__MACOSX', '.ipynb_checkpoints', 'PlantVillage'}
    
    for root, dirs, files in os.walk(DATASET_PATH):
        # Heuristic: A folder is a class if it contains images (e.g., .jpg)
        image_count = len([f for f in files if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
        if image_count > 0:
            folder_name = os.path.basename(root)
            if folder_name not in EXCLUDE:
                # If TARGET_CLASSES is set, filter. Otherwise take all.
                if not TARGET_CLASSES or folder_name in TARGET_CLASSES:
                    valid_classes.append((root, folder_name))
                    
    if not valid_classes:
        print("Error: Could not find any valid class folders with images.")
        return None
        
    print(f"Detected {len(valid_classes)} classes.")
    
    # 3. Copy target classes
    count = 0
    detected_names = []
    for src_path, cls_name in valid_classes:
        dst = os.path.join(PROCESSED_DIR, cls_name)
        if not os.path.exists(dst):
            shutil.copytree(src_path, dst)
            detected_names.append(cls_name)
            count += 1
            
    print(f"Successfully prepared {count} classes for training.")
    return PROCESSED_DIR

def train_model(data_dir):
    print("\n" + "="*40)
    print("      STARTING TRAINING PIPELINE      ")
    print("="*40)
    
    # Enhanced Data Augmentation for Better Generalization
    train_datagen = ImageDataGenerator(
        preprocessing_function=preprocess_input,
        rotation_range=45,  # Increased rotation
        width_shift_range=0.25,  # More aggressive shifts
        height_shift_range=0.25,
        shear_range=0.25,
        zoom_range=0.3,  # Increased zoom range
        horizontal_flip=True,
        vertical_flip=True,  # Added vertical flip for leaf images
        brightness_range=[0.7, 1.3],  # Wider brightness range
        fill_mode='nearest',
        validation_split=0.2
    )
    
    # Validation generator (no augmentation except preprocessing)
    val_datagen = ImageDataGenerator(
        preprocessing_function=preprocess_input,
        validation_split=0.2
    )
    
    print("\n[1/4] Loading Training Data...")
    train_generator = train_datagen.flow_from_directory(
        data_dir,
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        subset='training'
    )
    
    print("\n[2/4] Loading Validation Data...")
    validation_generator = val_datagen.flow_from_directory(
        data_dir,
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        subset='validation',
        shuffle=False  # Don't shuffle validation data for consistent evaluation
    )
    
    # Check classes
    class_indices = train_generator.class_indices
    class_names = list(class_indices.keys())
    print(f"\nClasses found ({len(class_names)}): {class_names}")
    
    if len(class_names) < 2:
        print("Error: Need at least 2 classes to train. Aborting.")
        return
    
    # Save classes for inference immediately
    # (Safe to save this early as it defines the schema)
    with open(CLASSES_SAVE_PATH, 'w') as f:
        json.dump(class_names, f)
    print(f"Saved class mapping to {CLASSES_SAVE_PATH}")
    
    # Model Setup (EfficientNetB2 - Enhanced Architecture)
    print("\n[3/4] Building Model (EfficientNetB2)...")
    base_model = EfficientNetB2(weights='imagenet', include_top=False, input_shape=(260, 260, 3))
    base_model.trainable = False  # Freeze base initially
    
    # Enhanced classification head
    x = base_model.output
    x = GlobalAveragePooling2D(name='avg_pool')(x)
    x = BatchNormalization(name='bn_1')(x)
    x = Dense(256, activation='relu', name='dense_1')(x)
    x = Dropout(0.5, name='dropout_1')(x)
    x = BatchNormalization(name='bn_2')(x)
    x = Dense(128, activation='relu', name='dense_2')(x)
    x = Dropout(0.3, name='dropout_2')(x)
    predictions = Dense(len(class_names), activation='softmax', name='predictions')(x)
    
    model = Model(inputs=base_model.input, outputs=predictions)
    
    model.compile(optimizer=Adam(learning_rate=LEARNING_RATE),
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])
    
    try:
        # Setup logging directories
        logs_dir = os.path.join(TRAIN_DIR, 'logs')
        os.makedirs(logs_dir, exist_ok=True)
        
        # Comprehensive Callbacks
        early_stop = EarlyStopping(
            monitor='val_loss', 
            patience=7,  # Increased patience for fine-tuning
            restore_best_weights=True,
            verbose=1
        )
        
        checkpoint = ModelCheckpoint(
            MODEL_SAVE_PATH, 
            monitor='val_accuracy', 
            save_best_only=True, 
            mode='max',
            verbose=1
        )
        
        reduce_lr = tf.keras.callbacks.ReduceLROnPlateau(
            monitor='val_loss', 
            factor=0.2, 
            patience=3, 
            min_lr=1e-7,
            verbose=1
        )
        
        # TensorBoard for visualization
        tensorboard = TensorBoard(
            log_dir=os.path.join(logs_dir, 'tensorboard'),
            histogram_freq=1,
            write_graph=True,
            write_images=False
        )
        
        # CSV Logger for training history
        csv_logger = CSVLogger(
            os.path.join(logs_dir, 'training_history.csv'),
            append=False
        )

        # Stage 1: Train Top Layers
        print(f"\n[4/4] Stage 1: Training top layers for {EPOCHS} epochs...")
        print(f"Total training samples: {train_generator.samples}")
        print(f"Total validation samples: {validation_generator.samples}")
        
        history_stage1 = model.fit(
            train_generator,
            epochs=EPOCHS,
            validation_data=validation_generator,
            callbacks=[early_stop, checkpoint, reduce_lr, tensorboard, csv_logger],
            verbose=1
        )
        
        print(f"\nStage 1 Complete - Best Val Accuracy: {max(history_stage1.history['val_accuracy']):.4f}")
        
        # Stage 2: Fine-tuning (Gradual Unfreezing)
        print("\n[5/5] Stage 2: Fine-tuning base model...")
        print(f"Unfreezing last 50 layers of EfficientNetB2 for fine-tuning...")
        
        base_model.trainable = True
        # Unfreeze last 50 layers for EfficientNetB2 (more capacity than B0)
        for layer in base_model.layers[:-50]:
            layer.trainable = False
        
        # Count trainable parameters
        trainable_count = sum([tf.keras.backend.count_params(w) for w in model.trainable_weights])
        print(f"Trainable parameters: {trainable_count:,}")
        
        # Cosine decay learning rate schedule
        cosine_decay = tf.keras.optimizers.schedules.CosineDecay(
            initial_learning_rate=FINE_TUNE_LR,
            decay_steps=FINE_TUNE_EPOCHS * len(train_generator),
            alpha=0.1  # Minimum learning rate will be 10% of initial
        )
        
        model.compile(
            optimizer=Adam(learning_rate=cosine_decay),
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        # Update CSV logger for stage 2
        csv_logger_ft = CSVLogger(
            os.path.join(logs_dir, 'finetuning_history.csv'),
            append=False
        )
        
        history_stage2 = model.fit(
            train_generator,
            epochs=FINE_TUNE_EPOCHS,
            validation_data=validation_generator,
            callbacks=[early_stop, checkpoint, reduce_lr, tensorboard, csv_logger_ft],
            verbose=1
        )
        
        print(f"\nStage 2 Complete - Best Val Accuracy: {max(history_stage2.history['val_accuracy']):.4f}")
        
        # Final Evaluation
        print("\n" + "="*40)
        print("      FINAL EVALUATION")
        print("="*40)
        
        final_loss, final_accuracy = model.evaluate(validation_generator, verbose=1)
        print(f"\nFinal Validation Loss: {final_loss:.4f}")
        print(f"Final Validation Accuracy: {final_accuracy:.4f}")
        
        # Save Model
        print(f"\nSaving model to {MODEL_SAVE_PATH}...")
        model.save(MODEL_SAVE_PATH)
        
        # Save training history
        history_path = os.path.join(logs_dir, 'complete_training_history.json')
        complete_history = {
            'stage1': {k: [float(v) for v in vals] for k, vals in history_stage1.history.items()},
            'stage2': {k: [float(v) for v in vals] for k, vals in history_stage2.history.items()},
            'final_metrics': {
                'val_loss': float(final_loss),
                'val_accuracy': float(final_accuracy)
            }
        }
        with open(history_path, 'w') as f:
            json.dump(complete_history, f, indent=2)
        print(f"Training history saved to {history_path}")
        
        print("\n" + "="*40)
        print("SUCCESS: Model Training Complete!")
        print("="*40)
        print(f"Model: EfficientNetB2")
        print(f"Classes: {len(class_names)}")
        print(f"Final Accuracy: {final_accuracy*100:.2f}%")
        print(f"Model saved: {MODEL_SAVE_PATH}")
        print(f"Logs directory: {logs_dir}")
        print("="*40)
        
    except KeyboardInterrupt:
        print("\nTraining interrupted by user. Model NOT saved.")
    except Exception as e:
        print(f"\nError during training: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    try:
        setup_directories()
        
        # Clean start sequence
        if find_and_extract_zip():
            final_data_dir = organize_dataset()
            if final_data_dir:
                train_model(final_data_dir)
            else:
                print("Failed to organize dataset.")
        else:
            print("Setup failed.")
            
        # Optional: Cleanup processed data to save space? 
        # For now, we keep it in case user wants to inspect.
            
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        traceback.print_exc()
