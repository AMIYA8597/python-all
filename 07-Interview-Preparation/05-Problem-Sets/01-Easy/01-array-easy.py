"""
# ==============================================================================
# LABORATORY: INTERVIEW PREPARATION (PROBLEM SETS - ARRAY EASY)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# "Easy" Array problems are often used as the first 10 minutes of a phone screen.
# They test your baseline competence with Hash Maps, Arrays, and fundamental 
# loop structures. If you struggle here or provide an O(N^2) solution, the 
# interview is immediately terminated.
#
# A junior engineer solves 'Two Sum' using nested for-loops (O(N^2) Time).
# 
# A senior engineer solves 'Two Sum' in a single pass using a Hash Map (O(N) 
# Time, O(N) Space), mathematically calculating the exact complement needed 
# and instantly checking if it has been seen before.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master the Single-Pass Hash Map paradigm (Two Sum).
# - Master Hash Sets for instant O(1) membership checks (Contains Duplicate).
# - Understand character frequency mapping (Valid Anagram).
#
# ==============================================================================
"""

import collections
from typing import List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. TWO SUM (THE HASH MAP COMPLEMENT)
# ==============================================================================
def two_sum(nums: List[int], target: int) -> List[int]:
    """
    Time: O(N) | Space: O(N)
    Given an array of integers and an integer target, return indices of the two 
    numbers such that they add up to target.
    """
    # Maps a Value to its specific Array Index!
    seen = {}
    
    print(f"  Target: {target} | Array: {nums}")
    
    for current_index, current_value in enumerate(nums):
        # The mathematical complement! What number do we explicitly need?
        complement = target - current_value
        print(f"    -> Index {current_index} (Val: {current_value}): Mathematically needs a {complement}")
        
        # O(1) instant lookup! Have we seen this complement in the past?
        if complement in seen:
            complement_index = seen[complement]
            print(f"      [SUCCESS] Found {complement} at Index {complement_index}!")
            return [complement_index, current_index]
            
        # We didn't find the complement. Record our current value in the Hash Map 
        # so future numbers can potentially use it!
        seen[current_value] = current_index
        print(f"      [MISS] Added {current_value} (Index {current_index}) to Hash Map.")
        
    return []

def demonstrate_two_sum():
    section_header("Easy: Two Sum (O(N) Hash Map)")
    
    nums = [2, 7, 11, 15]
    target = 9
    ans = two_sum(nums, target)
    print(f"\nResult: {ans} (Expected: [0, 1])")


# ==============================================================================
# 4. CONTAINS DUPLICATE (THE HASH SET)
# ==============================================================================
def contains_duplicate(nums: List[int]) -> bool:
    """
    Time: O(N) | Space: O(N)
    Given an integer array nums, return true if any value appears at least twice.
    """
    # A Hash Set is identical to a Hash Map, but without Values! 
    # It strictly stores Keys, providing perfectly optimized O(1) membership checks.
    seen = set()
    
    print(f"  Checking array for duplicates: {nums}")
    
    for num in nums:
        # O(1) Check
        if num in seen:
            print(f"    -> [COLLISION] Duplicate {num} detected!")
            return True
            
        # O(1) Insertion
        seen.add(num)
        
    print("    -> No duplicates found. Array is completely unique.")
    return False

def demonstrate_contains_duplicate():
    section_header("Easy: Contains Duplicate (O(N) Hash Set)")
    
    nums = [1, 2, 3, 1]
    ans = contains_duplicate(nums)
    print(f"\nResult: {ans} (Expected: True)")


# ==============================================================================
# 5. VALID ANAGRAM (FREQUENCY MAPPING)
# ==============================================================================
def is_anagram(s: str, t: str) -> bool:
    """
    Time: O(N) | Space: O(1) 
    (Space is O(1) because the English alphabet strictly has 26 lowercase letters, 
    so the Hash Map will never exceed 26 keys regardless of string length).
    """
    # If the lengths are different, they mathematically CANNOT be anagrams!
    if len(s) != len(t):
        return False
        
    # We could use `collections.Counter(s) == collections.Counter(t)`, but manual 
    # mapping is often preferred in interviews to demonstrate low-level logic!
    counts = {}
    
    print(f"  String 1: '{s}' | String 2: '{t}'")
    
    # We increment counts for String 's', and instantly decrement for String 't'!
    for i in range(len(s)):
        char_s = s[i]
        char_t = t[i]
        
        counts[char_s] = counts.get(char_s, 0) + 1
        counts[char_t] = counts.get(char_t, 0) - 1
        
    # If they are mathematically perfect anagrams, every single increment was 
    # perfectly offset by a corresponding decrement, leaving a map full of Zeros!
    for char, count in counts.items():
        if count != 0:
            print(f"    -> [MISMATCH] Character '{char}' has a net balance of {count}")
            return False
            
    print("    -> [MATCH] Perfect Anagram! All characters net to exactly 0.")
    return True

def demonstrate_anagram():
    section_header("Easy: Valid Anagram (Frequency Map)")
    
    s = "anagram"
    t = "nagaram"
    ans = is_anagram(s, t)
    print(f"\nResult: {ans} (Expected: True)")


def run_all_labs():
    demonstrate_two_sum()
    demonstrate_contains_duplicate()
    demonstrate_anagram()


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "In Two Sum, why do we store `Value -> Index` in the Hash Map, instead of `Index -> Value`?"
   Senior Answer: "Hash Maps are fundamentally optimized to perform lightning-fast $O(1)$ lookups on their *Keys*, not their *Values*. In Two Sum, our goal is to instantly answer the question: 'Have we seen the complement number before?'. If we stored the Index as the Key, we would have to loop through all the Values in the Hash Map to find the complement, degrading the algorithm back to a horrific $O(N^2)$ Time Complexity. By assigning the raw Number as the Key, we can query `if complement in hash_map` in strict $O(1)$ constant time. We store the original Array Index as the corresponding Value so we can successfully return it to the user."

2. Interviewer: "Can Two Sum be solved in $O(1)$ Space instead of $O(N)$ Space? If so, what is the trade-off?"
   Senior Answer: "Yes, but only if we mathematically sacrifice the Time Complexity. To achieve $O(1)$ Space, we must abandon the Hash Map entirely. We can sort the array in-place ($O(N \\log N)$ Time), and then use the Two-Pointer technique (Left and Right bounds). We sum the pointers: if the sum is too small, we move Left up; if the sum is too large, we move Right down. The fatal flaw with sorting is that it permanently destroys the original Indices! If the problem requires returning the *original* indices (like Two Sum usually does), we are forced to attach the original index to the value *before* sorting, which requires allocating a new array of Tuples, instantly defeating the $O(1)$ Space constraint anyway."

3. Interviewer: "In Valid Anagram, why is the Space Complexity explicitly $O(1)$ even though we allocate a Hash Map that scales with the string?"
   Senior Answer: "The Space Complexity of an algorithm is defined by how the memory scales relative to $N$ (the size of the input). A Hash Map mapping character frequencies is strictly bounded by the size of the alphabet. If the input string contains only lowercase English letters, the Hash Map will physically max out at exactly 26 keys. It mathematically does not matter if the input string is 10 characters long or 100 Billion characters long; the Hash Map will never exceed 26 integer counters. Because the maximum memory ceiling is a permanent constant bound, the Space Complexity is mathematically $O(1)$."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Problem Sets (Array Easy) Completed.")
