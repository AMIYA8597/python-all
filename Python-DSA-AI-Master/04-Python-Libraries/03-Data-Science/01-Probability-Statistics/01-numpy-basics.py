"""
Module: 01-numpy-basics
Description: Comprehensive textbook-grade interactive lesson on NumPy Basics for Probability and Statistics.

===========================================================================
TEXTBOOK LESSON: NUMPY BASICS FOR DATA SCIENCE, PROBABILITY, & STATISTICS
===========================================================================

Learning Objectives:
1. Understand the mathematical and structural foundations of NumPy's `ndarray`.
2. Master array creation, slicing, broadcasting, and vectorization.
3. Apply statistical and mathematical functions provided by NumPy.
4. Perform random sampling and simulate probability distributions.
5. Understand the performance implications (Big-O analysis and memory mapping) of NumPy vs. pure Python.
6. Solve real-world data science problems using vectorized operations.

---------------------------------------------------------------------------
1. MATHEMATICAL BACKGROUND & BIG-O ANALYSIS
---------------------------------------------------------------------------
NumPy (Numerical Python) is the foundational library for scientific computing in Python.
Its core feature is the `ndarray` (N-dimensional array), a fast, flexible container for
large data sets in Python.

Unlike Python lists, which are arrays of pointers to scattered objects in memory,
NumPy arrays are stored in contiguous blocks of memory. This spatial locality
allows NumPy to leverage modern CPU features like SIMD (Single Instruction, Multiple Data)
and avoids the overhead of Python's dynamic typing during loops.

Big-O Performance Characteristics:
- Element-wise operations (addition, multiplication): O(N) in time, but highly optimized 
  in C. Constant factor is vastly smaller than Python lists.
- Reduction operations (sum, mean, max): O(N).
- Dot product (1D arrays of size N): O(N).
- Matrix Multiplication (N x M and M x P matrices): O(N * M * P) naive, but NumPy 
  uses highly optimized BLAS libraries (e.g., OpenBLAS, MKL) which are O(N^2.37) theoretically, 
  and highly parallelized in practice.
- Memory: O(N) space, but typically 1/4th to 1/8th the size of equivalent Python lists 
  since it stores raw C data types (e.g., int32, float64) rather than Python object overhead.

---------------------------------------------------------------------------
2. BROADCASTING
---------------------------------------------------------------------------
Broadcasting allows NumPy to perform operations on arrays of different shapes.
The smaller array is "broadcast" across the larger array so that they have compatible shapes.
Rules of Broadcasting:
1. If the arrays do not have the same rank, prepend the shape of the lower rank array with 1s.
2. The two arrays are said to be compatible in a dimension if they have the same size in the dimension, or if one of the arrays has size 1 in that dimension.
3. The arrays can be broadcast together if they are compatible in all dimensions.

"""

import time
import timeit
import math
import cProfile
from typing import List, Tuple, Any, Optional, Dict

import numpy as np

# =========================================================================
# SECTION 1: ARRAY CREATION AND PROPERTIES
# =========================================================================

def demonstrate_array_creation() -> None:
    """
    Demonstrates various methods for creating NumPy arrays and exploring their properties.
    """
    print("\n" + "="*50)
    print("SECTION 1: ARRAY CREATION AND PROPERTIES")
    print("="*50)
    
    # 1. From a Python list
    # The 'dtype' parameter is used to force a specific data type.
    arr_from_list = np.array([1, 2, 3, 4, 5], dtype=np.float32)
    print(f"Array from list: {arr_from_list}")
    print(f"Shape: {arr_from_list.shape}, Type: {arr_from_list.dtype}, Dimensions: {arr_from_list.ndim}")
    
    # 2. Built-in constructors
    zeros_arr = np.zeros((2, 3)) # 2x3 matrix of zeros
    ones_arr = np.ones((3, 2), dtype=np.int32) # 3x2 matrix of ones
    identity_matrix = np.eye(3) # 3x3 identity matrix
    
    print("\nZeros Array (2x3):")
    print(zeros_arr)
    
    print("\nOnes Array (3x2):")
    print(ones_arr)
    
    print("\nIdentity Matrix (3x3):")
    print(identity_matrix)
    
    # 3. Generating sequences
    # arange is similar to Python's range, but returns an array
    seq_arr = np.arange(0, 10, 2) # Start, Stop (exclusive), Step
    print(f"\nSequence array (arange): {seq_arr}")
    
    # linspace generates linearly spaced values
    lin_arr = np.linspace(0, 1, 5) # Start, Stop (inclusive), Number of elements
    print(f"Linearly spaced array: {lin_arr}")


# =========================================================================
# SECTION 2: VECTORIZED OPERATIONS AND BROADCASTING
# =========================================================================

def demonstrate_vectorization_and_broadcasting() -> None:
    """
    Shows how vectorized operations work and demonstrates the rules of broadcasting.
    """
    print("\n" + "="*50)
    print("SECTION 2: VECTORIZED OPERATIONS & BROADCASTING")
    print("="*50)
    
    # Vectorized operations replace slow Python loops with C loops
    arr = np.array([1, 2, 3, 4, 5])
    
    print(f"Original Array: {arr}")
    
    # Element-wise operations
    squared = arr ** 2
    print(f"Squared: {squared}")
    
    sin_arr = np.sin(arr)
    print(f"Sine: {sin_arr}")
    
    # Broadcasting
    # Adding a scalar to a 1D array (scalar is broadcast to shape of arr)
    added = arr + 10
    print(f"\nAdded 10 (Broadcasting scalar): {added}")
    
    # Broadcasting 1D array to 2D array
    matrix = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    vector = np.array([10, 20, 30])
    
    # matrix shape: (3, 3), vector shape: (3,) -> broadcast to (3, 3)
    result = matrix + vector
    
    print(f"\nMatrix (3x3):\n{matrix}")
    print(f"Vector (3,):\n{vector}")
    print(f"Matrix + Vector (Broadcasting 1D to 2D):\n{result}")


# =========================================================================
# SECTION 3: INDEXING, SLICING, AND BOOLEAN MASKING
# =========================================================================

def demonstrate_indexing_slicing() -> None:
    """
    Advanced indexing techniques including multidimensional slicing and boolean masking.
    """
    print("\n" + "="*50)
    print("SECTION 3: INDEXING, SLICING, & MASKING")
    print("="*50)
    
    # Create a 4x4 matrix
    matrix = np.arange(1, 17).reshape(4, 4)
    print(f"Matrix:\n{matrix}")
    
    # Standard slicing: array[row_start:row_end, col_start:col_end]
    sub_matrix = matrix[0:2, 1:3]
    print(f"\nSub-matrix (rows 0-1, cols 1-2):\n{sub_matrix}")
    
    # Modifying a slice modifies the original array (slices are views, not copies!)
    sub_matrix[0, 0] = 999
    print(f"\nMatrix after modifying the slice (Notice the change!):\n{matrix}")
    
    # Boolean masking (Filtering)
    # Reset matrix
    matrix = np.arange(1, 17).reshape(4, 4)
    
    # Find all even numbers
    mask = matrix % 2 == 0
    print(f"\nBoolean Mask (matrix % 2 == 0):\n{mask}")
    
    # Apply mask
    even_numbers = matrix[mask]
    print(f"\nExtracted Even Numbers: {even_numbers}")
    
    # Combined condition masking
    cond = (matrix > 5) & (matrix < 12)
    print(f"Numbers between 5 and 12: {matrix[cond]}")


# =========================================================================
# SECTION 4: PROBABILITY & STATISTICAL FUNCTIONS
# =========================================================================

def demonstrate_statistics() -> None:
    """
    Using NumPy for descriptive statistics and probability calculations.
    """
    print("\n" + "="*50)
    print("SECTION 4: DESCRIPTIVE STATISTICS")
    print("="*50)
    
    # Generate some data representing test scores
    np.random.seed(42) # For reproducibility
    scores = np.random.normal(loc=75, scale=10, size=1000) # mean=75, std=10
    
    # Basic Descriptive Statistics
    mean = np.mean(scores)
    median = np.median(scores)
    std_dev = np.std(scores)
    variance = np.var(scores)
    min_val, max_val = np.min(scores), np.max(scores)
    
    print(f"Data Points: 1000 Simulated Test Scores")
    print(f"Mean (μ):           {mean:.2f}")
    print(f"Median:             {median:.2f}")
    print(f"Standard Dev (σ):   {std_dev:.2f}")
    print(f"Variance (σ²):      {variance:.2f}")
    print(f"Min Score:          {min_val:.2f}")
    print(f"Max Score:          {max_val:.2f}")
    
    # Percentiles
    p25 = np.percentile(scores, 25)
    p75 = np.percentile(scores, 75)
    print(f"25th Percentile:    {p25:.2f}")
    print(f"75th Percentile:    {p75:.2f}")
    print(f"Interquartile Range:{p75 - p25:.2f}")


# =========================================================================
# SECTION 5: PERFORMANCE ANALYSIS (NUMPY VS PYTHON)
# =========================================================================

def analyze_performance() -> None:
    """
    Demonstrates the time and space complexity advantages of NumPy arrays
    over standard Python lists through benchmarking.
    """
    print("\n" + "="*50)
    print("SECTION 5: PERFORMANCE BENCHMARKING")
    print("="*50)
    
    size = 1_000_000
    print(f"Benchmarking operations on {size:,} elements...")
    
    # 1. Python Lists
    py_list = list(range(size))
    
    start_time = time.time()
    py_squared = [x ** 2 for x in py_list]
    py_time = time.time() - start_time
    print(f"Python List comprehension time: {py_time:.5f} seconds")
    
    # 2. NumPy Arrays
    np_arr = np.arange(size)
    
    start_time = time.time()
    np_squared = np_arr ** 2
    np_time = time.time() - start_time
    print(f"NumPy Vectorized time:          {np_time:.5f} seconds")
    
    # Calculate speedup
    speedup = py_time / np_time if np_time > 0 else 0
    print(f"--> NumPy is approximately {speedup:.2f}x faster for element-wise squaring.")


# =========================================================================
# SECTION 6: REAL-WORLD APPLICATION - CENTRAL LIMIT THEOREM
# =========================================================================

def simulate_central_limit_theorem(num_samples: int = 1000, sample_size: int = 30) -> None:
    """
    Real-world Application: Simulating the Central Limit Theorem (CLT).
    The CLT states that the distribution of sample means approximates a normal 
    distribution as the sample size becomes larger, regardless of the population's 
    underlying distribution.
    
    Args:
        num_samples: Number of random samples to draw.
        sample_size: The size of each random sample.
    """
    print("\n" + "="*50)
    print("SECTION 6: REAL-WORLD APP - CENTRAL LIMIT THEOREM")
    print("="*50)
    print(f"Simulating {num_samples} samples of size {sample_size} from a Uniform Distribution...")
    
    # Step 1: Define a non-normal population (Uniform distribution between 0 and 100)
    # We don't need to generate the whole population, just draw samples directly.
    
    # Step 2: Draw samples and calculate their means
    # We can do this extremely efficiently with NumPy by creating a matrix
    # of size (num_samples, sample_size) and taking the mean across the columns (axis=1)
    
    samples = np.random.uniform(low=0.0, high=100.0, size=(num_samples, sample_size))
    sample_means = np.mean(samples, axis=1)
    
    # Step 3: Analyze the distribution of sample means
    grand_mean = np.mean(sample_means)
    grand_std = np.std(sample_means)
    
    print("\nPopulation Details:")
    print("Distribution: Uniform[0, 100]")
    print("Theoretical Population Mean (μ): 50.0")
    print(f"Theoretical Population Std (σ):  {np.sqrt((100-0)**2 / 12):.2f}")
    
    print("\nSample Means Distribution Analysis:")
    print(f"Mean of Sample Means: {grand_mean:.2f} (Should be very close to 50.0)")
    print(f"Std Dev of Sample Means (Standard Error): {grand_std:.2f}")
    
    expected_stderr = np.sqrt((100-0)**2 / 12) / np.sqrt(sample_size)
    print(f"Expected Standard Error: {expected_stderr:.2f} (Theoretical σ / sqrt(n))")
    print("\nConclusion: The sample means follow a normal distribution centered around the population mean, demonstrating the CLT.")


# =========================================================================
# SECTION 7: INTERVIEW CHALLENGE
# =========================================================================

def interview_challenge_matrix_search(matrix: np.ndarray, target: int) -> bool:
    """
    Interview Challenge: Search in a 2D matrix.
    Given an MxN matrix where each row is sorted from left to right, 
    and the first integer of each row is greater than the last integer of the previous row.
    Return True if target exists, otherwise False.
    
    Time Complexity Requirement: O(log(M*N))
    Space Complexity: O(1)
    
    Args:
        matrix: 2D NumPy array.
        target: Value to search for.
    Returns:
        bool: True if target is in matrix.
    """
    if matrix.size == 0:
        return False
        
    m, n = matrix.shape
    left, right = 0, m * n - 1
    
    while left <= right:
        mid = (left + right) // 2
        
        # Map 1D mid index to 2D row, col coordinates
        mid_row = mid // n
        mid_col = mid % n
        
        mid_value = matrix[mid_row, mid_col]
        
        if mid_value == target:
            return True
        elif mid_value < target:
            left = mid + 1
        else:
            right = mid - 1
            
    return False

def test_interview_challenge() -> None:
    print("\n" + "="*50)
    print("SECTION 7: INTERVIEW CHALLENGE - 2D MATRIX SEARCH")
    print("="*50)
    
    matrix = np.array([
        [1, 3, 5, 7],
        [10, 11, 16, 20],
        [23, 30, 34, 60]
    ])
    
    print(f"Searching in Matrix:\n{matrix}")
    
    target1 = 3
    result1 = interview_challenge_matrix_search(matrix, target1)
    print(f"Target: {target1} -> Found: {result1} (Expected: True)")
    
    target2 = 13
    result2 = interview_challenge_matrix_search(matrix, target2)
    print(f"Target: {target2} -> Found: {result2} (Expected: False)")


# =========================================================================
# MAIN EXECUTION / TEST SUITE
# =========================================================================

if __name__ == "__main__":
    print("Starting NumPy Basics Masterclass...")
    
    try:
        demonstrate_array_creation()
        demonstrate_vectorization_and_broadcasting()
        demonstrate_indexing_slicing()
        demonstrate_statistics()
        analyze_performance()
        simulate_central_limit_theorem()
        test_interview_challenge()
        print("\nAll sections completed successfully!")
    except Exception as e:
        print(f"\nAn error occurred during execution: {e}")

