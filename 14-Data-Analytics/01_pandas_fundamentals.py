"""
# 01 - Data Analytics: NumPy & Pandas Masterclass

## A. Concept Name
Vectorized Data Manipulation with NumPy and Pandas.

## B. One-Sentence Definition
Pandas is a high-performance, in-memory data manipulation library built on top of NumPy that allows AI engineers to clean, transform, and analyze tabular data using fast, vectorized C-operations instead of slow Python loops.

## C. Why Does This Exist?
In raw Python, looping over 1,000,000 rows to multiply two columns takes seconds. In Pandas/NumPy, it takes milliseconds. 
AI models require perfectly clean, numerically encoded tabular data (Tensors/Matrices). Pandas is the bridge between dirty real-world data (CSVs, Excel files with missing values and typos) and pristine matrices ready for Machine Learning.

## D. Intuition & Real-World Analogy
Think of Pandas as Excel on steroids without a graphical interface.
- A **Series** is a single column in Excel.
- A **DataFrame** is the entire spreadsheet.
- **Vectorization** is like writing a formula `=A1*B1` and dragging it all the way down the column. Instead of calculating one by one, the computer's CPU processes chunks of data simultaneously.

## E. Core Mechanics & Mathematical Concepts

### 1. Broadcasting (NumPy Core)
When you do `df['Age'] + 10`, you are adding a scalar (10) to a vector (Age). Instead of throwing an error, NumPy "broadcasts" the 10 across every element instantly in C.

### 2. .loc vs .iloc (The Indexing Rules)
- `.loc[row_label, col_label]`: Accesses by the ACTUAL NAME (Label). Inclusive of the end boundary `[0:5]` includes 5.
- `.iloc[row_index, col_index]`: Accesses by the INTEGER POSITION (0-indexed). Exclusive of the end boundary `[0:5]` stops at 4.

### 3. The Split-Apply-Combine Pattern (GroupBy)
The mathematical foundation of analytics.
1. **Split**: Break the data into groups (e.g., by Department).
2. **Apply**: Calculate a metric for each group (e.g., Mean Salary).
3. **Combine**: Stitch the results back into a new DataFrame.

## F. Common Mistakes & Anti-Patterns (CRITICAL)
1. **Using `.iterrows()`**: NEVER DO THIS. Iterating through a DataFrame row-by-row in Python is 1000x slower than using a vectorized operation or `.apply()`. If you write a `for` loop to modify a DataFrame, you are doing it wrong.
2. **SettingWithCopyWarning**: `df[df['Age'] > 25]['Status'] = 'Adult'`. This causes a massive warning in Pandas because you are modifying a *temporary view* of the data, not the original data. 
   **Fix**: Always use `.loc` to set values: `df.loc[df['Age'] > 25, 'Status'] = 'Adult'`.

## G. Interview Connection
**Q: "How do you handle missing (NaN) values in a dataset?"**
A: "Depending on the context, I can drop them using `.dropna()` if the dataset is large and the missing rows are few. Otherwise, I impute them using `.fillna()`, replacing them with the mean, median, or a specific constant. For time-series, I might use forward-fill or backward-fill interpolation."

## H. Implementation & Guided Practice
"""

import pandas as pd
import numpy as np
import time

def demonstrate_vectorization_vs_loops():
    print("--- 1. The Power of Vectorization (NO LOOPS!) ---")
    
    # Create a DataFrame with 1,000,000 rows
    print("Generating 1,000,000 rows of data...")
    df = pd.DataFrame({
        'Price': np.random.uniform(10, 100, 1000000),
        'Quantity': np.random.randint(1, 10, 1000000)
    })
    
    # Anti-Pattern: Using a Python loop (Iterrows)
    print("\nCalculating Total Sales (Price * Quantity)...")
    start = time.time()
    totals = []
    # NOTE: We only do 50,000 rows for the loop so the script doesn't take forever
    for index, row in df.head(50000).iterrows():
        totals.append(row['Price'] * row['Quantity'])
    loop_time = time.time() - start
    print(f"Anti-Pattern (.iterrows on just 50K rows) took: {loop_time:.4f} seconds")
    
    # Best Practice: Vectorization
    start = time.time()
    # This runs in C via NumPy, instantly calculating all 1,000,000 rows!
    df['Total_Sales'] = df['Price'] * df['Quantity']
    vector_time = time.time() - start
    print(f"Best Practice (Vectorization on ALL 1M rows) took: {vector_time:.4f} seconds")
    print(f"Vectorization is infinitely faster. NEVER USE FOR LOOPS IN PANDAS.")


def demonstrate_loc_and_iloc():
    print("\n--- 2. .loc vs .iloc (Indexing Mastery) ---")
    
    # Setting a custom index (string labels instead of 0, 1, 2)
    data = {
        'Name': ['Alice', 'Bob', 'Charlie', 'David'],
        'Age': [25, 30, 35, 40],
        'Department': ['HR', 'IT', 'IT', 'Sales']
    }
    df = pd.DataFrame(data, index=['ID101', 'ID102', 'ID103', 'ID104'])
    print("DataFrame with Custom String Index:")
    print(df)
    
    # ILOC: Integer position (Python standard, exclusive end)
    print("\n.iloc[0:2] (Gets rows 0 and 1):")
    print(df.iloc[0:2])
    
    # LOC: Label name (Pandas specific, INCLUSIVE end)
    print("\n.loc['ID101':'ID103'] (Gets 101, 102, AND 103):")
    print(df.loc['ID101':'ID103'])
    
    # THE SETTING WITH COPY FIX
    # Anti-pattern (will cause warning in some pandas versions):
    # df[df['Age'] > 30]['Department'] = 'Senior' 
    
    # Correct way to update data based on a condition:
    df.loc[df['Age'] > 30, 'Department'] = 'Exec'
    print("\nAfter updating Dept for Age > 30 using .loc:")
    print(df)


def demonstrate_missing_data_and_groupby():
    print("\n--- 3. Missing Data & The Split-Apply-Combine Pattern ---")
    
    df = pd.DataFrame({
        'City': ['NY', 'NY', 'LA', 'LA', 'SF', 'SF'],
        'Store': ['A', 'B', 'C', 'D', 'E', 'F'],
        'Revenue': [1000, np.nan, 2000, 2500, np.nan, 3000] # Missing data!
    })
    print("Raw Data with NaNs:")
    print(df)
    
    # 1. Impute missing data
    # We will fill missing revenue with the MEAN revenue of the entire company
    mean_rev = df['Revenue'].mean()
    df['Revenue'] = df['Revenue'].fillna(mean_rev)
    print(f"\nAfter filling NaNs with Mean ({mean_rev}):")
    print(df)
    
    # 2. GroupBy (Split-Apply-Combine)
    print("\nTotal Revenue per City (GroupBy):")
    city_rev = df.groupby('City')['Revenue'].sum().reset_index()
    print(city_rev)
    
    # Multiple Aggregations
    print("\nMultiple Aggregations per City:")
    agg_stats = df.groupby('City').agg({
        'Revenue': ['sum', 'mean', 'count']
    })
    print(agg_stats)


## I. Active Recall Questions
"""
1. Why is `.iloc[0:3]` different from `.loc[0:3]`?
   *Answer: `.iloc` is integer-based and exclusive at the end, so it gets indices 0, 1, 2. `.loc` is label-based and inclusive at the end, so it looks for the exact labels '0', '1', '2', and '3' and returns all four.*
2. How does Pandas achieve its massive speed compared to standard Python?
   *Answer: Under the hood, Pandas stores data in contiguous C-arrays (via NumPy) and performs operations using highly optimized, compiled C code (Vectorization) rather than interpreting Python loops line-by-line.*
3. What is the correct way to change the values of a column for rows that meet a specific condition?
   *Answer: Use `.loc`. Example: `df.loc[df['Score'] < 50, 'Status'] = 'Fail'`.*
"""

if __name__ == "__main__":
    print("========== PANDAS & NUMPY MASTERCLASS ==========\n")
    demonstrate_vectorization_vs_loops()
    demonstrate_loc_and_iloc()
    demonstrate_missing_data_and_groupby()
    print("\n========== MASTERCLASS COMPLETE ==========")
