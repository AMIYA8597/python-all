"""
# 05 - Machine Learning: Pipelines, Data Leakage, and Evaluation Metrics

## A. Concept Name
ML Pipelines, Feature Engineering, and Model Evaluation (Precision, Recall, ROC-AUC).

## B. One-Sentence Definition
Machine learning isn't just `model.fit()`; it requires rigorous, reproducible pipelines to prevent data leakage, and sophisticated evaluation metrics to understand exactly *how* a model fails in the real world.

## C. Why Does This Exist?
1. **Pipelines**: If you impute missing values or scale your data BEFORE splitting into Train/Test, your Test set has secretly influenced your Train set (Data Leakage). Your model will look amazing in testing, and fail immediately in production. Pipelines guarantee the test set is completely isolated.
2. **Evaluation Metrics**: "99% Accuracy" is useless if you are predicting a disease that affects 1% of the population (a model that just says "No" every time is 99% accurate, but 100% useless). We need Precision and Recall to measure true effectiveness.

## D. Intuition & Real-World Analogy
- **Data Leakage**: A teacher gives you the answers to the final exam while you are studying. You get an A+. But in the real world, you know nothing.
- **Precision**: The "Boy Who Cried Wolf" metric. Out of all the times you yelled "WOLF!" (Predicted Positive), how many times was there actually a wolf? (High precision = You don't cry wolf).
- **Recall**: The "Security Guard" metric. Out of all the ACTUAL thieves (Actual Positives), how many did you catch? (High recall = No thief escapes).

## E. Core Mathematical Concepts

### 1. The Confusion Matrix
- **True Positive (TP)**: Sick person correctly diagnosed as sick.
- **False Positive (FP)**: Healthy person incorrectly diagnosed as sick (Type I Error).
- **True Negative (TN)**: Healthy person correctly diagnosed as healthy.
- **False Negative (FN)**: Sick person incorrectly diagnosed as healthy (Type II Error - Often fatal!).

### 2. The Metrics
- **Accuracy**: `(TP + TN) / Total`
- **Precision**: `TP / (TP + FP)` (When I flag it, am I right?)
- **Recall (Sensitivity)**: `TP / (TP + FN)` (Did I miss any?)
- **F1-Score**: Harmonic mean of Precision and Recall. `2 * (P * R) / (P + R)`. Used when you care about both.

## F. Common Mistakes & Anti-Patterns
1. **Imputing before Splitting**: `df = df.fillna(df.mean()) -> train_test_split()`. WRONG! The `df.mean()` includes data from the test set. 
   **Fix**: `train_test_split() -> imputer.fit(train) -> imputer.transform(train/test)`. Scikit-learn `Pipeline` does this automatically!
2. **Using Accuracy for Imbalanced Data**: Predicting credit card fraud (0.1% of transactions). A dumb model predicting 0 always gets 99.9% accuracy.

## G. Interview Connection
**Q: "If you are building a cancer detection model, do you care more about Precision or Recall?"**
A: "Recall. A False Negative (missing cancer) means the patient dies. A False Positive (low precision) just means the patient gets a follow-up test. We want to maximize Recall, even if Precision drops slightly."

## H. Implementation & Guided Practice
"""

from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report, roc_auc_score
import pandas as pd
import numpy as np

def run_pipeline_masterclass():
    print("--- 1. Building a Bulletproof ML Pipeline ---")
    
    # 1. Generate Realistic Imbalanced Data
    np.random.seed(42)
    n_samples = 1000
    
    # Features
    age = np.random.normal(40, 10, size=n_samples)
    salary = np.random.normal(60000, 20000, size=n_samples)
    department = np.random.choice(['IT', 'HR', 'Marketing', 'Sales'], size=n_samples)
    
    # Target: "Promoted". Let's make it rare (Imbalanced!)
    # Logic: High salary and High age are more likely to be promoted, but it's noisy.
    prob = 1 / (1 + np.exp(-((age - 40)*0.1 + (salary - 60000)*0.0001 - 3)))
    promoted = np.random.binomial(1, prob)
    
    # Inject missing values (NaNs) AFTER creating the target so prob doesn't break
    age[np.random.choice(n_samples, 50, replace=False)] = np.nan
    salary[np.random.choice(n_samples, 50, replace=False)] = np.nan
    
    df = pd.DataFrame({'age': age, 'salary': salary, 'department': department, 'promoted': promoted})
    
    print(f"Dataset generated: {n_samples} rows.")
    print(f"Target Distribution:\n{df['promoted'].value_counts(normalize=True) * 100}")
    
    # 2. Split Data FIRST (Prevent Data Leakage)
    X = df.drop('promoted', axis=1)
    y = df['promoted']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # 3. Define the Blueprint for Feature Engineering
    numeric_features = ['age', 'salary']
    categorical_features = ['department']
    
    # Numeric pipeline: Impute missing with Median -> Scale to Mean 0, Std 1
    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])
    
    # Categorical pipeline: Impute missing with 'Unknown' -> One-Hot Encode
    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='constant', fill_value='Unknown')),
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])
    
    # Combine both into a ColumnTransformer
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)
        ])
        
    # 4. Define the Final Pipeline (Preprocessor -> Model)
    # class_weight='balanced' forces the Random Forest to care about the rare class!
    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', RandomForestClassifier(random_state=42, class_weight='balanced'))
    ])
    
    # 5. Train!
    # Because we use a pipeline, `fit()` calculates the median and scaling factors 
    # ONLY on the training data. The test data remains perfectly untouched.
    pipeline.fit(X_train, y_train)
    print("\nPipeline trained successfully without Data Leakage!")
    
    # 6. Evaluate
    print("\n--- 2. Evaluation Metrics ---")
    # `predict()` automatically applies the median and scaling factors learned from the Train set to the Test set.
    y_pred = pipeline.predict(X_test)
    y_prob = pipeline.predict_proba(X_test)[:, 1]
    
    print("Confusion Matrix:")
    cm = confusion_matrix(y_test, y_pred)
    print(f"True Negatives (TN): {cm[0][0]}  |  False Positives (FP): {cm[0][1]}")
    print(f"False Negatives (FN): {cm[1][0]}  |  True Positives (TP):  {cm[1][1]}")
    
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    auc = roc_auc_score(y_test, y_prob)
    print(f"ROC-AUC Score: {auc:.3f} (1.0 is perfect, 0.5 is random guessing)")


## I. Active Recall Questions
"""
1. What is Data Leakage?
   *Answer: When information from the test dataset accidentally influences the training process (e.g., calculating the global mean to fill NaNs before splitting). The model "cheats" and looks better than it actually is.*
2. In a spam filter, what is a False Positive?
   *Answer: A legitimate email (Negative) that is incorrectly flagged as Spam (Positive).*
3. Why use an ML Pipeline instead of manually transforming the data step-by-step?
   *Answer: Pipelines guarantee that transformations are applied consistently to Train, Test, and future Production data, eliminating the risk of data leakage and simplifying deployment.*
"""

if __name__ == "__main__":
    print("========== ML PIPELINES & EVALUATION MASTERCLASS ==========\n")
    run_pipeline_masterclass()
    print("\n========== MASTERCLASS COMPLETE ==========")
