"""
# ==============================================================================
# LABORATORY: BOYER-MOORE (SUB-LINEAR STRING MATCHING)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# KMP and Rabin-Karp are brilliant, mathematically guaranteeing O(N) time.
# That means to search a 1,000,000 character webpage, they must execute roughly 
# 1,000,000 operations.
#
# Can we search a 1,000,000 character webpage in only 100,000 operations? 
# Can we search FASTER than O(N)? 
#
# In 1977, Robert Boyer and J Strother Moore achieved the impossible: Sub-Linear 
# time complexity. They proved that the longer your search pattern is, the FASTER 
# the algorithm finishes.
#
# Their stroke of genius: Read the pattern BACKWARDS.
# 
# Imagine searching for the 7-letter word "EXAMPLE" inside a massive document.
# The window covers the first 7 letters: [A, B, C, D, E, F, Z].
#
# Naive and KMP look at the 'A'. 
# Boyer-Moore looks at the 'Z' (the LAST character of the window).
# It asks: "Does the letter 'Z' exist ANYWHERE inside the word 'EXAMPLE'?"
# Answer: No! 
# 
# Conclusion: It is mathematically impossible for the word 'EXAMPLE' to exist 
# anywhere that overlaps with that 'Z'. 
# Boyer-Moore instantly slides the ENTIRE 7-character window forward!
# With one single check, it skipped 7 characters. It achieves O(N / M) speed!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the "Bad Character Heuristic".
# - Implement the Bad Character Hash Map.
# - Master right-to-left inner loop checking.
#
# ==============================================================================
"""

from typing import List, Dict

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. BAD CHARACTER HEURISTIC ENGINE
# ==============================================================================
def build_bad_char_table(pattern: str) -> Dict[str, int]:
    """
    Precomputes the 'Bad Character' rule map. O(M)
    For every character in the pattern, we record its LAST KNOWN (rightmost) 
    index. If the character appears multiple times, the rightmost index overwrites 
    the older ones.
    """
    bad_char_table = {}
    for i in range(len(pattern)):
        bad_char_table[pattern[i]] = i
    return bad_char_table


# ==============================================================================
# 4. BOYER-MOORE SEARCH ENGINE (O(N / M) Average)
# ==============================================================================
def boyer_moore_search(text: str, pattern: str) -> List[int]:
    """
    Average Time Complexity: O(N / M)
    Worst Case (Pathological): O(N * M)
    """
    n = len(text)
    m = len(pattern)
    
    if m == 0 or m > n:
        return []
        
    found_indices = []
    
    # 1. Precompute the Bad Character Map
    bad_char = build_bad_char_table(pattern)
    
    # `s` is the shift of the pattern with respect to the text
    s = 0 
    
    # 2. The Main Outer Loop
    while s <= (n - m):
        
        # We start checking from the RIGHT end of the pattern!
        j = m - 1
        
        # 3. Right-to-Left Inner Loop
        # Keep moving left as long as characters match
        while j >= 0 and pattern[j] == text[s + j]:
            j -= 1
            
        # 4. MISMATCH RESOLUTION
        if j < 0:
            # We perfectly matched the entire pattern backwards!
            found_indices.append(s)
            
            # Slide the pattern to search for the next occurrence.
            # Look at the character sitting directly immediately after our pattern 
            # in the text. Does it exist in our Bad Character Map?
            # If so, align it! If not, slide by a full length M!
            if s + m < n:
                next_char_in_text = text[s + m]
                rightmost_index_in_pattern = bad_char.get(next_char_in_text, -1)
                s += m - rightmost_index_in_pattern
            else:
                s += 1 # We reached the absolute end of the text
                
        else:
            # A MISMATCH occurred at index `j` of the pattern!
            # The mismatched character in the text is `text[s + j]`.
            bad_character = text[s + j]
            
            # Where is the rightmost occurrence of this bad character in our pattern?
            rightmost_index = bad_char.get(bad_character, -1)
            
            # We want to slide the pattern to the right so that `rightmost_index` 
            # aligns with the bad character in the text.
            shift_distance = j - rightmost_index
            
            # Edge Case: What if the rightmost occurrence is to the RIGHT of our 
            # current `j`? That would mean sliding backwards! We never slide backwards.
            # We enforce a minimum slide of 1.
            s += max(1, shift_distance)
            
    return found_indices


def demonstrate_boyer_moore():
    section_header("Algorithm: Boyer-Moore (Sub-Linear Search)")
    
    # --- Example 1: Understanding the Slide ---
    pattern = "EXAMPLE"
    bad_char = build_bad_char_table(pattern)
    print("Pattern: EXAMPLE")
    print(f"Bad Character Map: {bad_char}")
    print("Notice how 'E' maps to 6 (the last E), not 0!")
    
    section_header("Boyer-Moore Execution")
    
    text = "THIS IS A TEST OF THE BOYER MOORE EXAMPLE STRING MATCHING ALGO"
    search_pattern = "EXAMPLE"
    
    print(f"Text length: {len(text)}")
    print(f"Pattern length: {len(search_pattern)}")
    
    print("\nExecuting Right-to-Left Window Checking...")
    indices = boyer_moore_search(text, search_pattern)
    
    print(f"\nFound exact matches at starting indices: {indices}")
    if indices:
        start = indices[0]
        end = start + len(search_pattern)
        print(f"Extraction: '{text[start:end]}'")


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why does checking right-to-left make it $O(N / M)$?
   Answer: In English text, most characters in the text do NOT exist in the search pattern. If we check the very LAST character of the window (rightmost) and it mismatches, and that mismatched character doesn't exist anywhere in the pattern, we mathematically prove that the pattern cannot possibly overlap with this entire window. We instantly slide the window forward by exactly $M$ spaces. If the text is $N$ characters, and we jump $M$ spaces every time, we finish the entire search in exactly $N / M$ operations! Sub-linear!

2. What is the $s += \max(1, j - \text{rightmost\_index})$ safety constraint?
   Answer: Imagine Pattern="ABA", Text="...OBA...". 
   We check backwards. 'A' vs 'A' (Match, $j=2$). 
   'B' vs 'B' (Match, $j=1$). 
   'A' vs 'O' (Mismatch at $j=0$). 
   The bad character in the text is 'O'. 'O' is not in our map (so it is $-1$). $j - (-1) = 1$. We shift by 1.
   But what if Pattern="AABB", Text="...BAB...". 
   Match 'B' at $j=3$. 
   Mismatch at $j=2$ ('B' vs 'A'). 
   The bad char in the text is 'A'. The map says 'A' exists at index 1! 
   $j - 1 = 2 - 1 = 1$. Shift by 1.
   If the map said 'A' was at index 5 (to the right of our current $j$), $j - 5$ would be negative! The pattern would slide backwards, creating an infinite loop. We force `max(1, ...)` to ensure the window always marches forward.

3. Is the Bad Character Heuristic the complete Boyer-Moore algorithm?
   Answer: No! The full standard algorithm (used in GNU `grep` and Python's `find`) also includes the "Good Suffix Heuristic". If a partial suffix matches, but the next character fails, it uses a pre-calculated table (similar to KMP's LPS array) to slide the pattern so that the matched suffix perfectly aligns with another occurrence of that same suffix earlier in the pattern. The Bad Character rule is amazing for large alphabets (English text), but the Good Suffix rule is mandatory for small alphabets (DNA sequences ACGT) to prevent worst-case $O(N \\times M)$ performance.
"""

if __name__ == "__main__":
    demonstrate_boyer_moore()
    print("\n[SUCCESS] Laboratory: Boyer-Moore Algorithm Completed.")
