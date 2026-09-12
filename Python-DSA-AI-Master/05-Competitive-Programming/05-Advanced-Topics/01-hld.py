\"\"\"
Module: Heavy-Light Decomposition (HLD)
=======================================
Why it exists:
Heavy-Light Decomposition is a powerful technique for tree data structures. It maps 
the nodes of a tree to a 1D array such that any path between two nodes `u` and `v` 
can be decomposed into O(log N) contiguous segments. 

Industry Use Cases:
Used in network routing topologies, database query optimizations on hierarchical data, 
and extensively in Competitive Programming to answer path queries (like max edge on 
a path, sum of nodes on a path) in O(log^2 N) time.

Learning Objectives:
1. Understand the concept of "heavy" vs "light" edges.
2. Implement DFS to calculate subtree sizes.
3. Build the HLD chains and map them to a Segment Tree (or Fenwick Tree).
4. Perform path queries efficiently.

Concept Explanation:
--------------------
1. **Size of Subtree**: For each node, calculate the number of nodes in its subtree.
2. **Heavy Edge**: For a node `u`, the edge to a child `v` is "heavy" if `size(v) > size(u)/2`. 
   Every node has at most one heavy child. All other edges are "light".
3. **Chains**: Heavy edges form continuous paths or "chains". The path between any two nodes 
   in the tree will traverse at most O(log N) light edges and hence O(log N) heavy chains.
4. **Segment Tree**: Flatten the tree so that each chain occupies a contiguous subarray. 
   We can then use a Segment Tree to query/update paths efficiently.

Time Complexity:
- Preprocessing: O(N)
- Path Query/Update: O(log^2 N)
\"\"\"

from typing import List, Callable

class SegmentTree:
    \"\"\"
    A simple Segment Tree for Point Update and Range Max Query.
    \"\"\"
    def __init__(self, size: int):
        self.size = size
        self.tree = [0] * (2 * size)

    def update(self, pos: int, value: int):
        pos += self.size
        self.tree[pos] = value
        pos //= 2
        while pos > 0:
            self.tree[pos] = max(self.tree[2 * pos], self.tree[2 * pos + 1])
            pos //= 2

    def query(self, left: int, right: int) -> int:
        left += self.size
        right += self.size
        res = -float('inf')
        while left <= right:
            if left % 2 == 1:
                res = max(res, self.tree[left])
                left += 1
            if right % 2 == 0:
                res = max(res, self.tree[right])
                right -= 1
            left //= 2
            right //= 2
        return res

class HLD:
    def __init__(self, n: int, adj: List[List[int]]):
        self.n = n
        self.adj = adj
        
        self.parent = [-1] * n
        self.depth = [0] * n
        self.heavy = [-1] * n
        self.head = [-1] * n
        self.pos = [0] * n
        self.current_pos = 0
        
        self.seg_tree = SegmentTree(n)
        
        # Build sizes and heavy edges
        self._dfs(0)
        # Build chains and positions
        self._decompose(0, 0)

    def _dfs(self, v: int) -> int:
        size = 1
        max_sub_size = 0
        
        for u in self.adj[v]:
            if u != self.parent[v]:
                self.parent[u] = v
                self.depth[u] = self.depth[v] + 1
                
                sub_size = self._dfs(u)
                size += sub_size
                
                if sub_size > max_sub_size:
                    max_sub_size = sub_size
                    self.heavy[v] = u
                    
        return size

    def _decompose(self, v: int, h: int):
        self.head[v] = h
        self.pos[v] = self.current_pos
        self.current_pos += 1
        
        if self.heavy[v] != -1:
            self._decompose(self.heavy[v], h)
            
        for u in self.adj[v]:
            if u != self.parent[v] and u != self.heavy[v]:
                self._decompose(u, u)

    def update(self, u: int, val: int):
        \"\"\"Update node u's value.\"\"\"
        self.seg_tree.update(self.pos[u], val)

    def query(self, u: int, v: int) -> int:
        \"\"\"Query max value on path between u and v.\"\"\"
        res = -float('inf')
        while self.head[u] != self.head[v]:
            if self.depth[self.head[u]] > self.depth[self.head[v]]:
                u, v = v, u
            # Now head[v] is deeper
            res = max(res, self.seg_tree.query(self.pos[self.head[v]], self.pos[v]))
            v = self.parent[self.head[v]]
            
        if self.depth[u] > self.depth[v]:
            u, v = v, u
        res = max(res, self.seg_tree.query(self.pos[u], self.pos[v]))
        return res

# ---------------------------------------------------------
# Example Usage and Tests
# ---------------------------------------------------------
def main():
    # Tree:
    #     0
    #    / \
    #   1   2
    #  / \
    # 3   4
    adj = [[1, 2], [0, 3, 4], [0], [1], [1]]
    hld = HLD(5, adj)
    
    # Values: Node 0: 10, Node 1: 5, Node 2: 20, Node 3: 15, Node 4: 25
    hld.update(0, 10)
    hld.update(1, 5)
    hld.update(2, 20)
    hld.update(3, 15)
    hld.update(4, 25)
    
    # Path 3 to 2: 3 -> 1 -> 0 -> 2
    # Values: 15, 5, 10, 20. Max is 20
    assert hld.query(3, 2) == 20
    
    # Path 3 to 4: 3 -> 1 -> 4
    # Values: 15, 5, 25. Max is 25
    assert hld.query(3, 4) == 25
    
    print("HLD Tests Passed!")

if __name__ == "__main__":
    main()

\"\"\"
Interview Challenge:
--------------------
Q: How does HLD handle Edge Queries instead of Node Queries?
A: For edge updates/queries, we map each edge to its deeper node. So the edge (u, v) 
is stored at the node which has the larger depth. When querying a path (u, v), 
we find the LCA(u, v) and query the paths from u to LCA and v to LCA, but we exclude 
the LCA itself from the segment tree query since the LCA represents an edge above it 
which is not part of the (u, v) path.
\"\"\"
