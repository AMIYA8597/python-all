"""
# ==============================================================================
# LABORATORY: TOPOLOGICAL SORT & EVENTUAL SAFE STATES
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You've learned how to use Topological Sort (Kahn's Algorithm) to order tasks 
# or detect cycles. 
# But in a massive system with hundreds of microservices, some services might form 
# a localized circular dependency (A -> B -> A), while other services do not. 
# If you are analyzing system stability, you want to identify all "Safe Nodes" — 
# nodes that are GUARANTEED to eventually reach a safe termination state and will 
# NEVER get trapped in a cycle.
#
# This problem (LeetCode #802: Find Eventual Safe States) is brilliantly solved 
# using a REVERSED Topological Sort. By reversing the edges and pushing "Terminal 
# Nodes" (out-degree 0) into the queue, we can mathematically prove which nodes 
# are safe!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the concept of "Terminal Nodes" and "Safe States".
# - Apply Kahn's Algorithm on a REVERSED graph to solve complex flow problems.
#
# ==============================================================================
"""

from collections import deque, defaultdict
from typing import List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. REVERSE TOPOLOGICAL SORT (EVENTUAL SAFE STATES)
# ==============================================================================
def eventual_safe_nodes(graph: List[List[int]]) -> List[int]:
    """
    LeetCode #802: Find Eventual Safe States
    A node is a "Terminal Node" if it has NO outgoing edges.
    A node is a "Safe Node" if ALL possible paths starting from it lead strictly 
    to a Terminal Node (meaning it cannot possibly enter a cycle).
    
    Time Complexity: O(V + E)
    """
    n = len(graph)
    
    # 1. Build the REVERSED Graph and track original OUT-DEGREES
    reversed_graph = defaultdict(list)
    out_degree = [0] * n
    
    for i in range(n):
        for destination in graph[i]:
            # Original edge: i -> destination
            # Reversed edge: destination -> i
            reversed_graph[destination].append(i)
        
        # We track how many outgoing edges the node ORIGINAL had
        out_degree[i] = len(graph[i])
        
    # 2. Initialize Queue with Terminal Nodes
    # Any node with an original out-degree of 0 is inherently safe!
    queue = deque([i for i in range(n) if out_degree[i] == 0])
    
    # Track the safe nodes
    safe_nodes = [False] * n
    
    # 3. Process Kahn's Algorithm backwards
    while queue:
        node = queue.popleft()
        
        # If this node was placed in the queue, we have proven it is safe
        safe_nodes[node] = True
        
        # Look at all nodes that USED to point to this safe node
        for neighbor in reversed_graph[node]:
            # We "remove" this outgoing edge from the neighbor
            out_degree[neighbor] -= 1
            
            # If the neighbor now has 0 outgoing edges left to process, it means 
            # ALL of its outgoing edges successfully pointed to safe nodes!
            # Therefore, this neighbor is ALSO safe.
            if out_degree[neighbor] == 0:
                queue.append(neighbor)
                
    # Return sorted indices of all safe nodes
    return [i for i in range(n) if safe_nodes[i]]


def demonstrate_safe_states():
    section_header("Algorithm: Eventual Safe States (Reversed Kahn's)")
    
    print("Graph Structure:")
    print(" 0 -> 1, 2")
    print(" 1 -> 2, 3")
    print(" 2 -> 5")
    print(" 3 -> 0 (Cycle! 0 -> 1 -> 3 -> 0)")
    print(" 4 -> 5")
    print(" 5 -> (Terminal Node)")
    print(" 6 -> (Terminal Node)")
    
    # Adjacency list matching the structure above
    graph = [
        [1, 2], # Node 0
        [2, 3], # Node 1
        [5],    # Node 2
        [0],    # Node 3
        [5],    # Node 4
        [],     # Node 5 (Terminal)
        []      # Node 6 (Terminal)
    ]
    
    safe_nodes = eventual_safe_nodes(graph)
    
    print("\nExpected Safe Nodes:")
    print(" - 5 and 6 are Terminal (Inherently Safe).")
    print(" - 2 points ONLY to 5. So 2 is Safe.")
    print(" - 4 points ONLY to 5. So 4 is Safe.")
    print(" - 0, 1, and 3 are trapped in a cycle or point to a cycle. UNSAFE.")
    
    print(f"\nCalculated Safe Nodes: {safe_nodes} (Expected: [2, 4, 5, 6])")


# ==============================================================================
# 4. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Standard Kahn's Algorithm starts by placing nodes with an IN-DEGREE of 0 into the queue. Why does the Eventual Safe States algorithm place nodes with an OUT-DEGREE of 0 into the queue?
   Answer: Because we are working backwards! We want to prove that paths safely terminate. We start from the absolute end (Terminal Nodes, Out-Degree 0) and walk backwards up the graph, validating that every branch upstream eventually flows into these safe terminal nodes.

2. Why must we reverse the graph (`reversed_graph`)?
   Answer: Because we start at the Terminal Nodes and need to notify the nodes that point TO them. In a standard adjacency list, you only know where a node is going, not where it came from. Reversing the graph allows information to flow upstream from the destination to the source.

3. Can this algorithm detect nodes trapped in a cycle?
   Answer: Yes, inherently. A node in a cycle will always have an out-degree of at least 1 pointing to another node in the cycle. Because the cycle has no absolute "end", none of the nodes in the cycle will ever have their out-degrees drop to 0, so they will never enter the queue, and will never be marked as Safe.
"""

if __name__ == "__main__":
    demonstrate_safe_states()
    print("\n[SUCCESS] Laboratory: Eventual Safe States Completed.")
