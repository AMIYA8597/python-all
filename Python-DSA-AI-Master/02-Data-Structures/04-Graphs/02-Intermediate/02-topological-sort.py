"""
## A. Concept Name
Topological Sort

## B. Analogy
Imagine taking college courses where some courses have prerequisites (like you must take Math 101 before Math 201). A topological sort gives you a valid sequence in which you can take all the courses.

## C. Definition
Topological sorting for Directed Acyclic Graph (DAG) is a linear ordering of vertices such that for every directed edge u v, vertex u comes before v in the ordering. Topological Sorting for a graph is not possible if the graph is not a DAG.

## D. Use Cases
1. Build systems (e.g., make, npm, pip) where certain packages must be compiled/installed before others.
2. Task scheduling.
3. Resolving symbol dependencies in linkers.
4. Instruction scheduling in compilers.

## X. Project Connection
Understanding topological sort is essential for AI projects involving task planning, dependency resolution in complex agents, and optimizing execution order in neural network computation graphs.
"""

from collections import defaultdict, deque

class Graph:
    def __init__(self, vertices):
        self.graph = defaultdict(list)
        self.V = vertices

    def add_edge(self, u, v):
        self.graph[u].append(v)

    def topological_sort(self):
        # Array to store indegrees of all vertices. Initialize all indegrees as 0.
        in_degree = {i: 0 for i in range(self.V)}

        # Traverse adjacency lists to fill indegrees of vertices
        for i in range(self.V):
            for j in self.graph[i]:
                in_degree[j] += 1

        # Create a queue and enqueue all vertices with indegree 0
        queue = deque()
        for i in range(self.V):
            if in_degree[i] == 0:
                queue.append(i)

        # Initialize count of visited vertices
        cnt = 0

        # Vector to store result (A topological ordering of the vertices)
        top_order = []

        # One by one dequeue vertices from queue and enqueue adjacents if indegree of adjacent becomes 0
        while queue:
            # Extract front of queue and add it to topological order
            u = queue.popleft()
            top_order.append(u)

            # Iterate through all its neighbouring nodes of dequeued node u and decrease their in-degree by 1
            for i in self.graph[u]:
                in_degree[i] -= 1
                # If in-degree becomes zero, add it to queue
                if in_degree[i] == 0:
                    queue.append(i)

            cnt += 1

        # Check if there was a cycle
        if cnt != self.V:
            print("There exists a cycle in the graph")
            return []
        else:
            return top_order

if __name__ == '__main__':
    g = Graph(6)
    g.add_edge(5, 2)
    g.add_edge(5, 0)
    g.add_edge(4, 0)
    g.add_edge(4, 1)
    g.add_edge(2, 3)
    g.add_edge(3, 1)

    print("Following is a Topological Sort of the given graph:")
    print(g.topological_sort())
