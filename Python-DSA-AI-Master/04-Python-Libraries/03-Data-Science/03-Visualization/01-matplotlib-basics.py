"""
Module: 01-matplotlib-basics
Description: A comprehensive, textbook-grade interactive lesson on Matplotlib.

=============================================================================
MATPLOTLIB BASICS: A COMPREHENSIVE GUIDE
=============================================================================

Matplotlib is the most widely used data visualization library in Python. It 
was created by John D. Hunter in 2003 and provides a MATLAB-like interface 
for plotting. It allows complete control over the elements of a figure.

Learning Objectives:
1. Understand the fundamental architecture of Matplotlib (Figure vs. Axes).
2. Differentiate between the state-based (pyplot) and object-oriented interfaces.
3. Master basic plots: Line, Scatter, Bar, Histogram, and Pie charts.
4. Learn customization techniques: Colors, Markers, Linestyles, Legends, Annotations.
5. Create complex layouts using subplots and GridSpec.
6. Real-world applications and performance tips.

Mathematical / Conceptual Background:
Matplotlib renders plots inside a `Figure` object, which can contain one or 
more `Axes` (the actual plots with x-y Cartesian planes).
- Figure (Top-level container): The entire window or page that everything is drawn on.
- Axes (The Plot): The area where data is plotted, with a title, x-label, and y-label.
- Axis: Number-line objects.
- Artist: Everything you can see on the figure (Text objects, Line2D objects, collections).

Time Complexity (Big-O Analysis):
- Matplotlib rendering scales linearly O(N) with the number of data points.
- Plotting > 100,000 points in standard Line2D or scatter can be slow.
  Optimization: Downsample data, use `plot` over `scatter`, or use rasterized 
  backends.

=============================================================================
"""

import sys
import time
import math
import random
from typing import List, Dict, Any, Tuple, Optional

# Attempt to import necessary libraries
try:
    import matplotlib.pyplot as plt
    import matplotlib.gridspec as gridspec
    import matplotlib.patches as patches
    import numpy as np
except ImportError as e:
    print(f"Error: Required libraries not found. Please run 'pip install matplotlib numpy'")
    sys.exit(1)


# ============================================================================
# 1. ARCHITECTURE AND INTERFACES
# ============================================================================

def demonstrate_interfaces() -> None:
    """
    Demonstrates the difference between the Pyplot API (state-machine)
    and the Object-Oriented API.
    
    The Pyplot API is convenient for quick plots.
    The Object-Oriented API gives you more control and is strongly recommended
    for anything beyond a single plot.
    """
    print("\n--- 1. Matplotlib Interfaces ---")
    
    # Generate some sample data
    x = np.linspace(0, 10, 100)
    y1 = np.sin(x)
    y2 = np.cos(x)
    
    # --- Interface A: Pyplot (State-Machine) ---
    print("Generating plot using Pyplot interface...")
    plt.figure(figsize=(8, 4))
    plt.plot(x, y1, label='sin(x)')
    plt.title('Pyplot Interface Example')
    plt.xlabel('x-axis')
    plt.ylabel('y-axis')
    plt.legend()
    # plt.show() # Commented out to prevent blocking in automation scripts
    plt.close() # Close figure to free memory
    
    # --- Interface B: Object-Oriented (Recommended) ---
    print("Generating plot using Object-Oriented interface...")
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(x, y2, color='red', linestyle='--', label='cos(x)')
    ax.set_title('Object-Oriented Interface Example')
    ax.set_xlabel('x-axis')
    ax.set_ylabel('y-axis')
    ax.legend()
    # plt.show()
    plt.close()
    print("Successfully demonstrated both interfaces.")


# ============================================================================
# 2. FUNDAMENTAL PLOT TYPES
# ============================================================================

def basic_plots() -> None:
    """
    Explores the most common plot types: Line, Scatter, Bar, Histogram, Pie.
    """
    print("\n--- 2. Fundamental Plot Types ---")
    
    # Prepare data
    np.random.seed(42)
    x = np.linspace(0, 5, 20)
    y = x ** 2
    
    categories = ['A', 'B', 'C', 'D', 'E']
    values = [15, 30, 45, 10, 50]
    
    data_dist = np.random.randn(1000)
    
    # Create a 2x3 grid of subplots
    fig, axs = plt.subplots(2, 3, figsize=(15, 10))
    fig.suptitle('Basic Plot Types in Matplotlib', fontsize=16)
    
    # 1. Line Plot (axs[0, 0])
    # Good for continuous data, time series
    axs[0, 0].plot(x, y, marker='o', color='b', linestyle='-')
    axs[0, 0].set_title('Line Plot')
    axs[0, 0].grid(True)
    
    # 2. Scatter Plot (axs[0, 1])
    # Good for showing correlation between two variables
    axs[0, 1].scatter(x, y + np.random.normal(0, 2, len(x)), c='r', marker='x')
    axs[0, 1].set_title('Scatter Plot')
    
    # 3. Bar Chart (Vertical) (axs[0, 2])
    # Good for comparing categorical data
    axs[0, 2].bar(categories, values, color='skyblue', edgecolor='black')
    axs[0, 2].set_title('Bar Chart')
    
    # 4. Bar Chart (Horizontal) (axs[1, 0])
    axs[1, 0].barh(categories, values, color='lightgreen')
    axs[1, 0].set_title('Horizontal Bar Chart')
    
    # 5. Histogram (axs[1, 1])
    # Good for visualizing distributions
    axs[1, 1].hist(data_dist, bins=30, color='purple', alpha=0.7)
    axs[1, 1].set_title('Histogram')
    
    # 6. Pie Chart (axs[1, 2])
    # Shows parts of a whole
    explode = (0, 0.1, 0, 0, 0) # "explode" the 2nd slice
    axs[1, 2].pie(values, labels=categories, autopct='%1.1f%%', explode=explode, shadow=True, startangle=90)
    axs[1, 2].set_title('Pie Chart')
    
    plt.tight_layout() # Adjusts subplots so they don't overlap
    # plt.show()
    plt.close()
    print("Generated standard plot types successfully.")


# ============================================================================
# 3. ADVANCED CUSTOMIZATION
# ============================================================================

def advanced_customization() -> None:
    """
    Demonstrates deep customization: ticks, spines, annotations, math text.
    """
    print("\n--- 3. Advanced Customization ---")
    
    x = np.linspace(-np.pi, np.pi, 256)
    c, s = np.cos(x), np.sin(x)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Plotting with custom linewidth, color, linestyle
    ax.plot(x, c, color="blue", linewidth=2.5, linestyle="-", label="cosine")
    ax.plot(x, s, color="red",  linewidth=2.5, linestyle="-", label="sine")
    
    # Customizing axes limits
    ax.set_xlim(x.min() * 1.1, x.max() * 1.1)
    ax.set_ylim(c.min() * 1.1, c.max() * 1.1)
    
    # Customizing ticks and tick labels (using LaTeX math text)
    ax.set_xticks([-np.pi, -np.pi/2, 0, np.pi/2, np.pi])
    ax.set_xticklabels([r'$-\pi$', r'$-\pi/2$', r'$0$', r'$+\pi/2$', r'$+\pi$'], fontsize=14)
    ax.set_yticks([-1, 0, +1])
    ax.set_yticklabels([r'$-1$', r'$0$', r'$+1$'], fontsize=14)
    
    # Moving spines (the box lines around the plot)
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.spines['bottom'].set_position(('data', 0)) # Move bottom spine to y=0
    ax.spines['left'].set_position(('data', 0))   # Move left spine to x=0
    
    # Annotate a specific point
    t = 2 * np.pi / 3
    # Draw a dashed line from the x-axis to the sine curve
    ax.plot([t, t], [0, np.sin(t)], color='red', linewidth=1.5, linestyle="--")
    # Plot the point
    ax.scatter([t], [np.sin(t)], 50, color='red')
    # Add annotation text with an arrow
    ax.annotate(r'$\sin(\frac{2\pi}{3})=\frac{\sqrt{3}}{2}$',
                xy=(t, np.sin(t)), xycoords='data',
                xytext=(+10, +30), textcoords='offset points', fontsize=16,
                arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))
                
    ax.legend(loc='upper left', frameon=False)
    
    plt.title('Trigonometric Functions Customization', y=1.05)
    # plt.show()
    plt.close()
    print("Customized plots created with specific ticks, spines, and annotations.")


# ============================================================================
# 4. COMPLEX LAYOUTS WITH GRIDSPEC
# ============================================================================

def complex_layouts() -> None:
    """
    Shows how to use GridSpec for uneven subplot sizes.
    """
    print("\n--- 4. Complex Layouts using GridSpec ---")
    
    fig = plt.figure(figsize=(10, 8))
    # Create a 3x3 grid
    gs = gridspec.GridSpec(3, 3)
    
    # Ax1 spans the entire first row
    ax1 = fig.add_subplot(gs[0, :])
    ax1.set_title('gs[0, :]')
    
    # Ax2 spans the second row, first two columns
    ax2 = fig.add_subplot(gs[1, :-1])
    ax2.set_title('gs[1, :-1]')
    
    # Ax3 spans the second row, last column down to the third row, last column
    ax3 = fig.add_subplot(gs[1:, -1])
    ax3.set_title('gs[1:, -1]')
    
    # Ax4 spans the third row, first column
    ax4 = fig.add_subplot(gs[-1, 0])
    ax4.set_title('gs[-1, 0]')
    
    # Ax5 spans the third row, second column
    ax5 = fig.add_subplot(gs[-1, -2])
    ax5.set_title('gs[-1, -2]')
    
    # Clean up layout
    fig.tight_layout()
    # plt.show()
    plt.close()
    print("Complex layout GridSpec example constructed.")


# ============================================================================
# 5. PERFORMANCE AND EDGE CASES
# ============================================================================

def analyze_performance_and_edge_cases() -> None:
    """
    Discusses performance with large datasets and memory management.
    """
    print("\n--- 5. Performance Analysis & Edge Cases ---")
    print("Performance Tips:")
    print("1. Big Data in Line Plots: Using `ax.plot` with > 1,000,000 points gets slow.")
    print("   Solution: Downsample your data or use specialized libraries like DataShader.")
    print("2. Memory Management: Always use `plt.close(fig)` when creating figures in a loop,")
    print("   otherwise Matplotlib keeps all figures in memory, leading to memory leaks.")
    print("3. Vector vs Raster: Saving as PDF/SVG is vector (infinitely scalable, but large file size for many points).")
    print("   Saving as PNG/JPG is raster (pixelated if zoomed, smaller size).")
    print("   You can use `ax.plot(..., rasterized=True)` to only rasterize the heavy data parts but keep text as vectors.")
    print("\nEdge Cases:")
    print("1. Logarithmic scales (`ax.set_yscale('log')`) fail if data contains zero or negative values.")
    print("2. Handling NaNs: Matplotlib naturally breaks lines at `np.nan` values, which is often useful for missing data gaps.")


# ============================================================================
# 6. INTERVIEW CHALLENGE
# ============================================================================

def interview_challenge() -> None:
    """
    Challenge: Write a function that plots the Mandelbrot set using matplotlib.
    This demonstrates manipulating image data (2D arrays) with Matplotlib.
    """
    print("\n--- 6. Interview Challenge: Mandelbrot Set ---")
    print("Task: Compute and visualize the Mandelbrot set.")
    
    # Function to compute Mandelbrot set
    def mandelbrot(c: complex, max_iter: int) -> int:
        z = 0
        for n in range(max_iter):
            if abs(z) > 2:
                return n
            z = z*z + c
        return max_iter
    
    # Grid parameters
    width, height = 400, 300
    x_min, x_max = -2.0, 1.0
    y_min, y_max = -1.5, 1.5
    max_iter = 50
    
    # Initialize the image array
    image = np.zeros((height, width))
    
    print("Computing Mandelbrot fractal (this may take a second)...")
    start_time = time.time()
    for y in range(height):
        for x in range(width):
            real = x_min + (x / width) * (x_max - x_min)
            imag = y_min + (y / height) * (y_max - y_min)
            c = complex(real, imag)
            image[y, x] = mandelbrot(c, max_iter)
            
    print(f"Computed in {time.time() - start_time:.2f} seconds.")
    
    # Plotting using imshow
    fig, ax = plt.subplots(figsize=(8, 6))
    im = ax.imshow(image, cmap='magma', extent=[x_min, x_max, y_min, y_max])
    ax.set_title("Mandelbrot Set")
    ax.set_xlabel("Re(c)")
    ax.set_ylabel("Im(c)")
    fig.colorbar(im, ax=ax, label="Iterations")
    
    # plt.show()
    plt.close()
    print("Mandelbrot plotted successfully.")


# ============================================================================
# 7. MAIN EXECUTION & TESTS
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print(" EXPLORING MATPLOTLIB BASICS - MASTERCLASS")
    print("=" * 60)
    
    # Run modules
    demonstrate_interfaces()
    basic_plots()
    advanced_customization()
    complex_layouts()
    analyze_performance_and_edge_cases()
    interview_challenge()
    
    print("\n" + "=" * 60)
    print(" END OF MATPLOTLIB MASTERCLASS")
    print("=" * 60)
