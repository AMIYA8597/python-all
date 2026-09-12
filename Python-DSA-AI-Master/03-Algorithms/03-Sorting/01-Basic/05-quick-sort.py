"""
# Quick Sort: Beginner to Professional

## 1. What is it?
Quick Sort is a highly efficient, in-place, divide-and-conquer sorting algorithm. It works by selecting a "pivot" element from the array and partitioning the other elements into two sub-arrays: those less than the pivot and those greater than the pivot. The sub-arrays are then sorted recursively.

## 2. Why does it exist?
While algorithms like Bubble Sort or Insertion Sort take O(N^2) time, making them unscalable for large datasets, Quick Sort achieves O(N log N) time on average. It exists because we need a fast, general-purpose sorting algorithm that doesn't require extra memory (unlike Merge Sort, which requires O(N) auxiliary space). 

## 3. What problem does it solve?
It solves the problem of organizing data efficiently in-place. Efficient sorting is the prerequisite for binary search, database indexing, and many machine learning data-preprocessing steps.

## 4. Intuition & Mental Model
Imagine you are organizing a disorganized stack of test papers by student ID.
1. **Choose a pivot:** You grab a random paper from the middle (say, ID 50).
2. **Partition:** You make two new piles. Everything less than 50 goes in the left pile. Everything greater goes in the right pile. 
3. **Recurse:** You now have two smaller piles. You repeat the exact same process for the left pile and the right pile until every pile has exactly 1 paper.
4. **Result:** When you stack them back together, they are perfectly sorted!

## 5. Formal Definition
Given an array `A` of `n` elements:
1. **Divide**: Choose an element `x` from `A` as a pivot. Rearrange `A` such that all elements <= `x` are placed before `x`, and all elements > `x` are placed after it.
2. **Conquer**: Recursively sort the subarrays `A[0...pivot_index-1]` and `A[pivot_index+1...n-1]`.
3. **Combine**: No work is needed because the array is sorted in place.

## 6. Time and Space Complexity
- **Best Case Time**: O(N log N). Occurs when the pivot always divides the array into two equal halves.
- **Average Case Time**: O(N log N).
- **Worst Case Time**: O(N^2). Occurs when the array is already sorted (or reverse sorted) and we pick the first or last element as the pivot. The array splits into 0 and N-1 elements.
- **Space Complexity**: O(log N) average, O(N) worst case (due to the recursive call stack). It operates in-place, requiring no extra arrays.

## 7. Trade-offs (Quick Sort vs Merge Sort)
- **Memory**: Quick Sort is in-place O(1) auxiliary space (excluding stack). Merge Sort requires O(N) extra space.
- **Stability**: Quick Sort is typically *unstable* (equal elements might swap relative order). Merge Sort is *stable*.
- **Worst Case**: Quick Sort worst case is O(N^2). Merge Sort is always O(N log N).
- **Practical Speed**: Quick Sort is often faster in practice due to good cache locality and smaller constant factors.

## 8. When NOT to use Quick Sort
- When you need a **stable** sort (e.g., sorting users by Age, and wanting to preserve their previous sorting by Name). Use Merge Sort or Timsort.
- When you are sorting a linked list. (Merge sort is generally better for linked lists because random access is slow).
- When guaranteed O(N log N) worst-case time is strictly required (use Heap Sort).

---
"""

from typing import List
import random
import time
import sys

# ============================================================================
# IMPLEMENTATION 1: Pythonic (Educational but NOT memory efficient)
# ============================================================================
def quick_sort_pythonic(arr: List[int]) -> List[int]:
    """
    Pythonic implementation using list comprehensions.
    
    Why learn this? It perfectly illustrates the mental model.
    Why avoid this in production? It creates multiple new arrays, violating 
    the O(1) in-place space advantage of real Quick Sort.
    """
    if len(arr) <= 1:
        return arr
    
    pivot = arr[len(arr) // 2]  # Middle element
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    
    return quick_sort_pythonic(left) + middle + quick_sort_pythonic(right)


# ============================================================================
# IMPLEMENTATION 2: Professional In-Place Quick Sort (Lomuto Partition Scheme)
# ============================================================================
def partition_lomuto(arr: List[int], low: int, high: int) -> int:
    """
    Lomuto partition scheme.
    Chooses the last element as the pivot.
    Maintains an index `i` of the smaller element.
    """
    # 1. Randomize pivot to avoid O(N^2) on sorted arrays
    # Swap a random element with the last element
    rand_idx = random.randint(low, high)
    arr[rand_idx], arr[high] = arr[high], arr[rand_idx]
    
    pivot = arr[high]
    i = low - 1  # Points to the end of the "less than pivot" region
    
    for j in range(low, high):
        # If current element is smaller than or equal to pivot
        if arr[j] <= pivot:
            i += 1
            # Swap it into the "less than pivot" region
            arr[i], arr[j] = arr[j], arr[i]
            
    # Swap the pivot into its correct absolute position
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    
    # Return the index of the pivot
    return i + 1

def quick_sort_inplace(arr: List[int], low: int, high: int) -> None:
    """
    In-place recursive implementation of Quick Sort.
    """
    if low < high:
        # pi is partitioning index, arr[pi] is now at right place
        pi = partition_lomuto(arr, low, high)
        
        # Separately sort elements before partition and after partition
        quick_sort_inplace(arr, low, pi - 1)
        quick_sort_inplace(arr, pi + 1, high)


# ============================================================================
# IMPLEMENTATION 3: Advanced (Hoare Partition Scheme)
# ============================================================================
# Hoare's scheme is generally more efficient than Lomuto's because it does 
# three times fewer swaps on average. It uses two pointers starting from ends.

def partition_hoare(arr: List[int], low: int, high: int) -> int:
    pivot = arr[low + (high - low) // 2] # Middle element
    i = low - 1
    j = high + 1
    
    while True:
        # Move right until we find an element >= pivot
        i += 1
        while arr[i] < pivot:
            i += 1
            
        # Move left until we find an element <= pivot
        j -= 1
        while arr[j] > pivot:
            j -= 1
            
        if i >= j:
            return j
            
        # Swap the elements
        arr[i], arr[j] = arr[j], arr[i]

def quick_sort_hoare(arr: List[int], low: int, high: int) -> None:
    if low < high:
        pi = partition_hoare(arr, low, high)
        quick_sort_hoare(arr, low, pi)
        quick_sort_hoare(arr, pi + 1, high)


# ============================================================================
# DEBUGGING EXERCISE: Find the Bug!
# ============================================================================
def buggy_partition(arr: List[int], low: int, high: int) -> int:
    """
    BUGGY VERSION: Can you spot the mistake?
    """
    pivot = arr[high]
    i = low
    for j in range(low, high):
        if arr[j] < pivot:
            arr[i], arr[j] = arr[j], arr[i]
            i += 1
    # BUG: Forgot to put the pivot in its correct place!
    # Correct code should be: arr[i], arr[high] = arr[high], arr[i]
    return i

# ============================================================================
# ACTIVE RECALL & INTERVIEW PREPARATION
# ============================================================================
"""
Q: What is the worst-case time complexity of Quick Sort and when does it happen?
A: O(N^2). It happens when the array is already sorted (or reverse sorted) AND 
   we always pick the first/last element as the pivot.

Q: How do we fix the worst-case scenario in real life?
A: Randomize the pivot selection, or use a "median of three" approach (pick the 
   median of the first, middle, and last elements as the pivot).

Q: Is Quick Sort stable? Why or why not?
A: No, standard in-place Quick Sort is NOT stable. The swapping during the 
   partitioning phase can change the relative order of equal elements.

Q: Why is Quick Sort preferred over Merge Sort for arrays, despite the O(N^2) worst case?
A: 1. It is an in-place sort, saving memory.
   2. It has excellent cache locality (array elements are accessed sequentially), 
      making it very fast on modern CPU architectures.
"""

# ============================================================================
# TESTS & VERIFICATION
# ============================================================================
def run_tests():
    print("Running Quick Sort Tests...")
    
    # 1. Basic test
    arr1 = [10, 7, 8, 9, 1, 5]
    quick_sort_inplace(arr1, 0, len(arr1) - 1)
    assert arr1 == [1, 5, 7, 8, 9, 10], f"Failed: {arr1}"
    
    # 2. Already sorted
    arr2 = [1, 2, 3, 4, 5]
    quick_sort_inplace(arr2, 0, len(arr2) - 1)
    assert arr2 == [1, 2, 3, 4, 5]
    
    # 3. Reverse sorted
    arr3 = [5, 4, 3, 2, 1]
    quick_sort_inplace(arr3, 0, len(arr3) - 1)
    assert arr3 == [1, 2, 3, 4, 5]
    
    # 4. Duplicates
    arr4 = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]
    quick_sort_inplace(arr4, 0, len(arr4) - 1)
    assert arr4 == sorted([3, 1, 4, 1, 5, 9, 2, 6, 5, 3])
    
    # 5. Hoare's Scheme Test
    arr5 = [10, 7, 8, 9, 1, 5]
    quick_sort_hoare(arr5, 0, len(arr5) - 1)
    assert arr5 == [1, 5, 7, 8, 9, 10]
    
    print("All tests passed successfully!")

# ============================================================================
# MEMORY ANCHOR
# ============================================================================
"""
## MEMORY ANCHOR
### One sentence to remember
Quick Sort is a Divide & Conquer algorithm that partitions an array around a pivot, sorting the left and right sides in-place.

### Three things not to confuse
1. Quick Sort vs Merge Sort: Quick Sort is in-place but unstable. Merge sort needs O(N) memory but is stable.
2. Lomuto vs Hoare: Lomuto uses the last element and one pointer. Hoare uses two pointers moving towards each other (faster).
3. Best vs Worst case: Best is O(N log N). Worst is O(N^2) (prevented by random pivots).
"""

if __name__ == "__main__":
    # Increase recursion depth for worst-case large arrays (optional but good practice)
    sys.setrecursionlimit(2000)
    run_tests()
