"""
===========================================================================
Python DSA Masterclass: Digit Dynamic Programming (Digit DP)
===========================================================================

## 1. Introduction to Digit DP

Digit Dynamic Programming (Digit DP) is a powerful paradigm used to count
the number of integers in a given range [L, R] that satisfy a certain
property. A naive approach of iterating from L to R takes O(R - L) time,
which is unfeasible when R can be up to 10^18 (or even larger, up to 10^10000).

Digit DP solves this by iterating over the *digits* of the number from
left to right (most significant digit to least significant digit) and
building the number digit by digit.

Instead of O(R) time, the complexity becomes proportional to the number
of digits, typically O(D * S) where D is the number of digits (log10(R))
and S is the number of states we need to track.

## 2. The Core State of Digit DP

The hallmark of a Digit DP problem is the state tuple. A standard state
looks like this:
    `dp(idx, is_tight, is_leading_zero, *custom_states)`

1. **idx (Index)**: 
   The current position we are filling in the number (from left to right).
   If the maximum number has D digits, `idx` ranges from 0 to D-1.

2. **is_tight (Boolean)**:
   This flag indicates if the prefix we have built so far is exactly equal
   to the prefix of the upper bound `R`.
   - If `is_tight == True`: The next digit cannot exceed the corresponding
     digit in `R`. (e.g., if R = "456" and we have built "4", the next
     digit can at most be 5).
   - If `is_tight == False`: We have already placed a digit smaller than
     the corresponding digit in `R`. The remaining digits can be anything
     from 0 to 9.

3. **is_leading_zero (Boolean)** (Optional but common):
   Tracks if all digits placed so far are zero. This is crucial for problems
   where leading zeros affect the property (e.g., counting the number of
   times the digit '0' appears).

4. **custom_states**:
   Problem-specific variables, such as:
   - Sum of digits modulo K.
   - The actual value modulo K.
   - The previous digit placed.
   - Count of a specific digit.

## 3. Mathematical Background and Transitions

Let the upper bound N be represented as a string of digits S = S_0 S_1 ... S_{D-1}.
We define a recursive function `solve(idx, tight, ...)` returning the count
of valid completions.

The transition explores all valid digits `d` for the current `idx`:
   limit = int(S[idx]) if tight else 9
   
   for d in range(0, limit + 1):
       new_tight = tight and (d == limit)
       ans += solve(idx + 1, new_tight, ...)

By memoizing this function (using dynamic programming/caching), we ensure
each state is evaluated only once.

## 4. Range Queries [L, R]

To answer queries for a range [L, R], we use the prefix sum property:
   Count(L, R) = Count(0, R) - Count(0, L - 1)
Thus, we only ever need to compute the answer for numbers up to an upper bound X.

===========================================================================
"""

from typing import Dict, List, Tuple
from functools import lru_cache

# ============================================================================
# Concept 1: Basic Digit DP - Sum of Digits
# ============================================================================

def count_numbers_with_sum_limit(upper_bound: int, target_sum: int) -> int:
    """
    Problem: Count how many numbers x in [0, upper_bound] have a digit sum
    exactly equal to `target_sum`.

    Mathematical State:
    - `idx`: Current digit position.
    - `is_tight`: Is the prefix matching the upper bound?
    - `current_sum`: The sum of digits chosen so far.

    Base Case:
    - If `idx == len(str_N)`: return 1 if `current_sum == target_sum` else 0.
    
    Time Complexity:
    - Number of states = D (length of upper_bound) * 2 (is_tight) * (9*D) (max possible sum)
    - Transition = O(10) per state
    - Overall: O(10 * D^2 * 2), where D is the number of digits in `upper_bound`.
      For upper_bound = 10^18, D=18. 10 * 324 * 2 = 6480 operations. Blazing fast!

    Space Complexity:
    - O(D^2) to store the memoization table.
    """
    if upper_bound < 0:
        return 0

    s = str(upper_bound)
    n = len(s)

    # We use a dictionary for explicit memoization to show the inner workings,
    # though Python's @lru_cache is often easier.
    memo: Dict[Tuple[int, bool, int], int] = {}

    def dp(idx: int, is_tight: bool, current_sum: int) -> int:
        # Pruning: If the sum exceeds the target, no need to continue.
        if current_sum > target_sum:
            return 0

        # Base case: We have filled all digits.
        if idx == n:
            return 1 if current_sum == target_sum else 0

        # Check memoization table
        state = (idx, is_tight, current_sum)
        if state in memo:
            return memo[state]

        # Determine the upper limit for the current digit
        limit = int(s[idx]) if is_tight else 9
        
        total_valid = 0
        
        # Try placing all valid digits
        for digit in range(limit + 1):
            new_tight = is_tight and (digit == limit)
            total_valid += dp(idx + 1, new_tight, current_sum + digit)

        # Memoize and return
        memo[state] = total_valid
        return total_valid

    return dp(0, True, 0)

# ============================================================================
# Concept 2: Range Queries and Modulo Arithmetic
# ============================================================================

def count_divisible_by_k_in_range(L: int, R: int, K: int) -> int:
    """
    Problem: Find the number of integers in [L, R] that are divisible by K.
    Assume K is relatively small (e.g., K <= 100).
    
    We solve this by finding f(R) - f(L-1), where f(X) counts numbers <= X
    that are divisible by K.

    Mathematical State:
    - `idx`: Current digit position.
    - `is_tight`: Tight flag.
    - `rem`: Current remainder of the number modulo K.

    Transition:
    - If we place digit `d`, the new number in base 10 shifts left and adds `d`.
    - new_rem = (rem * 10 + d) % K
    """
    if K == 0:
        raise ValueError("K cannot be zero")

    def count_up_to(limit_val: int) -> int:
        if limit_val < 0:
            return 0
            
        s = str(limit_val)
        n = len(s)
        
        @lru_cache(maxsize=None)
        def dp(idx: int, is_tight: bool, rem: int) -> int:
            if idx == n:
                return 1 if rem == 0 else 0
                
            upper_digit = int(s[idx]) if is_tight else 9
            ans = 0
            
            for digit in range(upper_digit + 1):
                ans += dp(
                    idx + 1, 
                    is_tight and (digit == upper_digit), 
                    (rem * 10 + digit) % K
                )
                
            return ans
            
        return dp(0, True, 0)

    # Prefix sum logic for ranges
    return count_up_to(R) - count_up_to(L - 1)

# ============================================================================
# Concept 3: Dealing with Leading Zeros
# ============================================================================

def count_digit_occurrences(L: int, R: int, target_digit: int) -> int:
    """
    Problem: Count the total number of times `target_digit` appears in all 
    numbers from L to R inclusive.
    
    Why leading zero matters:
    If we are counting occurrences of the digit '0', a number like "005"
    represents "5". We should NOT count the leading zeros.
    Thus, we need an `is_leading_zero` flag.

    Mathematical State:
    - `idx`: Current digit position.
    - `is_tight`: Tight flag.
    - `is_leading_zero`: True if all previous digits were 0.
    - `count`: How many times target_digit has appeared so far.
    """
    def count_up_to(limit_val: int) -> int:
        if limit_val < 0:
            return 0
            
        s = str(limit_val)
        n = len(s)
        
        @lru_cache(maxsize=None)
        def dp(idx: int, is_tight: bool, is_leading_zero: bool, count: int) -> int:
            if idx == n:
                return count
                
            upper_digit = int(s[idx]) if is_tight else 9
            ans = 0
            
            for digit in range(upper_digit + 1):
                new_tight = is_tight and (digit == upper_digit)
                new_leading_zero = is_leading_zero and (digit == 0)
                
                # Check if we should increment the count.
                # If target_digit is 0, we only count it if it's NOT a leading zero.
                increment = 0
                if digit == target_digit:
                    if target_digit != 0 or not new_leading_zero:
                        increment = 1
                        
                ans += dp(idx + 1, new_tight, new_leading_zero, count + increment)
                
            return ans
            
        return dp(0, True, True, 0)

    return count_up_to(R) - count_up_to(L - 1)

# ============================================================================
# Concept 4: Complex Inter-digit Constraints
# ============================================================================

def count_stepper_numbers(L: int, R: int) -> int:
    """
    Problem: A "stepper number" is a number where the absolute difference
    between every adjacent pair of digits is exactly 1.
    For example, 1234, 3234, 989 are stepper numbers.
    Single digit numbers are also stepper numbers.
    Find the number of stepper numbers in [L, R].

    Mathematical State:
    - `idx`: Current digit.
    - `is_tight`: Tight flag.
    - `is_leading_zero`: True if the number hasn't started yet.
    - `prev_digit`: The previous digit placed (0-9). If is_leading_zero is true,
                    this can be any sentinel value (e.g., -1).
    """
    def count_up_to(limit_val: int) -> int:
        if limit_val < 0:
            return 0
            
        s = str(limit_val)
        n = len(s)
        
        @lru_cache(maxsize=None)
        def dp(idx: int, is_tight: bool, is_leading_zero: bool, prev_digit: int) -> int:
            if idx == n:
                # If the number is entirely zeros (and limit > 0), 0 is a stepper number.
                # Usually 0 is considered single-digit, so it's a stepper number.
                return 1
                
            upper_digit = int(s[idx]) if is_tight else 9
            ans = 0
            
            for digit in range(upper_digit + 1):
                new_tight = is_tight and (digit == upper_digit)
                new_leading_zero = is_leading_zero and (digit == 0)
                
                # If we are just starting out (leading zeros), any digit is valid
                if is_leading_zero:
                    ans += dp(idx + 1, new_tight, new_leading_zero, digit)
                else:
                    # If the number has started, the adjacent difference must be 1
                    if abs(digit - prev_digit) == 1:
                        ans += dp(idx + 1, new_tight, new_leading_zero, digit)
                        
            return ans
            
        return dp(0, True, True, -1)

    return count_up_to(R) - count_up_to(L - 1)

# ============================================================================
# Real World Applications
# ============================================================================
# 1. Telecommunications: Validating and counting block pools of mobile numbers 
#    that follow specific geographic patterns or routing logic constraints.
# 2. Database Key Generation: Computing uniform distributions of hashed primary 
#    keys within a sharded environment, specifically keys ending in particular digits.
# 3. Cryptography & Hash Checks: Fast evaluation of properties on immense numerical
#    spaces, such as locating pseudoprime gaps.

# ============================================================================
# Test Suite
# ============================================================================

def run_tests():
    print("Running Digit DP Masterclass tests...")
    
    # 1. Basic Sum Limit
    # Numbers up to 20 with sum of digits = 2 -> 2, 11, 20 (3 numbers)
    assert count_numbers_with_sum_limit(20, 2) == 3
    # Numbers up to 10 with sum of digits = 1 -> 1, 10 (2 numbers)
    assert count_numbers_with_sum_limit(10, 1) == 2

    # 2. Divisible by K
    # Divisible by 2 between 10 and 20: 10, 12, 14, 16, 18, 20 (6 numbers)
    assert count_divisible_by_k_in_range(10, 20, 2) == 6
    # Divisible by 3 between 10 and 20: 12, 15, 18 (3 numbers)
    assert count_divisible_by_k_in_range(10, 20, 3) == 3
    
    # 3. Digit Occurrences
    # Occurrences of '1' from 1 to 15: 1, 10, 11 (two 1s), 12, 13, 14, 15 -> Total: 8
    assert count_digit_occurrences(1, 15, 1) == 8
    # Occurrences of '0' from 1 to 20: 10, 20 -> Total: 2
    assert count_digit_occurrences(1, 20, 0) == 2
    
    # 4. Stepper Numbers
    # Stepper numbers between 10 and 20: 10, 12. (11 is not, diff=0). (21 is out of range).
    assert count_stepper_numbers(10, 20) == 2
    # Stepper numbers between 0 and 9: all 10 single digit numbers.
    assert count_stepper_numbers(0, 9) == 10

    # 5. Massive Scale Test
    # This demonstrates the power of Digit DP. 
    # Counting numbers up to 10^18 with sum of digits = 50.
    # Brute force would take thousands of years. Digit DP takes < 1ms.
    huge_ans = count_numbers_with_sum_limit(10**18, 50)
    assert huge_ans > 0
    print(f"Numbers up to 10^18 with sum of digits 50: {huge_ans}")

    print("All tests passed successfully! You are now a Digit DP Master.")

if __name__ == "__main__":
    run_tests()
