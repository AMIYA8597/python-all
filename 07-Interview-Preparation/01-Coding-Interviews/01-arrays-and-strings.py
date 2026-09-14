"""
# ==============================================================================
# LABORATORY: INTERVIEW PREPARATION (ARRAYS & STRINGS)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You are sitting in a FAANG interview. The interviewer asks:
# "Find the longest substring without repeating characters."
#
# If you write an O(N^2) double-for-loop, you fail the interview instantly.
# 
# In Coding Interviews, Arrays and Strings are designed to test your mastery of 
# "Linear Time Optimizations". They want to see if you can solve complex array 
# interactions in exactly ONE pass through the data, using O(1) extra space.
#
# To achieve this, you must master the "Big Three" algorithmic patterns:
# 1. Two Pointers (Left/Right convergence)
# 2. Sliding Window (Dynamic expansion/contraction)
# 3. Prefix Sum (O(1) range queries via precomputation)
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master the Two Pointer pattern (e.g., Valid Palindrome, Two Sum Sorted).
# - Master the Sliding Window pattern (e.g., Longest Substring, Min Size Subarray).
# - Master Prefix Sums (e.g., Subarray Sum Equals K).
#
# ==============================================================================
"""

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE TWO POINTER PATTERN (CONVERGENCE)
# ==============================================================================
def two_sum_sorted(numbers: list[int], target: int) -> tuple[int, int]:
    """
    Problem: Find two numbers that add up to the Target. The array is SORTED.
    Brute Force: O(N^2).
    Two Pointers: O(N) Time, O(1) Space.
    """
    # 1. Place a pointer at the extreme Left (smallest number)
    left = 0
    # 2. Place a pointer at the extreme Right (largest number)
    right = len(numbers) - 1
    
    while left < right:
        current_sum = numbers[left] + numbers[right]
        
        if current_sum == target:
            return (numbers[left], numbers[right])
        elif current_sum < target:
            # We are too small! The only way to increase the sum is to 
            # mathematically move the Left pointer to the right (bigger number).
            left += 1
        else:
            # We are too big! We must move the Right pointer to the left.
            right -= 1
            
    return (-1, -1)

def demonstrate_two_pointer():
    section_header("Two Pointers (O(1) Space Convergence)")
    
    arr = [2, 7, 11, 15, 20, 25]
    target = 26
    
    print(f"Array: {arr}")
    print(f"Target Sum: {target}")
    
    result = two_sum_sorted(arr, target)
    print(f"Found Pair: {result}")
    print("Why is this O(N)? Because each pointer only moves in one direction. ")
    print("They converge towards the center and meet exactly once. No nested loops!")


# ==============================================================================
# 4. SLIDING WINDOW PATTERN (DYNAMIC SIZING)
# ==============================================================================
def longest_substring_without_repeats(s: str) -> int:
    """
    Problem: Find the length of the longest substring without repeating characters.
    Brute Force: O(N^3).
    Sliding Window: O(N) Time, O(1) Space (HashMap limited to 26 chars).
    """
    # The "Window" is defined by [left, right]
    left = 0
    max_length = 0
    
    # We use a Set to track characters physically inside our current window
    char_set = set()
    
    # The Right pointer aggressively expands the window
    for right in range(len(s)):
        current_char = s[right]
        
        # INVARIANT VIOLATION!
        # If the character already exists in our window, we MUST shrink the 
        # window from the Left until the duplicate is physically evicted!
        while current_char in char_set:
            char_set.remove(s[left])
            left += 1
            
        # The window is now mathematically valid again. Add the new char!
        char_set.add(current_char)
        
        # Update our record
        window_size = (right - left) + 1
        max_length = max(max_length, window_size)
        
    return max_length

def demonstrate_sliding_window():
    section_header("Sliding Window (Dynamic Constraints)")
    
    s = "abcabcbb"
    print(f"String: '{s}'")
    
    ans = longest_substring_without_repeats(s)
    print(f"Longest Substring Without Repeats: {ans} (Expected 3: 'abc')")
    
    print("\nHow it works:")
    print("1. 'Right' pointer aggressively expands: [a], [a,b], [a,b,c]. Max = 3.")
    print("2. It sees 'a' again! Violation!")
    print("3. 'Left' pointer violently shrinks the window until 'a' is gone.")
    print("4. Result: [b,c,a]. The window organically inches across the array in O(N) time!")


# ==============================================================================
# 5. PREFIX SUM WITH HASHMAP (O(N) MATHEMATICS)
# ==============================================================================
def subarray_sum_equals_k(nums: list[int], k: int) -> int:
    """
    Problem: Count the total number of continuous subarrays whose sum equals K.
    *NOTE*: The array contains NEGATIVE numbers! Sliding Window is mathematically 
    impossible here (because expanding might DECREASE the sum).
    
    Solution: Prefix Sum + Hash Map. O(N) Time, O(N) Space.
    """
    # Maps a Prefix Sum -> The number of times we have seen it!
    # Base case: We have seen a sum of '0' exactly one time (the empty array).
    prefix_counts = {0: 1}
    
    current_sum = 0
    total_subarrays = 0
    
    for num in nums:
        current_sum += num
        
        # ALGEBRA MAGIC:
        # If (current_sum - past_sum = K), then (past_sum = current_sum - K).
        # We simply ask the Hash Map: "Have we ever seen a Prefix Sum equal to 
        # (current_sum - K) anywhere behind us?"
        target = current_sum - k
        
        if target in prefix_counts:
            # Every time we saw that sum, it represents a valid boundary!
            total_subarrays += prefix_counts[target]
            
        # Add our current sum to the history book for future iterations
        prefix_counts[current_sum] = prefix_counts.get(current_sum, 0) + 1
        
    return total_subarrays

def demonstrate_prefix_sum():
    section_header("Prefix Sum + HashMap (Algebraic Ranges)")
    
    arr = [1, -1, 1, 1, 1, -1]
    k = 2
    
    print(f"Array: {arr}")
    print(f"Target Subarray Sum: {k}")
    
    ans = subarray_sum_equals_k(arr, k)
    print(f"Total Subarrays matching {k}: {ans}")
    print("Why? By storing the history of all running totals in an O(1) Hash Map, ")
    print("we use basic algebra (Current - Target = History) to instantly find ")
    print("valid boundaries without writing an O(N^2) nested loop!")


def run_all_labs():
    demonstrate_two_pointer()
    demonstrate_sliding_window()
    demonstrate_prefix_sum()


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why does the Two Pointer pattern guarantee an $O(N)$ runtime?
   Answer: In a brute-force $O(N^2)$ solution, the outer loop moves 1 step, and the inner loop traverses the *entire* array. This causes mathematical duplication of work. In the Two Pointer pattern, the `left` pointer only ever moves to the right. The `right` pointer only ever moves to the left. Once a pointer passes an index, it physically never looks back. The total combined distance traveled by both pointers is strictly equal to the length of the array ($N$). Because they meet exactly in the middle and terminate, the algorithm is mathematically locked to a single $O(N)$ pass.

2. What is the fatal mathematical flaw that prevents you from using a "Sliding Window" on an array containing Negative Numbers?
   Answer: A Sliding Window relies entirely on "Monotonicity" (strictly increasing or decreasing trends). The logic is: "If my sum is too small, I move Right to increase it. If my sum is too big, I move Left to decrease it." This logic is physically broken by negative numbers. If your sum is too small, moving Right might add a `-100`, making the sum even smaller! You lose the ability to deterministically decide which pointer to move. When Monotonicity is destroyed by negative numbers, you MUST abandon Sliding Window and use the algebraic "Prefix Sum + Hash Map" pattern instead.

3. In the Prefix Sum pattern, explain the mathematical formula: `(current_sum - target) in hash_map`.
   Answer: Think of a Prefix Sum as physical distance markers on a highway. You are currently at Mile 50 (`current_sum = 50`). You want to find a section of highway that is exactly 20 miles long (`K = 20`). Basic algebra dictates that this section must have started at Mile 30 (`50 - 20 = 30`). Therefore, you simply ask the Hash Map: "When I was driving earlier, did I ever pass a marker for Mile 30?". If the Hash Map says "Yes, you passed it 2 times", it means there are exactly 2 distinct starting points in the past that create a 20-mile stretch ending exactly at your current location!
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Interview Prep (Arrays & Strings) Completed.")
