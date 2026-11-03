3736. Minimum Moves to Equal Array Elements III





You are given an integer array nums.

In one move, you may increase the value of any single element nums[i] by 1.

Return the minimum total number of moves required so that all elements in nums become equal.

 

Example 1:

Input: nums = [2,1,3]

Output: 3

Explanation:

To make all elements equal:

Increase nums[0] = 2 by 1 to make it 3.
Increase nums[1] = 1 by 1 to make it 2.
Increase nums[1] = 2 by 1 to make it 3.
Now, all elements of nums are equal to 3. The minimum total moves is 3.

Example 2:

Input: nums = [4,4,5]

Output: 2

Explanation:

To make all elements equal:

Increase nums[0] = 4 by 1 to make it 5.
Increase nums[1] = 4 by 1 to make it 5.
Now, all elements of nums are equal to 5. The minimum total moves is 2.

 

Constraints:

1 <= nums.length <= 100
1 <= nums[i] <= 100




























class Solution:
    def minMoves(self, nums: List[int]) -> int:
        mx = max(nums)
        return sum(mx - num for num in nums)














class Solution:
    def minMoves(self, nums: List[int]) -> int:
        return max(nums) * len(nums) - sum(nums)










# LeetCode 3736 — Minimum Moves to Equal Array Elements III

Let's understand this problem from zero level, step by step, and then implement the Python solution.

## 1. Understand the problem

You are given an integer array `nums`.

You can perform only ONE operation:

- Increase any element by `1`.
- You cannot decrease any element.
- Your goal is to make every element equal.
- Return the minimum number of total operations.

Important: Since we can only increase elements, we must make every element equal to the largest element.

## 2. Example 1

Input:

```
nums = [2, 1, 3]
```

Our goal is to make all elements equal.

Currently:

```
2    1    3
```

The maximum element is `3`.

Therefore, we need to convert every element into `3`.

Step-by-step:

```
Element 2:
2 → 3
Moves = 1

Element 1:
1 → 2 → 3
Moves = 2

Element 3:
Already 3
Moves = 0
```

Final array:

```
[3, 3, 3]
```

Total moves:

```
1 + 2 + 0 = 3
```

Output:

```
3
```

## 3. Understand the logic

There are two important things:

1. Find the maximum element using `max(nums)`.
2. Calculate how many increments each element needs to reach that maximum.

The formula is:

\\[ \text{Minimum Moves} = \sum\_{i=0}^{n-1}(\text{max}(nums)-nums[i]) \\]

In simple English:

Required moves = Maximum value - Current value

Then add the moves of all elements.

## 4. Python solution

Optimal Solution

```
class Solution:    def minMoves(self, nums: List[int]) -> int:        mx = max(nums)        moves = 0        for num in nums:            moves += mx - num        return moves
```

## 5. Dry run (line-by-line execution)

Consider:

```
nums = [4, 4, 5]
```

Step 1: Find maximum.

```
mx = max(nums)
```

Result:

```
mx = 5
```

Step 2: Initialize moves.

```
moves = 0
```

Step 3: Run the loop.

| Iteration | num | mx - num  | moves |
| --------- | --- | --------- | ----- |
| 1         | 4   | 5 - 4 = 1 | 1     |
| 2         | 4   | 5 - 4 = 1 | 2     |
| 3         | 5   | 5 - 5 = 0 | 2     |

Step 4: Return the answer.

```
return moves
```

Output:

```
2
```

## 6. Complexity analysis

Let `n` be the number of elements in the array.

| Operation             | Time complexity |
| --------------------- | --------------- |
| Find maximum          | O(n)            |
| Iterate through array | O(n)            |
| Calculate total moves | O(n)            |

- Time Complexity: \\(O(n)\\)
- Space Complexity: \\(O(1)\\)

We don't create another array or use any additional data structure.

## 7. Important concepts to remember

- `max(nums)` → Finds the largest element.
- `for num in nums` → Visits every element.
- `mx - num` → Calculates the increments needed.
- `moves += ...` → Adds the increments to the total.

Interview takeaway: Whenever a problem allows only increasing elements and asks to make all elements equal with minimum operations, consider making every element equal to the maximum element.

This is a simple Greedy approach.















