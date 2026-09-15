"""
# ==============================================================================
# LABORATORY: DATA ANALYTICS (DATA VISUALIZATION)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A junior analyst presents a spreadsheet with 10,000 rows of numbers to the 
# CEO to explain why Q3 Revenue dropped. The CEO stares at the raw numbers, 
# understands nothing, gets frustrated, and rejects the analysis.
#
# A senior data scientist understands "Anscombe's Quartet"—the mathematical 
# proof that four datasets can have the exact same Mean, Variance, and Correlation, 
# but look completely different when graphed. They use Matplotlib and Seaborn 
# to architect a visual narrative. They plot a clear, labeled Line Chart with 
# a 7-day rolling average and a shaded confidence interval. The CEO instantly 
# sees the exact day the drop occurred, understands the trend, and approves the 
# recovery budget.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master Matplotlib's Object-Oriented API (Figure and Axes).
# - Execute Seaborn for Statistical Data Visualization.
# - Architect Data Narratives using labels, titles, and legends.
#
# ==============================================================================
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE BUSINESS LOGIC (THE DATASET)
# ==============================================================================
class VisualizationSimulator:
    
    def __init__(self):
        self.df = None
        self.output_dir = "visualization_output"
        
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            
        self._generate_time_series_data()
        
    def _generate_time_series_data(self):
        """Generates 365 days of stock/revenue data for visual analysis."""
        print("  [INIT] Generating 365 days of Time-Series data...")
        
        # Creating a date range
        dates = pd.date_range(start='2023-01-01', periods=365)
        
        # Simulating random walks (like a stock price)
        np.random.seed(42)
        revenue_tech = np.cumsum(np.random.randn(365) * 10) + 1000
        revenue_retail = np.cumsum(np.random.randn(365) * 8) + 800
        
        self.df = pd.DataFrame({
            'Date': dates,
            'Tech_Revenue': revenue_tech,
            'Retail_Revenue': revenue_retail
        })


    # --------------------------------------------------------------------------
    # THE ANTI-PATTERN: PROCEDURAL PLOTTING (plt.plot)
    # --------------------------------------------------------------------------
    def generate_bad_plot(self):
        """
        [WARNING] The Junior Approach.
        Relying on stateful `plt.plot()` without managing the Figure/Axes explicitly.
        This leads to overlapping plots in Jupyter Notebooks and terrible formatting.
        """
        print("\n  [EXECUTION] Generating Procedural Plot (The Bad Way)...")
        
        plt.figure(figsize=(8, 4))
        plt.plot(self.df['Date'], self.df['Tech_Revenue'])
        # No Title, No Legend, Unreadable X-Axis dates!
        
        # We will save it to prove how bad it looks.
        out_path = os.path.join(self.output_dir, "bad_plot.png")
        plt.savefig(out_path)
        plt.close() # MUST close to clear memory!
        
        print(f"  -> Saved bad plot to: {out_path}")


    # --------------------------------------------------------------------------
    # THE ARCHITECTURAL PATTERN: OBJECT-ORIENTED PLOTTING
    # --------------------------------------------------------------------------
    def generate_good_plot(self):
        """
        [SECURE] The Senior Approach (Object-Oriented API).
        We explicitly define the Figure (the canvas) and the Axes (the chart).
        We control every single pixel of the visualization.
        """
        print("\n  [EXECUTION] Generating Object-Oriented Plot (The Good Way)...")
        
        # Set a professional Seaborn style globally
        sns.set_theme(style="whitegrid")
        
        # 1. Architecture: Create Canvas (fig) and Plot Area (ax)
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # 2. Execution: Plot the data explicitly on the `ax`
        ax.plot(self.df['Date'], self.df['Tech_Revenue'], label='Tech Sector', color='blue', linewidth=2)
        ax.plot(self.df['Date'], self.df['Retail_Revenue'], label='Retail Sector', color='orange', linewidth=2)
        
        # 3. Enhancement: Calculate and plot a 30-Day Moving Average
        tech_ma = self.df['Tech_Revenue'].rolling(window=30).mean()
        ax.plot(self.df['Date'], tech_ma, label='Tech (30-Day MA)', color='red', linestyle='--')
        
        # 4. Context: Add titles, labels, and legends
        ax.set_title("Annual Revenue Trends by Sector (2023)", fontsize=16, fontweight='bold')
        ax.set_xlabel("Date (Quarters)", fontsize=12)
        ax.set_ylabel("Revenue (USD in Thousands)", fontsize=12)
        
        # 5. formatting: Rotate X-axis dates so they don't overlap!
        fig.autofmt_xdate()
        
        ax.legend(loc='upper left')
        
        out_path = os.path.join(self.output_dir, "good_plot.png")
        fig.savefig(out_path, dpi=300, bbox_inches='tight')
        plt.close(fig)
        
        print(f"  -> Saved professional plot to: {out_path}")


# ==============================================================================
# 4. MATHEMATICAL PROOF (THE BENCHMARK)
# ==============================================================================
def demonstrate_visualization():
    section_header("Data Analytics: Visualization Architecture")
    
    sim = VisualizationSimulator()
    sim.generate_bad_plot()
    sim.generate_good_plot()
    
    print("\n  [ARCHITECTURE PROOF]")
    print("  By utilizing the Object-Oriented `fig, ax = plt.subplots()` API, ")
    print("  the Data Engineer mathematically decoupled the Canvas from the Chart, ")
    print("  allowing absolute control over formatting, moving averages, and legends.")


def run_all_labs():
    demonstrate_visualization()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "What is the architectural difference between Matplotlib's `plt.plot()` (Pyplot interface) and `fig, ax = plt.subplots()` (Object-Oriented interface)?"
   Senior Answer: "Stateful vs Stateless Architecture. `plt.plot()` relies on a global, stateful machine hidden inside Matplotlib. When you call it, it mathematically draws on whatever the 'currently active' figure is. In a massive Jupyter Notebook, this causes charts to bleed into one another and crash. The Object-Oriented API (`fig, ax = plt.subplots()`) is stateless. You explicitly instantiate a `Figure` Object (the blank canvas) and an `Axes` Object (the actual physical chart area). You then explicitly command `ax.plot()`. This guarantees thread-safety and allows you to architect complex layouts (e.g., $2 \\times 2$ grid of charts) without state corruption."

2. Interviewer: "Why do Senior Data Scientists use Seaborn in addition to Matplotlib?"
   Senior Answer: "Statistical Abstraction. Matplotlib is a low-level graphics library; it draws lines and polygons on a screen. If you want to draw a Linear Regression line through a scatter plot with a $95\\%$ Confidence Interval, you must manually execute the calculus, solve the regression, compute the bounds, and draw 3 separate elements in Matplotlib. Seaborn is a high-level statistical wrapper. You write exactly one line: `sns.lmplot(x='Age', y='Income', data=df)`. Seaborn mathematically calculates the regression, computes the confidence interval, and executes the Matplotlib drawing commands under the hood, saving hours of development time."

3. Interviewer: "Explain the concept of a 'Rolling Average' (Moving Average) in Time-Series visualization, and why it is mathematically necessary."
   Senior Answer: "Noise Smoothing. Financial and operational data is mathematically noisy; it fluctuates wildly from day to day due to random variance. If you plot raw daily revenue, the chart looks like erratic static, making it physically impossible for the human eye to detect the macro-trend. A Rolling Average (e.g., `df.rolling(window=7).mean()`) mathematically slides a 7-day window across the data, calculating the Mean at every step. This acts as a Low-Pass Filter in signal processing, mathematically stripping away the daily high-frequency noise and exposing the true, underlying architectural trend line to the business stakeholders."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Data Analytics (Visualization) Completed.")
