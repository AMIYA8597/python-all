"""
## A. Concept Name
AVL Tree

## B. One-Sentence Definition
A self-balancing binary search tree where the height difference between left and right child subtrees of any node is at most 1.

## C. Why Does This Exist?
Standard Binary Search Trees can degrade into linked lists (O(n) time) if elements are inserted in sorted order. AVL Trees were invented to guarantee O(log n) time complexity for search, insertion, and deletion by strictly maintaining balance.

## D. Intuition
Imagine hanging weights on a mobile. If you put too many weights on one side, it tilts. To fix it, you move the connection point. An AVL tree tracks its "tilt" (balance factor) and automatically shifts its connection points (rotations) whenever one side gets too heavy.

## E. Real-Life Analogy
Think of an adjustable suspension bridge. If too much traffic (data) builds up on one side, the bridge automatically tightens cables on the other side and shifts the center of gravity to keep the roadway balanced.

## F. Mental Model
Every node carries a `height` property. 
Balance Factor = Height(LeftSubtree) - Height(RightSubtree).
Valid Balance Factors: -1, 0, 1.
If Balance Factor becomes +2 (Left Heavy) or -2 (Right Heavy), the tree performs a rotation (Left, Right, Left-Right, or Right-Left) to fix it.

## G. Visual Explanation
```
Unbalanced (Right Heavy):
  10
    \
     20
       \
        30
(Node 10 has Balance Factor -2)

After Left Rotation at 10:
     20
    /  \
  10    30
(All nodes have Balance Factor 0)
```

## H. Formal Explanation
An AVL tree is a strictly balancing binary search tree. A node's balance factor is calculated as height(left) - height(right). Whenever a node is inserted or deleted, we update heights along the path back to the root and check the balance factor of each node. If a node's balance factor exits the set {-1, 0, 1}, we restore balance using one of four rotations.

## I. Mathematical Foundation
The maximum height h of an AVL tree with n nodes is bounded by c * log2(n) + b, where c ≈ 1.44. This ensures the height is strictly logarithmic in relation to the number of nodes, guaranteeing O(log n) operations.

## J. From-Scratch Implementation
(See the code below)

## K. Library / Production Implementation
Python doesn't have an AVL tree in its standard library. `collections.OrderedDict` or `set`/`dict` (which use hash tables) are often used for general lookups. However, packages like `bintrees` or `sortedcontainers` provide balanced tree-like behavior. Databases often use B-Trees (a generalization of balanced trees) for indexing.

## L. Trace (walk through example)
Insert 10, 20, 30:
1. Insert 10. (Root=10, BF=0)
2. Insert 20. (Root=10, Right=20, Node 10 BF=-1)
3. Insert 30. (Root=10, Right=20, Right.Right=30. Node 10 BF=-2. Right-Right case!)
4. Perform Left Rotation on 10.
5. New root is 20, Left=10, Right=30. All BFs are 0.

## M. Complexity
- Time: Search, Insertion, Deletion all take O(log n).
- Space: O(n) for nodes, O(log n) for recursive call stack.

## N. Common Mistakes
- Forgetting to update node heights during rotations.
- Calculating balance factor incorrectly (e.g., right - left instead of left - right, or inconsistent usage).
- Not returning the new root after a rotation.

## O. Common Confusions
- "Why does a Right-Left case need two rotations?"
  A single rotation would just shift the imbalance from one side to the other. The first rotation straightens out the "kink" into a straight line (Right-Right), and the second rotation balances the line.

## P. When To Use
- When lookups (searches) are frequent and must be strictly O(log n).
- When the data set is read-heavy (many searches, fewer insertions/deletions).

## Q. When NOT To Use
- When data is mostly written/updated. Red-Black trees are slightly faster for insertions/deletions because they require fewer rotations.
- When an average O(1) lookup is needed (use Hash Tables).

## R. Trade-offs
- AVL Trees vs Red-Black Trees: AVL is more strictly balanced, leading to faster lookups but potentially slower insertions/deletions due to more frequent rotations.

## S. Debugging
- Print the balance factor of every node after each insertion. If any node has a BF outside [-1, 0, 1], your rotations are failing or heights are not updating.
- Visualize the tree structure to trace exactly where the rotation happened.

## T. Memory Hook
AVL = Always Very Level. 

## U. Active Recall
- What is the valid range of balance factors in an AVL tree?
- What are the four rotation cases?

## V. Practice
- Implement the deletion operation for an AVL tree.

## W. Interview Question
"Design a data structure that allows insertion, deletion, and searching in O(log n) time, and also supports finding the k-th smallest element in O(log n) time." (Hint: AVL tree with subtree sizes).

## X. Project Connection
Building an in-memory database index engine where precise ordering, range queries, and guaranteed fast lookups are required.
"""

from typing import Optional, List, Tuple

class AVLNode:
    def __init__(self, key: int):
        self.key: int = key
        self.left: Optional['AVLNode'] = None
        self.right: Optional['AVLNode'] = None
        self.height: int = 1

class AVLTree:
    """Basic/Intermediate Implementation of an AVL Tree."""
    
    def get_height(self, node: Optional[AVLNode]) -> int:
        if not node:
            return 0
        return node.height

    def get_balance(self, node: Optional[AVLNode]) -> int:
        if not node:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)

    def right_rotate(self, y: AVLNode) -> AVLNode:
        x = y.left
        T2 = x.right

        # Perform rotation
        x.right = y
        y.left = T2

        # Update heights
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))

        # Return the new root
        return x

    def left_rotate(self, x: AVLNode) -> AVLNode:
        y = x.right
        T2 = y.left

        # Perform rotation
        y.left = x
        x.right = T2

        # Update heights
        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))

        # Return the new root
        return y

    def insert(self, root: Optional[AVLNode], key: int) -> AVLNode:
        # 1. Normal BST insertion
        if not root:
            return AVLNode(key)
        elif key < root.key:
            root.left = self.insert(root.left, key)
        else:
            root.right = self.insert(root.right, key)

        # 2. Update height of this ancestor node
        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))

        # 3. Get the balance factor
        balance = self.get_balance(root)

        # 4. If unbalanced, then there are 4 cases
        
        # Case 1 - Left Left
        if balance > 1 and key < root.left.key:
            return self.right_rotate(root)

        # Case 2 - Right Right
        if balance < -1 and key > root.right.key:
            return self.left_rotate(root)

        # Case 3 - Left Right
        if balance > 1 and key > root.left.key:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)

        # Case 4 - Right Left
        if balance < -1 and key < root.right.key:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root
        
    def pre_order(self, root: Optional[AVLNode], result: List[int]) -> None:
        if not root:
            return
        result.append(root.key)
        self.pre_order(root.left, result)
        self.pre_order(root.right, result)

def test_avl_tree():
    tree = AVLTree()
    root = None

    keys = [10, 20, 30, 40, 50, 25]
    for key in keys:
        root = tree.insert(root, key)

    result = []
    tree.pre_order(root, result)
    assert result == [30, 20, 10, 25, 40, 50], f"Expected [30, 20, 10, 25, 40, 50], got {result}"
    print("AVL Tree basic tests passed!")

if __name__ == "__main__":
    test_avl_tree()
