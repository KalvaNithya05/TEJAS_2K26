import pandas as pd
try:
    df = pd.read_csv(r"d:\Projects\TEJAS_2K26\backend\ml\data\mitti_mitra_all_india_dataset.csv")
    print("Columns:", list(df.columns))
except Exception as e:
    print(e)
