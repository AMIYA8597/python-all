"""
# ==============================================================================
# LABORATORY: ADVANCED PIPELINES & COLUMN TRANSFORMERS
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Real-world data is a disaster. It is a mix of Text categories ("Red", "Blue"), 
# missing values (NaN), and numerical scales (Age=50, Salary=100000).
#
# If you try to preprocess this manually using Pandas, your code becomes an 
# unmaintainable nightmare. Worse, when you deploy the model to production, 
# you have to exactly replicate that massive block of Pandas code to preprocess 
# the live data coming from the user!
#
# Scikit-Learn `Pipeline` and `ColumnTransformer` solve this. They allow you 
# to mathematically bind the Preprocessing Steps (Imputers, Scalers, One-Hot 
# Encoders) directly to the Machine Learning Model (Random Forest).
#
# When you save the Pipeline object, you are saving the ENTIRE preprocessing 
# engine alongside the model. In production, you just pass raw, dirty JSON 
# directly into `pipeline.predict()`, and it handles everything automatically.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand One-Hot Encoding for categorical data.
# - Construct a `ColumnTransformer` to split numeric/categorical processing.
# - Build an end-to-end unified `Pipeline` for seamless production deployment.
#
# ==============================================================================
"""

import numpy as np
import pandas as pd

# In a real environment: pip install scikit-learn
try:
    from sklearn.model_selection import train_test_split
    from sklearn.compose import ColumnTransformer
    from sklearn.pipeline import Pipeline
    from sklearn.impute import SimpleImputer
    from sklearn.preprocessing import StandardScaler, OneHotEncoder
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.metrics import accuracy_score
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. GENERATING REAL-WORLD DIRTY DATA
# ==============================================================================
def get_dirty_data():
    """Generates a dataset simulating dirty, mixed-type, missing real-world data."""
    rng = np.random.default_rng(42)
    
    # 500 rows
    n = 500
    
    # Numeric features (with NaNs!)
    age = rng.uniform(20, 80, n)
    age[rng.choice(n, 20, replace=False)] = np.nan # Inject missing ages
    
    salary = rng.uniform(30000, 150000, n)
    
    # Categorical features
    cities = rng.choice(["New York", "London", "Tokyo", "Paris"], n)
    
    # Target (High Net Worth: Salary > 80k AND Age > 40)
    # We add noise so it's not a perfect deterministic split
    target = ((salary > 80000) & (age > 40)).astype(int)
    flip_indices = rng.choice(n, 30, replace=False)
    target[flip_indices] = 1 - target[flip_indices] # Add 30 random flips
    
    df = pd.DataFrame({
        "Age": age,
        "Salary": salary,
        "City": cities
    })
    
    return df, target


# ==============================================================================
# 4. THE COLUMN TRANSFORMER
# ==============================================================================
def demonstrate_columntransformer():
    section_header("The ColumnTransformer Engine")
    
    if not HAS_SKLEARN:
        print("[WARNING] Scikit-Learn not installed.")
        return
        
    print("Machine Learning algorithms CANNOT read the string 'New York'.")
    print("We must convert categories to binary vectors using One-Hot Encoding.")
    print("But we only want to encode the 'City' column, and we want to Scale ")
    print("the 'Age' and 'Salary' columns. The ColumnTransformer does this simultaneously!\n")
    
    X, y = get_dirty_data()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 1. DEFINE COLUMN GROUPS
    numeric_features = ["Age", "Salary"]
    categorical_features = ["City"]
    
    # 2. DEFINE NUMERIC PREPROCESSING PIPELINE
    # Step A: Fill NaNs with the Median value
    # Step B: Scale to mean=0, var=1
    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])
    
    # 3. DEFINE CATEGORICAL PREPROCESSING PIPELINE
    # Step A: Fill NaNs with the word 'missing'
    # Step B: One-Hot Encode (New York -> [1, 0, 0, 0])
    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])
    
    # 4. COMBINE INTO A SINGLE COLUMN TRANSFORMER
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)
        ])
    
    # 5. ATTACH THE PREPROCESSOR TO THE FINAL MODEL
    # This is the master Pipeline object. It contains the Imputer, Scaler, 
    # One-Hot Encoder, AND the Random Forest Classifier all bound together!
    full_pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))
    ])
    
    print("Training the massive end-to-end Pipeline...")
    # Notice we pass the RAW DIRTY DATAFRAME directly to the fit method!
    full_pipeline.fit(X_train, y_train)
    
    # Notice we pass the RAW DIRTY TEST SET directly to the predict method!
    # No Pandas manual manipulation required!
    preds = full_pipeline.predict(X_test)
    
    acc = accuracy_score(y_test, preds)
    print(f"End-to-End Pipeline Accuracy: {acc*100:.1f}%\n")
    
    print("If you serialize this `full_pipeline` object using Joblib, you can load ")
    print("it onto a Web Server. When a user submits a raw JSON payload:")
    print("  {'Age': null, 'Salary': 95000, 'City': 'Tokyo'}")
    print("The pipeline will automatically impute the age, scale the numbers, ")
    print("one-hot encode the city, and generate the prediction in milliseconds!")


def run_all_labs():
    demonstrate_columntransformer()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. What is the fundamental danger of filling NaNs (Imputing) using Pandas `df.fillna(df.mean())` before using `train_test_split()`?
   Answer: DATA LEAKAGE! If you use Pandas to calculate the Mean of the entire column and fill the NaNs before splitting, the Mean contains mathematical information from the secret Test set! The Test set has mathematically "leaked" into the Training set. By using a Scikit-Learn `Pipeline` with a `SimpleImputer`, the imputer strictly calculates the Mean on the $X_{train}$ chunk during `.fit()`, and then safely uses that saved Train-Mean to fill NaNs in the $X_{test}$ chunk during `.predict()`, perfectly isolating the datasets.

2. Why do we use One-Hot Encoding (`[1,0,0], [0,1,0]`) for Cities instead of Label Encoding (`1, 2, 3`)?
   Answer: Machine Learning algorithms (like SVM or Linear Regression) interpret numbers geometrically. If you assign `New York = 1`, `London = 2`, and `Tokyo = 3`, the algorithm will mathematically assume that Tokyo is "greater than" New York, and that London is the exact midpoint between New York and Tokyo! This is mathematically absurd. One-Hot Encoding solves this by creating 3 independent binary columns (Is_NewYork, Is_London, Is_Tokyo). This ensures all cities are geometrically equidistant and mathematically independent in the model.

3. Why is `handle_unknown='ignore'` critical for One-Hot Encoders in production?
   Answer: In your training data, the City column contained New York, London, Tokyo, and Paris. The One-Hot Encoder created 4 binary columns. You deploy the Pipeline to a production server. A week later, a user submits a live transaction from "Berlin". If `handle_unknown='error'` is set, the entire Pipeline will crash with a KeyError because it has never seen Berlin! By setting `handle_unknown='ignore'`, the Pipeline safely assigns `[0, 0, 0, 0]` to all 4 known city columns and allows the Random Forest to continue processing the numeric data without crashing the server.
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Advanced Pipelines Completed.")
