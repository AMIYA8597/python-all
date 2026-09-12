"""
Advanced Graph Problems

Overview:
This module dives deep into advanced graph theory algorithms that form the backbone
of modern computing infrastructure, compiler optimization, network routing, and
competitive programming. The core algorithms discussed are Strongly Connected Components
(Tarjan's and Kosaraju's), Eulerian Paths/Circuits (Hierholzer's), and 2-Satisfiability (2-SAT).

Learning Objectives:
1. Understand the theoretical foundations of Strongly Connected Components (SCCs).
2. Implement and contrast Tarjan's Algorithm and Kosaraju's Algorithm for SCCs.
3. Master Hierholzer's Algorithm to find Eulerian Paths and Circuits.
4. Reduce Boolean Satisfiability (2-SAT) problems to Graph Theory and solve using SCCs.

-------------------------------------------------------------------------------
1. Strongly Connected Components (SCC)
-------------------------------------------------------------------------------
A directed graph is "strongly connected" if there is a path between all pairs of vertices.
An SCC is a maximal subgraph that is strongly connected.

Tarjan's Algorithm:
- Uses a single Depth First Search (DFS).
- Maintains `disc` (discovery time) and `low` (lowest discovery time reachable from the node).
- A node is the root of an SCC if `low[u] == disc[u]`.
- Time Complexity: O(V + E)
- Space Complexity: O(V) for recursion stack and arrays.

Kosaraju's Algorithm:
- Uses two DFS passes.
- Pass 1: DFS on the original graph to push vertices to a stack upon completion.
- Pass 2: DFS on the transposed (reversed edges) graph in the order of the stack.
- Highly intuitive but theoretically slightly slower due to two passes and graph transposition.
- Time Complexity: O(V + E)
- Space Complexity: O(V) for stack and transposed graph.

-------------------------------------------------------------------------------
2. Eulerian Paths and Circuits (Hierholzer's Algorithm)
-------------------------------------------------------------------------------
An Eulerian Path is a trail in a finite graph that visits every edge exactly once.
An Eulerian Circuit is an Eulerian Path that starts and ends on the same vertex.

Conditions (Directed Graph):
- Eulerian Circuit: Every vertex has strictly equal in-degree and out-degree.
- Eulerian Path: At most one vertex has (out - in) = 1 (start node), at most one
  vertex has (in - out) = 1 (end node), and all others have equal in and out degrees.
  
Hierholzer's Algorithm:
- Start at the appropriate start node.
- Follow a trail of edges until you get stuck. Since the degree conditions hold, you
  will only get stuck at the end node.
- Push the stuck node to the result and backtrack.
- Reverse the result to get the path.
- Time Complexity: O(V + E)
- Space Complexity: O(V + E)

-------------------------------------------------------------------------------
3. 2-Satisfiability (2-SAT)
-------------------------------------------------------------------------------
A boolean formula in 2-CNF consists of an AND of OR clauses, each containing 2 literals.
Example: (A OR B) AND (~A OR C) AND (B OR ~C)

Reduction to Graph Theory:
- (A OR B) is logically equivalent to (~A -> B) and (~B -> A).
- Create a directed implication graph.
- A formula is satisfiable if and only if no variable x and its negation ~x belong to the same SCC.
- We can find a valid truth assignment by processing SCCs in reverse topological order.
- Time Complexity: O(V + E), where V is variables and E is clauses.

-------------------------------------------------------------------------------
Industry Applications:
- Tarjan's SCC: Garbage collection (detecting reference cycles), packaging dependencies.
- Eulerian Paths: DNA sequencing (De Bruijn graphs), route planning.
- 2-SAT: Dependency resolution systems, automated theorem proving, circuit design.
"""

from typing import List, Dict, Set, Tuple, Optional
from collections import defaultdict


class TarjanSCC:
    """
    Tarjan's algorithm for finding Strongly Connected Components.
    """
    def __init__(self, n: int):
        self.n = n
        self.graph: List[List[int]] = [[] for _ in range(n)]
        self.time = 0
        
    def add_edge(self, u: int, v: int) -> None:
        """Adds a directed edge from u to v."""
        self.graph[u].append(v)
        
    def get_sccs(self) -> List[List[int]]:
        """
        Executes Tarjan's Algorithm.
        Returns a list of SCCs, where each SCC is a list of node indices.
        """
        # disc[i] stores the discovery time of node i
        disc = [-1] * self.n
        # low[i] stores the lowest discovery time reachable from node i
        low = [-1] * self.n
        # Tracks nodes currently in the recursion stack
        stack_member = [False] * self.n
        stack: List[int] = []
        result: List[List[int]] = []
        
        def _dfs(u: int) -> None:
            disc[u] = self.time
            low[u] = self.time
            self.time += 1
            stack_member[u] = True
            stack.append(u)
            
            # Explore all neighbors
            for v in self.graph[u]:
                if disc[v] == -1:
                    # If v is not visited, recurse on it
                    _dfs(v)
                    # Tree edge: update low[u] with low[v]
                    low[u] = min(low[u], low[v])
                elif stack_member[v]:
                    # Back-edge found: v is in the current DFS path
                    low[u] = min(low[u], disc[v])
                    
            # If u is the root of an SCC
            if low[u] == disc[u]:
                scc = []
                while True:
                    v = stack.pop()
                    stack_member[v] = False
                    scc.append(v)
                    if u == v:
                        break
                result.append(scc)
                
        # Handle disconnected graphs
        for i in range(self.n):
            if disc[i] == -1:
                _dfs(i)
                
        return result


class KosarajuSCC:
    """
    Kosaraju's algorithm for finding Strongly Connected Components.
    """
    def __init__(self, n: int):
        self.n = n
        self.graph: List[List[int]] = [[] for _ in range(n)]
        self.reversed_graph: List[List[int]] = [[] for _ in range(n)]
        
    def add_edge(self, u: int, v: int) -> None:
        """Adds a directed edge from u to v."""
        self.graph[u].append(v)
        self.reversed_graph[v].append(u)
        
    def get_sccs(self) -> List[List[int]]:
        """
        Executes Kosaraju's Algorithm.
        """
        visited = [False] * self.n
        stack: List[int] = []
        
        # Pass 1: Fill vertices in stack according to their finishing times
        def fill_order(u: int):
            visited[u] = True
            for v in self.graph[u]:
                if not visited[v]:
                    fill_order(v)
            stack.append(u)
            
        for i in range(self.n):
            if not visited[i]:
                fill_order(i)
                
        # Pass 2: Process all vertices in order defined by Stack
        visited = [False] * self.n
        result: List[List[int]] = []
        
        def _dfs_reversed(u: int, scc: List[int]):
            visited[u] = True
            scc.append(u)
            for v in self.reversed_graph[u]:
                if not visited[v]:
                    _dfs_reversed(v, scc)
                    
        while stack:
            u = stack.pop()
            if not visited[u]:
                scc: List[int] = []
                _dfs_reversed(u, scc)
                result.append(scc)
                
        return result


class EulerianPathSolver:
    """
    Solves Eulerian Path and Circuit problems in Directed Graphs.
    """
    def __init__(self, edges: List[Tuple[str, str]]):
        self.graph = defaultdict(list)
        self.in_degree = defaultdict(int)
        self.out_degree = defaultdict(int)
        self.nodes = set()
        
        # Build graph and compute degrees
        for u, v in edges:
            self.graph[u].append(v)
            self.out_degree[u] += 1
            self.in_degree[v] += 1
            self.nodes.add(u)
            self.nodes.add(v)
            
        # Optional: Sort neighbors for lexical ordering (useful for problems like LeetCode 332)
        for k in self.graph:
            self.graph[k].sort(reverse=True)
            
    def _find_start_node(self) -> Optional[str]:
        """
        Determines the starting node for the Eulerian Path.
        Returns None if no Eulerian path is possible.
        """
        start_node = None
        end_node = None
        
        for node in self.nodes:
            out_d = self.out_degree[node]
            in_d = self.in_degree[node]
            
            if out_d - in_d == 1:
                if start_node is not None:
                    return None  # More than one node has out - in = 1
                start_node = node
            elif in_d - out_d == 1:
                if end_node is not None:
                    return None  # More than one node has in - out = 1
                end_node = node
            elif out_d != in_d:
                return None  # Node violates degree conditions
                
        # If no start node found (Eulerian Circuit), pick any node with outgoing edges
        if start_node is None:
            for node in self.nodes:
                if self.out_degree[node] > 0:
                    return node
        return start_node
        
    def find_eulerian_path(self) -> Optional[List[str]]:
        """
        Executes Hierholzer's Algorithm to find the Eulerian path/circuit.
        """
        start_node = self._find_start_node()
        if start_node is None:
            return None  # No Eulerian path exists
            
        route = []
        
        def _dfs(node: str):
            while self.graph[node]:
                # Pop the neighbor to remove the edge (Hierholzer's condition)
                next_node = self.graph[node].pop()
                _dfs(next_node)
            # Add node to route when stuck
            route.append(node)
            
        _dfs(start_node)
        
        # Check if all edges are visited (checks for disconnected components)
        for node in self.nodes:
            if self.graph[node]:
                return None
                
        return route[::-1]


class TwoSAT:
    """
    Solves the 2-Satisfiability problem using Tarjan's SCC Algorithm.
    Given n boolean variables, they are represented as 0 to n-1 (positive literals)
    and n to 2n-1 (negative literals).
    """
    def __init__(self, n: int):
        self.n = n
        self.tj = TarjanSCC(2 * n)
        
    def _neg(self, i: int) -> int:
        """Returns the index representing the negation of variable i."""
        if i < self.n:
            return i + self.n
        return i - self.n
        
    def add_clause(self, i: int, j: int) -> None:
        """
        Adds a clause (i OR j) to the 2-CNF formula.
        Variables should be in the range [0, 2n-1].
        """
        # (~i -> j) and (~j -> i)
        self.tj.add_edge(self._neg(i), j)
        self.tj.add_edge(self._neg(j), i)
        
    def solve(self) -> Tuple[bool, List[bool]]:
        """
        Returns (is_satisfiable, assignment_list).
        """
        sccs = self.tj.get_sccs()
        
        # Map each variable to its SCC ID.
        # Tarjan's algorithm produces SCCs in reverse topological order.
        scc_id = [-1] * (2 * self.n)
        for i, scc in enumerate(sccs):
            for node in scc:
                scc_id[node] = i
                
        assignment = [False] * self.n
        
        for i in range(self.n):
            if scc_id[i] == scc_id[self._neg(i)]:
                return False, []
            # A topological sort means if scc_id[i] < scc_id[~i], 
            # the SCC for i appears earlier in reverse topological order,
            # meaning it comes LATER in actual topological order.
            # We assign True if the variable's SCC comes later.
            assignment[i] = scc_id[i] < scc_id[self._neg(i)]
            
        return True, assignment


# ==============================================================================
# Interactive Lesson Test Cases
# ==============================================================================
def run_tests():
    print("=" * 60)
    print("Executing Advanced Graph Algorithms Test Suite")
    print("=" * 60)
    
    # ---------------------------------------------------------
    # 1. Strongly Connected Components (SCC)
    # ---------------------------------------------------------
    print("\n--- 1. Strongly Connected Components (SCC) ---")
    print("Testing Tarjan's and Kosaraju's algorithms on a graph...")
    
    # Graph: 1->0, 0->2, 2->1, 0->3, 3->4
    # SCCs should be: [1, 2, 0], [3], [4]
    tj = TarjanSCC(5)
    ks = KosarajuSCC(5)
    edges = [(1, 0), (0, 2), (2, 1), (0, 3), (3, 4)]
    
    for u, v in edges:
        tj.add_edge(u, v)
        ks.add_edge(u, v)
        
    tj_sccs = tj.get_sccs()
    ks_sccs = ks.get_sccs()
    
    # Sort SCCs for comparison
    tj_sccs_sorted = sorted([sorted(scc) for scc in tj_sccs])
    ks_sccs_sorted = sorted([sorted(scc) for scc in ks_sccs])
    
    print(f"Tarjan's SCCs:   {tj_sccs_sorted}")
    print(f"Kosaraju's SCCs: {ks_sccs_sorted}")
    assert tj_sccs_sorted == ks_sccs_sorted, "SCC mismatch!"
    print("✅ Both algorithms produced identical SCCs.")

    # ---------------------------------------------------------
    # 2. Eulerian Paths
    # ---------------------------------------------------------
    print("\n--- 2. Eulerian Paths (Hierholzer's Algorithm) ---")
    print("Testing airline itinerary reconstruction...")
    tickets = [("MUC", "LHR"), ("JFK", "MUC"), ("SFO", "SJC"), ("LHR", "SFO")]
    
    eps = EulerianPathSolver(tickets)
    itinerary = eps.find_eulerian_path()
    
    print(f"Tickets: {tickets}")
    print(f"Reconstructed Itinerary: {itinerary}")
    assert itinerary == ["JFK", "MUC", "LHR", "SFO", "SJC"]
    print("✅ Eulerian Path reconstructed successfully.")
    
    # ---------------------------------------------------------
    # 3. 2-Satisfiability (2-SAT)
    # ---------------------------------------------------------
    print("\n--- 3. 2-Satisfiability (2-SAT) ---")
    print("Solving formula: (A or B) and (~A or ~B) and (A or ~B)")
    # Variables: A = 0, B = 1. Negations: ~A = 2, ~B = 3
    solver = TwoSAT(2)
    # (A or B)
    solver.add_clause(0, 1)
    # (~A or ~B)
    solver.add_clause(2, 3)
    # (A or ~B)
    solver.add_clause(0, 3)
    
    is_sat, assignment = solver.solve()
    print(f"Is Satisfiable? {is_sat}")
    if is_sat:
        print(f"Truth Assignment (A, B): {assignment}")
    assert is_sat and assignment == [True, False], "2-SAT solver failed!"
    print("✅ 2-SAT resolved successfully.")

    print("\n" + "=" * 60)
    print("All Tests Passed! You are now a Master of Advanced Graphs!")
    print("=" * 60)


if __name__ == '__main__':
    run_tests()
