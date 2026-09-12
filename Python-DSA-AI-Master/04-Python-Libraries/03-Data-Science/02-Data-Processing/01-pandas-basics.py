"""
Module: 01-pandas-basics
Description: A textbook-grade, interactive lesson on Pandas Basics.

Learning Objectives:
1. Understand the foundational structures of Pandas: Series and DataFrame.
2. Master data ingestion, creation, and inspection techniques.
3. Comprehend index mechanisms: loc and iloc.
4. Perform data cleaning, handling missing values, and type casting.
5. Apply mathematical operations and broadcasting efficiently.
6. Grouping and Aggregating data.
7. Performance analysis, memory optimization, and Big-O complexities of Pandas operations.
8. Solve complex real-world data processing challenges.

Mathematical Background & Big-O Analysis:
Pandas is built on top of NumPy, utilizing contiguous memory blocks for columnar data storage
(BlockManager). This makes operations on columns incredibly fast (O(1) access, O(N) vectorized operations).
However, row-based iterations (like `iterrows`) are notoriously slow due to boxing/unboxing
overhead, often running in O(N) time with massive constant factors.

Common Big-O Complexities:
- Column Selection: O(1)
- Row Selection by Label (loc): O(1) expected, O(N) worst case if non-unique index
- Row Selection by Integer (iloc): O(1)
- Masking/Filtering: O(N)
- Vectorized Arithmetic (e.g., A + B): O(N)
- GroupBy (hash-based): O(N)
- Sorting: O(N log N)
- Concatenation: O(N) where N is the total number of elements.

Understanding these complexities is critical for building scalable data pipelines.
"""

import os
import sys
import time
import math
import string
import random
from typing import List, Dict, Any, Optional, Tuple, Union

try:
    import numpy as np
    import pandas as pd
except ImportError:
    print("Error: numpy or pandas not found. Please install them using 'pip install numpy pandas'.")
    sys.exit(1)


# ==============================================================================
# SECTION 1: INTRODUCTION TO SERIES AND DATAFRAMES
# ==============================================================================

def explore_series() -> None:
    """
    Explores the Pandas Series, which is a one-dimensional labeled array 
    capable of holding any data type (integers, strings, floating point numbers, 
    Python objects, etc.).
    
    A Series has two main components:
    1. The sequence of values.
    2. The sequence of identifiers, which is the index.
    """
    print("=" * 60)
    print("SECTION 1: PANDAS SERIES")
    print("=" * 60)

    # Creating a Series from a list
    data = [10.5, 20.1, 30.8, 40.2]
    # A default integer index (0, 1, 2, 3) is created automatically.
    s1 = pd.Series(data)
    print(f"Basic Series from List:\n{s1}\n")

    # Creating a Series with a custom index
    index_labels = ['a', 'b', 'c', 'd']
    s2 = pd.Series(data, index=index_labels, name="Sensor_Readings")
    print(f"Series with Custom Index and Name:\n{s2}\n")

    # Creating a Series from a Dictionary
    # The dictionary keys become the index.
    dict_data = {"apple": 50, "banana": 20, "cherry": 15, "date": 5}
    s3 = pd.Series(dict_data, name="Fruit_Quantities")
    print(f"Series from Dictionary:\n{s3}\n")
    
    # Mathematical Operations and Broadcasting (O(N) operation)
    # Pandas naturally aligns operations based on the index.
    print(f"Series Math (s3 * 2):\n{s3 * 2}\n")
    
    # Conditional Filtering (Boolean Masking)
    mask = s3 > 15
    print(f"Boolean Mask (s3 > 15):\n{mask}\n")
    print(f"Filtered Series (s3[s3 > 15]):\n{s3[mask]}\n")


def explore_dataframes() -> None:
    """
    Explores the Pandas DataFrame, a 2-dimensional labeled data structure with 
    columns of potentially different types. You can think of it like a spreadsheet 
    or SQL table, or a dict of Series objects.
    """
    print("=" * 60)
    print("SECTION 2: PANDAS DATAFRAMES")
    print("=" * 60)

    # Creating a DataFrame from a dictionary of lists
    # Each key is a column name, and the list represents the column data.
    data = {
        "Employee_ID": [101, 102, 103, 104, 105],
        "Name": ["Alice", "Bob", "Charlie", "David", "Eve"],
        "Department": ["HR", "Engineering", "Engineering", "Marketing", "HR"],
        "Salary": [65000.0, 120000.0, 115000.0, 85000.0, 70000.0],
        "Years_Experience": [3, 8, 7, 4, 5]
    }
    
    df = pd.DataFrame(data)
    
    # Setting a specific column as the index
    # Note: inplace=False by default. Setting it here returns a new DataFrame.
    df_indexed = df.set_index("Employee_ID")
    
    print("DataFrame Structure:\n", df_indexed)
    print("\nDataFrame Info:")
    # df.info() prints directly to stdout. We can capture or just let it print.
    df_indexed.info()
    print("\nDescriptive Statistics:\n", df_indexed.describe())


# ==============================================================================
# SECTION 2: INDEXING, SELECTING, AND FILTERING
# ==============================================================================

def explore_indexing() -> pd.DataFrame:
    """
    Demonstrates `loc` (label-based) and `iloc` (integer-position-based) indexing.
    
    - loc: O(1) expected for unique index, O(N) for non-unique.
    - iloc: O(1) integer-based positional access.
    """
    print("\n" + "=" * 60)
    print("SECTION 3: INDEXING (LOC vs ILOC)")
    print("=" * 60)

    # Generate some dummy data
    np.random.seed(42)
    dates = pd.date_range("20230101", periods=6)
    df = pd.DataFrame(np.random.randn(6, 4), index=dates, columns=list("ABCD"))
    print("Original Time-Series DataFrame:\n", df, "\n")
    
    # 1. Column Selection (O(1))
    print("Select Column 'A':\n", df["A"], "\n")
    
    # 2. Row Selection using loc (Label-based)
    # Selecting the first row by its label (the Timestamp)
    first_date = dates[0]
    print(f"Select Row by Label (loc) for {first_date}:\n", df.loc[first_date], "\n")
    
    # Selecting multiple rows and specific columns using loc
    print("Select specific rows and columns (loc):\n", df.loc["2023-01-02":"2023-01-04", ["A", "C"]], "\n")
    
    # 3. Row Selection using iloc (Position-based)
    print("Select first two rows (iloc):\n", df.iloc[:2], "\n")
    
    # Selecting specific positions (rows 1 & 2, columns 0 & 2)
    print("Select subset by position (iloc):\n", df.iloc[[1, 2], [0, 2]], "\n")
    
    # 4. Boolean Indexing (Filtering)
    # Find all rows where column A is greater than 0
    print("Rows where A > 0:\n", df[df["A"] > 0], "\n")

    return df


# ==============================================================================
# SECTION 3: DATA CLEANING AND PREPARATION
# ==============================================================================

def data_cleaning_and_handling_nan() -> None:
    """
    Handling Missing Data (NaN/NaT).
    Data rarely comes clean. Missing values must be dropped or imputed.
    
    Methods:
    - dropna(): drops rows/cols with NaN.
    - fillna(): replaces NaN with a specified value.
    - isna() / notna(): boolean masks for missing data.
    """
    print("\n" + "=" * 60)
    print("SECTION 4: DATA CLEANING & MISSING VALUES")
    print("=" * 60)

    raw_data = {
        "Name": ["Alice", "Bob", "Charlie", np.nan, "Eve", "Frank"],
        "Age": [25, np.nan, 30, 22, np.nan, 28],
        "Score": [85.5, 90.0, np.nan, 88.0, 92.5, np.nan]
    }
    df = pd.DataFrame(raw_data)
    print("Raw DataFrame with Missing Values (NaN):\n", df, "\n")
    
    # 1. Checking for missing values
    print("Is NaN counts per column:\n", df.isna().sum(), "\n")
    
    # 2. Dropping missing values
    # dropna(axis=0, how='any') -> drops any row containing at least one NaN
    df_dropped = df.dropna(how='any')
    print("DataFrame after dropna (how='any'):\n", df_dropped, "\n")
    
    # 3. Filling missing values (Imputation)
    # We can fill Names with 'Unknown', Age with the median age, Score with mean score.
    # We use a dictionary to apply specific rules per column.
    fill_rules = {
        "Name": "Unknown",
        "Age": df["Age"].median(),
        "Score": df["Score"].mean()
    }
    df_filled = df.fillna(value=fill_rules)
    print("DataFrame after fillna with Median/Mean rules:\n", df_filled, "\n")
    
    # 4. Type Casting (astype)
    # Age should logically be an integer, not float.
    df_filled["Age"] = df_filled["Age"].astype(int)
    print("DataFrame after type casting Age to int:\n", df_filled, "\n")


# ==============================================================================
# SECTION 4: GROUPBY AND AGGREGATION
# ==============================================================================

def groupby_and_aggregations() -> None:
    """
    The "split-apply-combine" paradigm.
    Pandas allows us to group data by certain columns and apply aggregations,
    transformations, or filtering.
    """
    print("\n" + "=" * 60)
    print("SECTION 5: GROUPBY & AGGREGATIONS")
    print("=" * 60)

    # Creating Sales Data
    sales_data = {
        "Region": ["North", "South", "North", "East", "West", "South", "East", "West", "North"],
        "Category": ["Electronics", "Clothing", "Clothing", "Electronics", "Furniture", 
                     "Electronics", "Furniture", "Clothing", "Electronics"],
        "Sales": [1500, 400, 600, 1200, 800, 1800, 900, 500, 2000],
        "Units": [3, 10, 15, 2, 4, 5, 3, 12, 4]
    }
    df = pd.DataFrame(sales_data)
    print("Sales DataFrame:\n", df, "\n")
    
    # 1. Simple GroupBy
    # Total sales per Region
    # O(N) complexity for hash-based grouping
    region_sales = df.groupby("Region")["Sales"].sum()
    print("Total Sales by Region:\n", region_sales, "\n")
    
    # 2. Multi-column GroupBy
    # Total sales per Region and Category
    region_category_sales = df.groupby(["Region", "Category"])["Sales"].sum()
    print("Total Sales by Region & Category:\n", region_category_sales, "\n")
    
    # 3. Multiple Aggregations using `agg`
    # We can compute multiple statistics simultaneously
    agg_funcs = {
        "Sales": ["sum", "mean", "max"],
        "Units": ["sum", "mean"]
    }
    complex_aggs = df.groupby("Region").agg(agg_funcs)
    print("Complex Aggregations per Region:\n", complex_aggs, "\n")


# ==============================================================================
# SECTION 5: PERFORMANCE AND MEMORY OPTIMIZATION
# ==============================================================================

def performance_and_memory_optimization() -> None:
    """
    Demonstrates best practices for memory optimization and performance in Pandas.
    - Iteration vs Vectorization
    - Downcasting datatypes
    - Using Categorical Data
    """
    print("\n" + "=" * 60)
    print("SECTION 6: PERFORMANCE & MEMORY")
    print("=" * 60)

    # Create a reasonably large dataframe
    num_rows = 1_000_000
    df_large = pd.DataFrame({
        "ID": np.random.randint(1, 100000, size=num_rows),
        "Value": np.random.randn(num_rows),
        "Category": np.random.choice(["A", "B", "C", "D", "E"], size=num_rows)
    })
    
    # 1. Memory Usage Analysis
    mem_usage_original = df_large.memory_usage(deep=True).sum() / (1024 ** 2)
    print(f"Original Memory Usage: {mem_usage_original:.2f} MB")
    
    # 2. Downcasting numeric columns
    # We can cast ID to 32-bit integer or smaller since max is 100,000
    df_large["ID"] = pd.to_numeric(df_large["ID"], downcast='integer')
    df_large["Value"] = pd.to_numeric(df_large["Value"], downcast='float')
    
    # 3. Categorical Conversion
    # String columns take a lot of memory. Converting to categorical saves massive space.
    df_large["Category"] = df_large["Category"].astype("category")
    
    mem_usage_optimized = df_large.memory_usage(deep=True).sum() / (1024 ** 2)
    print(f"Optimized Memory Usage: {mem_usage_optimized:.2f} MB")
    print(f"Memory Saved: {100 * (1 - mem_usage_optimized / mem_usage_original):.2f}%\n")
    
    # 4. Anti-Pattern: Iteration (iterrows) vs Vectorization
    print("Performance Comparison: Vectorization vs Iteration")
    # Let's take a small subset for iteration because iterrows on 1M rows will freeze
    df_small = df_large.head(10_000).copy()
    
    # Task: Create a new column which is ID * Value
    
    # Anti-Pattern: Iteration (Extremely Slow)
    start_time = time.time()
    result_list = []
    for index, row in df_small.iterrows():
        result_list.append(row["ID"] * row["Value"])
    df_small["Result_Iter"] = result_list
    iter_time = time.time() - start_time
    
    # Pattern: Vectorization (Extremely Fast, O(N) optimized in C)
    start_time = time.time()
    df_small["Result_Vec"] = df_small["ID"] * df_small["Value"]
    vec_time = time.time() - start_time
    
    print(f"Time using iterrows (10k rows): {iter_time:.4f} sec")
    print(f"Time using Vectorization (10k rows): {vec_time:.4f} sec")
    if vec_time > 0:
        print(f"Speedup: {iter_time / vec_time:.0f}x faster using Vectorization\n")


# ==============================================================================
# SECTION 6: INTERVIEW CHALLENGE & REAL-WORLD APPLICATION
# ==============================================================================

def interview_challenge_moving_average() -> None:
    """
    Common Interview Challenge: Moving Averages and Rolling Windows.
    
    Problem Statement:
    Given a DataFrame of daily stock prices, calculate the 3-day and 7-day 
    moving averages (SMA). Also, compute the daily percentage return.
    """
    print("\n" + "=" * 60)
    print("SECTION 7: INTERVIEW CHALLENGE - MOVING AVERAGES")
    print("=" * 60)

    # Simulating 14 days of stock prices
    dates = pd.date_range("2023-01-01", periods=14, freq="D")
    prices = [100.0, 102.5, 101.0, 105.0, 107.5, 106.0, 110.0, 
              109.0, 112.5, 115.0, 114.0, 118.0, 120.0, 119.0]
    
    stock_df = pd.DataFrame({"Price": prices}, index=dates)
    
    # 1. Calculating Moving Averages using `rolling`
    # O(N) complexity
    stock_df["SMA_3"] = stock_df["Price"].rolling(window=3).mean()
    stock_df["SMA_7"] = stock_df["Price"].rolling(window=7).mean()
    
    # 2. Calculating Daily Returns using `pct_change`
    # Formula: (Price_today - Price_yesterday) / Price_yesterday
    stock_df["Daily_Return_%"] = stock_df["Price"].pct_change() * 100
    
    print("Stock Analysis DataFrame:\n", stock_df.round(2))
    
    # Validate the results manually for a specific day
    # Day 3 SMA_3 should be (100 + 102.5 + 101.0) / 3 = 101.17
    assert math.isclose(stock_df.iloc[2]["SMA_3"], 101.166, abs_tol=0.01)
    print("\n[✔] Moving Average Logic Verified!")


# ==============================================================================
# TEST SUITE
# ==============================================================================

def run_tests() -> None:
    """
    Executes unit tests for basic pandas sanity checks.
    Ensures that our environment is correctly processing data operations.
    """
    print("\n" + "=" * 60)
    print("SECTION 8: RUNNING TESTS")
    print("=" * 60)

    try:
        # Test 1: Series Creation
        s = pd.Series([1, 2, 3])
        assert s.sum() == 6, "Series sum failed"
        
        # Test 2: DataFrame GroupBy
        df = pd.DataFrame({"A": ["foo", "bar", "foo", "bar"], "B": [1, 2, 3, 4]})
        res = df.groupby("A").sum()
        assert res.loc["foo", "B"] == 4, "GroupBy aggregation failed"
        
        # Test 3: Missing Values Fill
        df_nan = pd.DataFrame({"Val": [1.0, np.nan, 3.0]})
        df_filled = df_nan.fillna(0.0)
        assert df_filled["Val"].sum() == 4.0, "Fillna failed"
        
        print("[✔] All Pandas Core Integrity Tests Passed Successfully!")
    except AssertionError as e:
        print(f"[✘] Test Failed: {e}")


# ==============================================================================
# MAIN EXECUTION
# ==============================================================================

if __name__ == "__main__":
    print("==================================================================")
    print("PANDAS BASICS: COMPREHENSIVE INTERACTIVE LESSON")
    print("==================================================================\n")
    
    explore_series()
    explore_dataframes()
    explore_indexing()
    data_cleaning_and_handling_nan()
    groupby_and_aggregations()
    performance_and_memory_optimization()
    interview_challenge_moving_average()
    
    run_tests()
    
    print("\n==================================================================")
    print("LESSON COMPLETED SUCCESSFULLY")
    print("==================================================================")
