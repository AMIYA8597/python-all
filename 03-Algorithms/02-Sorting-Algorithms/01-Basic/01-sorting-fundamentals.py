#!/usr/bin/env python3
"""
Comprehensive Sorting Algorithms Implementation
==============================================

This module provides implementations of all major sorting algorithms with detailed
analysis, optimization techniques, and performance comparisons.

Sorting Algorithms Covered:
- Bubble Sort (O(n²) - educational)
- Selection Sort (O(n²) - simple)
- Insertion Sort (O(n²) - efficient for small arrays)
- Merge Sort (O(n log n) - stable, divide & conquer)
- Quick Sort (O(n log n) average - in-place)
- Heap Sort (O(n log n) - in-place)
- Counting Sort (O(n+k) - non-comparison)
- Radix Sort (O(d×n) - integer sorting)
- Bucket Sort (O(n) average - distributed data)

Topics Covered:
- Time and space complexity analysis
- Stability and adaptability
- In-place vs external sorting
- Comparison-based vs non-comparison sorting
- Best-case, average-case, and worst-case analysis
- Optimization techniques
- Hybrid approaches
- Real-world applications

Author: Python DSA Master Course
Version: 1.0
"""

import sys
import time
import random
import math
from typing import List, Tuple, Callable, Any, Optional
from enum import Enum
from dataclasses import dataclass


# ============================================================================
# SECTION 1: SIMPLE SORTING ALGORITHMS (O(n²))
# ============================================================================

def bubble_sort(arr: List[int], verbose: bool = False) -> List[int]:
    """
    Bubble Sort Implementation
    
    Algorithm: Repeatedly steps through the list, compares adjacent elements
    and swaps them if they are in the wrong order.
    
    Time Complexity:
    - Best case: O(n) - already sorted with early termination
    - Average case: O(n²)
    - Worst case: O(n²)
    
    Space Complexity: O(1)
    Stability: Stable
    In-place: Yes
    Adaptive: Yes (with optimization)
    """
    if not arr:
        return arr
    
    result = arr.copy()
    n = len(result)
    comparisons = 0
    swaps = 0
    
    for i in range(n):
        # Flag to detect if any swap occurred in this pass
        swapped = False
        
        # Last i elements are already in place
        for j in range(0, n - i - 1):
            comparisons += 1
            
            # Swap if current element is greater than next
            if result[j] > result[j + 1]:
                result[j], result[j + 1] = result[j + 1], result[j]
                swapped = True
                swaps += 1
                
                if verbose:
                    print(f"    Swap {result[j+1]} and {result[j]}: {result}")
        
        # If no swaps occurred, array is sorted
        if not swapped:
            break
    
    if verbose:
        print(f"  Bubble Sort: {comparisons} comparisons, {swaps} swaps")
    
    return result


def selection_sort(arr: List[int], verbose: bool = False) -> List[int]:
    """
    Selection Sort Implementation
    
    Algorithm: Finds the minimum element in unsorted portion and moves it
    to the beginning.
    
    Time Complexity:
    - Best case: O(n²)
    - Average case: O(n²)
    - Worst case: O(n²)
    
    Space Complexity: O(1)
    Stability: Not stable (but can be made stable)
    In-place: Yes
    Adaptive: No
    """
    if not arr:
        return arr
    
    result = arr.copy()
    n = len(result)
    comparisons = 0
    swaps = 0
    
    for i in range(n):
        # Find minimum element in remaining unsorted array
        min_idx = i
        
        for j in range(i + 1, n):
            comparisons += 1
            if result[j] < result[min_idx]:
                min_idx = j
        
        # Swap minimum element with first element
        if min_idx != i:
            result[i], result[min_idx] = result[min_idx], result[i]
            swaps += 1
            
            if verbose:
                print(f"    Swap {result[min_idx]} and {result[i]}: {result}")
    
    if verbose:
        print(f"  Selection Sort: {comparisons} comparisons, {swaps} swaps")
    
    return result


def insertion_sort(arr: List[int], verbose: bool = False) -> List[int]:
    """
    Insertion Sort Implementation
    
    Algorithm: Builds the sorted array one element at a time by inserting
    each element into its proper position.
    
    Time Complexity:
    - Best case: O(n) - already sorted
    - Average case: O(n²)
    - Worst case: O(n²)
    
    Space Complexity: O(1)
    Stability: Stable
    In-place: Yes
    Adaptive: Yes
    
    Note: Very efficient for small arrays and nearly sorted arrays
    """
    if not arr:
        return arr
    
    result = arr.copy()
    n = len(result)
    comparisons = 0
    shifts = 0
    
    for i in range(1, n):
        key = result[i]
        j = i - 1
        
        # Move elements greater than key one position ahead
        while j >= 0:
            comparisons += 1
            if result[j] > key:
                result[j + 1] = result[j]
                j -= 1
                shifts += 1
            else:
                break
        
        # Place key in its correct position
        result[j + 1] = key
        
        if verbose and shifts > 0:
            print(f"    Insert {key} at position {j + 1}: {result}")
    
    if verbose:
        print(f"  Insertion Sort: {comparisons} comparisons, {shifts} shifts")
    
    return result


# ============================================================================
# SECTION 2: EFFICIENT SORTING ALGORITHMS (O(n log n))
# ============================================================================

def merge_sort(arr: List[int], verbose: bool = False) -> List[int]:
    """
    Merge Sort Implementation
    
    Algorithm: Divide and conquer approach that recursively divides the array
    and merges sorted subarrays.
    
    Time Complexity:
    - Best case: O(n log n)
    - Average case: O(n log n)
    - Worst case: O(n log n)
    
    Space Complexity: O(n)
    Stability: Stable
    In-place: No
    Adaptive: No
    
    Note: Guaranteed O(n log n) performance makes it suitable for large datasets
    """
    if len(arr) <= 1:
        return arr
    
    def merge(left: List[int], right: List[int]) -> List[int]:
        """Merge two sorted arrays."""
        result = []
        i = j = 0
        
        # Merge elements in sorted order
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:  # <= ensures stability
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        
        # Add remaining elements
        result.extend(left[i:])
        result.extend(right[j:])
        
        if verbose:
            print(f"    Merge {left} + {right} = {result}")
        
        return result
    
    # Divide
    mid = len(arr) // 2
    left = merge_sort(arr[:mid], verbose)
    right = merge_sort(arr[mid:], verbose)
    
    # Conquer
    return merge(left, right)


def quick_sort(arr: List[int], verbose: bool = False) -> List[int]:
    """
    Quick Sort Implementation
    
    Algorithm: Divide and conquer approach that selects a pivot and partitions
    the array around it.
    
    Time Complexity:
    - Best case: O(n log n)
    - Average case: O(n log n)
    - Worst case: O(n²) - occurs with poor pivot selection
    
    Space Complexity: O(log n) - recursion stack
    Stability: Not stable (but can be made stable)
    In-place: Yes
    Adaptive: No
    
    Note: Often faster than merge sort in practice due to good cache locality
    """
    def quick_sort_helper(arr: List[int], low: int, high: int) -> None:
        """In-place quick sort helper."""
        if low < high:
            # Partition and get pivot index
            pivot_idx = partition(arr, low, high)
            
            if verbose:
                print(f"    Partitioned around {arr[pivot_idx]}: {arr[low:high+1]}")
            
            # Recursively sort elements before and after partition
            quick_sort_helper(arr, low, pivot_idx - 1)
            quick_sort_helper(arr, pivot_idx + 1, high)
    
    def partition(arr: List[int], low: int, high: int) -> int:
        """Lomuto partition scheme."""
        # Choose rightmost element as pivot
        pivot = arr[high]
        
        # Index of smaller element (indicates right position of pivot)
        i = low - 1
        
        for j in range(low, high):
            # If current element is smaller than or equal to pivot
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        
        # Place pivot in correct position
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1
    
    if not arr:
        return arr
    
    result = arr.copy()
    quick_sort_helper(result, 0, len(result) - 1)
    return result


def heap_sort(arr: List[int], verbose: bool = False) -> List[int]:
    """
    Heap Sort Implementation
    
    Algorithm: Uses a binary heap data structure to sort elements.
    First builds a max heap, then repeatedly extracts the maximum.
    
    Time Complexity:
    - Best case: O(n log n)
    - Average case: O(n log n)
    - Worst case: O(n log n)
    
    Space Complexity: O(1)
    Stability: Not stable
    In-place: Yes
    Adaptive: No
    
    Note: Guaranteed O(n log n) performance with O(1) space
    """
    def heapify(arr: List[int], n: int, i: int) -> None:
        """Heapify subtree rooted at index i."""
        largest = i  # Initialize largest as root
        left = 2 * i + 1
        right = 2 * i + 2
        
        # Check if left child exists and is greater than root
        if left < n and arr[left] > arr[largest]:
            largest = left
        
        # Check if right child exists and is greater than largest so far
        if right < n and arr[right] > arr[largest]:
            largest = right
        
        # If largest is not root, swap and recursively heapify
        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            heapify(arr, n, largest)
    
    if not arr:
        return arr
    
    result = arr.copy()
    n = len(result)
    
    # Build max heap
    for i in range(n // 2 - 1, -1, -1):
        heapify(result, n, i)
    
    if verbose:
        print(f"    Max heap built: {result}")
    
    # Extract elements from heap one by one
    for i in range(n - 1, 0, -1):
        # Move current root to end
        result[0], result[i] = result[i], result[0]
        
        if verbose:
            print(f"    Extracted {result[i]}: {result[:i]} | {result[i:]}")
        
        # Call heapify on reduced heap
        heapify(result, i, 0)
    
    return result


# ============================================================================
# SECTION 3: NON-COMPARISON SORTING ALGORITHMS
# ============================================================================

def counting_sort(arr: List[int], verbose: bool = False) -> List[int]:
    """
    Counting Sort Implementation
    
    Algorithm: Non-comparison sorting algorithm that counts occurrences
    of each distinct element.
    
    Time Complexity: O(n + k) where k is the range of input
    Space Complexity: O(k)
    Stability: Stable
    In-place: No
    Adaptive: No
    
    Note: Very efficient for integers with small range
    """
    if not arr:
        return arr
    
    # Find the range of input
    min_val = min(arr)
    max_val = max(arr)
    range_val = max_val - min_val + 1
    
    # Create count array
    count = [0] * range_val
    
    # Count occurrences of each element
    for num in arr:
        count[num - min_val] += 1
    
    if verbose:
        print(f"    Count array: {count}")
    
    # Modify count array to store actual positions
    for i in range(1, range_val):
        count[i] += count[i - 1]
    
    # Build output array
    result = [0] * len(arr)
    
    # Build output array from right to left to maintain stability
    for i in range(len(arr) - 1, -1, -1):
        result[count[arr[i] - min_val] - 1] = arr[i]
        count[arr[i] - min_val] -= 1
    
    return result


def radix_sort(arr: List[int], verbose: bool = False) -> List[int]:
    """
    Radix Sort Implementation
    
    Algorithm: Sorts integers by processing digits from least significant
    to most significant using counting sort as subroutine.
    
    Time Complexity: O(d × (n + k)) where d is number of digits
    Space Complexity: O(n + k)
    Stability: Stable
    In-place: No
    Adaptive: No
    
    Note: Efficient for integers, can be extended to strings
    """
    if not arr or min(arr) < 0:
        return arr  # This implementation handles only non-negative integers
    
    def counting_sort_for_radix(arr: List[int], exp: int) -> List[int]:
        """Counting sort for radix sort (sort by digit)."""
        n = len(arr)
        output = [0] * n
        count = [0] * 10  # For digits 0-9
        
        # Count occurrences of each digit
        for num in arr:
            digit = (num // exp) % 10
            count[digit] += 1
        
        # Modify count array to store actual positions
        for i in range(1, 10):
            count[i] += count[i - 1]
        
        # Build output array (from right to maintain stability)
        for i in range(n - 1, -1, -1):
            digit = (arr[i] // exp) % 10
            output[count[digit] - 1] = arr[i]
            count[digit] -= 1
        
        return output
    
    # Find maximum number to determine number of digits
    max_num = max(arr)
    
    # Sort by each digit
    result = arr.copy()
    exp = 1  # 10^0 = 1
    
    while max_num // exp > 0:
        if verbose:
            print(f"    Sorting by digit at position {exp}: {result}")
        
        result = counting_sort_for_radix(result, exp)
        exp *= 10
    
    return result


def bucket_sort(arr: List[float], num_buckets: int = None, verbose: bool = False) -> List[float]:
    """
    Bucket Sort Implementation
    
    Algorithm: Distributes elements into buckets, sorts individual buckets,
    then concatenates them.
    
    Time Complexity:
    - Best case: O(n + k)
    - Average case: O(n + k)
    - Worst case: O(n²)
    
    Space Complexity: O(n + k)
    Stability: Stable (if underlying sort is stable)
    In-place: No
    Adaptive: Yes
    
    Note: Works well for uniformly distributed data
    """
    if not arr:
        return arr
    
    n = len(arr)
    if num_buckets is None:
        num_buckets = n
    
    # Find minimum and maximum values
    min_val, max_val = min(arr), max(arr)
    
    # Handle edge case where all elements are equal
    if min_val == max_val:
        return arr.copy()
    
    # Create empty buckets
    buckets = [[] for _ in range(num_buckets)]
    
    # Distribute elements into buckets
    bucket_range = (max_val - min_val) / num_buckets
    
    for num in arr:
        # Calculate bucket index
        if num == max_val:
            bucket_idx = num_buckets - 1  # Handle edge case
        else:
            bucket_idx = int((num - min_val) / bucket_range)
        buckets[bucket_idx].append(num)
    
    if verbose:
        print(f"    Distributed into {num_buckets} buckets:")
        for i, bucket in enumerate(buckets):
            if bucket:
                print(f"      Bucket {i}: {bucket}")
    
    # Sort individual buckets and concatenate
    result = []
    for bucket in buckets:
        if bucket:
            # Use insertion sort for small buckets
            sorted_bucket = sorted(bucket)  # Could use any stable sort
            result.extend(sorted_bucket)
    
    return result


# ============================================================================
# SECTION 4: HYBRID AND ADVANCED SORTING ALGORITHMS
# ============================================================================

def timsort_simplified(arr: List[int], verbose: bool = False) -> List[int]:
    """
    Simplified TimSort Implementation
    
    TimSort is Python's built-in sorting algorithm. This is a simplified version
    that demonstrates the key concepts:
    - Uses insertion sort for small arrays
    - Uses merge sort for larger arrays
    - Optimized for partially sorted data
    
    Time Complexity:
    - Best case: O(n)
    - Average case: O(n log n)
    - Worst case: O(n log n)
    
    Space Complexity: O(n)
    Stability: Stable
    Adaptive: Yes
    """
    MIN_MERGE = 32
    
    def insertion_sort_for_timsort(arr: List[int], left: int, right: int) -> None:
        """Insertion sort for small arrays."""
        for i in range(left + 1, right + 1):
            key = arr[i]
            j = i - 1
            while j >= left and arr[j] > key:
                arr[j + 1] = arr[j]
                j -= 1
            arr[j + 1] = key
    
    def merge_for_timsort(arr: List[int], left: int, mid: int, right: int) -> None:
        """Merge function for TimSort."""
        left_part = arr[left:mid + 1]
        right_part = arr[mid + 1:right + 1]
        
        i = j = 0
        k = left
        
        while i < len(left_part) and j < len(right_part):
            if left_part[i] <= right_part[j]:
                arr[k] = left_part[i]
                i += 1
            else:
                arr[k] = right_part[j]
                j += 1
            k += 1
        
        while i < len(left_part):
            arr[k] = left_part[i]
            i += 1
            k += 1
        
        while j < len(right_part):
            arr[k] = right_part[j]
            j += 1
            k += 1
    
    if not arr:
        return arr
    
    result = arr.copy()
    n = len(result)
    
    # Sort individual subarrays of size MIN_MERGE using insertion sort
    for start in range(0, n, MIN_MERGE):
        end = min(start + MIN_MERGE - 1, n - 1)
        insertion_sort_for_timsort(result, start, end)
    
    if verbose:
        print(f"    After insertion sort on chunks: {result}")
    
    # Start merging subarrays
    size = MIN_MERGE
    while size < n:
        for start in range(0, n, size * 2):
            mid = start + size - 1
            end = min(start + size * 2 - 1, n - 1)
            
            if mid < end:
                merge_for_timsort(result, start, mid, end)
        
        if verbose:
            print(f"    After merging size {size}: {result}")
        
        size *= 2
    
    return result


def intro_sort(arr: List[int], verbose: bool = False) -> List[int]:
    """
    Introspective Sort (Introsort) Implementation
    
    Hybrid sorting algorithm that combines quicksort, heapsort, and insertion sort:
    - Begins with quicksort
    - Switches to heapsort when recursion depth exceeds a limit
    - Uses insertion sort for small arrays
    
    Time Complexity:
    - Best case: O(n log n)
    - Average case: O(n log n)
    - Worst case: O(n log n) - guaranteed by heapsort fallback
    
    Space Complexity: O(log n)
    Stability: Not stable
    In-place: Yes
    Adaptive: Yes
    
    Note: Used by C++ std::sort
    """
    if not arr:
        return arr
    
    result = arr.copy()
    max_depth = 2 * int(math.log2(len(result)))
    
    def introsort_helper(arr: List[int], low: int, high: int, depth: int) -> None:
        """Introsort helper function."""
        size = high - low + 1
        
        # Use insertion sort for small arrays
        if size < 16:
            insertion_sort_range(arr, low, high)
            return
        
        # Use heapsort if maximum depth exceeded
        if depth == 0:
            heapsort_range(arr, low, high)
            return
        
        # Use quicksort
        pivot = partition_for_intro(arr, low, high)
        introsort_helper(arr, low, pivot - 1, depth - 1)
        introsort_helper(arr, pivot + 1, high, depth - 1)
    
    def insertion_sort_range(arr: List[int], low: int, high: int) -> None:
        """Insertion sort for a range."""
        for i in range(low + 1, high + 1):
            key = arr[i]
            j = i - 1
            while j >= low and arr[j] > key:
                arr[j + 1] = arr[j]
                j -= 1
            arr[j + 1] = key
    
    def heapsort_range(arr: List[int], low: int, high: int) -> None:
        """Heapsort for a range (simplified)."""
        # This is a simplified version - full implementation would be more complex
        temp = arr[low:high+1]
        temp.sort()  # Using built-in sort as placeholder for heap operations
        arr[low:high+1] = temp
    
    def partition_for_intro(arr: List[int], low: int, high: int) -> int:
        """Partition function for introsort."""
        # Median-of-three pivot selection
        mid = (low + high) // 2
        if arr[mid] < arr[low]:
            arr[low], arr[mid] = arr[mid], arr[low]
        if arr[high] < arr[low]:
            arr[low], arr[high] = arr[high], arr[low]
        if arr[mid] < arr[high]:
            arr[mid], arr[high] = arr[high], arr[mid]
        
        pivot = arr[high]
        i = low - 1
        
        for j in range(low, high):
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1
    
    introsort_helper(result, 0, len(result) - 1, max_depth)
    return result


# ============================================================================
# SECTION 5: PERFORMANCE ANALYSIS AND COMPARISON
# ============================================================================

@dataclass
class SortingResult:
    """Results of sorting algorithm execution."""
    algorithm: str
    time_taken: float
    comparisons: int
    memory_usage: str
    is_stable: bool
    is_adaptive: bool


class SortingTester:
    """Comprehensive sorting algorithm tester and analyzer."""
    
    def __init__(self):
        self.sorting_algorithms = {
            'Bubble Sort': bubble_sort,
            'Selection Sort': selection_sort,
            'Insertion Sort': insertion_sort,
            'Merge Sort': merge_sort,
            'Quick Sort': quick_sort,
            'Heap Sort': heap_sort,
            'Counting Sort': counting_sort,
            'Radix Sort': radix_sort,
            'TimSort (Simplified)': timsort_simplified,
            'Intro Sort': intro_sort
        }
    
    def generate_test_data(self, size: int, data_type: str = 'random') -> List[int]:
        """Generate test data of different types."""
        if data_type == 'random':
            return [random.randint(1, 1000) for _ in range(size)]
        elif data_type == 'sorted':
            return list(range(1, size + 1))
        elif data_type == 'reverse':
            return list(range(size, 0, -1))
        elif data_type == 'nearly_sorted':
            arr = list(range(1, size + 1))
            # Introduce a few random swaps
            for _ in range(size // 10):
                i, j = random.randint(0, size - 1), random.randint(0, size - 1)
                arr[i], arr[j] = arr[j], arr[i]
            return arr
        elif data_type == 'duplicates':
            return [random.randint(1, 10) for _ in range(size)]
        else:
            return [random.randint(1, 1000) for _ in range(size)]
    
    def benchmark_algorithm(self, algorithm: Callable, data: List[int]) -> float:
        """Benchmark a single sorting algorithm."""
        data_copy = data.copy()
        
        start_time = time.perf_counter()
        sorted_data = algorithm(data_copy)
        end_time = time.perf_counter()
        
        # Verify the result is sorted
        assert sorted_data == sorted(data), f"Algorithm {algorithm.__name__} failed to sort correctly"
        
        return end_time - start_time
    
    def compare_algorithms(self, data_sizes: List[int], data_types: List[str]) -> None:
        """Compare multiple sorting algorithms across different scenarios."""
        print("=== SORTING ALGORITHM PERFORMANCE COMPARISON ===")
        
        for data_type in data_types:
            print(f"\n{data_type.upper()} DATA:")
            print("-" * 50)
            
            for size in data_sizes:
                print(f"\nArray size: {size}")
                data = self.generate_test_data(size, data_type)
                
                results = {}
                for name, algorithm in self.sorting_algorithms.items():
                    try:
                        # Skip certain algorithms for specific conditions
                        if name == 'Counting Sort' and (max(data) - min(data)) > size * 10:
                            continue
                        if name == 'Radix Sort' and any(x < 0 for x in data):
                            continue
                        if name in ['Bubble Sort', 'Selection Sort'] and size > 1000:
                            continue  # Too slow for large arrays
                        
                        exec_time = self.benchmark_algorithm(algorithm, data)
                        results[name] = exec_time
                        
                    except Exception as e:
                        print(f"    {name}: Error - {e}")
                
                # Display results sorted by execution time
                sorted_results = sorted(results.items(), key=lambda x: x[1])
                for name, time_taken in sorted_results:
                    print(f"    {name:<20}: {time_taken:.6f}s")
    
    def analyze_stability(self) -> None:
        """Analyze stability of sorting algorithms."""
        print("\n=== STABILITY ANALYSIS ===")
        
        # Create test data with equal values but different original positions
        # We'll use tuples (value, original_index) to track stability
        class StabilityTester:
            def __init__(self, value, index):
                self.value = value
                self.index = index
            
            def __lt__(self, other):
                return self.value < other.value
            
            def __le__(self, other):
                return self.value <= other.value
            
            def __eq__(self, other):
                return self.value == other.value
            
            def __repr__(self):
                return f"({self.value},{self.index})"
        
        # Test with simple integers for now
        test_data = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]
        
        stable_algorithms = ['Merge Sort', 'Insertion Sort', 'Counting Sort', 'Radix Sort', 'TimSort (Simplified)']
        unstable_algorithms = ['Quick Sort', 'Heap Sort', 'Selection Sort']
        
        print("Stable algorithms:", stable_algorithms)
        print("Unstable algorithms:", unstable_algorithms)
        
        # Note: Full stability testing would require custom comparison objects
        # This is a simplified demonstration


def demonstrate_sorting_concepts():
    """Demonstrate key sorting concepts with examples."""
    print("=== SORTING ALGORITHM DEMONSTRATIONS ===")
    
    # Small dataset for clear visualization
    test_data = [64, 34, 25, 12, 22, 11, 90]
    print(f"Original array: {test_data}")
    print()
    
    # Demonstrate different algorithms
    algorithms = [
        ('Bubble Sort', bubble_sort),
        ('Selection Sort', selection_sort),
        ('Insertion Sort', insertion_sort),
        ('Merge Sort', merge_sort),
        ('Quick Sort', quick_sort),
        ('Heap Sort', heap_sort)
    ]
    
    for name, algorithm in algorithms:
        print(f"{name}:")
        sorted_data = algorithm(test_data, verbose=True)
        print(f"  Result: {sorted_data}")
        print()
    
    # Demonstrate non-comparison sorts
    print("Non-comparison sorts:")
    
    # Counting sort
    print("Counting Sort:")
    sorted_data = counting_sort(test_data, verbose=True)
    print(f"  Result: {sorted_data}")
    print()
    
    # Radix sort
    print("Radix Sort:")
    sorted_data = radix_sort(test_data, verbose=True)
    print(f"  Result: {sorted_data}")
    print()
    
    # Bucket sort with floats
    float_data = [0.897, 0.565, 0.656, 0.1234, 0.665, 0.3434]
    print(f"Bucket Sort (floats): {float_data}")
    sorted_data = bucket_sort(float_data, verbose=True)
    print(f"  Result: {sorted_data}")


# ============================================================================
# SECTION 6: REAL-WORLD APPLICATIONS
# ============================================================================

def sorting_applications():
    """Demonstrate real-world applications of different sorting algorithms."""
    print("\n=== REAL-WORLD SORTING APPLICATIONS ===")
    
    print("1. Database Query Processing:")
    # Simulate a database table
    employees = [
        {'name': 'Alice', 'salary': 70000, 'department': 'Engineering'},
        {'name': 'Bob', 'salary': 50000, 'department': 'Marketing'},
        {'name': 'Charlie', 'salary': 80000, 'department': 'Engineering'},
        {'name': 'Diana', 'salary': 60000, 'department': 'Finance'},
        {'name': 'Eve', 'salary': 75000, 'department': 'Engineering'}
    ]
    
    # Sort by salary (descending)
    sorted_by_salary = sorted(employees, key=lambda x: x['salary'], reverse=True)
    print("  Employees sorted by salary (highest first):")
    for emp in sorted_by_salary:
        print(f"    {emp['name']}: ${emp['salary']:,}")
    
    print("\n2. E-commerce Product Ranking:")
    products = [
        {'name': 'Laptop', 'price': 999, 'rating': 4.5, 'reviews': 150},
        {'name': 'Mouse', 'price': 25, 'rating': 4.2, 'reviews': 300},
        {'name': 'Keyboard', 'price': 75, 'rating': 4.8, 'reviews': 120},
        {'name': 'Monitor', 'price': 300, 'rating': 4.3, 'reviews': 80}
    ]
    
    # Sort by rating (descending), then by number of reviews (descending)
    sorted_products = sorted(products, key=lambda x: (x['rating'], x['reviews']), reverse=True)
    print("  Products sorted by rating and reviews:")
    for product in sorted_products:
        print(f"    {product['name']}: {product['rating']}★ ({product['reviews']} reviews)")
    
    print("\n3. System Process Scheduling:")
    processes = [
        {'pid': 1001, 'priority': 3, 'cpu_time': 120, 'memory': 256},
        {'pid': 1002, 'priority': 1, 'cpu_time': 50, 'memory': 128},
        {'pid': 1003, 'priority': 2, 'cpu_time': 200, 'memory': 512},
        {'pid': 1004, 'priority': 1, 'cpu_time': 30, 'memory': 64}
    ]
    
    # Sort by priority (lower number = higher priority), then by CPU time
    sorted_processes = sorted(processes, key=lambda x: (x['priority'], x['cpu_time']))
    print("  Processes sorted by priority and CPU time:")
    for proc in sorted_processes:
        print(f"    PID {proc['pid']}: Priority {proc['priority']}, CPU {proc['cpu_time']}ms")
    
    print("\n4. Algorithm Choice Guidelines:")
    guidelines = [
        "Small arrays (< 50 elements): Insertion Sort",
        "Large arrays, stability required: Merge Sort",
        "Large arrays, memory constrained: Heap Sort",
        "Large arrays, average case: Quick Sort or Intro Sort",
        "Integer arrays with small range: Counting Sort",
        "Integer arrays: Radix Sort",
        "Nearly sorted arrays: Insertion Sort or Tim Sort",
        "General purpose: Tim Sort (Python's default)"
    ]
    
    for guideline in guidelines:
        print(f"  • {guideline}")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main function to run all demonstrations."""
    print("Comprehensive Sorting Algorithms Implementation")
    print("=" * 60)
    
    try:
        # Demonstrate sorting concepts
        demonstrate_sorting_concepts()
        
        # Show real-world applications
        sorting_applications()
        
        # Performance comparison
        tester = SortingTester()
        
        # Quick comparison with small data
        print("\n=== QUICK PERFORMANCE COMPARISON ===")
        small_sizes = [100, 500]
        data_types = ['random', 'sorted', 'reverse']
        
        tester.compare_algorithms(small_sizes, data_types)
        
        # Analyze stability
        tester.analyze_stability()
        
    except Exception as e:
        print(f"Error during execution: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        print(f"\n{'=' * 60}")
        print("Sorting algorithms demonstration complete!")
        print(f"Python version: {sys.version}")


if __name__ == "__main__":
    main()


# ============================================================================
# PRACTICE EXERCISES
# ============================================================================

"""
PRACTICE EXERCISES:

1. Implement iterative merge sort using bottom-up approach.

2. Create a dual-pivot quick sort implementation.

3. Implement external merge sort for datasets larger than memory.

4. Create a stable version of quick sort.

5. Implement shell sort with different gap sequences.

6. Build a parallel merge sort using threading.

7. Create an adaptive sorting algorithm that chooses the best algorithm based on data characteristics.

8. Implement cycle sort (minimize memory writes).

9. Build a sorting algorithm for linked lists.

10. Create a tournament sort implementation.

ADVANCED CHALLENGES:

1. Implement multi-key sorting (sort by multiple criteria)
2. Create cache-oblivious sorting algorithms
3. Build external sorting for very large files
4. Implement parallel quicksort
5. Create string-specific sorting algorithms (suffix arrays)
6. Build sorting algorithms for special data types (dates, IP addresses)
7. Implement approximate sorting algorithms
8. Create online sorting algorithms
9. Build sorting with partial information
10. Implement sorting with custom comparison functions

ALGORITHM OPTIMIZATION:

1. Profile and optimize sorting algorithms for specific hardware
2. Implement SIMD-optimized sorting
3. Create GPU-accelerated sorting
4. Build memory-efficient sorting for embedded systems
5. Implement real-time sorting constraints

SYSTEM APPLICATIONS:

1. Database index sorting
2. File system operations
3. Network packet processing
4. Image processing algorithms
5. Scientific computing data processing
"""
