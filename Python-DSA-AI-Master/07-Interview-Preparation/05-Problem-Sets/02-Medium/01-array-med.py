"""
Medium Array Problems

This module covers core medium-level Array interview questions. Array manipulation is fundamental
to technical interviews because arrays are the building blocks of most data structures and systems.

Beginner Explanation:
Medium array problems usually require moving beyond basic loops. You'll often need to use techniques
like Two Pointers, Hashing, or Prefix Sums to achieve optimal time complexity (usually O(N) or O(N log N)).

Advanced Technical Explanation:
The problems in this module require minimizing time and space complexities. You must avoid naive O(N^2)
solutions by leveraging memory (hash maps) or sorting and pointers. Cache locality is excellent with arrays,
meaning contiguous memory blocks are fast to access; minimizing extra allocations and operating in-place 
wherever possible is a strong signal to interviewers.

Topics Covered:
1. Two Pointers (3Sum, Container With Most Water)
2. Prefix/Suffix Arrays (Product of Array Except Self)
"""

from typing import List

# ==============================================================================
# Problem 1: 3Sum
# ==============================================================================
"""
Industry Use Case:
Finding combinations of factors or balancing risk models often maps to subset sum problems.
3Sum is a classic algorithmic puzzle evaluating a candidate's ability to reduce an O(N^3)
naive approach to O(N^2) using sorting and two pointers.

Common Mistakes:
- Failing to handle duplicate triplets, resulting in a wrong answer or Time Limit Exceeded due to
  hashing overhead.
"""

def three_sum(nums: List[int]) -> List[List[int]]:
    """
    Finds all unique triplets in the array which gives the sum of zero.
    
    Args:
        nums (List[int]): Array of integers.
        
    Returns:
        List[List[int]]: List of triplets that sum to zero.
    """
    res = []
    nums.sort()  # Sorting is crucial for the two-pointer approach and avoiding duplicates
    n = len(nums)

    for i in range(n - 2):
        # Skip duplicate elements for the first number
        if i > 0 and nums[i] == nums[i - 1]:
            continue
            
        left, right = i + 1, n - 1
        
        while left < right:
            total = nums[i] + nums[left] + nums[right]
            
            if total < 0:
                left += 1
            elif total > 0:
                right -= 1
            else:
                res.append([nums[i], nums[left], nums[right]])
                
                # Skip duplicates for the second number
                while left < right and nums[left] == nums[left + 1]:
                    left += 1
                # Skip duplicates for the third number
                while left < right and nums[right] == nums[right - 1]:
                    right -= 1
                    
                left += 1
                right -= 1
                
    return res

# ==============================================================================
# Problem 2: Container With Most Water
# ==============================================================================
"""
Industry Use Case:
Optimization problems where bounded constraints determine maximum yield (like capacity planning).

Description:
Given n non-negative integers representing vertical lines on a graph, find two lines that together
with the x-axis form a container, such that the container contains the most water.
"""

def max_area(height: List[int]) -> int:
    """
    Calculates the maximum area of water a container can store.
    
    Args:
        height (List[int]): Heights of the lines.
        
    Returns:
        int: Maximum area.
    """
    left, right = 0, len(height) - 1
    max_water = 0
    
    while left < right:
        # Area is limited by the shorter line
        current_width = right - left
        current_height = min(height[left], height[right])
        current_area = current_width * current_height
        
        max_water = max(max_water, current_area)
        
        # Move the pointer of the shorter line inward
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1
            
    return max_water

# ==============================================================================
# Problem 3: Product of Array Except Self
# ==============================================================================
"""
Industry Use Case:
Useful in data transformation pipelines where aggregate statistical properties are calculated 
excluding the current data point (e.g., cross-validation models).

Description:
Given an integer array nums, return an array answer such that answer[i] is equal to the product 
of all the elements of nums except nums[i].
Constraint: MUST run in O(n) time and without using the division operation.
"""

def product_except_self(nums: List[int]) -> List[int]:
    """
    Calculates the product of all elements except the element at each index.
    
    Args:
        nums (List[int]): Input array.
        
    Returns:
        List[int]: Output array.
    """
    n = len(nums)
    res = [1] * n
    
    # Calculate prefix products
    prefix = 1
    for i in range(n):
        res[i] = prefix
        prefix *= nums[i]
        
    # Calculate suffix products and multiply with prefix products
    suffix = 1
    for i in range(n - 1, -1, -1):
        res[i] *= suffix
        suffix *= nums[i]
        
    return res

# ==============================================================================
# Tests
# ==============================================================================

def run_tests():
    """Executes tests for medium array problems."""
    # Test 3Sum
    assert three_sum([-1, 0, 1, 2, -1, -4]) == [[-1, -1, 2], [-1, 0, 1]]
    assert three_sum([0, 1, 1]) == []
    assert three_sum([0, 0, 0]) == [[0, 0, 0]]
    
    # Test Container With Most Water
    assert max_area([1,8,6,2,5,4,8,3,7]) == 49
    assert max_area([1,1]) == 1
    
    # Test Product of Array Except Self
    assert product_except_self([1, 2, 3, 4]) == [24, 12, 8, 6]
    assert product_except_self([-1, 1, 0, -3, 3]) == [0, 0, 9, 0, 0]
    
    print("All Medium Array tests passed successfully!")

if __name__ == "__main__":
    run_tests()
