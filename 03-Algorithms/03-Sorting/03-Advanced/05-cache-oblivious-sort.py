"""
# ==============================================================================
# LABORATORY: CACHE-OBLIVIOUS ALGORITHMS
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# In standard Big-O notation, we assume every memory read takes the exact same 
# amount of time. This is called the "RAM Model". 
# 
# In the real world, this is FALSE. Modern CPUs have a memory hierarchy:
# - L1 Cache: ~1 nanosecond (Tiny, ~64 KB)
# - L2 Cache: ~3 nanoseconds (Medium, ~512 KB)
# - L3 Cache: ~15 nanoseconds (Large, ~16 MB)
# - Main RAM: ~100 nanoseconds (Massive, ~16 GB)
#
# If your algorithm jumps randomly across memory (like Heap Sort or Linked Lists), 
# it causes "Cache Misses", forcing the CPU to wait 100ns for main RAM every time.
#
# "Cache-Aware" algorithms fix this by explicitly tuning parameters (like chunk sizes) 
# to perfectly fit into the L1 cache. But if you move the code to a different CPU, 
# it breaks!
#
# "Cache-Oblivious" algorithms are mathematically designed to optimally use the 
# CPU cache without ever explicitly knowing the size of the cache! They scale 
# dynamically across ANY hardware.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the External Memory Model (Disk/RAM/Cache transfers).
# - Understand why Divide & Conquer is naturally Cache-Oblivious.
# - Concept: The Cache-Oblivious Matrix Transpose.
#
# ==============================================================================
"""

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE DIVIDE & CONQUER MIRACLE
# ==============================================================================
def explain_divide_and_conquer():
    section_header("Concept: Why Recursion is Cache-Oblivious")
    print("""
Standard Merge Sort splits an array in half until it reaches size 1.

Imagine we have an array of 100 Million items. The CPU Cache can only hold 1,000 items.

When Merge Sort begins, it splits 100M -> 50M -> 25M. 
At this point, it is causing massive Cache Misses because 25M items do not fit 
in the cache. It is thrashing RAM.

BUT... it keeps dividing!
Eventually, the recursive calls reach a sub-array of size 500.
Suddenly, magic happens. The ENTIRE 500-item sub-array fits perfectly into the 
CPU's L1 cache! 

The next recursive splits (500 -> 250 -> 125 -> 62 -> 31) and all of their 
subsequent MERGE operations happen ENTIRELY inside the lightning-fast L1 Cache, 
without ever touching main RAM!

Did we write a line of code saying `if size <= 1000: use_l1_cache()`?
NO!
The algorithm is *Cache-Oblivious*. It naturally tuned itself to the hardware 
simply by using the Divide & Conquer paradigm. If you move this code to a CPU 
with a 5,000 item cache, it will automatically start working in cache at the 
2,500 split.
    """)


# ==============================================================================
# 4. CACHE-OBLIVIOUS MATRIX ALGORITHMS
# ==============================================================================
def cache_ignorant_transpose(matrix, n):
    """
    Standard matrix transposition.
    matrix[i][j] = matrix[j][i]
    
    If N is massive (e.g., 10,000x10,000), iterating column-by-column causes 
    a Cache Miss on EVERY SINGLE read, because 2D arrays are stored as a 1D 
    contiguous block in C/RAM. Jumping down a column means jumping exactly 
    `N` memory addresses forward, entirely skipping the CPU Cache lines!
    """
    # This is O(N^2) time mathematically, but will run terribly slow.
    pass


def cache_oblivious_transpose(matrix, n, row_start, col_start, size):
    """
    Cache-Oblivious Transpose using Divide and Conquer.
    Instead of iterating row-by-row, we divide the matrix into 4 quadrants.
    We recursively divide the quadrants until they are tiny blocks (e.g. 2x2).
    
    When the recursion hits a small enough block, that ENTIRE 2D block fits 
    perfectly inside a single CPU Cache line! We can transpose the tiny block 
    with zero cache misses!
    """
    if size <= 16:
        # Base case: The block is so small it fits entirely in L1 Cache.
        # Transpose it natively here using standard loops.
        pass
    else:
        # Divide into 4 sub-quadrants
        half = size // 2
        # Top-Left Quadrant
        cache_oblivious_transpose(matrix, n, row_start, col_start, half)
        # Top-Right Quadrant
        cache_oblivious_transpose(matrix, n, row_start, col_start + half, half)
        # Bottom-Left Quadrant
        cache_oblivious_transpose(matrix, n, row_start + half, col_start, half)
        # Bottom-Right Quadrant
        cache_oblivious_transpose(matrix, n, row_start + half, col_start + half, half)


def demonstrate_cache_oblivious():
    section_header("Algorithm: Cache-Oblivious Sorting (Funnel Sort)")
    print("""
While Merge Sort is naturally cache-oblivious for the lower levels of the tree, 
the final massive merge (merging two 50-Million item arrays) STILL causes heavy 
cache misses.

To solve this, researchers invented "Funnel Sort" and "Cache-Oblivious Distribution Sort".

Funnel Sort uses a complex "K-Funnel" data structure. It acts like a massive 
Merge Sort, but it buffers the incoming streams into tiny queues that perfectly 
fit into cache lines. It mathematically guarantees the optimal number of memory 
transfers O( (N/B) * log_{M/B}(N/B) ) where B is the block size and M is the 
cache size, WITHOUT ever knowing M or B in the code!

These algorithms are incredibly complex to implement and are generally relegated 
to theoretical computer science and highly specialized math libraries (like BLAS 
or LAPACK for Matrix operations).
    """)


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. What is the difference between Cache-Aware and Cache-Oblivious?
   Answer: A Cache-Aware algorithm has explicit hardcoded variables for the hardware (e.g., `CACHE_SIZE = 64000`). If the hardware changes, the code must be rewritten. A Cache-Oblivious algorithm achieves the exact same optimal cache performance purely through algorithmic structure (usually Divide and Conquer), meaning it auto-scales to any hardware instantly.

2. Why do Arrays have better cache performance than Linked Lists?
   Answer: Locality of Reference. When a CPU reads a byte from RAM, it doesn't just read 1 byte. It pulls a "Cache Line" (usually 64 contiguous bytes) into the L1 cache. Because an Array is contiguous, reading `arr[0]` instantly pulls `arr[1]` through `arr[15]` into the ultra-fast cache. A Linked List scatters nodes randomly in RAM, meaning `node.next` will almost certainly cause a Cache Miss, forcing the CPU to wait for main RAM again.

3. Why did Heap Sort fail the cache test?
   Answer: Heap Sort accesses memory using the formula `2*i + 1`. If `i` is 1 Million, the CPU jumps exactly 1 Million addresses forward. This guarantees the data will not be in the current 64-byte cache line. Quick Sort uses a sliding window (two pointers moving sequentially), which is perfectly contiguous and maximizes cache hits.
"""

if __name__ == "__main__":
    explain_divide_and_conquer()
    demonstrate_cache_oblivious()
    print("\n[SUCCESS] Laboratory: Cache-Oblivious Concepts Completed.")
