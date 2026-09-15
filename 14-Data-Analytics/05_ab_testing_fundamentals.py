"""
# ==============================================================================
# LABORATORY: DATA ANALYTICS (A/B TESTING & STATISTICS)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A junior product manager launches a new red "Buy Now" button. The next day, 
# sales increase by 5%. They immediately declare the red button a success and 
# deploy it globally. The following week, sales plummet by 10%. They failed to 
# realize the 5% bump was purely random statistical variance.
#
# A senior data scientist understands Hypothesis Testing. They run a randomized 
# A/B Test for 14 days. They mathematically compute the Variance, Standard Error, 
# and the P-Value. The T-Test returns a P-Value of 0.23 (23%). Because 0.23 is 
# greater than the strict Alpha threshold of 0.05, the data scientist rejects 
# the finding, proving mathematically that the 5% bump was pure noise. They save 
# the company from a disastrous launch.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master Hypothesis Testing (Null vs Alternative Hypothesis).
# - Execute Statistical T-Tests using SciPy.
# - Architect proper experimental design (Sample Size & Alpha thresholds).
#
# ==============================================================================
"""

import pandas as pd
import numpy as np
from scipy import stats
import math

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE BUSINESS LOGIC (THE EXPERIMENT)
# ==============================================================================
class ABTestingSimulator:
    
    def __init__(self, sample_size: int = 5000):
        self.sample_size = sample_size
        self.df = None
        self._simulate_experiment()
        
    def _simulate_experiment(self):
        """
        Simulates an E-Commerce A/B Test.
        Group A (Control)   : Sees the Blue Button
        Group B (Treatment) : Sees the Red Button
        """
        print(f"  [INIT] Simulating A/B Test with {self.sample_size * 2:,} total users...")
        np.random.seed(42)
        
        # Group A: 12.0% Conversion Rate, $50 average order value
        conversions_A = np.random.binomial(n=1, p=0.120, size=self.sample_size)
        revenue_A = conversions_A * np.random.normal(loc=50.0, scale=10.0, size=self.sample_size)
        
        # Group B: 12.8% Conversion Rate, $51 average order value
        # Notice how close they are! Is the 0.8% difference real, or just noise?
        conversions_B = np.random.binomial(n=1, p=0.128, size=self.sample_size)
        revenue_B = conversions_B * np.random.normal(loc=51.0, scale=10.5, size=self.sample_size)
        
        # Combine into a Pandas DataFrame
        data_A = pd.DataFrame({'group': 'A (Control)', 'converted': conversions_A, 'revenue': revenue_A})
        data_B = pd.DataFrame({'group': 'B (Treatment)', 'converted': conversions_B, 'revenue': revenue_B})
        
        self.df = pd.concat([data_A, data_B], ignore_index=True)


    # --------------------------------------------------------------------------
    # THE ARCHITECTURAL PATTERN: STATISTICAL INFERENCE
    # --------------------------------------------------------------------------
    def execute_t_test(self):
        """
        Executes a Two-Sample Independent T-Test to calculate the P-Value.
        """
        print("\n  [ANALYSIS] Executing Hypothesis Testing...")
        
        # 1. State the Hypotheses
        print("  -> H0 (Null Hypothesis): The Red button has NO effect on Revenue.")
        print("  -> H1 (Alternative): The Red button mathematically increases Revenue.")
        
        # 2. Separate the Data Arrays
        rev_A = self.df[self.df['group'] == 'A (Control)']['revenue']
        rev_B = self.df[self.df['group'] == 'B (Treatment)']['revenue']
        
        mean_A = rev_A.mean()
        mean_B = rev_B.mean()
        
        print(f"\n  [OBSERVED METRICS]")
        print(f"  -> Group A (Control) Mean Revenue:   ${mean_A:.2f}")
        print(f"  -> Group B (Treatment) Mean Revenue: ${mean_B:.2f}")
        print(f"  -> Observed Difference (Lift):       +${(mean_B - mean_A):.2f}")
        
        # 3. Calculate the T-Statistic and P-Value!
        # We use SciPy's highly optimized C-functions.
        t_stat, p_value = stats.ttest_ind(rev_B, rev_A, equal_var=False)
        
        print(f"\n  [MATHEMATICAL PROOF]")
        print(f"  -> T-Statistic: {t_stat:.4f}")
        print(f"  -> P-Value:     {p_value:.4f}")
        
        # 4. The Decision (Alpha = 0.05)
        alpha = 0.05
        if p_value < alpha:
            print("  -> [DECISION] REJECT H0! The P-Value is < 0.05.")
            print("                The 0.8% bump is statistically significant. Deploy to Production!")
        else:
            print("  -> [DECISION] FAIL TO REJECT H0. The P-Value is >= 0.05.")
            print("                The bump is mathematically indistinguishable from random noise.")
            print("                Do NOT deploy. Keep the Blue button.")


# ==============================================================================
# 4. MATHEMATICAL PROOF (THE BENCHMARK)
# ==============================================================================
def demonstrate_ab_testing():
    section_header("Data Analytics: A/B Testing & Statistics")
    
    sim = ABTestingSimulator(sample_size=5000)
    sim.execute_t_test()
    
    print("\n  [ARCHITECTURE PROOF]")
    print("  By relying on the rigorous P-Value rather than raw averages, ")
    print("  the Data Scientist prevented the company from making a blind ")
    print("  business decision based on statistical illusion.")


def run_all_labs():
    demonstrate_ab_testing()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "In an A/B Test, define exactly what the P-Value represents mathematically."
   Senior Answer: "The Probability of Noise. The P-Value is NOT the probability that the new feature is 'better'. It is mathematically defined as the probability of observing our current test results (or more extreme results) *assuming that the Null Hypothesis is absolutely true*. If we get a P-Value of 0.23, it means there is a 23% chance that random variance alone could have caused the 5% lift we saw. Because 23% is far too high of a risk (our threshold is usually 5%, or Alpha=0.05), we refuse to conclude that the feature actually worked."

2. Interviewer: "What is a 'Type I Error', and how does it relate to the Alpha threshold?"
   Senior Answer: "A False Positive. A Type I Error occurs when the Null Hypothesis is actually true (the red button does absolutely nothing), but random luck causes Group B to buy more on that specific day, resulting in a P-Value < 0.05, causing us to erroneously deploy the feature. The Alpha threshold ($\alpha = 0.05$) is our mathematically defined risk tolerance. By setting $\alpha = 0.05$, we are explicitly accepting that $5\\%$ of all successful A/B tests we run will be False Positives. If we work in Medicine (e.g., testing a vaccine), we lower $\alpha$ to $0.01$ or $0.001$ because a False Positive is deadly."

3. Interviewer: "Why can't you just run an A/B test indefinitely and stop it the exact moment the P-Value drops below 0.05?"
   Senior Answer: "The Peeking Problem (p-hacking). A T-Test mathematically assumes a fixed sample size determined *before* the experiment begins. Because data fluctuates over time due to variance, the P-Value will constantly oscillate up and down. If you 'peek' at the data every day and stop the test the second it dips below $0.05$, you have mathematically guaranteed a False Positive (Type I Error) inflation. You must use a Power Analysis formula to calculate that you need exactly $14,000$ users to achieve $80\\%$ Statistical Power, run the test until you hit $14,000$, calculate the P-Value exactly once, and strictly abide by the result."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Data Analytics (A/B Testing) Completed.")
