"""
Module: 04_bokeh
Description: A textbook-grade interactive lesson on Bokeh, a Python interactive visualization library.

===========================================================================
Python Data Science Master - Visualization with Bokeh
===========================================================================

Learning Objectives:
1. Understand the core architecture of Bokeh (Python -> JSON -> BokehJS).
2. Learn how to create fundamental plots using glyphs (scatter, line, bar).
3. Implement interactivity: toolbars, hover tools, and linked brushing.
4. Manage data efficiently using ColumnDataSource.
5. Understand the performance implications (Big-O analysis) of rendering 
   large datasets in the browser.
6. Explore real-world applications of interactive dashboards.

===========================================================================
1. Concept Explanation
===========================================================================
Bokeh is an interactive visualization library for modern web browsers. It 
provides elegant, concise construction of versatile graphics, and affords 
high-performance interactivity over large or streaming datasets. Unlike 
Matplotlib, which primarily generates static images, Bokeh creates 
JSON objects representing the plot, which are rendered by BokehJS in the 
browser.

Architecture:
Python Code -> Bokeh Models -> JSON -> BokehJS (JavaScript in Browser)

Mathematical Background & Big-O Analysis:
Rendering geometric primitives (glyphs) involves mapping data coordinates 
to screen pixels.
Given N data points, translating from data space (x, y) to screen space 
(sx, sy):
    sx = a_x * x + b_x
    sy = a_y * y + b_y

Time Complexity:
- Constructing the ColumnDataSource: O(N), where N is the number of points.
- Serializing to JSON: O(N).
- Rendering in browser (DOM/Canvas): O(N). Modern browsers handle rendering 
  up to ~10^4 to 10^5 points well. Beyond that, performance degrades.
- Downsampling (e.g., Datashader integration) reduces O(N) points to 
  O(W * H) pixels (where W and H are the width and height of the plot in pixels).

Space Complexity:
- O(N) memory is required in Python.
- O(N) memory is required in the browser for BokehJS to maintain the models.

Real-World Applications:
- Financial Dashboards: Real-time stock prices or cryptocurrency tracking.
- Bioinformatics: Interactive gene expression heatmaps.
- Geospatial Data: Interactive maps with overlays.
===========================================================================
"""

import sys
import time
import math
import random
from typing import List, Dict, Any, Optional, Tuple, Union

try:
    import numpy as np
    import pandas as pd
    from bokeh.plotting import figure, show, output_file, save
    from bokeh.models import ColumnDataSource, HoverTool, CategoricalColorMapper
    from bokeh.layouts import gridplot, column, row
    from bokeh.palettes import Spectral6
    from bokeh.transform import factor_cmap
    BOKEH_AVAILABLE = True
except ImportError:
    BOKEH_AVAILABLE = False
    print("WARNING: Bokeh, NumPy, or Pandas is not installed. Please install using:")
    print("pip install bokeh numpy pandas")


def basic_glyph_rendering(output_path: str = "basic_scatter.html") -> None:
    """
    Demonstrates the fundamental usage of Bokeh: rendering basic glyphs.
    
    Time Complexity: O(N) to process and render N points.
    Space Complexity: O(N) memory overhead for lists and Bokeh models.
    """
    print("--- 1. Basic Glyph Rendering ---")
    if not BOKEH_AVAILABLE:
        print("Bokeh not available. Skipping basic_glyph_rendering.")
        return

    # Generate some random data
    # N = 100 points
    N = 100
    x: List[float] = [random.random() * 100 for _ in range(N)]
    y: List[float] = [val * 1.5 + (random.random() * 20 - 10) for val in x]
    
    # Specify the output file
    output_file(output_path, title="Basic Scatter Plot")

    # Create a new figure with tools
    # We define the tools we want in the toolbar.
    tools = "pan,wheel_zoom,box_zoom,reset,save"
    
    p = figure(
        title="Simple Scatter Plot (x vs y)", 
        x_axis_label="X-Axis", 
        y_axis_label="Y-Axis",
        tools=tools,
        width=600,
        height=400
    )
    
    # Add a circle glyph
    p.scatter(x, y, size=8, color="navy", alpha=0.5)
    
    # Save the plot
    save(p)
    print(f"Basic scatter plot saved to {output_path}\n")


def column_data_source_and_hover(output_path: str = "hover_plot.html") -> None:
    """
    Demonstrates the use of ColumnDataSource and HoverTool.
    ColumnDataSource is the core data structure in Bokeh that maps column names
    to sequences of data.
    """
    print("--- 2. ColumnDataSource and Interactive Hover ---")
    if not BOKEH_AVAILABLE:
        print("Bokeh not available. Skipping column_data_source_and_hover.")
        return

    # 1. Create Data
    # In a real-world scenario, this might come from a pandas DataFrame
    data: Dict[str, List[Any]] = {
        'x': [1, 2, 3, 4, 5],
        'y': [2, 5, 8, 2, 7],
        'desc': ['A', 'b', 'C', 'd', 'E'],
        'size': [10, 20, 30, 20, 15]
    }
    
    # Create the ColumnDataSource
    source = ColumnDataSource(data=data)
    
    # Define HoverTool
    # The tooltips parameter accepts a list of tuples (label, value_reference)
    # @ refers to a column in the ColumnDataSource
    # $ refers to a special field like $x or $y (coordinates of the cursor)
    hover = HoverTool(
        tooltips=[
            ("Index", "$index"),
            ("Coordinates", "($x, $y)"),
            ("Description", "@desc"),
            ("Value", "@y")
        ]
    )

    output_file(output_path, title="Hover Tool Example")
    
    p = figure(
        title="Interactive Hover Tool Example",
        width=600,
        height=400,
        tools=[hover, "pan", "wheel_zoom", "reset"]
    )
    
    # Use the source parameter to link glyphs to the ColumnDataSource
    p.scatter('x', 'y', size='size', source=source, color="firebrick", alpha=0.6)
    
    save(p)
    print(f"Hover plot saved to {output_path}\n")


def linked_brushing_and_panning(output_path: str = "linked_plots.html") -> None:
    """
    Demonstrates advanced interactivity: linked panning and linked brushing.
    When plots share data sources or axis ranges, Bokeh automatically links them.
    
    Time Complexity: O(N) across multiple plots.
    Space Complexity: O(N), though memory is shared via a single ColumnDataSource.
    """
    print("--- 3. Linked Brushing and Panning ---")
    if not BOKEH_AVAILABLE:
        print("Bokeh not available. Skipping linked_brushing_and_panning.")
        return

    # Generate data
    N = 300
    x = np.linspace(0, 4 * np.pi, N)
    y0 = np.sin(x)
    y1 = np.cos(x)
    y2 = np.sin(x) + np.cos(x)

    # A shared ColumnDataSource enables Linked Brushing (selection)
    source = ColumnDataSource(data=dict(x=x, y0=y0, y1=y1, y2=y2))
    
    # Create three plots
    # Linked Panning: achieved by sharing x_range or y_range
    p1 = figure(width=350, height=350, tools="pan,box_select,reset,save", title="Sine")
    p1.scatter('x', 'y0', source=source, color="blue", alpha=0.6)

    # Share x_range with p1
    p2 = figure(width=350, height=350, x_range=p1.x_range, tools="pan,box_select,reset,save", title="Cosine")
    p2.scatter('x', 'y1', source=source, color="green", alpha=0.6)

    # Share x_range with p1 and p2
    p3 = figure(width=350, height=350, x_range=p1.x_range, tools="pan,box_select,reset,save", title="Sine + Cosine")
    p3.scatter('x', 'y2', source=source, color="red", alpha=0.6)

    # Arrange plots in a grid layout
    layout = gridplot([[p1, p2, p3]])
    
    output_file(output_path, title="Linked Plots")
    save(layout)
    print(f"Linked plots saved to {output_path}\n")


def categorical_data_and_bar_charts(output_path: str = "bar_chart.html") -> None:
    """
    Demonstrates handling categorical data and creating bar charts.
    """
    print("--- 4. Categorical Data and Bar Charts ---")
    if not BOKEH_AVAILABLE:
        print("Bokeh not available. Skipping categorical_data_and_bar_charts.")
        return

    # Categories must be strings
    fruits = ['Apples', 'Pears', 'Nectarines', 'Plums', 'Grapes', 'Strawberries']
    counts = [5, 3, 4, 2, 4, 6]

    source = ColumnDataSource(data=dict(fruits=fruits, counts=counts))
    
    # We define the x_range using the list of categories
    p = figure(
        x_range=fruits, 
        height=350, 
        title="Fruit Counts",
        toolbar_location=None, 
        tools=""
    )

    # color palette from Spectral6
    # Map the fruits to colors
    p.vbar(
        x='fruits', 
        top='counts', 
        width=0.9, 
        source=source, 
        line_color="white",
        fill_color=factor_cmap('fruits', palette=Spectral6, factors=fruits)
    )

    p.xgrid.grid_line_color = None
    p.y_range.start = 0

    output_file(output_path, title="Categorical Bar Chart")
    save(p)
    print(f"Bar chart saved to {output_path}\n")


def performance_analysis() -> None:
    """
    Analyzes performance bottlenecks and Big-O constraints for Bokeh.
    """
    print("--- 5. Performance Analysis & Best Practices ---")
    print("1. JSON Serialization (O(N)): Every data point in ColumnDataSource is serialized to JSON.")
    print("   Avoid passing massive datasets (>100k rows) directly. Use downsampling (e.g., Datashader).")
    print("2. Browser DOM Limits: Drawing too many glyphs slows down Canvas/SVG rendering in the browser.")
    print("3. Bokeh Server: For large streaming datasets or complex callbacks requiring Python,")
    print("   use Bokeh Server instead of static HTML outputs.")
    print("4. Avoid redundant ColumnDataSources: If multiple plots use the same data, share the source.\n")


def interview_challenge(data_points: int = 1000) -> Tuple[float, float]:
    """
    Interview Challenge: 
    Implement a function that simulates data transformation for a Bokeh dashboard.
    Given N data points, you need to normalize them (min-max scaling) in O(N) time,
    so they fit within a [0, 1] scale for rendering a specialized heatmap.
    
    Args:
        data_points: Number of points to generate and normalize.
    
    Returns:
        Tuple of (time_taken, verification_sum)
    """
    print(f"--- 6. Interview Challenge: O(N) Data Normalization for {data_points} points ---")
    start_time = time.time()
    
    # 1. Generate random data O(N)
    raw_data = [random.uniform(0, 1000) for _ in range(data_points)]
    
    # 2. Find min and max in O(N)
    min_val = min(raw_data)
    max_val = max(raw_data)
    
    # 3. Normalize to [0, 1] in O(N)
    range_val = max_val - min_val if max_val != min_val else 1
    normalized_data = [(x - min_val) / range_val for x in raw_data]
    
    end_time = time.time()
    time_taken = end_time - start_time
    
    # Verification sum to ensure the math is somewhat checked
    verification_sum = sum(normalized_data)
    
    print(f"Normalization completed in {time_taken:.6f} seconds.")
    print(f"Expected sum roughly ~ {data_points / 2:.2f}, got {verification_sum:.2f}\n")
    
    return time_taken, verification_sum


def run_tests() -> None:
    """
    Validates mathematical transformations and logic in the module.
    """
    print("--- Running Tests ---")
    try:
        # Test normalization logic
        time_taken, verif_sum = interview_challenge(100)
        assert 35 <= verif_sum <= 65, f"Normalization sum out of expected bounds: {verif_sum}"
        
        print("All logical tests passed successfully!\n")
    except AssertionError as e:
        print(f"Test Failed: {e}\n")


if __name__ == "__main__":
    print(f"========== Exploring BOKEH ==========\n")
    
    basic_glyph_rendering()
    column_data_source_and_hover()
    linked_brushing_and_panning()
    categorical_data_and_bar_charts()
    performance_analysis()
    
    # Interview Challenge
    interview_challenge(100000)
    
    # Tests
    run_tests()
    
    print(f"========== END OF BOKEH ==========\n")
