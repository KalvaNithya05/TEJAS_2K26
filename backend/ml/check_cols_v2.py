import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
try:
    df = pd.read_csv(r"d:\Projects\mitti mitra\data\mitti_mitra_master_dataset_all_india.csv")
    for col in df.columns:
        print(col)
except Exception as e:
    print(e)
