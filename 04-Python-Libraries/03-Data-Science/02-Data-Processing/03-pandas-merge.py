"""
# ==============================================================================
# LABORATORY: RELATIONAL ALGEBRA (PANDAS MERGE & CONCAT)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# In the real world, data is never stored in one gigantic file. It is distributed 
# across multiple Relational Database tables (e.g., PostgreSQL or Snowflake) 
# to save space and prevent redundancy (Normalization).
#
# - Table 1: `Users` (user_id, name, email)
# - Table 2: `Purchases` (purchase_id, user_id, amount, date)
#
# If you want to find the Name of the user who made Purchase #5, you must 
# mathematically "Join" the two tables together using the shared `user_id` key.
#
# Pandas provides the exact same relational algebra as SQL, but executes it in 
# highly optimized memory using `.merge()` and `.concat()`.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Stack DataFrames vertically using `pd.concat()` (SQL UNION).
# - Join DataFrames horizontally using `pd.merge()` (SQL JOIN).
# - Understand the critical differences between INNER, LEFT, RIGHT, and OUTER joins.
#
# ==============================================================================
"""

import pandas as pd

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. VERTICAL STACKING (CONCAT / SQL UNION)
# ==============================================================================
def demonstrate_concat():
    section_header("Vertical Stacking (pd.concat)")
    
    # Imagine we have sales data separated by month.
    jan_data = pd.DataFrame({
        "Transaction": [1, 2],
        "Amount": [100, 200]
    })
    
    feb_data = pd.DataFrame({
        "Transaction": [3, 4],
        "Amount": [300, 400]
    })
    
    print("January Data:")
    print(jan_data)
    print("\nFebruary Data:")
    print(feb_data)
    
    # 1. CONCAT (Stacking them on top of each other)
    # This is identical to a SQL `UNION ALL`.
    # `ignore_index=True` prevents the index from duplicating (0,1,0,1 -> 0,1,2,3).
    combined = pd.concat([jan_data, feb_data], ignore_index=True)
    
    print("\nCombined Data (pd.concat):")
    print(combined)


# ==============================================================================
# 4. HORIZONTAL JOINING (MERGE / SQL JOIN)
# ==============================================================================
def demonstrate_merge():
    section_header("Horizontal Joining (pd.merge)")
    
    # Table 1: Employees and their Department IDs
    employees = pd.DataFrame({
        "Emp_ID": [101, 102, 103, 104],
        "Name": ["Alice", "Bob", "Charlie", "David"],
        "Dept_ID": ["D1", "D2", "D1", "D99"] # Notice David is in D99
    })
    
    # Table 2: Departments and their Locations
    departments = pd.DataFrame({
        "Dept_ID": ["D1", "D2", "D3"], # Notice D3 exists, but D99 does NOT!
        "Dept_Name": ["Engineering", "Sales", "HR"],
        "Location": ["New York", "London", "Tokyo"]
    })
    
    print("Table A: Employees")
    print(employees)
    print("\nTable B: Departments")
    print(departments)
    
    # 1. INNER JOIN (The Default)
    # Only keeps rows where the `Dept_ID` perfectly matches in BOTH tables.
    # David (D99) is deleted because D99 doesn't exist in Departments.
    # HR (D3) is deleted because no Employee has D3.
    inner_join = pd.merge(employees, departments, on="Dept_ID", how="inner")
    
    print("\n1. INNER JOIN (Strict Match Only):")
    print(inner_join)
    
    # 2. LEFT JOIN
    # Keeps EVERY row from the Left Table (Employees), even if there is no match.
    # David (D99) will be kept, but his Location will be filled with NaN!
    left_join = pd.merge(employees, departments, on="Dept_ID", how="left")
    
    print("\n2. LEFT JOIN (Keep all Employees):")
    print(left_join)
    
    # 3. RIGHT JOIN
    # Keeps EVERY row from the Right Table (Departments).
    # HR (D3) will be kept, but the Employee Name will be NaN!
    right_join = pd.merge(employees, departments, on="Dept_ID", how="right")
    
    print("\n3. RIGHT JOIN (Keep all Departments):")
    print(right_join)
    
    # 4. OUTER JOIN
    # Keeps absolutely everything from BOTH tables. Fills NaN everywhere missing.
    outer_join = pd.merge(employees, departments, on="Dept_ID", how="outer")
    
    print("\n4. OUTER JOIN (Keep Everything!):")
    print(outer_join)


# ==============================================================================
# 5. HANDLING COLUMN NAME COLLISIONS
# ==============================================================================
def demonstrate_suffixes():
    section_header("Column Collisions & Suffixes")
    
    # What if both tables have a column with the exact same name, but they are NOT 
    # the key we are joining on?
    
    # E.g., Both tables have an "Updated_At" column tracking when the row was modified.
    table1 = pd.DataFrame({
        "ID": [1], 
        "Value": ["Alpha"], 
        "Updated_At": ["2024-01-01"]
    })
    
    table2 = pd.DataFrame({
        "ID": [1], 
        "Description": ["First Item"], 
        "Updated_At": ["2024-02-15"]
    })
    
    # Pandas will automatically append suffixes (_x, _y) to prevent the columns 
    # from physically overwriting each other in RAM!
    merged = pd.merge(table1, table2, on="ID", how="inner")
    
    print("Merged Table with automatic Suffixes (_x, _y):")
    print(merged)
    
    # You can explicitly control the suffixes for readability!
    clean_merge = pd.merge(table1, table2, on="ID", how="inner", suffixes=("_emp", "_dept"))
    print("\nMerged Table with Custom Suffixes:")
    print(clean_merge)


def run_all_labs():
    demonstrate_concat()
    demonstrate_merge()
    demonstrate_suffixes()


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. When should you use `pd.concat` vs `pd.merge`?
   Answer: `pd.concat` is for VERTICAL stacking (like SQL `UNION`). You use it when you have identically structured files (e.g., Sales 2023, Sales 2024) and you just want to glue them on top of each other to make one massive timeline. `pd.merge` is for HORIZONTAL joining (like SQL `JOIN`). You use it when you have different tables representing different entities (Users vs Purchases) and you want to mathematically connect them sideways using a shared Foreign Key (e.g., `user_id`).

2. What is the danger of a LEFT JOIN?
   Answer: A LEFT JOIN forces Pandas to retain every single row from the Left Table, regardless of whether a match exists in the Right Table. If a match is not found, Pandas instantly injects `NaN` (Not a Number) values into the missing Right columns. Because Pandas forces homogeneity, injecting a single float `NaN` into an Integer column will instantly upcast the entire column to Float, potentially corrupting strict integer IDs or introducing memory bloat. You must immediately clean these NaNs using `.fillna()` or `.dropna()` after the merge.

3. If Table A has 10 rows with `Dept_ID = 5`, and Table B has 10 rows with `Dept_ID = 5`, how many rows will be produced if you Inner Join them on `Dept_ID`?
   Answer: 100 Rows! This is known as a Cartesian Explosion. An Inner Join matches EVERY valid combination of the key. Since all 10 rows on the left match all 10 rows on the right, it produces $10 \times 10 = 100$ permutations. This is the most common reason junior data scientists accidentally crash production servers with OutOfMemory errors when attempting to merge massive datasets on non-unique keys.
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Relational Algebra (Pandas Merge) Completed.")
