"""
Module: 04-pandas-time-series
Description: A textbook-grade interactive lesson on Pandas Time Series analysis.
Author: Python DSA Master
Version: 1.0

Learning Objectives:
1. Understand the fundamental building blocks of Pandas Time Series: Timestamps, Periods, and Timedeltas.
2. Master indexing, slicing, and filtering time-based data.
3. Learn to generate date ranges and handle time zones.
4. Perform complex resampling (upsampling and downsampling) and frequency conversion.
5. Apply rolling windows, expanding windows, and exponentially weighted moving averages (EWMA).
6. Understand the mathematical background of Moving Averages and EWMA.
7. Solve a real-world data science application (Algorithmic Trading Signal Generation & Anomaly Detection).

Mathematical Background:
------------------------
1. Simple Moving Average (SMA):
   Given a time series X = {x_1, x_2, ..., x_n}, the SMA of period k at time t is:
   SMA_t = (x_t + x_{t-1} + ... + x_{t-k+1}) / k
   
   Time Complexity: O(N) for a sequence of N elements if rolling sum is maintained (O(1) per step).

2. Exponentially Weighted Moving Average (EWMA):
   EWMA applies weighting factors which decrease exponentially. The weight for each older datum decreases exponentially, never reaching zero.
   Given a decay factor alpha (0 < alpha <= 1):
   EWMA_t = alpha * x_t + (1 - alpha) * EWMA_{t-1}
   
   Alternatively, using span s: alpha = 2 / (s + 1)
   Alternatively, using center of mass (com) c: alpha = 1 / (1 + c)
   Alternatively, using half-life h: alpha = 1 - exp(-ln(2) / h)
   
   Time Complexity: O(N) for computing over the entire series.

Big-O Analysis of Pandas Operations:
------------------------------------
- Accessing a row by datetime index: O(1) on average (backed by hash map or binary search if sorted, mostly O(1)).
- Slicing a time range (e.g., df['2023-01':'2023-03']): O(log N + K), where N is total rows and K is rows in range (for sorted indices).
- Resampling: O(N) as it involves grouping elements by time bins.
- Rolling window calculations: O(N) for basic aggregations (sum, mean, min, max) using optimized Cython routines. O(N * K) for custom python functions where K is window size.

"""

import sys
import time
import math
import random
import datetime
from typing import List, Dict, Any, Optional, Tuple, Union

try:
    import numpy as np
    import pandas as pd
    from pandas.core.frame import DataFrame
    from pandas.core.series import Series
except ImportError:
    print("This module requires numpy and pandas. Please install them using 'pip install numpy pandas'.")
    sys.exit(1)


# ============================================================================
# Section 1: Fundamental Time Series Structures
# ============================================================================

def fundamentals_of_time_series() -> None:
    """
    Demonstrates the three core time series components in Pandas:
    1. Timestamp (represents a single moment in time) -> DatetimeIndex
    2. Period (represents a timespan, e.g., a specific month) -> PeriodIndex
    3. Timedelta (represents an exact length of time) -> TimedeltaIndex
    """
    print("=" * 60)
    print("1. FUNDAMENTALS OF TIME SERIES IN PANDAS")
    print("=" * 60)

    # 1.1 Timestamps
    # pd.Timestamp is the Pandas equivalent of python's datetime.datetime
    ts1: pd.Timestamp = pd.Timestamp('2026-01-01 12:00:00')
    ts2: pd.Timestamp = pd.Timestamp(year=2026, month=1, day=2, hour=8)
    print(f"Timestamp 1: {ts1} | Type: {type(ts1)}")
    print(f"Timestamp 2: {ts2}")

    # 1.2 DatetimeIndex
    # Multiple timestamps form a DatetimeIndex
    dates: List[str] = ['2026-01-01', '2026-01-02', '2026-01-03']
    dt_index: pd.DatetimeIndex = pd.DatetimeIndex(dates)
    series_ts: Series = pd.Series(data=[100, 200, 300], index=dt_index)
    print("\nDatetimeIndex Series:")
    print(series_ts)
    
    # 1.3 Periods
    # A period represents a duration. 'M' stands for month.
    p: pd.Period = pd.Period('2026-01', freq='M')
    print(f"\nPeriod: {p} | Start Time: {p.start_time} | End Time: {p.end_time}")
    
    # 1.4 PeriodIndex
    periods: pd.PeriodIndex = pd.period_range(start='2026-01', end='2026-03', freq='M')
    series_period: Series = pd.Series([10, 20, 30], index=periods)
    print("\nPeriodIndex Series:")
    print(series_period)

    # 1.5 Timedeltas
    # Differences between timestamps
    delta: pd.Timedelta = ts2 - ts1
    print(f"\nTimedelta between {ts2} and {ts1}: {delta}")
    
    # 1.6 TimedeltaIndex
    td_index: pd.TimedeltaIndex = pd.timedelta_range(start='1 days', periods=3, freq='D')
    print("\nTimedeltaIndex:")
    print(td_index)
    print("\n")


# ============================================================================
# Section 2: Date Ranges and Frequencies
# ============================================================================

def generating_date_ranges() -> None:
    """
    Shows how to generate continuous sequences of dates using pd.date_range.
    Explores different frequencies (business days, hours, months, etc.).
    """
    print("=" * 60)
    print("2. DATE RANGES AND FREQUENCIES")
    print("=" * 60)

    # Generate daily dates
    # freq='D' (Calendar Daily)
    daily_dates = pd.date_range(start='2026-01-01', periods=5, freq='D')
    print("Daily Dates (freq='D'):")
    print(daily_dates)

    # Generate business days
    # freq='B' (Business Daily - skips weekends)
    biz_dates = pd.date_range(start='2026-01-01', periods=5, freq='B')
    print("\nBusiness Dates (freq='B', skipping weekends):")
    print(biz_dates)
    
    # Hourly frequency
    hourly_dates = pd.date_range(start='2026-01-01', periods=6, freq='H')
    print("\nHourly Dates (freq='H'):")
    print(hourly_dates)

    # Custom frequencies: E.g., 2 hours and 30 minutes
    custom_freq = pd.date_range(start='2026-01-01', periods=4, freq='2h30min')
    print("\nCustom Frequency (2h30min):")
    print(custom_freq)

    # Monthly frequency (Month End)
    monthly_dates = pd.date_range(start='2026-01-01', periods=3, freq='M')
    print("\nMonthly End Dates (freq='M'):")
    print(monthly_dates)
    print("\n")


# ============================================================================
# Section 3: Indexing, Slicing, and Filtering
# ============================================================================

def indexing_and_slicing() -> None:
    """
    Demonstrates time-based indexing, slicing, and filtering.
    One of Pandas' most powerful features is intelligent datetime slicing.
    """
    print("=" * 60)
    print("3. TIME-BASED INDEXING AND SLICING")
    print("=" * 60)

    # Create a dense time series: every minute for a whole year
    print("Creating a large time series (every minute for 2026)...")
    idx = pd.date_range(start='2026-01-01', end='2026-12-31 23:59:00', freq='T')
    
    # Using np.random.randn for normal distribution
    np.random.seed(42)
    data = np.random.randn(len(idx))
    ts: Series = pd.Series(data, index=idx)
    
    print(f"Total data points: {len(ts)}")
    
    # 3.1 Partial String Indexing (O(1) / O(log N) operations)
    # Get all data for a specific month
    jan_data = ts['2026-01']
    print(f"\nData points in Jan 2026: {len(jan_data)}")
    
    # Get data for a specific day
    val_day = ts['2026-02-14']
    print(f"Data points on Feb 14, 2026: {len(val_day)}")
    
    # 3.2 Slicing
    # Slice between two specific times
    # Note: Datetime slicing includes BOTH endpoints in pandas!
    sliced_ts = ts['2026-03-01 10:00:00' : '2026-03-01 10:05:00']
    print("\nSliced data between 10:00 and 10:05 on March 1st:")
    print(sliced_ts)
    
    # 3.3 Exact Matching
    exact_val = ts['2026-04-15 12:30:00']
    print(f"\nExact value at 2026-04-15 12:30:00: {exact_val:.4f}")
    print("\n")


# ============================================================================
# Section 4: Shifting and Lagging
# ============================================================================

def shifting_and_lagging() -> None:
    """
    Time series often require comparing current values with past (lagging) or future (leading) values.
    `shift()` moves the data along the index, while `tshift()` / `shift(freq=...)` moves the index itself.
    """
    print("=" * 60)
    print("4. SHIFTING AND LAGGING DATA")
    print("=" * 60)

    dates = pd.date_range('2026-01-01', periods=5, freq='D')
    prices = pd.Series([100, 102, 101, 105, 108], index=dates)
    
    print("Original Time Series (e.g., Stock Prices):")
    print(prices)
    
    # 4.1 Lagging (shifting forward in time perspective, data moves down)
    # Used to get yesterday's price today
    lagged = prices.shift(1)
    print("\nLagged by 1 period (Data moved forward):")
    print(lagged)
    
    # 4.2 Leading (shifting backward, data moves up)
    # Used to get tomorrow's price today
    leading = prices.shift(-1)
    print("\nLeading by 1 period (Data moved backward):")
    print(leading)
    
    # 4.3 Percentage Change (Return computation)
    # Formula: (Price_t / Price_{t-1}) - 1
    # Pandas provides a built-in method: pct_change()
    returns = prices.pct_change()
    print("\nDaily Returns (Percentage Change):")
    print(returns)
    print("\n")


# ============================================================================
# Section 5: Resampling and Frequency Conversion
# ============================================================================

def resampling_data() -> None:
    """
    Resampling involves changing the frequency of time series observations.
    - Downsampling: Aggregating higher frequency data to lower frequency (e.g., Days to Months).
    - Upsampling: Interpolating lower frequency data to higher frequency (e.g., Months to Days).
    """
    print("=" * 60)
    print("5. RESAMPLING (DOWNSAMPLING & UPSAMPLING)")
    print("=" * 60)

    # Create minute-level data
    idx = pd.date_range('2026-01-01', periods=100, freq='T') # 'T' = minute
    data = pd.Series(range(100), index=idx)
    
    print("Original Minute-Level Data (first 5 rows):")
    print(data.head())
    
    # 5.1 Downsampling
    # Aggregate minute data into 15-minute chunks using different aggregations
    print("\nDownsampling to 15-minute intervals (Sum):")
    resampled_sum = data.resample('15T').sum()
    print(resampled_sum)
    
    print("\nDownsampling to 15-minute intervals (Mean):")
    resampled_mean = data.resample('15T').mean()
    print(resampled_mean)
    
    # Open-High-Low-Close (OHLC) - Very common in finance
    print("\nDownsampling to 15-minute intervals (OHLC):")
    resampled_ohlc = data.resample('15T').ohlc()
    print(resampled_ohlc)
    
    # 5.2 Upsampling
    # Create weekly data and upsample to daily
    weekly_idx = pd.date_range('2026-01-01', periods=3, freq='W')
    weekly_data = pd.Series([10, 20, 30], index=weekly_idx)
    
    print("\nOriginal Weekly Data:")
    print(weekly_data)
    
    print("\nUpsampling to Daily (Introducing NaNs):")
    daily_upsampled = weekly_data.resample('D').asfreq()
    print(daily_upsampled.head(10))
    
    print("\nUpsampling to Daily with Forward Fill (ffill):")
    # Fills missing values with the last known value
    daily_ffill = weekly_data.resample('D').ffill()
    print(daily_ffill.head(10))
    
    print("\nUpsampling to Daily with Interpolation (Linear):")
    daily_interp = weekly_data.resample('D').interpolate(method='linear')
    print(daily_interp.head(10))
    print("\n")


# ============================================================================
# Section 6: Rolling and Expanding Windows
# ============================================================================

def window_functions() -> None:
    """
    Window functions perform calculations over a sliding or expanding subset of data.
    These are crucial for smoothing out noise and finding trends.
    """
    print("=" * 60)
    print("6. ROLLING, EXPANDING WINDOWS & EWMA")
    print("=" * 60)

    # Generate daily stock-like data with random walk
    np.random.seed(42)
    idx = pd.date_range('2026-01-01', periods=50, freq='D')
    # Random walk: cumulative sum of random normal variables
    price = 100 + np.random.randn(50).cumsum()
    ts = pd.Series(price, index=idx)
    
    print("Original Time Series (First 10 days):")
    print(ts.head(10))
    
    # 6.1 Rolling Window (Simple Moving Average - SMA)
    # A window of size N slides across the data.
    # The first N-1 elements will be NaN because the window isn't full.
    window_size = 5
    sma = ts.rolling(window=window_size).mean()
    
    print(f"\n{window_size}-Day Simple Moving Average (SMA):")
    print(sma.head(10))
    
    # 6.2 Expanding Window
    # The window starts at the beginning of the series and grows with each new data point.
    # Calculates the cumulative mean (or sum, max, etc.) up to the current point.
    exp_mean = ts.expanding(min_periods=1).mean()
    
    print("\nExpanding Mean (Cumulative Average):")
    print(exp_mean.head(10))
    
    # 6.3 Exponentially Weighted Moving Average (EWMA)
    # Gives more weight to recent observations, solving the "lag" issue of SMA.
    # alpha = 2 / (span + 1)
    ewma = ts.ewm(span=5, adjust=False).mean()
    
    print("\n5-Day Exponentially Weighted Moving Average (EWMA):")
    print(ewma.head(10))
    print("\n")


# ============================================================================
# Section 7: Time Zones Handling
# ============================================================================

def timezone_handling() -> None:
    """
    Handling localized times vs naive times.
    Time zones are notoriously tricky; Pandas abstracts away most of the pain.
    """
    print("=" * 60)
    print("7. TIME ZONES HANDLING")
    print("=" * 60)
    
    # Create timezone-naive timestamps
    naive_dates = pd.date_range('2026-01-01 09:00', periods=3, freq='D')
    naive_ts = pd.Series([1, 2, 3], index=naive_dates)
    
    print("Timezone Naive Series:")
    print(naive_ts)
    print(f"Timezone: {naive_ts.index.tz}")
    
    # Localize naive timestamps to a specific timezone (e.g., UTC)
    utc_ts = naive_ts.tz_localize('UTC')
    print("\nLocalized to UTC:")
    print(utc_ts)
    print(f"Timezone: {utc_ts.index.tz}")
    
    # Convert from UTC to another timezone (e.g., US/Eastern)
    eastern_ts = utc_ts.tz_convert('US/Eastern')
    print("\nConverted to US/Eastern:")
    print(eastern_ts)
    print(f"Timezone: {eastern_ts.index.tz}")
    print("\n")


# ============================================================================
# Real-World Application: Trading Signals & Anomaly Detection
# ============================================================================

def real_world_application() -> DataFrame:
    """
    Real-world scenario: Designing a simplistic algorithmic trading signal 
    generator and detecting anomalies (e.g., extreme volatility).
    
    Strategy: Moving Average Crossover.
    - Buy Signal: When short-term MA crosses ABOVE long-term MA.
    - Sell Signal: When short-term MA crosses BELOW long-term MA.
    
    Anomaly Detection:
    - Flag periods where daily return exceeds 3 standard deviations.
    """
    print("=" * 60)
    print("REAL-WORLD APPLICATION: ALGO TRADING & ANOMALY DETECTION")
    print("=" * 60)

    # 1. Generate Synthetic Asset Data
    np.random.seed(101)
    dates = pd.date_range('2025-01-01', periods=365, freq='D')
    # Generate geometric brownian motion-like series for realistic stock prices
    returns = np.random.normal(loc=0.0005, scale=0.02, size=365)
    # Inject an anomaly artificially
    returns[150] = 0.15 # Massive 15% jump
    returns[250] = -0.12 # Massive 12% crash
    
    price = 100 * np.exp(np.cumsum(returns))
    df = pd.DataFrame({'Close': price}, index=dates)
    
    # 2. Compute Moving Averages
    df['SMA_20'] = df['Close'].rolling(window=20).mean()
    df['SMA_50'] = df['Close'].rolling(window=50).mean()
    
    # 3. Generate Trading Signals (1 for Buy, -1 for Sell, 0 for Hold)
    df['Signal'] = 0
    # Buy when 20-day SMA > 50-day SMA
    # Using np.where to vectorize the condition mapping
    df['Signal'] = np.where(df['SMA_20'] > df['SMA_50'], 1, -1)
    
    # The actual trade happens on the CROSSOVER, so we take the difference
    df['Position'] = df['Signal'].diff()
    # If Position == 2, it means signal went from -1 to 1 (BUY)
    # If Position == -2, it means signal went from 1 to -1 (SELL)
    
    # 4. Anomaly Detection (Z-Score of Returns)
    df['Daily_Return'] = df['Close'].pct_change()
    mean_return = df['Daily_Return'].mean()
    std_return = df['Daily_Return'].std()
    
    # Z-score = (X - Mean) / Std
    df['Z_Score'] = (df['Daily_Return'] - mean_return) / std_return
    
    # Flag anomalies: Absolute Z-Score > 3
    df['Anomaly'] = df['Z_Score'].abs() > 3
    
    print("Preview of Trading Data (First 10 rows after MAs are calculated):")
    print(df.iloc[45:55][['Close', 'SMA_20', 'SMA_50', 'Signal', 'Position']])
    
    print("\nDetected Anomalies (High Volatility Events):")
    anomalies = df[df['Anomaly']]
    print(anomalies[['Close', 'Daily_Return', 'Z_Score']])
    print("\nApplication completed successfully.")
    
    return df


# ============================================================================
# Interview Challenge
# ============================================================================

def interview_challenge(ts: pd.Series, max_gap: pd.Timedelta) -> int:
    """
    Common Time Series Interview Challenge:
    Given a Pandas Series indexed by Datetime, find the maximum continuous
    stretch (in terms of number of data points) where the time gap between 
    consecutive data points does NOT exceed `max_gap`.
    
    Args:
        ts (pd.Series): Datetime indexed series.
        max_gap (pd.Timedelta): Maximum allowed gap between consecutive points.
        
    Returns:
        int: Length of the longest continuous stretch.
    """
    print("=" * 60)
    print("INTERVIEW CHALLENGE: MAX CONTINUOUS TIME STRETCH")
    print("=" * 60)
    
    if len(ts) == 0:
        return 0
        
    # Calculate time differences between consecutive indices
    # diff() on a DatetimeIndex yields a TimedeltaIndex
    time_diffs: pd.TimedeltaIndex = ts.index.to_series().diff()
    
    # Check where the gap exceeds max_gap
    # The first element will be NaT (Not a Time), we fill it with False (0)
    gap_exceeded: Series = (time_diffs > max_gap).fillna(False)
    
    # We can group continuous segments using cumulative sum
    # Every time the gap is exceeded, cumulative sum increments, creating a new group ID
    segment_ids: Series = gap_exceeded.cumsum()
    
    # Find the size of each segment
    segment_sizes = segment_ids.value_counts()
    
    max_length = int(segment_sizes.max())
    print(f"Max gap threshold: {max_gap}")
    print(f"Lengths of segments found: {segment_sizes.to_dict()}")
    print(f"Maximum continuous stretch length: {max_length}\n")
    
    return max_length


# ============================================================================
# Test Suite
# ============================================================================

def run_tests() -> None:
    """
    Comprehensive test suite validating the edge cases and correctness of logic.
    """
    print("=" * 60)
    print("RUNNING UNIT TESTS")
    print("=" * 60)
    
    # Test Interview Challenge
    dates = pd.DatetimeIndex([
        '2026-01-01 10:00', # Segment 1 (len 2)
        '2026-01-01 10:05',
        '2026-01-01 10:30', # Gap > 10m! Segment 2 (len 4)
        '2026-01-01 10:35',
        '2026-01-01 10:40',
        '2026-01-01 10:45',
        '2026-01-01 11:10', # Gap > 10m! Segment 3 (len 1)
    ])
    ts = pd.Series(range(len(dates)), index=dates)
    
    ans = interview_challenge(ts, pd.Timedelta(minutes=10))
    assert ans == 4, f"Test failed! Expected 4, got {ans}"
    
    # Test edge case: empty series
    ans_empty = interview_challenge(pd.Series(dtype=float), pd.Timedelta(minutes=10))
    assert ans_empty == 0, f"Test failed! Expected 0, got {ans_empty}"
    
    # Test edge case: single element
    ans_single = interview_challenge(pd.Series([1], index=[pd.Timestamp('2026-01-01')]), pd.Timedelta(minutes=10))
    assert ans_single == 1, f"Test failed! Expected 1, got {ans_single}"

    print("All tests passed successfully! 🚀\n")


# ============================================================================
# Main Execution Block
# ============================================================================

if __name__ == "__main__":
    print(f"========== Exploring PANDAS TIME SERIES ==========\n")
    
    fundamentals_of_time_series()
    generating_date_ranges()
    indexing_and_slicing()
    shifting_and_lagging()
    resampling_data()
    window_functions()
    timezone_handling()
    
    app_data = real_world_application()
    
    # Run tests which internally tests the interview challenge
    run_tests()
    
    print(f"========== END OF PANDAS TIME SERIES ==========\n")
