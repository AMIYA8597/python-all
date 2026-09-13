"""
# ==============================================================================
# LABORATORY: B-TREES (DATABASE STORAGE ENGINES)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A standard Binary Tree stores 1 value per node. This is fine in RAM. But if 
# you are building a Database (MySQL, PostgreSQL) and storing data on a Hard Drive, 
# Disk I/O is 10,000x slower than RAM. If your Binary Tree is 30 levels deep, 
# finding a row takes 30 Disk Reads. 
# A B-Tree flattens the tree. By storing hundreds of values inside a SINGLE node, 
# a B-Tree can store 1 Billion rows and only be 4 levels deep! This means finding 
# any row in the database takes a maximum of 4 Disk Reads.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the `t` parameter (Minimum Degree) of a B-Tree.
# - Understand how a B-Tree Node stores multiple keys and multiple children.
# - Understand the complex "Node Splitting" algorithm.
# - Implement B-Tree Search.
#
# ==============================================================================
"""

from typing import List, Tuple, Optional

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. B-TREE NODE DEFINITION
# ==============================================================================
class BTreeNode:
    def __init__(self, leaf: bool = False):
        # A node contains a LIST of keys, always kept in sorted order.
        self.keys: List[int] = []
        # A node contains a LIST of pointers to its children.
        # Rule: The number of children is ALWAYS exactly len(keys) + 1.
        self.children: List['BTreeNode'] = []
        # Is this node a leaf? (Leaves have no children)
        self.leaf: bool = leaf


# ==============================================================================
# 4. B-TREE IMPLEMENTATION & SPLITTING
# ==============================================================================
class BTree:
    """
    A B-Tree of minimum degree `t`.
    - Every node (except root) must contain at least t-1 keys.
    - Every node can contain at most 2t-1 keys.
    - If a node gets 2t keys, it MUST SPLIT into two nodes, and push the middle key up.
    """
    def __init__(self, t: int):
        self.root = BTreeNode(leaf=True)
        self.t = t # Minimum degree

    def search(self, node: BTreeNode, k: int) -> Optional[Tuple[BTreeNode, int]]:
        """
        O(log N) search. 
        Instead of just `left` and `right`, we linearly (or binary) search 
        through the keys inside the node to find the correct child pointer.
        """
        i = 0
        # Find the first key greater than or equal to k
        while i < len(node.keys) and k > node.keys[i]:
            i += 1

        # Did we find the exact key in this node?
        if i < len(node.keys) and k == node.keys[i]:
            return (node, i)

        # If we didn't find it, and this is a leaf, the key doesn't exist.
        if node.leaf:
            return None

        # Recursively search the correct child
        return self.search(node.children[i], k)

    def insert(self, k: int) -> None:
        """
        Insertion in a B-Tree is complex. 
        Unlike a BST (where we add leaves at the bottom), a B-Tree grows 
        FROM THE ROOT UPWARDS. 
        If the root is full (2t-1 keys), we must split the root BEFORE inserting!
        """
        root = self.root
        if len(root.keys) == (2 * self.t) - 1:
            # The root is full. We must split it, which creates a new root 
            # and increases the height of the tree by 1.
            new_root = BTreeNode(leaf=False)
            self.root = new_root
            new_root.children.append(root)
            self._split_child(new_root, 0, root)
            self._insert_non_full(new_root, k)
        else:
            self._insert_non_full(root, k)

    def _split_child(self, parent: BTreeNode, i: int, full_child: BTreeNode) -> None:
        """
        Splits a full node (2t-1 keys) into two nodes (t-1 keys each).
        The middle key (median) is pushed UP to the parent node.
        """
        t = self.t
        new_child = BTreeNode(leaf=full_child.leaf)
        
        # 1. The new child gets the upper half of the keys
        new_child.keys = full_child.keys[t:]
        
        # 2. If it's not a leaf, it also gets the upper half of the children pointers
        if not full_child.leaf:
            new_child.children = full_child.children[t:]
            full_child.children = full_child.children[:t]
            
        # 3. The parent receives the middle key
        median_key = full_child.keys[t - 1]
        
        # 4. The full child is reduced to the lower half
        full_child.keys = full_child.keys[:t - 1]
        
        # 5. Wire the parent to the new child
        parent.children.insert(i + 1, new_child)
        parent.keys.insert(i, median_key)

    def _insert_non_full(self, node: BTreeNode, k: int) -> None:
        """
        Recursively finds the correct leaf and inserts the key.
        Because of the proactive splitting, we guarantee that any node we 
        traverse through is NEVER full.
        """
        i = len(node.keys) - 1
        
        if node.leaf:
            # We are at the leaf! Just insert it in sorted order.
            node.keys.append(0) # Make space
            while i >= 0 and k < node.keys[i]:
                node.keys[i + 1] = node.keys[i]
                i -= 1
            node.keys[i + 1] = k
        else:
            # We are not at a leaf. Find the correct child to descend into.
            while i >= 0 and k < node.keys[i]:
                i -= 1
            i += 1
            
            # If the child we are about to descend into is full, split it FIRST.
            if len(node.children[i].keys) == (2 * self.t) - 1:
                self._split_child(node, i, node.children[i])
                # After splitting, the median key moved up. We might need to adjust 
                # our descent path if the new key is less than k.
                if k > node.keys[i]:
                    i += 1
                    
            self._insert_non_full(node.children[i], k)

    def display(self, node: Optional[BTreeNode] = None, level: int = 0):
        if node is None:
            node = self.root
        
        print("  " * level + str(node.keys))
        if not node.leaf:
            for child in node.children:
                self.display(child, level + 1)


# ==============================================================================
# 5. EXECUTION & DEMONSTRATION
# ==============================================================================
def demonstrate_btree():
    section_header("B-Tree Mechanics (Degree t=3)")
    print("A B-Tree of degree t=3 means nodes can hold a maximum of 5 keys.")
    print("Once a node hits 5 keys, it splits, pushing the median up.\n")
    
    btree = BTree(t=3)
    
    # Insert sequentially. In a BST, this creates a Linked List.
    # Watch how the B-Tree handles it.
    for i in range(1, 15):
        btree.insert(i)
        
    print("B-Tree Structure (Indentation = Depth):")
    btree.display()
    
    print("\nNotice how the root only contains [6].")
    print("The left child contains [3], which branches to [1, 2] and [4, 5].")
    print("The tree is perfectly balanced and extremely shallow!")
    
    print("\nSearch for Key 10:")
    result = btree.search(btree.root, 10)
    if result:
        node, idx = result
        print(f"Found! It is at index {idx} inside the node containing keys: {node.keys}")


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why does a B-Tree minimize Disk I/O?
   Answer: When an OS reads from a hard drive, it pulls data in 4KB chunks (pages). A single node in a B-Tree is designed to be exactly 4KB in size. By packing hundreds of keys into one node, the tree becomes incredibly wide and shallow. Reading a node takes 1 Disk I/O, and since the tree is only 3 or 4 levels deep, finding any record takes at most 3 or 4 Disk I/Os.

2. Why is it important that the number of children is always `len(keys) + 1`?
   Answer: Because the keys act as dividers. If a node has keys `[10, 20]`, it creates 3 intervals: less than 10, between 10 and 20, and greater than 20. Each interval requires a corresponding child pointer.

3. How does a B-Tree grow taller?
   Answer: Unlike a BST which grows downwards at the leaves, a B-Tree grows UPWARDS. When the root node becomes completely full, it splits into two, and pushes its median key up into a brand new root node, increasing the height of the tree by 1.
"""

if __name__ == "__main__":
    demonstrate_btree()
    print("\n[SUCCESS] Laboratory: B-Trees Completed.")
