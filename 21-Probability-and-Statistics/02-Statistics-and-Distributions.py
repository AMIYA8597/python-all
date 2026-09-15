"""
# ==============================================================================
# LABORATORY: PROBABILITY & STATISTICS (DISTRIBUTIONS)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A junior developer tries to detect credit card fraud by writing a rule: 
# `if transaction_amount > $5000: block()`. They block all legitimate business 
# purchases and miss the $4,999 fraudulent purchases. 
#
# A senior AI engineer understands "Statistical Distributions". They calculate 
# the Mean and Standard Deviation of a specific user's purchasing history. 
# They map the history onto a Gaussian (Normal) Distribution. If a new transaction 
# falls 3 Standard Deviations away from the mean (a Z-Score of 3.0), the 
# mathematics prove that there is a 99.7% chance this transaction is an anomaly. 
# The AI flags it as fraud probabilistically, regardless of the absolute dollar amount.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master Gaussian (Normal) Distributions.
# - Execute Variance and Standard Deviation calculations.
# - Architect Z-Score Anomaly Detection.
#
# ==============================================================================
"""

import numpy as np

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE BUSINESS LOGIC (STATISTICAL DISTRIBUTIONS)
# ==============================================================================
class StatisticalMathematics:
    
    @staticmethod
    def simulate_normal_distribution():
        """
        [SECURE] Mean, Variance, and Standard Deviation.
        The foundation of all statistical Machine Learning.
        """
        print("  [INIT] Calculating Statistical Parameters of a Dataset...")
        
        # A dataset of transaction amounts (in dollars)
        transactions = np.array([45.0, 50.0, 55.0, 48.0, 52.0, 49.0, 51.0, 47.0, 53.0])
        
        # 1. The Mean (Average)
        mean = np.mean(transactions)
        
        # 2. The Variance (Average squared distance from the mean)
        # We square it to prevent negative distances from canceling out positive ones.
        variance = np.var(transactions)
        
        # 3. The Standard Deviation (Square root of Variance)
        # Returns the metric back to the original unit (dollars).
        std_dev = np.std(transactions)
        
        print(f"  -> Dataset: {transactions}")
        print(f"  -> Mean (Mu):               ${mean:.2f}")
        print(f"  -> Variance (Sigma^2):       {variance:.2f}")
        print(f"  -> Standard Deviation (Sigma): ${std_dev:.2f}")
        
        print("\n  [MATHEMATICAL PROOF] On average, a transaction deviates from the ")
        print(f"  mean by exactly ${std_dev:.2f}. This is the 'Normal' behavior of the system.")

    @staticmethod
    def simulate_z_score_anomaly_detection():
        """
        [SECURE] Z-Score Anomaly Detection.
        Formula: Z = (X - Mean) / Standard_Deviation
        """
        print("\n  [INIT] Executing Z-Score Anomaly Detection...")
        
        # The established baseline of a user
        mean = 50.0
        std_dev = 3.16
        
        # 1. A normal incoming transaction
        t_normal = 55.0
        z_normal = (t_normal - mean) / std_dev
        
        # 2. A fraudulent incoming transaction
        t_fraud = 250.0
        z_fraud = (t_fraud - mean) / std_dev
        
        print(f"  -> Transaction 1: ${t_normal:.2f}  | Z-Score: {z_normal:.2f} (Within 2 Sigma)")
        print(f"  -> Transaction 2: ${t_fraud:.2f} | Z-Score: {z_fraud:.2f} (Extreme Outlier)")
        
        print("\n  [FLAWLESS] The Empirical Rule (68-95-99.7) states that 99.7% of all ")
        print("  legitimate data points must fall within a Z-Score of 3.0. Transaction 2 ")
        print("  has a Z-Score of 63.29. The mathematics prove it is an absolute anomaly.")


# ==============================================================================
# 4. MATHEMATICAL PROOF (THE BENCHMARK)
# ==============================================================================
def demonstrate_statistics():
    section_header("Probability & Statistics: Distributions & Z-Scores")
    
    math = StatisticalMathematics()
    math.simulate_normal_distribution()
    math.simulate_z_score_anomaly_detection()


def run_all_labs():
    demonstrate_statistics()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "What is the 'Empirical Rule' (68-95-99.7) in a Normal Distribution?"
   Senior Answer: "The Law of Standard Deviations. In any perfect Gaussian distribution, regardless of whether you are measuring human heights or stock prices, exactly $68\\%$ of all data points will fall within $1$ Standard Deviation of the Mean. Exactly $95\\%$ will fall within $2$ Standard Deviations. And exactly $99.7\\%$ will fall within $3$ Standard Deviations. In Machine Learning, if an input data point falls outside the $3$rd standard deviation, the network statistically treats it as an outlier or anomaly, as it represents less than $0.3\\%$ of observed reality."

2. Interviewer: "Why do we mathematically 'Normalize' or 'Standardize' input data before feeding it into a Neural Network?"
   Senior Answer: "Gradient Stability and Convergence. If Feature A (Age) ranges from $0-100$, and Feature B (Income) ranges from $0-1,000,000$, the Neural Network's Loss Landscape becomes mathematically warped into an extreme oval. Gradient Descent will violently oscillate across the Income axis and crawl across the Age axis, destroying the learning rate. By 'Standardizing' both features using their Z-Scores ($Z = \\frac{X - \\mu}{\\sigma}$), both features are mathematically crushed into a perfect Normal Distribution with a Mean of $0.0$ and a Standard Deviation of $1.0$. The Loss Landscape becomes a perfect geometric bowl, and Gradient Descent converges flawlessly."

3. Interviewer: "What is a 'Long-Tail' (Power Law) distribution, and why does it break standard Machine Learning models?"
   Senior Answer: "Extreme Asymmetry. A Normal distribution is perfectly symmetrical (a Bell Curve). A Power Law distribution is wildly asymmetrical (e.g., $1\\%$ of Twitter users generate $90\\%$ of the tweets). If you try to calculate the Mean and Standard Deviation of a Power Law dataset, the mathematics will fundamentally lie to you. The Mean will be drastically pulled up by the massive outliers, making it completely unrepresentative of the 'average' user. If you feed Long-Tail data into a standard Linear Regression or Neural Network without applying a mathematical transformation (like a Logarithmic Transform), the model will heavily overfit to the $1\\%$ of outliers and catastrophically fail on the $99\\%$ majority."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Probability (Distributions) Completed.")
