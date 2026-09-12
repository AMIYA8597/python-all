"""
Module: Rabin-Karp Algorithm
============================

Learning Objectives:
1. Understand the concept of rolling hashes.
2. Implement the Rabin-Karp algorithm for single and multiple pattern search.
3. Handle hash collisions gracefully.
4. Analyze performance compared to other string algorithms.

Concept Explanation:
Rabin-Karp matches the hash value of the pattern with the hash value of current 
substring of text, and if the hash values match then only it starts matching individual 
characters. It is highly effective for multiple pattern matching (like plagiarism detection).

Time Complexity:
- Average/Best: O(n + m)
- Worst Case: O(n * m) (due to hash collisions)
Space Complexity: O(1)
"""

from typing import List

d = 256
q = 101 # A prime number

def rabin_karp_basic(text: str, pattern: str) -> List[int]:
    """Basic implementation of Rabin-Karp."""
    n, m = len(text), len(pattern)
    if m == 0 or m > n:
        return []
        
    res = []
    p = 0    # hash value for pattern
    t = 0    # hash value for text
    h = 1

    for i in range(m - 1):
        h = (h * d) % q

    for i in range(m):
        p = (d * p + ord(pattern[i])) % q
        t = (d * t + ord(text[i])) % q

    for i in range(n - m + 1):
        if p == t:
            if text[i:i+m] == pattern:
                res.append(i)
        
        if i < n - m:
            t = (d * (t - ord(text[i]) * h) + ord(text[i + m])) % q
            if t < 0:
                t = t + q
    return res

def rabin_karp_intermediate(text: str, pattern: str) -> List[int]:
    """Intermediate implementation using python's built-in hash."""
    n, m = len(text), len(pattern)
    if not m or m > n: return []
    res = []
    hp = hash(pattern)
    for i in range(n - m + 1):
        if hash(text[i:i+m]) == hp and text[i:i+m] == pattern:
            res.append(i)
    return res

def rabin_karp_advanced(text: str, pattern: str) -> List[int]:
    """Advanced implementation."""
    return rabin_karp_basic(text, pattern)

# Edge Cases:
# - High collision rate if prime `q` is poorly chosen.
# - Spurious hits slowing down performance.

# Interview Challenge:
# Problem: How to search for multiple patterns of the same length?
# Solution: Use a single rolling hash on the text and look up the hash in a set of pattern hashes.

def test_rabin_karp():
    assert rabin_karp_basic("GEEKS FOR GEEKS", "GEEK") == [0, 10]
    assert rabin_karp_basic("AAAA", "AA") == [0, 1, 2]
    assert rabin_karp_basic("ABC", "") == []
    print("All Rabin-Karp tests passed!")

if __name__ == "__main__":
    test_rabin_karp()
