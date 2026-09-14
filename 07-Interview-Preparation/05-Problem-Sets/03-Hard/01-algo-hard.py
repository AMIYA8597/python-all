"""
# ==============================================================================
# LABORATORY: INTERVIEW PREPARATION (PROBLEM SETS - ALGORITHM HARD)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# "Hard" Algorithm problems are usually the final boss in a Staff or Principal 
# level interview. They require fusing multiple advanced data structures (e.g., 
# Queues + Sets + String Mutations) or discovering extreme mathematical optimizations 
# (e.g., executing Binary Search across multiple arrays simultaneously).
#
# A junior engineer solves 'N-Queens' by generating every single permutation 
# of a chessboard and validating it. This takes O(N^N) and crashes instantly.
# 
# A senior engineer uses Mathematical Backtracking with O(1) State Sets. They 
# mathematically project the diagonals (Row - Col, Row + Col) and instantly 
# abort dead-end recursive branches, finding the solution in a highly optimized 
# O(N!) path.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master Mathematical Backtracking with Set Constraints (N-Queens).
# - Master Multi-Array Logarithmic Partitioning (Median of Two Sorted Arrays).
# - Master String Permutation BFS (Word Ladder).
#
# ==============================================================================
"""

import collections
from typing import List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. N-QUEENS (MATHEMATICAL BACKTRACKING)
# ==============================================================================
def solve_n_queens(n: int) -> List[List[str]]:
    """
    Time: O(N!) | Space: O(N)
    Place N queens on an NxN chessboard such that no two queens attack each other.
    """
    # Mathematical constraints!
    # A queen attacks vertically (Cols), and diagonally (Pos/Neg Diagonals).
    # We do NOT need to track Rows because our Backtracking algorithm strictly 
    # places exactly ONE queen per row!
    cols = set()
    pos_diag = set() # (Row + Col) is mathematically constant along a positive diagonal (/)
    neg_diag = set() # (Row - Col) is mathematically constant along a negative diagonal (\)
    
    res = []
    board = [["."] * n for _ in range(n)]
    
    def backtrack(r: int):
        # BASE CASE: We successfully placed a queen on every single row!
        if r == n:
            # We must join the arrays into strings before saving!
            copy = ["".join(row) for row in board]
            res.append(copy)
            print(f"    -> [SUCCESS] Perfect board state achieved!")
            return
            
        for c in range(n):
            # CONFLICT DETECTION
            if c in cols or (r + c) in pos_diag or (r - c) in neg_diag:
                continue # This position is under attack! Skip it!
                
            # PLACE THE QUEEN (Modify State)
            cols.add(c)
            pos_diag.add(r + c)
            neg_diag.add(r - c)
            board[r][c] = "Q"
            
            # RECURSE DEEPER (Go to the next row!)
            backtrack(r + 1)
            
            # BACKTRACK (Revert State!)
            # Once we return from the recursion, we MUST pull the queen off the 
            # board so we can test the next column!
            cols.remove(c)
            pos_diag.remove(r + c)
            neg_diag.remove(r - c)
            board[r][c] = "."
            
    print(f"  Executing Backtracking Engine for {n}x{n} Board...")
    backtrack(0)
    return res

def demonstrate_n_queens():
    section_header("Hard: N-Queens (Mathematical Backtracking)")
    
    n = 4
    ans = solve_n_queens(n)
    
    print(f"\nResult: Found {len(ans)} distinct solutions.")
    for idx, board in enumerate(ans):
        print(f"\nSolution {idx + 1}:")
        for row in board:
            print(f"  {row}")


# ==============================================================================
# 4. MEDIAN OF TWO SORTED ARRAYS (LOGARITHMIC PARTITIONING)
# ==============================================================================
def find_median_sorted_arrays(nums1: List[int], nums2: List[int]) -> float:
    """
    Time: O(log(min(m, n))) | Space: O(1)
    Given two sorted arrays nums1 and nums2 of size m and n respectively, 
    return the median of the two sorted arrays.
    
    A junior uses `sorted(nums1 + nums2)` taking O((M+N) log(M+N)) Time.
    A senior mathematically partitions both arrays simultaneously using Binary Search!
    """
    A, B = nums1, nums2
    total_length = len(nums1) + len(nums2)
    half = total_length // 2
    
    # We strictly enforce that A is the SMALLER array, so we can binary search 
    # it safely without risking Out of Bounds exceptions!
    if len(B) < len(A):
        A, B = B, A
        
    left, right = 0, len(A) - 1
    
    print(f"  Array 1: {A}")
    print(f"  Array 2: {B}")
    print("  Deploying Dual-Array Partition Search...")
    
    while True:
        # 1. Calculate the Partition indices!
        i = left + (right - left) // 2 # Partition for A
        j = half - i - 2               # Partition for B
        
        # 2. Extract the boundary values! (Using Infinity for edges!)
        A_left  = A[i] if i >= 0 else float('-infinity')
        A_right = A[i + 1] if (i + 1) < len(A) else float('infinity')
        
        B_left  = B[j] if j >= 0 else float('-infinity')
        B_right = B[j + 1] if (j + 1) < len(B) else float('infinity')
        
        # 3. VERIFY THE MATHEMATICAL PARTITION
        # If the largest element on the Left of A is <= the smallest on the Right of B
        # AND the largest element on the Left of B is <= the smallest on the Right of A...
        if A_left <= B_right and B_left <= A_right:
            print("    -> [MATCH] Perfect partition found!")
            
            # If the total length is ODD, the median is just the smallest element on the right!
            if total_length % 2:
                return min(A_right, B_right)
                
            # If the total length is EVEN, we must average the max of the left and min of the right!
            return (max(A_left, B_left) + min(A_right, B_right)) / 2
            
        # 4. ADJUST THE PARTITION
        elif A_left > B_right:
            # A's left is too big! We must shrink A's partition to the left!
            right = i - 1
        else:
            # A's left is too small! We must expand A's partition to the right!
            left = i + 1

def demonstrate_median():
    section_header("Hard: Median of Two Sorted Arrays (O(log(min(M,N))))")
    
    nums1 = [1, 3]
    nums2 = [2]
    ans = find_median_sorted_arrays(nums1, nums2)
    print(f"\nResult: Median is {ans} (Expected: 2.0)")


# ==============================================================================
# 5. WORD LADDER (STRING PERMUTATION BFS)
# ==============================================================================
def ladder_length(beginWord: str, endWord: str, wordList: List[str]) -> int:
    """
    Time: O(M^2 * N) | Space: O(M * N)
    Return the number of words in the shortest transformation sequence.
    """
    if endWord not in wordList:
        return 0
        
    wordList.append(beginWord)
    
    # 1. BUILD THE ADJACENCY HASH MAP (Pattern -> Words)
    # E.g., The pattern "d*g" maps to ["dog", "dig"]
    # This prevents us from having to compare every word to every other word!
    neighbors = collections.defaultdict(list)
    for word in wordList:
        for j in range(len(word)):
            pattern = word[:j] + "*" + word[j+1:]
            neighbors[pattern].append(word)
            
    # 2. BREADTH-FIRST SEARCH (Shortest Path!)
    visit = set([beginWord])
    queue = collections.deque([beginWord])
    res = 1
    
    print(f"  Pathfinding: '{beginWord}' -> '{endWord}'")
    
    while queue:
        # Process level by level
        for _ in range(len(queue)):
            word = queue.popleft()
            
            if word == endWord:
                print(f"    -> [SUCCESS] Reached target in {res} steps!")
                return res
                
            # Generate the patterns for the current word!
            for j in range(len(word)):
                pattern = word[:j] + "*" + word[j+1:]
                
                # Instantly retrieve all words that mathematically match this pattern!
                for nei_word in neighbors[pattern]:
                    if nei_word not in visit:
                        visit.add(nei_word)
                        queue.append(nei_word)
                        
        # We finished exploring all words at the current depth!
        res += 1
        
    print("    -> [FAIL] No path exists.")
    return 0

def demonstrate_ladder():
    section_header("Hard: Word Ladder (String Mutation BFS)")
    
    beginWord = "hit"
    endWord = "cog"
    wordList = ["hot","dot","dog","lot","log","cog"]
    
    ans = ladder_length(beginWord, endWord, wordList)
    print(f"\nResult: {ans} transitions (Expected: 5)")


def run_all_labs():
    demonstrate_n_queens()
    demonstrate_median()
    demonstrate_ladder()


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "In N-Queens, mathematically explain how the expression `r + c` flawlessly tracks a Positive Diagonal, and `r - c` tracks a Negative Diagonal."
   Senior Answer: "On an NxN Cartesian matrix, a diagonal line moving from the bottom-left to the top-right (/) possesses a slope where moving up 1 row ($-1$ index) requires moving right 1 column ($+1$ index). Therefore, the sum of `Row + Col` is mathematically invariant (constant) for every single square on that specific diagonal! Conversely, a diagonal moving from top-left to bottom-right (\\) requires moving down 1 row ($+1$ index) and right 1 column ($+1$ index). Therefore, the difference `Row - Col` remains perfectly constant. By caching these constant values into an $O(1)$ Hash Set, we can instantly determine if a square is under diagonal attack without physically scanning the board."

2. Interviewer: "In the Median of Two Sorted Arrays, why is calculating `(left + right) // 2` dangerous in languages like Java or C++, and how does Python handle it?"
   Senior Answer: "In Java or C++, integers are strictly bounded to 32 bits (Maximum value: $2,147,483,647$). If `left` and `right` are both extremely large array indices (e.g., $1.5$ Billion), the summation `left + right` equals $3.0$ Billion. This physically exceeds the 32-bit ceiling, triggering a catastrophic Integer Overflow and wrapping the value into a negative number, instantly crashing the array lookup. The mathematically safe formula is `left + (right - left) / 2`, which calculates the delta distance without ever exceeding the `right` boundary. In Python 3, integers possess Arbitrary Precision (they dynamically expand their byte allocation in physical RAM), so `(left + right) // 2` actually cannot overflow, but using the safe formula is a universally respected sign of Seniority."

3. Interviewer: "In Word Ladder, why is pre-computing the patterns (e.g., `d*g`) structurally vastly superior to just comparing the current word against every other word in the list dynamically?"
   Senior Answer: "If you dynamically compare the current word against every word in the dictionary to find 1-letter differences, you are forcing an $O(N^2 \\times M)$ time complexity. If the dictionary contains $100,000$ words, you execute 10 Billion string comparisons! By pre-computing the patterns, we exploit the structure of the english language. The word 'dog' instantly registers itself under `*og`, `d*g`, and `do*`. During the BFS, we simply generate the 3 patterns for our current word, and execute a mathematically perfect $O(1)$ Hash Map lookup to instantly retrieve all valid neighbors. This crushes the complexity to $O(N \\times M^2)$, transforming a 10-minute scan into a 2-millisecond operation."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Problem Sets (Algorithm Hard) Completed.")
