"""
# ==============================================================================
# LABORATORY: ADVANCED COMPONENTS (TARJAN'S & BRIDGES)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You learned Kosaraju's algorithm for Strongly Connected Components (SCCs), 
# which requires two DFS passes and reversing the graph. 
# Tarjan's Algorithm accomplishes the EXACT same thing in a SINGLE DFS pass using 
# "Low-Link" values, making it highly efficient.
#
# Furthermore, what if you manage a power grid, and you need to know which single 
# power line, if cut by a storm, would split the entire state into two disconnected 
# grids? That critical power line is called a "Bridge" (or Cut Edge). 
# Tarjan's Low-Link logic is the exact algorithm used to find these critical 
# vulnerabilities in any network.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand ID and Low-Link values in Tarjan's Algorithm.
# - Implement Tarjan's Algorithm to find SCCs.
# - Implement Tarjan's Algorithm to find Bridges (Critical Connections).
#
# ==============================================================================
"""

from collections import defaultdict
from typing import List, Dict

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. TARJAN'S ALGORITHM (STRONGLY CONNECTED COMPONENTS)
# ==============================================================================
def tarjans_scc(num_nodes: int, edges: List[List[int]]) -> List[List[int]]:
    """
    Finds Strongly Connected Components in a Directed Graph in a single DFS pass.
    """
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        
    # Variables used across the recursive DFS
    id_counter = 0
    ids = [-1] * num_nodes      # The step number when a node was visited
    low = [0] * num_nodes       # The lowest ID reachable from this node
    on_stack = [False] * num_nodes # Is the node currently in the current SCC stack?
    stack = []
    
    sccs = []
    
    def dfs(at: int):
        nonlocal id_counter
        stack.append(at)
        on_stack[at] = True
        ids[at] = low[at] = id_counter
        id_counter += 1
        
        # Explore neighbors
        for to in graph[at]:
            if ids[to] == -1: # Unvisited
                dfs(to)
                # On return, this node's low-link is the minimum of its own or its child's
                low[at] = min(low[at], low[to])
            elif on_stack[to]: 
                # This is a back-edge to a node already in our current component!
                low[at] = min(low[at], ids[to])
                
        # After exploring all neighbors, if this node's low-link equals its original ID,
        # it means this node is the ROOT of an SCC!
        if ids[at] == low[at]:
            current_scc = []
            while True:
                node = stack.pop()
                on_stack[node] = False
                current_scc.append(node)
                if node == at:
                    break
            sccs.append(current_scc)

    for i in range(num_nodes):
        if ids[i] == -1:
            dfs(i)
            
    return sccs

def demonstrate_tarjans_scc():
    section_header("Algorithm: Tarjan's SCC (Single Pass)")
    
    # 0 -> 1 -> 2 -> 0 (Triangle SCC)
    # 2 -> 3
    # 3 -> 4 (Linear, independent SCCs)
    edges = [[0, 1], [1, 2], [2, 0], [2, 3], [3, 4]]
    
    print("Graph Structure:")
    print(" Component 1: 0, 1, 2 form a cycle.")
    print(" Node 2 points to 3. Node 3 points to 4.")
    
    sccs = tarjans_scc(5, edges)
    
    print(f"\nStrongly Connected Components Found: {len(sccs)}")
    for i, scc in enumerate(sccs):
        print(f"  SCC {i+1}: {scc}")


# ==============================================================================
# 4. BRIDGES (CRITICAL CONNECTIONS IN A NETWORK)
# ==============================================================================
def find_bridges(num_nodes: int, edges: List[List[int]]) -> List[List[int]]:
    """
    LeetCode #1192: Critical Connections in a Network
    Finds all Bridges (edges that, if removed, disconnect the graph).
    This graph is UNDIRECTED.
    """
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
        
    id_counter = 0
    ids = [-1] * num_nodes
    low = [0] * num_nodes
    bridges = []
    
    def dfs(at: int, parent: int):
        nonlocal id_counter
        ids[at] = low[at] = id_counter
        id_counter += 1
        
        for to in graph[at]:
            if to == parent: # Ignore the edge we just came from
                continue
                
            if ids[to] == -1: # Unvisited child
                dfs(to, at)
                low[at] = min(low[at], low[to])
                
                # CRITICAL LOGIC FOR A BRIDGE:
                # If the child's absolute lowest reachable node is STRICTLY GREATER 
                # than the current node's ID, it means the child has NO back-edge 
                # to ancestors. 
                # Therefore, the only way into that child's subtree is this exact 
                # edge. If we cut it, the child is stranded!
                if low[to] > ids[at]:
                    bridges.append([at, to])
                    
            else:
                # We found a back-edge! This node can loop back to a previously seen node.
                low[at] = min(low[at], ids[to])
                
    # Assume connected graph starting at 0
    dfs(0, -1)
    return bridges

def demonstrate_bridges():
    section_header("Algorithm: Finding Bridges (Critical Connections)")
    
    print("Graph Structure (Undirected):")
    print(" 0 --- 1")
    print(" |   /    (0, 1, 2 form a redundant triangle)")
    print(" 2 --- 3  (Node 2 connects to Node 3. This is the only way in/out of the triangle!)")
    print("       |")
    print("       4  (Node 3 connects to Node 4)")
    
    edges = [[0, 1], [1, 2], [2, 0], [2, 3], [3, 4]]
    bridges = find_bridges(5, edges)
    
    print("\nBridges (Critical Edges) found:")
    for u, v in bridges:
        print(f"  Edge ({u} <--> {v})")
    
    print("\nNotice that removing (0, 1) doesn't break the graph because (1, 2, 0) is a cycle.")
    print("But removing (2, 3) strands nodes 3 and 4 entirely!")


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. What does the "Low-Link" value represent in Tarjan's Algorithm?
   Answer: It represents the smallest node ID reachable from a given node, INCLUDING back-edges. If a node explores its children, and none of them have a back-edge to an older node, the node's Low-Link will remain equal to its original ID. This means the node is the strict root of a component.

2. How do we identify a Bridge mathematically?
   Answer: `if low[child] > id[current]:`. If the child's lowest reachable node is strictly greater than the current node's ID, it means the child's entire subtree never loops back to the current node or above. Therefore, the edge from `current -> child` is the ONLY way into that subtree. It is a bridge.

3. Tarjan's vs Kosaraju's for SCCs. Which is better?
   Answer: Tarjan's is technically faster in practice because it only requires ONE pass of DFS and doesn't require allocating memory to reverse the entire graph. However, Kosaraju's is conceptually much simpler and easier to memorize for interviews. Both are technically O(V + E).
"""

if __name__ == "__main__":
    demonstrate_tarjans_scc()
    demonstrate_bridges()
    print("\n[SUCCESS] Laboratory: Advanced Components (Tarjan & Bridges) Completed.")
