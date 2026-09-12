"""
## A. Concept Name
Maximum Subarray Problem (Divide and Conquer Approach)

## B. Problem Statement
Find the contiguous subarray within a one-dimensional array of numbers which has the largest sum.

## C. Real-World Analogy
Imagine you are looking at historical stock prices over a period. You want to find the exact days to buy and sell to maximize your profit. This is equivalent to finding the maximum sum of daily price changes.

## D. Divide and Conquer Strategy
The array can be divided into two halves. The maximum subarray must lie in one of three places:
1. Entirely in the left half.
2. Entirely in the right half.
3. Crossing the midpoint.

## E. Time & Space Complexity
Time Complexity: O(N log N)
Space Complexity: O(log N) for the recursion stack.

## F. Visual Tracing
Array: [-2, 1, -3, 4, -1, 2, 1, -5, 4]
Midpoint divides it. We find max in left, max in right, and max crossing mid recursively.

## G. Edge Cases
- All negative numbers (should return the smallest negative number).
- Array of length 1 (returns the single element).
- All positive numbers (entire array is the answer).

## X. Project Connection
This concept is foundational for financial analysis modules in our AI project, specifically when calculating maximum drawdown or peak profit periods over large datasets.
"""

def find_max_crossing_subarray(arr, low, mid, high):
    left_sum = float('-inf')
    total = 0
    max_left = mid
    
    for i in range(mid, low - 1, -1):
        total += arr[i]
        if total > left_sum:
            left_sum = total
            max_left = i
            
    right_sum = float('-inf')
    total = 0
    max_right = mid + 1
    
    for i in range(mid + 1, high + 1):
        total += arr[i]
        if total > right_sum:
            right_sum = total
            max_right = i
            
    return (max_left, max_right, left_sum + right_sum)

def find_maximum_subarray(arr, low, high):
    if low == high:
        return (low, high, arr[low])
        
    mid = (low + high) // 2
    
    left_low, left_high, left_sum = find_maximum_subarray(arr, low, mid)
    right_low, right_high, right_sum = find_maximum_subarray(arr, mid + 1, high)
    cross_low, cross_high, cross_sum = find_max_crossing_subarray(arr, low, mid, high)
    
    if left_sum >= right_sum and left_sum >= cross_sum:
        return (left_low, left_high, left_sum)
    elif right_sum >= left_sum and right_sum >= cross_sum:
        return (right_low, right_high, right_sum)
    else:
        return (cross_low, cross_high, cross_sum)

def max_subarray(arr):
    if not arr:
        return 0
    _, _, max_sum = find_maximum_subarray(arr, 0, len(arr) - 1)
    return max_sum

if __name__ == "__main__":
    nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
    print(f"Maximum subarray sum is {max_subarray(nums)}")
