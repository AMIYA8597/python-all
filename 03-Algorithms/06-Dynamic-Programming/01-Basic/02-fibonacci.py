"""
# ==============================================================================
# LABORATORY: FIBONACCI (THE O(LOG N) MATRIX EXPONENTIATION MIRACLE)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# By now, you know how to calculate the N-th Fibonacci number.
# - Naive Recursion: O(2^N) Time, O(N) Space
# - Top-Down Memoization: O(N) Time, O(N) Space
# - Bottom-Up Tabulation: O(N) Time, O(N) Space
# - Space-Optimized Sliding Window: O(N) Time, O(1) Space
#
# So, $O(N)$ Time and $O(1)$ Space is the absolute mathematical limit, right?
# Wrong. 
#
# If a Quantitative Trading firm asks you to calculate the 10 Billionth Fibonacci 
# number, an $O(N)$ `for` loop will take 10 Billion iterations. That takes several 
# seconds. In HFT (High-Frequency Trading), a microsecond delay loses millions.
#
# We can calculate Fibonacci in **O(log N)** Time!
# We use **Matrix Exponentiation**. 
# We model the Fibonacci transition as a 2x2 Matrix. By using Binary Exponentiation 
# on the matrix, we can instantly jump billions of steps ahead mathematically 
# without looping through them!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the Fibonacci Matrix `[[1, 1], [1, 0]]`.
# - Master Binary Exponentiation (Fast Power algorithm).
# - Shatter the O(N) linear time barrier.
#
# ==============================================================================
"""

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. MATRIX EXPONENTIATION ENGINE (O(log N))
# ==============================================================================
def multiply_matrices(A, B):
    """
    Multiplies two 2x2 matrices together in O(1) Time.
    """
    a = A[0][0]*B[0][0] + A[0][1]*B[1][0]
    b = A[0][0]*B[0][1] + A[0][1]*B[1][1]
    c = A[1][0]*B[0][0] + A[1][1]*B[1][0]
    d = A[1][0]*B[0][1] + A[1][1]*B[1][1]
    
    return [[a, b], [c, d]]

def matrix_power(matrix, p):
    """
    Raises a 2x2 matrix to the power `p` in O(log P) Time!
    This uses the "Binary Exponentiation" trick.
    Instead of multiplying the matrix by itself `p` times (which takes O(P)), 
    we mathematically square the matrix and halve the exponent!
    x^8 = ((x^2)^2)^2. (3 operations instead of 8).
    """
    # The "Identity Matrix" (The matrix equivalent of the number 1)
    result = [[1, 0], [0, 1]]
    
    # Base matrix
    base = matrix
    
    while p > 0:
        # If the current exponent bit is 1, multiply the result by the current base
        if p % 2 == 1:
            result = multiply_matrices(result, base)
            
        # Square the base, and halve the exponent!
        base = multiply_matrices(base, base)
        p //= 2
        
    return result

def fib_matrix_log_n(n: int) -> int:
    """
    Calculates the N-th Fibonacci number in strictly O(log N) Time.
    """
    if n == 0: return 0
    if n == 1: return 1
    
    # The magical Fibonacci Transition Matrix.
    # [1, 1] * [F(n-1)] = [F(n-1) + F(n-2)] = [F(n)]
    # [1, 0]   [F(n-2)]   [F(n-1)]          = [F(n-1)]
    F = [[1, 1], 
         [1, 0]]
    
    # We raise the transition matrix to the power of (N - 1)
    F = matrix_power(F, n - 1)
    
    # The answer is located at the top-left corner of the resulting matrix!
    return F[0][0]


def demonstrate_matrix_fib():
    section_header("Algorithm: Fibonacci via Matrix Exponentiation")
    
    import time
    
    # Let's calculate a MASSIVE Fibonacci number.
    # Wait, Python handles arbitrarily large integers, so calculating the 
    # 1,000,000th Fibonacci number will literally return a number with 
    # hundreds of thousands of digits.
    # To keep console output clean, we will only print the digit count.
    
    n_massive = 1_000_000 
    print(f"Calculating the {n_massive:,}th Fibonacci number...")
    print("A standard O(N) DP loop would take 1 Million iterations.")
    print("Matrix Exponentiation O(log N) takes roughly ~20 iterations!\n")
    
    start = time.time()
    ans = fib_matrix_log_n(n_massive)
    end = time.time()
    
    # Convert to string to count the digits
    ans_str = str(ans)
    
    print(f"Time Taken: {(end - start) * 1000:.2f} milliseconds!")
    print(f"The resulting number has exactly {len(ans_str):,} digits.")
    print(f"First 10 digits: {ans_str[:10]}...")
    print(f"Last 10 digits: ...{ans_str[-10:]}")


# ==============================================================================
# 4. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. How does the `[[1, 1], [1, 0]]` matrix mathematically generate Fibonacci?
   Answer: It comes from Linear Algebra. We want to convert the state vector $[F_{n-1}, F_{n-2}]$ into the next state vector $[F_n, F_{n-1}]$. 
   $F_n = 1 \\times F_{n-1} + 1 \\times F_{n-2}$.
   $F_{n-1} = 1 \\times F_{n-1} + 0 \\times F_{n-2}$.
   If you extract the coefficients, you get the matrix: `[[1, 1], [1, 0]]`. By raising this matrix to a power, you are essentially "fast-forwarding" the mathematical equations!

2. How does Binary Exponentiation drop the time to $O(\\log N)$?
   Answer: Because $X^{1000}$ is mathematically identical to $(X^{500})^2$. And $X^{500}$ is $(X^{250})^2$. Instead of multiplying $X$ by itself 1,000 times, you just square it 10 times! Every time you square the base, you divide the required exponent by 2. This is the exact definition of a logarithmic $O(\\log_2 N)$ algorithm.

3. Does Matrix Exponentiation work for other DP problems?
   Answer: YES! It works for ANY DP problem that has a "Linear Recurrence Relation" with constant coefficients. If a DP equation looks like `dp[i] = A * dp[i-1] + B * dp[i-2] + C * dp[i-3]`, you can construct a $3 \\times 3$ matrix and solve it in $O(\\log N)$ time. It is an extremely powerful tool for advanced combinatorial problems.
"""

if __name__ == "__main__":
    demonstrate_matrix_fib()
    print("\n[SUCCESS] Laboratory: Matrix Exponentiation Completed.")