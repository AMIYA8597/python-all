"""
# ==============================================================================
# LABORATORY: COMPETITIVE PROGRAMMING (CODECHEF LONG CHALLENGE)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# CodeChef Long Challenges (now defunct, but legendary for their style) were 
# 10-day marathons. The problems were not meant to be solved in 10 minutes. 
# They were heavily mathematical, often requiring you to discover obscure 
# Number Theory sequences (like Catalan numbers) or optimize an O(N^2) DP 
# into O(N) using Matrix Exponentiation.
#
# A hallmark of CodeChef is the "Subtask" system. 
# Subtask 1 (30 pts): N <= 1,000. (O(N^2) passes).
# Subtask 2 (70 pts): N <= 1,000,000. (O(N) required).
#
# In this lab, we will simulate a classic CodeChef Math problem:
# "Count the number of valid bracket sequences of length 2N."
#
# 2N can be up to 2,000,000. 
# You cannot generate the strings. You must use Catalan Numbers!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand CodeChef Subtasks and partial scoring.
# - Master Catalan Numbers for combinatorial geometry/strings.
# - Calculate Combinatorics in O(N) under a Modulo.
#
# ==============================================================================
"""

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")

MOD = 10**9 + 7

# ==============================================================================
# 3. CODECHEF SUBTASK 1 (O(N^2) DYNAMIC PROGRAMMING)
# ==============================================================================
def count_valid_brackets_subtask_1(n: int) -> int:
    """
    Subtask 1: N <= 1000.
    We can use a 2D DP array. dp[length][open_brackets_unclosed]
    Time Complexity: O(N^2)
    Space Complexity: O(N^2)
    """
    if n == 0: return 1
    
    # 2N characters total. Maximum possible unclosed brackets is N.
    length = 2 * n
    dp = [[0] * (n + 1) for _ in range(length + 1)]
    
    # Base Case: At length 0, we have 0 unclosed brackets. (1 valid way)
    dp[0][0] = 1
    
    for i in range(1, length + 1):
        for j in range(n + 1):
            # 1. We can append an OPEN bracket '('
            # This increases our unclosed count `j` by 1.
            # We can only do this if `j - 1` was a valid state in the previous step.
            if j > 0:
                dp[i][j] = (dp[i][j] + dp[i - 1][j - 1]) % MOD
                
            # 2. We can append a CLOSE bracket ')'
            # This decreases our unclosed count `j` by 1.
            # We can only do this if `j + 1` was a valid state in the previous step 
            # (and doesn't exceed N).
            if j < n:
                dp[i][j] = (dp[i][j] + dp[i - 1][j + 1]) % MOD
                
    # We want exactly 0 unclosed brackets at the very end of the string!
    return dp[length][0]


# ==============================================================================
# 4. CODECHEF SUBTASK 2 (O(N) CATALAN NUMBERS)
# ==============================================================================
class FastCombinatorics:
    def __init__(self, max_n: int):
        self.fact = [1] * (max_n + 1)
        self.inv_fact = [1] * (max_n + 1)
        for i in range(1, max_n + 1):
            self.fact[i] = (self.fact[i - 1] * i) % MOD
        self.inv_fact[max_n] = pow(self.fact[max_n], MOD - 2, MOD)
        for i in range(max_n - 1, -1, -1):
            self.inv_fact[i] = (self.inv_fact[i + 1] * (i + 1)) % MOD

    def nCr(self, n: int, k: int) -> int:
        if k < 0 or k > n: return 0
        ans = self.fact[n]
        ans = (ans * self.inv_fact[k]) % MOD
        ans = (ans * self.inv_fact[n - k]) % MOD
        return ans

def count_valid_brackets_subtask_2(n: int) -> int:
    """
    Subtask 2: N <= 1,000,000.
    The O(N^2) DP will instantly TLE.
    The answer is mathematically proven to be exactly the N-th Catalan Number!
    Catalan Formula: C(n) = (2n C n) / (n + 1)
    
    Time Complexity: O(N) to precompute factorials, then O(1) query.
    Space Complexity: O(N) for factorials.
    """
    if n == 0: return 1
    
    # Precompute factorials up to 2N
    combo = FastCombinatorics(2 * n)
    
    # Calculate (2n C n)
    ways = combo.nCr(2 * n, n)
    
    # Divide by (n + 1) using Modular Inverse!
    inverse_n_plus_1 = pow(n + 1, MOD - 2, MOD)
    
    catalan_number = (ways * inverse_n_plus_1) % MOD
    return catalan_number

def demonstrate_codechef_subtasks():
    section_header("CodeChef Subtasks (Catalan Math)")
    
    n = 3 # Length of string is 6. e.g. ((()))
    
    print(f"N = {n}. Total brackets = {2 * n}.")
    
    # Subtask 1
    ans_dp = count_valid_brackets_subtask_1(n)
    print(f"\nSubtask 1 [O(N^2) DP]: {ans_dp} valid sequences.")
    
    # Subtask 2
    ans_math = count_valid_brackets_subtask_2(n)
    print(f"Subtask 2 [O(1) Math] : {ans_math} valid sequences.")
    
    print("\nValid sequences for N=3 are exactly 5:")
    print("1. ((()))\n2. (()())\n3. (())()\n4. ()(())\n5. ()()()")
    
    print("\nIf N = 100,000, Subtask 1 runs 10 Billion operations and fails.")
    print("Subtask 2 runs instantly using pure combinatorics!")


def run_all_labs():
    demonstrate_codechef_subtasks()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. In the $O(N^2)$ DP for Subtask 1, why do we track `open_brackets_unclosed` (`j`) instead of just generating the raw string?
   Answer: State abstraction! A string like `((()` and a string like `()((` both have a length of 4, and both have exactly 2 unclosed opening brackets waiting for a match. For the purpose of adding future brackets, these two strings are *mathematically identical realities*. By grouping them purely by their `(Length, Unclosed_Count)`, we compress $2^{2N}$ chaotic string permutations into a tiny, manageable $O(N^2)$ matrix, radically dropping the complexity from Exponential to Polynomial.

2. What is a Catalan Number, and why does it perfectly model the Valid Parentheses problem?
   Answer: The Catalan Numbers (1, 1, 2, 5, 14, 42...) appear everywhere in Combinatorics where you have strict boundary limits (e.g., "Paths on a grid that never cross the diagonal" or "Triangulations of a polygon"). For parentheses, the strict limit is: "At no point in the string can the count of `)` exceed the count of `(`". The Catalan formula $C(n) = \frac{1}{n+1} \binom{2n}{n}$ calculates the total number of ways to pick $N$ slots for opening brackets out of $2N$ total slots, and then mathematically subtracts the exact number of invalid paths that violated the boundary condition.

3. In Subtask 2, how do we mathematically execute the division by `(n + 1)` under a Modulo $10^9+7$?
   Answer: Floating point division is mathematically illegal under a cyclic Modulo. `(A / B) % P` does not work. Instead, we must convert the division into multiplication using Fermat's Little Theorem. We find the Modular Multiplicative Inverse of `B` by calculating $B^{P-2} \pmod P$. For `(n + 1)`, we execute `pow(n + 1, MOD - 2, MOD)`. We then take our original combinatorics numerator, multiply it by this inverse, and take the modulo. This perfectly simulates division in a finite Galois Field!
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: CodeChef Long Challenge Completed.")
