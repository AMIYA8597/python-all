"""
# ==============================================================================
# LABORATORY: MANACHER'S ALGORITHM (LONGEST PALINDROME)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You are given a string "BABAD". What is the Longest Palindromic Substring? 
# ("BAB" or "ABA").
#
# - Naive Brute Force: Check every possible substring. O(N^3).
# - "Expand Around Center": Pick every character, and physically expand left 
#   and right as far as possible. There are 2N-1 centers (to account for even 
#   length palindromes like "ABBA"). This takes O(N^2) time. This is the standard 
#   FAANG interview answer!
#
# But can we do it in strict O(N) linear time?
# In 1975, Glenn Manacher achieved the impossible. 
#
# The Core Insight: MIRRORING.
# Imagine you found a massive palindrome: "XYABACABA...".
# The center is 'C'. You are currently expanding around the 'B' on the right side.
# Wait... you ALREADY expanded around the 'B' on the left side! 
# Because the entire string is a palindrome around 'C', the right side is a 
# mathematically perfect mirror of the left side!
# You don't need to expand around the right 'B' from scratch. You just copy the 
# previously calculated radius from the left mirror!
#
# This uses the exact same `[L, R]` boundary logic as the Z-Algorithm to ensure 
# we never do redundant character comparisons, achieving a flawless O(N) runtime.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - The `#` Transformation (Unifying Even/Odd Palindromes).
# - The Center and Right-Bound `[C, R]` state tracking.
# - The Mirror Index formula: `mirror = 2*C - i`.
#
# ==============================================================================
"""

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. MANACHER'S ENGINE (O(N))
# ==============================================================================
def manachers_algorithm(s: str) -> str:
    """
    Finds the Longest Palindromic Substring in strict O(N) time.
    """
    if not s:
        return ""
        
    # --------------------------------------------------------------------------
    # 1. THE STRING TRANSFORMATION
    # --------------------------------------------------------------------------
    # Odd palindromes ("ABA") have a clear center ('B').
    # Even palindromes ("ABBA") do NOT have a clear center.
    # To fix this, we inject a dummy character '#' between EVERY letter.
    # "ABBA" becomes "#A#B#B#A#". 
    # Now, the center of the palindrome is the middle '#'!
    # We add '^' and '$' at the ends to prevent out-of-bounds errors, eliminating 
    # the need for constant boundary `if` checks during expansion!
    T = "^#" + "#".join(s) + "#$"
    n = len(T)
    
    # P[i] stores the RADIUS of the longest palindrome centered at index `i`.
    P = [0] * n
    
    # C = The Center of the palindrome that extends furthest to the right.
    # R = The Rightmost boundary of that palindrome.
    C = 0
    R = 0
    
    # --------------------------------------------------------------------------
    # 2. THE LINEAR SCAN (O(N))
    # --------------------------------------------------------------------------
    for i in range(1, n - 1):
        
        # Calculate the mirror index of `i` perfectly reflected across the Center `C`.
        # Math: C - mirror = i - C  =>  mirror = 2*C - i
        mirror = 2 * C - i
        
        # CASE 1: We are INSIDE the right boundary `R`.
        # We can instantly copy the radius from the left mirror!
        if i < R:
            # We take the MINIMUM of the mirror's radius, and the distance from 
            # `i` to the boundary `R`. 
            # Why? Because if the mirror's palindrome was so huge that it expands 
            # OUTSIDE the boundary `R` on the left, we cannot guarantee the right 
            # side mirrors it outside `R` (uncharted territory)!
            P[i] = min(R - i, P[mirror])
            
        # ----------------------------------------------------------------------
        # 3. THE EXPANSION (UNCHARTED TERRITORY)
        # ----------------------------------------------------------------------
        # We physically expand left and right, but ONLY starting from the radius 
        # we legally verified above! 
        # (If P[i] is 0, it starts from scratch. If P[i] is 3, it instantly starts 
        # checking the 4th character out!)
        # The '^' and '$' characters mathematically guarantee this loop will 
        # eventually hit a mismatch and never crash out of bounds!
        while T[i + (1 + P[i])] == T[i - (1 + P[i])]:
            P[i] += 1
            
        # 4. UPDATE THE BOUNDARY
        # If this new palindrome extends further right than our current `R`, 
        # it becomes the new global Center of attention!
        if i + P[i] > R:
            C = i
            R = i + P[i]
            
    # --------------------------------------------------------------------------
    # 5. EXTRACT THE WINNER
    # --------------------------------------------------------------------------
    max_radius = 0
    center_index = 0
    
    for i in range(1, n - 1):
        if P[i] > max_radius:
            max_radius = P[i]
            center_index = i
            
    # The true length of the palindrome in the original string is EXACTLY the 
    # radius in the transformed string!
    # To extract the original string, we find the start index in the original 
    # string using math: (CenterIndex - 1 - MaxRadius) // 2
    
    start_index = (center_index - 1 - max_radius) // 2
    return s[start_index : start_index + max_radius]


def demonstrate_manacher():
    section_header("Algorithm: Manacher's Longest Palindrome")
    
    test_strings = [
        "BABAD",
        "CBBD",
        "A",
        "ACACACACACACA",
        "XYABACABAQ"
    ]
    
    for s in test_strings:
        print(f"\nOriginal String: '{s}'")
        lps = manachers_algorithm(s)
        print(f"Longest Palindromic Substring: '{lps}' (Length: {len(lps)})")
        
    section_header("The Magic of the '#' Transformation")
    s = "ABBA"
    T = "^#" + "#".join(s) + "#$"
    print(f"Original: {s}")
    print(f"Transformed: {T}")
    print("Notice the center is exactly at index 5 ('#').")
    print("Radius at index 5 is 4. Original length is 4. The math aligns perfectly!")


# ==============================================================================
# 4. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why does Manacher's Algorithm mathematically guarantee $O(N)$ execution time?
   Answer: Look at the `R` pointer (the Right boundary). It ONLY ever increments. Inside the inner `while` loop (the physical character-expansion check), every time a character matches, `P[i]` increases by 1. But more importantly, because it matched, `i + P[i]` increases, pushing `R` further to the right! Because `R` can mathematically only increment a maximum of $2N$ times (the length of the transformed string), the physical character check can only execute a total of $2N$ times across the entire lifespan of the algorithm. Thus, it is $O(N)$!

2. Why do we need the $min(R - i, P[mirror])$ bound?
   Answer: Imagine the string: `X [A B A C A B A] Y`. Center `C` is at `C`. `R` is at `]`. 
   We are evaluating the right `B`. Its mirror is the left `B`.
   What if the left string was actually `A [A B A C A B A] Y`?
   The left `B` is the center of the palindrome `AABA` (radius 2). 
   However, the radius extends OUTSIDE the left boundary `[`! We have NO IDEA what is outside the right boundary `]`. In this case, the right side has a `Y`, not an `A`. If we blindly copied the mirror's radius of 2, we would falsely claim the right side is `YBAY` without checking! The `min()` forces the algorithm to safely truncate the copied radius precisely at the `R` boundary, and manually verify the uncharted territory via the `while` loop!

3. If Manacher's is $O(N)$, why do FAANG interviews expect "Expand Around Center" $O(N^2)$?
   Answer: Manacher's Algorithm is considered a "Competitive Programming" or textbook "Aha!" trick. The state management of `C` and `R` is highly brittle and easily forgotten under the intense stress of a 40-minute whiteboard interview. The $O(N^2)$ Expand Around Center approach demonstrates core algorithmic fundamentals (two-pointer expansion, handling even/odd states elegantly) without requiring memorized magic math.
"""

if __name__ == "__main__":
    demonstrate_manacher()
    print("\n[SUCCESS] Laboratory: Manacher's Algorithm Completed.")
