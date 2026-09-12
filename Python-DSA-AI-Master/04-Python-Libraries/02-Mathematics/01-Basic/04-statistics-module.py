"""
Module: Python Statistics Module Mastery
Description: A textbook-grade, interactive, and highly comprehensive guide to Python's built-in `statistics` module.

================================================================================
TABLE OF CONTENTS
================================================================================
1. Introduction & Mathematical Foundations
2. Measures of Central Tendency (Averages)
3. Measures of Spread (Dispersion)
4. Statistical Relationships (Correlation, Covariance)
5. Advanced Statistical Classes (NormalDist)
6. Real-World Applications & Edge Cases
7. Performance Analysis & Big-O Considerations
8. Comprehensive Test Suite
================================================================================

1. INTRODUCTION & MATHEMATICAL FOUNDATIONS
--------------------------------------------------------------------------------
The `statistics` module, introduced in Python 3.4 (with significant additions in 
3.8, 3.9, and 3.10), provides functions for calculating mathematical statistics of 
numeric (Real-valued) data.

Unlike `numpy` or `pandas` which are designed for heavy matrix computations and 
vectorization, the `statistics` module focuses on built-in, native Python data 
types (`int`, `float`, `Decimal`, `Fraction`). It handles data robustly with a 
focus on mathematical correctness and precision over raw speed.

Key differences from other libraries:
- Operates on standard Python Iterables.
- Handles precision better natively for fractions and decimals.
- Returns values of the same type as the input where appropriate.

2. MEASURES OF CENTRAL TENDENCY
--------------------------------------------------------------------------------
Central tendency describes the "center" or typical value of a dataset.

- Mean (μ for population, x̄ for sample): Sum of all values divided by count.
  μ = (Σ x_i) / N
- FMean: Fast floating-point arithmetic mean.
- Geometric Mean: The nth root of the product of all n data values.
  GM = (Π x_i)^(1/n)
- Harmonic Mean: The reciprocal of the arithmetic mean of the reciprocals.
  HM = n / (Σ (1/x_i))
- Median: The middle value when sorted.
- Mode: The most frequent value.

3. MEASURES OF SPREAD
--------------------------------------------------------------------------------
Spread describes how much the data varies or deviates from the center.

- Variance (σ² for population, s² for sample): Average of squared deviations.
  σ² = Σ (x_i - μ)² / N
  s² = Σ (x_i - x̄)² / (n - 1)   <-- Bessel's correction
- Standard Deviation (σ, s): Square root of the variance.

4. STATISTICAL RELATIONSHIPS
--------------------------------------------------------------------------------
- Covariance: Measure of joint variability of two variables.
- Correlation (Pearson's r): Normalized measure of linear correlation.

5. ADVANCED CLASSES: NormalDist
--------------------------------------------------------------------------------
`NormalDist` (introduced in Python 3.8) is a tool for creating and manipulating 
normal distributions of a random variable.
"""

import math
import statistics
import time
import random
from decimal import Decimal
from fractions import Fraction
from typing import List, Tuple, Dict, Any, Union, Sequence, Optional


# ============================================================================
# Section 1: Central Tendency
# ============================================================================

class CentralTendency:
    """
    Explores measures of central location.
    
    Time Complexity (Big-O):
    - mean(): O(N) where N is the length of data.
    - fmean(): O(N) but implemented in C for floats, faster than mean().
    - geometric_mean(): O(N), heavily dependent on underlying math operations.
    - harmonic_mean(): O(N).
    - median(), median_low(), median_high(): O(N log N) because sorting is required.
    - mode(), multimode(): O(N) using hashing (Counter-like behavior).
    """
    
    @staticmethod
    def explore_means(data: Sequence[Union[int, float]]) -> Dict[str, float]:
        """
        Computes various types of means.
        
        Args:
            data: A sequence of numeric values.
            
        Returns:
            Dictionary containing arithmetic, geometric, and harmonic means.
        """
        print(f"\n--- Exploring Means ---")
        print(f"Data: {data}")
        
        # 1. Arithmetic Mean
        # Formula: Sum(x) / n
        # Highly sensitive to outliers.
        arithmetic_mean = statistics.mean(data)
        
        # 2. Fast Floating Point Mean (Python 3.8+)
        # Converts data to floats and computes mean. Faster but can lose exact precision
        # for Decimals/Fractions.
        fast_mean = statistics.fmean(data)
        
        # 3. Geometric Mean (Python 3.8+)
        # Formula: nth root of product of all values.
        # Useful for measuring growth rates or proportional changes.
        try:
            geometric_mean = statistics.geometric_mean(data)
        except statistics.StatisticsError as e:
            print(f"Geometric Mean Error (requires strictly positive data): {e}")
            geometric_mean = float('nan')
            
        # 4. Harmonic Mean (Python 3.6+)
        # Formula: n / Sum(1/x)
        # Useful for computing average rates, like average speed.
        harmonic_mean = statistics.harmonic_mean(data)
        
        results = {
            "mean": arithmetic_mean,
            "fmean": fast_mean,
            "geometric_mean": geometric_mean,
            "harmonic_mean": harmonic_mean
        }
        
        for k, v in results.items():
            print(f"{k.capitalize():<15}: {v:.4f}")
            
        return results

    @staticmethod
    def explore_medians_and_modes(data: Sequence[Union[int, float]]) -> None:
        """
        Demonstrates medians (robust to outliers) and modes.
        """
        print(f"\n--- Exploring Medians and Modes ---")
        print(f"Data: {data}")
        
        # Median: The middle value. If length is even, average of the two middle values.
        med = statistics.median(data)
        
        # Median Low: If length is even, returns the smaller of the two middle values.
        med_low = statistics.median_low(data)
        
        # Median High: If length is even, returns the larger of the two middle values.
        med_high = statistics.median_high(data)
        
        # Mode: Most single common value. Prior to Python 3.8, threw StatisticsError on ties.
        # Now returns the first most common value.
        mode_val = statistics.mode(data)
        
        # Multimode (Python 3.8+): Returns a list of the most common values.
        multimodes = statistics.multimode(data)
        
        print(f"Median        : {med}")
        print(f"Median Low    : {med_low}")
        print(f"Median High   : {med_high}")
        print(f"Mode          : {mode_val}")
        print(f"Multimode     : {multimodes}")


# ============================================================================
# Section 2: Measures of Spread
# ============================================================================

class MeasuresOfSpread:
    """
    Analyzes the dispersion or variability of data.
    
    Time Complexity:
    - variance(), pvariance(): O(N). Usually computed in two passes (one for mean, one for variance)
      or one-pass using Welford's algorithm for numerical stability.
    - stdev(), pstdev(): O(N).
    - quantiles(): O(N log N) because it involves sorting.
    """
    
    @staticmethod
    def explore_variance_stdev(data: Sequence[Union[int, float]]) -> None:
        """
        Variance and standard deviation measure how far data points are from the mean.
        We have population functions (when data is the entire set) and sample functions
        (when data is a sample of a larger population).
        """
        print(f"\n--- Exploring Variance and Standard Deviation ---")
        print(f"Data: {data}")
        
        # Sample Variance (s²)
        # Uses n-1 in the denominator (Bessel's correction) to provide an unbiased estimator.
        sample_var = statistics.variance(data)
        
        # Sample Standard Deviation (s)
        sample_std = statistics.stdev(data)
        
        # Population Variance (σ²)
        # Uses n in the denominator.
        pop_var = statistics.pvariance(data)
        
        # Population Standard Deviation (σ)
        pop_std = statistics.pstdev(data)
        
        print(f"Sample Variance (s²)       : {sample_var:.4f}")
        print(f"Sample Std Dev (s)         : {sample_std:.4f}")
        print(f"Population Variance (σ²)   : {pop_var:.4f}")
        print(f"Population Std Dev (σ)     : {pop_std:.4f}")

    @staticmethod
    def explore_quantiles(data: Sequence[Union[int, float]]) -> None:
        """
        Quantiles divide ordered data into continuous intervals with equal probabilities.
        """
        print(f"\n--- Exploring Quantiles ---")
        
        # Quartiles: Divides data into 4 intervals (returns 3 cut points).
        quartiles = statistics.quantiles(data, n=4)
        print(f"Quartiles (n=4) : {quartiles}")
        
        # Deciles: Divides data into 10 intervals (returns 9 cut points).
        deciles = statistics.quantiles(data, n=10)
        print(f"Deciles (n=10)  : {[round(d, 2) for d in deciles]}")


# ============================================================================
# Section 3: Statistical Relationships
# ============================================================================

class StatisticalRelationships:
    """
    Analyzes how two distinct variables relate to each other.
    Available from Python 3.10+.
    """
    
    @staticmethod
    def explore_covariance_correlation() -> None:
        """
        Covariance indicates the direction of the linear relationship.
        Correlation normalizes this to [-1, 1], indicating both direction and strength.
        """
        print(f"\n--- Exploring Covariance and Correlation ---")
        
        # x represents hours studied, y represents test scores
        x = [1, 2, 3, 4, 5, 6, 7]
        y = [40, 50, 55, 65, 70, 80, 85]
        
        # Using getattr to ensure backward compatibility if run on older Python < 3.10
        if hasattr(statistics, 'covariance') and hasattr(statistics, 'correlation'):
            cov = statistics.covariance(x, y)
            cor = statistics.correlation(x, y)
            
            print(f"Hours Studied (x): {x}")
            print(f"Test Scores (y)  : {y}")
            print(f"Covariance       : {cov:.4f} (Positive indicates they move together)")
            print(f"Correlation (r)  : {cor:.4f} (Close to 1 implies strong positive linear correlation)")
            
            # Linear Regression (Python 3.10+)
            # Returns slope and intercept of the line of best fit (y = slope * x + intercept)
            if hasattr(statistics, 'linear_regression'):
                slope, intercept = statistics.linear_regression(x, y)
                print(f"Linear Regression: Score = {slope:.2f} * Hours + {intercept:.2f}")
        else:
            print("Note: covariance, correlation, and linear_regression require Python 3.10+")


# ============================================================================
# Section 4: Normal Distribution Object (Python 3.8+)
# ============================================================================

class NormalDistributionAnalysis:
    """
    Deep dive into `statistics.NormalDist`.
    NormalDist allows for analytic computation of properties of normal distributions,
    rather than operating on empirical data arrays.
    """
    
    @staticmethod
    def explore_normal_dist() -> None:
        """
        Demonstrates creating, combining, and querying NormalDist objects.
        """
        print(f"\n--- Exploring NormalDist ---")
        if not hasattr(statistics, 'NormalDist'):
            print("NormalDist requires Python 3.8+")
            return
            
        # Create a standard normal distribution (mean = 0, std = 1)
        standard_normal = statistics.NormalDist(mu=0, sigma=1)
        
        # Create a distribution from sample data
        sample_data = [random.gauss(50, 15) for _ in range(1000)]
        emp_dist = statistics.NormalDist.from_samples(sample_data)
        
        print(f"Standard Normal Dist: {standard_normal}")
        print(f"Empirical Dist (mu~50, sig~15): {emp_dist}")
        
        # 1. PDF (Probability Density Function)
        # Represents the relative likelihood of a continuous random variable taking on a given value.
        val = 0
        pdf_val = standard_normal.pdf(val)
        print(f"\nPDF at x=0 for Standard Normal: {pdf_val:.4f} (Should be ~0.3989)")
        
        # 2. CDF (Cumulative Distribution Function)
        # Probability that a random variable X will take a value less than or equal to x.
        val_cdf = 1.96
        cdf_val = standard_normal.cdf(val_cdf)
        print(f"CDF at x=1.96 for Standard Normal: {cdf_val:.4f} (Should be ~0.975)")
        
        # 3. Inv CDF (Quantile)
        # The inverse of CDF. Given a probability, what is the value?
        prob = 0.975
        inv_cdf = standard_normal.inv_cdf(prob)
        print(f"Inverse CDF for p=0.975: {inv_cdf:.4f} (Should be ~1.96)")
        
        # 4. Math with Distributions!
        # When you add two independent normally distributed random variables,
        # the result is normal with mu = mu1 + mu2, var = var1 + var2.
        dist_a = statistics.NormalDist(mu=10, sigma=2)
        dist_b = statistics.NormalDist(mu=5, sigma=3)
        dist_c = dist_a + dist_b
        print(f"\nDist A: {dist_a}")
        print(f"Dist B: {dist_b}")
        print(f"Dist A + Dist B: {dist_c} (mu=15, sigma=sqrt(4+9) = 3.605)")


# ============================================================================
# Section 5: Real-World Applications & Edge Cases
# ============================================================================

class RealWorldApplications:
    
    @staticmethod
    def calculate_moving_average(data: List[float], window: int) -> List[float]:
        """
        Calculates the Simple Moving Average (SMA) of a time series.
        Used extensively in quantitative finance.
        
        Time Complexity: O(N * window). Can be optimized to O(N) using sliding window sum.
        Here we use statistics.mean() for educational clarity.
        """
        if window <= 0:
            raise ValueError("Window must be strictly positive.")
        if window > len(data):
            return []
            
        moving_averages = []
        for i in range(len(data) - window + 1):
            window_slice = data[i:i+window]
            moving_averages.append(statistics.mean(window_slice))
            
        return moving_averages

    @staticmethod
    def handle_extreme_precision() -> None:
        """
        Demonstrates the robust precision handling of `statistics` using Fractions and Decimals.
        Standard floats can introduce precision errors. The statistics module minimizes this.
        """
        print(f"\n--- Handling Extreme Precision ---")
        
        # Float issues
        float_data = [0.1, 0.1, 0.1]
        print(f"Float Sum of [0.1, 0.1, 0.1]: {sum(float_data)}")
        print(f"Float Mean: {statistics.mean(float_data)}")
        
        # Using Fractions for perfect precision
        fraction_data = [Fraction(1, 10), Fraction(1, 10), Fraction(1, 10)]
        print(f"Fraction Mean: {statistics.mean(fraction_data)}")
        
        # Using Decimals
        decimal_data = [Decimal('0.1'), Decimal('0.1'), Decimal('0.1')]
        print(f"Decimal Mean: {statistics.mean(decimal_data)}")


# ============================================================================
# Section 6: Comprehensive Tests
# ============================================================================

def run_tests() -> None:
    """
    A rigorous test suite ensuring the mathematical properties hold true.
    """
    print("\n================ TESTING SUITE ================\n")
    
    # Test 1: Mean correctness
    data = [1, 2, 3, 4, 5]
    assert statistics.mean(data) == 3, "Arithmetic mean failed!"
    
    # Test 2: Median correctness
    assert statistics.median([1, 3, 5]) == 3, "Odd median failed!"
    assert statistics.median([1, 2, 3, 4]) == 2.5, "Even median failed!"
    
    # Test 3: Mode correctness
    assert statistics.mode([1, 1, 2, 3]) == 1, "Mode failed!"
    assert statistics.multimode([1, 1, 2, 2, 3]) == [1, 2], "Multimode failed!"
    
    # Test 4: Variance correctness
    # For [1, 2, 3], mean = 2. Deviations: -1, 0, 1.
    # Squared: 1, 0, 1. Sum = 2.
    # Population variance = 2/3. Sample variance = 2/2 = 1.
    assert statistics.variance([1, 2, 3]) == 1.0, "Sample variance failed!"
    assert math.isclose(statistics.pvariance([1, 2, 3]), 2/3), "Population variance failed!"
    
    # Test 5: Moving Average application
    stocks = [10, 20, 30, 40, 50]
    sma_3 = RealWorldApplications.calculate_moving_average(stocks, window=3)
    assert sma_3 == [20.0, 30.0, 40.0], f"SMA failed: {sma_3}"
    
    print("ALL TESTS PASSED SUCCESSFULLY! ✅")


# ============================================================================
# Execution Driver
# ============================================================================

def main():
    print("========== PYTHON STATISTICS MODULE MASTERY ==========\n")
    
    # Sample Dataset: Heights of students in cm
    heights = [165, 170, 168, 175, 172, 160, 180, 165, 170, 175, 165, 190]
    
    # 1. Central Tendency
    CentralTendency.explore_means(heights)
    CentralTendency.explore_medians_and_modes(heights)
    
    # 2. Measures of Spread
    MeasuresOfSpread.explore_variance_stdev(heights)
    MeasuresOfSpread.explore_quantiles(heights)
    
    # 3. Relationships
    StatisticalRelationships.explore_covariance_correlation()
    
    # 4. Normal Distributions
    NormalDistributionAnalysis.explore_normal_dist()
    
    # 5. Precision Applications
    RealWorldApplications.handle_extreme_precision()
    
    # 6. Tests
    run_tests()
    
    print("\n========== LESSON COMPLETED ==========")


if __name__ == "__main__":
    main()
