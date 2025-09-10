#!/usr/bin/env python3
"""
Competitive Programming - Two Pointers Technique

This module covers the Two Pointers technique, one of the most important
patterns in competitive programming. It's used to solve array and string
problems efficiently with O(n) time complexity instead of O(n²).

Topics covered:
- Basic two pointers (start and end)
- Fast and slow pointers
- Meeting in the middle
- Sliding window variations
- Multiple arrays processing

Author: Python DSA Master
Date: 2024
"""

from typing import List, Optional, Tuple, Set
import sys
from collections import defaultdict


class TwoPointersBasic:
    """
    Basic Two Pointers Techniques
    
    These problems use two pointers moving from opposite ends
    or in the same direction to solve problems efficiently.
    """
    
    @staticmethod
    def two_sum_sorted(arr: List[int], target: int) -> Optional[Tuple[int, int]]:
        """
        Two Sum in Sorted Array
        
        Find two numbers in a sorted array that add up to target.
        
        Time Complexity: O(n)
        Space Complexity: O(1)
        
        Args:
            arr: Sorted array of integers
            target: Target sum
            
        Returns:
            Tuple of indices if found, None otherwise
            
        Example:
            >>> TwoPointersBasic.two_sum_sorted([1, 2, 3, 4, 6], 6)
            (1, 3)  # arr[1] + arr[3] = 2 + 4 = 6
        """
        left, right = 0, len(arr) - 1
        
        while left < right:
            current_sum = arr[left] + arr[right]
            
            if current_sum == target:
                return (left, right)
            elif current_sum < target:
                left += 1
            else:
                right -= 1
        
        return None
    
    @staticmethod
    def three_sum(arr: List[int]) -> List[List[int]]:
        """
        Three Sum Problem
        
        Find all unique triplets that sum to zero.
        
        Time Complexity: O(n²)
        Space Complexity: O(1) excluding result
        
        Args:
            arr: Array of integers
            
        Returns:
            List of triplets that sum to zero
            
        Example:
            >>> TwoPointersBasic.three_sum([-1, 0, 1, 2, -1, -4])
            [[-1, -1, 2], [-1, 0, 1]]
        """
        if len(arr) < 3:
            return []
        
        arr.sort()
        result = []
        n = len(arr)
        
        for i in range(n - 2):
            # Skip duplicates for first number
            if i > 0 and arr[i] == arr[i - 1]:
                continue
            
            left, right = i + 1, n - 1
            
            while left < right:
                current_sum = arr[i] + arr[left] + arr[right]
                
                if current_sum == 0:
                    result.append([arr[i], arr[left], arr[right]])
                    
                    # Skip duplicates for second and third numbers
                    while left < right and arr[left] == arr[left + 1]:
                        left += 1
                    while left < right and arr[right] == arr[right - 1]:
                        right -= 1
                    
                    left += 1
                    right -= 1
                elif current_sum < 0:
                    left += 1
                else:
                    right -= 1
        
        return result
    
    @staticmethod
    def remove_duplicates(arr: List[int]) -> int:
        """
        Remove Duplicates from Sorted Array
        
        Remove duplicates in-place and return new length.
        
        Time Complexity: O(n)
        Space Complexity: O(1)
        
        Args:
            arr: Sorted array with duplicates
            
        Returns:
            New length after removing duplicates
            
        Example:
            >>> arr = [1, 1, 2, 2, 3, 4, 4]
            >>> TwoPointersBasic.remove_duplicates(arr)
            4
            >>> arr[:4]
            [1, 2, 3, 4]
        """
        if not arr:
            return 0
        
        write_ptr = 1
        
        for read_ptr in range(1, len(arr)):
            if arr[read_ptr] != arr[read_ptr - 1]:
                arr[write_ptr] = arr[read_ptr]
                write_ptr += 1
        
        return write_ptr
    
    @staticmethod
    def reverse_words_in_string(s: str) -> str:
        """
        Reverse Words in String
        
        Reverse the order of words in a string using two pointers.
        
        Time Complexity: O(n)
        Space Complexity: O(1) excluding result
        
        Args:
            s: Input string
            
        Returns:
            String with words reversed
            
        Example:
            >>> TwoPointersBasic.reverse_words_in_string("the sky is blue")
            "blue is sky the"
        """
        # Convert to list for in-place operations
        chars = list(s.strip())
        n = len(chars)
        
        if n == 0:
            return ""
        
        # Helper function to reverse a portion of the array
        def reverse_range(start: int, end: int):
            while start < end:
                chars[start], chars[end] = chars[end], chars[start]
                start += 1
                end -= 1
        
        # Reverse the entire string
        reverse_range(0, n - 1)
        
        # Reverse each word
        start = 0
        for i in range(n + 1):
            if i == n or chars[i] == ' ':
                reverse_range(start, i - 1)
                start = i + 1
        
        return ''.join(chars)
    
    @staticmethod
    def container_with_most_water(heights: List[int]) -> int:
        """
        Container With Most Water
        
        Find two lines that form a container with the most water.
        
        Time Complexity: O(n)
        Space Complexity: O(1)
        
        Args:
            heights: Array of heights
            
        Returns:
            Maximum water that can be contained
            
        Example:
            >>> TwoPointersBasic.container_with_most_water([1,8,6,2,5,4,8,3,7])
            49
        """
        if len(heights) < 2:
            return 0
        
        left, right = 0, len(heights) - 1
        max_area = 0
        
        while left < right:
            # Calculate current area
            width = right - left
            height = min(heights[left], heights[right])
            area = width * height
            max_area = max(max_area, area)
            
            # Move the pointer with smaller height
            if heights[left] < heights[right]:
                left += 1
            else:
                right -= 1
        
        return max_area


class FastSlowPointers:
    """
    Fast and Slow Pointers (Floyd's Cycle Detection)
    
    This technique uses two pointers moving at different speeds
    to detect cycles and find middle elements.
    """
    
    class ListNode:
        """Simple linked list node for demonstration."""
        def __init__(self, val: int = 0, next_node=None):
            self.val = val
            self.next = next_node
    
    @staticmethod
    def has_cycle(head: Optional[ListNode]) -> bool:
        """
        Detect Cycle in Linked List
        
        Use fast and slow pointers to detect if a cycle exists.
        
        Time Complexity: O(n)
        Space Complexity: O(1)
        
        Args:
            head: Head of the linked list
            
        Returns:
            True if cycle exists, False otherwise
        """
        if not head or not head.next:
            return False
        
        slow = fast = head
        
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            
            if slow == fast:
                return True
        
        return False
    
    @staticmethod
    def find_cycle_start(head: Optional[ListNode]) -> Optional[ListNode]:
        """
        Find Start of Cycle in Linked List
        
        If a cycle exists, find where it starts.
        
        Time Complexity: O(n)
        Space Complexity: O(1)
        
        Args:
            head: Head of the linked list
            
        Returns:
            Node where cycle starts, None if no cycle
        """
        if not head or not head.next:
            return None
        
        # Phase 1: Detect if cycle exists
        slow = fast = head
        
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            
            if slow == fast:
                break
        else:
            return None  # No cycle found
        
        # Phase 2: Find cycle start
        slow = head
        while slow != fast:
            slow = slow.next
            fast = fast.next
        
        return slow
    
    @staticmethod
    def find_middle_node(head: Optional[ListNode]) -> Optional[ListNode]:
        """
        Find Middle Node of Linked List
        
        Use fast and slow pointers to find the middle node.
        
        Time Complexity: O(n)
        Space Complexity: O(1)
        
        Args:
            head: Head of the linked list
            
        Returns:
            Middle node of the list
        """
        if not head:
            return None
        
        slow = fast = head
        
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        
        return slow
    
    @staticmethod
    def is_palindrome_list(head: Optional[ListNode]) -> bool:
        """
        Check if Linked List is Palindrome
        
        Use fast/slow pointers to find middle, reverse second half, compare.
        
        Time Complexity: O(n)
        Space Complexity: O(1)
        
        Args:
            head: Head of the linked list
            
        Returns:
            True if list is palindrome, False otherwise
        """
        if not head or not head.next:
            return True
        
        # Find middle using fast/slow pointers
        slow = fast = head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        
        # Reverse second half
        def reverse_list(node):
            prev = None
            while node:
                next_node = node.next
                node.next = prev
                prev = node
                node = next_node
            return prev
        
        second_half = reverse_list(slow)
        
        # Compare first and second halves
        first_half = head
        while second_half:
            if first_half.val != second_half.val:
                return False
            first_half = first_half.next
            second_half = second_half.next
        
        return True


class SlidingWindowPatterns:
    """
    Sliding Window Variations with Two Pointers
    
    These problems use two pointers to maintain a window
    and solve substring/subarray problems efficiently.
    """
    
    @staticmethod
    def longest_substring_without_repeating(s: str) -> int:
        """
        Longest Substring Without Repeating Characters
        
        Find length of longest substring without repeating characters.
        
        Time Complexity: O(n)
        Space Complexity: O(min(m, n)) where m is charset size
        
        Args:
            s: Input string
            
        Returns:
            Length of longest substring without repeating characters
            
        Example:
            >>> SlidingWindowPatterns.longest_substring_without_repeating("abcabcbb")
            3  # "abc"
        """
        if not s:
            return 0
        
        char_index = {}
        left = max_length = 0
        
        for right in range(len(s)):
            char = s[right]
            
            # If character is already in current window, move left pointer
            if char in char_index and char_index[char] >= left:
                left = char_index[char] + 1
            
            char_index[char] = right
            max_length = max(max_length, right - left + 1)
        
        return max_length
    
    @staticmethod
    def minimum_window_substring(s: str, t: str) -> str:
        """
        Minimum Window Substring
        
        Find minimum window in s which contains all characters of t.
        
        Time Complexity: O(|s| + |t|)
        Space Complexity: O(|s| + |t|)
        
        Args:
            s: Source string
            t: Target string containing required characters
            
        Returns:
            Minimum window substring
            
        Example:
            >>> SlidingWindowPatterns.minimum_window_substring("ADOBECODEBANC", "ABC")
            "BANC"
        """
        if not s or not t or len(s) < len(t):
            return ""
        
        # Count characters in t
        t_count = defaultdict(int)
        for char in t:
            t_count[char] += 1
        
        required_chars = len(t_count)
        formed_chars = 0
        window_counts = defaultdict(int)
        
        left = right = 0
        min_len = float('inf')
        min_left = 0
        
        while right < len(s):
            # Expand window by including character at right
            char = s[right]
            window_counts[char] += 1
            
            if char in t_count and window_counts[char] == t_count[char]:
                formed_chars += 1
            
            # Contract window from left while it's valid
            while left <= right and formed_chars == required_chars:
                # Update minimum window if current is smaller
                if right - left + 1 < min_len:
                    min_len = right - left + 1
                    min_left = left
                
                # Remove character at left from window
                char = s[left]
                window_counts[char] -= 1
                if char in t_count and window_counts[char] < t_count[char]:
                    formed_chars -= 1
                
                left += 1
            
            right += 1
        
        return "" if min_len == float('inf') else s[min_left:min_left + min_len]
    
    @staticmethod
    def max_consecutive_ones_with_k_flips(nums: List[int], k: int) -> int:
        """
        Max Consecutive Ones III
        
        Find max consecutive 1s after flipping at most k zeros.
        
        Time Complexity: O(n)
        Space Complexity: O(1)
        
        Args:
            nums: Binary array
            k: Maximum number of zeros that can be flipped
            
        Returns:
            Maximum length of consecutive 1s possible
            
        Example:
            >>> SlidingWindowPatterns.max_consecutive_ones_with_k_flips([1,1,1,0,0,0,1,1,1,1,0], 2)
            6
        """
        left = max_length = zeros_count = 0
        
        for right in range(len(nums)):
            # Expand window
            if nums[right] == 0:
                zeros_count += 1
            
            # Contract window if we have too many zeros
            while zeros_count > k:
                if nums[left] == 0:
                    zeros_count -= 1
                left += 1
            
            # Update maximum length
            max_length = max(max_length, right - left + 1)
        
        return max_length
    
    @staticmethod
    def subarray_sum_equals_k(nums: List[int], k: int) -> int:
        """
        Subarray Sum Equals K
        
        Count number of continuous subarrays whose sum equals k.
        
        Time Complexity: O(n)
        Space Complexity: O(n)
        
        Args:
            nums: Array of integers
            k: Target sum
            
        Returns:
            Number of subarrays with sum equal to k
            
        Example:
            >>> SlidingWindowPatterns.subarray_sum_equals_k([1,1,1], 2)
            2
        """
        count = 0
        prefix_sum = 0
        sum_count = defaultdict(int)
        sum_count[0] = 1  # Empty subarray
        
        for num in nums:
            prefix_sum += num
            
            # Check if (prefix_sum - k) exists
            if (prefix_sum - k) in sum_count:
                count += sum_count[prefix_sum - k]
            
            sum_count[prefix_sum] += 1
        
        return count


class MultipleArraysPatterns:
    """
    Two Pointers for Multiple Arrays
    
    These problems involve processing multiple sorted arrays
    using two or more pointers.
    """
    
    @staticmethod
    def merge_sorted_arrays(arr1: List[int], arr2: List[int]) -> List[int]:
        """
        Merge Two Sorted Arrays
        
        Merge two sorted arrays into one sorted array.
        
        Time Complexity: O(n + m)
        Space Complexity: O(n + m)
        
        Args:
            arr1: First sorted array
            arr2: Second sorted array
            
        Returns:
            Merged sorted array
            
        Example:
            >>> MultipleArraysPatterns.merge_sorted_arrays([1,2,3], [2,5,6])
            [1, 2, 2, 3, 5, 6]
        """
        result = []
        i = j = 0
        
        while i < len(arr1) and j < len(arr2):
            if arr1[i] <= arr2[j]:
                result.append(arr1[i])
                i += 1
            else:
                result.append(arr2[j])
                j += 1
        
        # Add remaining elements
        result.extend(arr1[i:])
        result.extend(arr2[j:])
        
        return result
    
    @staticmethod
    def intersection_of_sorted_arrays(arr1: List[int], arr2: List[int]) -> List[int]:
        """
        Intersection of Two Sorted Arrays
        
        Find intersection of two sorted arrays.
        
        Time Complexity: O(n + m)
        Space Complexity: O(min(n, m))
        
        Args:
            arr1: First sorted array
            arr2: Second sorted array
            
        Returns:
            Array containing intersection elements
            
        Example:
            >>> MultipleArraysPatterns.intersection_of_sorted_arrays([1,2,2,1], [2,2])
            [2, 2]
        """
        result = []
        i = j = 0
        
        while i < len(arr1) and j < len(arr2):
            if arr1[i] == arr2[j]:
                result.append(arr1[i])
                i += 1
                j += 1
            elif arr1[i] < arr2[j]:
                i += 1
            else:
                j += 1
        
        return result
    
    @staticmethod
    def find_median_sorted_arrays(nums1: List[int], nums2: List[int]) -> float:
        """
        Median of Two Sorted Arrays
        
        Find median of two sorted arrays in O(log(min(m,n))) time.
        
        Time Complexity: O(log(min(m, n)))
        Space Complexity: O(1)
        
        Args:
            nums1: First sorted array
            nums2: Second sorted array
            
        Returns:
            Median of combined sorted arrays
            
        Example:
            >>> MultipleArraysPatterns.find_median_sorted_arrays([1,3], [2])
            2.0
        """
        # Ensure nums1 is the smaller array
        if len(nums1) > len(nums2):
            nums1, nums2 = nums2, nums1
        
        m, n = len(nums1), len(nums2)
        total = m + n
        half = total // 2
        
        left, right = 0, m
        
        while True:
            # Partition nums1
            i = (left + right) // 2
            # Partition nums2
            j = half - i
            
            # Get boundary values
            nums1_left = float('-inf') if i == 0 else nums1[i - 1]
            nums1_right = float('inf') if i == m else nums1[i]
            nums2_left = float('-inf') if j == 0 else nums2[j - 1]
            nums2_right = float('inf') if j == n else nums2[j]
            
            # Check if partition is correct
            if nums1_left <= nums2_right and nums2_left <= nums1_right:
                # Even total length
                if total % 2 == 0:
                    return (max(nums1_left, nums2_left) + min(nums1_right, nums2_right)) / 2
                # Odd total length
                else:
                    return min(nums1_right, nums2_right)
            elif nums1_left > nums2_right:
                right = i - 1
            else:
                left = i + 1


def solve_competitive_problems():
    """Demonstrate solutions to common competitive programming problems."""
    print("Competitive Programming - Two Pointers Solutions")
    print("=" * 55)
    
    # Problem 1: Two Sum in Sorted Array
    print("\n1. Two Sum in Sorted Array")
    arr = [1, 2, 3, 4, 6]
    target = 6
    result = TwoPointersBasic.two_sum_sorted(arr, target)
    print(f"Array: {arr}, Target: {target}")
    print(f"Indices: {result}, Values: {arr[result[0]] if result else 'Not found'} + {arr[result[1]] if result else ''}")
    
    # Problem 2: Three Sum
    print("\n2. Three Sum")
    arr = [-1, 0, 1, 2, -1, -4]
    result = TwoPointersBasic.three_sum(arr)
    print(f"Array: {arr}")
    print(f"Triplets summing to 0: {result}")
    
    # Problem 3: Container With Most Water
    print("\n3. Container With Most Water")
    heights = [1, 8, 6, 2, 5, 4, 8, 3, 7]
    result = TwoPointersBasic.container_with_most_water(heights)
    print(f"Heights: {heights}")
    print(f"Max water: {result}")
    
    # Problem 4: Longest Substring Without Repeating
    print("\n4. Longest Substring Without Repeating Characters")
    s = "abcabcbb"
    result = SlidingWindowPatterns.longest_substring_without_repeating(s)
    print(f"String: '{s}'")
    print(f"Longest substring length: {result}")
    
    # Problem 5: Minimum Window Substring
    print("\n5. Minimum Window Substring")
    s = "ADOBECODEBANC"
    t = "ABC"
    result = SlidingWindowPatterns.minimum_window_substring(s, t)
    print(f"String: '{s}', Pattern: '{t}'")
    print(f"Minimum window: '{result}'")
    
    # Problem 6: Max Consecutive Ones III
    print("\n6. Max Consecutive Ones III")
    nums = [1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0]
    k = 2
    result = SlidingWindowPatterns.max_consecutive_ones_with_k_flips(nums, k)
    print(f"Array: {nums}, K: {k}")
    print(f"Max consecutive 1s: {result}")
    
    # Problem 7: Merge Sorted Arrays
    print("\n7. Merge Sorted Arrays")
    arr1 = [1, 2, 3]
    arr2 = [2, 5, 6]
    result = MultipleArraysPatterns.merge_sorted_arrays(arr1, arr2)
    print(f"Array 1: {arr1}, Array 2: {arr2}")
    print(f"Merged: {result}")
    
    # Problem 8: Median of Two Sorted Arrays
    print("\n8. Median of Two Sorted Arrays")
    nums1 = [1, 3]
    nums2 = [2]
    result = MultipleArraysPatterns.find_median_sorted_arrays(nums1, nums2)
    print(f"Array 1: {nums1}, Array 2: {nums2}")
    print(f"Median: {result}")


def competitive_programming_tips():
    """Provide tips for competitive programming with two pointers."""
    print("\nCompetitive Programming Tips - Two Pointers")
    print("=" * 45)
    
    print("\n🎯 When to Use Two Pointers:")
    print("• Array/string problems with sorted data")
    print("• Finding pairs/triplets with specific sum")
    print("• Removing duplicates or elements")
    print("• Sliding window problems")
    print("• Cycle detection in linked lists")
    print("• Palindrome checking")
    
    print("\n⚡ Time Complexity Benefits:")
    print("• Reduces O(n²) brute force to O(n)")
    print("• Often achieves O(1) space complexity")
    print("• Very cache-friendly due to sequential access")
    
    print("\n🔧 Implementation Tips:")
    print("• Always check boundary conditions")
    print("• Handle duplicate elements carefully")
    print("• Consider edge cases (empty arrays, single element)")
    print("• Use while loops with proper termination conditions")
    print("• For sliding window, expand right first, then contract left")
    
    print("\n📚 Common Variations:")
    print("• Start-end pointers (opposite directions)")
    print("• Fast-slow pointers (same direction, different speeds)")
    print("• Multiple arrays (one pointer per array)")
    print("• Sliding window (dynamic window size)")
    print("• Fixed window size problems")
    
    print("\n🏆 Contest Strategy:")
    print("• Two pointers problems are often 800-1400 rating on Codeforces")
    print("• Usually appear in Div2 A, B, or C problems")
    print("• Can be combined with other techniques (binary search, etc.)")
    print("• Practice pattern recognition for quick identification")


def main():
    """Main function to demonstrate two pointers techniques."""
    print("Python DSA Master - Two Pointers Technique")
    print("=" * 50)
    
    try:
        solve_competitive_problems()
        competitive_programming_tips()
        
    except KeyboardInterrupt:
        print("\nDemo interrupted by user")
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()
    
    print(f"\n{'='*50}")
    print("Two Pointers demonstration complete!")


if __name__ == "__main__":
    main()


# ============================================================================
# PRACTICE PROBLEMS FOR COMPETITIVE PROGRAMMING
# ============================================================================

"""
PRACTICE PROBLEMS BY DIFFICULTY:

🟢 EASY (Codeforces 800-1000):
1. Remove Element (LeetCode 27)
2. Move Zeroes (LeetCode 283)
3. Reverse String (LeetCode 344)
4. Valid Palindrome (LeetCode 125)
5. Intersection of Two Arrays (LeetCode 349)

🟡 MEDIUM (Codeforces 1000-1400):
6. 3Sum (LeetCode 15)
7. Container With Most Water (LeetCode 11)
8. Longest Substring Without Repeating Characters (LeetCode 3)
9. Minimum Window Substring (LeetCode 76)
10. Sort Colors (LeetCode 75)

🔴 HARD (Codeforces 1400+):
11. Trapping Rain Water (LeetCode 42)
12. Median of Two Sorted Arrays (LeetCode 4)
13. Minimum Window Substring (LeetCode 76)
14. Sliding Window Maximum (LeetCode 239)
15. Longest Duplicate Substring (LeetCode 1044)

📝 PLATFORM-SPECIFIC PROBLEMS:
• Codeforces: Search "two pointers" tag
• AtCoder: Beginner Contest problems often feature two pointers
• LeetCode: Filter by "Two Pointers" tag
• HackerRank: Array and string manipulation problems
• CodeChef: EASY to MEDIUM difficulty array problems

🎯 CONTEST PREPARATION:
• Solve 5-10 problems of each difficulty level
• Time yourself: aim for 10-15 minutes per easy problem
• Focus on clean, bug-free implementation
• Practice edge case handling
• Learn to recognize the pattern quickly
"""
