"""
# ==============================================================================
# LABORATORY: ECONOMETRICS & INFERENCE (STATSMODELS)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# There is a massive philosophical divide between "Machine Learning" (Scikit-Learn) 
# and "Statistical Modeling" (Statsmodels).
#
# Machine Learning cares exclusively about **Prediction**. If a Neural Network 
# can accurately predict house prices with 99% accuracy, the Data Scientist is 
# happy, even if the Neural Network is a "Black Box" and nobody understands 
# *how* it made the prediction.
#
# Econometrics (Statsmodels) cares exclusively about **Inference**. If a 
# pharmaceutical company is testing a new heart drug, they don't just want a 
# prediction. They need to mathematically PROVE to the FDA exactly how much the 
# drug lowers blood pressure, and provide a 95% Confidence Interval for that 
# specific variable! 
#
# `statsmodels` provides rigorous, traditional Statistical Models (OLS, Logit, 
# ARIMA) that output massive diagnostic summary tables containing R-Squared 
# values, P-Values, Standard Errors, and Confidence Intervals for every single 
# feature in the dataset.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand Ordinary Least Squares (OLS) Regression.
# - Interpret the `summary()` table (R-Squared, Coef, P>|t|).
# - Understand the difference between ML prediction and Statistical Inference.
#
# ==============================================================================
"""

import numpy as np
import pandas as pd

# In a real environment: pip install statsmodels
try:
    import statsmodels.api as sm
    HAS_STATSMODELS = True
except ImportError:
    HAS_STATSMODELS = False

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. ORDINARY LEAST SQUARES (OLS) REGRESSION
# ==============================================================================
def demonstrate_ols():
    section_header("Ordinary Least Squares (OLS) Inference")
    
    if not HAS_STATSMODELS:
        print("[WARNING] statsmodels is not installed. Skipping simulation.")
        print("Install using: pip install statsmodels")
        return
        
    print("Scenario: Analyzing the determinants of an Employee's Salary.")
    print("Features (X): Years of Experience, Years of Education, and Random Noise.")
    print("Target (Y): Salary ($)")
    
    rng = np.random.default_rng(42)
    n = 1000
    
    # 1. GENERATE SYNTHETIC DATA
    experience = rng.uniform(0, 30, n)
    education = rng.uniform(12, 22, n)
    noise = rng.normal(0, 5000, n) # Unexplained variance
    
    # The True Mathematical Formula (Hidden from the model!)
    # Base salary $30k + $2k per year of experience + $5k per year of education.
    salary = 30000 + (2000 * experience) + (5000 * education) + noise
    
    # 2. PREPARE THE DATA
    # We construct a Pandas DataFrame.
    X = pd.DataFrame({
        "Experience": experience,
        "Education": education,
        # Let's add a fake variable that has ZERO impact on salary!
        "Random_Noise_Var": rng.uniform(0, 100, n) 
    })
    y = salary
    
    # CRITICAL: Unlike Scikit-Learn, Statsmodels does NOT automatically add an 
    # Intercept (the Y-intercept constant) to the equation. We must explicitly 
    # inject a column of 1s into our X matrix!
    X = sm.add_constant(X)
    
    # 3. FIT THE MODEL
    # OLS minimizes the Sum of Squared Residuals to find the line of best fit.
    model = sm.OLS(endog=y, exog=X)
    results = model.fit()
    
    # 4. INFERENCE (THE SUMMARY TABLE)
    print("\n" + "="*78)
    print("                       OLS REGRESSION RESULTS")
    print("="*78)
    # The `.summary()` method is the crown jewel of statsmodels!
    print(results.summary())
    print("="*78)
    
    print("\n--- HOW TO INTERPRET THIS TABLE ---")
    
    # R-Squared
    r2 = results.rsquared
    print(f"1. R-Squared ({r2:.3f}):")
    print(f"   Our model explains {r2*100:.1f}% of the total variance in Salary.")
    
    # Coefficients
    exp_coef = results.params["Experience"]
    print(f"\n2. Coefficient ('coef' column for Experience = {exp_coef:.0f}):")
    print(f"   Holding education constant, every 1 extra year of experience ")
    print(f"   increases salary by exactly ${exp_coef:.0f} (matches our true $2000!).")
    
    # P-Values
    noise_p = results.pvalues["Random_Noise_Var"]
    print(f"\n3. P-Value ('P>|t|' column for Random_Noise_Var = {noise_p:.3f}):")
    print(f"   The P-Value is {noise_p:.3f} (Greater than 0.05). ")
    print(f"   We FAIL to reject the Null Hypothesis. The model mathematically ")
    print(f"   proved that 'Random_Noise_Var' is statistically meaningless!")
    
    # Confidence Intervals
    edu_low = results.conf_int().loc["Education", 0]
    edu_high = results.conf_int().loc["Education", 1]
    print(f"\n4. 95% Confidence Interval ('[0.025 - 0.975]' for Education):")
    print(f"   We are 95% confident the TRUE monetary value of 1 year of education ")
    print(f"   lies between ${edu_low:.0f} and ${edu_high:.0f} (Encompasses our true $5000!).")


def run_all_labs():
    demonstrate_ols()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why must you run `sm.add_constant(X)` before fitting a Statsmodels OLS regression?
   Answer: The mathematical equation for a line is $Y = \beta_0 + \beta_1 X_1$. The $\beta_0$ term is the Constant (the Y-intercept). Scikit-Learn models automatically calculate this constant behind the scenes. Statsmodels enforces strict econometric matrix algebra. If you pass an $X$ matrix without a column of exactly $1$s, the matrix multiplication ($X \beta$) has no way to formulate a constant, forcing the regression line to physically intersect the origin $(0,0)$. This fundamentally corrupts the entire model unless your data explicitly dictates a zero-intercept! `add_constant` fixes this by injecting the $1$s.

2. What is the fundamental difference in philosophy between Scikit-Learn and Statsmodels?
   Answer: Scikit-Learn is engineered for Predictive Machine Learning. It prioritizes cross-validation, hyperparameter tuning, predictive accuracy on unseen data, and rapid deployment. It provides very little statistical diagnostic information. 
   Statsmodels is engineered for Econometrics and Statistical Inference. It prioritizes the rigorous mathematical proof of relationships. It generates massive diagnostic tables containing Standard Errors, P-Values, and Confidence Intervals, allowing a statistician to definitively prove *how* and *why* a variable affects the outcome, which is required for regulatory compliance (e.g., FDA drug trials or Banking discrimination laws).

3. How do you interpret a P-Value (P>|t|) of $0.632$ for a specific coefficient in the OLS summary table?
   Answer: The Null Hypothesis for a coefficient is that its true value is exactly $0$ (meaning it has absolutely no effect on the target variable). A P-Value of $0.632$ means there is a $63.2\%$ chance that any observed correlation in our sample data was purely due to random statistical noise. Because $0.632$ is massively higher than the standard $0.05$ threshold, we fail to reject the Null Hypothesis. The variable is statistically insignificant and should likely be removed from the model entirely.
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Statsmodels Econometrics Completed.")
