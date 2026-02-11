import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

df = pd.read_csv('c:/Users/NITHYA/mitti_mitra/data/mitti_mitra_master_dataset_all_india.csv')
X = df.drop('crop', axis=1)
y = df['crop']

le = LabelEncoder()
for col in X.columns:
    if X[col].dtype == 'object':
        X[col] = le.fit_transform(X[col].astype(str))

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
dt = DecisionTreeClassifier()
dt.fit(X_train, y_train)

print(f"Accuracy with ALL columns: {dt.score(X_test, y_test):.4f}")

importances = pd.Series(dt.feature_importances_, index=X.columns)
print("\nFeature Importances:")
print(importances.sort_values(ascending=False))
