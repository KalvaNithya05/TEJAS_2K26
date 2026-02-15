import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
try:
    df = pd.read_csv(r"d:\Projects\TEJAS_2K26\backend\ml\data\mitti_mitra_masterall_india_dataset.csv")
    for col in df.columns:
        print(col)
except Exception as e:
    print(e)
