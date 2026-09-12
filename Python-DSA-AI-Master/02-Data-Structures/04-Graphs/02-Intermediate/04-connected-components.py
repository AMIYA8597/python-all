"""
## A. Concept Name
Connected Components

## B. One-Sentence Definition
A connected component is a maximal set of vertices in a graph where every vertex is reachable from every other vertex in the set.

## C. Why Does This Exist?
To identify isolated clusters or subnetworks within a larger network (like friend circles in social networks or independent subnets in computer networks).

## D. Intuition
If you pour water onto a node, the connected component is everywhere the water can flow without jumping across gaps. 

## E. Real-Life Analogy
- Islands in an archipelago: Each island is a connected component where you can walk anywhere, but you need a boat to reach another island.
- Friend networks: Groups of people where everyone has a chain of mutual friends to everyone else in the group.

## F. Mental Model
Think of vertices as beads and edges as strings. If you pick up one bead, all the beads that dangle connected to it form one connected component.

## G. Visual Explanation
Vertices: {1, 2, 3, 4}
Edges: (1-2), (3-4)
Component 1: {1, 2}
Component 2: {3, 4}
There is no path from 1 to 3, so they are in separate components.

## H. Formal Explanation
In an undirected graph, a connected component is a maximal subgraph where a path exists between any two vertices. In a directed graph, a Strongly Connected Component (SCC) requires a directed path from u to v AND from v to u for all pairs (u, v) in the SCC.

## I. Mathematical Foundation (if applicable)
An equivalence relation `~` can be defined on vertices where `u ~ v` if there is a path from u to v. Connected components are the equivalence classes of this relation.

## J. From-Scratch Implementation (if applicable)
(See code below for basic DFS, Bridge finding, and Tarjan's SCC algorithm).

## K. Library / Production Implementation (if applicable)
`networkx.connected_components(G)` for undirected graphs, or `networkx.strongly_connected_components(G)` for directed graphs.

## L. Trace (walk through example)
For graph {1: [2], 2: [1], 3: [4], 4: [3]}:
1. Start DFS at 1. Mark 1 visited, visit 2. Mark 2 visited. Return. Component {1, 2} found.
2. 2 is already visited. Skip.
3. Start DFS at 3. Mark 3 visited, visit 4. Mark 4 visited. Return. Component {3, 4} found.

## M. Complexity
- Time Complexity: O(V + E) for standard components and Tarjan's SCC.
- Space Complexity: O(V) for visited sets and recursion stacks.

## N. Common Mistakes
- Forgetting to loop through ALL vertices to start the search (since some might be unreachable from the first vertex).
- Confusing connected components (undirected) with strongly connected components (directed).

## O. Common Confusions
- "Why use Tarjan's algorithm instead of Kosaraju's for SCCs?" Tarjan's requires only one DFS pass, while Kosaraju's requires two, making Tarjan's slightly more efficient in practice though both are O(V + E).

## P. When To Use
- Identifying clusters, community detection.
- Checking network reliability (finding bridges/articulation points).
- Identifying dependency cycles (SCCs).

## Q. When NOT To Use
- If you only need the shortest path between two specific nodes (use BFS or Dijkstra).

## R. Trade-offs
- DFS vs BFS for finding components: Both are O(V + E). DFS is usually easier to implement recursively, but BFS avoids recursion depth limits on very deep graphs.

## S. Debugging
- Print the visited set after each outer loop iteration to ensure nodes are being added correctly.
- Ensure directed edges are processed correctly for SCCs (unlike undirected components).

## T. Memory Hook (a short memorable principle)
Outer loop catches the disconnected, inner DFS/BFS sweeps the connected.

## U. Active Recall (questions before answers)
1. What is the time complexity to find all connected components? (O(V + E)).
2. What does a bridge in a graph represent? (An edge whose removal increases the number of connected components).

## V. Practice (exercises)
1. Implement connected components using BFS instead of DFS.
2. Implement an algorithm to find Articulation Points (vertices whose removal disconnects the graph).

## W. Interview Question
"Given a list of edges representing a network, how do you determine if the entire network is connected?"
(Answer: Run a DFS/BFS starting from node 0. Count how many nodes are visited. If it equals the total number of nodes, it's connected, otherwise it's not.)

## X. Project Connection
Used in image processing (connected-component labeling for object detection), social network analysis (identifying communities), and compilers (detecting dead code or circular dependencies).
"""

from typing import Dict, List, Set, Any
from collections import defaultdict
import unittest

# Basic Implementation: Connected Components
def find_connected_components(graph: Dict[Any, List[Any]]) -> List[List[Any]]:
    visited = set()
    components = []

    def dfs(node, current_component):
        visited.add(node)
        current_component.append(node)
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                dfs(neighbor, current_component)

    for node in list(graph.keys()):
        if node not in visited:
            comp = []
            dfs(node, comp)
            components.append(comp)

    return components

# Intermediate Implementation: Finding Bridges
def find_bridges(graph: Dict[Any, List[Any]], n: int) -> List[List[Any]]:
    ids = {}
    low = {}
    visited = set()
    bridges = []
    timer = 0

    def dfs(at, parent):
        nonlocal timer
        visited.add(at)
        ids[at] = low[at] = timer
        timer += 1

        for to in graph.get(at, []):
            if to == parent:
                continue
            if to in visited:
                low[at] = min(low[at], ids[to])
            else:
                dfs(to, at)
                low[at] = min(low[at], low[to])
                if ids[at] < low[to]:
                    bridges.append([at, to])

    for i in list(graph.keys()):
        if i not in visited:
            dfs(i, -1)
            
    return bridges

# Advanced Implementation: Tarjan's SCC Algorithm
def tarjan_scc(graph: Dict[Any, List[Any]]) -> List[List[Any]]:
    ids = {}
    low = {}
    on_stack = set()
    stack = []
    id_counter = 0
    sccs = []

    def dfs(at):
        nonlocal id_counter
        stack.append(at)
        on_stack.add(at)
        ids[at] = low[at] = id_counter
        id_counter += 1

        for to in graph.get(at, []):
            if to not in ids:
                dfs(to)
            if to in on_stack:
                low[at] = min(low[at], low[to])

        # If we are at the root of an SCC
        if ids[at] == low[at]:
            scc = []
            while True:
                node = stack.pop()
                on_stack.remove(node)
                scc.append(node)
                if node == at:
                    break
            sccs.append(scc)

    for node in list(graph.keys()):
        if node not in ids:
            dfs(node)

    return sccs

# Interview Challenge
def critical_connections(n: int, connections: List[List[int]]) -> List[List[int]]:
    """
    Find all critical connections in the network. A critical connection is an edge that, 
    if removed, makes some server unable to reach some other server.
    """
    graph = defaultdict(list)
    for u, v in connections:
        graph[u].append(v)
        graph[v].append(u)
    
    # Ensure all vertices from 0 to n-1 are present in the graph dictionary
    for i in range(n):
        if i not in graph:
            graph[i] = []
            
    return find_bridges(graph, n)

# Tests
class TestConnectedComponents(unittest.TestCase):
    def test_connected_components(self):
        graph = {1: [2], 2: [1], 3: [4], 4: [3]}
        comps = find_connected_components(graph)
        self.assertEqual(len(comps), 2)

    def test_bridges(self):
        bridges = critical_connections(4, [[0,1],[1,2],[2,0],[1,3]])
        # 1-3 or 3-1 is the only bridge
        self.assertTrue([1,3] in bridges or [3,1] in bridges)

    def test_tarjan_scc(self):
        graph = {0: [1], 1: [2], 2: [0, 3], 3: [4], 4: [5], 5: [3]}
        sccs = tarjan_scc(graph)
        self.assertEqual(len(sccs), 2)

if __name__ == '__main__':
    unittest.main()
