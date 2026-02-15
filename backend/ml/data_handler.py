import pandas as pd
import os
import sys

class DataHandler:
    def __init__(self):
        # Determine the root directory (assuming this script is in backend/ml/)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(os.path.dirname(os.path.dirname(current_dir)), 'data')
        
        # Prioritize restored high-quality dataset
        restored_path = os.path.join(data_dir, 'Crop_recommendation_restored.csv')
        master_path = os.path.join(data_dir, 'mitti_mitra_all_india_dataset.csv')
        
        if os.path.exists(restored_path):
            self.data_path = restored_path
            print(f"Using high-quality restored dataset: {self.data_path}")
        else:
            self.data_path = master_path

    def load_data(self):
        """
        Loads the crop recommendation dataset.
        Returns:
            pd.DataFrame: Cleaned dataframe ready for training.
        """
        if not os.path.exists(self.data_path):
            raise FileNotFoundError(f"Dataset not found at {self.data_path}")

        try:
            df = pd.read_csv(self.data_path)
            
            # Normalize column names first
            df.columns = [c.strip().lower() for c in df.columns]
            
            # Mapping for standard Kaggle dataset or master dataset
            # Kaggle: N, P, K, temperature, humidity, ph, rainfall, label
            # Master: soil_n, soil_p, soil_k, soil_ph, avg_temperature, avg_humidity, avg_rainfall, crop
            column_mapping = {
                'soil_n': 'N',
                'soil_p': 'P',
                'soil_k': 'K',
                'soil_ph': 'ph',
                'avg_temperature': 'temperature',
                'avg_humidity': 'humidity',
                'avg_rainfall': 'rainfall',
                'crop': 'label',
                # Handle lowercase Kaggle format
                'n': 'N',
                'p': 'P',
                'k': 'K'
            }
            
            df.rename(columns=column_mapping, inplace=True)
            
            # Filter for required columns
            required_cols = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall', 'label']
            
            # Check which are missing
            missing = [c for c in required_cols if c not in df.columns]
            
            if missing:
                print(f"Warning: Missing columns in master dataset: {missing}")
                
            # Drop rows with missing values in required columns (if they exist)
            available_cols = [c for c in required_cols if c in df.columns]
            if available_cols:
                df.dropna(subset=available_cols, inplace=True)
            
            return df[available_cols] if not missing else df
        except Exception as e:
            print(f"Error loading data: {e}")
            return None
