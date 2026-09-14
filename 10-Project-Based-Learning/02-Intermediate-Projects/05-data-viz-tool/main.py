"""
# ==============================================================================
# LABORATORY: PROJECT-BASED LEARNING (OOP DATA VISUALIZATION)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A junior data scientist needs to generate 50 different charts for a financial 
# report. They copy-paste the exact same 15 lines of `matplotlib.pyplot` code 
# 50 times, creating a massive 750-line procedural script. When the CEO asks 
# them to change the font color of all titles to "Blue", the junior scientist 
# mathematically panics and spends 3 hours manually altering 50 different blocks 
# of code.
#
# A senior data engineer builds an "OOP Visualization Engine". They mathematically 
# encapsulate the `matplotlib` Figures and Axes into strict Python Classes. 
# They define universal styling matrices (colors, fonts, grids) in a single 
# configuration dictionary. They generate all 50 charts using a 5-line `for` loop. 
# When the CEO asks for "Blue" titles, the engineer changes one string in the 
# configuration dictionary, re-runs the loop, and deploys the report in 4 seconds.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master Object-Oriented Abstraction of third-party libraries.
# - Execute programmatic generation of mathematical Data Visualizations.
# - Understand the architecture of the Matplotlib Figure/Axis DOM.
#
# ==============================================================================
"""

import math
import random

# Gracefully handle missing dependencies
try:
    import matplotlib.pyplot as plt
    import pandas as pd
    HAS_LIBS = True
except ImportError:
    HAS_LIBS = False

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE ARCHITECTURAL ENGINE (THE VISUALIZER)
# ==============================================================================
class ChartEngine:
    """
    An Object-Oriented Wrapper around Matplotlib.
    It mathematically enforces styling consistency and prevents procedural spaghetti code.
    """
    
    # We define a strict mathematical Theme Dictionary!
    # If the company rebrands, we only change colors here.
    THEME = {
        'background_color': '#f8f9fa',
        'grid_color': '#dee2e6',
        'title_color': '#212529',
        'primary_color': '#0d6efd',
        'secondary_color': '#dc3545',
        'font_family': 'sans-serif'
    }

    def __init__(self, title: str, x_label: str, y_label: str):
        # We ask Matplotlib to generate the absolute mathematical Canvas (Figure) 
        # and the specific Graph Area (Axis).
        self.fig, self.ax = plt.subplots(figsize=(10, 6))
        
        self.title = title
        self.x_label = x_label
        self.y_label = y_label
        
        self._apply_corporate_theme()

    def _apply_corporate_theme(self):
        """Mathematically enforces the strict corporate styling matrix."""
        # 1. Backgrounds
        self.fig.patch.set_facecolor(self.THEME['background_color'])
        self.ax.set_facecolor(self.THEME['background_color'])
        
        # 2. Mathematical Grids
        self.ax.grid(True, linestyle='--', alpha=0.7, color=self.THEME['grid_color'])
        
        # 3. Titles and Labels (Strict Font Control)
        self.ax.set_title(self.title, color=self.THEME['title_color'], fontsize=16, fontweight='bold', pad=20)
        self.ax.set_xlabel(self.x_label, fontsize=12, fontweight='500')
        self.ax.set_ylabel(self.y_label, fontsize=12, fontweight='500')
        
        # 4. Hide the ugly top and right borders (Spines)
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)

    def add_line_series(self, x_data: list, y_data: list, label: str, color_key: str = 'primary_color'):
        """Mathematically injects a Line Graph onto the Axis."""
        color = self.THEME.get(color_key, '#000000')
        # We plot the data, utilizing a mathematical Line Width and Marker!
        self.ax.plot(x_data, y_data, label=label, color=color, linewidth=2.5, marker='o', markersize=6)
        
    def add_bar_series(self, x_data: list, y_data: list, label: str, color_key: str = 'secondary_color'):
        """Mathematically injects a Bar Chart onto the Axis."""
        color = self.THEME.get(color_key, '#000000')
        self.ax.bar(x_data, y_data, label=label, color=color, alpha=0.8)

    def render(self, save_path: str = None):
        """Executes the final mathematical render pipeline."""
        # Activate the Legend based on the injected labels
        self.ax.legend(loc='upper left', frameon=True, facecolor='white', edgecolor=self.THEME['grid_color'])
        
        # Mathematically tighten the layout so labels don't get cut off!
        plt.tight_layout()
        
        if save_path:
            # We save it to the Hard Drive!
            self.fig.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"  [RENDER] Chart successfully exported to: {save_path} (300 DPI)")
        else:
            # We render it to the User's Screen! (Disabled in CLI labs to prevent freezing)
            print("  [RENDER] Chart Engine simulated successful screen rendering.")
            
        # We absolutely MUST close the Figure, or Matplotlib will suffer a RAM Leak!
        plt.close(self.fig)


# ==============================================================================
# 4. MATHEMATICAL PROOF (THE SIMULATION)
# ==============================================================================
def demonstrate_visualization():
    section_header("Project: OOP Data Visualization Engine")
    
    if not HAS_LIBS:
        print("  [ERROR] Matplotlib/Pandas not installed. Run `pip install matplotlib pandas`.")
        return
        
    print("  [PHASE 1: THE MATHEMATICAL DATA GENERATION]")
    # We generate a synthetic dataset of Monthly Revenue and Expenses!
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
    
    # Revenue climbs steadily, Expenses are chaotic
    revenue = [12000, 13500, 14200, 15800, 17100, 18500]
    expenses = [8000, 9500, 8200, 11000, 9100, 10500]
    
    # We wrap it in a Pandas DataFrame for architectural purity
    df = pd.DataFrame({
        'Month': months,
        'Revenue': revenue,
        'Expenses': expenses
    })
    
    print("    -> Pandas DataFrame successfully constructed.")
    
    print("\n  [PHASE 2: THE ARCHITECTURAL RENDERING]")
    print("    -> Instantiating Chart Engine...")
    
    # 1. We Boot the Engine!
    chart = ChartEngine(
        title="Q1/Q2 Financial Performance (Synthetic)",
        x_label="Fiscal Month",
        y_label="USD ($)"
    )
    
    # 2. We inject the Data!
    print("    -> Injecting Revenue Line Series (Primary Color)...")
    chart.add_line_series(df['Month'], df['Revenue'], label="Gross Revenue", color_key='primary_color')
    
    print("    -> Injecting Expenses Bar Series (Secondary Color)...")
    chart.add_bar_series(df['Month'], df['Expenses'], label="Operating Expenses", color_key='secondary_color')
    
    # 3. We execute the Render!
    output_filename = "financial_report_lab.png"
    chart.render(save_path=output_filename)


def run_all_labs():
    demonstrate_visualization()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "Why did we execute `plt.subplots()` to mathematically separate the `Figure` and the `Axis`? Why not just use `plt.plot()` like all the beginner tutorials do?"
   Senior Answer: "Object-Oriented Architectural Control. `plt.plot()` uses the 'State-Machine' interface (MATLAB style). It implicitly assumes you want to draw on whatever the 'currently active' canvas is. If you run a script generating $50$ charts simultaneously across $4$ CPU Threads, the State-Machine will violently collapse, plotting Revenue lines onto HR charts because the 'active' canvas is constantly shifting. By extracting explicit `Figure` (the physical window) and `Axis` (the mathematical graph region) objects, we achieve absolute Object-Oriented isolation. We can pass the `Axis` object to different functions and mathematically guarantee we are modifying the correct graph, enabling multi-threaded rendering without Race Conditions."

2. Interviewer: "In the `render()` method, why is it mathematically catastrophic to forget to call `plt.close(self.fig)` when running inside a web server?"
   Senior Answer: "RAM Exhaustion (Memory Leak). When you generate a Figure in Matplotlib, the C++ backend allocates a massive block of physical RAM (often $5$-$20$ MB) to hold the pixel matrix and vector data. If you serve a Chart via a Django or FastAPI web endpoint, and you forget `plt.close()`, Matplotlib will mathematically keep the Figure alive in RAM forever, assuming you still want to interact with it. If $1,000$ users request a chart, your server instantly bleeds $20$ GB of RAM, triggering an Out-Of-Memory (OOM) fatal crash. `plt.close()` mathematically commands the OS to destroy the C++ objects and free the memory."

3. Interviewer: "What is the architectural purpose of setting the DPI (Dots Per Inch) to 300 when executing `savefig()`?"
   Senior Answer: "Print Media Resolution Standardization. By default, Matplotlib saves images at $100$ DPI. On a standard $1920x1080$ monitor, this looks acceptable. However, if that chart is injected into a PDF and physically printed on a piece of paper, a $100$ DPI image will look violently pixelated and unprofessional. The global standard for high-quality print publishing (books, scientific journals) is $300$ DPI. By mathematically forcing $300$ DPI, we increase the pixel density of the output matrix by a factor of $9$ ($3\\times$ width, $3\\times$ height), mathematically guaranteeing crisp, vector-like quality in the final PNG file."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Capstone Project (Data Visualization) Completed.")
