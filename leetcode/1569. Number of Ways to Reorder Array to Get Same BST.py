1569. Number of Ways to Reorder Array to Get Same BST
Hard
Topics
premium lock icon
Companies
Hint
Given an array nums that represents a permutation of integers from 1 to n. We are going to construct a binary search tree (BST) by inserting the elements of nums in order into an initially empty BST. Find the number of different ways to reorder nums so that the constructed BST is identical to that formed from the original array nums.

For example, given nums = [2,1,3], we will have 2 as the root, 1 as a left child, and 3 as a right child. The array [2,3,1] also yields the same BST but [3,2,1] yields a different BST.
Return the number of ways to reorder nums such that the BST formed is identical to the original BST formed from nums.

Since the answer may be very large, return it modulo 109 + 7.

 

Example 1:


Input: nums = [2,1,3]
Output: 1
Explanation: We can reorder nums to be [2,3,1] which will yield the same BST. There are no other ways to reorder nums which will yield the same BST.
Example 2:


Input: nums = [3,4,5,1,2]
Output: 5
Explanation: The following 5 arrays will yield the same BST: 
[3,1,2,4,5]
[3,1,4,2,5]
[3,1,4,5,2]
[3,4,1,2,5]
[3,4,1,5,2]
Example 3:


Input: nums = [1,2,3]
Output: 0
Explanation: There are no other orderings of nums that will yield the same BST.
 

Constraints:

1 <= nums.length <= 1000
1 <= nums[i] <= nums.length
All integers in nums are distinct.




































class Solution:
    def numOfWays(self, nums: list[int]) -> int:
        MOD = 10**9 + 7
        n = len(nums)

        comb = [[0] * n for _ in range(n)]

        for i in range(n):
            comb[i][0] = 1
            comb[i][i] = 1
            for j in range(1, i):
                comb[i][j] = (comb[i - 1][j - 1] + comb[i - 1][j]) % MOD

        def solve(arr):
            if len(arr) <= 2:
                return 1

            root = arr[0]
            left = [x for x in arr[1:] if x < root]
            right = [x for x in arr[1:] if x > root]

            left_ways = solve(left)
            right_ways = solve(right)

            ways = comb[len(left) + len(right)][len(left)]

            return (ways * left_ways * right_ways) % MOD

        return (solve(nums) - 1) % MOD














# https://www.youtube.com/@0x3f
class Solution:
    def numOfWays(self, nums: list[int]) -> int:
        MOD = 1_000_000_007
        # 数组模拟双向链表
        n = len(nums)
        prev = [i - 1 for i in range(n + 2)]
        next = [i + 1 for i in range(n + 2)]

        # size[x] 表示子树 x 的大小（节点个数）
        size = [0] * (n + 2)

        # 分母
        mul = 1

        # 自底向上构建二叉搜索树
        for x in reversed(nums):
            size[x] = 1

            # 加上左子树的大小
            left = prev[x]
            if size[left] > 0:
                size[x] += size[left]
                # 删除节点 left
                pl = prev[left]
                prev[x] = pl
                next[pl] = x

            # 加上右子树的大小
            right = next[x]
            if size[right] > 0:
                size[x] += size[right]
                # 删除节点 right
                nr = next[right]
                prev[nr] = x
                next[x] = nr

            mul = mul * size[x] % MOD

        fac = 1  # 分子
        for i in range(2, n + 1):
            fac = fac * i % MOD

        return (fac * pow(mul, -1, MOD) - 1) % MOD


















from math import comb

class Solution:
    def numOfWays(self, nums: list[int]) -> int:
        MOD = 10**9 + 7
        def ways(arr):
            if len(arr) <= 2: return 1
            root = arr[0]
            left = [x for x in arr if x < root]
            right = [x for x in arr if x > root]
            return comb(len(left) + len(right), len(left)) * ways(left) * ways(right) % MOD
        return (ways(nums) - 1) % MOD
