"""
# ==============================================================================
# LABORATORY: COMPETITIVE PROGRAMMING (TWO POINTERS)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You are given a sorted array of 1,000,000 integers. You need to find two 
# numbers that add up to exactly 500,000.
#
# A junior developer will write a nested `for` loop:
# for i in array:
#     for j in array:
#         if i + j == target: return
#
# This is an O(N^2) algorithm. For 1,000,000 elements, it requires 
# 1 Trillion operations. The server will freeze and time out.
#
# An expert developer will use the Two Pointers Technique. By placing one 
# pointer at the Start of the array, and one at the End, you can logically 
# squeeze them together based on the sum. This solves the problem in a single 
# pass: O(N) Time Complexity. 1 Trillion operations drops to 1 Million operations!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the architectural pattern of Two Pointers.
# - Implement Two Sum II (Sorted Array).
# - Implement Valid Palindrome string checking.
# - Implement Container With Most Water (Greedy Optimization).
#
# ==============================================================================
"""

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. TWO SUM II (SORTED ARRAY)
# ==============================================================================
def two_sum_sorted(numbers: list[int], target: int) -> list[int]:
    """
    Finds two numbers in a SORTED array that add up to the target.
    Returns their 1-indexed positions.
    Time Complexity: O(N), Space Complexity: O(1).
    """
    # Initialize the Two Pointers
    left = 0
    right = len(numbers) - 1
    
    # We must not overlap the pointers. We squeeze them together.
    while left < right:
        current_sum = numbers[left] + numbers[right]
        
        if current_sum == target:
            # Found it! Return 1-indexed positions as per standard LeetCode rules.
            return [left + 1, right + 1]
            
        elif current_sum > target:
            # The sum is TOO BIG. Because the array is sorted, the only way 
            # to make the sum smaller is to move the Right pointer to the left!
            right -= 1
            
        else:
            # The sum is TOO SMALL. The only way to increase the sum is to 
            # move the Left pointer to the right!
            left += 1
            
    return []

def demonstrate_two_sum():
    section_header("Two Sum II (O(N) Optimization)")
    
    arr = [2, 7, 11, 15, 20, 25, 30]
    target = 35
    
    print(f"Array : {arr}")
    print(f"Target: {target}")
    
    result = two_sum_sorted(arr, target)
    print(f"Result (1-indexed indices): {result}")
    if result:
        print(f"Verification: {arr[result[0]-1]} + {arr[result[1]-1]} == {target}")


# ==============================================================================
# 4. VALID PALINDROME
# ==============================================================================
def is_palindrome(s: str) -> bool:
    """
    Checks if a string is a palindrome, ignoring non-alphanumeric characters.
    Time Complexity: O(N), Space Complexity: O(1).
    """
    left = 0
    right = len(s) - 1
    
    while left < right:
        # Skip non-alphanumeric characters from the left
        while left < right and not s[left].isalnum():
            left += 1
            
        # Skip non-alphanumeric characters from the right
        while left < right and not s[right].isalnum():
            right -= 1
            
        # Compare the characters (case-insensitive)
        if s[left].lower() != s[right].lower():
            return False
            
        # Move pointers inward
        left += 1
        right -= 1
        
    return True

def demonstrate_palindrome():
    section_header("Valid Palindrome (Two Pointers on Strings)")
    
    test_str = "A man, a plan, a canal: Panama"
    print(f"String: '{test_str}'")
    
    # We could do string slicing: cleaned = ''.join(c.lower() for c in s if c.isalnum())
    # and check cleaned == cleaned[::-1]. 
    # But that creates massive strings in memory (Space Complexity O(N)).
    # The Two Pointer approach uses exactly O(1) Space!
    
    is_pal = is_palindrome(test_str)
    print(f"Is Palindrome? {is_pal}")


# ==============================================================================
# 5. CONTAINER WITH MOST WATER (GREEDY APPROACH)
# ==============================================================================
def max_area(heights: list[int]) -> int:
    """
    Given an array of wall heights, find two walls that together with the 
    x-axis form a container that holds the most water.
    Time Complexity: O(N), Space Complexity: O(1).
    """
    left = 0
    right = len(heights) - 1
    max_water = 0
    
    while left < right:
        # The water height is bottlenecked by the SHORTEST wall.
        current_height = min(heights[left], heights[right])
        
        # The width is the distance between the two pointers.
        width = right - left
        
        # Calculate current volume
        current_water = current_height * width
        
        # Keep track of the absolute maximum volume seen so far
        max_water = max(max_water, current_water)
        
        # Greedy Choice: We want to maximize height. 
        # So we abandon the SHORTER wall and move that pointer inward, 
        # hoping to find a taller wall!
        if heights[left] < heights[right]:
            left += 1
        else:
            right -= 1
            
    return max_water

def demonstrate_container():
    section_header("Container With Most Water")
    
    heights = [1, 8, 6, 2, 5, 4, 8, 3, 7]
    print(f"Wall Heights: {heights}")
    
    max_vol = max_area(heights)
    print(f"Maximum Water Volume: {max_vol}")


def run_all_labs():
    demonstrate_two_sum()
    demonstrate_palindrome()
    demonstrate_container()


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. In the "Two Sum II (Sorted)" problem, why must the array be sorted for the Two Pointers algorithm to work?
   Answer: The algorithm relies entirely on monotonic logic. If the `current_sum` is greater than the `target`, the algorithm mathematically guarantees it can reduce the sum by moving the `right` pointer to the left. If the array was unsorted, moving the `right` pointer to the left might randomly increase OR decrease the sum, destroying the logical invariant and causing the algorithm to fail. (For unsorted arrays, you must use a Hash Map instead, which requires $O(N)$ Space).

2. Why is the Two Pointer Palindrome check superior to simply doing `s == s[::-1]` in Python?
   Answer: Space Complexity and Memory Allocation. `s[::-1]` is a Python slicing operation that creates a complete, physical copy of the string in reverse order in RAM. If the string is 1 Gigabyte long, `s[::-1]` will allocate another 1 Gigabyte of RAM (Space Complexity $O(N)$) and could crash the system. The Two Pointer approach simply uses two integer indexes (left and right). It requires absolutely zero new memory allocation, executing with mathematically perfect $O(1)$ Space Complexity regardless of the string's length.

3. In "Container With Most Water", why do we always move the pointer pointing to the shorter line?
   Answer: The volume of water is determined by `Width * min(Height_Left, Height_Right)`. At any given step, moving a pointer inward *always* decreases the Width by 1. The only mathematical way to compensate for the lost Width and achieve a higher volume is to increase the Height. Since the volume is completely bottlenecked by the *shorter* wall, moving the pointer of the *taller* wall is useless; the volume will still be restricted by the shorter wall. We greedily discard the shorter wall, hoping the next wall we evaluate is taller.
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Competitive Programming (Two Pointers) Completed.")
