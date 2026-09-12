"""
===========================================================================
    01-sklearn-basics: A Textbook-Grade Interactive Lesson
===========================================================================

Welcome to the comprehensive, textbook-grade module on Scikit-Learn (sklearn)
basics. Scikit-Learn is the premier library in the Python ecosystem for 
machine learning, providing robust implementations of numerous classical 
machine learning algorithms, alongside powerful tools for data preprocessing,
model evaluation, and hyperparameter tuning.

### 1. Mathematical Background & Theoretical Foundations

Machine learning (ML) primarily involves finding a mapping function 
f(X) -> Y that minimizes a specific loss function over a dataset.

#### 1.1 Linear Regression
Linear Regression models the relationship between a dependent variable y 
and one or more independent variables X by fitting a linear equation.
  y_hat = w_0 + w_1*x_1 + w_2*x_2 + ... + w_n*x_n
where w represents the weights (coefficients) and w_0 is the bias (intercept).

Loss Function (Mean Squared Error):
  J(w) = (1 / 2m) * Σ(y_hat_i - y_i)^2
Objective: Minimize J(w) using Normal Equation or Gradient Descent.

#### 1.2 Logistic Regression
Despite its name, Logistic Regression is used for binary classification. 
It uses the logistic (sigmoid) function to map outputs to a probability 
between 0 and 1.
  σ(z) = 1 / (1 + e^(-z))
  y_hat = σ(w^T * X + b)

Loss Function (Binary Cross-Entropy or Log Loss):
  J(w) = - (1/m) * Σ[y_i * log(y_hat_i) + (1 - y_i) * log(1 - y_hat_i)]

#### 1.3 K-Nearest Neighbors (KNN)
KNN is a non-parametric, instance-based learning algorithm. To predict a 
new instance, it finds the 'K' closest samples in the training set and 
returns the majority vote (classification) or the average (regression).
Distance Metrics:
  Euclidean distance: d(p, q) = sqrt(Σ(p_i - q_i)^2)

#### 1.4 Decision Trees
Decision Trees partition the feature space into hyper-rectangles using 
splitting criteria like Gini Impurity or Entropy.
  Entropy(S) = - Σ p_i * log2(p_i)
  Gini(S) = 1 - Σ p_i^2

### 2. Algorithmic Complexity (Big-O Analysis)
| Algorithm            | Training Time | Prediction Time | Space Complexity |
|----------------------|---------------|-----------------|------------------|
| Linear Regression    | O(n^2 * m)    | O(n)            | O(n)             |
| Logistic Regression  | O(n * m * e)  | O(n)            | O(n)             |
| K-Nearest Neighbors  | O(1)          | O(n * m)        | O(n * m)         |
| Decision Trees       | O(n * m log m)| O(d)            | O(nodes)         |
* n = number of features, m = number of samples, e = epochs, d = depth.

### 3. Key Concepts in Scikit-Learn API
Scikit-Learn follows a highly consistent and elegant API design:
- `Estimator`: Any object that can estimate some parameters based on a 
  dataset (e.g., `model.fit(X, y)`).
- `Transformer`: Estimators that can transform a dataset 
  (e.g., `scaler.transform(X)` or `scaler.fit_transform(X)`).
- `Predictor`: Estimators that can make predictions 
  (e.g., `model.predict(X)` or `model.predict_proba(X)`).

### 4. Real-World Application
We will implement an end-to-end pipeline predicting a target variable 
with data generation, preprocessing, model training, and evaluation.
"""

import math
import time
import traceback
from typing import List, Dict, Any, Tuple, Optional, Callable

# Standard ML imports (usually numpy and pandas are expected alongside sklearn)
# For the sake of this lesson, we will rely on sklearn where available.
try:
    import numpy as np
    from sklearn.datasets import make_classification, make_regression
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import StandardScaler, MinMaxScaler
    from sklearn.linear_model import LinearRegression, LogisticRegression
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.metrics import (
        mean_squared_error, r2_score, accuracy_score, 
        precision_score, recall_score, f1_score
    )
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    print("WARNING: Scikit-Learn or NumPy is not installed. Some interactive parts will be skipped.")
    print("Please install via: pip install numpy scikit-learn")


# =============================================================================
# 1. DATA PREPARATION & PREPROCESSING
# =============================================================================

class DataPreprocessor:
    """
    A textbook example of data preprocessing. In machine learning, raw data 
    is rarely ready for immediate training. We must handle scaling, encoding, 
    and splitting.
    """
    
    @staticmethod
    def generate_classification_data(n_samples: int = 1000, n_features: int = 10) -> Tuple[Any, Any]:
        """
        Generates a synthetic classification dataset.
        
        Args:
            n_samples (int): Total number of samples.
            n_features (int): Total number of features per sample.
            
        Returns:
            Tuple[np.ndarray, np.ndarray]: Feature matrix X and target vector y.
        """
        if not SKLEARN_AVAILABLE:
            return None, None
            
        print(f"[*] Generating synthetic classification data ({n_samples} samples, {n_features} features)...")
        X, y = make_classification(
            n_samples=n_samples, 
            n_features=n_features,
            n_informative=int(n_features * 0.8),
            n_redundant=int(n_features * 0.2),
            random_state=42
        )
        return X, y

    @staticmethod
    def generate_regression_data(n_samples: int = 1000, n_features: int = 5) -> Tuple[Any, Any]:
        """
        Generates a synthetic regression dataset.
        """
        if not SKLEARN_AVAILABLE:
            return None, None
            
        print(f"[*] Generating synthetic regression data ({n_samples} samples, {n_features} features)...")
        X, y = make_regression(
            n_samples=n_samples, 
            n_features=n_features, 
            noise=10.0, 
            random_state=42
        )
        return X, y

    @staticmethod
    def split_and_scale(X: Any, y: Any, test_size: float = 0.2, scaler_type: str = 'standard') -> Tuple[Any, Any, Any, Any, Any]:
        """
        Splits the dataset into training and testing sets, then scales the features.
        
        Why Scaling? 
        Algorithms like KNN, SVM, and Neural Networks are distance-based or gradient-based. 
        Features with larger scales can dominate the objective function or distance calculation.
        
        StandardScaler: z = (x - u) / s
        MinMaxScaler: x_scaled = (x - x_min) / (x_max - x_min)
        
        Returns:
            X_train_scaled, X_test_scaled, y_train, y_test, scaler_object
        """
        if not SKLEARN_AVAILABLE:
            return None, None, None, None, None
            
        print(f"[*] Splitting data with test_size={test_size}")
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)
        
        if scaler_type == 'standard':
            scaler = StandardScaler()
        elif scaler_type == 'minmax':
            scaler = MinMaxScaler()
        else:
            raise ValueError("Unsupported scaler_type. Use 'standard' or 'minmax'.")
            
        print(f"[*] Applying {scaler.__class__.__name__} to feature matrices...")
        
        # Fit ONLY on the training data to prevent data leakage!
        # Transform BOTH training and testing data.
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        return X_train_scaled, X_test_scaled, y_train, y_test, scaler


# =============================================================================
# 2. MACHINE LEARNING MODELS (LINEAR & LOGISTIC REGRESSION)
# =============================================================================

class LinearModelsLesson:
    """
    Demonstrates Linear Models in Scikit-Learn.
    Linear models are extremely interpretable and serve as excellent baselines.
    """
    
    @staticmethod
    def train_linear_regression(X_train: Any, y_train: Any) -> Any:
        """
        Trains a classic Ordinary Least Squares (OLS) Linear Regression model.
        Time Complexity (Training): O(n^2 * m) where n=features, m=samples.
        """
        if not SKLEARN_AVAILABLE:
            return None
            
        print("\n[+] Training Linear Regression...")
        start_time = time.time()
        
        model = LinearRegression()
        model.fit(X_train, y_train)
        
        print(f"    - Training Time: {time.time() - start_time:.4f}s")
        print(f"    - Model Coefficients: {model.coef_[:3]}... (showing first 3)")
        print(f"    - Model Intercept: {model.intercept_:.4f}")
        return model

    @staticmethod
    def train_logistic_regression(X_train: Any, y_train: Any) -> Any:
        """
        Trains a Logistic Regression model for classification.
        Logistic Regression applies the sigmoid function to a linear combination of features.
        """
        if not SKLEARN_AVAILABLE:
            return None
            
        print("\n[+] Training Logistic Regression...")
        start_time = time.time()
        
        model = LogisticRegression(max_iter=1000, random_state=42)
        model.fit(X_train, y_train)
        
        print(f"    - Training Time: {time.time() - start_time:.4f}s")
        print(f"    - Classes: {model.classes_}")
        return model


# =============================================================================
# 3. NON-LINEAR & INSTANCE-BASED MODELS
# =============================================================================

class NonLinearModelsLesson:
    """
    Demonstrates Non-Linear classification models.
    """
    
    @staticmethod
    def train_knn(X_train: Any, y_train: Any, k: int = 5) -> Any:
        """
        Trains a K-Nearest Neighbors Classifier.
        Remember: KNN has virtually no training time, but high prediction time O(m*n).
        """
        if not SKLEARN_AVAILABLE:
            return None
            
        print(f"\n[+] Training K-Nearest Neighbors (k={k})...")
        start_time = time.time()
        
        model = KNeighborsClassifier(n_neighbors=k, n_jobs=-1)
        model.fit(X_train, y_train)
        
        print(f"    - 'Training' Time (storing data): {time.time() - start_time:.4f}s")
        return model

    @staticmethod
    def train_decision_tree(X_train: Any, y_train: Any, max_depth: int = 5) -> Any:
        """
        Trains a Decision Tree Classifier.
        Decision trees recursively partition the data based on information gain.
        """
        if not SKLEARN_AVAILABLE:
            return None
            
        print(f"\n[+] Training Decision Tree Classifier (max_depth={max_depth})...")
        start_time = time.time()
        
        model = DecisionTreeClassifier(max_depth=max_depth, random_state=42)
        model.fit(X_train, y_train)
        
        print(f"    - Training Time: {time.time() - start_time:.4f}s")
        print(f"    - Tree Depth: {model.get_depth()}")
        print(f"    - Number of Leaves: {model.get_n_leaves()}")
        return model


# =============================================================================
# 4. MODEL EVALUATION
# =============================================================================

class EvaluationMetricsLesson:
    """
    Covers exhaustive evaluation metrics for both regression and classification.
    """
    
    @staticmethod
    def evaluate_regression(model: Any, X_test: Any, y_test: Any) -> Dict[str, float]:
        """
        Evaluates a regression model using MSE and R^2 score.
        """
        if not SKLEARN_AVAILABLE:
            return {}
            
        y_pred = model.predict(X_test)
        
        mse = mean_squared_error(y_test, y_pred)
        rmse = math.sqrt(mse)
        r2 = r2_score(y_test, y_pred)
        
        print(f"    [!] Regression Metrics: RMSE={rmse:.4f}, R^2={r2:.4f}")
        return {"rmse": rmse, "r2": r2}

    @staticmethod
    def evaluate_classification(model: Any, X_test: Any, y_test: Any) -> Dict[str, float]:
        """
        Evaluates a classification model using Accuracy, Precision, Recall, and F1.
        """
        if not SKLEARN_AVAILABLE:
            return {}
            
        start_time = time.time()
        y_pred = model.predict(X_test)
        predict_time = time.time() - start_time
        
        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred, average='weighted', zero_division=0)
        rec = recall_score(y_test, y_pred, average='weighted', zero_division=0)
        f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)
        
        print(f"    [!] Classification Metrics (Accuracy: {acc:.4f}, F1: {f1:.4f}) | Pred Time: {predict_time:.4f}s")
        return {"accuracy": acc, "precision": prec, "recall": rec, "f1": f1, "predict_time": predict_time}


# =============================================================================
# 5. REAL WORLD APPLICATION PIPELINE
# =============================================================================

def run_real_world_pipeline() -> None:
    """
    Orchestrates a full Machine Learning workflow from data generation to evaluation.
    This simulates a real-world scenario where multiple models are compared.
    """
    if not SKLEARN_AVAILABLE:
        print("Skipping real-world pipeline (Scikit-Learn not installed).")
        return
        
    print("\n" + "="*60)
    print("🚀 STARTING REAL-WORLD ML PIPELINE SIMULATION")
    print("="*60)
    
    # ---------------------------------------------------------
    # Scenario A: House Price Prediction (Regression)
    # ---------------------------------------------------------
    print("\n--- SCENARIO A: Regression (e.g., Housing Prices) ---")
    X_reg, y_reg = DataPreprocessor.generate_regression_data(n_samples=5000, n_features=15)
    X_train_r, X_test_r, y_train_r, y_test_r, _ = DataPreprocessor.split_and_scale(X_reg, y_reg, test_size=0.2)
    
    lin_model = LinearModelsLesson.train_linear_regression(X_train_r, y_train_r)
    EvaluationMetricsLesson.evaluate_regression(lin_model, X_test_r, y_test_r)
    
    # ---------------------------------------------------------
    # Scenario B: Medical Diagnosis (Classification)
    # ---------------------------------------------------------
    print("\n--- SCENARIO B: Classification (e.g., Disease Diagnosis) ---")
    X_clf, y_clf = DataPreprocessor.generate_classification_data(n_samples=3000, n_features=20)
    X_train_c, X_test_c, y_train_c, y_test_c, _ = DataPreprocessor.split_and_scale(X_clf, y_clf, test_size=0.2)
    
    # Model 1: Logistic Regression
    log_model = LinearModelsLesson.train_logistic_regression(X_train_c, y_train_c)
    EvaluationMetricsLesson.evaluate_classification(log_model, X_test_c, y_test_c)
    
    # Model 2: K-Nearest Neighbors
    knn_model = NonLinearModelsLesson.train_knn(X_train_c, y_train_c, k=7)
    EvaluationMetricsLesson.evaluate_classification(knn_model, X_test_c, y_test_c)
    
    # Model 3: Decision Tree
    dt_model = NonLinearModelsLesson.train_decision_tree(X_train_c, y_train_c, max_depth=8)
    EvaluationMetricsLesson.evaluate_classification(dt_model, X_test_c, y_test_c)
    
    print("\n" + "="*60)
    print("✅ PIPELINE EXECUTION COMPLETE")
    print("="*60 + "\n")


# =============================================================================
# 6. TESTS & INTERVIEW QUESTIONS
# =============================================================================

def sklearn_interview_questions() -> None:
    """
    Common Scikit-Learn / ML interview questions and implementations.
    """
    print("\n--- INTERVIEW CORNER ---")
    print("Q1: Why do we use StandardScaler before applying PCA or KNN?")
    print("A: Distance-based algorithms (like KNN) and variance-maximizing algorithms "
          "(like PCA) are highly sensitive to the scale of features. If one feature "
          "is in thousands and another in decimals, the larger feature will disproportionately "
          "influence the outcome. StandardScaler standardizes features to zero mean and unit variance.")
          
    print("\nQ2: What is Data Leakage in standard preprocessing?")
    print("A: Data leakage occurs if you fit your scaler/imputer on the ENTIRE dataset "
          "before splitting. Information from the test set 'leaks' into the training process. "
          "Always split first, fit the scaler on the train set, then transform both train and test.")


def run_tests() -> None:
    """
    Comprehensive test suite ensuring the robust functioning of the pipeline.
    """
    if not SKLEARN_AVAILABLE:
        print("Skipping tests (Scikit-Learn not installed).")
        return
        
    print("--- Running Test Suite ---")
    try:
        # Test 1: Data Generation Shapes
        X, y = DataPreprocessor.generate_classification_data(100, 5)
        assert X.shape == (100, 5), f"Expected shape (100, 5), got {X.shape}"
        assert y.shape == (100,), f"Expected shape (100,), got {y.shape}"
        
        # Test 2: Split and Scale
        X_tr, X_te, y_tr, y_te, scaler = DataPreprocessor.split_and_scale(X, y, test_size=0.2)
        assert X_tr.shape[0] == 80, "Train size should be 80"
        assert X_te.shape[0] == 20, "Test size should be 20"
        
        # Mean of scaled train set should be near 0
        mean_val = np.mean(X_tr, axis=0)
        assert np.allclose(mean_val, 0, atol=1e-7), f"Scaled mean is not 0: {mean_val}"
        
        # Test 3: Model instantiation
        model = LogisticRegression()
        model.fit(X_tr, y_tr)
        assert hasattr(model, "coef_"), "Model did not fit properly"
        
        print("All internal assertions passed successfully. ✅\n")
        
    except AssertionError as e:
        print(f"❌ Test Failed: {e}")
        traceback.print_exc()
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")


# =============================================================================
# MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":
    print("\n" + "#"*70)
    print(" " * 15 + "SCI-KIT LEARN FOUNDATIONS LESSON")
    print("#"*70 + "\n")
    
    # 1. Pipeline Execution
    run_real_world_pipeline()
    
    # 2. Theory and Interview Questions
    sklearn_interview_questions()
    
    # 3. Unit Tests
    run_tests()
    
    print("LESSON COMPLETED. You are now equipped with the foundations of Scikit-Learn!")
