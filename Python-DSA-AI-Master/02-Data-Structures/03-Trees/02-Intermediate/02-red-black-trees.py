"""
Red-Black Trees

## A. Concept Name
Red-Black Trees

## B. One-Sentence Definition
A Red-Black Tree is a self-balancing binary search tree where each node has a color (red or black) that is used to maintain an approximate balance, guaranteeing O(log n) operations.

## C. Why Does This Exist?
While standard Binary Search Trees can degrade to O(n) time complexity and strictly balanced AVL trees require frequent and computationally expensive rotations, Red-Black Trees provide a "good enough" balance that keeps operations at O(log n) while minimizing the overhead of restructuring the tree during insertions and deletions.

## D. Intuition
Think of a Red-Black tree as a way to simulate a 2-3-4 tree using a standard binary search tree structure. By coloring some links "red", we effectively bind a child node to its parent, creating a larger "super-node" with multiple values. The coloring rules ensure that no path from the root to a leaf is more than twice as long as any other path, ensuring the tree remains relatively bushy.

## E. Real-Life Analogy
Imagine managing a growing company hierarchy. An AVL tree insists that every department has exactly the same number of management levels, which requires constant, disruptive reorganizations every time someone is hired or fired. A Red-Black Tree, on the other hand, allows some departments to have a slightly different number of management layers (red nodes represent "assistant managers" who don't add to the official chain of command length), as long as no department chain is more than twice as long as another. This provides a good balance between maintaining structure and reducing administrative overhead.

## F. Mental Model
1. Every node is either Red or Black.
2. The root is always Black.
3. All empty leaves (NIL nodes) are considered Black.
4. If a node is Red, both its children MUST be Black (no two Red nodes can be adjacent).
5. Every path from a given node to any of its descendant NIL nodes must contain the exact same number of Black nodes (the "Black Height").

## G. Visual Explanation
```text
      [55 (B)]
      /      \
 [40 (B)]   [65 (R)]
             /    \
       [60 (B)]  [75 (B)]
       /
  [57 (R)]
```
Notice how:
- The root (55) is Black.
- The Red node (65) has Black children (60 and 75).
- Every path from the root to a NIL leaf has the same number of Black nodes (e.g., 55 -> 40 -> NIL has 2 black nodes; 55 -> 65 -> 60 -> 57 -> NIL has 2 black nodes).

## H. Formal Explanation
A Red-Black Tree is a Binary Search Tree that satisfies the following red-black properties:
1. Every node is either red or black.
2. The root is black.
3. Every leaf (NIL) is black.
4. If a node is red, then both its children are black.
5. For each node, all simple paths from the node to descendant leaves contain the same number of black nodes.
These constraints enforce that the longest possible path (alternating red and black nodes) is no more than twice the length of the shortest possible path (all black nodes), thus keeping the tree roughly balanced.

## I. Mathematical Foundation
Let h be the height of the tree, n be the number of internal nodes, and bh(x) be the black-height of node x (number of black nodes on path from x to a leaf, not including x).
A sub-tree rooted at node x contains at least 2^(bh(x)) - 1 internal nodes.
Since the root r has a black-height of at least h/2 (due to the property that red nodes cannot have red children), we have:
n >= 2^(h/2) - 1
n + 1 >= 2^(h/2)
log2(n + 1) >= h/2
h <= 2 * log2(n + 1)
This proves that the height of a Red-Black Tree is O(log n).

## J. From-Scratch Implementation
(The implementation is provided below)

## K. Library / Production Implementation
Red-Black Trees are extremely common in standard libraries:
- C++: `std::map`, `std::set`, `std::multimap`, `std::multiset` are almost universally implemented using Red-Black Trees.
- Java: `java.util.TreeMap` and `java.util.TreeSet` use Red-Black Trees. The `HashMap` also uses Red-Black trees to handle hash collisions when buckets become too large.
- Linux Kernel: The Completely Fair Scheduler (CFS) uses a Red-Black Tree to schedule processes.

## L. Trace (walk through example)
Let's insert 57 into the visual tree above.
1. Insert 57 as a standard BST insertion. It lands as the left child of 60.
2. Newly inserted nodes are always Red.
3. 57 is Red. Its parent, 60, is Black.
4. Since the parent is Black, no Red-Black properties are violated (specifically, no two Red nodes are adjacent).
5. The insertion is complete with zero rotations or recoloring.

## M. Complexity
- Search: O(log n)
- Insert: O(log n) time, requires at most 2 rotations.
- Delete: O(log n) time, requires at most 3 rotations.
- Space: O(n) to store the nodes, plus O(log n) for the recursive call stack or parent pointers.

## N. Common Mistakes
- Forgetting to handle the "uncle" node's color. The color of a node's uncle dictates whether we recolor or rotate during insertion fix-up.
- Forgetting that the NIL sentinel leaves are Black. This is crucial for counting black-heights and checking the color of an empty child.
- Modifying the root and forgetting to paint it Black at the end of the insertion.

## O. Common Confusions
- **Why not just use AVL trees?** AVL trees are more rigidly balanced, which makes lookups slightly faster. However, this rigid balance means AVL trees require more frequent rotations during insertions and deletions. Red-Black trees trade slightly slower lookups for faster insertions/deletions.
- **Why is a new node always red?** Inserting a Red node doesn't change the black-height of any path, preserving property 5. It might violate property 4 (no adjacent reds), but that is easier to fix locally via rotations and recoloring.

## P. When To Use
- When you need a sorted map or set with guaranteed O(log n) worst-case time complexity for all operations.
- When your workload involves a mix of insertions, deletions, and lookups (where AVL trees might suffer from too many rotations).
- Real-time systems where worst-case guarantees are strictly required.

## Q. When NOT To Use
- If the data is static or built once and only queried. (A perfectly balanced BST, an array + binary search, or a Hash Map might be better).
- If you only need fast lookups by key and don't care about sorting/ordering (use a Hash Table - O(1)).
- If the dataset is small enough that the constant overhead of pointers and color bits outweighs the algorithmic benefits.

## R. Trade-offs
- **Lookups vs Insertions:** Slightly slower lookups than AVL trees, but faster insertions and deletions.
- **Memory vs Hash Table:** Uses more memory than a standard array or open-addressed hash table due to left, right, and parent pointers, plus the color bit.
- **Worst-case vs Average-case:** Provides O(log n) worst-case guarantees, unlike Hash Tables which have O(n) worst-case (though O(1) average).

## S. Debugging
- Print the tree and verify the 5 properties.
- Property 2: Is the root black?
- Property 4: Are there any red nodes with red children?
- Property 5: Is the black-height the same for all paths? A recursive function that returns the black height (or throws an error if mismatched) is a great debugging tool.

## T. Memory Hook
"Red nodes must be surrounded by Black nodes (parent and children). Black nodes ensure the tree's backbone is balanced." Think of it like a chain where every red link must be sandwiched between black links.

## U. Active Recall
1. What is the maximum height of a Red-Black Tree with n nodes?
2. What are the 5 properties of a Red-Black Tree?
3. During insertion, if the parent is red and the uncle is red, what is the fix?

## V. Practice
- Implement the `insert_fix` algorithm from memory.
- Implement the `delete` operation (much harder than insertion!).
- Draw the tree that results from inserting the numbers 1 through 10 in order.

## W. Interview Question
"Explain the differences between a Hash Table, an AVL Tree, and a Red-Black Tree. In what scenarios would you choose one over the others?"

## X. Project Connection
Build a custom in-memory database index. If you need range queries (e.g., "Find all users aged 20-30"), a hash table won't work, but a Red-Black Tree is perfect.
"""

from typing import Optional, List

class RBNode:
    def __init__(self, val: int):
        self.val: int = val
        self.parent: Optional['RBNode'] = None
        self.left: Optional['RBNode'] = None
        self.right: Optional['RBNode'] = None
        self.color: int = 1 # 1 = Red, 0 = Black

class RedBlackTree:
    """Basic/Intermediate Implementation of a Red-Black Tree."""
    def __init__(self):
        self.TNULL = RBNode(0)
        self.TNULL.color = 0
        self.root: RBNode = self.TNULL

    def left_rotate(self, x: RBNode):
        y = x.right
        x.right = y.left
        if y.left != self.TNULL:
            y.left.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def right_rotate(self, x: RBNode):
        y = x.left
        x.left = y.right
        if y.right != self.TNULL:
            y.right.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    def insert_fix(self, k: RBNode):
        while k.parent and k.parent.color == 1:
            if k.parent == k.parent.parent.right:
                u = k.parent.parent.left
                if u.color == 1:
                    u.color = 0
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    k = k.parent.parent
                else:
                    if k == k.parent.left:
                        k = k.parent
                        self.right_rotate(k)
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    self.left_rotate(k.parent.parent)
            else:
                u = k.parent.parent.right
                if u.color == 1:
                    u.color = 0
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    k = k.parent.parent
                else:
                    if k == k.parent.right:
                        k = k.parent
                        self.left_rotate(k)
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    self.right_rotate(k.parent.parent)
            if k == self.root:
                break
        self.root.color = 0

    def insert(self, key: int):
        node = RBNode(key)
        node.parent = None
        node.left = self.TNULL
        node.right = self.TNULL
        node.color = 1

        y = None
        x = self.root

        while x != self.TNULL:
            y = x
            if node.val < x.val:
                x = x.left
            else:
                x = x.right

        node.parent = y
        if y is None:
            self.root = node
        elif node.val < y.val:
            y.left = node
        else:
            y.right = node

        if node.parent is None:
            node.color = 0
            return

        if node.parent.parent is None:
            return

        self.insert_fix(node)

    def in_order_helper(self, node: RBNode, result: List[int]):
        if node != self.TNULL:
            self.in_order_helper(node.left, result)
            result.append(node.val)
            self.in_order_helper(node.right, result)

def test_rb_tree():
    rbt = RedBlackTree()
    for val in [55, 40, 65, 60, 75, 57]:
        rbt.insert(val)
    res = []
    rbt.in_order_helper(rbt.root, res)
    assert res == [40, 55, 57, 60, 65, 75]
    print("Red-Black Tree basic tests passed!")

if __name__ == "__main__":
    test_rb_tree()
