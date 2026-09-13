"""
# ==============================================================================
# LABORATORY: DATA PROCESSING ARCHITECTURE (PANDAS BASICS)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# NumPy is phenomenal for raw matrix multiplication, but it is deeply flawed 
# for real-world datasets. 
# 
# Why? Because a NumPy array enforces strict Homogeneity. It must contain 
# exactly one data type (e.g., exclusively 64-bit floats). 
# A real-world Excel Spreadsheet or SQL Table contains a mix of Integers (Ages), 
# Floats (Salaries), Strings (Names), and Timestamps (Registration Date).
#
# Pandas solves this. It provides the `DataFrame`. 
# Under the hood, a DataFrame is simply a Python Dictionary. The keys are the 
# Column Names, and the values are independent 1D NumPy arrays (Series)!
# Because each column is its own isolated NumPy array, Column A can be strict 
# Strings, and Column B can be strict Floats. 
#
# Pandas gives you the vectorized speed of NumPy, combined with the structural 
# logic of an SQL database.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the architectural difference between `Series` and `DataFrame`.
# - Master `.loc` (Label-based) vs `.iloc` (Integer-based) indexing.
# - Execute vectorized boolean masking (SQL WHERE).
#
# ==============================================================================
"""

import pandas as pd
import numpy as np

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. SERIES AND DATAFRAMES
# ==============================================================================
def demonstrate_structures():
    section_header("The Pandas Architecture")
    
    # 1. THE SERIES (1D NumPy Array + Label Index)
    # A Series is a single column of data. 
    # Unlike a raw NumPy array, it attaches a permanent "Label" to every row!
    ages = pd.Series([25, 30, 22], index=["Alice", "Bob", "Charlie"], name="Age")
    
    print("Pandas Series (1D):")
    print(ages)
    
    # 2. THE DATAFRAME (2D Dictionary of Series)
    # A DataFrame is physically constructed by combining multiple Series together.
    data = {
        "Name": ["Alice", "Bob", "Charlie", "David", "Eve"],
        "Age": [25, 30, 22, 35, 28],
        "Salary": [75000, 120000, 50000, 95000, 110000],
        "Department": ["Engineering", "Sales", "Engineering", "HR", "Sales"]
    }
    
    df = pd.DataFrame(data)
    
    print("\nPandas DataFrame (2D):")
    print(df)
    
    # Proof of architecture: Extracting a single column returns a Series!
    col = df["Salary"]
    print(f"\nExtracting a single column: Type is {type(col)}")


# ==============================================================================
# 4. SLICING AND INDEXING (.loc vs .iloc)
# ==============================================================================
def demonstrate_indexing():
    section_header("Advanced Indexing (.loc vs .iloc)")
    
    df = pd.DataFrame({
        "Name": ["Alice", "Bob", "Charlie", "David", "Eve"],
        "Age": [25, 30, 22, 35, 28],
        "Salary": [75000, 120000, 50000, 95000, 110000]
    })
    
    # Let's change the Index from default numbers [0, 1, 2] to actual strings!
    df.set_index("Name", inplace=True)
    
    print("DataFrame with Custom String Index:")
    print(df)
    
    # 1. LABEL-BASED INDEXING (.loc)
    # `.loc` strictly searches the human-readable Index Labels.
    # It answers the question: "Get me the row physically labeled 'Charlie'."
    charlie_data = df.loc["Charlie"]
    print("\n.loc['Charlie'] -> Label Search:")
    print(charlie_data)
    
    # 2. INTEGER-BASED INDEXING (.iloc)
    # `.iloc` completely ignores the human labels. It strictly searches the 
    # underlying C-array memory indices (0, 1, 2, 3).
    # It answers the question: "Get me the 3rd row in memory, regardless of its name."
    row_2 = df.iloc[2]
    print("\n.iloc[2] -> Memory Index Search:")
    print(row_2)
    print("(Notice it perfectly matches Charlie, because Charlie is at memory index 2!)")
    
    # 3. SLICING (Matrix Extraction)
    # Extracting a specific subset of Rows AND Columns simultaneously!
    # df.loc[ row_labels, column_labels ]
    subset = df.loc[["Alice", "Eve"], ["Salary"]]
    print("\n.loc[['Alice', 'Eve'], ['Salary']]:")
    print(subset)


# ==============================================================================
# 5. VECTORIZED BOOLEAN MASKING (SQL WHERE)
# ==============================================================================
def demonstrate_masking():
    section_header("Vectorized Filtering (Boolean Masks)")
    
    # DO NOT LOOP OVER A DATAFRAME.
    # If you use `for index, row in df.iterrows():`, you are crashing the 
    # performance down to Python speeds. 
    # Always use Vectorized Masks!
    
    df = pd.DataFrame({
        "Name": ["Alice", "Bob", "Charlie", "David", "Eve"],
        "Age": [25, 30, 22, 35, 28],
        "Salary": [75000, 120000, 50000, 95000, 110000],
        "Department": ["Engineering", "Sales", "Engineering", "HR", "Sales"]
    })
    
    # Objective: Find everyone in Engineering making more than $60,000.
    
    # 1. CREATE THE MASK
    # This executes entirely in C, instantly returning a True/False array.
    mask = (df["Department"] == "Engineering") & (df["Salary"] > 60000)
    
    # 2. APPLY THE MASK
    # We pass the True/False array back into the DataFrame. 
    # It instantly drops all the False rows!
    filtered_df = df[mask]
    
    print("Original DataFrame:")
    print(df)
    
    print("\nFiltered (Engineering AND Salary > 60k):")
    print(filtered_df)
    
    # Objective 2: Find people in Sales OR HR
    # Using `.isin()` is massively faster than chaining `(Dept == A) | (Dept == B)`
    mask_or = df["Department"].isin(["Sales", "HR"])
    print("\nFiltered (.isin(['Sales', 'HR'])):")
    print(df[mask_or])


def run_all_labs():
    demonstrate_structures()
    demonstrate_indexing()
    demonstrate_masking()


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Under the hood, how does a Pandas DataFrame store memory?
   Answer: A Pandas DataFrame is physically constructed as a Python Dictionary. The Dictionary Keys are the human-readable Column Names. The Dictionary Values are completely independent 1-Dimensional NumPy `ndarray` objects (called Series). Because each column is an isolated NumPy array, Column A can lock its memory block to strict `float64`, while Column B locks its memory block to strict `int32`, allowing for high-performance vectorized math on tabular datasets containing heterogeneous data types.

2. What is the fundamental difference between `.loc` and `.iloc`?
   Answer: `.loc` is strictly Label-based. It searches the custom, human-readable Index attached to the DataFrame. If the rows are labeled with dates, you query `.loc["2024-01-01"]`. `.iloc` is strictly Integer-based. It completely ignores the human labels and accesses the physical memory array directly by its C-level integer offset. You query `.iloc[0]` to get the absolute first row in memory. **Critical Edge Case:** If you slice using `.loc[A:B]`, the end label $B$ is INCLUDED. If you slice using `.iloc[0:5]`, the end index $5$ is EXCLUDED (matching standard Python slicing rules).

3. Why is `for index, row in df.iterrows():` considered a catastrophic anti-pattern?
   Answer: `iterrows()` completely destroys the performance benefits of Pandas. It rips the data out of the optimized $C$ contiguous memory blocks, dynamically converts every single row into a slow Python `Series` object, and yields it to the slow Python Interpreter. A loop that takes 10 minutes using `iterrows()` will execute in 0.05 seconds if rewritten using vectorized Boolean Masking (e.g., `df[df['Salary'] > 50000]`), because the masking completely bypasses Python and executes purely in hardware SIMD vectorization.
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Pandas Basics Completed.")
