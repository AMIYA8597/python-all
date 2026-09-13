"""
# ==============================================================================
# LABORATORY: DIVIDE & CONQUER (RECURSIVE BINARY SEARCH)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You have reached the "Divide and Conquer" paradigm.
# 
# Divide and Conquer works in 3 steps:
# 1. DIVIDE the problem into smaller, NON-OVERLAPPING subproblems.
# 2. CONQUER the subproblems by solving them recursively.
# 3. COMBINE the answers of the subproblems to solve the original problem.
#
# The most pure, fundamental example of Divide & Conquer is Binary Search.
# If you have a sorted array of 1 Billion numbers, a naive loop takes 1 Billion 
# operations to find your target.
# 
# Binary Search looks at the middle element. Is it too high? 
# If yes, we instantly throw away the entire right half of the array (500 million 
# numbers) and recursively search the left half.
# 
# It divides the dataset by 2 at every step. 
# 1,000,000,000 -> 500M -> 250M -> 125M ... -> 1.
# It takes exactly 30 operations to search 1 Billion numbers.
# This mathematically defines O(log2 N) Time Complexity.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the 3 pillars of Divide & Conquer.
# - Implement standard Recursive Binary Search.
# - Prevent the infamous Integer Overflow bug when calculating `mid`.
#
# ==============================================================================
"""

from typing import List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. RECURSIVE BINARY SEARCH (O(log N))
# ==============================================================================
def binary_search_recursive(nums: List[int], target: int, left: int, right: int) -> int:
    """
    Time Complexity: O(log N)
    Space Complexity: O(log N) due to the Recursion Call Stack.
                      (Iterative Binary Search is O(1) Space).
    """
    
    # 1. BASE CASE (FAILURE)
    # If the left pointer crosses the right pointer, the subproblem is empty.
    # The target mathematically does not exist in the array.
    if left > right:
        return -1
        
    # 2. DIVIDE (FIND THE MIDDLE)
    # Why don't we use `(left + right) // 2` ?
    # In Python, integers have arbitrary precision, so it doesn't matter.
    # BUT in Java, C++, or Go, if `left` and `right` are massive numbers 
    # (e.g. 2 Billion), adding them together yields 4 Billion, which exceeds 
    # the 32-bit integer limit (2.14 Billion). The program will crash!
    # The FAANG-safe way is to calculate the distance between them, halve it, 
    # and add it to the left pointer.
    mid = left + (right - left) // 2
    
    # 3. CONQUER (RECURSIVE CALLS)
    if nums[mid] == target:
        # We found it!
        return mid
        
    elif nums[mid] > target:
        # The middle element is too big. The target MUST be in the left half.
        # We discard `mid` and everything to the right of it.
        return binary_search_recursive(nums, target, left, mid - 1)
        
    else:
        # The middle element is too small. The target MUST be in the right half.
        # We discard `mid` and everything to the left of it.
        return binary_search_recursive(nums, target, mid + 1, right)


def demonstrate_binary_search():
    section_header("Algorithm: Recursive Binary Search")
    
    nums = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]
    target = 23
    
    print(f"Sorted Input Array: {nums}")
    print(f"Target Value: {target}")
    
    print("\nExecuting Recursive Divide & Conquer...")
    # Initialize bounds to encompass the entire array
    ans = binary_search_recursive(nums, target, 0, len(nums) - 1)
    
    print(f"Target found at Index: {ans} (Expected: 5)")
    
    print("\nVisualizing the Recursion:")
    print("Call 1: L=0, R=9 -> Mid=4 (Val 16). 16 < 23. Search Right!")
    print("Call 2: L=5, R=9 -> Mid=7 (Val 56). 56 > 23. Search Left!")
    print("Call 3: L=5, R=6 -> Mid=5 (Val 23). 23 == 23. Found!")


# ==============================================================================
# 4. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why does Divide & Conquer require the array to be sorted?
   Answer: Because we are making a mathematical assumption! If `nums[mid] > target`, we assume that EVERY element to the right of `mid` is ALSO strictly greater than the target, allowing us to safely throw half the array away. If the array was unsorted, a smaller number could be hiding on the right side, and we would just blindly delete it.

2. Why is Iterative Binary Search usually preferred over Recursive Binary Search?
   Answer: Space Complexity! Recursive Binary Search takes $O(\\log N)$ memory because every time it splits the array, it opens a new function in the Operating System's Call Stack. An Iterative Binary Search uses a `while left <= right:` loop, which takes strictly $O(1)$ constant memory and avoids the tiny CPU overhead of jumping to new function memory addresses.

3. Is Binary Search always $O(\\log N)$?
   Answer: Yes, standard Binary Search on an array is exactly $O(\\log_2 N)$. However, if you are doing a "Ternary Search" (splitting into 3 parts instead of 2), it becomes $O(\\log_3 N)$. The base of the logarithm represents the number of partitions you create at each step of the Divide phase.
"""

if __name__ == "__main__":
    demonstrate_binary_search()
    print("\n[SUCCESS] Laboratory: Recursive Binary Search Completed.")
