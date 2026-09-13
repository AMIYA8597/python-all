"""
# ==============================================================================
# LABORATORY: SUBSET SUM (0/1 BOOLEAN KNAPSACK)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You are given an array of integers `[3, 34, 4, 12, 5, 2]` and a target `9`.
# Is there ANY combination of these numbers that adds up exactly to 9?
# Yes: [4, 5].
#
# This is the "Subset Sum" problem. It is mathematically identical to the 
# 0/1 Knapsack problem! 
# In Knapsack, we wanted to MAXIMIZE VALUE. 
# Here, we don't care about value. We just want a Boolean (True/False) answering 
# whether the sum is physically possible to construct.
#
# This algorithm is the foundation for solving "Partition Equal Subset Sum" 
# (e.g. Can you split an array into two halves that have the exact same sum?).
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Model Boolean States in Dynamic Programming.
# - Master the OR (`|`) State Transition Equation.
# - Optimize 2D DP down to a single 1D Array (The Backwards Traversal Trick).
#
# ==============================================================================
"""

from typing import List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. 2D TABULATION (O(N * SUM))
# ==============================================================================
def subset_sum_2d(nums: List[int], target: int) -> bool:
    n = len(nums)
    
    # 1. STATE DEFINITION
    # dp[i][j] is True if there is a subset of the first `i` elements that sums to `j`.
    dp = [[False for _ in range(target + 1)] for _ in range(n + 1)]
    
    # 2. BASE CASES
    # If the target sum is 0, the answer is ALWAYS True (just pick the Empty Subset []).
    for i in range(n + 1):
        dp[i][0] = True
        
    # If we have 0 elements, no sum > 0 can be reached. (Already False by default).
    
    # 3. TABULATION LOOP
    for i in range(1, n + 1):
        curr_num = nums[i - 1]
        
        for j in range(1, target + 1):
            
            # --- STATE TRANSITION EQUATION ---
            # Option 1: EXCLUDE the current number.
            # Can we make the sum `j` using the previous elements?
            exclude = dp[i - 1][j]
            
            # Option 2: INCLUDE the current number.
            # We can only include it if it's not bigger than our target `j`.
            include = False
            if curr_num <= j:
                # If we use it, we check if the PREVIOUS elements could make the 
                # remaining sum (`j - curr_num`).
                include = dp[i - 1][j - curr_num]
                
            # If EITHER option is True, the current state is True!
            dp[i][j] = exclude or include
            
    return dp[n][target]


# ==============================================================================
# 4. 1D SPACE OPTIMIZATION (THE BACKWARDS TRICK)
# ==============================================================================
def subset_sum_1d(nums: List[int], target: int) -> bool:
    """
    Time Complexity: O(N * Target)
    Space Complexity: O(Target) (Down from O(N * Target)!)
    """
    # 1. We squash the 2D matrix into a single 1D array of size `Target + 1`.
    dp = [False] * (target + 1)
    
    # Base Case: Sum of 0 is always True.
    dp[0] = True
    
    for num in nums:
        # 2. THE BACKWARDS LOOP
        # CRITICAL TRICK: We MUST loop backwards from `target` down to `num`.
        # Why? Because our Transition Equation `dp[j] = dp[j] or dp[j - num]` 
        # requires the value of `dp[j - num]` from the PREVIOUS row (i-1).
        # If we looped forwards, we would overwrite `dp[j - num]` with the NEW 
        # row's value before we had a chance to use it!
        for j in range(target, num - 1, -1):
            dp[j] = dp[j] or dp[j - num]
            
    return dp[target]


def demonstrate_subset_sum():
    section_header("Algorithm: Subset Sum")
    
    nums = [3, 34, 4, 12, 5, 2]
    target1 = 9
    
    print(f"Array: {nums}")
    print(f"Target Sum: {target1}")
    
    ans1_2d = subset_sum_2d(nums, target1)
    ans1_1d = subset_sum_1d(nums, target1)
    
    print(f"Result (2D DP): {ans1_2d} (Expected: True -> [4, 5])")
    print(f"Result (1D DP): {ans1_1d} (Expected: True)")
    
    target2 = 30
    print(f"\nTarget Sum: {target2}")
    print(f"Result (1D DP): {subset_sum_1d(nums, target2)} (Expected: False)")


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. What is the fundamental difference between Subset Sum and Coin Change?
   Answer: In Subset Sum (a 0/1 Knapsack variation), you can only use each number EXACTLY ONCE. In Coin Change (an Unbounded Knapsack variation), you can use each number INFINITE times.

2. How does the 1D Space Optimization code mathematically control "Use Once" vs "Use Infinite"?
   Answer: The inner loop direction! 
   - `for j in range(target, num-1, -1):` (Backwards) guarantees that `dp[j-num]` was calculated in the PREVIOUS outer loop iteration, enforcing "Use Once" (0/1 Knapsack).
   - `for j in range(num, target+1):` (Forwards) guarantees that `dp[j-num]` was calculated in the CURRENT outer loop iteration, meaning the number can mathematically add to itself repeatedly, enforcing "Use Infinite" (Coin Change).

3. How do you solve "Partition Equal Subset Sum"?
   Answer: If you have an array `[1, 5, 11, 5]`, you first sum the whole array (22). You want to split it in half, so the target for one half is $22 / 2 = 11$. You simply call `subset_sum(nums, target=11)`. If you can make 11, the remaining numbers MUST mathematically sum to 11. (Note: if the total sum is odd, it is instantly mathematically impossible).
"""

if __name__ == "__main__":
    demonstrate_subset_sum()
    print("\n[SUCCESS] Laboratory: Subset Sum Completed.")
