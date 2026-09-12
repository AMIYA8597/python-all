"""
Module: 05-advanced-viz
Description: Comprehensive textbook-grade lesson on Advanced Visualization in Python.

===========================================================================
Advanced Data Visualization in Python
===========================================================================

Learning Objectives:
1. Master advanced matplotlib features like GridSpec and custom projections.
2. Implement complex statistical visualizations using Seaborn's FacetGrid and PairGrid.
3. Understand interactive and 3D visualizations using Plotly and Matplotlib 3D toolkit.
4. Learn to optimize rendering performance for large datasets (Big-O analysis of rendering).
5. Apply architectural patterns for building reusable visualization pipelines.

Mathematical Background:
Visualizations map data values to visual encodings (position, size, color, shape). 
For instance, Kernel Density Estimation (KDE), often used in Seaborn, estimates the 
Probability Density Function (PDF) of a random variable.
KDE formula:
    f_h(x) = (1 / nh) * sum(K((x - x_i) / h))
Where:
- K is the kernel (e.g., Gaussian)
- h is the bandwidth (smoothing parameter)
- n is the number of data points

Big-O Analysis (Visualization Performance):
- Matplotlib Scatter Plot: O(N) where N is the number of points. However, rendering overhead 
  becomes significant > 10^5 points due to object creation (artists).
- Plotly WebGL (Scattergl): O(N) but handled via GPU pipeline, capable of 10^6 points at 60fps.
- Density approximations (e.g., hexbin, Datashader): O(N) binning step + O(B) rendering step, 
  where B is the number of bins. Highly efficient for massive datasets.

Modern Type Hints:
We will utilize precise type hints to ensure our data visualization functions are robust and 
safe for integration into larger Data Science pipelines.
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
    import matplotlib.gridspec as gridspec
    import seaborn as sns
    from mpl_toolkits.mplot3d import Axes3D
except ImportError as e:
    print(f"Warning: Missing required libraries for advanced visualization: {e}")
    print("Please install them using: pip install numpy pandas matplotlib seaborn")

# =========================================================================
# 1. Advanced Matplotlib: GridSpec and Custom Layouts
# =========================================================================

def build_dashboard_layout(data_size: int = 100) -> None:
    """
    Demonstrates advanced Matplotlib layouts using GridSpec.
    This creates a dashboard-like arrangement of plots.
    
    Args:
        data_size (int): Number of data points to generate.
    """
    print("--- 1. Advanced Matplotlib: GridSpec ---")
    if 'plt' not in globals():
        print("Matplotlib not available. Skipping.")
        return

    # Generate synthetic data
    x = np.linspace(0, 10, data_size)
    y1 = np.sin(x)
    y2 = np.cos(x)
    y3 = y1 * y2
    
    # Initialize the figure
    fig = plt.figure(figsize=(12, 8), constrained_layout=True)
    
    # Create a GridSpec: 3 rows, 3 columns
    gs = gridspec.GridSpec(3, 3, figure=fig)
    
    # Ax 1: Spans row 0, cols 0 to 2 (top wide plot)
    ax1 = fig.add_subplot(gs[0, :])
    ax1.plot(x, y1, 'r-', linewidth=2, label='sin(x)')
    ax1.set_title("Time Series (sin(x))")
    ax1.legend()

    # Ax 2: Spans row 1 and 2, col 0 (tall left plot)
    ax2 = fig.add_subplot(gs[1:, 0])
    ax2.scatter(y1, y2, c='b', alpha=0.5)
    ax2.set_title("Phase Plot (sin vs cos)")
    
    # Ax 3: Row 1, col 1 and 2 (middle wide)
    ax3 = fig.add_subplot(gs[1, 1:])
    ax3.fill_between(x, y3, color='g', alpha=0.3)
    ax3.set_title("Area Plot (sin * cos)")
    
    # Ax 4: Row 2, col 1 (bottom middle)
    ax4 = fig.add_subplot(gs[2, 1])
    ax4.hist(np.random.randn(1000), bins=20, color='purple', alpha=0.7)
    ax4.set_title("Distribution")
    
    # Ax 5: Row 2, col 2 (bottom right)
    ax5 = fig.add_subplot(gs[2, 2])
    sns.kdeplot(np.random.randn(1000), ax=ax5, fill=True, color='orange')
    ax5.set_title("KDE Estimate")

    plt.suptitle("Complex Dashboard using GridSpec", fontsize=16)
    # Note: Using plt.show(block=False) or plt.close() in automated environments
    plt.close(fig) 
    print("Dashboard layout successfully constructed and closed.\n")


# =========================================================================
# 2. Seaborn: High-level Statistical Visualizations
# =========================================================================

def statistical_faceting() -> None:
    """
    Utilizes Seaborn's FacetGrid to create conditional, multi-plot visualizations.
    Demonstrates plotting the distribution of variables conditioned on categories.
    """
    print("--- 2. Seaborn: FacetGrid ---")
    if 'sns' not in globals() or 'pd' not in globals():
        print("Seaborn/Pandas not available. Skipping.")
        return

    # Create synthetic categorical data
    np.random.seed(42)
    n = 300
    df = pd.DataFrame({
        'value': np.concatenate([np.random.normal(0, 1, n), 
                                 np.random.normal(2, 1.5, n),
                                 np.random.normal(-2, 0.5, n)]),
        'category': ['A'] * n + ['B'] * n + ['C'] * n,
        'group': np.random.choice(['Control', 'Treatment'], size=3*n)
    })

    # FacetGrid allows mapping a plot type to subsets of data
    # col="category", row="group" creates a matrix of plots
    g = sns.FacetGrid(df, col="category", row="group", hue="group", height=3, aspect=1.2)
    g.map(sns.kdeplot, "value", fill=True)
    g.add_legend()
    g.fig.subplots_adjust(top=0.9)
    g.fig.suptitle("FacetGrid: Distributions by Category and Group")
    
    plt.close(g.fig)
    print("FacetGrid layout successfully constructed and closed.\n")


# =========================================================================
# 3. 3D and Interactive Plotting concepts
# =========================================================================

def three_dimensional_surface() -> None:
    """
    Demonstrates rendering a 3D surface plot using mpl_toolkits.mplot3d.
    Mathematical surface: z = sin(sqrt(x^2 + y^2))
    """
    print("--- 3. Matplotlib 3D: Surface Plot ---")
    if 'plt' not in globals():
        return
        
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')
    
    # Generate data
    x = np.linspace(-5, 5, 100)
    y = np.linspace(-5, 5, 100)
    X, Y = np.meshgrid(x, y)
    R = np.sqrt(X**2 + Y**2)
    Z = np.sin(R)
    
    # Plot surface
    surf = ax.plot_surface(X, Y, Z, cmap='viridis', edgecolor='none', alpha=0.8)
    fig.colorbar(surf, shrink=0.5, aspect=10)
    
    ax.set_title("3D Surface Plot: $z = \sin(\sqrt{x^2 + y^2})$")
    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')
    ax.set_zlabel('Z axis')
    
    plt.close(fig)
    print("3D surface plot constructed and closed.\n")


# =========================================================================
# 4. Performance Optimization and Edge Cases
# =========================================================================

def analyze_performance_and_edge_cases() -> None:
    """
    Analyzes performance bottlenecks and discusses edge cases in visualization.
    """
    print("--- 4. Performance Analysis & Edge Cases ---")
    print("1. Performance (O(N) rendering): Plotting 1M points in standard matplotlib will lag.")
    print("   Solution: Downsample data, use Hexbin plots, or specialized libraries like Datashader.")
    print("2. Memory Leak Edge Case: Repeatedly calling plt.plot() without plt.close() in a loop ")
    print("   will consume RAM rapidly. Always manage Figure lifecycles.")
    print("3. Data Quality: NaNs or Infs will break some Seaborn clustering/KDE algorithms.")
    print("   Solution: Sanitize and impute data beforehand.\n")


# =========================================================================
# 5. Real World Application / Interview Challenge
# =========================================================================

def interview_challenge_anomaly_visualization(data: List[float], threshold: float) -> Tuple[List[float], List[float]]:
    """
    Common interview challenge (Data Science focused): 
    Given a time series, identify and separate the anomalies (values > threshold),
    so they can be plotted in a different color.
    
    Args:
        data: List of float values representing time series.
        threshold: The threshold above which a point is considered anomalous.
        
    Returns:
        Tuple containing two lists: 
        - Normal values (or None where anomaly occurred)
        - Anomaly values (or None where normal)
    """
    print("--- 5. Interview Challenge: Anomaly Extraction for Plotting ---")
    normal_points: List[float] = []
    anomaly_points: List[float] = []
    
    for val in data:
        if val > threshold:
            normal_points.append(float('nan'))
            anomaly_points.append(val)
        else:
            normal_points.append(val)
            anomaly_points.append(float('nan'))
            
    print(f"Total points: {len(data)}")
    print(f"Anomalies detected: {sum(1 for x in anomaly_points if not math.isnan(x))}\n")
    return normal_points, anomaly_points


# =========================================================================
# 6. Comprehensive Test Suite
# =========================================================================

def run_tests() -> None:
    """
    Validates logic in the module without displaying plots.
    """
    print("--- 6. Running Tests ---")
    try:
        # Test Anomaly Extraction
        ts_data = [1.2, 1.5, 5.5, 1.1, 1.3, 6.0, 1.4]
        thresh = 3.0
        norm, anom = interview_challenge_anomaly_visualization(ts_data, thresh)
        
        assert len(norm) == len(ts_data), "Normal list length mismatch"
        assert len(anom) == len(ts_data), "Anomaly list length mismatch"
        assert math.isnan(norm[2]) and anom[2] == 5.5, "Anomaly extraction failed at index 2"
        assert norm[0] == 1.2 and math.isnan(anom[0]), "Normal extraction failed at index 0"
        
        print("All logical tests passed successfully!\n")
    except AssertionError as e:
        print(f"Test Failed: {e}\n")


if __name__ == "__main__":
    print(f"========== Exploring {'05-advanced-viz'.upper()} ==========\n")
    
    # 1. Advanced GridSpec Layouts
    build_dashboard_layout(100)
    
    # 2. Seaborn Faceting
    statistical_faceting()
    
    # 3. 3D Plotting
    three_dimensional_surface()
    
    # 4. Performance & Edge Cases
    analyze_performance_and_edge_cases()
    
    # 5. Interview Challenge Execution
    ts_example = [1.0, 1.2, 1.1, 4.5, 1.3, 1.0, 5.8, 1.1]
    n_pts, a_pts = interview_challenge_anomaly_visualization(ts_example, threshold=2.0)
    
    # 6. Run unit tests
    run_tests()
    
    print(f"========== END OF {'05-advanced-viz'.upper()} ==========\n")
