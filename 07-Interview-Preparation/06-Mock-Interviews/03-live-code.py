"""
Module: 03-live-code
Learning Objectives:
- Master live coding interview environments.
- Practice thinking aloud and writing clean code.
- Implement robust algorithms with error handling.

This script simulates a live coding environment with a common string manipulation problem:
Longest Substring Without Repeating Characters.
"""

from typing import Dict
import logging

# Set up logging for the live code simulation
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# --- Concept Explanation ---
# In a live coding interview, communication is key.
# The interviewer wants to see your thought process, how you handle bugs, and your coding style.
# The Sliding Window pattern is commonly used for substring/subarray problems.

# --- Implementation ---
def length_of_longest_substring(s: str) -> int:
    """
    Finds the length of the longest substring without repeating characters.
    
    Args:
        s: Input string.
        
    Returns:
        Integer representing the max length.
    """
    char_index_map: Dict[str, int] = {}
    max_len = 0
    start = 0
    
    for end, char in enumerate(s):
        # If the character is already in the map and is within the current window
        if char in char_index_map and char_index_map[char] >= start:
            # Move the start pointer to the right of the previous occurrence
            start = char_index_map[char] + 1
            
        # Update the character's latest index
        char_index_map[char] = end
        
        # Calculate max length so far
        max_len = max(max_len, end - start + 1)
        
    return max_len

# --- Performance Analysis ---
# Time: O(N) where N is the length of the string, since we iterate through the string once.
# Space: O(min(N, M)) where M is the size of the charset (e.g., 26 for lowercase English letters).

# --- Edge Cases ---
# 1. Empty string -> returns 0.
# 2. String with all identical characters (e.g., "aaaa") -> returns 1.
# 3. String with all unique characters -> returns length of string.

# --- Interview Challenge ---
# Challenge: Find the longest substring with at most K distinct characters.

# --- Tests ---
def run_live_tests():
    test_cases = [
        ("abcabcbb", 3),
        ("bbbbb", 1),
        ("pwwkew", 3),
        ("", 0),
        ("a", 1),
        ("dvdf", 3)
    ]
    
    for i, (input_str, expected) in enumerate(test_cases):
        result = length_of_longest_substring(input_str)
        if result == expected:
            logging.info(f"Test {i+1} Passed: '{input_str}' -> {result}")
        else:
            logging.error(f"Test {i+1} Failed: '{input_str}' -> Got {result}, Expected {expected}")
            assert False, f"Test {i+1} failed"

if __name__ == "__main__":
    run_live_tests()
