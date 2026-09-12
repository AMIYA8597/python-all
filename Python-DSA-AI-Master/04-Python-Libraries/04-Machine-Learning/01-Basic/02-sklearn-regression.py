"""
Module: 02-sklearn-regression
Description: A textbook-grade interactive lesson on Regression Analysis using scikit-learn.

=========================================================================================
                               MACHINE LEARNING: REGRESSION
=========================================================================================

Learning Objectives:
1. Understand the theoretical and mathematical foundations of regression models.
2. Implement Ordinary Least Squares (OLS) Linear Regression using scikit-learn.
3. Master regularization techniques: Ridge (L2) and Lasso (L1) regression.
4. Handle non-linear relationships using Polynomial Regression.
5. Evaluate regression models using appropriate metrics (MSE, MAE, R²).
6. Understand the Time and Space Complexity (Big-O) of regression algorithms.
7. Solve a real-world predictive modeling scenario and a common interview challenge.

=========================================================================================
1. MATHEMATICAL BACKGROUND
=========================================================================================
Regression analysis is a set of statistical processes for estimating the relationships 
between a dependent variable (target, y) and one or more independent variables 
(features, X).

1.1 Ordinary Least Squares (OLS) Linear Regression
---------------------------------------------------
Model: \u0177 = w_0 + w_1*x_1 + w_2*x_2 + ... + w_p*x_p = Xw

Objective Function (Cost Function J):
Minimize the Residual Sum of Squares (RSS) / Mean Squared Error (MSE).
J(w) = ||y - Xw||^2 = \u2211(y_i - \u0177_i)^2

Closed-form solution (Normal Equation):
w = (X^T * X)^-1 * X^T * y

1.2 Ridge Regression (L2 Regularization)
----------------------------------------
Prevents overfitting by penalizing large weights.
J(w) = ||y - Xw||^2 + \u03b1 * ||w||_2^2
Closed-form solution:
w = (X^T * X + \u03b1 * I)^-1 * X^T * y

1.3 Lasso Regression (L1 Regularization)
----------------------------------------
Encourages sparsity (feature selection) by penalizing the absolute size of weights.
J(w) = ||y - Xw||^2 + \u03b1 * ||w||_1
No closed-form solution; solved via optimization (e.g., coordinate descent).

=========================================================================================
2. COMPLEXITY ANALYSIS (BIG-O)
=========================================================================================
Let n = number of samples (rows), p = number of features (columns).

OLS Linear Regression:
- Time Complexity (Training): O(n * p^2 + p^3) due to matrix multiplication (X^T * X) 
  and inversion. (Modern solvers use SVD, complexity O(n * p^2)).
- Time Complexity (Inference): O(p) per sample.
- Space Complexity: O(n * p) to store data, O(p) to store weights.

Ridge/Lasso:
- Time Complexity (Training): O(n * p^2) for SVD/Cholesky or iterative solvers.
- Time Complexity (Inference): O(p) per sample.

=========================================================================================
"""

import sys
import time
import math
import warnings
from typing import Tuple, List, Dict, Any, Optional, Callable

# Standard Scientific Stack
try:
    import numpy as np
    import matplotlib.pyplot as plt
    from sklearn.linear_model import LinearRegression, Ridge, Lasso
    from sklearn.preprocessing import PolynomialFeatures, StandardScaler
    from sklearn.pipeline import make_pipeline
    from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
    from sklearn.model_selection import train_test_split
except ImportError as e:
    print(f"Required libraries missing: {e}. Please install numpy, matplotlib, scikit-learn.")
    sys.exit(1)

# Ignore convergence warnings for illustrative purposes when using small alphas in Lasso
warnings.filterwarnings("ignore")


# =======================================================================================
# 1. DATA GENERATION UTILITIES
# =======================================================================================

def generate_linear_data(n_samples: int = 100, noise: float = 10.0, random_state: int = 42) -> Tuple[np.ndarray, np.ndarray]:
    """
    Generates synthetic dataset for linear regression.
    y = 3*x + 4 + noise
    
    Args:
        n_samples (int): Number of data points.
        noise (float): Standard deviation of Gaussian noise.
        random_state (int): Seed for reproducibility.
        
    Returns:
        Tuple[np.ndarray, np.ndarray]: Feature matrix X (2D) and target vector y (1D).
    """
    np.random.seed(random_state)
    X = 10 * np.random.rand(n_samples, 1)  # Features between 0 and 10
    # True weights: slope = 3.0, intercept = 4.0
    true_w1, true_w0 = 3.0, 4.0
    y = true_w1 * X.squeeze() + true_w0 + np.random.randn(n_samples) * noise
    return X, y


def generate_nonlinear_data(n_samples: int = 100, noise: float = 2.0, random_state: int = 42) -> Tuple[np.ndarray, np.ndarray]:
    """
    Generates synthetic dataset for polynomial regression.
    y = 0.5 * x^2 + x + 2 + noise
    
    Args:
        n_samples (int): Number of data points.
        noise (float): Standard deviation of Gaussian noise.
        random_state (int): Seed for reproducibility.
        
    Returns:
        Tuple[np.ndarray, np.ndarray]: Feature matrix X (2D) and target vector y (1D).
    """
    np.random.seed(random_state)
    X = 6 * np.random.rand(n_samples, 1) - 3  # Features between -3 and 3
    # True function: 0.5 * X^2 + 1.0 * X + 2.0
    y = 0.5 * X.squeeze()**2 + X.squeeze() + 2 + np.random.randn(n_samples) * noise
    return X, y


# =======================================================================================
# 2. CORE REGRESSION IMPLEMENTATIONS
# =======================================================================================

def evaluate_model(y_true: np.ndarray, y_pred: np.ndarray, model_name: str) -> Dict[str, float]:
    """
    Evaluates regression predictions using MSE, MAE, and R-squared.
    
    Args:
        y_true (np.ndarray): Ground truth target values.
        y_pred (np.ndarray): Predicted target values.
        model_name (str): Identifier for logging.
        
    Returns:
        Dict[str, float]: Dictionary of metric names to values.
    """
    mse = mean_squared_error(y_true, y_pred)
    mae = mean_absolute_error(y_true, y_pred)
    r2 = r2_score(y_true, y_pred)
    
    print(f"--- Evaluation for {model_name} ---")
    print(f"MSE: {mse:.4f} (Mean Squared Error - Penalizes large errors)")
    print(f"MAE: {mae:.4f} (Mean Absolute Error - Linear error metric)")
    print(f"R² : {r2:.4f} (Coefficient of Determination - Variance explained, closer to 1 is better)\n")
    
    return {"MSE": mse, "MAE": mae, "R2": r2}


def basic_linear_regression() -> None:
    """
    Demonstrates Ordinary Least Squares (OLS) Linear Regression using scikit-learn.
    Includes data splitting, training, prediction, evaluation, and theoretical analysis.
    """
    print("\n" + "="*50)
    print("1. OLS LINEAR REGRESSION")
    print("="*50)
    
    # 1. Data Preparation
    X, y = generate_linear_data(n_samples=200, noise=5.0)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 2. Model Initialization and Training
    # LinearRegression fits a linear model with coefficients w = (w1, ..., wp)
    # to minimize the residual sum of squares between observed targets and predictions.
    start_time = time.perf_counter()
    model = LinearRegression(fit_intercept=True)
    model.fit(X_train, y_train)
    training_time = time.perf_counter() - start_time
    
    # 3. Model Inspection
    print("Model Parameters:")
    print(f"Estimated Intercept (w_0): {model.intercept_:.4f} (True: 4.0)")
    print(f"Estimated Coefficient (w_1): {model.coef_[0]:.4f} (True: 3.0)")
    print(f"Training Time (n=160, p=1): {training_time:.6f} sec")
    
    # 4. Inference
    y_pred_train = model.predict(X_train)
    y_pred_test = model.predict(X_test)
    
    # 5. Evaluation
    evaluate_model(y_train, y_pred_train, "OLS Linear Regression (Train)")
    evaluate_model(y_test, y_pred_test, "OLS Linear Regression (Test)")


def regularized_regression_comparison() -> None:
    """
    Demonstrates Ridge (L2) and Lasso (L1) regression. 
    Shows how they handle high-dimensional or collinear data by shrinking coefficients.
    """
    print("\n" + "="*50)
    print("2. REGULARIZED REGRESSION (RIDGE vs LASSO)")
    print("="*50)
    
    # Generate data with many redundant/collinear features
    np.random.seed(42)
    n_samples, n_features = 100, 20
    X = np.random.randn(n_samples, n_features)
    
    # Only the first 3 features are informative
    true_coef = np.array([5.0, 3.0, 1.5] + [0.0] * (n_features - 3))
    y = X.dot(true_coef) + np.random.randn(n_samples) * 2.0
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    
    # Standardizing features is crucial for regularized models
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    models = {
        "OLS": LinearRegression(),
        "Ridge (\u03b1=10)": Ridge(alpha=10.0), # L2 penalty
        "Lasso (\u03b1=0.5)": Lasso(alpha=0.5) # L1 penalty
    }
    
    for name, model in models.items():
        model.fit(X_train_scaled, y_train)
        y_pred = model.predict(X_test_scaled)
        
        print(f"--- {name} ---")
        mse = mean_squared_error(y_test, y_pred)
        
        # Count non-zero coefficients
        # Ridge shrinks coefficients towards zero, Lasso forces them exactly to zero.
        coef = model.coef_
        non_zero = np.sum(np.abs(coef) > 1e-5)
        
        print(f"Test MSE: {mse:.4f}")
        print(f"Number of non-zero coefficients: {non_zero} out of {n_features}")
        if name == "Lasso (\u03b1=0.5)":
            print(f"Lasso performs implicit feature selection by zeroing out {n_features - non_zero} irrelevant features.")
        print("-" * 20)


def polynomial_regression() -> None:
    """
    Demonstrates Polynomial Regression.
    Linear models can fit non-linear data by creating polynomial features.
    y = w0 + w1*x + w2*x^2 + ... + wd*x^d
    """
    print("\n" + "="*50)
    print("3. POLYNOMIAL REGRESSION")
    print("="*50)
    
    X, y = generate_nonlinear_data(n_samples=150, noise=1.5)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Evaluate models with different polynomial degrees
    degrees = [1, 2, 15]
    
    for degree in degrees:
        # A Pipeline sequentially applies a list of transforms and a final estimator.
        # 1. PolynomialFeatures generates a new feature matrix consisting of all polynomial combinations
        # 2. StandardScaler scales features (important for high degrees)
        # 3. LinearRegression fits the model
        model = make_pipeline(
            PolynomialFeatures(degree, include_bias=False),
            StandardScaler(),
            LinearRegression()
        )
        
        start_time = time.perf_counter()
        model.fit(X_train, y_train)
        train_time = time.perf_counter() - start_time
        
        y_train_pred = model.predict(X_train)
        y_test_pred = model.predict(X_test)
        
        train_mse = mean_squared_error(y_train, y_train_pred)
        test_mse = mean_squared_error(y_test, y_test_pred)
        
        print(f"--- Degree {degree} Polynomial Regression ---")
        print(f"Train MSE: {train_mse:.4f}")
        print(f"Test MSE : {test_mse:.4f}")
        
        if degree == 1:
            print("Observation: Underfitting (High bias). Linear model cannot capture the curve.")
        elif degree == 2:
            print("Observation: Good Fit. Matches the true data generating process (quadratic).")
        elif degree == 15:
            print("Observation: Overfitting (High variance). Train error is very low, but Test error explodes.")
        print(f"Training Time: {train_time:.6f} sec\n")


# =======================================================================================
# 3. INTERVIEW CHALLENGES & REAL-WORLD APPLICATIONS
# =======================================================================================

def interview_challenge_implement_gradient_descent(X: np.ndarray, y: np.ndarray, lr: float = 0.01, epochs: int = 1000) -> Tuple[float, float]:
    """
    Interview Challenge: Implement Simple Linear Regression (1 feature) using 
    Batch Gradient Descent from scratch.
    
    Mathematical Formulation:
    Hypothesis: h(x) = w * x + b
    Cost Function: J(w,b) = (1/2n) * \u2211(h(x_i) - y_i)^2
    Gradients:
    dj/dw = (1/n) * \u2211(h(x_i) - y_i) * x_i
    dj/db = (1/n) * \u2211(h(x_i) - y_i)
    
    Args:
        X (np.ndarray): 1D array of features.
        y (np.ndarray): 1D array of targets.
        lr (float): Learning rate.
        epochs (int): Number of iterations.
        
    Returns:
        Tuple[float, float]: Weight (slope) and bias (intercept).
    """
    print("\n" + "="*50)
    print("4. INTERVIEW CHALLENGE: GRADIENT DESCENT FROM SCRATCH")
    print("="*50)
    
    n = len(y)
    w, b = 0.0, 0.0 # Initialize parameters
    
    print(f"Training with LR={lr}, Epochs={epochs}...")
    for epoch in range(epochs):
        # 1. Predictions
        y_pred = w * X + b
        
        # 2. Compute error
        error = y_pred - y
        
        # 3. Compute gradients
        dw = (1 / n) * np.sum(error * X)
        db = (1 / n) * np.sum(error)
        
        # 4. Update parameters
        w = w - lr * dw
        b = b - lr * db
        
        if epoch % 200 == 0:
            cost = (1 / (2 * n)) * np.sum(error ** 2)
            print(f"Epoch {epoch:4d} | Cost: {cost:.4f} | w: {w:.4f} | b: {b:.4f}")
            
    return w, b


# =======================================================================================
# 4. UNIT TESTS
# =======================================================================================

def run_tests() -> None:
    """
    Automated test suite to validate implementations and mathematical correctness.
    """
    print("\n" + "="*50)
    print("5. SYSTEM TESTS")
    print("="*50)
    
    try:
        # Test Data Generators
        X_lin, y_lin = generate_linear_data(n_samples=50)
        assert X_lin.shape == (50, 1), "Linear data X shape mismatch"
        assert y_lin.shape == (50,), "Linear data y shape mismatch"
        
        # Test Evaluation Metrics (Integration with sklearn)
        y_true = np.array([3.0, -0.5, 2.0, 7.0])
        y_pred = np.array([2.5, 0.0, 2.0, 8.0])
        # MSE = (0.5^2 + 0.5^2 + 0^2 + 1.0^2) / 4 = 1.5 / 4 = 0.375
        mse = mean_squared_error(y_true, y_pred)
        assert np.isclose(mse, 0.375), f"MSE calculation incorrect. Expected 0.375, got {mse}"
        
        # Test custom Gradient Descent
        # Simple data: y = 2x + 1
        X_test = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
        y_test = np.array([3.0, 5.0, 7.0, 9.0, 11.0])
        
        w_gd, b_gd = interview_challenge_implement_gradient_descent(X_test, y_test, lr=0.01, epochs=2500)
        assert np.isclose(w_gd, 2.0, atol=0.1), f"GD failed to find slope. Expected ~2.0, got {w_gd}"
        assert np.isclose(b_gd, 1.0, atol=0.1), f"GD failed to find intercept. Expected ~1.0, got {b_gd}"
        
        print("All internal system tests passed successfully! \u2705")
        
    except AssertionError as e:
        print(f"\u274c Test Failed: {e}")
        sys.exit(1)


# =======================================================================================
# 5. MAIN EXECUTION
# =======================================================================================

if __name__ == "__main__":
    print(f"{'='*80}")
    print(f"{'PYTHON DSA MASTER: SKLEARN REGRESSION'.center(80)}")
    print(f"{'='*80}\n")
    
    print("This module provides a comprehensive tutorial on Regression techniques")
    print("using scikit-learn, covering theory, implementations, and complexities.\n")
    
    # 1. OLS Linear Regression
    basic_linear_regression()
    
    # 2. Ridge vs Lasso Regularization
    regularized_regression_comparison()
    
    # 3. Polynomial Regression (Non-linear modeling)
    polynomial_regression()
    
    # 4. Interview Challenge (Gradient Descent)
    run_tests()
    
    print("\n" + "="*80)
    print("LESSON COMPLETED. You now have a foundational understanding of")
    print("Regression models, cost functions, regularization, and model evaluation.")
    print("="*80)
