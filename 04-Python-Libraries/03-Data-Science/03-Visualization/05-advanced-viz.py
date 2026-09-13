"""
# ==============================================================================
# LABORATORY: ADVANCED VISUALIZATION (ALTAIR & NETWORKX)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You have learned Matplotlib (Imperative), Seaborn (Statistical), and Plotly 
# (Interactive). But there are two highly specialized realms remaining:
#
# A) Declarative Visualization (Altair)
# Instead of telling the computer *how* to draw the chart (e.g., "draw a blue 
# circle at x, y"), you declare *what* the chart should mean (e.g., "Map the 
# X-axis to Age, the Y-axis to Salary, and the Color to Department"). Altair, 
# based on Vega-Lite, mathematically translates your declaration into an 
# interactive Javascript chart automatically!
#
# B) Graph Theory & Network Topologies (NetworkX)
# How do you visualize a Social Network? Or the Internet? Or a Supply Chain? 
# These are mathematical Graphs (Nodes connected by Edges). Standard charting 
# libraries cannot render them. You need specialized mathematical layout 
# engines (like Spring Layouts) to visualize the physics of the network.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the "Grammar of Graphics" using Altair.
# - Construct mathematical graphs (Nodes and Edges) using NetworkX.
# - Render Network Topologies using Force-Directed Spring layouts.
#
# ==============================================================================
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# In a real environment: pip install altair vega_datasets networkx
try:
    import altair as alt
    HAS_ALTAIR = True
except ImportError:
    HAS_ALTAIR = False

try:
    import networkx as nx
    HAS_NETWORKX = True
except ImportError:
    HAS_NETWORKX = False

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. DECLARATIVE VISUALIZATION (ALTAIR)
# ==============================================================================
def demonstrate_altair():
    section_header("The Grammar of Graphics (Altair)")
    
    if not HAS_ALTAIR:
        print("[WARNING] Altair not installed. Install using: pip install altair")
        return
        
    print("In Altair, you do not write loops or configure pixels. You simply ")
    print("map Data Columns to Visual Encodings (X, Y, Color, Size).")
    
    # 1. GENERATE DATA
    df = pd.DataFrame({
        "Horsepower": np.random.uniform(50, 300, 100),
        "MPG": np.random.uniform(10, 50, 100),
        "Origin": np.random.choice(["USA", "Europe", "Japan"], 100),
        "Weight": np.random.uniform(2000, 5000, 100)
    })
    
    # We want a negative correlation: High Horsepower = Low MPG
    df["MPG"] = 60 - (df["Horsepower"] / 6) + np.random.normal(0, 5, 100)
    
    # 2. THE ALTAIR DECLARATION
    # `alt.Chart(df)` initializes the engine.
    # `.mark_circle()` says we want scatter dots.
    # `.encode()` is the absolute magic of Altair. We just map columns to visuals!
    
    chart = alt.Chart(df).mark_circle().encode(
        x='Horsepower',       # Map X-axis to the Horsepower column
        y='MPG',              # Map Y-axis to the MPG column
        color='Origin',       # Automatically color the dots based on Origin!
        size='Weight',        # Automatically scale the dot size based on Weight!
        tooltip=['Horsepower', 'MPG', 'Origin'] # Enable interactive hover tooltips!
    ).properties(
        title="Automobile Statistics (Altair Declarative)",
        width=600,
        height=400
    ).interactive() # Instantly enables zooming and panning!
    
    # In a Jupyter notebook, typing `chart` renders it.
    # chart.save('altair_chart.html')
    print("\nAltair chart generated in memory! (Highly readable Python code).")
    print("The entire complex chart was built with a single chained method call.")


# ==============================================================================
# 4. NETWORK TOPOLOGIES (NETWORKX)
# ==============================================================================
def demonstrate_networkx():
    section_header("Graph Theory Visualization (NetworkX)")
    
    if not HAS_NETWORKX:
        print("[WARNING] NetworkX not installed. Install using: pip install networkx")
        return
        
    print("Imagine modeling an Airline's flight routes. The Cities are Nodes, ")
    print("and the Flights are Edges connecting the Nodes.")
    
    # 1. INITIALIZE THE GRAPH
    # G is an Undirected Graph (Flights go both ways)
    G = nx.Graph()
    
    # 2. ADD NODES AND EDGES
    G.add_nodes_from(["New York", "London", "Paris", "Tokyo", "Dubai", "Sydney"])
    
    edges = [
        ("New York", "London"),
        ("New York", "Paris"),
        ("London", "Paris"),
        ("London", "Dubai"),
        ("Dubai", "Tokyo"),
        ("Dubai", "Sydney"),
        ("Tokyo", "Sydney")
    ]
    G.add_edges_from(edges)
    
    print(f"\nGraph Constructed mathematically in memory.")
    print(f"Total Nodes: {G.number_of_nodes()}")
    print(f"Total Edges: {G.number_of_edges()}")
    
    # 3. CALCULATE THE PHYSICAL LAYOUT
    # You cannot just plot nodes randomly on a 2D screen; they would overlap!
    # NetworkX uses a "Spring Layout" (Force-Directed Graph). It pretends the 
    # Nodes are electrically repelling each other, and the Edges are rubber bands 
    # pulling them together. It runs a physics simulation to find the perfect 
    # aesthetic layout!
    
    pos = nx.spring_layout(G, seed=42)
    
    # 4. RENDER WITH MATPLOTLIB
    # NetworkX calculates the math, but Matplotlib physically draws the pixels.
    fig, ax = plt.subplots(figsize=(8, 6))
    
    nx.draw(
        G, 
        pos=pos,               # The physical (x, y) coordinates from the physics simulation
        ax=ax, 
        with_labels=True,      # Draw the city names
        node_color='skyblue',  # Node color
        node_size=2000,        # Node size
        edge_color='gray',     # Line color
        font_size=12,
        font_weight='bold'
    )
    
    ax.set_title("Global Airline Flight Network Topology")
    print("Graph physically drawn to Matplotlib Axes using a Spring Physics Layout!")


def run_all_labs():
    demonstrate_altair()
    demonstrate_networkx()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. What is the fundamental difference between Imperative plotting (Matplotlib) and Declarative plotting (Altair)?
   Answer: Imperative plotting forces the programmer to micro-manage the rendering engine. You must write a `for` loop to iterate through the data, manually map the 'Origin' column to a Hex Color string, and then explicitly call `plt.scatter(x, y, color=c)`. Declarative plotting relies on the "Grammar of Graphics". You simply declare the logical mapping: `color='Origin'`. The underlying Vega-Lite engine mathematically analyzes the data types and automatically handles all loops, scales, legends, and hex color generation without you writing a single line of rendering code.

2. Why do we need `nx.spring_layout()` when plotting a Network Graph?
   Answer: A mathematical Graph consists strictly of Nodes and Edges; it contains absolutely zero geometric information. "New York" is connected to "London", but the math doesn't say if New York is at coordinate $(0,0)$ or $(100,500)$. If you plotted them randomly, the lines would cross chaotically. `spring_layout()` runs a Force-Directed physics simulation where nodes repel each other (like magnets) but edges act as springs pulling connected nodes together. The simulation runs until equilibrium is reached, resulting in a perfectly spaced, aesthetically pleasing 2D geometry.

3. Can NetworkX render massive, interactive web graphs?
   Answer: No! NetworkX is a pure mathematical Graph Theory library written in Python. It is spectacular for calculating Shortest Paths (Dijkstra), Centrality, and running Spring Layout physics. However, its rendering engine relies on Matplotlib, generating static, non-interactive PNG images that struggle beyond a few hundred nodes. For massive, interactive web-based network visualizations, Data Scientists calculate the math in NetworkX, export the JSON, and render it using specialized JavaScript libraries like `D3.js`, `Sigma.js`, or `Cytoscape`.
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Advanced Visualization Completed.")
