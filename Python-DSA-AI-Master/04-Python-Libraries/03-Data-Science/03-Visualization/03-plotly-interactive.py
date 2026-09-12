"""
Module: 03-plotly-interactive
Description: Comprehensive textbook-grade interactive lesson for Plotly.

Learning Objectives:
1. Understand the core concepts of Plotly, a graphing library that makes interactive, publication-quality graphs.
2. Master the creation of basic charts: Scatter, Line, Bar, Pie.
3. Master advanced charts: 3D surfaces, Heatmaps, Animations, and Subplots.
4. Implement interactivity explicitly using custom controls (Dropdowns, Sliders, Buttons).
5. Analyze mathematical backgrounds, Big-O complexities of data transformations and rendering.
6. Real-world applications: Financial Dashboards and Scientific Visualizations.

Mathematical Background:
Plotly utilizes the concept of declarative programming for visualizations, where the user specifies *what* 
to render (traces and layout) instead of *how* to render it. The underlying engine (Plotly.js) translates
these JSON specifications into D3.js and WebGL rendering operations.

For 3D plotting, we often visualize scalar fields $f: \mathbb{R}^2 \to \mathbb{R}$, generating a meshgrid.
For instance, the "Sombrero" or "Sinc" surface function:
    $z = \frac{\sin(R)}{R}$ where $R = \sqrt{x^2 + y^2}$
This requires computing the distance $R$ for an $N \times N$ grid, which takes $O(N^2)$ time.

Big-O Analysis:
- Time Complexity (Data Preparation): Typically $O(N)$ for 1D arrays or $O(N \cdot M)$ for 2D grids, where 
  $N$ is the number of data points. Sorting data for line plots is $O(N \log N)$.
- Space Complexity (Data Transmission): Plotly figures are serialized to JSON. The space complexity is 
  $O(V + E)$ or $O(N)$, where $N$ is the total number of vertices/points in the dataset. Massive datasets 
  ($>100,000$ points) can cause browser lag and high memory consumption (JSON overhead). Thus, one must 
  aggregate or use `Scattergl` (WebGL) to achieve $O(1)$ perceived rendering time for large sets.

Modern Type Hints & Best Practices:
- Utilizes `typing` module for static type checking.
- Focuses on comprehensive inline documentation.
- Test cases ensure the functions return valid `go.Figure` objects.

Prerequisites:
- pip install plotly numpy pandas
"""

import sys
import time
import math
import random
from typing import List, Dict, Any, Optional, Tuple

try:
    import numpy as np
    import pandas as pd
    import plotly.graph_objects as go
    import plotly.express as px
    from plotly.subplots import make_subplots
except ImportError as e:
    print(f"Error importing required libraries: {e}")
    print("Please install them using: pip install plotly numpy pandas")
    sys.exit(1)


def generate_basic_visualizations() -> Dict[str, go.Figure]:
    """
    Demonstrates basic implementations of Plotly graphs using Plotly Express and Graph Objects.
    
    Returns:
        Dict[str, go.Figure]: A dictionary mapping graph names to Plotly Figure objects.
    """
    print("--- 1. Basic Visualizations ---")
    figures: Dict[str, go.Figure] = {}
    
    # 1. Scatter Plot (O(N) rendering)
    # Using random walk for data
    np.random.seed(42)
    N = 100
    random_x = np.linspace(0, 1, N)
    random_y0 = np.random.randn(N) + 5
    random_y1 = np.random.randn(N)
    random_y2 = np.random.randn(N) - 5

    # Create figure using graph_objects
    fig_scatter = go.Figure()
    
    # Add traces (individual plots within the same figure)
    fig_scatter.add_trace(go.Scatter(x=random_x, y=random_y0, mode='markers', name='markers'))
    fig_scatter.add_trace(go.Scatter(x=random_x, y=random_y1, mode='lines+markers', name='lines+markers'))
    fig_scatter.add_trace(go.Scatter(x=random_x, y=random_y2, mode='lines', name='lines'))
    
    fig_scatter.update_layout(title="Random Walk Scatter & Line Plot",
                              xaxis_title="Time (s)",
                              yaxis_title="Amplitude",
                              template="plotly_dark")
    figures['scatter'] = fig_scatter
    
    # 2. Bar Chart
    categories = ['Apples', 'Oranges', 'Bananas', 'Berries']
    sales_2023 = [400, 300, 500, 600]
    sales_2024 = [450, 250, 550, 700]
    
    fig_bar = go.Figure(data=[
        go.Bar(name='2023', x=categories, y=sales_2023),
        go.Bar(name='2024', x=categories, y=sales_2024)
    ])
    # Change the bar mode
    fig_bar.update_layout(barmode='group', title="Fruit Sales (Grouped Bar Chart)")
    figures['bar'] = fig_bar
    
    # 3. Pie Chart
    labels = ['Oxygen', 'Hydrogen', 'Carbon_Dioxide', 'Nitrogen']
    values = [4500, 2500, 1053, 500]
    
    fig_pie = go.Figure(data=[go.Pie(labels=labels, values=values, pull=[0.1, 0, 0, 0])])
    fig_pie.update_layout(title="Atmospheric Composition (Exploded Pie)")
    figures['pie'] = fig_pie
    
    print("Basic visualizations generated successfully.\n")
    return figures


def generate_interactive_controls() -> go.Figure:
    """
    Creates a plot with interactive UI controls: Dropdowns and Sliders.
    
    Plotly allows interactivity without setting up a backend server by embedding 
    JavaScript callbacks into the generated HTML.
    
    Returns:
        go.Figure: The figure containing interactive controls.
    """
    print("--- 2. Interactive Controls (Dropdowns & Sliders) ---")
    
    # Generate a sine wave data set
    x = np.linspace(0, 10, 1000)
    
    fig = go.Figure()
    
    # Add traces for different frequencies
    frequencies = [1, 2, 3, 4, 5]
    for step in frequencies:
        fig.add_trace(
            go.Scatter(
                visible=False,
                line=dict(color="#00CED1", width=3),
                name=f"v = {step}",
                x=x,
                y=np.sin(step * x)
            )
        )
        
    # Make the first trace visible
    fig.data[0].visible = True
    
    # Create and add slider
    steps = []
    for i in range(len(fig.data)):
        # Determine visibility array (only the i-th trace is True)
        visibility = [False] * len(fig.data)
        visibility[i] = True
        
        step = dict(
            method="update",
            args=[{"visible": visibility},
                  {"title": f"Sine Wave Slider: Frequency = {frequencies[i]}"}],
            label=str(frequencies[i])
        )
        steps.append(step)
        
    sliders = [dict(
        active=0,
        currentvalue={"prefix": "Frequency: "},
        pad={"t": 50},
        steps=steps
    )]
    
    # Add dropdown menu to change color theme
    updatemenus = [
        dict(
            buttons=list([
                dict(args=["line.color", "#00CED1"], label="Cyan", method="restyle"),
                dict(args=["line.color", "#FF6347"], label="Tomato", method="restyle"),
                dict(args=["line.color", "#32CD32"], label="Lime", method="restyle"),
            ]),
            direction="down",
            pad={"r": 10, "t": 10},
            showactive=True,
            x=0.1,
            xanchor="left",
            y=1.1,
            yanchor="top"
        ),
    ]

    fig.update_layout(
        sliders=sliders,
        updatemenus=updatemenus,
        title=f"Sine Wave Slider: Frequency = {frequencies[0]}",
        xaxis_title="x",
        yaxis_title="sin(f * x)"
    )
    
    print("Interactive controls visualization generated.\n")
    return fig


def generate_3d_mathematical_surface() -> go.Figure:
    """
    Advanced implementation showing 3D surface rendering.
    
    Mathematical function: Sinc function
        z = sin(R) / R, where R = sqrt(x^2 + y^2)
        
    Time Complexity for Grid Calculation: O(N^2) for an N x N meshgrid.
    Space Complexity: O(N^2) storing coordinates.
    
    Returns:
        go.Figure: The 3D surface plot figure.
    """
    print("--- 3. 3D Mathematical Surface ---")
    start_time = time.time()
    
    # Create O(N^2) grid
    N = 100 # Grid resolution
    x = np.linspace(-10, 10, N)
    y = np.linspace(-10, 10, N)
    x_grid, y_grid = np.meshgrid(x, y)
    
    # Compute R = sqrt(x^2 + y^2)
    # Using np.hypot which is equivalent to sqrt(x**2 + y**2)
    R = np.hypot(x_grid, y_grid)
    
    # To avoid division by zero at origin
    # np.sinc(x) is normalized as sin(pi*x)/(pi*x). We use explicit sin(r)/r for exact formulation.
    z_grid = np.sin(R) / (R + 1e-10) 
    
    fig = go.Figure(data=[go.Surface(z=z_grid, x=x_grid, y=y_grid, colorscale='Viridis')])
    
    fig.update_layout(title='3D Sinc Surface (Sombrero)',
                      scene=dict(
                          xaxis_title='X Axis',
                          yaxis_title='Y Axis',
                          zaxis_title='Z (Amplitude)'
                      ),
                      autosize=False,
                      width=800, height=800,
                      margin=dict(l=65, r=50, b=65, t=90))
                      
    end_time = time.time()
    print(f"3D Surface Matrix Calculation and Rendering init took: {end_time - start_time:.6f} seconds")
    print("3D surface visualization generated.\n")
    return fig


def generate_real_world_financial_dashboard() -> go.Figure:
    """
    Real-world application: Simulating a financial candlestick chart with 
    Moving Averages and Volume bars using Subplots.
    
    This demonstrates handling time-series data and creating compound dashboards.
    
    Returns:
        go.Figure: The composed dashboard figure.
    """
    print("--- 4. Real-world Financial Dashboard ---")
    
    # Simulate 100 days of stock data
    np.random.seed(101)
    dates = pd.date_range(start='2023-01-01', periods=100)
    
    # Random walk for price
    price = 100 + np.random.randn(100).cumsum()
    # High, Low, Open, Close
    open_p = price
    close_p = price + np.random.randn(100)
    high_p = np.maximum(open_p, close_p) + np.random.rand(100)*2
    low_p = np.minimum(open_p, close_p) - np.random.rand(100)*2
    volume = np.random.randint(1000, 50000, 100)
    
    df = pd.DataFrame({
        'Date': dates, 'Open': open_p, 'High': high_p, 
        'Low': low_p, 'Close': close_p, 'Volume': volume
    })
    
    # Calculate Simple Moving Average (SMA)
    df['SMA_20'] = df['Close'].rolling(window=20).mean()
    
    # Create subplots: Top plot (Candlestick), Bottom plot (Volume)
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                        vertical_spacing=0.03, subplot_titles=('Stock Price', 'Volume'),
                        row_width=[0.2, 0.7])
    
    # Candlestick Trace
    fig.add_trace(go.Candlestick(x=df['Date'],
                                 open=df['Open'], high=df['High'],
                                 low=df['Low'], close=df['Close'],
                                 name='OHLC'),
                  row=1, col=1)
                  
    # Moving Average Trace
    fig.add_trace(go.Scatter(x=df['Date'], y=df['SMA_20'], 
                             line=dict(color='orange', width=2),
                             name='SMA 20'),
                  row=1, col=1)
                  
    # Volume Trace (Bar)
    fig.add_trace(go.Bar(x=df['Date'], y=df['Volume'], showlegend=False,
                         marker_color='blue'),
                  row=2, col=1)
                  
    # Remove rangeslider (often too bulky)
    fig.update_layout(xaxis_rangeslider_visible=False,
                      title="AAPL Simulated Financial Dashboard",
                      template="plotly_dark",
                      height=800)
                      
    print("Financial dashboard generated.\n")
    return fig


def analyze_performance_and_edge_cases() -> None:
    """
    Analyzes performance bottlenecks and discusses edge cases in Plotly interactive graphs.
    """
    print("--- 5. Performance Analysis & Edge Cases ---")
    print("1. Performance (Large Datasets): Rendering >100k points with `go.Scatter` crashes browsers.")
    print("   Solution: Use `go.Scattergl` (WebGL) for massive 2D data or aggregate data beforehand.")
    print("2. JSON Serialization Overhead: Data mapped to Plotly graphs must be serialized to JSON.")
    print("   Avoid plotting deep recursion trees or raw gigabyte logs directly.")
    print("3. Edge Case: Missing Data (`np.nan` or `None`). Plotly naturally breaks line plots where")
    print("   `nan` exists. Use `connectgaps=True` inside traces to draw lines across missing data.")
    print("4. Edge Case: Handling datetime indices. Plotly infers timezone. Converting to UTC standardizes plots.\n")


def interview_challenge(data: List[float], window: int) -> List[float]:
    """
    Common interview challenge related to data preparation for visualizations:
    Calculate the Simple Moving Average (SMA) of a 1D array natively in O(N) time.
    
    Mathematical Formulation:
    SMA_t = (P_t + P_{t-1} + ... + P_{t-k+1}) / k
    
    Using a sliding window algorithm to ensure O(N) instead of O(N * K).
    
    Args:
        data: List of prices or values.
        window: Integer representing the window size K.
        
    Returns:
        List[float]: The moving average array of same length. The first (window-1) 
                     elements are usually None or nan, here we will pad with None.
    """
    print(f"--- 6. Interview Challenge (Sliding Window / SMA) ---")
    if not data or window <= 0:
        return []
    
    n = len(data)
    if window > n:
        return [None] * n # type: ignore
        
    result: List[Optional[float]] = [None] * n
    
    # Initial sum calculation for the first valid window
    window_sum = sum(data[:window])
    result[window - 1] = window_sum / window
    
    # Sliding the window in O(N)
    for i in range(window, n):
        window_sum += data[i] - data[i - window]
        result[i] = window_sum / window
        
    return result # type: ignore


def run_tests() -> None:
    """
    Simple test suite to validate data generation and algorithmic challenges.
    """
    print("--- 7. Running Tests ---")
    try:
        # Test Interview Challenge SMA
        prices = [10.0, 20.0, 30.0, 40.0, 50.0]
        sma = interview_challenge(prices, window=3)
        assert sma == [None, None, 20.0, 30.0, 40.0], f"SMA test failed: {sma}"
        
        # Test basic visualization generation (check if valid figure is returned)
        figs = generate_basic_visualizations()
        assert 'scatter' in figs, "Scatter plot missing"
        assert isinstance(figs['scatter'], go.Figure), "Scatter plot is not a go.Figure instance"
        
        print("All tests passed successfully!\n")
    except AssertionError as e:
        print(f"Test Failed: {e}\n")


if __name__ == "__main__":
    print(f"========== Exploring Plotly Interactive Data Visualization ==========\n")
    
    # Step 1: Basic Visualizations
    basic_figs = generate_basic_visualizations()
    # Note: In a Jupyter Notebook or regular python environment, 
    # you can call `basic_figs['scatter'].show()` to view it in the browser.
    
    # Step 2: Interactive Controls
    interactive_fig = generate_interactive_controls()
    # interactive_fig.show()
    
    # Step 3: Advanced 3D Plot
    surface_fig = generate_3d_mathematical_surface()
    # surface_fig.show()
    
    # Step 4: Real-World Dashboard
    dashboard_fig = generate_real_world_financial_dashboard()
    # dashboard_fig.show()
    
    # Step 5: Performance & Edge Cases
    analyze_performance_and_edge_cases()
    
    # Step 6: Interview Challenge
    sample_data = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0]
    res = interview_challenge(sample_data, 3)
    print(f"Interview Challenge SMA Result for data {sample_data} with window 3:\n{res}\n")
    
    # Step 7: Tests
    run_tests()
    
    print(f"========== END OF Plotly Interactive Lesson ==========\n")
    print("To view any of the generated figures, uncomment the `fig.show()` lines in the script.")
