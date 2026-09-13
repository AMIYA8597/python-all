"""
# ==============================================================================
# LABORATORY: MERGE SORT & THE MASTER THEOREM
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You've seen Merge Sort as a Sorting Algorithm. But here, we view it purely 
# as a mathematical implementation of the "Divide and Conquer" paradigm.
# 
# 1. DIVIDE: Split the array perfectly in half.
# 2. CONQUER: Recursively sort the two halves.
# 3. COMBINE: Merge the two sorted halves back together in O(N) time.
#
# How do we mathematically prove the Time Complexity of this recursive structure?
# We write a "Recurrence Relation": 
# T(n) = 2 * T(n/2) + O(n)
# 
# The "Master Theorem" is a mathematical formula that solves these recurrences 
# instantly. It compares the rate of subproblem growth against the rate of the 
# combine step.
#
# For Merge Sort:
# a = 2 (We make 2 recursive calls)
# b = 2 (We divide the input by 2)
# f(n) = O(n^1) (The merge step takes linear time)
#
# Because log_b(a) = log_2(2) = 1, and our f(n) exponent is also 1, we are in 
# "Case 2" of the Master Theorem. 
# The formula is $O(n^1 \\times \\log n)$.
# Therefore, Merge Sort is mathematically proven to run in O(N log N) time!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the 3 D&C Steps within Merge Sort.
# - Differentiate the recursive split from the iterative merge.
# - Understand how the Master Theorem defines algorithm bounds.
#
# ==============================================================================
"""

from typing import List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. DIVIDE & CONQUER (MERGE SORT)
# ==============================================================================
def merge_sort_dc(nums: List[int]) -> List[int]:
    """
    Time Complexity: O(N log N) (Proven via Master Theorem Case 2).
    Space Complexity: O(N) (Allocating new arrays during the Combine step).
    """
    # 1. BASE CASE
    if len(nums) <= 1:
        return nums
        
    # 2. DIVIDE
    # Split the array perfectly in half. O(1) mathematical calculation.
    mid = len(nums) // 2
    
    # 3. CONQUER (RECURSIVE CALLS)
    # We create two subproblems. T(n) = 2 * T(n/2)
    left_half = merge_sort_dc(nums[:mid])
    right_half = merge_sort_dc(nums[mid:])
    
    # 4. COMBINE
    # This is the f(n) = O(n) step!
    return merge(left_half, right_half)


def merge(left: List[int], right: List[int]) -> List[int]:
    """
    The Two-Pointer algorithm to zip two sorted arrays together in O(N) time.
    """
    merged = []
    i = 0
    j = 0
    
    # Compare the tops of both piles, take the smaller one.
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
            
    # If one pile is empty, blindly sweep the rest of the other pile!
    merged.extend(left[i:])
    merged.extend(right[j:])
    
    return merged


def demonstrate_merge_sort_dc():
    section_header("Algorithm: Merge Sort (D&C Paradigm)")
    
    nums = [38, 27, 43, 3, 9, 82, 10]
    
    print(f"Unsorted Input: {nums}")
    print("\nExecuting Divide and Conquer (Merge Sort)...")
    
    ans = merge_sort_dc(nums)
    
    print(f"\nSorted Output: {ans}")
    print("\nVisualizing the Tree:")
    print("                [38, 27, 43, 3, 9, 82, 10]")
    print("DIVIDE:     [38, 27, 43]          [3, 9, 82, 10]")
    print("CONQUER: [38]   [27, 43]       [3, 9]     [82, 10]")
    print("COMBINE: [38]   [27, 43]       [3, 9]     [10, 82]")
    print("COMBINE:    [27, 38, 43]          [3, 9, 10, 82]")
    print("FINAL:          [3, 9, 10, 27, 38, 43, 82]")


# ==============================================================================
# 4. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. What is the Recurrence Relation for Binary Search?
   Answer: In Binary Search, we make ONE recursive call (we throw the other half away). We divide the input by 2. The mathematical comparison to find the middle is $O(1)$. 
   $T(n) = 1 \\times T(n/2) + O(1)$. 
   Using the Master Theorem: $a=1, b=2, f(n)=n^0$. 
   $\\log_2(1) = 0$. Since the exponent $0$ matches $f(n)$'s exponent $0$, we are in Case 2. 
   Formula: $n^0 \\times \\log n = 1 \\times \\log n = O(\\log N)$.

2. What is the Recurrence Relation for standard recursive DFS on a Binary Tree?
   Answer: We explore BOTH the left and right children. $a=2, b=2$. There is no "Combine" step, we just do $O(1)$ work at the node.
   $T(n) = 2 \\times T(n/2) + O(1)$.
   Using Master Theorem: $a=2, b=2, f(n)=n^0$.
   $\\log_2(2) = 1$. Since $1 > 0$, we are in Case 1 (The recursive leaves dominate the workload).
   Formula: $O(n^{\\log_b a}) = O(n^1) = O(N)$.

3. Why is Merge Sort guaranteed $O(N \\log N)$, but Quick Sort can degrade to $O(N^2)$?
   Answer: Merge Sort forces $b=2$ mathematically by just cutting the array index in half. It is a guaranteed perfect 50/50 split every single time. Quick Sort relies on a Pivot. If the pivot is the largest or smallest element in the array, the split is $T(n) = 1 \\times T(n-1) + O(n)$. This violently breaks the Master Theorem (because $b$ is no longer a fraction, it's subtraction). A recurrence of $T(n) = T(n-1) + O(n)$ resolves algebraically to the sum of $1+2+3...N$, which is $O(N^2)$.
"""

if __name__ == "__main__":
    demonstrate_merge_sort_dc()
    print("\n[SUCCESS] Laboratory: Merge Sort D&C Completed.")
