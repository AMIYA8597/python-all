"""
# ==============================================================================
# LABORATORY: BICONNECTED COMPONENTS (BCC)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# In the previous lab, you learned how to find Articulation Points (single nodes 
# that, if deleted, shatter the network).
# 
# But what if you want to identify the safe zones? 
# A "Biconnected Component" (BCC) is a maximal cluster of nodes that is 
# physically indestructible by a single point of failure. You can delete ANY 
# single node inside a BCC, and the rest of the nodes in that BCC will remain 
# perfectly connected.
#
# In fact, an entire graph is mathematically constructed of robust BCCs glued 
# together precisely at the fragile Articulation Points!
#
# How do we extract these robust clusters?
# Tarjan's algorithm (yet again). We use the exact same `discovery_time` and 
# `low_link` logic. But this time, instead of pushing NODES to a stack, we 
# push EDGES to a stack.
# 
# Whenever the mathematical trigger `low_link[v] >= discovery_time[u]` goes off, 
# we know `u` is an Articulation Point. More importantly, it proves that the 
# DFS just finished exploring a complete Biconnected Component! 
# We instantly pop edges off the stack until we pop the specific edge `u-v`, 
# perfectly extracting the indestructible cluster!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the difference between SCC (Directed) and BCC (Undirected).
# - Maintain an Edge Stack during the DFS.
# - Extract BCCs using the Articulation Point trigger.
#
# ==============================================================================
"""

from typing import Dict, List, Set, Tuple

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. TARJAN'S BICONNECTED COMPONENTS ENGINE (O(V + E))
# ==============================================================================
class BiconnectedComponents:
    def __init__(self, vertices: int, graph: Dict[int, List[int]]):
        self.V = vertices
        self.graph = graph
        
        self.time = 0
        self.discovery_time = [-1] * vertices
        self.low_link = [-1] * vertices
        
        # We push EDGES (u, v) to the stack, not just nodes!
        self.edge_stack: List[Tuple[int, int]] = []
        
        # The final output: A list of BCCs (each BCC is a list of its edges)
        self.bccs: List[List[Tuple[int, int]]] = []
        
    def _dfs(self, u: int, parent: int):
        self.discovery_time[u] = self.time
        self.low_link[u] = self.time
        self.time += 1
        
        children = 0
        
        for v in self.graph.get(u, []):
            if v == parent:
                continue
                
            # Case A: Unvisited Neighbor
            if self.discovery_time[v] == -1:
                children += 1
                
                # Push the edge we are about to traverse onto the stack!
                self.edge_stack.append((u, v))
                
                self._dfs(v, u)
                
                # Update low-link
                self.low_link[u] = min(self.low_link[u], self.low_link[v])
                
                # --------------------------------------------------------------
                # BCC EXTRACTION TRIGGER
                # --------------------------------------------------------------
                # If U is an Articulation Point (or the Root with children > 1),
                # it means the sub-graph we just explored from V is physically 
                # trapped. It is a complete Biconnected Component!
                
                # Note: We trigger even for the Root node here because every edge 
                # attached to the root belongs to SOME BCC, and we must pop them!
                if parent == -1 and children > 1 or (parent != -1 and self.low_link[v] >= self.discovery_time[u]):
                    
                    bcc = []
                    # Pop edges off the stack until we pop the specific bridge (u, v)
                    while True:
                        edge = self.edge_stack.pop()
                        bcc.append(edge)
                        if edge == (u, v) or edge == (v, u):
                            break
                            
                    self.bccs.append(bcc)
                    
            # Case B: Visited Neighbor (Valid Back-Edge found!)
            elif self.discovery_time[v] < self.discovery_time[u]:
                # We found a back-edge! This edge is part of a cycle, so we push 
                # it to the stack so it gets included in the current BCC!
                self.edge_stack.append((u, v))
                self.low_link[u] = min(self.low_link[u], self.discovery_time[v])
                
        # Edge case: If we finish exploring the absolute Root node, and there 
        # are still edges left on the stack, they form the final BCC!
        if parent == -1 and len(self.edge_stack) > 0:
            bcc = []
            while self.edge_stack:
                bcc.append(self.edge_stack.pop())
            self.bccs.append(bcc)


    def find_bccs(self) -> List[List[Tuple[int, int]]]:
        for i in range(self.V):
            if self.discovery_time[i] == -1:
                self._dfs(i, -1)
        return self.bccs


def demonstrate_bcc():
    section_header("Algorithm: Biconnected Components")
    
    vertices = 5
    # Same graph from the Articulation Points lab!
    # 0 - 1, 1 - 2, 2 - 0 (Triangle BCC #1)
    # 0 - 3 (Single Edge BCC #2)
    # 3 - 4 (Single Edge BCC #3)
    graph = {
        0: [1, 2, 3],
        1: [0, 2],
        2: [0, 1],
        3: [0, 4],
        4: [3]
    }
    
    print("Graph Adjacency List (Undirected):")
    for k, v in graph.items(): print(f" Node {k} connected to: {v}")
        
    print("\nExecuting Tarjan's Edge-Stack Algorithm...")
    bcc_finder = BiconnectedComponents(vertices, graph)
    bccs = bcc_finder.find_bccs()
    
    print(f"\nTotal Indestructible Clusters (BCCs) found: {len(bccs)}")
    for i, bcc in enumerate(bccs):
        print(f" -> Cluster {i+1} Edges: {bcc}")


# ==============================================================================
# 4. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why does BCC use an Edge Stack instead of a Node Stack?
   Answer: In a Directed Graph (SCC), a Node belongs to exactly ONE cluster. In an Undirected Graph, an Articulation Point is physically the "glue" that holds two clusters together. Therefore, the Articulation Point belongs to MULTIPLE Biconnected Components simultaneously! If we pushed nodes to the stack and popped them, we would rip the AP out of the graph and ruin the other BCCs that needed it. Edges are strictly unique to a single BCC, making them safe to pop.

2. Why is a single straight wire (e.g. 0-3) considered its own BCC?
   Answer: The mathematical definition of a Biconnected Component is a maximal subgraph where deleting ANY ONE node leaves it connected. If you have a single wire between 0 and 3, and you delete Node 0, you are left with just Node 3. Node 3 is technically a connected graph of size 1! So a single isolated edge perfectly satisfies the definition of a BCC.

3. Why do we check `discovery_time[v] < discovery_time[u]` for back-edges?
   Answer: In an undirected graph, if we are at U, we might see V (which is our Parent, so `disc[v] < disc[u]`), or we might see a true Back-Edge to an ancestor (`disc[v] < disc[u]`). We might also see a Forward-Edge to a descendant that has somehow already been visited (which shouldn't happen in standard DFS, but we check anyway). By ensuring we only push edges to the stack when pointing UP the tree to an older node, we prevent infinitely pushing duplicate edges.
"""

if __name__ == "__main__":
    demonstrate_bcc()
    print("\n[SUCCESS] Laboratory: Biconnected Components Completed.")
