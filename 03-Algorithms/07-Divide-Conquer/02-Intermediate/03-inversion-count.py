"""
# ==============================================================================
# LABORATORY: COUNTING INVERSIONS (DIVIDE & CONQUER)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# What if a company asks you: "How unsorted is this array?"
# A perfectly sorted array `[1, 2, 3]` is 0% unsorted.
# A completely reversed array `[3, 2, 1]` is 100% unsorted.
# 
# How do we quantify this mathematically? We count "Inversions".
# An Inversion is any pair of numbers where a LARGER number appears BEFORE a 
# SMALLER number in the array.
# For `[3, 2, 1]`, the inversions are (3,2), (3,1), and (2,1). Total: 3.
#
# This exact metric is used in Data Science and Recommendation Engines (like 
# Netflix Collaborative Filtering) to determine how similar two users' rankings are!
#
# A naive `for i ... for j` loop counts inversions in O(N^2) time.
# But we can use Divide & Conquer (specifically, a modified Merge Sort) to count 
# them in blazing fast O(N log N) time!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the definition of an Inversion.
# - Hijack the Merge Sort algorithm to count crossing inversions.
# - Master the mathematical logic: `inversions += (len(left) - i)`.
#
# ==============================================================================
"""

from typing import List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. DIVIDE & CONQUER INVERSION ENGINE (O(N log N))
# ==============================================================================
def count_inversions(nums: List[int]) -> int:
    """
    Time Complexity: O(N log N) (Standard Merge Sort recurrence).
    Space Complexity: O(N) for temporary arrays during the merge step.
    """
    
    # We will use a nested helper function so we can modify the array in place 
    # without constantly allocating new arrays. (Professional optimization).
    def merge_and_count(left_idx: int, mid: int, right_idx: int) -> int:
        # Create copies of the left and right halves
        left_half = nums[left_idx : mid + 1]
        right_half = nums[mid + 1 : right_idx + 1]
        
        i = 0 # Pointer for left_half
        j = 0 # Pointer for right_half
        k = left_idx # Pointer for the main array `nums`
        
        inversions = 0
        
        while i < len(left_half) and j < len(right_half):
            if left_half[i] <= right_half[j]:
                # NORMAL. The left element is smaller. No inversion!
                nums[k] = left_half[i]
                i += 1
            else:
                # INVERSION DETECTED!
                # The right element is smaller than the left element.
                # Because `left_half` is internally sorted, if `right_half[j]` 
                # is smaller than `left_half[i]`, it is mathematically guaranteed 
                # to ALSO be smaller than every single element AFTER `i` in the left half!
                # We don't need to count them one by one. We just add the remaining length!
                inversions += (len(left_half) - i)
                
                nums[k] = right_half[j]
                j += 1
            k += 1
            
        # Clean up any remaining elements
        while i < len(left_half):
            nums[k] = left_half[i]
            i += 1
            k += 1
            
        while j < len(right_half):
            nums[k] = right_half[j]
            j += 1
            k += 1
            
        return inversions

    def divide_and_conquer(left_idx: int, right_idx: int) -> int:
        inversions = 0
        if left_idx < right_idx:
            mid = left_idx + (right_idx - left_idx) // 2
            
            # Count inversions strictly inside the left half
            inversions += divide_and_conquer(left_idx, mid)
            
            # Count inversions strictly inside the right half
            inversions += divide_and_conquer(mid + 1, right_idx)
            
            # Count "Crossing Inversions" that span between the two halves!
            inversions += merge_and_count(left_idx, mid, right_idx)
            
        return inversions

    # Kick off the recursive engine
    return divide_and_conquer(0, len(nums) - 1)


def demonstrate_inversion_counting():
    section_header("Algorithm: Counting Inversions (D&C)")
    
    # A completely reversed array.
    # Mathematically, maximum inversions = N * (N - 1) / 2.
    # For N=5: 5 * 4 / 2 = 10 inversions!
    nums1 = [5, 4, 3, 2, 1]
    
    print(f"Input Array 1 (Completely Reversed): {nums1}")
    # Note: `count_inversions` physically sorts the array during the process!
    # We must pass a copy if we want to preserve the original.
    ans1 = count_inversions(nums1.copy())
    print(f"Total Inversions: {ans1} (Expected: 10)")
    
    nums2 = [2, 4, 1, 3, 5]
    print(f"\nInput Array 2: {nums2}")
    ans2 = count_inversions(nums2.copy())
    print(f"Total Inversions: {ans2} (Expected: 3)")
    print("Explanation of Array 2:")
    print(" (2, 1) - 2 appears before 1.")
    print(" (4, 1) - 4 appears before 1.")
    print(" (4, 3) - 4 appears before 3.")


# ==============================================================================
# 4. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why does `inversions += (len(left_half) - i)` mathematically work?
   Answer: Because Divide & Conquer guarantees that `left_half` is already perfectly sorted! If `left_half = [4, 5, 6]` and `right_half = [1]`. We compare `4` and `1`. Since `1 < 4`, it is an inversion! Because the left array is sorted, we instantly know that `5` and `6` must be larger than `4`, which means they MUST also be larger than `1`. We don't have to check them. We just add all 3 remaining elements in the left array to our inversion count!

2. Why must we physically sort the array to count the inversions? Why can't we just count them and leave the array alone?
   Answer: The entire $O(1)$ math trick `(len - i)` RELIES on the two halves being completely sorted. If the left half wasn't sorted, we would have no idea if the elements after `i` were larger or smaller than the right element. We would have to manually scan them, which would degrade the algorithm back to $O(N^2)$. Sorting the array as we merge is the only way to enable the math trick for the next recursive level up.

3. How is this used in Data Science / Recommendation Engines?
   Answer: "Kendall Rank Correlation Coefficient". If User A ranks 5 movies: `[A, B, C, D, E]`, and User B ranks the same 5 movies: `[B, D, A, E, C]`. You map User A's movies to the integers `[1, 2, 3, 4, 5]`. Then you map User B's movies to those same integers based on User A's baseline: `[2, 4, 1, 5, 3]`. You run the Inversion Count algorithm on User B's array. The fewer the inversions, the more similar their tastes are! Netflix uses this to recommend movies.
"""

if __name__ == "__main__":
    demonstrate_inversion_counting()
    print("\n[SUCCESS] Laboratory: Inversion Counting Completed.")
