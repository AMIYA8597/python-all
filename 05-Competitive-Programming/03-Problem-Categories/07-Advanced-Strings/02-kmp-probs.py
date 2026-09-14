"""
# ==============================================================================
# LABORATORY: COMPETITIVE PROGRAMMING (KMP STRING MATCHING)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You are searching for a specific substring (the "Pattern") inside a massive 
# 1-Billion character text file (the "Text").
# 
# Text: "AAAAABAAAAACAAAAABAAAAAD"
# Pattern: "AAAAAD"
#
# A naive algorithm checks the pattern against index 0. It matches "AAAAA" 
# but fails on 'B' instead of 'D'. The algorithm shifts over exactly 1 index 
# and restarts checking from scratch. 
# Because the string is highly repetitive, checking from scratch takes O(N * M) 
# time. Your code will stall for 5 minutes.
#
# The Knuth-Morris-Pratt (KMP) algorithm observes a fundamental mathematical 
# truth: If you just matched "AAAAA", you already KNOW the previous characters! 
# Why throw that information away? 
# KMP precalculates a "Prefix Array" (LPS) that tells the algorithm exactly how 
# far to jump forward without ever re-evaluating characters it has already seen!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the architecture of the LPS (Longest Prefix Suffix) array.
# - Implement KMP String Search in exact O(N + M) time.
#
# ==============================================================================
"""

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. KMP ALGORITHM (O(N + M))
# ==============================================================================
def compute_lps_array(pattern: str) -> list[int]:
    """
    Computes the Longest Proper Prefix which is also Suffix (LPS).
    This array tells the KMP algorithm how to safely backtrack during a mismatch.
    Time Complexity: O(M) where M is length of the pattern.
    """
    m = len(pattern)
    lps = [0] * m
    
    # Length of the previous longest prefix suffix
    length = 0 
    
    # Start checking from index 1 (since lps[0] is always 0)
    i = 1 
    
    while i < m:
        if pattern[i] == pattern[length]:
            # It matches! Extend the known prefix length!
            length += 1
            lps[i] = length
            i += 1
        else:
            # MISMATCH DETECTED!
            if length != 0:
                # We do NOT reset length to 0!
                # We consult the LPS array to gracefully fall back to a smaller, 
                # previously known valid prefix. 
                # Notice we do NOT increment `i`. We will re-test this same character!
                length = lps[length - 1]
            else:
                # Absolute failure. No prefix exists. We write 0 and move on.
                lps[i] = 0
                i += 1
                
    return lps

def kmp_search(text: str, pattern: str) -> list[int]:
    """
    Finds all occurrences of `pattern` in `text` using KMP.
    Time Complexity: O(N + M) where N = len(text), M = len(pattern)
    Space Complexity: O(M) for the LPS array.
    """
    n = len(text)
    m = len(pattern)
    
    if m == 0: return []
    
    lps = compute_lps_array(pattern)
    
    i = 0 # index for text
    j = 0 # index for pattern
    
    matches = []
    
    while i < n:
        if pattern[j] == text[i]:
            # Characters match! Advance both pointers!
            i += 1
            j += 1
            
        if j == m:
            # PERFECT MATCH! We reached the end of the pattern!
            # We record the starting index of the match (i - j)
            matches.append(i - j)
            
            # To continue searching for more matches, we consult the LPS array 
            # to gracefully backtrack `j` instead of resetting it to 0!
            j = lps[j - 1]
            
        elif i < n and pattern[j] != text[i]:
            # MISMATCH DETECTED!
            if j != 0:
                # Do NOT reset `j` to 0! 
                # Do NOT reset `i`!
                # Ask the LPS array how much of the pattern we can salvage!
                j = lps[j - 1]
            else:
                # We couldn't salvage anything. Advance the text pointer.
                i += 1
                
    return matches

def demonstrate_kmp():
    section_header("KMP String Search Algorithm")
    
    pattern = "ABABCABAB"
    text = "ABABDABACDABABCABABABABCABAB"
    
    print(f"Pattern: {pattern}")
    print(f"Text   : {text}")
    
    lps = compute_lps_array(pattern)
    print(f"\nPrecomputed LPS Array: {lps}")
    print("This array is the mathematical brain of the algorithm.")
    
    matches = kmp_search(text, pattern)
    print(f"\nMatches found at indices: {matches}")
    
    print("\nVisual Verification:")
    for idx in matches:
        print(f"Index {idx:2d}: {text[idx:idx+len(pattern)]}")


def run_all_labs():
    demonstrate_kmp()


# ==============================================================================
# 4. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. What does LPS stand for, and what does the value `lps[5] = 2` physically mean?
   Answer: LPS stands for "Longest Proper Prefix which is also Suffix". A proper prefix cannot be the entire string itself. If `lps[5] = 2`, it means that if you look at the substring spanning from index 0 to index 5, the first 2 characters of that substring (the Prefix) are mathematically identical to the last 2 characters of that substring (the Suffix). 

2. How does the LPS array mathematically prevent the KMP algorithm from ever moving the Text pointer (`i`) backwards?
   Answer: Imagine the pattern is `A B A B X`. You are scanning the text. You match `A B A B`, but fail on `X` (the text had a `Z`). In a naive algorithm, you reset `i` all the way back to the second character and start over. But KMP looks at the LPS array for `A B A B`, which is `2`. The LPS array says: "Hey! You failed at the end, but the suffix of what you just matched (`A B`) is identical to the prefix of the pattern (`A B`)! Therefore, you don't need to backtrack the text pointer! You can mathematically assume that the first 2 characters of the pattern have ALREADY matched the text!" KMP instantly shifts the pattern's pointer `j` to index 2, perfectly salvaging the partial match while keeping the text pointer `i` relentlessly moving forward, achieving strict $O(N)$ time.

3. Explain the exact mechanism of the line `length = lps[length - 1]` inside the LPS generation function when a mismatch occurs.
   Answer: This line is a brilliant, recursive-like fallback. Suppose you have matched a prefix of length 4 (`A B C D`), and you are trying to match the 5th character (`E`). But the character fails. You do not drop the length to 0! You ask the LPS array: "Within the `A B C D` that we just successfully matched, what is the largest internal prefix-suffix overlap?" You check `lps[4 - 1]`. Let's say it returns 1. This means you can salvage a length of 1 (`A`). You instantly set `length = 1`, and attempt to match the 2nd character (`B`) against the failure point. The algorithm gracefully cascades down the LPS states, salvaging as much pattern as mathematically possible before hitting 0.
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: KMP String Matching Completed.")
