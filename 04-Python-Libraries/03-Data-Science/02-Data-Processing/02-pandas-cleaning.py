"""
# ==============================================================================
# LABORATORY: DATA CLEANING & AGGREGATION (PANDAS)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# In academic datasets (like Kaggle's Titanic dataset), the data is perfectly 
# clean. You load it into a Machine Learning model, and it achieves 95% accuracy 
# instantly.
#
# In the real world (e.g., extracting data from hospital medical records), the 
# data is a catastrophic disaster.
# - Half the patients don't have a recorded Age (`NaN`).
# - A doctor accidentally typed "999" for a patient's Weight.
# - The database duplicated 500 records during a server migration.
#
# If you feed this corrupted data into a Neural Network, the Neural Network will 
# assume a 999 lb patient is a biological reality, completely destroying the 
# mathematical gradients. "Garbage In, Garbage Out."
#
# A Data Scientist spends 80% of their career cleaning data, and 20% training models.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Mathematically handle Missing Values (`NaN`) via Dropping or Imputation.
# - Eradicate Data Duplication and anomalies.
# - Perform massive SQL-style Aggregations using `groupby()`.
#
# ==============================================================================
"""

import pandas as pd
import numpy as np

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. HANDLING MISSING DATA (NaN)
# ==============================================================================
def demonstrate_missing_data():
    section_header("Handling Missing Data (NaN)")
    
    # NaN stands for "Not a Number". It is an IEEE 754 floating-point standard.
    # Because it is a float, any column containing a NaN is automatically 
    # upcast to a float by Pandas, even if the rest of the numbers are Integers!
    
    # A corrupted dataset of employees
    data = {
        "Name": ["Alice", "Bob", "Charlie", "David", "Eve"],
        "Age": [25, np.nan, 22, 35, np.nan],         # Bob and Eve forgot their age
        "Salary": [75000, 120000, np.nan, 95000, 110000], # Charlie forgot his salary
        "Department": ["HR", "Sales", "HR", "IT", "Sales"]
    }
    
    df = pd.DataFrame(data)
    print("Original Corrupted DataFrame:")
    print(df)
    
    # 1. IDENTIFYING MISSING DATA
    # `isna()` returns a True/False mask of the entire dataframe.
    # `.sum()` counts the True values per column.
    print("\nCount of Missing Values per Column:")
    print(df.isna().sum())
    
    # 2. STRATEGY A: DROPPING (The Nuclear Option)
    # Drop ANY row that has at least 1 NaN value.
    # Dangerous! We just deleted 60% of our dataset!
    df_dropped = df.dropna()
    print("\nStrategy A (Drop all rows with NaN):")
    print(df_dropped)
    
    # 3. STRATEGY B: IMPUTATION (Statistical Replacement)
    # Instead of deleting Bob and Eve, let's guess their age based on the 
    # Average (Mean) age of the company!
    mean_age = df["Age"].mean()
    print(f"\nCalculated Mean Age: {mean_age:.1f}")
    
    # `.fillna()` replaces all NaNs in that column with the specified value.
    df["Age"] = df["Age"].fillna(mean_age)
    
    # Let's fill Charlie's salary with the Median salary!
    median_salary = df["Salary"].median()
    df["Salary"] = df["Salary"].fillna(median_salary)
    
    print("\nStrategy B (Imputed DataFrame):")
    print(df)
    print("(Notice how the NaN values were surgically replaced!)")


# ==============================================================================
# 4. DUPLICATES AND ANOMALIES
# ==============================================================================
def demonstrate_cleaning():
    section_header("Duplicates and Anomalies")
    
    data = {
        "Name": ["Alice", "Bob", "Charlie", "Alice", "Eve"], # Alice is duplicated!
        "Age": [25, 30, 22, 25, -1],                         # Eve has an impossible age!
        "Salary": [75000, 120000, 50000, 75000, 110000]
    }
    df = pd.DataFrame(data)
    
    print("Original DataFrame (With Duplicates and Anomalies):")
    print(df)
    
    # 1. REMOVING DUPLICATES
    # `drop_duplicates` scans all columns. If two rows are perfectly identical, 
    # it deletes the second one.
    df = df.drop_duplicates()
    print("\nAfter drop_duplicates():")
    print(df)
    
    # 2. FIXING ANOMALIES (Vectorized Replacement)
    # We cannot have an Age of -1. We will replace any Age < 0 with NaN, 
    # effectively flagging it for Imputation later!
    # `np.where(condition, value_if_true, value_if_false)`
    df["Age"] = np.where(df["Age"] < 0, np.nan, df["Age"])
    
    print("\nAfter removing impossible ages (-1 -> NaN):")
    print(df)


# ==============================================================================
# 5. SQL-STYLE AGGREGATION (GROUPBY)
# ==============================================================================
def demonstrate_groupby():
    section_header("Data Aggregation (GroupBy)")
    
    # A massive sales database
    data = {
        "Store": ["New York", "New York", "London", "London", "Tokyo", "Tokyo"],
        "Product": ["Laptops", "Phones", "Laptops", "Phones", "Laptops", "Phones"],
        "Revenue": [500, 300, 400, 600, 900, 200],
        "Profit": [50, 30, 40, 60, 90, 20]
    }
    df = pd.DataFrame(data)
    print("Raw Sales Database:")
    print(df)
    
    # 1. BASIC GROUPBY (SQL: SELECT SUM(Revenue) FROM df GROUP BY Store)
    # We group all rows by "Store", isolate the "Revenue" column, and Sum it.
    revenue_by_store = df.groupby("Store")["Revenue"].sum()
    
    print("\nTotal Revenue by Store:")
    print(revenue_by_store)
    
    # 2. ADVANCED AGGREGATION (.agg)
    # What if we want the SUM of Revenue, but the AVERAGE (Mean) of Profit?
    # `.agg()` allows us to pass a dictionary of specific math operations for 
    # specific columns!
    advanced_agg = df.groupby("Store").agg({
        "Revenue": "sum",
        "Profit": "mean"
    })
    
    print("\nAdvanced Aggregation (Sum Revenue, Mean Profit):")
    print(advanced_agg)


def run_all_labs():
    demonstrate_missing_data()
    demonstrate_cleaning()
    demonstrate_groupby()


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why does a Pandas Integer column automatically convert to Float if a single `NaN` value is introduced?
   Answer: `NaN` (Not a Number) is strictly defined by the IEEE 754 standard as a specific hardware `Float` configuration in CPU architecture. There is no such thing as a "NaN Integer" in traditional C architecture. Because a NumPy array (which powers the Pandas column) must be perfectly homogeneous (one single data type), introducing a Float `NaN` forces NumPy to instantly upcast every single Integer in the entire column into a Float to maintain homogeneity and prevent a crash. (Note: Pandas recently introduced `Int64` nullable integer types to fix this, but it must be explicitly declared).

2. When should you use Data Imputation (filling NaNs with the Mean/Median) instead of just dropping the rows?
   Answer: You drop rows (`dropna`) only if the missing data is an astronomically small percentage of your massive dataset (e.g., dropping 10 corrupted rows out of 10 Million). If $20\%$ of your users didn't fill out their "Age" on a registration form, dropping those rows deletes $20\%$ of your valuable training data! Instead, we Impute the data. We mathematically replace the missing Age with the Median age of all users. This perfectly preserves the size of the dataset without radically shifting the underlying statistical distribution of the Age column.

3. How does `np.where(condition, true_val, false_val)` execute so fast compared to a Python `if/else` loop?
   Answer: `np.where()` is entirely vectorized. It does not evaluate the condition on a single row at a time. It evaluates the boolean condition array simultaneously across the entire column in contiguous C-memory using hardware SIMD (Single Instruction, Multiple Data). It then uses raw memory pointers to instantly bulk-overwrite the `true_val` wherever the boolean mask is True, completely bypassing the Python interpreter.
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Pandas Data Cleaning Completed.")
