"""
# ==============================================================================
# LABORATORY: MATROID THEORY (THE MATH OF GREEDY ALGORITHMS)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You've seen that Greedy Algorithms work perfectly for Kruskal's MST and 
# Job Sequencing with Deadlines, but fail catastrophically for 0/1 Knapsack.
#
# Is there a mathematical law that dictates EXACTLY when Greedy is allowed?
# Yes. In 1935, Hassler Whitney invented "Matroid Theory".
#
# A "Matroid" is a mathematical structure. If you can prove that your specific 
# problem fits the exact definition of a Matroid, then it is mathematically 
# GUARANTEED that a Greedy Algorithm will find the perfect optimal answer.
#
# A Matroid requires three things:
# 1. A finite set of elements `E` (e.g., all edges in a graph).
# 2. A collection of subsets `I` called "Independent Sets".
# 3. Two strict Axioms:
#    - Axiom A (Hereditary): If a set is valid, ANY subset of it is also valid.
#      (e.g., If 5 cables don't form a cycle, 4 of those cables also don't form a cycle).
#    - Axiom B (Exchange): If Set A is smaller than Set B, you can ALWAYS take 
#      an element from Set B, move it to Set A, and Set A will STILL be valid!
#
# If a problem violates the Hereditary or Exchange axioms, Greedy FAILS.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the Hereditary and Exchange (Augmentation) Axioms.
# - Prove why Kruskal's MST is a "Graphic Matroid".
# - Prove why 0/1 Knapsack is NOT a Matroid.
#
# ==============================================================================
"""

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. PROVING MATROID AXIOMS IN PYTHON
# ==============================================================================
def verify_hereditary_property(valid_set: set) -> bool:
    """
    Demonstrates the Hereditary Axiom.
    In a Graphic Matroid (like Kruskal's), an "Independent Set" is a set of 
    edges that DO NOT contain a cycle (a forest).
    """
    print("Axiom 1: Hereditary Property")
    print(f"Given a valid (cycle-free) set of edges: {valid_set}")
    
    # Let's remove an edge to create a subset.
    subset = valid_set.copy()
    removed_edge = subset.pop()
    
    print(f"If we remove {removed_edge}, the subset is: {subset}")
    print("Conclusion: If the original set had no cycles, it is mathematically ")
    print("impossible for a subset to suddenly HAVE a cycle! The property holds.")
    return True


def explain_knapsack_failure():
    section_header("Why 0/1 Knapsack is NOT a Matroid")
    
    print("Let's try to apply the Matroid Axioms to a 50 lb Knapsack.")
    print("Set E: {Item A: 30 lbs, Item B: 20 lbs, Item C: 40 lbs}")
    print("An 'Independent Set' is any combination that fits in 50 lbs.")
    
    print("\nDoes the Hereditary Axiom hold?")
    print("If {A, B} fits (30+20=50), does the subset {A} fit? Yes (30).")
    print("The Hereditary Axiom holds!")
    
    print("\nDoes the Exchange (Augmentation) Axiom hold?")
    print("Let Set A = {C}. Total weight = 40. (Size 1).")
    print("Let Set B = {A, B}. Total weight = 50. (Size 2).")
    print("Axiom says: Because Set B is larger, we MUST be able to take an item ")
    print("from B (either A or B) and add it to A, and it MUST remain valid.")
    
    print("\nLet's try:")
    print("1. Take Item A (30) from B, add to A: 40 + 30 = 70. OVER 50! Fails.")
    print("2. Take Item B (20) from B, add to A: 40 + 20 = 60. OVER 50! Fails.")
    
    print("\nConclusion:")
    print("The Exchange Axiom collapses completely! Because 0/1 Knapsack is NOT ")
    print("a Matroid, a Greedy Algorithm is mathematically forbidden. You MUST use DP.")


# ==============================================================================
# 4. THE GENERIC GREEDY MATROID ALGORITHM
# ==============================================================================
def generic_matroid_greedy(elements: list, weight_func, is_independent_func) -> list:
    """
    If you can prove a problem is a Matroid, this ONE algorithm solves it.
    This exact code solves Kruskal's MST, Job Sequencing, and more.
    """
    # 1. Sort elements by weight (Descending or Ascending depending on the goal)
    elements.sort(key=weight_func, reverse=True)
    
    optimal_set = []
    
    # 2. Iterate through elements
    for element in elements:
        
        # 3. Test independence (Axiom 1 guarantees this won't break previous choices)
        test_set = optimal_set + [element]
        if is_independent_func(test_set):
            optimal_set.append(element)
            
    return optimal_set


def demonstrate_matroid_theory():
    section_header("Algorithm: Matroid Theory")
    
    verify_hereditary_property({'Edge(0,1)', 'Edge(1,2)', 'Edge(2,3)'})
    explain_knapsack_failure()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. What is a "Graphic Matroid"?
   Answer: A Graphic Matroid is the specific application of matroid theory to graphs. The elements are the edges of the graph. An "Independent Set" is defined as any subset of edges that forms a Forest (contains absolutely no cycles). This is the mathematical framework that proves Kruskal's Algorithm works.

2. What is a "Transversal Matroid"?
   Answer: A Transversal Matroid applies to Bipartite Matching. The classic example is "Job Sequencing with Deadlines". The elements are the jobs. An "Independent Set" is a set of jobs that can all be successfully mapped to unique deadline slots without overlapping. Because it forms a Matroid, sorting by Profit and picking greedily is guaranteed to work!

3. Are you expected to write Matroid proofs in FAANG interviews?
   Answer: NO. Matroid theory is typically reserved for PhD-level computer science courses or highly theoretical algorithmic research. However, understanding WHY greedy fails (Exchange Axiom failure in Knapsack) is an incredible superpower that will instantly allow you to smell when an interviewer's problem requires DP instead of Greedy.
"""

if __name__ == "__main__":
    demonstrate_matroid_theory()
    print("\n[SUCCESS] Laboratory: Matroid Theory Completed.")
