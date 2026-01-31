import pandas as pd 
import numpy as np
import os 
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
import joblib
os.makedirs("models", exist_ok=True)
MODEL_DIR = "models/"

def train():
    df = pd.read_csv('data/final_dataset.csv')
    X = df.drop('churn', axis=1)
    y = df['churn'].values

    X_train, X_test, y_train, y_test = train_test_split(X,y,test_size = 0.30, random_state = 40, stratify=y)

    # 1. Logistic Regression
    scaler = StandardScaler()
    X_scaled_train = scaler.fit_transform(X_train)
    X_scaled_test = scaler.transform(X_test)
    
    logreg = LogisticRegression(max_iter=1000, class_weight="balanced")
    logreg.fit(X_scaled_train, y_train)

    # 2. Random Forest
    rf = RandomForestClassifier(n_estimators=200, random_state=42, class_weight="balanced", max_leaf_nodes=30)
    rf.fit(X_train, y_train)

    # Exporting
    joblib.dump(rf, MODEL_DIR + 'random_forest_model.pkl')
    joblib.dump(logreg, MODEL_DIR + 'logistic_regression_model.pkl')
    joblib.dump(scaler, MODEL_DIR + 'scaler.pkl')
    print("Models saved!")


if __name__ == "__main__":
    train()