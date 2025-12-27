import pandas as pd
try:
    df = pd.read_csv(r"d:\Projects\mitti mitra\data\mitti_mitra_master_dataset_all_india.csv")
    print("Columns:", list(df.columns))
except Exception as e:
    print(e)
