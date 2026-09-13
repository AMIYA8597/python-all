"""
# ==============================================================================
# LABORATORY: CLASSICAL TIME SERIES (ARIMA)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Facebook Prophet is a magical curve-fitter, but it abstracts away the true 
# statistical mathematics of Time Series.
#
# If you work in Quantitative Finance, High-Frequency Trading, or Econometrics, 
# you cannot just use a curve-fitter. You must mathematically prove that your 
# data is Stationary, calculate the exact Autocorrelation of the sequence, 
# and explicitly model the Moving Average of the error terms.
#
# You must use ARIMA (AutoRegressive Integrated Moving Average).
# ARIMA is the foundation of classical statistical forecasting. It forces you 
# to dissect the data into its core mathematical components:
# 1. AR (AutoRegressive): How much does yesterday's price affect today's price?
# 2. I (Integrated): How much must we difference the data to remove the trend?
# 3. MA (Moving Average): How does a sudden shock (error) ripple through time?
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand Stationarity and the Augmented Dickey-Fuller (ADF) Test.
# - Understand Autocorrelation (ACF) and Partial Autocorrelation (PACF).
# - Understand the math of the ARIMA (p, d, q) parameters.
#
# ==============================================================================
"""

import numpy as np
import pandas as pd

# In a real environment: pip install statsmodels
try:
    from statsmodels.tsa.stattools import adfuller
    from statsmodels.tsa.arima.model import ARIMA
    HAS_STATSMODELS = True
except ImportError:
    HAS_STATSMODELS = False

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. STATIONARITY & THE DICKEY-FULLER TEST
# ==============================================================================
def demonstrate_stationarity():
    section_header("Stationarity (The Golden Rule of ARIMA)")
    
    if not HAS_STATSMODELS:
        print("[WARNING] statsmodels not installed.")
        return
        
    print("ARIMA mathematically requires the data to be 'Stationary'.")
    print("A Time Series is Stationary if its Mean (Average) and Variance (Volatility) ")
    print("remain completely constant over time. It cannot have a Trend!")
    
    print("\nIf the stock market goes up 10% every year, it is Non-Stationary. ")
    print("The math of ARIMA will catastrophically break because the linear ")
    print("regression coefficients will fail to converge.")
    
    print("\n--- The Augmented Dickey-Fuller (ADF) Test ---")
    print("This is a statistical Hypothesis Test.")
    print("Null Hypothesis (H0): The data is Non-Stationary.")
    print("Alternate Hypothesis (H1): The data is Stationary.")
    print("If the p-value is < 0.05, we mathematically prove it is Stationary!\n")
    
    # 1. Generate Non-Stationary Data (An upward trend)
    np.random.seed(42)
    time = np.arange(100)
    non_stationary_data = 10 + (time * 0.5) + np.random.normal(0, 2, 100)
    
    print("Executing ADF Test on Non-Stationary Data (Upward Trend)...")
    result = adfuller(non_stationary_data)
    print(f"p-value: {result[1]:.4f}")
    if result[1] > 0.05:
        print("Result: Failed to reject H0. The data is NON-STATIONARY. ARIMA will fail.")
        
    print("\n--- Differencing (The 'I' in ARIMA) ---")
    print("How do we fix it? We take the Difference!")
    print("Instead of predicting the absolute Stock Price, we predict the ")
    print("DAY-OVER-DAY CHANGE in the Stock Price!")
    
    # Calculate Difference: Price(T) - Price(T-1)
    stationary_data = np.diff(non_stationary_data)
    
    print("\nExecuting ADF Test on Differenced Data (Day-over-Day change)...")
    result_diff = adfuller(stationary_data)
    print(f"p-value: {result_diff[1]:.4f}")
    if result_diff[1] < 0.05:
        print("Result: Rejected H0. The data is now STATIONARY! ARIMA can proceed.")


# ==============================================================================
# 4. THE ARIMA PARAMETERS (p, d, q)
# ==============================================================================
def demonstrate_arima_math():
    section_header("The Mathematics of ARIMA (p, d, q)")
    
    print("An ARIMA model is defined by exactly 3 hyperparameters: (p, d, q).")
    
    print("\n1. 'p' (AutoRegressive Lags)")
    print("   How many previous days do we look at? If p=2, we use linear ")
    print("   regression to predict Today based purely on Yesterday and ")
    print("   the Day Before Yesterday.")
    print("   Formula: Y(t) = C + (W1 * Y(t-1)) + (W2 * Y(t-2)) + Error")
    
    print("\n2. 'd' (Degree of Differencing)")
    print("   How many times did we have to subtract the data to make it Stationary?")
    print("   If d=1, we are modeling the 1st derivative (Day-over-Day change).")
    print("   If d=2, we are modeling the 2nd derivative (Acceleration).")
    
    print("\n3. 'q' (Moving Average Lags)")
    print("   This has NOTHING to do with a standard moving average (like a 50-day SMA).")
    print("   It models the ERROR terms! If q=1, we assume that yesterday's ")
    print("   random statistical shock (e.g. a sudden news event) will bleed ")
    print("   over and affect today's price.")
    print("   Formula: Y(t) = C + Error(t) + (W1 * Error(t-1))")
    
    print("\nTo choose p and q, Data Scientists plot the ACF (Autocorrelation Function) ")
    print("and PACF (Partial Autocorrelation Function) charts to physically count ")
    print("the number of statistically significant lags.")


# ==============================================================================
# 5. EXECUTING THE ARIMA MODEL
# ==============================================================================
def demonstrate_arima_execution():
    section_header("Executing the ARIMA Forecast")
    
    if not HAS_STATSMODELS: return
    
    # Generate somewhat complex data (Stationary noise + slight AR pattern)
    np.random.seed(42)
    data = np.random.normal(0, 1, 100)
    for i in range(1, 100):
        data[i] = 0.6 * data[i-1] + np.random.normal(0, 1)
        
    df = pd.Series(data)
    
    try:
        print("Initializing ARIMA with (p=1, d=0, q=0)...")
        # Since the data is already stationary, d=0. 
        # We model it based purely on yesterday (p=1).
        model = ARIMA(df, order=(1, 0, 0))
        
        print("Training the statistical model...")
        fitted_model = model.fit()
        
        print("\n--- Model Summary (Coefficients) ---")
        # The 'ar.L1' coefficient should be roughly 0.6 (since we hardcoded 0.6 above!)
        print(fitted_model.summary().tables[1])
        
        print("\nExecuting 3-Step Future Forecast...")
        forecast = fitted_model.forecast(steps=3)
        print(forecast)
        
    except Exception as e:
        print(f"Execution skipped: {e}")


def run_all_labs():
    demonstrate_stationarity()
    demonstrate_arima_math()
    demonstrate_arima_execution()


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. What is the fundamental difference between standard AutoRegression (the 'p' in ARIMA) and Moving Average (the 'q' in ARIMA)?
   Answer: AutoRegression (AR) predicts Today based on the actual, physical *Values* of Yesterday ($Y_{t-1}$). If Apple stock was \$150 yesterday, we multiply \$150 by a learned weight to predict today. Moving Average (MA) predicts Today based on the unobservable *Error/Residual Shocks* of Yesterday ($\epsilon_{t-1}$). If our model predicted \$148 yesterday, but the actual price was \$150, the Error is +\$2. The MA component assumes this +\$2 shock will mathematically "echo" or bleed into today's price, and multiplies the +\$2 by a learned weight to adjust today's prediction.

2. Why must a Time Series be "Stationary" before applying an ARMA model, and how do we achieve it?
   Answer: ARMA relies on linear regression coefficients. If the data has an aggressive upward trend (non-stationary), the mean is constantly shifting toward infinity. The linear regression equation ($Y_t = C + W_1 \times Y_{t-1}$) will catastrophically fail to fit a single constant baseline ($C$) or stable weights across the timeline, because the mathematical distribution of the 1990s data is completely different from the 2020s data. We fix this by taking the Difference (the 'I' or 'Integration' step). By modeling the Day-over-Day *Change* instead of the absolute price, the mean is forced to exactly 0 (a flat line), stabilizing the variance and allowing the regression weights to converge perfectly.

3. You run an Augmented Dickey-Fuller (ADF) test on your dataset and get a p-value of 0.85. What does this mean, and what must you do?
   Answer: A p-value of 0.85 is vastly higher than the standard 0.05 statistical threshold (alpha). This means you have *Failed to Reject the Null Hypothesis*. Because the Null Hypothesis of the ADF test states that the data is Non-Stationary (has a unit root), the test has mathematically proven that your data has a trend. You cannot run ARMA on this data. You must execute a first-order Differencing operation ($Y_t - Y_{t-1}$), and then re-run the ADF test on the differenced data to verify the p-value has dropped below 0.05.
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Classical Time Series (ARIMA) Completed.")
