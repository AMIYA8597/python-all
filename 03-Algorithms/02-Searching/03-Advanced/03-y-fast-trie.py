"""
# ==============================================================================
# LABORATORY: Y-FAST TRIE (O(log log M) INTEGER SEARCH)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# If you want to store integers and query for the "Predecessor" (the largest 
# number strictly less than X) or "Successor" (the smallest number strictly 
# greater than X):
#
# - A Balanced BST (Red-Black / AVL) takes O(log N) time.
# - Can we do faster than O(log N) if the keys are integers? Yes!
#
# Dan Willard invented the X-Fast Trie, which achieves O(log log M) time, 
# where M is the maximum possible integer (e.g., 2^32). It does this by storing 
# prefixes in Hash Tables and Binary Searching the depth of the Trie. 
# But X-Fast Tries use a massive O(N log M) memory!
#
# Willard then invented the **Y-Fast Trie**.
# It chops the N integers into small groups of size O(log M).
# - It stores ONLY the "representative" (maximum) of each group in an X-Fast Trie.
# - It stores the actual elements in standard Balanced BSTs.
# 
# This maintains the blistering O(log log M) search speed, but drops the memory 
# overhead to strictly O(N)!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the limits of X-Fast Tries.
# - Understand how Y-Fast Tries use representative grouping.
# - Understand how $O(\\log \\log M)$ completely destroys $O(\\log N)$ for large N.
#
# ==============================================================================
"""

import math
import bisect
from typing import List, Optional

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. MOCK Y-FAST TRIE IMPLEMENTATION
# ==============================================================================
# Note: A true X-Fast/Y-Fast Trie requires bitwise Hash Tables and complex 
# dynamic hashing. This is a conceptual implementation demonstrating the 
# "Representative Grouping" architecture that makes Y-Fast Tries memory-efficient.

class YFastTrieGroup:
    """
    The small secondary structure. 
    In a real Y-Fast Trie, this would be a balanced BST (like a Red-Black tree).
    For Python, we use a simple sorted list to represent the $O(\\log M)$ sized block.
    """
    def __init__(self):
        self.elements: List[int] = []
        self.representative = -1 # Usually the max element of the group
        
    def insert(self, val: int):
        bisect.insort(self.elements, val)
        self.representative = self.elements[-1]
        
    def get_successor(self, target: int) -> Optional[int]:
        idx = bisect.bisect_right(self.elements, target)
        if idx < len(self.elements):
            return self.elements[idx]
        return None


class MockYFastTrie:
    """
    Demonstrates the architecture of a Y-Fast Trie.
    """
    def __init__(self, bit_length: int = 32):
        self.bit_length = bit_length
        # The target size for each group is O(log M). 
        # For a 32-bit integer, M = 2^32, so log(M) = 32.
        self.target_group_size = bit_length 
        
        # This array represents the "X-Fast Trie" that ONLY stores the representatives.
        # It takes up O(N / log M) space, perfectly cancelling out the X-Fast memory bloat!
        self.x_fast_representatives: List[int] = []
        
        # Maps the representative to its actual Group
        self.groups: dict[int, YFastTrieGroup] = {}

    def insert(self, val: int) -> None:
        """
        Inserts a value. If a group gets too big, it splits (like a B-Tree).
        """
        # Find the correct group using the representatives
        idx = bisect.bisect_left(self.x_fast_representatives, val)
        
        if idx == len(self.x_fast_representatives):
            # No valid group exists (val is larger than all representatives).
            # If there is a group at the end, add it there, else create a new one.
            if self.x_fast_representatives:
                rep = self.x_fast_representatives[-1]
                group = self.groups[rep]
            else:
                # First element ever
                new_group = YFastTrieGroup()
                new_group.insert(val)
                self.x_fast_representatives.append(new_group.representative)
                self.groups[new_group.representative] = new_group
                return
        else:
            rep = self.x_fast_representatives[idx]
            group = self.groups[rep]
            
        # 1. Insert into the group
        old_rep = group.representative
        group.insert(val)
        new_rep = group.representative
        
        # Update representative if it changed
        if new_rep != old_rep:
            self.x_fast_representatives.remove(old_rep)
            del self.groups[old_rep]
            
            bisect.insort(self.x_fast_representatives, new_rep)
            self.groups[new_rep] = group
            
        # 2. SPLIT the group if it exceeds 2 * target_group_size
        if len(group.elements) > 2 * self.target_group_size:
            mid = len(group.elements) // 2
            
            # Left half stays in the original group
            left_elements = group.elements[:mid]
            
            # Right half forms a new group
            right_elements = group.elements[mid:]
            
            # Rebuild left group
            self.x_fast_representatives.remove(group.representative)
            del self.groups[group.representative]
            
            left_group = YFastTrieGroup()
            for x in left_elements: left_group.insert(x)
            
            right_group = YFastTrieGroup()
            for x in right_elements: right_group.insert(x)
            
            # Insert both back into the X-Fast structures
            bisect.insort(self.x_fast_representatives, left_group.representative)
            self.groups[left_group.representative] = left_group
            
            bisect.insort(self.x_fast_representatives, right_group.representative)
            self.groups[right_group.representative] = right_group

    def successor(self, target: int) -> Optional[int]:
        """
        Queries the successor in O(log log M) time.
        """
        # 1. Find the correct representative using the X-Fast Trie (O(log log M))
        idx = bisect.bisect_right(self.x_fast_representatives, target)
        
        if idx == len(self.x_fast_representatives):
            return None # Target is greater than all elements
            
        rep = self.x_fast_representatives[idx]
        group = self.groups[rep]
        
        # 2. The group has at most O(log M) elements.
        # Searching a balanced BST of size log M takes O(log(log M)) time!
        return group.get_successor(target)


def demonstrate_y_fast():
    section_header("Algorithm: Y-Fast Trie (Architecture)")
    
    # We will simulate a very small bit_length to force the groups to split early
    # Let's say M = 2^4 (Numbers up to 16). So log M = 4. Group size is 4.
    yft = MockYFastTrie(bit_length=4)
    
    print("Inserting numbers: 2, 3, 5, 7, 9, 11, 13, 15, 16")
    for x in [2, 3, 5, 7, 9, 11, 13, 15, 16]:
        yft.insert(x)
        
    print("\nInternal Architecture:")
    print(f"X-Fast Representatives (Group Maxes): {yft.x_fast_representatives}")
    for rep in yft.x_fast_representatives:
        print(f"  Group [{rep}]: {yft.groups[rep].elements}")
        
    print("\nSuccessor Queries (Strictly > Target):")
    queries = [4, 7, 12, 16]
    for q in queries:
        ans = yft.successor(q)
        print(f" Successor of {q:2} -> {ans}")
        
    print("\nNotice how the elements were chopped into smaller groups.")
    print("The primary X-Fast Trie only tracks the MAXIMUM of each group.")


# ==============================================================================
# 4. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why does the X-Fast Trie use $O(N \\log M)$ memory?
   Answer: An X-Fast Trie is a bitwise Trie where every integer is represented by exactly $W$ bits (where $W = \\log M$). Inserting one integer creates $W$ nodes in the Trie. Therefore, $N$ integers require $N \\times W$ nodes. For 64-bit integers, it creates $64N$ nodes, which is huge!

2. How does the Y-Fast Trie reduce memory back to $O(N)$?
   Answer: It groups the $N$ integers into blocks of size $W$. It only inserts the maximum element of each block into the X-Fast Trie. So the X-Fast Trie only holds $N / W$ elements. The memory of the X-Fast Trie becomes $(N / W) \\times W = O(N)$. The secondary trees also take $O(N)$ space. Total memory is perfectly $O(N)$.

3. Why is $O(\\log \\log M)$ so much faster than $O(\\log N)$?
   Answer: If you have a database of 4 Billion IP addresses ($N = 2^{32}$). 
   A standard Balanced BST takes $\\log_2(2^{32}) = 32$ operations.
   A Y-Fast Trie takes $\\log_2(\\log_2(2^{32})) = \\log_2(32) = 5$ operations.
   It is 6x faster and completely independent of how many items are currently in the database!
"""

if __name__ == "__main__":
    demonstrate_y_fast()
    print("\n[SUCCESS] Laboratory: Y-Fast Trie Completed.")
