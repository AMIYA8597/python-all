"""
# ==============================================================================
# LABORATORY: COMPETITIVE PROGRAMMING (DIGIT DYNAMIC PROGRAMMING)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You are given a problem: "Count how many numbers between L and R have a 
# digit-sum equal to 10." 
# L and R can be up to $10^{18}$.
#
# If you run a `for` loop from L to R, casting each number to a string and 
# summing the digits, it will take $10^{18}$ operations. Your code will finish 
# executing in approximately 3,000 years. (Time Limit Exceeded).
#
# You must use Digit DP. Instead of iterating through the *values* of the 
# numbers, Digit DP iterates through the *positions* of the digits (from left 
# to right) like building a string. It reduces a $O(10^{18})$ search space down 
# to $O(\text{Number of Digits} \times \text{States})$, taking literally 0.001 seconds!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the architecture of Digit DP.
# - Master the `is_tight` boolean flag (The Boundary Enforcer).
# - Utilize Python's `@cache` to automatically memoize the digit states.
#
# ==============================================================================
"""

from functools import cache

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. DIGIT DP ARCHITECTURE
# ==============================================================================
def count_numbers_with_sum(L: int, R: int, target_sum: int) -> int:
    """
    Finds the number of integers in the range [L, R] whose digits sum to `target_sum`.
    Time Complexity: O(18 * 2 * 162) ~ O(1) Time! 
    Because max digits = 18, is_tight = 2, max sum = 9*18 = 162.
    """
    
    # 1. THE MATH TRICK (Prefix Subtraction)
    # Finding the answer for [L, R] is mathematically identical to finding the 
    # answer for [0, R] and subtracting the answer for [0, L - 1].
    # This completely eliminates the need to track a lower bound during the DP!
    
    def solve_for_upper_bound(bound_str: str) -> int:
        
        # 2. THE MEMOIZED DFS ENGINE
        @cache
        def dp(idx: int, is_tight: bool, current_sum: int) -> int:
            """
            idx: The current digit position (from left to right).
            is_tight: True if the prefix we've built so far EXACTLY matches `bound_str`.
            current_sum: The running sum of the digits we have placed so far.
            """
            
            # Base Case: We have successfully placed all digits!
            if idx == len(bound_str):
                return 1 if current_sum == target_sum else 0
                
            # If our sum already exceeds the target, mathematically impossible! Prune!
            if current_sum > target_sum:
                return 0
                
            # 3. DETERMINE THE DIGIT CEILING
            # If we are `tight`, we CANNOT place a digit larger than the upper bound.
            # Example: bound = "529". If we placed "5" in the hundreds place, 
            # the tens place CANNOT be > 2, otherwise we exceed 529!
            # If we are NOT `tight` (e.g., we placed "4" in the hundreds place),
            # we are mathematically guaranteed to be smaller than 529, so we 
            # can safely loop all the way up to 9!
            upper_limit = int(bound_str[idx]) if is_tight else 9
            
            total_valid_numbers = 0
            
            # 4. BRANCH INTO THE TREE (Place a digit from 0 up to the ceiling)
            for digit in range(upper_limit + 1):
                
                # We remain 'tight' ONLY IF we were already tight AND we picked 
                # the absolute maximum ceiling digit right now!
                next_tight = is_tight and (digit == upper_limit)
                
                total_valid_numbers += dp(
                    idx + 1, 
                    next_tight, 
                    current_sum + digit
                )
                
            return total_valid_numbers

        # Start at index 0, strictly 'tight' to the upper bound, with a sum of 0.
        return dp(0, True, 0)
        
    # Execute the Prefix Subtraction
    return solve_for_upper_bound(str(R)) - solve_for_upper_bound(str(L - 1))

def demonstrate_digit_dp():
    section_header("Digit Dynamic Programming")
    
    L = 10
    R = 1000
    target = 10
    
    print(f"Counting numbers in range [{L}, {R}] whose digits sum to {target}...")
    
    ans = count_numbers_with_sum(L, R, target)
    print(f"\nResult: {ans} numbers found!")
    
    print("\nIf you used a `for` loop to check numbers individually, ")
    print("it would have taken O(N) time. If R was 10^18, your computer would crash.")
    print("Digit DP solved it in exactly O(1) constant time because the ")
    print("search space is bound by the string length (18), not the integer value!")


def run_all_labs():
    demonstrate_digit_dp()


# ==============================================================================
# 4. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. In Digit DP, what does the boolean flag `is_tight` do, and why is it mandatory?
   Answer: The `is_tight` flag enforces the Upper Bound of the problem. If the absolute maximum bound is `314`, and we are currently choosing the tens digit, what is our maximum allowed choice? If the hundreds digit we chose was `3`, we are currently "tight" against the boundary. Choosing a tens digit $\ge 2$ would instantly exceed `314`. Therefore, if `is_tight == True`, our `upper_limit` is strictly restricted to `1`. However, if the hundreds digit we chose was `2`, we are mathematically guaranteed to be smaller than `314` no matter what we choose next! We are no longer "tight". If `is_tight == False`, our `upper_limit` instantly opens up to `9`, unlocking the entire search space.

2. Why do we solve the range $[L, R]$ by calculating $f(R) - f(L-1)$ instead of just passing both $L$ and $R$ into the DP state?
   Answer: State Bloat. If you pass both bounds into the DP, you must track two separate boolean flags: `is_tight_upper` and `is_tight_lower`. This makes the logic exceptionally complicated, doubling the surface area for bugs, and forcing complex `if` statements to handle lower-bound ceilings. By mathematically breaking it into Prefix Subtraction ($f(R) - f(L-1)$), the lower bound becomes mathematically exactly `0`. We completely eliminate the `is_tight_lower` flag from existence, making the DP state significantly cleaner and faster to code during a contest.

3. Explain the Time Complexity of Digit DP. Why does it execute in basically $O(1)$ time regardless of the size of $R$?
   Answer: The Time Complexity of Memoized DP is strictly bounded by the number of unique states. The state variables are `(index, is_tight, current_sum)`. For an astronomically large upper bound like $10^{18}$:
   - `index` ranges from $0$ to $18$.
   - `is_tight` is boolean (2 states).
   - The absolute maximum `current_sum` for an 18-digit number is $9 \times 18 = 162$.
   The absolute maximum number of states calculated is $18 \times 2 \times 162 = 5,832$. Evaluating $5,000$ states executes in literally 1 millisecond. Even if $R$ is $10^{100}$, it executes instantly. The time complexity is bound strictly by the *Logarithm Base 10* of $R$, not the value of $R$ itself!
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Digit Dynamic Programming Completed.")
