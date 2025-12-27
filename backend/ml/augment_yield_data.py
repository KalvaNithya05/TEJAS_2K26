import pandas as pd
import os
import random

# Configuration
DATA_DIR = r"d:\Projects\mitti mitra\data"
INPUT_FILE = "crop_yield.csv"
OUTPUT_FILE = "crop_yield_updated.csv"

# Telangana Details
TELANGANA_DATA = {
    "State": "Telangana",
    "Districts": ["Hyderabad", "Warangal", "Karimnagar", "Nizamabad", "Khammam", "Adilabad"],
    "Crops": ["Rice", "Cotton", "Maize", "Chili", "Pulses"],
    "Soil_Types": ["Red Soil", "Black Soil"], # Note: Original dataset might not have Soil Type column, need to check
    # If original doesn't have Soil Type, we might need to rely on existing columns or add it.
    # Based on user request: "Add Telangana state details in crop_yeild dataset... Inputs: State, district, Crop, Soil type..."
    # So we MUST add Soil Type column if missing.
}

def load_data():
    path = os.path.join(DATA_DIR, INPUT_FILE)
    if not os.path.exists(path):
        print(f"File not found: {path}")
        return None
    return pd.read_csv(path)

def augment_data(df):
    # Check if 'Soil_Type' exists, if not create it with random/default values for existing data first
    # to maintain consistency, or just for new rows?
    # Better to add it to all.
    
    # 1. Normalize columns
    df.columns = [c.strip() for c in df.columns]
    
    # Check existing columns
    print("Existing columns:", df.columns.tolist())
    
    # 2. Generate Telangana Rows
    new_rows = []
    
    # Years to simulate
    years = range(2018, 2025)
    seasons = ["Kharif", "Rabi", "Whole Year"]
    
    for district in TELANGANA_DATA["Districts"]:
        for crop in TELANGANA_DATA["Crops"]:
            for year in years:
                season = random.choice(seasons)
                
                # Simulate data based on typical values (mock logic)
                area = random.uniform(1000, 50000) # Hectares
                yield_per_hectare = random.uniform(1.5, 5.0) # Tons/Hectare (Rice/Maize etc)
                production = area * yield_per_hectare
                
                rainfall = random.uniform(700, 1200) # mm
                fertilizer = random.uniform(100, 200) # kg/ha
                pesticide = random.uniform(0.5, 5.0) # kg/ha
                
                # Soil type assignment (simple random or logic)
                soil = random.choice(TELANGANA_DATA["Soil_Types"])
                
                row = {
                    "Crop": crop,
                    "Crop_Year": year,
                    "Season": season,
                    "State": "Telangana",
                    "Area": round(area, 2),
                    "Production": round(production, 2),
                    "Annual_Rainfall": round(rainfall, 1),
                    "Fertilizer": round(fertilizer, 2),
                    "Pesticide": round(pesticide, 2),
                    "Yield": round(yield_per_hectare, 2),
                     # Add extra columns required by user if not present
                    "District": district,
                    "Soil_Type": soil
                }
                new_rows.append(row)
                
    new_df = pd.DataFrame(new_rows)
    
    # 3. Merge with existing
    # Ensure existing df has same columns. If 'District' or 'Soil_Type' missing in original, add them with 'Unknown'
    if "District" not in df.columns:
        df["District"] = "Unknown"
    if "Soil_Type" not in df.columns:
        df["Soil_Type"] = "Unknown" # Or infer from State if possible, but keep simple
        
    combined_df = pd.concat([df, new_df], ignore_index=True)
    
    return combined_df

def main():
    df = load_data()
    if df is None:
        return
        
    updated_df = augment_data(df)
    
    output_path = os.path.join(DATA_DIR, OUTPUT_FILE)
    updated_df.to_csv(output_path, index=False)
    print(f"Saved updated dataset to {output_path}")
    print(f"Total rows: {len(updated_df)}")
    print(f"Telangana rows: {len(updated_df[updated_df['State'] == 'Telangana'])}")

if __name__ == "__main__":
    main()
