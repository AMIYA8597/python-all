#!/usr/bin/env python3
"""
Lists Implementation - Comprehensive Guide
=========================================

This module demonstrates list implementations in Python with detailed analysis
of built-in lists, custom dynamic arrays, and performance comparisons.

Topics Covered:
- Python built-in list operations and complexity
- Custom dynamic array implementation
- Memory management and growth strategies
- Performance benchmarking and optimization
- Real-world applications and use cases
- Comparison with other data structures

Author: Python DSA Master Course
Version: 1.0
"""

import sys
import time
import timeit
import random
from typing import List, Any, Optional, Iterator, TypeVar, Generic
import array
import gc
from collections import deque
import matplotlib.pyplot as plt
import numpy as np


T = TypeVar('T')


# ============================================================================
# SECTION 1: PYTHON BUILT-IN LIST ANALYSIS
# ============================================================================

def builtin_list_analysis():
    """
    Analyze Python's built-in list implementation and behavior.
    """
    print("=== PYTHON BUILT-IN LIST ANALYSIS ===")
    
    # Memory growth pattern analysis
    def analyze_memory_growth():
        """Analyze how Python lists grow in memory."""
        print("Memory growth pattern analysis:")
        
        sizes = []
        capacities = []
        
        lst = []
        for i in range(100):
            lst.append(i)
            size = len(lst)
            # Estimate capacity by finding when next append causes reallocation
            old_id = id(lst)
            temp_list = lst.copy()
            temp_list.append(None)
            capacity = size
            
            # More accurate capacity estimation using __sizeof__
            # Rough estimation: (sizeof - base_size) / pointer_size
            base_size = sys.getsizeof([])
            pointer_size = 8  # 64-bit systems
            estimated_capacity = (sys.getsizeof(lst) - base_size) // pointer_size
            
            if i < 20 or i % 10 == 0:
                print(f"  Size: {size:3d}, Estimated capacity: {estimated_capacity:3d}, "
                      f"Memory: {sys.getsizeof(lst):4d} bytes")
            
            sizes.append(size)
            capacities.append(estimated_capacity)
    
    analyze_memory_growth()
    
    # Time complexity demonstration
    def demonstrate_complexity():
        """Demonstrate time complexity of common list operations."""
        print(f"\nTime complexity demonstration:")
        
        # Append operation - O(1) amortized
        def test_append(n):
            lst = []
            start = time.perf_counter()
            for i in range(n):
                lst.append(i)
            end = time.perf_counter()
            return end - start
        
        sizes = [1000, 2000, 4000, 8000, 16000]
        append_times = []
        
        for size in sizes:
            time_taken = test_append(size)
            append_times.append(time_taken)
            print(f"  Append {size} items: {time_taken:.6f} seconds")
        
        # Insert at beginning - O(n)
        def test_insert_front(n):
            lst = []
            start = time.perf_counter()
            for i in range(n):
                lst.insert(0, i)
            end = time.perf_counter()
            return end - start
        
        print(f"\nInsert at beginning (O(n) each operation):")
        sizes_small = [100, 200, 400, 800]  # Smaller sizes due to O(n²) behavior
        for size in sizes_small:
            time_taken = test_insert_front(size)
            print(f"  Insert {size} items at front: {time_taken:.6f} seconds")
        
        # Search operation - O(n)
        def test_search(lst, target):
            start = time.perf_counter()
            result = target in lst
            end = time.perf_counter()
            return end - start, result
        
        test_list = list(range(100000))
        search_targets = [0, 50000, 99999, 100000]  # Beginning, middle, end, not found
        
        print(f"\nSearch in list of 100,000 elements:")
        for target in search_targets:
            time_taken, found = test_search(test_list, target)
            print(f"  Search for {target}: {time_taken:.6f} seconds, found: {found}")
    
    demonstrate_complexity()


# ============================================================================
# SECTION 2: CUSTOM DYNAMIC ARRAY IMPLEMENTATION
# ============================================================================

class DynamicArray(Generic[T]):
    """
    Custom implementation of a dynamic array (similar to Python list).
    
    Demonstrates memory management, growth strategies, and core operations.
    """
    
    def __init__(self, initial_capacity: int = 4):
        """Initialize dynamic array with given initial capacity."""
        self._capacity = max(initial_capacity, 1)
        self._size = 0
        self._data = [None] * self._capacity
        self._growth_factor = 1.5  # Growth factor for resizing
    
    def __len__(self) -> int:
        """Return the number of elements in the array."""
        return self._size
    
    def __getitem__(self, index: int) -> T:
        """Get item at given index with bounds checking."""
        if not 0 <= index < self._size:
            raise IndexError(f"Index {index} out of range [0, {self._size})")
        return self._data[index]
    
    def __setitem__(self, index: int, value: T) -> None:
        """Set item at given index with bounds checking."""
        if not 0 <= index < self._size:
            raise IndexError(f"Index {index} out of range [0, {self._size})")
        self._data[index] = value
    
    def __str__(self) -> str:
        """String representation of the array."""
        return '[' + ', '.join(str(self._data[i]) for i in range(self._size)) + ']'
    
    def __repr__(self) -> str:
        """Detailed representation for debugging."""
        return f"DynamicArray(size={self._size}, capacity={self._capacity}, data={str(self)})"
    
    def append(self, value: T) -> None:
        """
        Add element to the end of array.
        
        Time Complexity: O(1) amortized, O(n) worst case (when resize needed)
        Space Complexity: O(1)
        """
        if self._size >= self._capacity:
            self._resize()
        
        self._data[self._size] = value
        self._size += 1
    
    def insert(self, index: int, value: T) -> None:
        """
        Insert element at given index.
        
        Time Complexity: O(n) - need to shift elements
        Space Complexity: O(1)
        """
        if not 0 <= index <= self._size:
            raise IndexError(f"Index {index} out of range [0, {self._size}]")
        
        if self._size >= self._capacity:
            self._resize()
        
        # Shift elements to the right
        for i in range(self._size, index, -1):
            self._data[i] = self._data[i - 1]
        
        self._data[index] = value
        self._size += 1
    
    def pop(self, index: int = -1) -> T:
        """
        Remove and return element at given index (default: last element).
        
        Time Complexity: O(1) for last element, O(n) for arbitrary index
        Space Complexity: O(1)
        """
        if self._size == 0:
            raise IndexError("pop from empty array")
        
        # Handle negative indices
        if index < 0:
            index = self._size + index
        
        if not 0 <= index < self._size:
            raise IndexError(f"Index {index} out of range [0, {self._size})")
        
        value = self._data[index]
        
        # Shift elements to the left
        for i in range(index, self._size - 1):
            self._data[i] = self._data[i + 1]
        
        self._size -= 1
        self._data[self._size] = None  # Clear reference
        
        # Shrink if array is too sparse
        if self._size < self._capacity // 4 and self._capacity > 4:
            self._shrink()
        
        return value
    
    def remove(self, value: T) -> None:
        """
        Remove first occurrence of value.
        
        Time Complexity: O(n) - need to search and shift
        Space Complexity: O(1)
        """
        for i in range(self._size):
            if self._data[i] == value:
                self.pop(i)
                return
        raise ValueError(f"{value} not in array")
    
    def index(self, value: T) -> int:
        """
        Find index of first occurrence of value.
        
        Time Complexity: O(n)
        Space Complexity: O(1)
        """
        for i in range(self._size):
            if self._data[i] == value:
                return i
        raise ValueError(f"{value} not in array")
    
    def extend(self, iterable) -> None:
        """
        Extend array with elements from iterable.
        
        Time Complexity: O(k) where k is length of iterable
        Space Complexity: O(k)
        """
        for item in iterable:
            self.append(item)
    
    def clear(self) -> None:
        """
        Remove all elements from array.
        
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        for i in range(self._size):
            self._data[i] = None
        self._size = 0
    
    def copy(self) -> 'DynamicArray[T]':
        """
        Create shallow copy of array.
        
        Time Complexity: O(n)
        Space Complexity: O(n)
        """
        new_array = DynamicArray(self._capacity)
        for i in range(self._size):
            new_array.append(self._data[i])
        return new_array
    
    def _resize(self) -> None:
        """Resize the internal array when capacity is exceeded."""
        old_capacity = self._capacity
        self._capacity = int(self._capacity * self._growth_factor)
        
        old_data = self._data
        self._data = [None] * self._capacity
        
        # Copy elements to new array
        for i in range(self._size):
            self._data[i] = old_data[i]
        
        print(f"  Resized from {old_capacity} to {self._capacity}")
    
    def _shrink(self) -> None:
        """Shrink the internal array when it becomes too sparse."""
        old_capacity = self._capacity
        self._capacity = max(self._capacity // 2, 4)
        
        old_data = self._data
        self._data = [None] * self._capacity
        
        # Copy elements to new array
        for i in range(self._size):
            self._data[i] = old_data[i]
        
        print(f"  Shrank from {old_capacity} to {self._capacity}")
    
    @property
    def capacity(self) -> int:
        """Get current capacity of the array."""
        return self._capacity
    
    def memory_info(self) -> dict:
        """Get detailed memory information about the array."""
        return {
            'size': self._size,
            'capacity': self._capacity,
            'load_factor': self._size / self._capacity if self._capacity > 0 else 0,
            'memory_usage': sys.getsizeof(self._data) + sys.getsizeof(self),
            'wasted_space': self._capacity - self._size
        }


def demonstrate_dynamic_array():
    """Demonstrate the custom DynamicArray implementation."""
    print(f"\n=== CUSTOM DYNAMIC ARRAY DEMONSTRATION ===")
    
    # Basic operations
    arr = DynamicArray[int](initial_capacity=2)
    print(f"Initial array: {arr}")
    print(f"Memory info: {arr.memory_info()}")
    
    # Test append operations and resizing
    print(f"\nTesting append operations:")
    for i in range(10):
        arr.append(i)
        if i < 5 or arr.capacity != arr.memory_info()['capacity']:
            print(f"After append({i}): {arr}")
    
    print(f"Final memory info: {arr.memory_info()}")
    
    # Test insert operations
    print(f"\nTesting insert operations:")
    arr.insert(0, -1)  # Insert at beginning
    print(f"After insert(0, -1): {arr}")
    
    arr.insert(5, 100)  # Insert in middle
    print(f"After insert(5, 100): {arr}")
    
    # Test removal operations
    print(f"\nTesting removal operations:")
    removed = arr.pop()  # Remove last
    print(f"Popped: {removed}, Array: {arr}")
    
    removed = arr.pop(0)  # Remove first
    print(f"Popped first: {removed}, Array: {arr}")
    
    # Test search operations
    print(f"\nTesting search operations:")
    try:
        index = arr.index(100)
        print(f"Index of 100: {index}")
    except ValueError as e:
        print(f"Search error: {e}")
    
    # Test error handling
    print(f"\nTesting error handling:")
    try:
        arr[100] = 1
    except IndexError as e:
        print(f"Index error: {e}")
    
    try:
        arr.remove(999)
    except ValueError as e:
        print(f"Remove error: {e}")


# ============================================================================
# SECTION 3: PERFORMANCE BENCHMARKING
# ============================================================================

def benchmark_list_operations():
    """
    Comprehensive benchmarking of list operations.
    """
    print(f"\n=== PERFORMANCE BENCHMARKING ===")
    
    def benchmark_append():
        """Benchmark append operations."""
        print("Benchmarking append operations:")
        
        sizes = [1000, 5000, 10000, 50000, 100000]
        
        # Test Python list
        python_times = []
        for size in sizes:
            stmt = f"""
lst = []
for i in range({size}):
    lst.append(i)
"""
            time_taken = timeit.timeit(stmt, number=10) / 10
            python_times.append(time_taken)
            print(f"  Python list append {size} items: {time_taken:.6f}s")
        
        # Test custom dynamic array
        print(f"\nCustom DynamicArray:")
        custom_times = []
        for size in sizes:
            start = time.perf_counter()
            arr = DynamicArray()
            for i in range(size):
                arr.append(i)
            end = time.perf_counter()
            time_taken = end - start
            custom_times.append(time_taken)
            print(f"  DynamicArray append {size} items: {time_taken:.6f}s")
    
    def benchmark_insert():
        """Benchmark insert operations at different positions."""
        print(f"\nBenchmarking insert operations:")
        
        size = 10000
        positions = ['beginning', 'middle', 'end']
        
        for pos in positions:
            # Python list
            if pos == 'beginning':
                index = 0
            elif pos == 'middle':
                index = size // 2
            else:
                index = size
            
            # Create initial list
            lst = list(range(size))
            
            start = time.perf_counter()
            for i in range(100):  # Insert 100 items
                if pos == 'end':
                    lst.append(i)
                else:
                    lst.insert(index, i)
            end = time.perf_counter()
            
            print(f"  Python list insert at {pos}: {end - start:.6f}s")
    
    def benchmark_access():
        """Benchmark random access operations."""
        print(f"\nBenchmarking random access:")
        
        size = 100000
        num_accesses = 10000
        
        # Create test data
        python_list = list(range(size))
        custom_array = DynamicArray()
        custom_array.extend(range(size))
        
        # Generate random indices
        indices = [random.randint(0, size - 1) for _ in range(num_accesses)]
        
        # Test Python list
        start = time.perf_counter()
        total = sum(python_list[i] for i in indices)
        end = time.perf_counter()
        python_time = end - start
        
        # Test custom array
        start = time.perf_counter()
        total = sum(custom_array[i] for i in indices)
        end = time.perf_counter()
        custom_time = end - start
        
        print(f"  Python list random access: {python_time:.6f}s")
        print(f"  DynamicArray random access: {custom_time:.6f}s")
        print(f"  Speedup ratio: {custom_time / python_time:.2f}x")
    
    def benchmark_memory():
        """Benchmark memory usage of different list implementations."""
        print(f"\nMemory usage comparison:")
        
        size = 100000
        
        # Python list
        python_list = list(range(size))
        python_memory = sys.getsizeof(python_list)
        
        # Custom dynamic array
        custom_array = DynamicArray()
        custom_array.extend(range(size))
        custom_memory = custom_array.memory_info()['memory_usage']
        
        # Array module (for comparison)
        int_array = array.array('i', range(size))
        array_memory = sys.getsizeof(int_array)
        
        print(f"  Python list ({size} elements): {python_memory:,} bytes")
        print(f"  DynamicArray ({size} elements): {custom_memory:,} bytes")
        print(f"  Array module ({size} elements): {array_memory:,} bytes")
        print(f"  Python list overhead: {python_memory / array_memory:.1f}x")
        print(f"  DynamicArray overhead: {custom_memory / array_memory:.1f}x")
    
    # Run all benchmarks
    benchmark_append()
    benchmark_insert()
    benchmark_access()
    benchmark_memory()


# ============================================================================
# SECTION 4: COMPARISON WITH OTHER DATA STRUCTURES
# ============================================================================

def compare_data_structures():
    """
    Compare lists with other linear data structures.
    """
    print(f"\n=== DATA STRUCTURE COMPARISON ===")
    
    def compare_operations():
        """Compare common operations across different structures."""
        size = 10000
        operations = 1000
        
        # Initialize structures
        python_list = list(range(size))
        deque_obj = deque(range(size))
        custom_array = DynamicArray()
        custom_array.extend(range(size))
        
        print(f"Comparing operations on {size} elements:")
        
        # Append operations
        times = {}
        
        # List append
        start = time.perf_counter()
        for i in range(operations):
            python_list.append(i)
        end = time.perf_counter()
        times['list_append'] = end - start
        
        # Deque append
        start = time.perf_counter()
        for i in range(operations):
            deque_obj.append(i)
        end = time.perf_counter()
        times['deque_append'] = end - start
        
        # Custom array append
        start = time.perf_counter()
        for i in range(operations):
            custom_array.append(i)
        end = time.perf_counter()
        times['custom_append'] = end - start
        
        print(f"  Append {operations} items:")
        for name, time_taken in times.items():
            print(f"    {name}: {time_taken:.6f}s")
        
        # Pop operations (from end)
        times = {}
        
        # List pop
        start = time.perf_counter()
        for i in range(min(operations, len(python_list))):
            python_list.pop()
        end = time.perf_counter()
        times['list_pop'] = end - start
        
        # Deque pop
        start = time.perf_counter()
        for i in range(min(operations, len(deque_obj))):
            deque_obj.pop()
        end = time.perf_counter()
        times['deque_pop'] = end - start
        
        # Custom array pop
        start = time.perf_counter()
        for i in range(min(operations, len(custom_array))):
            custom_array.pop()
        end = time.perf_counter()
        times['custom_pop'] = end - start
        
        print(f"  Pop {operations} items from end:")
        for name, time_taken in times.items():
            print(f"    {name}: {time_taken:.6f}s")
        
        # Pop from beginning (where deque shines)
        python_list = list(range(size))
        deque_obj = deque(range(size))
        
        # List pop from beginning (O(n) each)
        start = time.perf_counter()
        for i in range(min(100, len(python_list))):  # Fewer operations due to O(n²)
            python_list.pop(0)
        end = time.perf_counter()
        list_pop_left = end - start
        
        # Deque pop from beginning (O(1) each)
        start = time.perf_counter()
        for i in range(min(operations, len(deque_obj))):
            deque_obj.popleft()
        end = time.perf_counter()
        deque_pop_left = end - start
        
        print(f"  Pop from beginning:")
        print(f"    list_pop_left (100 ops): {list_pop_left:.6f}s")
        print(f"    deque_popleft ({operations} ops): {deque_pop_left:.6f}s")
        print(f"    Deque is ~{(list_pop_left * operations / 100) / deque_pop_left:.0f}x faster")
    
    compare_operations()


# ============================================================================
# SECTION 5: REAL-WORLD APPLICATIONS
# ============================================================================

def real_world_applications():
    """
    Demonstrate real-world applications of list data structures.
    """
    print(f"\n=== REAL-WORLD APPLICATIONS ===")
    
    def sliding_window_example():
        """Demonstrate sliding window technique using lists."""
        print("1. Sliding Window - Maximum in Window")
        
        def max_sliding_window(nums: List[int], k: int) -> List[int]:
            """Find maximum in each sliding window of size k."""
            if not nums or k <= 0:
                return []
            
            result = []
            for i in range(len(nums) - k + 1):
                window = nums[i:i + k]
                result.append(max(window))
            return result
        
        # Test data
        numbers = [1, 3, -1, -3, 5, 3, 6, 7]
        window_size = 3
        
        result = max_sliding_window(numbers, window_size)
        print(f"  Array: {numbers}")
        print(f"  Window size: {window_size}")
        print(f"  Max in each window: {result}")
    
    def dynamic_programming_example():
        """Demonstrate DP problem using lists for memoization."""
        print(f"\n2. Dynamic Programming - Fibonacci with Memoization")
        
        def fibonacci_dp(n: int) -> int:
            """Calculate nth Fibonacci number using DP with list."""
            if n <= 1:
                return n
            
            # Use list for memoization
            dp = [0, 1]
            
            for i in range(2, n + 1):
                dp.append(dp[i - 1] + dp[i - 2])
            
            return dp[n]
        
        # Calculate several Fibonacci numbers
        for i in range(10):
            fib = fibonacci_dp(i)
            print(f"  F({i}) = {fib}")
    
    def data_processing_pipeline():
        """Demonstrate data processing using list operations."""
        print(f"\n3. Data Processing Pipeline")
        
        # Sample data: student records
        students_data = [
            "Alice,85,92,78",
            "Bob,90,87,95",
            "Charlie,78,85,88",
            "Diana,95,98,92",
            "Eve,82,89,91"
        ]
        
        def process_student_data(raw_data: List[str]) -> List[dict]:
            """Process raw student data into structured format."""
            processed = []
            
            for line in raw_data:
                parts = line.split(',')
                if len(parts) >= 4:
                    name = parts[0]
                    scores = [int(score) for score in parts[1:]]
                    average = sum(scores) / len(scores)
                    
                    student = {
                        'name': name,
                        'scores': scores,
                        'average': average,
                        'grade': 'A' if average >= 90 else 'B' if average >= 80 else 'C'
                    }
                    processed.append(student)
            
            return processed
        
        # Process data
        students = process_student_data(students_data)
        
        # Sort by average (descending)
        students.sort(key=lambda x: x['average'], reverse=True)
        
        print("  Processed student data (sorted by average):")
        for student in students:
            print(f"    {student['name']}: {student['average']:.1f} ({student['grade']})")
        
        # Find top performers
        top_performers = [s for s in students if s['average'] >= 90]
        print(f"  Top performers (>= 90): {[s['name'] for s in top_performers]}")
    
    def inventory_management():
        """Demonstrate inventory management using lists."""
        print(f"\n4. Inventory Management System")
        
        class InventoryManager:
            def __init__(self):
                self.items = []
                self.transaction_log = []
            
            def add_item(self, item_id: str, name: str, quantity: int):
                """Add new item to inventory."""
                item = {
                    'id': item_id,
                    'name': name,
                    'quantity': quantity,
                    'reserved': 0
                }
                self.items.append(item)
                self.transaction_log.append(f"Added: {name} (qty: {quantity})")
            
            def find_item(self, item_id: str) -> Optional[dict]:
                """Find item by ID."""
                for item in self.items:
                    if item['id'] == item_id:
                        return item
                return None
            
            def update_quantity(self, item_id: str, change: int):
                """Update item quantity."""
                item = self.find_item(item_id)
                if item:
                    old_qty = item['quantity']
                    item['quantity'] += change
                    self.transaction_log.append(
                        f"Updated {item['name']}: {old_qty} -> {item['quantity']}"
                    )
                    return True
                return False
            
            def get_low_stock_items(self, threshold: int = 10) -> List[dict]:
                """Get items with low stock."""
                return [item for item in self.items if item['quantity'] < threshold]
            
            def get_total_value(self, price_map: dict) -> float:
                """Calculate total inventory value."""
                total = 0
                for item in self.items:
                    price = price_map.get(item['id'], 0)
                    total += price * item['quantity']
                return total
        
        # Demonstrate inventory management
        inventory = InventoryManager()
        
        # Add items
        inventory.add_item("LAPTOP001", "Gaming Laptop", 15)
        inventory.add_item("MOUSE001", "Wireless Mouse", 50)
        inventory.add_item("KEYBOARD001", "Mechanical Keyboard", 25)
        
        # Update quantities
        inventory.update_quantity("LAPTOP001", -3)  # Sold 3 laptops
        inventory.update_quantity("MOUSE001", -45)  # Sold 45 mice
        
        # Check low stock
        low_stock = inventory.get_low_stock_items(threshold=10)
        print("  Low stock items:")
        for item in low_stock:
            print(f"    {item['name']}: {item['quantity']} remaining")
        
        # Show recent transactions
        print("  Recent transactions:")
        for log_entry in inventory.transaction_log[-5:]:
            print(f"    {log_entry}")
    
    # Run all examples
    sliding_window_example()
    dynamic_programming_example()
    data_processing_pipeline()
    inventory_management()


# ============================================================================
# SECTION 6: TESTING AND VALIDATION
# ============================================================================

def test_implementations():
    """
    Comprehensive testing of list implementations.
    """
    print(f"\n=== TESTING AND VALIDATION ===")
    
    def test_dynamic_array():
        """Test DynamicArray implementation."""
        print("Testing DynamicArray implementation:")
        
        # Test basic operations
        arr = DynamicArray()
        
        # Test append and access
        for i in range(10):
            arr.append(i)
        
        assert len(arr) == 10, f"Length should be 10, got {len(arr)}"
        assert arr[0] == 0, f"First element should be 0, got {arr[0]}"
        assert arr[9] == 9, f"Last element should be 9, got {arr[9]}"
        
        # Test insert
        arr.insert(0, -1)
        assert arr[0] == -1, f"After insert, first element should be -1, got {arr[0]}"
        assert len(arr) == 11, f"Length should be 11 after insert, got {len(arr)}"
        
        # Test pop
        last = arr.pop()
        assert last == 9, f"Popped element should be 9, got {last}"
        assert len(arr) == 10, f"Length should be 10 after pop, got {len(arr)}"
        
        # Test remove
        arr.remove(-1)
        assert arr[0] != -1, f"First element should not be -1 after remove"
        assert len(arr) == 9, f"Length should be 9 after remove, got {len(arr)}"
        
        # Test index
        idx = arr.index(5)
        assert arr[idx] == 5, f"Index operation failed"
        
        print("  All DynamicArray tests passed!")
    
    def test_error_conditions():
        """Test error handling in implementations."""
        print("Testing error conditions:")
        
        arr = DynamicArray()
        
        # Test index errors
        try:
            arr[0]
            assert False, "Should raise IndexError for empty array"
        except IndexError:
            pass
        
        try:
            arr.pop()
            assert False, "Should raise IndexError for pop from empty array"
        except IndexError:
            pass
        
        # Add some elements
        arr.append(1)
        arr.append(2)
        
        try:
            arr[10]
            assert False, "Should raise IndexError for out of bounds access"
        except IndexError:
            pass
        
        try:
            arr.remove(100)
            assert False, "Should raise ValueError for removing non-existent element"
        except ValueError:
            pass
        
        print("  All error condition tests passed!")
    
    def test_consistency():
        """Test consistency between implementations."""
        print("Testing consistency between Python list and DynamicArray:")
        
        # Create parallel structures
        py_list = []
        custom_arr = DynamicArray()
        
        operations = [
            ('append', 1),
            ('append', 2),
            ('append', 3),
            ('insert', 0, 0),
            ('append', 4),
            ('pop',),
            ('remove', 2),
        ]
        
        for op in operations:
            if op[0] == 'append':
                py_list.append(op[1])
                custom_arr.append(op[1])
            elif op[0] == 'insert':
                py_list.insert(op[1], op[2])
                custom_arr.insert(op[1], op[2])
            elif op[0] == 'pop':
                py_val = py_list.pop()
                custom_val = custom_arr.pop()
                assert py_val == custom_val, f"Pop mismatch: {py_val} vs {custom_val}"
            elif op[0] == 'remove':
                py_list.remove(op[1])
                custom_arr.remove(op[1])
            
            # Check length consistency
            assert len(py_list) == len(custom_arr), f"Length mismatch after {op}"
            
            # Check element consistency
            for i in range(len(py_list)):
                assert py_list[i] == custom_arr[i], f"Element mismatch at index {i}"
        
        print("  Consistency tests passed!")
    
    # Run all tests
    test_dynamic_array()
    test_error_conditions()
    test_consistency()


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """
    Main function to run all demonstrations and tests.
    """
    print("Lists Implementation - Comprehensive Demonstration")
    print("=" * 55)
    
    try:
        # Run all demonstrations
        builtin_list_analysis()
        demonstrate_dynamic_array()
        benchmark_list_operations()
        compare_data_structures()
        real_world_applications()
        test_implementations()
        
    except Exception as e:
        print(f"Error during execution: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        print(f"\n{'=' * 55}")
        print("Lists implementation demonstration complete!")
        print(f"Python version: {sys.version}")


if __name__ == "__main__":
    main()


# ============================================================================
# PRACTICE EXERCISES
# ============================================================================

"""
PRACTICE EXERCISES:

1. Implement a CircularArray that wraps around when reaching capacity.

2. Create a SortedArray that maintains elements in sorted order.

3. Implement a ResizableArray with different growth strategies:
   - Linear growth (add fixed amount)
   - Exponential growth (multiply by factor)
   - Fibonacci growth

4. Build a CompressedArray for storing boolean values efficiently.

5. Implement a MultiTypeArray that can store different data types.

6. Create a ThreadSafeArray with proper synchronization.

7. Build a LazyArray that computes elements on-demand.

8. Implement a BitArray for efficient boolean storage.

9. Create a MemoryMappedArray for very large datasets.

10. Build a DistributedArray that spans multiple machines.

ALGORITHM CHALLENGES:

1. Implement merge operation for two sorted arrays.
2. Find the kth largest element without sorting.
3. Rotate array elements by k positions.
4. Find longest increasing subsequence.
5. Implement array-based stack and queue.
6. Find all triplets that sum to zero.
7. Implement sliding window maximum.
8. Find peak element in array.
9. Merge overlapping intervals.
10. Find majority element in array.

OPTIMIZATION CHALLENGES:

1. Minimize memory allocations in dynamic array.
2. Implement cache-friendly array operations.
3. Optimize for different access patterns.
4. Implement memory pool for array allocation.
5. Create SIMD-optimized array operations.

DESIGN PATTERNS:

1. Iterator pattern for array traversal.
2. Strategy pattern for different growth strategies.
3. Template method for common array operations.
4. Observer pattern for array change notifications.
5. Command pattern for undoable array operations.
"""
