"""
# ==============================================================================
# LABORATORY: HEAPS (UNDER THE HOOD)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You already know that `heapq` implements a Min-Heap. But how does it actually 
# work without using `Node` objects or `left`/`right` pointers?
# A Heap is an "Implicit Data Structure". It is a Complete Binary Tree mathematically 
# mapped onto a standard 1D Array. Understanding this index math is crucial for 
# systems programming and implementing the famous Heap Sort algorithm.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the Array math: Left Child (2i + 1), Right Child (2i + 2), Parent ((i-1)//2).
# - Build a Min-Heap from scratch using `sift_up` and `sift_down`.
# - Understand why `heapify` takes O(N) time instead of O(N log N).
# - Implement Heap Sort.
#
# ==============================================================================
"""

from typing import List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. HEAP ARRAY MATH & SIFTING
# ==============================================================================
class CustomMinHeap:
    """
    A custom implementation of a Min-Heap using a standard Python list.
    No node objects. No pointers. Just math.
    """
    def __init__(self):
        self.heap: List[int] = []
        
    def _parent(self, i: int) -> int:
        return (i - 1) // 2
        
    def _left_child(self, i: int) -> int:
        return 2 * i + 1
        
    def _right_child(self, i: int) -> int:
        return 2 * i + 2
        
    def _swap(self, i: int, j: int) -> None:
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

    def insert(self, val: int) -> None:
        """O(log N): Add to the end of the array, then bubble it up."""
        self.heap.append(val)
        self._sift_up(len(self.heap) - 1)
        
    def _sift_up(self, i: int) -> None:
        # While we are not at the root, AND the current node is SMALLER than its parent...
        while i > 0 and self.heap[i] < self.heap[self._parent(i)]:
            parent_idx = self._parent(i)
            self._swap(i, parent_idx)
            i = parent_idx # Move up the tree

    def extract_min(self) -> int:
        """O(log N): Swap root with the last element, pop it, then bubble the new root down."""
        if not self.heap:
            raise IndexError("extract_min from empty heap")
            
        if len(self.heap) == 1:
            return self.heap.pop()
            
        # Save the min value
        min_val = self.heap[0]
        
        # Move the last element to the root
        self.heap[0] = self.heap.pop()
        
        # Restore the heap property by pushing the new root down
        self._sift_down(0)
        
        return min_val
        
    def _sift_down(self, i: int) -> None:
        n = len(self.heap)
        
        while True:
            smallest = i
            left = self._left_child(i)
            right = self._right_child(i)
            
            # Find the smallest among the node and its two children
            if left < n and self.heap[left] < self.heap[smallest]:
                smallest = left
            if right < n and self.heap[right] < self.heap[smallest]:
                smallest = right
                
            # If the node is already the smallest, the heap is valid. Stop.
            if smallest == i:
                break
                
            # Otherwise, swap with the smallest child and continue down
            self._swap(i, smallest)
            i = smallest


def demonstrate_custom_heap():
    section_header("Custom Min-Heap Implementation (Array Math)")
    
    h = CustomMinHeap()
    values = [9, 4, 7, 1, 3, 2, 8]
    
    print(f"Inserting values: {values}")
    for v in values:
        h.insert(v)
        
    print(f"Internal Array Representation: {h.heap}")
    # Math check: Root is 1. Left child (index 1) is 3. Right child (index 2) is 2.
    
    print("\nExtracting minimums (Should be sorted):")
    sorted_output = []
    while h.heap:
        sorted_output.append(h.extract_min())
        
    print(sorted_output)


# ==============================================================================
# 4. THE O(N) HEAPIFY ALGORITHM
# ==============================================================================
def heapify_array(arr: List[int]) -> None:
    """
    If you have an unsorted array and you insert items one by one into a new heap, 
    it takes O(N log N) time.
    Floyd's Heapify Algorithm does this IN-PLACE in O(N) time!
    
    How? It starts at the lowest non-leaf nodes and calls `sift_down` on them, 
    working backwards up to the root.
    """
    n = len(arr)
    
    def sift_down(i: int):
        while True:
            smallest = i
            left = 2 * i + 1
            right = 2 * i + 2
            
            if left < n and arr[left] < arr[smallest]:
                smallest = left
            if right < n and arr[right] < arr[smallest]:
                smallest = right
            if smallest == i:
                break
            arr[i], arr[smallest] = arr[smallest], arr[i]
            i = smallest

    # The last half of the array are leaves (they have no children).
    # So we only need to sift down the first half, starting from the bottom up!
    last_non_leaf = (n // 2) - 1
    for i in range(last_non_leaf, -1, -1):
        sift_down(i)

def demonstrate_heapify():
    section_header("Floyd's O(N) Heapify Algorithm")
    
    arr = [9, 4, 7, 1, 3, 2, 8]
    print(f"Unsorted Array: {arr}")
    
    heapify_array(arr)
    print(f"In-Place Heapified Array: {arr}")


# ==============================================================================
# 5. HEAP SORT ALGORITHM
# ==============================================================================
def heap_sort(arr: List[int]) -> None:
    """
    Time Complexity: O(N log N)
    Space Complexity: O(1) In-Place
    
    Strategy: 
    1. Build a MAX-HEAP in O(N) time.
    2. Swap the root (largest item) with the last item in the array.
    3. Decrease the simulated "heap size" by 1.
    4. Sift down the new root.
    5. Repeat until the simulated heap size is 1. The array is now sorted!
    """
    n = len(arr)
    
    # 1. Helper function for Max-Heap Sift Down
    def max_sift_down(i: int, heap_size: int):
        while True:
            largest = i
            left = 2 * i + 1
            right = 2 * i + 2
            
            if left < heap_size and arr[left] > arr[largest]:
                largest = left
            if right < heap_size and arr[right] > arr[largest]:
                largest = right
            if largest == i:
                break
            arr[i], arr[largest] = arr[largest], arr[i]
            i = largest

    # 2. Build Max-Heap O(N)
    for i in range((n // 2) - 1, -1, -1):
        max_sift_down(i, n)
        
    # 3. Sort O(N log N)
    for i in range(n - 1, 0, -1):
        # Move current root (largest) to the end
        arr[0], arr[i] = arr[i], arr[0]
        
        # Sift down the new root, but pretend the array is smaller by 1
        max_sift_down(0, i)

def demonstrate_heap_sort():
    section_header("Algorithm: Heap Sort O(N log N) In-Place")
    
    arr = [9, 4, 7, 1, 3, 2, 8]
    print(f"Unsorted Array: {arr}")
    
    heap_sort(arr)
    print(f"Heap Sorted Array: {arr}")


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. How does a Heap store a Binary Tree inside a 1D Array without using Node pointers?
   Answer: It relies on the fact that a heap is a Complete Binary Tree. By storing it sequentially, the mathematical relationship between indices is perfect. For any index `i`, its left child is `2i + 1`, right child is `2i + 2`, and parent is `(i - 1) // 2`.

2. How does `extract_min()` maintain the O(log N) heap structure?
   Answer: It removes the root (index 0). It then takes the very last element in the array and places it at index 0. Finally, it calls `sift_down()` on index 0, which repeatedly swaps the element with its smallest child until the heap property is restored.

3. Why is `heapify` O(N) time, but inserting N elements takes O(N log N)?
   Answer: Inserting elements one-by-one requires a `sift_up` for every element, which travels all the way to the root (log N). Floyd's `heapify` algorithm works bottom-up, calling `sift_down`. Since half the tree are leaves, they don't move at all. The next level up only moves 1 step. Most of the work is done on the smallest possible subtrees, mathematically converging to an O(N) total runtime.
"""

if __name__ == "__main__":
    demonstrate_custom_heap()
    demonstrate_heapify()
    demonstrate_heap_sort()
    print("\n[SUCCESS] Laboratory: Heaps Completed.")
