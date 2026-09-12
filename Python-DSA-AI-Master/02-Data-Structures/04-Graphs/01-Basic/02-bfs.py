"""
# Breadth-First Search (BFS)

## 1. Intuition
Breadth-First Search (BFS) is a systematic way to explore a graph or tree. Instead of going deep down one path (like Depth-First Search), BFS explores the graph layer by layer, starting from the source node. It visits all immediate neighbors first, then moves on to their neighbors, and so on.

## 2. Real-World Analogy
Imagine throwing a stone into a still pond. The ripples spread outwards in concentric circles. Each circle represents a "level" or "layer" of nodes in BFS. 
Alternatively, think of a social network. If you want to find the shortest connection between you and a celebrity, you first check your friends (Level 1), then your friends of friends (Level 2), and so on, until you find someone who knows the celebrity.

## 3. Formal Explanation
BFS uses a Queue (FIFO - First In, First Out) to keep track of nodes to visit next. 
1. Enqueue the starting node and mark it as visited.
2. While the queue is not empty:
   a. Dequeue a node.
   b. Process it (e.g., print, check for target, update distances).
   c. For each unvisited neighbor of this node:
      i. Mark it as visited.
      ii. Enqueue it.

Marking a node as visited *before* putting it in the queue (or right when you put it in) is critical to prevent enqueuing the same node multiple times, which would blow up the space complexity.

## 4. Complexity
- **Time Complexity:** O(V + E), where V is the number of vertices and E is the number of edges. We visit every vertex once and examine every edge at most twice (in an undirected graph).
- **Space Complexity:** O(V), for the queue and the `visited` set. In the worst-case (a very broad tree or graph), the queue will hold all nodes at the widest level, which could be O(V).

## 5. Debugging & Common Mistakes
- **Mistake 1:** Marking nodes as visited *when popping* from the queue. 
  *Consequence:* The same node can be added to the queue multiple times by different neighbors before it gets popped and marked visited.
- **Mistake 2:** Forgetting to handle disconnected graphs. 
  *Fix:* If you need to traverse the entire graph, iterate through all nodes and run BFS on any unvisited node.
- **Mistake 3:** Using a standard list as a queue (`queue.pop(0)`).
  *Consequence:* This makes dequeuing an O(N) operation. Use `collections.deque` for O(1) pops from both ends.

## 6. Active Recall & Memory Anchors
- **Q:** What data structure does BFS use? 
  **A:** Queue (FIFO). Think of standing in line for a ticket (first come, first served).
- **Q:** When is BFS preferred over DFS?
  **A:** When finding the shortest path on an unweighted graph, or when the target is expected to be close to the source.
- **Q:** Where do we mark a node as visited?
  **A:** Right when we *discover* it (before/during enqueue), NOT when we process it.

---
"""

from collections import deque
from typing import Dict, List, Set, Tuple, Optional

class Graph:
    def __init__(self):
        self.adj_list: Dict[str, List[str]] = {}

    def add_edge(self, u: str, v: str, bidirectional: bool = True):
        if u not in self.adj_list:
            self.adj_list[u] = []
        if v not in self.adj_list:
            self.adj_list[v] = []
        
        self.adj_list[u].append(v)
        if bidirectional:
            self.adj_list[v].append(u)

    def bfs_traversal(self, start: str) -> List[str]:
        """
        Standard BFS to simply traverse and return nodes in visited order.
        """
        if start not in self.adj_list:
            return []

        visited: Set[str] = {start}
        queue: deque[str] = deque([start])
        order: List[str] = []

        while queue:
            node = queue.popleft()
            order.append(node)

            for neighbor in self.adj_list.get(node, []):
                # Check unvisited before enqueueing!
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

        return order

    def bfs_shortest_path(self, start: str, target: str) -> Optional[List[str]]:
        """
        Uses BFS to find the shortest path between 'start' and 'target' in an unweighted graph.
        We track the 'parent' of each node to reconstruct the path later.
        """
        if start not in self.adj_list or target not in self.adj_list:
            return None

        visited: Set[str] = {start}
        queue: deque[str] = deque([start])
        parent_map: Dict[str, Optional[str]] = {start: None}

        found = False

        while queue and not found:
            node = queue.popleft()

            if node == target:
                found = True
                break

            for neighbor in self.adj_list.get(node, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    parent_map[neighbor] = node
                    queue.append(neighbor)

        if not found:
            return None  # Path doesn't exist

        # Reconstruct path by tracing back from target to start
        path = []
        curr = target
        while curr is not None:
            path.append(curr)
            curr = parent_map[curr]
            
        path.reverse()  # Since we traced backwards
        return path

    def bfs_levels(self, start: str) -> Dict[str, int]:
        """
        Calculates the minimum distance (number of edges) from 'start' to all reachable nodes.
        Demonstrates exploring graph "layer by layer".
        """
        if start not in self.adj_list:
            return {}

        distances: Dict[str, int] = {start: 0}
        queue: deque[str] = deque([start])

        while queue:
            node = queue.popleft()
            current_dist = distances[node]

            for neighbor in self.adj_list.get(node, []):
                if neighbor not in distances:
                    distances[neighbor] = current_dist + 1
                    queue.append(neighbor)

        return distances

def demo_bfs():
    # 1. Initialize our graph
    g = Graph()
    
    # Let's create a graph resembling a social network
    edges = [
        ("Alice", "Bob"),
        ("Alice", "Charlie"),
        ("Bob", "David"),
        ("Bob", "Eve"),
        ("Charlie", "Eve"),
        ("Charlie", "Frank"),
        ("Eve", "Grace"),
        ("Frank", "Grace")
    ]
    
    for u, v in edges:
        g.add_edge(u, v)

    print("--- BFS Traversal ---")
    traversal_order = g.bfs_traversal("Alice")
    print(f"BFS from Alice: {' -> '.join(traversal_order)}")
    # Expected Output layer by layer: Alice -> Bob, Charlie -> David, Eve, Frank -> Grace
    
    print("\n--- Shortest Path (Unweighted) ---")
    path_to_grace = g.bfs_shortest_path("Alice", "Grace")
    print(f"Shortest path from Alice to Grace: {' -> '.join(path_to_grace)}")

    print("\n--- Node Levels (Distances) ---")
    distances = g.bfs_levels("Alice")
    for node, dist in distances.items():
        print(f"Distance from Alice to {node}: {dist} edges")

if __name__ == "__main__":
    demo_bfs()
