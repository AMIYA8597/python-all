2567. Minimum Score by Changing Two Elements


You are given an integer array nums.

The low score of nums is the minimum absolute difference between any two integers.
The high score of nums is the maximum absolute difference between any two integers.
The score of nums is the sum of the high and low scores.
Return the minimum score after changing two elements of nums.

 

Example 1:

Input: nums = [1,4,7,8,5]

Output: 3

Explanation:

Change nums[0] and nums[1] to be 6 so that nums becomes [6,6,7,8,5].
The low score is the minimum absolute difference: |6 - 6| = 0.
The high score is the maximum absolute difference: |8 - 5| = 3.
The sum of high and low score is 3.
Example 2:

Input: nums = [1,4,3]

Output: 0

Explanation:

Change nums[1] and nums[2] to 1 so that nums becomes [1,1,1].
The sum of maximum absolute difference and minimum absolute difference is 0.
 

Constraints:

3 <= nums.length <= 105
1 <= nums[i] <= 109

























class Solution:
    def minimizeSum(self, nums: List[int]) -> int:
        nums.sort()
        n = len(nums)

        return min(
            nums[n - 1] - nums[2],
            nums[n - 2] - nums[1],
            nums[n - 3] - nums[0]
        )

















class Solution:
    def minimizeSum(self, nums: List[int]) -> int:
        if len(nums)<=3:
            return 0
        
        small=sorted(heapq.nsmallest(3,nums))
        large=sorted(heapq.nlargest(3,nums))
        o0=large[0]-small[0]
        o1=large[1]-small[1]
        o2=large[2]-small[2]
        return min(o0,o1,o2)





















from heapq import nsmallest, nlargest
class Solution:
    def minimizeSum(self, nums: List[int]) -> int:
        # we can discard two smallest elements, two largest elements, one small and one large, evaluate all three possibilities
        # to decide that approach, find out the min value between third element - last element, third last element - first element, second largest element - second smallest element(middle values lie close to each other in this case)

        min1, min2, min3 = heapq.nsmallest(3, nums)
        max1, max2, max3 = heapq.nlargest(3, nums)

        return min(max3 - min1, max1 - min3, max2 - min2)

























class Solution:
    def minimizeSum(self, nums: List[int]) -> int:
        if len(nums) <= 3:
            return 0
        s1 = s2 = s3 = float('inf')    # 3 smallest, ascending
        l1 = l2 = l3 = float('-inf')   # 3 largest, descending
        for x in nums:
            if x < s1:   s1, s2, s3 = x, s1, s2
            elif x < s2: s2, s3 = x, s2
            elif x < s3: s3 = x
            if x > l1:   l1, l2, l3 = x, l1, l2
            elif x > l2: l2, l3 = x, l2
            elif x > l3: l3 = x    
        return min(
            l2 - s2,
            l1 - s3,
            l3 - s1
        )

        





















class Solution:
    def minimizeSum(self, nums: List[int]) -> int:
        if len(nums) <= 3:
            return 0
        s1 = s2 = s3 = 1000000   # 3 smallest, ascending
        l1 = l2 = l3 = -1   # 3 largest, descending
        for x in nums:
            if x < s1:   s1, s2, s3 = x, s1, s2
            elif x < s2: s2, s3 = x, s2
            elif x < s3: s3 = x
            if x > l1:   l1, l2, l3 = x, l1, l2
            elif x > l2: l2, l3 = x, l2
            elif x > l3: l3 = x    
        return min(
            l2 - s2,
            l1 - s3,
            l3 - s1
        )

        
        
