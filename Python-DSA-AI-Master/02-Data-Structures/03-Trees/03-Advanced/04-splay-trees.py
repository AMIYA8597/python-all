"""
## A. Concept Name
Splay Trees

## B. Core Explanation
A Splay Tree is a self-adjusting binary search tree where recently accessed elements are moved to the root, making them quick to access again.

## C. Analogy
Imagine a stack of books on your desk. Every time you read a book, you place it on top. Over time, your most frequently read books stay near the top, making them easy to grab.

## D. Visual Representation
Accessing 'X' splays it to the root:
    Y             X
   / \   splay   / \
  X   Z  ====>  A   Y
 / \               / \
A   B             B   Z

## E. Key Properties
- Binary Search Tree properties hold.
- Self-optimizing for biased access patterns.
- No extra metadata is stored per node (unlike AVL or Red-Black).

## F. Basic Operations
- Search: Finds an element and splays it to the root.
- Insert: Inserts an element and splays it to the root.

## G. Advanced Operations
- Splay: A sequence of Zig, Zig-Zig, and Zig-Zag rotations to bring a node to the root.

## H. Algorithm Steps
1. Perform standard BST search/insert.
2. If element is found/inserted, perform splay rotations repeatedly.
3. Node becomes the new root.

## I. Edge Cases
- Searching for a non-existent key splays the last accessed node.
- Inserting a duplicate key is ignored, but the existing node is splayed.

## J. Time Complexity
- Search: O(log N) amortized
- Insert: O(log N) amortized
- Delete: O(log N) amortized

## K. Space Complexity
- Space Complexity: O(N)

## L. Advantages
- Great for temporal locality (caches).
- Simpler to implement than some self-balancing trees.

## M. Disadvantages
- Can become linear O(N) in worst-case (though amortized is O(log N)).
- Not strictly balanced.

## N. Common Uses
- Caches (like LRU).
- Network routers.

## O. Comparison
- vs AVL: Less strict balance, no height metadata.
- vs Red-Black: No color metadata, adapts to access patterns.

## P. Common Pitfalls
- Forgetting to splay on every search/access operation.
- Mistaking Zig-Zag for Zig-Zig.

## Q. Interview Focus
- Why is it good for caching? (Answer: frequently accessed nodes stay near root).

## R. Optimization
- Top-down splaying can be slightly faster than bottom-up.

## S. Related Concepts
- AVL Trees, Red-Black Trees, Treaps.

## T. Code Structure
- SplayTreeNode class: holds key, left, right.
- SplayTree class: contains rotations and splay logic.

## U. Debugging Tips
- Check root pointer after each operation.

## V. Test Cases
- Insert sequences of sorted keys (triggers worst-case tree structure before splaying).
- Access deep nodes to verify they bubble up to the root.

## W. Real-world Examples
- GCC compiler uses splay trees for some internal data structures.

## X. Project Connection
Can be integrated as the core data structure in an LRU Cache or a high-performance routing table simulator.
"""

from typing import Optional

class SplayTreeNode:
    def __init__(self, key: int):
        self.key = key
        self.left: Optional['SplayTreeNode'] = None
        self.right: Optional['SplayTreeNode'] = None


class SplayTree:
    def __init__(self):
        self.root: Optional[SplayTreeNode] = None

    def right_rotate(self, x: SplayTreeNode) -> SplayTreeNode:
        y = x.left
        if y is not None:
            x.left = y.right
            y.right = x
            return y
        return x

    def left_rotate(self, x: SplayTreeNode) -> SplayTreeNode:
        y = x.right
        if y is not None:
            x.right = y.left
            y.left = x
            return y
        return x

    def splay(self, root: Optional[SplayTreeNode], key: int) -> Optional[SplayTreeNode]:
        """
        Splays the key to the root. If the key doesn't exist, the last accessed node becomes the root.
        """
        if root is None or root.key == key:
            return root

        # Key lies in left subtree
        if root.key > key:
            if root.left is None:
                return root
            
            # Zig-Zig (Left Left)
            if root.left.key > key:
                root.left.left = self.splay(root.left.left, key)
                root = self.right_rotate(root)
            # Zig-Zag (Left Right)
            elif root.left.key < key:
                root.left.right = self.splay(root.left.right, key)
                if root.left.right is not None:
                    root.left = self.left_rotate(root.left)
            
            return root if root.left is None else self.right_rotate(root)

        # Key lies in right subtree
        else:
            if root.right is None:
                return root

            # Zag-Zig (Right Left)
            if root.right.key > key:
                root.right.left = self.splay(root.right.left, key)
                if root.right.left is not None:
                    root.right = self.right_rotate(root.right)
            # Zag-Zag (Right Right)
            elif root.right.key < key:
                root.right.right = self.splay(root.right.right, key)
                root = self.left_rotate(root)
            
            return root if root.right is None else self.left_rotate(root)

    def search(self, key: int) -> bool:
        """
        Search for a key. As a side effect, splays the found node to the root.
        """
        self.root = self.splay(self.root, key)
        return self.root is not None and self.root.key == key

    def insert(self, key: int) -> None:
        """
        Insert a key into the Splay Tree.
        """
        if self.root is None:
            self.root = SplayTreeNode(key)
            return

        self.root = self.splay(self.root, key)
        
        if self.root.key == key:
            return # Key already present
        
        new_node = SplayTreeNode(key)
        if self.root.key > key:
            new_node.right = self.root
            new_node.left = self.root.left
            self.root.left = None
        else:
            new_node.left = self.root
            new_node.right = self.root.right
            self.root.right = None
        
        self.root = new_node

    def preorder(self, node: Optional[SplayTreeNode]) -> None:
        if node is not None:
            print(node.key, end=" ")
            self.preorder(node.left)
            self.preorder(node.right)


def test_splay_tree():
    print("--- Splay Tree Operations ---")
    tree = SplayTree()
    
    keys = [10, 20, 30, 100, 90, 40, 50]
    for k in keys:
        tree.insert(k)
        
    print("Preorder traversal after insertions:")
    tree.preorder(tree.root)
    print("\nRoot is currently:", tree.root.key if tree.root else None)
    
    print("\nSearching for 20...")
    found = tree.search(20)
    print(f"Found 20? {found}")
    print("Preorder traversal after searching for 20 (it should now be at root):")
    tree.preorder(tree.root)
    print("\nRoot is now:", tree.root.key if tree.root else None)

if __name__ == "__main__":
    test_splay_tree()
