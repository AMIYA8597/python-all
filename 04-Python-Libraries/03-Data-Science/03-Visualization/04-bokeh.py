"""
# ==============================================================================
# LABORATORY: STREAMING WEB VISUALIZATION (BOKEH)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Plotly is excellent for generating interactive HTML files, but it struggles 
# when you need to render 1,000,000 data points simultaneously, or when you 
# need the graph to update in Real-Time (e.g., a live Stock Market ticker or 
# a live IoT sensor dashboard).
#
# **Bokeh** is a specialized interactive visualization library engineered by 
# Anaconda. Like Plotly, it generates JavaScript for the browser (BokehJS). 
# However, Bokeh is specifically optimized for:
# 1. Massive Data: It handles huge datasets far better than standard WebGL.
# 2. Live Streaming: It can bind directly to a Python "Bokeh Server" that 
#    continuously pushes new data via WebSockets to update the graph in real-time 
#    without refreshing the webpage!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the Bokeh architecture (`figure` and glyphs).
# - Generate interactive plots with hover tools.
# - Understand the concept of the `ColumnDataSource`.
#
# ==============================================================================
"""

import numpy as np
import pandas as pd

# In a real environment: pip install bokeh
try:
    import bokeh.plotting as bp
    from bokeh.models import ColumnDataSource, HoverTool
    from bokeh.layouts import column, row
    HAS_BOKEH = True
except ImportError:
    HAS_BOKEH = False

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. BOKEH ARCHITECTURE & GLYPHS
# ==============================================================================
def demonstrate_glyphs():
    section_header("Bokeh Architecture (Figures and Glyphs)")
    
    if not HAS_BOKEH:
        print("[WARNING] Bokeh not installed. Install using: pip install bokeh")
        return
        
    # 1. OUTPUT DESTINATION
    # We tell Bokeh that we want the final result to be a standalone HTML file.
    # bp.output_file("bokeh_scatter.html")
    
    # 2. INSTANTIATE THE FIGURE
    # This is the canvas. We can enable specific interactive tools here!
    # "pan", "wheel_zoom", "box_zoom", "reset", "save"
    p = bp.figure(
        title="Bokeh Interactive Scatter Plot",
        x_axis_label="X-Axis (Random)",
        y_axis_label="Y-Axis (Random)",
        tools="pan,wheel_zoom,box_zoom,reset,save",
        width=800, 
        height=400
    )
    
    # 3. GENERATE DATA
    x = np.random.normal(0, 1, 500)
    y = np.random.normal(0, 1, 500)
    sizes = np.random.uniform(5, 20, 500)
    
    # 4. DRAW GLYPHS
    # Unlike Matplotlib (`plot`) or Plotly (`scatter`), Bokeh focuses on 
    # drawing specific geometric shapes called "Glyphs" (circles, squares, lines, patches).
    # We add a "Circle" glyph to the figure.
    p.circle(
        x, y, 
        size=sizes, 
        color="navy", 
        alpha=0.5, 
        legend_label="Random Data"
    )
    
    print("Bokeh Figure and Glyphs configured in memory!")
    # bp.show(p) # Opens a browser tab to view the HTML!


# ==============================================================================
# 4. THE COLUMN DATA SOURCE & HOVER TOOLS
# ==============================================================================
def demonstrate_cds_and_hover():
    section_header("The ColumnDataSource & Hover Tools")
    
    if not HAS_BOKEH: return
    
    # While you can pass raw NumPy arrays directly to `p.circle()`, the TRUE 
    # power of Bokeh is the `ColumnDataSource` (CDS). 
    # A CDS is the core data structure of Bokeh. It is a dictionary that maps 
    # string names to arrays of data. If you update the CDS in a Bokeh Server, 
    # every single graph attached to it instantly updates in the browser!
    
    df = pd.DataFrame({
        "Employee": ["Alice", "Bob", "Charlie", "David", "Eve"],
        "Salary": [70000, 120000, 55000, 95000, 110000],
        "Tenure": [2, 10, 1, 5, 8],
        "Department": ["HR", "Sales", "HR", "IT", "Sales"]
    })
    
    # Convert Pandas DataFrame into a Bokeh ColumnDataSource
    source = ColumnDataSource(df)
    
    # Instantiate Figure
    p = bp.figure(
        title="Employee Salary vs Tenure",
        x_axis_label="Tenure (Years)",
        y_axis_label="Salary (USD)",
        width=800, 
        height=400,
        tools="pan,box_zoom,reset" # We will add HoverTool manually!
    )
    
    # Draw Glyphs using the CDS!
    # Notice we pass the STRING column names, and then pass `source=source`
    p.circle(
        x="Tenure", 
        y="Salary", 
        size=15, 
        color="darkgreen", 
        alpha=0.7, 
        source=source
    )
    
    # ADDING THE HOVER TOOL
    # We want a beautiful tooltip to appear when the mouse touches a circle.
    # The `@` symbol tells Bokeh to look inside the CDS for that specific column!
    hover = HoverTool(tooltips=[
        ("Name", "@Employee"),        # Displays the Employee column
        ("Dept", "@Department"),      # Displays the Department column
        ("Salary", "$@Salary{0,0}"),  # Formats the Salary with commas!
        ("Years", "@Tenure")
    ])
    
    p.add_tools(hover)
    
    print("\nBokeh Figure with ColumnDataSource and HoverTool configured!")
    print("If this was running on a Bokeh Server, modifying the Python `source` ")
    print("object would magically push the changes to the user's browser via WebSockets!")


# ==============================================================================
# 5. DASHBOARD LAYOUTS
# ==============================================================================
def demonstrate_layouts():
    section_header("Bokeh Layouts (Rows and Columns)")
    
    if not HAS_BOKEH: return
    
    # Creating a dashboard requires placing multiple graphs next to each other.
    p1 = bp.figure(width=400, height=300, title="Left Graph")
    p1.line([1, 2, 3], [1, 4, 9], line_width=2, color="blue")
    
    p2 = bp.figure(width=400, height=300, title="Right Graph")
    p2.square([1, 2, 3], [9, 4, 1], size=10, color="red")
    
    p3 = bp.figure(width=800, height=300, title="Bottom Graph")
    p3.circle([1, 2, 3], [5, 5, 5], size=15, color="green")
    
    # Bokeh Layouts are incredibly intuitive.
    # We put p1 and p2 in a Row, and then put that Row on top of p3 in a Column!
    dashboard = column(
        row(p1, p2),
        p3
    )
    
    print("Dashboard Layout configured in memory! (row/column nested structure)")


def run_all_labs():
    demonstrate_glyphs()
    demonstrate_cds_and_hover()
    demonstrate_layouts()


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. What is the difference between Plotly and Bokeh?
   Answer: Plotly is designed for incredibly rapid, high-level, beautiful interactive charting (`plotly.express`), and creates massive HTML files. Bokeh is a slightly lower-level library built specifically for high-performance streaming. While both generate JavaScript, Bokeh is engineered to connect to a live Python `Bokeh Server`. The Bokeh Server maintains an active WebSocket connection with the browser, allowing the Python backend to push millions of live data updates directly to the graph without ever refreshing the webpage.

2. What is the `ColumnDataSource` (CDS)?
   Answer: The CDS is the foundational data structure of Bokeh. Instead of passing raw arrays to a graphing function, you load all your arrays (or a Pandas DataFrame) into a single CDS object. You then point multiple graphs at the same CDS. The magic happens when you update the data: If you change one array inside the CDS, EVERY graph that is bound to that CDS instantly and automatically updates simultaneously!

3. How does the HoverTool access data that isn't explicitly on the X or Y axis?
   Answer: Through the `ColumnDataSource`! If you plot Salary (Y) vs Tenure (X), those are the only two variables mathematically drawn. But because the entire Pandas DataFrame was loaded into the CDS, the HoverTool has access to the hidden columns. By writing `@Employee` in the tooltip configuration, the Bokeh JavaScript engine knows to look up the "Employee" array in the CDS at the exact index of the hovered circle, displaying data that isn't physically on the axes.
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Bokeh Interactive Visualization Completed.")
