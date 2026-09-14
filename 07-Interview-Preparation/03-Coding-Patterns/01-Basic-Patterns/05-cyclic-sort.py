"""
# ==============================================================================
# LABORATORY: INTERVIEW PREPARATION (CODING PATTERNS - CYCLIC SORT)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Interviewer: "You are given an unsorted array of size N containing numbers 
# from 0 to N. One number is missing. Find it in O(N) Time and O(1) Space."
#
# If you call `.sort()`, you write O(N log N) time and you fail.
# If you use a Hash Set to find the missing number, you write O(N) space and fail.
#
# A senior engineer recognizes the mathematical constraint: "Numbers from 0 to N". 
# This means the numbers themselves can be used as their own array indices! 
# If the number `5` is at index `2`, it is in the wrong place. We can blindly swap 
# it with the number at index `5`. By repeating this blindly, every number will 
# magically orbit into its perfectly sorted slot in O(N) time without allocating 
# any extra memory! This is the 'Cyclic Sort' pattern.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master Cyclic Sort algorithm (In-place index orbiting).
# - Master finding the Missing Number.
# - Understand the algorithmic Time Complexity proof (Amortized O(N)).
#
# ==============================================================================
"""

from typing import List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. CYCLIC SORT (THE ORBIT ALGORITHM)
# ==============================================================================
def cyclic_sort(nums: List[int]) -> None:
    """
    Time: O(N) | Space: O(1)
    Sorts an array containing numbers from 1 to N.
    The goal is to mathematically force `nums[i] == i + 1`.
    """
    i = 0
    while i < len(nums):
        # What is the mathematically correct index for the current number?
        # If the number is 3, it belongs at index 2 (because arrays are 0-indexed).
        correct_index = nums[i] - 1
        
        # If the number is NOT at its correct index, SWAP IT!
        if 0 <= correct_index < len(nums) and nums[i] != nums[correct_index]:
            print(f"  Swap: {nums[i]} (idx {i}) <-> {nums[correct_index]} (idx {correct_index})")
            
            # Python tuple unpacking for simultaneous swapping!
            nums[correct_index], nums[i] = nums[i], nums[correct_index]
            
            # CRITICAL: Do NOT increment `i`! 
            # We just swapped a brand new number into index `i`. We must evaluate 
            # this new number before we move forward!
        else:
            # The number is either at the correct index, or out of bounds. Move on!
            i += 1

def demonstrate_cyclic_sort():
    section_header("Cyclic Sort (In-Place Orbiting)")
    
    nums = [3, 1, 5, 4, 2]
    print(f"Original Array: {nums}\n")
    
    cyclic_sort(nums)
    
    print(f"\nSorted Array: {nums}")
    print("We achieved this without using `.sort()`, perfectly in O(N) Time and O(1) Space!")


# ==============================================================================
# 4. FIND THE MISSING NUMBER
# ==============================================================================
def find_missing_number(nums: List[int]) -> int:
    """
    Time: O(N) | Space: O(1)
    Array contains numbers from 0 to N. One is missing.
    """
    # Phase 1: Cyclic Sort!
    i = 0
    n = len(nums)
    
    print("  Phase 1: Forcing numbers into their correct orbits...")
    while i < n:
        # Since numbers are 0 to N, the correct index for 'value' is just 'value'.
        correct_index = nums[i]
        
        # If the number is N, it falls out of bounds (ignore it).
        if correct_index < n and nums[i] != nums[correct_index]:
            nums[correct_index], nums[i] = nums[i], nums[correct_index]
        else:
            i += 1
            
    print(f"  Orbit completed: {nums}")
            
    # Phase 2: Find the mathematical anomaly!
    print("  Phase 2: Scanning for the mathematical anomaly...")
    for i in range(n):
        if nums[i] != i:
            print(f"    -> Anomaly! Index {i} contains the number {nums[i]}!")
            return i
            
    # If all indices match, the missing number MUST be N itself!
    return n

def demonstrate_find_missing():
    section_header("Find Missing Number (0 to N)")
    
    nums = [4, 0, 3, 1]
    print(f"Array: {nums} (N=4). The missing number should be 2.\n")
    
    result = find_missing_number(nums)
    
    print(f"\nResult: The missing number is {result}")


def run_all_labs():
    demonstrate_cyclic_sort()
    demonstrate_find_missing()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "In the Cyclic Sort algorithm, there is a `while` loop, and inside it, we sometimes perform a swap WITHOUT incrementing the loop counter `i`. Doesn't this cause an infinite loop? Why is the time complexity $O(N)$ instead of $O(N^2)$?"
   Senior Answer: "It does not cause an infinite loop because every single swap mathematically forces at least ONE number into its absolute, permanently correct position in the array. Because there are $N$ numbers, the absolute maximum number of swaps that can possibly occur across the entire lifetime of the algorithm is exactly $N-1$. Even though the `while` loop doesn't increment `i` on a swap, the global swap counter is relentlessly approaching its mathematical ceiling of $N$. Therefore, the total number of operations is bounded by $N$ (loop increments) + $N-1$ (max swaps) = $2N$. This simplifies to a strict, amortized $O(N)$ time complexity."

2. Interviewer: "What is the critical constraint that dictates you MUST use Cyclic Sort?"
   Senior Answer: "The defining constraint is when the problem states: 'You are given an array containing numbers in the range from 1 to N' (or 0 to N). The moment you see that specific mathematical bound, you know the values perfectly correlate to the array indices. The second critical constraint is a strict memory limit: 'You must do this in $O(1)$ extra space'. Cyclic Sort is the only algorithm that can establish perfect order for this specific dataset without allocating Hash Maps or triggering the heavy $O(N \\log N)$ engine of a comparison sort like Merge Sort."

3. Interviewer: "I can solve 'Find the Missing Number' in $O(N)$ time and $O(1)$ space using the Gauss Summation formula ($Sum = N(N+1)/2$). I just subtract the array sum from the Gauss sum. Why learn Cyclic Sort?"
   Senior Answer: "The Gauss Summation formula is brilliant, but it is mathematically brittle. It ONLY works for finding exactly one missing number. If the interviewer modifies the problem to: 'Find ALL the missing numbers', or 'Find the Duplicate number', the Gauss formula instantly collapses because it cannot distinguish between multiple mathematical overlapping anomalies. Cyclic Sort physically rearranges the memory. Once sorted, a simple $O(N)$ scan can instantly identify 5 missing numbers, 3 duplicates, or any combination of corruption simultaneously."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Interview Prep (Cyclic Sort) Completed.")
