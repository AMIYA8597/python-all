"""
# ==============================================================================
# LABORATORY: RED-BLACK TREES
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# While AVL Trees guarantee perfect O(log N) balance, they do so by performing 
# expensive rotations constantly during insertions and deletions. 
# Red-Black (RB) Trees offer a compromise: "Loose Balancing". They guarantee that 
# the longest path from root to leaf is no more than TWICE the length of the 
# shortest path. This guarantees O(log N) search, but requires far fewer 
# rotations when writing data. 
# Red-Black Trees are the industry standard for in-memory ordered data structures 
# (e.g., C++ `std::map`, Java `TreeMap`, and the Linux Completely Fair Scheduler).
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the 5 Rules of Red-Black Trees.
# - Understand the trade-off between AVL Trees (Read-Heavy) and RB Trees (Write-Heavy).
# - Validate the Black-Height property of a Red-Black Tree.
#
# ==============================================================================
"""

from typing import Optional, Tuple

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE 5 RULES OF RED-BLACK TREES
# ==============================================================================
def explain_rb_rules():
    section_header("The 5 Rules of Red-Black Trees")
    print("""
To maintain its "loose" balance, every node is painted Red or Black. 
The tree MUST satisfy these 5 rules at all times:

1. Every node is either Red or Black.
2. The Root is ALWAYS Black.
3. Every leaf (NIL/None pointer) is considered Black.
4. If a node is Red, BOTH of its children MUST be Black. 
   (Meaning: You can NEVER have two Red nodes in a row).
5. (The Black-Height Rule): For any given node, every path from that node 
   down to its leaves must contain the EXACT SAME number of Black nodes.

Because of Rule 4 and Rule 5, the longest possible path (alternating 
Black-Red-Black-Red...) can be at most twice as long as the shortest possible 
path (all Black). This guarantees the tree's height is O(log N).
    """)


# ==============================================================================
# 4. RED-BLACK TREE VALIDATOR
# ==============================================================================
class RBNode:
    def __init__(self, val: int, color: str):
        self.val = val
        self.color = color # "RED" or "BLACK"
        self.left: Optional['RBNode'] = None
        self.right: Optional['RBNode'] = None

def validate_rb_tree(root: Optional[RBNode]) -> bool:
    """
    Validates if a given tree satisfies the Red-Black properties.
    Specifically checks Rule 4 (No consecutive Reds) and Rule 5 (Equal Black-Height).
    """
    if not root:
        return True
        
    if root.color != "BLACK":
        print("Violation: Root must be BLACK.")
        return False
        
    def check_node(node: Optional[RBNode]) -> Tuple[bool, int]:
        """Returns (is_valid, black_height)"""
        if not node:
            # Rule 3: NIL nodes are BLACK, so they contribute 1 to the black-height
            return True, 1
            
        # Rule 4: Check for consecutive reds
        if node.color == "RED":
            if (node.left and node.left.color == "RED") or \
               (node.right and node.right.color == "RED"):
                print(f"Violation: Node {node.val} is RED and has a RED child.")
                return False, 0
                
        # Recursively check left and right subtrees
        left_valid, left_bh = check_node(node.left)
        right_valid, right_bh = check_node(node.right)
        
        if not left_valid or not right_valid:
            return False, 0
            
        # Rule 5: Black-heights of left and right MUST match
        if left_bh != right_bh:
            print(f"Violation: Black-Height mismatch at Node {node.val}. Left={left_bh}, Right={right_bh}")
            return False, 0
            
        # Calculate this node's contribution to the black-height
        current_bh = left_bh + (1 if node.color == "BLACK" else 0)
        
        return True, current_bh

    is_valid, _ = check_node(root)
    return is_valid

def demonstrate_validator():
    section_header("Validating Red-Black Properties")
    
    # 1. Build a VALID Red-Black Tree
    #          10(B)
    #         /     \
    #      5(R)     15(R)
    #     /   \     /   \
    #  2(B)  7(B) 12(B) 20(B)
    
    valid_root = RBNode(10, "BLACK")
    valid_root.left = RBNode(5, "RED")
    valid_root.right = RBNode(15, "RED")
    
    valid_root.left.left = RBNode(2, "BLACK")
    valid_root.left.right = RBNode(7, "BLACK")
    valid_root.right.left = RBNode(12, "BLACK")
    valid_root.right.right = RBNode(20, "BLACK")
    
    print("Testing Valid RB Tree:")
    print(f"Result: {validate_rb_tree(valid_root)}\n")
    
    # 2. Build an INVALID Red-Black Tree (Consecutive Reds)
    invalid_red = RBNode(10, "BLACK")
    invalid_red.left = RBNode(5, "RED")
    invalid_red.left.left = RBNode(2, "RED") # Violation!
    
    print("Testing Invalid RB Tree (Consecutive Reds):")
    print(f"Result: {validate_rb_tree(invalid_red)}\n")
    
    # 3. Build an INVALID Red-Black Tree (Black-Height Mismatch)
    #          10(B)
    #         /     \
    #      5(B)     15(R)  <-- Right path has fewer black nodes
    invalid_bh = RBNode(10, "BLACK")
    invalid_bh.left = RBNode(5, "BLACK")
    invalid_bh.right = RBNode(15, "RED")
    
    print("Testing Invalid RB Tree (Black-Height Mismatch):")
    print(f"Result: {validate_rb_tree(invalid_bh)}")


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why does the Linux Kernel use Red-Black trees instead of AVL trees for process scheduling?
   Answer: The Linux scheduler (CFS) must constantly insert new tasks and remove finished tasks. AVL trees are too strictly balanced, meaning they waste CPU cycles performing rotations on every insert/delete. Red-Black trees are "loosely" balanced, guaranteeing O(log N) search times while minimizing rotation overhead during writes.

2. What does the "Black-Height" property guarantee?
   Answer: It guarantees that every path from a node to its leaves has the exact same number of black nodes. Combined with the rule that you cannot have two consecutive red nodes, this mathematically guarantees that the longest possible path (B-R-B-R-B) is at most exactly twice as long as the shortest possible path (B-B-B).

3. When inserting a new node into an RB Tree, what color is it initially painted?
   Answer: It is always painted RED initially. This prevents it from immediately violating the Black-Height rule (Rule 5). We then check if it violated Rule 4 (consecutive reds with its parent), and if so, we fix it using recoloring or rotations.
"""

if __name__ == "__main__":
    explain_rb_rules()
    demonstrate_validator()
    print("\n[SUCCESS] Laboratory: Red-Black Trees Completed.")
