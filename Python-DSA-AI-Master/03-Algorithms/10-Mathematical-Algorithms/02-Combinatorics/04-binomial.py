"""
Module: Binomial Coefficients

Learning Objectives:
1. Understand the definition and properties of binomial coefficients.
2. Implement Pascal's triangle.
3. Compute combinations modulo P efficiently using Fermat's Little Theorem.

Concept Explanation:
- Binomial coefficient C(n, k) represents the number of ways to pick k items from n items.
- C(n, k) = n! / (k! * (n - k)!)
- Pascal's identity: C(n, k) = C(n-1, k-1) + C(n-1, k)

Performance Analysis:
- DP (Pascal): O(n*k) time and space.
- Modular Arithmetic: O(n) precomputation, O(1) query time.

Edge Cases:
- k > n: Returns 0.
- k = 0 or k = n: Returns 1.
"""

# --- Basic Implementation ---
def binomial_basic(n: int, k: int) -> int:
    """Compute C(n, k) using Pascal's Triangle (O(n*k) space and time)."""
    if k > n or k < 0: return 0
    dp = [[0] * (k + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        for j in range(min(i, k) + 1):
            if j == 0 or j == i:
                dp[i][j] = 1
            else:
                dp[i][j] = dp[i - 1][j - 1] + dp[i - 1][j]
    return dp[n][k]

# --- Intermediate Implementation ---
def binomial_optimized(n: int, k: int) -> int:
    """Compute C(n, k) using optimized 1D DP array (O(k) space)."""
    if k > n or k < 0: return 0
    if k > n - k: k = n - k
    dp = [0] * (k + 1)
    dp[0] = 1
    for i in range(1, n + 1):
        for j in range(min(i, k), 0, -1):
            dp[j] = dp[j] + dp[j - 1]
    return dp[k]

# --- Advanced Implementation ---
class ModCombinatorics:
    """Computes C(n, k) % P efficiently using modular inverse."""
    def __init__(self, max_n: int, mod: int):
        self.mod = mod
        self.fact = [1] * (max_n + 1)
        self.inv = [1] * (max_n + 1)
        for i in range(1, max_n + 1):
            self.fact[i] = (self.fact[i - 1] * i) % mod
        
        # Fermat's Little Theorem for modular inverse: a^(p-2) % p
        self.inv[max_n] = pow(self.fact[max_n], mod - 2, mod)
        for i in range(max_n - 1, -1, -1):
            self.inv[i] = (self.inv[i + 1] * (i + 1)) % mod

    def ncr(self, n: int, k: int) -> int:
        if k > n or k < 0: return 0
        return (self.fact[n] * self.inv[k] % self.mod * self.inv[n - k] % self.mod)

# --- Interview Challenge ---
# Problem: Number of Paths in a Grid
# Find ways to reach (m-1, n-1) from (0, 0) moving only right or down.
def grid_paths(m: int, n: int) -> int:
    """The answer is C((m-1) + (n-1), m-1)."""
    return binomial_optimized(m + n - 2, m - 1)

# --- Tests ---
def run_tests():
    assert binomial_basic(5, 2) == 10
    assert binomial_optimized(5, 2) == 10
    
    mc = ModCombinatorics(100, 10**9 + 7)
    assert mc.ncr(5, 2) == 10
    assert mc.ncr(100, 50) == binomial_optimized(100, 50) % (10**9 + 7)
    
    assert grid_paths(3, 3) == 6
    print("All tests passed for 04-binomial.py!")

if __name__ == "__main__":
    run_tests()
