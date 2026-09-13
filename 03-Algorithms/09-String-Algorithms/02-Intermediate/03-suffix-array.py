"""
# ==============================================================================
# LABORATORY: SUFFIX ARRAY (PREFIX DOUBLING)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You have the entire Human Genome (3 Billion characters of DNA). You want to 
# search for a specific 100-character sequence.
#
# - KMP / Z-Algorithm takes O(N) time. Searching 3 Billion characters takes seconds. 
#   If you need to search for 1 Million different sequences, it takes WEEKS.
#
# What if we could pre-process the text so that ANY search, no matter how long 
# the text is, takes O(M log N) time? (For 3 Billion characters, log2(3B) is just 31!).
#
# Enter the Suffix Array.
# A Suffix Array is just a simple array of integers. It lists the starting indices 
# of all possible suffixes of a string, SORTED in strict alphabetical order.
#
# Example: "banana$"
# Suffixes: "banana$", "anana$", "nana$", "ana$", "na$", "a$", "$"
# Sorted: 
# 1. "$"       (Index 6)
# 2. "a$"      (Index 5)
# 3. "ana$"    (Index 3)
# 4. "anana$"  (Index 1)
# 5. "banana$" (Index 0)
# 6. "na$"     (Index 4)
# 7. "nana$"   (Index 2)
#
# Suffix Array: [6, 5, 3, 1, 0, 4, 2]
#
# How does this solve searching? 
# Because the array is alphabetically sorted, you can use Binary Search!
# To find "nan", you just binary search the Suffix Array. It takes O(log N) 
# checks. Each check compares M characters. Total time: O(M log N).
#
# Building the Suffix Array naively takes O(N^2 log N) time.
# The "Prefix Doubling" algorithm builds it in O(N log^2 N) time.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the alphabetical sorting of Suffixes.
# - Implement the Prefix Doubling $O(N \log^2 N)$ algorithm.
# - Execute $O(M \log N)$ string searching via Binary Search.
#
# ==============================================================================
"""

from typing import List, Tuple

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. SUFFIX ARRAY ENGINE (O(N log^2 N))
# ==============================================================================
def build_suffix_array(s: str) -> List[int]:
    """
    Builds the Suffix Array using the Prefix Doubling technique.
    Time Complexity: O(N log^2 N)
    """
    # We append the $ character. It is lexicographically smaller than any alphabet 
    # character, which guarantees it perfectly caps off the string for sorting.
    s += "$"
    n = len(s)
    
    # 1. INITIALIZATION (Sort based on the first 1 character)
    # The suffix array initially just holds the indices 0 to N-1
    suffix_array = list(range(n))
    
    # The `rank` array holds the alphabetical ranking of the prefix.
    # Initially, the rank is just the ASCII value of the single character.
    rank = [ord(c) for c in s]
    
    # 2. PREFIX DOUBLING LOOP (1, 2, 4, 8, 16...)
    k = 1
    while k < n:
        
        # We want to sort the suffixes based on their 2k-length prefix!
        # Because we ALREADY sorted based on the k-length prefix in the previous 
        # loop, we can just pair up the ranks!
        # Pair = ( Rank of first half, Rank of second half )
        
        def get_rank_pair(i: int) -> Tuple[int, int]:
            # The rank of the first k characters
            first_half = rank[i]
            # The rank of the second k characters (if it extends past the string, rank is -1)
            second_half = rank[i + k] if i + k < n else -1
            return (first_half, second_half)
            
        # Sort the suffix array based on these pairs!
        # (Python's Timsort is stable and highly optimized for tuples, taking O(N log N))
        suffix_array.sort(key=get_rank_pair)
        
        # 3. RE-RANKING
        # Now that they are sorted, we must assign NEW integer ranks from 0 upwards.
        new_rank = [0] * n
        current_rank = 0
        
        # The lowest sorted suffix naturally gets rank 0
        new_rank[suffix_array[0]] = 0
        
        for i in range(1, n):
            # If the rank pair of this suffix is identical to the previous one, 
            # they get the EXACT SAME integer rank!
            prev_suffix = suffix_array[i - 1]
            curr_suffix = suffix_array[i]
            
            if get_rank_pair(prev_suffix) == get_rank_pair(curr_suffix):
                new_rank[curr_suffix] = current_rank
            else:
                current_rank += 1
                new_rank[curr_suffix] = current_rank
                
        # Overwrite the old ranks with the newly calculated 2k ranks
        rank = new_rank
        
        # Double the prefix length!
        k *= 2
        
    return suffix_array


# ==============================================================================
# 4. BINARY SEARCH (O(M log N))
# ==============================================================================
def search_suffix_array(text: str, pattern: str, suffix_array: List[int]) -> bool:
    """
    Binary searches the Suffix Array to find if `pattern` exists.
    Time Complexity: O(M log N)
    """
    n = len(text)
    m = len(pattern)
    
    left = 0
    right = n # Note: The suffix array length is N+1 because of the '$'
    
    while left <= right:
        mid = (left + right) // 2
        
        # Extract the actual index in the text where this suffix starts
        suffix_start_index = suffix_array[mid]
        
        # Extract the prefix of the suffix (up to length M) to compare with pattern
        # The '$' is technically appended to the end of the text in memory.
        suffix_string = (text + "$")[suffix_start_index : suffix_start_index + m]
        
        if suffix_string == pattern:
            # We found a match! (In a real engine, you could scan left and right 
            # from `mid` to find ALL occurrences of this pattern).
            return True
        elif suffix_string < pattern:
            left = mid + 1
        else:
            right = mid - 1
            
    return False


def demonstrate_suffix_array():
    section_header("Algorithm: Suffix Array (Prefix Doubling)")
    
    text = "banana"
    print(f"Original String: '{text}'")
    
    sa = build_suffix_array(text)
    
    print("\nCalculated Suffix Array:")
    for i, idx in enumerate(sa):
        suffix = (text + "$")[idx:]
        print(f" SA[{i}] = {idx:2} -> '{suffix}'")
        
    section_header("Binary Search against Suffix Array")
    
    patterns = ["ana", "nan", "band", "a", "nana"]
    
    for pat in patterns:
        found = search_suffix_array(text, pat, sa)
        print(f"Searching for '{pat:4}' -> {'FOUND!' if found else 'Not Found'}")


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why does the Prefix Doubling algorithm run in $O(N \\log^2 N)$?
   Answer: The outer `while k < n` loop executes exactly $\\log_2 N$ times, because $k$ doubles ($1, 2, 4, 8...$). Inside this loop, we execute a sorting algorithm on an array of length $N$. A standard sorting algorithm takes $O(N \\log N)$ time. Multiplying the outer loop by the inner sort gives $O(N \\log N \\times \\log N) = O(N \\log^2 N)$. 

2. How is this better than the Naive sorting method?
   Answer: A naive method extracts all $N$ suffixes as strings, places them in a list, and calls `.sort()`. Sorting $N$ items takes $O(N \\log N)$ comparisons. But comparing two strings of length $N$ takes $O(N)$ time! Therefore, the naive approach takes $O(N^2 \\log N)$ time. By using the integer `rank` pairs, the Prefix Doubling algorithm mathematically bypasses the physical string comparison entirely, comparing tuples of integers in $O(1)$ time!

3. Is $O(N \\log^2 N)$ the fastest way to build a Suffix Array?
   Answer: No! In 2003, Kärkkäinen and Sanders invented the DC3 Algorithm (Difference Cover modulo 3), also known as the Skew Algorithm. It mathematically guarantees the construction of the Suffix Array in strict linear $O(N)$ time. Another method involves building a Suffix Tree using Ukkonen's Algorithm ($O(N)$) and performing a DFS to instantly extract the Suffix Array in $O(N)$. However, Prefix Doubling remains the undisputed standard for competitive programming due to its brevity and low constant factors.
"""

if __name__ == "__main__":
    demonstrate_suffix_array()
    print("\n[SUCCESS] Laboratory: Suffix Array Completed.")
