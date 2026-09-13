"""
# ==============================================================================
# LABORATORY: EDIT DISTANCE (LEVENSHTEIN DISTANCE)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# If you type "teh" into Google, it instantly asks: "Did you mean: the?"
# How does it know that? 
# Because the "Edit Distance" between "teh" and "the" is extremely small.
#
# The Edit Distance (invented by Vladimir Levenshtein in 1965) is the minimum 
# number of operations required to transform Word A into Word B.
# You are allowed exactly 3 mathematical operations:
# 1. INSERT a character
# 2. DELETE a character
# 3. REPLACE a character
#
# This algorithm is the engine behind Autocorrect, DNA Sequence Alignment 
# (Bioinformatics), Plagiarism Detection, and Fuzzy String Matching.
#
# Like Longest Common Subsequence (LCS), this requires 2D Dynamic Programming.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Model string transformations on a 2D Grid.
# - Map Insert/Delete/Replace to grid movements (Left, Up, Diagonal).
# - Implement the 2D Tabulation logic.
#
# ==============================================================================
"""

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. 2D TABULATION
# ==============================================================================
def min_distance(word1: str, word2: str) -> int:
    """
    Time Complexity: O(M * N) where M and N are string lengths.
    Space Complexity: O(M * N) for the DP table.
    """
    m = len(word1)
    n = len(word2)
    
    # 1. STATE DEFINITION
    # `dp[i][j]` represents the Minimum Operations required to convert the 
    # prefix `word1[0:i]` into the prefix `word2[0:j]`.
    
    dp = [[0 for _ in range(n + 1)] for _ in range(m + 1)]
    
    # 2. INITIALIZATION (THE BASE CASES)
    # What if word2 is empty? (j=0)
    # The only way to convert "abc" into "" is to DELETE all 3 characters.
    # So `dp[i][0] = i`.
    for i in range(m + 1):
        dp[i][0] = i
        
    # What if word1 is empty? (i=0)
    # The only way to convert "" into "abc" is to INSERT all 3 characters.
    # So `dp[0][j] = j`.
    for j in range(n + 1):
        dp[0][j] = j
        
    # 3. TABULATION LOOP
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            
            # Remember: DP array is 1-indexed (padding), strings are 0-indexed.
            if word1[i - 1] == word2[j - 1]:
                
                # CASE 1: MATCH
                # The characters are identical! We don't need to do any operations.
                # The cost is exactly the same as the cost BEFORE these characters 
                # were added (Look at the Top-Left Diagonal).
                dp[i][j] = dp[i - 1][j - 1]
                
            else:
                # CASE 2: MISMATCH
                # The characters are different. We must use exactly 1 operation.
                # Which operation is the cheapest? We check all 3 adjacent cells!
                
                # A. REPLACE: Look Diagonal. We magically replaced the mismatch, 
                # so the cost is 1 + the cost of everything before it.
                replace_cost = dp[i - 1][j - 1]
                
                # B. DELETE: Look Up. We delete the character from word1, so we 
                # step backwards in word1 (i-1) but stay at the same target (j).
                delete_cost = dp[i - 1][j]
                
                # C. INSERT: Look Left. We magically insert the missing character 
                # into word1, which matches word2 (so j steps backwards), but 
                # word1 hasn't processed its current character yet (i stays).
                insert_cost = dp[i][j - 1]
                
                # Take the absolute cheapest path and add 1 (for the operation itself)
                dp[i][j] = 1 + min(replace_cost, delete_cost, insert_cost)
                
    return dp[m][n]


def demonstrate_edit_distance():
    section_header("Algorithm: Edit Distance")
    
    word1 = "horse"
    word2 = "ros"
    
    print(f"Transforming '{word1}' into '{word2}'...")
    print("Operations allowed: Insert, Delete, Replace.\n")
    
    ans = min_distance(word1, word2)
    print(f"Minimum Operations: {ans} (Expected: 3)")
    print(" 1. horse -> rorse (Replace 'h' with 'r')")
    print(" 2. rorse -> rose  (Delete 'r')")
    print(" 3. rose  -> ros   (Delete 'e')\n")
    
    word1 = "intention"
    word2 = "execution"
    print(f"Transforming '{word1}' into '{word2}'...")
    ans = min_distance(word1, word2)
    print(f"Minimum Operations: {ans} (Expected: 5)")


# ==============================================================================
# 4. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. What do the 3 directions in the DP grid physically represent?
   Answer: 
   - Moving DIAGONAL (`i-1, j-1`): Processing both characters simultaneously. (If they match, cost is 0. If they mismatch, it represents a REPLACE operation, cost is 1).
   - Moving UP (`i-1, j`): Skipping a character in `word1`. This represents a DELETE operation.
   - Moving LEFT (`i, j-1`): Skipping a character in `word2`. This represents an INSERT operation into `word1`.

2. How is this used in Bioinformatics (DNA)?
   Answer: In bioinformatics, this is known as the "Needleman-Wunsch Algorithm" (for global alignment) or "Smith-Waterman Algorithm" (for local alignment). When scientists compare two DNA strands (e.g. "ACGTG" vs "ACGCT"), they use Edit Distance to see how closely related the species are, or to locate genetic mutations. They assign different "Penalty Scores" (e.g., an Insertion might cost 2 points, but a Replace might cost 5 points).

3. Can we Space-Optimize this algorithm?
   Answer: Yes! Exactly like LCS. The mathematical equation `dp[i][j]` only ever references the current row `i` (for insertions) and the previous row `i-1` (for deletions and replacements). Therefore, you don't need an $O(M \\times N)$ grid. You only need two 1D arrays of size $N$, swapping them on every loop, dropping the space complexity to $O(N)$.
"""

if __name__ == "__main__":
    demonstrate_edit_distance()
    print("\n[SUCCESS] Laboratory: Edit Distance Completed.")
