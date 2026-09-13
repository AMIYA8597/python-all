"""
Module: Amazon Interview Questions (Python)

Learning Objectives:
- Master grid traversal using BFS and DFS.
- Implement object-oriented design for common data structures (e.g., LRU Cache).
- Learn priority queue (Heap) applications for 'Top K' problems.

Concept Explanation:
Amazon focuses heavily on arrays, strings, trees, and object-oriented design. Number of Islands is a classic graph/grid traversal problem. LRU cache tests combined knowledge of Hash Maps and Doubly Linked Lists.

Performance Analysis:
- Number of Islands: Time O(M*N), Space O(M*N) in worst case for call stack (DFS) or queue (BFS).
- LRU Cache: O(1) for both get and put operations.
"""

from typing import List
import collections

# Basic/Intermediate: Number of Islands (Grid DFS/BFS)
def num_islands(grid: List[List[str]]) -> int:
    """Counts the number of islands in a 2D grid."""
    if not grid:
        return 0
        
    count = 0
    rows, cols = len(grid), len(grid[0])
    
    def dfs(r: int, c: int):
        if r < 0 or c < 0 or r >= rows or c >= cols or grid[r][c] == '0':
            return
        grid[r][c] = '0' # Mark as visited
        dfs(r+1, c)
        dfs(r-1, c)
        dfs(r, c+1)
        dfs(r, c-1)
        
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':
                count += 1
                dfs(r, c)
                
    return count

# Advanced: LRU Cache
class Node:
    def __init__(self, key: int, value: int):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}
        self.head = Node(0, 0)
        self.tail = Node(0, 0)
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node: Node):
        prev_node = node.prev
        next_node = node.next
        prev_node.next = next_node
        next_node.prev = prev_node

    def _add(self, node: Node):
        prev_node = self.tail.prev
        prev_node.next = node
        node.prev = prev_node
        node.next = self.tail
        self.tail.prev = node

    def get(self, key: int) -> int:
        if key in self.cache:
            node = self.cache[key]
            self._remove(node)
            self._add(node)
            return node.value
        return -1

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self._remove(self.cache[key])
        node = Node(key, value)
        self._add(node)
        self.cache[key] = node
        if len(self.cache) > self.capacity:
            lru_node = self.head.next
            self._remove(lru_node)
            del self.cache[lru_node.key]


def test_amazon_questions():
    print("Testing Number of Islands...")
    grid1 = [
        ["1","1","1","1","0"],
        ["1","1","0","1","0"],
        ["1","1","0","0","0"],
        ["0","0","0","0","0"]
    ]
    grid2 = [
        ["1","1","0","0","0"],
        ["1","1","0","0","0"],
        ["0","0","1","0","0"],
        ["0","0","0","1","1"]
    ]
    assert num_islands(grid1) == 1
    assert num_islands(grid2) == 3
    print("Passed.")

    print("Testing LRU Cache...")
    lru = LRUCache(2)
    lru.put(1, 1)
    lru.put(2, 2)
    assert lru.get(1) == 1
    lru.put(3, 3) # evicts 2
    assert lru.get(2) == -1
    lru.put(4, 4) # evicts 1
    assert lru.get(1) == -1
    assert lru.get(3) == 3
    assert lru.get(4) == 4
    print("Passed.")

if __name__ == "__main__":
    test_amazon_questions()
    print("All Amazon interview tests passed!")
