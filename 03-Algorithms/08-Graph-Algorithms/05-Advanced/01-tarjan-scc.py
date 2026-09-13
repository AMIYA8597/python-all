"""
# ==============================================================================
# LABORATORY: TARJAN'S STRONGLY CONNECTED COMPONENTS (SCC)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You are building Twitter (or X). Users follow each other, creating a massive 
# DIRECTED graph. (A -> B means A follows B).
#
# You want to find "Echo Chambers" or "Cliques": A specific group of users where 
# EVERY single person in the group can mathematically reach EVERY other person in 
# the group through a chain of follows.
#
# In Graph Theory, this is called a "Strongly Connected Component" (SCC).
#
# How do we find them? 
# A naive algorithm would run a full BFS from every single user to see who they 
# can reach, taking O(V * (V+E)) time. For 300 million users, the server melts.
#
# In 1972, Robert Tarjan (the same genius who formalized the Push-Relabel max flow, 
# and the Disjoint Set Union time complexity) invented an algorithm that finds 
# EVERY SCC in the entire graph in a single pass: O(V + E) time.
#
# The Magic:
# He uses a single Depth First Search (DFS). As the DFS explores, it assigns a 
# "Discovery Time" to every node. It also tracks the "Lowest Reachable Time" 
# (Low-Link value). 
# If a node discovers a back-edge to a previously visited node, it updates its 
# low-link! If a node finishes its DFS and realizes its low-link perfectly 
# matches its discovery time, it means it is the "Root" of an SCC! It instantly 
# pops all the nodes off a special tracking stack, perfectly isolating the clique!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand Discovery Time vs Low-Link Value.
# - Implement Tarjan's single-pass DFS engine.
# - Understand the role of the Active Stack.
#
# ==============================================================================
"""

from typing import Dict, List, Set

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. TARJAN'S SCC ENGINE (O(V + E))
# ==============================================================================
class TarjanSCC:
    def __init__(self, vertices: int, graph: Dict[int, List[int]]):
        self.V = vertices
        self.graph = graph
        
        # The global clock. Ticks up every time we discover a new node.
        self.time = 0
        
        # Arrays to track the DFS state of every node
        self.discovery_time = [-1] * vertices
        self.low_link = [-1] * vertices
        
        # The Active Stack tracks nodes that are CURRENTLY part of the DFS path 
        # being explored.
        self.stack = []
        self.in_stack = [False] * vertices
        
        # The final output: A list of cliques (SCCs)
        self.sccs = []
        
    def _dfs(self, u: int):
        """
        The recursive DFS core.
        """
        # 1. DISCOVERY
        # Record the exact tick of the clock when this node was discovered
        self.discovery_time[u] = self.time
        self.low_link[u] = self.time
        self.time += 1
        
        # Push to the active stack
        self.stack.append(u)
        self.in_stack[u] = True
        
        # 2. EXPLORE NEIGHBORS
        for v in self.graph.get(u, []):
            # Case A: We have never seen this neighbor before.
            if self.discovery_time[v] == -1:
                # Recurse deeper!
                self._dfs(v)
                # When the recursion returns, does this neighbor have a path 
                # to a node HIGHER up in the tree than we do? Steal its low-link!
                self.low_link[u] = min(self.low_link[u], self.low_link[v])
                
            # Case B: We HAVE seen this neighbor, AND it's currently in the stack!
            # This means we just found a "Back-Edge" pointing up the tree! We found a cycle!
            elif self.in_stack[v]:
                # Update our low-link to match the discovery time of this higher node!
                self.low_link[u] = min(self.low_link[u], self.discovery_time[v])
                
        # 3. ROOT DETECTION & COMPONENT EXTRACTION
        # After fully exploring all neighbors, check the mathematical trigger:
        # If my low-link perfectly matches my original discovery time, it means 
        # I am the absolute highest node in this specific cycle. I am the ROOT 
        # of the Strongly Connected Component!
        if self.low_link[u] == self.discovery_time[u]:
            clique = []
            
            # Pop nodes off the stack until I pop MYSELF!
            while True:
                popped_node = self.stack.pop()
                self.in_stack[popped_node] = False
                clique.append(popped_node)
                
                if popped_node == u:
                    break
                    
            # Record this isolated clique
            self.sccs.append(clique)


    def find_sccs(self) -> List[List[int]]:
        """
        Executes Tarjan's algorithm across the entire graph.
        We must loop through all vertices to catch disconnected islands.
        """
        for i in range(self.V):
            if self.discovery_time[i] == -1:
                self._dfs(i)
                
        return self.sccs


def demonstrate_tarjan():
    section_header("Algorithm: Tarjan's SCC (Graph Cliques)")
    
    vertices = 5
    # Adjacency List for a Directed Graph
    # 0 -> 2, 2 -> 1, 1 -> 0 (This is a Cycle! SCC #1)
    # 0 -> 3 (One way bridge)
    # 3 -> 4 (One way bridge)
    # 4 -> 3 (Wait, 3 and 4 point to each other! SCC #2)
    graph = {
        0: [2, 3],
        1: [0],
        2: [1],
        3: [4],
        4: [3]
    }
    
    print("Graph Adjacency List (Directed Follows):")
    for k, v in graph.items(): print(f" User {k} follows: {v}")
        
    print("\nExecuting Tarjan's O(V+E) Algorithm...")
    tarjan = TarjanSCC(vertices, graph)
    cliques = tarjan.find_sccs()
    
    print(f"\nTotal Echo Chambers (SCCs) found: {len(cliques)}")
    for i, clique in enumerate(cliques):
        print(f" -> Clique {i+1}: {clique}")
        
    print("\nNotice how Users 0, 1, 2 form one clique, and 3, 4 form another!")


# ==============================================================================
# 4. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. What does the `low_link` value actually physically represent?
   Answer: The `low_link` is the absolute lowest `discovery_time` (meaning the highest up in the DFS tree) reachable from a node, including all its descendants, using at most ONE back-edge. If a node explores its neighbors, and one of its descendants finds a secret backdoor pipe leading all the way back up to the Root, that descendant passes the Root's `discovery_time` back down the chain, updating everyone's `low_link`.

2. Why do we need the `in_stack` array? Why can't we just check if it's visited?
   Answer: In a Directed Graph, you can have "Cross-Edges" that point to nodes in completely different branches of the tree that have ALREADY finished their DFS and been popped off the stack! If Node A points to Node Z (which finished 5 minutes ago and is sitting in a completely different SCC), we DO NOT want to update Node A's low-link with Z's time! The `in_stack` boolean guarantees we only update low-links if the target node is CURRENTLY an active ancestor in our specific cycle path!

3. Is Tarjan's the only way to find SCCs?
   Answer: No, Kosaraju's Algorithm is another famous $O(V+E)$ algorithm. It is arguably easier to understand: It runs a full DFS, pushes nodes to a stack based on their finish times, then physically REVERSES every edge in the entire graph, and runs a second DFS popping from the stack. However, Tarjan's is vastly preferred in FAANG/Production because it only requires ONE pass, whereas Kosaraju requires two full passes and the overhead of duplicating the graph in reverse.
"""

if __name__ == "__main__":
    demonstrate_tarjan()
    print("\n[SUCCESS] Laboratory: Tarjan's SCC Algorithm Completed.")
