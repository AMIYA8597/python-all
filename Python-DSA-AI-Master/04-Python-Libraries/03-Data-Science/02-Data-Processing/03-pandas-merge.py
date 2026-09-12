"""
Pandas Data Merging, Joining, and Concatenation Masterclass
===========================================================

Module: 03-pandas-merge.py
Author: Python DSA Master Expert
Topics: Data Processing, pandas (merge, join, concat)

1. Mathematical Background
--------------------------
In relational algebra, merging data from multiple tables is performed using join operations.
Let A and B be two relations (DataFrames).
- Inner Join (A ⨝ B): Contains all tuples that satisfy the join condition.
- Left Outer Join (A ⟕ B): Contains all tuples from A and matched tuples from B.
- Right Outer Join (A ⟖ B): Contains matched tuples from A and all tuples from B.
- Full Outer Join (A ⟗ B): Contains all tuples from A and B, matched where possible.
- Cross Join (A × B): Cartesian product of A and B.

2. Big-O Analysis
-----------------
Let N be the number of rows in DataFrame A and M be the number of rows in DataFrame B.
- `pd.concat`: O(N + M) time complexity, as it largely involves memory allocation and copying.
- `pd.merge`:
    - Inner/Outer Joins on indexed columns: O(N + M) expected time using hash joins.
    - Joins on unindexed columns: Can degrade to O(N log N + M log M) due to sorting, or O(N * M) worst-case if highly duplicated keys exist.
- Space Complexity: O(N + M) for storing the new DataFrame.

3. Real-World Applications
--------------------------
- Customer Analytics: Merging customer profiles with their transaction history.
- Financial Modeling: Joining end-of-day stock prices from multiple exchanges.
- Data Warehousing: Combining star schema tables (fact tables and dimension tables).

4. Overview
-----------
This module provides an exhaustive, interactive guide to combining datasets using `pandas`.
It covers `concat`, `merge`, and `join` with robust error handling, modern type hints, and
comprehensive logging.
"""

import pandas as pd
import numpy as np
import logging
from typing import Tuple, List, Optional, Dict, Any

# Configure logging for the interactive lesson
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

def demonstrate_concatenation() -> None:
    """
    Demonstrates `pd.concat` operation along different axes.
    
    Mathematical Context:
    Concatenation is analogous to the union (∪) of two sets, preserving duplicates (multiset union).
    
    Time Complexity: O(N + M)
    """
    logging.info("--- Demonstrating Concatenation (pd.concat) ---")
    
    # Create sample DataFrames
    df1 = pd.DataFrame({
        'A': ['A0', 'A1', 'A2', 'A3'],
        'B': ['B0', 'B1', 'B2', 'B3']
    }, index=[0, 1, 2, 3])
    
    df2 = pd.DataFrame({
        'A': ['A4', 'A5', 'A6', 'A7'],
        'B': ['B4', 'B5', 'B6', 'B7']
    }, index=[4, 5, 6, 7])
    
    # Vertical Concatenation (Axis=0)
    # Adds rows of df2 below df1
    vertical_concat = pd.concat([df1, df2], axis=0)
    print("\nVertical Concatenation:")
    print(vertical_concat)
    
    # Horizontal Concatenation (Axis=1)
    df3 = pd.DataFrame({
        'C': ['C0', 'C1', 'C2', 'C3'],
        'D': ['D0', 'D1', 'D2', 'D3']
    }, index=[0, 1, 2, 3])
    
    horizontal_concat = pd.concat([df1, df3], axis=1)
    print("\nHorizontal Concatenation:")
    print(horizontal_concat)


def demonstrate_inner_merge() -> None:
    """
    Demonstrates Inner Merge using `pd.merge`.
    
    Mathematical Context: A ⨝ B
    Returns only the intersection of keys from both DataFrames.
    """
    logging.info("--- Demonstrating Inner Merge ---")
    
    left = pd.DataFrame({
        'key': ['K0', 'K1', 'K2', 'K3'],
        'A': ['A0', 'A1', 'A2', 'A3'],
        'B': ['B0', 'B1', 'B2', 'B3']
    })
    
    right = pd.DataFrame({
        'key': ['K0', 'K1', 'K2', 'K4'],
        'C': ['C0', 'C1', 'C2', 'C3'],
        'D': ['D0', 'D1', 'D2', 'D3']
    })
    
    # Inner Merge
    # Notice that 'K3' from left and 'K4' from right are dropped
    inner_merged = pd.merge(left, right, how='inner', on='key')
    print("\nInner Merge Result (Intersection):")
    print(inner_merged)


def demonstrate_outer_merge() -> None:
    """
    Demonstrates Full Outer Merge using `pd.merge`.
    
    Mathematical Context: A ⟗ B
    Returns the union of keys from both DataFrames. Missing values are filled with NaN.
    """
    logging.info("--- Demonstrating Outer Merge ---")
    
    left = pd.DataFrame({
        'key': ['K0', 'K1', 'K2', 'K3'],
        'A': ['A0', 'A1', 'A2', 'A3']
    })
    
    right = pd.DataFrame({
        'key': ['K0', 'K1', 'K2', 'K4'],
        'B': ['B0', 'B1', 'B2', 'B3']
    })
    
    outer_merged = pd.merge(left, right, how='outer', on='key')
    print("\nOuter Merge Result (Union with NaNs):")
    print(outer_merged)


def demonstrate_left_right_merge() -> None:
    """
    Demonstrates Left and Right Merges using `pd.merge`.
    
    Mathematical Context: 
    Left Join: A ⟕ B
    Right Join: A ⟖ B
    """
    logging.info("--- Demonstrating Left and Right Merges ---")
    
    left = pd.DataFrame({
        'key': ['K0', 'K1', 'K2', 'K3'],
        'A': ['A0', 'A1', 'A2', 'A3']
    })
    
    right = pd.DataFrame({
        'key': ['K0', 'K1', 'K2', 'K4'],
        'B': ['B0', 'B1', 'B2', 'B3']
    })
    
    left_merged = pd.merge(left, right, how='left', on='key')
    print("\nLeft Merge Result (All from Left, matched from Right):")
    print(left_merged)
    
    right_merged = pd.merge(left, right, how='right', on='key')
    print("\nRight Merge Result (All from Right, matched from Left):")
    print(right_merged)


def perform_complex_merge(
    df_sales: pd.DataFrame, 
    df_customers: pd.DataFrame
) -> pd.DataFrame:
    """
    Performs a complex merge simulating a real-world scenario.
    
    Args:
        df_sales: DataFrame containing transaction records.
        df_customers: DataFrame containing customer demographic data.
        
    Returns:
        Merged DataFrame enriched with customer details.
        
    Raises:
        ValueError: If expected keys are missing in either DataFrame.
    """
    if 'customer_id' not in df_sales.columns or 'customer_id' not in df_customers.columns:
        raise ValueError("Both DataFrames must contain 'customer_id' column for merging.")
    
    # Merge sales with customer info using left join to retain all sales records
    enriched_sales = pd.merge(
        df_sales, 
        df_customers, 
        on='customer_id', 
        how='left',
        indicator=True # Adds _merge column to show match status
    )
    
    return enriched_sales


def run_tests() -> None:
    """
    Executes a suite of test cases to validate the data merging operations.
    """
    logging.info("Running Unit Tests...")
    
    # Test Data Setup
    sales_data = pd.DataFrame({
        'transaction_id': [101, 102, 103, 104],
        'customer_id': [1, 2, 1, 99], # 99 is a missing customer
        'amount': [250.0, 150.0, 300.0, 50.0]
    })
    
    customer_data = pd.DataFrame({
        'customer_id': [1, 2, 3],
        'name': ['Alice', 'Bob', 'Charlie'],
        'tier': ['Gold', 'Silver', 'Bronze']
    })
    
    # Execute Test
    result = perform_complex_merge(sales_data, customer_data)
    
    # Assertions
    assert len(result) == 4, "Length of merged data should match sales data length for left join."
    assert result.loc[result['transaction_id'] == 104, 'name'].isnull().iloc[0], "Unmatched customer should have NaN name."
    assert 'left_only' in result['_merge'].values, "There should be left_only records."
    
    logging.info("All tests passed successfully.")


if __name__ == '__main__':
    print("=========================================================")
    print(" Pandas Data Merging, Joining, and Concatenation Masterclass ")
    print("=========================================================\n")
    
    demonstrate_concatenation()
    demonstrate_inner_merge()
    demonstrate_outer_merge()
    demonstrate_left_right_merge()
    
    run_tests()
