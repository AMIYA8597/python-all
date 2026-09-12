"""
Module: 02-sklearn-pipeline
Description: Comprehensive, textbook-grade interactive lesson on Scikit-Learn Pipelines.

=========================================================================================
LEARNING OBJECTIVES:
1. Understand the mathematical and structural purpose of Scikit-Learn Pipelines.
2. Master `Pipeline`, `make_pipeline`, `ColumnTransformer`, and `FeatureUnion`.
3. Build custom transformers using `BaseEstimator` and `TransformerMixin`.
4. Perform hyperparameter tuning on pipelines using `GridSearchCV`.
5. Analyze the time and space complexity (Big-O) of pipeline operations.
6. Apply pipelines to real-world, heterogeneous datasets.

=========================================================================================
MATHEMATICAL BACKGROUND:

A machine learning pipeline conceptually maps raw data $X$ to predictions $\hat{y}$ through a
composition of functions:

    f(X) = M(T_n(T_{n-1}(...T_1(X)...)))

Where:
- $T_i$ represents a data transformation step (e.g., scaling, imputation, encoding).
- $M$ represents the final estimator (model) that makes predictions.

During the `fit` phase, parameters for each $T_i$ are learned sequentially:
    X_1 = T_1.fit_transform(X)
    X_2 = T_2.fit_transform(X_1)
    ...
    M.fit(X_n, y)

During the `predict` phase, the learned parameters are applied:
    X_1 = T_1.transform(X)
    X_2 = T_2.transform(X_1)
    ...
    \hat{y} = M.predict(X_n)

This structure prevents **data leakage** because statistics used for scaling or imputing
are learned strictly from the training set and rigidly applied to the validation/test sets.

=========================================================================================
BIG-O ANALYSIS:

Let $N$ be the number of samples, $D$ be the number of features, and $P$ be the number
of pipeline steps.
- Time Complexity (Fitting): $O(\sum_{i=1}^{P-1} \text{Time}(T_i) + \text{Time}(M))$.
  For standard scaling: $O(N \times D)$. For imputation: $O(N \times D)$.
  Thus, data preprocessing is usually linear with respect to dataset size.
- Space Complexity: $O(N \times D)$ to store intermediate transformed arrays in memory,
  though Scikit-Learn pipelines process in a memory-efficient manner when possible.

=========================================================================================
REAL-WORLD APPLICATIONS:
- Productionizing Machine Learning models where raw data streams directly to the API.
- Simplifying cross-validation by ensuring no leakage occurs across folds.
- Handling complex text processing and tabular data simultaneously via FeatureUnions.
"""

import time
import logging
from typing import Any, Dict, List, Tuple, Union, Optional

import numpy as np
import pandas as pd

# Scikit-Learn Imports
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder, MinMaxScaler
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.datasets import make_classification

# Configure logging for the interactive lesson
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


# =======================================================================================
# 1. CUSTOM TRANSFORMERS
# =======================================================================================

class OutlierCapper(BaseEstimator, TransformerMixin):
    """
    A Custom Transformer to cap outliers at a specified quantile.
    Demonstrates how to build proprietary logic into the Scikit-Learn ecosystem.
    
    Mathematical Concept:
    For a feature $x$, any value $x_i > Q_q(x)$ is set to $Q_q(x)$,
    and $x_i < Q_{1-q}(x)$ is set to $Q_{1-q}(x)$, where $Q$ is the quantile function.
    """
    
    def __init__(self, lower_quantile: float = 0.05, upper_quantile: float = 0.95):
        """
        Initialize the OutlierCapper.
        
        Args:
            lower_quantile (float): The lower percentile (e.g., 0.05 for 5th percentile).
            upper_quantile (float): The upper percentile (e.g., 0.95 for 95th percentile).
        """
        self.lower_quantile = lower_quantile
        self.upper_quantile = upper_quantile
        self.lower_bounds_: Optional[np.ndarray] = None
        self.upper_bounds_: Optional[np.ndarray] = None
        
    def fit(self, X: Union[pd.DataFrame, np.ndarray], y: Optional[Any] = None) -> "OutlierCapper":
        """
        Learns the quantiles from the training data.
        
        Args:
            X: Input data of shape (n_samples, n_features).
            y: Target values (ignored).
            
        Returns:
            self
        """
        # Convert to numpy array for uniformity
        X_arr = X.to_numpy() if isinstance(X, pd.DataFrame) else X
        
        # Calculate limits column-wise (axis=0)
        self.lower_bounds_ = np.nanquantile(X_arr, self.lower_quantile, axis=0)
        self.upper_bounds_ = np.nanquantile(X_arr, self.upper_quantile, axis=0)
        return self

    def transform(self, X: Union[pd.DataFrame, np.ndarray]) -> np.ndarray:
        """
        Caps the data based on the fitted quantiles.
        
        Args:
            X: Input data to be transformed.
            
        Returns:
            Transformed numpy array.
        """
        if self.lower_bounds_ is None or self.upper_bounds_ is None:
            raise RuntimeError("Transformer must be fitted before calling transform().")
            
        X_arr = X.to_numpy() if isinstance(X, pd.DataFrame) else X
        # Apply clipping
        X_capped = np.clip(X_arr, self.lower_bounds_, self.upper_bounds_)
        return X_capped


class LogTransformer(BaseEstimator, TransformerMixin):
    """
    Custom transformer to apply logarithmic scaling.
    Useful for highly right-skewed data distributions.
    
    Equation:
    $X' = \ln(X + 1)$
    """
    
    def fit(self, X: Any, y: Any = None) -> "LogTransformer":
        # No state needs to be learned for a static log transform
        return self
        
    def transform(self, X: Union[pd.DataFrame, np.ndarray]) -> np.ndarray:
        X_arr = X.to_numpy() if isinstance(X, pd.DataFrame) else X
        # Add 1 to avoid log(0)
        return np.log1p(np.maximum(X_arr, 0))


# =======================================================================================
# 2. DATA GENERATION
# =======================================================================================

def generate_mock_data(n_samples: int = 1000) -> pd.DataFrame:
    """
    Generates a realistic heterogeneous dataset with missing values and mixed types.
    """
    np.random.seed(42)
    
    # Numerical feature 1: Normal distribution
    age = np.random.normal(45, 15, n_samples)
    
    # Numerical feature 2: Right-skewed distribution (needs log transform or clipping)
    income = np.random.exponential(50000, n_samples)
    
    # Categorical feature 1: Binary
    gender = np.random.choice(['Male', 'Female', np.nan], size=n_samples, p=[0.48, 0.48, 0.04])
    
    # Categorical feature 2: Multi-class
    city = np.random.choice(['New York', 'London', 'Tokyo', 'Paris'], size=n_samples)
    
    # Target variable (Binary Classification based on a hidden function)
    # y = 1 if (age > 40 AND income > 60000) OR city == 'Tokyo'
    y = ((age > 40) & (income > 60000)) | (city == 'Tokyo')
    # Add some noise to target
    noise = np.random.choice([True, False], size=n_samples, p=[0.1, 0.9])
    y = np.where(noise, ~y, y).astype(int)
    
    df = pd.DataFrame({
        'Age': age,
        'Income': income,
        'Gender': gender,
        'City': city,
        'Target': y
    })
    
    # Introduce random missing values in Income and Age
    df.loc[np.random.choice(df.index, size=int(n_samples*0.05)), 'Income'] = np.nan
    df.loc[np.random.choice(df.index, size=int(n_samples*0.05)), 'Age'] = np.nan
    
    return df


# =======================================================================================
# 3. PIPELINE LESSONS
# =======================================================================================

def lesson_1_basic_pipeline() -> None:
    """
    LESSON 1: The Basic Pipeline
    Demonstrates sequential transformations on homogeneous data.
    """
    print("\n" + "="*60)
    print("LESSON 1: BASIC PIPELINE (Homogeneous Data)")
    print("="*60)
    
    # Generate simple numerical data
    X, y = make_classification(n_samples=500, n_features=5, random_state=42)
    
    # Introduce missing values
    X[0:50, 0] = np.nan 
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Create pipeline: Impute missing -> Scale -> Classify
    # The string names are used to access parameters later
    basic_pipe = Pipeline([
        ('imputer', SimpleImputer(strategy='mean')),
        ('scaler', StandardScaler()),
        ('classifier', LogisticRegression())
    ])
    
    print("Pipeline Structure:")
    for name, step in basic_pipe.steps:
        print(f"  -> {name}: {step.__class__.__name__}")
        
    start_time = time.time()
    
    # fit_transform on steps 1,2; fit on step 3
    basic_pipe.fit(X_train, y_train)
    
    # transform on steps 1,2; predict on step 3
    y_pred = basic_pipe.predict(X_test)
    
    acc = accuracy_score(y_test, y_pred)
    print(f"\nExecution Time: {time.time() - start_time:.4f}s")
    print(f"Test Accuracy: {acc:.4f}")
    print("Key Takeaway: The scaler learned its mean and variance ONLY from X_train.\n")


def lesson_2_column_transformer(df: pd.DataFrame) -> None:
    """
    LESSON 2: ColumnTransformer
    Applying different preprocessing steps to different subsets of features.
    """
    print("\n" + "="*60)
    print("LESSON 2: COLUMN TRANSFORMER (Heterogeneous Data)")
    print("="*60)
    
    X = df.drop(columns=['Target'])
    y = df['Target']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Define feature groups
    numeric_features_standard = ['Age']
    numeric_features_skewed = ['Income']
    categorical_features = ['Gender', 'City']
    
    # Sub-pipeline for standard numeric features
    numeric_std_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])
    
    # Sub-pipeline for skewed numeric features (using our Custom Transformer)
    numeric_skew_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('capper', OutlierCapper(lower_quantile=0.01, upper_quantile=0.99)),
        ('log', LogTransformer()),
        ('scaler', MinMaxScaler()) # Scaled to [0,1]
    ])
    
    # Sub-pipeline for categorical features
    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])
    
    # Combine sub-pipelines using ColumnTransformer
    preprocessor = ColumnTransformer(
        transformers=[
            ('num_std', numeric_std_transformer, numeric_features_standard),
            ('num_skew', numeric_skew_transformer, numeric_features_skewed),
            ('cat', categorical_transformer, categorical_features)
        ],
        remainder='drop' # or 'passthrough'
    )
    
    # Full end-to-end pipeline
    full_pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', RandomForestClassifier(n_estimators=50, random_state=42))
    ])
    
    print("Fitting the complex ColumnTransformer Pipeline...")
    full_pipeline.fit(X_train, y_train)
    
    y_pred = full_pipeline.predict(X_test)
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))


def lesson_3_hyperparameter_tuning(df: pd.DataFrame) -> None:
    """
    LESSON 3: GridSearchCV with Pipelines
    Tuning both preprocessing parameters and model hyperparameters simultaneously.
    """
    print("\n" + "="*60)
    print("LESSON 3: PIPELINE HYPERPARAMETER TUNING")
    print("="*60)
    
    X = df[['Age', 'Income']].copy() # Simplified to numeric for speed
    y = df['Target']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Pipeline using make_pipeline (automatically names steps as lowercase class names)
    pipe = Pipeline([
        ('imputer', SimpleImputer()),
        ('scaler', StandardScaler()),
        ('clf', LogisticRegression())
    ])
    
    # Parameter grid syntax: stepname__parametername
    param_grid = {
        'imputer__strategy': ['mean', 'median'],
        'scaler': [StandardScaler(), MinMaxScaler()], # You can swap entire steps!
        'clf__C': [0.1, 1.0, 10.0]
    }
    
    print("GridSearch Parameter Space:")
    for k, v in param_grid.items():
        print(f"  {k}: {v}")
        
    grid_search = GridSearchCV(pipe, param_grid, cv=3, scoring='accuracy', n_jobs=-1)
    
    start_time = time.time()
    print("\nStarting GridSearch (this may take a moment)...")
    grid_search.fit(X_train, y_train)
    print(f"GridSearch completed in {time.time() - start_time:.2f}s")
    
    print(f"\nBest Parameters Found: {grid_search.best_params_}")
    print(f"Best Cross-Validation Score: {grid_search.best_score_:.4f}")
    
    # The best model is automatically refitted on the entire training set
    test_score = grid_search.score(X_test, y_test)
    print(f"Test Set Score with Best Estimator: {test_score:.4f}")


def lesson_4_big_o_and_performance() -> None:
    """
    LESSON 4: Algorithm Analysis and Edge Cases
    """
    print("\n" + "="*60)
    print("LESSON 4: PERFORMANCE ANALYSIS & EDGE CASES")
    print("="*60)
    
    analysis_text = """
    1. Time Complexity Breakdown:
       - Fitting Imputer: O(N * D) to compute means/medians.
       - Fitting Scaler: O(N * D) to compute variance.
       - Model Training (e.g., Logistic Regression): O(N * D * Iterations)
       Total Fit Time: O(N*D + N*D*Iter). Extremely scalable.
       
    2. Edge Cases to Handle:
       - Unknown Categorical Classes in Production:
         Use `OneHotEncoder(handle_unknown='ignore')` to prevent crashes when 
         the prediction data contains categories unseen during training.
       - Data Leakage:
         Never call `fit_transform` on the test set or validation set. 
         Pipelines inherently protect against this if used correctly.
         
    3. Statefulness:
       - Scikit-Learn transformers hold state (e.g., `imputer.statistics_`).
       - If you modify the pipeline inplace after fitting, you risk corrupting the state.
    """
    print(analysis_text)


def run_tests() -> None:
    """
    Unit testing to ensure the custom transformers operate correctly mathematically.
    """
    print("\n" + "="*60)
    print("RUNNING PIPELINE TESTS")
    print("="*60)
    
    # Test OutlierCapper
    test_data = pd.DataFrame({'val': [1, 2, 3, 4, 1000, -1000]})
    capper = OutlierCapper(lower_quantile=0.1, upper_quantile=0.9)
    res = capper.fit_transform(test_data)
    
    assert res.max() < 1000, "OutlierCapper failed to cap upper bound"
    assert res.min() > -1000, "OutlierCapper failed to cap lower bound"
    print(" [PASS] Custom Transformer 'OutlierCapper' validated.")
    
    # Test LogTransformer
    log_t = LogTransformer()
    test_arr = np.array([[0, e - 1] for e in [np.e, np.e**2]]) # Adding constants
    res_log = log_t.transform(test_arr)
    assert np.allclose(res_log[0, 1], 1.0), "LogTransformer math incorrect"
    print(" [PASS] Custom Transformer 'LogTransformer' validated.")
    
    print("\nAll pipeline architecture tests passed successfully!")


if __name__ == "__main__":
    print(f"\n{'='*20} INTERACTIVE LESSON: SCIKIT-LEARN PIPELINES {'='*20}\n")
    
    # Prepare Mock Data
    print("Generating comprehensive dataset for the lesson...")
    df_mock = generate_mock_data(n_samples=2000)
    print(f"Dataset Shape: {df_mock.shape}\n")
    
    # Execute Modules
    lesson_1_basic_pipeline()
    lesson_2_column_transformer(df_mock)
    lesson_3_hyperparameter_tuning(df_mock)
    lesson_4_big_o_and_performance()
    run_tests()
    
    print(f"\n{'='*20} END OF LESSON {'='*20}\n")
