import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

def best_possible():
    df = pd.read_csv('c:/Users/NITHYA/mitti_mitra/data/mitti_mitra_master_dataset_all_india.csv')
    le = LabelEncoder()
    
    # Encode ALL objects
    for col in df.columns:
        if df[col].dtype == 'object' and col != 'crop':
            df[col] = le.fit_transform(df[col].astype(str))
            
    X = df.drop('crop', axis=1)
    y = df['crop']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    rf.fit(X_train, y_train)
    
    print(f"Accuracy with ALL columns: {rf.score(X_test, y_test):.4f}")
    
    # Feature importances
    importances = pd.Series(rf.feature_importances_, index=X.columns).sort_values(ascending=False)
    print("\nFeature Importances:")
    print(importances)

if __name__ == "__main__":
    best_possible()
