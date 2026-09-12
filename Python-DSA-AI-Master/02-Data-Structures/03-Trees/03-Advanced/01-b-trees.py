"""
## A. Concept Name
B-Trees

## B. Core Concept
A B-Tree is a self-balancing search tree in which nodes can have more than two children. It is specifically designed to minimize disk I/O operations, making it highly suitable for databases and file systems.

## C. Key Properties
- Every node has at most 2t-1 keys.
- Every non-leaf node (except root) has at least t-1 keys.
- The root has at least one key if it is not empty.
- A non-leaf node with k keys contains k+1 children.
- All leaves appear in the same level.

## D. Real-World Analogy
Think of a B-Tree as a library's filing cabinet. Instead of opening a drawer (loading a node) to find just one book title (key), you open a large drawer and immediately see many book titles and pointers to other cabinets. This reduces the number of times you have to open and close drawers (disk reads).

## E. Performance Analysis (Time & Space Complexity)
- Time Complexity: O(log N) for Search, Insert, Delete. (Base of log is proportional to branching factor m).
- Space Complexity: O(N)

## F. Memory Layout
Nodes in B-Trees are typically sized to match a disk block or page size, so that fetching one node exactly consumes one disk read.

## G. Common Use Cases
- Relational Databases (e.g., MySQL, PostgreSQL indexing)
- File Systems (e.g., NTFS, HFS+, ext4)

## H. Edge Cases
- Inserting into an empty tree.
- Splitting the root node.
- Keys already sorted vs unsorted insertions.

## I. Data Structures Compared
- **BST**: O(log N) but base 2, many disk I/O ops.
- **B-Tree**: O(log N) but large base, minimal disk I/O ops.

## J. Advantages
- High branching factor drastically reduces height.
- Cache-friendly due to sequential keys in a node.

## K. Disadvantages
- More complex implementation for insertion/deletion than a simple BST.
- Wasted space in nodes that are only half full.

## L. Step-by-Step Implementation
Implemented below in Python. Contains BTreeNode and BTree classes with insertion and search functionality.

## M. System Design Context
Used extensively in database engine design to create primary and secondary indexes.

## N. Troubleshooting / Common Bugs
- Incorrect median key selection during split.
- Failing to link children properly when a node splits.

## O. Testing Strategies
- Test with sequential inserts to force repeated node splitting.
- Test with random inserts.

## P. Best Practices
- Choose minimum degree `t` based on the disk block size to optimize I/O.

## Q. Variations
- B+ Trees (stores data only in leaves).
- B* Trees.

## R. Interview Questions
Q: How does a B-Tree differ from a Binary Search Tree in terms of disk I/O?
A: In an environment where data does not fit in RAM, accessing a node requires a disk read. A BST of height log2(N) might require many reads. A B-Tree has a high branching factor, drastically reducing its height to log_m(N), which means far fewer disk accesses.

## S. Recommended Tools
- Database visualization tools to see index structures.

## T. Glossary
- **Order (m)**: Maximum number of children a node can have.
- **Minimum Degree (t)**: Defines bounds on number of keys.

## U. Historical Context
Invented by Rudolf Bayer and Edward M. McCreight in 1971.

## V. Reference Materials
- "Introduction to Algorithms" by Cormen et al. (CLRS)

## W. Future Outlook
Will remain foundational as long as block-storage mechanisms (like SSDs and HDDs) are used.

## X. Project Connection
By understanding B-Trees, you can better implement or optimize storage mechanisms, file systems, and database indexing engines in your projects.
"""

from typing import List, Optional, Tuple, Any

class BTreeNode:
    def __init__(self, leaf: bool = False):
        self.leaf: bool = leaf
        self.keys: List[Any] = []
        self.children: List['BTreeNode'] = []

    def __str__(self) -> str:
        return f"Node(keys={self.keys}, leaf={self.leaf})"

class BTree:
    def __init__(self, t: int):
        """
        Initialize the B-Tree.
        :param t: The minimum degree
        """
        self.root: BTreeNode = BTreeNode(leaf=True)
        self.t: int = t

    def search(self, k: Any, node: Optional[BTreeNode] = None) -> Optional[Tuple[BTreeNode, int]]:
        """
        Search for key k in the B-Tree.
        Returns a tuple of (Node, index) if found, else None.
        """
        if node is None:
            node = self.root

        i = 0
        while i < len(node.keys) and k > node.keys[i]:
            i += 1

        if i < len(node.keys) and k == node.keys[i]:
            return (node, i)
        
        if node.leaf:
            return None
            
        return self.search(k, node.children[i])

    def insert(self, k: Any) -> None:
        """
        Insert key k into the B-Tree.
        """
        root = self.root
        if len(root.keys) == (2 * self.t) - 1:
            # Root is full, tree grows in height
            temp = BTreeNode()
            self.root = temp
            temp.children.insert(0, root)
            self._split_child(temp, 0)
            self._insert_non_full(temp, k)
        else:
            self._insert_non_full(root, k)

    def _insert_non_full(self, x: BTreeNode, k: Any) -> None:
        """
        Insert key k into node x which is assumed to be non-full.
        """
        i = len(x.keys) - 1
        if x.leaf:
            x.keys.append(None) # Make space
            while i >= 0 and k < x.keys[i]:
                x.keys[i + 1] = x.keys[i]
                i -= 1
            x.keys[i + 1] = k
        else:
            while i >= 0 and k < x.keys[i]:
                i -= 1
            i += 1
            if len(x.children[i].keys) == (2 * self.t) - 1:
                self._split_child(x, i)
                if k > x.keys[i]:
                    i += 1
            self._insert_non_full(x.children[i], k)

    def _split_child(self, x: BTreeNode, i: int) -> None:
        """
        Split the full child x.children[i] of node x.
        """
        t = self.t
        y = x.children[i]
        z = BTreeNode(leaf=y.leaf)
        
        # Insert z into x's children
        x.children.insert(i + 1, z)
        # Move median key from y to x
        x.keys.insert(i, y.keys[t - 1])
        
        # z gets the upper t-1 keys of y
        z.keys = y.keys[t:(2 * t - 1)]
        # y retains the lower t-1 keys
        y.keys = y.keys[0:(t - 1)]

        # If y is not a leaf, z gets the upper t children of y
        if not y.leaf:
            z.children = y.children[t:(2 * t)]
            y.children = y.children[0:t]

    def print_tree(self, x: Optional[BTreeNode] = None, l: int = 0) -> None:
        """
        Print the B-Tree structure for visualization.
        """
        if x is None:
            x = self.root
        print("Level", l, " ", len(x.keys), ":", x.keys)
        i = 0
        for i in range(len(x.children)):
            self.print_tree(x.children[i], l + 1)


def test_btree():
    print("--- B-Tree Operations ---")
    B = BTree(t=3) # Min degree 3 => keys per node: min 2, max 5

    # Insert elements
    keys_to_insert = [10, 20, 5, 6, 12, 30, 7, 17, 15]
    print(f"Inserting keys: {keys_to_insert}")
    for key in keys_to_insert:
        B.insert(key)
        
    print("\nTree Structure:")
    B.print_tree()

    print("\nSearching for 12:")
    res = B.search(12)
    if res:
        print(f"Found key 12 in node with keys: {res[0].keys} at index {res[1]}")
    else:
        print("Key 12 not found")

    print("\nSearching for 99:")
    res = B.search(99)
    print("Found" if res else "Not found")

if __name__ == "__main__":
    test_btree()
