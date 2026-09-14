"""
# ==============================================================================
# LABORATORY: TESTING AND DEBUGGING (PERFORMANCE BENCHMARKING)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A junior developer writes a Unit Test to verify that their algorithm sorts 
# an array correctly. The test passes. They deploy the algorithm to Production. 
# In Production, the array has 10,000,000 items instead of 10 items. Because 
# the algorithm has an O(N^2) Time Complexity (Bubble Sort), the server mathematically 
# locks up for 4 hours, and the database connection times out, crashing the system.
#
# A senior software engineer understands that logical correctness is not enough; 
# "Performance" is a mathematically testable feature. They use Pytest Benchmarks 
# to explicitly test the O(N) execution time of the algorithm. They configure the 
# CI/CD pipeline to mathematically crash if the function ever takes longer than 
# 0.500 seconds to execute, guaranteeing that O(N^2) regressions can never reach 
# the Production environment.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master automated Performance Testing (Benchmarking).
# - Execute statistical analysis of execution time (Mean, StdDev).
# - Architect CI/CD performance guardrails.
#
# ==============================================================================
"""

import time
import pytest
import math
from typing import List

# Gracefully handle pytest-benchmark dependency
try:
    from pytest_benchmark.fixture import BenchmarkFixture
    HAS_LIBS = True
except ImportError:
    HAS_LIBS = False

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE BUSINESS LOGIC (THE ALGORITHMS)
# ==============================================================================
class DataEngine:
    
    @staticmethod
    def slow_search(data: List[int], target: int) -> bool:
        """
        O(N) Linear Search.
        Mathematically checks every single element one by one.
        """
        for item in data:
            if item == target:
                return True
        return False
        
    @staticmethod
    def fast_search(data: set, target: int) -> bool:
        """
        O(1) Hash Table Lookup.
        Mathematically jumps directly to the memory address.
        """
        return target in data


# ==============================================================================
# 4. THE PYTEST BENCHMARK SUITE
# ==============================================================================
# In a real environment, you run this via `pytest --benchmark-only`
# The `benchmark` fixture is automatically injected by `pytest-benchmark`.

if HAS_LIBS:
    
    @pytest.fixture
    def massive_list() -> List[int]:
        """Generates 1,000,000 integers."""
        return list(range(1_000_000))
        
    @pytest.fixture
    def massive_set() -> set:
        """Generates 1,000,000 integers in a Hash Table."""
        return set(range(1_000_000))

    # --- THE TESTS ---

    def test_linear_search_performance(benchmark: BenchmarkFixture, massive_list: List[int]):
        """
        Tests the worst-case scenario: the target is at the absolute end of the list.
        The benchmark fixture mathematically runs this function hundreds of times 
        to calculate the statistical Mean and Standard Deviation of execution time!
        """
        target = 999_999
        
        # We command the benchmark to execute the slow_search function!
        result = benchmark(DataEngine.slow_search, massive_list, target)
        
        assert result is True


    def test_hash_search_performance(benchmark: BenchmarkFixture, massive_set: set):
        """
        Tests the Hash Table lookup.
        This should be mathematically thousands of times faster than the List.
        """
        target = 999_999
        
        result = benchmark(DataEngine.fast_search, massive_set, target)
        
        assert result is True


# ==============================================================================
# 5. MATHEMATICAL PROOF (THE SIMULATION)
# ==============================================================================
def demonstrate_benchmarking():
    section_header("Unit Testing: Automated Performance Benchmarking")
    
    if not HAS_LIBS:
        print("  [ERROR] pytest-benchmark not installed. Run `pip install pytest pytest-benchmark`.")
        return
        
    print("  [EXECUTION] Usually executed via: `pytest test_perf.py --benchmark-compare`")
    print("  We simulate the statistical output here...\n")
    
    # We execute a manual `timeit` equivalent to prove the math without breaking the lab
    import timeit
    
    massive_list = list(range(1_000_000))
    massive_set = set(range(1_000_000))
    target = 999_999
    
    print("  [RUNNING] Executing O(N) Linear Search (List)...")
    start = timeit.default_timer()
    DataEngine.slow_search(massive_list, target)
    linear_time = timeit.default_timer() - start
    
    print("  [RUNNING] Executing O(1) Hash Search (Set)...")
    start = timeit.default_timer()
    DataEngine.fast_search(massive_set, target)
    hash_time = timeit.default_timer() - start
    
    print("\n  [ARCHITECTURE PROOF]")
    print(f"  Linear Search Time: {linear_time:.6f} seconds")
    print(f"  Hash Search Time:   {hash_time:.6f} seconds")
    
    if hash_time > 0:
        speedup = linear_time / hash_time
        print(f"  -> [FLAWLESS] Hash Table was mathematically {speedup:,.0f}x faster!")


def run_all_labs():
    demonstrate_benchmarking()


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "Why do we use `pytest-benchmark` to run a function $100$ times instead of just using Python's `time.time()` once at the start and end of the function?"
   Senior Answer: "Statistical Significance and OS Jitter. If you measure a function exactly once, you are mathematically vulnerable to OS-level interruptions. If the Operating System decides to pause your Python thread to process a network packet or run the Garbage Collector during that exact microsecond, your execution time will artificially spike by $300\\%$. The test will fail due to 'OS Jitter', causing a flaky CI/CD pipeline. `pytest-benchmark` executes the function hundreds of times, mathematically drops the extreme outliers, and calculates the pure statistical Mean and Standard Deviation, guaranteeing a deterministic, repeatable performance metric that proves the algorithm's true Big-O complexity."

2. Interviewer: "How do you enforce Performance Constraints in a CI/CD pipeline? How do you mathematically stop a junior developer from deploying an O(N^2) algorithm?"
   Senior Answer: "Benchmark Regression Assertions. You configure `pytest-benchmark` (or similar tools) to explicitly assert against historical data or hard thresholds. For example, `assert benchmark.stats.stats.mean < 0.05` mathematically forces the pipeline to crash if the average execution time exceeds $50$ milliseconds. Alternatively, you can use the `--benchmark-compare` flag to compare the current Pull Request's execution time against the `main` branch's execution time. If the new code is statistically $10\\%$ slower than the existing production code, the CI/CD pipeline violently rejects the merge, ensuring Performance is treated as a mathematically verifiable feature."

3. Interviewer: "When benchmarking a highly optimized function, why do we sometimes see the execution time drop to exactly $0.000000$ seconds, making the benchmark fail?"
   Senior Answer: "Compiler Optimization and Dead Code Elimination. If you write a benchmark that calculates `result = 5 + 5` but you never actually *use* the `result` variable or `return` it, advanced Just-In-Time compilers (like PyPy or Numba) will execute an AST static analysis pass. They mathematically realize that the output of the calculation is completely ignored, and they will physically delete the math from the Machine Code to save CPU cycles (Dead Code Elimination). The benchmark executes in $0$ seconds because the code literally doesn't exist anymore. To benchmark correctly, you must force the CPU to evaluate the data by asserting the result or returning it to the global scope."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Testing and Debugging (Performance Benchmarking) Completed.")
