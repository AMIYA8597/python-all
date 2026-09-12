"""
## A. Concept Name
Tree Data Structure

## B. One-Sentence Definition
A tree is a hierarchical data structure consisting of nodes connected by edges, with a single root and no cycles.

## C. Why Does This Exist?
To represent hierarchical relationships (like file systems, organizational charts, or taxonomies) and to enable efficient searching and sorting compared to linear data structures like arrays or linked lists.

## D. Intuition
Imagine a family tree or a corporate hierarchy. There is one person at the top (root), who has children (subnodes), who in turn have their own children, forming a branching structure.

## E. Real-Life Analogy
A file system on a computer. The root directory (e.g., `C:\`) contains folders (child nodes), which contain subfolders or files (leaf nodes). 

## F. Mental Model
Think of an upside-down physical tree. The root is at the top, branching downwards into sub-branches, and finally ending in leaves (nodes with no children).

## G. Visual Explanation
        [Root]
       /      \
   [Node A]   [Node B]
    /    \         \
[Leaf 1] [Leaf 2]  [Leaf 3]

## H. Formal Explanation
A tree is a connected, acyclic graph. It consists of a set of nodes (vertices) and a set of directed edges that connect pairs of nodes. It has exactly one root node, and every other node has exactly one parent.

## I. Mathematical Foundation
A tree with $N$ nodes always has exactly $N - 1$ edges. The depth of a node is the number of edges from the root to the node. The height of a tree is the maximum depth of any node.

## J. From-Scratch Implementation
```python
class TreeNode:
    def __init__(self, data):
        self.data = data
        self.children = []

    def add_child(self, child_node):
        self.children.append(child_node)
        
    def traverse(self):
        # Basic pre-order traversal
        nodes = [self.data]
        for child in self.children:
            nodes.extend(child.traverse())
        return nodes
```

## K. Library / Production Implementation
Python doesn't have a built-in tree data structure in its standard library, though `xml.etree.ElementTree` is used for XML trees, and `ast` represents Abstract Syntax Trees. Usually, developers create custom classes or use third-party libraries like `anytree`.

## L. Trace (walk through example)
1. Create root node 'CEO'.
2. Create child nodes 'CTO' and 'CFO'.
3. `CEO.add_child(CTO)` and `CEO.add_child(CFO)`.
4. Traversal starting at 'CEO' visits 'CEO', then explores 'CTO' and its children, then 'CFO' and its children.

## M. Complexity
- Space Complexity: $O(N)$ where $N$ is the number of nodes.
- Time Complexity (Traversal): $O(N)$ to visit all nodes.
- Search/Insert/Delete: Depends heavily on tree type (e.g., $O(\\log N)$ for balanced BST, $O(N)$ for general unorganized tree).

## N. Common Mistakes
- Creating cycles (making a child point back to a parent or ancestor), which turns the tree into a general graph.
- Forgetting to handle the base case (empty tree or leaf node) in recursive traversal functions.

## O. Common Confusions
- "Is a Linked List a Tree?" Yes, a linked list is a degenerate tree where each node has exactly one child.
- Tree vs Graph: All trees are graphs, but not all graphs are trees. Trees must be connected and acyclic.

## P. When To Use
- When data has a natural hierarchical structure (e.g., categories, menus).
- For efficient searching, inserting, and deleting operations (specifically Binary Search Trees).
- Representing parsed data like HTML/XML DOM or code (AST).

## Q. When NOT To Use
- When data is strictly linear or sequential.
- When you need to model cyclical relationships (use a Graph instead).
- When rapid, indexed access is required (use an Array or Hash Table).

## R. Trade-offs
- Better search performance than linked lists, but requires more overhead (pointers/references).
- Recursive algorithms for trees are elegant but can cause stack overflow for very deep trees.

## S. Debugging
- Print tree structures visually (e.g., using indentation to show depth) to quickly spot misplaced nodes.
- When recursing, verify that your base cases (e.g., `if not node`) are correct.

## T. Memory Hook
"Root at the top, leaves at the bottom, no circles allowed."

## U. Active Recall
1. What defines a tree compared to a general graph?
2. How many edges does a tree with $N$ nodes have?
3. What is the difference between node depth and tree height?

## V. Practice
- Implement a function to find the maximum depth (height) of a given tree.
- Write a function that counts the total number of leaf nodes in a tree.

## W. Interview Question
"Given the root of an n-ary tree, return the level order traversal of its nodes' values."

## X. Project Connection
In an AI or Machine Learning project, Decision Trees use this exact structure to make classifications. Each internal node represents a test on an attribute, each branch represents an outcome, and each leaf node holds a class label.
"""

class TreeNode:
    """
    A basic implementation of a General Tree Node.
    """
    def __init__(self, data):
        self.data = data
        self.children = []

    def add_child(self, child_node):
        """Adds a child to the current node."""
        if not isinstance(child_node, TreeNode):
            child_node = TreeNode(child_node)
        self.children.append(child_node)

    def print_tree(self, level=0):
        """Prints the tree recursively with indentation."""
        prefix = " " * (level * 2) + "|__ " if level > 0 else ""
        print(prefix + str(self.data))
        for child in self.children:
            child.print_tree(level + 1)

    def __repr__(self):
        return f"TreeNode({self.data})"

if __name__ == "__main__":
    # Basic usage example
    root = TreeNode("Electronics")
    
    laptop = TreeNode("Laptop")
    laptop.add_child("MacBook")
    laptop.add_child("ThinkPad")
    
    phone = TreeNode("Phone")
    phone.add_child("iPhone")
    phone.add_child("Pixel")
    
    root.add_child(laptop)
    root.add_child(phone)
    
    print("Tree structure:")
    root.print_tree()
