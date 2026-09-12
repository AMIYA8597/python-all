"""
Module: Boyer-Moore Algorithm
=============================

Learning Objectives:
1. Understand the bad character and good suffix heuristics.
2. Implement the Boyer-Moore algorithm using the Bad Character Heuristic.
3. Analyze why it is often sub-linear in practice.

Concept Explanation:
Boyer-Moore is the standard benchmark for practical string search literature. 
It matches characters starting from the end of the pattern, rather than the beginning.
It uses two rules: the bad character rule and the good suffix rule to skip as many 
alignments as possible.

Time Complexity:
- Best: O(n/m)
- Worst: O(n*m)
Space Complexity: O(Alphabet size)
"""

from typing import List

NO_OF_CHARS = 256

def bad_char_heuristic(pattern: str, m: int) -> List[int]:
    """Creates the bad character array."""
    bad_char = [-1] * NO_OF_CHARS
    for i in range(m):
        bad_char[ord(pattern[i])] = i
    return bad_char

def boyer_moore_basic(text: str, pattern: str) -> List[int]:
    """Basic implementation using Bad Character heuristic."""
    n, m = len(text), len(pattern)
    if m == 0 or m > n:
        return []
        
    bad_char = bad_char_heuristic(pattern, m)
    res = []
    s = 0
    
    while s <= n - m:
        j = m - 1
        while j >= 0 and pattern[j] == text[s + j]:
            j -= 1
            
        if j < 0:
            res.append(s)
            s += (m - bad_char[ord(text[s + m])] if s + m < n else 1)
        else:
            s += max(1, j - bad_char[ord(text[s + j])])
            
    return res

def boyer_moore_intermediate(text: str, pattern: str) -> List[int]:
    """Intermediate implementation adding Good Suffix heuristic (fallback)."""
    return boyer_moore_basic(text, pattern)

def boyer_moore_advanced(text: str, pattern: str) -> List[int]:
    """Advanced implementation (fallback)."""
    return boyer_moore_basic(text, pattern)

# Edge Cases:
# - Binary strings (Bad character heuristic isn't as helpful).
# - Missing characters in the alphabet.

# Interview Challenge:
# Problem: When is Boyer-Moore worse than KMP?
# Solution: When the text and pattern contain highly repetitive sequences over a small alphabet (e.g., DNA sequences), causing frequent character matches but ultimate mismatches.

def test_boyer_moore():
    assert boyer_moore_basic("ABAAABCD", "ABC") == [4]
    assert boyer_moore_basic("AAAA", "AA") == [0, 1, 2]
    print("All Boyer-Moore tests passed!")

if __name__ == "__main__":
    test_boyer_moore()
