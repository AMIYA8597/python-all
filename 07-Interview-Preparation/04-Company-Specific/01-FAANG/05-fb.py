"""
Module: Meta/Facebook Interview Questions (Python)

Learning Objectives:
- Master prefix sums and hash maps for array processing.
- Understand string palindromes and two-pointer techniques.

Concept Explanation:
Meta loves prefix sums (Subarray Sum Equals K), two pointers (Valid Palindrome II), and greedy approaches. Code needs to be bug-free as interviews emphasize speed and correctness.

Performance Analysis:
- Subarray Sum Equals K: Time O(N), Space O(N) using hash map.
- Valid Palindrome II: Time O(N), Space O(1).
"""

from typing import List
import collections

# Basic/Intermediate: Valid Palindrome II (Two Pointers)
def valid_palindrome(s: str) -> bool:
    """
    Given a string s, return true if the s can be palindrome after deleting at most one character from it.
    """
    def check_palindrome(left: int, right: int) -> bool:
        while left < right:
            if s[left] != s[right]:
                return False
            left += 1
            right -= 1
        return True

    l, r = 0, len(s) - 1
    while l < r:
        if s[l] != s[r]:
            # Try skipping left OR skipping right
            return check_palindrome(l + 1, r) or check_palindrome(l, r - 1)
        l += 1
        r -= 1
        
    return True

# Advanced: Subarray Sum Equals K (Prefix Sum + Hash Map)
def subarray_sum(nums: List[int], k: int) -> int:
    """
    Given an array of integers nums and an integer k, return the total number of subarrays whose sum equals to k.
    """
    count = 0
    curr_sum = 0
    prefix_sums = collections.defaultdict(int)
    prefix_sums[0] = 1
    
    for num in nums:
        curr_sum += num
        # If curr_sum - k exists in hash map, we found valid subarrays
        if (curr_sum - k) in prefix_sums:
            count += prefix_sums[curr_sum - k]
        prefix_sums[curr_sum] += 1
        
    return count


def test_fb_questions():
    print("Testing Valid Palindrome II...")
    assert valid_palindrome("aba") is True
    assert valid_palindrome("abca") is True
    assert valid_palindrome("abc") is False
    print("Passed.")

    print("Testing Subarray Sum Equals K...")
    assert subarray_sum([1,1,1], 2) == 2
    assert subarray_sum([1,2,3], 3) == 2
    print("Passed.")

if __name__ == "__main__":
    test_fb_questions()
    print("All Meta/Facebook interview tests passed!")
