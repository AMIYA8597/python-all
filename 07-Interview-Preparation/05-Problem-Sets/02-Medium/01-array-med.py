"""
# ==============================================================================
# LABORATORY: INTERVIEW PREPARATION (PROBLEM SETS - ARRAY MEDIUM)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# "Medium" Array problems are the absolute gold standard of tech interviews. 
# They usually require $O(N)$ or $O(N \\log N)$ time limits and frequently enforce 
# strict $O(1)$ space constraints, instantly failing candidates who rely on 
# allocating extra Hash Maps or Arrays.
#
# A junior engineer solves '3Sum' by using three nested loops ($O(N^3)$), which 
# is an instant failure.
# 
# A senior engineer sorts the array ($O(N \\log N)$) and deploys a Two-Pointer 
# collapsing window for every element, crushing the time complexity to $O(N^2)$ 
# and explicitly bypassing duplicate permutations dynamically.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master the Collapsing Window (3Sum).
# - Master Prefix/Suffix accumulation arrays (Product of Array Except Self).
# - Master complex boundary tracking (Search in Rotated Sorted Array).
#
# ==============================================================================
"""

from typing import List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. 3SUM (THE COLLAPSING WINDOW)
# ==============================================================================
def three_sum(nums: List[int]) -> List[List[int]]:
    """
    Time: O(N^2) | Space: O(1) or O(N) depending on sorting algorithm
    Find all unique triplets in the array which gives the sum of zero.
    """
    # 1. We MUST sort the array. This takes O(N log N).
    # Sorting mathematically groups duplicates together (for easy skipping) and 
    # provides the ordered structure required for Two-Pointer logic!
    nums.sort()
    result = []
    n = len(nums)
    
    print(f"  Sorted Array: {nums}")
    
    for i in range(n - 2):
        # 2. DUPLICATE ANNIHILATION (Outer Loop)
        # If the current anchor number is identical to the previous one, skip it!
        # Otherwise, we will generate the exact same triplets again.
        if i > 0 and nums[i] == nums[i - 1]:
            continue
            
        # 3. MATHEMATICAL SHORT-CIRCUIT
        # Because the array is sorted, if our anchor is greater than 0, 
        # the remaining numbers (which are even larger) can NEVER sum to 0!
        if nums[i] > 0:
            break
            
        # 4. THE COLLAPSING WINDOW
        left = i + 1
        right = n - 1
        
        while left < right:
            total = nums[i] + nums[left] + nums[right]
            
            if total < 0:
                # The sum is too small. We need a larger number. Move left pointer up!
                left += 1
            elif total > 0:
                # The sum is too large. We need a smaller number. Move right pointer down!
                right -= 1
            else:
                # WE FOUND A PERFECT TRIPLET!
                print(f"    -> [MATCH] Triplet Found: {nums[i]} + {nums[left]} + {nums[right]} == 0")
                result.append([nums[i], nums[left], nums[right]])
                
                # We must continue searching for OTHER combinations with this same anchor!
                left += 1
                right -= 1
                
                # 5. DUPLICATE ANNIHILATION (Inner Loop)
                # We must physically skip over any identical left pointers to avoid 
                # duplicate triplets!
                while left < right and nums[left] == nums[left - 1]:
                    left += 1
                    
    return result

def demonstrate_3sum():
    section_header("Medium: 3Sum (O(N^2) Two-Pointer)")
    
    nums = [-1, 0, 1, 2, -1, -4]
    ans = three_sum(nums)
    print(f"\nResult: {ans}")


# ==============================================================================
# 4. PRODUCT OF ARRAY EXCEPT SELF (O(1) SPACE PREFIX/SUFFIX)
# ==============================================================================
def product_except_self(nums: List[int]) -> List[int]:
    """
    Time: O(N) | Space: O(1) (The output array does not count towards Space Complexity)
    Given an integer array nums, return an array answer such that answer[i] is equal 
    to the product of all the elements of nums except nums[i].
    
    CRITICAL CONSTRAINT: You MUST write an algorithm that runs in O(n) time and 
    without using the division operation!
    """
    n = len(nums)
    # We initialize the result array with 1s.
    result = [1] * n
    
    # 1. PREFIX PASS (Left to Right)
    # We mathematically calculate the product of every number strictly to the LEFT 
    # of the current index!
    prefix = 1
    print("  Executing Prefix Pass (Left to Right)...")
    for i in range(n):
        result[i] = prefix
        prefix *= nums[i]
        
    print(f"    -> Prefix State: {result}")
        
    # 2. SUFFIX PASS (Right to Left)
    # We calculate the product of every number strictly to the RIGHT of the current 
    # index, and MULTIPLY it directly into the result array!
    suffix = 1
    print("  Executing Suffix Pass (Right to Left)...")
    for i in range(n - 1, -1, -1):
        result[i] *= suffix
        suffix *= nums[i]
        
    print(f"    -> Final State:  {result}")
        
    return result

def demonstrate_product():
    section_header("Medium: Product of Array Except Self")
    
    nums = [1, 2, 3, 4]
    print(f"Original Array: {nums}\n")
    ans = product_except_self(nums)
    print(f"\nResult: {ans} (Expected: [24, 12, 8, 6])")


# ==============================================================================
# 5. SEARCH IN ROTATED SORTED ARRAY (FRACTURED BINARY SEARCH)
# ==============================================================================
def search_rotated(nums: List[int], target: int) -> int:
    """
    Time: O(log N) | Space: O(1)
    The array is sorted, but it has been rotated at some unknown pivot!
    Example: [0,1,2,4,5,6,7] might become [4,5,6,7,0,1,2].
    We must still find the target in O(log N) time!
    """
    left = 0
    right = len(nums) - 1
    
    print(f"  Searching for {target} in Rotated Array {nums}")
    
    while left <= right:
        mid = left + (right - left) // 2
        
        if nums[mid] == target:
            print(f"    -> [SUCCESS] Found target {target} at index {mid}!")
            return mid
            
        # THE CORE LOGIC: Because the array is rotated exactly ONCE, one of the 
        # two halves (Left or Right) is mathematically GUARANTEED to be perfectly sorted!
        
        # Scenario A: The Left half is perfectly sorted!
        if nums[left] <= nums[mid]:
            # Does the target fall mathematically inside this sorted boundary?
            if nums[left] <= target < nums[mid]:
                # It does! We can safely annihilate the entire Right half!
                right = mid - 1
                print("    -> Target is in the sorted Left half. Shrinking right.")
            else:
                # It does NOT! We must annihilate the entire Left half!
                left = mid + 1
                print("    -> Target is NOT in the sorted Left half. Shrinking left.")
                
        # Scenario B: The Right half is perfectly sorted!
        else:
            # Does the target fall mathematically inside this sorted boundary?
            if nums[mid] < target <= nums[right]:
                left = mid + 1
                print("    -> Target is in the sorted Right half. Shrinking left.")
            else:
                right = mid - 1
                print("    -> Target is NOT in the sorted Right half. Shrinking right.")
                
    return -1

def demonstrate_rotated():
    section_header("Medium: Search in Rotated Sorted Array")
    
    nums = [4, 5, 6, 7, 0, 1, 2]
    target = 0
    ans = search_rotated(nums, target)
    print(f"\nResult: Index {ans} (Expected: 4)")


def run_all_labs():
    demonstrate_3sum()
    demonstrate_product()
    demonstrate_rotated()


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "In 3Sum, why do we use a Two-Pointer collapsing window instead of a Hash Map like we did in Two Sum? Wouldn't a Hash Map be faster?"
   Senior Answer: "If we lock the first number as an anchor, we could technically solve the remaining Two Sum problem using a Hash Map, yielding an identical $O(N^2)$ Time Complexity. However, the constraints for 3Sum explicitly demand that the returned triplets must be mathematically unique. Hash Maps do not possess inherent structural ordering, making it horrific to prevent identical triplets from being generated without serializing them into Strings and storing them in an external $O(N)$ Hash Set. By sorting the array ($O(N \\log N)$) and using Two-Pointers, we can physically skip identical adjacent numbers instantly (`while nums[left] == nums[left - 1]`), ensuring perfect uniqueness in strict $O(1)$ Space."

2. Interviewer: "In Product of Array Except Self, why is the division operator (`/`) explicitly forbidden?"
   Senior Answer: "If the division operator were allowed, the problem is trivial: calculate the total product of the entire array, and then for each element, just append `total / nums[i]`. The interviewer forbids it because Division violently breaks when the number `0` is introduced. If there is a single `0` in the array, the total product becomes `0`, and attempting to divide by it crashes the server with a `ZeroDivisionError`. The Prefix/Suffix approach mathematically multiplies the numbers *around* the element, flawlessly handling one, two, or multiple Zeroes without any algorithmic corruption."

3. Interviewer: "In the Rotated Sorted Array problem, why does checking `nums[left] <= nums[mid]` mathematically prove that the Left half is perfectly sorted?"
   Senior Answer: "The array was originally sorted in ascending order and rotated at exactly one pivot point. This means there is exactly one 'fracture' in the entire array where a larger number sits to the left of a smaller number (e.g., the `7` and `0` in `[4, 5, 6, 7, 0, 1, 2]`). If we look at `left` and `mid`, and `nums[left]` is strictly less than or equal to `nums[mid]`, it physically proves that the 'fracture' does NOT exist between those two indices. Without a fracture, the sequence is unbroken, proving the Left half is perfectly, continuously sorted."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Problem Sets (Array Medium) Completed.")
