#!/usr/bin/env python3
"""
Technical Interview Preparation - Arrays and Strings

This module contains comprehensive solutions and explanations for the most
frequently asked array and string problems in technical interviews at major
tech companies (Google, Facebook, Amazon, Microsoft, Apple, etc.).

Each problem includes:
- Multiple solution approaches (brute force, optimized)
- Time and space complexity analysis  
- Edge cases and test cases
- Interview tips and follow-up questions
- Company-specific insights

Author: Python DSA Master
Date: 2024
"""

from typing import List, Optional, Dict, Set, Tuple
from collections import defaultdict, Counter
import bisect


class ArrayInterviewProblems:
    """
    Essential Array Problems for Technical Interviews
    
    These problems are commonly asked across all major tech companies
    and cover fundamental array manipulation techniques.
    """
    
    @staticmethod
    def two_sum(nums: List[int], target: int) -> List[int]:
        """
        🔥 MOST ASKED: Two Sum (Easy)
        
        Companies: Google, Amazon, Facebook, Microsoft, Apple, Uber, LinkedIn
        
        Given an array and target, return indices of two numbers that add up to target.
        
        Time Complexity: O(n)
        Space Complexity: O(n)
        
        Args:
            nums: List of integers
            target: Target sum
            
        Returns:
            List of two indices
            
        Example:
            >>> ArrayInterviewProblems.two_sum([2,7,11,15], 9)
            [0, 1]
            
        Interview Notes:
        - Always ask: Are there duplicate values?
        - Ask: Can I assume exactly one solution exists?
        - Follow-up: What if the array is sorted? (Two pointers approach)
        """
        num_to_index = {}
        
        for i, num in enumerate(nums):
            complement = target - num
            
            if complement in num_to_index:
                return [num_to_index[complement], i]
            
            num_to_index[num] = i
        
        return []  # No solution found
    
    @staticmethod
    def three_sum(nums: List[int]) -> List[List[int]]:
        """
        🔥 VERY COMMON: 3Sum (Medium)
        
        Companies: Facebook, Amazon, Microsoft, Google
        
        Find all unique triplets that sum to zero.
        
        Time Complexity: O(n²)
        Space Complexity: O(1) excluding result
        
        Args:
            nums: List of integers
            
        Returns:
            List of unique triplets
            
        Interview Notes:
        - Key insight: Fix one element, use two pointers for the rest
        - Critical: Handle duplicates correctly
        - Follow-up: 3Sum closest, 4Sum
        """
        if len(nums) < 3:
            return []
        
        nums.sort()
        result = []
        
        for i in range(len(nums) - 2):
            # Skip duplicates for first element
            if i > 0 and nums[i] == nums[i - 1]:
                continue
            
            left, right = i + 1, len(nums) - 1
            
            while left < right:
                current_sum = nums[i] + nums[left] + nums[right]
                
                if current_sum == 0:
                    result.append([nums[i], nums[left], nums[right]])
                    
                    # Skip duplicates
                    while left < right and nums[left] == nums[left + 1]:
                        left += 1
                    while left < right and nums[right] == nums[right - 1]:
                        right -= 1
                    
                    left += 1
                    right -= 1
                elif current_sum < 0:
                    left += 1
                else:
                    right -= 1
        
        return result
    
    @staticmethod
    def max_subarray(nums: List[int]) -> int:
        """
        🔥 CLASSIC: Maximum Subarray (Kadane's Algorithm) - Easy/Medium
        
        Companies: Amazon, Microsoft, Google, LinkedIn
        
        Find contiguous subarray with maximum sum.
        
        Time Complexity: O(n)
        Space Complexity: O(1)
        
        Args:
            nums: List of integers
            
        Returns:
            Maximum sum of contiguous subarray
            
        Interview Notes:
        - Classic DP problem, but greedy solution exists
        - Ask: Do you want just the sum or the actual subarray?
        - Follow-up: Maximum product subarray, circular array version
        """
        if not nums:
            return 0
        
        max_so_far = max_ending_here = nums[0]
        
        for i in range(1, len(nums)):
            # Either extend existing subarray or start new one
            max_ending_here = max(nums[i], max_ending_here + nums[i])
            max_so_far = max(max_so_far, max_ending_here)
        
        return max_so_far
    
    @staticmethod
    def rotate_array(nums: List[int], k: int) -> None:
        """
        🔥 COMMON: Rotate Array - Easy
        
        Companies: Microsoft, Amazon, Google
        
        Rotate array to the right by k steps in-place.
        
        Time Complexity: O(n)
        Space Complexity: O(1)
        
        Args:
            nums: List to rotate (modified in-place)
            k: Number of steps to rotate right
            
        Interview Notes:
        - Multiple approaches: extra array, cyclic replacements, reversing
        - Ask about constraints: Can I use extra space?
        - Edge case: k > len(nums)
        """
        if not nums or k == 0:
            return
        
        n = len(nums)
        k = k % n  # Handle k > n
        
        # Reverse entire array
        def reverse(start, end):
            while start < end:
                nums[start], nums[end] = nums[end], nums[start]
                start += 1
                end -= 1
        
        # Three reversals: entire array, first k, remaining
        reverse(0, n - 1)
        reverse(0, k - 1)
        reverse(k, n - 1)
    
    @staticmethod
    def product_except_self(nums: List[int]) -> List[int]:
        """
        🔥 POPULAR: Product of Array Except Self - Medium
        
        Companies: Amazon, Facebook, Google, Microsoft
        
        Return array where output[i] equals product of all elements except nums[i].
        Cannot use division and must be O(n) time.
        
        Time Complexity: O(n)
        Space Complexity: O(1) excluding output array
        
        Args:
            nums: Input array
            
        Returns:
            Array of products
            
        Interview Notes:
        - Key insight: Left products × Right products
        - Constraint: Cannot use division
        - Follow-up: What if zeros are allowed?
        """
        n = len(nums)
        result = [1] * n
        
        # Left pass: result[i] contains product of all elements to left of i
        for i in range(1, n):
            result[i] = result[i - 1] * nums[i - 1]
        
        # Right pass: multiply by product of all elements to right of i
        right_product = 1
        for i in range(n - 1, -1, -1):
            result[i] *= right_product
            right_product *= nums[i]
        
        return result
    
    @staticmethod
    def container_with_most_water(height: List[int]) -> int:
        """
        🔥 FREQUENT: Container With Most Water - Medium
        
        Companies: Amazon, Facebook, Google, Microsoft
        
        Find two lines that form container holding the most water.
        
        Time Complexity: O(n)
        Space Complexity: O(1)
        
        Args:
            height: Array of heights
            
        Returns:
            Maximum water area
            
        Interview Notes:
        - Two pointers technique
        - Key insight: Move pointer with smaller height
        - Common mistake: Moving both pointers
        """
        if len(height) < 2:
            return 0
        
        left, right = 0, len(height) - 1
        max_area = 0
        
        while left < right:
            # Calculate current area
            width = right - left
            current_height = min(height[left], height[right])
            area = width * current_height
            max_area = max(max_area, area)
            
            # Move pointer with smaller height
            if height[left] < height[right]:
                left += 1
            else:
                right -= 1
        
        return max_area
    
    @staticmethod
    def merge_intervals(intervals: List[List[int]]) -> List[List[int]]:
        """
        🔥 VERY COMMON: Merge Intervals - Medium
        
        Companies: Facebook, Google, Amazon, Microsoft, LinkedIn, Uber
        
        Merge overlapping intervals.
        
        Time Complexity: O(n log n)
        Space Complexity: O(n)
        
        Args:
            intervals: List of intervals [start, end]
            
        Returns:
            Merged intervals
            
        Interview Notes:
        - Always sort first by start time
        - Check overlap condition carefully
        - Follow-up: Insert interval, meeting rooms
        """
        if not intervals:
            return []
        
        # Sort by start time
        intervals.sort(key=lambda x: x[0])
        merged = [intervals[0]]
        
        for current in intervals[1:]:
            last_merged = merged[-1]
            
            # Check if current overlaps with last merged
            if current[0] <= last_merged[1]:
                # Merge intervals
                last_merged[1] = max(last_merged[1], current[1])
            else:
                # No overlap, add current interval
                merged.append(current)
        
        return merged


class StringInterviewProblems:
    """
    Essential String Problems for Technical Interviews
    
    String manipulation problems are extremely common in interviews
    and test algorithmic thinking and implementation skills.
    """
    
    @staticmethod
    def longest_substring_without_repeating(s: str) -> int:
        """
        🔥 VERY POPULAR: Longest Substring Without Repeating Characters - Medium
        
        Companies: Amazon, Facebook, Google, Microsoft, Apple
        
        Find length of longest substring without repeating characters.
        
        Time Complexity: O(n)
        Space Complexity: O(min(m, n)) where m is charset size
        
        Args:
            s: Input string
            
        Returns:
            Length of longest substring
            
        Interview Notes:
        - Sliding window technique
        - Use hashmap to track character positions
        - Handle duplicates correctly
        """
        if not s:
            return 0
        
        char_index = {}
        left = max_length = 0
        
        for right in range(len(s)):
            char = s[right]
            
            # If char is in current window, move left pointer
            if char in char_index and char_index[char] >= left:
                left = char_index[char] + 1
            
            char_index[char] = right
            max_length = max(max_length, right - left + 1)
        
        return max_length
    
    @staticmethod
    def group_anagrams(strs: List[str]) -> List[List[str]]:
        """
        🔥 COMMON: Group Anagrams - Medium
        
        Companies: Amazon, Facebook, Uber, Airbnb
        
        Group strings that are anagrams of each other.
        
        Time Complexity: O(n * k log k) where k is max string length
        Space Complexity: O(n * k)
        
        Args:
            strs: List of strings
            
        Returns:
            Grouped anagrams
            
        Interview Notes:
        - Key insight: Anagrams have same sorted characters
        - Alternative: Use character count as key
        - Consider unicode characters
        """
        if not strs:
            return []
        
        anagram_groups = defaultdict(list)
        
        for s in strs:
            # Use sorted string as key
            key = ''.join(sorted(s))
            anagram_groups[key].append(s)
        
        return list(anagram_groups.values())
    
    @staticmethod
    def valid_palindrome(s: str) -> bool:
        """
        🔥 FREQUENT: Valid Palindrome - Easy
        
        Companies: Amazon, Microsoft, Facebook
        
        Check if string is palindrome considering only alphanumeric characters.
        
        Time Complexity: O(n)
        Space Complexity: O(1)
        
        Args:
            s: Input string
            
        Returns:
            True if valid palindrome
            
        Interview Notes:
        - Two pointers from ends
        - Handle non-alphanumeric characters
        - Case insensitive comparison
        """
        left, right = 0, len(s) - 1
        
        while left < right:
            # Skip non-alphanumeric from left
            while left < right and not s[left].isalnum():
                left += 1
            
            # Skip non-alphanumeric from right
            while left < right and not s[right].isalnum():
                right -= 1
            
            # Compare characters (case insensitive)
            if s[left].lower() != s[right].lower():
                return False
            
            left += 1
            right -= 1
        
        return True
    
    @staticmethod
    def longest_palindromic_substring(s: str) -> str:
        """
        🔥 POPULAR: Longest Palindromic Substring - Medium
        
        Companies: Amazon, Microsoft, Facebook, Google
        
        Find the longest palindromic substring.
        
        Time Complexity: O(n²)
        Space Complexity: O(1)
        
        Args:
            s: Input string
            
        Returns:
            Longest palindromic substring
            
        Interview Notes:
        - Expand around centers approach
        - Consider both odd and even length palindromes
        - Alternative: Dynamic programming O(n²) space
        """
        if not s:
            return ""
        
        start = max_len = 0
        
        def expand_around_center(left: int, right: int) -> int:
            while left >= 0 and right < len(s) and s[left] == s[right]:
                left -= 1
                right += 1
            return right - left - 1
        
        for i in range(len(s)):
            # Check for odd length palindromes (center at i)
            len1 = expand_around_center(i, i)
            
            # Check for even length palindromes (center between i and i+1)
            len2 = expand_around_center(i, i + 1)
            
            # Update longest palindrome if found
            current_max = max(len1, len2)
            if current_max > max_len:
                max_len = current_max
                start = i - (current_max - 1) // 2
        
        return s[start:start + max_len]
    
    @staticmethod
    def minimum_window_substring(s: str, t: str) -> str:
        """
        🔥 HARD BUT POPULAR: Minimum Window Substring - Hard
        
        Companies: Facebook, Google, Uber, Snapchat
        
        Find minimum window in s containing all characters of t.
        
        Time Complexity: O(|s| + |t|)
        Space Complexity: O(|s| + |t|)
        
        Args:
            s: Source string
            t: Target string
            
        Returns:
            Minimum window substring
            
        Interview Notes:
        - Sliding window with character counts
        - Expand right, contract left
        - Track when window is valid
        """
        if not s or not t:
            return ""
        
        # Count characters in t
        t_count = Counter(t)
        required_chars = len(t_count)
        formed_chars = 0
        
        # Sliding window
        window_counts = defaultdict(int)
        left = right = 0
        min_len = float('inf')
        min_left = 0
        
        while right < len(s):
            # Expand window
            char = s[right]
            window_counts[char] += 1
            
            if char in t_count and window_counts[char] == t_count[char]:
                formed_chars += 1
            
            # Contract window
            while left <= right and formed_chars == required_chars:
                # Update minimum window
                if right - left + 1 < min_len:
                    min_len = right - left + 1
                    min_left = left
                
                # Remove from window
                char = s[left]
                window_counts[char] -= 1
                if char in t_count and window_counts[char] < t_count[char]:
                    formed_chars -= 1
                
                left += 1
            
            right += 1
        
        return "" if min_len == float('inf') else s[min_left:min_left + min_len]


class InterviewStrategies:
    """
    Interview strategies and tips for array and string problems.
    """
    
    @staticmethod
    def problem_solving_framework():
        """
        Step-by-step framework for tackling interview problems.
        """
        print("🎯 PROBLEM SOLVING FRAMEWORK")
        print("=" * 40)
        
        steps = [
            "1. UNDERSTAND THE PROBLEM",
            "   • Ask clarifying questions",
            "   • Identify inputs, outputs, constraints",
            "   • Work through examples manually",
            "",
            "2. THINK OUT LOUD",
            "   • Share your thought process",
            "   • Discuss trade-offs",
            "   • Consider edge cases",
            "",
            "3. START WITH BRUTE FORCE",
            "   • Get a working solution first",
            "   • Analyze time/space complexity",
            "   • Then optimize if needed",
            "",
            "4. OPTIMIZE SYSTEMATICALLY",
            "   • Look for patterns and techniques",
            "   • Consider data structures and algorithms",
            "   • Think about preprocessing",
            "",
            "5. CODE CLEANLY",
            "   • Use meaningful variable names",
            "   • Handle edge cases",
            "   • Write modular code",
            "",
            "6. TEST THOROUGHLY",
            "   • Walk through your code",
            "   • Test with examples",
            "   • Consider edge cases"
        ]
        
        for step in steps:
            print(step)
    
    @staticmethod
    def common_patterns():
        """
        Common patterns and techniques for arrays and strings.
        """
        print("\n🔧 COMMON PATTERNS & TECHNIQUES")
        print("=" * 40)
        
        patterns = [
            "📍 Two Pointers",
            "   • Opposite ends: palindromes, two sum in sorted array",
            "   • Same direction: remove duplicates, fast-slow",
            "",
            "📍 Sliding Window",
            "   • Fixed size: max sum of k elements",
            "   • Variable size: longest substring without repeating",
            "",
            "📍 Hash Maps",
            "   • Count occurrences: anagrams, character frequency",
            "   • Store indices: two sum, longest substring",
            "",
            "📍 Prefix/Suffix Arrays",
            "   • Running sums: subarray sum, product except self",
            "   • Max/min so far: maximum subarray",
            "",
            "📍 Sorting",
            "   • Enable two pointers: three sum",
            "   • Group similar items: merge intervals",
            "",
            "📍 Stack",
            "   • Matching pairs: valid parentheses",
            "   • Nearest elements: next greater element"
        ]
        
        for pattern in patterns:
            print(pattern)
    
    @staticmethod
    def time_management_tips():
        """
        Tips for managing time during coding interviews.
        """
        print("\n⏰ TIME MANAGEMENT TIPS")
        print("=" * 30)
        
        tips = [
            "📋 TYPICAL 45-MINUTE INTERVIEW BREAKDOWN:",
            "   • 5 min: Problem understanding & clarification",
            "   • 10 min: Discuss approaches and trade-offs",
            "   • 20 min: Code implementation",
            "   • 5 min: Testing and debugging",
            "   • 5 min: Follow-up questions",
            "",
            "🎯 PRIORITY ORDER:",
            "   1. Get working solution (even if not optimal)",
            "   2. Handle basic edge cases",
            "   3. Optimize if time permits",
            "   4. Discuss further optimizations",
            "",
            "🚨 RED FLAGS TO AVOID:",
            "   • Jumping to code without discussion",
            "   • Silent coding for long periods",
            "   • Ignoring interviewer hints",
            "   • Not testing your solution"
        ]
        
        for tip in tips:
            print(tip)


def demonstrate_interview_problems():
    """Demonstrate solutions to common interview problems."""
    print("Technical Interview Preparation - Arrays and Strings")
    print("=" * 60)
    
    # Array problems
    print("\n🔥 ARRAY PROBLEMS")
    print("-" * 20)
    
    # Two Sum
    print("\n1. Two Sum")
    result = ArrayInterviewProblems.two_sum([2, 7, 11, 15], 9)
    print(f"Input: [2,7,11,15], target=9 → Output: {result}")
    
    # Three Sum
    print("\n2. Three Sum")
    result = ArrayInterviewProblems.three_sum([-1, 0, 1, 2, -1, -4])
    print(f"Input: [-1,0,1,2,-1,-4] → Output: {result}")
    
    # Maximum Subarray
    print("\n3. Maximum Subarray (Kadane's Algorithm)")
    result = ArrayInterviewProblems.max_subarray([-2, 1, -3, 4, -1, 2, 1, -5, 4])
    print(f"Input: [-2,1,-3,4,-1,2,1,-5,4] → Max sum: {result}")
    
    # Product Except Self
    print("\n4. Product of Array Except Self")
    result = ArrayInterviewProblems.product_except_self([1, 2, 3, 4])
    print(f"Input: [1,2,3,4] → Output: {result}")
    
    # Container With Most Water
    print("\n5. Container With Most Water")
    result = ArrayInterviewProblems.container_with_most_water([1, 8, 6, 2, 5, 4, 8, 3, 7])
    print(f"Input: [1,8,6,2,5,4,8,3,7] → Max area: {result}")
    
    # String problems
    print("\n\n🔥 STRING PROBLEMS")
    print("-" * 20)
    
    # Longest Substring Without Repeating
    print("\n1. Longest Substring Without Repeating Characters")
    result = StringInterviewProblems.longest_substring_without_repeating("abcabcbb")
    print(f"Input: 'abcabcbb' → Length: {result}")
    
    # Group Anagrams
    print("\n2. Group Anagrams")
    result = StringInterviewProblems.group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"])
    print(f"Input: ['eat','tea','tan','ate','nat','bat']")
    print(f"Output: {result}")
    
    # Valid Palindrome
    print("\n3. Valid Palindrome")
    result = StringInterviewProblems.valid_palindrome("A man, a plan, a canal: Panama")
    print(f"Input: 'A man, a plan, a canal: Panama' → Is palindrome: {result}")
    
    # Longest Palindromic Substring
    print("\n4. Longest Palindromic Substring")
    result = StringInterviewProblems.longest_palindromic_substring("babad")
    print(f"Input: 'babad' → Longest palindrome: '{result}'")


def main():
    """Main function for interview preparation demonstration."""
    print("Python DSA Master - Interview Preparation")
    print("=" * 50)
    
    try:
        demonstrate_interview_problems()
        print("\n")
        
        strategies = InterviewStrategies()
        strategies.problem_solving_framework()
        strategies.common_patterns()
        strategies.time_management_tips()
        
    except KeyboardInterrupt:
        print("\nDemo interrupted by user")
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()
    
    print(f"\n{'='*50}")
    print("Interview preparation demonstration complete!")


if __name__ == "__main__":
    main()


# ============================================================================
# COMPANY-SPECIFIC INTERVIEW INSIGHTS
# ============================================================================

"""
🏢 COMPANY-SPECIFIC INSIGHTS:

🔵 GOOGLE:
• Focus on algorithmic thinking and optimization
• Expect follow-up questions and variations
• Common topics: Arrays, strings, trees, graphs
• Style: Clean code, handle edge cases

🔵 FACEBOOK/META:
• Heavy emphasis on system design for senior roles
• Behavioral questions are crucial
• Common topics: Hash tables, BFS/DFS, dynamic programming
• Style: Discuss trade-offs explicitly

🔵 AMAZON:
• Leadership principles assessment
• Focus on customer obsession in problem-solving
• Common topics: Trees, graphs, string manipulation
• Style: Bias for action - get working solution quickly

🔵 MICROSOFT:
• Collaborative approach appreciated
• Mix of coding and system design
• Common topics: Linked lists, trees, recursion
• Style: Think out loud, explain reasoning

🔵 APPLE:
• Attention to detail and code quality
• Focus on user experience in solutions
• Common topics: Arrays, strings, bit manipulation
• Style: Elegant, efficient solutions

🎯 PREPARATION TIMELINE (8-12 WEEKS):

Week 1-2: Arrays and Strings (Easy problems)
Week 3-4: Linked Lists and Trees (Medium problems)
Week 5-6: Dynamic Programming and Graphs
Week 7-8: System Design and Advanced Topics
Week 9-10: Company-specific practice
Week 11-12: Mock interviews and final prep

📚 RECOMMENDED PRACTICE PROBLEMS:

MUST-DO (Top 25):
1. Two Sum                    14. Merge Intervals
2. Add Two Numbers           15. Insert Interval  
3. Longest Substring         16. Spiral Matrix
4. Median of Two Arrays      17. Jump Game
5. Longest Palindrome        18. Unique Paths
6. ZigZag Conversion         19. Minimum Path Sum
7. Reverse Integer           20. Climbing Stairs
8. String to Integer         21. Edit Distance
9. Palindrome Number         22. Decode Ways
10. Container Most Water     23. Word Break
11. 3Sum                     24. Maximum Subarray
12. Letter Combinations      25. Best Time to Buy/Sell
13. Remove Nth Node

COMPANY FAVORITES:
• Google: Binary search variations, graph algorithms
• Facebook: BFS/DFS, dynamic programming  
• Amazon: Tree traversals, string matching
• Microsoft: Recursion, backtracking
• Apple: Bit manipulation, mathematical problems
"""
