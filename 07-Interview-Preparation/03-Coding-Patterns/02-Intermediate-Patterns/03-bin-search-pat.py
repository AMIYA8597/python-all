"""
# ==============================================================================
# LABORATORY: INTERVIEW PREPARATION (CODING PATTERNS - BINARY SEARCH)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Interviewer: "Find an element in a sorted array of 1 Trillion items."
#
# A junior engineer uses a `for` loop (Linear Search). It executes 1 Trillion 
# times, consuming 100% of the CPU for 10 minutes.
# 
# A senior engineer writes a Binary Search. Because the data is sorted, they check 
# the absolute middle. If the middle is too big, they mathematically eliminate 
# the entire right half of the universe. By destroying half the data structure 
# every single loop, 1 Trillion items is mathematically reduced to exactly 40 
# iterations! (log2(1,000,000,000,000) ≈ 40). O(log N) is practically O(1).
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master the mathematical template for standard Binary Search.
# - Master the 'Modified Binary Search' (Rotated Sorted Array).
# - Understand the horrific Integer Overflow bug in `(left + right) // 2`.
#
# ==============================================================================
"""

from typing import List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. STANDARD BINARY SEARCH
# ==============================================================================
def binary_search(nums: List[int], target: int) -> int:
    """
    Time: O(log N) | Space: O(1)
    The array MUST be sorted.
    """
    left = 0
    right = len(nums) - 1
    
    print(f"  Target: {target}")
    
    # CRITICAL: It MUST be `<=`, not `<`. 
    # If the array has only 1 element, left == right. If we use `<`, the loop 
    # will never execute, and we will falsely return -1!
    while left <= right:
        # THE INTEGER OVERFLOW BUG:
        # In Java/C++, `mid = (left + right) / 2` will crash if left + right > 2 Billion!
        # The mathematically perfect way to calculate mid is: left + (right - left) // 2.
        # Python automatically handles arbitrarily large integers, so we can cheat here.
        mid = left + (right - left) // 2
        
        print(f"  Bounds: [{left}, {right}] -> Mid Index: {mid}, Mid Value: {nums[mid]}")
        
        if nums[mid] == target:
            print("    -> TARGET FOUND!")
            return mid
        elif nums[mid] < target:
            # The middle value is too small. 
            # Because it's sorted, EVERYTHING to the left is also too small.
            # We violently annihilate the left half!
            print("    -> Too small. Annihilating left half.")
            left = mid + 1
        else:
            print("    -> Too large. Annihilating right half.")
            right = mid - 1
            
    return -1

def demonstrate_binary_search():
    section_header("Standard Binary Search")
    
    nums = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]
    target = 23
    
    print(f"Sorted Array: {nums}\n")
    
    result = binary_search(nums, target)
    print(f"\nResult: Target found at index {result}")


# ==============================================================================
# 4. MODIFIED BINARY SEARCH (ROTATED SORTED ARRAY)
# ==============================================================================
def search_rotated_array(nums: List[int], target: int) -> int:
    """
    Time: O(log N) | Space: O(1)
    The array was sorted, but then "rotated" at some pivot.
    Example: [0,1,2,4,5,6,7] might become [4,5,6,7,0,1,2].
    We can still use Binary Search, but we must logically determine WHICH half 
    is mathematically intact (sorted) before we can eliminate anything!
    """
    left, right = 0, len(nums) - 1
    
    while left <= right:
        mid = left + (right - left) // 2
        
        print(f"  Bounds: [{left}, {right}] -> Mid: {nums[mid]}")
        
        if nums[mid] == target:
            return mid
            
        # LOGICAL DEDUCTION 1: Is the LEFT half perfectly sorted?
        if nums[left] <= nums[mid]:
            print("    -> Left half is strictly sorted.")
            # Does the target mathematically exist within this sorted left half?
            if nums[left] <= target < nums[mid]:
                print("    -> Target is trapped in the left half! Annihilating right.")
                right = mid - 1
            else:
                print("    -> Target is NOT in the left half! Annihilating left.")
                left = mid + 1
                
        # LOGICAL DEDUCTION 2: If the left isn't sorted, the RIGHT half MUST be sorted!
        else:
            print("    -> Right half is strictly sorted.")
            # Does the target mathematically exist within this sorted right half?
            if nums[mid] < target <= nums[right]:
                print("    -> Target is trapped in the right half! Annihilating left.")
                left = mid + 1
            else:
                print("    -> Target is NOT in the right half! Annihilating right.")
                right = mid - 1
                
    return -1

def demonstrate_rotated_array():
    section_header("Modified Binary Search (Rotated Array)")
    
    # It is sorted, but cut and swapped!
    nums = [34, 45, 56, 67, 78, 12, 19, 23, 29]
    target = 19
    
    print(f"Rotated Array: {nums}\n")
    
    result = search_rotated_array(nums, target)
    print(f"\nResult: Target found at index {result}")


def run_all_labs():
    demonstrate_binary_search()
    demonstrate_rotated_array()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "Why must the `while` loop condition be `left <= right` instead of just `left < right`?"
   Senior Answer: "If the array contains an EVEN number of elements (e.g., 2), the final execution state will often result in the `left` pointer and `right` pointer aggressively collapsing onto the exact same index. If the `while` condition is `left < right`, the loop will abruptly terminate the millisecond they meet, entirely failing to check that final, critical index. By enforcing `left <= right`, we mathematically guarantee that the final overlapping element is processed before the pointers cross over and terminate the loop."

2. Interviewer: "In C++ and Java, writing `mid = (left + right) / 2` causes a catastrophic bug. What is the bug, why does it happen, and why doesn't it happen in Python?"
   Senior Answer: "In Java/C++, Integers are strictly locked into 32-bit hardware memory registers. The maximum positive value of a 32-bit Signed Integer is ~2.14 Billion. If `left` is 1.5 Billion and `right` is 2.0 Billion, calculating `(left + right)` results in 3.5 Billion, which instantly overflows the 32-bit register, wrapping around into a horrific Negative number! Dividing a Negative number by 2 produces a Negative Array Index, violently crashing the program with an `IndexOutOfBoundsException`. To fix this, you must write `left + (right - left) / 2`, which mathematically prevents the sum from ever exceeding `right`. Python completely avoids this because Python 3 integers possess arbitrary precision; they are not bound by 32-bit registers and dynamically expand in RAM until the server runs out of physical memory."

3. Interviewer: "How does the 'Search in Rotated Sorted Array' algorithm maintain $O(\\log N)$ time complexity when the array is no longer strictly sorted from start to finish?"
   Senior Answer: "The mathematical brilliance of a Rotated Sorted Array is that if you cut it in half, at least ONE of the two halves is mathematically guaranteed to be strictly, perfectly sorted. The algorithm leverages this by performing a $O(1)$ check at each step: `if nums[left] <= nums[mid]`. Once it definitively proves which half is strictly sorted, it can safely check if the target falls within that perfect boundary. If it does, we annihilate the unsorted half. If it doesn't, we annihilate the sorted half. By continually cutting the search space in half at every step, we preserve the exact $O(\\log N)$ properties of Binary Search."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Interview Prep (Binary Search) Completed.")
