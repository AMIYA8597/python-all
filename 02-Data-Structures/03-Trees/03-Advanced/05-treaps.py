"""
# ==============================================================================
# LABORATORY: TREAPS (TREE + HEAP)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You've seen that AVL Trees and Red-Black Trees are incredibly complex to implement. 
# What if there was a way to guarantee O(log N) balance without keeping track of 
# Heights or Colors, and without analyzing dozens of Edge Cases?
# Enter the Treap (Tree + Heap). It relies on PROBABILITY. 
# Every node is given a normal Key (which strictly follows BST rules: Left < Root < Right).
# But every node is ALSO given a randomly generated Priority (which strictly follows 
# Max-Heap rules: Parent > Children). 
# Because the priorities are completely random, the tree naturally balances itself 
# with high mathematical probability, yielding expected O(log N) performance!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the dual-property of a Treap node (BST Key + Heap Priority).
# - Understand how Rotations are used to restore the Heap property.
# - Implement a Treap Insertion.
#
# ==============================================================================
"""

import random
from typing import Optional, Tuple

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. TREAP NODE DEFINITION
# ==============================================================================
class TreapNode:
    def __init__(self, key: int):
        self.key = key
        # Assign a completely random priority!
        # In a real system, use a large integer range.
        self.priority = random.randint(1, 1000) 
        self.left: Optional['TreapNode'] = None
        self.right: Optional['TreapNode'] = None


# ==============================================================================
# 4. TREAP IMPLEMENTATION & ROTATIONS
# ==============================================================================
class Treap:
    def __init__(self):
        self.root: Optional[TreapNode] = None

    def _right_rotate(self, y: TreapNode) -> TreapNode:
        """Standard BST Right Rotation."""
        x = y.left
        T2 = x.right
        
        # Perform rotation
        x.right = y
        y.left = T2
        
        return x # Return new root

    def _left_rotate(self, x: TreapNode) -> TreapNode:
        """Standard BST Left Rotation."""
        y = x.right
        T2 = y.left
        
        # Perform rotation
        y.left = x
        x.right = T2
        
        return y # Return new root

    def insert(self, root: Optional[TreapNode], key: int) -> TreapNode:
        """
        Recursive insertion. 
        1. Insert based on standard BST rules (using the Key).
        2. On the way back up the recursion stack, check the Heap rule (Priority).
        3. If the Heap rule is violated, perform a single rotation!
        """
        # 1. Standard BST Insertion
        if not root:
            return TreapNode(key)
            
        if key <= root.key:
            root.left = self.insert(root.left, key)
            
            # 2. Heap Property Check (Max-Heap)
            # If the left child's priority is GREATER than the parent's priority,
            # we must rotate the child UP. A Right Rotation pulls the left child up.
            if root.left.priority > root.priority:
                root = self._right_rotate(root)
                
        else:
            root.right = self.insert(root.right, key)
            
            # 2. Heap Property Check (Max-Heap)
            # If the right child's priority is GREATER than the parent's priority,
            # we must rotate the child UP. A Left Rotation pulls the right child up.
            if root.right.priority > root.priority:
                root = self._left_rotate(root)
                
        return root

    def search(self, root: Optional[TreapNode], key: int) -> bool:
        """Standard O(log N) BST Search."""
        if not root:
            return False
        if root.key == key:
            return True
        if key < root.key:
            return self.search(root.left, key)
        return self.search(root.right, key)


def print_treap(root: Optional[TreapNode], level=0, prefix="Root: "):
    if root is not None:
        print(" " * (level * 4) + prefix + f"[K:{root.key} | P:{root.priority}]")
        print_treap(root.left, level + 1, "L: ")
        print_treap(root.right, level + 1, "R: ")


# ==============================================================================
# 5. EXECUTION & DEMONSTRATION
# ==============================================================================
def demonstrate_treap():
    section_header("Algorithm: Treap (Randomized Balancing)")
    
    # We will set a static seed so the "random" priorities are predictable 
    # for this demonstration, allowing you to see the heap property clearly.
    random.seed(42) 
    
    treap = Treap()
    
    # If we insert sorted data into a BST, it becomes a Linked List (O(N)).
    # Let's insert sorted data into the Treap!
    sorted_data = [10, 20, 30, 40, 50, 60, 70]
    
    print(f"Inserting perfectly sorted data: {sorted_data}")
    for key in sorted_data:
        treap.root = treap.insert(treap.root, key)
        
    print("\nFinal Treap Structure:")
    print_treap(treap.root)
    
    print("\nObserve the Structure:")
    print("1. Keys (K) strictly follow BST rules (Left is smaller, Right is larger).")
    print("2. Priorities (P) strictly follow Max-Heap rules (Parent is ALWAYS larger than children).")
    print("3. Because the priorities were random, the tree automatically avoided becoming a Linked List!")
    print("   We achieved expected O(log N) balance with a fraction of the code of an AVL Tree.")


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. What two properties define a Treap?
   Answer: Every node has a Key (which maintains the Binary Search Tree property) and a Priority (which maintains the Heap property).

2. How does a Treap prevent worst-case O(N) degradation when inserting sorted data?
   Answer: When you insert sorted data, a standard BST keeps attaching it to the right child. But in a Treap, that new right child is given a random Priority. If that random priority happens to be higher than its parent, the Treap executes a Left Rotation, pulling the new node up and pushing the parent down to the left. Over many insertions, this randomization perfectly scrambles the structure, keeping it roughly balanced.

3. Treaps vs Red-Black Trees. Which should I use?
   Answer: In a production database, Red-Black Trees are strictly preferred because they offer mathematically guaranteed O(log N) worst-case bounds. Treaps offer EXPECTED O(log N) bounds. However, in competitive programming or fast prototyping where writing 300 lines of Red-Black rotations is prone to bugs, a Treap can be written in 30 lines and performs identically well 99.99% of the time.
"""

if __name__ == "__main__":
    demonstrate_treap()
    print("\n[SUCCESS] Laboratory: Treaps Completed.")
