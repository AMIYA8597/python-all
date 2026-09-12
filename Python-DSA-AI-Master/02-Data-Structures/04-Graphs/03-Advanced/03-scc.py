"""
## A. Concept Name
Strongly Connected Components (SCC)

## B. One-Sentence Definition
An SCC is a maximal subgraph of a directed graph where every vertex is reachable from every other vertex in that subgraph.

## C. Why Does This Exist?
To break down complex cyclic dependencies or directed graphs into their fundamental, non-divisible "clusters" or components, which can be treated as single super-nodes (forming a Directed Acyclic Graph - DAG).

## D. Intuition
Imagine a city's one-way street network. An SCC is a neighborhood where you can drive from any intersection to any other intersection within that neighborhood using only the one-way streets.

## E. Real-Life Analogy
Friend circles on a social network (directed follows). An SCC is a group of people where everyone has a path of following to everyone else in the group (e.g., A follows B, B follows C, C follows A).

## F. Mental Model
Think of the graph as a solar system. SCCs are the planets (clusters of tightly bound matter). Once you identify the planets, you can simplify the solar system into just the interactions between the planets, ignoring the internal structure of each planet.

## G. Visual Explanation
Graph: A -> B -> C -> A, and C -> D
SCCs:
1. {A, B, C} (they form a cycle)
2. {D} (can be reached, but can't go back)
If we shrink {A, B, C} into super-node S, the graph becomes S -> D (a DAG).

## H. Formal Explanation
A directed graph is strongly connected if there is a path between all pairs of vertices. An SCC is a maximal strongly connected subgraph. 
Kosaraju's algorithm uses the finishing time of a DFS and a reversed graph.
Tarjan's algorithm uses a DFS with low-link values to find SCCs in a single pass.

## I. Mathematical Foundation (if applicable)
In an SCC graph condensation (where each SCC is a single node), the resulting graph is always a Directed Acyclic Graph (DAG). Kosaraju's algorithm relies on the property that if $C$ and $C'$ are SCCs, and there's an edge from $C$ to $C'$, then the maximum finishing time in $C$ is greater than the maximum finishing time in $C'$.

## J. From-Scratch Implementation (if applicable)
(See code section below for Kosaraju and Tarjan algorithms)

## K. Library / Production Implementation (if applicable)
`scipy.sparse.csgraph.connected_components` can compute strongly connected components for sparse matrices efficiently. NetworkX also has `networkx.strongly_connected_components`.

## L. Trace (walk through example)
Tarjan's algorithm on A -> B -> C -> A:
1. DFS starts at A (disc=0, low=0). Stack: [A]
2. Goes to B (disc=1, low=1). Stack: [A, B]
3. Goes to C (disc=2, low=2). Stack: [A, B, C]
4. C looks at A. A is in stack. C's low becomes min(2, disc(A)=0) = 0.
5. C returns to B. B's low becomes min(1, 0) = 0.
6. B returns to A. A's low becomes min(0, 0) = 0.
7. A finishes. disc(A) == low(A) == 0. A pops the stack up to A: {C, B, A} is one SCC.

## M. Complexity
- Time Complexity: O(V + E) for both Kosaraju's and Tarjan's algorithms.
- Space Complexity: O(V + E) to store the graph and O(V) for the call stack and auxiliary arrays.

## N. Common Mistakes
- Using Kosaraju's on an undirected graph (meaningless, just use standard connected components).
- Forgetting to reset the visited array between the two DFS passes in Kosaraju's algorithm.

## O. Common Confusions
- "Why use Tarjan's instead of Kosaraju's?" Tarjan's only requires one DFS pass and doesn't require computing the transposed graph, making it practically faster and using less memory, although both are O(V + E).

## P. When To Use
- Resolving cyclic dependencies in package managers or build systems.
- Analyzing network connectivity or web link structures (PageRank preprocessing).
- 2-SAT problem solving.

## Q. When NOT To Use
- On undirected graphs (standard DFS/BFS connected components is sufficient).
- When you only need to know if the entire graph is strongly connected (a single pass or simple traversal check is enough).

## R. Trade-offs
- Kosaraju: Conceptually simpler and easier to implement, but requires two passes and graph transposition (more space).
- Tarjan: Single pass, more efficient in practice, but conceptually harder (requires understanding discovery times and low-link values).

## S. Debugging
- Check if the transpose graph in Kosaraju's is built correctly.
- In Tarjan's, ensure you use `disc[v]` instead of `low[v]` when updating `low[u]` via a cross/back edge to a node already in the stack.

## T. Memory Hook (a short memorable principle)
- Kosaraju: "Forward to order, Reverse to collect."
- Tarjan: "Low-link binds the cycle; Stack holds the pending."

## U. Active Recall (questions before answers)
1. What data structure is essential for Tarjan's algorithm? (A stack to keep track of the current SCC path).
2. Why does Kosaraju need the transposed graph? (To prevent DFS from bleeding into other SCCs once the DAG structure is reversed).

## V. Practice (exercises)
1. Implement Tarjan's algorithm to output the SCCs in topologically sorted order of the condensed DAG.
2. Solve the 2-SAT problem using an SCC algorithm.

## W. Interview Question
Q: "Why does Tarjan's algorithm use `disc[v]` instead of `low[v]` when considering a cross-edge to a node already in the stack?"
A: "If we use `low[v]`, we might incorrectly pull `u` into the SCC of `v` even if `u` is not part of it. `disc[v]` safely caps the low-link value to the discovery time of the root of the SCC being built."

## X. Project Connection
Used in compilers to detect mutually recursive functions, and in route planning systems to find sub-networks where every location is reachable from every other.
"""

from typing import List, Dict, Set
from collections import defaultdict

# Basic Implementation: Kosaraju's Algorithm
class Kosaraju:
    def __init__(self, vertices: int):
        self.V = vertices
        self.graph = defaultdict(list)
        
    def add_edge(self, u: int, v: int):
        self.graph[u].append(v)
        
    def _fill_order(self, v: int, visited: List[bool], stack: List[int]):
        visited[v] = True
        for i in self.graph[v]:
            if not visited[i]:
                self._fill_order(i, visited, stack)
        stack.append(v)
        
    def _get_transpose(self) -> 'Kosaraju':
        g = Kosaraju(self.V)
        for i in range(self.V):
            for j in self.graph[i]:
                g.add_edge(j, i)
        return g
        
    def _dfs(self, v: int, visited: List[bool], scc: List[int]):
        visited[v] = True
        scc.append(v)
        for i in self.graph[v]:
            if not visited[i]:
                self._dfs(i, visited, scc)
                
    def get_sccs(self) -> List[List[int]]:
        stack = []
        visited = [False] * self.V
        
        for i in range(self.V):
            if not visited[i]:
                self._fill_order(i, visited, stack)
                
        gr = self._get_transpose()
        visited = [False] * self.V
        sccs = []
        
        while stack:
            i = stack.pop()
            if not visited[i]:
                scc = []
                gr._dfs(i, visited, scc)
                sccs.append(scc)
        return sccs

# Advanced Implementation: Tarjan's Algorithm
class Tarjan:
    def __init__(self, vertices: int):
        self.V = vertices
        self.graph = defaultdict(list)
        self.time = 0
        
    def add_edge(self, u: int, v: int):
        self.graph[u].append(v)
        
    def _scc_util(self, u: int, low: List[int], disc: List[int], stack_member: List[bool], st: List[int], result: List[List[int]]):
        disc[u] = self.time
        low[u] = self.time
        self.time += 1
        stack_member[u] = True
        st.append(u)
        
        for v in self.graph[u]:
            if disc[v] == -1:
                self._scc_util(v, low, disc, stack_member, st, result)
                low[u] = min(low[u], low[v])
            elif stack_member[v]:
                low[u] = min(low[u], disc[v])
                
        w = -1
        if low[u] == disc[u]:
            scc = []
            while w != u:
                w = st.pop()
                scc.append(w)
                stack_member[w] = False
            result.append(scc)
            
    def get_sccs(self) -> List[List[int]]:
        disc = [-1] * self.V
        low = [-1] * self.V
        stack_member = [False] * self.V
        st = []
        result = []
        
        for i in range(self.V):
            if disc[i] == -1:
                self._scc_util(i, low, disc, stack_member, st, result)
        return result

def test_scc():
    # Kosaraju
    k = Kosaraju(5)
    k.add_edge(1, 0)
    k.add_edge(0, 2)
    k.add_edge(2, 1)
    k.add_edge(0, 3)
    k.add_edge(3, 4)
    sccs_k = k.get_sccs()
    assert len(sccs_k) == 3
    
    # Tarjan
    t = Tarjan(5)
    t.add_edge(1, 0)
    t.add_edge(0, 2)
    t.add_edge(2, 1)
    t.add_edge(0, 3)
    t.add_edge(3, 4)
    sccs_t = t.get_sccs()
    assert len(sccs_t) == 3
    
    print("All tests passed for Strongly Connected Components.")

if __name__ == "__main__":
    test_scc()
