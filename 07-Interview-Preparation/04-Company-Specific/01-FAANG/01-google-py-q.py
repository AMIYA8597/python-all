"""
# ==============================================================================
# LABORATORY: INTERVIEW PREPARATION (FAANG - GOOGLE PYTHON QUESTIONS)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Google interviews are legendary for their mathematical rigor and extreme 
# algorithmic optimization constraints. They do not care if you can solve the 
# problem. They care if you can solve the problem at the absolute theoretical 
# mathematical limits of Space and Time complexity.
#
# A junior engineer might solve a problem in O(N log N) using a sort. Google 
# will ask for O(N). If the junior achieves O(N) using a Hash Map, Google will 
# ask for O(N) Time and O(1) Space. You must push the boundaries of Bit Manipulation, 
# Two Pointers, and Dynamic Programming.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master Google-tier array manipulation (Next Permutation / Lexicographical).
# - Master extreme constraints (O(1) Space modifications).
# - Prepare for Google's "Follow-Up" interrogation phase.
#
# ==============================================================================
"""

from typing import List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. NEXT PERMUTATION (GOOGLE FAVORITE)
# ==============================================================================
def next_permutation(nums: List[int]) -> None:
    """
    Time: O(N) | Space: O(1)
    Given an array of integers, rearrange them into the mathematically NEXT 
    lexicographically greater permutation. If it's the absolute largest, 
    reverse it into the absolute smallest.
    
    Example: [1, 2, 3] -> [1, 3, 2]
    Example: [3, 2, 1] -> [1, 2, 3] (Reset!)
    """
    n = len(nums)
    
    print(f"  Initial Array: {nums}")
    
    # 1. Find the FIRST decreasing element from the RIGHT!
    # A perfectly descending suffix (e.g., [4, 3, 2, 1]) is mathematically MAXED OUT.
    # It cannot be made any larger. We must find the "pivot" right before it!
    i = n - 2
    while i >= 0 and nums[i] >= nums[i + 1]:
        i -= 1
        
    if i >= 0:
        print(f"    -> [PIVOT FOUND] at index {i} (value: {nums[i]})")
        
        # 2. Find the FIRST element strictly LARGER than the pivot from the RIGHT!
        # This will be the number we swap the pivot with to gently increment the array.
        j = n - 1
        while nums[j] <= nums[i]:
            j -= 1
            
        print(f"    -> [SWAP TARGET] at index {j} (value: {nums[j]})")
        nums[i], nums[j] = nums[j], nums[i]
        
    else:
        print("    -> [NO PIVOT] The entire array is descending. Resetting to minimum.")
        
    # 3. REVERSE THE SUFFIX
    # After the swap, the suffix is still mathematically sorted in descending order!
    # By reversing it in-place, we instantly reset it to ascending order, generating 
    # the absolute smallest possible increment!
    print(f"    -> Reversing suffix from index {i + 1} to the end.")
    left, right = i + 1, n - 1
    while left < right:
        nums[left], nums[right] = nums[right], nums[left]
        left += 1
        right -= 1

def demonstrate_next_permutation():
    section_header("Google: Next Permutation (O(N) Time, O(1) Space)")
    
    nums1 = [1, 2, 3]
    next_permutation(nums1)
    print(f"  Final State: {nums1} (Expected: [1, 3, 2])\n")
    
    nums2 = [1, 3, 5, 4, 2]
    next_permutation(nums2)
    print(f"  Final State: {nums2} (Expected: [1, 4, 2, 3, 5])\n")
    
    nums3 = [3, 2, 1]
    next_permutation(nums3)
    print(f"  Final State: {nums3} (Expected: [1, 2, 3])")


# ==============================================================================
# 4. MAXIMUM WATER CONTAINER (TWO POINTERS)
# ==============================================================================
def max_area(height: List[int]) -> int:
    """
    Time: O(N) | Space: O(1)
    Given an array of heights, find two lines that together with the x-axis 
    forms a container, such that the container contains the most water.
    
    Google Follow-Up: "Prove to me mathematically that moving the smaller pointer 
    inward doesn't miss the optimal solution."
    """
    left = 0
    right = len(height) - 1
    max_water = 0
    
    while left < right:
        # The physical water level is bottle-necked by the SHORTER wall!
        h = min(height[left], height[right])
        w = right - left
        current_water = h * w
        
        print(f"  Checking Bounds [{left}, {right}] -> Height: {h}, Width: {w} -> Area: {current_water}")
        
        max_water = max(max_water, current_water)
        
        # THE MATHEMATICAL PROOF (The Greedy Move):
        # The width is continuously shrinking. The ONLY way to possibly find a 
        # larger area is to find a TALLER wall. Therefore, we MUST discard the 
        # shorter wall and hope a taller one lies ahead!
        if height[left] < height[right]:
            print(f"    -> Left wall ({height[left]}) is shorter. Moving left pointer right.")
            left += 1
        else:
            print(f"    -> Right wall ({height[right]}) is shorter (or equal). Moving right pointer left.")
            right -= 1
            
    return max_water

def demonstrate_max_water():
    section_header("Google: Container With Most Water (O(N) Optimization)")
    
    heights = [1, 8, 6, 2, 5, 4, 8, 3, 7]
    print(f"Heights: {heights}\n")
    
    ans = max_area(heights)
    print(f"\nResult: Absolute Maximum Water Area = {ans}")


def run_all_labs():
    demonstrate_next_permutation()
    demonstrate_max_water()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "In the Next Permutation problem, after we execute the swap at the pivot, why does reversing the suffix magically produce the lexicographically 'next' combination?"
   Senior Answer: "The pivot marks the exact transition point where the array's suffix is in a mathematically perfect descending order. A descending sequence is maximized; it cannot be incremented further. When we swap the pivot with the next largest number from the right, we successfully increment the 'magnitude' of the permutation. However, the suffix is STILL in descending order, meaning it is the absolute largest possible variation of that new prefix! To find the *immediate* next permutation, we need the suffix to be as small as physically possible. Reversing a descending array instantly transforms it into a perfectly ascending array ($O(N)$), granting us the smallest possible variation in strictly $O(1)$ constant space."

2. Interviewer: "In the Container With Most Water problem, prove to me that the $O(N)$ Two Pointer strategy doesn't accidentally skip the optimal answer."
   Senior Answer: "Suppose our pointers are at `L` and `R`, and `height[L] < height[R]`. The current area is restricted by the shorter wall, `height[L]`. If we were to hold `L` in place and move `R` inward to test combinations, the width of the container strictly decreases. Furthermore, the height of the water can NEVER exceed `height[L]`, regardless of how tall the new inner right walls are! Therefore, every single combination involving `L` and any inner index is mathematically guaranteed to have a smaller area than the current `[L, R]` state. By moving the `L` pointer inward, we permanently discard combinations that are already mathematically proven to be inferior, achieving an optimal $O(N)$ search without skipping anything of value."

3. Interviewer: "How does Google evaluate a candidate who successfully solves a problem using $O(N)$ Time and $O(N)$ Space, versus someone who struggles but aims for $O(N)$ Time and $O(1)$ Space?"
   Senior Answer: "Google highly favors candidates who instantly recognize the theoretical limits of a problem. If a candidate solves it with $O(N)$ Space via Hash Maps, the interviewer will say, 'Can you do this in $O(1)$ Space?' If the candidate doesn't immediately grasp how Bit Manipulation, In-Place Array Swapping, or Two Pointers can achieve that, they fail. The struggle for perfection is respected far more than a quick, memory-inefficient solution. Google operates at an Exabyte scale; saving $O(N)$ memory across a Trillion-item cluster is a fundamental engineering requirement."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: FAANG Prep (Google) Completed.")
