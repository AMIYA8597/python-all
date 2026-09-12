"""
## A. Concept Name
Data Visualization with Matplotlib and Seaborn

## B. Concept Explanation
Data visualization is the graphical representation of information and data. By using visual elements like charts, graphs, and maps, data visualization tools provide an accessible way to see and understand trends, outliers, and patterns in data.

## C. Syntax & Structures
- `plt.plot()`: Line plot in Matplotlib.
- `plt.bar()`: Bar plot in Matplotlib.
- `sns.histplot()`: Histogram in Seaborn.
- `sns.boxplot()`: Box plot in Seaborn.
- `sns.heatmap()`: Correlation heatmap in Seaborn.

## D. Best Practices
- Always label your axes and provide a clear title.
- Choose the right type of plot for your data (e.g., line plot for time series).
- Use legends when multiple data series are present.
- Save high-quality plots for reporting using `plt.savefig()`.

## E. Common Pitfalls
- Overcrowding a single plot with too much information.
- Using misleading scales or not starting the y-axis at zero for bar charts.
- Forgetting to call `plt.close()` after saving, which can lead to memory leaks.
- Using poorly chosen color palettes that are hard to distinguish.

## F. Advanced Topics
- Customizing themes with `sns.set_theme()`.
- Complex layouts using `plt.subplots()` or `GridSpec`.
- Interactive visualizations with libraries like Plotly or Bokeh.

## X. Project Connection
Data visualization is the cornerstone of exploratory data analysis (EDA). In real-world projects, you will use these tools to understand your data distribution, identify correlations, detect outliers, and ultimately present your findings effectively to stakeholders.
"""
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import os

def generate_sample_data():
    np.random.seed(42)
    dates = pd.date_range(start='2023-01-01', periods=100)
    data = pd.DataFrame({
        'Date': dates,
        'Sales': np.random.normal(1000, 200, 100).cumsum(),
        'Expenses': np.random.normal(800, 150, 100).cumsum(),
        'Category': np.random.choice(['A', 'B', 'C'], 100),
        'Age': np.random.normal(35, 10, 100),
        'Score': np.random.normal(75, 15, 100)
    })
    return data

def run_visualization_tutorial():
    df = generate_sample_data()
    print("Sample data generated.")
    
    # Optional: ensure an output directory exists to save plots if running non-interactively
    out_dir = "plots"
    os.makedirs(out_dir, exist_ok=True)
    
    print("\n--- 1. Matplotlib Basics ---")
    
    # 1a. Line Plot
    plt.figure(figsize=(10, 5))
    plt.plot(df['Date'], df['Sales'], label='Sales', color='blue', linewidth=2)
    plt.plot(df['Date'], df['Expenses'], label='Expenses', color='red', linestyle='--')
    plt.title('Sales and Expenses Over Time', fontsize=16)
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Amount ($)', fontsize=12)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f"{out_dir}/1_line_plot.png")
    print(f"Saved line plot to {out_dir}/1_line_plot.png")
    plt.close()

    # 1b. Bar Plot
    category_sales = df.groupby('Category')['Sales'].mean().reset_index()
    plt.figure(figsize=(8, 5))
    plt.bar(category_sales['Category'], category_sales['Sales'], color=['skyblue', 'lightgreen', 'salmon'])
    plt.title('Average Sales by Category')
    plt.xlabel('Category')
    plt.ylabel('Average Sales')
    plt.savefig(f"{out_dir}/2_bar_plot.png")
    print(f"Saved bar plot to {out_dir}/2_bar_plot.png")
    plt.close()

    print("\n--- 2. Seaborn Basics ---")
    # Set seaborn style
    sns.set_theme(style="whitegrid")

    # 2a. Distribution Plot (Histogram + KDE)
    plt.figure(figsize=(8, 5))
    sns.histplot(df['Age'], kde=True, color='purple', bins=15)
    plt.title('Age Distribution')
    plt.savefig(f"{out_dir}/3_dist_plot.png")
    print(f"Saved distribution plot to {out_dir}/3_dist_plot.png")
    plt.close()

    # 2b. Box Plot (Categorical vs Numeric)
    plt.figure(figsize=(8, 5))
    sns.boxplot(x='Category', y='Score', data=df, palette='Set2')
    plt.title('Score Distribution by Category')
    plt.savefig(f"{out_dir}/4_box_plot.png")
    print(f"Saved box plot to {out_dir}/4_box_plot.png")
    plt.close()

    # 2c. Scatter Plot with Regression Line
    plt.figure(figsize=(8, 5))
    sns.regplot(x='Age', y='Score', data=df, scatter_kws={'alpha':0.5}, line_kws={'color':'red'})
    plt.title('Age vs Score')
    plt.savefig(f"{out_dir}/5_scatter_plot.png")
    print(f"Saved scatter plot to {out_dir}/5_scatter_plot.png")
    plt.close()

    print("\n--- 3. Advanced: Correlation Heatmap ---")
    plt.figure(figsize=(8, 6))
    # Select only numeric columns for correlation
    numeric_df = df.select_dtypes(include=[np.number])
    corr = numeric_df.corr()
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
    plt.title('Correlation Heatmap')
    plt.savefig(f"{out_dir}/6_heatmap.png")
    print(f"Saved heatmap to {out_dir}/6_heatmap.png")
    plt.close()
    
    print("\nVisualization scripts executed successfully! Plots saved in 'plots' directory.")

if __name__ == "__main__":
    run_visualization_tutorial()
