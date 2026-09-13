"""
# ==============================================================================
# LABORATORY: KNUTH-MORRIS-PRATT (KMP) STRING MATCHING
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# The Naive String Search algorithm has Amnesia. If you search for "AAAAAB" 
# inside "AAAAAAAAAB", it successfully matches 5 'A's, hits the 'B', fails, 
# and then brutally shifts right by EXACTLY ONE space and re-evaluates all 5 'A's.
#
# In 1970, Donald Knuth, Vaughan Pratt, and James H. Morris realized something 
# profound: "If we just successfully checked 5 characters, we ALREADY KNOW what 
# they are! Why are we blindly checking them again?"
#
# They invented the KMP algorithm. Its defining feature: The Text Pointer (`i`) 
# NEVER moves backward. It only marches forward.
#
# How? KMP pre-computes an LPS Array (Longest Prefix which is also Suffix).
# Before searching the text, it mathematically analyzes the `pattern` string to 
# find repeating inner structures. 
# If a mismatch occurs at index `j` of the pattern, the LPS array instantly tells 
# the algorithm: "Don't shift by 1! You can safely shift the pattern by 4 spaces 
# because you already know those prefixes match!"
#
# The time complexity instantly drops from the pathological O(N * M) down to 
# a mathematically flawless O(N + M).
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the theory of Proper Prefixes and Suffixes.
# - Implement the LPS (Longest Prefix Suffix) Array Generator.
# - Implement the KMP Search Engine utilizing the LPS array.
#
# ==============================================================================
"""

from typing import List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. KMP PREPROCESSING: THE LPS ARRAY (O(M))
# ==============================================================================
def compute_lps_array(pattern: str) -> List[int]:
    """
    Computes the Longest Prefix Suffix (LPS) array for the given pattern.
    lps[i] stores the length of the longest PROPER prefix of pattern[0..i] 
    that is also a suffix of pattern[0..i].
    """
    m = len(pattern)
    lps = [0] * m
    
    length = 0 # Length of the previous longest prefix suffix
    i = 1
    
    # We loop through the pattern to build the LPS array
    while i < m:
        if pattern[i] == pattern[length]:
            # The character matches the prefix!
            length += 1
            lps[i] = length
            i += 1
        else:
            # Mismatch!
            if length != 0:
                # This is the tricky part! We do NOT reset length to 0!
                # We fallback to the previous LPS value to see if a shorter 
                # prefix matches!
                length = lps[length - 1]
            else:
                # Absolute zero match
                lps[i] = 0
                i += 1
                
    return lps


# ==============================================================================
# 4. KMP SEARCH ENGINE (O(N))
# ==============================================================================
def kmp_search(text: str, pattern: str) -> List[int]:
    """
    Time Complexity: O(N + M) 
    Space Complexity: O(M) for the LPS array.
    """
    n = len(text)
    m = len(pattern)
    
    if m == 0 or m > n:
        return []
        
    # 1. Precompute the LPS array (O(M))
    lps = compute_lps_array(pattern)
    
    found_indices = []
    
    i = 0 # Pointer for text
    j = 0 # Pointer for pattern
    
    # 2. The Main Search Loop (O(N))
    # Notice: `i` only ever increments! It NEVER resets backwards!
    while i < n:
        if pattern[j] == text[i]:
            i += 1
            j += 1
            
        if j == m:
            # We found a complete match!
            # The start index in the text is exactly: (current_i - pattern_length)
            found_indices.append(i - j)
            
            # To continue searching for MORE matches, we don't reset `j` to 0!
            # We use the LPS array to slide the pattern optimally!
            j = lps[j - 1]
            
        elif i < n and pattern[j] != text[i]:
            # Mismatch occurred!
            if j != 0:
                # The KMP Magic: Do not reset `i`. 
                # Slide the pattern `j` pointer backwards based on the LPS array!
                j = lps[j - 1]
            else:
                # If we mismatched on the very first character of the pattern, 
                # there is nothing to slide. Just move the text pointer forward.
                i += 1
                
    return found_indices


def demonstrate_kmp():
    section_header("Algorithm: Knuth-Morris-Pratt (KMP)")
    
    # --- Example 1: Understanding LPS ---
    pattern = "AABAACAABAA"
    lps = compute_lps_array(pattern)
    
    print(f"Pattern: {list(pattern)}")
    print(f"LPS Arr: {lps}")
    print("\nLPS Explanation:")
    print("Look at the last index: 'AABAACAABAA'.")
    print("The longest prefix is 'AABAA'. The longest suffix is 'AABAA'.")
    print("They match! Length is 5. So lps[-1] = 5.")
    
    # --- Example 2: The Search ---
    section_header("KMP Search Execution")
    
    text = "ABABDABACDABABCABAB"
    search_pattern = "ABABCABAB"
    
    print(f"Text: '{text}'")
    print(f"Pattern: '{search_pattern}'")
    
    indices = kmp_search(text, search_pattern)
    print(f"\nFound exact matches at starting indices: {indices}")


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why does KMP mathematically guarantee $O(N)$ for the search phase?
   Answer: In the `while i < n` loop, the text pointer `i` NEVER decrements. It only goes up. Even though there is a nested `j = lps[j - 1]` rollback, that rollback is strictly bounded by how many times `j` was incremented previously! Because `j` can only be incremented when `i` increments, the total number of operations across the entire execution is strictly bounded by $2N$. Thus, it is $O(N)$ independent of the pattern structure!

2. How does the `j = lps[j - 1]` fallback physically work during a mismatch?
   Answer: Imagine Pattern: `ABCABX`, Text: `ABCABY`. 
   We matched `ABCAB` (Length 5). We mismatch at `X` vs `Y`.
   Instead of resetting `j=0` and shifting the pattern by 1 (Naive), the LPS array tells us: "The prefix `AB` is identical to the suffix `AB`!" 
   So we instantly slide the pattern so that the prefix `AB` perfectly aligns with where the suffix `AB` just was in the text! `j` becomes 2. We instantly resume checking the 3rd character without EVER moving the text pointer `i` backward!

3. If KMP is $O(N)$, why isn't it used for `Ctrl+F` in web browsers?
   Answer: KMP's worst-case is strictly $O(N)$. However, algorithms like Boyer-Moore use a "Bad Character Heuristic" that looks at the END of the pattern first. If it sees a character in the text that doesn't exist anywhere in the pattern, it instantly skips the entire window forward by $M$ spaces! Therefore, Boyer-Moore has a best-case / average-case of $O(N / M)$. For a 10,000 char webpage and a 10 char pattern, KMP does 10,000 checks. Boyer-Moore might only do 1,000 checks!
"""

if __name__ == "__main__":
    demonstrate_kmp()
    print("\n[SUCCESS] Laboratory: Knuth-Morris-Pratt Completed.")
