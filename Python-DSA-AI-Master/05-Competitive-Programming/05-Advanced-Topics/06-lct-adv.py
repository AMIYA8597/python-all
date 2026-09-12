\"\"\"
Module: Link/Cut Tree (Advanced Data Structure)
Why it exists: A Link/Cut tree maintains a forest of nodes subject to operations like linking two trees, cutting an edge, and querying properties (like max, sum, or path connectivity) on the path between any two nodes.
Industry Use Cases:
- Dynamic graph connectivity problems.
- Maintaining network flow and maximum capacity dynamically.
- Network routing and dynamic connectivity logging.

Learning Objectives:
1. Understand the core concept of heavy-light decomposition conceptually, adapted dynamically via Splay Trees.
2. Master the core operations of Link/Cut Trees: access, make_root, link, cut.
3. Understand how Splay trees act as the underlying auxiliary trees.

Beginner Explanation:
Imagine a forest of trees where edges are constantly being added and removed. We want to know the sum of values on a path between two nodes. Doing this naively takes O(N) per query. A Link-Cut Tree allows us to do this in O(log N) amortized time by representing paths as binary search trees (Splay Trees) based on their depth.

Advanced Explanation:
A Link/Cut Tree decomposes a tree into a set of vertex-disjoint paths. Each path is represented by a Splay Tree, keyed by depth in the original tree. The root of each Splay Tree has a `path_parent` pointer to the node strictly above the highest node in its path.
The fundamental operation `access(v)` rearranges the tree such that `v` and the root of the represented tree are in the same Splay Tree (same path), and `v` is the deepest node in that path (no right child).

Performance Considerations:
- Amortized Time Complexity: O(log N) for all operations.
- Space Complexity: O(N) to store the nodes.
- High constant factor due to splaying operations.
\"\"\"
from typing import Optional, List

class Node:
    def __init__(self, key: int, val: int = 0):
        self.key = key
        self.val = val
        self.sum = val
        self.left: Optional['Node'] = None
        self.right: Optional['Node'] = None
        self.parent: Optional['Node'] = None
        self.rev = False  # For reversing paths (make_root)

    def is_root(self) -> bool:
        # A node is the root of its splay tree if it's not the left or right child of its parent
        return not self.parent or (self.parent.left is not self and self.parent.right is not self)

class LinkCutTree:
    \"\"\"
    Professional Implementation of Link/Cut Tree maintaining path sums.
    \"\"\"
    def __init__(self, size: int):
        # 1-indexed nodes
        self.nodes = [Node(i) for i in range(size + 1)]

    def _push_up(self, x: Node) -> None:
        if x:
            x.sum = x.val
            if x.left:
                x.sum += x.left.sum
            if x.right:
                x.sum += x.right.sum

    def _push_down(self, x: Node) -> None:
        if x and x.rev:
            x.left, x.right = x.right, x.left
            if x.left:
                x.left.rev ^= True
            if x.right:
                x.right.rev ^= True
            x.rev = False

    def _rotate(self, x: Node) -> None:
        y = x.parent
        z = y.parent
        if not y.is_root():
            if z.left is y:
                z.left = x
            else:
                z.right = x
        x.parent = z

        self._push_down(y)
        self._push_down(x)

        if y.left is x:
            y.left = x.right
            if x.right:
                x.right.parent = y
            x.right = y
        else:
            y.right = x.left
            if x.left:
                x.left.parent = y
            x.left = y
        y.parent = x
        self._push_up(y)
        self._push_up(x)

    def _splay(self, x: Node) -> None:
        # Push down all ancestors first
        def push_all(node: Node):
            if not node.is_root():
                push_all(node.parent)
            self._push_down(node)
        
        push_all(x)
        while not x.is_root():
            y = x.parent
            z = y.parent
            if not y.is_root():
                if (y.left is x) == (z.left is y):
                    self._rotate(y)
                else:
                    self._rotate(x)
            self._rotate(x)
        self._push_up(x)

    def access(self, x_id: int) -> None:
        x = self.nodes[x_id]
        y = None
        curr = x
        while curr:
            self._splay(curr)
            curr.right = y
            self._push_up(curr)
            y = curr
            curr = curr.parent
        self._splay(x)

    def make_root(self, x_id: int) -> None:
        self.access(x_id)
        x = self.nodes[x_id]
        x.rev ^= True
        self._push_down(x)

    def find_root(self, x_id: int) -> int:
        self.access(x_id)
        x = self.nodes[x_id]
        self._push_down(x)
        while x.left:
            x = x.left
            self._push_down(x)
        self._splay(x)
        return x.key

    def link(self, x_id: int, y_id: int) -> None:
        if self.find_root(x_id) == self.find_root(y_id):
            return  # Already connected
        self.make_root(x_id)
        x = self.nodes[x_id]
        y = self.nodes[y_id]
        x.parent = y

    def cut(self, x_id: int, y_id: int) -> None:
        self.make_root(x_id)
        self.access(y_id)
        y = self.nodes[y_id]
        if y.left is self.nodes[x_id] and self.nodes[x_id].right is None:
            y.left.parent = None
            y.left = None
            self._push_up(y)

    def set_val(self, x_id: int, val: int) -> None:
        self.access(x_id)
        x = self.nodes[x_id]
        x.val = val
        self._push_up(x)

    def query_path(self, x_id: int, y_id: int) -> int:
        self.make_root(x_id)
        self.access(y_id)
        return self.nodes[y_id].sum


if __name__ == '__main__':
    print(\"--- Advanced Link/Cut Tree --- \")
    lct = LinkCutTree(5)
    
    # Initial values: node i has value i
    for i in range(1, 6):
        lct.set_val(i, i)
        
    # Link some nodes to form a tree:
    # 1 - 2 - 4
    #  \\
    #   3 - 5
    lct.link(1, 2)
    lct.link(1, 3)
    lct.link(2, 4)
    lct.link(3, 5)
    
    # Path sum from 4 to 5 should be: val(4) + val(2) + val(1) + val(3) + val(5) = 4 + 2 + 1 + 3 + 5 = 15
    assert lct.query_path(4, 5) == 15, \"Test Failed: Path sum 4 to 5\"
    
    # Cut 1-3, Link 2-3
    lct.cut(1, 3)
    lct.link(2, 3)
    
    # Now tree is 1 - 2 - 4
    #                 |
    #                 3 - 5
    # Path sum from 4 to 5 should be: val(4) + val(2) + val(3) + val(5) = 4 + 2 + 3 + 5 = 14
    assert lct.query_path(4, 5) == 14, \"Test Failed: Path sum after cut/link\"
    
    print(\"All Link/Cut Tree assertions passed!\")

\"\"\"
Interview Challenge:
Question: Given a dynamic forest, support operations to add an edge, remove an edge, and check if two vertices are in the same tree.
Solution: Link/Cut Tree is perfect for this. `find_root(u) == find_root(v)` checks connectivity in O(log N) time.
\"\"\"
