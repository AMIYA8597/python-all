"""
# ==============================================================================
# LABORATORY: DATA VISUALIZATION (MATPLOTLIB ARCHITECTURE)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Humans are terrible at reading massive tables of numbers. If you show a CEO 
# a Pandas DataFrame containing 10,000 rows of revenue data, they will learn 
# nothing. You must compress that data into a visual representation.
#
# Matplotlib is the grandfather of all Python visualization libraries. Every 
# other library (Seaborn, Pandas `.plot()`) is just a wrapper around Matplotlib.
#
# Matplotlib is notoriously difficult to learn because it has TWO completely 
# different ways to write code:
# 1. The State-Machine Interface (`plt.plot()`): Designed to mimic MATLAB. 
#    It is great for quick scripts, but terrible for complex dashboards.
# 2. The Object-Oriented Interface (`fig, ax = plt.subplots()`): The modern, 
#    industry-standard way. You physically instantiate a "Figure" (the canvas) 
#    and an "Axes" (the actual graph), and modify them as Python objects!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master the Object-Oriented (`fig, ax`) interface.
# - Generate Line Charts, Scatter Plots, and Bar Charts.
# - Customize titles, labels, legends, and gridlines.
#
# ==============================================================================
"""

import numpy as np

# In a real environment: pip install matplotlib
try:
    import matplotlib.pyplot as plt
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE OBJECT-ORIENTED INTERFACE (FIG, AX)
# ==============================================================================
def demonstrate_architecture():
    section_header("Matplotlib Architecture (Figure vs Axes)")
    
    if not HAS_MATPLOTLIB:
        print("[WARNING] Matplotlib not installed. Install using: pip install matplotlib")
        return
        
    print("1. THE FIGURE (The physical window/canvas).")
    print("2. THE AXES (The actual chart/graph drawn on the canvas).\n")
    print("You can draw multiple Axes on a single Figure!")
    
    # 1. INSTANTIATE THE OBJECTS
    # We create 1 canvas, and 1 graph on that canvas.
    fig, ax = plt.subplots(figsize=(8, 5))
    
    # 2. GENERATE DATA
    x = np.linspace(0, 10, 100) # 100 dots between 0 and 10
    y_sin = np.sin(x)
    y_cos = np.cos(x)
    
    # 3. PLOT TO THE AXES
    # We call methods specifically on the `ax` object!
    ax.plot(x, y_sin, color='blue', label='Sine Wave', linestyle='-')
    ax.plot(x, y_cos, color='red', label='Cosine Wave', linestyle='--')
    
    # 4. CUSTOMIZE THE AXES
    ax.set_title("Trigonometric Functions (Object-Oriented API)", fontsize=14)
    ax.set_xlabel("Time (Seconds)", fontsize=12)
    ax.set_ylabel("Amplitude", fontsize=12)
    
    # Enable the legend (which reads the 'label' arguments above)
    ax.legend(loc="upper right")
    
    # Enable the background grid
    ax.grid(True, alpha=0.3)
    
    # Save the Figure to the hard drive!
    # fig.savefig("sine_wave.png", dpi=300)
    print("Chart configured in memory! (Call plt.show() to render GUI window).")
    
    # plt.show() # (Commented out to prevent blocking the automated script)


# ==============================================================================
# 4. SCATTER PLOTS & BAR CHARTS
# ==============================================================================
def demonstrate_plot_types():
    section_header("Other Plot Types (Scatter & Bar)")
    
    if not HAS_MATPLOTLIB: return
    
    # Let's create a Figure that contains TWO separate graphs side-by-side!
    # nrows=1, ncols=2 means a 1x2 grid.
    # `axes` is now an array containing 2 distinct Graph objects!
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(12, 5))
    
    ax1 = axes[0] # The Left Graph
    ax2 = axes[1] # The Right Graph
    
    # -----------------------------------------------------
    # GRAPH 1: SCATTER PLOT
    # -----------------------------------------------------
    # Used for finding correlations between two continuous variables.
    height = np.random.normal(70, 3, 100)
    weight = height * 2.5 + np.random.normal(0, 10, 100) # Highly correlated!
    
    # alpha=0.6 makes the dots slightly transparent so we can see overlaps!
    ax1.scatter(height, weight, color='purple', alpha=0.6, edgecolors='black')
    
    ax1.set_title("Correlation: Height vs Weight")
    ax1.set_xlabel("Height (inches)")
    ax1.set_ylabel("Weight (lbs)")
    
    # -----------------------------------------------------
    # GRAPH 2: BAR CHART
    # -----------------------------------------------------
    # Used for comparing categorical data.
    categories = ['Apples', 'Bananas', 'Cherries', 'Dates']
    sales = [150, 300, 200, 100]
    
    ax2.bar(categories, sales, color=['red', 'yellow', 'darkred', 'brown'])
    
    ax2.set_title("Fruit Sales Q1")
    ax2.set_ylabel("Units Sold")
    
    # Matplotlib allows extreme micro-management. Let's rotate the X-labels!
    ax2.tick_params(axis='x', rotation=45)
    
    # Adjust spacing so the two graphs don't overlap
    fig.tight_layout()
    
    print("Side-by-Side Scatter Plot and Bar Chart configured in memory!")


def run_all_labs():
    demonstrate_architecture()
    demonstrate_plot_types()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why is the Object-Oriented (`fig, ax = plt.subplots()`) interface superior to the State-Machine (`plt.plot()`) interface?
   Answer: The State-Machine interface (`plt.plot()`, `plt.title()`) relies on a hidden, global variable representing the "Currently Active Graph". If you try to build a complex dashboard with 4 different charts, and you call `plt.title()`, it blindly applies the title to whichever chart was drawn last. It is a nightmare to debug. 
   The Object-Oriented interface physically instantiates distinct Python objects in RAM (`ax1`, `ax2`). You call `ax1.set_title()`, guaranteeing absolute, deterministic control over exactly which graph is being modified.

2. What is the difference between a Figure and an Axes?
   Answer: The `Figure` is the physical window (or the blank white canvas). It controls things like the total image resolution (`figsize`, `dpi`), and saving the image to disk (`fig.savefig()`). 
   The `Axes` is the actual mathematical Cartesian plane (the graph) drawn ON the Figure. A single Figure can contain multiple Axes. You plot data, set titles, and configure gridlines strictly on the `Axes` object. (Note: "Axes" is plural for Axis, representing the combined X and Y axes).

3. When should you use a Scatter Plot versus a Line Chart?
   Answer: You use a Line Chart when the X-axis represents a continuous, ordered progression (usually Time). Drawing lines between the points implies that intermediate values exist (e.g., Stock Prices or Temperature over a week). 
   You use a Scatter Plot when comparing two independent, non-chronological variables to search for mathematical Correlation (e.g., Square Footage vs House Price). Drawing lines between random houses would create a chaotic, meaningless scribble.
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Matplotlib Basics Completed.")
