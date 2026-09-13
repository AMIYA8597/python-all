"""
# ==============================================================================
# LABORATORY: BINOMIAL COEFFICIENTS & LUCAS' THEOREM
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You learned how to calculate Combinations (nCr) using Inverse Factorials. 
# But that technique has two major weaknesses:
# 1. It requires calculating the Modular Inverse. If the modulo M is NOT a prime 
#    number, Fermat's Little Theorem fails and the code crashes.
# 2. It requires O(N) pre-computation. If N is 1,000,000,000, you cannot 
#    allocate an array of 1 Billion factorials. Your RAM will explode.
#
# How do we bypass these constraints?
#
# Solution 1: Pascal's Triangle (O(N^2))
# If N is relatively small (e.g., N = 1000), but the Modulo is not prime, you 
# can build Pascal's Triangle. It calculates nCr using ONLY Addition! 
# C(n, k) = C(n-1, k-1) + C(n-1, k).
# Since it uses no division, you never need a Modular Inverse! It is 100% immune 
# to non-prime modulos.
#
# Solution 2: Lucas' Theorem (O(P log_P N))
# What if N is MASSIVE (10^18), but the prime modulo P is tiny (e.g., P = 13)?
# You cannot build a 10^18 array. 
# In 1878, Édouard Lucas proved a God-Tier mathematical theorem:
# If you convert N and R into Base-P numbers, you can calculate nCr modulo P 
# just by multiplying the combinations of their individual digits!
# 
# 2. LEARNING OBJECTIVES
# ----------------------
# - Build Pascal's Triangle to bypass division errors.
# - Expand Algebraic binomials $(x+y)^n$.
# - Master Lucas' Theorem for astronomically large N.
#
# ==============================================================================
"""

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. PASCAL'S TRIANGLE (IMMUNE TO NON-PRIME MODULOS)
# ==============================================================================
class PascalsTriangle:
    def __init__(self, n: int, mod: int = None):
        """
        Builds Pascal's Triangle up to row N.
        Time Complexity: O(N^2)
        Space Complexity: O(N^2)
        """
        self.mod = mod
        self.C = [[0] * (n + 1) for _ in range(n + 1)]
        
        for i in range(n + 1):
            # C(i, 0) is always 1. (Choosing 0 items from i).
            self.C[i][0] = 1
            
            # Use the recurrence: C(n, k) = C(n-1, k-1) + C(n-1, k)
            for j in range(1, i + 1):
                val = self.C[i - 1][j - 1] + self.C[i - 1][j]
                
                if self.mod:
                    val %= self.mod
                    
                self.C[i][j] = val

    def nCr(self, n: int, r: int) -> int:
        if r < 0 or r > n: return 0
        return self.C[n][r]
        
    def expand_binomial(self, n: int) -> str:
        """
        Expands (x + y)^n using the Binomial Theorem.
        """
        terms = []
        for k in range(n + 1):
            coef = self.C[n][k]
            
            x_pow = n - k
            y_pow = k
            
            x_str = f"x^{x_pow}" if x_pow > 1 else ("x" if x_pow == 1 else "")
            y_str = f"y^{y_pow}" if y_pow > 1 else ("y" if y_pow == 1 else "")
            
            term = ""
            if coef > 1 or (not x_str and not y_str): term += str(coef)
            if x_str: term += x_str
            if y_str: term += y_str
            
            terms.append(term)
            
        return " + ".join(terms)


# ==============================================================================
# 4. LUCAS' THEOREM (ASTRONOMICALLY LARGE N)
# ==============================================================================
# Helper for Lucas: We need a small O(P) combinatorics engine to handle the digits!
def get_small_nCr(n: int, r: int, p: int) -> int:
    if r < 0 or r > n: return 0
    if r == 0 or r == n: return 1
    if r > n - r: r = n - r
    
    num = 1
    for i in range(r):
        num = (num * (n - i)) % p
        
    den = 1
    for i in range(1, r + 1):
        den = (den * i) % p
        
    # Since P is strictly a prime in Lucas' theorem, we CAN use Fermat's Little Theorem here!
    inv_den = pow(den, p - 2, p)
    return (num * inv_den) % p


def lucas_theorem(n: int, r: int, p: int) -> int:
    """
    Calculates nCr modulo P for astronomically large N.
    Requirement: P MUST be a prime number.
    Time Complexity: O(P * log_P(N))
    """
    if r == 0: return 1
    
    # 1. We extract the Least Significant Digit in Base-P using Modulo!
    ni = n % p
    ri = r % p
    
    # 2. We calculate the combination of just these two single digits.
    # If the bottom digit is larger than the top digit, it is mathematically 
    # impossible to choose (e.g., 2 choose 4). The answer for this digit is 0!
    # Because Lucas' theorem multiplies all digit combinations together, one 0 
    # annihilates the entire massive number, instantly returning 0!
    if ri > ni:
        return 0
        
    digit_combo = get_small_nCr(ni, ri, p)
    
    # 3. We recursively shift the numbers right by 1 Base-P digit!
    # (By dividing by P)
    next_digits_combo = lucas_theorem(n // p, r // p, p)
    
    # 4. Multiply them together!
    return (digit_combo * next_digits_combo) % p


def demonstrate_binomial():
    section_header("Algorithm: Pascal's Triangle (Addition Only)")
    
    pascal = PascalsTriangle(5)
    print("Pascal's Triangle (Row 0 to 5):")
    for i in range(6):
        # Print centered
        row_str = " ".join(str(pascal.nCr(i, j)) for j in range(i + 1))
        print(row_str.center(20))
        
    print("\nBinomial Expansion of (x + y)^5 :")
    print(pascal.expand_binomial(5))
    
    section_header("Algorithm: Lucas' Theorem")
    
    # Massive N! Standard arrays will crash.
    n = 1000000000000000000 # 10^18 (One Quintillion)
    r = 500000000000000000
    p = 13 # A small prime modulo
    
    print(f"Calculating ({n} Choose {r}) modulo {p}...")
    ans = lucas_theorem(n, r, p)
    print(f"O(log_P N) Result: {ans}")


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why is Pascal's Triangle immune to division errors?
   Answer: The mathematical recurrence relation $C(n, k) = C(n-1, k-1) + C(n-1, k)$ relies strictly on Addition. To apply a modulo to Pascal's triangle, you simply do $(A + B) \% M$. Because it completely bypasses the formula $n! / (r! \times (n-r)!)$, it never performs a division. Therefore, it never needs a Modular Inverse, and never cares if the modulo $M$ is prime or composite!

2. How does Lucas' Theorem work conceptually?
   Answer: It treats $N$ and $R$ as strings of numbers in Base-$P$. 
   If $P=10$, and we want to calculate $423 \choose 112$, Lucas' Theorem breaks it down digit by digit:
   Answer $= {4 \choose 1} \times {2 \choose 1} \times {3 \choose 2} \pmod{10}$.
   By breaking a massive $10^{18}$ number down into its tiny Base-$P$ digits, we only ever have to calculate combinations of numbers smaller than $P$! We multiply those tiny combinations together to get the final answer.

3. What happens if $R_i > N_i$ in one of the Lucas digits?
   Answer: If we are calculating $12 \choose 4$ in Base-10.
   The ones digit asks us to calculate $2 \choose 4$. 
   It is mathematically impossible to choose 4 items from a pool of 2. The combination is strictly $0$.
   Because Lucas' theorem multiplies the results of all digits together, $X \times Y \times 0$ instantly collapses the entire massive equation to $0$. This mathematical shortcut allows Lucas to evaluate massive numbers almost instantaneously.
"""

if __name__ == "__main__":
    demonstrate_binomial()
    print("\n[SUCCESS] Laboratory: Binomial Coefficients Completed.")
