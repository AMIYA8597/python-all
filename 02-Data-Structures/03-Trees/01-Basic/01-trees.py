"""
# ==============================================================================
# LABORATORY: N-ARY TREES (GENERAL TREES)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# While Binary Trees are heavily tested in interviews, most real-world hierarchical 
# data structures are N-ary Trees (a node can have any number of children). 
# The File System on your OS, the DOM in a web browser, and the organizational 
# chart of a company are all N-ary Trees.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Build an N-ary Tree Node using a list of children.
# - Simulate a File System hierarchy.
# - Master DFS traversal for an N-ary tree.
# - Master BFS traversal for an N-ary tree.
#
# ==============================================================================
"""

from collections import deque
from typing import List, Any

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. N-ARY TREE NODE & CONSTRUCTION
# ==============================================================================
class TreeNode:
    """An N-ary Tree node holds data and a list of children pointers."""
    def __init__(self, val: Any):
        self.val = val
        self.children: List['TreeNode'] = []
        
    def add_child(self, node: 'TreeNode') -> 'TreeNode':
        self.children.append(node)
        return self

def build_file_system() -> TreeNode:
    """
    Builds the following N-ary tree:
                    root
                 /   |   \
               usr  bin  etc
              / | \       |
           bin lib local  nginx
    """
    root = TreeNode("root")
    
    usr = TreeNode("usr")
    bin_dir = TreeNode("bin")
    etc = TreeNode("etc")
    
    root.add_child(usr).add_child(bin_dir).add_child(etc)
    
    usr.add_child(TreeNode("bin"))
    usr.add_child(TreeNode("lib"))
    usr.add_child(TreeNode("local"))
    
    etc.add_child(TreeNode("nginx"))
    
    return root


# ==============================================================================
# 4. N-ARY DEPTH-FIRST SEARCH (DFS)
# ==============================================================================
def dfs_n_ary(node: TreeNode, depth: int = 0):
    """
    Traverses the tree deeply, printing with indentation to visualize depth.
    Notice there is no 'in-order' traversal for an N-ary tree because there is 
    no distinct 'left' and 'right'. We usually just do pre-order (process node, 
    then children).
    """
    # 1. Process the current node
    indent = "  " * depth
    print(f"{indent}|-- {node.val}")
    
    # 2. Recursively process all children
    for child in node.children:
        dfs_n_ary(child, depth + 1)

def demonstrate_dfs():
    section_header("N-ary DFS (File System Traversal)")
    root = build_file_system()
    print("Executing DFS to print directory structure:\n")
    dfs_n_ary(root)


# ==============================================================================
# 5. N-ARY BREADTH-FIRST SEARCH (BFS)
# ==============================================================================
def bfs_n_ary(root: TreeNode) -> List[List[Any]]:
    """
    Explores the N-ary tree level by level.
    Used when searching for the "closest" file or shortest path in a hierarchy.
    """
    if not root:
        return []
        
    result = []
    queue = deque([root])
    
    while queue:
        level_size = len(queue)
        current_level = []
        
        for _ in range(level_size):
            node = queue.popleft()
            current_level.append(node.val)
            
            # Enqueue all children of the current node
            for child in node.children:
                queue.append(child)
                
        result.append(current_level)
        
    return result

def demonstrate_bfs():
    section_header("N-ary BFS (Level-Order Traversal)")
    root = build_file_system()
    levels = bfs_n_ary(root)
    
    print("Executing BFS:\n")
    for i, level in enumerate(levels):
        print(f"Depth {i}: {level}")


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. What is the structural difference between a Binary Tree Node and an N-ary Tree Node?
   Answer: A Binary Tree node has strict `left` and `right` attributes (pointers). An N-ary tree node has a `children` attribute, which is a list (array) of pointers to its child nodes.

2. Why doesn't "In-Order" traversal exist for an N-ary tree?
   Answer: In-Order traversal implies visiting the left side, then the root, then the right side. In an N-ary tree with potentially 5 children, there is no logical "middle" point to visit the root. You can only do Pre-order (root before children) or Post-order (children before root).

3. If you want to build a feature that searches your entire hard drive for a specific file name, which traversal should you use and why?
   Answer: Both DFS and BFS will find the file in O(N) time. However, if you are looking for a system file that is likely near the root of the drive (e.g., in `/etc`), BFS will find it much faster. If you are looking for a deeply buried text document inside `User/Documents/Work/Projects`, DFS might find it faster (depending on branch order). The OS typically uses DFS to conserve memory (O(H) vs O(W)).
"""

if __name__ == "__main__":
    demonstrate_dfs()
    demonstrate_bfs()
    print("\n[SUCCESS] Laboratory: N-ary Trees Completed.")
