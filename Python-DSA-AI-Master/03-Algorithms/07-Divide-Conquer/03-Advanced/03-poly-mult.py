"""
Polynomial Multiplication using Divide and Conquer.

Learning Objectives:
1. Represent polynomials as arrays.
2. Use divide and conquer to multiply polynomials.
3. Combine with FFT for optimal performance.

Concept Explanation:
Multiplying two polynomials of degree n takes O(n^2) using standard distribution.
Using D&C (similar to Karatsuba), we can achieve O(n^1.58).
Using FFT, we can achieve O(n log n).
"""

from typing import List
import cmath

# Standard O(n^2)
def poly_mult_basic(A: List[int], B: List[int]) -> List[int]:
    m, n = len(A), len(B)
    prod = [0] * (m + n - 1)
    for i in range(m):
        for j in range(n):
            prod[i + j] += A[i] * B[j]
    return prod

# Helper for FFT
def fft(x: List[complex]) -> List[complex]:
    N = len(x)
    if N <= 1: return x
    even = fft(x[0::2])
    odd  = fft(x[1::2])
    T = [cmath.exp(-2j * cmath.pi * k / N) * odd[k] for k in range(N // 2)]
    return [even[k] + T[k] for k in range(N // 2)] + \
           [even[k] - T[k] for k in range(N // 2)]

def ifft(x: List[complex]) -> List[complex]:
    N = len(x)
    x_conj = [X.conjugate() for X in x]
    X = fft(x_conj)
    return [val.conjugate() / N for val in X]

def poly_mult_advanced(A: List[int], B: List[int]) -> List[int]:
    """O(N log N) polynomial multiplication using FFT."""
    n = 1
    # Pad to nearest power of 2 >= len(A) + len(B) - 1
    target_len = len(A) + len(B) - 1
    while n < target_len:
        n *= 2

    # Pad A and B with zeros
    A_complex = [complex(x, 0) for x in A] + [0j] * (n - len(A))
    B_complex = [complex(x, 0) for x in B] + [0j] * (n - len(B))

    # Forward FFT
    fft_A = fft(A_complex)
    fft_B = fft(B_complex)

    # Pointwise multiplication
    fft_C = [fft_A[i] * fft_B[i] for i in range(n)]

    # Inverse FFT
    C_complex = ifft(fft_C)
    
    # Round back to integers
    return [round(C_complex[i].real) for i in range(target_len)]

"""
Performance Analysis:
- Time Complexity: O(n log n) using FFT, O(n^2) basic.
- Space Complexity: O(n) due to zero-padding to powers of 2.

Edge Cases:
- Zero polynomials (empty or [0]).
- Polynomials of different degrees.

Interview Challenge:
Explain how floating point inaccuracies might affect the FFT polynomial multiplication of large integers.
"""

def test_poly_mult():
    A = [5, 0, 10, 6] # 5 + 10x^2 + 6x^3
    B = [1, 2, 4]     # 1 + 2x + 4x^2
    expected = [5, 10, 30, 26, 52, 24]
    
    res1 = poly_mult_basic(A, B)
    res2 = poly_mult_advanced(A, B)
    
    assert res1 == expected
    assert res2 == expected
    print("All tests passed.")

if __name__ == "__main__":
    test_poly_mult()
