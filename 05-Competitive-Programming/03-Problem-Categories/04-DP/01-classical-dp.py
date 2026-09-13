"""
# ==============================================================================
# LABORATORY: COMPETITIVE PROGRAMMING (CLASSICAL DYNAMIC PROGRAMMING)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You are a thief robbing a museum. You have a backpack that holds 50kg.
# There are 100 items, each with a specific weight and a specific dollar value.
# You want to maximize your profit.
#
# A "Greedy" algorithm (taking the items with the best value-to-weight ratio) 
# is mathematically proven to FAIL this problem. It might leave 5kg of empty 
# space that could have been perfectly filled by a different combination of items.
#
# To find the absolute mathematical maximum, you must explore all combinations.
# But 100 items means $2^{100}$ combinations. Your computer will freeze until 
# the heat death of the universe.
#
# You must use Dynamic Programming (DP). DP is the art of breaking a massive 
# problem into tiny sub-problems, solving them once, caching the result, and 
# reusing it to drastically reduce exponential $O(2^N)$ time into polynomial 
# $O(N \times W)$ time!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master the 0/1 Knapsack Problem (The foundational 2D DP).
# - Master Longest Common Subsequence (LCS).
# - Master Longest Increasing Subsequence (LIS in O(N log N)).
#
# ==============================================================================
"""

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE 0/1 KNAPSACK PROBLEM
# ==============================================================================
def knapsack_01(capacity: int, weights: list[int], values: list[int]) -> int:
    """
    Solves the 0/1 Knapsack problem using Bottom-Up 1D Dynamic Programming.
    Time Complexity: O(N * Capacity), Space Complexity: O(Capacity)
    """
    n = len(weights)
    
    # dp[w] will store the maximum value we can achieve using a backpack of capacity w.
    dp = [0] * (capacity + 1)
    
    # Iterate through every item one by one
    for i in range(n):
        w = weights[i]
        v = values[i]
        
        # We must iterate BACKWARDS through the capacities!
        # Why? Because if we iterate forwards, we might use the SAME item multiple 
        # times in a single loop (which solves the "Unbounded Knapsack" problem, 
        # not the "0/1" Knapsack problem where we only have 1 of each item).
        for current_capacity in range(capacity, w - 1, -1):
            
            # The State Transition Equation:
            # We either DO NOT take the item (keep the current max value),
            # OR we DO take the item (value of this item + max value of the leftover space)
            dp[current_capacity] = max(
                dp[current_capacity],
                v + dp[current_capacity - w]
            )
            
    return dp[capacity]

def demonstrate_knapsack():
    section_header("0/1 Knapsack Problem")
    
    weights = [10, 20, 30]
    values = [60, 100, 120]
    capacity = 50
    
    print(f"Item Weights: {weights}")
    print(f"Item Values : {values}")
    print(f"Backpack Cap: {capacity}kg")
    
    max_profit = knapsack_01(capacity, weights, values)
    print(f"\nAbsolute Maximum Profit: ${max_profit}")
    print("Expected: $220 (taking item 2 and 3: 20kg + 30kg = 50kg, $100 + $120 = $220)")


# ==============================================================================
# 4. LONGEST COMMON SUBSEQUENCE (LCS)
# ==============================================================================
def longest_common_subsequence(text1: str, text2: str) -> int:
    """
    Finds the length of the Longest Common Subsequence between two strings.
    Used in git diff, bioinformatics (DNA alignment).
    Time Complexity: O(N * M), Space Complexity: O(N * M)
    """
    n, m = len(text1), len(text2)
    
    # dp[i][j] stores the LCS of text1[0:i] and text2[0:j]
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            
            # If the characters match, the sequence grows by 1!
            if text1[i - 1] == text2[j - 1]:
                dp[i][j] = 1 + dp[i - 1][j - 1]
                
            # If they don't match, the longest sequence is the best we could do 
            # by either ignoring the current character of text1, or ignoring text2.
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
                
    return dp[n][m]

def demonstrate_lcs():
    section_header("Longest Common Subsequence (LCS)")
    
    s1 = "abcde"
    s2 = "ace"
    
    print(f"String 1: {s1}")
    print(f"String 2: {s2}")
    
    lcs_length = longest_common_subsequence(s1, s2)
    print(f"\nLongest Common Subsequence Length: {lcs_length}")
    print("The subsequence is 'ace'.")


# ==============================================================================
# 5. LONGEST INCREASING SUBSEQUENCE (LIS in O(N log N))
# ==============================================================================
import bisect

def longest_increasing_subsequence(nums: list[int]) -> int:
    """
    Finds the length of the longest strictly increasing subsequence.
    Time Complexity: O(N log N) using Binary Search (Patience Sorting).
    Space Complexity: O(N)
    """
    # `sub` will store the smallest tail of all increasing subsequences of length i+1.
    # It is NOT the actual longest subsequence itself, but its length will be correct!
    sub = []
    
    for num in nums:
        # Find the index where `num` should be inserted in `sub` to maintain sorted order
        # using O(log N) Binary Search.
        i = bisect.bisect_left(sub, num)
        
        # If `num` is larger than any element in `sub`, it extends the longest sequence!
        if i == len(sub):
            sub.append(num)
        # Otherwise, `num` overwrites an existing number. This doesn't increase the 
        # length of the sequence, but it lowers the "tail" value, making it 
        # mathematically easier to extend the sequence with future numbers!
        else:
            sub[i] = num
            
    return len(sub)

def demonstrate_lis():
    section_header("Longest Increasing Subsequence (O(N log N))")
    
    nums = [10, 9, 2, 5, 3, 7, 101, 18]
    print(f"Array: {nums}")
    
    lis_length = longest_increasing_subsequence(nums)
    print(f"\nLength of LIS: {lis_length}")
    print("The subsequence is [2, 3, 7, 101] (or [2, 3, 7, 18]).")


def run_all_labs():
    demonstrate_knapsack()
    demonstrate_lcs()
    demonstrate_lis()


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. In the 1D space-optimized version of the 0/1 Knapsack DP, why is it absolutely mandatory to iterate backwards (`for current_capacity in range(capacity, w - 1, -1)`)?
   Answer: In a 0/1 Knapsack, you are only allowed to use each physical item exactly *once*. The state equation `dp[c] = max(dp[c], v + dp[c - w])` relies on looking at the DP array from the *previous* state (`c - w`). If you iterate forwards from 0 to capacity, you update `dp[5]`. When the loop reaches `dp[10]`, it looks back at `dp[5]`. But `dp[5]` was *already* updated during this exact same item's loop! You just mathematically used the same item twice (once at capacity 5, once at capacity 10). This solves the "Unbounded/Infinite Knapsack". By iterating backwards from 50 down to 0, when `dp[10]` looks back at `dp[5]`, it is mathematically guaranteed that `dp[5]` has not been touched yet during this iteration, safely preserving the 0/1 rule.

2. Explain the intuition behind the State Transition Equation for Longest Common Subsequence (LCS): `dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])` when characters do NOT match.
   Answer: If we are comparing "ABCD" and "ABCE", the last characters ('D' and 'E') do not match. Since they don't match, they cannot possibly both be part of the final Longest Common Subsequence. The mathematical optimal answer MUST exist in one of two slightly smaller universes: either the universe where we completely ignore the 'D' (comparing "ABC" to "ABCE", which is `dp[i - 1][j]`), OR the universe where we completely ignore the 'E' (comparing "ABCD" to "ABC", which is `dp[i][j - 1]`). By taking the `max()` of these two parallel universes, we safely carry the longest known sequence forward.

3. In the $O(N \log N)$ LIS algorithm (Patience Sorting), does the array `sub` store the actual, physically correct subsequence?
   Answer: No! The `sub` array tracks the *smallest possible tail ending* for a subsequence of length $K$. For example, if the input is `[3, 4, 5, 1]`, `sub` will initially build `[3, 4, 5]`. When the `1` arrives, `bisect_left` replaces the `3` with the `1`, resulting in `sub = [1, 4, 5]`. Physically, the sequence `[1, 4, 5]` never occurred in the original array (1 came *after* 4 and 5). However, the *length* of `sub` (which is 3) remains mathematically correct! The overwrite ensures that if future small numbers arrive (like 2, 3), we have a tiny base (`1`) to build upon. We sacrifice the physical sequence history to optimize purely for tracking the maximum possible *length*.
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Classical Dynamic Programming Completed.")
