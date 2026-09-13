"""
02_data_cleaning_eda.py
Comprehensive Guide to Data Cleaning & Exploratory Data Analysis (EDA)

## A. Concept Name
Data Cleaning & Exploratory Data Analysis (EDA)

## B. Motivation
Raw data is rarely ready for modeling. Data cleaning ensures data quality, while EDA helps us understand patterns, anomalies, and relationships within the dataset before applying complex algorithms.

## C. Real-World Application
Data scientists spend up to 80% of their time cleaning and exploring data. It is used in analyzing customer churn, preprocessing medical records for diagnosis prediction, and detecting fraud in financial transactions.

## D. Common Pitfalls
1. Blindly dropping rows with missing values, leading to loss of valuable information.
2. Ignoring data type conversions (e.g., treating dates as strings).
3. Removing outliers without investigating their cause—sometimes anomalies are the most important data points.

## E. Best Practices
1. Always inspect the data (`head()`, `info()`, `describe()`) before modifying it.
2. Use appropriate imputation strategies (mean/median for numerical, mode for categorical) based on data distribution.
3. Document every transformation step to maintain a reproducible data pipeline.

## X. Project Connection
These data cleaning and EDA techniques will be heavily utilized in our final Capstone Project to preprocess raw datasets before feeding them into our predictive machine learning models.

This script covers:
1. Handling Missing Data (NaN)
2. Handling Duplicates
3. Handling Outliers
4. Data Type Conversions
5. Descriptive Statistics & EDA Techniques
"""
import pandas as pd
import numpy as np

def run_cleaning_eda_tutorial():
    # Creating a messy dataset
    data = {
        'ID': [1, 2, 3, 3, 4, 5, 6, 7, 8, 9, 10],
        'Name': ['Alice', 'Bob', 'Charlie', 'Charlie', 'David', 'Eva', np.nan, 'Frank', 'Grace', 'Heidi', 'Ivan'],
        'Age': [25, np.nan, 35, 35, 28, 22, 45, 120, 29, np.nan, 31], # 120 is an outlier
        'Salary': [70000, 80000, 120000, 120000, 90000, 60000, 150000, 65000, 72000, 85000, np.nan],
        'Join_Date': ['2020-01-15', '2021-02-20', '2019-05-10', '2019-05-10', '2022-08-01', 
                      '2023-01-10', '2018-11-22', '2021-07-30', '2020-09-14', '2019-12-01', '2022-03-15']
    }
    df = pd.DataFrame(data)
    
    print("--- 1. Initial Data Inspection (EDA Basics) ---")
    print("Data Head:\n", df.head())
    print("\nData Info:")
    df.info()
    print("\nDescriptive Statistics:\n", df.describe())

    print("\n--- 2. Handling Duplicates ---")
    print(f"Number of duplicates: {df.duplicated().sum()}")
    df = df.drop_duplicates()
    print(f"Duplicates removed. New shape: {df.shape}")

    print("\n--- 3. Handling Missing Data ---")
    print("Missing values per column:\n", df.isnull().sum())
    
    # Approach 1: Fill missing names with 'Unknown'
    df['Name'] = df['Name'].fillna('Unknown')
    
    # Approach 2: Fill missing age with median
    median_age = df['Age'].median()
    df['Age'] = df['Age'].fillna(median_age)
    
    # Approach 3: Drop rows where Salary is missing
    df = df.dropna(subset=['Salary'])
    
    print("\nAfter handling missing data:\n", df.isnull().sum())

    print("\n--- 4. Data Type Conversions ---")
    # Convert Join_Date to datetime
    df['Join_Date'] = pd.to_datetime(df['Join_Date'])
    
    # Extract Year and Month as new features (Feature Engineering)
    df['Join_Year'] = df['Join_Date'].dt.year
    print("\nData Types after conversion:\n", df.dtypes)
    print("\nDataFrame with new Join_Year feature:\n", df[['Name', 'Join_Date', 'Join_Year']].head())

    print("\n--- 5. Handling Outliers ---")
    # Simple outlier detection using Interquartile Range (IQR) for Age
    Q1 = df['Age'].quantile(0.25)
    Q3 = df['Age'].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    print(f"Age IQR Bounds: [{lower_bound}, {upper_bound}]")
    
    # Identifying outliers
    outliers = df[(df['Age'] < lower_bound) | (df['Age'] > upper_bound)]
    print("\nOutliers detected in Age:\n", outliers[['Name', 'Age']])
    
    # Capping outliers (Winsorization)
    df.loc[df['Age'] > upper_bound, 'Age'] = upper_bound
    print("\nMax age after capping:", df['Age'].max())

    print("\n--- 6. Advanced EDA (Correlations) ---")
    numeric_df = df.select_dtypes(include=[np.number])
    correlation_matrix = numeric_df.corr()
    print("\nCorrelation Matrix:\n", correlation_matrix)

if __name__ == "__main__":
    run_cleaning_eda_tutorial()
