"""
## A. Concept Name
Link-Cut Trees

## B. Concept Explanation
Link-Cut Trees maintain a forest of trees dynamically, supporting edge insertions (Link) 
and deletions (Cut) as well as path queries (like finding the root) in O(log N) amortized time.
Each tree is partitioned into vertex-disjoint paths (similar to Heavy-Light Decomposition), 
where each path is represented as a Splay Tree ordered by depth. Operations manipulate 
these auxiliary Splay Trees to restructure the overall forest.

## C. Conceptual Model
Imagine a forest of trees where paths from the root to leaves are separated into "heavy" and "light" edges.
The Link-Cut Tree groups nodes on a "preferred path" into a Splay Tree, keyed by their depth in the original tree.
Changing the preferred path (via the `access` operation) splits and merges these Splay Trees, 
allowing dynamic graph connectivity.

## D. Time and Space Complexity
- Time Complexity: Amortized O(log N) for Link, Cut, and Path Queries.
- Space Complexity: O(N) for N nodes, as each node requires a constant number of pointers.

## E. Edge Cases and Failure Modes
- Recognizing roots of auxiliary trees effectively detaches heavy paths logically without losing connectivity.
- Splaying up through the auxiliary trees accurately reconstructs paths using the `access` primitive.
- A node must verify it is the true root of its auxiliary tree by checking if its parent links back to it.

## F. Real-World Applications
- Network flow algorithms (e.g., dynamic trees in maximum flow algorithms).
- Maintaining dynamic connectivity in graphs.
- Dynamic Minimum Spanning Tree (MST) maintenance.

## G. Learning Objectives
1. Understand the purpose of dynamic trees for handling changing forests.
2. Implement Access, Link, and Cut operations.
3. Utilize Splay Trees as the underlying auxiliary data structure to represent paths.

## H. Interview Challenge
Q: What is the primary difference between Heavy-Light Decomposition and Link-Cut Trees?
A: HLD operates on a static tree structure; edges cannot be added or removed after initialization, 
   which makes segment tree overlays possible. Link-Cut Trees, however, maintain dynamic forests 
   where tree edges can be 'cut' or 'linked' efficiently, using self-adjusting Splay Trees to manage paths.

## I. Pythonic Implementation Details
- Uses `Optional` for type hinting node references.
- Leverages boolean evaluation `not bool(...)` for root checking.
- Clean separation of the Node class and the Tree manager class.

## X. Project Connection
These dynamic trees can be integrated into larger projects requiring real-time graph 
connectivity updates, such as network simulation tools or interactive graph visualization applications.
"""

from typing import Optional

class LCTNode:
    def __init__(self, key: int):
        self.key = key
        self.left: Optional['LCTNode'] = None
        self.right: Optional['LCTNode'] = None
        self.parent: Optional['LCTNode'] = None

    def is_root(self) -> bool:
        """ A node is root of its auxiliary tree if its parent doesn't point back to it """
        return not bool(self.parent and (self.parent.left == self or self.parent.right == self))

class LinkCutTree:
    def _rotate(self, x: LCTNode) -> None:
        p = x.parent
        g = p.parent
        is_left = (p.left == x)
        
        if not p.is_root():
            if g.left == p:
                g.left = x
            else:
                g.right = x
        x.parent = g
        
        if is_left:
            p.left = x.right
            if x.right:
                x.right.parent = p
            x.right = p
        else:
            p.right = x.left
            if x.left:
                x.left.parent = p
            x.left = p
        p.parent = x

    def _splay(self, x: LCTNode) -> None:
        while not x.is_root():
            p = x.parent
            g = p.parent
            if not p.is_root():
                if (p.left == x) == (g.left == p):
                    self._rotate(p)  # Zig-Zig
                else:
                    self._rotate(x)  # Zig-Zag
            self._rotate(x)

    def access(self, x: LCTNode) -> None:
        """
        Creates a path from the root of the represented tree to x.
        x becomes the root of the auxiliary Splay tree, and it will have no right child
        (meaning it is the deepest node in this path).
        """
        self._splay(x)
        x.right = None  # Disconnect anything deeper than x
        
        # Continue up the tree
        y = x
        while y.parent:
            p = y.parent
            self._splay(p)
            p.right = y # Connect the path
            y = p
            
        self._splay(x) # Bring x back to the root of the aux tree

    def find_root(self, x: LCTNode) -> LCTNode:
        """
        Finds the root of the represented tree containing x.
        """
        self.access(x)
        curr = x
        while curr.left:
            curr = curr.left
        self._splay(curr)
        return curr

    def link(self, x: LCTNode, y: LCTNode) -> None:
        """
        Makes x a child of y. Assumes x is a root of its represented tree.
        """
        self.access(x)
        self.access(y)
        x.left = y
        y.parent = x

    def cut(self, x: LCTNode) -> None:
        """
        Cuts the edge between x and its parent in the represented tree.
        """
        self.access(x)
        if x.left:
            x.left.parent = None
            x.left = None

def test_lct():
    print("--- Link-Cut Tree Operations ---")
    nodes = [LCTNode(i) for i in range(5)]
    lct = LinkCutTree()
    
    # 0 is root, 1 child of 0, 2 child of 1
    # 3 is standalone
    print("Linking 1 -> 0 and 2 -> 1...")
    lct.link(nodes[1], nodes[0])
    lct.link(nodes[2], nodes[1])
    
    root_of_2 = lct.find_root(nodes[2])
    print(f"Root of node 2 is: {root_of_2.key} (Expected 0)")
    
    root_of_3 = lct.find_root(nodes[3])
    print(f"Root of node 3 is: {root_of_3.key} (Expected 3)")
    
    print("\nCutting edge above node 1 (separating 1 and 2 from 0)...")
    lct.cut(nodes[1])
    
    root_of_2_new = lct.find_root(nodes[2])
    print(f"Root of node 2 after cut is: {root_of_2_new.key} (Expected 1)")
    
    print("\nLinking 1 -> 3...")
    lct.link(nodes[1], nodes[3])
    root_of_2_final = lct.find_root(nodes[2])
    print(f"Root of node 2 after linking to 3 is: {root_of_2_final.key} (Expected 3)")

if __name__ == "__main__":
    test_lct()
