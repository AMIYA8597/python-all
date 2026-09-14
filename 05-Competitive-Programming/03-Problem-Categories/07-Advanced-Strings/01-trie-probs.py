"""
# ==============================================================================
# LABORATORY: COMPETITIVE PROGRAMMING (ADVANCED STRING TREES)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You are given an array of 100,000 positive integers.
# You need to find the MAXIMUM possible XOR result between ANY two numbers in 
# the array. 
#
# A double `for` loop checking `arr[i] ^ arr[j]` takes O(N^2) time, which is 
# 10 Billion operations (Time Limit Exceeded).
#
# A Trie (Prefix Tree) is normally used for dictionary words (Strings of letters).
# But what if we treat an Integer as a 32-bit String of 1s and 0s? 
# We can insert all 100,000 numbers into a "Binary Trie" in O(N) time.
#
# Once built, we can query any number against the Trie. Because XOR thrives 
# on OPPOSITE bits (1^0 = 1), the Trie can mathematically guide us down the 
# absolute optimal path, aggressively choosing opposite bits at every junction, 
# finding the maximum XOR pair in exactly O(32 * N) time!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the architecture of a Binary Trie.
# - Master the Maximum XOR of Two Numbers algorithm using Greedy Bit Traversal.
#
# ==============================================================================
"""

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. BINARY TRIE (MAXIMUM XOR ALGORITHM)
# ==============================================================================
class BinaryTrieNode:
    def __init__(self):
        # A Binary Trie only has two possible children: 0 or 1.
        # We use a dictionary (or a size 2 array)
        self.children = {}

class BinaryTrie:
    def __init__(self):
        self.root = BinaryTrieNode()
        # We assume 32-bit signed integers (so we check bits 31 down to 0)
        self.max_bits = 31

    def insert(self, num: int) -> None:
        """
        Inserts an integer into the Trie as a 32-bit string (from Most Significant Bit 
        to Least Significant Bit).
        """
        node = self.root
        
        for i in range(self.max_bits, -1, -1):
            # Extract the i-th bit (0 or 1)
            # Shift num to the right by `i`, and AND it with 1.
            bit = (num >> i) & 1
            
            if bit not in node.children:
                node.children[bit] = BinaryTrieNode()
                
            node = node.children[bit]

    def find_maximum_xor(self, num: int) -> int:
        """
        Given a number, walks the Trie to find the OTHER number that yields the 
        maximum possible XOR.
        Greedy Strategy: Always try to go down the path of the OPPOSITE bit!
        """
        node = self.root
        current_xor = 0
        
        for i in range(self.max_bits, -1, -1):
            # What is the i-th bit of our current number?
            bit = (num >> i) & 1
            
            # To maximize XOR, we desperately want the OPPOSITE bit!
            # If bit is 1, opposite is 0. If bit is 0, opposite is 1. (1 - bit)
            target_bit = 1 - bit
            
            # Does the opposite bit exist in the Trie?
            if target_bit in node.children:
                # YES! We successfully forced a 1 in our XOR result!
                # Add the physical value of this bit position (2^i) to our total.
                current_xor += (1 << i)
                node = node.children[target_bit]
                
            else:
                # NO! We are forced to take the SAME bit. 
                # This yields a 0 in our XOR result (we add nothing).
                node = node.children[bit]
                
        return current_xor

def find_maximum_xor_in_array(nums: list[int]) -> int:
    """
    Time Complexity: O(N * 32) -> O(N)
    Space Complexity: O(N * 32) -> O(N)
    """
    if not nums:
        return 0
        
    trie = BinaryTrie()
    max_xor = 0
    
    # 1. Build the Trie
    for num in nums:
        trie.insert(num)
        
    # 2. Query every number against the full Trie
    for num in nums:
        max_xor = max(max_xor, trie.find_maximum_xor(num))
        
    return max_xor

def demonstrate_binary_trie():
    section_header("Binary Trie (Maximum XOR Pair)")
    
    nums = [3, 10, 5, 25, 2, 8]
    print(f"Array of Numbers: {nums}")
    
    print("\nInserting all numbers into the Binary Trie as 32-bit paths...")
    ans = find_maximum_xor_in_array(nums)
    
    print(f"Absolute Maximum XOR found: {ans}")
    print("Why? 5 (00101) XOR 25 (11001) = 28 (11100)")
    print("The O(N) Binary Trie perfectly navigated the bits to find this pair instantly!")


def run_all_labs():
    demonstrate_binary_trie()


# ==============================================================================
# 4. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why must the Binary Trie insert the bits starting from the Most Significant Bit (MSB, bit 31) down to the Least Significant Bit (LSB, bit 0)? Why not start from bit 0?
   Answer: Because we are using a Greedy Algorithm! A single '1' at the 31st bit (value of 2 Billion) is mathematically worth infinitely more than all the lower 30 bits combined. The Trie forces us to make irreversible directional choices as we walk down the tree. By placing the MSB at the very top of the tree (the root), our very first Greedy choice is attempting to secure the 2-Billion-value bit. If we started from the LSB, we might perfectly optimize the 1s and 2s places, but irreparably steer ourselves down a branch that completely misses the 2-Billion bit at the very bottom, resulting in a disastrously wrong answer.

2. In the `find_maximum_xor` method, explain the line `current_xor += (1 << i)`. What does it mathematically accomplish?
   Answer: If we successfully traverse down a branch that contains the OPPOSITE bit of our current number (e.g., our bit is 1, and the tree has a 0), we know that `1 ^ 0 = 1`. This proves that in the final XOR result, the `i-th` bit will definitively be a `1`. The mathematical decimal value of a `1` at the `i-th` bit position is exactly $2^i$. The bitwise shift `(1 << i)` rapidly calculates $2^i$. We add this value to our running total, slowly building the final decimal integer of the maximum XOR as we walk down the tree.

3. Why is finding the Maximum XOR of two numbers in an array solvable in $O(N)$ time, while finding the Maximum SUM of two numbers in an array requires $O(N \log N)$ sorting?
   Answer: Because Addition carries over, but XOR is strictly columnar! In standard Addition, a change in the 1s column can cascade and flip bits all the way up to the 32nd column. Because of this chaotic linkage, you cannot build an isolated tree to evaluate sums; you must sort the numbers mathematically $O(N \log N)$. XOR has absolutely zero carryover. Bit 5 is mathematically isolated from Bit 4. This perfect columnar isolation allows us to deconstruct the integer into a strict sequence of 32 independent choices, mapping perfectly onto a Tree data structure, dropping the complexity down to a linear $O(N \times 32)$!
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Advanced String Trees Completed.")
