"""
## A. Concept Name
Heavy-Light Decomposition (HLD)

## B. Learning Objectives
1. Understand how to break down a tree into paths for efficient querying.
2. Implement depth and subtree size calculations.
3. Build the Heavy-Light chain structure.
4. Execute path queries in O(log^2 N) time using a Segment Tree on the flattened tree.

## C. Concept Explanation
Heavy-Light Decomposition splits a tree into a set of disjoint paths. For any node, the edge 
to the child with the largest subtree is a "heavy" edge. All other edges are "light" edges. 
Paths formed by heavy edges are continuous. By laying out these heavy paths consecutively in 
an array, we can use a Segment Tree to query values along any path in the tree. 
Any path between two nodes u and v will span at most O(log N) light edges, resulting in 
O(log^2 N) overall path query time.

## D. Performance Analysis
- Time Complexity: O(N) for preprocessing, O(log^2 N) per path query/update.
- Space Complexity: O(N) for tree, HLD metadata, and Segment Tree.

## X. Project Connection
HLD is highly useful in networking for efficient routing, querying tree-shaped topologies, and updating node values (like server loads) dynamically. It allows for extremely fast path aggregation queries in distributed systems.
"""

from typing import List, Dict

class SegmentTree:
    def __init__(self, size: int):
        self.n = size
        self.tree = [0] * (2 * self.n)

    def build(self, arr: List[int]):
        for i in range(self.n):
            self.tree[self.n + i] = arr[i]
        for i in range(self.n - 1, 0, -1):
            self.tree[i] = self.tree[i * 2] + self.tree[i * 2 + 1]

    def update(self, pos: int, value: int):
        pos += self.n
        self.tree[pos] = value
        pos //= 2
        while pos > 0:
            self.tree[pos] = self.tree[2 * pos] + self.tree[2 * pos + 1]
            pos //= 2

    def query(self, left: int, right: int) -> int:
        """ Queries sum in [left, right] """
        left += self.n
        right += self.n + 1
        res = 0
        while left < right:
            if left % 2 == 1:
                res += self.tree[left]
                left += 1
            if right % 2 == 1:
                right -= 1
                res += self.tree[right]
            left //= 2
            right //= 2
        return res


class HLD:
    def __init__(self, n: int, adj: List[List[int]], values: List[int]):
        self.n = n
        self.adj = adj
        self.values = values

        self.parent = [-1] * n
        self.depth = [0] * n
        self.heavy = [-1] * n
        self.head = [0] * n
        self.pos = [0] * n
        
        self.current_pos = 0

        # Subtree size
        def dfs(v: int, p: int = -1, d: int = 0) -> int:
            self.parent[v] = p
            self.depth[v] = d
            size = 1
            max_sub_size = 0
            
            for child in self.adj[v]:
                if child != p:
                    sub_size = dfs(child, v, d + 1)
                    size += sub_size
                    if sub_size > max_sub_size:
                        max_sub_size = sub_size
                        self.heavy[v] = child
            return size

        dfs(0)

        # Decompose
        def decompose(v: int, h: int, p: int = -1):
            self.head[v] = h
            self.pos[v] = self.current_pos
            self.current_pos += 1
            
            if self.heavy[v] != -1:
                decompose(self.heavy[v], h, v)
                
            for child in self.adj[v]:
                if child != p and child != self.heavy[v]:
                    decompose(child, child, v)

        decompose(0, 0)
        
        # Build segment tree
        arr = [0] * n
        for i in range(n):
            arr[self.pos[i]] = self.values[i]
        
        self.seg_tree = SegmentTree(n)
        self.seg_tree.build(arr)

    def query_path(self, a: int, b: int) -> int:
        res = 0
        # While they are not on the same heavy path
        while self.head[a] != self.head[b]:
            if self.depth[self.head[a]] > self.depth[self.head[b]]:
                a, b = b, a
            
            # Now head[b] is deeper, so we move b up
            res += self.seg_tree.query(self.pos[self.head[b]], self.pos[b])
            b = self.parent[self.head[b]]

        if self.depth[a] > self.depth[b]:
            a, b = b, a
            
        res += self.seg_tree.query(self.pos[a], self.pos[b])
        return res

    def update_node(self, node: int, value: int):
        self.seg_tree.update(self.pos[node], value)


# ==========================================
# Edge Cases & Interview Challenge
# ==========================================
"""
Edge Cases Handled:
- Queries properly swap endpoints based on chain head depths to climb up the tree systematically.
- Leaves correctly terminate recursion.
- Root node (0-indexed) is handled efficiently.

Interview Challenge:
Q: Why does Heavy-Light Decomposition guarantee O(log^2 N) time per query?
A: In any path from a node to the root, a light edge always transitions to a subtree that is at 
   most half the size of the parent's subtree. Therefore, any path can traverse at most log(N) 
   light edges. Between these light edges are heavy paths. Each heavy path can be queried in 
   O(log N) time using a Segment Tree, yielding an overall bound of O(log^2 N).
"""

def test_hld():
    print("--- Heavy-Light Decomposition ---")
    n = 5
    # Tree structure:
    #     0
    #    / \
    #   1   2
    #  / \
    # 3   4
    adj = [[1, 2], [0, 3, 4], [0], [1], [1]]
    values = [10, 20, 30, 40, 50]
    
    hld = HLD(n, adj, values)
    
    print(f"Initial Values: {values}")
    
    # Path from 3 to 2 passes through 3 -> 1 -> 0 -> 2 
    # Sum = 40 + 20 + 10 + 30 = 100
    res = hld.query_path(3, 2)
    print(f"Query Path(3, 2): {res} (Expected 100)")
    
    # Update node 1 from 20 to 100
    print("\nUpdating Node 1 from 20 to 100")
    hld.update_node(1, 100)
    
    # New sum = 40 + 100 + 10 + 30 = 180
    res = hld.query_path(3, 2)
    print(f"Query Path(3, 2): {res} (Expected 180)")

if __name__ == "__main__":
    test_hld()
