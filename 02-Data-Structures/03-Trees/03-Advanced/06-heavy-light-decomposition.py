"""
# ==============================================================================
# LABORATORY: HEAVY-LIGHT DECOMPOSITION (HLD)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You know how to use a Segment Tree to find the sum/max of a range in a 1D ARRAY 
# in O(log N) time. 
# But what if you have a massive N-ary Tree (e.g., a network topology of servers), 
# and you need to constantly find the maximum bottleneck (latency) on the path 
# between Server A and Server B? You can't use a standard Segment Tree because a 
# tree is not a flat array!
# Heavy-Light Decomposition (HLD) is an algorithm that breaks ANY tree down into 
# a set of completely flat, disjoint 1D arrays ("Chains"). You then put a Segment 
# Tree on top of these arrays. This allows you to query ANY path in a tree in 
# O(log^2 N) time!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the difference between "Heavy" and "Light" edges.
# - Execute DFS Pass 1: Calculate Subtree Sizes.
# - Execute DFS Pass 2: Decompose the tree into Chains.
#
# ==============================================================================
"""

from collections import defaultdict
from typing import List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE CONCEPT OF HLD
# ==============================================================================
def explain_hld_concept():
    section_header("The Concept of HLD")
    print("""
Imagine a Node with 5 children.
- We count the total number of nodes in the subtrees of all 5 children.
- The child with the LARGEST subtree is designated the "Heavy" child.
- The other 4 children are designated "Light" children.
- The edge connecting the parent to the Heavy child is a "Heavy Edge".
- The edges connecting the parent to the Light children are "Light Edges".

A sequence of contiguous Heavy Edges forms a "Heavy Chain".
Because it is a single continuous line from top to bottom, a Heavy Chain 
can be flattened into a standard 1D Array! 

Mathematical Guarantee: Any path from a node to the root will pass through 
at most O(log N) Light Edges. This means the path is broken into at most 
O(log N) Heavy Chains. We can query each chain in O(log N) using a Segment 
Tree, yielding a total query time of O(log^2 N).
    """)


# ==============================================================================
# 4. HLD IMPLEMENTATION (THE TWO DFS PASSES)
# ==============================================================================
class HLD:
    def __init__(self, n: int):
        self.n = n
        self.adj = defaultdict(list)
        
        # Arrays populated by DFS 1
        self.subtree_size = [0] * n
        self.parent = [-1] * n
        self.depth = [0] * n
        self.heavy_child = [-1] * n # Stores the ID of the heavy child
        
        # Arrays populated by DFS 2
        self.head = [-1] * n      # Stores the head of the heavy chain the node belongs to
        self.pos = [-1] * n       # The node's 1D position in the flattened array
        self.current_pos = 0      # Global counter for flattening

    def add_edge(self, u: int, v: int):
        # Undirected tree
        self.adj[u].append(v)
        self.adj[v].append(u)

    def dfs1(self, u: int, p: int, d: int) -> int:
        """
        DFS Pass 1: 
        Calculates subtree sizes, depth, and identifies the heavy child.
        """
        self.parent[u] = p
        self.depth[u] = d
        self.subtree_size[u] = 1
        
        max_sub_size = 0
        
        for v in self.adj[u]:
            if v != p: # Don't go back up to parent
                sub_size = self.dfs1(v, u, d + 1)
                self.subtree_size[u] += sub_size
                
                # If this child's subtree is the largest we've seen, it becomes the Heavy Child!
                if sub_size > max_sub_size:
                    max_sub_size = sub_size
                    self.heavy_child[u] = v
                    
        return self.subtree_size[u]

    def dfs2(self, u: int, p: int, chain_head: int):
        """
        DFS Pass 2:
        Builds the Heavy Chains and maps them to a flat 1D array (`self.pos`).
        """
        # Assign the head of the current chain
        self.head[u] = chain_head
        
        # Assign the node's position in the flattened array
        self.pos[u] = self.current_pos
        self.current_pos += 1
        
        # 1. We MUST visit the Heavy Child FIRST. 
        # This guarantees that nodes in the same Heavy Chain occupy CONTIGUOUS 
        # indices in the `self.pos` array!
        if self.heavy_child[u] != -1:
            self.dfs2(self.heavy_child[u], u, chain_head)
            
        # 2. Visit all the Light Children. 
        # Each Light Child starts a brand NEW Heavy Chain, where the Light Child 
        # is the head of its own new chain.
        for v in self.adj[u]:
            if v != p and v != self.heavy_child[u]:
                self.dfs2(v, u, v)

    def query_path(self, u: int, v: int):
        """
        Conceptual Query: Find max/sum between node u and node v.
        We bounce between chains, moving the lower node up, until they 
        both land on the same Heavy Chain.
        """
        # (This is conceptual. In reality, you would query a Segment Tree 
        # using the `self.pos` bounds we calculate here).
        print(f"Querying path between {u} and {v}:")
        
        while self.head[u] != self.head[v]:
            # Always move the node that is lower down the tree
            if self.depth[self.head[u]] > self.depth[self.head[v]]:
                print(f"  -> Querying Segment Tree for Chain {self.head[u]} from pos {self.pos[self.head[u]]} to {self.pos[u]}")
                u = self.parent[self.head[u]] # Jump across the light edge to the parent chain
            else:
                print(f"  -> Querying Segment Tree for Chain {self.head[v]} from pos {self.pos[self.head[v]]} to {self.pos[v]}")
                v = self.parent[self.head[v]]
                
        # Now they are on the SAME Heavy Chain. 
        # Query the segment between them.
        if self.depth[u] > self.depth[v]:
            u, v = v, u # Swap so u is higher
        print(f"  -> Querying Segment Tree for final segment on Chain {self.head[u]} from pos {self.pos[u]} to {self.pos[v]}")


# ==============================================================================
# 5. EXECUTION & DEMONSTRATION
# ==============================================================================
def demonstrate_hld():
    section_header("Algorithm Execution: Heavy-Light Decomposition")
    
    # 0 is the root.
    # 0 connects to 1 and 2.
    # 1 connects to 3, 4, 5.
    # 3 connects to 6, 7.
    n = 8
    hld = HLD(n)
    edges = [(0, 1), (0, 2), (1, 3), (1, 4), (1, 5), (3, 6), (3, 7)]
    for u, v in edges:
        hld.add_edge(u, v)
        
    print("Executing DFS Pass 1 (Subtree sizes and Heavy children)...")
    hld.dfs1(0, -1, 0)
    
    print("\nHeavy Children mapping:")
    for i in range(n):
        heavy = hld.heavy_child[i]
        print(f"  Node {i} (Subtree size {hld.subtree_size[i]}) -> Heavy Child: {heavy if heavy != -1 else 'None'}")
        
    print("\nExecuting DFS Pass 2 (Chain building & Flattening)...")
    # Start at root(0), parent(-1), chain_head(0)
    hld.dfs2(0, -1, 0)
    
    print("\nChain Head mapping:")
    for i in range(n):
        print(f"  Node {i} -> Belongs to Chain with Head: {hld.head[i]} | Flattened Index: {hld.pos[i]}")
        
    print("\nNotice how Nodes 0, 1, and 3 are on the SAME CHAIN (Head 0).")
    print("Notice how their flattened indices are contiguous: 0, 1, 2.")
    print("This means we can query the path 0-1-3 in O(log N) using a single Segment Tree query on indices [0:2]!\n")
    
    hld.query_path(6, 2)


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. What defines a "Heavy Edge" in HLD?
   Answer: The edge connecting a node to its child that has the largest subtree (most descendants). All other edges to its remaining children are "Light Edges".

2. Why do we visit the Heavy Child FIRST during DFS Pass 2?
   Answer: By visiting the heavy child first, the recursion dives straight down the Heavy Chain before visiting any light edges. This guarantees that all nodes in a Heavy Chain are assigned contiguous integer indices in the flattened 1D array. This is strictly required so that a Segment Tree can query the chain.

3. Why is the query time O(log^2 N)?
   Answer: Any path from a leaf to the root passes through at most O(log N) Light Edges, meaning the path spans at most O(log N) Heavy Chains. Querying a single Heavy Chain takes O(log N) using a Segment Tree. Multiplying these gives O(log^2 N).
"""

if __name__ == "__main__":
    explain_hld_concept()
    demonstrate_hld()
    print("\n[SUCCESS] Laboratory: Heavy-Light Decomposition Completed.")
