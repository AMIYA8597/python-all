3420. Count Non-Decreasing Subarrays After K Operations


You are given an array nums of n integers and an integer k.

For each subarray of nums, you can apply up to k operations on it. In each operation, you increment any element of the subarray by 1.

Note that each subarray is considered independently, meaning changes made to one subarray do not persist to another.

Return the number of subarrays that you can make non-decreasing ​​​​​after performing at most k operations.

An array is said to be non-decreasing if each element is greater than or equal to its previous element, if it exists.

 

Example 1:

Input: nums = [6,3,1,2,4,4], k = 7

Output: 17

Explanation:

Out of all 21 possible subarrays of nums, only the subarrays [6, 3, 1], [6, 3, 1, 2], [6, 3, 1, 2, 4] and [6, 3, 1, 2, 4, 4] cannot be made non-decreasing after applying up to k = 7 operations. Thus, the number of non-decreasing subarrays is 21 - 4 = 17.

Example 2:

Input: nums = [6,3,1,3,6], k = 4

Output: 12

Explanation:

The subarray [3, 1, 3, 6] along with all subarrays of nums with three or fewer elements, except [6, 3, 1], can be made non-decreasing after k operations. There are 5 subarrays of a single element, 4 subarrays of two elements, and 2 subarrays of three elements except [6, 3, 1], so there are 1 + 5 + 4 + 2 = 12 subarrays that can be made non-decreasing.

 

Constraints:

1 <= nums.length <= 105
1 <= nums[i] <= 109
1 <= k <= 109


























class Solution:
    def countNonDecreasingSubarrays(self, nums: list[int], k: int) -> int:
        n = len(nums)

        # Monotonic stack: (value, count)
        stack = []

        # Segment tree for range sums
        size = 1
        while size < n:
            size <<= 1

        tree = [0] * (2 * size)

        def update(i, val):
            i += size
            tree[i] = val

            while i > 1:
                i >>= 1
                tree[i] = tree[2 * i] + tree[2 * i + 1]

        def query(l, r):
            res = 0
            l += size
            r += size

            while l < r:
                if l & 1:
                    res += tree[l]
                    l += 1
                if r & 1:
                    r -= 1
                    res += tree[r]

                l >>= 1
                r >>= 1

            return res

        ans = 0
        left = 0

        for right in range(n):
            x = nums[right]
            count = 1

            while stack and stack[-1][0] < x:
                val, cnt = stack.pop()
                count += cnt

            stack.append((x, count))

            # Calculate operations needed
            # (Implementation continues with range maintenance)
            update(right, x)

            while left <= right:
                # Check whether current window is valid
                # using prefix maximum increments
                cost = 0
                mx = 0

                for i in range(left, right + 1):
                    mx = max(mx, nums[i])
                    cost += mx - nums[i]

                if cost <= k:
                    break

                left += 1

            ans += right - left + 1

        return ans

























class Solution:
    def countNonDecreasingSubarrays(self, nums: List[int], k: int) -> int:
        cost = 0
        queue = Deque([(nums[-1], 1)])
        res = 1
        back = len(nums)-1
        for i in range(len(nums)-2, -1, -1):
            cur = nums[i]
            cnt = 1

            while queue and queue[-1][0] < cur:
                lesser, count = queue.pop()
                cnt += count
                cost += (cur-lesser) * count
            queue.append((cur, cnt))
            while cost > k:
                more, count = queue.popleft()
                count -= 1
                cost -= (more-nums[back])
                back -= 1
                if count > 0:
                    queue.appendleft((more, count))

            res += back - i + 1
        return res


























class Solution:
    def countNonDecreasingSubarrays(self, nums: List[int], k: int) -> int:

        right = len(nums) - 1
        total_cost = 0
        q = deque() # reqval, count
        res = 0

        for left in range(len(nums)-1, -1, -1):
            x = nums[left]
            c = 1

            while q and q[0][0] < x:
                value, count = q.popleft()    
                total_cost += (x - value) * count
                c += count
            
            q.appendleft((x,c))
                
            while k < total_cost:
                value, c = q.pop()

                total_cost -= value - nums[right]
                right -= 1

                if c > 1:
                    q.append((value, c - 1))

            res += right - left + 1
        
        return res





       
        
