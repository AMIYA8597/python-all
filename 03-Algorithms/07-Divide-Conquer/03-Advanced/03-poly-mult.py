"""
# ==============================================================================
# LABORATORY: POLYNOMIAL MULTIPLICATION (D&C ALGEBRA)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# In the previous lab, you learned Karatsuba's trick for multiplying two integers. 
# But mathematically, what IS an integer?
# The number 1234 is just a polynomial: $1x^3 + 2x^2 + 3x^1 + 4x^0$ evaluated at $x = 10$.
#
# Because integers are just polynomials in disguise, the exact same Divide & 
# Conquer math (Karatsuba) can be applied to multiply actual algebraic 
# polynomials (like $3x^2 + 2x + 1$).
#
# A polynomial is represented in code as an array of its coefficients. 
# $A(x) = 2x^2 + 3x + 4$ is represented as `[4, 3, 2]` (ascending powers of $x$).
#
# Naive multiplication (Convolution) requires every coefficient in A to be 
# multiplied by every coefficient in B. Time: O(N^2).
# By splitting the coefficient arrays in half and applying the 3-multiplication 
# algebraic trick, we can multiply massive polynomials in O(N^1.585) time!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Represent polynomials as arrays in Python.
# - Implement naive O(N^2) convolution.
# - Translate the Karatsuba algebraic formula to Array Operations.
#
# ==============================================================================
"""

from typing import List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. POLYNOMIAL MATH HELPERS
# ==============================================================================
def add_poly(A: List[int], B: List[int]) -> List[int]:
    """Adds two polynomials. O(N)"""
    max_len = max(len(A), len(B))
    # Pad with zeros to equalize lengths
    a_padded = A + [0] * (max_len - len(A))
    b_padded = B + [0] * (max_len - len(B))
    return [a_padded[i] + b_padded[i] for i in range(max_len)]

def sub_poly(A: List[int], B: List[int]) -> List[int]:
    """Subtracts B from A. O(N)"""
    max_len = max(len(A), len(B))
    a_padded = A + [0] * (max_len - len(A))
    b_padded = B + [0] * (max_len - len(B))
    return [a_padded[i] - b_padded[i] for i in range(max_len)]


# ==============================================================================
# 4. NAIVE CONVOLUTION (O(N^2))
# ==============================================================================
def mult_poly_naive(A: List[int], B: List[int]) -> List[int]:
    """
    Standard FOIL method. 
    A polynomial of degree N times a polynomial of degree M yields N+M-1 coefficients.
    """
    n, m = len(A), len(B)
    result = [0] * (n + m - 1)
    
    for i in range(n):
        for j in range(m):
            result[i + j] += A[i] * B[j]
            
    return result


# ==============================================================================
# 5. KARATSUBA D&C POLYNOMIAL ENGINE (O(N^1.585))
# ==============================================================================
def mult_poly_karatsuba(A: List[int], B: List[int]) -> List[int]:
    """
    Multiplies two polynomials using Karatsuba Divide & Conquer.
    Assumes A and B have the same length and it is a power of 2 for simplicity.
    """
    n = len(A)
    
    # 1. BASE CASE
    if n == 1:
        return [A[0] * B[0]]
        
    # 2. DIVIDE
    # Split the coefficient arrays exactly in half.
    mid = n // 2
    
    # Low powers of X
    A_low = A[:mid]
    B_low = B[:mid]
    
    # High powers of X
    A_high = A[mid:]
    B_high = B[mid:]
    
    # 3. CONQUER (The 3 Magical Multiplications)
    # z2 = High terms multiplied
    z2 = mult_poly_karatsuba(A_high, B_high)
    
    # z0 = Low terms multiplied
    z0 = mult_poly_karatsuba(A_low, B_low)
    
    # z1 = The middle terms
    A_sum = add_poly(A_low, A_high)
    B_sum = add_poly(B_low, B_high)
    
    z1_temp = mult_poly_karatsuba(A_sum, B_sum)
    # z1 = (A_low + A_high)*(B_low + B_high) - z2 - z0
    z1 = sub_poly(sub_poly(z1_temp, z2), z0)
    
    # 4. COMBINE
    # We must shift the arrays by placing zeros in front!
    # z2 is multiplied by x^(2 * mid), so we prepend `2 * mid` zeros.
    # z1 is multiplied by x^mid, so we prepend `mid` zeros.
    result_len = 2 * n - 1
    result = [0] * result_len
    
    # Add z0
    for i in range(len(z0)):
        result[i] += z0[i]
        
    # Add shifted z1
    for i in range(len(z1)):
        result[i + mid] += z1[i]
        
    # Add shifted z2
    for i in range(len(z2)):
        result[i + 2 * mid] += z2[i]
        
    return result


def demonstrate_polynomials():
    section_header("Algorithm: Polynomial Multiplication")
    
    # P1: 2x^1 + 1  -> [1, 2]
    # P2: 4x^1 + 3  -> [3, 4]
    # (2x + 1)(4x + 3) = 8x^2 + 10x + 3  -> [3, 10, 8]
    
    # We pad arrays to length 4 (power of 2) for the simple D&C algorithm.
    A = [1, 2, 0, 0] # 2x + 1
    B = [3, 4, 0, 0] # 4x + 3
    
    print(f"Polynomial A: {A}")
    print(f"Polynomial B: {B}")
    
    print("\nExecuting Naive Convolution (O(N^2))...")
    naive_ans = mult_poly_naive(A, B)
    # Trim trailing zeros for output
    while naive_ans and naive_ans[-1] == 0: naive_ans.pop()
    print(f"Result: {naive_ans}")
    
    print("\nExecuting Karatsuba D&C Convolution (O(N^1.585))...")
    kara_ans = mult_poly_karatsuba(A, B)
    while kara_ans and kara_ans[-1] == 0: kara_ans.pop()
    print(f"Result: {kara_ans}")
    
    print("\nMathematical representation:")
    print("Coefficients [3, 10, 8] translates to: 8x^2 + 10x + 3")


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. How is shifting an array equivalent to multiplying by $x^{mid}$?
   Answer: In our array representation, index $i$ represents the coefficient of $x^i$. If we prepend 5 zeros to the front of the array, the number that was previously at index 0 is now at index 5. We physically transformed $4x^0$ into $4x^5$, which is mathematically identical to multiplying the entire polynomial by $x^5$!

2. If Karatsuba for Polynomials is $O(N^{1.585})$, why did we learn FFT which is $O(N \\log N)$?
   Answer: The Fast Fourier Transform (FFT) is strictly faster than Karatsuba for incredibly massive polynomials (degree > 10,000). However, FFT requires complex numbers, heavy trigonometry (`math.sin`, `math.cos`), and floating-point precision, which can cause round-off errors. Karatsuba uses pure integer addition and subtraction, guaranteeing 100% exact precision with much lower implementation overhead for medium-sized polynomials.

3. Why do we pad the arrays to a power of 2?
   Answer: The recursion splits the arrays in half `n // 2`. If the array length is odd (like 5), splitting it yields lengths 2 and 3. The addition and subtraction arrays (`z1`) become mismatched in length, drastically complicating the boundary indices during the Combine step. Padding with imaginary $0x$ coefficients to a power of 2 ensures perfectly symmetrical recursive cuts down to the base case of 1.
"""

if __name__ == "__main__":
    demonstrate_polynomials()
    print("\n[SUCCESS] Laboratory: Polynomial Multiplication Completed.")
