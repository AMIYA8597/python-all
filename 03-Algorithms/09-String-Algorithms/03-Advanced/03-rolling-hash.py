"""
# ==============================================================================
# LABORATORY: ADVANCED ROLLING HASH (2D & DOUBLE HASHING)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# In the Basic String Algorithms phase, you learned the Rabin-Karp algorithm.
# It used a 1D Rolling Hash to find a 1D string in O(N+M) time.
#
# But the Rolling Hash paradigm is far more powerful.
# 
# Scenario 1: The Hash Collision Nightmare.
# If you are hashing DNA sequences or processing billions of substrings, the 
# Pigeonhole Principle guarantees massive hash collisions if you only use one Modulo.
# Solution: Double Hashing. Calculate Hash A (modulo 10^9+7) and Hash B 
# (modulo 10^9+9). The probability of BOTH hashes colliding simultaneously is 
# astronomically low (effectively zero).
#
# Scenario 2: 2D Image Matching (The 2D Rabin-Karp).
# You are building a Computer Vision system (like early facial recognition or 
# Where's Waldo). You have a 1000x1000 pixel image, and you are searching for 
# a 50x50 pixel template.
# - Naive search takes O(N^2 * M^2). 
# By using a 2D Rolling Hash, you can slide a 2D window across the image in 
# O(1) time per step! 
# How? You roll horizontally (like standard Rabin-Karp) to create Column Hashes, 
# and then you roll those Column Hashes VERTICALLY!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand Double Hashing for collision prevention.
# - Implement a 2D Rolling Hash for Matrix Pattern Matching.
#
# ==============================================================================
"""

from typing import List, Tuple

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. DOUBLE HASHING ENGINE (1D)
# ==============================================================================
def double_hash_search(text: str, pattern: str) -> List[int]:
    """
    Rabin-Karp using TWO distinct primes to virtually eliminate Spurious Hits.
    """
    n, m = len(text), len(pattern)
    if m == 0 or m > n: return []
    
    d = 256
    # Two large prime numbers
    q1 = 1000000007
    q2 = 1000000009
    
    h1 = pow(d, m - 1, q1)
    h2 = pow(d, m - 1, q2)
    
    p_hash1, p_hash2 = 0, 0
    t_hash1, t_hash2 = 0, 0
    
    # Initial Hashes
    for i in range(m):
        p_hash1 = (d * p_hash1 + ord(pattern[i])) % q1
        p_hash2 = (d * p_hash2 + ord(pattern[i])) % q2
        
        t_hash1 = (d * t_hash1 + ord(text[i])) % q1
        t_hash2 = (d * t_hash2 + ord(text[i])) % q2
        
    found_indices = []
    
    # Sliding Window
    for i in range(n - m + 1):
        # We only consider it a match if BOTH hashes match perfectly!
        if p_hash1 == t_hash1 and p_hash2 == t_hash2:
            # Note: Because the probability of a double collision is so low 
            # (1 in 10^18), competitive programmers often skip the O(M) char-by-char 
            # verification step entirely to save time! We will verify just to be safe.
            if text[i : i+m] == pattern:
                found_indices.append(i)
                
        # Roll the hashes!
        if i < n - m:
            t_hash1 = (d * (t_hash1 - ord(text[i]) * h1) + ord(text[i + m])) % q1
            t_hash2 = (d * (t_hash2 - ord(text[i]) * h2) + ord(text[i + m])) % q2
            
            # Fix negative modulos
            t_hash1 = (t_hash1 + q1) % q1
            t_hash2 = (t_hash2 + q2) % q2
            
    return found_indices


# ==============================================================================
# 4. 2D RABIN-KARP ENGINE (MATRIX MATCHING)
# ==============================================================================
def search_2d_matrix(matrix: List[List[int]], pattern: List[List[int]]) -> List[Tuple[int, int]]:
    """
    Finds the 2D Pattern inside the 2D Matrix in O(R*C) time using a 2D Rolling Hash.
    """
    R_M, C_M = len(matrix), len(matrix[0])
    R_P, C_P = len(pattern), len(pattern[0])
    
    if R_P > R_M or C_P > C_M: return []
    
    q = 1000000007
    d_row = 256 # Base for Horizontal hashing
    d_col = 257 # Base for Vertical hashing
    
    # 1. Calculate the H multipliers for subtraction
    h_row = pow(d_row, C_P - 1, q)
    h_col = pow(d_col, R_P - 1, q)
    
    # --------------------------------------------------------------------------
    # 2. HASH THE PATTERN
    # --------------------------------------------------------------------------
    pattern_hash = 0
    for r in range(R_P):
        row_hash = 0
        for c in range(C_P):
            row_hash = (row_hash * d_row + pattern[r][c]) % q
        pattern_hash = (pattern_hash * d_col + row_hash) % q
        
    # --------------------------------------------------------------------------
    # 3. PRE-COMPUTE 1D ROW HASHES FOR THE MATRIX
    # --------------------------------------------------------------------------
    # Instead of rolling 2D boxes directly, we first collapse the matrix 
    # horizontally. We create a new matrix where every cell represents the 
    # Hash of a C_P-length horizontal window!
    
    row_hashes = [[0] * (C_M - C_P + 1) for _ in range(R_M)]
    
    for r in range(R_M):
        current_row_hash = 0
        # Hash the first window of length C_P
        for c in range(C_P):
            current_row_hash = (current_row_hash * d_row + matrix[r][c]) % q
            
        row_hashes[r][0] = current_row_hash
        
        # Roll horizontally!
        for c in range(1, C_M - C_P + 1):
            leading_val = matrix[r][c - 1]
            trailing_val = matrix[r][c + C_P - 1]
            current_row_hash = (d_row * (current_row_hash - leading_val * h_row) + trailing_val) % q
            current_row_hash = (current_row_hash + q) % q
            row_hashes[r][c] = current_row_hash

    # --------------------------------------------------------------------------
    # 4. ROLL VERTICALLY TO FIND THE 2D MATCH
    # --------------------------------------------------------------------------
    found_coords = []
    
    # We now look at the `row_hashes` matrix. 
    # For every valid column, we roll vertically down the rows!
    for c in range(C_M - C_P + 1):
        
        current_col_hash = 0
        # Hash the first vertical window of length R_P
        for r in range(R_P):
            current_col_hash = (current_col_hash * d_col + row_hashes[r][c]) % q
            
        if current_col_hash == pattern_hash:
            # We assume no spurious hits for this lab example
            found_coords.append((0, c))
            
        # Roll vertically!
        for r in range(1, R_M - R_P + 1):
            leading_val = row_hashes[r - 1][c]
            trailing_val = row_hashes[r + R_P - 1][c]
            
            current_col_hash = (d_col * (current_col_hash - leading_val * h_col) + trailing_val) % q
            current_col_hash = (current_col_hash + q) % q
            
            if current_col_hash == pattern_hash:
                found_coords.append((r, c))
                
    return found_coords


def demonstrate_advanced_hash():
    section_header("Algorithm: Double Hashing (1D)")
    
    text = "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG"
    pattern = "THE"
    
    indices = double_hash_search(text, pattern)
    print(f"Double Hashed Pattern '{pattern}' found at: {indices}")
    
    section_header("Algorithm: 2D Rabin-Karp (Matrix Search)")
    
    # A 5x5 Image (Values are ASCII or Pixel intensities)
    matrix = [
        [1, 2, 3, 4, 5],
        [2, 9, 8, 7, 6],
        [3, 8, 9, 8, 7],
        [4, 7, 8, 9, 8],
        [5, 6, 7, 8, 9]
    ]
    
    # A 3x3 Template we want to find inside the image
    pattern_2d = [
        [9, 8, 7],
        [8, 9, 8],
        [7, 8, 9]
    ]
    
    print("Matrix:")
    for row in matrix: print(row)
        
    print("\nPattern to find:")
    for row in pattern_2d: print(row)
        
    print("\nExecuting 2D Rolling Hash...")
    coords = search_2d_matrix(matrix, pattern_2d)
    
    print(f"\n2D Pattern found at Top-Left Coordinates: {coords}")
    if coords:
        r, c = coords[0]
        print(f"Verification: matrix[{r}][{c}] is {matrix[r][c]}, which matches pattern[0][0]!")


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why does Double Hashing virtually eliminate spurious hits?
   Answer: If we use one modulo $Q_1 = 10^9+7$, the probability of two random strings hashing to the same value is $1 / 10^9$. In a text of 1 Billion characters, you are statistically guaranteed to hit a spurious collision. If we add a second modulo $Q_2 = 10^9+9$, the probability of a string colliding on BOTH hashes simultaneously is $(1 / 10^9) \times (1 / 10^9) = 1 / 10^{18}$. This number is larger than the total number of CPU cycles executed by all computers on Earth in a year. The probability of collision is so low it can be mathematically ignored in production.

2. Why does the 2D Rabin-Karp pre-compute 1D row hashes?
   Answer: If we tried to roll a $3 \times 3$ 2D box natively, shifting the box one pixel to the right requires subtracting 3 left-pixels, shifting the remaining 6 pixels, and adding 3 right-pixels. This is heavily complex and slow. By pre-computing 1D row hashes, we collapse the matrix into a single numerical representation horizontally. Then, a $3 \times 3$ box mathematically becomes a 1D column of 3 numbers! We can just use the standard 1D vertical rolling hash on that column!

3. Where is 2D Rabin-Karp used?
   Answer: Early computer vision, Plagiarism detection for 2D code blocks, and searching for 2D visual templates inside satellite imagery. Modern AI (Convolutional Neural Networks) has largely replaced it for fuzzy/imperfect image matching, but 2D Rabin-Karp remains the absolute fastest algorithm for EXACT 2D sub-matrix extraction.
"""

if __name__ == "__main__":
    demonstrate_advanced_hash()
    print("\n[SUCCESS] Laboratory: Advanced Rolling Hash Completed.")
