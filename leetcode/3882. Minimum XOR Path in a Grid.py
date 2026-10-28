3882. Minimum XOR Path in a Grid
Medium
Topics
premium lock icon
Companies
Hint
You are given a 2D integer array grid of size m * n.

You start at the top-left cell (0, 0) and want to reach the bottom-right cell (m - 1, n - 1).

At each step, you may move either right or down.

The cost of a path is defined as the bitwise XOR of all the values in the cells along that path, including the start and end cells.

Return the minimum possible XOR value among all valid paths from (0, 0) to (m - 1, n - 1).

 

Example 1:

Input: grid = [[1,2],[3,4]]

Output: 6

Explanation:

There are two valid paths:

(0, 0) → (0, 1) → (1, 1) with XOR: 1 XOR 2 XOR 4 = 7
(0, 0) → (1, 0) → (1, 1) with XOR: 1 XOR 3 XOR 4 = 6
The minimum XOR value among all valid paths is 6.

Example 2:

Input: grid = [[6,7],[5,8]]

Output: 9

Explanation:

There are two valid paths:

(0, 0) → (0, 1) → (1, 1) with XOR: 6 XOR 7 XOR 8 = 9
(0, 0) → (1, 0) → (1, 1) with XOR: 6 XOR 5 XOR 8 = 11
The minimum XOR value among all valid paths is 9.

Example 3:

Input: grid = [[2,7,5]]

Output: 0

Explanation:

There is only one valid path:

(0, 0) → (0, 1) → (0, 2) with XOR: 2 XOR 7 XOR 5 = 0
The XOR value of this path is 0, which is the minimum possible.

 

Constraints:

1 <= m == grid.length <= 1000
1 <= n == grid[i].length <= 1000
m * n <= 1000
0 <= grid[i][j] <= 1023​























class Solution:
    def minCost(self, grid: list[list[int]]) -> int:
        m, n = len(grid), len(grid[0])

        dp = [[set() for _ in range(n)] for _ in range(m)]
        dp[0][0].add(grid[0][0])

        for i in range(m):
            for j in range(n):
                if i == 0 and j == 0:
                    continue

                if i > 0:
                    for x in dp[i - 1][j]:
                        dp[i][j].add(x ^ grid[i][j])

                if j > 0:
                    for x in dp[i][j - 1]:
                        dp[i][j].add(x ^ grid[i][j])

        return min(dp[m - 1][n - 1])










# For each node, store a bitvector "path" where `path[i]` is set to 1
# iff there is a path to the node whose xor is `i`. To calculate the
# mask array for a node, first we OR the paths of the left and top cell.
# Then, if bit 0 of the node is set, we swap each pair of bits;
# if bit 1 is set, we swap each group of 2 bits; if bit 2 is set,
# we swap each group of 4 bits, etc.

# swapmask[0] will mask bits 0, 2, 4, 6, 8, 10, 12, 14, ...
# swapmask[1] will mask bits 0, 1, 4, 5, 8, 9, 12, 13, ...
# swapmask[2] will mask bits 0, 1, 2, 3, 8, 9, 10, 11, ...
sm = (1 << (512))-1
swapmasks = [0]*9 + [sm]
for i in range(8, -1, -1):
    sm ^= sm << (1 << i)
    swapmasks[i] = sm

def swap_for(path, cell):
    for i in range(10):
        if cell & (1 << i):
            path = ((path & swapmasks[i]) << (1 << i)) | ((path & (swapmasks[i] << (1 << i))) >> (1 << i))
    return path

class Solution:
    def minCost(self, grid: list[list[int]]) -> int:
        m, n = len(grid), len(grid[0])
        paths = [0]*n
        xor = grid[0][0]
        paths[0] = 1 << xor
        for c in range(1, n):
            xor ^= grid[0][c]
            paths[c] = 1 << xor
        xor = grid[0][0]
        for r in range(1, m):
            xor ^= grid[r][0]
            paths[0] = 1 << xor
            for c in range(1, n):
                paths[c] = swap_for(paths[c-1] | paths[c], grid[r][c])

        return (paths[n-1] & -paths[n-1]).bit_length() - 1
















class Solution:
    def minCost(self, grid: list[list[int]]) -> int:
        m, n = len(grid), len(grid[0])
        prev = None
        for i in range(m):
            cur = [None]*n
            for j in range(n):
                if i == 0 and j == 0:
                    cur[0] = {grid[0][0]}
                    continue
                src = set()
                if j > 0:
                    src |= cur[j-1]
                if i > 0:
                    src |= prev[j]
                v = grid[i][j]
                cur[j] = {x ^ v for x in src}
            prev = cur
        return min(prev[n-1])










