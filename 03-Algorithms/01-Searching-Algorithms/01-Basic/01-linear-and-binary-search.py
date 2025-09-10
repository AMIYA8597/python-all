#!/usr/bin/env python3
"""
Comprehensive Search Algorithms Implementation

This module provides complete implementations of fundamental search algorithms
including linear search, binary search, and their variants with detailed
explanations, performance analysis, and practical applications.

Author: Python DSA Master
Date: 2024
"""

import time
import random
from typing import List, Optional, Tuple, Any, Callable
import bisect
from dataclasses import dataclass


@dataclass
class SearchResult:
    """Result of a search operation with metadata."""
    found: bool
    index: Optional[int]
    comparisons: int
    time_taken: float
    algorithm_used: str


class SearchAlgorithms:
    """
    Comprehensive collection of search algorithms with analysis.
    
    This class implements various search algorithms with detailed
    performance tracking and comparison capabilities.
    """
    
    @staticmethod
    def linear_search(arr: List[Any], target: Any, 
                     key_func: Optional[Callable] = None) -> SearchResult:
        """
        Linear Search Algorithm
        
        Searches for a target element by examining each element sequentially.
        
        Time Complexity: O(n)
        Space Complexity: O(1)
        
        Args:
            arr: List to search in
            target: Element to find
            key_func: Optional function to extract comparison key
            
        Returns:
            SearchResult with details about the search operation
            
        Examples:
            >>> searcher = SearchAlgorithms()
            >>> arr = [64, 34, 25, 12, 22, 11, 90]
            >>> result = searcher.linear_search(arr, 22)
            >>> print(f"Found at index: {result.index}")
            Found at index: 4
        """
        start_time = time.perf_counter()
        comparisons = 0
        
        for i, element in enumerate(arr):
            comparisons += 1
            compare_value = key_func(element) if key_func else element
            target_value = key_func(target) if key_func else target
            
            if compare_value == target_value:
                end_time = time.perf_counter()
                return SearchResult(
                    found=True,
                    index=i,
                    comparisons=comparisons,
                    time_taken=end_time - start_time,
                    algorithm_used="Linear Search"
                )
        
        end_time = time.perf_counter()
        return SearchResult(
            found=False,
            index=None,
            comparisons=comparisons,
            time_taken=end_time - start_time,
            algorithm_used="Linear Search"
        )
    
    @staticmethod
    def binary_search(arr: List[Any], target: Any, 
                     key_func: Optional[Callable] = None) -> SearchResult:
        """
        Binary Search Algorithm (Iterative)
        
        Searches for a target in a sorted array by repeatedly dividing
        the search space in half.
        
        Time Complexity: O(log n)
        Space Complexity: O(1)
        
        Args:
            arr: Sorted list to search in
            target: Element to find
            key_func: Optional function to extract comparison key
            
        Returns:
            SearchResult with details about the search operation
            
        Examples:
            >>> searcher = SearchAlgorithms()
            >>> arr = [11, 12, 22, 25, 34, 64, 90]  # Must be sorted
            >>> result = searcher.binary_search(arr, 22)
            >>> print(f"Found at index: {result.index}")
            Found at index: 2
        """
        start_time = time.perf_counter()
        comparisons = 0
        left, right = 0, len(arr) - 1
        
        while left <= right:
            mid = (left + right) // 2
            comparisons += 1
            
            mid_value = key_func(arr[mid]) if key_func else arr[mid]
            target_value = key_func(target) if key_func else target
            
            if mid_value == target_value:
                end_time = time.perf_counter()
                return SearchResult(
                    found=True,
                    index=mid,
                    comparisons=comparisons,
                    time_taken=end_time - start_time,
                    algorithm_used="Binary Search (Iterative)"
                )
            elif mid_value < target_value:
                left = mid + 1
            else:
                right = mid - 1
        
        end_time = time.perf_counter()
        return SearchResult(
            found=False,
            index=None,
            comparisons=comparisons,
            time_taken=end_time - start_time,
            algorithm_used="Binary Search (Iterative)"
        )
    
    @staticmethod
    def binary_search_recursive(arr: List[Any], target: Any, 
                               key_func: Optional[Callable] = None,
                               left: int = 0, right: Optional[int] = None,
                               comparisons: int = 0, 
                               start_time: Optional[float] = None) -> SearchResult:
        """
        Binary Search Algorithm (Recursive)
        
        Recursive implementation of binary search.
        
        Time Complexity: O(log n)
        Space Complexity: O(log n) due to recursion stack
        
        Args:
            arr: Sorted list to search in
            target: Element to find
            key_func: Optional function to extract comparison key
            left: Left boundary of search space
            right: Right boundary of search space
            comparisons: Number of comparisons made (internal use)
            start_time: Start time of search (internal use)
            
        Returns:
            SearchResult with details about the search operation
        """
        if start_time is None:
            start_time = time.perf_counter()
        if right is None:
            right = len(arr) - 1
        
        if left > right:
            end_time = time.perf_counter()
            return SearchResult(
                found=False,
                index=None,
                comparisons=comparisons,
                time_taken=end_time - start_time,
                algorithm_used="Binary Search (Recursive)"
            )
        
        mid = (left + right) // 2
        comparisons += 1
        
        mid_value = key_func(arr[mid]) if key_func else arr[mid]
        target_value = key_func(target) if key_func else target
        
        if mid_value == target_value:
            end_time = time.perf_counter()
            return SearchResult(
                found=True,
                index=mid,
                comparisons=comparisons,
                time_taken=end_time - start_time,
                algorithm_used="Binary Search (Recursive)"
            )
        elif mid_value < target_value:
            return SearchAlgorithms.binary_search_recursive(
                arr, target, key_func, mid + 1, right, comparisons, start_time
            )
        else:
            return SearchAlgorithms.binary_search_recursive(
                arr, target, key_func, left, mid - 1, comparisons, start_time
            )
    
    @staticmethod
    def interpolation_search(arr: List[int], target: int) -> SearchResult:
        """
        Interpolation Search Algorithm
        
        An improved binary search for uniformly distributed sorted arrays.
        Uses position estimation based on target value.
        
        Time Complexity: O(log log n) for uniform distribution, O(n) worst case
        Space Complexity: O(1)
        
        Args:
            arr: Sorted list of integers
            target: Integer to find
            
        Returns:
            SearchResult with details about the search operation
        """
        start_time = time.perf_counter()
        comparisons = 0
        left, right = 0, len(arr) - 1
        
        while left <= right and target >= arr[left] and target <= arr[right]:
            # If array has only one element
            if left == right:
                comparisons += 1
                if arr[left] == target:
                    end_time = time.perf_counter()
                    return SearchResult(
                        found=True,
                        index=left,
                        comparisons=comparisons,
                        time_taken=end_time - start_time,
                        algorithm_used="Interpolation Search"
                    )
                break
            
            # Calculate position using interpolation formula
            pos = left + int(((target - arr[left]) / (arr[right] - arr[left])) * (right - left))
            
            # Ensure position is within bounds
            pos = max(left, min(right, pos))
            
            comparisons += 1
            if arr[pos] == target:
                end_time = time.perf_counter()
                return SearchResult(
                    found=True,
                    index=pos,
                    comparisons=comparisons,
                    time_taken=end_time - start_time,
                    algorithm_used="Interpolation Search"
                )
            elif arr[pos] < target:
                left = pos + 1
            else:
                right = pos - 1
        
        end_time = time.perf_counter()
        return SearchResult(
            found=False,
            index=None,
            comparisons=comparisons,
            time_taken=end_time - start_time,
            algorithm_used="Interpolation Search"
        )
    
    @staticmethod
    def exponential_search(arr: List[Any], target: Any, 
                          key_func: Optional[Callable] = None) -> SearchResult:
        """
        Exponential Search Algorithm
        
        Finds range for binary search by repeated doubling,
        then applies binary search within that range.
        
        Time Complexity: O(log n)
        Space Complexity: O(1)
        
        Args:
            arr: Sorted list to search in
            target: Element to find
            key_func: Optional function to extract comparison key
            
        Returns:
            SearchResult with details about the search operation
        """
        start_time = time.perf_counter()
        
        if not arr:
            end_time = time.perf_counter()
            return SearchResult(
                found=False,
                index=None,
                comparisons=0,
                time_taken=end_time - start_time,
                algorithm_used="Exponential Search"
            )
        
        # Check if target is at first position
        first_value = key_func(arr[0]) if key_func else arr[0]
        target_value = key_func(target) if key_func else target
        
        if first_value == target_value:
            end_time = time.perf_counter()
            return SearchResult(
                found=True,
                index=0,
                comparisons=1,
                time_taken=end_time - start_time,
                algorithm_used="Exponential Search"
            )
        
        # Find range for binary search
        i = 1
        comparisons = 1  # First comparison already done
        
        while i < len(arr):
            current_value = key_func(arr[i]) if key_func else arr[i]
            comparisons += 1
            
            if current_value >= target_value:
                break
            i *= 2
        
        # Apply binary search in found range
        left = i // 2
        right = min(i, len(arr) - 1)
        
        while left <= right:
            mid = (left + right) // 2
            comparisons += 1
            
            mid_value = key_func(arr[mid]) if key_func else arr[mid]
            
            if mid_value == target_value:
                end_time = time.perf_counter()
                return SearchResult(
                    found=True,
                    index=mid,
                    comparisons=comparisons,
                    time_taken=end_time - start_time,
                    algorithm_used="Exponential Search"
                )
            elif mid_value < target_value:
                left = mid + 1
            else:
                right = mid - 1
        
        end_time = time.perf_counter()
        return SearchResult(
            found=False,
            index=None,
            comparisons=comparisons,
            time_taken=end_time - start_time,
            algorithm_used="Exponential Search"
        )


class AdvancedSearchAlgorithms:
    """Advanced search algorithms for specialized use cases."""
    
    @staticmethod
    def ternary_search(arr: List[Any], target: Any, 
                      key_func: Optional[Callable] = None) -> SearchResult:
        """
        Ternary Search Algorithm
        
        Divides array into three parts instead of two.
        
        Time Complexity: O(log₃ n) ≈ O(log n)
        Space Complexity: O(1)
        
        Note: Generally performs more comparisons than binary search.
        """
        start_time = time.perf_counter()
        comparisons = 0
        left, right = 0, len(arr) - 1
        
        while left <= right:
            mid1 = left + (right - left) // 3
            mid2 = right - (right - left) // 3
            
            mid1_value = key_func(arr[mid1]) if key_func else arr[mid1]
            mid2_value = key_func(arr[mid2]) if key_func else arr[mid2]
            target_value = key_func(target) if key_func else target
            
            comparisons += 1
            if mid1_value == target_value:
                end_time = time.perf_counter()
                return SearchResult(
                    found=True,
                    index=mid1,
                    comparisons=comparisons,
                    time_taken=end_time - start_time,
                    algorithm_used="Ternary Search"
                )
            
            comparisons += 1
            if mid2_value == target_value:
                end_time = time.perf_counter()
                return SearchResult(
                    found=True,
                    index=mid2,
                    comparisons=comparisons,
                    time_taken=end_time - start_time,
                    algorithm_used="Ternary Search"
                )
            
            if target_value < mid1_value:
                right = mid1 - 1
            elif target_value > mid2_value:
                left = mid2 + 1
            else:
                left = mid1 + 1
                right = mid2 - 1
        
        end_time = time.perf_counter()
        return SearchResult(
            found=False,
            index=None,
            comparisons=comparisons,
            time_taken=end_time - start_time,
            algorithm_used="Ternary Search"
        )
    
    @staticmethod
    def jump_search(arr: List[Any], target: Any, 
                   key_func: Optional[Callable] = None) -> SearchResult:
        """
        Jump Search Algorithm
        
        Jumps ahead by fixed steps, then does linear search
        in the identified block.
        
        Time Complexity: O(√n)
        Space Complexity: O(1)
        """
        start_time = time.perf_counter()
        comparisons = 0
        n = len(arr)
        
        if n == 0:
            end_time = time.perf_counter()
            return SearchResult(
                found=False,
                index=None,
                comparisons=0,
                time_taken=end_time - start_time,
                algorithm_used="Jump Search"
            )
        
        # Calculate optimal jump size
        jump_size = int(n ** 0.5)
        prev = 0
        
        # Jump to find the block containing target
        target_value = key_func(target) if key_func else target
        
        while prev < n:
            current_index = min(prev + jump_size - 1, n - 1)
            current_value = key_func(arr[current_index]) if key_func else arr[current_index]
            comparisons += 1
            
            if current_value >= target_value:
                break
            prev += jump_size
        
        # Linear search in the identified block
        for i in range(prev, min(prev + jump_size, n)):
            current_value = key_func(arr[i]) if key_func else arr[i]
            comparisons += 1
            
            if current_value == target_value:
                end_time = time.perf_counter()
                return SearchResult(
                    found=True,
                    index=i,
                    comparisons=comparisons,
                    time_taken=end_time - start_time,
                    algorithm_used="Jump Search"
                )
        
        end_time = time.perf_counter()
        return SearchResult(
            found=False,
            index=None,
            comparisons=comparisons,
            time_taken=end_time - start_time,
            algorithm_used="Jump Search"
        )


class SearchUtilities:
    """Utility functions for search operations."""
    
    @staticmethod
    def find_all_occurrences(arr: List[Any], target: Any,
                           key_func: Optional[Callable] = None) -> List[int]:
        """Find all indices where target appears in the array."""
        indices = []
        target_value = key_func(target) if key_func else target
        
        for i, element in enumerate(arr):
            element_value = key_func(element) if key_func else element
            if element_value == target_value:
                indices.append(i)
        
        return indices
    
    @staticmethod
    def find_first_occurrence(arr: List[Any], target: Any,
                            key_func: Optional[Callable] = None) -> Optional[int]:
        """Find the first occurrence of target in a sorted array."""
        left, right = 0, len(arr) - 1
        result = None
        target_value = key_func(target) if key_func else target
        
        while left <= right:
            mid = (left + right) // 2
            mid_value = key_func(arr[mid]) if key_func else arr[mid]
            
            if mid_value == target_value:
                result = mid
                right = mid - 1  # Continue searching in left half
            elif mid_value < target_value:
                left = mid + 1
            else:
                right = mid - 1
        
        return result
    
    @staticmethod
    def find_last_occurrence(arr: List[Any], target: Any,
                           key_func: Optional[Callable] = None) -> Optional[int]:
        """Find the last occurrence of target in a sorted array."""
        left, right = 0, len(arr) - 1
        result = None
        target_value = key_func(target) if key_func else target
        
        while left <= right:
            mid = (left + right) // 2
            mid_value = key_func(arr[mid]) if key_func else arr[mid]
            
            if mid_value == target_value:
                result = mid
                left = mid + 1  # Continue searching in right half
            elif mid_value < target_value:
                left = mid + 1
            else:
                right = mid - 1
        
        return result
    
    @staticmethod
    def count_occurrences(arr: List[Any], target: Any,
                         key_func: Optional[Callable] = None) -> int:
        """Count occurrences of target in a sorted array."""
        first = SearchUtilities.find_first_occurrence(arr, target, key_func)
        if first is None:
            return 0
        
        last = SearchUtilities.find_last_occurrence(arr, target, key_func)
        return last - first + 1


def performance_comparison():
    """Compare performance of different search algorithms."""
    print("Search Algorithms Performance Comparison")
    print("=" * 50)
    
    # Generate test data
    sizes = [1000, 10000, 100000]
    algorithms = [
        ("Linear Search", SearchAlgorithms.linear_search),
        ("Binary Search (Iterative)", SearchAlgorithms.binary_search),
        ("Binary Search (Recursive)", SearchAlgorithms.binary_search_recursive),
        ("Jump Search", AdvancedSearchAlgorithms.jump_search),
        ("Exponential Search", SearchAlgorithms.exponential_search),
    ]
    
    for size in sizes:
        print(f"\nArray Size: {size:,}")
        print("-" * 30)
        
        # Create sorted array
        arr = list(range(0, size * 2, 2))  # Even numbers
        target = size  # Middle element
        
        for name, algorithm in algorithms:
            # Skip linear search for very large arrays to save time
            if name == "Linear Search" and size > 10000:
                print(f"{name:<25}: Skipped (too slow for large arrays)")
                continue
            
            result = algorithm(arr, target)
            print(f"{name:<25}: {result.time_taken*1000:.3f}ms, "
                  f"{result.comparisons:,} comparisons")


def search_examples():
    """Demonstrate various search algorithms with examples."""
    print("Search Algorithms Examples")
    print("=" * 40)
    
    # Example 1: Basic searching
    print("\n1. Basic Search Operations")
    arr = [64, 34, 25, 12, 22, 11, 90]
    target = 22
    
    print(f"Array: {arr}")
    print(f"Searching for: {target}")
    
    linear_result = SearchAlgorithms.linear_search(arr, target)
    print(f"Linear Search: Found at index {linear_result.index} "
          f"({linear_result.comparisons} comparisons)")
    
    # Example 2: Binary search (requires sorted array)
    print("\n2. Binary Search (Sorted Array)")
    sorted_arr = sorted(arr)
    print(f"Sorted array: {sorted_arr}")
    
    binary_result = SearchAlgorithms.binary_search(sorted_arr, target)
    print(f"Binary Search: Found at index {binary_result.index} "
          f"({binary_result.comparisons} comparisons)")
    
    # Example 3: Search with custom key function
    print("\n3. Search with Custom Key Function")
    students = [
        {"name": "Alice", "grade": 85},
        {"name": "Bob", "grade": 92},
        {"name": "Charlie", "grade": 78},
        {"name": "Diana", "grade": 96}
    ]
    
    # Search by grade
    result = SearchAlgorithms.linear_search(
        students, 92, key_func=lambda x: x["grade"]
    )
    if result.found:
        student = students[result.index]
        print(f"Student with grade 92: {student['name']}")
    
    # Example 4: Multiple occurrences
    print("\n4. Multiple Occurrences")
    arr_with_duplicates = [1, 2, 2, 2, 3, 4, 5]
    target = 2
    
    all_indices = SearchUtilities.find_all_occurrences(arr_with_duplicates, target)
    first_index = SearchUtilities.find_first_occurrence(arr_with_duplicates, target)
    last_index = SearchUtilities.find_last_occurrence(arr_with_duplicates, target)
    count = SearchUtilities.count_occurrences(arr_with_duplicates, target)
    
    print(f"Array: {arr_with_duplicates}")
    print(f"All occurrences of {target}: {all_indices}")
    print(f"First occurrence: {first_index}")
    print(f"Last occurrence: {last_index}")
    print(f"Total count: {count}")
    
    # Example 5: Advanced search algorithms
    print("\n5. Advanced Search Algorithms")
    large_arr = list(range(1, 101, 2))  # Odd numbers 1-99
    target = 47
    
    print(f"Searching for {target} in array of {len(large_arr)} odd numbers")
    
    jump_result = AdvancedSearchAlgorithms.jump_search(large_arr, target)
    ternary_result = AdvancedSearchAlgorithms.ternary_search(large_arr, target)
    exp_result = SearchAlgorithms.exponential_search(large_arr, target)
    
    print(f"Jump Search: Index {jump_result.index} ({jump_result.comparisons} comparisons)")
    print(f"Ternary Search: Index {ternary_result.index} ({ternary_result.comparisons} comparisons)")
    print(f"Exponential Search: Index {exp_result.index} ({exp_result.comparisons} comparisons)")


def real_world_applications():
    """Demonstrate real-world applications of search algorithms."""
    print("\nReal-World Applications")
    print("=" * 30)
    
    # Application 1: Phone book search
    print("\n1. Phone Book Search")
    contacts = [
        {"name": "Alice Johnson", "phone": "555-0123"},
        {"name": "Bob Smith", "phone": "555-0124"},
        {"name": "Charlie Brown", "phone": "555-0125"},
        {"name": "Diana Prince", "phone": "555-0126"},
        {"name": "Eve Wilson", "phone": "555-0127"}
    ]
    
    # Binary search by name (assuming sorted)
    result = SearchAlgorithms.binary_search(
        contacts, "Charlie Brown", key_func=lambda x: x["name"]
    )
    if result.found:
        contact = contacts[result.index]
        print(f"Found {contact['name']}: {contact['phone']}")
    
    # Application 2: Library catalog search
    print("\n2. Library Catalog Search")
    books = [
        {"title": "Data Structures", "isbn": "978-0123456789", "year": 2020},
        {"title": "Algorithms", "isbn": "978-0234567890", "year": 2019},
        {"title": "Python Programming", "isbn": "978-0345678901", "year": 2021}
    ]
    
    # Search by ISBN
    isbn_to_find = "978-0234567890"
    result = SearchAlgorithms.linear_search(
        books, isbn_to_find, key_func=lambda x: x["isbn"]
    )
    if result.found:
        book = books[result.index]
        print(f"Found book: {book['title']} ({book['year']})")
    
    # Application 3: Log file analysis
    print("\n3. Log File Analysis (Simulated)")
    log_entries = [
        {"timestamp": "2024-01-01 10:00:00", "level": "INFO", "message": "Server started"},
        {"timestamp": "2024-01-01 10:15:00", "level": "WARNING", "message": "High memory usage"},
        {"timestamp": "2024-01-01 10:30:00", "level": "ERROR", "message": "Database connection failed"},
        {"timestamp": "2024-01-01 10:45:00", "level": "INFO", "message": "Connection restored"}
    ]
    
    # Find all ERROR level entries
    error_indices = SearchUtilities.find_all_occurrences(
        log_entries, "ERROR", key_func=lambda x: x["level"]
    )
    
    print(f"Found {len(error_indices)} error entries:")
    for idx in error_indices:
        entry = log_entries[idx]
        print(f"  {entry['timestamp']}: {entry['message']}")


def main():
    """Main function to demonstrate search algorithms."""
    print("Python DSA Master - Search Algorithms")
    print("=" * 50)
    
    try:
        search_examples()
        performance_comparison()
        real_world_applications()
        
    except KeyboardInterrupt:
        print("\nDemo interrupted by user")
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()
    
    print(f"\n{'='*50}")
    print("Search Algorithms demonstration complete!")


if __name__ == "__main__":
    main()


# ============================================================================
# PRACTICE EXERCISES
# ============================================================================

"""
PRACTICE EXERCISES:

1. BEGINNER LEVEL:
   - Implement a search function that finds the position of the maximum element
   - Create a function to search for an element in a rotated sorted array
   - Write a function to find the square root of a number using binary search

2. INTERMEDIATE LEVEL:
   - Implement search in a 2D sorted matrix
   - Create a function to find the peak element in an array
   - Write a search algorithm for finding a target in a sorted array with duplicates

3. ADVANCED LEVEL:
   - Implement search in an infinite sorted array
   - Create a function for searching in a sorted array of unknown size
   - Write an algorithm to find the median of two sorted arrays

4. OPTIMIZATION CHALLENGES:
   - Compare the performance of different search algorithms on various data sets
   - Implement a cache-aware search algorithm
   - Create a parallel search algorithm using threading

5. REAL-WORLD APPLICATIONS:
   - Build a simple search engine for documents
   - Create a autocomplete system using search algorithms
   - Implement a spell checker using fuzzy search techniques
"""
