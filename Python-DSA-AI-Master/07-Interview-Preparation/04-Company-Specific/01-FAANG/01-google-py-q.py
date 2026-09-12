"""
Module: Google Interview Questions (Python)

Learning Objectives:
- Master advanced sliding window techniques.
- Understand graph traversal and cycle detection.
- Develop proficiency in optimizing string and array operations.

Concept Explanation:
Google frequently tests string manipulation with sliding window, graph algorithms (DFS/BFS/Union-Find), and dynamic programming. We'll cover a string manipulation algorithm (Longest Substring with At Most K Distinct Characters) and a graph evaluation problem.

Performance Analysis:
- Sliding Window: Time O(N), Space O(K) where N is string length, K is number of allowed characters.
- Graph Evaluation: Time O(V + E) per query, Space O(V + E) for adjacency list.
"""

from typing import List, Dict, Set, Tuple
import collections

# Basic/Intermediate: Longest Substring with At Most K Distinct Characters (Sliding Window)
def length_of_longest_substring_k_distinct(s: str, k: int) -> int:
    """Finds length of longest substring with at most k distinct characters."""
    if not s or k == 0:
        return 0
    
    char_count = collections.defaultdict(int)
    left = 0
    max_len = 0
    
    for right in range(len(s)):
        char_count[s[right]] += 1
        
        while len(char_count) > k:
            char_count[s[left]] -= 1
            if char_count[s[left]] == 0:
                del char_count[s[left]]
            left += 1
            
        max_len = max(max_len, right - left + 1)
        
    return max_len

# Advanced: Evaluate Division (Graph DFS)
def calc_equation(equations: List[List[str]], values: List[float], queries: List[List[str]]) -> List[float]:
    """
    Evaluates equations based on a graph representation.
    """
    graph = collections.defaultdict(dict)
    for (u, v), val in zip(equations, values):
        graph[u][v] = val
        graph[v][u] = 1.0 / val
        
    def dfs(src: str, dst: str, visited: Set[str]) -> float:
        if src not in graph or dst not in graph:
            return -1.0
        if src == dst:
            return 1.0
        visited.add(src)
        for neighbor, weight in graph[src].items():
            if neighbor not in visited:
                result = dfs(neighbor, dst, visited)
                if result != -1.0:
                    return result * weight
        return -1.0

    return [dfs(q[0], q[1], set()) for q in queries]


# Edge Cases:
# - Empty string or k=0 for substring problem.
# - Unconnected nodes or self-queries in graph problem.

def test_google_questions():
    print("Testing Length of Longest Substring K Distinct...")
    assert length_of_longest_substring_k_distinct("eceba", 2) == 3
    assert length_of_longest_substring_k_distinct("aa", 1) == 2
    assert length_of_longest_substring_k_distinct("", 2) == 0
    print("Passed.")

    print("Testing Evaluate Division...")
    eqs = [["a","b"],["b","c"]]
    vals = [2.0, 3.0]
    queries = [["a","c"],["b","a"],["a","e"],["a","a"],["x","x"]]
    res = calc_equation(eqs, vals, queries)
    assert res == [6.0, 0.5, -1.0, 1.0, -1.0]
    print("Passed.")

if __name__ == "__main__":
    test_google_questions()
    print("All Google interview tests passed!")
