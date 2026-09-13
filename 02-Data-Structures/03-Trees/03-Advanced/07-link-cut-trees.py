"""
# ==============================================================================
# LABORATORY: LINK-CUT TREES (DYNAMIC FORESTS)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Heavy-Light Decomposition (HLD) is amazing for querying paths, but it requires 
# the Tree to be STATIC. If you add a new edge (`link`) or delete an edge (`cut`), 
# the entire HLD array flattening is destroyed, and you have to rebuild it in O(N).
# 
# A Link-Cut Tree solves the "Dynamic Forest" problem. It allows you to maintain 
# a forest of trees, query paths, link two trees together, or cut an edge to split 
# a tree into two—all in O(log N) amortized time!
# It achieves this by using Splay Trees to represent the "chains", because Splay 
# Trees can be easily split and merged dynamically.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the difference between the "Represented Tree" and the "Auxiliary Trees".
# - Understand the core `access(v)` operation.
# - Understand how `link(u, v)` and `cut(u, v)` work conceptually.
#
# ==============================================================================
"""

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. LINK-CUT TREE ARCHITECTURE (CONCEPTUAL)
# ==============================================================================
def explain_link_cut_architecture():
    section_header("Architecture: Represented Tree vs Auxiliary Tree")
    print("""
Like HLD, a Link-Cut Tree breaks the "Represented Tree" (the actual tree you care 
about) into a set of disjoint paths (Preferred Paths).

However, instead of flattening these paths into a 1D Array, each path is stored 
as an independent SPLAY TREE (called an "Auxiliary Tree").
- The Splay Tree is ordered by DEPTH. The left child of a node in the Splay Tree 
  is higher up (closer to the root) in the Represented Tree. The right child is 
  deeper down.
- There are multiple Splay Trees (one for each preferred path).
- The root of each Splay Tree has a special "Path Parent" pointer that points 
  to a node in a DIFFERENT Splay Tree, linking the forest together.
    """)


# ==============================================================================
# 4. THE CORE OPERATION: ACCESS(V)
# ==============================================================================
def explain_access_operation():
    section_header("The Engine: access(v)")
    print("""
The heart of a Link-Cut Tree is the `access(v)` operation.
Goal: Reconfigure the data structure so that there is a SINGLE continuous 
preferred path from the absolute Root of the Represented Tree down to node `v`.

How it works (Conceptually):
1. Start at node `v`. Splay `v` to the root of its current Auxiliary Splay Tree.
2. Sever the connection to its current right child (because `v` must be the 
   absolute deepest node in our new preferred path).
3. Follow `v`'s Path Parent pointer to reach the Splay Tree above it. Let's call 
   that node `u`.
4. Splay `u` to the root of its Auxiliary Splay Tree.
5. Sever `u`'s current right child, and make `v` its new right child! (This merges 
   the two preferred paths).
6. Repeat until you hit the absolute root of the Represented Tree.
7. Finally, Splay `v` one last time so `v` is the root of the single remaining 
   Splay Tree.

Once `access(v)` is called, the path from the Root to `v` is stored in a single 
Splay Tree, meaning you can find the Sum/Max/Min of that path instantly!
    """)


# ==============================================================================
# 5. LINK AND CUT OPERATIONS
# ==============================================================================
def explain_link_and_cut():
    section_header("Dynamic Operations: link(u, v) and cut(u, v)")
    
    print("--- LINK(u, v) ---")
    print("Goal: Draw an edge between node `u` and node `v` (where `v` is a root of another tree).")
    print("1. Call `access(u)` and Splay `u`.")
    print("2. Call `access(v)` and Splay `v`.")
    print("3. Simply set `v`'s Path Parent pointer to point to `u`.")
    print("Amortized Time: O(log N)\n")
    
    print("--- CUT(u, v) ---")
    print("Goal: Destroy the edge between `u` and `v` (assuming `u` is the parent).")
    print("1. Call `access(v)`.")
    print("   (This puts the path from the Root through `u` down to `v` into ONE Splay tree).")
    print("2. Splay `v`. Because `u` is the direct parent of `v` in the Represented Tree,")
    print("   `u` will be the LEFT child of `v` in the Splay Tree.")
    print("3. Sever the pointer: `v.left = None`. Also clear `u`'s parent pointer.")
    print("4. The trees are now split!")
    print("Amortized Time: O(log N)")


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why does a Link-Cut Tree use Splay Trees instead of Segment Trees for its paths?
   Answer: Segment Trees require a static array size. Because Link-Cut Trees support `link` and `cut` operations, the paths dynamically grow, shrink, merge, and split. Splay Trees are self-balancing binary search trees that can be split and merged in O(log N) time, making them the perfect underlying structure.

2. What is the difference between a "Left Child" in the Splay Tree and a "Left Child" in the Represented Tree?
   Answer: In the Represented Tree, children are just spatial relations. But inside the Auxiliary Splay Tree, the tree is strictly sorted by DEPTH. A Left Child in the Splay tree strictly means "this node is closer to the root of the Represented Tree than its parent".

3. Are Link-Cut Trees common in Software Engineering Interviews?
   Answer: Absolutely not. They are widely considered the hardest data structure taught in undergraduate computer science (if taught at all). They are strictly the domain of Advanced Competitive Programming and theoretical computer science.
"""

if __name__ == "__main__":
    explain_link_cut_architecture()
    explain_access_operation()
    explain_link_and_cut()
    print("\n[SUCCESS] Laboratory: Link-Cut Trees Completed.")
