"""
# ==============================================================================
# LABORATORY: COMPETITIVE PROGRAMMING (CONTEST PRACTICE: HARD)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# "Hard" problems mathematically separate the top 1% of engineers.
# They rarely introduce completely new data structures. Instead, they require 
# you to execute known algorithms with absolute flawless precision, often 
# combining Multiple Pointers, Priority Queues, and mathematical edge-cases.
#
# In "Trapping Rain Water", you are given an array representing the height 
# of a mountain range. It rains. How much water gets trapped in the valleys?
# You could solve this with a Stack or Dynamic Programming, but the true 
# O(N) Time / O(1) Space solution requires a beautiful dual-pointer collision 
# algorithm.
#
# In "Merge K Sorted Lists", you are given 10,000 Linked Lists. You must merge 
# them into one. Comparing them linearly takes O(N * K) time. You must use a 
# Min-Heap (Priority Queue) to mathematically extract the absolute smallest 
# node out of all K lists simultaneously in exactly O(N log K) time.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master the Dual-Pointer Collision algorithm for Trapping Rain Water.
# - Master the Min-Heap architecture for Merging K Arrays/Lists.
#
# ==============================================================================
"""

import heapq

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. DUAL-POINTER COLLISION (TRAPPING RAIN WATER)
# ==============================================================================
def trap_rain_water(heights: list[int]) -> int:
    """
    Problem: Calculate total trapped rain water between elevation blocks.
    Time Complexity: O(N)
    Space Complexity: O(1) - Constant Space!
    """
    if not heights:
        return 0
        
    # We place two pointers at the absolute edges of the array.
    left, right = 0, len(heights) - 1
    
    # We track the absolute highest mountains we have seen so far on both sides.
    max_left, max_right = 0, 0
    total_water = 0
    
    # The pointers move inward and eventually collide.
    while left < right:
        # The amount of water trapped at any specific index is strictly determined 
        # by the SHORTER of the two tallest mountains bounding it.
        # Water = min(max_left, max_right) - current_height.
        
        # We always process the mathematically smaller side!
        if heights[left] < heights[right]:
            # Can this block hold water?
            if heights[left] >= max_left:
                # No! It is the new tallest mountain on the left. It physically 
                # cannot hold water above itself. Update the max.
                max_left = heights[left]
            else:
                # Yes! It is smaller than `max_left`. Because we ALREADY KNOW 
                # that `heights[right]` is even taller than `max_left`, we mathematically 
                # guarantee this block is bounded on both sides!
                total_water += (max_left - heights[left])
                
            # Move the left pointer inward
            left += 1
            
        else:
            # Symmetrical logic for the right side
            if heights[right] >= max_right:
                max_right = heights[right]
            else:
                total_water += (max_right - heights[right])
                
            right -= 1
            
    return total_water

def demonstrate_trapping_water():
    section_header("Dual-Pointer (Trapping Rain Water)")
    
    # Elevation map
    heights = [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]
    print(f"Elevation Map: {heights}")
    
    water = trap_rain_water(heights)
    
    print(f"\nTotal Water Trapped: {water} units.")
    print("Expected: 6 units.")
    print("The O(1) space dual-pointer method perfectly calculated the bounds ")
    print("without needing to pre-calculate DP arrays!")


# ==============================================================================
# 4. MIN-HEAP (MERGE K SORTED ARRAYS/LISTS)
# ==============================================================================
def merge_k_sorted_arrays(arrays: list[list[int]]) -> list[int]:
    """
    Problem: Merge K sorted arrays into a single sorted array.
    (This is identical to Merge K Sorted Linked Lists, just using Arrays for simplicity).
    
    Time Complexity: O(N * log K) where N is total elements, K is number of arrays.
    Space Complexity: O(K) for the Priority Queue.
    """
    # The Heap will store tuples: (value, array_index, element_index)
    min_heap = []
    
    # 1. Initialization Step
    # We take the absolute first element from EVERY array and push it into the Heap.
    # The heap instantly sorts them and brings the absolute smallest to the top!
    for array_idx, array in enumerate(arrays):
        if array: # If the array is not empty
            # Push: (Value, Which Array it came from, Its Index in that Array)
            heapq.heappush(min_heap, (array[0], array_idx, 0))
            
    merged_result = []
    
    # 2. Extraction and Replacement Step
    while min_heap:
        # Pop the absolute smallest value currently known in the universe!
        val, array_idx, element_idx = heapq.heappop(min_heap)
        merged_result.append(val)
        
        # We just removed an element from `array_idx`. 
        # We must immediately replace it with the NEXT element from that exact same array!
        next_element_idx = element_idx + 1
        
        if next_element_idx < len(arrays[array_idx]):
            next_val = arrays[array_idx][next_element_idx]
            heapq.heappush(min_heap, (next_val, array_idx, next_element_idx))
            
    return merged_result

def demonstrate_merge_k():
    section_header("Min-Heap (Merge K Sorted Arrays)")
    
    arrays = [
        [1, 4, 5],
        [1, 3, 4],
        [2, 6]
    ]
    
    print("3 Sorted Arrays:")
    for arr in arrays:
        print(arr)
        
    ans = merge_k_sorted_arrays(arrays)
    
    print(f"\nMerged Result: {ans}")
    print("The Min-Heap maintained a size of exactly K (3), allowing us to ")
    print("extract the minimums in strict O(log K) time per element!")


def run_all_labs():
    demonstrate_trapping_water()
    demonstrate_merge_k()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. In Trapping Rain Water, how does the Dual-Pointer approach mathematically prove it is safe to calculate water based on `max_left` without knowing the exact value of `max_right`?
   Answer: The logic heavily relies on the `if heights[left] < heights[right]:` condition. If this condition is true, we mathematically *guarantee* that whatever the maximum height on the right side of the array is, it is definitely $\ge heights[right]$, which is strictly $> heights[left]$. Therefore, `heights[left]` is mathematically locked as the *global bottleneck* for that specific column of water. We don't need to know if the right side has a mountain of size 100 or size 1000. We just need to know it is taller than our current side. Because of this guarantee, we can safely calculate `Water = max_left - current_height` using only the local maximum!

2. Why is Merging K Arrays using a Min-Heap $O(N \log K)$ instead of $O(N \log N)$?
   Answer: $N$ represents the *total* number of elements across all arrays combined. If you threw all $N$ elements into a giant single array and called `.sort()`, it would take $O(N \log N)$ time. By using a Min-Heap, we exploit the fact that the individual arrays are *already sorted*. The Min-Heap only ever contains exactly $K$ elements at any given time (one element from the front of each array). Extracting the minimum and inserting the next element takes exactly $O(\log K)$ time. Since we do this for all $N$ elements, the total time is strictly $O(N \log K)$. If $N = 100,000$ and $K = 3$, $O(N \log 3)$ is virtually $O(N)$ linear time!

3. In the `merge_k_sorted_arrays` function, why do we store the tuple `(value, array_idx, element_idx)` in the heap?
   Answer: The Min-Heap automatically sorts elements based on the first item in the tuple (`value`). But when we `pop()` the smallest value and append it to our final list, the Heap has a gaping hole! We must fetch the *next* element to replace it. But how do we know where the popped element came from? By explicitly storing `array_idx` (which array it belonged to) and `element_idx` (its specific position within that array), we provide the exact coordinates needed to confidently say: "Go to `arrays[array_idx]`, fetch `element_idx + 1`, and push it into the Heap!"
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Contest Practice (Hard) Completed.")
