"""
# Classical Dynamic Programming (DP) - A Comprehensive Guide

## 1. Introduction to Dynamic Programming
Dynamic Programming (DP) is a powerful algorithmic technique for solving complex problems by breaking them down into simpler, overlapping subproblems. 
It is primarily used for optimization problems, where we want to find the "best" or "optimal" solution among many possible valid solutions.

### 1.1 Core Principles
A problem must exhibit two key attributes to be solvable using DP:
1. **Optimal Substructure**: The optimal solution to a problem incorporates the optimal solutions to its subproblems.
2. **Overlapping Subproblems**: The problem can be broken down into subproblems which are reused several times. If the subproblems do not overlap, we would use Divide and Conquer (like Merge Sort).

### 1.2 The DP Paradigms
- **Top-Down (Memoization)**: We write the procedure recursively in a natural manner, but we save the result of each subproblem in a lookup table (cache or memo). If a subproblem is encountered again, we return the saved result instead of recomputing it.
- **Bottom-Up (Tabulation)**: We avoid recursion entirely. We build a table iteratively, starting from the smallest subproblems up to the larger problem. We compute the solution to a problem only after we have computed the solutions to all its subproblems.

### 1.3 Mathematical Background & State Representation
The core of any DP solution is defining the **state** and the **recurrence relation** (state transition).
- **State**: A set of parameters that uniquely identify a particular position or subproblem in the given context.
- **Recurrence Relation**: A mathematical formula that relates the solution of a larger problem to the solutions of its smaller subproblems.

## 2. Real-World Applications
Dynamic Programming forms the backbone of several critical modern technologies:
- **Bioinformatics**: DNA sequence alignment (Needleman-Wunsch, Smith-Waterman algorithms).
- **Natural Language Processing (NLP)**: Speech recognition, spell checking (Edit Distance / Levenshtein Distance).
- **Operations Research**: Resource allocation, inventory control, and scheduling (Knapsack Problem variations).
- **Networking**: Routing algorithms (Bellman-Ford, Floyd-Warshall).
- **Finance**: Portfolio optimization, option pricing models.

## 3. Scope of this Lesson
In this lesson, we will implement and mathematically analyze five classical DP problems:
1. Longest Common Subsequence (LCS)
2. 0/1 Knapsack Problem
3. Longest Increasing Subsequence (LIS)
4. Coin Change Problem
5. Edit Distance (Levenshtein Distance)
"""

import bisect
from typing import List, Tuple
from functools import lru_cache

# =============================================================================
# 1. Longest Common Subsequence (LCS)
# =============================================================================
#
# Concept: Given two strings, find the length of the longest subsequence present
# in both of them. A subsequence is a sequence that appears in the same relative
# order, but not necessarily contiguous.
#
# Mathematical Background (Recurrence Relation):
# Let L[i, j] be the length of LCS of X[0..i-1] and Y[0..j-1].
# - Base Case: L[i, j] = 0 if i = 0 or j = 0
# - Transition: 
#   If X[i-1] == Y[j-1]: L[i, j] = 1 + L[i-1, j-1]
#   If X[i-1] != Y[j-1]: L[i, j] = max(L[i-1, j], L[i, j-1])
#
# Real-World App: git diff, bioinformatics (DNA sequencing).
# =============================================================================

def longest_common_subsequence(text1: str, text2: str) -> int:
    """
    Bottom-Up Tabulation implementation for Longest Common Subsequence.
    
    Time Complexity: O(M * N) - We process every cell in the M x N matrix exactly once.
    Space Complexity: O(M * N) - The DP table requires M * N space. 
                      (Note: Space can be optimized to O(min(M, N)) if path reconstruction is not needed).
                      
    Args:
        text1: First input string.
        text2: Second input string.
        
    Returns:
        The length of the longest common subsequence.
    """
    m, n = len(text1), len(text2)
    # Initialize an (m+1) x (n+1) matrix with zeros.
    # dp[i][j] represents the LCS of text1[0:i] and text2[0:j].
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            # If characters match, add 1 to the result of the sequences without these characters.
            if text1[i - 1] == text2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                # If they don't match, take the maximum from either excluding the current character
                # of text1 or excluding the current character of text2.
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
                
    return dp[m][n]

def longest_common_subsequence_with_path(text1: str, text2: str) -> Tuple[int, str]:
    """
    Extension of LCS that also reconstructs the actual subsequence string.
    
    Time Complexity: O(M * N) for table building + O(M + N) for backtracking. Total O(M * N).
    Space Complexity: O(M * N) for the full DP table necessary for backtracking.
    """
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # Build DP table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
                
    # Backtrack to find the sequence
    i, j = m, n
    lcs_chars = []
    
    while i > 0 and j > 0:
        if text1[i - 1] == text2[j - 1]:
            # Character is part of LCS
            lcs_chars.append(text1[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] > dp[i][j - 1]:
            # Came from top cell
            i -= 1
        else:
            # Came from left cell
            j -= 1
            
    # The sequence was built backwards, reverse it
    return dp[m][n], "".join(reversed(lcs_chars))


# =============================================================================
# 2. 0/1 Knapsack Problem
# =============================================================================
#
# Concept: Given weights and values of n items, and a knapsack capacity W, 
# find the maximum value subset of items such that their total weight is <= W.
# You cannot break an item, either pick it or not (hence 0/1).
#
# Mathematical Background (Recurrence Relation):
# Let DP[i][w] be the max value for first i items with capacity w.
# - Base Case: DP[0][w] = 0 for all w.
# - Transition:
#   If weight[i-1] <= w: 
#       DP[i][w] = max(DP[i-1][w], val[i-1] + DP[i-1][w - weight[i-1]])
#   If weight[i-1] > w:
#       DP[i][w] = DP[i-1][w]
#
# Space Optimization: We only need the previous row `i-1` to compute row `i`.
# Therefore, we can reduce space to O(W) by updating a 1D array in reverse.
#
# Real-World App: Financial portfolio selection, cargo loading, memory allocation.
# =============================================================================

def knapsack_01(weights: List[int], values: List[int], capacity: int) -> int:
    """
    Space-optimized Bottom-Up DP for 0/1 Knapsack.
    
    Time Complexity: O(N * W) where N is number of items and W is capacity.
    Space Complexity: O(W) because we only use a 1D array of size W + 1.
    """
    n = len(weights)
    if n == 0 or capacity == 0:
        return 0
        
    # dp[w] stores the maximum value achievable with a knapsack capacity of w
    dp = [0] * (capacity + 1)
    
    # Iterate through all items
    for i in range(n):
        current_weight = weights[i]
        current_value = values[i]
        
        # Traverse backwards from capacity down to current_weight.
        # Why backwards? In 0/1 Knapsack, an item can be picked at most once.
        # If we went forwards, we might use the newly updated value (which already
        # includes the current item) to update higher capacities, effectively using
        # the item multiple times (which is Unbounded Knapsack, not 0/1).
        for w in range(capacity, current_weight - 1, -1):
            dp[w] = max(dp[w], dp[w - current_weight] + current_value)
            
    return dp[capacity]


# =============================================================================
# 3. Longest Increasing Subsequence (LIS)
# =============================================================================
#
# Concept: Find the length of the longest subsequence of a given sequence such 
# that all elements of the subsequence are sorted in strictly increasing order.
#
# Mathematical Background (Recurrence Relation for O(N^2) DP):
# Let DP[i] be the length of LIS ending at index i.
# - Base Case: DP[i] = 1 for all i.
# - Transition: 
#   For j from 0 to i-1:
#       If arr[j] < arr[i]: DP[i] = max(DP[i], DP[j] + 1)
#
# Professional Optimization: Patience Sorting with Binary Search achieves O(N log N).
#
# Real-World App: Time-series analysis, scheduling, sorting networks.
# =============================================================================

def longest_increasing_subsequence_dp(nums: List[int]) -> int:
    """
    Classical O(N^2) Dynamic Programming approach for LIS.
    
    Time Complexity: O(N^2) - nested loops over the array.
    Space Complexity: O(N) - to store the DP array.
    """
    if not nums:
        return 0
        
    n = len(nums)
    dp = [1] * n
    
    for i in range(1, n):
        for j in range(i):
            if nums[i] > nums[j]:
                dp[i] = max(dp[i], dp[j] + 1)
                
    return max(dp)

def longest_increasing_subsequence_optimized(nums: List[int]) -> int:
    """
    Optimal O(N log N) approach using Patience Sorting and Binary Search.
    
    Time Complexity: O(N log N) - We iterate N times, each time doing binary search (O(log N)).
    Space Complexity: O(N) - to store the active subsequence tails.
    """
    if not nums:
        return 0
        
    # 'sub' stores the smallest tail of all increasing subsequences of length i+1.
    # Note: 'sub' is NOT necessarily the actual LIS, but its length equals the LIS length.
    sub = []
    
    for num in nums:
        # Find the index of the first element in 'sub' that is >= num
        pos = bisect.bisect_left(sub, num)
        
        # If 'num' is greater than any element in 'sub', it extends the longest subsequence
        if pos == len(sub):
            sub.append(num)
        else:
            # Otherwise, it replaces the element at 'pos'. 
            # This maintains the potential for a longer sequence in the future 
            # by keeping the tails as small as possible.
            sub[pos] = num
            
    return len(sub)


# =============================================================================
# 4. Coin Change Problem
# =============================================================================
#
# Concept: Given an integer array of coin denominations and an integer amount,
# return the fewest number of coins that you need to make up that amount.
# If that amount cannot be made up, return -1.
# (This is an example of the Unbounded Knapsack problem).
#
# Mathematical Background (Recurrence Relation):
# Let DP[i] be the minimum coins to make amount i.
# - Base Case: DP[0] = 0
# - Transition: 
#   DP[i] = min(DP[i], 1 + DP[i - coin]) for all coin in coins where coin <= i
#
# Real-World App: Vending machines, ATM cash dispensing algorithms.
# =============================================================================

def coin_change(coins: List[int], amount: int) -> int:
    """
    Bottom-Up DP to find minimum coins for a given amount.
    
    Time Complexity: O(S * N) where S is the amount and N is the number of coin denominations.
    Space Complexity: O(S) to store the DP array.
    """
    # Initialize DP array with an impossible high value (amount + 1)
    # This acts as our "infinity"
    dp = [amount + 1] * (amount + 1)
    dp[0] = 0  # 0 coins needed to make amount 0
    
    # Iterate over all amounts from 1 to the target amount
    for i in range(1, amount + 1):
        for coin in coins:
            # If the current coin value is less than or equal to the amount we are building
            if coin <= i:
                # Minimum of what we have found so far, or 1 + the solution to (amount - coin)
                dp[i] = min(dp[i], dp[i - coin] + 1)
                
    # If the target amount remains greater than amount, it's unreachable
    return dp[amount] if dp[amount] <= amount else -1


# =============================================================================
# 5. Edit Distance (Levenshtein Distance)
# =============================================================================
#
# Concept: Given two strings word1 and word2, return the minimum number of 
# operations required to convert word1 to word2.
# Permitted operations: Insert a character, Delete a character, Replace a character.
#
# Mathematical Background (Recurrence Relation):
# Let DP[i][j] be the min operations to convert word1[0:i] to word2[0:j].
# - Base Cases: 
#   DP[i][0] = i (i deletions)
#   DP[0][j] = j (j insertions)
# - Transition:
#   If word1[i-1] == word2[j-1]: 
#       DP[i][j] = DP[i-1][j-1]
#   Else:
#       DP[i][j] = 1 + min(
#           DP[i-1][j],    # Delete
#           DP[i][j-1],    # Insert
#           DP[i-1][j-1]   # Replace
#       )
#
# Real-World App: Autocorrect, spell checkers, computational biology (DNA alignment).
# =============================================================================

def edit_distance(word1: str, word2: str) -> int:
    """
    Bottom-up Tabulation for Edit Distance.
    
    Time Complexity: O(M * N) where M and N are the lengths of word1 and word2.
    Space Complexity: O(M * N) for the DP table. (Can be optimized to O(min(M, N))).
    """
    m, n = len(word1), len(word2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # Initialize base cases
    # Converting word1 of length i to empty word2 requires i deletions
    for i in range(m + 1):
        dp[i][0] = i
        
    # Converting empty word1 to word2 of length j requires j insertions
    for j in range(n + 1):
        dp[0][j] = j
        
    # Fill the DP table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                # Characters match, no operation needed for this step
                dp[i][j] = dp[i - 1][j - 1]
            else:
                # Characters don't match, consider all 3 operations and take the minimum
                dp[i][j] = 1 + min(
                    dp[i - 1][j],    # Delete
                    dp[i][j - 1],    # Insert
                    dp[i - 1][j - 1] # Replace
                )
                
    return dp[m][n]


# =============================================================================
# Execution and Tests
# =============================================================================

def run_all_tests():
    """
    Comprehensive test suite validating the functionality of all DP implementations.
    """
    print("--- Starting Classical DP Algorithms Test Suite ---")
    
    # 1. LCS Tests
    assert longest_common_subsequence("abcde", "ace") == 3
    assert longest_common_subsequence("abc", "abc") == 3
    assert longest_common_subsequence("abc", "def") == 0
    
    length, sequence = longest_common_subsequence_with_path("abcde", "ace")
    assert length == 3 and sequence == "ace"
    print("[PASSED] Longest Common Subsequence")
    
    # 2. 0/1 Knapsack Tests
    weights = [10, 20, 30]
    values = [60, 100, 120]
    assert knapsack_01(weights, values, 50) == 220
    assert knapsack_01(weights, values, 10) == 60
    assert knapsack_01([1, 2, 3], [10, 15, 40], 6) == 65
    print("[PASSED] 0/1 Knapsack Problem")
    
    # 3. LIS Tests
    seq = [10, 9, 2, 5, 3, 7, 101, 18]
    assert longest_increasing_subsequence_dp(seq) == 4
    assert longest_increasing_subsequence_optimized(seq) == 4
    assert longest_increasing_subsequence_optimized([7, 7, 7, 7]) == 1
    assert longest_increasing_subsequence_optimized([0, 1, 0, 3, 2, 3]) == 4
    print("[PASSED] Longest Increasing Subsequence")
    
    # 4. Coin Change Tests
    assert coin_change([1, 2, 5], 11) == 3   # 5 + 5 + 1
    assert coin_change([2], 3) == -1         # Impossible
    assert coin_change([1], 0) == 0          # Amount is 0
    print("[PASSED] Coin Change Problem")
    
    # 5. Edit Distance Tests
    assert edit_distance("horse", "ros") == 3    # replace h->r, delete r, delete e
    assert edit_distance("intention", "execution") == 5
    assert edit_distance("", "a") == 1
    print("[PASSED] Edit Distance")
    
    print("--- All tests passed successfully! ---")

if __name__ == "__main__":
    run_all_tests()
