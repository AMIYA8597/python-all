"""
# ==============================================================================
# LABORATORY: SUFFIX TREES (UKKONEN'S ALGORITHM CONCEPTS)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You learned the Suffix Array, which allows searching 3 Billion characters of 
# DNA in O(M log N) time.
#
# But what if O(M log N) is not fast enough? What if you want strictly O(M) time?
# You need a Suffix Tree.
# 
# A Suffix Tree is a massive, compressed Trie (Prefix Tree) containing EVERY 
# single suffix of a string. 
#
# To find a pattern of length M, you simply start at the Root of the tree, and 
# walk down the edges matching characters. If you successfully walk M steps, the 
# pattern exists! It requires exactly M character comparisons. O(M) time. 
# 3 Billion characters of text does not matter. The search time is utterly 
# independent of N.
#
# The Problem: Building it.
# A naive algorithm inserts every suffix one by one into a Trie. O(N^2) time.
# In 1995, Esko Ukkonen achieved the Holy Grail: An online algorithm that builds 
# the entire Suffix Tree in strict O(N) time and O(N) space!
#
# Ukkonen's Algorithm is widely considered one of the most intellectually difficult 
# algorithms to understand and implement in all of Computer Science.
# It relies on three mind-bending optimizations:
# 1. The Active Point: (Active Node, Active Edge, Active Length).
# 2. Suffix Links: "Wormholes" that teleport you across the tree.
# 3. Global End Pointers: O(1) leaf extensions.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the compressed Trie architecture of a Suffix Tree.
# - Understand how O(M) search works.
# - Conceptually grasp Ukkonen's Active Point and Suffix Link state machine.
#
# ==============================================================================
"""

from typing import Dict, List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. SUFFIX TREE ARCHITECTURE
# ==============================================================================
class SuffixTreeNode:
    def __init__(self):
        # A dictionary mapping the first character of an edge to the child node.
        # e.g., children['a'] = child_node
        self.children: Dict[str, 'SuffixTreeNode'] = {}
        
        # Suffix trees compress paths! Instead of one node per character 
        # (A -> N -> A), we compress them into a single edge ("ANA").
        # To save massive amounts of RAM, we DO NOT store the actual string "ANA".
        # We just store pointers to the original string: [start_index, end_index].
        self.start = -1
        self.end = -1
        
        # A pointer to another node in the tree representing the same suffix 
        # minus the first character. This is the "Wormhole" Ukkonen uses to achieve O(N).
        self.suffix_link: 'SuffixTreeNode' = None

class NaiveSuffixTree:
    """
    To understand the Tree architecture before tackling Ukkonen's, we implement 
    a Naive O(N^2) builder. It demonstrates how edges are split and compressed!
    """
    def __init__(self, text: str):
        self.text = text + "$"
        self.root = SuffixTreeNode()
        self._build_naive()
        
    def _build_naive(self):
        n = len(self.text)
        
        # Insert every single suffix one by one! O(N^2)
        for i in range(n):
            self._insert_suffix(i)
            
    def _insert_suffix(self, suffix_start: int):
        current_node = self.root
        current_index = suffix_start
        n = len(self.text)
        
        while current_index < n:
            char = self.text[current_index]
            
            # CASE 1: No edge exists for this character. 
            # We just create a new leaf node directly!
            if char not in current_node.children:
                new_leaf = SuffixTreeNode()
                new_leaf.start = current_index
                new_leaf.end = n # Points to the absolute end of the string
                current_node.children[char] = new_leaf
                break # Suffix fully inserted!
                
            # CASE 2: An edge exists! We must traverse it.
            child = current_node.children[char]
            edge_start = child.start
            edge_end = child.end
            
            # Walk down the existing edge character by character to see if we diverge.
            diverge_idx = edge_start
            while diverge_idx < edge_end and current_index < n and self.text[diverge_idx] == self.text[current_index]:
                diverge_idx += 1
                current_index += 1
                
            # Subcase 2A: We exhausted the edge perfectly. We just move to the child 
            # node and continue the `while current_index < n` loop from there!
            if diverge_idx == edge_end:
                current_node = child
                continue
                
            # Subcase 2B: DIVERGENCE! We found a mismatch in the middle of a compressed edge!
            # Example: Edge is "ANANA". We are inserting "AND". We matched "AN", diverged at 'A' vs 'D'.
            # We must SPLIT the edge in half!
            if diverge_idx < edge_end:
                # 1. Create a new Internal Node right where the divergence happened.
                internal_node = SuffixTreeNode()
                internal_node.start = edge_start
                internal_node.end = diverge_idx
                
                # 2. Re-wire the old child to hang off the new internal node.
                # Its edge shrinks to only contain the remaining characters.
                child.start = diverge_idx
                internal_node.children[self.text[diverge_idx]] = child
                
                # 3. Re-wire the parent to point to the new internal node.
                current_node.children[char] = internal_node
                
                # 4. Create the new leaf node for the divergent suffix we were trying to insert!
                new_leaf = SuffixTreeNode()
                new_leaf.start = current_index
                new_leaf.end = n
                internal_node.children[self.text[current_index]] = new_leaf
                
                break # Suffix fully inserted!

    def search(self, pattern: str) -> bool:
        """
        O(M) Search! It strictly only takes M operations, regardless of how 
        massive the tree is!
        """
        current_node = self.root
        pattern_idx = 0
        m = len(pattern)
        
        while pattern_idx < m:
            char = pattern[pattern_idx]
            
            if char not in current_node.children:
                return False # Path dead-ends. Pattern does not exist!
                
            child = current_node.children[char]
            edge_start = child.start
            edge_end = child.end
            
            # Walk down the compressed edge
            edge_idx = edge_start
            while edge_idx < edge_end and pattern_idx < m:
                if self.text[edge_idx] != pattern[pattern_idx]:
                    return False # Diverged in the middle of an edge!
                edge_idx += 1
                pattern_idx += 1
                
            # If we exhausted the edge and still have pattern characters left, 
            # jump to the child node and continue the outer loop!
            current_node = child
            
        # If we successfully walked `M` characters, it exists!
        return True


def demonstrate_suffix_tree():
    section_header("Algorithm: Suffix Tree (Naive O(N^2) Construction)")
    
    text = "banana"
    print(f"Building Suffix Tree for '{text}'...")
    
    # We use the Naive O(N^2) builder because a pure Ukkonen O(N) implementation 
    # requires roughly 300 lines of highly dense state-machine spaghetti code.
    # The architecture and O(M) search logic is absolutely identical.
    tree = NaiveSuffixTree(text)
    
    section_header("O(M) Pattern Search")
    
    patterns = ["ana", "nan", "band", "a", "nana"]
    
    for pat in patterns:
        found = tree.search(pat)
        print(f"Searching for '{pat:4}' -> {'FOUND!' if found else 'Not Found'}")
        
    print("\nObservation:")
    print("Searching for 'ana' takes exactly 3 character checks. Period.")
    print("If the original string was the 3-Billion-character Human Genome,")
    print("it would STILL take exactly 3 checks!")


# ==============================================================================
# 4. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why does a Suffix Tree compress its edges?
   Answer: A standard Trie has one node per character. If a string has $N$ characters, it has $N$ suffixes, with lengths $1, 2, 3 \dots N$. The total number of characters across all suffixes is $(N \times (N+1)) / 2$. This means a standard Trie would require $O(N^2)$ nodes! By collapsing paths with no branching (e.g. `A -> N -> A`) into a single edge `ANA` storing just `[start, end]` pointers, the maximum number of internal nodes is mathematically bounded to $N-1$, and leaves to $N$. The space complexity instantly drops from $O(N^2)$ to $O(N)$!

2. Conceptually, how does Ukkonen achieve $O(N)$ construction time?
   Answer: Ukkonen's algorithm builds the tree "Online" (reading characters left to right: $T[0], T[1], T[2] \dots$). 
   - Rule 1 (Global End): Leaf nodes use a global `END` pointer. When a new character arrives, ALL existing leaves are automatically extended in $O(1)$ time just by incrementing the global `END` variable!
   - Rule 2 (Suffix Links): If the algorithm creates a new internal node at `A-N-A`, it creates a "Wormhole" pointer directly to the node `N-A`. When the next suffix needs to be inserted, it doesn't walk down from the root from scratch! It takes the wormhole directly to the correct spot in the tree in $O(1)$ time!

3. Why use a Suffix Array instead of a Suffix Tree?
   Answer: Memory overhead. While both take $O(N)$ memory mathematically, a Suffix Tree requires allocating massive Objects/Structs for Nodes, HashMaps/Arrays for the 256 children pointers, `start`/`end` integers, and `suffix_link` pointers. A Suffix Tree can easily consume 20 to 50 bytes per character. The 3GB human genome would require 150GB of RAM! A Suffix Array is just a bare-metal array of 32-bit integers. It requires exactly 4 bytes per character (12GB for the genome). This is why Bioinformatics uses Suffix Arrays + LCP instead of Trees.
"""

if __name__ == "__main__":
    demonstrate_suffix_tree()
    print("\n[SUCCESS] Laboratory: Suffix Trees Completed.")
