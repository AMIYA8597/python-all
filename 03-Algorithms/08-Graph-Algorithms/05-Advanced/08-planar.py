"""
# ==============================================================================
# LABORATORY: PLANAR GRAPHS (EULER & KURATOWSKI)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You are designing a Printed Circuit Board (PCB) or a silicon microchip. 
# You have millions of transistors (Vertices) and microscopic copper wires (Edges).
# 
# Can you physically print this circuit onto a single flat 2D silicon wafer 
# WITHOUT any of the copper wires crossing over each other? (If they cross, 
# it causes a short-circuit and the chip explodes).
#
# In Graph Theory, a graph that can be drawn on a 2D plane without ANY edges 
# intersecting is called a "Planar Graph".
#
# - Euler's Formula (1752): For ANY connected planar graph, the relationship 
#   between Vertices (V), Edges (E), and enclosed 2D regions or Faces (F) is 
#   mathematically absolute: V - E + F = 2.
# 
# - The Edge Bound Theorem: Because planar graphs cannot have too many edges 
#   without forcing a crossover, it is mathematically proven that for any planar 
#   graph with V >= 3, the number of edges must satisfy: E <= 3V - 6.
#
# - Kuratowski's Theorem (1930): The Polish mathematician Kazimierz Kuratowski 
#   proved exactly WHAT makes a graph non-planar. A graph is non-planar if and 
#   only if it hides one of two specific structures inside it:
#   1. K_5: The "Complete Graph" of 5 nodes (a pentagram where everyone connects).
#   2. K_3,3: The "Complete Bipartite Graph" (The famous "Three Utilities Problem" 
#      where 3 houses must connect to Water, Gas, and Electric without crossing lines).
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Evaluate the O(1) Edge Bound check to instantly reject dense graphs.
# - Calculate Faces using Euler's Formula.
# - Understand the conceptual foundations of Kuratowski's Theorem.
#
# ==============================================================================
"""

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. PLANARITY MATHEMATICAL ENGINES
# ==============================================================================
def check_edge_bound(vertices: int, edges: int) -> bool:
    """
    O(1) mathematical check.
    If E > 3V - 6, it is mathematically IMPOSSIBLE for the graph to be planar.
    Note: This is a ONE-WAY check. If it passes, it MIGHT be planar, but it is 
    not guaranteed (e.g., K_3,3 passes this check but is not planar).
    """
    if vertices < 3:
        return True # Trivial graphs (1 or 2 nodes) are always planar
        
    maximum_allowed_edges = (3 * vertices) - 6
    
    if edges > maximum_allowed_edges:
        return False
    return True


def check_bipartite_edge_bound(vertices: int, edges: int) -> bool:
    """
    O(1) mathematical check for BIPARTITE graphs.
    Bipartite graphs have no triangles! Because the smallest cycle must be 4 edges, 
    the bounding constraint becomes even tighter: E <= 2V - 4.
    """
    if vertices < 3:
        return True
        
    maximum_allowed_edges = (2 * vertices) - 4
    
    if edges > maximum_allowed_edges:
        return False
    return True


def calculate_faces(vertices: int, edges: int, connected_components: int = 1) -> int:
    """
    Euler's Formula: V - E + F = 1 + C  (Where C is connected components).
    For a fully connected graph (C=1), V - E + F = 2.
    Therefore: F = 2 - V + E.
    (Note: The 'Faces' includes the 1 infinite infinite region outside the graph).
    """
    faces = (1 + connected_components) - vertices + edges
    return faces


# ==============================================================================
# 4. KURATOWSKI'S FORBIDDEN MINORS (CONCEPTUAL)
# ==============================================================================
def analyze_k5():
    """
    The K_5 graph is the Complete Graph on 5 vertices.
    Every vertex connects to every other vertex.
    """
    v = 5
    # In a complete graph, E = V(V-1)/2
    e = (5 * 4) // 2 # 10 edges
    
    print("\n[Analyzing K_5: The Complete Graph on 5 Nodes]")
    print(f"Vertices: {v}, Edges: {e}")
    
    is_potentially_planar = check_edge_bound(v, e)
    
    if not is_potentially_planar:
        print(f"FAILED EDGE BOUND! E ({e}) > 3V - 6 (which is {3*v - 6}).")
        print("Conclusion: K_5 is mathematically PROVEN to be Non-Planar!")


def analyze_k3_3():
    """
    The K_3,3 graph is the Complete Bipartite Graph (3 Houses, 3 Utilities).
    """
    v = 6 # 3 houses + 3 utilities
    # Every house connects to exactly 3 utilities.
    e = 3 * 3 # 9 edges
    
    print("\n[Analyzing K_3,3: The Three Utilities Problem]")
    print(f"Vertices: {v}, Edges: {e}")
    
    # 1. Standard Edge Bound Check
    is_potentially_planar = check_edge_bound(v, e)
    print(f"Standard Edge Bound (E <= 3V-6): 9 <= {3*6 - 6}. Passes! Seems planar?")
    
    # 2. Bipartite Edge Bound Check
    # Because it is bipartite, it MUST satisfy the tighter bound!
    is_actually_planar = check_bipartite_edge_bound(v, e)
    
    if not is_actually_planar:
        print(f"FAILED BIPARTITE BOUND! E ({e}) > 2V - 4 (which is {2*v - 4}).")
        print("Conclusion: K_3,3 is mathematically PROVEN to be Non-Planar!")


def demonstrate_planarity():
    section_header("Algorithm: Planar Graphs & Euler's Formula")
    
    # Let's test a simple square with an X in the middle (but the X doesn't intersect, 
    # one edge routes outside the square).
    v = 4
    e = 6 # 4 perimeter edges + 2 cross edges
    
    print(f"Validating a standard 4-node dense graph (V={v}, E={e}):")
    if check_edge_bound(v, e):
        print(" -> Edge bound satisfied. The graph can be drawn without crossing!")
        faces = calculate_faces(v, e)
        print(f" -> Euler's Formula proves it will enclose exactly {faces} 2D regions (faces)!")
    
    section_header("Kuratowski's Forbidden Subgraphs")
    print("Why do PCBs require multiple 'Layers' (e.g. 4-layer or 8-layer boards)?")
    print("Because complex circuits inherently contain K_5 and K_3,3 structures!")
    analyze_k5()
    analyze_k3_3()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why does the bound $E \le 3V - 6$ exist?
   Answer: In geometry, the most efficient way to pack 2D space with lines without them crossing is by creating Triangles. If a planar graph is "Maximal" (you literally cannot add a single new edge without crossing another), every single face in the graph is a triangle! Since every face is bounded by 3 edges, and every edge is shared by 2 faces, $3F = 2E$. If you substitute $F = 2E / 3$ into Euler's formula ($V - E + F = 2$), the algebra perfectly collapses into $E = 3V - 6$. 

2. How do compilers / real-world systems ACTUALLY check for planarity?
   Answer: They do not just check edge bounds (which are necessary but not sufficient). In 1974, John Hopcroft and Robert Tarjan (yes, Tarjan again!) invented the Hopcroft-Tarjan algorithm. It uses a highly complex DFS to partition the graph into "fragments" and attempts to embed them on the inside or outside of a cycle. It mathematically proves planarity in linear $O(V)$ time.

3. How does this apply to Map Coloring (The 4-Color Theorem)?
   Answer: A physical map (e.g., countries on Earth) is inherently a Planar Graph! The countries are Vertices, and if two countries share a border, there is an Edge between them. Because physical maps are strictly 2D planar, the 4-Color Theorem mathematically guarantees that you will NEVER need more than 4 colors to color any map in the universe!
"""

if __name__ == "__main__":
    demonstrate_planarity()
    print("\n[SUCCESS] Laboratory: Planar Graphs Completed.")
