"""
# ==============================================================================
# LABORATORY: GRAPH ALGORITHMS (DFS VARIATIONS)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You have reached Phase 08: Graphs.
# A Graph is simply a collection of "Nodes" (Vertices) connected by "Edges".
# The internet is a graph. Social networks are graphs. Maps are graphs.
# 
# How do we explore a graph? 
# Depth-First Search (DFS) is the most fundamental algorithm. It goes as DEEP 
# as mathematically possible down a single path before it hits a dead end, 
# then it Backtracks.
#
# DFS on a Tree is easy. But on a Graph, there are CYCLES. If A connects to B, 
# B to C, and C back to A, a naive DFS will spin in an infinite loop forever 
# until the computer crashes with a `RecursionError`.
# We MUST use a `visited` Set to track memory!
#
# Furthermore, what happens if the Graph is disconnected? (e.g., Two separate 
# islands of nodes that don't touch). A standard DFS will only explore the 
# island it starts on! We must wrap it in a global loop.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the Adjacency List representation.
# - Implement Recursive DFS with cycle protection.
# - Implement Iterative DFS using an explicit Stack.
# - Discover Disconnected Components.
#
# ==============================================================================
"""

from typing import Dict, List, Set

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. RECURSIVE DFS (O(V + E))
# ==============================================================================
def dfs_recursive(graph: Dict[int, List[int]], start_node: int, visited: Set[int] = None) -> List[int]:
    """
    Time Complexity: O(V + E) where V=Vertices, E=Edges.
    Space Complexity: O(V) for the visited set and the Call Stack.
    """
    if visited is None:
        visited = set()
        
    traversal_path = []
    
    # 1. MARK AND RECORD
    visited.add(start_node)
    traversal_path.append(start_node)
    
    # 2. EXPLORE NEIGHBORS
    for neighbor in graph.get(start_node, []):
        # 3. CYCLE PROTECTION
        if neighbor not in visited:
            # Recursively dive deeper into the unvisited neighbor!
            path = dfs_recursive(graph, neighbor, visited)
            traversal_path.extend(path)
            
    return traversal_path


# ==============================================================================
# 4. ITERATIVE DFS (O(V + E))
# ==============================================================================
def dfs_iterative(graph: Dict[int, List[int]], start_node: int) -> List[int]:
    """
    Uses a manual Stack instead of the OS Call Stack.
    Prevents `RecursionError` (StackOverflow) on massive graphs!
    """
    visited = set()
    traversal_path = []
    
    # Python Lists double perfectly as a LIFO Stack!
    stack = [start_node]
    
    while stack:
        # Pop from the TOP of the stack
        current = stack.pop()
        
        # We might have pushed this node multiple times from different neighbors,
        # so we must check if we already visited it before processing!
        if current not in visited:
            visited.add(current)
            traversal_path.append(current)
            
            # Push all unvisited neighbors to the stack!
            # Note: Because it's a LIFO stack, the LAST neighbor pushed will be 
            # the FIRST one popped. To match the exact output of Recursive DFS, 
            # we must push the neighbors in REVERSE order.
            for neighbor in reversed(graph.get(current, [])):
                if neighbor not in visited:
                    stack.append(neighbor)
                    
    return traversal_path


# ==============================================================================
# 5. DISCONNECTED COMPONENTS DFS
# ==============================================================================
def count_connected_components(graph: Dict[int, List[int]]) -> int:
    """
    Finds how many isolated "islands" exist in the graph.
    """
    visited = set()
    components = 0
    
    # Sweep every single node in the entire mathematical graph
    for node in graph:
        # If the node is unvisited, it means it is a brand new island!
        if node not in visited:
            components += 1
            # Fire the DFS engine to fully explore and paint the entire island
            dfs_recursive(graph, node, visited)
            
    return components


def demonstrate_dfs():
    section_header("Algorithm: Depth First Search")
    
    # Adjacency List representing a graph with a CYCLE and DISCONNECTED ISLANDS
    # Island 1: 1 -> 2 -> 3 -> 1 (Cycle)
    #             \-> 4
    # Island 2: 5 -> 6
    graph = {
        1: [2, 4],
        2: [3],
        3: [1],   # The Cycle!
        4: [],
        5: [6],
        6: []
    }
    
    print("Graph Adjacency List:")
    for k, v in graph.items(): print(f" Node {k} connects to {v}")
    
    print("\nExecuting Recursive DFS from Node 1...")
    path1 = dfs_recursive(graph, 1)
    print(f"Path: {path1}")
    
    print("\nExecuting Iterative (Stack) DFS from Node 1...")
    path2 = dfs_iterative(graph, 1)
    print(f"Path: {path2}")
    
    print("\nCounting Disconnected Components...")
    islands = count_connected_components(graph)
    print(f"Total Isolated Islands found: {islands} (Expected: 2)")


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why is the time complexity exactly $O(V + E)$?
   Answer: In a DFS, every vertex ($V$) is added to the `visited` set exactly once. Inside the loop, we iterate over the neighbors of that vertex. Over the entire execution of the algorithm, the inner loop processes every single edge ($E$) exactly once (in a directed graph) or twice (in an undirected graph). Mathematically, the work is $V$ vertices + $E$ edges = $O(V + E)$.

2. Why do we push neighbors in `reversed()` order for the Iterative Stack?
   Answer: Recursive DFS processes the first neighbor in the list, dives into it, and completely finishes it before looking at the second neighbor. If `neighbors = [A, B]`, Recursive DFS goes to `A` first. If we push `[A, B]` to a Stack in normal order, `B` goes on top! The `pop()` command will pull `B` off first, altering the traversal order. Reversing it to `[B, A]` puts `A` on top, ensuring the Iterative output perfectly matches the Recursive output.

3. What happens if you don't use a `visited` set on a graph?
   Answer: Infinite loops and catastrophic failure. If Node 1 points to 2, and Node 2 points to 1, the DFS will bounce between 1 and 2 billions of times per second. In Python, the recursion stack is strictly limited (usually 1,000 frames). It will hit the limit and instantly crash the program with a `RecursionError`.
"""

if __name__ == "__main__":
    demonstrate_dfs()
    print("\n[SUCCESS] Laboratory: DFS Variations Completed.")
