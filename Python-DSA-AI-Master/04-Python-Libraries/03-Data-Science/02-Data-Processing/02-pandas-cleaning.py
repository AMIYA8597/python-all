"""
Module: 02-pandas-cleaning
Description: A Masterclass on Data Cleaning using Pandas.

=============================================================================
Data Science with Python - Pandas Data Cleaning (Textbook Grade Lesson)
=============================================================================

Learning Objectives:
1. Master the theoretical underpinnings of data quality and integrity.
2. Identify, handle, and logically resolve missing data (NaNs) and duplicates.
3. Understand the mathematical background of Outlier Detection (Z-Score & IQR).
4. Optimize DataFrame memory usage via intelligent type casting.
5. Clean and standardize unstructured text data using Regex.
6. Analyze Big-O time and space complexities of common Pandas cleaning operations.
7. Solve rigorous data cleaning interview challenges.

-----------------------------------------------------------------------------
1. THEORETICAL FOUNDATION: WHY DATA CLEANING MATTERS
-----------------------------------------------------------------------------
In any machine learning pipeline or data science project, 80% of the time is 
often spent cleaning and preparing data. "Garbage In, Garbage Out" (GIGO) is a 
fundamental rule. If the data is polluted with duplicates, outliers, missing 
values, or incorrect types, the downstream model will learn polluted relationships.

Missing Data Types:
- MCAR (Missing Completely At Random): The probability of an instance being missing 
  does not depend on any known or unknown variable.
- MAR (Missing At Random): The probability of an instance being missing depends on 
  another observed variable (e.g., men being less likely to report depression).
- MNAR (Missing Not At Random): The probability depends on the unobserved missing 
  value itself (e.g., wealthy people refusing to report high income).

-----------------------------------------------------------------------------
2. MATHEMATICAL BACKGROUND: OUTLIER DETECTION
-----------------------------------------------------------------------------
Outliers can drastically skew statistics like mean and variance.

A. The Z-Score Method
Assumes a Gaussian (Normal) distribution. Z-score represents how many standard 
deviations a point is from the mean.
Z = (X - μ) / σ
- X: Observation
- μ: Mean
- σ: Standard Deviation
Threshold: Usually, |Z| > 3 indicates an outlier (captures 99.7% of data if normal).

B. The IQR (Interquartile Range) Method
Robust to non-normal distributions.
IQR = Q3 - Q1
- Q1: 25th percentile
- Q3: 75th percentile
Lower Bound = Q1 - 1.5 * IQR
Upper Bound = Q3 + 1.5 * IQR
Any value strictly outside [Lower Bound, Upper Bound] is an outlier.

-----------------------------------------------------------------------------
3. BIG-O COMPLEXITY OF PANDAS OPERATIONS
-----------------------------------------------------------------------------
Let N be the number of rows, and M be the number of columns.
- `df.dropna()`: O(N * M) time complexity.
- `df.fillna()`: O(N * M) time complexity.
- `df.duplicated()`: Average O(N) using a hash map for rows.
- `df.apply()`: O(N) but heavily bounded by Python-level loops unless vectorized.

For optimal performance, ALWAYS prefer vectorized Pandas/NumPy operations 
over row-by-row `.apply()` or `.iterrows()`.
"""

import math
import time
import re
import gc
from typing import List, Dict, Any, Tuple, Optional, Union
import numpy as np
import pandas as pd
from pandas.api.types import is_numeric_dtype

# ==============================================================================
# SECTION 1: MISSING VALUES (IDENTIFICATION & IMPUTATION)
# ==============================================================================

def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Demonstrates advanced techniques for handling missing data.
    
    Operations:
    1. Identify missing values.
    2. Drop columns with excessive missing data (> 50%).
    3. Impute numeric columns with Median (robust to outliers).
    4. Impute categorical columns with Mode.
    5. Interpolate time-series or sequential data.
    
    Args:
        df: Input DataFrame with potential missing values.
        
    Returns:
        pd.DataFrame: Cleaned DataFrame.
    """
    print("\n--- [Section 1] Missing Values Handling ---")
    df_clean = df.copy()
    
    # 1. Identify missing values percentage per column
    missing_pct = df_clean.isna().mean() * 100
    print(f"Missing Value Percentages:\n{missing_pct[missing_pct > 0]}")
    
    # 2. Drop columns with > 50% missing values
    threshold = 0.50
    cols_to_drop = df_clean.columns[df_clean.isna().mean() > threshold]
    df_clean.drop(columns=cols_to_drop, inplace=True)
    if not cols_to_drop.empty:
        print(f"Dropped columns exceeding {threshold*100}% missing: {list(cols_to_drop)}")
        
    # 3 & 4. Impute remaining missing values
    for col in df_clean.columns:
        if df_clean[col].isna().any():
            if is_numeric_dtype(df_clean[col]):
                # Median imputation is robust against outliers unlike mean.
                # O(N log N) for median calculation, O(N) for filling
                median_val = df_clean[col].median()
                df_clean[col].fillna(median_val, inplace=True)
                print(f"Imputed missing '{col}' with median: {median_val}")
            else:
                # Mode imputation for categorical data
                mode_val = df_clean[col].mode()[0]
                df_clean[col].fillna(mode_val, inplace=True)
                print(f"Imputed missing '{col}' with mode: '{mode_val}'")
                
    return df_clean

# ==============================================================================
# SECTION 2: DUPLICATES & INCONSISTENCIES
# ==============================================================================

def remove_duplicates_and_standardize(df: pd.DataFrame, text_col: str) -> pd.DataFrame:
    """
    Identifies and removes duplicate records, and standardizes text columns.
    
    Args:
        df: The DataFrame.
        text_col: A specific text column to standardize.
        
    Returns:
        pd.DataFrame: Deduplicated and standardized DataFrame.
    """
    print("\n--- [Section 2] Duplicates & Text Standardization ---")
    df_clean = df.copy()
    
    # Check for duplicates
    # Time Complexity: O(N) average case using hashing.
    initial_shape = df_clean.shape
    duplicate_count = df_clean.duplicated().sum()
    print(f"Found {duplicate_count} duplicate rows.")
    
    # Drop duplicates keeping the first occurrence
    df_clean.drop_duplicates(keep='first', inplace=True)
    print(f"Shape after deduplication: {df_clean.shape} (from {initial_shape})")
    
    # Standardize Text Column (e.g., removing extra spaces, lowercase, removing special chars)
    if text_col in df_clean.columns:
        print(f"Standardizing text in column: '{text_col}'")
        
        # Vectorized string operations: O(N)
        # .str is a fast accessor for text operations in Pandas
        df_clean[text_col] = (
            df_clean[text_col]
            .astype(str)
            .str.lower()
            .str.strip()  # Strip leading/trailing whitespaces
            .replace(r'[^a-z0-9\s]', '', regex=True) # Remove special chars using regex
            .replace(r'\s+', ' ', regex=True)        # Replace multiple spaces with single space
        )
        print("Text standardization completed.")
        
    return df_clean

# ==============================================================================
# SECTION 3: OUTLIER DETECTION (Z-SCORE & IQR)
# ==============================================================================

def cap_outliers_iqr(df: pd.DataFrame, col: str) -> pd.DataFrame:
    """
    Caps outliers using the IQR (Interquartile Range) method.
    Capping (Winsorization) limits extreme values to the upper and lower bounds.
    
    Args:
        df: Input DataFrame.
        col: The numeric column to apply IQR outlier capping.
        
    Returns:
        pd.DataFrame: DataFrame with capped outliers.
    """
    print(f"\n--- [Section 3] Outlier Handling (IQR) for '{col}' ---")
    df_clean = df.copy()
    
    if col not in df_clean.columns or not is_numeric_dtype(df_clean[col]):
        print(f"Column {col} is not numeric or doesn't exist.")
        return df_clean
        
    # Calculate Q1 (25th percentile) and Q3 (75th percentile)
    Q1 = df_clean[col].quantile(0.25)
    Q3 = df_clean[col].quantile(0.75)
    IQR = Q3 - Q1
    
    # Define bounds
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    # Count outliers
    outliers = df_clean[(df_clean[col] < lower_bound) | (df_clean[col] > upper_bound)]
    print(f"Identified {len(outliers)} outliers based on IQR bounds: [{lower_bound:.2f}, {upper_bound:.2f}]")
    
    # Cap the outliers (Winsorize) using np.where (O(N) time complexity)
    df_clean[col] = np.where(
        df_clean[col] > upper_bound, upper_bound,
        np.where(df_clean[col] < lower_bound, lower_bound, df_clean[col])
    )
    
    print(f"Outliers capped successfully.")
    return df_clean

# ==============================================================================
# SECTION 4: MEMORY OPTIMIZATION & TYPE CASTING
# ==============================================================================

def optimize_memory_usage(df: pd.DataFrame) -> pd.DataFrame:
    """
    Downcasts numeric data types and converts low-cardinality strings to categories
    to significantly reduce memory footprint.
    
    Memory optimization is critical for scaling Pandas up to millions of rows.
    """
    print("\n--- [Section 4] Memory Optimization ---")
    df_opt = df.copy()
    start_mem = df_opt.memory_usage(deep=True).sum() / 1024**2
    print(f"Initial Memory Usage: {start_mem:.2f} MB")
    
    for col in df_opt.columns:
        col_type = df_opt[col].dtype
        
        # Optimize numeric columns
        if is_numeric_dtype(col_type):
            c_min = df_opt[col].min()
            c_max = df_opt[col].max()
            
            # Integer downcasting
            if str(col_type)[:3] == 'int':
                if c_min > np.iinfo(np.int8).min and c_max < np.iinfo(np.int8).max:
                    df_opt[col] = df_opt[col].astype(np.int8)
                elif c_min > np.iinfo(np.int16).min and c_max < np.iinfo(np.int16).max:
                    df_opt[col] = df_opt[col].astype(np.int16)
                elif c_min > np.iinfo(np.int32).min and c_max < np.iinfo(np.int32).max:
                    df_opt[col] = df_opt[col].astype(np.int32)
                    
            # Float downcasting
            else:
                if c_min > np.finfo(np.float16).min and c_max < np.finfo(np.float16).max:
                    df_opt[col] = df_opt[col].astype(np.float16)
                elif c_min > np.finfo(np.float32).min and c_max < np.finfo(np.float32).max:
                    df_opt[col] = df_opt[col].astype(np.float32)
                    
        # Optimize object/string columns to 'category' if cardinality is low (< 50% unique)
        elif col_type == 'object':
            num_unique = len(df_opt[col].unique())
            num_total = len(df_opt[col])
            if num_unique / num_total < 0.5:
                df_opt[col] = df_opt[col].astype('category')
                
    end_mem = df_opt.memory_usage(deep=True).sum() / 1024**2
    reduction = 100 * (start_mem - end_mem) / start_mem
    print(f"Final Memory Usage: {end_mem:.2f} MB")
    print(f"Memory Reduced by: {reduction:.1f}%")
    
    return df_opt

# ==============================================================================
# SECTION 5: INTERVIEW CHALLENGES
# ==============================================================================

def interview_challenge_iqr_numpy(arr: np.ndarray) -> np.ndarray:
    """
    Interview Challenge: 
    Implement IQR Outlier detection and returning the non-outlier array
    USING ONLY NUMPY (No Pandas).
    
    Constraint: Time complexity O(N log N) because of sorting for quartiles.
    
    Args:
        arr: 1D numpy array of numbers.
    Returns:
        1D numpy array filtered without outliers.
    """
    print("\n--- [Section 5] Interview Challenge: Numpy IQR ---")
    if arr.size == 0:
        return arr
        
    # np.percentile computes quartiles. Under the hood, it partitions/sorts.
    q1 = np.percentile(arr, 25)
    q3 = np.percentile(arr, 75)
    iqr = q3 - q1
    
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    
    # Boolean indexing (O(N))
    filtered_arr = arr[(arr >= lower_bound) & (arr <= upper_bound)]
    print(f"Original shape: {arr.shape}, Filtered shape: {filtered_arr.shape}")
    return filtered_arr


def interview_challenge_custom_fillna(df: pd.DataFrame, col: str) -> pd.DataFrame:
    """
    Interview Challenge:
    Fill missing values in a time series using Forward Fill (ffill) and 
    Backward Fill (bfill) logic consecutively, but implement it iteratively 
    as a thought exercise (though natively df.ffill().bfill() is preferred).
    
    Args:
        df: DataFrame
        col: Column to fill.
    """
    print("\n--- [Section 5] Interview Challenge: Custom Fillna ---")
    df_res = df.copy()
    values = df_res[col].values
    
    # Custom O(N) Forward Fill
    last_valid = None
    for i in range(len(values)):
        if pd.isna(values[i]):
            if last_valid is not None:
                values[i] = last_valid
        else:
            last_valid = values[i]
            
    # Custom O(N) Backward Fill for remaining NaNs at the start
    last_valid = None
    for i in range(len(values)-1, -1, -1):
        if pd.isna(values[i]):
            if last_valid is not None:
                values[i] = last_valid
        else:
            last_valid = values[i]
            
    df_res[col] = values
    print("Custom fill completed.")
    return df_res

# ==============================================================================
# TEST SUITE & MAIN EXECUTION
# ==============================================================================

def generate_mock_data() -> pd.DataFrame:
    """Generates a dirty dataset for demonstration purposes."""
    np.random.seed(42)
    n = 1000
    
    data = {
        'id': np.arange(1, n + 1),
        'age': np.random.normal(loc=35, scale=10, size=n),
        'salary': np.random.lognormal(mean=10, sigma=1, size=n), # High right skew -> Outliers
        'department': np.random.choice(['IT', 'HR', 'Finance', 'Sales', np.nan], size=n, p=[0.3, 0.2, 0.2, 0.2, 0.1]),
        'feedback': np.random.choice([' GREAT! ', 'Bad...', 'Ok@!', '   aWeSoMe   '], size=n),
        'useless_col': np.array([np.nan] * n) # 100% missing
    }
    
    df = pd.DataFrame(data)
    
    # Inject missing values in age
    df.loc[np.random.choice(df.index, size=50, replace=False), 'age'] = np.nan
    
    # Inject duplicates
    df = pd.concat([df, df.sample(50, random_state=42)], ignore_index=True)
    
    return df


def run_tests() -> None:
    """End-to-End Execution and testing of all Pandas Cleaning principles."""
    print("========== INITIALIZING DATA CLEANING MASTERCLASS ==========\n")
    
    # 0. Generate Data
    df_raw = generate_mock_data()
    print(f"Raw DataFrame Shape: {df_raw.shape}")
    print("Sample Data:")
    print(df_raw.head())
    
    # 1. Missing Values
    df_step1 = handle_missing_values(df_raw)
    assert 'useless_col' not in df_step1.columns, "Useless column should have been dropped."
    assert not df_step1['age'].isna().any(), "Age missing values should be imputed."
    
    # 2. Duplicates and Text Standardization
    df_step2 = remove_duplicates_and_standardize(df_step1, 'feedback')
    assert df_step2.shape[0] == 1000, "Duplicates were not removed correctly."
    assert df_step2['feedback'].str.contains('@').sum() == 0, "Special characters were not cleaned."
    
    # 3. Outlier Capping (IQR) on Salary
    df_step3 = cap_outliers_iqr(df_step2, 'salary')
    # Validate no extreme values remain
    q3_sal = df_step2['salary'].quantile(0.75)
    iqr_sal = q3_sal - df_step2['salary'].quantile(0.25)
    upper_sal = q3_sal + 1.5 * iqr_sal
    assert df_step3['salary'].max() <= upper_sal + 1, "Outliers not capped correctly."
    
    # 4. Memory Optimization
    df_step4 = optimize_memory_usage(df_step3)
    assert df_step4['department'].dtype == 'category', "Department should be optimized to category."
    
    # 5. Interview Challenges Tests
    test_arr = np.array([10, 12, 11, 15, 14, 100, -50])
    cleaned_arr = interview_challenge_iqr_numpy(test_arr)
    assert 100 not in cleaned_arr and -50 not in cleaned_arr, "Numpy IQR failed to remove outliers."
    
    df_custom = pd.DataFrame({'val': [np.nan, 2, np.nan, 4, np.nan]})
    df_custom_filled = interview_challenge_custom_fillna(df_custom, 'val')
    assert df_custom_filled['val'].iloc[0] == 2.0, "Backward fill failed in custom implementation."
    assert df_custom_filled['val'].iloc[-1] == 4.0, "Forward fill failed in custom implementation."

    print("\n========== ALL TESTS PASSED SUCCESSFULLY! ==========")
    print("The dataset is now cleaned, optimized, and ready for Machine Learning pipelines.")


if __name__ == "__main__":
    start_time = time.time()
    run_tests()
    print(f"\n[Execution Time: {time.time() - start_time:.4f} seconds]")
