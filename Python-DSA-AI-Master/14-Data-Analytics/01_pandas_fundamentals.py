"""
## A. Concept Name
Pandas Fundamentals (Series and DataFrames)

## B. Core Rules / Syntax
- Import pandas: `import pandas as pd`
- Series: 1D array with labels. `pd.Series(data, index=index)`
- DataFrame: 2D table with rows and columns. `pd.DataFrame(data)`
- Selecting columns: `df['col_name']` or `df[['col1', 'col2']]`
- Label-based indexing: `df.loc[rows, cols]`
- Integer-based indexing: `df.iloc[rows, cols]`

## C. Typical Use Cases
- Loading tabular data (CSV, Excel, SQL) into memory for analysis.
- Cleaning, filtering, and transforming raw data.
- Aggregating and summarizing data (groupby, aggregations).
- Joining and merging disparate datasets.

## D. Best Practices
- Avoid iterating over rows using `iterrows()` or `itertuples()`; use vectorized operations.
- Explicitly create copies using `.copy()` when assigning slices of DataFrames to avoid `SettingWithCopyWarning`.
- Use descriptive column names and set appropriate data types (e.g., categories for low-cardinality strings) to save memory.

## E. Common Pitfalls
- Confusing `.loc[]` (inclusive on both ends of a slice) and `.iloc[]` (exclusive on the right end).
- Modifying a DataFrame slice without using `.loc` resulting in `SettingWithCopyWarning`.
- Forgetting that many operations return a new DataFrame instead of modifying in-place unless `inplace=True` is specified.

## F. Example Concept
- Creating DataFrames from dictionaries.
- Using boolean indexing (`df[df['Age'] > 25]`).
- Using `.apply()` for custom functions.

## G. Under the Hood
- Pandas is built on top of NumPy arrays. Data is stored in column-oriented blocks.
- Missing data is often represented as `NaN` (Not a Number), utilizing NumPy's float underlying types, though recent versions support nullable integer types.

## H. Performance & Trade-offs
- Pandas operations are incredibly fast when vectorized but exceptionally slow when dealing with element-by-element iteration in Python.
- DataFrames can consume a lot of memory; large datasets that exceed RAM will cause performance issues (consider tools like Dask or Polars for larger-than-memory datasets).

## I. Related Patterns
- Method chaining (e.g., `df.dropna().assign(new_col=...).groupby(...).mean()`) for readable transformations.
- The Split-Apply-Combine pattern when using `groupby()`.

## X. Project Connection
Provides the data manipulation bedrock for any data analytics, machine learning, or ETL project processing tabular data.
"""
import pandas as pd
import numpy as np

def run_pandas_tutorial():
    print("--- 1. Series and DataFrame Creation ---")
    # Series
    s = pd.Series([10, 20, 30, 40], index=['a', 'b', 'c', 'd'])
    print("Series:\n", s)

    # DataFrame
    data = {
        'Name': ['Alice', 'Bob', 'Charlie', 'David', 'Eva'],
        'Age': [25, 30, 35, 28, 22],
        'City': ['New York', 'London', 'Paris', 'Tokyo', 'Sydney'],
        'Salary': [70000, 80000, 120000, 90000, 60000]
    }
    df = pd.DataFrame(data)
    print("\nDataFrame:\n", df)

    print("\n--- 2. Selection and Filtering ---")
    print("Select single column (Name):\n", df['Name'])
    print("\nSelect multiple columns:\n", df[['Name', 'Salary']])
    
    print("\nFilter: Age > 25\n", df[df['Age'] > 25])
    print("\nMultiple conditions: Age > 25 & Salary > 80000\n", 
          df[(df['Age'] > 25) & (df['Salary'] > 80000)])

    print("\n.loc (label-based indexing) row 0 to 2, Name and City columns:\n", 
          df.loc[0:2, ['Name', 'City']])
    
    print("\n.iloc (integer-based indexing) rows 0 to 2, cols 0 to 2:\n", 
          df.iloc[0:3, 0:3])

    print("\n--- 3. Data Manipulation ---")
    # Adding a column
    df['Bonus'] = df['Salary'] * 0.10
    print("After adding Bonus column:\n", df)

    # Applying a function
    df['Salary_Category'] = df['Salary'].apply(lambda x: 'High' if x > 85000 else 'Medium' if x > 65000 else 'Low')
    print("\nAfter applying lambda to create Salary_Category:\n", df)

    # Dropping a column
    df_dropped = df.drop('City', axis=1)
    print("\nAfter dropping City column:\n", df_dropped)

    print("\n--- 4. GroupBy and Aggregation ---")
    # Adding more data for grouping
    df_extended = pd.DataFrame({
        'Department': ['HR', 'IT', 'IT', 'HR', 'IT', 'Finance'],
        'Employee': ['Alice', 'Bob', 'Charlie', 'David', 'Eva', 'Frank'],
        'Salary': [50000, 80000, 90000, 55000, 75000, 110000]
    })
    
    # Group by Department and calculate mean salary
    grouped = df_extended.groupby('Department')['Salary'].mean()
    print("Mean Salary by Department:\n", grouped)
    
    # Multiple aggregations
    agg_df = df_extended.groupby('Department').agg({
        'Salary': ['mean', 'min', 'max', 'count']
    })
    print("\nMultiple aggregations by Department:\n", agg_df)

    print("\n--- 5. Merging, Joining, and Concatenating ---")
    df1 = pd.DataFrame({'ID': [1, 2, 3], 'Name': ['John', 'Jane', 'Doe']})
    df2 = pd.DataFrame({'ID': [2, 3, 4], 'Age': [28, 32, 25]})
    
    # Inner Join
    merged_inner = pd.merge(df1, df2, on='ID', how='inner')
    print("Inner Merge:\n", merged_inner)
    
    # Left Join
    merged_left = pd.merge(df1, df2, on='ID', how='left')
    print("\nLeft Merge:\n", merged_left)

    # Concatenation
    df3 = pd.DataFrame({'ID': [5], 'Name': ['Smith']})
    concat_df = pd.concat([df1, df3], ignore_index=True)
    print("\nConcatenated DataFrame:\n", concat_df)

if __name__ == "__main__":
    run_pandas_tutorial()
