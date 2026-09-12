"""
Shell Sort Algorithm

Learning Objectives:
1. Understand the concept of diminishing increment sorting (gap sequences).
2. Learn how Shell Sort optimizes Insertion Sort by moving elements over large gaps.
3. Compare different gap sequences (Shell's, Knuth's, Hibbard's) and their impact on complexity.
4. Implement a clean, generic Shell Sort algorithm.

Concept Explanation:
Shell Sort is an in-place comparison sort. It can be seen as either a generalization of sorting 
by exchange (bubble sort) or sorting by insertion (insertion sort). The method starts by sorting 
pairs of elements far apart from each other, then progressively reducing the gap between elements 
to be compared. By starting with far apart elements, it can move some out-of-place elements into 
position faster than a simple nearest-neighbor exchange.

Beginner Explanation:
Imagine you have a deck of cards. Insertion sort goes through the deck one by one, shifting cards 
left until they are in place. If the smallest card is at the very end, it takes many shifts to get 
it to the front. Shell Sort says: let's first compare cards that are 5 positions apart, and swap 
them if needed. Then 3 positions apart. Finally, 1 position apart (which is just regular insertion sort).
By doing the large jumps first, the small cards zoom to the front quickly, making the final step very easy!

Advanced/Internal Details:
The performance of Shell Sort heavily depends on the chosen gap sequence.
- Original Shell sequence: N/2, N/4, ..., 1. Worst-case time complexity is O(N^2).
- Knuth's sequence: 1, 4, 13, 40... (3k + 1). Worst-case time complexity is O(N^(3/2)).
- Sedgewick's sequence: Complex interleaved sequence yielding O(N^(4/3)) average time.

Unlike Insertion Sort, Shell Sort is NOT stable because the large gap jumps can cross over 
equal elements and disturb their relative order.

Performance & Complexity:
- Time Complexity: 
  - Best: O(N log N)
  - Average/Worst: Depends on gap sequence, typically O(N^(3/2)) or O(N^(4/3))
- Space Complexity: O(1) auxiliary space (in-place).
- Stable: No.

Common Mistakes & Considerations:
- Choosing a bad gap sequence can severely degrade performance. Ensure the sequence ends with 1.
- Shell Sort is excellent for medium-sized arrays (up to ~10,000 elements) where the overhead 
  of complex algorithms like Quick Sort or Merge Sort isn't justified, and memory is constrained.

Interview Challenge:
"Why is Shell Sort useful in embedded systems compared to Quick Sort or Merge Sort?"
Answer: Shell sort is strictly in-place (O(1) memory), has no recursive overhead (avoids call stack overflow 
risks common in embedded C/C++), and performs reasonably well on medium datasets, whereas Quick Sort can hit 
O(N^2) or require O(log N) stack space, and Merge Sort needs O(N) memory.
"""

from typing import List, TypeVar

T = TypeVar('T')

def shell_sort_basic(arr: List[int]) -> None:
    """
    Basic implementation of Shell Sort using Shell's original gap sequence (N/2, N/4, ...).
    Mutates the array in-place.
    
    Args:
        arr: List of integers to sort.
    """
    n = len(arr)
    gap = n // 2
    
    # Continue reducing the gap until it becomes 0
    while gap > 0:
        # Perform a gapped insertion sort for this gap size.
        # The first gap elements a[0..gap-1] are already in gapped order
        # keep adding one more element until the entire array is gap sorted
        for i in range(gap, n):
            # add a[i] to the elements that have been gap sorted
            # save a[i] in temp and make a hole at position i
            temp = arr[i]
            
            # shift earlier gap-sorted elements up until the correct 
            # location for a[i] is found
            j = i
            while j >= gap and arr[j - gap] > temp:
                arr[j] = arr[j - gap]
                j -= gap
                
            # put temp (the original a[i]) in its correct location
            arr[j] = temp
            
        gap //= 2


def shell_sort_knuth(arr: List[T]) -> None:
    """
    Professional implementation of Shell Sort using Knuth's gap sequence: (3^k - 1) / 2
    This gap sequence provides O(N^(3/2)) worst-case time complexity.
    Supports generic comparable types.
    
    Args:
        arr: List of comparable items to sort in-place.
    """
    n = len(arr)
    if n <= 1:
        return
        
    # Calculate initial gap according to Knuth's sequence: 1, 4, 13, 40, 121...
    gap = 1
    while gap < n // 3:
        gap = gap * 3 + 1
        
    while gap > 0:
        # Gapped insertion sort
        for i in range(gap, n):
            temp = arr[i]
            j = i
            # Shift elements for the current gap
            while j >= gap and arr[j - gap] > temp: # type: ignore
                arr[j] = arr[j - gap]
                j -= gap
            arr[j] = temp
            
        # Move to the next smaller gap in the sequence
        gap //= 3


# ==========================================
# Tests and Assertions
# ==========================================
if __name__ == "__main__":
    print("Testing Shell Sort Algorithms...")
    
    # Test Basic Shell Sort
    nums1 = [12, 34, 54, 2, 3]
    shell_sort_basic(nums1)
    assert nums1 == [2, 3, 12, 34, 54], f"Basic test failed: {nums1}"
    
    # Test Knuth Sequence Shell Sort
    nums2 = [45, 23, 11, 89, 77, 98, 4, 28, 65, 43]
    expected2 = sorted(nums2)
    shell_sort_knuth(nums2)
    assert nums2 == expected2, f"Knuth sequence test failed: {nums2}"
    
    # Test with strings
    words = ["zebra", "apple", "monkey", "banana", "cat"]
    expected_words = sorted(words)
    shell_sort_knuth(words)
    assert words == expected_words, f"String sorting test failed: {words}"
    
    # Test empty and single element
    empty_arr = []
    shell_sort_knuth(empty_arr)
    assert empty_arr == [], "Empty array test failed"
    
    single = [42]
    shell_sort_knuth(single)
    assert single == [42], "Single element test failed"
    
    print("All tests passed successfully!")
