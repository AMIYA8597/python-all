"""
LeetCode Easy Problems for Competitive Programming
================================================

This module covers selected "Easy" level algorithmic problems commonly found on platforms
like LeetCode, HackerRank, and Codeforces.

Learning Objectives:
1. Master fundamental problem-solving techniques like Two Pointers, Hashing, and basic string/array manipulation.
2. Develop the habit of writing optimal solutions (O(N) instead of O(N^2)) even for easy problems.
3. Write clean, readable, and type-hinted code.

Concept Explanation:
"Easy" problems typically require a straightforward application of a single fundamental data structure 
or algorithm. However, they are essential for building speed and recognizing patterns. Often, the naive 
solution is O(N^2), but the optimal one relies on a hash map or two pointers to achieve O(N) time.

Basic vs Professional Implementation:
A basic implementation of Two Sum uses nested loops (O(N^2)). 
A professional implementation uses a Hash Map (O(N)), utilizes early returns, type hints, and 
handles edge cases correctly.

Use Cases:
- Phone screening interviews.
- Warm-up problems in competitive programming contests.
- Building blocks for more complex algorithms.

"""

from typing import List, Optional

def two_sum(nums: List[int], target: int) -> List[int]:
    """
    Finds two numbers in the array that add up to the target.
    
    Approach:
    Uses a hash map to store the elements and their indices as we iterate.
    For each element `num`, we check if `target - num` exists in the map.
    
    Time Complexity: O(N) where N is the number of elements.
    Space Complexity: O(N) for the hash map.
    
    Args:
        nums: List of integers.
        target: The target sum.
        
    Returns:
        A list containing the indices of the two numbers.
        Returns an empty list if no such pair exists.
    """
    num_map = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in num_map:
            return [num_map[complement], i]
        num_map[num] = i
    return []

def max_profit(prices: List[int]) -> int:
    """
    Calculates the maximum profit from buying and selling a stock once.
    
    Approach:
    Maintain the minimum price seen so far and update the maximum profit 
    at each step if selling at the current price yields a better profit.
    
    Time Complexity: O(N)
    Space Complexity: O(1)
    
    Args:
        prices: List of daily stock prices.
        
    Returns:
        Maximum profit achievable, or 0 if no profit can be made.
    """
    if not prices:
        return 0
        
    min_price = float('inf')
    max_profit_val = 0
    
    for price in prices:
        if price < min_price:
            min_price = price
        elif price - min_price > max_profit_val:
            max_profit_val = price - min_price
            
    return max_profit_val

def is_valid_parentheses(s: str) -> bool:
    """
    Determines if the input string has valid matching parentheses.
    
    Approach:
    Uses a stack. Push opening brackets. When encountering a closing bracket,
    check if it matches the top of the stack.
    
    Time Complexity: O(N)
    Space Complexity: O(N) in the worst case (all opening brackets).
    
    Args:
        s: String consisting of '(', ')', '{', '}', '[' and ']'.
        
    Returns:
        True if the string is valid, False otherwise.
    """
    stack = []
    mapping = {")": "(", "}": "{", "]": "["}
    
    for char in s:
        if char in mapping:
            # Pop the topmost element if stack is not empty, else assign a dummy value
            top_element = stack.pop() if stack else '#'
            if mapping[char] != top_element:
                return False
        else:
            stack.append(char)
            
    return not stack

# ==========================================
# Common Mistakes & Performance Considerations
# ==========================================
# 1. Using `in` operator on a list instead of a set/dict inside a loop leads to O(N^2) complexity.
# 2. Forgetting to handle empty inputs or cases where no valid answer exists.

# ==========================================
# Interview Challenge
# ==========================================
# Can you solve the Two Sum problem if the input array is already sorted, but using O(1) space?
# Hint: Use two pointers (left and right).

if __name__ == "__main__":
    print("Testing Two Sum...")
    assert two_sum([2, 7, 11, 15], 9) == [0, 1]
    assert two_sum([3, 2, 4], 6) == [1, 2]
    print("Two Sum passed.")

    print("Testing Max Profit...")
    assert max_profit([7, 1, 5, 3, 6, 4]) == 5
    assert max_profit([7, 6, 4, 3, 1]) == 0
    print("Max Profit passed.")

    print("Testing Valid Parentheses...")
    assert is_valid_parentheses("()") == True
    assert is_valid_parentheses("()[]{}") == True
    assert is_valid_parentheses("(]") == False
    assert is_valid_parentheses("([)]") == False
    assert is_valid_parentheses("{[]}") == True
    print("Valid Parentheses passed.")
    
    print("\nAll tests passed successfully.")
