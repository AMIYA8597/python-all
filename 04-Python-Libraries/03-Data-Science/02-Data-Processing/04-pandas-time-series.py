"""
# ==============================================================================
# LABORATORY: TIME SERIES ANALYSIS (PANDAS)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# If you work in Finance (Stock Market), IoT (Sensor Data), or Web Analytics 
# (Server Traffic), your data is heavily indexed by Time.
#
# Raw time data is usually stored in CSVs as a string: "2024-01-15 14:30:00".
# A string is completely useless for mathematics. You cannot subtract two strings 
# to find out how many days have passed. You cannot group strings to find the 
# "Average Monthly Revenue".
#
# Pandas possesses an incredibly powerful `Datetime` engine built directly on 
# top of NumPy's `datetime64` C-structs. 
# It allows you to parse strings into physical Time objects, set them as the 
# DataFrame's Index, and execute massive temporal mathematics (like calculating 
# a 30-Day Moving Average in 2 lines of code).
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Parse strings into `datetime` objects using `pd.to_datetime()`.
# - Execute temporal Aggregations using `.resample()` (e.g., Daily -> Monthly).
# - Calculate Rolling Windows (Moving Averages).
# - Generate Lagged Features using `.shift()` for Machine Learning.
#
# ==============================================================================
"""

import pandas as pd
import numpy as np

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. PARSING AND THE DATETIME INDEX
# ==============================================================================
def demonstrate_datetime():
    section_header("Parsing Strings & The DatetimeIndex")
    
    # Raw data loaded from a CSV
    data = {
        "Date_String": ["2023-01-01", "2023-01-02", "2023-01-03", "2023-01-04"],
        "Revenue": [500, 600, 550, 700]
    }
    df = pd.DataFrame(data)
    
    print("Original DataFrame (Dates are raw strings):")
    print(df.dtypes)
    
    # 1. PARSING TO DATETIME
    # This converts the string into a heavily optimized C-level integer representing 
    # the exact number of nanoseconds since the Unix Epoch (1970-01-01).
    df["Date_String"] = pd.to_datetime(df["Date_String"])
    
    print("\nAfter pd.to_datetime() (Dates are datetime64[ns]):")
    print(df.dtypes)
    
    # 2. SETTING THE DATETIME INDEX
    # Setting the temporal column as the actual Index unlocks the true power 
    # of Pandas Time Series analysis.
    df.set_index("Date_String", inplace=True)
    
    print("\nDataFrame with DatetimeIndex:")
    print(df)
    
    # 3. TEMPORAL SLICING
    # You can now slice the DataFrame using partial human-readable strings!
    print("\nSlicing specifically for '2023-01-02' to '2023-01-03':")
    print(df.loc["2023-01-02":"2023-01-03"])


# ==============================================================================
# 4. RESAMPLING (TEMPORAL GROUPBY)
# ==============================================================================
def demonstrate_resample():
    section_header("Resampling (Daily -> Monthly)")
    
    # Let's generate 365 days of fake Daily Revenue data!
    np.random.seed(42)
    # pd.date_range instantly generates a perfect contiguous temporal array
    dates = pd.date_range(start="2023-01-01", periods=365, freq="D")
    daily_revenue = np.random.normal(loc=1000, scale=200, size=365)
    
    df = pd.DataFrame({"Revenue": daily_revenue}, index=dates)
    
    print(f"Generated 365 Days of Revenue Data. (Shape: {df.shape})")
    print(df.head(3))
    
    # RESAMPLING is exactly like `groupby`, but exclusively for Time!
    # Let's compress the 365 Daily rows into 12 Monthly rows, taking the SUM!
    # "M" stands for Month End.
    monthly_revenue = df.resample("M")["Revenue"].sum()
    
    print("\nResampled to Monthly Revenue (Sum):")
    print(monthly_revenue.head(5))
    
    # We can also resample to Quarters ("Q") or Business Days ("B")!
    quarterly_avg = df.resample("Q")["Revenue"].mean()
    print("\nResampled to Quarterly Revenue (Average):")
    print(quarterly_avg)


# ==============================================================================
# 5. ROLLING WINDOWS & LAGGING
# ==============================================================================
def demonstrate_rolling_and_shifting():
    section_header("Rolling Windows & Lag Features")
    
    # Simulating a Stock Price for 10 days
    dates = pd.date_range(start="2024-01-01", periods=10, freq="D")
    prices = [100, 102, 101, 105, 107, 106, 110, 115, 114, 120]
    
    df = pd.DataFrame({"Price": prices}, index=dates)
    
    # 1. ROLLING WINDOWS (Moving Averages)
    # A 3-Day Moving Average smooths out the chaotic daily volatility.
    # It calculates the mean of [Today, Yesterday, Day Before].
    df["3_Day_MA"] = df["Price"].rolling(window=3).mean()
    
    # 2. SHIFTING (Lag Features)
    # Machine Learning models (like Random Forests) CANNOT understand Time. 
    # To teach an ML model how to predict tomorrow's stock price, you must 
    # physically create a column containing Yesterday's price on the same row!
    # `.shift(1)` pushes the entire column DOWN by 1 row in memory!
    df["Yesterday_Price"] = df["Price"].shift(1)
    
    # 3. CALCULATING PERCENTAGE CHANGE
    # Instantly computes exactly how much the stock grew compared to yesterday.
    df["Daily_Return_%"] = df["Price"].pct_change() * 100
    
    print("Advanced Time Series DataFrame:")
    print(df)
    
    print("\nNotice the NaNs? You cannot calculate a 3-Day Moving Average on ")
    print("Day 1 or Day 2, because you don't have 3 days of historical data yet! ")
    print("You must drop these NaNs before passing the data to a Neural Network.")


def run_all_labs():
    demonstrate_datetime()
    demonstrate_resample()
    demonstrate_rolling_and_shifting()


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Under the hood, how does Pandas store a `datetime` object to execute math so fast?
   Answer: It does not store strings. It stores the date as an `int64` (a 64-bit integer). This integer represents the exact number of nanoseconds that have elapsed since the Unix Epoch (Midnight, January 1, 1970). When you execute a time-based query like "Find all rows from January", Pandas instantly translates "January" into a range of two integers, and executes a hyper-fast C-level integer comparison (`time > A & time < B`). This is mathematically millions of times faster than parsing strings.

2. What is the difference between `.resample("M").sum()` and `.groupby(df.index.month).sum()`?
   Answer: `.groupby(df.index.month)` completely obliterates the timeline. It extracts the raw month number (e.g., 1 for January) and groups ALL Januaries from every year in history together into a single row labeled `1`. 
   `.resample("M")` perfectly preserves the chronological timeline. It groups the data into physical temporal buckets (e.g., `2023-01-31`, `2023-02-28`, `2024-01-31`), ensuring that January 2023 and January 2024 remain distinct, chronologically ordered mathematical entities.

3. Why is `.shift(1)` absolutely critical for Machine Learning?
   Answer: Standard ML algorithms (like Scikit-Learn's Random Forest) are completely blind to the concept of Time. They treat every row in a database as an entirely isolated, independent universe. If you want the model to predict the Weather today, and you know the Weather yesterday is highly correlated to the Weather today, you must use `.shift(1)` to physically drag Yesterday's Weather data down into Today's row in the DataFrame. This is called "Feature Lagging", and it is the only way to mathematically force a standard ML model to perceive the flow of time.
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Pandas Time Series Completed.")
