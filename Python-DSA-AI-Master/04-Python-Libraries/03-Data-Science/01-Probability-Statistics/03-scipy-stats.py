"""
Module: scipy.stats (Probability & Statistics in Python)
========================================================

Author: Python DSA Master
Target Audience: Intermediate to Advanced Data Scientists and Software Engineers

# Introduction to SciPy Stats
The `scipy.stats` module is the cornerstone of probability and statistics in Python. 
It contains a large number of probability distributions (both continuous and discrete), 
summary and frequency statistics, correlation functions, and statistical tests. 
It builds upon NumPy arrays to provide high-performance numerical routines.

# Mathematical Background
Let $X$ be a random variable.
1. **Probability Density Function (PDF)** - For continuous variables, $f(x)$ represents the density of probability at $x$.
   The probability of $X$ falling in interval $[a, b]$ is $\int_{a}^{b} f(x) dx$.
2. **Probability Mass Function (PMF)** - For discrete variables, $P(X = x)$ gives the probability that $X$ takes exact value $x$.
3. **Cumulative Distribution Function (CDF)** - $F(x) = P(X \le x)$. For continuous, it is $\int_{-\infty}^{x} f(t) dt$.
4. **Percent Point Function (PPF)** - The inverse of the CDF. Given a probability $p$, it returns $x$ such that $F(x) = p$.

# Computational Complexity
Many of the routines in `scipy.stats` are written in C/C++/Fortran and operate on 
NumPy arrays using SIMD (Single Instruction, Multiple Data) operations.
- Vectorized PDF/CDF evaluations on $N$ items take $O(N)$ time.
- Hypothesis tests (like T-test) typically take $O(N)$ time, where $N$ is the sample size.
Space complexity is generally $O(N)$ to store the outputs or intermediate contiguous arrays.

# Learning Objectives
1. Model random variables using discrete and continuous distributions.
2. Calculate summary statistics (moments, skewness, kurtosis).
3. Conduct hypothesis testing (t-tests, chi-square, normality tests).
4. Perform Monte Carlo simulations for probability approximations.
5. Understand the real-world application of A/B Testing.
"""

import math
import time
import typing
from typing import List, Dict, Any, Tuple, Optional

# Note: numpy and scipy are required for this module.
# In a real environment, they must be installed via `pip install numpy scipy`
try:
    import numpy as np
    import scipy.stats as stats
except ImportError:
    raise ImportError("This textbook lesson requires 'numpy' and 'scipy'. Please install them.")


# -----------------------------------------------------------------------------
# 1. Discrete Distributions (e.g., Binomial, Poisson)
# -----------------------------------------------------------------------------
def discrete_distributions_demo() -> Dict[str, Any]:
    """
    Demonstrates working with discrete random variables.
    
    The Binomial distribution models the number of successes in n independent 
    trials, each with success probability p.
    PMF: P(X = k) = C(n, k) * p^k * (1-p)^(n-k)
    
    The Poisson distribution models the number of events occurring in a fixed 
    interval of time/space, given a known constant mean rate lambda (mu).
    PMF: P(X = k) = (lambda^k * e^-lambda) / k!
    """
    print("--- 1. Discrete Distributions (Binomial & Poisson) ---")
    
    # --- Binomial Distribution ---
    n_trials = 10
    p_success = 0.5
    binom_dist = stats.binom(n_trials, p_success)
    
    # Calculate probability of getting exactly 5 successes (PMF)
    # PMF is used for discrete distributions instead of PDF.
    prob_5_successes = binom_dist.pmf(5)
    
    # Calculate probability of getting 5 or fewer successes (CDF)
    prob_leq_5 = binom_dist.cdf(5)
    
    # Generate random variates (RVS) - e.g., simulate 5 experiments
    simulated_binomial = binom_dist.rvs(size=5)
    
    print(f"Binomial(n={n_trials}, p={p_success}):")
    print(f"  P(X = 5) [PMF] = {prob_5_successes:.4f}")
    print(f"  P(X <= 5) [CDF] = {prob_leq_5:.4f}")
    print(f"  Simulated variates: {simulated_binomial}")
    
    # --- Poisson Distribution ---
    mu_rate = 3.0 # Average 3 events per interval
    poisson_dist = stats.poisson(mu_rate)
    
    # Probability of exactly 2 events
    prob_2_events = poisson_dist.pmf(2)
    
    print(f"\nPoisson(mu={mu_rate}):")
    print(f"  P(X = 2) [PMF] = {prob_2_events:.4f}")
    
    return {
        "binomial_pmf_5": prob_5_successes,
        "poisson_pmf_2": prob_2_events
    }


# -----------------------------------------------------------------------------
# 2. Continuous Distributions (e.g., Normal)
# -----------------------------------------------------------------------------
def continuous_distributions_demo() -> Dict[str, float]:
    """
    Demonstrates continuous distributions using the Normal (Gaussian) distribution.
    
    Normal Distribution PDF:
    f(x) = (1 / (sigma * sqrt(2 * pi))) * e^(-0.5 * ((x - mu)/sigma)^2)
    """
    print("\n--- 2. Continuous Distributions (Normal) ---")
    
    # Standard Normal Distribution (mu=0, sigma=1)
    norm_dist = stats.norm(loc=0, scale=1)
    
    # PDF at x=0 (the peak of the standard normal curve)
    pdf_0 = norm_dist.pdf(0)
    
    # CDF at x=0 (should be 0.5 since it's symmetric)
    cdf_0 = norm_dist.cdf(0)
    
    # PPF (Inverse CDF): What value of X gives us a cumulative probability of 0.95?
    # This is critical for finding confidence intervals and critical values in hypothesis testing.
    ppf_95 = norm_dist.ppf(0.95)
    
    # Area under curve between -1 and 1 standard deviations (Empirical Rule says ~68.27%)
    prob_within_1_sd = norm_dist.cdf(1) - norm_dist.cdf(-1)
    
    print(f"Normal(mu=0, sigma=1):")
    print(f"  f(0) [PDF] = {pdf_0:.4f}")
    print(f"  P(X <= 0) [CDF] = {cdf_0:.4f}")
    print(f"  Value for 95th percentile [PPF] = {ppf_95:.4f}")
    print(f"  P(-1 <= X <= 1) = {prob_within_1_sd * 100:.2f}%")
    
    return {
        "pdf_0": pdf_0,
        "cdf_0": cdf_0,
        "ppf_95": ppf_95,
        "prob_1_sd": prob_within_1_sd
    }


# -----------------------------------------------------------------------------
# 3. Descriptive Statistics
# -----------------------------------------------------------------------------
def descriptive_statistics(data: np.ndarray) -> Dict[str, float]:
    """
    Calculates various descriptive statistics.
    
    - Skewness: Measure of the asymmetry of the probability distribution.
      Positive skew = long tail on the right. Negative skew = long tail on the left.
    - Kurtosis: Measure of the "tailedness" of the distribution.
      High kurtosis = heavy tails (more outliers).
    
    Complexity: O(N) time to compute these statistics on a NumPy array of size N.
    """
    print("\n--- 3. Descriptive Statistics ---")
    
    desc = stats.describe(data)
    
    print(f"Data summary for array of size {len(data)}:")
    print(f"  Min, Max: {desc.minmax}")
    print(f"  Mean: {desc.mean:.4f}")
    print(f"  Variance: {desc.variance:.4f}")
    print(f"  Skewness: {desc.skewness:.4f} (measure of asymmetry)")
    print(f"  Kurtosis: {desc.kurtosis:.4f} (measure of tailedness relative to normal)")
    
    # We can also call these independently
    return {
        "mean": float(np.mean(data)),
        "variance": float(np.var(data, ddof=1)),
        "skewness": float(stats.skew(data)),
        "kurtosis": float(stats.kurtosis(data))
    }


# -----------------------------------------------------------------------------
# 4. Hypothesis Testing
# -----------------------------------------------------------------------------
def hypothesis_testing_demo() -> None:
    """
    Demonstrates basic statistical tests used to make inferences from data.
    
    1. 1-Sample T-Test: Checks if the population mean is equal to a specified value.
    2. 2-Sample Independent T-Test: Checks if two independent populations have the same mean.
    3. Normality Test (Shapiro-Wilk): Checks if data is drawn from a normal distribution.
    """
    print("\n--- 4. Hypothesis Testing ---")
    
    np.random.seed(42) # For reproducibility
    
    # 1. One-Sample T-Test
    # Generate data from a normal distribution with mean=5.5
    sample = np.random.normal(loc=5.5, scale=2.0, size=100)
    
    # Null Hypothesis (H0): Population mean is 5.0
    # Alternative Hypothesis (H1): Population mean is NOT 5.0
    t_stat, p_val = stats.ttest_1samp(sample, popmean=5.0)
    
    print("One-Sample T-Test (H0: mean == 5.0):")
    print(f"  T-statistic: {t_stat:.4f}, p-value: {p_val:.4e}")
    if p_val < 0.05:
        print("  Result: Reject H0. The mean is significantly different from 5.0.")
    else:
        print("  Result: Fail to reject H0.")
        
    # 2. Two-Sample T-Test
    sample_a = np.random.normal(loc=10.0, scale=1.5, size=50)
    sample_b = np.random.normal(loc=11.0, scale=1.5, size=50)
    
    # H0: Means of A and B are equal.
    t_stat_ind, p_val_ind = stats.ttest_ind(sample_a, sample_b)
    print("\nTwo-Sample Independent T-Test (H0: mean(A) == mean(B)):")
    print(f"  T-statistic: {t_stat_ind:.4f}, p-value: {p_val_ind:.4e}")
    
    # 3. Shapiro-Wilk Test for Normality
    # H0: Data is normally distributed
    w_stat, p_val_shap = stats.shapiro(sample_a)
    print("\nShapiro-Wilk Normality Test:")
    print(f"  W-statistic: {w_stat:.4f}, p-value: {p_val_shap:.4f}")
    if p_val_shap > 0.05:
        print("  Result: Data looks normal (Fail to reject H0).")


# -----------------------------------------------------------------------------
# 5. Performance and Edge Cases
# -----------------------------------------------------------------------------
def analyze_performance() -> None:
    """
    Analyzes performance bottlenecks and Vectorization vs Loops.
    """
    print("\n--- 5. Performance Analysis ---")
    size = 1_000_000
    print(f"Comparing PDF calculation for {size} normally distributed numbers...")
    
    data = np.random.normal(0, 1, size)
    norm_dist = stats.norm(0, 1)
    
    # 1. Vectorized (SciPy internal C/NumPy calls)
    start = time.time()
    _ = norm_dist.pdf(data)
    vec_time = time.time() - start
    
    # 2. Loop (Python native overhead)
    # Note: We take a small subset for the loop because it's terribly slow!
    small_size = 10_000
    small_data = data[:small_size]
    start = time.time()
    _ = [norm_dist.pdf(x) for x in small_data]
    loop_time = time.time() - start
    
    # Extrapolate loop time
    extrapolated_loop_time = loop_time * (size / small_size)
    
    print(f"  Vectorized execution time: {vec_time:.5f} sec")
    print(f"  Extrapolated Loop execution time: {extrapolated_loop_time:.5f} sec")
    print(f"  Speedup: ~{extrapolated_loop_time / vec_time:.1f}x faster using vectorized operations.")
    print("  Conclusion: NEVER use Python loops for statistical operations on large datasets. Always use the vectorized scipy methods directly on NumPy arrays.")


# -----------------------------------------------------------------------------
# 6. Real-World Application: A/B Testing Simulator
# -----------------------------------------------------------------------------
class ABTester:
    """
    A practical, real-world utility for evaluating A/B Tests (Conversion Rates)
    using the Two-Proportion Z-Test.
    """
    def __init__(self, visitors_a: int, conversions_a: int, visitors_b: int, conversions_b: int):
        self.n_a = visitors_a
        self.x_a = conversions_a
        self.n_b = visitors_b
        self.x_b = conversions_b
        
        self.p_a = self.x_a / self.n_a
        self.p_b = self.x_b / self.n_b

    def run_z_test(self, alpha: float = 0.05) -> Dict[str, Any]:
        """
        Runs a Two-Proportion Z-Test to see if Group B is significantly 
        different from Group A.
        """
        # Pooled proportion
        p_pool = (self.x_a + self.x_b) / (self.n_a + self.n_b)
        
        # Standard Error
        se = math.sqrt(p_pool * (1 - p_pool) * (1/self.n_a + 1/self.n_b))
        
        # Z-statistic
        z_stat = (self.p_b - self.p_a) / se
        
        # Two-tailed p-value using the Normal Survival Function (1 - CDF)
        # Using sf() is often more numerically stable and accurate than 1 - cdf()
        # For a two-tailed test, we multiply by 2
        p_value = stats.norm.sf(abs(z_stat)) * 2
        
        is_significant = p_value < alpha
        
        return {
            "conversion_rate_A": self.p_a,
            "conversion_rate_B": self.p_b,
            "relative_uplift": (self.p_b - self.p_a) / self.p_a,
            "z_statistic": z_stat,
            "p_value": p_value,
            "is_significant": is_significant
        }


def real_world_application() -> None:
    print("\n--- 6. Real-World Application: A/B Testing ---")
    print("Scenario: We changed the 'Buy Now' button from Blue (A) to Red (B).")
    
    tester = ABTester(visitors_a=10000, conversions_a=400, 
                      visitors_b=10200, conversions_b=510)
    
    results = tester.run_z_test()
    
    print(f"  Group A (Blue) Conversion Rate: {results['conversion_rate_A']*100:.2f}%")
    print(f"  Group B (Red) Conversion Rate: {results['conversion_rate_B']*100:.2f}%")
    print(f"  Uplift: {results['relative_uplift']*100:.2f}%")
    print(f"  P-value: {results['p_value']:.5f}")
    if results['is_significant']:
        print("  Conclusion: The change is STATISTICALLY SIGNIFICANT. Roll out the Red button!")
    else:
        print("  Conclusion: Not enough evidence to prove the Red button is better.")


# -----------------------------------------------------------------------------
# 7. Interview Challenge
# -----------------------------------------------------------------------------
def interview_challenge(sample_sizes: List[int], n_simulations: int = 1000) -> Dict[int, float]:
    """
    Challenge: Central Limit Theorem (CLT) Simulator
    
    Problem Statement:
    Write a function that simulates rolling a fair 6-sided die. 
    For different sample sizes 'n' (e.g., [2, 10, 30, 100]), roll 'n' dice 
    and calculate their mean. Repeat this 'n_simulations' times.
    Return a dictionary mapping 'n' to the empirical variance of the sample means.
    
    According to the CLT, the variance of the sample mean should be Var(X)/n.
    The variance of a single 6-sided die is ~2.9167.
    """
    print("\n--- 7. Interview Challenge: CLT Verification ---")
    results = {}
    
    # Population variance of a fair 6-sided die
    pop_var = np.var([1, 2, 3, 4, 5, 6], ddof=0)
    
    print(f"Theoretical Population Variance (1 die): {pop_var:.4f}")
    
    for n in sample_sizes:
        # Simulate rolling n dice, n_simulations times.
        # Shape: (n_simulations, n)
        rolls = np.random.randint(1, 7, size=(n_simulations, n))
        
        # Calculate the mean of each simulation
        sample_means = np.mean(rolls, axis=1)
        
        # Variance of the sample means
        empirical_variance = np.var(sample_means, ddof=1)
        theoretical_variance = pop_var / n
        
        results[n] = float(empirical_variance)
        print(f"  Sample size n={n}:")
        print(f"    Empirical Var(X_bar): {empirical_variance:.5f}")
        print(f"    Theoretical Var(X_bar) (Var/n): {theoretical_variance:.5f}")
        
    return results


# -----------------------------------------------------------------------------
# 8. Test Suite
# -----------------------------------------------------------------------------
def run_tests() -> None:
    """
    Test suite to validate the logic.
    """
    print("\n--- 8. Running Tests ---")
    
    # Test Descriptive Stats
    data = np.array([1, 2, 3, 4, 5])
    desc = descriptive_statistics(data)
    assert np.isclose(desc['mean'], 3.0), "Mean calculation failed."
    assert np.isclose(desc['variance'], 2.5), "Variance calculation failed."
    
    # Test A/B Tester
    t = ABTester(100, 10, 100, 20)
    res = t.run_z_test()
    assert np.isclose(res['conversion_rate_A'], 0.1), "AB Tester Rate A failed"
    assert np.isclose(res['conversion_rate_B'], 0.2), "AB Tester Rate B failed"
    
    print("All tests passed successfully!")


if __name__ == "__main__":
    print(f"{'='*60}")
    print(f"Exploring scipy.stats: Probability and Statistics")
    print(f"{'='*60}")
    
    # 1. Discrete Distributions
    discrete_distributions_demo()
    
    # 2. Continuous Distributions
    continuous_distributions_demo()
    
    # 3. Descriptive Stats
    sample_data = np.random.lognormal(mean=0, sigma=1, size=1000)
    descriptive_statistics(sample_data)
    
    # 4. Hypothesis Testing
    hypothesis_testing_demo()
    
    # 5. Performance
    analyze_performance()
    
    # 6. Real World App
    real_world_application()
    
    # 7. Interview Challenge
    interview_challenge([2, 5, 30, 100])
    
    # 8. Tests
    run_tests()
    
    print(f"\n{'='*60}")
    print(f"END OF MODULE")
    print(f"{'='*60}")
