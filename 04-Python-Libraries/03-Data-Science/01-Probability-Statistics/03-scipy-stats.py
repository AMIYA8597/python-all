"""
# ==============================================================================
# LABORATORY: STATISTICAL INFERENCE & HYPOTHESIS TESTING (SCIPY.STATS)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# If you run an A/B test on a website, and Version B gets a 2% higher click 
# rate than Version A, how do you know if Version B is ACTUALLY better? 
# Maybe Version B just randomly got luckier users that day.
#
# You cannot rely on human intuition to answer this. You must use Statistical 
# Hypothesis Testing to calculate the exact mathematical probability that the 
# 2% difference was purely due to random chance (The P-Value).
#
# `scipy.stats` is the ultimate library for Statistical Inference. It provides 
# over 100 continuous and discrete probability distributions, and the industry 
# standard algorithms for Hypothesis Testing (T-Tests, ANOVA, Chi-Square).
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the P-Value and Statistical Significance.
# - Execute a Two-Sample T-Test (A/B Testing).
# - Execute a One-Way ANOVA test (comparing 3+ groups).
# - Perform Kernel Density Estimation (KDE) to smooth histograms.
#
# ==============================================================================
"""

import numpy as np
from scipy import stats

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. HYPOTHESIS TESTING (THE INDEPENDENT T-TEST)
# ==============================================================================
def demonstrate_ttest():
    section_header("A/B Testing (Two-Sample T-Test)")
    
    # We run an A/B test for an e-commerce checkout page.
    # We record the amount of money spent per user.
    rng = np.random.default_rng(42)
    
    # Version A (Control): Mean spend $50, StdDev $10, 1000 users.
    group_A = rng.normal(loc=50.0, scale=10.0, size=1000)
    
    # Version B (Experimental): Mean spend $51.50, StdDev $10, 1000 users.
    # (Version B is physically generating more money!)
    group_B = rng.normal(loc=51.50, scale=10.0, size=1000)
    
    print(f"Group A Mean Spend: ${np.mean(group_A):.2f}")
    print(f"Group B Mean Spend: ${np.mean(group_B):.2f}")
    
    # Is the $1.50 difference statistically significant, or just random luck?
    # We perform an Independent Two-Sample T-Test.
    # H0 (Null Hypothesis): There is NO DIFFERENCE between the two groups.
    # H1 (Alternative Hypothesis): There IS A TRUE DIFFERENCE.
    
    t_stat, p_value = stats.ttest_ind(group_A, group_B)
    
    print(f"\nT-Statistic: {t_stat:.4f} (How far apart the means are, scaled by variance)")
    print(f"P-Value    : {p_value:.6f}")
    
    # Interpreting the P-Value (Alpha = 0.05)
    print("\nConclusion:")
    if p_value < 0.05:
        print("P-Value < 0.05. We REJECT the Null Hypothesis!")
        print("The difference is Statistically Significant. Version B is truly better!")
    else:
        print("P-Value >= 0.05. We FAIL TO REJECT the Null Hypothesis.")
        print("The difference could just be random noise. Do not launch Version B.")


# ==============================================================================
# 4. COMPARING MULTIPLE GROUPS (ANOVA)
# ==============================================================================
def demonstrate_anova():
    section_header("One-Way ANOVA (Analysis of Variance)")
    
    # What if we have 3 versions of the website? (A, B, and C)
    # You cannot run multiple T-Tests (A vs B, B vs C, A vs C) because doing so 
    # compounds your error rate (The Multiple Comparisons Problem).
    # You must use an ANOVA test.
    
    rng = np.random.default_rng(42)
    
    # We test 3 different Fertilizer brands on crop yield (kg)
    # Brand 1 and 2 are effectively identical. Brand 3 is actually better!
    brand_1 = rng.normal(loc=20.0, scale=5.0, size=50)
    brand_2 = rng.normal(loc=21.0, scale=5.0, size=50)
    brand_3 = rng.normal(loc=25.0, scale=5.0, size=50)
    
    # H0: All brands yield the exact same results.
    f_stat, p_value = stats.f_oneway(brand_1, brand_2, brand_3)
    
    print(f"F-Statistic: {f_stat:.4f}")
    print(f"P-Value    : {p_value:.6f}")
    
    if p_value < 0.05:
        print("P-Value < 0.05. We REJECT the Null Hypothesis!")
        print("At least ONE of the fertilizer brands is statistically different!")
    else:
        print("No statistical difference found between any brands.")


# ==============================================================================
# 5. KERNEL DENSITY ESTIMATION (KDE)
# ==============================================================================
def demonstrate_kde():
    section_header("Kernel Density Estimation (KDE)")
    
    # If you have a raw list of ages, you usually plot a Histogram.
    # But Histograms are blocky and highly sensitive to where you draw the "bins".
    # KDE mathematically smooths the raw data points into a continuous Probability 
    # Density Curve (PDF) by placing a microscopic Gaussian bell curve over every 
    # single data point and adding them all together!
    
    rng = np.random.default_rng(42)
    # Generate 1000 random ages, clustered heavily around 30.
    ages = rng.normal(loc=30, scale=5, size=1000)
    
    # 1. Fit the KDE Model
    kde_model = stats.gaussian_kde(ages)
    
    # 2. Evaluate the continuous curve!
    # What is the relative probability density at age 25, vs age 30, vs age 60?
    test_points = np.array([25, 30, 60])
    densities = kde_model.evaluate(test_points)
    
    print("Probability Densities extracted from raw data via KDE:")
    print(f"Density at Age 25: {densities[0]:.6f}")
    print(f"Density at Age 30: {densities[1]:.6f} (Peak of the curve!)")
    print(f"Density at Age 60: {densities[2]:.6f} (Effectively zero!)")


def run_all_labs():
    demonstrate_ttest()
    demonstrate_anova()
    demonstrate_kde()


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. What does a P-Value of $0.01$ mathematically mean in an A/B test?
   Answer: It means: "Assuming the Null Hypothesis is true (assuming that Version A and Version B are exactly identical in reality), there is only a $1\%$ mathematical probability of observing a difference this extreme purely due to random chance." Because a $1\%$ probability is so incredibly low, we conclude that our assumption (the Null Hypothesis) must be false. Therefore, the difference is real, and the result is Statistically Significant. (Standard threshold is $\alpha = 0.05$).

2. Why can't we just use three T-Tests instead of a One-Way ANOVA?
   Answer: The Multiple Comparisons Problem! Every time you run a statistical test with an alpha of $0.05$, there is a $5\%$ chance of getting a False Positive (detecting a difference that doesn't exist). If you run 3 separate T-Tests (A vs B, B vs C, A vs C), your total False Positive rate compounds mathematically ($1 - 0.95^3 \approx 14.2\%$). Your error rate balloons! The ANOVA test evaluates the variance of all 3 groups simultaneously in a single mathematical operation, locking the False Positive rate safely at $5\%$.

3. How does Kernel Density Estimation (KDE) work under the hood?
   Answer: A histogram groups continuous data into discrete, arbitrary bins, which can wildly change the shape of the data based on bin size. KDE completely ignores bins. Instead, it takes every single scalar data point in the array and drops a tiny mathematical Gaussian (Bell) Curve centered exactly on that point. It then sums the heights of all the overlapping bell curves together. Where data points are dense, the curves stack up to create massive peaks. The result is a perfectly smooth, mathematically continuous probability density function.
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Statistical Inference Completed.")
