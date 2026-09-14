"""
# ==============================================================================
# LABORATORY: COMPETITIVE PROGRAMMING (COMBINATORICS & MODULO)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You are asked to calculate "Out of 100,000 users, how many unique ways can 
# I choose exactly 50,000 of them?"
# 
# This is Combinations (nCr). The mathematical formula is N! / (K! * (N-K)!).
# The factorial of 100,000 has roughly 450,000 digits. If you attempt to 
# calculate this raw number, your computer's RAM will explode and Python's 
# BigInt math will trigger a Time Limit Exceeded (TLE) crash.
#
# The problem statement will say: "Return the answer modulo 10^9 + 7."
#
# You CANNOT use floating point division (`/`) under a modulo. It mathematically 
# breaks. You cannot use integer division (`//`) under a modulo. It also breaks.
# You must use Fermat's Little Theorem and the Modular Multiplicative Inverse 
# to mathematically convert the Division operation into a Multiplication operation!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the limits of massive factorials.
# - Master Combinatorics under a Prime Modulo (nCr % P).
# - Optimize multiple nCr queries using $O(N)$ Precomputed Factorial Arrays.
#
# ==============================================================================
"""

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")

# The standard Prime Modulo
MOD = 10**9 + 7


# ==============================================================================
# 3. COMBINATORICS (nCr % P) USING MODULAR INVERSE
# ==============================================================================
def nCr_single(n: int, k: int) -> int:
    """
    Calculates nCr % (10^9 + 7) for a single query.
    Time Complexity: O(N) to calculate factorials.
    """
    if k < 0 or k > n: return 0
    if k == 0 or k == n: return 1
    
    # 1. Calculate N! % MOD
    num = 1
    for i in range(1, n + 1):
        num = (num * i) % MOD
        
    # 2. Calculate K! % MOD
    den1 = 1
    for i in range(1, k + 1):
        den1 = (den1 * i) % MOD
        
    # 3. Calculate (N-K)! % MOD
    den2 = 1
    for i in range(1, (n - k) + 1):
        den2 = (den2 * i) % MOD
        
    # MATHEMATICAL TRAP! 
    # The formula is num / (den1 * den2).
    # But `(num / (den1 * den2)) % MOD` is ILLEGAL math.
    
    # SOLUTION: Modular Multiplicative Inverse (Fermat's Little Theorem)
    # Instead of dividing, we multiply by the INVERSE!
    # Inverse of X = pow(X, MOD - 2, MOD)
    # Python 3.8+ allows `pow(X, -1, MOD)`
    
    denominator = (den1 * den2) % MOD
    inverse_denominator = pow(denominator, MOD - 2, MOD)
    
    # Final step: Multiply Numerator by the Inverse Denominator!
    return (num * inverse_denominator) % MOD

def demonstrate_ncr_single():
    section_header("Single Query Combinatorics (nCr % P)")
    
    n = 5
    k = 2
    
    ans = nCr_single(n, k)
    print(f"{n} Choose {k} = {ans}")
    print("Expected: 10")
    

# ==============================================================================
# 4. O(1) COMBINATORICS FOR MASSIVE QUERIES
# ==============================================================================
class FastCombinatorics:
    """
    If a problem asks you to calculate nCr 100,000 times, the O(N) loop 
    in `nCr_single` will cause a TLE.
    We must precompute ALL factorials and ALL inverse factorials in O(MAX_N) time.
    After that, every nCr query evaluates in exactly O(1) time!
    """
    def __init__(self, max_n: int):
        self.max_n = max_n
        self.fact = [1] * (max_n + 1)
        self.inv_fact = [1] * (max_n + 1)
        
        # 1. Precompute Factorials: O(N)
        for i in range(1, max_n + 1):
            self.fact[i] = (self.fact[i - 1] * i) % MOD
            
        # 2. Precompute the Inverse of the MAXIMUM factorial: O(log MOD)
        # Using Fermat's Little Theorem!
        self.inv_fact[max_n] = pow(self.fact[max_n], MOD - 2, MOD)
        
        # 3. Backwards generation of all other inverses! O(N)
        # Math trick: 1/(N-1)! = (1/N!) * N
        for i in range(max_n - 1, -1, -1):
            self.inv_fact[i] = (self.inv_fact[i + 1] * (i + 1)) % MOD

    def nCr(self, n: int, k: int) -> int:
        """Returns nCr % MOD in exact O(1) time."""
        if k < 0 or k > n: return 0
        
        # Formula: N! * (1/K!) * (1/(N-K)!) % MOD
        ans = self.fact[n]
        ans = (ans * self.inv_fact[k]) % MOD
        ans = (ans * self.inv_fact[n - k]) % MOD
        
        return ans

def demonstrate_fast_combinatorics():
    section_header("O(1) Combinatorics (Precomputed Inverses)")
    
    # Precalculate factorials up to 100,000
    combinatorics = FastCombinatorics(100000)
    print("Precomputed 100,000 factorials and their inverses in O(N) time!")
    
    # O(1) Queries
    n1, k1 = 100000, 50000
    ans1 = combinatorics.nCr(n1, k1)
    
    print(f"\nQuery 1: {n1} Choose {k1} modulo {MOD} = {ans1}")
    print("If you tried to calculate the raw factorial of 100,000, Python would crash!")


def run_all_labs():
    demonstrate_ncr_single()
    demonstrate_fast_combinatorics()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why is calculating `(A / B) % P` completely illegal mathematically?
   Answer: Modulo arithmetic is cyclic and completely destroys linear magnitude. If $A = 10$, $B = 2$, and $P = 7$: True division yields $10 / 2 = 5$. If you apply the modulo to the numbers first, $A \% 7 = 3$, $B \% 7 = 2$. If you try to divide $3 / 2$, you get $1.5$. $1.5 \neq 5$. Division under a modulo is physically undefined. To mathematically divide by $B$ in a cyclic field, you must multiply by a number $X$ such that $(B \times X) \% P = 1$. This magical number $X$ is the Modular Multiplicative Inverse of $B$.

2. Explain Fermat's Little Theorem and how it finds the Modular Inverse in $O(\log P)$ time.
   Answer: Pierre de Fermat proved in 1640 that if $P$ is a Prime Number, $B^{P-1} \equiv 1 \pmod P$. By algebraically dividing both sides by $B$, we discover that the true mathematical inverse $B^{-1}$ is exactly equal to $B^{P-2} \pmod P$. To calculate this exponent, we do not need a billion iterations. Using Binary Exponentiation (which Python's `pow()` function natively uses), we can calculate any massive exponent in exactly $O(\log P)$ time. Since $P = 10^9+7$, $O(\log P)$ is roughly 30 operations!

3. In the `FastCombinatorics` class, why do we use a backwards loop to generate the inverses `inv_fact[i] = (inv_fact[i+1] * (i+1)) % MOD` instead of just calling `pow()` on every single number?
   Answer: Calling `pow()` takes $O(\log P)$ time. If we call it 100,000 times inside a `for` loop, it takes $100,000 \times 30 = 3,000,000$ operations. While fast, it is not optimal. The backwards loop utilizes a brilliant algebraic trick. If we already know the inverse of $10!$ ($\frac{1}{10!}$), how do we find the inverse of $9!$ ($\frac{1}{9!}$)? Algebraically, $\frac{1}{10!} \times 10 = \frac{10}{10 \times 9!} = \frac{1}{9!}$. By calculating `pow()` exactly *one single time* for the absolute largest factorial ($100,000!$), we can ripple backward with a simple $O(1)$ multiplication, completely calculating all 100,000 inverses in strict $O(N)$ linear time!
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Combinatorics & Modulo Completed.")
