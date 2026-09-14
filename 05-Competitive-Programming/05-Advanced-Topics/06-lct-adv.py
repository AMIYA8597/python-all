"""
# ==============================================================================
# LABORATORY: COMPETITIVE PROGRAMMING (LINK/CUT TREES)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You are given a Graph of 100,000 nodes.
# You must handle three types of queries online (in real-time):
# 1. Add an edge between Node U and Node V (Link).
# 2. Remove the edge between Node U and Node V (Cut).
# 3. Find the maximum value on the path between Node U and Node V.
#
# Disjoint Set Union (DSU) can Link, but it CANNOT Cut.
# Heavy-Light Decomposition (HLD) can query paths in O(log^2 N), but it requires 
# the Tree to be strictly STATIC. It cannot Link or Cut edges.
#
# Enter the Link/Cut Tree (invented by Sleator and Tarjan). It is the absolute 
# pinnacle of Graph Data Structures. It mathematically maintains a "Dynamic Forest". 
# It can Link trees, Cut trees, and query arbitrary paths all in strictly 
# O(log N) amortized time!
#
# It does this by abandoning static arrays and replacing HLD's straight chains 
# with "Splay Trees" (Self-Balancing Binary Search Trees). The Splay Trees 
# physically rotate and re-organize themselves at runtime to mathematically force 
# the queried path to the absolute top of the data structure!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the architecture of Splay Trees representing Paths.
# - Understand the magical `access()` function that exposes a path to the root.
# - Understand Link and Cut operations.
#
# ==============================================================================
"""

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. LINK/CUT TREE ARCHITECTURE
# ==============================================================================
class LCTNode:
    def __init__(self, key: int):
        self.key = key
        # Left and Right children IN THE SPLAY TREE!
        # (A Splay Tree represents a single top-to-bottom Path in the actual graph).
        self.left = None
        self.right = None
        self.parent = None
        
        # Path-Parent pointer (The dashed line in LCT architecture).
        # This points from the Root of a Splay Tree to a node in a DIFFERENT Splay Tree.
        self.path_parent = None
        
        # We can store values here (e.g., maximum on path) and update them during rotations.
        # self.value = ...
        # self.max_val = ...
        
        # Lazy propagation tag for reversing paths
        self.reverse_flag = False

class LinkCutTree:
    """
    A conceptual implementation to demonstrate the architecture.
    A full production-ready LCT in Python requires ~250 lines of complex Splay 
    Tree rotation logic (zig, zag, zig-zig, zig-zag) which is beyond the scope 
    of a single textbook file, but the architectural operations are fully explained here.
    """
    
    def __init__(self):
        # We create independent nodes. They start as a forest of N disconnected trees.
        pass

    def _is_root(self, node: LCTNode) -> bool:
        """
        Is this node the root of its current Splay Tree?
        In a Splay Tree, if you have a parent, you MUST be one of its children!
        If your parent doesn't acknowledge you as a child, you are the Root of 
        your Splay Tree, and that parent pointer is actually a Path-Parent pointer!
        """
        return node.parent is None

    def _splay(self, node: LCTNode) -> None:
        """
        The engine of the LCT. 
        Physically rotates the binary tree to bring `node` to the absolute root 
        of its Splay Tree. (Implementation omitted for brevity).
        """
        pass

    def access(self, node: LCTNode) -> None:
        """
        The absolute core magic of the Link/Cut Tree!
        It mathematically forces `node`, and every node on the path from `node` 
        to the absolute Root of the entire Graph, to belong to the EXACT SAME 
        Splay Tree!
        
        Once `access(node)` is called, the right-child of `node` is severed 
        (because the path ends at `node`), making `node` the absolute deepest 
        node in its Splay Tree.
        """
        # 1. Splay the node to the top of its current local Splay Tree.
        self._splay(node)
        
        # 2. Sever its right child (because the path we care about ends at `node`).
        # The severed right child becomes its own independent Splay Tree!
        if node.right:
            node.right.parent = None
            node.right.path_parent = node
            node.right = None
            # Update node's internal values (e.g., max_val) since it lost a child.
            
        # 3. Walk UP the path-parent pointers, fusing Splay Trees together!
        current = node
        while current.path_parent is not None:
            parent_splay_root = current.path_parent
            
            # Splay the parent to the top of ITS local Splay Tree
            self._splay(parent_splay_root)
            
            # Sever the parent's current right child
            if parent_splay_root.right:
                parent_splay_root.right.parent = None
                parent_splay_root.right.path_parent = parent_splay_root
                
            # Attach our current Splay Tree as the parent's NEW right child!
            parent_splay_root.right = current
            current.parent = parent_splay_root
            current.path_parent = None
            
            # Update parent's internal values
            
            # Move up
            current = parent_splay_root
            
        # Final Splay to bring the originally requested node to the absolute 
        # root of this newly fused, massive Splay Tree!
        self._splay(node)

    def make_root(self, node: LCTNode) -> None:
        """
        Magically alters the physical structure of the Graph so that `node` 
        becomes the absolute Root of the entire tree it belongs to!
        """
        # 1. Access it, fusing the path from `node` to the old Root.
        self.access(node)
        
        # 2. Because `node` is now at the top of the Splay Tree, and the path 
        # ends at `node`, the entire path is mathematically contained in its LEFT branch!
        # By reversing the Left branch (lazy propagation), we mathematically invert 
        # the entire path, instantly making `node` the new Root of the Graph!
        node.reverse_flag = not node.reverse_flag

    def link(self, u: LCTNode, v: LCTNode) -> None:
        """
        Adds a physical edge between disconnected trees U and V.
        """
        # 1. Make U the absolute root of its tree.
        self.make_root(u)
        
        # 2. Access V to bring it to the root of its tree.
        self.access(v)
        
        # 3. Mathematically attach U as a child of V using a Path-Parent pointer!
        u.path_parent = v

    def cut(self, u: LCTNode, v: LCTNode) -> None:
        """
        Physically removes the edge between U and V.
        """
        # 1. Make U the absolute root of the tree.
        self.make_root(u)
        
        # 2. Access V. Because U is the root, V is deeper. 
        # Fusing the path guarantees U and V are in the exact same Splay Tree.
        self.access(v)
        
        # 3. Because U and V are directly connected by an edge in the Graph, 
        # and U is the Root, U is mathematically guaranteed to be the LEFT CHILD of V 
        # in the Splay Tree!
        if v.left == u:
            v.left = None
            u.parent = None
            # The edge is destroyed!

def demonstrate_lct():
    section_header("Link/Cut Tree (Dynamic Forests)")
    
    print("Architectural Breakdown:")
    print("1. Instead of static 1D Arrays (HLD), LCT uses Dynamic Splay Trees.")
    print("2. A Splay Tree perfectly represents a contiguous PATH in the Graph.")
    print("3. The `access(u)` function violently reorganizes the trees to form a ")
    print("   single contiguous path from `u` to the Root.")
    print("4. `make_root(u)` utilizes Lazy Reversal (`reverse_flag`) to instantly ")
    print("   invert a path, making `u` the new mathematical Root of the Graph.")
    print("5. With `make_root` and `access`, `link()` and `cut()` are mathematically ")
    print("   reduced to trivial pointer assignments in O(log N) amortized time!")
    print("\nLCT is considered the ultimate endpoint of Tree Algorithms.")


def run_all_labs():
    demonstrate_lct()


# ==============================================================================
# 4. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. What is the fundamental difference in how Heavy-Light Decomposition (HLD) and Link/Cut Trees (LCT) handle straight paths (Chains)?
   Answer: HLD analyzes the tree statically and assigns every node a permanent, rigid index in a massive 1D array. Heavy chains are physically contiguous blocks of memory. This allows blazing fast $O(\log^2 N)$ queries via Segment Tree, but absolutely forbids changing the structure of the tree. LCT completely discards the static array. Instead, every single "Chain" is physically represented by an independent, self-balancing Splay Tree. Because Splay Trees can be dynamically split and merged in $O(\log N)$ time, LCT can violently sever edges and fuse new branches at runtime, maintaining flawless performance on Dynamic Forests.

2. In the LCT `access(node)` function, why do we mathematically sever the `right` child of the node before traversing up the path-parent pointers?
   Answer: In a Splay Tree representing a path, the structural rule is strict: Left children are geometrically "higher up" (closer to the Root) on the path, and Right children are geometrically "deeper" on the path. When we call `access(node)`, our goal is to isolate the specific path from the Root exactly down to `node`. If `node` had a right child, that child would represent nodes that are geometrically *deeper* than `node`! Since we want the path to terminate precisely at `node`, we must mathematically sever the right child. The severed child isn't deleted; it simply transforms into the Root of its own independent Splay Tree!

3. Explain the sheer mathematical brilliance of the `make_root(node)` function using the `reverse_flag`.
   Answer: If you want to change the Root of a tree, you normally have to run a full DFS/BFS to invert all the parent-child pointers along the path, taking $O(N)$ time. LCT solves this instantly. First, `access(node)` fuses the entire path from `node` up to the old Root into a single Splay Tree. Because `node` is the deepest element on this path, the entire path rests in its Left branch. To invert the parent-child relationships, we simply need to flip the depth geometry! By tagging `node.reverse_flag = True`, the Splay Tree will lazily swap Left and Right children as it traverses. This mathematically inverts the depths in $O(1)$ time, instantly turning the absolute deepest node into the absolute highest node (the new Root)!
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Advanced Topics (Link/Cut Trees) Completed.")
