"""
Module: Z Algorithm
===================

Learning Objectives:
1. Understand the concept of the Z-array.
2. Implement the Z algorithm in linear time.
3. Use the Z algorithm for pattern matching.

Concept Explanation:
The Z algorithm finds all occurrences of a pattern in a text in linear time.
It constructs a Z array. For a string str[0..n-1], Z array is of same length.
An element Z[i] is the length of the longest substring starting from str[i] 
which is also a prefix of str[0..n-1].

Time Complexity: O(m + n)
Space Complexity: O(m + n)
"""

from typing import List

def get_z_array(string: str) -> List[int]:
    """Compute the Z array for a given string."""
    n = len(string)
    z = [0] * n
    l, r, k = 0, 0, 0
    for i in range(1, n):
        if i > r:
            l, r = i, i
            while r < n and string[r - l] == string[r]:
                r += 1
            z[i] = r - l
            r -= 1
        else:
            k = i - l
            if z[k] < r - i + 1:
                z[i] = z[k]
            else:
                l = i
                while r < n and string[r - l] == string[r]:
                    r += 1
                z[i] = r - l
                r -= 1
    return z

def z_algo_basic(text: str, pattern: str) -> List[int]:
    """Basic implementation of Z-algorithm pattern search."""
    if not pattern:
        return []
    concat = pattern + "$" + text
    z = get_z_array(concat)
    res = []
    
    for i in range(len(concat)):
        if z[i] == len(pattern):
            res.append(i - len(pattern) - 1)
    return res

def z_algo_intermediate(text: str, pattern: str) -> List[int]:
    return z_algo_basic(text, pattern)

def z_algo_advanced(text: str, pattern: str) -> List[int]:
    return z_algo_basic(text, pattern)

# Edge Cases:
# - Pattern not in text.
# - Special separator character `$` must not be in text or pattern.

# Interview Challenge:
# Problem: How to find all palindromes using a similar prefix-matching concept?
# Solution: Manacher's algorithm is preferred, but Z-array can help in certain prefix-palindrome problems by reversing the string.

def test_z_algo():
    assert z_algo_basic("GEEKS FOR GEEKS", "GEEK") == [0, 10]
    assert z_algo_basic("AAAA", "AA") == [0, 1, 2]
    print("All Z Algorithm tests passed!")

if __name__ == "__main__":
    test_z_algo()
