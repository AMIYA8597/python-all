"""
## A. Concept Name
Advanced Graph Theory (SCC, Eulerian Path, 2-SAT)

## B. One-Sentence Definition
Advanced graph algorithms solve complex connectivity, pathfinding, and boolean satisfiability problems by exploiting the structural properties of directed and undirected graphs.

## C. Why Does This Exist?
To efficiently solve problems that go beyond basic traversal (DFS/BFS) or shortest paths, such as identifying mutually reachable components in networks or finding paths that traverse every edge exactly once.

## D. Intuition
Think of basic graph algorithms like navigating a city map. Advanced graph algorithms are like analyzing the city's traffic flow to find bottlenecks (SCCs), planning a snowplow route that clears every street exactly once (Eulerian Path), or logically deducing the only valid combination of traffic light states (2-SAT).

## E. Real-Life Analogy
- SCC: Friend groups on a social network where everyone in the group can trace a path of follows to everyone else in the group.
- Eulerian Path: A garbage truck route that must travel down every single street in a neighborhood exactly once without retracing its steps unnecessarily.
- 2-SAT: Choosing pizza toppings where every decision is linked ("If we get pepperoni, we cannot get mushrooms", "We must get either mushrooms or onions").

## F. Mental Model
- SCC (Tarjan's): Track "discovery time" and "lowest reachable time" during DFS. If they match when returning from recursion, you've found the root of an SCC.
- Eulerian Path (Hierholzer's): Walk randomly until you get stuck. Since you must use every edge, backtrack and stitch unvisited subpaths into your main path.
- 2-SAT: Convert logical OR constraints into IMPLICATION edges. If A implies B, and B implies A, they must have the same truth value (same SCC).

## G. Visual Explanation
SCC (Tarjan's):
1 -> 2 -> 3 -> 1 (Cycle / SCC 1)
|
v
4 -> 5 -> 4 (Cycle / SCC 2)

Eulerian Path:
Post-order traversal of edges in a graph where degrees match Eulerian conditions gives the path in reverse.

## H. Formal Explanation
1. Strongly Connected Components (SCC): A maximal subgraph of a directed graph where for every pair of vertices u, v, there is a directed path from u to v and v to u. Tarjan's algorithm finds these in O(V + E) using a single DFS.
2. Eulerian Path: A trail in a finite graph that visits every edge exactly once. Exists if at most one vertex has (out-degree) - (in-degree) = 1, at most one vertex has (in-degree) - (out-degree) = 1, and all others have equal in/out degrees.
3. 2-Satisfiability (2-SAT): A special case of boolean satisfiability where each clause has exactly two literals. Solvable in polynomial time using implication graphs and SCCs.

## I. Mathematical Foundation (if applicable)
For Eulerian paths, Euler's theorem states that a connected directed graph has an Eulerian cycle if and only if every vertex has equal in-degree and out-degree.

## J. From-Scratch Implementation (if applicable)
See the `TarjanSCC` and `find_eulerian_path` implementations below.

## K. Library / Production Implementation (if applicable)
`networkx` provides `strongly_connected_components` and `eulerian_path` in Python, heavily optimized in C/Cython for large-scale graphs.

## L. Trace (walk through example)
Eulerian Path on tickets = [["JFK", "MUC"], ["MUC", "LHR"], ["LHR", "SFO"], ["SFO", "SJC"]]
1. Start at JFK. Next is MUC.
2. From MUC, next is LHR.
3. From LHR, next is SFO.
4. From SFO, next is SJC.
5. SJC has no outgoing. Append SJC to route. Backtrack.
6. Append SFO, LHR, MUC, JFK.
7. Reverse route: ["JFK", "MUC", "LHR", "SFO", "SJC"].

## M. Complexity
- Tarjan's SCC: Time O(V + E), Space O(V)
- Hierholzer's Eulerian Path: Time O(V + E log E) (if sorting edges), Space O(V + E)

## N. Common Mistakes
1. Tarjan's: Confusing back-edges with cross-edges. A back-edge points to an ancestor in the current DFS stack.
2. Eulerian Path: Not traversing in post-order or forgetting to reverse the path at the end.
3. 2-SAT: Forgetting to add BOTH implications for a clause (A OR B -> ~A implies B AND ~B implies A).

## O. Common Confusions
"Why do we reverse the result in Hierholzer's?" Because we append to the route only when a node has no more outgoing edges (we get stuck). The first node we append is actually the LAST node in the Eulerian path.

## P. When To Use
- SCC: Identifying cycles or mutual dependencies (e.g., package managers, spreadsheet cells).
- Eulerian Path: Route planning, DNA sequence reconstruction (De Bruijn graphs).
- 2-SAT: Constraint satisfaction problems with binary choices.

## Q. When NOT To Use
- When dealing with undirected graphs where simple DFS/BFS handles connected components.
- When clauses in boolean logic have 3 or more literals (3-SAT is NP-Complete).

## R. Trade-offs
Tarjan's vs. Kosaraju's for SCC: Tarjan's requires only one DFS pass but is slightly more complex to implement and understand mentally. Kosaraju's is very intuitive but requires two DFS passes.

## S. Debugging
- Check your graph representation (Adjacency List is best).
- For Tarjan's, print `disc` and `low` arrays at the end of each DFS step to trace the back-edges.
- For Eulerian Path, verify the in/out degrees of all nodes before starting the DFS to ensure a path is mathematically possible.

## T. Memory Hook (a short memorable principle)
Tarjan's: "Low link matches discovery time? We found an SCC root."
Eulerian: "Walk till stuck, save node, step back."

## U. Active Recall (questions before answers)
1. What is the time complexity of finding SCCs using Tarjan's?
2. What are the degree conditions for an Eulerian path in a directed graph?
3. How is 2-SAT modeled using a graph?

## V. Practice (exercises)
1. Implement Kosaraju's Algorithm and compare its performance with Tarjan's.
2. Solve LeetCode 332 (Reconstruct Itinerary).
3. Write a solver for a 2-SAT problem using your SCC implementation.

## W. Interview Question
"Given a list of airline tickets represented by pairs of departure and arrival airports, reconstruct the itinerary in order. You must use all the tickets once and only once." (Eulerian Path)

## X. Project Connection
Used in compilers for dependency resolution and dead code elimination, in bioinformatics for genome assembly, and in logistics for routing and scheduling.
"""

from typing import List, Dict, Set


class TarjanSCC:
    """
    Tarjan's strongly connected components algorithm.
    Time Complexity: O(V + E)
    """
    def __init__(self, n: int):
        self.n = n
        self.graph = [[] for _ in range(n)]
        self.time = 0
        
    def add_edge(self, u: int, v: int):
        self.graph[u].append(v)
        
    def get_sccs(self) -> List[List[int]]:
        disc = [-1] * self.n
        low = [-1] * self.n
        stack_member = [False] * self.n
        stack = []
        result = []
        
        def _dfs(u: int):
            disc[u] = self.time
            low[u] = self.time
            self.time += 1
            stack_member[u] = True
            stack.append(u)
            
            for v in self.graph[u]:
                if disc[v] == -1:  # If v is not visited
                    _dfs(v)
                    low[u] = min(low[u], low[v])
                elif stack_member[v]:  # Back-edge
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
                
        for i in range(self.n):
            if disc[i] == -1:
                _dfs(i)
                
        return result


def find_eulerian_path(graph_edges: List[List[str]]) -> List[str]:
    """
    Finds the Eulerian Path in a directed graph using Hierholzer's algorithm.
    Given a list of directed edges like [['JFK', 'SFO'], ['JFK', 'ATL'], ...],
    reconstruct the itinerary. Commonly seen as LeetCode 332 (Reconstruct Itinerary).
    """
    from collections import defaultdict
    
    graph = defaultdict(list)
    for u, v in graph_edges:
        graph[u].append(v)
        
    # Sort for lexical order requirements usually seen in problems
    for k in graph:
        graph[k].sort(reverse=True)
        
    route = []
    
    def _dfs(node: str):
        while graph[node]:
            next_node = graph[node].pop()
            _dfs(next_node)
        route.append(node)
        
    # Start node (Problem specific, e.g., 'JFK' for airline problems)
    # For a general Eulerian path, you would compute in/out degrees to find the start node.
    _dfs("JFK")
    return route[::-1]


def _run_tests():
    # 1. Tarjan SCC Test
    tj = TarjanSCC(5)
    tj.add_edge(1, 0)
    tj.add_edge(0, 2)
    tj.add_edge(2, 1)
    tj.add_edge(0, 3)
    tj.add_edge(3, 4)
    
    sccs = tj.get_sccs()
    # Expect 3 SCCs: [4], [3], [1, 2, 0] (order may vary)
    assert len(sccs) == 3

    # 2. Eulerian Path Test
    tickets = [["MUC", "LHR"], ["JFK", "MUC"], ["SFO", "SJC"], ["LHR", "SFO"]]
    itinerary = find_eulerian_path(tickets)
    assert itinerary == ["JFK", "MUC", "LHR", "SFO", "SJC"]


if __name__ == '__main__':
    print("Running Advanced Graph algorithm tests...")
    _run_tests()
    print("All tests passed!")
