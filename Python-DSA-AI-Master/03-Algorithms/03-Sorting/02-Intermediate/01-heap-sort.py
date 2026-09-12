"""
Module: Heap Sort
=================

## A. Concept Name
Heap Sort

## B. One-Sentence Definition
Heap Sort is an in-place, comparison-based sorting algorithm that uses a binary heap data structure to build a max-heap and repeatedly extract the maximum element to sort an array.

## C. Core Intuition
Instead of finding the maximum element by scanning the array repeatedly (like selection sort), Heap Sort organizes the data into a tree structure (a heap) that allows for fast $O(\log n)$ extraction of the largest element, while maintaining the heap property efficiently.

## D. Visual Model
Imagine a complete binary tree where every parent node is greater than or equal to its children (max-heap). We repeatedly take the root (the largest item), swap it with the last leaf, shrink the tree by one, and sift down the new root to restore order.

## E. Step-by-Step Walkthrough
1. Build a max-heap from the input array.
2. The largest item is now at the root of the heap (index 0).
3. Swap the root with the last element in the heap.
4. Reduce the considered size of the heap by 1.
5. Sift down the new root (heapify) to restore the max-heap property.
6. Repeat steps 3-5 until the heap size is 1.

## F. Time Complexity
Best, Worst, and Average Case: $O(n \log n)$. Building the heap takes $O(n)$ time, and extracting the elements takes $O(n \log n)$ time.

## G. Space Complexity
$O(1)$ auxiliary space. The sorting is done in-place by rearranging the elements in the input array.

## H. Stability
Not stable. The relative order of equal elements might not be preserved during the swap and heapify operations.

## I. In-place vs Out-of-place
In-place. No extra arrays or data structures are required.

## J. Best/Worst Cases
Both best and worst cases are $O(n \log n)$. Unlike Quick Sort, there is no $O(n^2)$ worst-case scenario.

## K. When to Use
Use when $O(n \log n)$ time complexity is strictly required and auxiliary memory is severely limited (e.g., embedded systems). It provides a strong worst-case guarantee.

## L. When NOT to Use
Avoid when stability is required or when average-case performance needs to be maximized (Quick Sort is often faster in practice due to better cache locality).

## M. Pattern Recognition
Useful for "Kth largest/smallest" problems, priority queue implementations, and situations requiring consistent worst-case performance bounds.

## N. Real-world Applications
Operating system task scheduling, priority queues, and algorithms like Dijkstra's Shortest Path or Prim's Minimum Spanning Tree.

## O. Common Pitfalls
Forgetting that array elements are 0-indexed, meaning the left child is $2i + 1$ and the right child is $2i + 2$. Using 1-based indexing math on a 0-based array causes out-of-bounds errors.

## P. Debugging
Print the array after the initial `build_max_heap` step. If the first element isn't the absolute maximum, the heapify logic is flawed. Then, trace the array after each extraction to ensure the sorted partition grows correctly at the end.

## Q. Edge Cases
- Empty arrays or single-element arrays (already sorted).
- Arrays with all identical elements.
- Arrays that are already sorted (ascending or descending).

## R. Optimization
Although standard heap sort uses recursive `heapify`, an iterative approach can avoid function call overhead. Additionally, a "bottom-up" heap sort can reduce the number of comparisons by sinking the root all the way to the bottom and then bubbling it back up.

## S. Related Algorithms
- Quick Sort (faster average case but worse worst case).
- Merge Sort (stable and fast, but requires $O(n)$ extra space).
- Selection Sort (similar idea of finding the max/min, but uses $O(n^2)$ time).

## T. Prerequisites
Understanding of binary trees, array representation of complete binary trees, and the max-heap property.

## U. AI/ML Applications
Priority queues are used in search algorithms like A* for pathfinding, which are fundamental in classical AI. Also used in K-nearest neighbors (KNN) optimizations when maintaining the top K closest points.

## V. System Design Implications
Because Heap Sort is an in-place $O(n \log n)$ algorithm, it is an excellent fallback algorithm for language runtimes (like Introsort) when Quick Sort degrades to $O(n^2)$.

## W. Common Interview Questions
1. "Why is Heap Sort not stable?"
2. "How do you find the Kth largest element in an array using a Heap?"
3. "Compare Heap Sort, Merge Sort, and Quick Sort."

## X. Project Connection
In AI/DSA projects, Heap Sort is often integrated into hybrid sorting algorithms (like Introsort in Python's `sort()` underlying C++ implementations) or used to manage dynamic priority queues in real-time simulations.
"""

from typing import List

def heapify(arr: List[int], n: int, i: int) -> None:
    """
    To heapify a subtree rooted with node i.
    n is size of heap.
    """
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2
    
    # See if left child of root exists and is greater than root
    if left < n and arr[i] < arr[left]:
        largest = left
        
    # See if right child of root exists and is greater than root
    if right < n and arr[largest] < arr[right]:
        largest = right
        
    # Change root, if needed
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        # Heapify the root.
        heapify(arr, n, largest)

def heap_sort(arr: List[int]) -> List[int]:
    """
    Implementation of Heap Sort.
    """
    n = len(arr)
    
    # Build a maxheap.
    # Since last parent will be at ((n//2)-1) we can start at that location.
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)
        
    # One by one extract elements
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i] # swap
        heapify(arr, i, 0)
        
    return arr

def complexity_analysis():
    """
    Time Complexity:
    - Best/Worst/Average Case: O(N log N)
    
    Space Complexity: O(1) in-place sorting.
    Stability: Not stable.
    """
    pass

def run_tests():
    arr = [12, 11, 13, 5, 6, 7]
    expected = [5, 6, 7, 11, 12, 13]
    
    assert heap_sort(arr.copy()) == expected
    assert heap_sort([5, 4, 3, 2, 1]) == [1, 2, 3, 4, 5]
    
    print("[+] Heap Sort tests passed!")

if __name__ == "__main__":
    run_tests()
