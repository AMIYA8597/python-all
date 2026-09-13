"""
# ==============================================================================
# LABORATORY: AHO-CORASICK AUTOMATON (MULTI-PATTERN SEARCH)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# KMP and Z-Algorithm are blindingly fast, but they have a fatal limitation: 
# They can only search for ONE pattern at a time.
#
# What if you are building an Anti-Virus scanner, and you need to scan a 
# 1-Gigabyte executable file for 10,000 different known virus signatures simultaneously?
#
# - Naive: Run KMP 10,000 times. Time: O(10,000 * N). Extremely slow.
# - Rabin-Karp: Hash a fixed-length window. But virus signatures are all DIFFERENT 
#   lengths! Rabin-Karp only works well if all patterns are the same length.
#
# In 1975, Alfred V. Aho and Margaret J. Corasick invented the ultimate Multi-Pattern 
# search algorithm. It searches for ALL 10,000 patterns simultaneously in a SINGLE 
# O(N) pass over the text!
#
# The architecture is a fusion of a Trie (Prefix Tree) and KMP's LPS array:
# 1. Build a Trie of all 10,000 virus signatures.
# 2. Run a BFS to inject "Failure Links" into the Trie. 
#    A Failure Link is exactly like KMP's fallback pointer: If you mismatch at 
#    "SHES", the failure link instantly teleports you to the node "HES" or "HE" 
#    or "S" in a COMPLETELY DIFFERENT pattern in the Trie!
#
# As you read the 1GB file, you just walk down the Trie. If you mismatch, you 
# instantly teleport via the Failure Link and keep walking. You never restart.
# Time Complexity: O(N + M + Z) (N=Text, M=Sum of Patterns, Z=Matches Found).
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Build the Prefix Trie.
# - Compute Failure Links via BFS (Automaton transition).
# - Execute the single-pass state machine search.
#
# ==============================================================================
"""

from collections import deque
from typing import Dict, List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. AHO-CORASICK ENGINE
# ==============================================================================
class AhoCorasickNode:
    def __init__(self):
        self.children: Dict[str, 'AhoCorasickNode'] = {}
        
        # If this node represents the end of a valid pattern, we store the pattern 
        # string here. (A node could theoretically end MULTIPLE patterns if one 
        # pattern is a substring of another, so we use a list).
        self.output: List[str] = []
        
        # The KMP Fallback! Where to teleport if the next character mismatches!
        self.failure_link: 'AhoCorasickNode' = None

class AhoCorasickAutomaton:
    def __init__(self):
        self.root = AhoCorasickNode()
        
    def add_pattern(self, pattern: str):
        """
        Step 1: Standard Trie Insertion. O(M) per pattern.
        """
        node = self.root
        for char in pattern:
            if char not in node.children:
                node.children[char] = AhoCorasickNode()
            node = node.children[char]
        # Mark the end of the pattern!
        node.output.append(pattern)
        
    def build_failure_links(self):
        """
        Step 2: Breadth-First Search (BFS) to wire up the Failure Links.
        This turns the static Trie into a Dynamic Finite Automaton!
        """
        queue = deque()
        
        # 1. The Root's failure link is itself (or None).
        self.root.failure_link = self.root
        
        # 2. All nodes at Depth 1 (direct children of Root) strictly fail back to Root!
        for char, child in self.root.children.items():
            child.failure_link = self.root
            queue.append(child)
            
        # 3. BFS for Depth 2 and beyond...
        while queue:
            current_node = queue.popleft()
            
            for char, child_node in current_node.children.items():
                queue.append(child_node)
                
                # To find the Failure Link for `child_node` (which arrived via `char`),
                # we look at the parent's (`current_node`) Failure Link!
                fallback_node = current_node.failure_link
                
                # We travel up the chain of failure links until we find a node 
                # that actually has an edge for `char`, OR we hit the Root.
                while fallback_node != self.root and char not in fallback_node.children:
                    fallback_node = fallback_node.failure_link
                    
                # If we found a valid fallback edge, take it!
                if char in fallback_node.children:
                    child_node.failure_link = fallback_node.children[char]
                else:
                    child_node.failure_link = self.root
                    
                # The Dictionary Match Rule: 
                # If my Failure Link represents a completed pattern, I MUST absorb 
                # its output! 
                # (Example: Searching for "HE" and "SHE". The node 'E' in "SHE" 
                # has a failure link to the node 'E' in "HE". When we hit "SHE", 
                # we implicitly also found "HE"!)
                child_node.output.extend(child_node.failure_link.output)

    def search(self, text: str) -> Dict[str, List[int]]:
        """
        Step 3: The Single-Pass Scan. O(N + Z).
        Returns a dictionary mapping Pattern -> List of Starting Indices.
        """
        results = defaultdict(list)
        from collections import defaultdict # Local import for safety
        results = defaultdict(list)
        
        current_node = self.root
        
        for i, char in enumerate(text):
            
            # 1. Follow Failure Links until we find a valid edge (or hit Root)
            while current_node != self.root and char not in current_node.children:
                current_node = current_node.failure_link
                
            # 2. Traverse the edge if it exists!
            if char in current_node.children:
                current_node = current_node.children[char]
            else:
                current_node = self.root
                
            # 3. Check for matches!
            # Because we absorbed outputs during BFS, `current_node.output` 
            # instantly contains ALL completed patterns!
            for pattern in current_node.output:
                # The index `i` is the END of the pattern. 
                # Calculate the start index:
                start_index = i - len(pattern) + 1
                results[pattern].append(start_index)
                
        return dict(results)


def demonstrate_aho_corasick():
    section_header("Algorithm: Aho-Corasick Multi-Pattern Search")
    
    automaton = AhoCorasickAutomaton()
    
    patterns = ["HE", "SHE", "HIS", "HERS"]
    print(f"Building Trie & Automaton for patterns: {patterns}")
    
    for p in patterns:
        automaton.add_pattern(p)
        
    automaton.build_failure_links()
    
    section_header("Single-Pass Execution")
    
    text = "USHERS"
    print(f"Text to scan: '{text}'")
    
    results = automaton.search(text)
    
    print("\nResults Found (in a single pass!):")
    for pattern, indices in results.items():
        print(f" -> '{pattern}' found at indices: {indices}")
        
    print("\nTrace Explanation for 'USHERS':")
    print("1. Hits 'S' -> 'H' -> 'E'. Finds 'SHE'.")
    print("2. Magic: The 'E' in SHE has a failure link to the 'E' in HE!")
    print("3. It instantly reports 'HE' without ever backtracking the text pointer!")
    print("4. Hits 'R' -> 'S'. Finds 'HERS'.")


# ==============================================================================
# 4. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. What is the fundamental difference between a Trie and the Aho-Corasick Automaton?
   Answer: A standard Trie is just a strict, isolated tree structure. If you walk down a path and mismatch, you fall off the tree and must restart your search from the absolute Root. The Aho-Corasick Automaton wires the leaves and internal branches across different patterns together using Failure Links. It converts the strict Tree into a highly interconnected Directed Graph (a Deterministic Finite Automaton). You never fall off; you simply glide via failure links to the next most viable state!

2. Why do we absorb `child_node.output.extend(child_node.failure_link.output)` during BFS?
   Answer: Substring embedding! Suppose our dictionary has "AT" and "CAT". The Trie has a branch `C -> A -> T`. The `T` node has a failure link pointing to the `T` node in the isolated `A -> T` branch. When we scan the text and land on `C -> A -> T`, the physical `T` node in the `CAT` branch ONLY knows it completed "CAT". It is oblivious to the fact that it simultaneously completed "AT"! By absorbing the outputs of the failure link during BFS, the `T` in `CAT` holds `["CAT", "AT"]`. It instantly reports both matches in $O(1)$ time!

3. Where is Aho-Corasick used in the real world?
   Answer: High-performance Network Intrusion Detection Systems (NIDS) like Snort use Aho-Corasick to scan raw TCP/IP packets at gigabit speeds for thousands of malicious byte-signatures simultaneously. It is also the underlying engine for the famous UNIX command `fgrep` (or `grep -F`), which searches for a massive list of fixed strings.
"""

if __name__ == "__main__":
    demonstrate_aho_corasick()
    print("\n[SUCCESS] Laboratory: Aho-Corasick Completed.")
