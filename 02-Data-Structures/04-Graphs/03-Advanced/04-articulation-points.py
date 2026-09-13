"""
# ==============================================================================
# LABORATORY: ARTICULATION POINTS (CUT VERTICES)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You learned how to find "Bridges" (Cut Edges) using Tarjan's Low-Link algorithm. 
# A bridge is a critical cable that, if cut, disconnects the network.
# 
# What if the cables are indestructible, but the SERVERS (routers) can fail? 
# An "Articulation Point" (Cut Vertex) is a single node that, if it goes offline, 
# splits the entire network into disconnected components. Identifying these nodes 
# is critical for reinforcing network infrastructure, placing backup generators, 
# or identifying single points of failure in distributed systems.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Differentiate between Bridges (`low[v] > id[u]`) and Articulation Points (`low[v] >= id[u]`).
# - Handle the special "Root Node" edge case in DFS.
# - Implement the algorithm in O(V + E) time.
#
# ==============================================================================
"""

from collections import defaultdict
from typing import List, Set

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. ARTICULATION POINTS IMPLEMENTATION
# ==============================================================================
def find_articulation_points(num_nodes: int, edges: List[List[int]]) -> List[int]:
    """
    Time Complexity: O(V + E)
    Space Complexity: O(V)
    """
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u) # Undirected graph
        
    id_counter = 0
    ids = [-1] * num_nodes
    low = [0] * num_nodes
    
    # Use a set because a node might trigger the AP condition multiple times 
    # (if it has multiple independent children that rely on it).
    articulation_points = set()
    
    def dfs(at: int, parent: int):
        nonlocal id_counter
        ids[at] = low[at] = id_counter
        id_counter += 1
        
        # Track how many independent DFS branches spawn from this node.
        # This is ONLY used to check if the root node is an Articulation Point.
        children = 0
        
        for to in graph[at]:
            if to == parent:
                continue
                
            if ids[to] == -1: # Unvisited child
                children += 1
                dfs(to, at)
                
                # On return, update the low-link
                low[at] = min(low[at], low[to])
                
                # CRITICAL LOGIC FOR ARTICULATION POINT:
                # If the child's lowest reachable node is >= the current node's ID.
                # Notice the >= (Greater than OR EQUAL TO).
                # If it's >, it means the child has NO back-edges (it's a Bridge).
                # If it's ==, it means the child's absolute highest back-edge points 
                # EXACTLY to the current node, and no higher. 
                # In both cases, the current node is the absolute bottleneck! If we 
                # delete it, the child is stranded.
                if parent != -1 and low[to] >= ids[at]:
                    articulation_points.add(at)
                    
            else:
                # Back-edge found
                low[at] = min(low[at], ids[to])
                
        # ROOT NODE EDGE CASE:
        # The DFS root node has no parent (parent == -1). The mathematical `low[to] >= ids[at]` 
        # condition is essentially ALWAYS true for the root.
        # Instead, the root is an Articulation Point ONLY IF it spawns 2 or more 
        # independent children in the DFS tree. If it only spawns 1 child, deleting 
        # the root just removes a leaf-like appendage, it doesn't split the graph!
        if parent == -1 and children > 1:
            articulation_points.add(at)

    # Graph might be disconnected, check all nodes
    for i in range(num_nodes):
        if ids[i] == -1:
            dfs(i, -1)
            
    return list(articulation_points)

def demonstrate_articulation_points():
    section_header("Algorithm: Articulation Points (Cut Vertices)")
    
    print("Graph Structure (Undirected):")
    print(" 0 --- 1")
    print(" |   /   ")
    print(" 2 --- 3 --- 4")
    print("             | \\")
    print("             5--6")
    
    # 0, 1, 2 form a triangle (Safe loop)
    # 2 connects to 3
    # 3 connects to 4
    # 4 connects to 5 and 6, which connect to each other (Triangle)
    
    # What happens if we delete Node 3? 
    #   [0,1,2] splits from [4,5,6]. Node 3 is an AP!
    # What happens if we delete Node 4?
    #   [0,1,2,3] splits from [5,6]. Node 4 is an AP!
    # What happens if we delete Node 2?
    #   [0,1] splits from [3,4,5,6]. Node 2 is an AP!
    
    edges = [
        [0, 1], [1, 2], [2, 0],
        [2, 3],
        [3, 4],
        [4, 5], [4, 6], [5, 6]
    ]
    
    aps = find_articulation_points(7, edges)
    
    print(f"\nArticulation Points Found: {sorted(aps)}")
    print("(Expected: [2, 3, 4])")


# ==============================================================================
# 4. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. What is the difference between `low[v] > id[u]` and `low[v] >= id[u]`?
   Answer: `>` is used for finding Bridges (Cut Edges). It strictly means the child has NO back-edges to the current node or above. `>=` is used for finding Articulation Points (Cut Vertices). It means the child's highest back-edge might point directly to the current node, but no higher. Therefore, deleting the current node destroys the only escape route for the child's subtree.

2. Why does the Root Node of the DFS tree require a special case?
   Answer: The Root Node's ID is 0. Since no node can have a lower ID, the condition `low[child] >= id[root]` will basically always evaluate to True (e.g., `0 >= 0`). However, if the Root only has 1 branch, deleting it just removes a dangling node; it doesn't split the rest of the network. Therefore, the Root is ONLY an AP if it launches 2 or more independent DFS branches.

3. Are all endpoints of a Bridge guaranteed to be Articulation Points?
   Answer: Mostly, yes. If an edge U-V is a bridge, removing it splits the graph. Removing node U achieves the same split. The ONLY exception is if U or V has a degree of exactly 1 (meaning it's a dead-end leaf node). Removing a leaf node doesn't split the graph into two, it just shrinks it.
"""

if __name__ == "__main__":
    demonstrate_articulation_points()
    print("\n[SUCCESS] Laboratory: Articulation Points Completed.")
