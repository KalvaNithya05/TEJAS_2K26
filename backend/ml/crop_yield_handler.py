import pandas as pd
import os
import sys

class CropYieldHandler:
    def __init__(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Use the updated/augmented dataset
        self.data_path = os.path.join(os.path.dirname(os.path.dirname(current_dir)), 'data', 'crop_yield_updated.csv')

    def load_data(self):
        """
        Loads the crop yield dataset.
        """
        if not os.path.exists(self.data_path):
            # Fallback to original if updated doesn't exist
            original_path = self.data_path.replace('_updated.csv', '.csv')
            if os.path.exists(original_path):
                print(f"Updated dataset not found, using original: {original_path}")
                self.data_path = original_path
            else:
                raise FileNotFoundError(f"Dataset not found at {self.data_path}")

        try:
            df = pd.read_csv(self.data_path)
            
            # Normalize columns
            df.columns = [c.strip() for c in df.columns]
            
            # Encode Categorical Variables if needed or handled in pipeline
            # We return raw DF here, preprocessing handles encoding
            
            return df
        except Exception as e:
            print(f"Error loading yield data: {e}")
            return None
