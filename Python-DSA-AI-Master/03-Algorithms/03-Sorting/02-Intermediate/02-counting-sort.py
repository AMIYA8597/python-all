"""
## A. Concept Name
Counting Sort Algorithm

## B. One-Sentence Definition
Counting Sort is a non-comparative integer sorting algorithm that works by counting the occurrences of each unique element and using arithmetic to calculate their positions in the sorted array.

## C. Intuition
Imagine you have a bunch of test scores between 0 and 100. Instead of comparing scores to each other, you make a list of 101 buckets (one for each possible score). You go through your scores, throwing each into its corresponding bucket. Then, you simply walk through the buckets from 0 to 100 and pull out the scores. They naturally come out sorted!

## D. Internal Details
Counting sort operates in three main phases:
1. Histogram phase: Count the occurrences of each element in the input array.
2. Prefix sum phase: Compute the cumulative sum in the count array. `count[i]` will contain the actual position (1-based) of the last occurrence of the element `i` in the sorted array.
3. Placement phase: Iterate through the input array in reverse (to maintain stability) and place each element into its correct position in the output array according to the count array, then decrement the count.

## E. Time Complexity
O(N + K), where N is the number of elements and K is the range of input values (max - min + 1).

## F. Space Complexity
O(N + K) for the count array and output array.

## G. Stability & In-Place
- Stable: Yes (if implemented correctly with the reverse traversal).
- In-place: No.

## H. Real-World Applications
- Used inside Radix Sort as a subroutine to sort elements by significant digits.
- Sorting elements with a known, small range (e.g., ages of people, RGB color channels, exam scores).

## I. Common Mistakes
- Memory Prohibitive: Do not use Counting Sort when the range K is significantly larger than N (e.g., sorting [1, 1000000000]).
- Handling Negatives: The basic version doesn't handle negative numbers. We must offset all values by the minimum element to map the minimum value to index 0.

## J. Edge Cases
- Empty arrays or single-element arrays.
- Arrays with all identical elements.
- Arrays with negative numbers.

## K. Related Concepts
- Radix Sort
- Bucket Sort
- Pigeonhole Sort

## L. Interview Challenge
"Given an array of integers representing colors (0 for Red, 1 for White, 2 for Blue), sort them in-place in linear time."
While counting sort requires O(N) space generally, for a tiny known range (K=3), you can do a 3-way partition (Dutch National Flag), or a naive 2-pass counting sort taking O(1) auxiliary space!

## M. Debugging
- Ensure the size of the count array is exactly K (max - min + 1).
- Verify the prefix sum logic accurately accumulates frequencies.
- Always iterate backwards during the placement phase to guarantee stable sorting.
- Check if elements are mapped correctly back and forth with the `min` offset.

## N. Step-by-Step Walkthrough
Given `[4, 2, 2, 8, 3, 3, 1]`:
1. Find max=8, min=1, k=8.
2. Count array records frequencies: `count = [1(for 1), 2(for 2), 2(for 3), 1(for 4), 0..0, 1(for 8)]`.
3. Prefix sums turn it into positions.
4. Reverse traverse the input to place into the output array.

## O. Visualization
Input: `[4, 2, 2, 8, 3, 3, 1]`
Counts: 1:1, 2:2, 3:2, 4:1, 5:0, 6:0, 7:0, 8:1
Sorted Output: `[1, 2, 2, 3, 3, 4, 8]`

## P. Code Implementation
The code implementation below includes basic, stable, and object-based counting sorts.

## Q. Test Cases
- Small random arrays.
- Arrays with negative values (e.g., `[4, -2, 2, -8, 3, 3, 1, 0, -2]`).
- Objects sorted by integer keys (to test stability).

## R. Best Practices
- Use only when K is on the same order of magnitude as N or smaller.
- For objects, always use the stable implementation (reverse placement).

## S. Alternative Approaches
- If space is strict O(1), use Quicksort or Heapsort (though they take O(N log N)).
- If range is extremely large, use comparison sorts or hash-based bucketing.

## T. History/Origin
Counting Sort was first proposed by Harold H. Seward in 1954 as part of his Master's thesis at MIT.

## U. Interactive Exercises
1. Try modifying the implementation to sort characters in a string.
2. Adapt the algorithm to find the mode (most frequent element) of the array while sorting.

## V. Further Reading
- Introduction to Algorithms (CLRS) - Chapter 8.
- Wikipedia article on Counting Sort.

## W. Glossary
- **Non-comparative sort**: Sorting without direct value-to-value comparisons.
- **Prefix sum**: An array where each element is the sum of all preceding elements.
- **Stable sort**: A sort that preserves the relative order of equal elements.

## X. Project Connection
In our DSA-AI-Master project, Counting Sort serves as the foundation for our next module on Radix Sort and helps analyze datasets with bounded categorical variables efficiently.
"""

from typing import List, TypeVar, Generic, Callable, Any

def counting_sort_basic(arr: List[int]) -> List[int]:
    """
    Basic implementation of Counting Sort (assumes non-negative integers).
    
    Args:
        arr: List of non-negative integers to sort.
        
    Returns:
        A new sorted list.
    """
    if not arr:
        return []
        
    max_val = max(arr)
    # Phase 1: Initialize count array
    count = [0] * (max_val + 1)
    
    # Phase 2: Histogram
    for num in arr:
        count[num] += 1
        
    # Phase 3: Reconstruct sorted array
    sorted_arr = []
    for i, freq in enumerate(count):
        sorted_arr.extend([i] * freq)
        
    return sorted_arr


def counting_sort_stable_with_negatives(arr: List[int]) -> List[int]:
    """
    Professional implementation of Counting Sort.
    - Handles negative numbers by offsetting.
    - Maintains stability by building the output array backwards using cumulative counts.
    
    Args:
        arr: List of integers to sort.
        
    Returns:
        A new sorted list.
    """
    if not arr:
        return []
        
    min_val = min(arr)
    max_val = max(arr)
    
    # Range of values
    k = max_val - min_val + 1
    
    # Initialize count array
    count = [0] * k
    
    # Phase 1: Histogram (with offset)
    for num in arr:
        count[num - min_val] += 1
        
    # Phase 2: Prefix sum (cumulative count)
    for i in range(1, k):
        count[i] += count[i - 1]
        
    # Phase 3: Placement (iterate backwards for stability)
    output = [0] * len(arr)
    for num in reversed(arr):
        # Find index in count array
        count_idx = num - min_val
        # The position in output array is count - 1 (0-indexed)
        output_pos = count[count_idx] - 1
        output[output_pos] = num
        # Decrement count for the next occurrence of the same number
        count[count_idx] -= 1
        
    return output


T = TypeVar('T')

def counting_sort_objects(arr: List[T], key: Callable[[T], int]) -> List[T]:
    """
    Advanced implementation: Stable Counting Sort for arbitrary objects based on an integer key.
    
    Args:
        arr: List of objects to sort.
        key: A function that extracts an integer key from an object.
        
    Returns:
        A new sorted list of objects.
    """
    if not arr:
        return []
        
    # Extract keys and find min/max
    keys = [key(item) for item in arr]
    min_key = min(keys)
    max_key = max(keys)
    
    k = max_key - min_key + 1
    count = [0] * k
    
    # Histogram
    for k_val in keys:
        count[k_val - min_key] += 1
        
    # Prefix sum
    for i in range(1, k):
        count[i] += count[i - 1]
        
    # Placement (stable)
    output = [None] * len(arr) # type: List[Any]
    for i in range(len(arr) - 1, -1, -1):
        item = arr[i]
        k_val = keys[i]
        count_idx = k_val - min_key
        output_pos = count[count_idx] - 1
        
        output[output_pos] = item
        count[count_idx] -= 1
        
    return output # type: ignore


# ==========================================
# Tests and Assertions
# ==========================================
if __name__ == "__main__":
    print("Testing Counting Sort Algorithms...")
    
    # Test Basic Implementation
    nums1 = [4, 2, 2, 8, 3, 3, 1]
    res1 = counting_sort_basic(nums1)
    assert res1 == sorted(nums1), f"Basic test failed: {res1}"
    
    # Test Professional Implementation with Negatives
    nums2 = [4, -2, 2, -8, 3, 3, 1, 0, -2]
    res2 = counting_sort_stable_with_negatives(nums2)
    assert res2 == sorted(nums2), f"Negative numbers test failed: {res2}"
    
    # Test Object Sorting (Stability check)
    class Player:
        def __init__(self, name: str, score: int):
            self.name = name
            self.score = score
            
        def __repr__(self):
            return f"Player({self.name}, {self.score})"
            
        def __eq__(self, other):
            return self.name == other.name and self.score == other.score

    players = [
        Player("Alice", 10),
        Player("Bob", 5),
        Player("Charlie", 10),
        Player("Dave", 2)
    ]
    
    sorted_players = counting_sort_objects(players, key=lambda p: p.score)
    # Expected order: Dave (2), Bob (5), Alice (10), Charlie (10)
    # Notice that Alice and Charlie both have 10, but Alice comes first in input, 
    # so she must come first in output to prove stability.
    assert sorted_players[2].name == "Alice", "Stability test failed for object sort"
    assert sorted_players[3].name == "Charlie", "Stability test failed for object sort"
    
    print("All tests passed successfully!")
