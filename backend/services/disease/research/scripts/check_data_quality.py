import pandas as pd
import os
import sys

# Adjust path to import local modules
sys.path.append(os.path.join(os.getcwd(), 'backend', 'ml'))
from data_handler import DataHandler

def check_quality():
    handler = DataHandler()
    df = handler.load_data()
    
    if df is None:
        print("Failed to load data")
        return

    print("--- Dataset Info ---")
    print(df.info())
    print("\n--- Descriptive Stats ---")
    print(df.describe())
    
    print("\n--- Value Counts for Label ---")
    print(df['label'].value_counts())
    
    # Check for constant columns
    print("\n--- Standard Deviation ---")
    print(df.std(numeric_only=True))

    # Correlations
    print("\n--- Correlation with Label (Numeric approx) ---")
    df_numeric = df.select_dtypes(include=['number']).copy()
    from sklearn.preprocessing import LabelEncoder
    le = LabelEncoder()
    df_numeric['label_enc'] = le.fit_transform(df['label'])
    print(df_numeric.corr()['label_enc'].sort_values())

if __name__ == "__main__":
    check_quality()
