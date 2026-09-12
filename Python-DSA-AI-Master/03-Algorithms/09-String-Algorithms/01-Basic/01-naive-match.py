"""
Module: Naive String Matching Algorithm
=======================================

Learning Objectives:
1. Understand the fundamental concept of string matching.
2. Implement the naive approach to finding substrings.
3. Analyze the time and space complexity of the naive method.
4. Recognize edge cases and how to handle them.

Concept Explanation:
The naive string matching algorithm slides the pattern over text one by one and 
checks for a match. If a match is found, it slides by 1 again to check for subsequent 
matches. This approach doesn't require any pre-processing phases.

Time Complexity:
- Best Case: O(n) where n is length of text (when the first character of the pattern is not present in text at all).
- Worst Case: O(m*(n-m+1)) where m is length of pattern (when all characters of the text and pattern are same).

Space Complexity: O(1) as no extra space is needed.
"""

from typing import List

def naive_match_basic(text: str, pattern: str) -> List[int]:
    """Basic implementation of naive string matching."""
    n, m = len(text), len(pattern)
    res = []
    if m == 0:
        return res
        
    for i in range(n - m + 1):
        j = 0
        while j < m and text[i + j] == pattern[j]:
            j += 1
        if j == m:
            res.append(i)
    return res

def naive_match_intermediate(text: str, pattern: str) -> List[int]:
    """Intermediate implementation using slicing."""
    n, m = len(text), len(pattern)
    if not m or not text:
        return []
    return [i for i in range(n - m + 1) if text[i:i+m] == pattern]

def naive_match_advanced(text: str, pattern: str) -> List[int]:
    """Advanced implementation handling generators or streaming (simulated via iterators)."""
    def match_gen(t: str, p: str):
        n, m = len(t), len(p)
        if m == 0:
            return
        for i in range(n - m + 1):
            if all(t[i + k] == p[k] for k in range(m)):
                yield i
                
    return list(match_gen(text, pattern))

# Edge Cases to Handle:
# - Empty pattern or empty text
# - Pattern longer than text
# - Overlapping matches (e.g., text="AAAA", pattern="AA")

# Interview Challenge:
# Problem: How would you optimize this if you only needed to find the FIRST occurrence?
# Solution: Just return early when `j == m` instead of accumulating in a list.

def test_naive_match():
    # Test 1: Basic string matching
    assert naive_match_basic("AABAACAADAABAABA", "AABA") == [0, 9, 12]
    # Test 2: Edge cases
    assert naive_match_intermediate("ABC", "") == []
    assert naive_match_advanced("", "A") == []
    assert naive_match_basic("AAA", "AA") == [0, 1]
    
    print("All Naive Match tests passed!")

if __name__ == "__main__":
    test_naive_match()
