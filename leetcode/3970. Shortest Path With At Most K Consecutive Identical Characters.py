3970. Shortest Path With At Most K Consecutive Identical Characters


You are given an integer n representing the number of nodes in a directed weighted graph, numbered from 0 to n - 1. This is represented by a 2D integer array edges, where edges[i] = [ui, vi, wi] represents a directed edge from node ui to node vi with weight wi.

You are also given a string labels of length n, where labels[i] is the character assigned to node i, and an integer k.

Return the minimum total edge weight of a path from node 0 to node n - 1 such that the concatenation of the labels of the nodes along the path contains at most k consecutive identical characters. If no valid path exists, return -1.

 

Example 1:

Input: n = 3, edges = [[0,1,1],[1,2,1],[0,2,3]], labels = "aab", k = 1

Output: 3

Explanation:

The optimal valid path from node 0 to node 2 is as follows:

Use edges[2] = [0, 2, 3] to reach node 2 with a weight wi = 3.
The corresponding concatenation of labels is "ab", which satisfies at most k = 1 consecutive identical characters. Thus, the answer is 3.
Example 2:

Input: n = 3, edges = [[0,1,1],[1,2,1],[0,2,3]], labels = "aab", k = 2

Output: 2

Explanation:

The optimal valid path from node 0 to node 2 is as follows:

Use edges[0] = [0, 1, 1] to reach node 1 with weight wi = 1.
Use edges[1] = [1, 2, 1] to reach node 2 with weight wi = 1.
The corresponding concatenation of labels is "aab", which satisfies at most k = 2 consecutive identical characters. Thus, the answer is 2.
Example 3:

Input: n = 3, edges = [[0,1,1],[1,2,1]], labels = "aaa", k = 2

Output: -1

Explanation:

There is no valid path from node 0 to node 2 that satisfies at most k = 2 consecutive identical characters. Thus, the answer is -1.

 

Constraints:

1 <= n == labels.length <= 5 * 104
0 <= edges.length <= 5 * 104
edges[i] == [ui, vi, wi]
0 <= ui, vi <= n - 1
ui != vi
1 <= wi <= 104
labels consists of lowercase English letters
1 <= k <= 50









































from typing import List
import heapq

class Solution:
    def shortestPath(self, n: int, edges: List[List[int]], labels: str, k: int) -> int:
        graph = [[] for _ in range(n)]

        for u, v, w in edges:
            graph[u].append((v, w))

        INF = float('inf')
        dist = [[INF] * (k + 1) for _ in range(n)]

        dist[0][1] = 0
        pq = [(0, 0, 1)]

        while pq:
            cost, u, count = heapq.heappop(pq)

            if cost != dist[u][count]:
                continue

            if u == n - 1:
                return cost

            for v, w in graph[u]:
                if labels[u] == labels[v]:
                    if count == k:
                        continue
                    new_count = count + 1
                else:
                    new_count = 1

                new_cost = cost + w

                if new_cost < dist[v][new_count]:
                    dist[v][new_count] = new_cost
                    heapq.heappush(pq, (new_cost, v, new_count))

        return -1



















import heapq

class Solution:
    def shortestPath(self, n: int, edges: list[list[int]], labels: str, k: int) -> int:
        return self.Dijkstra(n, self.edges2table(n, edges), labels, k)

    def edges2table(self, n, edges):
        table = [[] for _ in range(n)]
        for u, v, w in edges:
            table[u].append((v, w))

        return table

    def Dijkstra(self, n: int, table: list[list[tuple]], labels: str, k: int):
        visited = [False for _ in range(n)]

        q = [(0, 0, 1, labels[0])]

        while q:
            weight, now, cnt, last_char = heapq.heappop(q)

            if now == n - 1:
                return weight

            if visited[now]:
                continue

            for v, w in table[now]:
                if visited[v]:
                    continue

                if last_char == labels[v]:
                    if cnt + 1 > k:
                        continue
                    heapq.heappush(q, (weight + w, v, cnt + 1, last_char))
                    visited[now] = True
                else:
                    heapq.heappush(q, (weight + w, v, 1, labels[v]))
                    visited[now] = True

        return -1



























class Solution:
    def shortestPath(self, n: int, edges: List[List[int]], labels: str, k: int) -> int:
        graph = [[] for _ in range(n)]
        for u, v, w in edges:
            graph[u].append((v, w, labels[u] == labels[v]))

        done = [k + 1] * n  # min run length among popped states per node
        heap = [(0, 0, 1)]
        last = n - 1

        while heap:
            d, u, r = heappop(heap)
            if r >= done[u]:  # dominated by an earlier (cheaper-or-equal) pop
                continue
            done[u] = r
            if u == last:
                return d
            for v, w, same in graph[u]:
                nr = r + 1 if same else 1
                if nr < done[v]:  # also enforces nr <= k, since done starts at k+1
                    heappush(heap, (d + w, v, nr))

        return -1





















class Solution:
    def shortestPath(self, n: int, edges: List[List[int]], labels: str, k: int) -> int:
        graph = [[] for _ in range(n)]
        for u, v, w in edges:
            graph[u].append((v, w, labels[u] == labels[v]))

        done = [k + 1] * n  # min run length among popped states per node
        heap = [(0, 0, 1)]
        last = n - 1

        while heap:
            d, u, r = heappop(heap)
            if r >= done[u]:  # dominated by an earlier (cheaper-or-equal) pop
                continue
            done[u] = r
            if u == last:
                return d
            for v, w, same in graph[u]:
                nr = r + 1 if same else 1
                if nr < done[v]:  # also enforces nr <= k, since done starts at k+1
                    heappush(heap, (d + w, v, nr))

        return -1
