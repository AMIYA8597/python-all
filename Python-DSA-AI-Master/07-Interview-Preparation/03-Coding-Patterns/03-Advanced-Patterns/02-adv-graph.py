"""
Advanced Graph Patterns (Topological Sort, Union Find)
=======================================================

Learning Objectives:
1. Understand the Disjoint Set (Union-Find) data structure.
2. Implement Path Compression and Union by Rank for optimal performance.
3. Apply topological sorting to dependency resolution.

Concept Explanation:
Union-Find is a data structure that tracks a set of elements partitioned into a number 
of disjoint (non-overlapping) subsets. It provides near-constant-time operations to 
add new sets, merge existing sets, and determine whether elements are in the same set.
Topological Sort is used for DAGs (Directed Acyclic Graphs) to linearly order vertices 
so that for every directed edge u->v, vertex u comes before v.
"""

from typing import List, Dict, Set
import unittest
from collections import defaultdict, deque

class UnionFind:
    """Basic/Intermediate Implementation of Disjoint Set."""
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank = [1] * n

    def find(self, x: int) -> int:
        """Finds the root of x with path compression."""
        if x != self.parent[x]:
            self.parent[x] = self.find(self.parent[x])  # Path compression
        return self.parent[x]

    def union(self, x: int, y: int) -> bool:
        """Unites the sets containing x and y. Returns False if already in same set."""
        rootX = self.find(x)
        rootY = self.find(y)
        
        if rootX != rootY:
            if self.rank[rootX] > self.rank[rootY]:
                self.parent[rootY] = rootX
            elif self.rank[rootX] < self.rank[rootY]:
                self.parent[rootX] = rootY
            else:
                self.parent[rootY] = rootX
                self.rank[rootX] += 1
            return True
        return False

class GraphAlgorithms:
    """Advanced Implementation: Topological Sort and Cycle Detection."""
    
    @staticmethod
    def canFinishCourses(numCourses: int, prerequisites: List[List[int]]) -> bool:
        """
        Course Schedule: returns True if you can finish all courses.
        Uses Kahn's Algorithm (Topological Sort via BFS).
        """
        adj = defaultdict(list)
        indegree = [0] * numCourses
        
        for course, pre in prerequisites:
            adj[pre].append(course)
            indegree[course] += 1
            
        queue = deque([i for i in range(numCourses) if indegree[i] == 0])
        count = 0
        
        while queue:
            curr = queue.popleft()
            count += 1
            for neighbor in adj[curr]:
                indegree[neighbor] -= 1
                if indegree[neighbor] == 0:
                    queue.append(neighbor)
                    
        return count == numCourses

# --- Performance Analysis ---
# Union-Find with path compression and union by rank has an amortized time complexity 
# of O(alpha(n)) per operation, where alpha is the inverse Ackermann function.
# Topological Sort runs in O(V + E) time.

# --- Edge Cases ---
# Graph with multiple disconnected components, single node graph, graph with self-loops.

class TestAdvancedGraph(unittest.TestCase):
    def test_union_find(self):
        uf = UnionFind(5)
        self.assertTrue(uf.union(0, 1))
        self.assertTrue(uf.union(1, 2))
        self.assertFalse(uf.union(0, 2)) # Already connected
        self.assertEqual(uf.find(0), uf.find(2))
        self.assertNotEqual(uf.find(0), uf.find(3))

    def test_course_schedule(self):
        self.assertTrue(GraphAlgorithms.canFinishCourses(2, [[1,0]]))
        self.assertFalse(GraphAlgorithms.canFinishCourses(2, [[1,0],[0,1]]))

if __name__ == '__main__':
    unittest.main()
