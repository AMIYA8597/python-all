"""
Module: Bucket Sort
===================

Learning Objectives:
1. Understand the core mechanics of Bucket Sort (Scatter-Gather approach).
2. Learn how to map elements to buckets efficiently using a hash-like function.
3. Understand when Bucket Sort is optimal (uniformly distributed data) and its degradation scenarios.
4. Implement a robust Bucket Sort that handles different data ranges, not just [0, 1).

-------------------------------------------------------------------
1. Intuition & Real-World Analogy
-------------------------------------------------------------------
Real-World Analogy:
Imagine you are sorting a massive pile of unorganized mail by postal code. 
Instead of comparing each letter against every other letter (like QuickSort or MergeSort), 
you set up a series of bins labeled "00000-09999", "10000-19999", etc. 
You first "scatter" the letters into these bins based on the leading digits of the postal code.
Then, you sort the smaller pile within each bin individually (perhaps using Insertion Sort). 
Finally, you "gather" all the letters from the bins in order.

Intuition:
Bucket sort takes advantage of our knowledge about the data's distribution. 
By dividing a global sorting problem into many local, smaller sorting problems, 
we can achieve linear time sorting O(N), provided the data is uniformly distributed across the buckets.

Memory Anchor: "Scatter, Sort, Gather."
- Scatter items into buckets based on their value.
- Sort each bucket individually.
- Gather items from buckets sequentially.

-------------------------------------------------------------------
2. Formal Explanation
-------------------------------------------------------------------
Bucket Sort relies on a mapping function (similar to a hash function) that assigns each element 
to a bucket index. 

Given an array `arr` of size `N`:
1. Create `K` empty buckets.
2. Iterate over `arr` and map each element to a bucket index. 
   The most common mapping function for elements distributed between `min_val` and `max_val` is:
   `index = floor(K * (value - min_val) / (max_val - min_val))`
3. Sort each individual bucket (often using Insertion Sort for small arrays).
4. Concatenate the sorted buckets to form the fully sorted array.

-------------------------------------------------------------------
3. Implementation (Professional Grade)
-------------------------------------------------------------------
We will implement a versatile Bucket Sort that is not restricted to floating-point numbers in [0, 1), 
but can handle any numerical values (integers or floats) by calculating the minimum and maximum.
"""

from typing import List, TypeVar, Union
import math

# Type alias for numerical values
Num = TypeVar('Num', int, float)

def insertion_sort(bucket: List[Num]) -> List[Num]:
    """
    Sorts a small bucket using Insertion Sort.
    Insertion Sort is highly efficient for small or nearly sorted arrays.
    """
    for i in range(1, len(bucket)):
        current_val = bucket[i]
        j = i - 1
        # Shift elements greater than current_val to the right
        while j >= 0 and bucket[j] > current_val:
            bucket[j + 1] = bucket[j]
            j -= 1
        bucket[j + 1] = current_val
    return bucket


def bucket_sort(arr: List[Num], num_buckets: int = -1) -> List[Num]:
    """
    Sorts an array using Bucket Sort.
    
    Args:
        arr: The list of numerical values to sort.
        num_buckets: The number of buckets to use. If -1, dynamically calculated.
        
    Returns:
        A new sorted list.
    """
    if not arr or len(arr) == 1:
        return arr.copy()
        
    # 1. Determine min and max to understand the range
    min_val = min(arr)
    max_val = max(arr)
    
    # If all elements are exactly the same, no need to sort
    if min_val == max_val:
        return arr.copy()
        
    # Default to len(arr) buckets for an expected O(1) elements per bucket 
    # if data is uniformly distributed
    if num_buckets <= 0:
        num_buckets = len(arr)
        
    # Initialize empty buckets
    buckets: List[List[Num]] = [[] for _ in range(num_buckets)]
    
    # 2. Scatter: Distribute elements into buckets
    val_range = max_val - min_val
    for num in arr:
        # Mapping function: normalize value to [0, 1), then multiply by num_buckets
        normalized = (num - min_val) / val_range
        index = int(normalized * num_buckets)
        
        # Edge case: max_val will map to index == num_buckets, which is out of bounds
        if index == num_buckets:
            index -= 1
            
        buckets[index].append(num)
        
    # 3. Sort: Sort individual buckets
    for i in range(num_buckets):
        # We can use insertion_sort, or Python's built-in Timsort (which is optimized)
        # We'll use our insertion_sort to stick to the classical algorithm design
        buckets[i] = insertion_sort(buckets[i])
        
    # 4. Gather: Concatenate the results
    sorted_arr = []
    for bucket in buckets:
        sorted_arr.extend(bucket)
        
    return sorted_arr

"""
-------------------------------------------------------------------
4. Complexity Analysis
-------------------------------------------------------------------
Let N be the number of elements and K be the number of buckets.

Time Complexity:
- Best Case: O(N + K)
  Occurs when elements are uniformly distributed and each bucket gets O(N/K) elements.
  If K = N, each bucket gets O(1) elements. Sorting K buckets takes O(K) time, plus O(N) to scatter.
- Average Case: O(N + K)
  When data distribution is fairly uniform.
- Worst Case: O(N^2)
  Occurs when all elements map to the exact same bucket.
  The algorithm degrades to the time complexity of the inner sorting algorithm (Insertion Sort -> O(N^2)).
  
Space Complexity: O(N + K)
- We need O(N) auxiliary space to store the elements inside buckets.
- We need O(K) space for the bucket pointers/lists themselves.
This makes Bucket Sort an Out-Of-Place (not in-place) sorting algorithm.

-------------------------------------------------------------------
5. Common Mistakes & Debugging
-------------------------------------------------------------------
Common Mistakes:
1. Hardcoding the range: Beginners often assume the input is strictly between [0.0, 1.0).
   Fix: Always compute `min_val` and `max_val` to normalize dynamically.
2. Out of bounds index for `max_val`: Since the normalized value of `max_val` is 1.0, 
   `int(1.0 * K)` gives `K`, causing an IndexError.
   Fix: Explicitly check `if index == K: index -= 1`.
3. Choosing the wrong inner sort: Using QuickSort inside the buckets adds unnecessary overhead. 
   Insertion Sort is faster for tiny arrays (size < 10-20), which bucket sort naturally produces.

Debugging Tips:
- Print the sizes of the buckets before the sort step. If one bucket has almost all elements 
  (e.g., len(bucket[i]) ≈ N), your data is heavily skewed or your mapping function is wrong.
- Verify that `min_val != max_val` early on to prevent ZeroDivisionError during normalization.

-------------------------------------------------------------------
6. Active Recall & Memory Anchors
-------------------------------------------------------------------
Q1. When should you choose Bucket Sort over Merge Sort?
A1. When the input data is known to be uniformly distributed across a range, allowing O(N) time complexity.

Q2. What causes Bucket Sort to degrade to O(N^2)?
A2. When elements are highly clustered, meaning they all fall into a single bucket, and Insertion Sort is used.

Q3. Why is Insertion Sort typically used to sort individual buckets?
A3. Because uniformly distributed buckets will contain very few elements, and Insertion Sort has extremely low overhead for small arrays.
"""

def run_tests():
    """Test suite for professional bucket sort implementation."""
    
    # 1. Standard float array
    floats = [0.897, 0.565, 0.656, 0.1234, 0.665, 0.3434]
    assert bucket_sort(floats) == sorted(floats), "Failed on standard floats"
    
    # 2. Integers with negative numbers
    ints = [10, -5, 23, 15, -10, 0, 8, 42, 1]
    assert bucket_sort(ints) == sorted(ints), "Failed on integers with negatives"
    
    # 3. Already sorted
    sorted_arr = [1.1, 2.2, 3.3, 4.4, 5.5]
    assert bucket_sort(sorted_arr) == sorted(sorted_arr), "Failed on sorted array"
    
    # 4. Reverse sorted
    reverse_arr = [5.5, 4.4, 3.3, 2.2, 1.1]
    assert bucket_sort(reverse_arr) == sorted(reverse_arr), "Failed on reverse sorted array"
    
    # 5. All same elements
    same_arr = [4, 4, 4, 4, 4]
    assert bucket_sort(same_arr) == same_arr, "Failed on identical elements"
    
    # 6. Single element and empty
    assert bucket_sort([42]) == [42], "Failed on single element"
    assert bucket_sort([]) == [], "Failed on empty list"
    
    print("[+] All Bucket Sort tests passed successfully!")

if __name__ == "__main__":
    run_tests()
