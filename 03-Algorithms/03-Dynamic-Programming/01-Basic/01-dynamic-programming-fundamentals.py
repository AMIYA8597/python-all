#!/usr/bin/env python3
"""
Dynamic Programming Fundamentals
===============================

This module provides comprehensive implementations of dynamic programming
algorithms, including classic problems and optimization techniques:

1. Fibonacci Numbers (Multiple Approaches)
2. Longest Common Subsequence (LCS)
3. Knapsack Problems (0/1 and Unbounded)
4. Coin Change Problem
5. Edit Distance
6. Maximum Subarray Sum (Kadane's Algorithm)
7. Palindrome Problems
8. Path Counting Problems
9. Stock Trading Problems
10. Optimization Patterns

All implementations include detailed explanations, complexity analysis,
and multiple solution approaches (recursive, memoized, tabulated).

Author: Python DSA Master
Date: 2024
"""

import sys
from typing import List, Dict, Tuple, Any, Optional
from functools import lru_cache
from dataclasses import dataclass
import time

# ==============================================================================
# FIBONACCI SEQUENCE - MULTIPLE APPROACHES
# ==============================================================================

class FibonacciSolver:
    """Fibonacci sequence with different DP approaches."""
    
    @staticmethod
    def fibonacci_naive(n: int) -> int:
        """
        Naive recursive approach.
        Time: O(2^n), Space: O(n) - call stack
        """
        if n <= 1:
            return n
        return FibonacciSolver.fibonacci_naive(n - 1) + FibonacciSolver.fibonacci_naive(n - 2)
    
    @staticmethod
    def fibonacci_memoized(n: int, memo: Dict[int, int] = None) -> int:
        """
        Top-down DP with memoization.
        Time: O(n), Space: O(n)
        """
        if memo is None:
            memo = {}
        
        if n in memo:
            return memo[n]
        
        if n <= 1:
            return n
        
        memo[n] = FibonacciSolver.fibonacci_memoized(n - 1, memo) + \
                  FibonacciSolver.fibonacci_memoized(n - 2, memo)
        return memo[n]
    
    @staticmethod
    def fibonacci_tabulated(n: int) -> int:
        """
        Bottom-up DP with tabulation.
        Time: O(n), Space: O(n)
        """
        if n <= 1:
            return n
        
        dp = [0] * (n + 1)
        dp[0], dp[1] = 0, 1
        
        for i in range(2, n + 1):
            dp[i] = dp[i - 1] + dp[i - 2]
        
        return dp[n]
    
    @staticmethod
    def fibonacci_optimized(n: int) -> int:
        """
        Space-optimized DP.
        Time: O(n), Space: O(1)
        """
        if n <= 1:
            return n
        
        prev2, prev1 = 0, 1
        for _ in range(2, n + 1):
            current = prev1 + prev2
            prev2, prev1 = prev1, current
        
        return prev1
    
    @staticmethod
    @lru_cache(maxsize=None)
    def fibonacci_lru(n: int) -> int:
        """Using Python's LRU cache decorator."""
        if n <= 1:
            return n
        return FibonacciSolver.fibonacci_lru(n - 1) + FibonacciSolver.fibonacci_lru(n - 2)

# ==============================================================================
# LONGEST COMMON SUBSEQUENCE (LCS)
# ==============================================================================

class LCSolver:
    """Longest Common Subsequence problem solver."""
    
    @staticmethod
    def lcs_length_recursive(text1: str, text2: str) -> int:
        """
        Recursive solution for LCS length.
        Time: O(2^(m+n)), Space: O(m+n)
        """
        def helper(i: int, j: int) -> int:
            if i == 0 or j == 0:
                return 0
            
            if text1[i - 1] == text2[j - 1]:
                return 1 + helper(i - 1, j - 1)
            else:
                return max(helper(i - 1, j), helper(i, j - 1))
        
        return helper(len(text1), len(text2))
    
    @staticmethod
    def lcs_length_memoized(text1: str, text2: str) -> int:
        """
        Memoized solution for LCS length.
        Time: O(m*n), Space: O(m*n)
        """
        m, n = len(text1), len(text2)
        memo = {}
        
        def helper(i: int, j: int) -> int:
            if (i, j) in memo:
                return memo[(i, j)]
            
            if i == 0 or j == 0:
                return 0
            
            if text1[i - 1] == text2[j - 1]:
                result = 1 + helper(i - 1, j - 1)
            else:
                result = max(helper(i - 1, j), helper(i, j - 1))
            
            memo[(i, j)] = result
            return result
        
        return helper(m, n)
    
    @staticmethod
    def lcs_tabulated(text1: str, text2: str) -> Tuple[int, str]:
        """
        Tabulated solution that returns both length and LCS string.
        Time: O(m*n), Space: O(m*n)
        """
        m, n = len(text1), len(text2)
        
        # Create DP table
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        
        # Fill the table
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if text1[i - 1] == text2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1] + 1
                else:
                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
        
        # Reconstruct LCS string
        lcs = []
        i, j = m, n
        while i > 0 and j > 0:
            if text1[i - 1] == text2[j - 1]:
                lcs.append(text1[i - 1])
                i -= 1
                j -= 1
            elif dp[i - 1][j] > dp[i][j - 1]:
                i -= 1
            else:
                j -= 1
        
        lcs.reverse()
        return dp[m][n], ''.join(lcs)
    
    @staticmethod
    def lcs_space_optimized(text1: str, text2: str) -> int:
        """
        Space-optimized solution for LCS length only.
        Time: O(m*n), Space: O(min(m,n))
        """
        m, n = len(text1), len(text2)
        
        # Ensure text2 is shorter for space optimization
        if m < n:
            text1, text2 = text2, text1
            m, n = n, m
        
        # Use only two rows
        prev = [0] * (n + 1)
        curr = [0] * (n + 1)
        
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if text1[i - 1] == text2[j - 1]:
                    curr[j] = prev[j - 1] + 1
                else:
                    curr[j] = max(prev[j], curr[j - 1])
            
            prev, curr = curr, prev
        
        return prev[n]

# ==============================================================================
# KNAPSACK PROBLEMS
# ==============================================================================

@dataclass
class Item:
    """Item for knapsack problems."""
    weight: int
    value: int
    name: str = ""

class KnapsackSolver:
    """0/1 and Unbounded Knapsack problem solvers."""
    
    @staticmethod
    def knapsack_01_recursive(capacity: int, items: List[Item]) -> int:
        """
        0/1 Knapsack recursive solution.
        Time: O(2^n), Space: O(n)
        """
        def helper(i: int, remaining_capacity: int) -> int:
            if i == 0 or remaining_capacity == 0:
                return 0
            
            # Can't include current item
            if items[i - 1].weight > remaining_capacity:
                return helper(i - 1, remaining_capacity)
            
            # Max of including or excluding current item
            include = items[i - 1].value + helper(i - 1, remaining_capacity - items[i - 1].weight)
            exclude = helper(i - 1, remaining_capacity)
            
            return max(include, exclude)
        
        return helper(len(items), capacity)
    
    @staticmethod
    def knapsack_01_memoized(capacity: int, items: List[Item]) -> int:
        """
        0/1 Knapsack memoized solution.
        Time: O(n*W), Space: O(n*W)
        """
        memo = {}
        
        def helper(i: int, remaining_capacity: int) -> int:
            if (i, remaining_capacity) in memo:
                return memo[(i, remaining_capacity)]
            
            if i == 0 or remaining_capacity == 0:
                return 0
            
            if items[i - 1].weight > remaining_capacity:
                result = helper(i - 1, remaining_capacity)
            else:
                include = items[i - 1].value + helper(i - 1, remaining_capacity - items[i - 1].weight)
                exclude = helper(i - 1, remaining_capacity)
                result = max(include, exclude)
            
            memo[(i, remaining_capacity)] = result
            return result
        
        return helper(len(items), capacity)
    
    @staticmethod
    def knapsack_01_tabulated(capacity: int, items: List[Item]) -> Tuple[int, List[Item]]:
        """
        0/1 Knapsack tabulated solution with item tracking.
        Time: O(n*W), Space: O(n*W)
        """
        n = len(items)
        dp = [[0] * (capacity + 1) for _ in range(n + 1)]
        
        # Fill the table
        for i in range(1, n + 1):
            for w in range(1, capacity + 1):
                if items[i - 1].weight <= w:
                    include = items[i - 1].value + dp[i - 1][w - items[i - 1].weight]
                    exclude = dp[i - 1][w]
                    dp[i][w] = max(include, exclude)
                else:
                    dp[i][w] = dp[i - 1][w]
        
        # Backtrack to find selected items
        selected_items = []
        i, w = n, capacity
        while i > 0 and w > 0:
            if dp[i][w] != dp[i - 1][w]:
                selected_items.append(items[i - 1])
                w -= items[i - 1].weight
            i -= 1
        
        return dp[n][capacity], selected_items
    
    @staticmethod
    def knapsack_01_space_optimized(capacity: int, items: List[Item]) -> int:
        """
        0/1 Knapsack space-optimized solution.
        Time: O(n*W), Space: O(W)
        """
        dp = [0] * (capacity + 1)
        
        for item in items:
            # Traverse backwards to avoid using updated values
            for w in range(capacity, item.weight - 1, -1):
                dp[w] = max(dp[w], dp[w - item.weight] + item.value)
        
        return dp[capacity]
    
    @staticmethod
    def knapsack_unbounded(capacity: int, items: List[Item]) -> int:
        """
        Unbounded Knapsack problem.
        Time: O(n*W), Space: O(W)
        """
        dp = [0] * (capacity + 1)
        
        for w in range(1, capacity + 1):
            for item in items:
                if item.weight <= w:
                    dp[w] = max(dp[w], dp[w - item.weight] + item.value)
        
        return dp[capacity]

# ==============================================================================
# COIN CHANGE PROBLEMS
# ==============================================================================

class CoinChangeSolver:
    """Coin change problem solvers."""
    
    @staticmethod
    def min_coins_recursive(coins: List[int], amount: int) -> int:
        """
        Minimum coins recursive solution.
        Time: O(amount^n), Space: O(amount)
        """
        if amount == 0:
            return 0
        if amount < 0:
            return float('inf')
        
        min_coins = float('inf')
        for coin in coins:
            result = CoinChangeSolver.min_coins_recursive(coins, amount - coin)
            if result != float('inf'):
                min_coins = min(min_coins, result + 1)
        
        return min_coins
    
    @staticmethod
    def min_coins_memoized(coins: List[int], amount: int) -> int:
        """
        Minimum coins memoized solution.
        Time: O(amount * len(coins)), Space: O(amount)
        """
        memo = {}
        
        def helper(remaining: int) -> int:
            if remaining in memo:
                return memo[remaining]
            
            if remaining == 0:
                return 0
            if remaining < 0:
                return float('inf')
            
            min_coins = float('inf')
            for coin in coins:
                result = helper(remaining - coin)
                if result != float('inf'):
                    min_coins = min(min_coins, result + 1)
            
            memo[remaining] = min_coins
            return min_coins
        
        result = helper(amount)
        return result if result != float('inf') else -1
    
    @staticmethod
    def min_coins_tabulated(coins: List[int], amount: int) -> Tuple[int, List[int]]:
        """
        Minimum coins tabulated solution with coin tracking.
        Time: O(amount * len(coins)), Space: O(amount)
        """
        dp = [float('inf')] * (amount + 1)
        dp[0] = 0
        parent = [-1] * (amount + 1)  # To track which coin was used
        
        for i in range(1, amount + 1):
            for coin in coins:
                if coin <= i and dp[i - coin] + 1 < dp[i]:
                    dp[i] = dp[i - coin] + 1
                    parent[i] = coin
        
        if dp[amount] == float('inf'):
            return -1, []
        
        # Reconstruct solution
        result_coins = []
        curr = amount
        while curr > 0:
            coin_used = parent[curr]
            result_coins.append(coin_used)
            curr -= coin_used
        
        return dp[amount], result_coins
    
    @staticmethod
    def count_ways(coins: List[int], amount: int) -> int:
        """
        Count number of ways to make amount.
        Time: O(amount * len(coins)), Space: O(amount)
        """
        dp = [0] * (amount + 1)
        dp[0] = 1  # One way to make 0: use no coins
        
        for coin in coins:
            for i in range(coin, amount + 1):
                dp[i] += dp[i - coin]
        
        return dp[amount]

# ==============================================================================
# EDIT DISTANCE (LEVENSHTEIN DISTANCE)
# ==============================================================================

class EditDistanceSolver:
    """Edit distance problem solver."""
    
    @staticmethod
    def edit_distance_recursive(word1: str, word2: str) -> int:
        """
        Recursive solution for edit distance.
        Time: O(3^max(m,n)), Space: O(max(m,n))
        """
        def helper(i: int, j: int) -> int:
            if i == 0:
                return j  # Insert all characters from word2
            if j == 0:
                return i  # Delete all characters from word1
            
            if word1[i - 1] == word2[j - 1]:
                return helper(i - 1, j - 1)  # No operation needed
            
            # Try all three operations and take minimum
            insert = helper(i, j - 1) + 1
            delete = helper(i - 1, j) + 1
            replace = helper(i - 1, j - 1) + 1
            
            return min(insert, delete, replace)
        
        return helper(len(word1), len(word2))
    
    @staticmethod
    def edit_distance_tabulated(word1: str, word2: str) -> Tuple[int, List[str]]:
        """
        Tabulated solution with operation tracking.
        Time: O(m*n), Space: O(m*n)
        """
        m, n = len(word1), len(word2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        
        # Initialize base cases
        for i in range(m + 1):
            dp[i][0] = i
        for j in range(n + 1):
            dp[0][j] = j
        
        # Fill the table
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if word1[i - 1] == word2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1]
                else:
                    dp[i][j] = min(
                        dp[i][j - 1] + 1,    # Insert
                        dp[i - 1][j] + 1,    # Delete
                        dp[i - 1][j - 1] + 1 # Replace
                    )
        
        # Reconstruct operations
        operations = []
        i, j = m, n
        while i > 0 or j > 0:
            if i > 0 and j > 0 and word1[i - 1] == word2[j - 1]:
                i -= 1
                j -= 1
            elif i > 0 and j > 0 and dp[i][j] == dp[i - 1][j - 1] + 1:
                operations.append(f"Replace '{word1[i - 1]}' with '{word2[j - 1]}' at position {i}")
                i -= 1
                j -= 1
            elif j > 0 and dp[i][j] == dp[i][j - 1] + 1:
                operations.append(f"Insert '{word2[j - 1]}' at position {i + 1}")
                j -= 1
            else:
                operations.append(f"Delete '{word1[i - 1]}' at position {i}")
                i -= 1
        
        operations.reverse()
        return dp[m][n], operations
    
    @staticmethod
    def edit_distance_space_optimized(word1: str, word2: str) -> int:
        """
        Space-optimized solution.
        Time: O(m*n), Space: O(min(m,n))
        """
        m, n = len(word1), len(word2)
        
        if m < n:
            word1, word2 = word2, word1
            m, n = n, m
        
        prev = list(range(n + 1))
        curr = [0] * (n + 1)
        
        for i in range(1, m + 1):
            curr[0] = i
            for j in range(1, n + 1):
                if word1[i - 1] == word2[j - 1]:
                    curr[j] = prev[j - 1]
                else:
                    curr[j] = min(curr[j - 1], prev[j], prev[j - 1]) + 1
            prev, curr = curr, prev
        
        return prev[n]

# ==============================================================================
# MAXIMUM SUBARRAY PROBLEMS
# ==============================================================================

class SubarraySolver:
    """Maximum subarray problem solvers."""
    
    @staticmethod
    def max_subarray_kadane(nums: List[int]) -> Tuple[int, Tuple[int, int]]:
        """
        Kadane's algorithm for maximum subarray sum.
        Time: O(n), Space: O(1)
        """
        max_sum = float('-inf')
        current_sum = 0
        start = end = 0
        temp_start = 0
        
        for i, num in enumerate(nums):
            current_sum += num
            
            if current_sum > max_sum:
                max_sum = current_sum
                start = temp_start
                end = i
            
            if current_sum < 0:
                current_sum = 0
                temp_start = i + 1
        
        return max_sum, (start, end)
    
    @staticmethod
    def max_subarray_dp(nums: List[int]) -> int:
        """
        DP approach for maximum subarray sum.
        Time: O(n), Space: O(1)
        """
        if not nums:
            return 0
        
        max_ending_here = max_so_far = nums[0]
        
        for i in range(1, len(nums)):
            max_ending_here = max(nums[i], max_ending_here + nums[i])
            max_so_far = max(max_so_far, max_ending_here)
        
        return max_so_far
    
    @staticmethod
    def max_product_subarray(nums: List[int]) -> int:
        """
        Maximum product subarray problem.
        Time: O(n), Space: O(1)
        """
        if not nums:
            return 0
        
        max_product = min_product = result = nums[0]
        
        for i in range(1, len(nums)):
            if nums[i] < 0:
                max_product, min_product = min_product, max_product
            
            max_product = max(nums[i], max_product * nums[i])
            min_product = min(nums[i], min_product * nums[i])
            
            result = max(result, max_product)
        
        return result

# ==============================================================================
# PALINDROME PROBLEMS
# ==============================================================================

class PalindromeSolver:
    """Palindrome-related DP problems."""
    
    @staticmethod
    def longest_palindromic_subsequence(s: str) -> int:
        """
        Length of longest palindromic subsequence.
        Time: O(n^2), Space: O(n^2)
        """
        n = len(s)
        dp = [[0] * n for _ in range(n)]
        
        # Every single character is a palindrome
        for i in range(n):
            dp[i][i] = 1
        
        # Check for palindromes of length 2
        for i in range(n - 1):
            if s[i] == s[i + 1]:
                dp[i][i + 1] = 2
            else:
                dp[i][i + 1] = 1
        
        # Check for palindromes of length 3 and more
        for length in range(3, n + 1):
            for i in range(n - length + 1):
                j = i + length - 1
                
                if s[i] == s[j]:
                    dp[i][j] = dp[i + 1][j - 1] + 2
                else:
                    dp[i][j] = max(dp[i + 1][j], dp[i][j - 1])
        
        return dp[0][n - 1]
    
    @staticmethod
    def min_insertions_for_palindrome(s: str) -> int:
        """
        Minimum insertions to make string palindrome.
        Time: O(n^2), Space: O(n^2)
        """
        n = len(s)
        lps_length = PalindromeSolver.longest_palindromic_subsequence(s)
        return n - lps_length
    
    @staticmethod
    def palindrome_partitioning_min_cuts(s: str) -> int:
        """
        Minimum cuts needed to partition string into palindromes.
        Time: O(n^2), Space: O(n^2)
        """
        n = len(s)
        
        # is_palindrome[i][j] = True if s[i:j+1] is palindrome
        is_palindrome = [[False] * n for _ in range(n)]
        
        # Every single character is palindrome
        for i in range(n):
            is_palindrome[i][i] = True
        
        # Check for palindromes of length 2
        for i in range(n - 1):
            is_palindrome[i][i + 1] = (s[i] == s[i + 1])
        
        # Check for palindromes of length 3 and more
        for length in range(3, n + 1):
            for i in range(n - length + 1):
                j = i + length - 1
                is_palindrome[i][j] = (s[i] == s[j]) and is_palindrome[i + 1][j - 1]
        
        # cuts[i] = minimum cuts needed for s[0:i+1]
        cuts = [0] * n
        
        for i in range(n):
            if is_palindrome[0][i]:
                cuts[i] = 0
            else:
                cuts[i] = float('inf')
                for j in range(i):
                    if is_palindrome[j + 1][i]:
                        cuts[i] = min(cuts[i], cuts[j] + 1)
        
        return cuts[n - 1]

# ==============================================================================
# DEMONSTRATION AND TESTING
# ==============================================================================

def demonstrate_dp_algorithms():
    """Demonstrate all DP algorithms with examples."""
    print("Dynamic Programming Algorithms Demonstration")
    print("=" * 60)
    
    # 1. Fibonacci
    print("\n1. Fibonacci Sequence:")
    n = 20
    print(f"   Computing Fibonacci({n}):")
    
    start_time = time.time()
    fib_opt = FibonacciSolver.fibonacci_optimized(n)
    opt_time = time.time() - start_time
    
    start_time = time.time()
    fib_tab = FibonacciSolver.fibonacci_tabulated(n)
    tab_time = time.time() - start_time
    
    print(f"   Optimized: {fib_opt} (Time: {opt_time:.6f}s)")
    print(f"   Tabulated: {fib_tab} (Time: {tab_time:.6f}s)")
    
    # 2. Longest Common Subsequence
    print("\n2. Longest Common Subsequence:")
    text1, text2 = "ABCDGH", "AEDFHR"
    length, lcs_str = LCSolver.lcs_tabulated(text1, text2)
    print(f"   Text1: '{text1}', Text2: '{text2}'")
    print(f"   LCS Length: {length}, LCS: '{lcs_str}'")
    
    # 3. 0/1 Knapsack
    print("\n3. 0/1 Knapsack Problem:")
    items = [
        Item(10, 60, "Item1"),
        Item(20, 100, "Item2"),
        Item(30, 120, "Item3")
    ]
    capacity = 50
    
    max_value, selected = KnapsackSolver.knapsack_01_tabulated(capacity, items)
    print(f"   Capacity: {capacity}")
    print(f"   Items: {[(item.name, item.weight, item.value) for item in items]}")
    print(f"   Maximum value: {max_value}")
    print(f"   Selected items: {[(item.name, item.weight, item.value) for item in selected]}")
    
    # 4. Coin Change
    print("\n4. Coin Change Problem:")
    coins = [1, 3, 4]
    amount = 6
    min_coins, coin_sequence = CoinChangeSolver.min_coins_tabulated(coins, amount)
    ways = CoinChangeSolver.count_ways(coins, amount)
    
    print(f"   Coins: {coins}, Amount: {amount}")
    print(f"   Minimum coins: {min_coins}")
    print(f"   Coin sequence: {coin_sequence}")
    print(f"   Number of ways: {ways}")
    
    # 5. Edit Distance
    print("\n5. Edit Distance:")
    word1, word2 = "kitten", "sitting"
    distance, operations = EditDistanceSolver.edit_distance_tabulated(word1, word2)
    print(f"   Word1: '{word1}', Word2: '{word2}'")
    print(f"   Edit distance: {distance}")
    print(f"   Operations: {operations[:3]}...")  # Show first 3 operations
    
    # 6. Maximum Subarray
    print("\n6. Maximum Subarray (Kadane's Algorithm):")
    nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
    max_sum, (start, end) = SubarraySolver.max_subarray_kadane(nums)
    print(f"   Array: {nums}")
    print(f"   Maximum sum: {max_sum}")
    print(f"   Subarray: {nums[start:end+1]} (indices {start} to {end})")
    
    # 7. Longest Palindromic Subsequence
    print("\n7. Longest Palindromic Subsequence:")
    s = "bbbab"
    lps_length = PalindromeSolver.longest_palindromic_subsequence(s)
    min_insertions = PalindromeSolver.min_insertions_for_palindrome(s)
    print(f"   String: '{s}'")
    print(f"   LPS length: {lps_length}")
    print(f"   Minimum insertions for palindrome: {min_insertions}")

def benchmark_dp_approaches():
    """Benchmark different DP approaches."""
    print("\nDynamic Programming Performance Benchmark")
    print("=" * 50)
    
    # Fibonacci comparison
    print("Fibonacci computation benchmark:")
    test_values = [10, 15, 20, 25]
    
    for n in test_values:
        print(f"\n  n = {n}:")
        
        # Memoized
        start_time = time.time()
        result_memo = FibonacciSolver.fibonacci_memoized(n)
        memo_time = time.time() - start_time
        
        # Tabulated
        start_time = time.time()
        result_tab = FibonacciSolver.fibonacci_tabulated(n)
        tab_time = time.time() - start_time
        
        # Optimized
        start_time = time.time()
        result_opt = FibonacciSolver.fibonacci_optimized(n)
        opt_time = time.time() - start_time
        
        print(f"    Memoized:  {result_memo:>10} ({memo_time:.6f}s)")
        print(f"    Tabulated: {result_tab:>10} ({tab_time:.6f}s)")
        print(f"    Optimized: {result_opt:>10} ({opt_time:.6f}s)")
    
    # LCS comparison
    print(f"\nLCS computation benchmark:")
    text1, text2 = "ABCDEFGHIJKLMNOP", "ACDFHJLNPR"
    
    start_time = time.time()
    lcs_memo = LCSolver.lcs_length_memoized(text1, text2)
    memo_time = time.time() - start_time
    
    start_time = time.time()
    lcs_tab, _ = LCSolver.lcs_tabulated(text1, text2)
    tab_time = time.time() - start_time
    
    start_time = time.time()
    lcs_opt = LCSolver.lcs_space_optimized(text1, text2)
    opt_time = time.time() - start_time
    
    print(f"  Text lengths: {len(text1)}, {len(text2)}")
    print(f"  Memoized:      {lcs_memo} ({memo_time:.6f}s)")
    print(f"  Tabulated:     {lcs_tab} ({tab_time:.6f}s)")
    print(f"  Space-opt:     {lcs_opt} ({opt_time:.6f}s)")

def main():
    """Main demonstration function."""
    demonstrate_dp_algorithms()
    benchmark_dp_approaches()
    
    print("\n" + "=" * 60)
    print("Dynamic Programming Key Concepts:")
    print("- Optimal Substructure: Problem can be broken into smaller subproblems")
    print("- Overlapping Subproblems: Same subproblems solved multiple times")
    print("- Memoization: Top-down approach with caching")
    print("- Tabulation: Bottom-up approach filling table")
    print("- Space Optimization: Reduce space complexity when possible")
    print("- Time-Space Tradeoffs: Choose approach based on constraints")

if __name__ == "__main__":
    main()
