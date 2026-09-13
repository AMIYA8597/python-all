"""
# ==============================================================================
# COMPETITIVE PROGRAMMING: GRAPH TEMPLATES (DFS & BFS)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Graphs are the most frequently asked topic in FAANG interviews and LeetCode
# contests. Whether you are finding the Shortest Path in a maze, counting the 
# number of Islands on a grid, or determining if a Course Schedule is possible, 
# you are dealing with Graphs.
#
# If you try to invent a Breadth-First Search (BFS) from scratch during a 
# 45-minute interview, you will make an off-by-one error, forget the `visited` 
# set, or use a List instead of a Deque and trigger a TLE.
#
# You must memorize the flawless, boilerplate templates for both DFS and BFS.
# 
# 2. LEARNING OBJECTIVES
# ----------------------
# - Construct an Adjacency List rapidly using `collections.defaultdict`.
# - Execute a recursive Depth-First Search (DFS) template.
# - Execute an iterative Breadth-First Search (BFS) template using `deque`.
#
# ==============================================================================
"""

from collections import defaultdict, deque

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. GRAPH CONSTRUCTION (ADJACENCY LIST)
# ==============================================================================
def demonstrate_graph_construction():
    section_header("Building the Adjacency List")
    
    print("A Graph is usually given as an Edge List: [[0, 1], [1, 2], [2, 0]]")
    print("You CANNOT traverse an Edge List efficiently.")
    print("You must convert it into an Adjacency List (a Hash Map mapping ")
    print("a Node to a List of its Neighbors).\n")
    
    edges = [[0, 1], [1, 2], [2, 0], [1, 3]]
    
    # 1. Initialize with defaultdict to prevent KeyErrors
    adj = defaultdict(list)
    
    # 2. Populate the Graph
    for u, v in edges:
        adj[u].append(v)
        # If the graph is UNDIRECTED (bidirectional), uncomment the next line:
        # adj[v].append(u) 
        
    print("Final Adjacency List:")
    for node, neighbors in adj.items():
        print(f"Node {node} points to -> {neighbors}")


# ==============================================================================
# 4. DEPTH-FIRST SEARCH (DFS) TEMPLATE
# ==============================================================================
def demonstrate_dfs():
    section_header("Depth-First Search (DFS) Template")
    
    print("DFS dives as deeply as possible into the graph until it hits a dead end, ")
    print("then it backtracks. It uses the Call Stack (Recursion) to remember its path.\n")
    
    # Graph: 0 -> 1 -> 3
    #        |
    #        v
    #        2
    adj = {0: [1, 2], 1: [3], 2: [], 3: []}
    
    visited = set()
    traversal_order = []
    
    def dfs(node):
        # 1. Base Case: If already visited, stop.
        # This prevents Infinite Loops if the Graph has a Cycle!
        if node in visited:
            return
            
        # 2. Mark as visited immediately
        visited.add(node)
        traversal_order.append(node)
        
        # 3. Visit all neighbors recursively
        for neighbor in adj[node]:
            dfs(neighbor)
            
    print("Executing DFS starting at Node 0...")
    dfs(0)
    print(f"DFS Traversal Order: {traversal_order}")
    print("Notice how it went 0 -> 1 -> 3 to the very bottom BEFORE exploring 2!")


# ==============================================================================
# 5. BREADTH-FIRST SEARCH (BFS) TEMPLATE
# ==============================================================================
def demonstrate_bfs():
    section_header("Breadth-First Search (BFS) Template")
    
    print("BFS explores the graph layer by layer, radiating outward like a ripple.")
    print("It mathematically guarantees finding the SHORTEST PATH in an unweighted graph.")
    print("It explicitly uses an Iterative Queue (collections.deque).\n")
    
    # Graph: 0 -> 1, 2
    #        1 -> 3
    adj = {0: [1, 2], 1: [3], 2: [], 3: []}
    
    visited = set()
    traversal_order = []
    
    def bfs(start_node):
        # 1. Initialize Queue and Visited Set with the starting node
        queue = deque([start_node])
        visited.add(start_node)
        
        # Optional: Track the shortest path distance
        distance = 0 
        
        while queue:
            # 2. Process the ENTIRE current layer (crucial for shortest path calculations)
            level_size = len(queue)
            
            for _ in range(level_size):
                # 3. Pop from the FRONT of the queue in O(1) time
                node = queue.popleft()
                traversal_order.append(node)
                
                # 4. Add unvisited neighbors to the BACK of the queue
                for neighbor in adj[node]:
                    if neighbor not in visited:
                        visited.add(neighbor) # Mark visited WHEN ENQUEUING, not when popping!
                        queue.append(neighbor)
                        
            # The entire layer finished processing
            distance += 1 
            
    print("Executing BFS starting at Node 0...")
    bfs(0)
    print(f"BFS Traversal Order: {traversal_order}")
    print("Notice how it explored 0 -> 1, 2 (the entire first layer) BEFORE exploring 3!")


def run_all_labs():
    demonstrate_graph_construction()
    demonstrate_dfs()
    demonstrate_bfs()


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. When constructing an Adjacency List in Python, why should you use `collections.defaultdict(list)` instead of a standard `{}` dictionary?
   Answer: In a standard Python dictionary, if you attempt to append a neighbor to a node that hasn't been initialized yet (`adj[u].append(v)`), it will instantly crash with a `KeyError: u`. To prevent this, you would have to write defensive boilerplate code: `if u not in adj: adj[u] = []`. Using `defaultdict(list)` abstracts this logic into the C-level backend. If the key doesn't exist, it automatically initializes it with an empty list and then appends the value, saving time and reducing bugs during a timed contest.

2. In a Breadth-First Search (BFS), why is it critical to add the node to the `visited` set IMMEDIATELY when it is pushed into the queue, rather than waiting until it is popped from the queue?
   Answer: Memory Bloat and Queue Explosion. If Node A and Node B both point to Node C, and you process the queue layer, you will look at Node A's neighbors and push Node C into the queue. If you wait until popping to mark it visited, when you look at Node B's neighbors, it sees that Node C is still technically "unvisited", so it pushes a *second* copy of Node C into the queue. On massive, highly connected graphs (like 2D grids), this duplicate queueing causes the queue to explode exponentially in size, resulting in catastrophic Memory Limit Exceeded (MLE) crashes. By marking it visited the microsecond it touches the queue, you guarantee it is only queued exactly once.

3. When should you choose DFS over BFS, and vice-versa?
   Answer: 
   - Choose BFS (Queue) if the problem asks for the "Shortest Path" or "Minimum Steps" in an unweighted graph, or if you are doing Level-Order Traversal on a Tree.
   - Choose DFS (Recursion/Stack) if the problem asks to find "All Possible Paths" (Backtracking), detect a Cycle, perform Topological Sort, or if you simply need to visit every single node (like counting the number of Connected Components) because DFS is generally faster to type and requires less memory overhead (no physical queue object).
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Graph Templates (DFS/BFS) Completed.")
