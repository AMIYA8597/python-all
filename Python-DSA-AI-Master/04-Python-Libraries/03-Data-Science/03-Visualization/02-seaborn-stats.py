"""
Module: 02-seaborn-stats
Description: Comprehensive textbook-grade educational script on Statistical Visualization using Seaborn.

=========================================================================================
SEABORN STATISTICAL VISUALIZATION: A TEXTBOOK-GRADE INTERACTIVE LESSON
=========================================================================================

Learning Objectives:
1. Understand the core statistical plotting capabilities of the Seaborn library.
2. Master the usage of regression plots, distribution plots, categorical plots, and matrix plots.
3. Understand the mathematical background behind Kernel Density Estimation (KDE) and Linear Regression.
4. Analyze the computational complexity (Big-O) of generating statistical visualizations.
5. Apply seaborn techniques to real-world datasets and scenarios.
6. Solve interview-style data visualization and analysis challenges.

-----------------------------------------------------------------------------------------
1. Mathematical Background
-----------------------------------------------------------------------------------------
Seaborn abstracts many complex statistical operations. Two prominent ones are:

A. Kernel Density Estimation (KDE):
   KDE is a non-parametric way to estimate the probability density function (PDF) of a random variable.
   Formula:
     f_hat(x) = (1 / (n * h)) * SUM( K((x - x_i) / h) ) for i = 1 to n
   Where:
     - n: Number of data points
     - h: Bandwidth (smoothing parameter)
     - x_i: The i-th observation
     - K: The kernel function (typically Gaussian, i.e., Normal distribution)

B. Ordinary Least Squares (OLS) Linear Regression:
   Used in `lmplot` and `regplot` to fit a line that minimizes the sum of squared residuals.
   Formula:
     y_hat = beta_0 + beta_1 * x
   Where:
     - beta_1 = Cov(X, Y) / Var(X)
     - beta_0 = mean(Y) - beta_1 * mean(X)

-----------------------------------------------------------------------------------------
2. Complexity Analysis (Big-O)
-----------------------------------------------------------------------------------------
- KDE Plotting:
  - Time Complexity: O(n * m), where n is the number of data points and m is the number of
    points on the evaluation grid (typically 100 or 200).
  - Space Complexity: O(n) to store the data, plus O(m) for the grid.
- Linear Regression (OLS):
  - Time Complexity: O(n) for univariate OLS (calculating covariance and variance).
  - Space Complexity: O(1) auxiliary space beyond the input data arrays O(n).
- Pair Plot (Scatterplot Matrix):
  - Time Complexity: O(k^2 * n), where k is the number of features (variables) and n is the
    number of data points.
  - Space Complexity: O(k^2 * n) for rendering the subplots.

-----------------------------------------------------------------------------------------
3. Modern Type Hints & Architecture
-----------------------------------------------------------------------------------------
This module uses standard Python typing along with pandas and matplotlib stubs (if available).
The examples are structured as isolated functions to facilitate interactive learning and testing.

"""

import sys
import time
import math
import random
from typing import List, Dict, Any, Optional, Tuple, Union

try:
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns
except ImportError as e:
    print(f"Error: Missing required library. {e}")
    print("Please install numpy, pandas, matplotlib, and seaborn.")
    sys.exit(1)

# Set Seaborn theme for better aesthetics
sns.set_theme(style="whitegrid", palette="muted")


# =========================================================================================
# SECTION 1: DATA GENERATION & PREPARATION
# =========================================================================================

def generate_synthetic_data(n_samples: int = 500) -> pd.DataFrame:
    """
    Generates a synthetic dataset for demonstrating statistical plots.
    
    The dataset includes:
    - 'Age': Normally distributed data.
    - 'Income': Skewed distribution (log-normal) representing realistic income.
    - 'Experience': Correlated with Age and Income.
    - 'Department': Categorical data.
    - 'Satisfaction': Bimodal distribution representing job satisfaction scores.

    Args:
        n_samples (int): Number of samples to generate.

    Returns:
        pd.DataFrame: A pandas DataFrame containing the synthetic dataset.
    """
    print(f"--- Generating Synthetic Dataset ({n_samples} samples) ---")
    np.random.seed(42)
    
    # 1. Age (Normal Distribution)
    age = np.random.normal(loc=35, scale=10, size=n_samples)
    age = np.clip(age, 18, 70).astype(int)
    
    # 2. Experience (Correlated with Age)
    # Experience should generally be less than Age - 18
    experience = np.maximum(0, age - 18 - np.random.normal(loc=2, scale=3, size=n_samples))
    experience = np.round(experience, 1)
    
    # 3. Income (Log-Normal, correlated with Experience)
    base_income = np.random.lognormal(mean=10.5, sigma=0.5, size=n_samples)
    income = base_income + (experience * 2500) + np.random.normal(loc=0, scale=5000, size=n_samples)
    income = np.clip(income, 20000, 300000)
    
    # 4. Department (Categorical)
    departments = ['Engineering', 'Sales', 'Marketing', 'HR', 'Finance']
    department = np.random.choice(departments, size=n_samples, p=[0.4, 0.2, 0.15, 0.1, 0.15])
    
    # 5. Satisfaction (Bimodal - e.g., extremely happy or extremely unhappy folks)
    satisfaction1 = np.random.normal(loc=3, scale=1, size=n_samples // 2)
    satisfaction2 = np.random.normal(loc=8, scale=1.5, size=n_samples - (n_samples // 2))
    satisfaction = np.concatenate([satisfaction1, satisfaction2])
    np.random.shuffle(satisfaction)
    satisfaction = np.clip(satisfaction, 1, 10)
    
    df = pd.DataFrame({
        'Age': age,
        'Experience': experience,
        'Income': income,
        'Department': department,
        'Satisfaction': satisfaction
    })
    
    print("Dataset generated successfully.")
    print(f"Dataset shape: {df.shape}")
    print("Sample Data:")
    print(df.head(), "\n")
    return df


# =========================================================================================
# SECTION 2: DISTRIBUTION ANALYSIS (UNIVARIATE)
# =========================================================================================

def demonstrate_distribution_plots(df: pd.DataFrame, save_plots: bool = False) -> None:
    """
    Demonstrates how to analyze univariate distributions using histplot and kdeplot.
    
    Math Concept (KDE):
    Kernel Density Estimation smoothes out histograms to provide a continuous curve
    representing the probability density.
    
    Args:
        df (pd.DataFrame): The dataset to analyze.
        save_plots (bool): Whether to save the generated plots to disk.
    """
    print("--- 2. Distribution Analysis ---")
    
    # Create a figure with subplots
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    
    # 2.1 Histogram with KDE overlay
    # Big-O: O(n) for histogram binning, O(n*m) for KDE.
    sns.histplot(data=df, x='Income', kde=True, ax=axes[0], color='blue', bins=30)
    axes[0].set_title('Income Distribution (Hist + KDE)')
    axes[0].set_xlabel('Income ($)')
    axes[0].set_ylabel('Count')
    
    # 2.2 KDE Plot (Bimodal Distribution)
    # Useful for spotting multiple peaks
    sns.kdeplot(data=df, x='Satisfaction', ax=axes[1], color='purple', fill=True, bw_adjust=0.5)
    axes[1].set_title('Satisfaction Density (Bimodal)')
    axes[1].set_xlabel('Satisfaction Score')
    axes[1].set_ylabel('Density')
    
    # 2.3 Multiple KDE plots based on categories
    sns.kdeplot(data=df, x='Age', hue='Department', ax=axes[2], fill=True, alpha=0.3, common_norm=False)
    axes[2].set_title('Age Distribution by Department')
    axes[2].set_xlabel('Age (Years)')
    
    plt.tight_layout()
    if save_plots:
        plt.savefig("distribution_plots.png")
        print("Saved: distribution_plots.png")
    
    plt.show(block=False)
    plt.pause(2)
    plt.close()
    print("Completed distribution analysis.\n")


# =========================================================================================
# SECTION 3: CATEGORICAL STATISTICAL PLOTS
# =========================================================================================

def demonstrate_categorical_plots(df: pd.DataFrame, save_plots: bool = False) -> None:
    """
    Demonstrates statistical summaries of categorical variables.
    
    Focus:
    - Boxplot: Shows the quartiles and outliers (IQR method).
    - Violinplot: Combines boxplot and KDE.
    
    Args:
        df (pd.DataFrame): The dataset.
        save_plots (bool): Save flag.
    """
    print("--- 3. Categorical Statistical Analysis ---")
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # 3.1 Boxplot
    # Shows the median (line), 25th-75th percentile (box), and outliers (whiskers/points)
    sns.boxplot(data=df, x='Department', y='Income', ax=axes[0], palette='Set2')
    axes[0].set_title('Income Distribution by Department (Boxplot)')
    axes[0].tick_params(axis='x', rotation=45)
    
    # 3.2 Violinplot
    # Shows the density of the distribution along with quartile bounds.
    # We use scale='width' so all violins have the same width regardless of sample size.
    sns.violinplot(data=df, x='Department', y='Age', ax=axes[1], palette='Pastel1', split=False, inner='quartile')
    axes[1].set_title('Age Density by Department (Violinplot)')
    axes[1].tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    if save_plots:
        plt.savefig("categorical_plots.png")
    
    plt.show(block=False)
    plt.pause(2)
    plt.close()
    print("Completed categorical analysis.\n")


# =========================================================================================
# SECTION 4: REGRESSION & MULTIVARIATE ANALYSIS
# =========================================================================================

def demonstrate_regression_and_relationships(df: pd.DataFrame, save_plots: bool = False) -> None:
    """
    Demonstrates regression lines and multivariate pair-wise relationships.
    
    Mathematical focus: Ordinary Least Squares (OLS) regression line and confidence intervals.
    Seaborn's `lmplot` and `regplot` automatically fit a linear regression model and plot a 95% 
    confidence interval around the estimate using bootstrapping.
    
    Args:
        df (pd.DataFrame): The dataset.
        save_plots (bool): Save flag.
    """
    print("--- 4. Regression & Relational Analysis ---")
    
    # 4.1 Regression plot (regplot) within a figure
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.regplot(data=df, x='Experience', y='Income', ax=ax, scatter_kws={'alpha':0.5}, line_kws={'color':'red'})
    ax.set_title('Linear Regression: Income vs Experience')
    
    if save_plots:
        plt.savefig("regplot.png")
    plt.show(block=False)
    plt.pause(2)
    plt.close()
    
    # 4.2 Jointplot (Bivariate Analysis)
    # Shows the relationship and marginal distributions.
    # Note: jointplot creates its own figure.
    g = sns.jointplot(data=df, x='Age', y='Experience', kind='hex', color='g', marginal_kws=dict(bins=20, fill=True))
    g.fig.suptitle('Jointplot (Hexbin + Marginal Histograms)', y=1.02)
    
    if save_plots:
        g.savefig("jointplot.png")
    plt.show(block=False)
    plt.pause(2)
    plt.close()
    print("Completed regression and relationship analysis.\n")


# =========================================================================================
# SECTION 5: MATRIX PLOTS (HEATMAPS & CORRELATION)
# =========================================================================================

def demonstrate_matrix_plots(df: pd.DataFrame, save_plots: bool = False) -> None:
    """
    Demonstrates matrix plots like heatmaps to analyze variable correlations.
    
    Pearson Correlation Coefficient Formula:
    r = Cov(X, Y) / (Std(X) * Std(Y))
    
    Big-O:
    Computing correlation matrix: O(k^2 * n) where k is features, n is samples.
    Plotting heatmap: O(k^2).
    
    Args:
        df (pd.DataFrame): The dataset.
        save_plots (bool): Save flag.
    """
    print("--- 5. Matrix & Correlation Analysis ---")
    
    # Select only numeric columns for correlation
    numeric_df = df.select_dtypes(include=[np.number])
    corr_matrix = numeric_df.corr(method='pearson')
    
    fig, ax = plt.subplots(figsize=(8, 6))
    # Heatmap with annotations and coolwarm diverging palette
    sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap='coolwarm', vmin=-1, vmax=1, ax=ax, square=True)
    ax.set_title('Pearson Correlation Heatmap')
    
    plt.tight_layout()
    if save_plots:
        plt.savefig("heatmap.png")
    
    plt.show(block=False)
    plt.pause(2)
    plt.close()
    print("Completed matrix plot analysis.\n")


# =========================================================================================
# SECTION 6: PERFORMANCE & ADVANCED EDGE CASES
# =========================================================================================

def analyze_performance_and_edge_cases() -> None:
    """
    Analyzes performance bottlenecks and discusses edge cases in statistical plotting.
    """
    print("--- 6. Performance Analysis & Edge Cases ---")
    print("1. Performance (Large Datasets):")
    print("   - Using `sns.scatterplot()` or `sns.pairplot()` on >100,000 rows can freeze your machine.")
    print("   - Optimization: Use `sns.jointplot(..., kind='hex')` or downsample your dataset using `df.sample(n=10000)`.")
    print("2. KDE Performance:")
    print("   - High dimensionality KDE (e.g., in pairplots) is computationally expensive (O(n * m)).")
    print("   - Optimization: Disable KDE in pairplot by setting `diag_kind='hist'` for massive data.")
    print("3. Edge Case (Missing Values):")
    print("   - Seaborn usually drops NaNs implicitly, but it's best to explicitly handle them via `df.dropna()`.")
    print("   - Failing to handle NaNs may result in blank plots or misleading regression lines.")
    print("4. Edge Case (Zero Variance):")
    print("   - If a column has identical values (zero variance), KDE plotting will fail or produce an infinite spike.")
    print("   - Mitigation: Add slight jitter or check variance before plotting.\n")


# =========================================================================================
# SECTION 7: INTERVIEW CHALLENGE
# =========================================================================================

def interview_challenge(df: pd.DataFrame) -> Dict[str, float]:
    """
    Common Data Science Interview Challenge:
    Given a dataset, implement an algorithm that:
    1. Finds the feature most positively correlated with 'Income'.
    2. Finds the feature most negatively correlated with 'Income' (or least correlated).
    3. Exclude 'Income' itself.
    
    We'll do this programmatically without relying purely on a visualization, simulating 
    a quantitative screening before plotting.

    Args:
        df (pd.DataFrame): The input dataset.

    Returns:
        Dict[str, float]: The top and bottom correlated features and their scores.
    """
    print("--- 7. Interview Challenge ---")
    print("Task: Identify features with highest and lowest correlation to 'Income'.")
    
    numeric_df = df.select_dtypes(include=[np.number])
    if 'Income' not in numeric_df.columns:
        raise ValueError("'Income' column not found or not numeric.")
    
    # Get correlations with Income, drop Income itself
    correlations = numeric_df.corr()['Income'].drop('Income')
    
    # Identify max and min
    max_feat = correlations.idxmax()
    max_val = correlations.max()
    
    min_feat = correlations.idxmin()
    min_val = correlations.min()
    
    result = {
        "highest_correlation_feature": max_feat,
        "highest_correlation_value": float(max_val),
        "lowest_correlation_feature": min_feat,
        "lowest_correlation_value": float(min_val)
    }
    
    print(f"Results: {result}")
    print("Challenge completed.\n")
    return result


# =========================================================================================
# SECTION 8: TESTS
# =========================================================================================

def run_tests() -> None:
    """
    Simple unit test suite to validate the purely algorithmic components.
    """
    print("--- 8. Running Tests ---")
    
    # Test Data Generation
    try:
        test_df = generate_synthetic_data(n_samples=50)
        assert len(test_df) == 50, "Data generation size mismatch."
        assert 'Income' in test_df.columns, "Missing column 'Income'."
        assert not test_df.isnull().any().any(), "Dataset contains NaNs."
        
        # Test Interview Challenge
        res = interview_challenge(test_df)
        assert 'highest_correlation_feature' in res, "Missing key in result."
        assert isinstance(res['highest_correlation_value'], float), "Incorrect type for correlation value."
        
        print("All assertions passed successfully!\n")
    except AssertionError as e:
        print(f"Test Failed: {e}\n")


# =========================================================================================
# MAIN EXECUTION BLOCK
# =========================================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("EXPLORING SEABORN STATISTICAL PLOTTING (02-SEABORN-STATS)")
    print("=" * 80, "\n")
    
    # Note: In a real non-interactive environment, plots might block execution. 
    # We use plt.pause and plt.close to automate the flow for this textbook script.
    
    # 1. Prepare Data
    df_main = generate_synthetic_data(n_samples=1000)
    
    # 2. Distributions
    demonstrate_distribution_plots(df_main)
    
    # 3. Categorical
    demonstrate_categorical_plots(df_main)
    
    # 4. Regression
    demonstrate_regression_and_relationships(df_main)
    
    # 5. Matrix
    demonstrate_matrix_plots(df_main)
    
    # 6. Performance & Theory
    analyze_performance_and_edge_cases()
    
    # 7. Interview Challenge
    interview_challenge(df_main)
    
    # 8. Tests
    run_tests()
    
    print("=" * 80)
    print("END OF SEABORN STATISTICAL PLOTTING LESSON")
    print("=" * 80)
