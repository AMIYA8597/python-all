"""
## A. Concept Name
Selection Sort

## B. High-Level Concept
Selection sort is an in-place comparison sorting algorithm. It divides the input list into two parts: a sorted sublist of items which is built up from left to right at the front (left) of the list, and a sublist of the remaining unsorted items that occupy the rest of the list.

## C. Everyday Metaphor
Imagine you have a hand of playing cards, all jumbled up. To sort them, you look through all the cards in your hand, find the smallest one, and place it at the very beginning. Then, you look through the remaining unsorted cards, find the next smallest, and place it in the second position. You repeat this until the whole hand is sorted.

## D. Technical Mechanics
Initially, the sorted sublist is empty and the unsorted sublist is the entire input list. The algorithm proceeds by finding the smallest (or largest) element in the unsorted sublist, exchanging (swapping) it with the leftmost unsorted element (putting it in sorted order), and moving the sublist boundaries one element to the right.

## E. Step-by-Step Algorithm
1. Start with the first element as the current minimum.
2. Iterate through the rest of the unsorted array to find the true minimum element.
3. Swap the true minimum element with the first unsorted element.
4. Shift the boundary of the sorted/unsorted parts one element to the right.
5. Repeat until the array is fully sorted.

## F. Visual Walkthrough
Sorting [64, 25, 12, 22, 11]
Pass 1: Find min(64, 25, 12, 22, 11) -> 11. Swap 64 and 11. -> [11, 25, 12, 22, 64]
Pass 2: Find min(25, 12, 22, 64) -> 12. Swap 25 and 12. -> [11, 12, 25, 22, 64]
Pass 3: Find min(25, 22, 64) -> 22. Swap 25 and 22. -> [11, 12, 22, 25, 64]
Pass 4: Find min(25, 64) -> 25. Swap 25 and 25 (no op). -> [11, 12, 22, 25, 64]
Done.

## G. Time Complexity Analysis
Time Complexity is O(N^2) for all cases since we always scan the remaining array to find the minimum.

## H. Space Complexity Analysis
Space Complexity is O(1) as the sorting is done in-place.

## I. Algorithm Properties (Stability, In-place)
- In-place: Yes (O(1) auxiliary space).
- Stable: No. The swapping can change the relative order of equal elements.
- Adaptive: No. It always takes O(N^2) time regardless of initial order.

## J. Best Case Scenario
O(N^2) - Even if the array is already sorted, the algorithm still iterates through the unsorted portion to confirm the minimum.

## K. Worst Case Scenario
O(N^2) - When the array is reverse sorted, it does maximum comparisons and swaps.

## L. Average Case Scenario
O(N^2) - On average, roughly N^2 / 2 comparisons are made.

## M. Edge Cases
- Empty array
- Single element array
- Array with all identical elements
- Already sorted array

## N. System Constraints
Selection sort performs O(N^2) comparisons but only O(N) swaps. If writes to memory are significantly more expensive than reads (e.g., EEPROM or Flash memory), Selection Sort might outperform other O(N^2) algorithms like Bubble Sort.

## O. Comparison with Alternatives
- Bubble Sort: Selection Sort generally performs fewer swaps.
- Insertion Sort: Insertion Sort is generally faster for small arrays and is stable and adaptive.
- Merge/Quick Sort: Much more efficient O(N log N) but might require extra space or recursion overhead.

## P. Real-World Applications
Mainly used in systems where memory write operations are extremely costly, or strictly for educational purposes to demonstrate algorithmic thinking.

## Q. Common Interview Questions
1. Why is Selection Sort not stable? (Provide an example).
2. Can we make Selection Sort stable? (Yes, by shifting instead of swapping, but it breaks O(1) writes).

## R. Typical Pitfalls and Mistakes
- Forgetting that the outer loop needs to go up to n-1, not n.
- Swapping the element every time a smaller one is found, rather than tracking the minimum index and swapping once at the end of the pass.

## S. Language Specifics (Python)
Python's built-in `list.sort()` (Timsort) is significantly better. Selection sort here is purely for educational value. 

## T. Optimization Strategies
Cocktail Selection Sort (or Double Selection Sort): Find both the minimum and maximum in one pass, sorting from both ends simultaneously, reducing iterations by half (though still O(N^2) time).

## U. Advanced Variants
Bingo Sort: A variant of selection sort that works well if there are many duplicate items.

## V. Testing Strategy
Test with empty list, single element, negative numbers, duplicates, reversed lists, already sorted lists, and custom objects using the `key` function.

## W. AI Integration / Usage
Can be used as a foundational example when teaching LLMs how to reason about sorting states or tracking index bounds.

## X. Project Connection
Useful as a building block in our sorting visualizer project or as a performance benchmark baseline in the Python-DSA-AI-Master repo.
"""

from typing import TypeVar, List, Callable

# Type variable for generic sorting
T = TypeVar('T')

def selection_sort(
    arr: List[T], 
    key: Callable[[T], any] = lambda x: x, 
    reverse: bool = False
) -> None:
    """
    Sorts a list in-place using the Selection Sort algorithm.
    
    Args:
        arr (List[T]): The list of elements to sort.
        key (Callable): A function to extract a comparison key from each element. Defaults to identity.
        reverse (bool): If True, sorts in descending order. Defaults to False.
        
    Returns:
        None: The list is modified in-place.
    """
    n = len(arr)
    
    # Traverse through all array elements except the last one
    # as it will naturally be in the correct place once the rest are sorted.
    for i in range(n - 1):
        # Find the minimum (or maximum) element in remaining unsorted array
        extreme_idx = i
        
        for j in range(i + 1, n):
            val_j = key(arr[j])
            val_extreme = key(arr[extreme_idx])
            
            if reverse:
                # We want descending order, so look for maximum
                if val_j > val_extreme:
                    extreme_idx = j
            else:
                # We want ascending order, so look for minimum
                if val_j < val_extreme:
                    extreme_idx = j
                    
        # Swap the found extreme element with the first unsorted element
        if extreme_idx != i:
            arr[i], arr[extreme_idx] = arr[extreme_idx], arr[i]


if __name__ == "__main__":
    print("Running Selection Sort Tests...")
    
    # Test 1: Basic integer sorting
    nums = [64, 25, 12, 22, 11]
    selection_sort(nums)
    assert nums == [11, 12, 22, 25, 64], f"Test 1 Failed: {nums}"
    
    # Test 2: Reverse sorting
    nums_reverse = [64, 25, 12, 22, 11]
    selection_sort(nums_reverse, reverse=True)
    assert nums_reverse == [64, 25, 22, 12, 11], f"Test 2 Failed: {nums_reverse}"
    
    # Test 3: Custom key (sorting strings by length)
    words = ["apple", "banana", "kiwi", "strawberry"]
    selection_sort(words, key=len)
    assert words == ["kiwi", "apple", "banana", "strawberry"], f"Test 3 Failed: {words}"
    
    # Test 4: Edge cases (empty and single element)
    empty = []
    selection_sort(empty)
    assert empty == [], "Empty test failed"
    
    single = [42]
    selection_sort(single)
    assert single == [42], "Single element test failed"
    
    # Test 5: Already sorted and reverse sorted arrays
    sorted_arr = [1, 2, 3, 4, 5]
    selection_sort(sorted_arr)
    assert sorted_arr == [1, 2, 3, 4, 5], "Already sorted test failed"
    
    rev_sorted_arr = [5, 4, 3, 2, 1]
    selection_sort(rev_sorted_arr)
    assert rev_sorted_arr == [1, 2, 3, 4, 5], "Reverse sorted test failed"
    
    print("All Selection Sort tests passed successfully!")
