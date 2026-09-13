"""
# ==============================================================================
# LABORATORY: SORTING FUNDAMENTALS (O(N^2) ALGORITHMS)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Before studying advanced recursive algorithms like Quick Sort and Merge Sort,
# you must understand the foundational "Iterative" sorting algorithms.
# 
# These algorithms (Bubble Sort, Insertion Sort, Selection Sort) take O(N^2) time.
# While they are generally considered "too slow" for massive datasets, they have 
# incredible utility in specific edge cases:
# - Insertion Sort is actually FASTER than Quick Sort for tiny arrays (N < 30) due 
#   to having almost zero constant-factor overhead. (This is why Python's Timsort 
#   uses it internally!).
# - They introduce the critical concepts of "In-Place" memory modification and 
#   "Stability" (maintaining the relative order of duplicate elements).
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the Swap vs Shift mechanics.
# - Implement Bubble Sort (with the Early Exit optimization).
# - Implement Insertion Sort.
# - Master the concept of Algorithmic Stability.
#
# ==============================================================================
"""

from typing import List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. BUBBLE SORT (THE SLOWEST, BUT EASIEST)
# ==============================================================================
def bubble_sort(arr: List[int]) -> List[int]:
    """
    Time Complexity: O(N^2) Worst/Average. O(N) Best (If already sorted).
    Space Complexity: O(1) In-Place.
    Stability: STABLE (Only swaps adjacent elements).
    """
    n = len(arr)
    
    # We must do N passes over the array.
    for i in range(n):
        
        # EARLY EXIT OPTIMIZATION:
        # If we go through an entire pass without making a single swap,
        # it mathematically proves the array is perfectly sorted! We can stop.
        swapped_this_pass = False
        
        # We scan from the beginning up to the "unsorted" boundary.
        # After pass 1, the absolute largest element is guaranteed to have 
        # "bubbled" up to the very last index. We don't need to check it again!
        # So we subtract `i` and `1` from the boundary.
        for j in range(0, n - i - 1):
            
            # Compare adjacent elements
            if arr[j] > arr[j + 1]:
                # The left element is bigger. SWAP THEM!
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped_this_pass = True
                
        if not swapped_this_pass:
            print(f" [Bubble] Early exit triggered at pass {i}! Array is sorted.")
            break
            
    return arr

def demonstrate_bubble_sort():
    section_header("Algorithm: Bubble Sort")
    
    arr = [64, 34, 25, 12, 22, 11, 90]
    print(f"Initial Array: {arr}\n")
    bubble_sort(arr)
    print(f"\nFinal Sorted: {arr}")


# ==============================================================================
# 4. INSERTION SORT (THE "CARD GAME" SORT)
# ==============================================================================
def insertion_sort(arr: List[int]) -> List[int]:
    """
    Time Complexity: O(N^2) Worst/Average. O(N) Best (If already sorted).
    Space Complexity: O(1) In-Place.
    Stability: STABLE.
    
    How it works:
    Imagine holding playing cards in your left hand. You pick up a new card 
    with your right hand, and "insert" it into the correct position in your 
    left hand by shifting all the larger cards to the right.
    """
    n = len(arr)
    
    # Assume the first element (index 0) is a "sorted" array of length 1.
    # We start picking up new cards from index 1.
    for i in range(1, n):
        
        card_to_insert = arr[i]
        
        # `j` points to the last card in our "sorted left hand"
        j = i - 1
        
        # While there are still cards in our left hand, AND the card we are 
        # looking at is LARGER than our new card...
        while j >= 0 and arr[j] > card_to_insert:
            # SHIFT the larger card one spot to the right to make room!
            arr[j + 1] = arr[j]
            j -= 1
            
        # We found the exact spot where our new card belongs. Insert it!
        arr[j + 1] = card_to_insert
        
    return arr

def demonstrate_insertion_sort():
    section_header("Algorithm: Insertion Sort")
    
    arr = [12, 11, 13, 5, 6]
    print(f"Initial Array: {arr}\n")
    insertion_sort(arr)
    print(f"Final Sorted: {arr}")


# ==============================================================================
# 5. CONCEPT: ALGORITHMIC STABILITY
# ==============================================================================
def explain_stability():
    section_header("Concept: Algorithmic Stability")
    print("""
"Stability" is one of the most critical concepts in sorting.
It answers the question: "If two elements are exactly equal, do they stay in 
the same relative order they started in?"

Example: Sorting a list of Bank Transactions by Amount.
Original List (Ordered chronologically by Time):
1. Alice: $50  (9:00 AM)
2. Bob:   $100 (9:15 AM)
3. Carl:  $50  (9:30 AM)

Notice we have two $50 transactions. Alice came BEFORE Carl.

If we use a STABLE sort (Bubble, Insertion, Merge), the result is:
1. Alice: $50
2. Carl:  $50
3. Bob:   $100
(Alice and Carl stayed in chronological order!).

If we use an UNSTABLE sort (Selection, Quick, Heap), the result might be:
1. Carl:  $50
2. Alice: $50
3. Bob:   $100
(The sort violently swapped Carl and Alice, destroying the chronological data!).

HOW TO KNOW IF A SORT IS STABLE:
- Does it ONLY swap adjacent elements? (Bubble, Insertion). It is STABLE.
- Does it do "Long-Distance Swaps", throwing elements across the array? 
  (Quick, Selection). It is UNSTABLE, because duplicate elements might get caught 
  in the crossfire and swap positions randomly.
    """)


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why is Insertion Sort faster than Bubble Sort in practice?
   Answer: Bubble Sort uses a "Swap" operation `(a, b = b, a)` which requires 3 memory writes under the hood (temp=a, a=b, b=temp). Insertion Sort uses a "Shift" operation `(arr[j+1] = arr[j])` which requires exactly 1 memory write. Less memory I/O means it runs significantly faster on the CPU.

2. What is Timsort, and how does it use Insertion Sort?
   Answer: Timsort is Python's built-in `list.sort()`. It recognizes that real-world data is often "partially sorted". It chops the massive array into tiny chunks of 32 elements. It runs Insertion Sort on those chunks (because Insertion Sort has zero recursion overhead and is blazing fast for N < 32), and then uses Merge Sort to combine the sorted chunks together.

3. Why do we subtract `i` in the inner loop of Bubble Sort (`range(0, n - i - 1)`)?
   Answer: Because after 1 pass, the absolute largest element is guaranteed to have bubbled to the very last index. After 2 passes, the 2nd largest is locked in place. There is no mathematical reason to compare elements in the "locked" zone at the end of the array, so we shrink the boundary by `i` every pass to save CPU cycles.
"""

if __name__ == "__main__":
    demonstrate_bubble_sort()
    demonstrate_insertion_sort()
    explain_stability()
    print("\n[SUCCESS] Laboratory: Sorting Fundamentals Completed.")
