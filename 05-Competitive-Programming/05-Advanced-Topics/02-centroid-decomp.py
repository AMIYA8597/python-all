\"\"\"
Module: Centroid Decomposition
==============================
Why it exists:
Centroid Decomposition is a divide-and-conquer strategy on trees. It transforms a tree 
of `N` nodes and height `O(N)` into a "Centroid Tree" of height strictly `O(log N)`. 

Industry Use Cases:
Widely used to solve complex path problems (e.g., number of paths of length K, paths 
with weight W) efficiently in O(N log N) time, rather than O(N^2). Similar divide-and-conquer 
paradigms are used in big data processing (splitting tasks based on balanced partitions).

Learning Objectives:
1. Understand the definition of a Centroid.
2. Implement an algorithm to find the Centroid of a tree (or a sub-tree).
3. Recursively build the Centroid Tree.
4. Appreciate the O(log N) height property.

Concept Explanation:
--------------------
1. **Centroid**: A node in a tree such that if we remove it, no resulting connected 
   component has size greater than N/2. 
2. **Finding a Centroid**: Pick an arbitrary root, run DFS to find subtree sizes. 
   Start at the root; move to the heavy child (size > N/2). When no child has size > N/2, 
   the current node is the centroid.
3. **Decomposition**: Remove the centroid, effectively splitting the tree into a forest. 
   Recursively find centroids of the trees in this forest, making the newly found centroids 
   children of the previous centroid in the "Centroid Tree".
   
Time Complexity: 
- Building the centroid tree: O(N log N)
\"\"\"

from typing import List, Tuple

class CentroidDecomposition:
    def __init__(self, n: int, adj: List[List[int]]):
        self.n = n
        self.adj = adj
        
        self.sz = [0] * n
        self.is_removed = [False] * n
        
        # Parent array for the Centroid Tree
        self.centroid_parent = [-1] * n
        
        self._build(0, -1)

    def _get_sizes(self, v: int, p: int) -> int:
        self.sz[v] = 1
        for u in self.adj[v]:
            if u != p and not self.is_removed[u]:
                self.sz[v] += self._get_sizes(u, v)
        return self.sz[v]

    def _get_centroid(self, v: int, p: int, total_nodes: int) -> int:
        for u in self.adj[v]:
            if u != p and not self.is_removed[u]:
                if self.sz[u] > total_nodes // 2:
                    return self._get_centroid(u, v, total_nodes)
        return v

    def _build(self, v: int, p: int):
        total_nodes = self._get_sizes(v, -1)
        centroid = self._get_centroid(v, -1, total_nodes)
        
        self.centroid_parent[centroid] = p
        self.is_removed[centroid] = True
        
        for u in self.adj[centroid]:
            if not self.is_removed[u]:
                self._build(u, centroid)

    def get_centroid_tree(self) -> List[int]:
        \"\"\"
        Returns an array where array[i] is the parent of node i in the centroid tree.
        The root of the centroid tree has parent -1.
        \"\"\"
        return self.centroid_parent

# ---------------------------------------------------------
# Example Usage and Tests
# ---------------------------------------------------------
def main():
    # Tree (a line graph 0-1-2-3-4)
    # Centroid of whole tree is 2. 
    # Remaining: {0,1} and {3,4}
    # Centroid of {0,1} is 1 (or 0). 
    # Centroid of {3,4} is 3 (or 4).
    adj = [[1], [0, 2], [1, 3], [2, 4], [3]]
    n = 5
    
    cd = CentroidDecomposition(n, adj)
    parents = cd.get_centroid_tree()
    
    # Assert root of centroid tree is node 2
    assert parents[2] == -1, "Centroid of the path graph should be 2"
    
    # Verify tree constraints
    for i in range(n):
        if i != 2:
            assert parents[i] != -1
            
    print("Centroid Decomposition parents:", parents)
    print("Centroid Decomposition Tests Passed!")

if __name__ == "__main__":
    main()

\"\"\"
Interview Challenge:
--------------------
Q: Given a tree where each node has a letter, how would you find the number of paths 
that form a palindrome? 
A: Using Centroid Decomposition! For a centroid, we find all paths starting from it 
into its subtrees. We can keep track of letter parities (bitmasks). A path through 
the centroid forms a palindrome if the XOR of bitmasks is 0 (all even frequencies) 
or has exactly one bit set (one odd frequency). We process each subtree, counting 
matches with previously processed subtrees, then add the current subtree's paths 
to our frequency map. This takes O(N log N) overall.
\"\"\"
