"""
Medium String Problems

This module covers core medium-level String interview questions. Strings in Python are immutable,
meaning every modification creates a new string. Therefore, optimal solutions typically avoid 
repetitive string concatenation and leverage indexing, hash maps, or the Sliding Window technique.

Beginner Explanation:
When working with strings, you often need to parse, search, or group characters. Techniques like
Sliding Window allow you to parse substrings efficiently without checking every possible combination,
bringing O(N^2) operations down to O(N).

Advanced Technical Explanation:
At scale, processing massive strings or streams of text (like NLP tokenization or log parsing) requires
memory efficiency. Hash maps (dictionaries) provide O(1) character lookups, but fixed-size arrays 
(e.g., size 256 for ASCII) can be slightly faster due to lack of hashing overhead. When dynamic programming
is applied to strings (e.g., palindromes), memory optimization through state reduction is critical.

Topics Covered:
1. Sliding Window (Longest Substring Without Repeating Characters)
2. Expand Around Center (Longest Palindromic Substring)
3. Hash Mapping / Sorting (Group Anagrams)
"""

from typing import List, Dict
import collections

# ==============================================================================
# Problem 1: Longest Substring Without Repeating Characters
# ==============================================================================
"""
Industry Use Case:
Stream processing and network packet validation often require identifying unique sequences 
within sliding windows.

Description:
Given a string s, find the length of the longest substring without repeating characters.
"""

def length_of_longest_substring(s: str) -> int:
    """
    Finds the length of the longest substring without repeating characters.
    
    Args:
        s (str): The input string.
        
    Returns:
        int: Length of the longest valid substring.
    """
    char_index_map = {}
    max_length = 0
    left = 0
    
    for right in range(len(s)):
        # If the character is already in the map and is inside the current window
        if s[right] in char_index_map and char_index_map[s[right]] >= left:
            # Move the left pointer to the right of the previous occurrence
            left = char_index_map[s[right]] + 1
            
        # Update the latest index of the character
        char_index_map[s[right]] = right
        
        # Update max length found so far
        max_length = max(max_length, right - left + 1)
        
    return max_length

# ==============================================================================
# Problem 2: Longest Palindromic Substring
# ==============================================================================
"""
Industry Use Case:
Palindromic properties are used in computational biology (DNA sequence analysis) and
advanced string matching algorithms (like Manacher's Algorithm).

Description:
Given a string s, return the longest palindromic substring in s.
"""

def longest_palindrome(s: str) -> str:
    """
    Finds the longest palindromic substring using the expand around center approach.
    
    Args:
        s (str): The input string.
        
    Returns:
        str: The longest palindromic substring.
    """
    if not s or len(s) < 2:
        return s

    def expand_around_center(left: int, right: int) -> str:
        """Helper to expand outwards and find valid palindromes."""
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1
        return s[left + 1:right]

    longest = ""
    for i in range(len(s)):
        # Odd length palindrome center
        odd_pal = expand_around_center(i, i)
        if len(odd_pal) > len(longest):
            longest = odd_pal
            
        # Even length palindrome center
        even_pal = expand_around_center(i, i + 1)
        if len(even_pal) > len(longest):
            longest = even_pal
            
    return longest

# ==============================================================================
# Problem 3: Group Anagrams
# ==============================================================================
"""
Industry Use Case:
Anagram grouping maps to document clustering, search engine query normalization, and
cryptography (frequency analysis mapping).

Description:
Given an array of strings strs, group the anagrams together. You can return the answer in any order.
"""

def group_anagrams(strs: List[str]) -> List[List[str]]:
    """
    Groups anagrams using character count tuples as dictionary keys.
    
    Args:
        strs (List[str]): List of strings to group.
        
    Returns:
        List[List[str]]: Grouped anagrams.
    """
    # Using a defaultdict to automatically handle new keys
    anagram_map: Dict[tuple, List[str]] = collections.defaultdict(list)
    
    for word in strs:
        # Create a frequency array for the 26 lowercase English letters
        count = [0] * 26
        for char in word:
            count[ord(char) - ord('a')] += 1
            
        # Tuples are immutable and can be used as dict keys in Python
        anagram_map[tuple(count)].append(word)
        
    return list(anagram_map.values())

# ==============================================================================
# Tests
# ==============================================================================

def run_tests():
    """Executes tests for medium string problems."""
    # Test Longest Substring Without Repeating Characters
    assert length_of_longest_substring("abcabcbb") == 3
    assert length_of_longest_substring("bbbbb") == 1
    assert length_of_longest_substring("pwwkew") == 3
    
    # Test Longest Palindromic Substring
    assert longest_palindrome("babad") in ["bab", "aba"]
    assert longest_palindrome("cbbd") == "bb"
    
    # Test Group Anagrams
    ga_result = group_anagrams(["eat","tea","tan","ate","nat","bat"])
    # Sort inner lists and outer list for reliable comparison
    ga_result_sorted = sorted([sorted(group) for group in ga_result])
    expected = sorted([sorted(["eat","tea","ate"]), sorted(["tan","nat"]), sorted(["bat"])])
    assert ga_result_sorted == expected
    
    print("All Medium String tests passed successfully!")

if __name__ == "__main__":
    run_tests()
