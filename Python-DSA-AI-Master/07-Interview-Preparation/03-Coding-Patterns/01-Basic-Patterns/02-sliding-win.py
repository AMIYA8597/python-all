"""
Sliding Window Pattern - Comprehensive Guide

Learning Objectives:
- Understand the Sliding Window technique and its variants (Fixed vs Dynamic)
- Implement sliding window for subarray/substring problems
- Analyze time and space complexity of sliding window solutions
- Solve common interview challenges like Longest Substring, Max Sum Subarray

Concept Explanation:
The Sliding Window pattern is used to perform operations on a specific window size of a given array or linked list, such as finding the longest subarray containing all 1s. Sliding windows start from the 1st element and keep shifting right by one element and adjust the length of the window according to the problem that you are solving. In some cases, the window size remains constant and in other cases the sizes grows or shrinks.

When to use:
- Problem involves a linear data structure (Array, Linked List, String)
- You are asked to find the longest/shortest substring, subarray, or a desired value
"""

from typing import List
import math

# Basic: Maximum Sum Subarray of Size K (Fixed Window)
def max_sub_array_of_size_k(k: int, arr: List[int]) -> int:
    """
    Given an array of positive numbers and a positive number 'k', 
    find the maximum sum of any contiguous subarray of size 'k'.
    Time Complexity: O(N)
    Space Complexity: O(1)
    """
    max_sum, window_sum = 0, 0
    window_start = 0

    for window_end in range(len(arr)):
        window_sum += arr[window_end]
        if window_end >= k - 1:
            max_sum = max(max_sum, window_sum)
            window_sum -= arr[window_start]
            window_start += 1
            
    return max_sum


# Intermediate: Smallest Subarray with a given sum (Dynamic Window)
def smallest_subarray_with_given_sum(s: int, arr: List[int]) -> int:
    """
    Given an array of positive numbers and a positive number 's', 
    find the length of the smallest contiguous subarray whose sum is greater than or equal to 's'.
    Time Complexity: O(N)
    Space Complexity: O(1)
    """
    window_sum = 0
    min_length = math.inf
    window_start = 0

    for window_end in range(len(arr)):
        window_sum += arr[window_end]
        while window_sum >= s:
            min_length = min(min_length, window_end - window_start + 1)
            window_sum -= arr[window_start]
            window_start += 1
            
    if min_length == math.inf:
        return 0
    return int(min_length)


# Advanced: Longest Substring with K Distinct Characters
def longest_substring_with_k_distinct(str1: str, k: int) -> int:
    """
    Given a string, find the length of the longest substring in it with no more than K distinct characters.
    Time Complexity: O(N)
    Space Complexity: O(K) as we store max K+1 chars
    """
    window_start = 0
    max_length = 0
    char_frequency = {}

    for window_end in range(len(str1)):
        right_char = str1[window_end]
        if right_char not in char_frequency:
            char_frequency[right_char] = 0
        char_frequency[right_char] += 1

        while len(char_frequency) > k:
            left_char = str1[window_start]
            char_frequency[left_char] -= 1
            if char_frequency[left_char] == 0:
                del char_frequency[left_char]
            window_start += 1
            
        max_length = max(max_length, window_end - window_start + 1)
        
    return max_length

def run_tests():
    print("Testing Sliding Window...")
    assert max_sub_array_of_size_k(3, [2, 1, 5, 1, 3, 2]) == 9
    assert smallest_subarray_with_given_sum(7, [2, 1, 5, 2, 3, 2]) == 2
    assert longest_substring_with_k_distinct("araaci", 2) == 4
    print("All tests passed.")

if __name__ == '__main__':
    run_tests()
