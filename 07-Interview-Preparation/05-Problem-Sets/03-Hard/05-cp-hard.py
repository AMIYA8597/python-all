"""
# ==============================================================================
# LABORATORY: INTERVIEW PREPARATION (PROBLEM SETS - CP HARD)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Competitive Programming (CP) algorithms are the absolute bleeding edge of 
# Computer Science optimization. They are rarely asked in standard interviews, 
# but they are universally expected in High-Frequency Trading (HFT) firms like 
# Citadel and Jump Trading, where microseconds mathematically translate to millions 
# of dollars.
#
# A standard engineer searches for a substring using nested loops (O(N * M)).
# A CP engineer uses the KMP (Knuth-Morris-Pratt) Algorithm. They pre-compute an 
# LPS (Longest Prefix Suffix) array, ensuring the search pointer never physically 
# moves backward in RAM, achieving flawless O(N + M) Time Complexity.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master O(N) Substring Search (Knuth-Morris-Pratt Algorithm).
# - Master Range Queries with O(log N) updates (Segment Trees).
# - Understand the architecture of extreme performance algorithms.
#
# ==============================================================================
"""

from typing import List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. KMP ALGORITHM (KNUTH-MORRIS-PRATT)
# ==============================================================================
def compute_lps_array(pattern: str) -> List[int]:
    """
    Time: O(M) | Space: O(M)
    Builds the Longest Prefix Suffix (LPS) array for the pattern.
    LPS[i] stores the length of the maximum matching proper prefix which is also a suffix.
    """
    length = 0 # Length of the previous longest prefix suffix
    lps = [0] * len(pattern)
    i = 1
    
    while i < len(pattern):
        # We found a match! The pattern is repeating itself!
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                # This is the magic of KMP! Instead of resetting length to 0, 
                # we mathematically fall back to the previous known valid prefix!
                length = lps[length - 1]
            else:
                # Zero match. Move forward.
                lps[i] = 0
                i += 1
    return lps

def kmp_search(text: str, pattern: str) -> List[int]:
    """
    Time: O(N + M) | Space: O(M)
    Finds all occurrences of a pattern in a text without EVER moving the text pointer backwards!
    """
    if not pattern: return []
    
    # 1. Pre-compute the LPS Array (The Mathematical Routing Table)
    lps = compute_lps_array(pattern)
    print(f"  Pattern: '{pattern}' -> LPS Routing Table: {lps}")
    
    res = []
    i = 0 # Pointer for text
    j = 0 # Pointer for pattern
    
    print(f"  Searching Text: '{text}'...")
    
    while i < len(text):
        if pattern[j] == text[i]:
            i += 1
            j += 1
            
        if j == len(pattern):
            # We found a perfect mathematical match!
            start_index = i - j
            print(f"    -> [MATCH] Pattern found at index {start_index}!")
            res.append(start_index)
            # Use the LPS array to reset the pattern pointer intelligently!
            j = lps[j - 1]
            
        elif i < len(text) and pattern[j] != text[i]:
            # MISMATCH!
            # A junior engineer would reset the text pointer `i` back to the beginning.
            # We do NOT touch `i`. We mathematically rollback `j` using the LPS array!
            if j != 0:
                print(f"    -> [MISMATCH] at text idx {i}, pattern idx {j}. Rolling back pattern to {lps[j-1]}!")
                j = lps[j - 1]
            else:
                # If j is 0, we have no prefix to fall back on. Advance text!
                i += 1
                
    return res

def demonstrate_kmp():
    section_header("CP Hard: Knuth-Morris-Pratt Algorithm")
    text = "ABABDABACDABABCABAB"
    pattern = "ABABCABAB"
    ans = kmp_search(text, pattern)
    print(f"\nResult: Indices {ans} (Expected: [10])")


# ==============================================================================
# 4. SEGMENT TREE (RANGE SUM QUERY - MUTABLE)
# ==============================================================================
class SegmentTree:
    """
    Time: O(log N) for Queries | O(log N) for Updates
    Space: O(N)
    If you use an Array for Range Sums: Update is O(1), but Sum is O(N).
    If you use a Prefix Array: Sum is O(1), but Update is O(N).
    A Segment Tree mathematically balances BOTH operations to strict O(log N)!
    """
    def __init__(self, nums: List[int]):
        self.n = len(nums)
        # A Segment Tree requires exactly 2 * N memory slots!
        self.tree = [0] * (2 * self.n)
        
        # 1. Insert the raw data into the LEAVES of the tree! (The right half of the array)
        for i in range(self.n):
            self.tree[self.n + i] = nums[i]
            
        # 2. Build the Parents! (The left half of the array)
        # Parent(i) = LeftChild(2 * i) + RightChild(2 * i + 1)
        for i in range(self.n - 1, 0, -1):
            self.tree[i] = self.tree[2 * i] + self.tree[2 * i + 1]
            
        print(f"  [INIT] Segment Tree built: {self.tree}")

    def update(self, index: int, val: int) -> None:
        """Updates a value in O(log N) time."""
        # Teleport directly to the physical leaf node!
        pos = index + self.n
        self.tree[pos] = val
        
        print(f"  [UPDATE] Index {index} changed to {val}. Bubbling changes upwards...")
        
        # Mathematically bubble the sum updates up to the Root!
        while pos > 1:
            left = pos
            right = pos
            # If `pos` is even, it's the Left Child. The right child is `pos + 1`.
            if pos % 2 == 0:
                right = pos + 1
            else:
                left = pos - 1
                
            # Update the Parent (pos // 2)
            self.tree[pos // 2] = self.tree[left] + self.tree[right]
            # Move up the tree!
            pos //= 2

    def sumRange(self, left: int, right: int) -> int:
        """Queries the sum of the range [left, right] in O(log N) time."""
        # Teleport to the leaf nodes!
        l = left + self.n
        r = right + self.n
        range_sum = 0
        
        # Collapse the boundaries inward!
        while l <= r:
            # If the Left boundary is an ODD index, it is the RIGHT child of its parent!
            # That means its parent mathematically includes data OUTSIDE our requested range.
            # We must isolate this node, add it to our sum, and move inward!
            if l % 2 == 1:
                range_sum += self.tree[l]
                l += 1
                
            # If the Right boundary is an EVEN index, it is the LEFT child of its parent!
            if r % 2 == 0:
                range_sum += self.tree[r]
                r -= 1
                
            # Move up the tree!
            l //= 2
            r //= 2
            
        print(f"  [QUERY] Sum of range [{left}, {right}] = {range_sum}")
        return range_sum

def demonstrate_segment_tree():
    section_header("CP Hard: Segment Tree (Range Sum Query)")
    
    nums = [1, 3, 5, 7, 9, 11]
    st = SegmentTree(nums)
    
    st.sumRange(0, 2) # Sum of [1, 3, 5] = 9
    st.update(1, 10)  # Change the '3' to a '10'
    ans = st.sumRange(0, 2) # Sum of [1, 10, 5] = 16
    
    print(f"\nResult: {ans} (Expected: 16)")


def run_all_labs():
    demonstrate_kmp()
    demonstrate_segment_tree()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "In KMP, mathematically explain why the text pointer `i` never moves backwards, and why this is critical for high-performance streams."
   Senior Answer: "When a mismatch occurs, naive algorithms rollback the text pointer `i` and restart the comparison from scratch, creating a catastrophic $O(N \\times M)$ overlap. KMP uses the pre-computed LPS array to mathematically deduce how much of the *Pattern* we can safely salvage. If the pattern is 'ABABC' and we fail on the 'C', KMP knows the previous letters were 'ABAB'. It instantly recognizes that the suffix 'AB' perfectly matches the prefix 'AB'! It commands the pattern pointer `j` to snap back to the second 'AB' and resumes execution immediately. Because `i` never regresses, KMP can process infinite real-time data streams (like TCP packets) in strict $O(N)$ time, as it never needs to store or backtrack through historical network payloads."

2. Interviewer: "In a Segment Tree array, why does the data for node `i` reside at children `2 * i` and `2 * i + 1`?"
   Senior Answer: "This is the mathematical formula for a perfectly balanced Binary Tree mapped directly into a 1-Dimensional Array! By placing the Root at index 1, the Left Child is strictly $1 \\times 2 = 2$, and the Right Child is $1 \\times 2 + 1 = 3$. This arithmetic relationship allows us to traverse up and down the tree in $O(1)$ constant time using raw CPU bit-shifts (`pos >> 1` to find parent, `pos << 1` to find left child), completely bypassing the overhead of instantiating actual Python Objects and memory pointers, which is mandatory for Competitive Programming performance."

3. Interviewer: "During `sumRange` in the Segment Tree, why do we add `self.tree[l]` and do `l += 1` if `l % 2 == 1`?"
   Senior Answer: "In our 1D array mapping, an Odd index signifies that a node is the Right Child of its parent. If our requested search boundary starts precisely on a Right Child, its Parent node intrinsically contains the sum of BOTH the Left Child (which is mathematically OUTSIDE our requested boundary) and the Right Child. We cannot safely use the Parent node to aggregate our sum! We must cleanly sever the Right Child, add its raw value directly into our accumulator, and mathematically advance our Left Boundary inward (`l += 1`) so that on the next iteration up the tree, we only interact with Parents whose sub-trees perfectly align with our requested range."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Problem Sets (CP Hard) Completed.")
