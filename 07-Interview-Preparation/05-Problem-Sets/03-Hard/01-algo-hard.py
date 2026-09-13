"""
Hard Algorithmic Problems - Interview Preparation

Learning Objectives:
1. Understand and implement advanced algorithms (e.g., KMP, A*, DP on Trees).
2. Analyze time and space complexities for hard problems.
3. Handle edge cases in complex algorithms.

This module provides implementations for hard algorithmic interview questions.
"""

from typing import List, Optional
import math

# 1. String Matching: KMP Algorithm (Knuth-Morris-Pratt)
def compute_lps_array(pattern: str) -> List[int]:
    """Computes the Longest Prefix Suffix (LPS) array."""
    length = 0
    lps = [0] * len(pattern)
    i = 1
    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    return lps

def kmp_search(text: str, pattern: str) -> List[int]:
    """
    Finds all occurrences of a pattern in a text using KMP algorithm.
    Time Complexity: O(N + M)
    Space Complexity: O(M)
    """
    if not pattern:
        return []
    
    n = len(text)
    m = len(pattern)
    lps = compute_lps_array(pattern)
    result = []
    
    i = 0  # index for text
    j = 0  # index for pattern
    while i < n:
        if pattern[j] == text[i]:
            i += 1
            j += 1
            
        if j == m:
            result.append(i - j)
            j = lps[j - 1]
        elif i < n and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return result

# 2. Dynamic Programming: Edit Distance
def min_distance(word1: str, word2: str) -> int:
    """
    Calculates the minimum number of operations required to convert word1 to word2.
    Operations allowed: Insert, Delete, Replace.
    Time Complexity: O(M * N)
    Space Complexity: O(M * N) - can be optimized to O(min(M, N))
    """
    m, n = len(word1), len(word2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0:
                dp[i][j] = j
            elif j == 0:
                dp[i][j] = i
            elif word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i][j - 1],    # Insert
                                   dp[i - 1][j],    # Remove
                                   dp[i - 1][j - 1]) # Replace
    return dp[m][n]

def test_algorithms():
    print("Testing KMP Search:")
    text = "ABABDABACDABABCABAB"
    pattern = "ABABCABAB"
    res = kmp_search(text, pattern)
    print(f"Pattern found at indices: {res}")
    assert res == [10]
    
    print("\nTesting Edit Distance:")
    w1, w2 = "horse", "ros"
    dist = min_distance(w1, w2)
    print(f"Edit distance between '{w1}' and '{w2}' is {dist}")
    assert dist == 3

if __name__ == "__main__":
    test_algorithms()
    print("\nAll algorithms tests passed!")
