"""
# ==============================================================================
# LABORATORY: STATISTICAL VISUALIZATION (SEABORN)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Matplotlib is incredibly powerful, but it is a "low-level" drawing API. 
# If you want to draw a complex statistical plot (like a Violin Plot showing the 
# Kernel Density Estimation of a population), it takes 30 lines of complex 
# Matplotlib math to manually draw the curves.
#
# Seaborn is built directly on top of Matplotlib, but it operates at a much 
# higher level. It integrates perfectly with Pandas DataFrames.
# You just hand Seaborn an entire Pandas DataFrame, tell it which column is X 
# and which is Y, and it automatically calculates the statistical densities, 
# draws the graphs, colors the categories, and generates beautiful legends in 
# exactly 1 line of code.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand how Seaborn wraps Matplotlib (`sns` on `ax`).
# - Generate Statistical Distributions (Boxplots and Violinplots).
# - Generate Correlation Matrices (Heatmaps).
# - Generate multi-dimensional scatter matrices (Pairplots).
#
# ==============================================================================
"""

import pandas as pd
import numpy as np

# In a real environment: pip install seaborn
try:
    import seaborn as sns
    import matplotlib.pyplot as plt
    HAS_SEABORN = True
except ImportError:
    HAS_SEABORN = False

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. DISTRIBUTIONS (BOXPLOTS & VIOLINPLOTS)
# ==============================================================================
def demonstrate_distributions():
    section_header("Statistical Distributions (Violin Plots)")
    
    if not HAS_SEABORN:
        print("[WARNING] Seaborn not installed.")
        return
        
    # Let's generate a Pandas DataFrame simulating waiter "Tips" at a restaurant.
    rng = np.random.default_rng(42)
    
    # Dinner tips are higher and more volatile than Lunch tips.
    dinner_tips = rng.normal(loc=15, scale=5, size=200)
    lunch_tips = rng.normal(loc=10, scale=3, size=200)
    
    df = pd.DataFrame({
        "Time": ["Dinner"] * 200 + ["Lunch"] * 200,
        "Tip_Amount": np.concatenate([dinner_tips, lunch_tips]),
        # Let's add a 3rd categorical variable: Gender of the payer
        "Gender": rng.choice(["Male", "Female"], size=400)
    })
    
    # 1. INSTANTIATE MATPLOTLIB CANVAS
    # Seaborn still uses Matplotlib under the hood! We create the Canvas first.
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # 2. ONE-LINE SEABORN MAGIC
    # A Violin Plot combines a Boxplot with a KDE (Kernel Density Estimation) curve!
    # `hue` automatically splits the data by Gender and colors it!
    # `split=True` draws Male on the left side of the violin and Female on the right!
    sns.violinplot(
        data=df, 
        x="Time", 
        y="Tip_Amount", 
        hue="Gender", 
        split=True, 
        ax=ax,
        palette="muted"
    )
    
    ax.set_title("Distribution of Tips by Time and Gender (KDE)")
    
    print("Generated a complex split-KDE Violin Plot in exactly 1 line of Seaborn code.")


# ==============================================================================
# 4. CORRELATION MATRICES (HEATMAPS)
# ==============================================================================
def demonstrate_heatmaps():
    section_header("Correlation Matrices (Heatmaps)")
    
    if not HAS_SEABORN: return
    
    # When you receive a dataset with 50 numeric columns, you need to instantly 
    # know which columns are mathematically correlated (e.g. Square Footage vs Price).
    
    # Let's simulate Housing Data
    rng = np.random.default_rng(1337)
    sqft = rng.uniform(1000, 5000, 100)
    bedrooms = np.round(sqft / 1000) + rng.integers(-1, 2, 100) # Correlated with sqft
    age = rng.uniform(0, 50, 100) # Random, no correlation
    price = (sqft * 200) - (age * 1000) + rng.normal(0, 10000, 100) # Price depends on sqft and age
    
    df = pd.DataFrame({
        "SqFt": sqft,
        "Bedrooms": bedrooms,
        "Age": age,
        "Price": price
    })
    
    # 1. CALCULATE PEARSON CORRELATION (Pandas)
    # Returns a 4x4 matrix of floats between -1.0 and 1.0
    corr_matrix = df.corr()
    
    # 2. VISUALIZE WITH SEABORN
    fig, ax = plt.subplots(figsize=(6, 5))
    
    # annot=True physically writes the numbers inside the colored boxes!
    # cmap="coolwarm" uses Blue for Negative correlation, Red for Positive.
    sns.heatmap(
        corr_matrix, 
        annot=True, 
        cmap="coolwarm", 
        vmin=-1, vmax=1, 
        ax=ax
    )
    
    ax.set_title("Housing Data Pearson Correlation Heatmap")
    print("Generated a Correlation Heatmap.")
    print("Notice the dark red square between SqFt and Price (High Positive Correlation).")
    print("Notice the blue square between Age and Price (Negative Correlation).")


# ==============================================================================
# 5. MULTI-DIMENSIONAL ANALYSIS (PAIRPLOT)
# ==============================================================================
def demonstrate_pairplot():
    section_header("N-Dimensional Scatter Matrices (Pairplot)")
    
    if not HAS_SEABORN: return
    
    print("Pairplot is the most powerful exploratory tool in Data Science.")
    print("If you have 4 numeric columns, it automatically generates a 4x4 grid.")
    print("The diagonals are histograms. The off-diagonals are scatter plots ")
    print("comparing every variable against every other variable simultaneously!")
    
    # Note: Pairplot creates its own Matplotlib Figure natively, so we don't 
    # pass an `ax` object to it.
    
    # sns.pairplot(df, hue="Species")
    print("\n(Pairplot configured in memory. Call plt.show() to render).")


def run_all_labs():
    demonstrate_distributions()
    demonstrate_heatmaps()
    demonstrate_pairplot()


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. What is the relationship between Matplotlib and Seaborn?
   Answer: Seaborn is a high-level statistical wrapper built directly on top of Matplotlib. Seaborn does not physically draw pixels on the screen; it calculates the complex statistical math (like KDE curves for violin plots), generates the aesthetic color palettes, and then secretly feeds standard Matplotlib plotting commands to the underlying `Axes` object. You still use Matplotlib (`fig, ax = plt.subplots()`) to manage the physical canvas and save the image.

2. What does a Correlation of -0.85 in a Heatmap mean?
   Answer: Pearson Correlation ranges from $-1.0$ to $+1.0$. A value of $0.0$ means the two variables are completely mathematically independent (random static). A value of $+1.0$ is perfect positive correlation (as $X$ goes up, $Y$ goes up). A value of $-0.85$ is a very strong Negative Correlation (as $X$ goes up, $Y$ goes down). In housing data, Age vs Price is often heavily negative (older houses are cheaper). In the Heatmap, this would be represented by a dark blue square.

3. Why is a Violin Plot superior to a Box Plot?
   Answer: A Box Plot only shows 5 discrete mathematical summary statistics (Min, 25th Percentile, Median, 75th Percentile, Max). It completely hides the actual physical shape of the data. If a dataset has two massive peaks (Bimodal), the Box Plot will just show a giant square block, making you think the data is uniformly distributed! A Violin Plot solves this by running a Kernel Density Estimation (KDE) across the data, drawing the exact curved, continuous probability density shape of the dataset, instantly revealing multiple peaks and valleys.
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Seaborn Statistical Visualization Completed.")
