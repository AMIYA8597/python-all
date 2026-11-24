3411. Maximum Subarray With Equal Products


You are given an array of positive integers nums.

An array arr is called product equivalent if prod(arr) == lcm(arr) * gcd(arr), where:

prod(arr) is the product of all elements of arr.
gcd(arr) is the GCD of all elements of arr.
lcm(arr) is the LCM of all elements of arr.
Return the length of the longest product equivalent subarray of nums.

 

Example 1:

Input: nums = [1,2,1,2,1,1,1]

Output: 5

Explanation: 

The longest product equivalent subarray is [1, 2, 1, 1, 1], where prod([1, 2, 1, 1, 1]) = 2, gcd([1, 2, 1, 1, 1]) = 1, and lcm([1, 2, 1, 1, 1]) = 2.

Example 2:

Input: nums = [2,3,4,5,6]

Output: 3

Explanation: 

The longest product equivalent subarray is [3, 4, 5].

Example 3:

Input: nums = [1,2,3,1,4,5,1]

Output: 5

 

Constraints:

2 <= nums.length <= 100
1 <= nums[i] <= 10





























from math import gcd, lcm
from functools import reduce

class Solution:
    def maxLength(self, nums: List[int]) -> int:

        n = len(nums)
        ans = 0

        for i in range(n):
            product = 1
            g = 0
            l = 1

            for j in range(i, n):

                product *= nums[j]

                g = gcd(g, nums[j])
                l = lcm(l, nums[j])

                if product == g * l:
                    ans = max(ans, j - i + 1)

        return ans





















class Solution:
    def maxLength(self, nums: List[int]) -> int:
        # Prime factors for each number from 0 to 10
        PRIMES = (
            (),      # 0 (unused)
            (),      # 1 (no prime factors)
            (2,),    # 2
            (3,),    # 3
            (2,),    # 4
            (5,),    # 5
            (2, 3),  # 6
            (7,),    # 7
            (2,),    # 8
            (3,),    # 9
            (2, 5),  # 10
        )

        # Last seen index for primes 2, 3, 5, 7 (using array indices 0..7)
        last_seen = [-1] * 8
        res = min(len(nums), 2)
        start = 0

        for end, x in enumerate(nums):
            for p in PRIMES[x]:
                if last_seen[p] >= start:
                    start = last_seen[p] + 1
                last_seen[p] = end
            
            curr_len = end - start + 1
            if curr_len > res:
                res = curr_len

        return res



















class Solution:
    def maxLength(self, nums: List[int]) -> int:
        MASKS = (0, 0, 1, 2, 1, 4, 3, 8, 1, 2, 5)
        res, mask, start = 2, 0, 0

        for end, x in enumerate(nums):
            while mask & MASKS[x]:
                mask ^= MASKS[nums[start]]
                start += 1
            mask |= MASKS[x]
            res = max(res, end - start + 1)

        return res





















class Solution:
    def maxLength(self, nums: List[int]) -> int:
        MASKS = (0, 0, 1, 2, 1, 4, 3, 8, 1, 2, 5)
        res, mask, start = 2, 0, 0

        for end, x in enumerate(nums):
            while mask & MASKS[x]:
                mask ^= MASKS[nums[start]]
                start += 1
            mask |= MASKS[x]
            res = max(res, end - start + 1)

        return res



















class Solution:
    def maxLength(self, nums: List[int]) -> int:
        from math import gcd

        res = 2
        prod_val = 1
        n = len(nums)
        start, end = 0, 0

        while end < n:
            while gcd(prod_val, nums[end]) > 1:
                prod_val //= nums[start]
                start += 1
            prod_val *= nums[end]
            res = max(res, end - start + 1)
            end += 1

        return res
