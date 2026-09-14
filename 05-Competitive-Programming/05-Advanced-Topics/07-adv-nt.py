"""
# ==============================================================================
# LABORATORY: COMPETITIVE PROGRAMMING (ADVANCED NUMBER THEORY)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You are asked to find the N-th Fibonacci number modulo 10^9+7.
# 
# If N is 100,000, you can use a simple O(N) `for` loop or O(N) Dynamic Programming.
# But what if N is 1,000,000,000,000,000,000 (10^18)?
# 
# An O(N) loop will literally take 30 years to compute on a modern processor.
#
# You cannot use Binet's Formula (the Golden Ratio) because floating-point 
# math loses absolute precision at massive scales, and irrational numbers do 
# not play nicely with cyclic Modulos.
#
# You must use Matrix Exponentiation. 
# By encoding the Fibonacci recurrence relation into a 2x2 Matrix, you can 
# use Binary Exponentiation to mathematically raise that matrix to the power 
# of 10^18 in exactly O(log N) time! 
# 
# 30 years of computation is reduced to exactly 60 operations.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand how to encode Linear Recurrences into Transition Matrices.
# - Master Matrix Multiplication under a Modulo.
# - Master Binary Matrix Exponentiation for O(log N) massive leaps.
#
# ==============================================================================
"""

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")

MOD = 10**9 + 7


# ==============================================================================
# 3. MATRIX EXPONENTIATION (FIBONACCI IN O(log N))
# ==============================================================================
def multiply_matrices(A: list[list[int]], B: list[list[int]]) -> list[list[int]]:
    """
    Multiplies two 2x2 Matrices under a Modulo.
    A = [[a, b], [c, d]]
    B = [[e, f], [g, h]]
    """
    # Initialize a 2x2 matrix with 0s
    C = [[0, 0], [0, 0]]
    
    # Standard Matrix Multiplication: Dot product of Rows of A and Cols of B
    for i in range(2):
        for j in range(2):
            for k in range(2):
                C[i][j] = (C[i][j] + A[i][k] * B[k][j]) % MOD
                
    return C

def power_matrix(M: list[list[int]], p: int) -> list[list[int]]:
    """
    Binary Exponentiation for Matrices!
    Raises a 2x2 Matrix `M` to the power of `p` in strictly O(log p) time.
    """
    # The Matrix equivalent of '1' is the Identity Matrix!
    res = [[1, 0], 
           [0, 1]]
           
    base = M
    
    while p > 0:
        # If the current power bit is 1, multiply the result by the base
        if p % 2 == 1:
            res = multiply_matrices(res, base)
            
        # Square the base matrix! (M^1 -> M^2 -> M^4 -> M^8)
        base = multiply_matrices(base, base)
        
        # Shift to the next bit
        p //= 2
        
    return res

def fast_fibonacci(n: int) -> int:
    """
    Calculates the N-th Fibonacci number in O(log N) time.
    Fibonacci Recurrence: F(N) = F(N-1) + F(N-2)
    
    The Transition Matrix `T`:
    | 1  1 |   | F(N-1) |   | F(N)   |
    | 1  0 | * | F(N-2) | = | F(N-1) |
    """
    if n == 0: return 0
    if n == 1: return 1
    
    # The magic Fibonacci Transition Matrix
    T = [[1, 1], 
         [1, 0]]
         
    # To get to F(N), we must multiply the starting state by T exactly (N-1) times!
    T_power = power_matrix(T, n - 1)
    
    # The starting state is a Column Vector:
    # | F(1) | = | 1 |
    # | F(0) | = | 0 |
    
    # Multiply the powered matrix by the starting state vector:
    # Final F(N) = T_power[0][0] * F(1) + T_power[0][1] * F(0)
    # Since F(1) = 1 and F(0) = 0, this mathematically simplifies to just T_power[0][0]!
    
    return T_power[0][0]

def demonstrate_matrix_exponentiation():
    section_header("Matrix Exponentiation (O(log N) Fibonacci)")
    
    n = 10**18 # 1 Quintillion!
    
    print(f"Target: Fibonacci Number N = {n} (One Quintillion)")
    print("An O(N) loop would take roughly 30 years to compute.")
    
    print("\nExecuting Binary Matrix Exponentiation...")
    ans = fast_fibonacci(n)
    
    print(f"F({n}) modulo 10^9+7 = {ans}")
    print("The O(log N) algorithm executed in exactly 60 loop iterations!")


def run_all_labs():
    demonstrate_matrix_exponentiation()


# ==============================================================================
# 4. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why does Binet's Formula (The Golden Ratio) fail for finding massive Fibonacci numbers in Competitive Programming?
   Answer: Binet's formula, $F(n) = \frac{\Phi^n - \Psi^n}{\sqrt{5}}$, relies heavily on the irrational number $\sqrt{5}$. As $N$ approaches $10^{18}$, calculating $\Phi^n$ requires floating-point variables (like `double` or `float64`). Floating-point variables mathematically lose precision after ~15 significant digits! They will silently round off the exact integer values, producing a catastrophically wrong answer. Furthermore, CP problems always ask for the answer "Modulo $10^9+7$". Floating-point numbers cannot mathematically be modulo'd accurately. Matrix Exponentiation stays strictly in the realm of 100% precise, bounded Integer Arithmetic.

2. Explain the fundamental logic behind the Transition Matrix: `[[1, 1], [1, 0]]`. How does it calculate the next state?
   Answer: We encode our current knowledge into a vector: `[F(n-1), F(n-2)]`. We want to create the next state vector: `[F(n), F(n-1)]`. 
   Let's look at the rows of the Transition Matrix:
   Row 0: `[1, 1]`. By dot-product rules, this multiplies `1 * F(n-1) + 1 * F(n-2)`. What is that? That is the exact mathematical definition of $F(n)$! It successfully generates the top element of the next vector!
   Row 1: `[1, 0]`. This multiplies `1 * F(n-1) + 0 * F(n-2)`. What is that? It is simply $F(n-1)$! It successfully shifts our previous data down to the bottom slot! 
   This matrix flawlessly executes the physical recurrence logic.

3. Explain how Binary Matrix Exponentiation drops the time complexity from $O(N)$ to $O(\log N)$.
   Answer: To get $F(100)$, you must multiply the Transition Matrix $T$ by itself 99 times ($T^{99}$). A naive `for` loop does exactly 99 multiplications. Binary Exponentiation exploits the mathematical law of exponents: $T^2 \times T^2 = T^4$. $T^4 \times T^4 = T^8$. By continuously squaring the matrix, we can leapfrog massively! To calculate $T^{64}$, we don't multiply 64 times; we square $T$ exactly 6 times ($2 \to 4 \to 8 \to 16 \to 32 \to 64$). By breaking the target power $99$ into its binary representation ($64 + 32 + 2 + 1$), we only need to multiply those specific squared matrices together. This drops the iterations strictly to $\log_2(N)$.
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Advanced Topics (Matrix Exponentiation) Completed.")
