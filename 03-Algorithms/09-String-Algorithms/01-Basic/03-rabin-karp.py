"""
# ==============================================================================
# LABORATORY: RABIN-KARP STRING MATCHING (ROLLING HASH)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# KMP uses clever string-prefix math to avoid backtracking. 
# But in 1987, Michael Rabin and Richard Karp invented an entirely different 
# paradigm based on Cryptography and Hashing.
#
# If you are searching for the pattern "CAT", instead of comparing letters, 
# what if you converted "CAT" into a single mathematical integer? 
# (e.g., Hash("CAT") = 42).
#
# You then slide a window of length 3 across the text. For every window, you 
# calculate its Hash. 
# - If Hash(window) != 42, they are mathematically guaranteed NOT to match! 
#   Instantly skip to the next window!
# - If Hash(window) == 42, they MIGHT match. (Because of hash collisions, "DOG" 
#   might also equal 42). So you do a standard character-by-character check.
#
# The Fatal Flaw: If you calculate the hash from scratch for every window, 
# calculating the hash takes O(M) time. Sliding it N times makes the algorithm 
# exactly O(N * M), which is no better than the Naive algorithm!
#
# The Miracle Solution: The "Rolling Hash".
# When the window slides from [C A T] to [A T S], you DO NOT recalculate the 
# hash from scratch! You simply:
# 1. Subtract the numerical value of 'C'.
# 2. Multiply by the Base (Shift left).
# 3. Add the numerical value of 'S'.
# This Rolling Hash update takes exactly O(1) time! 
#
# Total Time Complexity: Average O(N + M).
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand Polynomial Hashing (Base and Modulo).
# - Implement the O(1) Rolling Hash subtraction/addition logic.
# - Understand Spurious Hits (Hash Collisions).
#
# ==============================================================================
"""

from typing import List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. RABIN-KARP ENGINE (ROLLING HASH)
# ==============================================================================
def rabin_karp_search(text: str, pattern: str) -> List[int]:
    """
    Time Complexity: Average O(N + M). Worst Case O(N * M) (if every hash collides).
    """
    n = len(text)
    m = len(pattern)
    
    if m == 0 or m > n:
        return []
        
    found_indices = []
    
    # --------------------------------------------------------------------------
    # HASHING CONSTANTS
    # --------------------------------------------------------------------------
    # Base 256 because there are 256 characters in the standard ASCII table.
    d = 256 
    
    # A large prime number to act as the Modulo. 
    # This prevents the hash integer from exploding to infinity (integer overflow) 
    # and evenly distributes the hashes to minimize collisions!
    q = 1000000007 
    
    # The value of h = d^(M-1) % q
    # We need this pre-calculated to subtract the leading character during the roll!
    h = 1
    for _ in range(m - 1):
        h = (h * d) % q
        
        
    # --------------------------------------------------------------------------
    # INITIAL HASH GENERATION (O(M))
    # --------------------------------------------------------------------------
    hash_pattern = 0
    hash_window = 0
    
    for i in range(m):
        # Hash Formula: (Previous_Hash * Base + ASCII_Value) % Prime
        hash_pattern = (d * hash_pattern + ord(pattern[i])) % q
        hash_window = (d * hash_window + ord(text[i])) % q
        
        
    # --------------------------------------------------------------------------
    # THE SLIDING WINDOW (O(N))
    # --------------------------------------------------------------------------
    for i in range(n - m + 1):
        
        # 1. HASH COMPARISON
        if hash_pattern == hash_window:
            
            # 2. COLLISION VERIFICATION (Spurious Hit Check)
            # Just because the hashes match does NOT guarantee the strings match!
            match = True
            for j in range(m):
                if text[i + j] != pattern[j]:
                    match = False
                    break # Spurious Hit! Hash collision!
                    
            if match:
                found_indices.append(i)
                
        # 3. THE ROLLING HASH MAGIC (O(1))
        # If we haven't reached the very end of the text... slide the window!
        if i < n - m:
            # Formula: new_hash = Base * (old_hash - LeadingChar * h) + TrailingChar
            
            # Step A: Subtract the leading character
            hash_window = (hash_window - ord(text[i]) * h)
            
            # Step B: Multiply by Base and Add the new trailing character
            hash_window = (hash_window * d + ord(text[i + m])) % q
            
            # Modulo Math Quirk: If the subtraction resulted in a negative number, 
            # we must add the prime to wrap it back around to a positive integer!
            if hash_window < 0:
                hash_window += q
                
    return found_indices


def demonstrate_rabinkarp():
    section_header("Algorithm: Rabin-Karp (Rolling Hash)")
    
    text = "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG"
    pattern = "THE"
    
    print(f"Text: '{text}'")
    print(f"Pattern: '{pattern}'")
    
    print("\nExecuting Rolling Hash Window...")
    indices = rabin_karp_search(text, pattern)
    
    print(f"\nFound exact matches at starting indices: {indices}")
    
    section_header("The Power of the Rolling Hash")
    print("Imagine hashing 'ABACUS' (Length 6).")
    print("Window 1: Hash('ABACUS') = 4591")
    print("To move to Window 2: 'BACUSZ'")
    print("Instead of a 6-character loop, Rabin-Karp does: (4591 - 'A'*(Base^5)) * Base + 'Z'")
    print("It calculates the Hash of a 1,000,000 character window in exactly 1 operation!")


# ==============================================================================
# 4. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why do we need the modulo `q`?
   Answer: We are calculating polynomial hashes. If $d = 256$ and the pattern is $1,000$ characters long, the final integer hash will be mathematically proportional to $256^{1000}$. This number is so massive it physically cannot fit into a CPU register (64-bit integer limit). It will overflow and crash. By taking the modulo of a large prime $q$ at EVERY step, we force the hash to safely stay within standard integer limits while retaining a high degree of uniqueness!

2. What is a "Spurious Hit"?
   Answer: A Hash Collision. If $q = 13$, the maximum possible hash value is 12. If we have 500 different string patterns, by the Pigeonhole Principle, multiple completely different strings MUST share the exact same hash (e.g., Hash("CAT") = 9, Hash("DOG") = 9). When the window hits "DOG", the hashes match (9 == 9). The algorithm halts and runs a char-by-char `if 'C' == 'D'` check. It instantly realizes it was a fake match (Spurious Hit) and moves on.

3. Why use Rabin-Karp when KMP is mathematically faster in the worst case?
   Answer: Multiple Pattern Search! KMP can only search for ONE pattern at a time. What if you need to search a text for 100 different banned words simultaneously? With Rabin-Karp, you pre-calculate the 100 hashes and put them in a Set. As the Rolling Hash slides across the text, you do an $O(1)$ lookup: `if hash_window in banned_hashes_set`. You can search for 10,000 different words simultaneously in a single $O(N)$ pass! This is used in Plagiarism Detection software!
"""

if __name__ == "__main__":
    demonstrate_rabinkarp()
    print("\n[SUCCESS] Laboratory: Rabin-Karp Algorithm Completed.")
