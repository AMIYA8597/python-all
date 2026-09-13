"""
# ==============================================================================
# LABORATORY: THE STATISTICS MODULE (DATA ANALYSIS)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# While Data Scientists overwhelmingly use Pandas and SciPy for massive datasets, 
# loading a 50MB C-compiled library just to calculate the average of 10 numbers 
# is overkill and introduces unnecessary third-party dependencies.
#
# Python 3.4 introduced the built-in `statistics` module, and Python 3.8 heavily 
# upgraded it. It provides highly accurate, native implementations of mathematical 
# statistics directly in the Standard Library.
#
# Crucially, the `statistics` module properly handles exact math using `Decimal` 
# and `Fraction` objects, which third-party C libraries (like NumPy) often 
# corrupt by forcing them down into 64-bit hardware floats!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Calculate Measures of Central Tendency (Mean, Median, Mode).
# - Differentiate between Population and Sample Standard Deviations.
# - Leverage the modern `NormalDist` object for analytical probability.
#
# ==============================================================================
"""

import math
import statistics
from decimal import Decimal

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. MEASURES OF CENTRAL TENDENCY (AVERAGES)
# ==============================================================================
def demonstrate_central_tendency():
    section_header("Central Tendency (Mean, Median, Mode)")
    
    # An incredibly skewed dataset (e.g., salaries in a small company).
    # 9 employees make ~$50k. The CEO makes $10,000,000.
    data = [45_000, 48_000, 52_000, 50_000, 49_000, 45_000, 51_000, 47_000, 45_000, 10_000_000]
    
    print(f"Dataset (10 Salaries): {data}")
    
    # 1. MEAN (Arithmetic Average)
    # The sum divided by N. Highly susceptible to outliers!
    mean_val = statistics.mean(data)
    print(f"\nMean Salary  : ${mean_val:,.2f} (The CEO skewed the average massively!)")
    
    # 2. MEDIAN (The Middle Value)
    # Sorts the data and picks the exact middle. Immune to extreme outliers!
    median_val = statistics.median(data)
    print(f"Median Salary: ${median_val:,.2f} (A much more honest representation)")
    
    # If the list length is EVEN, `median` averages the two middle numbers.
    # If you strictly want an actual physical data point from the dataset:
    print(f"Median Low   : ${statistics.median_low(data):,.2f} (Picks the lower of the two middles)")
    print(f"Median High  : ${statistics.median_high(data):,.2f} (Picks the higher of the two middles)")
    
    # 3. MODE (Most Frequent Value)
    mode_val = statistics.mode(data)
    print(f"Mode Salary  : ${mode_val:,.2f} (The most common salary is $45k)")
    
    # Python 3.8+ introduced multimode for multimodal datasets (multiple winners!)
    multimodal_data = [1, 1, 2, 2, 3]
    print(f"\nMultimode of {multimodal_data}: {statistics.multimode(multimodal_data)}")


# ==============================================================================
# 4. MEASURES OF SPREAD (VARIANCE & STANDARD DEVIATION)
# ==============================================================================
def demonstrate_spread():
    section_header("Spread (Variance & Standard Deviation)")
    
    # Test scores for a highly consistent class vs a highly volatile class
    consistent_class = [85, 86, 84, 85, 87, 85]
    volatile_class = [50, 100, 60, 95, 40, 100]
    
    print(f"Consistent Class Mean: {statistics.mean(consistent_class)}")
    print(f"Volatile Class Mean  : {statistics.mean(volatile_class)}")
    print("Notice the Means are almost identical, but the classes are vastly different!")
    
    # 1. POPULATION VS SAMPLE
    # If your data contains EVERY SINGLE ENTITY IN EXISTENCE (e.g., all 6 students 
    # in the class), you use Population Standard Deviation (divided by N).
    # If your data is a SAMPLE of a larger population (e.g., 6 randomly chosen 
    # students in a school of 1000), you MUST use Sample Standard Deviation 
    # (divided by N-1) to mathematically correct for bias (Bessel's Correction).
    
    pop_std_cons = statistics.pstdev(consistent_class)
    pop_std_vol = statistics.pstdev(volatile_class)
    
    print(f"\nConsistent Class StdDev: {pop_std_cons:.2f} (Scores are tightly packed)")
    print(f"Volatile Class StdDev  : {pop_std_vol:.2f} (Scores are wildly scattered)")


# ==============================================================================
# 5. EXACT ARITHMETIC INTEGRATION
# ==============================================================================
def demonstrate_exact_math():
    section_header("Handling Exact Math (Decimals)")
    
    # The IEEE 754 Floating Point Bug returns!
    floats = [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1] # 10 items
    
    print("Calculating Mean using hardware Floats:")
    print(f"statistics.mean(floats) = {statistics.mean(floats):.17f} (Corrupted!)")
    
    # The `statistics` module natively supports the `decimal` module without 
    # forcing it down into float approximations!
    decimals = [Decimal("0.1") for _ in range(10)]
    print("\nCalculating Mean using Decimals:")
    print(f"statistics.mean(decimals) = {statistics.mean(decimals)} (Perfectly exact!)")


# ==============================================================================
# 6. ANALYTICAL PROBABILITY (NORMAL DISTRIBUTIONS)
# ==============================================================================
def demonstrate_normal_dist():
    section_header("Analytical Probability (NormalDist)")
    
    # Python 3.8 introduced the `NormalDist` object.
    # Instead of simulating raw data, you instantiate a mathematical Bell Curve!
    
    # Example: Human IQ is defined as a Bell Curve with Mean = 100, StdDev = 15.
    iq_dist = statistics.NormalDist(mu=100, sigma=15)
    
    # 1. PDF (Probability Density Function)
    # What is the relative likelihood of having an IQ of exactly 130?
    print(f"Likelihood of exact 130 IQ (PDF) : {iq_dist.pdf(130):.4f}")
    
    # 2. CDF (Cumulative Distribution Function)
    # What percentage of the population has an IQ of 130 OR LOWER?
    percentile = iq_dist.cdf(130)
    print(f"Percentile of 130 IQ (CDF)       : {percentile * 100:.2f}th Percentile")
    
    # 3. INV_CDF (Inverse CDF / Quantile)
    # What exact IQ score do I need to be in the Top 1% (99th Percentile)?
    top_1_percent = iq_dist.inv_cdf(0.99)
    print(f"IQ required for Top 1% (inv_CDF): {top_1_percent:.1f}")


def run_all_labs():
    demonstrate_central_tendency()
    demonstrate_spread()
    demonstrate_exact_math()
    demonstrate_normal_dist()


# ==============================================================================
# 7. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. When evaluating the "Average" salary of a country, why is Median vastly superior to Mean?
   Answer: The Mean (Arithmetic Average) sums all values and divides by $N$. It is incredibly vulnerable to extreme outliers. If 99 people make \$50k and 1 billionaire walks into the room, the "Average Mean Salary" spikes to \$10 Million! The Mean lies. The Median sorts the data and picks the exact middle entity. The billionaire only moves the middle index by exactly 1 position. The Median Salary would remain \$50k, perfectly reflecting the reality of the population.

2. What is Bessel's Correction, and why does Python have `pstdev` vs `stdev`?
   Answer: `pstdev` (Population Standard Deviation) mathematically divides by $N$. You ONLY use this if your dataset contains every single entity in existence (e.g., measuring the heights of every player currently in the NBA). 
   `stdev` (Sample Standard Deviation) divides by $N-1$ (Bessel's Correction). If you only measured the heights of 50 randomly selected human beings, your tiny sample almost certainly missed the absolute tallest and shortest people on Earth. Therefore, your Sample Variance mathematically UNDERESTIMATES the true variance of the entire human species. Dividing by a smaller number ($N-1$) artificially inflates the variance, perfectly correcting the mathematical bias!

3. How does `NormalDist.cdf(x)` differ from `NormalDist.pdf(x)`?
   Answer: 
   - PDF (Probability Density Function) returns the height of the Bell Curve at a specific, exact point `x`. It is the relative likelihood of picking that exact number.
   - CDF (Cumulative Distribution Function) returns the entire mathematical AREA under the Bell Curve from $-\infty$ all the way up to `x`. It represents the probability of a random value being less than or equal to `x` (i.e., your Percentile Rank).
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: The Statistics Module Completed.")
