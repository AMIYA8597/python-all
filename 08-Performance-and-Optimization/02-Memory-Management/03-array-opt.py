"""
# ==============================================================================
# LABORATORY: PERFORMANCE AND OPTIMIZATION (MEMORY MANAGEMENT - ARRAYS & BUFFERS)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A standard Python `list` is not an array; it is a dynamically-sized, 
# heterogeneous Array of Pointers. If you store 1,000,000 integers in a Python 
# list, you are allocating 1,000,000 pointer references AND 1,000,000 separate 
# Integer objects scattered across RAM, resulting in catastrophic memory bloat 
# and terrible CPU Cache locality.
#
# A junior engineer uses a `list` to process 10 GB of binary sensor data. The 
# pointer overhead balloons the memory to 40 GB, crashing the server.
#
# A senior engineer imports the `array` module, enforcing strict C-types 
# (e.g., 32-bit signed integers). This forces Python to pack the raw binary 
# data contiguously in a single block of RAM, entirely eliminating the object 
# and pointer overhead, reducing memory by 80% and drastically increasing speed.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master contiguous memory packing using the `array` module.
# - Master zero-copy memory manipulation using `memoryview`.
# - Prove the CPU Cache efficiency of raw C-types over Python objects.
#
# ==============================================================================
"""

import sys
import array
import timeit

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. PYTHON LISTS VS C-ARRAYS (MEMORY OVERHEAD)
# ==============================================================================
def demonstrate_array_memory():
    section_header("Memory Overhead: List (Pointers) vs Array (Contiguous C-Types)")
    
    # We want to store 10,000,000 integers.
    N = 10_000_000
    print(f"  Allocating {N:,} elements...")
    
    # --- 1. THE PYTHON LIST (Catastrophic Overhead) ---
    py_list = list(range(N))
    
    # The list object itself just stores 10,000,000 memory pointers (8 bytes each on 64-bit).
    list_pointer_size = sys.getsizeof(py_list)
    
    # We must also account for the size of the ACTUAL integer objects in RAM!
    # In Python 3, a standard integer is 28 bytes.
    int_obj_size = sys.getsizeof(0)
    total_list_memory = list_pointer_size + (N * int_obj_size)
    
    # --- 2. THE C-ARRAY (Contiguous Packing) ---
    # The 'i' typecode forces the array to use raw 32-bit (4 bytes) signed C-integers.
    # There are NO pointers, and NO Python Integer Objects! Just raw binary data.
    c_array = array.array('i', range(N))
    total_array_memory = sys.getsizeof(c_array)
    
    print("\n  [PYTHON LIST (Array of Pointers)]")
    print(f"    -> Pointer Array Size:   {list_pointer_size / (1024*1024):.2f} MB")
    print(f"    -> Integer Objects Size: {(N * int_obj_size) / (1024*1024):.2f} MB")
    print(f"    -> TOTAL RAM CONSUMED:   {total_list_memory / (1024*1024):.2f} MB")
    
    print("\n  [C-ARRAY (Contiguous Packed Ints)]")
    print(f"    -> TOTAL RAM CONSUMED:   {total_array_memory / (1024*1024):.2f} MB")
    
    savings = ((total_list_memory - total_array_memory) / total_list_memory) * 100
    print(f"\n  [CONCLUSION] The `array` module reduced RAM consumption by {savings:.2f}%!")


# ==============================================================================
# 4. ZERO-COPY MANIPULATION WITH MEMORYVIEW
# ==============================================================================
def demonstrate_memoryview():
    section_header("Zero-Copy Optimization with `memoryview`")
    
    # A massive chunk of binary data (e.g., a 50 MB image file in RAM)
    raw_data = bytearray(b"A" * 50_000_000)
    print(f"  [INIT] Allocated 50 MB Bytearray.")
    
    # SCENARIO: We need to process the second half of the data.
    
    # --- NAIVE APPROACH (The Memory Spike) ---
    # Slicing a bytearray in Python creates a massive physical COPY in RAM!
    print("\n  [NAIVE SLICING]")
    start = timeit.default_timer()
    chunk_copy = raw_data[25_000_000:]
    end = timeit.default_timer()
    print(f"    -> Executed standard slice: raw_data[25M:]")
    print(f"    -> Time Taken: {(end - start) * 1000:.4f} ms")
    print(f"    -> CAUTION: We just physically copied 25 MB of RAM! (Total RAM: 75 MB)")
    
    # --- OPTIMAL APPROACH (Zero-Copy) ---
    # `memoryview` creates a purely mathematical window over the existing data.
    # It does not copy a single byte of memory.
    print("\n  [OPTIMAL MEMORYVIEW]")
    start = timeit.default_timer()
    mview = memoryview(raw_data)
    zero_copy_chunk = mview[25_000_000:]
    end = timeit.default_timer()
    print(f"    -> Executed memoryview slice: mview[25M:]")
    print(f"    -> Time Taken: {(end - start) * 1000:.4f} ms")
    print(f"    -> SUCCESS: Zero bytes copied! Perfect O(1) Time and Space. (Total RAM: 50 MB)")
    
    # PROOF OF REFERENCE
    print("\n  [MUTABILITY PROOF]")
    print(f"    -> Data at index 25,000,000 before edit: {chr(raw_data[25_000_000])}")
    zero_copy_chunk[0] = ord('Z')
    print("    -> Modified the zero_copy_chunk[0] to 'Z'...")
    print(f"    -> Data at index 25,000,000 after edit:  {chr(raw_data[25_000_000])}")
    print("    (The memoryview mathematically edits the original buffer!)")


def run_all_labs():
    demonstrate_array_memory()
    demonstrate_memoryview()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "Why does a Python `list` containing 1,000,000 integers consume significantly more memory than a C-array, and how does this impact CPU performance?"
   Senior Answer: "A Python `list` is a heterogeneous Array of Pointers. It must support storing an integer, a string, and an object simultaneously. To achieve this, it stores 1,000,000 memory addresses (pointers). The actual integers are full Python Objects (`PyLongObject` in C), which require 28 bytes each for reference counts and type information, and are scattered randomly across the heap. This causes catastrophic CPU Cache Misses. The `array` module restricts the structure to a single C-type (like a 4-byte integer). Python packs these raw bytes contiguously into a single block of RAM, entirely eliminating the 28-byte object overhead and the pointers, while mathematically guaranteeing perfect L1/L2 Cache Locality."

2. Interviewer: "If the `array` module is so much more memory-efficient, why do Data Scientists exclusively use `numpy` arrays instead?"
   Senior Answer: "The standard library `array` module solves the memory problem by packing data contiguously, but it does NOT solve the compute problem. If you try to multiply every element in an `array` by $2$, the CPython interpreter must still iterate through the array using a Python `for` loop, dynamically boxing each raw C-integer back into a Python Object, performing the math, and unboxing it, which is painfully slow. `numpy` arrays are not only contiguous in RAM, but they expose a vectorized C-API. When you do `arr * 2` in numpy, the operation is physically pushed down into highly optimized, compiled C/C++ loops (often utilizing SIMD CPU instructions) that bypass the Python Interpreter entirely, executing orders of magnitude faster."

3. Interviewer: "What is `memoryview`, and how does it prevent the 'Memory Spike' problem in high-throughput network applications?"
   Senior Answer: "When receiving a massive TCP network payload or reading an image file in Python, developers often need to parse specific chunks (e.g., stripping the 20-byte header off a 50 MB payload). Standard Python slicing (`payload[20:]`) forcefully duplicates the 50 MB chunk into a brand new memory allocation. If 10 concurrent requests arrive, the server's RAM violently spikes by 500 MB, potentially triggering an OOM (Out-of-Memory) crash. `memoryview` leverages the C-level 'Buffer Protocol'. It creates a lightweight, $O(1)$ mathematical window that simply points to the original memory block with an offset. Slicing a `memoryview` creates another pointer, copying absolutely zero bytes of the underlying data, completely immunizing the server against memory spikes."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Memory Management (Arrays & Buffers) Completed.")
