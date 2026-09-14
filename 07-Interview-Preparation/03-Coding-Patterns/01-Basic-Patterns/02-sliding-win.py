"""
# ==============================================================================
# LABORATORY: INTERVIEW PREPARATION (CODING PATTERNS - SLIDING WINDOW)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Interviewer: "Given an array, find the maximum sum of any contiguous subarray 
# of size K."
#
# If you write a nested loop that recalculates the sum of every K-sized block 
# from scratch, you write an O(N*K) algorithm. If N is 1 Million and K is 500,000, 
# your algorithm will execute 500 Billion operations and crash the server.
#
# A senior engineer recognizes the mathematical overlap. When moving a window of 
# size K one step to the right, you do NOT recalculate the middle items. You 
# mathematically SUBTRACT the item that fell out of the left side, and mathematically 
# ADD the new item that entered the right side. This transforms O(N*K) into 
# a lightning-fast O(N) algorithm!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master Fixed-Size Sliding Windows (Max Sum Subarray of Size K).
# - Master Dynamically Sized Sliding Windows (Longest Substring without Repeating).
# - Understand how to track window state using Hash Maps.
#
# ==============================================================================
"""

from typing import List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. FIXED-SIZE SLIDING WINDOW
# ==============================================================================
def max_subarray_sum(nums: List[int], k: int) -> int:
    """
    Time: O(N) | Space: O(1)
    Find the maximum sum of any contiguous subarray of size K.
    """
    if len(nums) < k: return -1
    
    # 1. Initialize the very first window mathematically
    window_sum = sum(nums[:k])
    max_sum = window_sum
    
    print(f"  Initial Window [0 to {k-1}]: Sum = {window_sum}")
    
    # 2. Slide the window one step at a time!
    for i in range(len(nums) - k):
        # The math: (Old Sum) - (Leaving Element) + (Entering Element)
        leaving_element = nums[i]
        entering_element = nums[i + k]
        
        window_sum = window_sum - leaving_element + entering_element
        print(f"  Sliding: -({leaving_element}) +({entering_element}) -> New Sum = {window_sum}")
        
        max_sum = max(max_sum, window_sum)
        
    return max_sum

def demonstrate_fixed_window():
    section_header("Fixed-Size Sliding Window")
    nums = [2, 1, 5, 1, 3, 2]
    k = 3
    print(f"Array: {nums} | K: {k}\n")
    
    result = max_subarray_sum(nums, k)
    print(f"\nResult: Maximum Sum = {result}")


# ==============================================================================
# 4. DYNAMIC-SIZE SLIDING WINDOW (THE INCHWORM PATTERN)
# ==============================================================================
def longest_substring_without_repeats(s: str) -> int:
    """
    Time: O(N) | Space: O(K) where K is the alphabet size
    Given a string, find the length of the longest substring without repeating characters.
    """
    char_index_map = {}
    left = 0
    max_len = 0
    
    print(f"  String: '{s}'")
    
    # The 'right' pointer strictly expands the window
    for right, char in enumerate(s):
        # If we have seen this character BEFORE, and it is currently INSIDE our window...
        if char in char_index_map and char_index_map[char] >= left:
            print(f"    [COLLISION!] Saw '{char}' again at idx {right}. It was previously at idx {char_index_map[char]}.")
            print(f"    -> Mathematically shrinking window by violently teleporting LEFT pointer.")
            # Teleport the left pointer to EXACTLY one step past the old duplicate!
            left = char_index_map[char] + 1
            
        # Update the memory of where we last saw this character
        char_index_map[char] = right
        
        # Calculate current window size mathematically
        current_len = (right - left) + 1
        print(f"  Window: '{s[left:right+1]}' (Len: {current_len})")
        
        max_len = max(max_len, current_len)
        
    return max_len

def demonstrate_dynamic_window():
    section_header("Dynamic Sliding Window (Inchworm)")
    s = "abcabcbb"
    
    result = longest_substring_without_repeats(s)
    print(f"\nResult: Maximum Length = {result}")


def run_all_labs():
    demonstrate_fixed_window()
    demonstrate_dynamic_window()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "Why does the Fixed-Size Sliding Window optimize algorithmic complexity from $O(N \\times K)$ down to $O(N)$?"
   Senior Answer: "If you calculate the sum of a K-sized block from scratch, you perform $K-1$ additions. When you move the block one index to the right, the new block mathematically shares $K-1$ elements with the old block! A naive nested loop completely ignores this overlapping physical memory and re-adds everything, taking $O(N \\times K)$ total time. The Sliding Window algorithm leverages this overlap by recognizing that the transition between states is purely a mathematical Delta: `New_Sum = Old_Sum - Oldest_Item + Newest_Item`. This reduces the transition down to exactly two $O(1)$ arithmetic operations, achieving perfect $O(N)$ global complexity."

2. Interviewer: "In the Longest Substring Without Repeating Characters algorithm, why do we use a Hash Map instead of just sliding the left pointer one step at a time when we hit a collision?"
   Senior Answer: "If the string is `abcdefghXijX`, and the Right pointer hits the second `X`, the Left pointer is currently at `a`. If we just slide the Left pointer forward one step at a time (e.g., `a`, then `b`, then `c`) checking if the substring is valid, we waste massive amounts of CPU cycles. We *mathematically know* that the collision is caused specifically by the first `X`. Therefore, we use a Hash Map to store the exact integer index of the first `X`, and we violently 'teleport' the Left pointer to the index immediately *after* the first `X` in a single $O(1)$ operation, completely bypassing all intermediate states."

3. Interviewer: "What are the visual clues in a LeetCode problem that scream 'Dynamic Sliding Window'?"
   Senior Answer: "The critical clues are: (1) The problem asks for a 'Subarray' or 'Substring' (contiguous memory), NOT a 'Subsequence' (non-contiguous). (2) It asks for optimization: 'Longest', 'Shortest', or 'Maximum/Minimum'. (3) It provides a dynamic mathematical condition that must be maintained (e.g., 'Sum is exactly equal to K' or 'Contains exactly 2 distinct characters'). The moment you see 'Longest Contiguous...', your brain should instantly snap to the Dynamic Inchworm pattern."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Interview Prep (Sliding Window) Completed.")
