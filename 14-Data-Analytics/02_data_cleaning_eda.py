"""
# ==============================================================================
# LABORATORY: DATA ANALYTICS (DATA CLEANING & EDA)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A junior data scientist trains a Machine Learning model on a dataset containing 
# missing values (NaN) and extreme outliers (e.g., an employee age of 999). 
# They deploy the model to Production. It predicts that a 999-year-old employee 
# requires a $50,000,000 salary. The model is mathematically corrupt.
#
# A senior data engineer understands that "Garbage In, Garbage Out" (GIGO) is 
# an absolute law of physics. Before any math is performed, they execute rigorous 
# Exploratory Data Analysis (EDA) and Data Cleaning. They mathematically impute 
# missing values using the Median to resist outlier skew, explicitly drop corrupted 
# rows, and normalize the distributions. The resulting model is flawlessly accurate.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master Missing Data Handling (`dropna`, `fillna`, Imputation).
# - Execute Outlier Detection via Interquartile Range (IQR).
# - Architect Aggregations (`groupby`, `agg`) for EDA.
#
# ==============================================================================
"""

import pandas as pd
import numpy as np

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE BUSINESS LOGIC (THE CORRUPT DATASET)
# ==============================================================================
class EDASimulator:
    
    def __init__(self):
        self.df = None
        self._generate_corrupt_data()
        
    def _generate_corrupt_data(self):
        """Generates a mathematically 'dirty' dataset full of NaNs and Outliers."""
        print("  [INIT] Generating dirty dataset (NaNs and Outliers)...")
        data = {
            'employee_id': [101, 102, 103, 104, 105, 106, 107],
            'department': ['Engineering', 'Sales', 'Engineering', 'HR', np.nan, 'Sales', 'HR'],
            'salary': [85000, np.nan, 92000, 55000, 60000, 9999999, 58000], # Notice the outlier!
            'age': [28, 35, np.nan, 42, 25, 45, -5] # Negative age!
        }
        self.df = pd.DataFrame(data)
        
        print("\n  [RAW DATA]")
        print(self.df.to_string())


    # --------------------------------------------------------------------------
    # THE CLEANING ARCHITECTURE
    # --------------------------------------------------------------------------
    def clean_dataset(self):
        """
        Executes a rigorous, step-by-step mathematical cleaning pipeline.
        """
        print("\n  [PIPELINE] Executing Data Cleaning...")
        
        df_clean = self.df.copy()
        
        # 1. Handle Categorical NaNs
        # We fill missing departments with 'Unknown'
        df_clean['department'] = df_clean['department'].fillna('Unknown')
        
        # 2. Handle Numerical NaNs (Imputation)
        # We use the MEDIAN because it is mathematically resistant to outliers!
        # If we used the MEAN, the 9,999,999 salary would destroy the average.
        median_salary = df_clean['salary'].median()
        df_clean['salary'] = df_clean['salary'].fillna(median_salary)
        
        # 3. Handle Logical Errors
        # You cannot have a negative age. We mathematically absolute it, or nullify it.
        # Let's replace negative ages with NaN, then impute.
        df_clean.loc[df_clean['age'] < 0, 'age'] = np.nan
        df_clean['age'] = df_clean['age'].fillna(df_clean['age'].median())
        
        # 4. Outlier Detection (The IQR Method)
        # We calculate the 25th (Q1) and 75th (Q3) Percentiles.
        Q1 = df_clean['salary'].quantile(0.25)
        Q3 = df_clean['salary'].quantile(0.75)
        IQR = Q3 - Q1
        
        # Define the mathematical bounds
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        # Filter the DataFrame to ONLY keep safe rows!
        df_clean = df_clean[(df_clean['salary'] >= lower_bound) & (df_clean['salary'] <= upper_bound)]
        
        print("\n  [CLEAN DATA]")
        print(df_clean.to_string())
        
        return df_clean

    # --------------------------------------------------------------------------
    # THE EXPLORATORY DATA ANALYSIS (EDA)
    # --------------------------------------------------------------------------
    def perform_eda(self, df_clean: pd.DataFrame):
        """
        Executes aggregations to understand the underlying mathematics of the business.
        """
        print("\n  [EDA] Executing GroupBy Aggregations...")
        
        # We group by Department and calculate Multiple metrics simultaneously!
        summary = df_clean.groupby('department').agg(
            employee_count=('employee_id', 'count'),
            avg_salary=('salary', 'mean'),
            max_age=('age', 'max')
        ).reset_index() # Flattens the Multi-Index for easier reading
        
        print(summary.to_string())


# ==============================================================================
# 4. MATHEMATICAL PROOF (THE BENCHMARK)
# ==============================================================================
def demonstrate_cleaning():
    section_header("Data Analytics: Cleaning and EDA")
    
    sim = EDASimulator()
    clean_data = sim.clean_dataset()
    sim.perform_eda(clean_data)
    
    print("\n  [ARCHITECTURE PROOF]")
    print("  By utilizing mathematical Imputation (Medians) and Statistical Outlier ")
    print("  Detection (IQR bounds), the Data Engineer successfully sterilized the ")
    print("  dataset. The final EDA groupings reflect actual business reality rather ")
    print("  than being corrupted by a $9,999,999 typo.")


def run_all_labs():
    demonstrate_cleaning()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "When imputing missing numerical values, why might a Senior Data Scientist choose the Median over the Mean?"
   Senior Answer: "Mathematical Resistance to Skew. The Mean (average) takes all values, sums them, and divides by $N$. If you have $99$ employees making $\$50,000$ and $1$ CEO making $\$50,000,000$, the Mean salary mathematically skyrockets to $\$549,500$. If you impute missing data with this Mean, you corrupt the dataset. The Median physically sorts the values and picks the exact middle number, which remains completely unaffected by the extreme CEO outlier. Therefore, the Median provides a statistically safer imputation baseline for highly skewed distributions."

2. Interviewer: "Explain the mathematics behind Outlier Detection using the Interquartile Range (IQR)."
   Senior Answer: "Statistical Bounds. The dataset is mathematically divided into four quartiles. Q1 is the $25th$ percentile, Q3 is the $75th$ percentile. The Interquartile Range (IQR) is the exact distance between Q1 and Q3 ($IQR = Q3 - Q1$), representing the middle $50\\%$ of the data. To identify extreme anomalies, we establish mathematical fences: `Lower Bound = Q1 - (1.5 * IQR)` and `Upper Bound = Q3 + (1.5 * IQR)`. Any data point physically residing outside these fences is statistically classified as an Outlier and removed to prevent model corruption."

3. Interviewer: "What is the difference between `dropna()` and Imputation, and what is the risk of using `dropna()` on a massive dataset?"
   Senior Answer: "Data Annihilation vs Data Synthesis. `dropna()` completely deletes the entire row if even a single column contains a NaN value. If you have a dataset with $1,000,000$ rows and $100$ columns, and each column has a random $1\\%$ chance of being missing, executing `dropna()` might mathematically wipe out $60\\%$ of your entire dataset, destroying valuable business intelligence. Imputation synthesizes the missing value using algorithms (Mean, Median, Forward-Fill, or KNN ML models), allowing the architect to retain the row and preserve the data in the other $99$ columns."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Data Analytics (Cleaning & EDA) Completed.")
