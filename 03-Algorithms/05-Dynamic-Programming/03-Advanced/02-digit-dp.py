"""
# ==============================================================================
# LABORATORY: DIGIT DP (O(log N) COUNTING)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You are given an interview question: "Find how many numbers between L and R 
# have a digit sum exactly equal to K."
# E.g., Between 1 and 100, how many numbers have digits that sum to 5?
# (5, 14, 23, 32, 41, 50). Answer: 6.
#
# The naive approach is a `for` loop from L to R, casting each number to a string 
# and summing the characters.
# But what if R is 10^18 (One Quintillion)? The `for` loop will take 30+ years 
# to run on a modern CPU.
#
# Enter **Digit DP**.
# Instead of iterating through the NUMBERS, we iterate through the DIGITS.
# A number up to 10^18 only has 18 digits! 
# We can construct the numbers recursively, digit by digit, from left to right.
# This drops the Time Complexity from O(N) down to O(log10 N). 
# A 30-year loop finishes in 2 milliseconds.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the `tight` bound flag (The core of Digit DP).
# - State representation: `dp(index, tight, sum_so_far)`.
# - Solve counting problems mathematically.
#
# ==============================================================================
"""

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE DIGIT DP ENGINE (TOP-DOWN MEMOIZATION)
# ==============================================================================
def count_numbers_with_sum(R: str, target_sum: int) -> int:
    """
    Counts how many numbers from 0 to R have a digit sum exactly equal to `target_sum`.
    R is passed as a string so we can easily index into its digits!
    """
    
    # Memoization Cache
    # Key: (index, tight, current_sum)
    memo = {}
    
    def dp(index: int, tight: bool, current_sum: int) -> int:
        """
        `index`: Which digit we are currently placing (Left to Right).
        `tight`: True if the number we are building is currently EXACTLY matching 
                 the prefix of R. (If True, we are restricted on what digit we can pick).
        `current_sum`: The sum of the digits we have placed so far.
        """
        # 1. PRUNING
        # If the sum already exceeded the target, this path is dead.
        if current_sum > target_sum:
            return 0
            
        # 2. BASE CASE
        # If we reached the end of the string, we built a full number!
        # Does the sum match our target?
        if index == len(R):
            return 1 if current_sum == target_sum else 0
            
        # 3. MEMOIZATION CHECK
        state = (index, tight, current_sum)
        if state in memo:
            return memo[state]
            
        # 4. CALCULATE UPPER BOUND FOR THE CURRENT DIGIT
        # This is the MAGIC of Digit DP!
        # If `tight` is False, it means a previous digit we placed was SMALLER 
        # than the digit in R. We have officially diverged below the ceiling!
        # We can place ANY digit from 0 to 9.
        # But if `tight` is True, we are riding exactly on the ceiling limit.
        # We can only place digits from 0 up to `int(R[index])`.
        limit = int(R[index]) if tight else 9
        
        total_valid_numbers = 0
        
        # 5. RECURSIVE TRANSITION
        for digit in range(limit + 1):
            
            # Update the tight flag for the next recursive call.
            # It ONLY remains True if it was ALREADY True, AND we picked the 
            # absolute maximum limit digit!
            new_tight = tight and (digit == limit)
            
            new_sum = current_sum + digit
            
            total_valid_numbers += dp(index + 1, new_tight, new_sum)
            
        memo[state] = total_valid_numbers
        return total_valid_numbers

    # Start at index 0. `tight` is True because we haven't placed anything yet, 
    # so we are mathematically bound by the very first digit of R!
    return dp(0, True, 0)


def solve_range(L: int, R: int, target_sum: int) -> int:
    """
    To find the answer for the range [L, R], we use the Prefix Sum math trick:
    Count(0 to R) - Count(0 to L-1).
    """
    str_R = str(R)
    str_L_minus_1 = str(L - 1)
    
    count_R = count_numbers_with_sum(str_R, target_sum)
    count_L = count_numbers_with_sum(str_L_minus_1, target_sum)
    
    return count_R - count_L


def demonstrate_digit_dp():
    section_header("Algorithm: Digit DP (Sum of Digits)")
    
    target = 5
    L = 1
    R = 100
    
    print(f"Finding numbers between {L} and {R} where digits sum to {target}...")
    ans1 = solve_range(L, R, target)
    print(f"Result: {ans1} (Expected: 6 -> 5, 14, 23, 32, 41, 50)\n")
    
    target = 35
    L = 1
    R = 10**18 # One Quintillion!
    print(f"Finding numbers between {L} and {R} (1 Quintillion) where digits sum to {target}...")
    
    import time
    start = time.time()
    ans2 = solve_range(L, R, target)
    end = time.time()
    
    print(f"Result: {ans2}")
    print(f"Time Taken: {(end-start)*1000:.2f} milliseconds!")
    print("A naive for-loop would have taken over 30 years to calculate this.")


# ==============================================================================
# 4. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Explain the `tight` flag with an example.
   Answer: Imagine $R = 432$. We are picking the first digit. `tight=True`. We can only pick 0, 1, 2, 3, or 4. 
   - If we pick 4: We are still matching the prefix! `new_tight = True`. When picking the second digit, our limit is 3. We cannot pick 442!
   - If we pick 2: We broke away from the prefix! `new_tight = False`. When picking the second digit, our limit is 9. We CAN pick 299, because 299 is safely less than 432. The `tight` flag mathematically enforces the upper bound.

2. Why do we solve for $[L, R]$ by doing $Solve(R) - Solve(L-1)$?
   Answer: Digit DP is fundamentally designed to calculate ranges from $0$ to $X$. It is incredibly difficult to enforce both a Lower Bound and an Upper Bound simultaneously inside the recursive logic. By using the mathematical property of Prefix Sums, we just run the easy $0$ to $X$ algorithm twice and subtract the difference.

3. Why is the Time Complexity $O(\\text{Digits} \\times 2 \\times \\text{MaxSum})$?
   Answer: Memoization caches based on the unique states. 
   - `index` goes from 0 to 18 (for a Quintillion).
   - `tight` is 2 boolean values.
   - `current_sum` goes from 0 to roughly $9 \\times 18 = 162$.
   $18 \\times 2 \\times 162 = 5,832$ maximum states evaluated. The algorithm runs in strictly constant $O(1)$ time relative to the magnitude of the number, but $O(\\log N)$ relative to the number of digits.
"""

if __name__ == "__main__":
    demonstrate_digit_dp()
    print("\n[SUCCESS] Laboratory: Digit DP Completed.")
