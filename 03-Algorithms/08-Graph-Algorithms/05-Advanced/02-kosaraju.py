"""
# ==============================================================================
# LABORATORY: KOSARAJU'S ALGORITHM (DOUBLE-PASS SCC)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# In the previous lab, you learned Tarjan's algorithm. It is incredibly fast, 
# finding all Strongly Connected Components (SCCs) in a single pass. But the 
# `low_link` and `in_stack` logic is notoriously difficult to memorize for interviews.
#
# In 1978, S. Rao Kosaraju published an alternative. It takes TWO passes, making 
# it slightly slower in practice, but the logic is mathematically beautiful and 
# incredibly easy to memorize.
#
# The Core Theorem of Kosaraju:
# If you reverse all the arrows in a Directed Graph, the physical locations of 
# the SCCs DO NOT CHANGE. If A, B, and C formed a cycle clockwise, reversing 
# the arrows just makes them form a cycle counter-clockwise. They are still an SCC!
#
# The Algorithm:
# 1. PASS 1 (The Topological Sort): Run a standard DFS. But there's a twist: 
#    ONLY add a node to a global Stack AFTER all its children have finished processing! 
#    This guarantees that the node that finished absolute last (the "Root" of the 
#    entire graph) ends up at the very TOP of the stack.
# 2. REVERSE THE GRAPH: Flip every single arrow backward.
# 3. PASS 2 (The Extraction): Pop the top node off the stack. Run a DFS on the 
#    REVERSED graph starting from that node. Because the arrows are backward, 
#    the DFS is mathematically trapped! It can only explore the exact nodes inside 
#    that specific SCC! Once the DFS halts, you have your isolated clique. 
#    Pop the next unvisited node and repeat.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand why reversing a graph preserves SCCs.
# - Implement the Post-Order Stack (Pass 1).
# - Build the Transpose Graph.
# - Implement the Trapped DFS (Pass 2).
#
# ==============================================================================
"""

from typing import Dict, List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. KOSARAJU'S ENGINE (O(V + E))
# ==============================================================================
class KosarajuSCC:
    def __init__(self, vertices: int, graph: Dict[int, List[int]]):
        self.V = vertices
        self.graph = graph
        
    def _dfs_pass_1(self, u: int, visited: List[bool], stack: List[int]):
        """
        Standard DFS, but strictly pushes to the stack POST-ORDER (after children finish).
        """
        visited[u] = True
        
        for v in self.graph.get(u, []):
            if not visited[v]:
                self._dfs_pass_1(v, visited, stack)
                
        # MAGIC: Only append to the stack AFTER exploring all possible children!
        stack.append(u)
        
    def _build_reversed_graph(self) -> Dict[int, List[int]]:
        """
        Creates the 'Transpose Graph' by flipping every arrow backward.
        """
        reversed_graph = {i: [] for i in range(self.V)}
        
        for u in range(self.V):
            for v in self.graph.get(u, []):
                # If original was u -> v, reversed is v -> u
                reversed_graph[v].append(u)
                
        return reversed_graph
        
    def _dfs_pass_2(self, u: int, visited: List[bool], reversed_graph: Dict[int, List[int]], current_scc: List[int]):
        """
        Trapped DFS on the reversed graph. Extracts the exact clique.
        """
        visited[u] = True
        current_scc.append(u)
        
        for v in reversed_graph.get(u, []):
            if not visited[v]:
                self._dfs_pass_2(v, visited, reversed_graph, current_scc)

    def find_sccs(self) -> List[List[int]]:
        """
        Executes Kosaraju's 3-step mathematical engine.
        """
        # 1. PASS 1: Fill the Stack
        stack = []
        visited = [False] * self.V
        
        for i in range(self.V):
            if not visited[i]:
                self._dfs_pass_1(i, visited, stack)
                
        # 2. REVERSE THE GRAPH
        reversed_graph = self._build_reversed_graph()
        
        # 3. PASS 2: Extract SCCs using the Stack
        # We must reset the visited array for the second pass!
        visited = [False] * self.V
        sccs = []
        
        # Pop from the absolute top of the stack (the nodes that finished last!)
        while stack:
            u = stack.pop()
            
            # If this node hasn't been claimed by an SCC yet...
            if not visited[u]:
                current_scc = []
                # Run the Trapped DFS!
                self._dfs_pass_2(u, visited, reversed_graph, current_scc)
                sccs.append(current_scc)
                
        return sccs


def demonstrate_kosaraju():
    section_header("Algorithm: Kosaraju's SCC")
    
    vertices = 5
    # Same graph from the Tarjan lab!
    # 0 -> 2, 2 -> 1, 1 -> 0 (SCC #1)
    # 0 -> 3 
    # 3 -> 4, 4 -> 3 (SCC #2)
    graph = {
        0: [2, 3],
        1: [0],
        2: [1],
        3: [4],
        4: [3]
    }
    
    print("Graph Adjacency List (Directed):")
    for k, v in graph.items(): print(f" Node {k} points to: {v}")
        
    print("\nExecuting Kosaraju's Double-Pass Engine...")
    kosaraju = KosarajuSCC(vertices, graph)
    cliques = kosaraju.find_sccs()
    
    print(f"\nTotal Strongly Connected Components found: {len(cliques)}")
    for i, clique in enumerate(cliques):
        print(f" -> SCC {i+1}: {clique}")


# ==============================================================================
# 4. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why does the `stack.append(u)` MUST happen post-order?
   Answer: We need the nodes that act as "Roots" or "Sinks" for the entire graph to be processed last. If we pushed them pre-order, the stack would just be a random jumble. By pushing post-order, a node is only added to the stack AFTER all of its descendants are in the stack. This mathematically guarantees that if there is a massive macro-structure to the graph (e.g. SCC #1 points to SCC #2), the nodes from SCC #1 will be higher on the stack than SCC #2!

2. Why is the DFS "Trapped" in Pass 2?
   Answer: Imagine the macro structure: SCC A -> SCC B. 
   During Pass 1, the stack guarantees that a node from SCC A is at the absolute top of the stack.
   In Pass 2, we pop the node from SCC A and run DFS on the REVERSED graph. 
   Because the graph is reversed, the macro structure is now SCC A <- SCC B. 
   When the DFS explores SCC A, it can freely travel in the local reversed cycle to find all A nodes. But when it looks outward, the bridge to SCC B is pointing backward! The DFS literally cannot leave SCC A. It halts, perfectly extracting the cluster!

3. Tarjan vs Kosaraju. Which is better?
   Answer: 
   - Kosaraju is easier to write and understand (two basic DFS functions). 
   - Tarjan requires only one pass and does not require allocating memory for a completely new reversed graph. In massive production systems where graph memory footprint is critical, Tarjan is vastly superior.
"""

if __name__ == "__main__":
    demonstrate_kosaraju()
    print("\n[SUCCESS] Laboratory: Kosaraju's Algorithm Completed.")
