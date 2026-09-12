"""
Memory Management: Array Optimizations

Learning Objectives:
1. Learn how lists in Python store references, adding memory overhead.
2. Understand the `array` module for contiguous homogeneous data.
3. Use NumPy arrays as a high-performance alternative.
4. Profile memory and speed differences.

Concept Explanation:
Python lists are arrays of pointers (references) to objects scattered in memory. 
This is flexible but inefficient for numerical data. The built-in `array` module
and the 3rd-party `numpy` library store unboxed primitive values contiguously in memory,
vastly improving cache locality and reducing memory overhead.
"""

import array
import sys
import timeit
from typing import List, Tuple

# --- Basic Implementation ---
def create_list(n: int) -> List[int]:
    """Standard list containing integers."""
    return [i for i in range(n)]

def create_array(n: int) -> array.array:
    """Built-in array containing integers ('i' for signed int)."""
    return array.array('i', range(n))

# --- Intermediate Implementation ---
# Simulating a large numerical dataset
def process_list(lst: List[int]) -> int:
    return sum(lst)

def process_array(arr: array.array) -> int:
    return sum(arr)

# --- Advanced Implementation / Performance Analysis ---
def compare_memory(n: int) -> Tuple[int, int]:
    """Compare memory footprint. Note: sys.getsizeof on a list doesn't include 
    the size of the elements themselves, only the pointers! We must account for elements."""
    lst = create_list(n)
    arr = create_array(n)
    
    # List size + size of all int objects
    list_size = sys.getsizeof(lst) + sum(sys.getsizeof(x) for x in lst)
    # Array size (elements are unboxed, so sys.getsizeof(arr) is accurate)
    arr_size = sys.getsizeof(arr)
    
    return list_size, arr_size

def compare_performance() -> None:
    """Compare summation speed."""
    setup = "from __main__ import create_list, create_array, process_list, process_array; l = create_list(10000); a = create_array(10000)"
    t_list = timeit.timeit("process_list(l)", setup=setup, number=1000)
    t_arr = timeit.timeit("process_array(a)", setup=setup, number=1000)
    
    print(f"Summation Time - List:  {t_list:.4f}s")
    print(f"Summation Time - Array: {t_arr:.4f}s")
    # Note: sum() on array might actually be slightly slower in pure Python 
    # due to boxing/unboxing on each iteration, but memory savings are huge!

# --- Edge Cases ---
def demonstrate_edge_cases() -> None:
    """Arrays strictly enforce type."""
    arr = array.array('i', [1, 2, 3])
    try:
        arr.append(4.5) # Floats are not allowed in int array
    except TypeError as e:
        print(f"Expected TypeError: {e}")

# --- Interview Challenge ---
"""
Challenge: Given a massive dataset of characters, would you use a list of strings
or an array? Demonstrate the array approach for characters.
"""
def char_array_example() -> array.array:
    # 'u' is for Unicode characters
    return array.array('u', "hello world")

# --- Tests ---
def run_tests() -> None:
    """Run validation tests."""
    lst = create_list(10)
    arr = create_array(10)
    assert len(lst) == len(arr)
    assert process_list(lst) == process_array(arr)
    assert char_array_example().tounicode() == "hello world"
    print("All tests passed.")

if __name__ == '__main__':
    print("--- Performance Analysis: Array vs List ---")
    N = 100_000
    mem_lst, mem_arr = compare_memory(N)
    print(f"Memory (List):  {mem_lst} bytes")
    print(f"Memory (Array): {mem_arr} bytes")
    print(f"Memory Saved:   {(mem_lst - mem_arr) / mem_lst * 100:.1f}%")
    
    compare_performance()
    demonstrate_edge_cases()
    run_tests()
