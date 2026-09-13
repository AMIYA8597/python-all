"""
# ==============================================================================
# LABORATORY: SHELL SORT & THE MATH OF GAP SEQUENCES
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Donald Shell invented Shell Sort in 1959. It is essentially Insertion Sort, 
# but it moves elements across large "Gaps" instead of just 1 slot at a time.
#
# But there is a massive open question in computer science: "What should the gaps be?"
#
# Shell's original sequence was N/2, N/4, N/8... down to 1.
# This seems logical, but it has a mathematically catastrophic flaw. If the gaps 
# are even numbers, the odd indices and even indices NEVER interact with each 
# other until the very final gap of 1! This degrades the sort to O(N^2) worst-case.
#
# Over the decades, mathematicians have proposed better Gap Sequences:
# - Hibbard (1963): 1, 3, 7, 15... (2^k - 1). Time: O(N^(3/2))
# - Pratt (1971): 1, 2, 3, 4, 6, 8, 9... (2^p * 3^q). Time: O(N log^2 N)
# - Sedgewick (1982): 1, 8, 23, 77, 281... Time: O(N^(4/3))
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand why Shell's original gap sequence fails.
# - Implement Hibbard's Gap Sequence.
# - Implement Sedgewick's Gap Sequence.
# - Master the generalized Gapped Insertion algorithm.
#
# ==============================================================================
"""

import math
from typing import List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE GAPPED INSERTION ENGINE
# ==============================================================================
def execute_gaps(arr: List[int], gaps: List[int]) -> List[int]:
    """
    The core engine of Shell Sort. It takes any arbitrary list of gap sizes 
    and executes the gapped insertion logic.
    """
    n = len(arr)
    comparisons = 0
    
    for gap in gaps:
        if gap >= n:
            continue
            
        print(f" Executing Gap size: {gap}")
        for i in range(gap, n):
            key = arr[i]
            j = i
            
            comparisons += 1
            while j >= gap and arr[j - gap] > key:
                arr[j] = arr[j - gap]
                j -= gap
                if j >= gap: comparisons += 1
                
            arr[j] = key
            
    print(f" Total Comparisons: {comparisons}")
    return arr


# ==============================================================================
# 4. GAP SEQUENCE GENERATORS
# ==============================================================================
def shell_sort_original(arr: List[int]) -> None:
    """
    Donald Shell's 1959 sequence: N/2, N/4, N/8... 1.
    Worst-case time: O(N^2) (due to the even-odd interaction flaw).
    """
    n = len(arr)
    gaps = []
    curr = n // 2
    while curr > 0:
        gaps.append(curr)
        curr //= 2
        
    print(f"Shell's Original Sequence: {gaps}")
    execute_gaps(arr, gaps)

def shell_sort_hibbard(arr: List[int]) -> None:
    """
    Hibbard's 1963 sequence: 2^k - 1 (1, 3, 7, 15, 31, 63...)
    Worst-case time: O(N^(3/2))
    Because the gaps are guaranteed to be ODD, elements interact much earlier!
    """
    n = len(arr)
    gaps = []
    k = 1
    while (2**k - 1) < n:
        gaps.append(2**k - 1)
        k += 1
        
    # Reverse it so we process largest gaps down to 1
    gaps.reverse()
    print(f"Hibbard's Sequence: {gaps}")
    execute_gaps(arr, gaps)

def shell_sort_sedgewick(arr: List[int]) -> None:
    """
    Sedgewick's 1982 sequence (used in many modern implementations).
    Formula merges two sequences: 9*(4^k) - 9*(2^k) + 1  and  4^k - 3*(2^k) + 1
    Worst-case time: O(N^(4/3))
    """
    n = len(arr)
    gaps = []
    k = 0
    while True:
        # Sedgewick formula for even indices
        gap1 = 9 * (4**k) - 9 * (2**k) + 1
        if gap1 >= n: break
        gaps.append(gap1)
        
        # Sedgewick formula for odd indices
        gap2 = (4**(k+2)) - 3 * (2**(k+2)) + 1
        if gap2 >= n: break
        gaps.append(gap2)
        
        k += 1
        
    gaps.sort(reverse=True)
    
    # Ensure 1 is always the final gap (safety catch)
    if not gaps or gaps[-1] != 1:
        if 1 in gaps: gaps.remove(1)
        gaps.append(1)
        
    print(f"Sedgewick's Sequence: {gaps}")
    execute_gaps(arr, gaps)

def demonstrate_gap_sequences():
    section_header("Algorithm: Shell Sort Gap Sequences")
    
    # We will sort the exact same reverse-sorted array 3 times to compare.
    base_arr = list(range(100, 0, -1)) # [100, 99, 98 ... 1]
    
    print("\n--- Running Shell's Original Sequence ---")
    arr1 = base_arr.copy()
    shell_sort_original(arr1)
    
    print("\n--- Running Hibbard's Sequence ---")
    arr2 = base_arr.copy()
    shell_sort_hibbard(arr2)
    
    print("\n--- Running Sedgewick's Sequence ---")
    arr3 = base_arr.copy()
    shell_sort_sedgewick(arr3)


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why does Donald Shell's original `N/2, N/4` sequence fail mathematically?
   Answer: Because powers of 2 share common divisors. If an array size is 1024, the gaps will be 512, 256, 128, etc. Notice that ALL of these are even numbers. This means an element at an even index will NEVER be compared to an element at an odd index during the massive gap jumps! They only finally interact when the gap reaches 1, forcing a massive, slow $O(N^2)$ standard insertion sort at the very end.

2. Why do Hibbard's and Sedgewick's sequences solve this?
   Answer: Their formulas are mathematically designed to be "Relatively Prime" (sharing no common divisors) as often as possible. By constantly mixing odd and even jump sizes, the elements "mix" much earlier in the process, resulting in a nearly sorted array when the final gap of 1 occurs.

3. Does anyone know the mathematically absolute BEST gap sequence?
   Answer: NO! It is an unsolved problem in Computer Science. Sedgewick's and Pratt's are excellent, but nobody has mathematically proven the theoretical optimal sequence. It is an area of active mathematical research.
"""

if __name__ == "__main__":
    demonstrate_gap_sequences()
    print("\n[SUCCESS] Laboratory: Advanced Shell Sort Completed.")
