"""
# ==============================================================================
# LABORATORY: ARRAYS (PYTHON VS C-ARRAYS VS NUMPY)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A Python `list` is an array of pointers to objects. This causes massive memory 
# bloat (28 bytes overhead per integer) and terrible Cache Locality. If you need 
# to process a billion numbers, you MUST use contiguous memory structures.
# Understanding the standard `array` module and the third-party `numpy` library 
# is the gateway to High-Performance Computing and Data Science.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the memory difference between `list` and `array.array`.
# - Implement a basic `array.array` (Unboxed primitive types).
# - Understand how Vectorization in `numpy` bypasses Python loops entirely.
# - Demonstrate performance differences for mathematical operations.
#
# ==============================================================================
"""

import sys
import array
import timeit

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE STANDARD ARRAY MODULE (UNBOXED TYPES)
# ==============================================================================
def demonstrate_array_module():
    """
    Python's built-in `array` module creates a contiguous block of memory 
    containing the raw C-primitives (e.g., 4-byte integers), NOT pointers 
    to 28-byte Python objects.
    """
    section_header("Python's Built-in array Module")
    
    # We must specify a "type code". 'i' stands for signed integer (usually 4 bytes).
    # 'd' stands for double precision float (8 bytes).
    c_array = array.array('i', [1, 2, 3, 4, 5])
    py_list = [1, 2, 3, 4, 5]
    
    print(f"List object: {py_list}")
    print(f"Array object: {c_array}")
    
    # Memory Comparison (For a large amount of data)
    N = 1_000_000
    large_list = list(range(N))
    large_array = array.array('i', range(N))
    
    # sys.getsizeof on a list ONLY measures the array of pointers (8MB).
    # It DOES NOT measure the 1,000,000 integer objects in the heap (28MB).
    # So the list actually consumes ~36MB total.
    list_pointer_size = sys.getsizeof(large_list)
    
    # sys.getsizeof on an array measures the ENTIRE contiguous memory block,
    # because the raw integers are stored directly inside the array structure!
    array_total_size = sys.getsizeof(large_array)
    
    print(f"\nMemory for {N:,} items:")
    print(f"List (Pointers ONLY): {list_pointer_size:,} bytes")
    print(f"Array (Total memory): {array_total_size:,} bytes")
    
    # Type checking
    try:
        c_array.append("hello") # type: ignore
    except TypeError as e:
        print(f"\nArray Type Safety Caught Error: {e}")


# ==============================================================================
# 4. NUMPY & VECTORIZATION (CONCEPTUAL)
# ==============================================================================
def demonstrate_vectorization():
    """
    While `array.array` saves memory, you still have to use a Python `for` loop 
    to do math on it, which is slow.
    NumPy (not built-in, but essential) allows you to apply mathematical 
    operations to the ENTIRE array at once at the C-level (Vectorization), 
    completely bypassing the Python interpreter.
    """
    section_header("Vectorization vs Python Loops")
    
    N = 1_000_000
    
    # 1. Pure Python approach
    data_list = list(range(N))
    def pure_python_math():
        result = []
        for x in data_list:
            result.append(x * 2)
        return result
        
    # We will simulate NumPy using list comprehensions just to show the loop timing.
    # In a real environment, you would run: `import numpy as np; arr = np.arange(N); arr * 2`
    
    print("If you want to multiply 1,000,000 numbers by 2:")
    
    py_time = timeit.timeit(pure_python_math, number=10)
    print(f"Python `for` loop time: {py_time:.4f} seconds")
    
    print("\nIn NumPy, you would simply write: `arr * 2`")
    print("NumPy passes the contiguous C-array directly to the CPU utilizing SIMD")
    print("(Single Instruction, Multiple Data) registers, executing in <0.01 seconds.")


# ==============================================================================
# 5. WHEN TO USE WHICH?
# ==============================================================================
def demonstrate_decision_tree():
    section_header("Array Decision Tree")
    print("""
1. Do you have mixed data types (integers, strings, objects)?
   -> USE: list
   
2. Do you have a massive list of numbers and want to save RAM, but only need 
   to iterate over it, append to it, or pass it to a C-library?
   -> USE: array.array
   
3. Do you have a massive list of numbers and need to perform heavy mathematical 
   operations (linear algebra, matrix multiplication, statistics)?
   -> USE: NumPy (numpy.ndarray)
   
4. Do you need to insert/delete items from the middle or front frequently?
   -> USE: None of the above! (Arrays are terrible for this). Use a Linked List.
    """)


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why is `array.array` much more memory-efficient than a `list`?
   Answer: A `list` stores 8-byte pointers to 28-byte Python objects scattered in the heap (massive overhead). An `array.array` stores raw C-primitives (like a 4-byte integer) directly in a single contiguous block of memory.

2. What does Vectorization mean in the context of NumPy?
   Answer: Instead of using a Python `for` loop (which carries dynamic type checking and interpreter overhead for every single item), Vectorization pushes the entire operation down to the C-level, applying the math to the contiguous array simultaneously using CPU SIMD instructions.

3. Can an `array.array` hold mixed data types?
   Answer: No. When creating an `array`, you must specify a type code (like 'i' for integers or 'd' for floats). It can only hold unboxed primitives of that specific type.
"""

if __name__ == "__main__":
    demonstrate_array_module()
    demonstrate_vectorization()
    demonstrate_decision_tree()
    print("\n[SUCCESS] Laboratory: Arrays Completed.")
