"""
# ==============================================================================
# LABORATORY: COMPETITIVE PROGRAMMING (ADVANCED GRAPH THEORY PART 2)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You are asked to solve the famous "Seven Bridges of Königsberg" problem: 
# Is it possible to walk through the city and cross every single bridge exactly 
# once? 
#
# This is mathematically known as finding an Eulerian Path. You cannot use 
# standard DFS; it will get stuck in dead ends and fail in O(V!) exponential 
# time. You must use Hierholzer's Algorithm to stitch cycles together in O(E) time.
#
# Second Scenario: You are analyzing a massive Directed Graph (like Twitter).
# You want to find "Echo Chambers" (clusters of people where everyone follows 
# everyone else within the cluster). This is mathematically known as finding 
# Strongly Connected Components (SCC).
# You must use Kosaraju's Algorithm, which uses the magic of a Transposed 
# Graph to find these clusters in exactly O(V + E) time!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand Kosaraju's Algorithm for Strongly Connected Components.
# - Understand Hierholzer's Algorithm for Eulerian Paths.
#
# ==============================================================================
"""

from collections import defaultdict

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. KOSARAJU'S ALGORITHM (STRONGLY CONNECTED COMPONENTS)
# ==============================================================================
class KosarajuSCC:
    """
    Finds all Strongly Connected Components (SCCs) in a Directed Graph.
    Time Complexity: O(V + E)
    Space Complexity: O(V + E)
    """
    def __init__(self, n: int, edges: list[list[int]]):
        self.n = n
        self.adj = defaultdict(list)
        # We physically create a reversed version of the graph!
        self.rev_adj = defaultdict(list)
        
        for u, v in edges:
            self.adj[u].append(v)
            # Transposed graph: all arrows point backward!
            self.rev_adj[v].append(u)
            
    def _dfs_pass_1(self, u: int, visited: set, stack: list) -> None:
        """First DFS: Computes finishing times"""
        visited.add(u)
        for v in self.adj[u]:
            if v not in visited:
                self._dfs_pass_1(v, visited, stack)
        # Push to stack exactly when the node finishes exploring all its children!
        stack.append(u)
        
    def _dfs_pass_2(self, u: int, visited: set, scc_group: list) -> None:
        """Second DFS: Explores the Transposed Graph to isolate clusters"""
        visited.add(u)
        scc_group.append(u)
        for v in self.rev_adj[u]:
            if v not in visited:
                self._dfs_pass_2(v, visited, scc_group)
                
    def find_sccs(self) -> list[list[int]]:
        stack = []
        visited = set()
        
        # Pass 1: standard DFS to populate the finishing time Stack
        for i in range(self.n):
            if i not in visited:
                self._dfs_pass_1(i, visited, stack)
                
        visited.clear()
        all_sccs = []
        
        # Pass 2: Process the stack in Reverse order on the Reversed Graph
        while stack:
            # Pop the node that finished LAST
            node = stack.pop()
            
            if node not in visited:
                scc_group = []
                self._dfs_pass_2(node, visited, scc_group)
                all_sccs.append(scc_group)
                
        return all_sccs

def demonstrate_kosaraju():
    section_header("Kosaraju's Algorithm (Echo Chambers / SCCs)")
    
    # Graph: 0 -> 1 -> 2 -> 0 (A cycle of 3 nodes)
    # 2 -> 3 (A bridge to another component)
    # 3 -> 4 -> 3 (A cycle of 2 nodes)
    edges = [
        [0, 1], [1, 2], [2, 0], 
        [2, 3], 
        [3, 4], [4, 3]
    ]
    
    print("Graph has two main clusters connected by a one-way street.")
    
    ks = KosarajuSCC(5, edges)
    sccs = ks.find_sccs()
    
    print(f"\nStrongly Connected Components found: {sccs}")
    print("Expected: [[0, 2, 1], [3, 4]]")


# ==============================================================================
# 4. HIERHOLZER'S ALGORITHM (EULERIAN PATH)
# ==============================================================================
def find_eulerian_path(edges: list[list[str]]) -> list[str]:
    """
    Finds a path that visits every EDGE exactly once in a Directed Graph.
    Used for reconstructing DNA sequences, or itinerary reconstruction (e.g. LeetCode 332).
    Time Complexity: O(E log E) because of lexicographical sorting.
    """
    # 1. Build Adjacency List (Sort to ensure Lexicographical order)
    adj = defaultdict(list)
    out_degree = defaultdict(int)
    in_degree = defaultdict(int)
    
    for u, v in sorted(edges, reverse=True):
        adj[u].append(v)
        out_degree[u] += 1
        in_degree[v] += 1
        # Make sure nodes are in the dictionaries even if they have 0 out-degree
        if v not in out_degree:
            out_degree[v] = 0
            
    # 2. Find the Start Node
    # A valid Eulerian Path starts at a node with (out_degree - in_degree == 1).
    # If all nodes are balanced, it's an Eulerian Circuit; start anywhere!
    start_node = list(adj.keys())[0]
    for node in out_degree:
        if out_degree[node] - in_degree[node] == 1:
            start_node = node
            break
            
    # 3. Hierholzer's DFS (Post-Order Traversal)
    path = []
    
    def dfs(curr: str):
        # Consume edges destructively! (Like burning a bridge after crossing it)
        while adj[curr]:
            next_node = adj[curr].pop() # Because we sorted reversed, pop() gets the lexicographically smallest!
            dfs(next_node)
            
        # We only append to the path AFTER getting stuck (no more outgoing edges).
        path.append(curr)
        
    dfs(start_node)
    
    # 4. Reverse the path because we built it backwards!
    return path[::-1]

def demonstrate_hierholzer():
    section_header("Hierholzer's Algorithm (Eulerian Path)")
    
    # Tickets: [Departure, Destination]
    tickets = [
        ["JFK", "SFO"],
        ["JFK", "ATL"],
        ["SFO", "ATL"],
        ["ATL", "JFK"],
        ["ATL", "SFO"]
    ]
    
    print(f"Flight Tickets: {tickets}")
    
    path = find_eulerian_path(tickets)
    print(f"\nValid Itinerary (Using every ticket exactly once):")
    print(" -> ".join(path))


def run_all_labs():
    demonstrate_kosaraju()
    demonstrate_hierholzer()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Explain the brilliance of the two-pass approach in Kosaraju's Algorithm. Why do we process nodes in reverse-finishing order on a reversed graph?
   Answer: In a Directed Graph, if Component A points to Component B, a DFS started in A will aggressively bleed into B, erroneously combining them. But if we reverse all the arrows in the graph, B now points to A! If we start a DFS in B, it cannot bleed into A anymore. The first DFS pass generates a Stack ordered by "Finishing Time". Nodes in Component A (the source) will mathematically finish *after* nodes in Component B (the sink) and end up on Top of the stack. During the second pass on the Reversed Graph, popping the stack ensures we start the DFS in A. Because the graph is reversed, A cannot reach B. The DFS gets trapped inside A, perfectly isolating the cluster!

2. In Hierholzer's Algorithm, why do we append nodes to the path ONLY AFTER the `while` loop finishes (Post-Order), rather than appending them as we visit them (Pre-Order)?
   Answer: Dead ends. If a graph has a massive cycle, and one tiny offshoot that leads to a dead end, a greedy Pre-Order DFS might accidentally take the offshoot immediately. It gets stuck at the dead end, having visited only 2 edges, and the algorithm fails. By appending in Post-Order, the algorithm dives into the dead end, realizes it's stuck, and appends the dead end to the path *first*. As the recursion backtracks, it unwinds, processes the massive cycle, and appends the cycle. Because the entire list is built backwards, the dead end mathematically ends up at the very end of the final path, which is exactly where a dead end belongs in an Eulerian Path!

3. How do you mathematically detect the correct Start Node for an Eulerian Path in a Directed Graph?
   Answer: You calculate the In-Degree (arrows pointing in) and Out-Degree (arrows pointing out) for every node. 
   - Nodes in the middle of the path must have `In-Degree == Out-Degree` (for every time you enter the city, you must leave the city).
   - The absolute Final Destination node will be a dead end where you stop walking, meaning it has one extra incoming arrow: `In-Degree - Out-Degree == 1`.
   - The Starting Node is where you begin the journey, meaning it has one extra outgoing arrow: `Out-Degree - In-Degree == 1`. 
   If no node matches the starting condition, all nodes are perfectly balanced, meaning the path is actually a closed loop (Eulerian Circuit), and you can safely start at any node!
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Advanced Graph Theory 2 Completed.")
