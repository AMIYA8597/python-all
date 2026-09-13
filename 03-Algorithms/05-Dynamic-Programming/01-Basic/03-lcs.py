"""
# ==============================================================================
# LABORATORY: LONGEST COMMON SUBSEQUENCE (2D DYNAMIC PROGRAMMING)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A "Subsequence" is a sequence derived from a string by deleting some (or no) 
# characters without changing the order. 
# (e.g. "ACE" is a subsequence of "ABCDE").
#
# A "Substring" must be strictly contiguous.
# (e.g. "ABC" is a substring of "ABCDE", but "ACE" is not).
#
# The Longest Common Subsequence (LCS) problem asks: Given two strings, what is 
# the length of the longest subsequence they both share?
# This algorithm is incredibly important. It is the core mathematical engine 
# behind `git diff`! When Git tells you exactly which lines you inserted and 
# deleted in a file, it ran LCS on the two versions of the file.
#
# This introduces 2D Dynamic Programming. Because we are comparing TWO independent 
# strings, our State cannot be a flat 1D array. It must be a 2D Matrix (Grid).
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the 2D Grid structure for string comparisons.
# - Master the State Transition Equation (Diagonal vs Top/Left).
# - Understand how to build the table Bottom-Up.
#
# ==============================================================================
"""

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. BOTTOM-UP 2D TABULATION
# ==============================================================================
def longest_common_subsequence(text1: str, text2: str) -> int:
    """
    Time Complexity: O(M * N) where M and N are string lengths.
    Space Complexity: O(M * N) for the 2D DP matrix.
    """
    m = len(text1)
    n = len(text2)
    
    # 1. STATE DEFINITION
    # `dp[i][j]` represents the LCS length of the prefix `text1[0:i]` 
    # and the prefix `text2[0:j]`.
    
    # 2. INITIALIZATION
    # We create a 2D matrix of size (M+1) x (N+1), filled with 0s.
    # Why the +1? We need a "dummy" row and column at the very beginning (Index 0) 
    # to represent comparing a string against an EMPTY string. 
    # The LCS of any string and an empty string is always 0!
    dp = [[0 for _ in range(n + 1)] for _ in range(m + 1)]
    
    # 3. TABULATION LOOP
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            
            # --- STATE TRANSITION EQUATION ---
            
            # Remember: Strings are 0-indexed, but our DP table is 1-indexed.
            # So `i-1` and `j-1` point to the actual characters we are currently comparing!
            if text1[i - 1] == text2[j - 1]:
                # CASE 1: MATCH!
                # The characters match. We look at the top-left DIAGONAL (dp[i-1][j-1]), 
                # which represents the LCS of the strings BEFORE these matching characters.
                # We add 1 to it!
                dp[i][j] = 1 + dp[i - 1][j - 1]
            else:
                # CASE 2: MISMATCH
                # They don't match. The optimal LCS up to this point must be the 
                # maximum of either ignoring the character from text1 (look UP), 
                # or ignoring the character from text2 (look LEFT).
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
                
    # The absolute final answer is in the bottom-right corner of the grid!
    return dp[m][n]


def demonstrate_lcs():
    section_header("Algorithm: Longest Common Subsequence")
    
    text1 = "abcde"
    text2 = "ace"
    
    print(f"String 1: {text1}")
    print(f"String 2: {text2}")
    
    ans = longest_common_subsequence(text1, text2)
    print(f"LCS Length: {ans} (Expected: 3 -> 'ace')\n")
    
    text1 = "abc"
    text2 = "def"
    print(f"String 1: {text1}")
    print(f"String 2: {text2}")
    
    ans = longest_common_subsequence(text1, text2)
    print(f"LCS Length: {ans} (Expected: 0 -> no common letters)")


# ==============================================================================
# 4. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why is the DP Matrix sized `(M+1)` and `(N+1)` instead of just `M` and `N`?
   Answer: To prevent Out-Of-Bounds indexing errors. In the `text1 == text2` case, we look at the diagonal `dp[i-1][j-1]`. If we didn't have the padding row of zeroes, querying `i-1` when `i=0` would crash the program. The padding provides mathematically correct "Base Cases" (Empty Strings = 0) that instantly solve the boundary conditions.

2. Can we Space-Optimize this from $O(M \\times N)$ to $O(\\min(M, N))$?
   Answer: Yes! Look at the State Transition Equation. To calculate the values for the current row `i`, we ONLY look at the current row `i` and the previous row `i-1`. We never look at row `i-2`. Therefore, we don't need a massive 2D grid! We can just keep two 1D arrays: `previous_row` and `current_row`, and swap them on every loop iteration, reducing space complexity massively.

3. How does `git diff` use this algorithm?
   Answer: Once you build the DP matrix, the number in the bottom right corner is the length of the LCS. But you don't know WHAT the sequence is! To find the actual sequence (or the diffs), you start at the bottom right corner and "Backtrack" up the matrix. If the characters match, you record it and step diagonally left-up. If they mismatch, you step in the direction of the `max(UP, LEFT)`.
"""

if __name__ == "__main__":
    demonstrate_lcs()
    print("\n[SUCCESS] Laboratory: LCS 2D-DP Completed.")
