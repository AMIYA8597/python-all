"""
## A. Concept Name
Treaps (Tree + Heap)

## B. Problem Space
Maintaining a balanced Binary Search Tree (BST) using deterministic algorithms (like AVL or Red-Black Trees) involves complex balancing logic. An unbalanced BST degrades to O(N) time complexity for operations. We need a simpler approach to ensure a tree remains balanced on average without strict balancing rules.

## C. Solution Architecture
A Treap is a randomized binary search tree. Each node stores two values: a key and a priority.
- The keys obey the Binary Search Tree property (left child < parent < right child).
- The priorities obey the Max-Heap property (parent priority > children priorities).
By assigning a random priority to each key upon insertion, we ensure that the tree remains balanced on average, yielding O(log N) operations.

## D. Core Implementation
The Treap implements `insert`, `delete`, and `search` using recursive traversals and standard BST logic, coupled with rotations (`_left_rotate`, `_right_rotate`) to restore the Max-Heap property.

## X. Project Connection
Treaps introduce the power of randomization in data structures, a core concept in advanced algorithm design. They offer a simple, elegant alternative to deterministic self-balancing trees, widely used in scenarios where average-case O(log N) performance is acceptable and implementation simplicity is valued.

Edge Cases Handled:
- Rotations efficiently handle restructuring after inserts and deletes.
- Deleting a node with two children requires rotating it down dynamically based on priority.

Interview Challenge:
Q: Since Treaps use random priorities, could it still degenerate into a linked list?
A: Yes, in the worst-case scenario where the randomly generated priorities happen to be sorted in the same order as the keys, a Treap could degrade into an O(N) linked list. However, the probability of this occurring is astronomically low (same as quicksort worst-case).
"""

import random
from typing import Optional, Tuple

class TreapNode:
    def __init__(self, key: int):
        self.key = key
        self.priority = random.random()
        self.left: Optional['TreapNode'] = None
        self.right: Optional['TreapNode'] = None

class Treap:
    def __init__(self):
        self.root: Optional[TreapNode] = None

    def _right_rotate(self, y: TreapNode) -> TreapNode:
        x = y.left
        if x:
            y.left = x.right
            x.right = y
            return x
        return y

    def _left_rotate(self, x: TreapNode) -> TreapNode:
        y = x.right
        if y:
            x.right = y.left
            y.left = x
            return y
        return x

    def insert(self, key: int) -> None:
        self.root = self._insert_node(self.root, key)

    def _insert_node(self, root: Optional[TreapNode], key: int) -> TreapNode:
        if root is None:
            return TreapNode(key)

        if key <= root.key:
            root.left = self._insert_node(root.left, key)
            # Fix heap property
            if root.left and root.left.priority > root.priority:
                root = self._right_rotate(root)
        else:
            root.right = self._insert_node(root.right, key)
            # Fix heap property
            if root.right and root.right.priority > root.priority:
                root = self._left_rotate(root)

        return root

    def delete(self, key: int) -> None:
        self.root = self._delete_node(self.root, key)

    def _delete_node(self, root: Optional[TreapNode], key: int) -> Optional[TreapNode]:
        if root is None:
            return None

        if key < root.key:
            root.left = self._delete_node(root.left, key)
        elif key > root.key:
            root.right = self._delete_node(root.right, key)
        else:
            # Node to be deleted found
            if root.left is None and root.right is None:
                return None
            elif root.left and root.right:
                # Both children exist: rotate node down to a leaf, then delete
                if root.left.priority > root.right.priority:
                    root = self._right_rotate(root)
                    root.right = self._delete_node(root.right, key)
                else:
                    root = self._left_rotate(root)
                    root.left = self._delete_node(root.left, key)
            else:
                # One child exists
                child = root.left if root.left else root.right
                return child

        return root

    def search(self, key: int) -> bool:
        curr = self.root
        while curr:
            if curr.key == key:
                return True
            elif key < curr.key:
                curr = curr.left
            else:
                curr = curr.right
        return False

    def inorder(self, node: Optional[TreapNode]) -> None:
        if node:
            self.inorder(node.left)
            print(f"(K:{node.key}, P:{node.priority:.2f})", end=" ")
            self.inorder(node.right)


def test_treap():
    print("--- Treap Operations ---")
    treap = Treap()
    
    keys = [50, 30, 20, 40, 70, 60, 80]
    print(f"Inserting keys: {keys}")
    for k in keys:
        treap.insert(k)
        
    print("\nInorder Traversal (should be sorted by Key):")
    treap.inorder(treap.root)
    print("\n")
    
    print("Search for 40:", treap.search(40))
    print("Search for 99:", treap.search(99))
    
    print("\nDeleting 50...")
    treap.delete(50)
    print("Inorder Traversal after deleting 50:")
    treap.inorder(treap.root)
    print()

if __name__ == "__main__":
    test_treap()
