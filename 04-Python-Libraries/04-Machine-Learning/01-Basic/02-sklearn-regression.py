"""
# ==============================================================================
# LABORATORY: REGRESSION AND REGULARIZATION (SCIKIT-LEARN)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Classification predicts discrete categories (Spam vs Not Spam).
# Regression predicts continuous numbers (House Price, Temperature, Stock Value).
#
# Ordinary Least Squares (OLS) Linear Regression is the grandfather of all ML. 
# It finds a line of best fit by mathematically minimizing the Residual Sum 
# of Squares (MSE). However, OLS is highly susceptible to Overfitting when 
# you have too many features (e.g., 1000 features, 100 rows).
#
# To solve this, we use **Regularization**.
# - Ridge (L2) Regression: Mathematically punishes large coefficients.
# - Lasso (L1) Regression: Mathematically punishes non-zero coefficients, 
#   acting as an automatic Feature Selector that aggressively deletes useless columns!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the math of OLS Linear Regression.
# - Combat Overfitting using Ridge (L2) and Lasso (L1) Regularization.
# - Model non-linear data using Polynomial Regression.
# - Understand the underlying Gradient Descent algorithm.
#
# ==============================================================================
"""

import numpy as np
import pandas as pd
import time

# In a real environment: pip install scikit-learn
try:
    from sklearn.model_selection import train_test_split
    from sklearn.linear_model import LinearRegression, Ridge, Lasso
    from sklearn.preprocessing import PolynomialFeatures, StandardScaler
    from sklearn.pipeline import Pipeline
    from sklearn.metrics import mean_squared_error, r2_score
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. ORDINARY LEAST SQUARES (OLS) REGRESSION
# ==============================================================================
def demonstrate_ols():
    section_header("Ordinary Least Squares (Linear Regression)")
    
    if not HAS_SKLEARN: return
    
    print("Scenario: Predicting a person's Salary based solely on Years of Experience.")
    
    # 1. GENERATE DATA (Linear relationship with noise)
    rng = np.random.default_rng(42)
    experience = rng.uniform(0, 30, 200).reshape(-1, 1) # Reshape to 2D column vector!
    
    # True Math: $40k base + $5k per year + Random Noise
    true_salary = 40000 + (5000 * experience)
    noisy_salary = true_salary + rng.normal(0, 15000, 200).reshape(-1, 1)
    
    X_train, X_test, y_train, y_test = train_test_split(experience, noisy_salary, test_size=0.2, random_state=42)
    
    # 2. FIT OLS MODEL
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    # 3. EXTRACT COEFFICIENTS
    print(f"Mathematical Equation found by the Machine:")
    print(f"Salary = {model.intercept_[0]:.0f} + ({model.coef_[0][0]:.0f} * Experience)")
    print(f"(Notice how close it is to our secret true math: 40000 + 5000 * Exp!)")
    
    # 4. EVALUATE
    preds = model.predict(X_test)
    mse = mean_squared_error(y_test, preds)
    r2 = r2_score(y_test, preds)
    
    print(f"\nMean Squared Error (MSE): ${np.sqrt(mse):.0f} (Root MSE means our guess is off by ~$14k on average)")
    print(f"R-Squared (R2)        : {r2:.3f} (The model explains 74% of the variance!)")


# ==============================================================================
# 4. OVERFITTING AND REGULARIZATION (RIDGE VS LASSO)
# ==============================================================================
def demonstrate_regularization():
    section_header("Regularization (L1 Lasso vs L2 Ridge)")
    
    if not HAS_SKLEARN: return
    
    # Let's generate a dataset designed to Overfit!
    # 100 Rows, but 50 Features! (High-dimensional data).
    # Only the first 3 features are mathematically real. The other 47 are pure noise!
    rng = np.random.default_rng(42)
    X = rng.normal(0, 1, (100, 50))
    
    # The true math only uses the first 3 columns.
    y = (X[:, 0] * 10.0) + (X[:, 1] * 5.0) + (X[:, 2] * 2.0) + rng.normal(0, 1, 100)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    
    # Always scale data before regularizing!
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)
    
    # 1. STANDARD OLS (Will Overfit heavily)
    ols = LinearRegression().fit(X_train, y_train)
    
    # 2. RIDGE REGRESSION (L2)
    # Adds a penalty equivalent to the SQUARE of the magnitude of coefficients.
    # It shrinks all coefficients toward zero, but never exactly zero.
    ridge = Ridge(alpha=10.0).fit(X_train, y_train)
    
    # 3. LASSO REGRESSION (L1)
    # Adds a penalty equivalent to the ABSOLUTE VALUE of the magnitude of coefficients.
    # It mathematically forces useless coefficients to be exactly 0.0 (Feature Selection!).
    lasso = Lasso(alpha=0.5).fit(X_train, y_train)
    
    print("Evaluating Test Set R-Squared (Higher is better):")
    print(f"OLS R2   : {r2_score(y_test, ols.predict(X_test)):.3f} (Terrible! Overfitted to the noise!)")
    print(f"Ridge R2 : {r2_score(y_test, ridge.predict(X_test)):.3f} (Good, prevented overfitting)")
    print(f"Lasso R2 : {r2_score(y_test, lasso.predict(X_test)):.3f} (Best! Isolated the true signal)")
    
    # Let's count how many coefficients the algorithms completely deleted (Zeroed out)!
    print("\nFeature Selection (Out of 50 features):")
    print(f"OLS Non-Zero Features  : {np.sum(np.abs(ols.coef_) > 1e-5)}")
    print(f"Ridge Non-Zero Features: {np.sum(np.abs(ridge.coef_) > 1e-5)}")
    print(f"Lasso Non-Zero Features: {np.sum(np.abs(lasso.coef_) > 1e-5)} (It completely erased the 47 columns of noise!)")


# ==============================================================================
# 5. POLYNOMIAL REGRESSION (NON-LINEAR DATA)
# ==============================================================================
def demonstrate_polynomial():
    section_header("Polynomial Regression (Curves)")
    
    if not HAS_SKLEARN: return
    
    # Linear Regression can only draw straight lines. What if the data is a curve?
    # e.g., A Parabola: Y = X^2
    rng = np.random.default_rng(42)
    X = rng.uniform(-3, 3, 100).reshape(-1, 1)
    y = (X[:, 0] ** 2) + rng.normal(0, 0.5, 100) # y = x^2 + noise
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 1. NAIVE LINEAR MODEL
    linear = LinearRegression().fit(X_train, y_train)
    print(f"Straight Line R2: {r2_score(y_test, linear.predict(X_test)):.3f} (Cannot fit a curve!)")
    
    # 2. POLYNOMIAL PIPELINE
    # We use a mathematical trick. We physically add a new column to the dataset 
    # containing X^2! Now the Linear model can fit a straight line in 2D space 
    # that projects as a curve in 1D space!
    pipeline = Pipeline([
        ('poly', PolynomialFeatures(degree=2, include_bias=False)),
        ('linear', LinearRegression())
    ])
    
    pipeline.fit(X_train, y_train)
    poly_r2 = r2_score(y_test, pipeline.predict(X_test))
    print(f"Polynomial R2   : {poly_r2:.3f} (Perfect fit!)")


def run_all_labs():
    demonstrate_ols()
    demonstrate_regularization()
    demonstrate_polynomial()


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why does an OLS model fail (Overfit) when there are more features than rows (e.g., Genetic data with 20k genes but 100 patients)?
   Answer: In OLS, the machine attempts to solve a system of linear equations to minimize the error to zero. If you have more variables (features) than equations (rows), the mathematical system is "underdetermined". The model can essentially draw an infinitely complex, jagged line that perfectly touches every single point in the training set (Train Error = 0). But when exposed to a new patient, this jagged line produces wildly inaccurate, extreme predictions (Test Error = Infinity). This is textbook Overfitting.

2. What is the fundamental difference between Ridge (L2) and Lasso (L1)?
   Answer: Both algorithms prevent Overfitting by adding a penalty to the loss function. 
   - **Ridge (L2)** squares the penalty ($\alpha \sum w^2$). This heavily punishes massive weights, forcing all coefficients to become very small, but it mathematically never pushes a weight to exactly $0.0$.
   - **Lasso (L1)** takes the absolute value of the penalty ($\alpha \sum |w|$). The sharp mathematical geometry (the "diamond" shape of the L1 norm) physically forces useless weights to collide exactly with the $0.0$ axis. Therefore, Lasso acts as an automatic Feature Selection tool, physically deleting useless columns from the model!

3. How does Polynomial Regression still qualify as a "Linear" Model?
   Answer: The term "Linear" in Linear Regression does not mean the line drawn on the graph must be straight! It means the mathematical equation is linear *with respect to its coefficients (weights)*. 
   Equation: $Y = W_1X_1 + W_2X_2$. 
   If we manually create a new column $X_2 = X_1^2$, the equation becomes $Y = W_1X_1 + W_2(X_1^2)$. The weights $W_1$ and $W_2$ are still multiplied linearly! The algorithm has no idea that $X_2$ is a square; it just treats it as a second feature. The resulting model can plot a complex curve on a graph while still utilizing the exact same highly-optimized linear algebra solvers!
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Scikit-Learn Regression Completed.")
