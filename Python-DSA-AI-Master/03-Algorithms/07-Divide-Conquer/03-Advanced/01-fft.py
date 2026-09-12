"""
Fast Fourier Transform (FFT).

Learning Objectives:
1. Understand polynomials and their representations.
2. Implement Cooley-Tukey FFT algorithm using Divide and Conquer.
3. Understand applications in signal processing and fast polynomial multiplication.

Concept Explanation:
The Discrete Fourier Transform (DFT) evaluates a polynomial at complex roots of unity.
The Fast Fourier Transform (FFT) computes the DFT in O(N log N) time by exploiting
the symmetry of the roots of unity, recursively splitting the polynomial into even and odd degree terms.
"""

import cmath
from typing import List

def dft_brute_force(x: List[complex]) -> List[complex]:
    """Basic O(N^2) Discrete Fourier Transform for comparison."""
    N = len(x)
    X = []
    for k in range(N):
        s = sum(x[n] * cmath.exp(-2j * cmath.pi * k * n / N) for n in range(N))
        X.append(s)
    return X

def fft(x: List[complex]) -> List[complex]:
    """Advanced O(N log N) Fast Fourier Transform (Cooley-Tukey)."""
    N = len(x)
    if N <= 1:
        return x
    
    # Divide
    even = fft(x[0::2])
    odd = fft(x[1::2])
    
    # Conquer
    T = [cmath.exp(-2j * cmath.pi * k / N) * odd[k] for k in range(N // 2)]
    
    return [even[k] + T[k] for k in range(N // 2)] + \
           [even[k] - T[k] for k in range(N // 2)]

def ifft(x: List[complex]) -> List[complex]:
    """Inverse FFT."""
    N = len(x)
    # Conjugate the complex numbers
    x_conj = [X.conjugate() for X in x]
    
    # Forward FFT
    X = fft(x_conj)
    
    # Conjugate and scale
    return [val.conjugate() / N for val in X]

"""
Performance Analysis:
- Time Complexity: O(N log N).
- Space Complexity: O(N) for recursion stack and arrays.

Edge Cases:
- Input size must be a power of 2 for this radix-2 implementation. 
  (Padding with zeros is required for arbitrary sizes).
- Empty input.

Interview Challenge:
Use FFT to multiply two large integers in O(N log N) time.
"""

def test_fft():
    # Simple test case: impulse at t=0
    x = [1.0, 0.0, 0.0, 0.0]
    X = fft(x)
    expected = [1.0, 1.0, 1.0, 1.0]
    
    for i in range(4):
        assert abs(X[i].real - expected[i]) < 1e-9
        assert abs(X[i].imag) < 1e-9
        
    print("All tests passed.")

if __name__ == "__main__":
    test_fft()
