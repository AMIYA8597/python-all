"""
Adobe Specific Interview Preparation Module.

Learning Objectives:
- Master foundational algorithms like string manipulation, Linked Lists, and Two Sum.
- Practice dynamic programming for Longest Palindromic Substring.
- Optimize simple approaches to acceptable O(N) or O(N log N) bounds.

Concept Explanation:
Adobe interviews assess strong fundamentals in data structures (Trees, Linked Lists, Hash Maps, Strings). Problems often feature edge cases with large data structures and necessitate well-optimized dynamic programming or pointer-based solutions.
"""
from typing import List, Optional

# Basic Implementation: Two Sum
def two_sum(nums: List[int], target: int) -> List[int]:
    """
    Basic level: Find indices of two numbers that add up to target.
    Uses Hash Map for O(N) time complexity.
    """
    num_map = {}
    for i, num in enumerate(nums):
        diff = target - num
        if diff in num_map:
            return [num_map[diff], i]
        num_map[num] = i
    return []

# Intermediate Implementation: Add Two Numbers (Linked Lists)
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def add_two_numbers(l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
    """
    Intermediate level: Add two numbers represented by linked lists.
    """
    dummy = ListNode(0)
    current = dummy
    carry = 0
    
    while l1 or l2 or carry:
        val1 = l1.val if l1 else 0
        val2 = l2.val if l2 else 0
        
        total = val1 + val2 + carry
        carry = total // 10
        current.next = ListNode(total % 10)
        
        current = current.next
        if l1: l1 = l1.next
        if l2: l2 = l2.next
        
    return dummy.next

# Advanced Implementation: Longest Palindromic Substring
def longest_palindrome(s: str) -> str:
    """
    Advanced level: Longest Palindromic Substring using Expand Around Center.
    
    Performance Analysis:
    - Time Complexity: O(N^2) where N is length of string.
    - Space Complexity: O(1) beyond the returned string.
    """
    if len(s) < 2:
        return s
        
    def expand_around_center(left: int, right: int) -> str:
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1
        return s[left + 1:right]

    longest = ""
    for i in range(len(s)):
        # Odd length palindromes
        odd = expand_around_center(i, i)
        # Even length palindromes
        even = expand_around_center(i, i + 1)
        
        longest = max(longest, odd, even, key=len)
        
    return longest

def run_tests():
    print("Testing Two Sum...")
    assert two_sum([2, 7, 11, 15], 9) == [0, 1]
    
    print("Testing Add Two Numbers...")
    l1 = ListNode(2, ListNode(4, ListNode(3)))
    l2 = ListNode(5, ListNode(6, ListNode(4)))
    res = add_two_numbers(l1, l2)
    assert res.val == 7 and res.next.val == 0 and res.next.next.val == 8
    
    print("Testing Longest Palindromic Substring...")
    assert longest_palindrome("babad") in ["bab", "aba"]
    assert longest_palindrome("cbbd") == "bb"
    
    print("All tests passed!")

if __name__ == "__main__":
    run_tests()
