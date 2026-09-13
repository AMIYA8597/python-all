"""
# ==============================================================================
# LABORATORY: SPLAY TREES (SELF-ADJUSTING BST)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# AVL and Red-Black trees balance themselves based on mathematical Height. 
# But what if your workload has "Temporal Locality"? Meaning, if a user accesses 
# their profile page once, they are highly likely to access it again in the next 
# 10 minutes. In a perfectly balanced AVL tree, fetching that profile might always 
# take 20 jumps down the tree.
# A Splay Tree is a BST with a radical rule: EVERY TIME you access a node, you 
# perform rotations ("Splaying") to move that node to the absolute ROOT of the tree.
# This means frequently accessed items are always at the top (O(1) access), 
# naturally creating an LRU (Least Recently Used) Cache behavior!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the concept of Amortized O(log N) vs Strict O(log N).
# - Understand the 3 Splay Rotations: Zig, Zig-Zig, and Zig-Zag.
# - Observe how querying a deep node pulls it to the root.
#
# ==============================================================================
"""

from typing import Optional

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. SPLAY TREE NODE & ROTATIONS
# ==============================================================================
class SplayNode:
    def __init__(self, val: int):
        self.val = val
        self.left: Optional['SplayNode'] = None
        self.right: Optional['SplayNode'] = None

class SplayTree:
    """
    Splay Trees don't store height or color! They are incredibly lightweight 
    in memory compared to AVL or Red-Black trees.
    """
    def __init__(self):
        self.root: Optional[SplayNode] = None

    def _right_rotate(self, x: SplayNode) -> SplayNode:
        y = x.left
        x.left = y.right
        y.right = x
        return y

    def _left_rotate(self, x: SplayNode) -> SplayNode:
        y = x.right
        x.right = y.left
        y.left = x
        return y

    def _splay(self, root: Optional[SplayNode], key: int) -> Optional[SplayNode]:
        """
        The Splay operation. It searches for the key. If found, it bubbles it up 
        to the root. If not found, it bubbles up the LAST node accessed!
        """
        if not root or root.val == key:
            return root

        # 1. Key lies in LEFT subtree
        if key < root.val:
            if not root.left:
                return root
                
            # Zig-Zig (Left Left)
            if key < root.left.val:
                # Recursively bring the key to the root of the left-left child
                root.left.left = self._splay(root.left.left, key)
                # Do first rotation for root
                root = self._right_rotate(root)
                
            # Zig-Zag (Left Right)
            elif key > root.left.val:
                # Recursively bring the key to the root of the left-right child
                root.left.right = self._splay(root.left.right, key)
                # Do first rotation for root.left
                if root.left.right:
                    root.left = self._left_rotate(root.left)
                    
            # Do second rotation for root
            return self._right_rotate(root) if root.left else root

        # 2. Key lies in RIGHT subtree
        else:
            if not root.right:
                return root
                
            # Zag-Zig (Right Left)
            if key < root.right.val:
                root.right.left = self._splay(root.right.left, key)
                if root.right.left:
                    root.right = self._right_rotate(root.right)
                    
            # Zag-Zag (Right Right)
            elif key > root.right.val:
                root.right.right = self._splay(root.right.right, key)
                root = self._left_rotate(root)
                
            return self._left_rotate(root) if root.right else root

    def search(self, key: int) -> bool:
        """
        Searches for a key. Whether it finds it or not, it SPLAYS the tree!
        """
        if not self.root:
            return False
            
        # Splay the tree around the key
        self.root = self._splay(self.root, key)
        
        # After splaying, IF the key exists in the tree, it MUST be the new root!
        return self.root.val == key

    def insert(self, key: int) -> None:
        """
        Inserts a new node and immediately splays it to the root.
        """
        if not self.root:
            self.root = SplayNode(key)
            return

        # Splay the tree around the new key.
        # This will bring the closest existing value to the root.
        self.root = self._splay(self.root, key)

        # If the key is already at the root, do nothing (assuming no duplicates)
        if self.root.val == key:
            return

        # Allocate new node
        new_node = SplayNode(key)

        # Wire up the new root
        if key < self.root.val:
            new_node.right = self.root
            new_node.left = self.root.left
            self.root.left = None
        else:
            new_node.left = self.root
            new_node.right = self.root.right
            self.root.right = None

        self.root = new_node


def print_tree(root: Optional[SplayNode], level=0, prefix="Root: "):
    if root is not None:
        print(" " * (level * 4) + prefix + str(root.val))
        print_tree(root.left, level + 1, "L: ")
        print_tree(root.right, level + 1, "R: ")


# ==============================================================================
# 4. EXECUTION & DEMONSTRATION
# ==============================================================================
def demonstrate_splay_tree():
    section_header("Splay Tree: Self-Adjusting Cache Behavior")
    
    st = SplayTree()
    
    # 1. Insert data
    print("Inserting 10, 20, 30, 40, 50, 60...")
    for v in [10, 20, 30, 40, 50, 60]:
        st.insert(v)
        
    print("\nTree structure after insertions (Notice 60 is the root because it was inserted last!):")
    print_tree(st.root)
    
    # 2. Search (Triggers Splaying)
    print("\n" + "-"*40)
    print("Now, let's search for '10' (which is currently buried at the very bottom).")
    print("In a normal BST, this would take O(N) since the tree is a linked list right now.")
    print("But watch what happens after the search...")
    
    found = st.search(10)
    print(f"Search for 10 result: {found}")
    
    print("\nTree structure AFTER searching for 10:")
    print_tree(st.root)
    
    print("\nMAGIC! 10 has been SPLAYED to the absolute root.")
    print("If we search for 10 again, it will take exactly O(1) time.")
    print("This naturally implements a Least Recently Used (LRU) Cache behavior")
    print("without requiring any extra Hash Maps or Doubly Linked Lists!")


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. What is the worst-case Time Complexity of a single operation in a Splay Tree?
   Answer: O(N). Because a Splay tree does not strictly enforce balance, it can degenerate into a Linked List. However, the *Amortized* (average over a sequence of operations) Time Complexity is mathematically proven to be O(log N).

2. If the worst-case is O(N), why use a Splay Tree instead of an AVL Tree?
   Answer: AVL Trees are best for uniform random access. Splay Trees are vastly superior when the data access pattern exhibits "Temporal Locality" (the 80/20 rule: 80% of queries fetch the same 20% of data). Because frequently accessed nodes are kept near the root, those queries execute in O(1) time. Furthermore, Splay Trees require zero extra memory per node (no height, no color variables).

3. What happens in a Splay Tree if you search for a value that does NOT exist?
   Answer: The standard BST search will hit a `None` pointer. The Splay Tree will then take the LAST valid node it touched before hitting `None` and Splay THAT node to the root.
"""

if __name__ == "__main__":
    demonstrate_splay_tree()
    print("\n[SUCCESS] Laboratory: Splay Trees Completed.")
