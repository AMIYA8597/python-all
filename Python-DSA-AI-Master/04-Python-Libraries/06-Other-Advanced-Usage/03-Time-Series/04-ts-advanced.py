"""
Module: 04-ts-advanced
Description: Comprehensive textbook-grade interactive lesson on Advanced Time Series Analysis.

===========================================================================
Python DSA & AI Masterclass: Advanced Time Series Analysis
===========================================================================

Learning Objectives:
1. Understand the core mathematical concepts behind Time Series (Stationarity, Autocorrelation, Seasonality).
2. Learn advanced usage of Pandas for time series manipulation (Resampling, Windowing, Shifting).
3. Implement and analyze time series transformations and moving averages.
4. Analyze the Big-O time and space complexity of time series algorithms.
5. Solve common interview challenges related to time series (e.g., finding anomalies, calculating moving averages).
6. Explore real-world applications of time series analysis in finance, sales forecasting, and IoT.

Concept Explanation & Mathematical Background:
---------------------------------------------------------------------------
Time Series data is a sequence of data points indexed in time order. Advanced time
series analysis involves understanding the underlying structure of this data to make
predictions (forecasting) or find patterns (anomaly detection).

1. Stationarity:
   A time series is strictly stationary if its statistical properties (mean, variance, 
   autocorrelation) do not change over time.
   - Mean: E(y_t) = mu (constant)
   - Variance: Var(y_t) = sigma^2 (constant)
   - Covariance: Cov(y_t, y_{t-k}) = gamma_k (depends only on lag k)

2. Autocorrelation (ACF) & Partial Autocorrelation (PACF):
   - ACF measures the linear dependence of a variable with itself at two points in time.
   - PACF measures the correlation between the time series and its lag, after removing
     the contributions from the intermediate lags.

3. Moving Averages:
   - Simple Moving Average (SMA): Unweighted mean of the previous N data points.
     SMA = (P_M + P_{M-1} + ... + P_{M-(N-1)}) / N
   - Exponential Moving Average (EMA): Gives more weight to recent prices.
     EMA_t = Value_t * (alpha) + EMA_{t-1} * (1 - alpha)
     where alpha = 2 / (N + 1)

Big-O Analysis:
---------------------------------------------------------------------------
- Simple Moving Average (SMA) of window W: O(N) using sliding window sum. Space: O(N).
- Exponential Moving Average (EMA): O(N) iterative calculation. Space: O(N).
- Naive anomaly detection (Z-score based rolling window): O(N * W) naively, or O(N) optimized.
"""

import sys
import time
import math
import random
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Tuple, Union

try:
    import numpy as np
    import pandas as pd
except ImportError:
    print("Warning: numpy or pandas not installed. Some examples will fall back to vanilla Python.")
    np = None
    pd = None


# =========================================================================
# 1. CORE TIME SERIES ABSTRACTIONS (VANILLA PYTHON)
# =========================================================================

class TimeSeriesPoint:
    """
    Represents a single data point in a time series.
    """
    __slots__ = ['timestamp', 'value']
    
    def __init__(self, timestamp: datetime, value: float):
        self.timestamp = timestamp
        self.value = value

    def __repr__(self) -> str:
        return f"TSPoint({self.timestamp.isoformat()}, {self.value:.4f})"


class TimeSeries:
    """
    A basic Time Series structure supporting foundational operations.
    """
    def __init__(self, name: str = "Series"):
        self.name = name
        self.points: List[TimeSeriesPoint] = []
        
    def add_point(self, point: TimeSeriesPoint) -> None:
        """
        Adds a point, maintaining chronological order via insertion sort logic.
        Time Complexity: O(N) worst case if out of order, O(1) if strictly appending.
        """
        if not self.points or point.timestamp >= self.points[-1].timestamp:
            self.points.append(point)
        else:
            # Insert in order
            for i in range(len(self.points) - 1, -1, -1):
                if self.points[i].timestamp <= point.timestamp:
                    self.points.insert(i + 1, point)
                    return
            self.points.insert(0, point)
            
    def get_values(self) -> List[float]:
        return [p.value for p in self.points]
        
    def __len__(self) -> int:
        return len(self.points)
        

# =========================================================================
# 2. ADVANCED TIME SERIES TRANSFORMS & ALGORITHMS
# =========================================================================

def calculate_sma(ts: TimeSeries, window: int) -> List[Optional[float]]:
    """
    Calculates Simple Moving Average (SMA).
    
    Algorithm:
    Maintains a running sum of the window elements. When the window slides,
    it adds the new element and subtracts the oldest element.
    
    Time Complexity: O(N) - Single pass through the data.
    Space Complexity: O(N) - Array of results.
    """
    print(f"--- Calculating SMA (Window={window}) ---")
    if len(ts) < window or window <= 0:
        return [None] * len(ts)
        
    result: List[Optional[float]] = [None] * (window - 1)
    
    current_sum = sum(p.value for p in ts.points[:window])
    result.append(current_sum / window)
    
    for i in range(window, len(ts)):
        current_sum = current_sum - ts.points[i - window].value + ts.points[i].value
        result.append(current_sum / window)
        
    return result


def calculate_ema(ts: TimeSeries, window: int) -> List[Optional[float]]:
    """
    Calculates Exponential Moving Average (EMA).
    
    Formula: EMA_t = Value_t * alpha + EMA_{t-1} * (1 - alpha)
             alpha = 2 / (window + 1)
             
    Time Complexity: O(N)
    Space Complexity: O(N)
    """
    print(f"--- Calculating EMA (Window={window}) ---")
    if len(ts) < window or window <= 0:
        return [None] * len(ts)
        
    result: List[Optional[float]] = [None] * (window - 1)
    
    # Initial EMA is often just the SMA of the first 'window' points
    initial_sma = sum(p.value for p in ts.points[:window]) / window
    result.append(initial_sma)
    
    alpha = 2.0 / (window + 1.0)
    
    for i in range(window, len(ts)):
        prev_ema = result[-1]
        current_val = ts.points[i].value
        # mypy check workaround - we know prev_ema is not None here
        assert prev_ema is not None 
        current_ema = (current_val * alpha) + (prev_ema * (1.0 - alpha))
        result.append(current_ema)
        
    return result


def detect_anomalies_zscore(ts: TimeSeries, window: int, threshold: float = 2.0) -> List[bool]:
    """
    Rolling Z-Score Anomaly Detection.
    Identifies points that are `threshold` standard deviations away from the rolling mean.
    
    Mathematical Background:
    Z = (X - mu) / sigma
    If |Z| > threshold, X is considered anomalous.
    
    Time Complexity: O(N * W) naively, can be optimized to O(N) using Welford's online algorithm.
                     Here we use a simplified recalculation for clarity which is O(N * W).
    Space Complexity: O(N)
    """
    print(f"--- Detecting Anomalies (Z-Score, Window={window}, Threshold={threshold}) ---")
    anomalies = [False] * len(ts)
    
    if len(ts) < window:
        return anomalies
        
    for i in range(window, len(ts)):
        window_slice = [p.value for p in ts.points[i-window:i]]
        mean = sum(window_slice) / window
        variance = sum((x - mean) ** 2 for x in window_slice) / window
        std_dev = math.sqrt(variance)
        
        if std_dev == 0:
            continue
            
        current_val = ts.points[i].value
        z_score = abs(current_val - mean) / std_dev
        
        if z_score > threshold:
            anomalies[i] = True
            
    return anomalies


# =========================================================================
# 3. ADVANCED USAGE WITH PANDAS (MODERN ECOSYSTEM)
# =========================================================================

def pandas_advanced_ts() -> None:
    """
    Demonstrates advanced Time Series manipulations using Pandas.
    Pandas provides heavily optimized C-backend operations for Time Series.
    """
    print("--- Advanced Time Series with Pandas ---")
    if pd is None or np is None:
        print("Pandas/Numpy not available. Skipping Pandas examples.")
        return
        
    # 1. Create a datetime index and random walk data
    dates = pd.date_range(start='2023-01-01', periods=100, freq='D')
    np.random.seed(42)
    random_walk = np.random.randn(100).cumsum()
    
    df = pd.DataFrame({'value': random_walk}, index=dates)
    
    # 2. Resampling (e.g., Daily to Weekly, taking the mean)
    # Time Complexity: O(N) internally grouping by frequency
    weekly_resampled = df.resample('W').mean()
    print(f"Weekly Resampled (First 3):\n{weekly_resampled.head(3)}\n")
    
    # 3. Rolling Window Operations (e.g., 7-day moving average and standard deviation)
    df['SMA_7'] = df['value'].rolling(window=7).mean()
    df['STD_7'] = df['value'].rolling(window=7).std()
    
    # 4. Shifting (Calculating percentage change day-over-day)
    # Diff formula: (Value_t - Value_{t-1}) / Value_{t-1}
    df['Pct_Change'] = df['value'].pct_change()
    
    print(f"DataFrame with Advanced Features (Rows 7-9):\n{df.iloc[7:10]}\n")
    
    # 5. Stationarity check heuristic (Autocorrelation at lag 1)
    acf_lag1 = df['value'].autocorr(lag=1)
    print(f"Autocorrelation (Lag 1): {acf_lag1:.4f}")
    if acf_lag1 > 0.8:
        print("High autocorrelation detected -> Time Series is likely NON-stationary (Trending).\n")


# =========================================================================
# 4. INTERVIEW CHALLENGE: THE MAX PROFIT PROBLEM
# =========================================================================

def max_profit_time_series(prices: List[float]) -> Tuple[float, int, int]:
    """
    Interview Challenge: Best Time to Buy and Sell Stock (Dynamic Programming / TS)
    
    Given an array of time series data (stock prices), find the maximum profit
    that can be achieved by buying on one day and selling on a future day.
    
    Approach:
    Keep track of the minimum price seen so far.
    Calculate the potential profit for each price (current_price - min_price).
    Update max_profit if potential profit is greater.
    
    Time Complexity: O(N) - One pass.
    Space Complexity: O(1) - Constant extra space.
    """
    print("--- Interview Challenge: Maximum Profit ---")
    if not prices or len(prices) < 2:
        return (0.0, -1, -1)
        
    min_price = prices[0]
    min_day = 0
    
    max_profit = 0.0
    buy_day = 0
    sell_day = 0
    
    for i in range(1, len(prices)):
        current_price = prices[i]
        
        # Check if we have a new minimum
        if current_price < min_price:
            min_price = current_price
            min_day = i
            
        # Check if selling today yields a better profit
        current_profit = current_price - min_price
        if current_profit > max_profit:
            max_profit = current_profit
            buy_day = min_day
            sell_day = i
            
    return (max_profit, buy_day, sell_day)


# =========================================================================
# 5. PERFORMANCE AND EDGE CASES
# =========================================================================

def analyze_performance_and_edge_cases() -> None:
    """
    Discusses performance optimizations and common pitfalls in TS analysis.
    """
    print("--- Performance Analysis & Edge Cases ---")
    print("1. Irregular Time Intervals:")
    print("   Real-world data often misses timestamps. Imputation (forward-fill, interpolation)")
    print("   is crucial before applying transformations.")
    
    print("2. Memory Constraints (Streaming Data):")
    print("   For unbounded IoT data streams, use Welford's algorithm for rolling standard")
    print("   deviation to avoid keeping all window data in memory (O(1) space instead of O(W)).")
    
    print("3. Lookahead Bias:")
    print("   In financial backtesting, ensure rolling metrics at time T only use data")
    print("   up to time T (inclusive or exclusive depending on the signal context).")
    
    print("4. Float Precision:")
    print("   Continuous addition/subtraction in moving averages can lead to floating-point drift.")
    print("   Periodically recalculating the true sum or using math.fsum helps.\n")


# =========================================================================
# 6. TESTS & MAIN EXECUTION
# =========================================================================

def run_tests() -> None:
    """
    Comprehensive test suite.
    """
    print("--- Running Tests ---")
    try:
        # Test 1: Max Profit
        prices = [7.0, 1.0, 5.0, 3.0, 6.0, 4.0]
        profit, b_day, s_day = max_profit_time_series(prices)
        assert abs(profit - 5.0) < 1e-9, f"Expected 5.0, got {profit}"
        assert b_day == 1 and s_day == 4, f"Expected days 1 and 4, got {b_day}, {s_day}"
        
        # Test 2: SMA Calculation
        ts = TimeSeries()
        base_time = datetime(2023, 1, 1)
        for i, val in enumerate([10, 20, 30, 40, 50]):
            ts.add_point(TimeSeriesPoint(base_time + timedelta(days=i), float(val)))
            
        sma = calculate_sma(ts, window=3)
        assert sma[0] is None
        assert sma[1] is None
        assert abs(sma[2] - 20.0) < 1e-9  # (10+20+30)/3
        assert abs(sma[3] - 30.0) < 1e-9  # (20+30+40)/3
        
        print("All tests passed successfully!\n")
    except AssertionError as e:
        print(f"Test Failed: {e}\n")


def generate_synthetic_data(n: int = 20) -> TimeSeries:
    """Helper to generate a noisy sine wave TimeSeries."""
    ts = TimeSeries("Noisy Sine")
    start_time = datetime.now()
    for i in range(n):
        # Base signal: Sine wave
        signal = 10 * math.sin(i * 0.5)
        # Add noise
        noise = random.uniform(-2, 2)
        # Insert an anomaly
        if i == 15:
            noise += 25 
            
        ts.add_point(TimeSeriesPoint(start_time + timedelta(hours=i), signal + noise))
    return ts


if __name__ == "__main__":
    print(f"========== Exploring {'Advanced Time Series Analysis'.upper()} ==========\n")
    
    # 1. Setup Synthetic Data
    ts_data = generate_synthetic_data(20)
    print(f"Generated {len(ts_data)} data points (first 3):")
    for p in ts_data.points[:3]:
        print(f"  {p}")
    print()
    
    # 2. Vanilla Python SMA and EMA
    sma_vals = calculate_sma(ts_data, window=4)
    ema_vals = calculate_ema(ts_data, window=4)
    
    print("SMA and EMA Sample (index 3 to 5):")
    for i in range(3, 6):
        s_val = sma_vals[i]
        e_val = ema_vals[i]
        s_str = f"{s_val:.2f}" if s_val else "None"
        e_str = f"{e_val:.2f}" if e_val else "None"
        print(f"  Index {i} | Raw: {ts_data.points[i].value:.2f} | SMA: {s_str} | EMA: {e_str}")
    print()
    
    # 3. Anomaly Detection
    anomalies = detect_anomalies_zscore(ts_data, window=5, threshold=2.0)
    print("Anomalies Detected at indices:")
    for i, is_anomaly in enumerate(anomalies):
        if is_anomaly:
            print(f"  Index {i}: {ts_data.points[i].value:.2f} (Spike!)")
    print()
    
    # 4. Pandas Advanced Features
    pandas_advanced_ts()
    
    # 5. Interview Challenge
    max_profit_time_series([10, 22, 5, 75, 65, 80])
    
    # 6. Theory & Edge Cases
    analyze_performance_and_edge_cases()
    
    # 7. Tests
    run_tests()
    
    print(f"========== END OF {'Advanced Time Series Analysis'.upper()} ==========\n")
