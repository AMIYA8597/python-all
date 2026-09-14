"""
# ==============================================================================
# LABORATORY: INTERVIEW PREPARATION (PROBLEM SETS - ALGORITHM EASY)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# "Easy" Algorithm problems introduce the two most critical paradigms in Computer 
# Science: Logarithmic Search (Binary Search) and Overlapping Subproblems (Dynamic 
# Programming).
#
# A junior engineer searches for a specific version in a massive codebase by 
# checking every single version sequentially (O(N) Time). If there are 100 
# Million versions, it takes days.
#
# A senior engineer uses Binary Search. By constantly halving the search space, 
# they mathematically guarantee finding the target out of 100 Million versions 
# in exactly 27 operations (O(log N) Time), executing in microseconds.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master Logarithmic Division (Binary Search, First Bad Version).
# - Master Fibonacci-style Overlapping Subproblems (Climbing Stairs).
# - Understand the O(N) Space to O(1) Space DP optimization.
#
# ==============================================================================
"""

from typing import List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. BINARY SEARCH (THE O(LOG N) MASTERCLASS)
# ==============================================================================
def search(nums: List[int], target: int) -> int:
    """
    Time: O(log N) | Space: O(1)
    Given an array of integers `nums` which is sorted in ascending order, and an 
    integer `target`, write a function to search `target` in `nums`.
    """
    left = 0
    right = len(nums) - 1
    
    print(f"  Executing Binary Search for target: {target}")
    
    # We must use <= (not <) because if left == right, that single remaining 
    # element might actually be our target!
    while left <= right:
        # THE INTEGER OVERFLOW AVOIDANCE TRICK:
        # Instead of `(left + right) // 2`, which can crash languages like C++ or 
        # Java if left + right exceeds 2^31, we mathematically calculate the offset!
        mid = left + (right - left) // 2
        
        print(f"    -> Checking bounds [{left}, {right}]. Midpoint is index {mid} (Value: {nums[mid]})")
        
        if nums[mid] == target:
            print("      [SUCCESS] Target found instantly!")
            return mid
            
        elif nums[mid] < target:
            # The midpoint is TOO SMALL! The target MUST be in the right half!
            # We annihilate the entire left half of the array!
            left = mid + 1
            print("      -> Target is larger. Annihilating left half.")
            
        else:
            # The midpoint is TOO BIG! The target MUST be in the left half!
            # We annihilate the entire right half of the array!
            right = mid - 1
            print("      -> Target is smaller. Annihilating right half.")
            
    print("  [FAIL] Target does not exist in the array.")
    return -1

def demonstrate_binary_search():
    section_header("Easy: Binary Search (Logarithmic Division)")
    
    nums = [-1, 0, 3, 5, 9, 12]
    target = 9
    ans = search(nums, target)
    print(f"\nResult: Index {ans} (Expected: 4)")


# ==============================================================================
# 4. CLIMBING STAIRS (DYNAMIC PROGRAMMING INTRODUCTION)
# ==============================================================================
def climb_stairs(n: int) -> int:
    """
    Time: O(N) | Space: O(1)
    You are climbing a staircase. It takes n steps to reach the top.
    Each time you can either climb 1 or 2 steps. In how many distinct ways can 
    you climb to the top?
    
    A junior engineer uses pure Recursion: `f(n) = f(n-1) + f(n-2)`. 
    Time Complexity: O(2^N). For n=45, this calculates 3.5 Billion branches and times out.
    
    A senior engineer recognizes the Fibonacci sequence! We don't need a massive DP 
    array of size N. We only ever mathematically need the TWO previous results!
    """
    if n <= 2: return n
    
    # We only store the absolute previous two steps!
    two_steps_back = 1
    one_step_back = 2
    
    print(f"  Calculating combinations for {n} stairs...")
    
    for i in range(3, n + 1):
        # The number of ways to reach step `i` is the sum of ways to reach 
        # the two steps directly preceding it!
        current = one_step_back + two_steps_back
        print(f"    -> Step {i}: {one_step_back} + {two_steps_back} = {current} combinations.")
        
        # Shift the variables forward for the next iteration!
        two_steps_back = one_step_back
        one_step_back = current
        
    return one_step_back

def demonstrate_climbing_stairs():
    section_header("Easy: Climbing Stairs (O(1) Space DP)")
    
    n = 6
    ans = climb_stairs(n)
    print(f"\nResult: {ans} distinct ways.")


# ==============================================================================
# 5. FIRST BAD VERSION (API ABSTRACTION)
# ==============================================================================
# Mock API for demonstration
BAD_VERSION_TARGET = 4
def isBadVersion(version: int) -> bool:
    return version >= BAD_VERSION_TARGET

def first_bad_version(n: int) -> int:
    """
    Time: O(log N) | Space: O(1)
    Suppose you have n versions [1, 2, ..., n] and you want to find out the 
    first bad one. You are given an API `isBadVersion(version)`.
    """
    left = 1
    right = n
    
    print(f"  Scanning {n} versions using Binary Search...")
    
    # Notice we don't have a `return mid` inside the loop!
    # Because we don't want JUST a bad version, we want the FIRST bad version!
    while left < right:
        mid = left + (right - left) // 2
        
        if isBadVersion(mid):
            # This is a bad version! 
            # However, we CANNOT do `right = mid - 1` because `mid` itself 
            # might literally be the FIRST bad version! We must keep it in the pool!
            right = mid
            print(f"    -> Version {mid} is BAD. It might be the first, or there might be an earlier one. Shrinking right boundary.")
        else:
            # This is a good version!
            # It is mathematically impossible for this to be the first bad version.
            # We can aggressively skip past it!
            left = mid + 1
            print(f"    -> Version {mid} is GOOD. All earlier versions are good. Advancing left boundary to {mid + 1}.")
            
    # When left == right, the loop terminates. The single surviving element is 
    # mathematically guaranteed to be the FIRST bad version.
    return left

def demonstrate_first_bad():
    section_header("Easy: First Bad Version (Boundary Retention)")
    
    n = 10
    ans = first_bad_version(n)
    print(f"\nResult: Version {ans} is the FIRST bad version. (Expected: 4)")


def run_all_labs():
    demonstrate_binary_search()
    demonstrate_climbing_stairs()
    demonstrate_first_bad()


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "In Binary Search, why must the array be strictly sorted before the algorithm can function?"
   Senior Answer: "Binary Search operates on the mathematical principle of Logical Elimination. If we check the midpoint and it is smaller than our target, we aggressively annihilate the entire left half of the array. The *only* reason we can safely do this is because the array is sorted, providing an absolute mathematical guarantee that every single number to the left of the midpoint is also smaller than the target. If the array was unsorted, a massive number could be hiding on the left side, and our elimination logic would bypass the target, returning a fatal False Negative."

2. Interviewer: "In the Climbing Stairs DP solution, why does solving `n=45` using pure Recursion take minutes, but the $O(1)$ Space DP loop takes microseconds?"
   Senior Answer: "Pure Recursion triggers overlapping subproblems. To calculate `f(5)`, it calculates `f(4)` and `f(3)`. But to calculate `f(4)`, it *re-calculates* `f(3)` entirely from scratch! The execution tree bifurcates exponentially, leading to an $O(2^N)$ time complexity. For `n=45`, this forces the CPU to execute over 3.5 Billion redundant function calls. The Dynamic Programming loop works Bottom-Up. It calculates `f(3)` exactly once, stores it in a variable, and reuses it for `f(4)` and `f(5)`. By permanently caching the previous states, the algorithm collapses into a strict linear $O(N)$ execution path, requiring exactly 45 iterations instead of 3.5 Billion."

3. Interviewer: "In 'First Bad Version', why is the while loop condition `left < right` instead of `left <= right`, and why do we set `right = mid` instead of `right = mid - 1`?"
   Senior Answer: "This is a specialized variation of Binary Search designed to find the absolute *Boundary* of a condition, rather than a specific match. If `isBadVersion(mid)` is True, we know `mid` is defective. However, we do not know if `mid - 1` is also defective. If we set `right = mid - 1`, and `mid` actually *was* the First Bad Version, we just mathematically deleted the correct answer from our search space! We must set `right = mid` to keep it alive. Because we are keeping `mid` alive, we MUST use `left < right` for the loop condition. If we used `left <= right`, the loop would become permanently trapped when `left == right`, causing an Infinite Loop."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Problem Sets (Algorithm Easy) Completed.")
