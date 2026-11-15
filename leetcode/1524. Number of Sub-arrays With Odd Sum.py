1524. Number of Sub-arrays With Odd Sum



Given an array of integers arr, return the number of subarrays with an odd sum.

Since the answer can be very large, return it modulo 109 + 7.

 

Example 1:

Input: arr = [1,3,5]
Output: 4
Explanation: All subarrays are [[1],[1,3],[1,3,5],[3],[3,5],[5]]
All sub-arrays sum are [1,4,9,3,8,5].
Odd sums are [1,9,3,5] so the answer is 4.
Example 2:

Input: arr = [2,4,6]
Output: 0
Explanation: All subarrays are [[2],[2,4],[2,4,6],[4],[4,6],[6]]
All sub-arrays sum are [2,6,12,4,10,6].
All sub-arrays have even sum and the answer is 0.
Example 3:

Input: arr = [1,2,3,4,5,6,7]
Output: 16
 

Constraints:

1 <= arr.length <= 105
1 <= arr[i] <= 100



























class Solution:
    def numOfSubarrays(self, arr: List[int]) -> int:
        MOD = 10**9 + 7

        odd = 0
        even = 1
        prefix = 0
        ans = 0

        for num in arr:
            prefix += num

            if prefix % 2 == 0:
                ans += odd
                even += 1
            else:
                ans += even
                odd += 1

        return ans % MOD


















class Solution:
    def numOfSubarrays(self, arr: List[int]) -> int:
        MOD = 10**9+7
        prefix_sum = 0
        oddCount = 0

        for a in arr:
            prefix_sum+=a
            oddCount+=prefix_sum%2

        oddCount+=(len(arr)-oddCount)*oddCount

        return  oddCount%MOD





















class Solution:
    def numOfSubarrays(self, arr: List[int]) -> int:
        oddCount, prefixSum, mod = 0, 0, 1_000_000_007
        for a in arr:
            prefixSum += a
            oddCount += prefixSum % 2
        oddCount += (len(arr) - oddCount) * oddCount
        return oddCount % mod




















class Solution:
    def numOfSubarrays(self, arr: list[int]) -> int:
        prefixsum=0
        result=0
        mod=10**9+7
        oddcount=0
        for n in arr:
            prefixsum+=n
            oddcount+=prefixsum%2
        evencount=len(arr)-oddcount
        result=oddcount+(evencount*oddcount)
    
        return result%mod
                    

















class Solution:
    def numOfSubarrays(self, arr: list[int]) -> int:
        # count prefix sums by parity; odd subarray = pair of prefixes with different parity
        even, odd, parity, total = 1, 0, 0, 0
        for x in arr:
            parity ^= x & 1
            if parity:
                total += even
                odd += 1
            else:
                total += odd
                even += 1
        return total % (10**9 + 7)





















class Solution:
    def numOfSubarrays(self, arr: list[int]) -> int:
        MOD = 10**9 + 7
        odd, even = 0, 1
        ans = 0
        parity = 0
        
        for x in arr:
            parity ^= (x & 1) # Обновляем четность через XOR
            if parity == 0:
                even += 1
                ans += odd
            else:
                odd += 1
                ans += even
                
        return ans % MOD
