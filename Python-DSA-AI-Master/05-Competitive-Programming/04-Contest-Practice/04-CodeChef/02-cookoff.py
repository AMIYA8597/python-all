"""
CodeChef Cook-Off Practice
==========================

Overview
--------
The CodeChef Cook-Off is a short contest (typically 2.5 hours) with 5 to 7 problems.
Speed, accuracy, and quick thinking are critical. The problems usually revolve around
greedy algorithms, ad-hoc logic, string manipulation, and standard dynamic programming.
Because time is limited, writing bug-free code quickly is more important than knowing
highly obscure data structures.

Learning Objectives:
1. Develop speed in translating ad-hoc logic into clean Python code.
2. Master greedy algorithms and standard two-pointer techniques.
3. Write robust edge-case handling on the first try.
4. Utilize Python's built-in tools for rapid development.

Concept Explanation
-------------------
A common Cook-Off problem might ask you to find the longest contiguous subarray that
satisfies a certain property (e.g., sum <= K, or max difference between elements is <= D).
The Two-Pointer (or Sliding Window) technique is perfect for this. It allows us to 
process the array in O(N) time instead of O(N^2), which is crucial for passing the
typical N <= 10^5 constraints.

Basic to Professional Implementation
------------------------------------
We implement a Sliding Window solver to find the length of the longest subarray with 
a sum less than or equal to a given limit `K`.
"""

from typing import List

def solve_cookoff_longest_subarray_basic(arr: List[int], k: int) -> int:
    """
    Basic O(N^2) implementation. Too slow for Cook-Off problems where N=10^5.
    """
    max_len = 0
    n = len(arr)
    for i in range(n):
        current_sum = 0
        for j in range(i, n):
            current_sum += arr[j]
            if current_sum <= k:
                max_len = max(max_len, j - i + 1)
            else:
                break
    return max_len

def solve_cookoff_longest_subarray_pro(arr: List[int], k: int) -> int:
    """
    Professional O(N) Sliding Window implementation.
    This is what you should write during a Cook-Off to pass time limits.
    Assumes non-negative integers in the array.
    """
    max_len = 0
    window_sum = 0
    left = 0
    
    for right in range(len(arr)):
        window_sum += arr[right]
        
        # Shrink window from the left if sum exceeds k
        while window_sum > k and left <= right:
            window_sum -= arr[left]
            left += 1
            
        max_len = max(max_len, right - left + 1)
        
    return max_len


# --- Advanced Concept: String Greedy Logic ---
def solve_cookoff_greedy_string(s: str) -> str:
    """
    Another common Cook-Off pattern: string manipulation.
    Problem: Given a string of lowercase letters, remove all adjacent duplicate characters.
    Continue this until no more adjacent duplicates exist.
    
    Example: "abbaca" -> "aaca" -> "ca"
    Implementation uses a stack for O(N) time.
    """
    stack = []
    for char in s:
        if stack and stack[-1] == char:
            stack.pop()
        else:
            stack.append(char)
    return "".join(stack)


if __name__ == "__main__":
    # Tests and Assertions
    print("Testing Sliding Window (Longest Subarray)...")
    arr = [3, 1, 2, 7, 4, 2, 1, 1, 5]
    k = 8
    # Valid subarrays: [3,1,2] sum=6, len=3
    # [1,2,7] X
    # [4,2,1,1] sum=8, len=4 -> Max length
    assert solve_cookoff_longest_subarray_pro(arr, k) == 4, "Sliding window failed"
    assert solve_cookoff_longest_subarray_pro([], 5) == 0, "Empty array failed"
    assert solve_cookoff_longest_subarray_pro([10, 20], 5) == 0, "No valid subarray failed"
    
    print("Testing Greedy String Manipulation...")
    assert solve_cookoff_greedy_string("abbaca") == "ca", "String stack test failed"
    assert solve_cookoff_greedy_string("azxxzy") == "ay", "String stack test 2 failed"
    
    print("All tests passed!")

"""
Complexity Analysis:
- `solve_cookoff_longest_subarray_pro`:
  Time Complexity: O(N), as both `left` and `right` pointers move forward at most N times.
  Space Complexity: O(1), only integer variables are maintained.
- `solve_cookoff_greedy_string`:
  Time Complexity: O(N) where N is string length, iterating once.
  Space Complexity: O(N) worst case if no duplicates, to store the stack.

Common Mistakes:
- In sliding window, forgetting the `left <= right` condition which can lead to index out of bounds or negative sums if not careful.
- Writing O(N^2) string concatenations instead of using a stack.

Interview Challenge:
How would you modify the sliding window approach if the array could contain negative numbers?
(Hint: The sliding window property breaks. You would need a prefix sum hash map or a monotonic queue).
"""
