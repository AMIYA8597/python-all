"""
# ==============================================================================
# LABORATORY: BINARY SEARCH ON ANSWERS (PARAMETRIC SEARCH)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You already know how to use Binary Search to find a number in a sorted array.
# But what if there IS NO ARRAY?
#
# "Binary Search on Answers" (also called Parametric Search) is an advanced 
# algorithmic technique used to solve Optimization problems. 
# If a problem asks you to find the "minimum capacity", "minimum speed", or 
# "maximum distance", and the answers follow a monotonic pattern (e.g., 
# False, False, False, True, True, True), you can Binary Search the entire 
# spectrum of possible answers!
#
# Classic examples:
# - Koko Eating Bananas (LeetCode 875)
# - Capacity to Ship Packages Within D Days (LeetCode 1011)
# - Split Array Largest Sum (LeetCode 410)
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand Monotonicity (The True/False threshold).
# - Design a `is_possible()` validation function.
# - Execute Binary Search over an invisible integer space.
# - Execute Binary Search over floating-point numbers.
#
# ==============================================================================
"""

import math
from typing import List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. BINARY SEARCH ON ANSWERS (KOKO EATING BANANAS)
# ==============================================================================
def min_eating_speed(piles: List[int], h: int) -> int:
    """
    Problem: Koko loves to eat bananas. There are N piles.
    Koko can decide her bananas-per-hour eating speed `k`.
    If she eats `k` bananas in an hour, and a pile has less than `k` bananas, 
    she finishes the pile but DOES NOT move to the next pile until the hour is over.
    Find the MINIMUM speed `k` so that she eats all bananas within `h` hours.
    """
    
    # 1. Define the Helper / Validation Function
    # This must run in O(N) time and return True or False.
    def is_possible_speed(k: int) -> bool:
        hours_needed = 0
        for pile in piles:
            # math.ceil(pile / k) gives the hours to finish this specific pile
            hours_needed += math.ceil(pile / k)
        return hours_needed <= h

    # 2. Define the Search Space (The lowest and highest possible answers)
    # The absolute slowest speed is 1 banana per hour.
    left = 1
    # The absolute fastest she ever needs to eat is the largest pile in 1 hour.
    # Eating faster than the largest pile does nothing because she waits for the hour to end anyway.
    right = max(piles)
    
    # The answer we want to return (the minimum valid speed)
    best_speed = right
    
    # 3. Binary Search the Answer Space
    # If piles = [3, 6, 7, 11] and H = 8.
    # Speeds 1, 2, 3 might return False (Too Slow).
    # Speeds 4, 5, 6... will return True (Fast enough).
    # We want the FIRST True! (Lower Bound).
    
    while left <= right:
        mid = left + (right - left) // 2
        
        if is_possible_speed(mid):
            # Mid is a VALID speed! 
            # Record it as the best so far, but try to find a SLOWER one.
            best_speed = mid
            right = mid - 1
        else:
            # Mid is INVALID (too slow).
            # We MUST eat faster.
            left = mid + 1
            
    return best_speed

def demonstrate_koko():
    section_header("Algorithm: Binary Search on Answers")
    piles = [3, 6, 7, 11]
    h = 8
    
    print(f"Piles of bananas: {piles}")
    print(f"Hours available: {h}")
    
    print("\nThe search space for speed is [1, 11].")
    print("Will test speeds using Binary Search...")
    
    optimal_speed = min_eating_speed(piles, h)
    
    print(f"\nOptimal Minimum Speed: {optimal_speed} bananas/hour")
    
    print(f"\nVerification for speed {optimal_speed}:")
    total_hours = sum(math.ceil(p / optimal_speed) for p in piles)
    print(f"Pile 3  -> {math.ceil(3/optimal_speed)} hours")
    print(f"Pile 6  -> {math.ceil(6/optimal_speed)} hours")
    print(f"Pile 7  -> {math.ceil(7/optimal_speed)} hours")
    print(f"Pile 11 -> {math.ceil(11/optimal_speed)} hours")
    print(f"Total   -> {total_hours} hours. (<= {h} is {total_hours <= h})")


# ==============================================================================
# 4. FLOATING POINT BINARY SEARCH
# ==============================================================================
def maximum_average_subarray(arr: List[int], k: int) -> float:
    """
    Demonstrates Binary Search on Floating Point numbers.
    Find a contiguous subarray whose length is >= k that has the MAXIMUM average.
    """
    
    def is_average_possible(target_avg: float) -> bool:
        # We want to find if there is a subarray with length >= k where:
        # sum(arr[i:j]) / (j-i) >= target_avg
        # Algebra trick: sum(arr[i:j]) >= target_avg * (j-i)
        # sum(arr[i:j] - target_avg) >= 0
        
        # Array of differences
        diff = [x - target_avg for x in arr]
        
        # We use a Prefix Sum to find if any subarray of length >= k has sum >= 0
        curr_sum = sum(diff[:k])
        if curr_sum >= 0:
            return True
            
        prev_sum = 0
        min_prev_sum = 0
        
        for i in range(k, len(arr)):
            curr_sum += diff[i]
            prev_sum += diff[i - k]
            min_prev_sum = min(min_prev_sum, prev_sum)
            
            # If current prefix sum minus the smallest previous prefix sum is >= 0,
            # then a valid subarray exists!
            if curr_sum - min_prev_sum >= 0:
                return True
                
        return False

    # Search Space for the average
    left = min(arr)
    right = max(arr)
    
    # For floating points, we don't use `left <= right` because float math has 
    # precision errors and it might loop infinitely.
    # Instead, we stop when the search space is infinitesimally small (1e-5),
    # or we just loop a fixed number of times (e.g., 60 times covers 10^18 precision).
    
    for _ in range(60):
        mid = (left + right) / 2.0
        
        if is_average_possible(mid):
            # This average IS possible. Try to find a HIGHER one.
            left = mid
        else:
            # This average is IMPOSSIBLE. Try to find a LOWER one.
            right = mid
            
    return left

def demonstrate_float_bs():
    section_header("Algorithm: Floating Point Binary Search")
    
    arr = [1, 12, -5, -6, 50, 3]
    k = 4
    
    print(f"Array: {arr}")
    print(f"Minimum length (K): {k}")
    
    max_avg = maximum_average_subarray(arr, k)
    print(f"\nMaximum possible average: {max_avg:.5f}")


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. When can you use Binary Search on Answers?
   Answer: You can use it whenever the problem asks for a Minimum or Maximum constraint, AND the validity of the answers forms a "Monotonic" sequence. For example, if checking speeds, speed 1 is False (too slow), 2 is False, 3 is True (fast enough). Because it shifts from False to True exactly once, you can Binary Search the threshold.

2. Why is Binary Search on Answers so fast?
   Answer: Because testing an answer (`is_possible`) usually takes O(N) time. The search space for the answer (e.g., 1 to 1 Billion) is completely separate from N. Binary searching 1 Billion takes exactly 30 steps. So the overall time is `O(N * 30)` which is effectively just `O(N)`.

3. Why do we loop exactly 60 times for Floating Point Binary Search?
   Answer: Floating point math introduces precision errors (e.g. `0.1 + 0.2 = 0.3000000004`). If you write `while right - left > 1e-5`, it can sometimes get caught in an infinite loop due to rounding errors. Since halving a range 60 times divides the search space by `2^60` (over a quintillion), it mathematically guarantees extreme precision without the risk of an infinite loop.
"""

if __name__ == "__main__":
    demonstrate_koko()
    demonstrate_float_bs()
    print("\n[SUCCESS] Laboratory: Binary Search on Answers Completed.")
