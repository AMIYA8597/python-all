"""
# ==============================================================================
# LABORATORY: INTERACTIVE VISUALIZATION (PLOTLY)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Matplotlib and Seaborn are fantastic for academic papers and PDF reports 
# because they render static image files (PNG/SVG). 
# 
# However, if you are building a modern web dashboard for a CEO, a static PNG 
# is unacceptable. Users expect to hover their mouse over a data point and see 
# the exact dollar amount. They expect to click and drag to zoom into a specific 
# timeline. They expect to click a legend item to hide a specific category.
#
# **Plotly** solves this. Plotly does not render PNG images. It generates massive 
# JSON objects and HTML/JavaScript code. When rendered in a Jupyter Notebook or 
# a web browser, it creates a fully interactive, GPU-accelerated visualization 
# powered by Plotly.js and WebGL.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the Plotly Express (`px`) high-level architecture.
# - Generate interactive Scatter Plots with Hover Tooltips.
# - Generate interactive Geographical Maps (Choropleth).
# - Export interactive HTML bundles for web deployment.
#
# ==============================================================================
"""

import pandas as pd
import numpy as np

# In a real environment: pip install plotly
try:
    import plotly.express as px
    import plotly.graph_objects as go
    HAS_PLOTLY = True
except ImportError:
    HAS_PLOTLY = False

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. PLOTLY EXPRESS (INTERACTIVE SCATTER PLOTS)
# ==============================================================================
def demonstrate_plotly_express():
    section_header("Plotly Express (px.scatter)")
    
    if not HAS_PLOTLY:
        print("[WARNING] Plotly is not installed. Install using: pip install plotly")
        return
        
    print("Plotly Express (`px`) is the Seaborn equivalent for Plotly. It allows ")
    print("you to build massive interactive charts in exactly 1 line of code.\n")
    
    # 1. GENERATE DATA
    # GDP per Capita vs Life Expectancy for various countries
    df = pd.DataFrame({
        "Country": ["USA", "China", "India", "Germany", "Brazil", "Nigeria", "Japan"],
        "Continent": ["Americas", "Asia", "Asia", "Europe", "Americas", "Africa", "Asia"],
        "GDP_per_Capita": [65000, 10000, 2000, 50000, 8000, 2500, 40000],
        "Life_Expectancy": [78, 76, 69, 81, 75, 54, 84],
        "Population": [330_000_000, 1_400_000_000, 1_380_000_000, 83_000_000, 212_000_000, 206_000_000, 125_000_000]
    })
    
    # 2. CREATE THE INTERACTIVE FIGURE
    # `size`: The bubbles will scale based on the Population column!
    # `color`: The bubbles will be colored by Continent!
    # `hover_name`: When you hover your mouse, the Country name appears in bold!
    fig = px.scatter(
        df,
        x="GDP_per_Capita",
        y="Life_Expectancy",
        size="Population",
        color="Continent",
        hover_name="Country",
        log_x=True, # GDP is exponential, so we use a Logarithmic X-Axis!
        size_max=60, # Maximum bubble size
        title="Global Wealth vs Health (Interactive)"
    )
    
    # 3. RENDERING
    # If we were in Jupyter, we would just type `fig.show()`.
    # Because we are in a script, we can save the entire interactive Javascript 
    # engine into a standalone HTML file!
    
    # fig.write_html("interactive_chart.html")
    print("Interactive Scatter Plot generated in memory!")
    print("In a real environment, calling `fig.write_html('chart.html')` allows ")
    print("you to email the interactive chart to anyone, and it will render ")
    print("perfectly in Google Chrome without them needing Python installed!")


# ==============================================================================
# 4. PLOTLY GRAPH OBJECTS (CUSTOM ARCHITECTURE)
# ==============================================================================
def demonstrate_graph_objects():
    section_header("Plotly Graph Objects (go.Figure)")
    
    if not HAS_PLOTLY: return
    
    print("Plotly Express (`px`) is great for standard DataFrames.")
    print("Plotly Graph Objects (`go`) is the low-level engine. You use it when ")
    print("you need absolute pixel-perfect control over every element, or when ")
    print("building complex Financial Candlestick charts.")
    
    # Simulating Stock Market Data
    dates = pd.date_range(start="2024-01-01", periods=5)
    open_p = [100, 102, 101, 105, 103]
    high_p = [105, 104, 106, 108, 107]
    low_p = [98, 99, 100, 102, 101]
    close_p = [102, 101, 105, 103, 106]
    
    # We manually construct a Figure, and manually append a "Trace" (a layer) to it!
    fig = go.Figure(data=[
        go.Candlestick(
            x=dates,
            open=open_p,
            high=high_p,
            low=low_p,
            close=close_p,
            increasing_line_color='green',
            decreasing_line_color='red'
        )
    ])
    
    fig.update_layout(
        title="AAPL Stock Price (Candlestick)",
        yaxis_title="Stock Price (USD)",
        xaxis_rangeslider_visible=False # Turns off the default timeline slider
    )
    
    print("\nLow-level Candlestick chart generated using Graph Objects.")


# ==============================================================================
# 5. GEOGRAPHICAL MAPS (CHOROPLETH)
# ==============================================================================
def demonstrate_maps():
    section_header("Interactive Geographical Maps")
    
    if not HAS_PLOTLY: return
    
    print("Plotly has native support for rendering interactive maps of the Earth!")
    
    df = pd.DataFrame({
        "Country_Code": ["USA", "CAN", "MEX", "BRA", "ARG"],
        "Sales": [15000, 8000, 5000, 12000, 3000]
    })
    
    # A Choropleth map colors polygons (countries/states) based on a variable.
    fig = px.choropleth(
        df,
        locations="Country_Code", # Plotly natively understands ISO-3 codes!
        color="Sales",
        hover_name="Country_Code",
        color_continuous_scale=px.colors.sequential.Plasma,
        title="Global Sales Heatmap"
    )
    
    # We can focus the interactive camera on a specific continent
    fig.update_geos(projection_type="natural earth", scope="world")
    
    print("Interactive 3D Choropleth map generated in memory.")


def run_all_labs():
    demonstrate_plotly_express()
    demonstrate_graph_objects()
    demonstrate_maps()


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. What is the fundamental architectural difference between Matplotlib and Plotly?
   Answer: Matplotlib is a Server-Side rendering engine. It calculates the geometry in Python, generates an array of colored pixels, and writes them to a static `.png` image file. Once the PNG is generated, the data is dead. Plotly is a Client-Side rendering engine. It takes the Python DataFrame, serializes the raw data and configuration into a massive JSON object, and injects it into an HTML template containing the `plotly.js` library. When a user opens the HTML file in a web browser, the browser's JavaScript engine reads the JSON and physically renders the interactive WebGL graph on the user's local GPU!

2. When would you use Plotly Graph Objects (`go`) instead of Plotly Express (`px`)?
   Answer: Plotly Express is a high-level wrapper (like Seaborn). It is designed to take a single, perfectly structured Pandas DataFrame and generate a standard chart (Scatter, Bar, Line) in exactly one line of code. Plotly Graph Objects (`go`) is the low-level architecture beneath it. You use `go` when you need to construct highly custom, multi-layered dashboards (e.g., placing a Candlestick chart, a Bar chart, and a Line chart onto the exact same grid), or when dealing with raw arrays rather than a Pandas DataFrame.

3. Why is `fig.write_html()` incredibly powerful for corporate reporting?
   Answer: In a corporate environment, the CEO or Business Stakeholders do not have Python, Jupyter, or an IDE installed on their laptops. If you use Matplotlib, you must send them a static PDF or PNG. With Plotly's `write_html()`, it bundles the entire JavaScript engine, the HTML layout, and the raw JSON data into a single, standalone `.html` file. You can attach this 2MB file to an email. When the CEO clicks it, it opens in Google Chrome, giving them a fully interactive, zooming, hovering dashboard with zero installation required!
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Plotly Interactive Visualization Completed.")
