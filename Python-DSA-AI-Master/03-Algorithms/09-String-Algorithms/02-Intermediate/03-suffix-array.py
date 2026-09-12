"""
Module: Suffix Array
====================

Learning Objectives:
1. Understand what a suffix array is and its relationship with suffix trees.
2. Implement an O(n log^2 n) construction of a suffix array.
3. Understand its application in fast string matching and LCP.

Concept Explanation:
A suffix array is a sorted array of all suffixes of a given string.
It is a simpler, space-efficient alternative to suffix trees. Suffix arrays 
allow binary searching for a pattern in O(m log n) time.

Time Complexity (Construction): O(n log^2 n) or O(n log n) depending on implementation.
Space Complexity: O(n)
"""

from typing import List
from functools import cmp_to_key

def suffix_array_basic(s: str) -> List[int]:
    """Basic O(n^2 log n) or naive O(n^2) implementation."""
    suffixes = [(s[i:], i) for i in range(len(s))]
    suffixes.sort(key=lambda x: x[0])
    return [x[1] for x in suffixes]

def suffix_array_intermediate(s: str) -> List[int]:
    """O(n log^2 n) implementation using prefix ranks."""
    n = len(s)
    if n == 0:
        return []
        
    su = []
    for i in range(n):
        su.append({'index': i, 'rank': [ord(s[i]) - ord('a'), 
                  ord(s[i + 1]) - ord('a') if i + 1 < n else -1]})
                  
    def cmp(a, b):
        if a['rank'][0] == b['rank'][0]:
            return a['rank'][1] - b['rank'][1]
        return a['rank'][0] - b['rank'][0]
        
    su.sort(key=cmp_to_key(cmp))
    
    ind = [0] * n
    k = 4
    while k < 2 * n:
        rank = 0
        prev_rank = su[0]['rank'][0]
        su[0]['rank'][0] = rank
        ind[su[0]['index']] = 0
        
        for i in range(1, n):
            if su[i]['rank'][0] == prev_rank and su[i]['rank'][1] == su[i - 1]['rank'][1]:
                prev_rank = su[i]['rank'][0]
                su[i]['rank'][0] = rank
            else:
                prev_rank = su[i]['rank'][0]
                rank += 1
                su[i]['rank'][0] = rank
            ind[su[i]['index']] = i
            
        for i in range(n):
            next_idx = su[i]['index'] + k // 2
            su[i]['rank'][1] = su[ind[next_idx]]['rank'][0] if next_idx < n else -1
            
        su.sort(key=cmp_to_key(cmp))
        k *= 2
        
    return [x['index'] for x in su]

def suffix_array_advanced(s: str) -> List[int]:
    return suffix_array_intermediate(s)

# Edge Cases:
# - Single character strings
# - All same characters
# - Non-alphabetical characters (needs mapping adjustment)

# Interview Challenge:
# Problem: How to find the longest repeated substring?
# Solution: Construct Suffix Array and LCP Array. The maximum value in LCP array gives the answer.

def test_suffix_array():
    # 'banana' -> a, ana, anana, banana, na, nana
    assert suffix_array_basic("banana") == [5, 3, 1, 0, 4, 2]
    assert suffix_array_intermediate("banana") == [5, 3, 1, 0, 4, 2]
    print("All Suffix Array tests passed!")

if __name__ == "__main__":
    test_suffix_array()
