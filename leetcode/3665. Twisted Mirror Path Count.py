3665. Twisted Mirror Path Count
Medium
Topics
premium lock icon
Companies
Hint
Given an m x n binary grid grid where:

grid[i][j] == 0 represents an empty cell, and
grid[i][j] == 1 represents a mirror.
A robot starts at the top-left corner of the grid (0, 0) and wants to reach the bottom-right corner (m - 1, n - 1). It can move only right or down. If the robot attempts to move into a mirror cell, it is reflected before entering that cell:

If it tries to move right into a mirror, it is turned down and moved into the cell directly below the mirror.
If it tries to move down into a mirror, it is turned right and moved into the cell directly to the right of the mirror.
If this reflection would cause the robot to move outside the grid boundaries, the path is considered invalid and should not be counted.

Return the number of unique valid paths from (0, 0) to (m - 1, n - 1).

Since the answer may be very large, return it modulo 109 + 7.

Note: If a reflection moves the robot into a mirror cell, the robot is immediately reflected again based on the direction it used to enter that mirror: if it entered while moving right, it will be turned down; if it entered while moving down, it will be turned right. This process will continue until either the last cell is reached, the robot moves out of bounds or the robot moves to a non-mirror cell.

 

Example 1:

Input: grid = [[0,1,0],[0,0,1],[1,0,0]]

Output: 5

Explanation:

Number	Full Path
1	(0, 0) → (0, 1) [M] → (1, 1) → (1, 2) [M] → (2, 2)
2	(0, 0) → (0, 1) [M] → (1, 1) → (2, 1) → (2, 2)
3	(0, 0) → (1, 0) → (1, 1) → (1, 2) [M] → (2, 2)
4	(0, 0) → (1, 0) → (1, 1) → (2, 1) → (2, 2)
5	(0, 0) → (1, 0) → (2, 0) [M] → (2, 1) → (2, 2)
[M] indicates the robot attempted to enter a mirror cell and instead reflected.

Example 2:

Input: grid = [[0,0],[0,0]]

Output: 2

Explanation:

Number	Full Path
1	(0, 0) → (0, 1) → (1, 1)
2	(0, 0) → (1, 0) → (1, 1)
Example 3:

Input: grid = [[0,1,1],[1,1,0]]

Output: 1

Explanation:

Number	Full Path
1	(0, 0) → (0, 1) [M] → (1, 1) [M] → (1, 2)
(0, 0) → (1, 0) [M] → (1, 1) [M] → (2, 1) goes out of bounds, so it is invalid.
 

Constraints:

m == grid.length
n == grid[i].length
2 <= m, n <= 500
grid[i][j] is either 0 or 1.
grid[0][0] == grid[m - 1][n - 1] == 0







































  class Solution:
    def uniquePaths(self, grid: List[List[int]]) -> int:
        MOD = 10**9 + 7
        m, n = len(grid), len(grid[0])

        dp = [0] * n

        for i in range(m):
            left = 0

            for j in range(n):
                if i == 0 and j == 0:
                    left = 1
                    dp[j] = 1
                    continue

                from_above = dp[j]
                from_left = left

                if i == m - 1 and j == n - 1:
                    return (from_above + from_left) % MOD

                if grid[i][j] == 0:
                    ways = (from_above + from_left) % MOD
                    dp[j] = ways
                    left = ways

                else:
                    dp[j] = from_left
                    left = from_above

                dp[j] %= MOD
                left %= MOD

        return 0






















class Solution:
    def uniquePaths(self, grid: List[List[int]]) -> int:

        m, n = len(grid), len(grid[0])
        curRow = [0] * n
        curRow[0] = 1

        for row in grid:
            prvRow, curRow, prvCel = curRow, [0] * n, 0
            
            for idx, (p, c) in enumerate(zip(prvRow, curRow)):
                if row[idx] == 0:
                    curRow[idx], prvCel = prvCel + p, prvCel + p + c
                else:
                    curRow[idx], prvCel = prvCel + c, p

        return curRow[-1] %1_000_000_007


























class Solution:
    def uniquePaths(self, grid: List[List[int]]) -> int:

        m, n = len(grid), len(grid[0])
        curRow = [0] * n
        curRow[0] = 1

        for row in grid:
            prvRow, curRow, prvCel = curRow, [0] * n, 0
            
            for idx, (p, c) in enumerate(zip(prvRow, curRow)):
                if row[idx] == 0:
                    curRow[idx], prvCel = prvCel + p, prvCel + p + c
                else:
                    curRow[idx], prvCel = prvCel + c, p

        return curRow[-1] %1_000_000_007




















class Solution:
    def uniquePaths(self, grid: list[list[int]]) -> int:
        MOD = 10**9 + 7
        m, n = len(grid), len(grid[0])
        
        # dp[c] = [paths_entering_moving_right, paths_entering_moving_down]
        dp = [[0, 0] for _ in range(n + 1)]
        
        # Base case: start with 1 path at the top-left boundary
        dp[1] = [1, 1]
        
        for r in range(m):
            for c in range(n):
                if grid[r][c] == 1:
                    # Mirror cell: Swap directions
                    # Incoming right-moving path turns down; 
                    # Incoming down-moving path turns right.
                    dp[c + 1] = [dp[c + 1][1], dp[c][0]]
                else:
                    # Empty cell: Sum incoming ways from left (dp[c][0]) and top (dp[c+1][1])
                    total_ways = (dp[c + 1][1] + dp[c][0]) % MOD
                    dp[c + 1] = [total_ways, total_ways]
                    
        return dp[n][1]






















from typing import List


class Solution:
    def uniquePaths(self, grid: List[List[int]]) -> int:
        MOD = 10 ** 9 + 7
        m = len(grid)
        n = len(grid[0])
        size = m * n

        # A[idx]: flat index of the cell where the robot finally lands when it
        #         attempts to enter cell `idx` while moving right
        #         (-1 if the reflections send it out of bounds).
        # B[idx]: same, when it attempts to enter cell `idx` while moving down.
        A = [-1] * size
        B = [-1] * size

        # Fill bottom-up, right-to-left.
        for i in range(m - 1, -1, -1):
            base = i * n
            row = grid[i]
            down_ok = (i + 1) < m
            for j in range(n - 1, -1, -1):
                idx = base + j
                if row[j] == 0:
                    A[idx] = idx
                    B[idx] = idx
                else:
                    # mirror: entered while moving right -> turned down,
                    # moves into the cell directly below the mirror
                    if down_ok:
                        A[idx] = B[idx + n]
                    # mirror: entered while moving down -> turned right,
                    # moves into the cell directly right of the mirror
                    if j + 1 < n:
                        B[idx] = A[idx + 1]

        dp = [0] * size
        dp[0] = 1

        for i in range(m):
            base = i * n
            row = grid[i]
            down_ok = (i + 1) < m
            for j in range(n):
                idx = base + j
                v = dp[idx]
                if not v or row[j]:
                    continue
                # try to move right (attempt to enter (i, j+1) moving right)
                if j + 1 < n:
                    t = A[idx + 1]
                    if t >= 0:
                        dp[t] = (dp[t] + v) % MOD
                # try to move down (attempt to enter (i+1, j) moving down)
                if down_ok:
                    t = B[idx + n]
                    if t >= 0:
                        dp[t] = (dp[t] + v) % MOD

        return dp[size - 1]
