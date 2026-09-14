"""
# ==============================================================================
# LABORATORY: COMPETITIVE PROGRAMMING (HEAVY-LIGHT DECOMPOSITION)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You are given a Tree with 100,000 nodes.
# You are given 100,000 queries. Each query is: "Add X to all nodes on the 
# simple path from Node U to Node V."
#
# If you run a DFS/BFS for every query to find the path and update the nodes, 
# it takes O(N) per query. 100,000 * 100,000 = 10 Billion operations (TLE).
#
# Can you use a Segment Tree? A Segment Tree only works on a FLAT 1D Array. 
# A Tree is chaotic and non-linear. You cannot build a Segment Tree on a Graph.
#
# Enter Heavy-Light Decomposition (HLD). HLD mathematically flattens the chaotic 
# Tree into a series of perfectly straight lines (chains). It guarantees that 
# the path between ANY two nodes in the entire Tree will be composed of at most 
# O(log N) straight chains. 
#
# Because each chain is a flat 1D array, you can map the ENTIRE Tree onto a 
# single Segment Tree! You answer complex path queries in exactly O(log^2 N) time!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the classification of "Heavy" and "Light" edges.
# - Understand the Two-Pass DFS architecture of HLD.
# - Conceptually link HLD to a 1D Segment Tree.
#
# ==============================================================================
"""

import sys

# Increase recursion depth for massive trees
sys.setrecursionlimit(200000)

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. HEAVY-LIGHT DECOMPOSITION (HLD)
# ==============================================================================
class HLD:
    def __init__(self, n: int, edges: list[tuple[int, int]]):
        self.n = n
        self.graph = [[] for _ in range(n)]
        for u, v in edges:
            self.graph[u].append(v)
            self.graph[v].append(u)
            
        # Standard Tree properties
        self.parent = [-1] * n
        self.depth = [0] * n
        self.subtree_size = [0] * n
        self.heavy_child = [-1] * n # Which child has the largest subtree?
        
        # HLD specific properties
        # head[u] stores the node at the absolute TOP of the straight chain u belongs to.
        self.head = [-1] * n 
        # pos[u] is the final mapped index of u in the flattened 1D Segment Tree array!
        self.pos = [-1] * n 
        self.current_pos = 0
        
        # 1. Execute the First DFS to establish Subtree Sizes and Heavy Edges
        self._dfs_size(0, -1, 0)
        
        # 2. Execute the Second DFS to physically build the straight Chains
        self._dfs_hld(0, -1, 0)

    def _dfs_size(self, current: int, p: int, d: int) -> int:
        """
        DFS Pass 1: Calculates depth, parent, and subtree size.
        Mathematically identifies the "Heavy" child (the child with the largest subtree).
        """
        self.parent[current] = p
        self.depth[current] = d
        self.subtree_size[current] = 1
        
        max_child_size = 0
        
        for neighbor in self.graph[current]:
            if neighbor != p:
                child_size = self._dfs_size(neighbor, current, d + 1)
                self.subtree_size[current] += child_size
                
                # Is this the largest child we have seen so far?
                if child_size > max_child_size:
                    max_child_size = child_size
                    # Mark this edge as the HEAVY edge!
                    self.heavy_child[current] = neighbor
                    
        return self.subtree_size[current]

    def _dfs_hld(self, current: int, p: int, chain_head: int) -> None:
        """
        DFS Pass 2: Flattens the Tree into 1D chains.
        """
        # Record the head of the chain we currently belong to
        self.head[current] = chain_head
        
        # Assign a 1D index to this node for the Segment Tree!
        self.pos[current] = self.current_pos
        self.current_pos += 1
        
        # If we have a Heavy Child, we MUST visit it FIRST!
        # Visiting the Heavy Child first guarantees that the entire straight chain 
        # will have contiguous indices in `self.pos`, allowing a Segment Tree 
        # to query the entire chain in a single O(log N) shot!
        if self.heavy_child[current] != -1:
            self._dfs_hld(self.heavy_child[current], current, chain_head)
            
        # After finishing the Heavy chain, we visit the Light Children.
        # EVERY Light Edge physically starts a completely NEW chain!
        for neighbor in self.graph[current]:
            if neighbor != p and neighbor != self.heavy_child[current]:
                # Notice we pass `neighbor` as the new `chain_head`!
                self._dfs_hld(neighbor, current, neighbor)

    def get_path_intervals(self, u: int, v: int) -> list[tuple[int, int]]:
        """
        Queries the path between Node U and Node V.
        Returns a list of 1D Array Intervals [L, R] that can be instantly fed 
        into a standard Segment Tree!
        """
        intervals = []
        
        # While U and V belong to DIFFERENT chains, we jump the deeper one UP!
        while self.head[u] != self.head[v]:
            # Ensure U is always the mathematically deeper node
            if self.depth[self.head[u]] < self.depth[self.head[v]]:
                u, v = v, u
                
            # The node U is at the bottom of a chain.
            # We want to query from U all the way to the top of its current chain.
            # (In the 1D array, the head has a smaller index than U).
            intervals.append((self.pos[self.head[u]], self.pos[u]))
            
            # Jump U across the Light Edge to the parent of its chain!
            u = self.parent[self.head[u]]
            
        # U and V are now in the EXACT SAME CHAIN!
        # We query the segment strictly between them.
        if self.depth[u] > self.depth[v]:
            u, v = v, u
            
        intervals.append((self.pos[u], self.pos[v]))
        return intervals

def demonstrate_hld():
    section_header("Heavy-Light Decomposition (HLD)")
    
    # Tree Structure:
    #       0
    #      / \
    #     1   2
    #    / \
    #   3   4
    #  /
    # 5
    n = 6
    edges = [(0, 1), (0, 2), (1, 3), (1, 4), (3, 5)]
    
    print("Tree Edges:")
    for u, v in edges: print(f"  {u} -- {v}")
    
    hld = HLD(n, edges)
    
    print("\nHLD Classification:")
    for i in range(n):
        heavy = hld.heavy_child[i]
        heavy_str = str(heavy) if heavy != -1 else "None (Leaf)"
        print(f"Node {i}: Belongs to Chain Head [{hld.head[i]}]. 1D Pos: {hld.pos[i]}. Heavy Child: {heavy_str}")
        
    print("\nQuerying Path from Node 5 to Node 4:")
    intervals = hld.get_path_intervals(5, 4)
    print(f"1D Segment Tree Intervals to Query: {intervals}")
    print("Explanation:")
    print("Node 5 jumps up its Heavy Chain to Node 1.")
    print("Node 4 is in a different chain, it jumps up to Node 1.")
    print("The chaotic Tree path is mathematically reduced to purely 1D intervals!")


def run_all_labs():
    demonstrate_hld()


# ==============================================================================
# 4. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. What defines a "Heavy Edge" and a "Light Edge" in HLD, and why is this distinction mathematically critical?
   Answer: From any given node, the edge pointing to the child with the absolute *largest subtree* is marked as "Heavy". All other edges pointing to the remaining children are marked as "Light". This distinction is the core mathematical engine of HLD. Because you only ever take a Light Edge when jumping into a smaller subtree, and that smaller subtree can mathematically be at most HALF the size of the parent's subtree... you can only take a Light Edge a maximum of $\log_2(N)$ times before the subtree size physically shrinks to 1! This mathematical proof guarantees that any path from a leaf to the root crosses at most $O(\log N)$ Light Edges.

2. In the Second DFS pass, why MUST we visit the `heavy_child` first before any of the other children?
   Answer: The goal of HLD is to map the Tree onto a 1D Segment Tree array. A Segment Tree can only query contiguous blocks of memory (e.g., indices 5 to 10). A chain is formed by connecting Heavy Edges. By forcing the DFS to physically walk down the Heavy Edge first, we mathematically guarantee that all nodes within that single straight chain are assigned perfectly contiguous indices in the `pos` array (e.g., 0, 1, 2, 3). If we visited a Light Child in the middle, the indices would be interrupted (0, 1, 99, 2, 3), destroying the contiguous block and making it physically impossible for the Segment Tree to query the chain in $O(\log N)$ time!

3. In `get_path_intervals`, when U and V are in different chains, why do we mathematically force the node with the deeper `head` to jump up, instead of just the deeper node?
   Answer: If Node U is at depth 10 (very deep), but it belongs to a massive Heavy Chain whose Head is at depth 2 (very high)... and Node V is at depth 5, but its Head is at depth 5 (a Light Node)... if you naively jumped the deeper Node (U), U would jump from depth 10 all the way to depth 1 (above V!). You would completely overshoot V and ruin the path! You must always jump the node whose *Chain Head* is mathematically deeper. This guarantees you safely ascend the tree structure one chain at a time without ever skipping the Lowest Common Ancestor (LCA).
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Advanced Topics (HLD) Completed.")
