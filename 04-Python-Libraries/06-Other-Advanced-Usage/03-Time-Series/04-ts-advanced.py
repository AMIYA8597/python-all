"""
# ==============================================================================
# LABORATORY: ADVANCED TIME SERIES (TRANSFORMERS & ANOMALIES)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# LSTMs are incredibly powerful, but they have a fatal flaw: they process data 
# sequentially. If your sequence is 1,000 days long, the LSTM must take 1,000 
# sequential steps. You cannot parallelize it on a GPU. It is slow to train.
#
# In 2017, the Transformer architecture (the "T" in ChatGPT) destroyed the LSTM. 
# Transformers process the entire 1,000-day sequence simultaneously in parallel 
# using the "Self-Attention" mechanism. Recently, researchers have adapted 
# Transformers (like Informer or TimeGPT) to conquer Time Series forecasting, 
# achieving state-of-the-art results on massive multivariate datasets.
#
# Furthermore, forecasting isn't the only goal. What if you are monitoring 
# IoT sensors on a nuclear reactor? You don't just want to predict the temperature; 
# you want to instantly detect Mathematical Anomalies before the reactor melts down!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand Transformers in Time Series (Self-Attention vs Recurrence).
# - Execute Time Series Anomaly Detection (Isolation Forests).
# - Understand Multivariate Time Series (VAR models).
#
# ==============================================================================
"""

import numpy as np
import pandas as pd

# In a real environment: pip install scikit-learn
try:
    from sklearn.ensemble import IsolationForest
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. TRANSFORMERS FOR TIME SERIES
# ==============================================================================
def demonstrate_transformers_ts():
    section_header("Transformers vs LSTMs in Time Series")
    
    print("--- The LSTM Sequential Bottleneck ---")
    print("An LSTM reads Day 1 -> outputs a hidden state -> reads Day 2 -> etc.")
    print("Because Day 2 mathematically requires the output of Day 1, you CANNOT ")
    print("process Day 2 at the same time as Day 1. The GPU sits 99% idle.")
    
    print("\n--- The Transformer (Self-Attention) ---")
    print("A Transformer takes all 1,000 days and passes them into the GPU ")
    print("SIMULTANEOUSLY!")
    
    print("\nHow does it know the chronological order? Positional Encoding!")
    print("It mathematically injects a Sine/Cosine wave signature into the data ")
    print("so the Neural Network knows that Day 5 happened after Day 4.")
    
    print("\nThen, Self-Attention calculates a massive $1000 \times 1000$ matrix.")
    print("It mathematically calculates the exact correlation between Day 1000 ")
    print("and Day 1, bypassing the 998 days in between instantly! This allows ")
    print("for infinite-range memory and 100x faster GPU training times.")


# ==============================================================================
# 4. TIME SERIES ANOMALY DETECTION
# ==============================================================================
def demonstrate_anomaly_detection():
    section_header("Time Series Anomaly Detection (Isolation Forests)")
    
    if not HAS_SKLEARN:
        print("[WARNING] Scikit-Learn not installed.")
        return
        
    print("You are monitoring a server's CPU temperature. 99% of the time, it is ")
    print("stable. Suddenly, a crypto-miner malware runs, and the temp spikes.")
    print("How do you detect this automatically?\n")
    
    # 1. GENERATE SYNTHETIC DATA
    np.random.seed(42)
    # 500 normal temperature readings (Gaussian noise around 60 degrees)
    normal_temps = np.random.normal(60, 2, 500)
    
    # Inject 5 extreme anomalies (e.g. 95 degrees!)
    anomalies = np.array([95.1, 96.2, 94.8, 97.5, 99.9])
    
    # Concatenate and shuffle slightly (keeping it as a 2D array for Scikit-Learn)
    # Shape: (505, 1)
    dataset = np.concatenate([normal_temps, anomalies]).reshape(-1, 1)
    
    # 2. ISOLATION FOREST ARCHITECTURE
    print("--- Isolation Forest Math ---")
    print("Standard algorithms try to map the 'Normal' data. Isolation Forests ")
    print("do the opposite: they try to ISOLATE the anomalies.")
    print("The algorithm builds random Decision Trees. If a data point is 99 degrees, ")
    print("it only takes 1 or 2 random 'splits' in the tree to completely isolate it ")
    print("from the rest of the 60-degree data. Normal data requires 20+ splits to isolate.")
    print("Therefore, points with very short 'Path Lengths' are flagged as Anomalies!\n")
    
    # contamination=0.01 tells the model we expect roughly 1% of data to be bad.
    model = IsolationForest(contamination=0.01, random_state=42)
    
    print("Training Isolation Forest on 505 time steps...")
    model.fit(dataset)
    
    # Predict: Returns 1 for Normal, -1 for Anomaly
    predictions = model.predict(dataset)
    
    print("\nScanning for Anomalies...")
    for i, pred in enumerate(predictions):
        if pred == -1:
            print(f"[ALERT] Anomaly Detected at Index {i}! Temp: {dataset[i][0]:.1f}")
            
    print("\nThe model successfully found all 5 mathematically anomalous spikes ")
    print("without us ever writing a hardcoded threshold rule (like `if temp > 90`)!")


# ==============================================================================
# 5. MULTIVARIATE TIME SERIES (VAR MODELS)
# ==============================================================================
def demonstrate_multivariate():
    section_header("Multivariate Time Series (VAR Models)")
    
    print("ARIMA and Prophet are Univariate (They look at ONE variable: e.g. Sales).")
    
    print("\nBut what if Sales (Y) is heavily influenced by Marketing Spend (X1) ")
    print("and Weather (X2)?")
    
    print("\nIf you use Univariate modeling, you are throwing away massive amounts ")
    print("of predictive data. You must use Vector AutoRegression (VAR) or VARMAX.")
    
    print("\n--- The VAR Architecture ---")
    print("In a VAR model, ALL variables influence ALL OTHER variables dynamically.")
    print("Sales(t) depends on Sales(t-1) AND Marketing(t-1).")
    print("Marketing(t) depends on Marketing(t-1) AND Sales(t-1).")
    
    print("\nThis creates a massive system of linear equations. It is computationally ")
    print("heavy, but allows you to prove 'Granger Causality' (e.g., mathematically ")
    print("proving that an increase in Marketing explicitly *causes* a future ")
    print("increase in Sales).")


def run_all_labs():
    demonstrate_transformers_ts()
    demonstrate_anomaly_detection()
    demonstrate_multivariate()


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why did the Transformer architecture completely replace LSTMs for large-scale sequential data?
   Answer: Two reasons: Parallelization and Infinite Memory. An LSTM must process data sequentially ($T_1 \rightarrow T_2 \rightarrow T_3$). This sequential bottleneck mathematically prevents the GPU from utilizing its thousands of cores, making training painfully slow. The Transformer drops the recurrent loop entirely. It passes the entire sequence (all $1,000$ time steps) into the GPU simultaneously! Secondly, if an LSTM needs to connect $T_{1000}$ back to $T_1$, the signal must survive 1,000 sequential mathematical operations, often causing the gradient to vanish. The Transformer's Self-Attention mechanism calculates the exact dot-product correlation between $T_{1000}$ and $T_1$ in a single, direct $O(1)$ mathematical step!

2. How does an Isolation Forest mathematically identify an anomaly in a Time Series dataset?
   Answer: An Isolation Forest builds an ensemble of completely random Decision Trees. It selects a random feature and a random split value, over and over, until every single data point is isolated into its own leaf node. If a data point is normal (e.g., clustered densely with 500 other normal points), it requires a massive number of random splits to finally separate it from the cluster. If a data point is a severe anomaly (e.g., sitting far away in mathematical space), a single random split will likely isolate it immediately. The algorithm calculates the "Average Path Length" across all trees; data points with abnormally short path lengths are mathematically flagged as anomalies.

3. Explain the concept of "Granger Causality" in a Multivariate Time Series (VAR) model.
   Answer: "Correlation does not imply Causation." If Ice Cream sales and Shark Attacks both spike in July, they are highly correlated, but one does not cause the other. Granger Causality is a strict statistical hypothesis test used in Vector AutoRegression (VAR). It mathematically checks if the *past* values of Variable X (Marketing Spend) provide statistically significant information to predict the *future* values of Variable Y (Sales), beyond what the past values of Y already provided. If the p-value is significant, we say "Marketing Granger-causes Sales", proving a directional, predictive relationship rather than just a coincidental correlation.
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Advanced Time Series Completed.")
