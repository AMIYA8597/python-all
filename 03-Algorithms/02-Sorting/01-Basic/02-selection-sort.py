"""
# ==============================================================================
# LABORATORY: SELECTION SORT (O(N^2) BASIC SORTING)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Selection Sort is one of the simplest sorting algorithms to understand.
# It works exactly how a human might sort a hand of playing cards:
# 1. Scan the entire array to find the absolute smallest card.
# 2. Swap it with the first card.
# 3. Ignore the first card (it's sorted). Scan the remaining cards to find the 
#    next smallest. Swap it with the second card.
# 4. Repeat until sorted.
#
# Like Bubble Sort, it is extremely slow for large datasets, operating in 
# O(N^2) time. However, it has one very specific advantage: It only ever makes 
# exactly O(N) swaps! If writing data to disk/memory is extremely expensive 
# (e.g., EEPROM or Flash memory), Selection Sort causes less hardware wear than 
# Bubble Sort (which does O(N^2) swaps).
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the find-minimum-and-swap mechanic.
# - Understand why it is ALWAYS O(N^2) even if the array is already sorted.
# - Understand why it is an UNSTABLE sort.
#
# ==============================================================================
"""

from typing import List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. SELECTION SORT IMPLEMENTATION
# ==============================================================================
def selection_sort(arr: List[int]) -> List[int]:
    """
    Sorts an array in-place using Selection Sort.
    Time Complexity: O(N^2) Best, Average, and Worst case.
    Space Complexity: O(1)
    """
    n = len(arr)
    
    # Track metrics for educational purposes
    comparisons = 0
    swaps = 0
    
    # We loop from index 0 to N-2. 
    # (When we reach the last element, it's already guaranteed to be the largest!)
    for i in range(n):
        
        # Assume the current position 'i' holds the minimum value
        min_index = i
        
        # Scan all the REMAINING elements to the right of 'i'
        for j in range(i + 1, n):
            comparisons += 1
            if arr[j] < arr[min_index]:
                # We found a new, smaller minimum! Record its index.
                min_index = j
                
        # If the minimum we found is NOT the one we started with, swap them!
        if min_index != i:
            arr[i], arr[min_index] = arr[min_index], arr[i]
            swaps += 1
            
        print(f" Pass {i+1}: Swapped {arr[min_index]:2} into index {i}. Array -> {arr}")
            
    print(f"\nStats: {comparisons} Comparisons, {swaps} Swaps.")
    return arr

def demonstrate_selection_sort():
    section_header("Algorithm: Selection Sort")
    
    arr = [64, 25, 12, 22, 11]
    print(f"Initial Unsorted Array: {arr}\n")
    
    selection_sort(arr)
    print(f"\nFinal Sorted Array: {arr}")
    
    print("\n--- Why it is ALWAYS O(N^2) ---")
    arr_sorted = [1, 2, 3, 4, 5]
    print(f"Sorting an ALREADY SORTED array: {arr_sorted}\n")
    selection_sort(arr_sorted)
    
    print("\nNotice that even though it made 0 Swaps, it STILL made exactly 10 Comparisons.")
    print("It has no way of knowing the array is sorted, because it must scan the")
    print("entire remaining array just to verify there isn't a smaller number hiding at the end!")


# ==============================================================================
# 4. THE STABILITY PROBLEM
# ==============================================================================
def explain_instability():
    section_header("Concept: Stable vs Unstable Sorting")
    print("""
A sorting algorithm is "Stable" if duplicate elements retain their original 
relative order after sorting.

Imagine we are sorting a list of students by Grade (A, B, C).
[ (Alice, B), (Bob, A), (Charlie, B) ]

If the sort is Stable, Alice will ALWAYS appear before Charlie in the final 
list because she was before him originally.

Selection Sort is UNSTABLE.
Let's sort this array of numbers by value. Notice we have two 4s.
[ 4(red),  4(blue),  1(green) ]

Pass 1: It looks for the minimum. It finds 1(green) at index 2.
It SWAPS index 0 with index 2!
[ 1(green),  4(blue),  4(red) ]

Wait! Look at the 4s! The red 4 was originally BEFORE the blue 4. But because 
Selection Sort violently threw the red 4 all the way to the end of the array 
during a long-distance swap, their relative order was destroyed.

Because it does long-distance swaps, Selection Sort is Unstable. 
(Bubble Sort and Insertion Sort only do adjacent short-distance swaps, so they 
are Stable).
    """)


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. What is the one advantage Selection Sort has over Bubble Sort?
   Answer: The number of swaps. Bubble Sort swaps continuously as elements bubble up, resulting in $O(N^2)$ swaps in the worst case. Selection Sort only swaps ONCE per pass, guaranteeing exactly $O(N)$ swaps worst case. This is better for systems where writing to memory is highly expensive.

2. Why doesn't Selection Sort have a "Best Case" $O(N)$ like Bubble Sort?
   Answer: Bubble Sort can stop early if it completes a full pass without making any swaps (proving the array is sorted). Selection Sort CANNOT stop early. Even if the array is perfectly sorted, when it looks at index 0, it is mathematically forced to check indices 1 through N just to guarantee there isn't a smaller number hiding.

3. Can you make Selection Sort stable?
   Answer: Yes, but you ruin its $O(1)$ space complexity. Instead of swapping, you would have to find the minimum element, and then shift all the other elements down by one spot to make room for it. Shifting an array takes $O(N)$ time, making the algorithm incredibly slow. At that point, you should just use Insertion Sort.
"""

if __name__ == "__main__":
    demonstrate_selection_sort()
    explain_instability()
    print("\n[SUCCESS] Laboratory: Selection Sort Completed.")
