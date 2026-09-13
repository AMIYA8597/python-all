"""
# ==============================================================================
# LABORATORY: FAST FOURIER TRANSFORM (THE MOST IMPORTANT ALGORITHM OF THE 20TH CENTURY)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# If you listen to an MP3, look at a JPEG, connect to Wi-Fi, use a cell phone, 
# or run an MRI machine, you are relying on the Fast Fourier Transform (FFT).
#
# The Discrete Fourier Transform (DFT) converts a signal from the "Time Domain" 
# (e.g. an audio wave) into the "Frequency Domain" (the individual pitches that 
# make up the sound). 
# A naive DFT requires O(N^2) time. For a 3-minute song (8 million audio samples), 
# O(N^2) would take 64 trillion operations. It would take longer to process the 
# song than to listen to it!
#
# In 1965, Cooley and Tukey rediscovered a Divide and Conquer trick (originally 
# noted by Gauss in 1805). They realized that you can split a polynomial into 
# its EVEN and ODD coefficients, solve them recursively, and combine them using 
# Complex Numbers (Roots of Unity)!
#
# This drops the time from O(N^2) to O(N log N).
# 64 trillion operations instantly drops to just 180 million. The song processes 
# in a fraction of a second. 
# It is widely considered one of the Top 10 most important algorithms ever invented.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand how polynomials relate to signals.
# - Grasp the Cooley-Tukey Divide & Conquer trick (Even vs Odd).
# - Implement O(N log N) recursive FFT using Python's `cmath` (complex numbers).
#
# ==============================================================================
"""

import cmath
import math
from typing import List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. RECURSIVE COOLEY-TUKEY FFT (O(N log N))
# ==============================================================================
def fft(P: List[complex]) -> List[complex]:
    """
    Computes the Discrete Fourier Transform of a polynomial `P` (represented as 
    a list of coefficients) in O(N log N) time using Divide and Conquer.
    NOTE: N MUST be a power of 2 for this simple recursive implementation.
    """
    n = len(P)
    
    # 1. BASE CASE
    if n == 1:
        return P
        
    # 2. DIVIDE (Even and Odd Coefficients)
    # E.g., [A0, A1, A2, A3] -> Even: [A0, A2], Odd: [A1, A3]
    # We step by 2!
    Pe = P[0::2]  
    Po = P[1::2]
    
    # 3. CONQUER (Recursive Calls)
    Ye = fft(Pe)
    Yo = fft(Po)
    
    # 4. COMBINE (Roots of Unity)
    # We must combine the even and odd halves.
    # The magical math trick: The N-th complex root of unity `w` rotates around 
    # the complex plane.
    # Because of symmetry, the second half of the answers are just the negative 
    # conjugates of the first half! We calculate BOTH halves simultaneously in 
    # one single loop of size N/2!
    
    # Preallocate the result array of size N
    Y = [0] * n
    
    # Calculate the principal N-th root of unity: e^(2 * pi * i / N)
    w = cmath.exp(2j * cmath.pi / n)
    
    for j in range(n // 2):
        # The combination equation!
        # Y[j] = Even[j] + (w^j * Odd[j])
        # Y[j + N/2] = Even[j] - (w^j * Odd[j])
        
        # Calculate w^j
        w_j = w ** j
        
        Y[j] = Ye[j] + w_j * Yo[j]
        Y[j + n // 2] = Ye[j] - w_j * Yo[j]
        
    return Y


def demonstrate_fft():
    section_header("Algorithm: Fast Fourier Transform (Cooley-Tukey)")
    
    # A polynomial: 1 + 2x + 3x^2 + 4x^3
    # N is 4 (which is a power of 2!)
    P = [1, 2, 3, 4]
    
    print(f"Time Domain Signal (Polynomial Coefficients): {P}")
    print("\nExecuting O(N log N) FFT...")
    
    # Convert inputs to complex numbers
    P_complex = [complex(x, 0) for x in P]
    frequencies = fft(P_complex)
    
    print("\nFrequency Domain (Discrete Fourier Transform):")
    for i, freq in enumerate(frequencies):
        # Round the tiny floating point artifacts from `cmath`
        real = round(freq.real, 4)
        imag = round(freq.imag, 4)
        print(f" X[{i}] = {real} + {imag}j")
        
    print("\nWhat does this mean?")
    print("This output represents the amplitudes and phases of the sine waves ")
    print("that, when added together, perfectly reconstruct the original signal!")


# ==============================================================================
# 4. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why does `N` have to be a power of 2 in this implementation?
   Answer: Because we are using the pure Cooley-Tukey Divide & Conquer algorithm, which relies on perfectly chopping the array in half at every level (`N -> N/2 -> N/4 -> 1`). If `N` was 5, we couldn't split it into equal even/odd halves! In the real world, if `N` is not a power of 2, engineers either "zero-pad" the array until it reaches the next power of 2, or they use Bluestein's FFT algorithm.

2. Why is FFT considered a "Divide & Conquer" algorithm?
   Answer: Because it follows the exact 3-step paradigm:
   1. Divide: Split the polynomial $P(x)$ into $P_{even}(x^2)$ and $x \cdot P_{odd}(x^2)$.
   2. Conquer: Recursively solve the DFT of the even and odd parts.
   3. Combine: Use the symmetry of the Complex Roots of Unity to mathematically fuse the two smaller DFTs into the global DFT in $O(N)$ time.
   $T(N) = 2T(N/2) + O(N) = O(N \log N)$.

3. How does FFT multiply two massive polynomials (or massive integers) so fast?
   Answer: If you multiply two polynomials of degree $N$, standard algebra takes $O(N^2)$ (FOIL method). But if you use FFT to convert both polynomials into the Frequency Domain ($O(N \log N)$), you can just multiply their frequencies together index-by-index in $O(N)$ time! Then you run the Inverse-FFT ($O(N \log N)$) to convert the answer back to the Time Domain! Total time: $O(N \log N)$, shattering the $O(N^2)$ barrier!
"""

if __name__ == "__main__":
    demonstrate_fft()
    print("\n[SUCCESS] Laboratory: Fast Fourier Transform Completed.")
