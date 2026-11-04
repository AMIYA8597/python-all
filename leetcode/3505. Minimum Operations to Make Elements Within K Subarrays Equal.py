3505. Minimum Operations to Make Elements Within K Subarrays Equal
Hard
Topics
premium lock icon
Companies
Hint
You are given an integer array nums and two integers, x and k. You can perform the following operation any number of times (including zero):

Increase or decrease any element of nums by 1.
Return the minimum number of operations needed to have at least k non-overlapping subarrays of size exactly x in nums, where all elements within each subarray are equal.

 

Example 1:

Input: nums = [5,-2,1,3,7,3,6,4,-1], x = 3, k = 2

Output: 8

Explanation:

Use 3 operations to add 3 to nums[1] and use 2 operations to subtract 2 from nums[3]. The resulting array is [5, 1, 1, 1, 7, 3, 6, 4, -1].
Use 1 operation to add 1 to nums[5] and use 2 operations to subtract 2 from nums[6]. The resulting array is [5, 1, 1, 1, 7, 4, 4, 4, -1].
Now, all elements within each subarray [1, 1, 1] (from indices 1 to 3) and [4, 4, 4] (from indices 5 to 7) are equal. Since 8 total operations were used, 8 is the output.
Example 2:

Input: nums = [9,-2,-2,-2,1,5], x = 2, k = 2

Output: 3

Explanation:

Use 3 operations to subtract 3 from nums[4]. The resulting array is [9, -2, -2, -2, -2, 5].
Now, all elements within each subarray [-2, -2] (from indices 1 to 2) and [-2, -2] (from indices 3 to 4) are equal. Since 3 operations were used, 3 is the output.
 

Constraints:

2 <= nums.length <= 105
-106 <= nums[i] <= 106
2 <= x <= nums.length
1 <= k <= 15
2 <= k * x <= nums.length


























class Solution:
    def minOperations(self, nums: List[int], x: int, k: int) -> int:
        n = len(nums)
        vals = sorted(set(nums))
        m = len(vals)
        rank = {v: i + 1 for i, v in enumerate(vals)}

        cnt = [0] * (m + 1)
        sm = [0] * (m + 1)

        def update(bit, i, d):
            while i <= m:
                bit[i] += d
                i += i & -i

        def query(bit, i):
            s = 0
            while i:
                s += bit[i]
                i -= i & -i
            return s

        def add(v, d):
            i = rank[v]
            update(cnt, i, d)
            update(sm, i, v * d)

        def median_cost():
            t = (x + 1) // 2
            idx, step = 0, 1 << (m.bit_length() - 1)

            while step:
                nxt = idx + step
                if nxt <= m and cnt[nxt] < t:
                    idx = nxt
                    t -= cnt[nxt]
                step >>= 1

            idx += 1
            med = vals[idx - 1]

            lc = query(cnt, idx)
            ls = query(sm, idx)
            rc = x - lc
            rs = query(sm, m) - ls

            return med * lc - ls + rs - med * rc

        costs = []

        for i in range(n):
            add(nums[i], 1)

            if i >= x:
                add(nums[i - x], -1)

            if i >= x - 1:
                costs.append(median_cost())

        INF = float('inf')
        prev = [0] * (n + 1)

        for j in range(1, k + 1):
            curr = [INF] * (n + 1)

            for i in range(1, n + 1):
                curr[i] = curr[i - 1]

                if i >= x:
                    curr[i] = min(
                        curr[i],
                        prev[i - x] + costs[i - x]
                    )

            prev = curr

        return prev[n]

























from typing import List
from heapq import heappush, heappop
from collections import defaultdict
import numpy as np


class Solution:
    def minOperations(self, nums: List[int], x: int, k: int) -> int:
        n = len(nums)
        small = []   # max-heap (negated) : lower half
        large = []   # min-heap : upper half
        delayed = defaultdict(int)
        sSize = 0
        lSize = 0
        sSum = 0
        lSum = 0
        cost = [0] * (n - x + 1)

        def prune_small():
            nonlocal small
            while small:
                v = -small[0]
                if delayed[v] > 0:
                    delayed[v] -= 1
                    heappop(small)
                else:
                    break

        def prune_large():
            while large:
                v = large[0]
                if delayed[v] > 0:
                    delayed[v] -= 1
                    heappop(large)
                else:
                    break

        def balance():
            nonlocal sSize, lSize, sSum, lSum
            while sSize > lSize + 1:
                v = -heappop(small)
                sSize -= 1
                sSum -= v
                heappush(large, v)
                lSize += 1
                lSum += v
                prune_small()
            while sSize < lSize:
                v = heappop(large)
                lSize -= 1
                lSum -= v
                heappush(small, -v)
                sSize += 1
                sSum += v
                prune_large()

        for i in range(n):
            v = nums[i]
            if not small or v <= -small[0]:
                heappush(small, -v)
                sSize += 1
                sSum += v
            else:
                heappush(large, v)
                lSize += 1
                lSum += v
            balance()
            if i >= x:
                out = nums[i - x]
                delayed[out] += 1
                if out <= -small[0]:
                    sSize -= 1
                    sSum -= out
                    if out == -small[0]:
                        prune_small()
                else:
                    lSize -= 1
                    lSum -= out
                    if large and out == large[0]:
                        prune_large()
                balance()
            if i >= x - 1:
                med = -small[0]
                cost[i - x + 1] = med * sSize - sSum + lSum - med * lSize

        INF = 1 << 60
        m = n - x + 1
        cost_np = np.array(cost, dtype=np.int64)
        dp_prev = np.zeros(n + 1, dtype=np.int64)
        for _ in range(k):
            b = np.full(n + 1, INF, dtype=np.int64)
            b[x:] = dp_prev[0:m] + cost_np
            dp_prev = np.minimum.accumulate(b)
        return int(dp_prev[n])
























class Solution:
    def minOperations(self, nums: List[int], x: int, k: int) -> int:

        n = len(nums)

        l_size = x // 2
        r_size = x - l_size

        init = sorted([(num, i) for i, num in enumerate(nums[:x])])
        mid = init[l_size][0]

        left, right = [], []
        cost = 0
        for idx in range(x):
            num, i = init[idx]
            cost += abs(num - mid)
            
            if idx < l_size:
                heapq.heappush(left, (-num, -i))
            else:
                heapq.heappush(right, (num, i))

        costs = [float('inf')] * x + [cost]

        for i in range(x, n):
            old, new = nums[i-x], nums[i]
            
            is_old_left = False
            if old < right[0][0] or (old == right[0][0] and i-x < right[0][1]):
                is_old_left = True

            if is_old_left:
                while left and -left[0][1] <= i-x:
                    heapq.heappop(left)

                cost -= abs(old - mid)
                cost += abs(new - mid)
                    
                if new < right[0][0]:
                    
                    heapq.heappush(left, (-new, -i))

                else:
                   
                    pop_right, pop_right_i = heapq.heappop(right)
                    while right and right[0][1] <= i-x:
                        heapq.heappop(right)

                    heapq.heappush(left, (-pop_right, -pop_right_i))
                    heapq.heappush(right, (new, i))

                    cost += l_size * abs(right[0][0] - mid)
                    cost -= r_size * abs(right[0][0] - mid)
                    mid = right[0][0]

            else:
                while right and right[0][1] <= i-x:
                    heapq.heappop(right)

                cost -= abs(old - mid)
                cost += abs(new - mid)

                if new >= -left[0][0]:
                    
                    heapq.heappush(right, (new, i))
                    if mid < right[0][0]:
                        cost += l_size * abs(right[0][0] - mid)
                        cost -= r_size * abs(right[0][0] - mid)
                    else:
                        cost -= (l_size + 1) * abs(right[0][0] - mid)
                        cost += (r_size - 1) * abs(right[0][0] - mid)
                    mid = right[0][0]

                else:
                    
                    pop_left, pop_left_i = heapq.heappop(left)
                    pop_left, pop_left_i = -pop_left, -pop_left_i

                    while left and -left[0][1] <= i-x:
                        heapq.heappop(left)

                    heapq.heappush(left, (-new, -i))
                    heapq.heappush(right, (pop_left, pop_left_i))

                    cost -= abs(mid - pop_left)
                    cost += (r_size - 1) * abs(mid - pop_left)
                    cost -= l_size * abs(mid - pop_left)
                    mid = pop_left
            
            costs.append(cost)

        dp = [float('inf')]
        for i in range(n):
            dp.append(min(dp[-1], costs[i+1]))

        for _ in range(1, k):
            ndp = [float('inf')] * x
            for i in range(x, n+1):
                ndp.append(min(ndp[-1], dp[i-x] + costs[i]))

            dp = ndp
        return dp[-1]





















class Solution:
    def minOperations(self, nums: List[int], x: int, k: int) -> int:
        n = len(nums)
        left, right = [], []
        delayed = defaultdict(int)
        left_size = right_size = 0
        sum_l = sum_r = 0
        ops = [0] * n

        def prune(h: List[int], sign: int) -> None:
            while h and delayed[sign * h[0]]:
                delayed[sign * h[0]] -= 1
                heappop(h)

        def balance() -> None:
            nonlocal left_size, right_size, sum_l, sum_r
            if left_size > right_size + 1:
                num = -heappop(left)
                heappush(right, num)
                sum_r += num
                sum_l -= num
                right_size += 1
                left_size -= 1
                prune(left, -1)
            elif right_size > left_size:
                num = heappop(right)
                heappush(left, -num)
                sum_l += num
                sum_r -= num
                left_size += 1
                right_size -= 1
                prune(right, 1)

        for i, num in enumerate(nums):
            if not left or num <= -left[0]:
                heappush(left, -num)
                left_size += 1
                sum_l += num
            else:
                heappush(right, num)
                right_size += 1
                sum_r += num
            balance()
            if i >= x:
                num = nums[i - x]
                delayed[num] += 1
                if num <= -left[0]:
                    left_size -= 1
                    sum_l -= num
                    if num == -left[0]:
                        prune(left, -1)
                else:
                    right_size -= 1
                    sum_r -= num
                    if num == right[0]:
                        prune(right, 1)
                balance()
            if i >= x - 1:
                mid = -left[0]
                ops[i] = sum_r - sum_l + mid * (left_size - right_size)

        dp = [[0] + [inf] * k for _ in range(n)]
        for j in range(1, k + 1):
            if j == 1:
                dp[x - 1][j] = ops[x - 1]
            else:
                dp[j * x - 1][j] = dp[(j - 1) * x - 1][j - 1] + ops[j * x - 1]
        for j in range(1, k + 1):
            for i in range(j * x, n):
                dp[i][j] = min(dp[i - x][j - 1] + ops[i], dp[i - 1][j])
        return dp[n - 1][k]
























class Solution:
    def minOperations(self, nums: List[int], x: int, k: int) -> int:
        n = len(nums)
        left, right = [], []
        delayed = defaultdict(int)
        left_size = right_size = 0
        sum_l = sum_r = 0
        ops = [0] * n

        def prune(h: List[int], sign: int) -> None:
            while h and delayed[sign * h[0]]:
                delayed[sign * h[0]] -= 1
                heappop(h)

        def balance() -> None:
            nonlocal left_size, right_size, sum_l, sum_r
            if left_size > right_size + 1:
                num = -heappop(left)
                heappush(right, num)
                sum_r += num
                sum_l -= num
                right_size += 1
                left_size -= 1
                prune(left, -1)
            elif right_size > left_size:
                num = heappop(right)
                heappush(left, -num)
                sum_l += num
                sum_r -= num
                left_size += 1
                right_size -= 1
                prune(right, 1)

        for i, num in enumerate(nums):
            if not left or num <= -left[0]:
                heappush(left, -num)
                left_size += 1
                sum_l += num
            else:
                heappush(right, num)
                right_size += 1
                sum_r += num
            balance()
            if i >= x:
                num = nums[i - x]
                delayed[num] += 1
                if num <= -left[0]:
                    left_size -= 1
                    sum_l -= num
                    if num == -left[0]:
                        prune(left, -1)
                else:
                    right_size -= 1
                    sum_r -= num
                    if num == right[0]:
                        prune(right, 1)
                balance()
            if i >= x - 1:
                mid = -left[0]
                ops[i] = sum_r - sum_l + mid * (left_size - right_size)

        dp = [[0] + [inf] * k for _ in range(n)]
        for j in range(1, k + 1):
            if j == 1:
                dp[x - 1][j] = ops[x - 1]
            else:
                dp[j * x - 1][j] = dp[(j - 1) * x - 1][j - 1] + ops[j * x - 1]
        for j in range(1, k + 1):
            for i in range(j * x, n):
                dp[i][j] = min(dp[i - x][j - 1] + ops[i], dp[i - 1][j])
        return dp[n - 1][k]
