"""
String Easy Problem Set

Learning Objectives:
1. Master string manipulation in Python.
2. Understand string immutability and its implications on performance.
3. Practice common string patterns: two pointers, frequency counting.

Concepts Explained:
- Strings in Python are immutable, meaning any modification creates a new string.
- Common patterns:
  * Two pointers (from ends moving towards center for palindromes).
  * Character counting (hash maps or arrays of size 26 for anagrams).
"""

from typing import List
import time

def is_palindrome(s: str) -> bool:
    """
    A phrase is a palindrome if, after converting all uppercase letters into lowercase letters 
    and removing all non-alphanumeric characters, it reads the same forward and backward.
    """
    left, right = 0, len(s) - 1
    
    while left < right:
        while left < right and not s[left].isalnum():
            left += 1
        while left < right and not s[right].isalnum():
            right -= 1
            
        if s[left].lower() != s[right].lower():
            return False
            
        left += 1
        right -= 1
        
    return True

def is_anagram(s: str, t: str) -> bool:
    """
    Given two strings s and t, return true if t is an anagram of s, and false otherwise.
    """
    if len(s) != len(t):
        return False
        
    count = {}
    for char in s:
        count[char] = count.get(char, 0) + 1
        
    for char in t:
        if char not in count or count[char] == 0:
            return False
        count[char] -= 1
        
    return True

def longest_common_prefix(strs: List[str]) -> str:
    """
    Write a function to find the longest common prefix string amongst an array of strings.
    If there is no common prefix, return an empty string "".
    """
    if not strs:
        return ""
        
    prefix = strs[0]
    for i in range(1, len(strs)):
        while strs[i].find(prefix) != 0:
            prefix = prefix[:-1]
            if not prefix:
                return ""
    return prefix

def performance_analysis():
    print("Performance Analysis for Valid Palindrome:")
    s = "A man, a plan, a canal: Panama" * 1000
    start = time.time()
    is_palindrome(s)
    print(f"Time taken: {time.time() - start:.6f} seconds")

# Interview Challenge: Reverse a string in-place (if it were an array of characters)
def reverse_string(s: List[str]) -> None:
    """
    Do not return anything, modify s in-place instead.
    """
    left, right = 0, len(s) - 1
    while left < right:
        s[left], s[right] = s[right], s[left]
        left += 1
        right -= 1

def test_string_easy():
    print("Testing Is Palindrome...")
    assert is_palindrome("A man, a plan, a canal: Panama") is True
    assert is_palindrome("race a car") is False
    
    print("Testing Is Anagram...")
    assert is_anagram("anagram", "nagaram") is True
    assert is_anagram("rat", "car") is False
    
    print("Testing Longest Common Prefix...")
    assert longest_common_prefix(["flower", "flow", "flight"]) == "fl"
    assert longest_common_prefix(["dog", "racecar", "car"]) == ""
    
    print("Testing Reverse String...")
    s = ["h","e","l","l","o"]
    reverse_string(s)
    assert s == ["o","l","l","e","h"]
    
    print("All tests passed!")

if __name__ == "__main__":
    test_string_easy()
    performance_analysis()
