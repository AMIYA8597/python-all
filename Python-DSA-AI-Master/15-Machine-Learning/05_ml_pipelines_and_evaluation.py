"""
ML Pipelines, Feature Engineering, and Evaluation Metrics
This script covers:
1. Feature Engineering (Scaling, Imputation, Encoding)
2. ML Pipelines
3. Evaluation Metrics (Confusion Matrix, ROC AUC)
"""

from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report, roc_auc_score
from sklearn.datasets import make_classification
import pandas as pd
import numpy as np

def pipeline_and_evaluation_example():
    print("--- ML Pipelines & Feature Engineering ---")
    
    # Create dummy DataFrame representing a realistic dataset
    # We will generate 100 rows to ensure robust evaluation
    np.random.seed(42)
    
    n_samples = 100
    age = np.random.randint(20, 60, size=n_samples).astype(float)
    # inject some NaNs
    age[np.random.choice(n_samples, 10, replace=False)] = np.nan
    
    salary = np.random.randint(40000, 120000, size=n_samples).astype(float)
    department = np.random.choice(['IT', 'HR', 'Marketing', 'Sales'], size=n_samples)
    
    # target variable logic (simplistic)
    promoted = ((age > 30) & (salary > 80000)).astype(int)
    
    df = pd.DataFrame({'age': age, 'salary': salary, 'department': department, 'promoted': promoted})
    
    X = df.drop('promoted', axis=1)
    y = df['promoted']
    
    # Define Numerical and Categorical features
    numeric_features = ['age', 'salary']
    categorical_features = ['department']
    
    # 1. Feature Engineering Transformers
    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])
    
    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])
    
    # Combine using ColumnTransformer
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)
        ])
        
    # 2. Build Pipeline
    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', RandomForestClassifier(random_state=42))
    ])
    
    # Split Data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    
    # Train
    pipeline.fit(X_train, y_train)
    print("Pipeline trained successfully!")
    
    # 3. Evaluation
    print("\n--- Evaluation Metrics ---")
    y_pred = pipeline.predict(X_test)
    y_prob = pipeline.predict_proba(X_test)[:, 1]
    
    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))
    
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    try:
        auc = roc_auc_score(y_test, y_prob)
        print(f"ROC AUC Score: {auc:.3f}")
    except ValueError:
        print("ROC AUC Score: Not enough classes in test set to calculate ROC AUC.")

if __name__ == "__main__":
    pipeline_and_evaluation_example()
