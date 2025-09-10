#!/usr/bin/env python3
"""
Python Performance Optimization - Profiling and Analysis

This module provides comprehensive coverage of Python performance optimization
techniques, profiling tools, and analysis methods. It covers both theoretical
concepts and practical implementation strategies for optimizing Python code.

Topics covered:
- Built-in profiling tools (cProfile, profile, timeit)
- Memory profiling and analysis
- Performance bottleneck identification
- Code optimization techniques
- Data structure selection for performance
- Algorithmic optimization strategies

Author: Python DSA Master
Date: 2024
"""

import cProfile
import pstats
import timeit
import time
import tracemalloc
import sys
import gc
import functools
from typing import List, Dict, Any, Callable, Tuple
from collections import deque, defaultdict, Counter
from dataclasses import dataclass
import matplotlib.pyplot as plt
import numpy as np


@dataclass
class PerformanceMetrics:
    """Container for performance measurement results."""
    execution_time: float
    memory_usage: int
    cpu_time: float
    function_calls: int
    algorithm_name: str


class PerformanceProfiler:
    """
    Comprehensive performance profiling toolkit.
    
    This class provides various profiling methods to analyze
    code performance and identify optimization opportunities.
    """
    
    def __init__(self):
        self.results = {}
    
    def profile_function_time(self, func: Callable, *args, **kwargs) -> Dict[str, Any]:
        """
        Profile a function's execution time using multiple methods.
        
        Args:
            func: Function to profile
            *args: Function arguments
            **kwargs: Function keyword arguments
            
        Returns:
            Dictionary with timing results
        """
        results = {}
        
        # Method 1: time.perf_counter() for high precision
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        results['perf_counter'] = end_time - start_time
        
        # Method 2: timeit for accurate measurement
        timer = timeit.Timer(lambda: func(*args, **kwargs))
        # Run once to avoid overhead of multiple runs for slow functions
        results['timeit'] = timer.timeit(number=1)
        
        # Method 3: cProfile for detailed analysis
        profiler = cProfile.Profile()
        profiler.enable()
        func(*args, **kwargs)
        profiler.disable()
        
        # Extract cProfile statistics
        stats = pstats.Stats(profiler)
        stats.sort_stats('cumulative')
        results['cprofile_stats'] = stats
        results['total_time'] = stats.total_tt
        results['function_calls'] = stats.total_calls
        
        results['return_value'] = result
        return results
    
    def profile_memory_usage(self, func: Callable, *args, **kwargs) -> Dict[str, Any]:
        """
        Profile memory usage of a function using tracemalloc.
        
        Args:
            func: Function to profile
            *args: Function arguments
            **kwargs: Function keyword arguments
            
        Returns:
            Dictionary with memory usage results
        """
        # Start tracing memory allocations
        tracemalloc.start()
        
        # Get initial memory snapshot
        snapshot_before = tracemalloc.take_snapshot()
        
        # Execute function
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        
        # Get final memory snapshot
        snapshot_after = tracemalloc.take_snapshot()
        
        # Stop tracing
        tracemalloc.stop()
        
        # Compare snapshots to get memory difference
        top_stats = snapshot_after.compare_to(snapshot_before, 'lineno')
        
        # Calculate total memory difference
        total_memory = sum(stat.size_diff for stat in top_stats)
        
        return {
            'execution_time': end_time - start_time,
            'memory_diff': total_memory,
            'memory_peak': max(stat.size for stat in top_stats) if top_stats else 0,
            'allocations': len(top_stats),
            'top_allocations': top_stats[:10],  # Top 10 memory allocations
            'return_value': result
        }
    
    def benchmark_algorithms(self, algorithms: Dict[str, Callable], 
                           test_data: Any, iterations: int = 1000) -> Dict[str, PerformanceMetrics]:
        """
        Benchmark multiple algorithms against each other.
        
        Args:
            algorithms: Dictionary mapping algorithm names to functions
            test_data: Data to test algorithms with
            iterations: Number of iterations to run each algorithm
            
        Returns:
            Dictionary mapping algorithm names to performance metrics
        """
        results = {}
        
        for name, algorithm in algorithms.items():
            print(f"Benchmarking {name}...")
            
            # Time measurement
            timer = timeit.Timer(lambda: algorithm(test_data))
            execution_time = timer.timeit(number=iterations) / iterations
            
            # Memory measurement
            memory_info = self.profile_memory_usage(algorithm, test_data)
            
            # CPU profiling
            profiler = cProfile.Profile()
            profiler.enable()
            for _ in range(min(iterations, 100)):  # Limit to avoid excessive profiling overhead
                algorithm(test_data)
            profiler.disable()
            
            stats = pstats.Stats(profiler)
            stats.sort_stats('cumulative')
            
            results[name] = PerformanceMetrics(
                execution_time=execution_time,
                memory_usage=memory_info['memory_diff'],
                cpu_time=stats.total_tt,
                function_calls=stats.total_calls,
                algorithm_name=name
            )
        
        return results
    
    def generate_performance_report(self, results: Dict[str, PerformanceMetrics]) -> str:
        """
        Generate a comprehensive performance report.
        
        Args:
            results: Dictionary of performance metrics
            
        Returns:
            Formatted performance report
        """
        report = ["Performance Analysis Report", "=" * 40, ""]
        
        # Sort by execution time
        sorted_results = sorted(results.items(), key=lambda x: x[1].execution_time)
        
        report.append("Execution Time Ranking:")
        report.append("-" * 25)
        for i, (name, metrics) in enumerate(sorted_results, 1):
            report.append(f"{i}. {name:<20} {metrics.execution_time:.6f}s")
        
        report.append("")
        report.append("Detailed Metrics:")
        report.append("-" * 20)
        
        for name, metrics in sorted_results:
            report.extend([
                f"\n{name}:",
                f"  Execution Time: {metrics.execution_time:.6f}s",
                f"  Memory Usage:   {metrics.memory_usage:,} bytes",
                f"  CPU Time:       {metrics.cpu_time:.6f}s",
                f"  Function Calls: {metrics.function_calls:,}"
            ])
        
        # Performance ratios
        if len(sorted_results) > 1:
            fastest = sorted_results[0][1]
            report.extend(["", "Performance Ratios (vs fastest):", "-" * 35])
            for name, metrics in sorted_results[1:]:
                ratio = metrics.execution_time / fastest.execution_time
                report.append(f"{name:<20} {ratio:.2f}x slower")
        
        return "\n".join(report)


class DataStructureOptimizer:
    """
    Optimization techniques for different data structures and operations.
    """
    
    @staticmethod
    def compare_list_operations():
        """Compare different list operations for performance."""
        
        def list_append(n: int) -> List[int]:
            """Append to list."""
            result = []
            for i in range(n):
                result.append(i)
            return result
        
        def list_comprehension(n: int) -> List[int]:
            """Use list comprehension."""
            return [i for i in range(n)]
        
        def preallocate_list(n: int) -> List[int]:
            """Pre-allocate list with known size."""
            result = [0] * n
            for i in range(n):
                result[i] = i
            return result
        
        def use_array_module(n: int) -> List[int]:
            """Use array module for numeric data."""
            import array
            result = array.array('i', range(n))
            return list(result)  # Convert back for comparison
        
        algorithms = {
            'list_append': list_append,
            'list_comprehension': list_comprehension,
            'preallocate_list': preallocate_list,
            'array_module': use_array_module
        }
        
        profiler = PerformanceProfiler()
        return profiler.benchmark_algorithms(algorithms, 100000, iterations=100)
    
    @staticmethod
    def compare_search_operations():
        """Compare different search operations."""
        
        def linear_search(data: List[int], target: int = 50000) -> bool:
            """Linear search in list."""
            return target in data
        
        def binary_search(data: List[int], target: int = 50000) -> bool:
            """Binary search in sorted list."""
            import bisect
            sorted_data = sorted(data)
            pos = bisect.bisect_left(sorted_data, target)
            return pos < len(sorted_data) and sorted_data[pos] == target
        
        def set_lookup(data: List[int], target: int = 50000) -> bool:
            """Set lookup."""
            data_set = set(data)
            return target in data_set
        
        def dict_lookup(data: List[int], target: int = 50000) -> bool:
            """Dictionary lookup."""
            data_dict = {x: True for x in data}
            return target in data_dict
        
        # Generate test data
        test_data = list(range(100000))
        
        algorithms = {
            'linear_search': lambda data: linear_search(data),
            'binary_search': lambda data: binary_search(data),
            'set_lookup': lambda data: set_lookup(data),
            'dict_lookup': lambda data: dict_lookup(data)
        }
        
        profiler = PerformanceProfiler()
        return profiler.benchmark_algorithms(algorithms, test_data, iterations=100)


class AlgorithmicOptimization:
    """
    Demonstrate algorithmic optimization techniques.
    """
    
    @staticmethod
    def fibonacci_implementations():
        """Compare different Fibonacci implementations."""
        
        def fib_recursive(n: int) -> int:
            """Naive recursive implementation."""
            if n <= 1:
                return n
            return fib_recursive(n - 1) + fib_recursive(n - 2)
        
        def fib_memoized(n: int, memo: Dict[int, int] = None) -> int:
            """Memoized recursive implementation."""
            if memo is None:
                memo = {}
            if n in memo:
                return memo[n]
            if n <= 1:
                return n
            memo[n] = fib_memoized(n - 1, memo) + fib_memoized(n - 2, memo)
            return memo[n]
        
        def fib_iterative(n: int) -> int:
            """Iterative implementation."""
            if n <= 1:
                return n
            a, b = 0, 1
            for _ in range(2, n + 1):
                a, b = b, a + b
            return b
        
        @functools.lru_cache(maxsize=None)
        def fib_lru_cache(n: int) -> int:
            """LRU cache implementation."""
            if n <= 1:
                return n
            return fib_lru_cache(n - 1) + fib_lru_cache(n - 2)
        
        def fib_matrix(n: int) -> int:
            """Matrix exponentiation implementation."""
            if n <= 1:
                return n
            
            def matrix_multiply(a, b):
                return [[a[0][0]*b[0][0] + a[0][1]*b[1][0], a[0][0]*b[0][1] + a[0][1]*b[1][1]],
                        [a[1][0]*b[0][0] + a[1][1]*b[1][0], a[1][0]*b[0][1] + a[1][1]*b[1][1]]]
            
            def matrix_power(matrix, power):
                if power == 1:
                    return matrix
                if power % 2 == 0:
                    half = matrix_power(matrix, power // 2)
                    return matrix_multiply(half, half)
                else:
                    return matrix_multiply(matrix, matrix_power(matrix, power - 1))
            
            base_matrix = [[1, 1], [1, 0]]
            result_matrix = matrix_power(base_matrix, n)
            return result_matrix[0][1]
        
        # Test with smaller numbers for recursive version
        test_n = 30
        
        algorithms = {
            'recursive': lambda x: fib_recursive(test_n),
            'memoized': lambda x: fib_memoized(test_n),
            'iterative': lambda x: fib_iterative(test_n),
            'lru_cache': lambda x: fib_lru_cache(test_n),
            'matrix': lambda x: fib_matrix(test_n)
        }
        
        profiler = PerformanceProfiler()
        return profiler.benchmark_algorithms(algorithms, None, iterations=100)
    
    @staticmethod
    def sorting_algorithm_comparison():
        """Compare different sorting algorithms."""
        
        def bubble_sort(arr: List[int]) -> List[int]:
            """Bubble sort implementation."""
            arr = arr.copy()
            n = len(arr)
            for i in range(n):
                for j in range(0, n - i - 1):
                    if arr[j] > arr[j + 1]:
                        arr[j], arr[j + 1] = arr[j + 1], arr[j]
            return arr
        
        def quick_sort(arr: List[int]) -> List[int]:
            """Quick sort implementation."""
            if len(arr) <= 1:
                return arr
            pivot = arr[len(arr) // 2]
            left = [x for x in arr if x < pivot]
            middle = [x for x in arr if x == pivot]
            right = [x for x in arr if x > pivot]
            return quick_sort(left) + middle + quick_sort(right)
        
        def merge_sort(arr: List[int]) -> List[int]:
            """Merge sort implementation."""
            if len(arr) <= 1:
                return arr
            
            mid = len(arr) // 2
            left = merge_sort(arr[:mid])
            right = merge_sort(arr[mid:])
            
            result = []
            i = j = 0
            
            while i < len(left) and j < len(right):
                if left[i] <= right[j]:
                    result.append(left[i])
                    i += 1
                else:
                    result.append(right[j])
                    j += 1
            
            result.extend(left[i:])
            result.extend(right[j:])
            return result
        
        def heap_sort(arr: List[int]) -> List[int]:
            """Heap sort implementation."""
            import heapq
            arr = arr.copy()
            heapq.heapify(arr)
            return [heapq.heappop(arr) for _ in range(len(arr))]
        
        def builtin_sort(arr: List[int]) -> List[int]:
            """Python's built-in sort (Timsort)."""
            return sorted(arr)
        
        # Generate random test data
        import random
        test_data = [random.randint(1, 1000) for _ in range(1000)]
        
        algorithms = {
            'bubble_sort': bubble_sort,
            'quick_sort': quick_sort,
            'merge_sort': merge_sort,
            'heap_sort': heap_sort,
            'builtin_sort': builtin_sort
        }
        
        profiler = PerformanceProfiler()
        return profiler.benchmark_algorithms(algorithms, test_data, iterations=10)


class MemoryOptimization:
    """
    Memory optimization techniques and analysis.
    """
    
    @staticmethod
    def compare_data_containers():
        """Compare memory usage of different data containers."""
        
        def use_list(n: int) -> List[int]:
            """Use regular list."""
            return list(range(n))
        
        def use_tuple(n: int) -> Tuple[int, ...]:
            """Use tuple."""
            return tuple(range(n))
        
        def use_array(n: int):
            """Use array module."""
            import array
            return array.array('i', range(n))
        
        def use_numpy_array(n: int):
            """Use NumPy array."""
            try:
                import numpy as np
                return np.arange(n)
            except ImportError:
                return list(range(n))  # Fallback if NumPy not available
        
        def use_generator(n: int):
            """Use generator (memory efficient)."""
            return (i for i in range(n))
        
        algorithms = {
            'list': use_list,
            'tuple': use_tuple,
            'array': use_array,
            'numpy_array': use_numpy_array,
            'generator': use_generator
        }
        
        profiler = PerformanceProfiler()
        results = {}
        
        n = 100000
        for name, func in algorithms.items():
            memory_info = profiler.profile_memory_usage(func, n)
            results[name] = {
                'memory_usage': memory_info['memory_diff'],
                'execution_time': memory_info['execution_time']
            }
        
        return results
    
    @staticmethod
    def demonstrate_slots():
        """Demonstrate __slots__ for memory optimization."""
        
        class RegularClass:
            """Regular class without slots."""
            def __init__(self, x, y, z):
                self.x = x
                self.y = y
                self.z = z
        
        class SlottedClass:
            """Class with slots."""
            __slots__ = ['x', 'y', 'z']
            
            def __init__(self, x, y, z):
                self.x = x
                self.y = y
                self.z = z
        
        def create_regular_objects(n: int) -> List[RegularClass]:
            """Create regular objects."""
            return [RegularClass(i, i+1, i+2) for i in range(n)]
        
        def create_slotted_objects(n: int) -> List[SlottedClass]:
            """Create slotted objects."""
            return [SlottedClass(i, i+1, i+2) for i in range(n)]
        
        algorithms = {
            'regular_class': create_regular_objects,
            'slotted_class': create_slotted_objects
        }
        
        profiler = PerformanceProfiler()
        results = {}
        
        n = 10000
        for name, func in algorithms.items():
            memory_info = profiler.profile_memory_usage(func, n)
            results[name] = {
                'memory_usage': memory_info['memory_diff'],
                'execution_time': memory_info['execution_time']
            }
        
        return results


def demonstrate_profiling():
    """Demonstrate various profiling techniques."""
    print("Python Performance Profiling Demonstration")
    print("=" * 50)
    
    profiler = PerformanceProfiler()
    
    # Example 1: List operations comparison
    print("\n1. List Operations Performance Comparison")
    print("-" * 45)
    
    list_results = DataStructureOptimizer.compare_list_operations()
    print(profiler.generate_performance_report(list_results))
    
    # Example 2: Search operations comparison
    print("\n\n2. Search Operations Performance Comparison")
    print("-" * 47)
    
    search_results = DataStructureOptimizer.compare_search_operations()
    print(profiler.generate_performance_report(search_results))
    
    # Example 3: Fibonacci implementations
    print("\n\n3. Fibonacci Implementations Comparison")
    print("-" * 43)
    
    fib_results = AlgorithmicOptimization.fibonacci_implementations()
    print(profiler.generate_performance_report(fib_results))
    
    # Example 4: Sorting algorithms
    print("\n\n4. Sorting Algorithms Comparison")
    print("-" * 36)
    
    sort_results = AlgorithmicOptimization.sorting_algorithm_comparison()
    print(profiler.generate_performance_report(sort_results))


def demonstrate_memory_optimization():
    """Demonstrate memory optimization techniques."""
    print("\n\nMemory Optimization Demonstration")
    print("=" * 40)
    
    # Data container comparison
    print("\n1. Data Container Memory Usage")
    print("-" * 32)
    
    container_results = MemoryOptimization.compare_data_containers()
    for name, metrics in sorted(container_results.items(), key=lambda x: x[1]['memory_usage']):
        print(f"{name:<15} Memory: {metrics['memory_usage']:>10,} bytes, "
              f"Time: {metrics['execution_time']:.6f}s")
    
    # Slots demonstration
    print("\n2. __slots__ Memory Optimization")
    print("-" * 34)
    
    slots_results = MemoryOptimization.demonstrate_slots()
    for name, metrics in slots_results.items():
        print(f"{name:<15} Memory: {metrics['memory_usage']:>10,} bytes, "
              f"Time: {metrics['execution_time']:.6f}s")


def performance_tips():
    """Provide performance optimization tips."""
    print("\n\nPython Performance Optimization Tips")
    print("=" * 40)
    
    tips = [
        "\n🚀 ALGORITHMIC OPTIMIZATIONS:",
        "• Choose the right algorithm (O(n) vs O(n²) makes a huge difference)",
        "• Use appropriate data structures (dict for lookups, set for membership)",
        "• Cache expensive computations (functools.lru_cache)",
        "• Avoid nested loops when possible",
        
        "\n💾 MEMORY OPTIMIZATIONS:",
        "• Use __slots__ for classes with many instances",
        "• Use generators instead of lists when possible",
        "• Prefer tuples over lists for immutable data",
        "• Use array.array for numeric data",
        "• Profile memory usage to find leaks",
        
        "\n⚡ CODE OPTIMIZATIONS:",
        "• Use list comprehensions instead of loops",
        "• Move invariant calculations out of loops",
        "• Use local variables (faster lookup than global)",
        "• Avoid . attribute access in tight loops",
        "• Use built-in functions (they're optimized in C)",
        
        "\n🔧 PROFILING BEST PRACTICES:",
        "• Profile before optimizing (measure, don't guess)",
        "• Use cProfile for CPU profiling",
        "• Use tracemalloc for memory profiling",
        "• Test with realistic data sizes",
        "• Profile the bottlenecks, not the entire application",
        
        "\n📊 MEASUREMENT GUIDELINES:",
        "• Use timeit for micro-benchmarks",
        "• Run multiple iterations for stable results",
        "• Consider worst-case, average-case scenarios",
        "• Profile in production-like environments",
        "• Monitor performance over time"
    ]
    
    for tip in tips:
        print(tip)


def main():
    """Main function to demonstrate performance optimization."""
    print("Python DSA Master - Performance Optimization")
    print("=" * 50)
    
    try:
        demonstrate_profiling()
        demonstrate_memory_optimization()
        performance_tips()
        
    except KeyboardInterrupt:
        print("\nDemo interrupted by user")
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()
    
    print(f"\n{'='*50}")
    print("Performance optimization demonstration complete!")


if __name__ == "__main__":
    main()


# ============================================================================
# ADVANCED OPTIMIZATION TECHNIQUES
# ============================================================================

"""
🔧 ADVANCED OPTIMIZATION TECHNIQUES:

1. CYTHON INTEGRATION:
   • Compile Python to C for speed improvements
   • Use static typing with cdef
   • Optimize numerical computations

2. NUMBA JIT COMPILATION:
   • Just-in-time compilation for numerical code
   • @jit decorator for automatic optimization
   • GPU acceleration with CUDA

3. MULTIPROCESSING & THREADING:
   • CPU-bound tasks: multiprocessing
   • I/O-bound tasks: threading or asyncio
   • Concurrent.futures for easy parallel execution

4. NUMPY VECTORIZATION:
   • Replace Python loops with vectorized operations
   • Use broadcasting for array operations
   • Leverage BLAS/LAPACK optimized routines

5. MEMORY-MAPPED FILES:
   • Handle large datasets without loading into memory
   • Use mmap for file-like access to memory
   • Efficient for data processing pipelines

6. PROFILING TOOLS:
   • cProfile: Built-in statistical profiler
   • line_profiler: Line-by-line profiling
   • memory_profiler: Memory usage profiling
   • py-spy: Statistical profiler for production

7. OPTIMIZATION STRATEGIES:
   • Lazy evaluation and generators
   • Memoization and caching strategies
   • Precomputation and lookup tables
   • Algorithmic complexity reduction

📈 PERFORMANCE MONITORING:
   • Continuous integration performance tests
   • Performance regression detection
   • Production monitoring and alerting
   • Load testing and capacity planning
"""
