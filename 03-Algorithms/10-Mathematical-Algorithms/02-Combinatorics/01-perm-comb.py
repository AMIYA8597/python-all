"""
# ==============================================================================
# LABORATORY: PERMUTATIONS & COMBINATIONS (O(1) nCr)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Combinatorics is the mathematical study of counting. 
# "How many ways can I choose 5 players from a team of 11?" (Combinations).
# "How many ways can 5 people sit in 5 chairs?" (Permutations).
#
# The math formulas are well known:
# Permutations (nPr) = n! / (n - r)!
# Combinations (nCr) = n! / (r! * (n - r)!)
#
# But there is a massive problem in Computer Science: Factorials grow explosively.
# 20! is $2.4 \times 10^{18}$ (almost exceeding a 64-bit integer).
# 100! has 158 digits.
#
# If a problem asks you to calculate nCr for $N = 1,000,000$, the number $1,000,000!$ 
# physically cannot fit in the RAM of your computer.
# 
# Therefore, almost all Combinatorics algorithms require you to output the answer 
# modulo $10^9 + 7$.
#
# But remember the Modulo Mathematics lab? DIVISION IS ILLEGAL in modular arithmetic!
# You CANNOT calculate: ( n! % M ) / ( r! % M ).
#
# The Solution: Inverse Factorials!
# We use Fermat's Little Theorem to pre-calculate the Modular Multiplicative 
# Inverse of every factorial! 
# Formula: nCr % M = ( fact[n] * inv_fact[r] * inv_fact[n - r] ) % M.
#
# By pre-calculating the factorials and inverse factorials in an array in O(N) time, 
# we can answer an INFINITE number of nCr queries in strict O(1) time!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the explosion of Factorials.
# - Pre-compute Factorials and Inverse Factorials in O(N).
# - Execute nCr and nPr queries in O(1) time.
#
# ==============================================================================
"""

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. O(N) COMBINATORICS ENGINE (MODULAR INVERSE FACTORIALS)
# ==============================================================================
class CombinatoricsEngine:
    def __init__(self, max_n: int, mod: int = 1000000007):
        self.mod = mod
        self.max_n = max_n
        
        # 1. PRE-COMPUTE FACTORIALS
        self.fact = [1] * (max_n + 1)
        for i in range(2, max_n + 1):
            # n! = (n * (n-1)!) % M
            self.fact[i] = (self.fact[i - 1] * i) % self.mod
            
        # 2. PRE-COMPUTE INVERSE FACTORIALS
        self.inv_fact = [1] * (max_n + 1)
        
        # We only need to calculate the inverse for the absolute LARGEST factorial 
        # using Fermat's Little Theorem! (O(log M) time).
        # Fermat: Inverse of X = pow(X, M-2, M)
        self.inv_fact[max_n] = pow(self.fact[max_n], self.mod - 2, self.mod)
        
        # Now, we use a brilliant mathematical trick to calculate all smaller inverses 
        # iteratively going backwards in strict O(1) time each!
        # Math: 1 / (N-1)! = N / N!
        for i in range(max_n - 1, 0, -1):
            self.inv_fact[i] = (self.inv_fact[i + 1] * (i + 1)) % self.mod

    def nCr(self, n: int, r: int) -> int:
        """
        Calculates n Choose r in O(1) time.
        n! / (r! * (n-r)!)
        """
        if r < 0 or r > n:
            return 0
            
        # Modulo Multiplication: (fact[n] * inv_fact[r] * inv_fact[n-r]) % M
        numerator = self.fact[n]
        denominator_inv = (self.inv_fact[r] * self.inv_fact[n - r]) % self.mod
        
        return (numerator * denominator_inv) % self.mod

    def nPr(self, n: int, r: int) -> int:
        """
        Calculates n Permute r in O(1) time.
        n! / (n-r)!
        """
        if r < 0 or r > n:
            return 0
            
        return (self.fact[n] * self.inv_fact[n - r]) % self.mod
        
    def catalan(self, n: int) -> int:
        """
        The N-th Catalan Number.
        Formula: (2n)! / ((n+1)! * n!)
        Equivalently: (1 / (n+1)) * (2n C n)
        Extremely common in combinatorics (Valid parentheses, BST structures, etc).
        """
        if n < 0: return 0
        
        # We can just use our O(1) nCr function!
        base_nCr = self.nCr(2 * n, n)
        
        # We must divide by (n+1). In modular math, we multiply by the modular inverse!
        inv_n_plus_1 = pow(n + 1, self.mod - 2, self.mod)
        
        return (base_nCr * inv_n_plus_1) % self.mod


def demonstrate_combinatorics():
    section_header("Algorithm: O(1) Modular nCr")
    
    # Let's support calculations up to N = 1,000,000
    print("Pre-computing 1 Million Factorials & Inverses in O(N)...")
    engine = CombinatoricsEngine(max_n=1000000)
    
    n, r = 1000, 500
    print(f"\nCalculating {n} Choose {r} modulo 10^9+7...")
    ans = engine.nCr(n, r)
    print(f"Result: {ans}")
    
    section_header("Algorithm: The Catalan Numbers")
    
    print("How many valid sequences of 3 pairs of parentheses exist?")
    print("Example: '((()))', '()()()', '(())()', '()(())', '(()())'")
    ans_catalan = engine.catalan(3)
    print(f"Calculated using 3rd Catalan number: {ans_catalan}")
    
    print("\nFirst 10 Catalan Numbers:")
    catalans = [engine.catalan(i) for i in range(10)]
    print(catalans)


# ==============================================================================
# 4. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why does the `inv_fact` array loop backwards?
   Answer: Fermat's Little Theorem `pow(X, M-2, M)` takes $O(\log M)$ time. If we ran it for all $N$ elements, the pre-computation would take $O(N \log M)$ time, which is slow. However, look at the mathematics of inverse factorials: 
   $\frac{1}{(N-1)!} = \frac{N}{N!}$. 
   If we ALREADY know the inverse of $N!$, we can mathematically calculate the inverse of $(N-1)!$ just by multiplying it by $N$! 
   Therefore, we only pay the $O(\log M)$ cost EXACTLY ONCE for the absolute maximum element `max_n`. Then we loop backwards, multiplying by $N$ to generate all smaller inverses in strict $O(1)$ time each! The total pre-compute drops to $O(N)$.

2. What is the difference between Permutations and Combinations?
   Answer: "Order matters". 
   - A Permutation (nPr) is a password. The sequence `[1, 2, 3]` is completely different from `[3, 2, 1]`. 
   - A Combination (nCr) is a salad. A bowl containing `[lettuce, tomato, onion]` is the exact same salad as `[onion, tomato, lettuce]`. 
   Because combinations remove all the duplicated orderings, the combination formula mathematically divides the permutation formula by $r!$ (the number of ways to arrange the chosen items).

3. Where do Catalan numbers appear in computer science?
   Answer: They are the God-Equation of Recursive Tree structures. 
   - How many structurally unique Binary Search Trees can you build with $N$ nodes? (Catalan $N$).
   - How many ways can you perfectly balance $N$ pairs of parentheses? (Catalan $N$).
   - How many ways can you cut an $N$-sided polygon into triangles? (Catalan $N-2$).
   - How many paths exist on an $N \times N$ grid from bottom-left to top-right without crossing the diagonal? (Catalan $N$).
"""

if __name__ == "__main__":
    demonstrate_combinatorics()
    print("\n[SUCCESS] Laboratory: Permutations & Combinations Completed.")
