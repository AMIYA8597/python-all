"""
# ==============================================================================
# LABORATORY: COMPETITIVE PROGRAMMING (CONTEST PRACTICE: EASY)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# "Easy" problems on LeetCode or Codeforces Div-4 are not about writing complex 
# Segment Trees. They are about executing fundamental Data Structures flawlessly 
# under severe time pressure.
# 
# An amateur solves "Two Sum" in 10 minutes using a double `for` loop, resulting 
# in O(N^2) time, which fails the hidden test cases.
# 
# A professional solves "Two Sum" in 30 seconds using a Hash Map, achieving 
# O(N) time and O(N) space, instantly moving on to the Hard problems.
#
# This laboratory covers the 3 absolute foundational pillars of Easy problems:
# 1. Hashing (Trading Space for Time)
# 2. The Stack (LIFO Parsing)
# 3. Two Pointers (In-Place Array Manipulation)
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master the Hash Map complement technique.
# - Master Valid Parentheses using a Stack.
# - Master merging arrays in-place from back-to-front.
#
# ==============================================================================
"""

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE HASH MAP COMPLEMENT (TWO SUM)
# ==============================================================================
def two_sum(nums: list[int], target: int) -> list[int]:
    """
    Problem: Find the indices of two numbers that add up to the target.
    Time Complexity: O(N) - One single pass.
    Space Complexity: O(N) - Worst case, we store N-1 elements in the dictionary.
    """
    # Dictionary mapping: `value` -> `index_in_array`
    seen = {}
    
    for i, num in enumerate(nums):
        # The mathematical Complement: What number do we desperately need 
        # to mathematically reach the target?
        complement = target - num
        
        # Does this exact complement already exist in our history?
        if complement in seen:
            # We found the pair! Return their indices.
            return [seen[complement], i]
            
        # We did not find it. Add the current number to our history so 
        # future numbers can potentially use it!
        seen[num] = i
        
    return []

def demonstrate_two_sum():
    section_header("Hashing (Two Sum)")
    
    nums = [2, 7, 11, 15]
    target = 9
    
    print(f"Array: {nums}, Target: {target}")
    
    ans = two_sum(nums, target)
    print(f"Indices: {ans}")
    print("Why? nums[0] + nums[1] = 2 + 7 = 9.")
    print("We used a Hash Map to look backwards in time in strict O(1) time!")


# ==============================================================================
# 4. THE STACK (VALID PARENTHESES)
# ==============================================================================
def is_valid_parentheses(s: str) -> bool:
    """
    Problem: Determine if a string of brackets is validly closed.
    Time Complexity: O(N)
    Space Complexity: O(N)
    """
    stack = []
    
    # Map every closing bracket to its strict required opening bracket.
    matching_bracket = {
        ')': '(',
        ']': '[',
        '}': '{'
    }
    
    for char in s:
        # If it is a CLOSING bracket...
        if char in matching_bracket:
            # Pop the top of the stack (if the stack is not empty).
            # If the stack is empty, we assign a dummy value '#' which will 
            # mathematically force a failure.
            top_element = stack.pop() if stack else '#'
            
            # Does the popped opening bracket perfectly match the required bracket?
            if matching_bracket[char] != top_element:
                return False
        else:
            # It is an OPENING bracket. Push it onto the stack!
            stack.append(char)
            
    # If the string was perfectly valid, the stack must be completely empty!
    # If len(stack) > 0, it means there are unclosed opening brackets left over.
    return not stack

def demonstrate_valid_parentheses():
    section_header("The Stack (Valid Parentheses)")
    
    valid_str = "()[]{}"
    invalid_str = "([)]"
    
    print(f"Is '{valid_str}' valid? {is_valid_parentheses(valid_str)}")
    print(f"Is '{invalid_str}' valid? {is_valid_parentheses(invalid_str)}")
    
    print("\nThe Stack perfectly enforces LIFO (Last-In, First-Out), which is ")
    print("the exact mathematical requirement for nested string structures.")


# ==============================================================================
# 5. TWO POINTERS (MERGE SORTED ARRAYS IN-PLACE)
# ==============================================================================
def merge_sorted_arrays(nums1: list[int], m: int, nums2: list[int], n: int) -> None:
    """
    Problem: Merge two sorted arrays. `nums1` has enough empty space (0s) at 
    the end to hold both arrays. You must merge them IN-PLACE.
    
    Time Complexity: O(N + M)
    Space Complexity: O(1) Absolute constant space!
    """
    # Initialize 3 Pointers:
    # p1 points to the end of the actual data in nums1.
    p1 = m - 1
    # p2 points to the end of nums2.
    p2 = n - 1
    # p_write points to the absolute end of the empty space in nums1!
    p_write = m + n - 1
    
    # We iterate BACKWARDS. Why? Because the back of nums1 is empty! 
    # If we iterate forwards, we will mathematically overwrite data we haven't 
    # processed yet, completely corrupting the array.
    while p1 >= 0 and p2 >= 0:
        if nums1[p1] > nums2[p2]:
            nums1[p_write] = nums1[p1]
            p1 -= 1
        else:
            nums1[p_write] = nums2[p2]
            p2 -= 1
        p_write -= 1
        
    # Edge Case: What if p1 runs out first, but p2 still has elements?
    # We must copy the remaining elements of nums2 into nums1!
    # (If p2 runs out first, we do nothing, because the remaining elements in 
    # nums1 are ALREADY in their correct sorted position!)
    while p2 >= 0:
        nums1[p_write] = nums2[p2]
        p2 -= 1
        p_write -= 1

def demonstrate_merge():
    section_header("Two Pointers (Merge Arrays In-Place)")
    
    # nums1 has 3 elements, and 3 trailing zeros for the merge space.
    nums1 = [1, 2, 3, 0, 0, 0]
    m = 3
    nums2 = [2, 5, 6]
    n = 3
    
    print(f"nums1 Data: {nums1[:m]} + Empty Space")
    print(f"nums2 Data: {nums2}")
    
    merge_sorted_arrays(nums1, m, nums2, n)
    
    print(f"\nMerged Array (In-Place): {nums1}")
    print("Writing from back-to-front prevents mathematically overwriting our own data!")


def run_all_labs():
    demonstrate_two_sum()
    demonstrate_valid_parentheses()
    demonstrate_merge()


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. In the Two Sum problem, why is storing elements in a Hash Map as you iterate strictly superior to pre-loading the entire array into the Hash Map first?
   Answer: Pre-loading the entire array requires a full $O(N)$ pass, followed by a second $O(N)$ pass to check complements. Worse, if the target is `6` and the array has a single `3`, pre-loading would place `3` in the map. When the loop encounters the `3`, it checks the map for `6 - 3 = 3`, finds it, and erroneously returns the same index twice! By storing elements *dynamically* as you iterate, you mathematically guarantee that when you are evaluating index $i$, the map ONLY contains elements from index $0$ to $i-1$. This makes it physically impossible to pair an element with itself, and successfully completes the algorithm in a single pass.

2. In the Valid Parentheses problem, why does the Stack (LIFO) perfectly model the mathematical rules of nested brackets?
   Answer: In nested logic, the most recently opened bracket MUST be the absolute first bracket to be closed. For example, in `([{}])`, the `{` is the last one opened, so it must be the first one closed. A Stack enforces Last-In, First-Out. When we push `(`, `[`, `{` onto the stack, the `{` is sitting exactly at the top. When we encounter the first closing bracket `}`, we simply `pop()` the top of the stack. If it perfectly matches, we discarded the innermost layer. We then repeat for `]` and `)`. If we used a Queue (FIFO), it would demand that the outermost bracket `(` be closed first, which is a catastrophic violation of nested string rules.

3. When merging sorted arrays in-place into `nums1`, why does writing from Back-to-Front mathematically prevent data corruption?
   Answer: `nums1` is constructed with exactly enough trailing zeros at the end to accommodate `nums2`. For example, `m=3`, `n=3`, total size = 6. The last 3 indices (3, 4, 5) are physically empty. The write pointer starts at index 5. The absolute largest elements of both arrays are being evaluated and written to the empty space at the end. Because the read pointers (`p1` and `p2`) start at index 2, and the write pointer starts at index 5, the write pointer is mathematically 3 steps ahead of the `nums1` read pointer! It is geometrically impossible for the write pointer to ever "catch up" to the read pointer and overwrite unprocessed data. If you iterate forward, the write pointer starts at 0, immediately colliding with your data!
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Contest Practice (Easy) Completed.")
