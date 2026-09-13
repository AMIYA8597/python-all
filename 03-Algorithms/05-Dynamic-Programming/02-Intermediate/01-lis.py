"""
# ==============================================================================
# LABORATORY: LONGEST INCREASING SUBSEQUENCE (LIS)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You are given an array of integers: [10, 9, 2, 5, 3, 7, 101, 18]
# You must find the length of the strictly increasing subsequence.
# (The answer is 4: [2, 3, 7, 101] or [2, 5, 7, 18]).
#
# The LIS problem is a monumental stepping stone in Computer Science because 
# there are two completely different ways to solve it:
#
# 1. Standard DP (O(N^2) Time): A beautiful double-loop where every element 
#    looks backwards at every previous element to see if it can "extend" their 
#    sequence.
#
# 2. Binary Search + DP (O(N log N) Time): A genius algorithm (often called 
#    "Patience Sorting") that builds a theoretical array of the "smallest 
#    possible tail elements" and uses Binary Search to overwrite them. This 
#    shatters the O(N^2) barrier and is heavily tested in FAANG interviews.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Implement O(N^2) nested DP arrays.
# - Understand the "Look Back" state transition.
# - Implement the O(N log N) Binary Search optimization (Patience Sorting).
#
# ==============================================================================
"""

import bisect
from typing import List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. STANDARD DP (O(N^2))
# ==============================================================================
def length_of_lis_dp(nums: List[int]) -> int:
    """
    Time Complexity: O(N^2)
    Space Complexity: O(N)
    """
    if not nums:
        return 0
        
    n = len(nums)
    
    # 1. STATE DEFINITION
    # `dp[i]` represents the length of the LIS that STRICTLY ENDS at index `i`.
    # Notice the phrasing! It MUST end at `i`.
    
    # 2. INITIALIZATION
    # Every single element is mathematically an Increasing Subsequence of length 1 
    # (just itself!). So we initialize the array with 1s.
    dp = [1] * n
    
    # 3. TABULATION LOOP
    for i in range(1, n):
        # We are at `nums[i]`. We must look BACKWARDS at every single element `j` 
        # that came before it.
        for j in range(i):
            
            # --- STATE TRANSITION EQUATION ---
            # Is the current number strictly greater than the previous number?
            # If so, we can mathematically "append" `nums[i]` to the subsequence 
            # that ended at `nums[j]`!
            if nums[i] > nums[j]:
                # The length becomes whatever length `j` had, PLUS ONE (for `i`).
                # We want the absolute MAX of all possible previous subsequences.
                dp[i] = max(dp[i], dp[j] + 1)
                
    # The final answer is NOT necessarily dp[N-1]!
    # The longest subsequence could have ended anywhere in the middle of the array!
    # So we must return the absolute maximum value found anywhere in the DP array.
    return max(dp)


# ==============================================================================
# 4. BINARY SEARCH + DP (O(N log N))
# ==============================================================================
def length_of_lis_binary_search(nums: List[int]) -> int:
    """
    Time Complexity: O(N log N)
    Space Complexity: O(N)
    
    This is known as the "Patience Sorting" trick.
    """
    # `tails` is an array storing the smallest tail of all increasing subsequences 
    # of length i+1 in tails[i].
    # Wait, what?
    # If we have sequences [2, 5] and [2, 3], they are both length 2.
    # But [2, 3] is VASTLY superior, because `3` is smaller, making it much 
    # easier to append a 4 or a 5 later! 
    # So `tails` only keeps the SMALLEST possible ending numbers.
    tails = []
    
    for num in nums:
        # 1. Use Binary Search to find the first element in `tails` that is 
        # greater than or equal to `num`.
        # `bisect_left` runs in O(log N) time!
        idx = bisect.bisect_left(tails, num)
        
        # 2. If `idx` is equal to the length of `tails`, it means `num` is 
        # strictly greater than EVERY tail currently stored!
        # We have found a new, longer subsequence! Append it.
        if idx == len(tails):
            tails.append(num)
            
        # 3. Else, `num` is smaller than an existing tail.
        # We OVERWRITE the larger tail with `num`. 
        # Why? Because we want to keep the tails as small as possible to make 
        # future insertions easier!
        else:
            tails[idx] = num
            
    # The length of the `tails` array is the length of the LIS!
    # (Note: The actual elements inside `tails` are NOT the valid subsequence, 
    # just the mathematical placeholder bounds).
    return len(tails)


def demonstrate_lis():
    section_header("Algorithm: Longest Increasing Subsequence")
    
    nums = [10, 9, 2, 5, 3, 7, 101, 18]
    print(f"Input Array: {nums}\n")
    
    print("Executing O(N^2) Dynamic Programming...")
    ans_dp = length_of_lis_dp(nums)
    print(f"Result: {ans_dp} (Expected: 4 -> [2, 3, 7, 101])\n")
    
    print("Executing O(N log N) Binary Search DP...")
    ans_bs = length_of_lis_binary_search(nums)
    print(f"Result: {ans_bs} (Expected: 4)")


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. In the $O(N^2)$ solution, why do we return `max(dp)` instead of `dp[-1]`?
   Answer: Because `dp[i]` is strictly defined as "The longest subsequence ENDING AT index i". If the input array is `[2, 3, 4, 1]`, the longest subsequence is `[2, 3, 4]` (length 3), which ends at index 2. The value at the final index `dp[3]` is for the subsequence `[1]`, which is just length 1! You must scan the entire DP array to find the global maximum.

2. Does the `tails` array in the Binary Search solution contain the actual Longest Subsequence?
   Answer: NO. This is a massive trap in FAANG interviews. If the input is `[4, 5, 6, 3]`, the `tails` array will build `[4, 5, 6]`. Then it processes `3`. Binary Search will overwrite `4` with `3`. The `tails` array becomes `[3, 5, 6]`. The length is correct (3), but `[3, 5, 6]` is not a valid subsequence from the original array! The `tails` array only mathematically stores the optimal lower bounds, not the physical subsequence.

3. Why is Patience Sorting $O(N \\log N)$?
   Answer: Because we iterate through the `nums` array exactly once with a `for` loop ($O(N)$). Inside that loop, instead of doing another linear search backwards, we use Python's `bisect_left()` to perform a Binary Search on the `tails` array, which takes $O(\\log N)$. $N \\times \\log N = N \\log N$.
"""

if __name__ == "__main__":
    demonstrate_lis()
    print("\n[SUCCESS] Laboratory: LIS Completed.")
