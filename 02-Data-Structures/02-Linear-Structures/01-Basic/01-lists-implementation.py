"""
# ==============================================================================
# LABORATORY: LISTS (DYNAMIC ARRAYS)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# The Python `list` is the most used data structure in the language. However, 
# it is NOT a linked list; it is a Dynamic Array of pointers. Misunderstanding 
# this leads to disastrous performance (e.g., using `insert(0, x)` in a loop).
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Prove that Python lists over-allocate memory to achieve O(1) appends.
# - Demonstrate the performance destruction of O(N) operations like `pop(0)`.
# - Implement a custom lightweight Dynamic Array class to understand the C-level mechanics.
# - Master List slicing, reversing, and sorting mechanics.
#
# ==============================================================================
"""

import sys
import timeit
import ctypes
from typing import Any

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. PROVING OVER-ALLOCATION (O(1) AMORTIZED APPENDS)
# ==============================================================================
def demonstrate_over_allocation():
    """
    If lists allocated memory exactly for their size, appending an item would 
    require copying the entire array every time (O(N)). Instead, Python 
    allocates extra "buffer" space. When the buffer fills, it creates a new 
    buffer ~1.125x larger.
    """
    section_header("List Memory Over-Allocation")
    
    data = []
    print("Watch the memory allocation jump in steps, not smoothly:")
    
    prev_size = sys.getsizeof(data)
    print(f"Length: 0, Size: {prev_size} bytes")
    
    for i in range(1, 25):
        data.append(i)
        curr_size = sys.getsizeof(data)
        
        # Only print when the underlying C-array physically resizes
        if curr_size != prev_size:
            print(f"Length: {i:<2} | Resized from {prev_size} to {curr_size} bytes")
            prev_size = curr_size


# ==============================================================================
# 4. THE O(N) PERFORMANCE TRAP (POP AND INSERT)
# ==============================================================================
def demonstrate_performance_traps():
    """
    Because a list is a contiguous array, removing from or inserting into the 
    front requires shifting EVERY other element.
    """
    section_header("Performance Traps: pop(0) and insert(0)")
    
    N = 50_000
    
    # 1. Pop from the end (O(1))
    def fast_pop():
        lst = list(range(N))
        while lst:
            lst.pop() # Pops from index -1
            
    # 2. Pop from the front (O(N))
    def slow_pop():
        lst = list(range(N))
        while lst:
            lst.pop(0) # Forces N-1 elements to shift left
            
    print(f"Testing with N={N} elements...")
    
    t_fast = timeit.timeit(fast_pop, number=1)
    t_slow = timeit.timeit(slow_pop, number=1)
    
    print(f"pop()  [O(1) back] : {t_fast:.5f} seconds")
    print(f"pop(0) [O(N) front]: {t_slow:.5f} seconds")
    print(f"-> pop(0) is {t_slow/t_fast:.0f}x slower. NEVER use a list as a queue!")


# ==============================================================================
# 5. BUILDING A CUSTOM DYNAMIC ARRAY (UNDER THE HOOD)
# ==============================================================================
class CustomDynamicArray:
    """
    A simplified recreation of Python's list behavior using raw C-style arrays.
    """
    def __init__(self):
        self.count = 0        # Actual number of elements
        self.capacity = 1     # Allocated physical slots
        self.array = self._make_array(self.capacity)
        
    def __len__(self):
        return self.count
        
    def __getitem__(self, index):
        if not 0 <= index < self.count:
            raise IndexError("Index out of bounds")
        return self.array[index]
        
    def append(self, element: Any):
        # 1. Check if capacity is exhausted
        if self.count == self.capacity:
            self._resize(2 * self.capacity) # Double the capacity
            
        # 2. Add the element
        self.array[self.count] = element
        self.count += 1
        
    def _resize(self, new_capacity: int):
        print(f"  [CustomArray] Resizing capacity from {self.capacity} to {new_capacity}")
        new_array = self._make_array(new_capacity)
        
        # Copy existing elements
        for i in range(self.count):
            new_array[i] = self.array[i]
            
        self.array = new_array
        self.capacity = new_capacity
        
    def _make_array(self, capacity: int):
        # Creates a raw C-array using the ctypes module
        return (capacity * ctypes.py_object)()

def demonstrate_custom_array():
    section_header("Custom Dynamic Array Implementation")
    
    arr = CustomDynamicArray()
    for i in range(5):
        print(f"Appending {i}...")
        arr.append(i)
        
    print(f"Final internal capacity: {arr.capacity}, Actual items: {len(arr)}")


# ==============================================================================
# 6. SLICING, REVERSING, AND SORTING
# ==============================================================================
def demonstrate_list_mechanics():
    section_header("List Mechanics: Slicing and Sorting")
    
    lst = [10, 20, 30, 40, 50]
    
    # 1. Slicing creates a SHALLOW copy in O(K) time where K is the slice length
    slice_copy = lst[1:4]
    print(f"Slice [1:4]: {slice_copy}")
    
    # 2. Reversing
    # Option A: In-place O(N) reverse
    lst.reverse()
    print(f"In-place reverse: {lst}")
    
    # Option B: Out-of-place O(N) slice reverse
    # This creates a brand new list in memory.
    new_reversed = lst[::-1]
    
    # 3. Sorting (Timsort: O(N log N))
    # Option A: In-place
    lst.sort()
    
    # Option B: Out-of-place (returns a new list)
    new_sorted = sorted([5, 1, 9, 3])
    print(f"Out-of-place sorted: {new_sorted}")


# ==============================================================================
# 7. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why does `sys.getsizeof()` jump in large blocks when appending to a list?
   Answer: Python dynamically over-allocates the underlying C-array to provide O(1) amortized appends. Without over-allocation, every append would require a full O(N) copy of the array.

2. Why should you never use `list.insert(0, x)` or `list.pop(0)`?
   Answer: Python lists are contiguous arrays. Inserting or deleting at the front requires physically shifting every other element in memory, making it an O(N) operation. For front-operations, use `collections.deque`.

3. What sorting algorithm does Python use, and what is its time complexity?
   Answer: Timsort (a hybrid of Merge Sort and Insertion Sort). Its worst-case and average-case time complexity is O(N log N), but its best-case (already sorted data) is O(N).
"""

if __name__ == "__main__":
    demonstrate_over_allocation()
    demonstrate_performance_traps()
    demonstrate_custom_array()
    demonstrate_list_mechanics()
    print("\n[SUCCESS] Laboratory: Lists Completed.")
