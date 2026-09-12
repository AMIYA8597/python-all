"""
# Binary Search: The Divide and Conquer Foundation

## A. Concept Name
Binary Search

## B. One-Sentence Definition
Binary Search is a highly efficient search algorithm that finds the position of a target value within a *sorted* array by repeatedly halving the search interval.

## C. Why Does This Exist? (What problem does it solve?)
Searching through an unsorted array takes linear time O(N), which becomes unacceptably slow for massive datasets (e.g., searching a user ID in a database of a billion users). Binary search exists to exploit the property of *sorted* data, reducing search time from billions of operations to a maximum of ~30 operations.

## D. Intuition & Real-Life Analogy
Imagine looking for the word "Python" in a physical dictionary. You don't read every word starting from page 1. Instead, you open the book to the exact middle. If you land on "Monkey", you know "Python" must be in the second half. You rip the book in half, throw away the first half, and repeat the process on the remaining pages until you find the word.

## E. Mental Model
```text
Target: 7

[ 1, 3, 5, 7, 9, 11, 15 ]
  ^        ^          ^
 Left     Mid       Right
```
Is `Mid` (7) our target? Yes. Done.
If Target was 9: `7 < 9`, so throw away left half. New search space: `[9, 11, 15]`.

## F. Formal Technical Explanation
Binary search maintains a `left` and `right` pointer defining the current search boundary. At each step, it calculates the `mid` index. If the array element at `mid` equals the target, the search terminates successfully. If the target is strictly less than the `mid` element, the search continues on the left sub-array (`right = mid - 1`). Otherwise, it continues on the right sub-array (`left = mid + 1`). This halves the search space at every iteration.

## G. Mathematical Foundation
Let N be the number of elements. 
After iteration 1, search space = N/2
After iteration 2, search space = N/4
After iteration k, search space = N / (2^k)
The search terminates when the search space is 1.
So, N / (2^k) = 1  => N = 2^k  => k = log2(N)
Therefore, maximum iterations = log2(N).

## H. Complexity Analysis
- **Time Complexity:** 
  - Best Case: O(1) (Target is exactly in the middle on the first check)
  - Average/Worst Case: O(log N)
- **Space Complexity:**
  - Iterative: O(1) (Requires only a few pointer variables)
  - Recursive: O(log N) (Due to the call stack depth)

## I. Common Mistakes & Pitfalls
- **Integer Overflow:** In languages like C++ or Java, `mid = (left + right) / 2` can overflow if `left` and `right` are very large. The safe way is `mid = left + (right - left) // 2`. (Python handles arbitrarily large integers automatically, but this is a critical system design habit).
- **Off-By-One Errors:** Forgetting to do `left = mid + 1` or `right = mid - 1` and instead doing `left = mid`, which causes infinite loops when the search space shrinks to 2 elements.
- **Unsorted Data:** Binary search strictly requires the array to be sorted beforehand.

## J. Common Confusions
- *Linear Search vs Binary Search:* Linear search works on ANY data, but takes O(N). Binary search is blindingly fast O(log N), but REQUIRES sorted data.
- *Binary Search vs Hash Table:* Hash tables provide O(1) lookups, but require O(N) extra memory and cannot easily answer range queries (e.g., "find all numbers between 5 and 10").

## K. When To Use It
- When you have a sorted array and need to find a specific element.
- When searching for a boundary or a condition that switches from False to True (e.g., finding the first bad version in Git Bisect).
- Whenever you see the phrase "sorted array" in an interview, think Binary Search.

## L. When NOT To Use It
- If the data is constantly changing (frequent inserts/deletes). Re-sorting the array takes O(N log N) or O(N), which destroys the O(log N) benefit of the search. Use a Balanced Binary Search Tree (BST) instead.
- If the array is very small (e.g., 10 elements). The overhead of calculating `mid` might actually make it slower than a simple O(N) linear scan.

## M. Trade-offs
- **Pros:** Extremely fast (O(log N)), uses no extra memory (O(1) space iteratively).
- **Cons:** Requires the array to be strictly sorted.

## N. Debugging Tips
- If it infinite loops, check your `left = mid + 1` and `right = mid - 1` updates.
- If it returns `-1` when the element is present, check if your while loop is `left < right` instead of `left <= right` (missing the final 1-element check).

## O. Memory Hook
"Halve it to solve it. Left, Right, Mid, and Off-by-one."

## P. Active Recall Questions
1. Why must the array be sorted for Binary Search to work?
2. What is the time complexity of Binary Search and why?
3. How do you calculate `mid` to prevent integer overflow?
4. Why do we use `left <= right` in the while loop condition?

## Q. Interview Questions & Answers
**Q: How would you find the *first* occurrence of a target in a sorted array containing duplicates?**
A: Instead of returning immediately when `arr[mid] == target`, you record the `mid` index as a potential answer, and then shrink the search space to the left (`right = mid - 1`) to see if there is an earlier occurrence.

**Q: Can you apply Binary Search to a problem that isn't an array?**
A: Yes! It can be applied to any monotonic function. For example, finding the square root of a number N. We know the answer is between 0 and N. We can binary search the answer by testing if `mid * mid <= N`.

## R. Project Connections
- **Databases:** B-Trees use binary search on their nodes to quickly find records.
- **Git:** `git bisect` uses binary search to find the exact commit that introduced a bug.
- **Machine Learning:** Used to efficiently search quantized embedding spaces or boundary conditions during thresholding.
"""

from typing import List

# ==============================================================================
# 1. EDUCATIONAL FROM-SCRATCH IMPLEMENTATION (ITERATIVE)
# ==============================================================================
def binary_search_iterative(arr: List[int], target: int) -> int:
    """
    Standard iterative Binary Search.
    Returns the index of the target if found, else -1.
    """
    left = 0
    right = len(arr) - 1

    # <= is crucial to check the final remaining element when left == right
    while left <= right:
        # Prevents integer overflow (Standard best practice, even in Python)
        mid = left + (right - left) // 2 

        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            # Target is in the right half
            left = mid + 1
        else:
            # Target is in the left half
            right = mid - 1
            
    return -1

# ==============================================================================
# 2. EDUCATIONAL FROM-SCRATCH IMPLEMENTATION (RECURSIVE)
# ==============================================================================
def binary_search_recursive(arr: List[int], target: int, left: int, right: int) -> int:
    """
    Recursive Binary Search. Space complexity is O(log N) due to call stack.
    """
    if left > right:
        return -1
        
    mid = left + (right - left) // 2
    
    if arr[mid] == target:
        return mid
    elif arr[mid] < target:
        return binary_search_recursive(arr, target, mid + 1, right)
    else:
        return binary_search_recursive(arr, target, left, mid - 1)

# ==============================================================================
# 3. INDUSTRY-STANDARD LIBRARY IMPLEMENTATION
# ==============================================================================
import bisect

def binary_search_library(arr: List[int], target: int) -> int:
    """
    Python's standard library `bisect` module implements binary search in C.
    `bisect_left` finds the insertion point for the target.
    """
    # bisect_left returns the index where 'target' should be inserted to maintain order.
    idx = bisect.bisect_left(arr, target)
    
    # We must check if the index is within bounds AND actually equals our target
    if idx < len(arr) and arr[idx] == target:
        return idx
    return -1

# ==============================================================================
# 4. DELIBERATELY BUGGY IMPLEMENTATION
# ==============================================================================
def binary_search_buggy(arr: List[int], target: int) -> int:
    """
    BUGGY VERSION - Can you spot the bug?
    """
    left = 0
    right = len(arr) - 1
    
    # BUG 1: Using `<` instead of `<=`. 
    # If the array is [5] and target is 5, left=0, right=0, loop never runs, returns -1.
    while left < right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            # BUG 2: Setting left = mid.
            # If left=0, right=1 (arr=[2, 4], target=5). mid=0. arr[0] < 5.
            # left becomes 0. Loop repeats endlessly. Infinite Loop!
            left = mid 
        else:
            right = mid - 1
    return -1

# ==============================================================================
# 5. ADVANCED INTERVIEW VARIANT
# ==============================================================================
def find_first_occurrence(arr: List[int], target: int) -> int:
    """
    Finds the FIRST occurrence of a target in a sorted array containing duplicates.
    """
    left, right = 0, len(arr) - 1
    first_idx = -1
    
    while left <= right:
        mid = left + (right - left) // 2
        
        if arr[mid] == target:
            first_idx = mid
            # Key difference: Don't return! Keep searching to the left.
            right = mid - 1
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
            
    return first_idx

# ==============================================================================
# 6. TESTING & VALIDATION
# ==============================================================================
def run_tests():
    print("--- Running Binary Search Tests ---")
    arr = [1, 3, 5, 7, 9, 11, 15]
    
    # Iterative Tests
    assert binary_search_iterative(arr, 7) == 3, "Failed to find 7"
    assert binary_search_iterative(arr, 15) == 6, "Failed to find 15 (edge)"
    assert binary_search_iterative(arr, 1) == 0, "Failed to find 1 (edge)"
    assert binary_search_iterative(arr, 100) == -1, "Failed on missing element"
    
    # Recursive Tests
    assert binary_search_recursive(arr, 7, 0, len(arr)-1) == 3
    assert binary_search_recursive(arr, 100, 0, len(arr)-1) == -1
    
    # Library Tests
    assert binary_search_library(arr, 7) == 3
    assert binary_search_library(arr, 100) == -1
    
    # Advanced Variant Tests
    dup_arr = [1, 2, 2, 2, 2, 3, 4]
    assert find_first_occurrence(dup_arr, 2) == 1, "Failed to find first occurrence"
    
    print("All tests passed successfully!")

if __name__ == "__main__":
    run_tests()
    print("\nVisual Trace of Binary Search for Target 7 in [1, 3, 5, 7, 9, 11, 15]:")
    print("Step 1: left=0(1), right=6(15) -> mid=3(7). 7 == 7. Found at index 3!")
