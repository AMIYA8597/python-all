"""
Module: Longest Common Prefix (LCP) Array
=========================================

Learning Objectives:
1. Understand the concept of the LCP array.
2. Implement Kasai's algorithm to compute the LCP array in O(n) time.
3. Understand its application with Suffix Arrays.

Concept Explanation:
The LCP array stores the lengths of the longest common prefixes between 
consecutive suffixes in a sorted Suffix Array. Kasai's algorithm allows us 
to compute it in linear time O(n) given the string and its suffix array.

Time Complexity: O(n)
Space Complexity: O(n)
"""

from typing import List

def get_suffix_array(s: str) -> List[int]:
    """Helper to get a basic suffix array."""
    suffixes = [(s[i:], i) for i in range(len(s))]
    suffixes.sort(key=lambda x: x[0])
    return [x[1] for x in suffixes]

def lcp_kasai_basic(s: str, suffix_arr: List[int]) -> List[int]:
    """Basic implementation of Kasai's Algorithm."""
    n = len(s)
    lcp = [0] * n
    inv_suff = [0] * n
    
    for i in range(n):
        inv_suff[suffix_arr[i]] = i
        
    k = 0
    for i in range(n):
        if inv_suff[i] == n - 1:
            k = 0
            continue
            
        j = suffix_arr[inv_suff[i] + 1]
        
        while i + k < n and j + k < n and s[i + k] == s[j + k]:
            k += 1
            
        lcp[inv_suff[i]] = k
        if k > 0:
            k -= 1
            
    return lcp

def lcp_intermediate(s: str) -> List[int]:
    """Computes suffix array and LCP together."""
    sa = get_suffix_array(s)
    return lcp_kasai_basic(s, sa)

def lcp_advanced(s: str) -> int:
    """Advanced: Find longest repeated substring length using LCP."""
    lcp_arr = lcp_intermediate(s)
    return max(lcp_arr) if lcp_arr else 0

# Edge Cases:
# - Empty string
# - No repeated substrings

# Interview Challenge:
# Problem: How to count the total number of unique substrings?
# Solution: (n * (n + 1) // 2) - sum(LCP array)

def test_lcp():
    s = "banana"
    sa = get_suffix_array(s)
    assert lcp_kasai_basic("banana", get_suffix_array("banana")) == [1, 3, 0, 0, 2, 0]
    print("All LCP Array tests passed!")

if __name__ == "__main__":
    test_lcp()
