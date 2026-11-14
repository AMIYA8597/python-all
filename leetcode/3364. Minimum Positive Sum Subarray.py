3364. Minimum Positive Sum Subarray 




You are given an integer array nums and two integers l and r. Your task is to find the minimum sum of a subarray whose size is between l and r (inclusive) and whose sum is greater than 0.

Return the minimum sum of such a subarray. If no such subarray exists, return -1.

A subarray is a contiguous non-empty sequence of elements within an array.

 

Example 1:

Input: nums = [3, -2, 1, 4], l = 2, r = 3

Output: 1

Explanation:

The subarrays of length between l = 2 and r = 3 where the sum is greater than 0 are:

[3, -2] with a sum of 1
[1, 4] with a sum of 5
[3, -2, 1] with a sum of 2
[-2, 1, 4] with a sum of 3
Out of these, the subarray [3, -2] has a sum of 1, which is the smallest positive sum. Hence, the answer is 1.

Example 2:

Input: nums = [-2, 2, -3, 1], l = 2, r = 3

Output: -1

Explanation:

There is no subarray of length between l and r that has a sum greater than 0. So, the answer is -1.

Example 3:

Input: nums = [1, 2, 3, 4], l = 2, r = 4

Output: 3

Explanation:

The subarray [1, 2] has a length of 2 and the minimum sum greater than 0. So, the answer is 3.

 

Constraints:

1 <= nums.length <= 100
1 <= l <= r <= nums.length
-1000 <= nums[i] <= 1000

























class Solution:
    def minimumSumSubarray(self, nums: List[int], l: int, r: int) -> int:
        n = len(nums)
        ans = float('inf')

        for i in range(n):
            curr_sum = 0

            for j in range(i, min(n, i + r)):
                curr_sum += nums[j]

                length = j - i + 1

                if length >= l and curr_sum > 0:
                    ans = min(ans, curr_sum)

        return ans if ans != float('inf') else -1

























class Solution:
    from bisect import bisect_left, insort

    def minimumSumSubarray(self, nums: List[int], l: int, r: int) -> int:
        n = len(nums)

        prefix = [0] * (n + 1)

        for i in range(n):
            prefix[i + 1] = prefix[i] + nums[i]

        window = []
        ans = float('inf')

        for i in range(l, n + 1):

            insort(window, prefix[i - l])

            if i - r - 1 >= 0:
                value = prefix[i - r - 1]
                pos = bisect_left(window, value)
                window.pop(pos)

            pos = bisect_left(window, prefix[i])

            if pos > 0:
                candidate = prefix[i] - window[pos - 1]

                if candidate > 0:
                    ans = min(ans, candidate)

        return -1 if ans == float('inf') else ans





















class Solution:
    def minimumSumSubarray(self, nums: List[int], l: int, r: int) -> int:
        n = len(nums)
        min_sum = float('inf')

        for L in range(l, r + 1):
            if L > n:
                break
            window = sum(nums[:L])          # O(L) once
            if 0 < window < min_sum:
                min_sum = window
            for i in range(1, n - L + 1):
                window += nums[i + L - 1] - nums[i - 1]   # O(1) per slide
                if 0 < window < min_sum:
                    min_sum = window

        return min_sum if min_sum != float('inf') else -1
























class Solution:
    def minimumSumSubarray(self, nums: List[int], l: int, r: int) -> int:
        n=len(nums)
        prefix=[0]*(n+1)
        for i,x in enumerate(nums):
            prefix[i+1] = prefix[i]+x
        best=float('inf')
        for length in range(l,r+1):
            for i in range(n - length+1):
                s = prefix[i + length] - prefix[i]
                if s > 0:
                    best=min(best,s)
        return -1 if best == float('inf') else best
























class Solution:
    def minimumSumSubarray(self, nums: list[int], l: int, r: int) -> int:
        prefix_sum = [0, *accumulate(nums)]

        min_sum = inf
        n = len(nums)
        for length in range(l, min(r, n) + 1):
            for start in range(n - length + 1):
                total = prefix_sum[start + length] - prefix_sum[start]
                if 0 < total < min_sum:
                    min_sum = total

        return -1 if min_sum == inf else min_sum
