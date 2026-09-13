"""
# ==============================================================================
# LABORATORY: TOPOLOGICAL SORT & KOSARAJU'S ALGORITHM
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# When resolving dependencies (e.g., Docker builds, Makefile compilation, 
# or College prerequisites), you must execute tasks in a specific order. 
# "Topological Sort" takes a Directed Acyclic Graph (DAG) and outputs a linear 
# order of nodes such that every node appears BEFORE all the nodes it points to.
#
# Additionally, in massive networks (like Twitter followers), how do you find 
# tight-knit communities where everyone can reach everyone else? This is the 
# "Strongly Connected Components" (SCC) problem. Kosaraju's Algorithm solves it 
# elegantly using two passes of DFS.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand and implement Topological Sort using DFS (Post-order reverse).
# - Understand the concept of the Transpose (Reversed) Graph.
# - Implement Kosaraju's Algorithm to find Strongly Connected Components.
#
# ==============================================================================
"""

from collections import defaultdict
from typing import List, Dict, Set

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. TOPOLOGICAL SORT (DFS APPROACH)
# ==============================================================================
def topological_sort(graph: Dict[int, List[int]], num_nodes: int) -> List[int]:
    """
    LeetCode #210: Course Schedule II
    Time Complexity: O(V + E)
    
    Logic:
    If we run DFS, the LAST node to finish (no unvisited neighbors) must be 
    the final step of some dependency chain.
    If we push nodes onto a stack right before returning (Post-Order), 
    and then pop them off the stack at the end, we get a valid Topological Sort!
    """
    visited = set()
    stack = []
    
    def dfs(node: int):
        visited.add(node)
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                dfs(neighbor)
        # Node has finished exploring all descendants. Push to stack!
        stack.append(node)
        
    for i in range(num_nodes):
        if i not in visited:
            dfs(i)
            
    # The stack contains the nodes in reverse Topological Order. 
    # Reverse it to get the correct execution order.
    return stack[::-1]

def demonstrate_topological_sort():
    section_header("Algorithm: Topological Sort (DFS)")
    
    # 5 -> 2, 5 -> 0, 4 -> 0, 4 -> 1, 2 -> 3, 3 -> 1
    graph = {
        5: [2, 0],
        4: [0, 1],
        2: [3],
        3: [1],
        0: [],
        1: []
    }
    
    print("Graph Dependencies:")
    print(" 5 requires nothing. It unlocks 2 and 0.")
    print(" 4 requires nothing. It unlocks 0 and 1.")
    print(" 2 unlocks 3. 3 unlocks 1.")
    
    order = topological_sort(graph, 6)
    print(f"\nValid Execution Order: {order}")


# ==============================================================================
# 4. STRONGLY CONNECTED COMPONENTS (KOSARAJU'S ALGORITHM)
# ==============================================================================
def get_transpose_graph(graph: Dict[int, List[int]], num_nodes: int) -> Dict[int, List[int]]:
    """Reverses the direction of ALL edges in the graph."""
    reversed_graph = defaultdict(list)
    for u in range(num_nodes):
        for v in graph.get(u, []):
            reversed_graph[v].append(u)
    return reversed_graph

def kosaraju_scc(graph: Dict[int, List[int]], num_nodes: int) -> List[List[int]]:
    """
    Kosaraju's Algorithm for finding Strongly Connected Components (SCCs).
    Time Complexity: O(V + E)
    
    An SCC is a subgraph where every node can reach every other node.
    
    Algorithm:
    1. Run standard DFS on the original graph. Push nodes to a stack upon finishing (Post-Order).
    2. Reverse ALL edges in the graph (Transpose Graph).
    3. Pop nodes from the stack one by one. If unvisited, run DFS on the REVERSED graph.
       The nodes visited during this DFS pass form exactly ONE Strongly Connected Component!
    """
    # PASS 1: Build the finishing order stack
    visited = set()
    stack = []
    
    def dfs_pass_1(node: int):
        visited.add(node)
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                dfs_pass_1(neighbor)
        stack.append(node)
        
    for i in range(num_nodes):
        if i not in visited:
            dfs_pass_1(i)
            
    # PASS 2: DFS on the Reversed Graph
    reversed_graph = get_transpose_graph(graph, num_nodes)
    visited.clear() # Reset visited set
    scc_list = []
    
    def dfs_pass_2(node: int, current_scc: List[int]):
        visited.add(node)
        current_scc.append(node)
        for neighbor in reversed_graph.get(node, []):
            if neighbor not in visited:
                dfs_pass_2(neighbor, current_scc)
                
    # Process nodes in the order they finished (pop from stack)
    while stack:
        node = stack.pop()
        if node not in visited:
            current_scc = []
            dfs_pass_2(node, current_scc)
            scc_list.append(current_scc)
            
    return scc_list

def demonstrate_kosaraju():
    section_header("Algorithm: Kosaraju's Strongly Connected Components")
    
    # 0 -> 1 -> 2 -> 0 (Triangle SCC)
    # 2 -> 3
    # 3 -> 4 (Linear, independent SCCs)
    graph = {
        0: [1],
        1: [2],
        2: [0, 3],
        3: [4],
        4: []
    }
    
    print("Graph Structure:")
    print(" Component 1: 0, 1, 2 form a cycle.")
    print(" Node 2 points to 3. Node 3 points to 4.")
    
    sccs = kosaraju_scc(graph, 5)
    
    print(f"\nStrongly Connected Components Found: {len(sccs)}")
    for i, scc in enumerate(sccs):
        print(f"  SCC {i+1}: {scc}")


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why does Topological Sort use a Post-Order (DFS finish time) stack?
   Answer: Because we want to ensure that a node is only added to our sequence AFTER all the nodes that depend on it have been processed. By pushing to a stack as the final step of a recursive DFS function, we guarantee it is placed after its descendants. Reversing the stack yields the correct topological order.

2. Does Topological Sort work if the graph has a cycle?
   Answer: No. A Topological Sort is strictly for Directed Acyclic Graphs (DAGs). If a cycle exists, there is a circular dependency (A requires B requires A), making any linear execution order impossible.

3. Why does reversing the graph in Kosaraju's algorithm isolate the Strongly Connected Components?
   Answer: If a group of nodes forms a cycle (an SCC), they can all reach each other regardless of edge direction! However, if SCC 1 points to SCC 2 with a one-way edge, reversing the graph means SCC 2 now points back to SCC 1. Because we process the nodes in decreasing finish-time order from Pass 1, we guarantee we start Pass 2 in the "sink" components of the reversed graph, preventing the DFS from leaking into other SCCs.
"""

if __name__ == "__main__":
    demonstrate_topological_sort()
    demonstrate_kosaraju()
    print("\n[SUCCESS] Laboratory: Advanced DFS (Topo Sort & Kosaraju) Completed.")
