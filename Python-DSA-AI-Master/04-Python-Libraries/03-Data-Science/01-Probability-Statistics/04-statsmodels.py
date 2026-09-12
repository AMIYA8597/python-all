"""
================================================================================
Statsmodels Mastery: A Comprehensive Interactive Lesson
================================================================================

Welcome to the textbook-grade interactive lesson on `statsmodels`!
This module is designed to provide you with a deep, theoretical, and practical
understanding of statistical modeling in Python using the `statsmodels` library.

`statsmodels` is a Python module that provides classes and functions for the 
estimation of many different statistical models, as well as for conducting 
statistical tests, and statistical data exploration. 

Table of Contents:
1. Introduction to Statistical Modeling
2. Ordinary Least Squares (OLS) Regression
3. Generalized Linear Models (GLM) & Logistic Regression
4. Time Series Analysis (ARIMA)
5. Analysis of Variance (ANOVA)
6. Real-World Applications & Testing

Mathematical Background:
------------------------
Statistical modeling revolves around finding mathematical relationships between
variables. A common form is:
    Y = f(X) + ε
Where:
- Y is the dependent variable (target)
- X represents the independent variables (features)
- f(X) is the systematic information that X provides about Y
- ε is the random error term (unpredictable noise)

Big-O Complexity:
-----------------
The computational complexity of fitting statistical models often depends on matrix
operations. For Ordinary Least Squares (OLS), finding the exact analytical solution
involves computing (X^T X)^-1 X^T Y, which requires matrix inversion.
- Time Complexity: O(p^2 n + p^3), where 'n' is the number of observations and 
  'p' is the number of features.
- Space Complexity: O(np + p^2) to store the data and covariance matrices.
Modern implementations use optimized linear algebra libraries (BLAS/LAPACK) like
QR decomposition or Singular Value Decomposition (SVD) for numerical stability.

Let's dive into the code!
"""

import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt
from typing import Tuple, Dict, Any, List

# Set random seed for reproducibility
np.random.seed(42)

# ==============================================================================
# Chapter 1 & 2: Ordinary Least Squares (OLS) Linear Regression
# ==============================================================================
"""
OLS Regression Mathematics:
---------------------------
In Simple Linear Regression: Y = β0 + β1*X + ε
We want to find the coefficients (β0, β1) that minimize the Sum of Squared Residuals (SSR):
SSR = Σ (y_i - ŷ_i)^2
    = Σ (y_i - (β0 + β1*x_i))^2

Using calculus (setting partial derivatives to zero), we get the normal equations.
In matrix notation for Multiple Linear Regression: Y = Xβ + ε
The estimated coefficients are given by:
β_hat = (X^T * X)^(-1) * X^T * Y
"""

def demonstrate_ols() -> sm.regression.linear_model.RegressionResultsWrapper:
    """
    Demonstrates Ordinary Least Squares (OLS) regression using statsmodels.
    Generates synthetic data, fits an OLS model, and prints the summary.
    
    Returns:
        The fitted OLS results wrapper object.
    """
    print("\n" + "="*60)
    print("--- Chapter 2: Ordinary Least Squares (OLS) ---")
    print("="*60)
    
    # 1. Generate Synthetic Data
    # Let's say we are predicting Salary based on Years of Experience and Education Level
    n_samples = 100
    experience = np.random.uniform(1, 20, n_samples)
    education_years = np.random.normal(14, 2, n_samples) # Average 14 years, std 2
    
    # True relationship: Salary = 30000 + 4000*Experience + 5000*Education + Noise
    true_beta0 = 30000
    true_beta1 = 4000
    true_beta2 = 5000
    noise = np.random.normal(0, 10000, n_samples) # Standard deviation of $10,000
    
    salary = true_beta0 + true_beta1*experience + true_beta2*education_years + noise
    
    # Create a DataFrame
    df = pd.DataFrame({
        'Experience': experience,
        'Education': education_years,
        'Salary': salary
    })
    
    print("Synthetic Data Preview:")
    print(df.head())
    
    # 2. Fit OLS using the Formula API (R-like syntax)
    # The formula 'Salary ~ Experience + Education' automatically adds an intercept
    # and treats Salary as the dependent variable.
    model = smf.ols(formula='Salary ~ Experience + Education', data=df)
    results = model.fit()
    
    # 3. Print the comprehensive summary
    print("\nOLS Regression Results Summary:")
    print(results.summary())
    
    # Extracting specific metrics
    print("\nKey Metrics Extracted:")
    print(f"R-squared (Coefficient of Determination): {results.rsquared:.4f}")
    print(f"Adjusted R-squared: {results.rsquared_adj:.4f}")
    print(f"F-statistic p-value: {results.f_pvalue:.4e}")
    print(f"Coefficients:\n{results.params}")
    
    return results

# ==============================================================================
# Chapter 3: Generalized Linear Models (GLM) & Logistic Regression
# ==============================================================================
"""
Logistic Regression Mathematics:
--------------------------------
When our dependent variable is binary (0 or 1), OLS is inappropriate (it can predict
values outside [0,1] and residuals aren't normally distributed).
We use Logistic Regression, a type of Generalized Linear Model (GLM) with a Binomial
family and Logit link function.

The Logit link function is the logarithm of the odds:
Logit(p) = ln(p / (1-p)) = β0 + β1*X1 + ... + βk*Xk
Solving for p (probability of Y=1):
p = 1 / (1 + e^-(β0 + β1*X1 + ... + βk*Xk)) -> The Sigmoid Function

Estimation is typically done via Maximum Likelihood Estimation (MLE), using
iterative algorithms like Newton-Raphson. Complexity is roughly O(k * p^2 n) where
k is the number of iterations until convergence.
"""

def demonstrate_logistic_regression() -> sm.genmod.generalized_linear_model.GLMResultsWrapper:
    """
    Demonstrates Logistic Regression using the GLM module in statsmodels.
    
    Returns:
        The fitted GLM results wrapper object.
    """
    print("\n" + "="*60)
    print("--- Chapter 3: Logistic Regression (GLM) ---")
    print("="*60)
    
    # 1. Generate Synthetic Data for Binary Classification
    # Predicting if a user will click an ad based on Age and Time Spent on site
    n_samples = 200
    age = np.random.uniform(18, 65, n_samples)
    time_spent = np.random.exponential(10, n_samples) # Average 10 mins
    
    # Log-odds equation: z = -4 + 0.05*Age + 0.2*TimeSpent
    z = -4 + 0.05*age + 0.2*time_spent
    
    # Convert log-odds to probabilities using Sigmoid function
    probabilities = 1 / (1 + np.exp(-z))
    
    # Generate binary outcomes based on probabilities
    clicks = np.random.binomial(1, probabilities)
    
    df_clf = pd.DataFrame({
        'Age': age,
        'TimeSpent': time_spent,
        'Clicked': clicks
    })
    
    print("Classification Data Preview:")
    print(df_clf.head())
    
    # 2. Fit Logistic Regression using GLM
    # We specify the family as Binomial (for binary outcomes)
    X = df_clf[['Age', 'TimeSpent']]
    X = sm.add_constant(X) # Explicitly add an intercept term
    y = df_clf['Clicked']
    
    model = sm.GLM(y, X, family=sm.families.Binomial())
    results = model.fit()
    
    print("\nLogistic Regression Results Summary:")
    print(results.summary())
    
    return results

# ==============================================================================
# Chapter 4: Time Series Analysis (ARIMA)
# ==============================================================================
"""
ARIMA Mathematics:
------------------
ARIMA stands for AutoRegressive Integrated Moving Average.
It consists of three components specified as ARIMA(p, d, q):

1. AR(p) - Autoregression:
   The current value is a linear combination of 'p' past values.
   Y_t = c + φ1*Y_{t-1} + φ2*Y_{t-2} + ... + φp*Y_{t-p} + ε_t

2. I(d) - Integration:
   Differencing the raw observations to make the time series stationary.
   If d=1, we model the change: Y'_t = Y_t - Y_{t-1}

3. MA(q) - Moving Average:
   The current value depends on past forecast errors.
   Y_t = c + ε_t + θ1*ε_{t-1} + ... + θq*ε_{t-q}

Combined ARIMA(p,d,q) models complex temporal dynamics. Fitting involves 
Kalman filters and MLE.
"""

def demonstrate_arima() -> Any:
    """
    Demonstrates Time Series forecasting using ARIMA in statsmodels.
    
    Returns:
        Fitted ARIMA model results.
    """
    print("\n" + "="*60)
    print("--- Chapter 4: Time Series Analysis (ARIMA) ---")
    print("="*60)
    
    # 1. Generate Synthetic Time Series Data with a trend and AR(1) process
    n_steps = 100
    np.random.seed(123)
    # Generate AR(1) process: Y_t = 0.6 * Y_{t-1} + noise
    ar_series = np.zeros(n_steps)
    for t in range(1, n_steps):
        ar_series[t] = 0.6 * ar_series[t-1] + np.random.normal(0, 1)
        
    # Add a linear trend to make it non-stationary (requires d=1)
    trend = np.linspace(0, 10, n_steps)
    time_series = ar_series + trend
    
    dates = pd.date_range(start='2023-01-01', periods=n_steps, freq='D')
    ts_df = pd.Series(time_series, index=dates)
    
    # 2. Fit ARIMA(1, 1, 0)
    # We use p=1 (since we generated with AR(1)), d=1 (to remove linear trend), q=0
    model = ARIMA(ts_df, order=(1, 1, 0))
    results = model.fit()
    
    print("\nARIMA(1,1,0) Results Summary:")
    print(results.summary())
    
    # 3. Forecasting
    forecast = results.forecast(steps=5)
    print("\nForecast for next 5 days:")
    print(forecast)
    
    return results

# ==============================================================================
# Chapter 5: Analysis of Variance (ANOVA)
# ==============================================================================
"""
ANOVA Mathematics:
------------------
ANOVA tests the hypothesis that the means of two or more populations are equal.
It partitions the total variance in the data into:
1. Variance Between Groups (due to the categorical variable/treatment)
2. Variance Within Groups (due to random noise/error)

F-statistic = (Variance Between Groups) / (Variance Within Groups)
A high F-statistic (and corresponding low p-value) indicates that the group means
are significantly different.
"""

def demonstrate_anova() -> Any:
    """
    Demonstrates One-Way ANOVA using statsmodels.
    """
    print("\n" + "="*60)
    print("--- Chapter 5: Analysis of Variance (ANOVA) ---")
    print("="*60)
    
    # 1. Generate Data: Plant Growth under 3 different fertilizers
    # Fertilizer A: mean=20, Fertilizer B: mean=25, Fertilizer C: mean=22
    np.random.seed(42)
    group_a = np.random.normal(20, 3, 30)
    group_b = np.random.normal(25, 3, 30)
    group_c = np.random.normal(22, 3, 30)
    
    df_anova = pd.DataFrame({
        'Growth': np.concatenate([group_a, group_b, group_c]),
        'Fertilizer': ['A']*30 + ['B']*30 + ['C']*30
    })
    
    # 2. Fit an OLS model for ANOVA
    # 'Growth ~ C(Fertilizer)' treats Fertilizer as a categorical variable
    model = smf.ols('Growth ~ C(Fertilizer)', data=df_anova).fit()
    
    # 3. Perform ANOVA
    anova_table = sm.stats.anova_lm(model, typ=2)
    print("\nANOVA Table:")
    print(anova_table)
    
    # Interpretation: If PR(>F) for C(Fertilizer) is < 0.05, we reject the null hypothesis
    # that all fertilizers yield the same average growth.
    
    return anova_table


# ==============================================================================
# Chapter 6: Real-World Applications & Testing
# ==============================================================================
def run_all_tests():
    """
    Executes all demonstrations and acts as the test suite for the module.
    Validates that statsmodels structures and assumptions hold.
    """
    print("Starting Statsmodels Interactive Lesson Test Suite...")
    
    # Test OLS
    try:
        ols_res = demonstrate_ols()
        assert ols_res.nobs == 100, "OLS should have 100 observations."
        assert len(ols_res.params) == 3, "OLS should have 3 parameters (Intercept, Experience, Education)."
        print("[SUCCESS] OLS Regression completed.")
    except Exception as e:
        print(f"[ERROR] OLS Regression failed: {e}")
        
    # Test GLM
    try:
        glm_res = demonstrate_logistic_regression()
        assert glm_res.nobs == 200, "GLM should have 200 observations."
        print("[SUCCESS] Logistic Regression completed.")
    except Exception as e:
        print(f"[ERROR] Logistic Regression failed: {e}")
        
    # Test ARIMA
    try:
        arima_res = demonstrate_arima()
        print("[SUCCESS] ARIMA forecasting completed.")
    except Exception as e:
        print(f"[ERROR] ARIMA failed: {e}")
        
    # Test ANOVA
    try:
        anova_res = demonstrate_anova()
        assert 'C(Fertilizer)' in anova_res.index, "Fertilizer effect should be in ANOVA table."
        print("[SUCCESS] ANOVA testing completed.")
    except Exception as e:
        print(f"[ERROR] ANOVA failed: {e}")
        
    print("\n--- End of Lesson ---")
    print("You have successfully navigated through linear modeling, logistic regression,")
    print("time series analysis, and variance testing using Python's statsmodels!")

if __name__ == '__main__':
    run_all_tests()

"""
Extended Discussion on Real-World Usage:
----------------------------------------
Why use `statsmodels` over `scikit-learn`?
1. Inferential Statistics: scikit-learn is primarily focused on predictive accuracy (Machine Learning).
   statsmodels provides classical statistical inference (p-values, confidence intervals, standard errors).
2. Diagnostics: statsmodels offers extensive post-estimation diagnostic tests (e.g., checking for
   heteroskedasticity, autocorrelation of residuals, normality tests).
3. Econometrics: Many econometric models (like ARIMA, VAR, GARCH) are natively supported or better
   implemented in statsmodels than scikit-learn.

In industry, a Data Scientist will often use `statsmodels` during the exploratory phase and hypothesis
testing phase to deeply understand the relationship between variables, identify significant features,
and ensure statistical assumptions are met. Later, they might transition to `scikit-learn` or `XGBoost`
for building the highly-scalable predictive pipeline.
"""
