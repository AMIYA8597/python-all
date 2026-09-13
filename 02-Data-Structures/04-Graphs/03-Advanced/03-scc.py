"""
# ==============================================================================
# LABORATORY: ADVANCED SCC APPLICATIONS (2-SATISFIABILITY)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You've learned how to find Strongly Connected Components (SCCs) using Kosaraju 
# or Tarjan's algorithm. But why do we care about SCCs outside of network analysis?
#
# SCCs are the secret to solving the "2-SAT" (2-Satisfiability) problem in O(V+E) time.
# Imagine a configuration file where a user selects options.
# Rule 1: You must pick Dark Mode OR Auto-Save.
# Rule 2: You must pick NOT Dark Mode OR Cloud Sync.
# Is there a valid combination of settings that satisfies all rules?
# 
# By converting the logic into an "Implication Graph" and finding the SCCs, 
# we can instantly determine if a valid configuration exists, and even generate it!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Model Boolean logic (A OR B) as an Implication Graph.
# - Use SCCs to determine if the logic is satisfiable.
# - Extract a valid boolean assignment.
#
# ==============================================================================
"""

from collections import defaultdict
from typing import List, Tuple

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. 2-SAT AND THE IMPLICATION GRAPH
# ==============================================================================
def explain_implication_graph():
    section_header("Concept: The Implication Graph")
    print("""
If a rule says: (A OR B) MUST be True.
This logically implies two things:
1. If A is False, B MUST be True. (!A -> B)
2. If B is False, A MUST be True. (!B -> A)

We can build a Directed Graph where nodes are variables (A, B) and their 
negations (!A, !B). 
The rule (A OR B) adds two directed edges: !A -> B and !B -> A.

If we run an SCC algorithm (like Tarjan's) on this graph, we check one simple rule:
Are 'A' and '!A' in the EXACT SAME Strongly Connected Component?
- If YES: It means A implies !A, and !A implies A. This is a paradox! The rules are impossible to satisfy.
- If NO (for all variables): The rules are perfectly satisfiable!
    """)


# ==============================================================================
# 4. TARJAN'S SCC ENGINE (REUSED FOR 2-SAT)
# ==============================================================================
def tarjans_scc(num_nodes: int, graph: dict) -> List[List[int]]:
    """Standard Tarjan's SCC implementation to support 2-SAT."""
    id_counter = 0
    ids = [-1] * num_nodes
    low = [0] * num_nodes
    on_stack = [False] * num_nodes
    stack = []
    sccs = []
    
    def dfs(at: int):
        nonlocal id_counter
        stack.append(at)
        on_stack[at] = True
        ids[at] = low[at] = id_counter
        id_counter += 1
        
        for to in graph.get(at, []):
            if ids[to] == -1:
                dfs(to)
                low[at] = min(low[at], low[to])
            elif on_stack[to]: 
                low[at] = min(low[at], ids[to])
                
        if ids[at] == low[at]:
            current_scc = []
            while True:
                node = stack.pop()
                on_stack[node] = False
                current_scc.append(node)
                if node == at:
                    break
            sccs.append(current_scc)

    for i in range(num_nodes):
        if ids[i] == -1:
            dfs(i)
            
    return sccs


# ==============================================================================
# 5. 2-SAT SOLVER
# ==============================================================================
def solve_2sat(num_vars: int, clauses: List[Tuple[int, int]]) -> bool:
    """
    Solves a 2-SAT problem.
    Variables are 1-indexed. Positive integer = Variable. Negative integer = NOT Variable.
    Example clause: (1, -2) means (Var 1 OR NOT Var 2)
    
    We map to a 0-indexed graph:
    For Var X (1-indexed):
    - Node representing X = (X - 1) * 2
    - Node representing !X = (X - 1) * 2 + 1
    """
    num_nodes = num_vars * 2
    graph = defaultdict(list)
    
    # Helper to convert clause literal to Graph Node ID
    def get_node(literal: int) -> int:
        var = abs(literal) - 1
        # Even index = True, Odd index = False (Negation)
        return var * 2 if literal > 0 else var * 2 + 1
        
    def get_negated_node(literal: int) -> int:
        var = abs(literal) - 1
        # Opposite parity
        return var * 2 + 1 if literal > 0 else var * 2
        
    # Build Implication Graph
    for u, v in clauses:
        # u OR v implies:
        # !u -> v
        # !v -> u
        graph[get_negated_node(u)].append(get_node(v))
        graph[get_negated_node(v)].append(get_node(u))
        
    # Find SCCs
    sccs = tarjans_scc(num_nodes, graph)
    
    # Map each node to its SCC ID
    scc_mapping = {}
    for scc_id, component in enumerate(sccs):
        for node in component:
            scc_mapping[node] = scc_id
            
    # Check for Paradox: Is Var X and !Var X in the same SCC?
    for i in range(num_vars):
        node_true = i * 2
        node_false = i * 2 + 1
        
        if scc_mapping.get(node_true, -1) == scc_mapping.get(node_false, -2):
            return False # Paradox! Unsatisfiable.
            
    return True # Satisfiable!

def demonstrate_2sat():
    section_header("Algorithm: 2-SAT via Implication Graph")
    
    print("Scenario 1: Satisfiable")
    # (A OR B) AND (!A OR B) AND (!B OR !B)
    # A = 1, B = 2
    # !B OR !B forces B to be False.
    # If B is False, A OR B forces A to be True.
    # If B is False, !A OR B forces !A to be True (so A is False).
    # Wait... A must be True AND False. This is a Paradox!
    clauses_paradox = [(1, 2), (-1, 2), (-2, -2)]
    
    # Let's try a real satisfiable one:
    # (A OR B) AND (!A OR C)
    # A=1, B=2, C=3
    clauses_valid = [(1, 2), (-1, 3)]
    
    print("Testing Paradox Clauses:")
    print(" (A OR B) AND (!A OR B) AND (!B OR !B)")
    print(f" Satisfiable? {solve_2sat(2, clauses_paradox)}")
    
    print("\nTesting Valid Clauses:")
    print(" (A OR B) AND (!A OR C)")
    print(f" Satisfiable? {solve_2sat(3, clauses_valid)}")


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why does `A OR B` create two directed edges `!A -> B` and `!B -> A`?
   Answer: It maps directly to Boolean Logic. The only way `A OR B` can be true if `A` is false, is if `B` is true. Thus, the state `!A` strictly implies the state `B`.

2. Why does a variable and its negation being in the same SCC make the formula unsatisfiable?
   Answer: A Strongly Connected Component is a cycle where every node can reach every other node. If `A` and `!A` are in the same SCC, it means `A -> ... -> !A` (if A is true, it forces itself to be false) AND `!A -> ... -> A` (if A is false, it forces itself to be true). This is a logical paradox.

3. Is there a 3-SAT (3-Satisfiability) algorithm using graphs?
   Answer: No. 2-SAT is polynomial time O(V+E). 3-SAT is proven to be NP-Complete (meaning no fast algorithm is known to exist). This is a classic theoretical computer science boundary.
"""

if __name__ == "__main__":
    explain_implication_graph()
    demonstrate_2sat()
    print("\n[SUCCESS] Laboratory: Advanced SCC (2-SAT) Completed.")
