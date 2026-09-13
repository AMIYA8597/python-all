"""
# ==============================================================================
# LABORATORY: TIME SERIES FORECASTING (FACEBOOK PROPHET)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You cannot use standard Machine Learning (like Random Forest or XGBoost) to 
# predict the stock market or future website traffic.
#
# Why? Because standard ML assumes that all rows of data are Independent and 
# Identically Distributed (IID). If you scramble the rows in a Random Forest 
# dataset, the model still trains perfectly.
#
# Time Series data is strictly Sequential. The traffic on Tuesday is mathematically 
# dependent on the traffic from Monday. If you scramble the rows, you destroy 
# the space-time continuum!
#
# Traditional Time Series math (like ARIMA) is incredibly complex, requiring 
# deep statistical knowledge of "Stationarity", "Differencing", and "Autocorrelation".
# Facebook open-sourced Prophet to solve this. It abstracts the complex math, 
# modeling Time Series as an additive curve fitting exercise, natively handling 
# Daily Seasonality, Weekly Seasonality, and Holidays automatically!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the components of Time Series (Trend + Seasonality + Noise).
# - Understand the architecture of Facebook Prophet.
# - Execute a Forecast and model Holiday effects.
#
# ==============================================================================
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# In a real environment: pip install prophet
try:
    from prophet import Prophet
    HAS_PROPHET = True
except ImportError:
    HAS_PROPHET = False

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. TIME SERIES COMPONENTS (TREND + SEASONALITY)
# ==============================================================================
def demonstrate_time_series_math():
    section_header("The Math of Time Series")
    
    print("Prophet assumes that every data point (e.g., website traffic today) ")
    print("is composed of 4 mathematical equations added together:\n")
    
    print("y(t) = g(t) + s(t) + h(t) + e(t)\n")
    
    print("1. Trend g(t)  : The overarching, non-periodic growth of the company.")
    print("2. Season s(t) : The cyclical patterns (Traffic spikes every Tuesday, ")
    print("                 traffic drops every Summer).")
    print("3. Holiday h(t): Irregular, massive anomalies (Black Friday).")
    print("4. Error e(t)  : The unpredictable random noise of the universe.")
    
    print("\nUnlike ARIMA (which tries to predict the next step based on the ")
    print("previous step), Prophet is a Curve Fitter. It fits a Fourier Series ")
    print("curve to the Seasonality and a piecewise linear curve to the Trend, ")
    print("making it highly resilient to missing data and outliers!")


# ==============================================================================
# 4. EXECUTING FACEBOOK PROPHET
# ==============================================================================
def demonstrate_prophet():
    section_header("Executing a Prophet Forecast")
    
    if not HAS_PROPHET:
        print("[WARNING] Prophet not installed. Install via: pip install prophet")
        return
        
    print("Prophet requires a very strict, non-negotiable DataFrame format.")
    print("Column 1: MUST be named 'ds' (Date Stamp).")
    print("Column 2: MUST be named 'y' (The numeric value to predict).\n")
    
    # 1. CREATE SYNTHETIC DATA
    # 365 days of website traffic with an upward trend and a weekend drop-off.
    dates = [datetime(2023, 1, 1) + timedelta(days=i) for i in range(365)]
    traffic = []
    
    for i, date in enumerate(dates):
        base_traffic = 1000 + (i * 2) # Upward Trend
        if date.weekday() >= 5:       # Weekend Drop-off
            base_traffic -= 300
        noise = np.random.normal(0, 50)
        traffic.append(base_traffic + noise)
        
    df = pd.DataFrame({'ds': dates, 'y': traffic})
    
    try:
        # 2. INITIALIZE AND TRAIN THE MODEL
        # We tell Prophet to explicitly look for Yearly and Weekly cycles.
        model = Prophet(yearly_seasonality=True, weekly_seasonality=True)
        
        # Prophet handles holidays natively! You just pass the country code.
        model.add_country_holidays(country_name='US')
        
        print("Training Prophet on 1 year of historical data...")
        model.fit(df)
        
        # 3. CREATE THE FUTURE DATAFRAME
        # Prophet creates an empty DataFrame extending 30 days into the future!
        future_df = model.make_future_dataframe(periods=30)
        
        # 4. EXECUTE THE FORECAST
        print("\nExecuting 30-Day Forecast...")
        forecast = model.predict(future_df)
        
        print("\n--- Forecast Output (Next 3 Days) ---")
        # Prophet outputs the exact Prediction ('yhat'), and the 80% Confidence 
        # Intervals ('yhat_lower', 'yhat_upper').
        display_cols = ['ds', 'yhat', 'yhat_lower', 'yhat_upper']
        print(forecast[display_cols].tail(3))
        
        print("\nIn a real script, you would plot this instantly using:")
        print("  fig = model.plot(forecast)")
        print("  fig2 = model.plot_components(forecast)")
        
    except Exception as e:
        print(f"Execution skipped: {e}")


def run_all_labs():
    demonstrate_time_series_math()
    demonstrate_prophet()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why must you use a specialized Time Series algorithm (like Prophet or ARIMA) instead of a standard Random Forest or Neural Network?
   Answer: Standard Machine Learning algorithms assume that all data points are Independent and Identically Distributed (IID). If you shuffle the rows of a housing dataset, a Random Forest still perfectly learns the relationship between `square_footage` and `price`. Time Series data violates the IID assumption because it is strictly sequential; the value at $T=5$ is mathematically dependent on the value at $T=4$ (Autocorrelation). If you shuffle Time Series data, you destroy the fabric of time. Traditional ML models have no native concept of sequence, trends, or cyclical seasonality, leading to catastrophic forecasting failures.

2. What is the difference between "Additive" and "Multiplicative" Seasonality in Prophet?
   Answer: In Additive Seasonality, the magnitude of the seasonal spike remains constant regardless of the overall trend. If a store gets exactly +500 extra customers every Christmas, whether they are a small startup or a massive corporation, you use Additive. In Multiplicative Seasonality, the seasonal spike scales proportionally with the trend. If a store sees a 20% increase in traffic every Christmas, the absolute number of customers gained will be massive if the overall baseline trend of the company has grown. If the company is growing exponentially, you MUST configure Prophet to use Multiplicative Seasonality, otherwise it will massively under-predict the future holiday spikes.

3. In classical statistics (ARIMA), you must make the data "Stationary" (constant mean and variance) before modeling by calculating rolling differences. Why does Prophet NOT require you to make the data Stationary?
   Answer: ARIMA is an Autoregressive model; it uses linear regression to predict $Y_t$ based on the previous actual values $Y_{t-1}, Y_{t-2}$. If the data has a massive upward trend (non-stationary), the linear regression coefficients become unstable and the math breaks. Prophet is NOT autoregressive. It is a Generalized Additive Curve-Fitting Model. It relies on Fourier Series (sines and cosines) to mathematically fit the seasonal curves, and piecewise linear regression to explicitly fit the trend. Because it models the non-stationary Trend as a distinct, explicit mathematical component, it completely bypasses the strict statistical requirement for stationarity!
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Time Series (Prophet) Completed.")
