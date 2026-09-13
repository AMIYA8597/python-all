"""
# ==============================================================================
# LABORATORY: Z-ALGORITHM (LINEAR TIME STRING SEARCH)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# KMP achieves O(N + M) time using the LPS array (Longest Prefix Suffix). 
# However, understanding and debugging the LPS fallback (`j = lps[j - 1]`) 
# is notoriously difficult for many engineers.
#
# The Z-Algorithm is a modern, highly elegant alternative that achieves the exact 
# same O(N + M) time complexity, but uses a completely different mathematical trick.
#
# The Z-Array Concept:
# Imagine you have a string: "AABCAABXAA".
# We define `Z[i]` as the length of the longest substring starting from index `i` 
# that perfectly matches the PREFIX (beginning) of the entire string.
# 
# Example: 
# Index 0: 'AABCAABXAA'. Prefix matches itself! Z[0] = 0 (Ignored by convention).
# Index 1: 'ABCAABXAA'. Compares to 'AAB'. First char 'A' matches, second 'B' != 'A'. Z[1] = 1.
# Index 4: 'AABXAA'. Compares to 'AABCAA'. Matches 'AAB' (length 3). Z[4] = 3.
#
# How does this solve String Matching?
# You take your Pattern, add a dummy character (like '$'), and attach the Text!
# String = Pattern + "$" + Text
# 
# You compute the Z-array for this massive string. 
# If `Z[i]` ever exactly equals the length of your Pattern... BOOM! You have 
# mathematically proven that the substring starting at `i` perfectly matches 
# the prefix of the entire string (which IS your Pattern!).
#
# To do this in O(N) time, the algorithm maintains a "Z-Box" [L, R], which 
# remembers the furthest right we have ever successfully matched. If we are 
# currently inside the Z-Box, we can instantly copy previous Z-values to avoid 
# redundant character checks!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the Z-Array definition.
# - Implement the [L, R] Z-Box optimization.
# - Execute O(N+M) string search using the concatenated string trick.
#
# ==============================================================================
"""

from typing import List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE Z-ARRAY GENERATOR (O(N))
# ==============================================================================
def compute_z_array(s: str) -> List[int]:
    """
    Computes the Z-array in strict O(N) time.
    """
    n = len(s)
    z = [0] * n
    
    # [L, R] represents the 'Z-Box'. 
    # It is the window of the furthest right prefix match we have found so far.
    # L is the left bound, R is the right bound (inclusive).
    L = 0
    R = 0
    
    for i in range(1, n):
        
        # CASE 1: We are OUTSIDE the Z-Box.
        # We have no previously calculated information to help us. 
        # We must use Naive character-by-character comparison!
        if i > R:
            L = R = i
            # Naive match loop: While within bounds AND characters match the prefix
            while R < n and s[R - L] == s[R]:
                R += 1
            
            # We stepped one character too far, pull R back so it is inclusive
            z[i] = R - L
            R -= 1
            
        # CASE 2: We are INSIDE the Z-Box.
        # We are currently exploring an index `i` that was ALREADY successfully 
        # matched as part of a previous prefix!
        else:
            # We can look back at the previously computed value for this exact 
            # relative position! The relative index is `i - L`.
            k = i - L
            
            # Check the previously computed Z-value `z[k]`.
            # If `z[k]` is SHORT enough that it doesn't cross the right boundary 
            # `R` of our current Z-Box, we can INSTANTLY copy it! O(1) time!
            if z[k] < R - i + 1:
                z[i] = z[k]
                
            # If `z[k]` is so massive that it stretches PAST the right boundary 
            # of our Z-Box, we can only safely copy up to the boundary `R`.
            # Beyond `R` is uncharted territory! We must resume naive checking 
            # from `R` onwards.
            else:
                L = i
                # Naive matching for the uncharted territory!
                while R < n and s[R - L] == s[R]:
                    R += 1
                
                z[i] = R - L
                R -= 1
                
    return z


# ==============================================================================
# 4. Z-ALGORITHM SEARCH ENGINE (O(N + M))
# ==============================================================================
def z_algorithm_search(text: str, pattern: str) -> List[int]:
    """
    Searches for `pattern` in `text` using the Z-Array.
    Time Complexity: O(N + M)
    Space Complexity: O(N + M) for the concatenated string and Z-array.
    """
    n = len(text)
    m = len(pattern)
    
    if m == 0 or m > n:
        return []
        
    found_indices = []
    
    # 1. THE CONCATENATION TRICK
    # We use a separator character '$' that is GUARANTEED to not exist in 
    # either the pattern or the text. This prevents the Z-values from ever 
    # growing larger than the pattern length `m`!
    concat_str = pattern + "$" + text
    
    # 2. COMPUTE Z-ARRAY
    z = compute_z_array(concat_str)
    
    # 3. SCAN FOR MATCHES
    # We iterate over the Z-array. We only care about the values corresponding 
    # to the `text` portion of the concatenated string.
    # The `text` starts at index (m + 1).
    for i in range(m + 1, len(concat_str)):
        
        # If the Z-value perfectly equals the length of the pattern...
        # It means the substring starting here perfectly matches the prefix 
        # of the whole string (which IS the pattern). WE FOUND A MATCH!
        if z[i] == m:
            
            # The current index `i` is relative to the concatenated string.
            # We must subtract the pattern length and the '$' character to get 
            # the true index relative to the original `text`.
            original_text_index = i - (m + 1)
            found_indices.append(original_text_index)
            
    return found_indices


def demonstrate_z_algo():
    section_header("Algorithm: Z-Algorithm (Linear Time Search)")
    
    # --- Example 1: Understanding the Z-Array ---
    s = "aabcaabxaa"
    z_arr = compute_z_array(s)
    print(f"String:  {list(s)}")
    print(f"Z-Array: {z_arr}")
    print("\nZ-Array Explanation:")
    print("Index 4 ('aabxaa'): Matches prefix 'aab'. Length is 3. So Z[4] = 3.")
    print("Index 8 ('aa'): Matches prefix 'aa'. Length is 2. So Z[8] = 2.")
    
    # --- Example 2: The Search ---
    section_header("Z-Algorithm Search Execution")
    
    text = "BAABAABCAA"
    pattern = "AAB"
    
    print(f"Text: '{text}'")
    print(f"Pattern: '{pattern}'")
    print(f"Concatenated String: '{pattern + '$' + text}'")
    
    print("\nComputing Z-Array and scanning...")
    indices = z_algorithm_search(text, pattern)
    
    print(f"\nFound exact matches at starting indices: {indices}")
    for idx in indices:
        print(f" -> text[{idx}:{idx+len(pattern)}] == '{text[idx:idx+len(pattern)]}'")


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why does the Z-Algorithm mathematically guarantee $O(N)$ execution time?
   Answer: Look at the `R` pointer. `R` represents the furthest right index we have ever successfully matched. Inside the `while` loop, `R` ONLY EVER INCREMENTS. It never moves backward. The inner `while` loop only executes for characters in the "uncharted territory" beyond `R`. Because `R` can increment a maximum of $N$ times, the inner loop can only physically execute a total of $N$ times across the entire lifespan of the algorithm! $O(N)$.

2. Why is the separator character `$` strictly necessary in the concatenated string?
   Answer: Imagine `Pattern = "A"`, `Text = "AAAAA"`. Concatenated without separator: `"AAAAAA"`. The Z-array for this is `[0, 5, 4, 3, 2, 1]`. The Z-values grow massively beyond the length of the pattern! It becomes ambiguous to decode where the actual matches are. By using a separator `$` that is guaranteed NOT to exist in the alphabet, the Z-value instantly hits a wall at the `$`. It physically forces the maximum possible Z-value to be exactly $M$ (the pattern length). If you see $M$, it is mathematically proven to be an exact match of the pattern!

3. KMP vs Z-Algorithm. Which is better?
   Answer: They both achieve $O(N+M)$ time and $O(N+M)$ space. KMP is slightly more memory-efficient because it only requires the $O(M)$ LPS array, whereas the standard Z-Algorithm concatenates the strings requiring an $O(N+M)$ Z-array. However, the Z-Algorithm logic (checking bounds within a Z-Box) is generally considered much easier to trace and debug during high-pressure FAANG interviews than the recursive fallback logic of KMP's LPS array.
"""

if __name__ == "__main__":
    demonstrate_z_algo()
    print("\n[SUCCESS] Laboratory: Z-Algorithm Completed.")
