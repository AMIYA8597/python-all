"""
# ==============================================================================
# LABORATORY: COMPETITIVE PROGRAMMING (ATCODER GRAND CONTEST)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# AtCoder Grand Contest (AGC) contains the most mathematically rigorous and 
# punishing ad-hoc problems in the world. 
# 
# AGC problems rarely require complex data structures like Segment Trees. 
# Instead, they describe a simple physical process: "You have an array. You can 
# choose any two adjacent numbers and replace them with their sum. Can you 
# reach target array X?"
#
# Standard BFS/DFS will instantly TLE (State Space Explosion). 
# DP is useless because the state transitions are chaotic.
#
# To solve an AGC problem, you must discover a "Mathematical Invariant" — a 
# property of the system that is physically impossible to change, no matter 
# what operations you perform. 
#
# If the starting array and the target array have different Invariants, the 
# answer is mathematically "NO" in O(1) time. No search required!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand Mathematical Invariants.
# - Solve a classic AGC-style Ad-Hoc Array Transformation problem.
#
# ==============================================================================
"""

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. MATHEMATICAL INVARIANTS (ARRAY TRANSFORMATION)
# ==============================================================================
def can_transform_array(start: list[int], target: list[int]) -> bool:
    """
    Problem: You are given an array `start`. In one operation, you can choose 
    any two adjacent elements `a` and `b`, and replace them with `(a + b)`. 
    You can do this infinitely many times. Can you transform `start` into `target`?
    
    Time Complexity: O(N)
    Space Complexity: O(1)
    """
    # 1. THE INVARIANT:
    # If you take [3, 4] and replace it with [7], what happened to the total sum?
    # Start: 3 + 4 = 7.
    # End: 7.
    # The total sum of the array is an INVARIANT! No matter how many operations 
    # you perform, you can never, ever change the total sum of the array.
    if sum(start) != sum(target):
        return False
        
    # 2. THE MONOTONICITY:
    # Because we are replacing two positive numbers with their sum, the array 
    # can only SHRINK in length. If `target` is longer than `start`, it's impossible!
    if len(target) > len(start):
        return False
        
    # 3. TWO POINTER GREEDY MATCHING:
    # Since we can only merge *adjacent* elements, we can iterate through the 
    # target array and greedily gobble up elements from the start array until 
    # they perfectly match the target element!
    p_start = 0
    
    for t_val in target:
        current_sum = 0
        
        # Greedily gobble adjacent elements from the start array
        while p_start < len(start) and current_sum < t_val:
            current_sum += start[p_start]
            p_start += 1
            
        # Did we perfectly hit the target value?
        if current_sum != t_val:
            # We overshot it! Because all numbers are positive, there is no way 
            # to "un-sum" or subtract. It is mathematically impossible.
            return False
            
    # If we made it through the entire target array without failing, it's True!
    return True

def demonstrate_invariants():
    section_header("AGC Ad-Hoc (Mathematical Invariants)")
    
    start = [1, 2, 3, 4, 5, 6]
    target = [3, 7, 11]
    
    print(f"Start Array : {start}")
    print(f"Target Array: {target}")
    
    # Simulation:
    # [1+2, 3+4, 5+6] -> [3, 7, 11]. It's perfectly valid!
    ans = can_transform_array(start, target)
    
    print(f"\nCan we reach the target? {ans}")
    print("Why? Because (1+2)=3, (3+4)=7, and (5+6)=11. The invariants perfectly aligned!")
    
    bad_target = [3, 8, 10]
    print(f"\nCan we reach {bad_target}? {can_transform_array(start, bad_target)}")
    print("Why? To make 8, we gobble (3+4)=7, which is too small. We gobble (3+4+5)=12, ")
    print("which is too big. We missed 8, so it is mathematically impossible.")


def run_all_labs():
    demonstrate_invariants()


# ==============================================================================
# 4. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. What is a "Mathematical Invariant" in the context of Game Theory and Array Transformations?
   Answer: An Invariant is a core property of a system that is mathematically immune to the allowed operations. If a problem allows you to swap any two elements, the "Sum of the Array" is an invariant. If a problem allows you to multiply a number by -1, the "Absolute Value" is an invariant. By identifying the invariant, you can completely bypass simulating the operations. If the starting state and the target state have different invariants, you instantly output "NO" in $O(1)$ time, avoiding an $O(2^N)$ DFS trap.

2. In the `can_transform_array` function, why does the Two-Pointer greedy matching guarantee the correct answer without needing to backtrack?
   Answer: Because the operations are strictly additive and the numbers are strictly positive! If you are trying to reach a target of `7`, and you add `3 + 4`, you hit `7`. Is there any alternate universe where it was a better idea to NOT merge `3` and `4`? No! Because you are forced to merge *adjacent* elements, and the target *requires* a `7` in that exact physical slot, you have no other choice. If you overshoot (`3 + 5 = 8`), there are no negative numbers available to bring the sum back down to `7`. The system is Monotonically Increasing. Therefore, greedy left-to-right matching is mathematically deterministic; there are no branching realities that require backtracking!

3. If the array contained NEGATIVE numbers, would the Greedy Two-Pointer algorithm still work?
   Answer: Absolutely not! The greedy algorithm relies on the fact that `current_sum` strictly increases. If `current_sum < t_val`, we know for a fact we MUST add the next number. But if negative numbers exist, adding the next number might actually *decrease* the sum! If we overshoot the target (`8 > 7`), we can't instantly return False, because the very next number might be `-1`, bringing us perfectly back to `7`. The introduction of negative numbers destroys the Monotonicity of the prefix sum, shattering the greedy proof and forcing the problem into a much harder DP or Graph Search domain.
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: AtCoder Grand Contest Completed.")
