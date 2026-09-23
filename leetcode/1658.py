1658. Minimum Operations to Reduce X to Zero
Medium
Topics
premium lock icon
Companies
Hint
You are given an integer array nums and an integer x. In one operation, you can either remove the leftmost or the rightmost element from the array nums and subtract its value from x. Note that this modifies the array for future operations.

Return the minimum number of operations to reduce x to exactly 0 if it is possible, otherwise, return -1.

 

Example 1:

Input: nums = [1,1,4,2,3], x = 5
Output: 2
Explanation: The optimal solution is to remove the last two elements to reduce x to zero.
Example 2:

Input: nums = [5,6,7,8,9], x = 4
Output: -1
Example 3:

Input: nums = [3,2,20,1,1,3], x = 10
Output: 5
Explanation: The optimal solution is to remove the last three elements and the first two elements (5 operations in total) to reduce x to zero.
 

Constraints:

1 <= nums.length <= 105
1 <= nums[i] <= 104
1 <= x <= 109



















class Solution:
    def minOperations(self, nums: List[int], x: int) -> int:
        total = sum(nums)
        target = total - x

        if target < 0:
            return -1

        if target == 0:
            return len(nums)

        left = 0
        curr_sum = 0
        max_len = -1

        for right in range(len(nums)):
            curr_sum += nums[right]

            while curr_sum > target:
                curr_sum -= nums[left]
                left += 1

            if curr_sum == target:
                max_len = max(max_len, right - left + 1)

        if max_len == -1:
            return -1

        return len(nums) - max_len




























        class Solution:
    def minOperations(self, nums: List[int], x: int) -> int:
        n = len(nums)
        # prefixes = [0]
        # for num in nums:
        #     prefixes.append(num + prefixes[-1])
        
        # target = prefixes[-1] - x
        target = sum(nums) - x
        if target == 0:
            return n
        elif target < 0:
            return -1

        res = -1
        currsum = 0
        l = 0
        for r in range(n):
            currsum += nums[r]
            while currsum > target:
                currsum -= nums[l]
                l += 1
            
            if currsum == target:
                res = max(res, (r - l + 1))    
        return n - res if res != -1 else -1
    
























    class Solution:
    def minOperations(self, nums: list[int], x: int) -> int:
        # 删除的数字总和要等于 x
        # 所以剩下的连续子数组总和应该等于:
        target = sum(nums) - x

        # 如果 target < 0:
        # 说明整个 nums 的总和都小于 x
        # 无论怎么删都不可能达到 x
        if target < 0:
            return -1

        # 特殊情况:
        # 如果 target == 0
        # 说明我们必须把整个数组全部删掉
        if target == 0:
            return len(nums)

        left = 0
        window_sum = 0

        # 记录满足 sum == target 的最长 window
        max_len = -1

        for right in range(len(nums)):
            # 把 nums[right] 加进窗口
            window_sum += nums[right]

            # 因为所有 nums[i] 都是正数
            # 如果窗口和太大，只能移动 left 缩小窗口
            while window_sum > target:
                window_sum -= nums[left]
                left += 1

            # 找到一个和刚好为 target 的连续子数组
            if window_sum == target:
                max_len = max(max_len, right - left + 1)

        # 如果根本不存在这样的中间子数组
        if max_len == -1:
            return -1

        # 总长度 - 最长保留长度 = 最少删除次数
        return len(nums) - max_len
    

























    class Solution:
    def minOperations(self, nums: List[int], x: int) -> int:
        target = sum(nums) - x
        
        if target < 0:
            return -1
        
        if target == 0:
            return len(nums)
        
        left = 0
        current_sum = 0
        max_length = -1
        
        for right in range(len(nums)):
            current_sum += nums[right]
            
            while current_sum > target and left <= right:
                current_sum -= nums[left]
                left += 1
            
            if current_sum == target:
                max_length = max(max_length, right - left + 1)
        
        return len(nums) - max_length if max_length != -1 else -1


























        class Solution:
    def minOperations(self, nums: List[int], x: int) -> int:
        total_sum = sum(nums)
        target = total_sum - x
        if target < 0:
            return -1
        if target == 0:
            return len(nums)

        left = 0
        window_sum = 0
        max_len = -1

        for right in range(len(nums)):
            window_sum += nums[right]
            while window_sum > target:
                window_sum -= nums[left]
                left += 1
            if window_sum == target:
                max_len = max(max_len, right - left + 1)

        if max_len == -1:
            return -1
        else:
            return len(nums) - max_len
            













            