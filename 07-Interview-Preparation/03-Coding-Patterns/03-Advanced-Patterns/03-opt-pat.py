"""
# ==============================================================================
# LABORATORY: INTERVIEW PREPARATION (CODING PATTERNS - OPTIMIZATIONS)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Interviewer: "I have a string of 100 Million characters. Count the number of 
# times the substring 'AABAACAABAA' appears in it."
#
# A junior engineer writes `string.count('AABAACAABAA')` which under the hood 
# does a naive nested loop matching. It runs in O(N*M) time, performing 1 Billion 
# character comparisons, and takes 5 seconds.
#
# A senior engineer deploys the Knuth-Morris-Pratt (KMP) string matching 
# algorithm. By pre-computing a 'Longest Prefix Suffix' (LPS) array in O(M) time, 
# the KMP algorithm never, ever steps backwards in the main string. It mathematically 
# skips redundant checks, reducing the search to a flawless O(N + M) time.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master Bit Manipulation (The XOR trick for finding singletons).
# - Master the KMP Algorithm (LPS Array for O(N) Substring Search).
# - Master Greedy Algorithms (Interval Scheduling).
#
# ==============================================================================
"""

from typing import List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. BIT MANIPULATION (THE XOR TRICK)
# ==============================================================================
def find_single_number(nums: List[int]) -> int:
    """
    Time: O(N) | Space: O(1)
    Given an array where every element appears twice EXCEPT for one. Find it.
    
    If we use a Hash Set, we use O(N) Space.
    If we use XOR (^), we use exactly O(1) space!
    
    Mathematical Laws of XOR:
    1. A ^ A = 0 (Any number XOR itself physically annihilates it!)
    2. A ^ 0 = A (XOR against 0 preserves the number)
    3. XOR is Associative and Commutative (Order doesn't matter!)
    
    Therefore, if we XOR every number in the array together, all duplicates 
    will mathematically annihilate each other into 0. The only thing left 
    will be 0 ^ Single_Number, which is exactly the Single Number!
    """
    result = 0
    for num in nums:
        result ^= num
        
    return result

def demonstrate_bit_manipulation():
    section_header("Bit Manipulation (The XOR Trick)")
    
    nums = [4, 1, 2, 1, 2]
    print(f"Array: {nums}")
    print("Every number appears twice except for '4'.")
    
    ans = find_single_number(nums)
    print(f"\nResult: {ans}")


# ==============================================================================
# 4. KMP ALGORITHM (O(N) SUBSTRING SEARCH)
# ==============================================================================
def compute_lps_array(pattern: str) -> List[int]:
    """
    Computes the Longest Prefix Suffix (LPS) array for the KMP algorithm.
    Time: O(M) where M is pattern length.
    """
    m = len(pattern)
    lps = [0] * m
    length = 0 # Length of the previous longest prefix suffix
    i = 1
    
    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    return lps

def kmp_search(text: str, pattern: str) -> List[int]:
    """
    Time: O(N + M) | Space: O(M) for the LPS array.
    Finds all starting indices of `pattern` inside `text`.
    """
    n, m = len(text), len(pattern)
    if m == 0: return []
    
    # Pre-compute the mathematical skip-table!
    lps = compute_lps_array(pattern)
    print(f"  Pattern '{pattern}' LPS Array: {lps}")
    
    result = []
    i = 0 # Index for text
    j = 0 # Index for pattern
    
    while i < n:
        if pattern[j] == text[i]:
            i += 1
            j += 1
            
        if j == m:
            print(f"  -> [MATCH FOUND] at index {i - j}")
            result.append(i - j)
            # Mathematically jump using the LPS array!
            j = lps[j - 1]
            
        elif i < n and pattern[j] != text[i]:
            # MISMATCH! We do NOT step 'i' backward!
            # We magically shift 'j' based on our pre-calculated table!
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
                
    return result

def demonstrate_kmp():
    section_header("KMP Algorithm (O(N) Substring Search)")
    
    text = "ABABDABACDABABCABAB"
    pattern = "ABABCABAB"
    
    print(f"Text:    {text}")
    print(f"Pattern: {pattern}\n")
    
    kmp_search(text, pattern)


# ==============================================================================
# 5. GREEDY ALGORITHMS (INTERVAL SCHEDULING)
# ==============================================================================
def max_non_overlapping_meetings(intervals: List[List[int]]) -> int:
    """
    Time: O(N log N) | Space: O(1)
    Given meeting times, what is the ABSOLUTE MAXIMUM number of meetings a single 
    person can attend without overlapping?
    
    THE GREEDY HEURISTIC: Always pick the meeting that ENDS EARLIEST.
    By finishing a meeting as early as possible, you mathematically leave the 
    maximum amount of free time available for the rest of the day!
    """
    if not intervals: return 0
    
    # SORT BY END TIME! (Not start time)
    intervals.sort(key=lambda x: x[1])
    
    count = 1
    current_end = intervals[0][1]
    
    print(f"  Attending: {intervals[0]}")
    
    for i in range(1, len(intervals)):
        # If the next meeting starts AFTER the current one ends, attend it!
        if intervals[i][0] >= current_end:
            print(f"  Attending: {intervals[i]}")
            count += 1
            current_end = intervals[i][1]
        else:
            print(f"  Skipping : {intervals[i]} (Overlaps!)")
            
    return count

def demonstrate_greedy():
    section_header("Greedy Algorithm (Interval Scheduling)")
    
    meetings = [[1, 2], [2, 3], [3, 4], [1, 3]]
    print(f"Meetings available: {meetings}\n")
    
    result = max_non_overlapping_meetings(meetings)
    print(f"\nResult: You can attend {result} meetings max.")


def run_all_labs():
    demonstrate_bit_manipulation()
    demonstrate_kmp()
    demonstrate_greedy()


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "Why does the Knuth-Morris-Pratt (KMP) algorithm pre-compute the Longest Prefix Suffix (LPS) array?"
   Senior Answer: "In a naive substring search, if we match 5 characters and then hit a mismatch on the 6th, we throw away all our work, step the main string's pointer back to index 1, and start completely over ($O(N \\times M)$). KMP realizes that those 5 successfully matched characters contain mathematical symmetry. By pre-computing the LPS array, KMP knows exactly how much of the prefix repeats itself. When a mismatch occurs, instead of moving the main string's pointer backward, it keeps it frozen in place, and mathematically shifts the pattern's pointer dynamically to the right by consulting the LPS array. This guarantees that the main string's pointer *never* moves backward, achieving a flawless $O(N)$ linear time complexity."

2. Interviewer: "In the Interval Scheduling (Max Meetings) problem, why must we sort by END TIME instead of START TIME?"
   Senior Answer: "If you sort by Start Time, you fall into a fatal Greedy trap. A meeting could start at 8:00 AM and end at 5:00 PM. Because it was first, you attend it, wiping out your entire day, resulting in a score of 1 meeting. Meanwhile, there were 10 different 30-minute meetings available between 8:00 AM and 5:00 PM. Sorting by End Time is the mathematically optimal Greedy heuristic. By always selecting the meeting that terminates the earliest, you mathematically liberate the absolute maximum contiguous block of remaining time for future meetings, perfectly guaranteeing the maximum global subset of non-overlapping intervals."

3. Interviewer: "Explain how XOR (`^`) mathematically isolates the single unique number in an array of duplicates."
   Senior Answer: "XOR is a bitwise operation that returns 1 only if the bits are different. Therefore, $A \\oplus A = 0$ (a number XORed against itself annihilates every bit into 0). Additionally, $A \\oplus 0 = A$ (XOR against 0 preserves the number). Finally, XOR is Commutative and Associative, meaning the order of operations is irrelevant. If we XOR every element in the array `[A, B, A, C, B]`, it mathematically rearranges to `(A \\oplus A) \\oplus (B \\oplus B) \\oplus C`. This evaluates to `0 \\oplus 0 \\oplus C`, which evaluates to `C`. It isolates the unique element in $O(N)$ time with zero memory allocation."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Interview Prep (Optimizations) Completed.")
