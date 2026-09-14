"""
# ==============================================================================
# LABORATORY: INTERVIEW PREPARATION (CODING PATTERNS - TWO POINTERS)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Interviewer: "Given a sorted array, find two numbers that add up to a Target. 
# Do it in O(1) Memory and O(N) Time."
#
# If you use a nested loop, you write O(N^2) time and you fail.
# If you use a Hash Map, you write O(N) memory and you fail.
# 
# The Two Pointers pattern is the mathematical foundation of array manipulation. 
# By placing one pointer at the start (Left) and one at the end (Right), you 
# can mathematically rule out massive chunks of the search space instantly 
# because the array is sorted.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master the 'Opposite Ends' Two Pointers (Two Sum II).
# - Master the 'Same Direction' Two Pointers (Remove Duplicates).
# - Master the algorithmic proof of WHY it works (Search Space Reduction).
#
# ==============================================================================
"""

from typing import List, Tuple

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. OPPOSITE ENDS (TWO SUM II - SORTED ARRAY)
# ==============================================================================
def two_sum_sorted(nums: List[int], target: int) -> Tuple[int, int]:
    """
    Time: O(N) | Space: O(1)
    Because the array is strictly sorted, we can mathematically eliminate 
    impossible combinations.
    """
    left = 0
    right = len(nums) - 1
    
    print(f"  Target: {target}")
    
    while left < right:
        current_sum = nums[left] + nums[right]
        print(f"  Checking: nums[{left}]({nums[left]}) + nums[{right}]({nums[right]}) = {current_sum}")
        
        if current_sum == target:
            return (left, right)
            
        elif current_sum < target:
            # The sum is too small! 
            # Because the array is sorted, moving `right` to the left would only 
            # make the sum EVEN SMALLER. Therefore, we MUST increase the sum by 
            # moving the `left` pointer to the right!
            print("    Sum too small! Moving LEFT pointer right (Increase).")
            left += 1
            
        else: # current_sum > target
            # The sum is too large!
            # We MUST decrease the sum by moving the `right` pointer to the left!
            print("    Sum too large! Moving RIGHT pointer left (Decrease).")
            right -= 1
            
    return (-1, -1)

def demonstrate_opposite_ends():
    section_header("Opposite Ends (Two Sum Sorted)")
    nums = [2, 7, 11, 15, 20, 25]
    target = 31
    print(f"Array: {nums}\n")
    
    idx1, idx2 = two_sum_sorted(nums, target)
    print(f"\nResult: Indices ({idx1}, {idx2}) -> Values ({nums[idx1]}, {nums[idx2]})")


# ==============================================================================
# 4. SAME DIRECTION (REMOVE DUPLICATES)
# ==============================================================================
def remove_duplicates_inplace(nums: List[int]) -> int:
    """
    Time: O(N) | Space: O(1)
    Given a sorted array, remove duplicates IN-PLACE so that each unique element 
    appears only once. Return the new length.
    
    We use two pointers starting at the same end:
    - 'writer': Points to where the NEXT unique element should be written.
    - 'reader': Scans ahead to find the next unique element.
    """
    if not nums: return 0
    
    writer = 1 # Index 0 is always unique by definition!
    
    for reader in range(1, len(nums)):
        # If the reader sees a DIFFERENT number than the one right behind it,
        # it is a brand new unique number!
        if nums[reader] != nums[reader - 1]:
            print(f"  Unique found: {nums[reader]} at idx {reader}. Writing to idx {writer}")
            # Overwrite the duplicate!
            nums[writer] = nums[reader]
            writer += 1
            
    return writer

def demonstrate_same_direction():
    section_header("Same Direction (Remove Duplicates In-Place)")
    nums = [0, 0, 1, 1, 1, 2, 2, 3, 3, 4]
    print(f"Original Array: {nums}\n")
    
    new_len = remove_duplicates_inplace(nums)
    print(f"\nFinal Array (First {new_len} elements matter): {nums[:new_len]}")
    print(f"Notice we didn't allocate a new array! Perfect O(1) space.")


def run_all_labs():
    demonstrate_opposite_ends()
    demonstrate_same_direction()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "Why is the Opposite-Ends Two Pointer algorithm mathematically guaranteed to find the correct answer in $O(N)$ time?"
   Senior Answer: "The algorithm relies entirely on the mathematical property of the sorted array. If `L + R < Target`, we are mathematically certain that pairing `L` with any index smaller than `R` will produce a sum that is *even smaller*. Therefore, the current `L` is entirely useless and can be permanently discarded by moving `L` to the right. We eliminate an entire column of the theoretical $N \\times N$ matrix of all possible pairs in $O(1)$ time. Because each step permanently discards either a row or a column without backtracking, the two pointers will meet in exactly $O(N)$ operations."

2. Interviewer: "When executing the 'Same Direction' Two Pointers (Reader/Writer) pattern to remove duplicates, why don't we just use `list.pop()` to physically remove the duplicate?"
   Senior Answer: "Calling `list.pop(index)` on an array is an $O(N)$ operation because it physically forces the CPU to shift every subsequent element in RAM one address to the left to fill the memory gap. If we do this inside an $O(N)$ loop, the total algorithmic complexity becomes $O(N^2)$, which will fail large test cases. The Two Pointers pattern bypasses this completely by simply *overwriting* the memory in-place (`nums[writer] = nums[reader]`). This is a pure $O(1)$ memory operation, achieving perfect $O(N)$ total time."

3. Interviewer: "What are the common visual 'tells' in a LeetCode problem that signal you MUST use Two Pointers?"
   Senior Answer: "The massive giveaways are: (1) The array is explicitly stated to be 'Sorted'. (2) You need to find a 'Pair' or a 'Triplet' of elements. (3) The problem places a draconian $O(1)$ space constraint on you, mathematically ruling out Hash Maps. (4) You need to perform in-place array manipulation (like removing elements, moving zeroes to the end, or reversing the array)."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Interview Prep (Two Pointers) Completed.")
