"""
# ==============================================================================
# LABORATORY: BI-DIRECTIONAL SEARCH (PATH RECONSTRUCTION)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You learned that Bi-Directional BFS exponentially reduces the time and space 
# bounds of finding a shortest path. 
# By launching a BFS from the Start, and a BFS from the Target simultaneously, 
# they meet in the middle, slashing the time from O(b^d) to O(b^(d/2)).
#
# But there is a massive engineering challenge. 
# When the two ripples finally crash into each other at some random node in the 
# middle of the graph (the "Collision Node"), how do you mathematically 
# reconstruct the exact Shortest Path from Start to Target?
#
# Standard BFS uses a single `parent` map and just walks backward.
# Bi-Directional BFS requires TWO completely separate `parent` maps. 
# When the collision happens, you must:
# 1. Trace the Start map backward from the Collision Node to the Start Node.
# 2. Trace the Target map backward from the Collision Node to the Target Node.
# 3. Carefully reverse and stitch the two halves together without duplicating 
#    the collision node in the final array!
#
# This is a classic FAANG interview requirement for problems like "Word Ladder".
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Manage dual queues, dual visited sets, and dual parent maps.
# - Detect the exact collision frame.
# - Execute complex pointer stitching to reconstruct the final path array.
#
# ==============================================================================
"""

from collections import deque
from typing import Dict, List, Optional

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. BI-DIRECTIONAL PATH RECONSTRUCTION ENGINE
# ==============================================================================
def reconstruct_path(parent_start: Dict[int, int], parent_target: Dict[int, int], collision_node: int) -> List[int]:
    """
    Stitches the two parent maps together at the collision node!
    """
    # 1. Trace backward from Collision to Start
    path_from_start = []
    curr = collision_node
    while curr is not None:
        path_from_start.append(curr)
        curr = parent_start[curr]
    
    # Reverse it, because we traced backward!
    path_from_start.reverse()
    
    # 2. Trace backward from Collision to Target
    path_to_target = []
    # We must skip the collision_node itself, otherwise it will appear TWICE 
    # in the final stitched array!
    curr = parent_target[collision_node]
    while curr is not None:
        path_to_target.append(curr)
        curr = parent_target[curr]
        
    # Do NOT reverse this half! By walking backward from the collision to the 
    # target, the path is ALREADY facing the correct forward direction relative 
    # to the start node!
    
    # Stitch them together!
    return path_from_start + path_to_target


def bi_directional_path(graph: Dict[int, List[int]], start: int, target: int) -> Optional[List[int]]:
    if start == target:
        return [start]
        
    q_start = deque([start])
    q_target = deque([target])
    
    # The dictionaries act as both the `visited` set AND the `parent` tracker!
    # Key: Node -> Value: Its Parent
    parent_start = {start: None}
    parent_target = {target: None}
    
    while q_start and q_target:
        
        # --- 1. EXPAND START RIPPLE BY 1 LAYER ---
        for _ in range(len(q_start)):
            curr = q_start.popleft()
            for neighbor in graph.get(curr, []):
                # Did we just hit a node that the Target Ripple has already visited?
                if neighbor in parent_target:
                    # COLLISION! We link the final gap and reconstruct.
                    parent_start[neighbor] = curr
                    return reconstruct_path(parent_start, parent_target, neighbor)
                    
                if neighbor not in parent_start:
                    parent_start[neighbor] = curr
                    q_start.append(neighbor)
                    
        # --- 2. EXPAND TARGET RIPPLE BY 1 LAYER ---
        for _ in range(len(q_target)):
            curr = q_target.popleft()
            for neighbor in graph.get(curr, []):
                # Did we just hit a node that the Start Ripple has already visited?
                if neighbor in parent_start:
                    # COLLISION!
                    parent_target[neighbor] = curr
                    return reconstruct_path(parent_start, parent_target, neighbor)
                    
                if neighbor not in parent_target:
                    parent_target[neighbor] = curr
                    q_target.append(neighbor)
                    
    return None # Target not reachable


def demonstrate_bidir_path():
    section_header("Algorithm: Bi-Directional Path Reconstruction")
    
    # Let's create a long graph to watch them meet in the middle
    # 1 - 2 - 3 - 4 - 5 - 6 - 7 - 8
    graph = {
        1: [2],
        2: [1, 3],
        3: [2, 4],
        4: [3, 5],
        5: [4, 6],
        6: [5, 7],
        7: [6, 8],
        8: [7]
    }
    
    start = 1
    target = 8
    
    print(f"Graph is a straight line from 1 to 8.")
    print(f"Executing Bi-Directional BFS ({start} -> {target})...")
    
    path = bi_directional_path(graph, start, target)
    print(f"\nFinal Stitched Path: {path}")


# ==============================================================================
# 4. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why do we NOT reverse the `path_to_target` array during reconstruction?
   Answer: Let's trace it physically. The start is 1, target is 5. They collide at 3. The `parent_target` map recorded exactly how the target ripple spread OUTWARD from 5. So `parent_target[3] = 4`, and `parent_target[4] = 5`. When we reconstruct from the collision node 3, we loop: `curr = parent_target[3]` (which is 4), append 4. `curr = parent_target[4]` (which is 5), append 5. The resulting array is `[4, 5]`. This is ALREADY facing perfectly forward toward the target! If you reversed it, you would break the path.

2. Does Bi-Directional BFS work on Directed Graphs?
   Answer: Yes, BUT you must have access to the "Reverse Graph" (or be able to calculate reverse edges dynamically). Because the Target Ripple is spreading backward, it must physically travel against the arrows of the directed graph to successfully collide with the forward-moving Start Ripple!

3. When does Bi-Directional Search perform poorly?
   Answer: If you know the Start Node, but you do NOT have a specific Target Node! (e.g. "Find the nearest hospital"). Standard BFS is perfect for this: just expand outward until you hit ANY node labeled 'hospital'. Bi-directional search strictly requires you to know the exact identity of the target node in advance so you can launch the second ripple from it.
"""

if __name__ == "__main__":
    demonstrate_bidir_path()
    print("\n[SUCCESS] Laboratory: Bi-Directional Path Reconstruction Completed.")
