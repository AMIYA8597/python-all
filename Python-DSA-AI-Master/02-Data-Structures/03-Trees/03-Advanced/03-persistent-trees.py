"""
## A. Concept Name
Persistent Trees

## B. Analogy
Think of a Persistent Tree like a version control system (e.g., Git) for a data structure. Instead of modifying the original tree and losing the past state, every modification creates a new "commit" or version. Unchanged parts are shared between versions to save space, just like Git shares unchanged files between commits.

## C. Core Idea
A persistent data structure always preserves the previous version of itself when it is modified. A Persistent BST achieves this via "Path Copying". When a node is inserted or updated, we do not mutate the existing node. Instead, we create a new node and copy the path from the root down to the modified node. Unchanged branches are shared between different versions, saving space and time.

## D. Why it Matters
It allows querying historical states of the data structure. It's heavily used in functional programming languages (where data is immutable by default), databases (for Multi-Version Concurrency Control), and computational geometry (like point location queries).

## E. Real-World Example
- Git (Version Control Systems)
- Databases (MVCC)
- Text editors (Undo/Redo history)

## F. Prerequisites
- Binary Search Trees
- Recursion
- Pointers and Memory References

## G. Path Copying
When a node is updated, the path from the root to that node is copied. The rest of the tree is shared.

## H. Node Sharing
Unmodified subtrees are referenced by multiple versions of the tree, significantly saving memory.

## I. Insertion Process
To insert, we recursively traverse the tree. When creating a new node, its child that doesn't change points to the old child, while its modified child points to a newly created node.

## J. Time Complexity
- Search: O(log N) for balanced trees.
- Insert: O(log N) for balanced trees.

## K. Space Complexity
- Insert: O(log N) per insert, as we create a new path of nodes (proportional to the height of the tree).

## L. Tree Balancing
For true O(log N) guarantees, persistent trees must be balanced (like Persistent Red-Black or AVL trees). A standard Persistent BST can degrade to O(N).

## M. Memory Management
Because of node sharing, memory management can be complex. In languages with Garbage Collection (like Python, Java), unreachable nodes are automatically cleaned up. In C/C++, reference counting or other GC techniques are required.

## N. Querying the Past
You can pass the root of any previous version to standard search/traversal functions, and they will work seamlessly as if they were querying the tree at that exact point in time.

## O. Immutable Data Structures
Persistent trees form the basis of immutable data structures, promoting safer concurrent programming by avoiding lock contention.

## P. Retroactive Data Structures
While persistent structures allow querying the past, retroactive structures allow modifying the past.

## Q. Fully vs Partially Persistent
- Partially Persistent: All versions can be accessed, but only the newest version can be modified.
- Fully Persistent: Every version can be both accessed and modified (branching history).

## R. Edge Cases
- Inserting duplicate values (might return the same version if unchanged).
- Searching for versions out of bounds.

## S. Pitfalls
- Accidentally mutating a node instead of returning a new one. This destroys the persistence property.

## T. Debugging Tips
Use `id(node)` in Python to verify if two versions are sharing the same unmodified subtree.

## U. Exercises
1. Implement a deletion operation that preserves past versions.
2. Verify node sharing using Python's `id()` function.
3. Extend the tree to be an AVL tree to guarantee O(log N) depth.

## V. Related Concepts
- Functional Data Structures
- Directed Acyclic Graphs (since shared nodes make the "tree" a DAG in memory)

## W. Summary
Persistent Trees allow you to maintain history efficiently using path copying. They trade a slight overhead in space and node creation time for the immense power of immutability and historical queries.

## X. Project Connection
In projects requiring undo/redo features, time-travel debugging, or complex functional state management, implementing a persistent data structure ensures that you never lose data when transitions happen.
"""

from typing import Optional, List

class PersistentTreeNode:
    def __init__(self, value: int, left: Optional['PersistentTreeNode'] = None, right: Optional['PersistentTreeNode'] = None):
        self.value = value
        self.left = left
        self.right = right

    def __str__(self):
        return f"Node({self.value})"


class PersistentBST:
    def __init__(self):
        self.versions: List[Optional[PersistentTreeNode]] = [None]  # stores roots of all versions

    def insert(self, value: int) -> int:
        """
        Insert a value and return the new version number.
        """
        latest_root = self.versions[-1]
        new_root = self._insert_recursive(latest_root, value)
        self.versions.append(new_root)
        return len(self.versions) - 1

    def _insert_recursive(self, node: Optional[PersistentTreeNode], value: int) -> PersistentTreeNode:
        if node is None:
            return PersistentTreeNode(value)
        
        if value < node.value:
            # Create a new node with the same value, left child is the new subtree, right child is shared
            return PersistentTreeNode(node.value, self._insert_recursive(node.left, value), node.right)
        elif value > node.value:
            # Create a new node with the same value, right child is the new subtree, left child is shared
            return PersistentTreeNode(node.value, node.left, self._insert_recursive(node.right, value))
        else:
            # Value already exists, just return the node as is (no change)
            return node

    def search(self, version: int, value: int) -> bool:
        """
        Search for a value in a specific version of the tree.
        """
        if version >= len(self.versions) or version < 0:
            raise ValueError("Invalid version number")
        
        root = self.versions[version]
        return self._search_recursive(root, value)

    def _search_recursive(self, node: Optional[PersistentTreeNode], value: int) -> bool:
        if node is None:
            return False
        if node.value == value:
            return True
        elif value < node.value:
            return self._search_recursive(node.left, value)
        else:
            return self._search_recursive(node.right, value)

    def inorder(self, version: int) -> List[int]:
        """
        Return inorder traversal for a given version.
        """
        root = self.versions[version]
        result: List[int] = []
        self._inorder_recursive(root, result)
        return result

    def _inorder_recursive(self, node: Optional[PersistentTreeNode], result: List[int]) -> None:
        if node:
            self._inorder_recursive(node.left, result)
            result.append(node.value)
            self._inorder_recursive(node.right, result)


# ==========================================
# Edge Cases & Interview Challenge
# ==========================================
"""
Edge Cases Handled:
- Inserting duplicate values (does nothing, returns same node).
- Searching in an invalid version number.

Interview Challenge:
Q: Why is path copying efficient compared to fully duplicating the tree?
A: Path copying only clones the nodes along the path from the root to the modified node. 
   In a balanced tree of N nodes, the path length is log(N). Therefore, we only copy 
   log(N) nodes instead of all N nodes, heavily optimizing both time and memory overhead.
"""

def test_persistent_tree():
    print("--- Persistent BST Operations ---")
    tree = PersistentBST()
    
    # Version 0 is empty
    v1 = tree.insert(10)
    v2 = tree.insert(5)
    v3 = tree.insert(15)
    v4 = tree.insert(2)

    print(f"Version {v1} elements: {tree.inorder(v1)}")
    print(f"Version {v2} elements: {tree.inorder(v2)}")
    print(f"Version {v3} elements: {tree.inorder(v3)}")
    print(f"Version {v4} elements: {tree.inorder(v4)}")

    print(f"\nSearching for 15 in Version {v2} (should be False): {tree.search(v2, 15)}")
    print(f"Searching for 15 in Version {v3} (should be True): {tree.search(v3, 15)}")
    
    # Check node sharing
    root_v3 = tree.versions[v3]
    root_v4 = tree.versions[v4]
    
    # Node 15 should be the exact same object in memory for v3 and v4 since it wasn't modified
    print(f"\nNode sharing verification:")
    print(f"Right child of root in V3 id: {id(root_v3.right)}")
    print(f"Right child of root in V4 id: {id(root_v4.right)}")
    print("Are they the same object?", root_v3.right is root_v4.right)

if __name__ == "__main__":
    test_persistent_tree()
