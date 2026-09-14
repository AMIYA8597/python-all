"""
# ==============================================================================
# LABORATORY: COMPETITIVE PROGRAMMING (CENTROID DECOMPOSITION)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You are given a Tree with 100,000 nodes.
# You are asked: "How many paths in this Tree have exactly length K?"
#
# If you run a DFS from every single node, it takes O(N^2) time. (TLE).
# If you use Heavy-Light Decomposition, it doesn't help because HLD optimizes 
# queries on *specific* paths, not *all* paths.
#
# You must use Centroid Decomposition. 
# A "Centroid" is a magical node in a Tree. If you delete the Centroid, the 
# Tree mathematically shatters into smaller independent subtrees, and none of 
# those subtrees will have a size greater than N/2!
#
# By finding the Centroid, counting all paths that physically pass THROUGH the 
# Centroid, and then recursively deleting the Centroid and repeating the process 
# on the shattered subtrees, you can mathematically process EVERY SINGLE PATH in 
# the entire Tree in exactly O(N log N) time!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master finding the Mathematical Centroid of a Tree.
# - Understand the recursive Divide & Conquer architecture of Centroid Decomposition.
# - Count all paths of length K.
#
# ==============================================================================
"""

import sys
from collections import defaultdict

# Increase recursion depth for massive trees
sys.setrecursionlimit(200000)

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. CENTROID DECOMPOSITION (DIVIDE & CONQUER ON TREES)
# ==============================================================================
class CentroidDecomposition:
    def __init__(self, n: int, edges: list[tuple[int, int]]):
        self.n = n
        self.graph = [[] for _ in range(n)]
        for u, v in edges:
            self.graph[u].append(v)
            self.graph[v].append(u)
            
        self.subtree_size = [0] * n
        # Marks nodes that have been physically "deleted" from the tree during recursion.
        self.is_deleted = [False] * n 
        
        self.total_paths_k = 0
        
    def _dfs_subtree_size(self, node: int, parent: int) -> int:
        """Calculates subtree sizes, explicitly ignoring deleted nodes."""
        self.subtree_size[node] = 1
        for neighbor in self.graph[node]:
            if neighbor != parent and not self.is_deleted[neighbor]:
                self.subtree_size[node] += self._dfs_subtree_size(neighbor, node)
        return self.subtree_size[node]

    def _get_centroid(self, node: int, parent: int, total_nodes: int) -> int:
        """
        Mathematical proof: A node is the Centroid if and only if NO child subtree 
        has a size strictly greater than Total_Nodes / 2.
        """
        for neighbor in self.graph[node]:
            if neighbor != parent and not self.is_deleted[neighbor]:
                if self.subtree_size[neighbor] > total_nodes // 2:
                    # The mathematical bulk of the tree is deeper in this direction!
                    # Move towards the bulk to find the true center of gravity.
                    return self._get_centroid(neighbor, node, total_nodes)
        # If we reach here, no child dominates. We are standing on the Centroid!
        return node

    def _get_distances(self, node: int, parent: int, current_dist: int, dist_map: dict) -> None:
        """DFS to collect all distances from the Centroid into the current subtree."""
        dist_map[current_dist] += 1
        for neighbor in self.graph[node]:
            if neighbor != parent and not self.is_deleted[neighbor]:
                self._get_distances(neighbor, node, current_dist + 1, dist_map)

    def solve_paths_of_length_k(self, start_node: int, k: int) -> None:
        """
        The Main Recursive Function.
        """
        # 1. Recalculate sizes for the CURRENT shattered component
        total_nodes = self._dfs_subtree_size(start_node, -1)
        
        # 2. Find the true Center of Gravity (Centroid) of this component
        centroid = self._get_centroid(start_node, -1, total_nodes)
        
        # 3. Process all paths that physically pass THROUGH this Centroid!
        # global_dist_map tracks all distances seen so far across previously processed branches.
        global_dist_map = defaultdict(int)
        global_dist_map[0] = 1 # The Centroid itself is at distance 0
        
        for neighbor in self.graph[centroid]:
            if not self.is_deleted[neighbor]:
                # Get all distances purely within this specific neighbor's branch
                local_dist_map = defaultdict(int)
                self._get_distances(neighbor, centroid, 1, local_dist_map)
                
                # Math: If we have a node in this branch at distance `d`, we desperately 
                # need a node from a PREVIOUS branch at distance `K - d` to complete the path!
                for d, count in local_dist_map.items():
                    if k - d in global_dist_map:
                        self.total_paths_k += count * global_dist_map[k - d]
                        
                # Merge this branch's data into the global tracker for the next branches to use
                for d, count in local_dist_map.items():
                    global_dist_map[d] += count
                    
        # 4. Physically DELETE the Centroid from reality!
        # This mathematically shatters the tree into smaller independent subtrees.
        self.is_deleted[centroid] = True
        
        # 5. Recursively conquer the shattered subtrees!
        for neighbor in self.graph[centroid]:
            if not self.is_deleted[neighbor]:
                self.solve_paths_of_length_k(neighbor, k)

def demonstrate_centroid():
    section_header("Centroid Decomposition (Paths of Length K)")
    
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
    k = 3
    
    print(f"Tree Nodes: {n}")
    print(f"Target Path Length (K): {k}")
    
    cd = CentroidDecomposition(n, edges)
    cd.solve_paths_of_length_k(0, k)
    
    print(f"\nTotal paths of exactly length {k} found: {cd.total_paths_k}")
    print("Why? The paths of length 3 are:")
    print("1. [5 -> 3 -> 1 -> 0]")
    print("2. [5 -> 3 -> 1 -> 4]")
    print("3. [3 -> 1 -> 0 -> 2]")
    print("4. [4 -> 1 -> 0 -> 2]")
    print("The O(N log N) algorithm elegantly processed all valid paths without overlapping!")


def run_all_labs():
    demonstrate_centroid()


# ==============================================================================
# 4. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. What is the strict mathematical definition of a Centroid in a Tree, and why is deleting it so powerful?
   Answer: A Centroid is a node that, if physically removed, shatters the tree into a forest of subtrees where *not a single resulting subtree* has a size strictly greater than $N/2$. Every tree is mathematically guaranteed to have at least one Centroid. Deleting the Centroid is incredibly powerful because it acts as a perfect Divide & Conquer mechanism. If every recursive step shrinks the tree size by at least half ($N \to N/2 \to N/4$), the maximum depth of the recursion tree is strictly bound to $\log_2(N)$. This guarantees the algorithm completes in $O(N \log N)$ time, preventing $O(N^2)$ worst-case line-graphs!

2. In the `_get_centroid` function, explain the logic `if subtree_size[neighbor] > total_nodes // 2`. Why does this guarantee finding the Centroid?
   Answer: Imagine holding the tree by a random node. If one of its branches contains $70\%$ of the total nodes, you are clearly not holding the tree by its center of mass! That massive branch will violate the $\le N/2$ rule if you delete your current node. To fix this, you must physically move *towards* the massive branch. You step down into that neighbor. You re-evaluate. You keep stepping towards the "heaviest" branch. Because the tree is finite, you will eventually reach a node where *none* of its branches contain more than $50\%$ of the nodes. At that exact moment, you have found the physical center of gravity.

3. When calculating paths that pass through the Centroid, why do we maintain a `local_dist_map` for the current branch and check it against the `global_dist_map` BEFORE merging them?
   Answer: To prevent mathematically illegal "V-shaped" paths within the SAME branch! A valid path through the Centroid MUST start in one branch, hit the Centroid, and exit through a COMPLETELY DIFFERENT branch. If you merged all branches into the `global_dist_map` simultaneously, a node at distance 1 in Branch A might pair with a node at distance 2 in Branch A, claiming it found a path of length 3. But that path doesn't actually cross the Centroid properly; it folds back on itself! By keeping the current branch `local`, checking it against the `global` history of *previously processed* branches, and only merging it *afterward*, we mathematically guarantee that all matched pairs span across two completely independent subtrees.
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Advanced Topics (Centroid Decomposition) Completed.")
