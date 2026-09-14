"""
# ==============================================================================
# LABORATORY: INTERVIEW PREPARATION (PROBLEM SETS - STRING MEDIUM)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# "Medium" String problems test your ability to implement Sliding Windows and 
# internal string expansion (Dynamic Programming logic). 
#
# A junior engineer solves "Longest Substring" by generating every single 
# combination of substrings ($O(N^3)$), timing out immediately on 10,000 chars.
#
# A senior engineer uses a dynamically adjusting Sliding Window with a Hash Map. 
# They process the string in exactly one $O(N)$ pass. If a collision is detected, 
# they instantly teleport the left side of the window past the collision, 
# completely bypassing the redundant character scanning!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master the Dynamic Sliding Window (Longest Substring).
# - Master Dual-Pointer Center Expansion (Longest Palindromic Substring).
# - Understand string manipulation without memory allocation constraints.
#
# ==============================================================================
"""

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. LONGEST SUBSTRING WITHOUT REPEATING CHARACTERS (SLIDING WINDOW)
# ==============================================================================
def length_of_longest_substring(s: str) -> int:
    """
    Time: O(N) | Space: O(1) (Hash Map scales strictly to alphabet size)
    Find the length of the longest substring without repeating characters.
    """
    # Maps a Character to its absolute LATEST INDEX in the string!
    seen = {}
    
    # The physical boundaries of our 'Window'
    left = 0
    max_length = 0
    
    print(f"  String: '{s}'")
    print("  Deploying Sliding Window...")
    
    for right in range(len(s)):
        char = s[right]
        
        # 1. COLLISION DETECTION!
        # Have we seen this character before? AND is its previous position 
        # physically INSIDE our current window? (If it's outside our left boundary, 
        # it's from a previous era and we don't care!)
        if char in seen and seen[char] >= left:
            print(f"    -> [COLLISION] '{char}' found again at index {right}. Previous was at {seen[char]}.")
            
            # 2. TELEPORT THE LEFT BOUNDARY!
            # We don't inch the left boundary forward by 1. That is slow!
            # We instantly snap the left boundary to exactly 1 position AFTER 
            # the old character, mathematically destroying the duplicate!
            left = seen[char] + 1
            print(f"       Snapping Left boundary to index {left}.")
            
        # 3. RECORD AND MEASURE
        # Record the NEW position of this character!
        seen[char] = right
        
        # Calculate the length of the current window (Right - Left + 1)
        current_length = right - left + 1
        max_length = max(max_length, current_length)
        
    return max_length

def demonstrate_longest_substring():
    section_header("Medium: Longest Substring Without Repeats")
    
    s = "abcabcbb"
    ans = length_of_longest_substring(s)
    print(f"\nResult: Length {ans} (Expected: 3, 'abc')")


# ==============================================================================
# 4. LONGEST PALINDROMIC SUBSTRING (CENTER EXPANSION)
# ==============================================================================
def longest_palindrome(s: str) -> str:
    """
    Time: O(N^2) | Space: O(1)
    Given a string s, return the longest palindromic substring in s.
    
    A junior uses DP which takes O(N^2) Time AND O(N^2) RAM.
    A senior uses Center Expansion which takes O(N^2) Time but strict O(1) RAM!
    """
    if not s or len(s) == 1:
        return s
        
    # We only store the physical boundaries of the absolute best palindrome found!
    best_left, best_right = 0, 0
    
    def expand_around_center(left_ptr: int, right_ptr: int) -> int:
        """
        Pushes pointers outward symmetrically until a mismatch occurs.
        Returns the absolute mathematical LENGTH of the palindrome.
        """
        # While pointers are in bounds AND the characters perfectly match...
        while left_ptr >= 0 and right_ptr < len(s) and s[left_ptr] == s[right_ptr]:
            left_ptr -= 1
            right_ptr += 1
            
        # The while loop terminated because a mismatch occurred (or bounds hit).
        # Therefore, the valid palindrome is one step INSIDE the current pointers!
        # Formula: (right_ptr - 1) - (left_ptr + 1) + 1  => right_ptr - left_ptr - 1
        return right_ptr - left_ptr - 1

    print("  Executing Dual-Center Expansion Engine...")
    for i in range(len(s)):
        # Case A: Odd-length Palindrome (Center is exactly 1 character, e.g. "aba")
        len1 = expand_around_center(i, i)
        
        # Case B: Even-length Palindrome (Center is exactly BETWEEN 2 characters, e.g. "abba")
        len2 = expand_around_center(i, i + 1)
        
        # Which expansion performed better?
        max_len = max(len1, len2)
        
        # Did it beat our global record?
        current_best = best_right - best_left + 1
        if max_len > current_best:
            # We must mathematically reverse-calculate the Left and Right bounds 
            # based on the center index (i) and the total length!
            best_left = i - (max_len - 1) // 2
            best_right = i + max_len // 2
            print(f"    -> [NEW RECORD] Length {max_len} found. String: '{s[best_left:best_right+1]}'")
            
    # Finally, allocate memory exactly ONCE to return the best string.
    return s[best_left:best_right+1]

def demonstrate_longest_palindrome():
    section_header("Medium: Longest Palindromic Substring (O(1) Space)")
    
    s = "babad"
    ans = longest_palindrome(s)
    print(f"\nResult: '{ans}' (Expected: 'bab' or 'aba')")


def run_all_labs():
    demonstrate_longest_substring()
    demonstrate_longest_palindrome()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "In 'Longest Substring Without Repeating Characters', why do we check `seen[char] >= left` instead of just checking if the character is in the map?"
   Senior Answer: "The Hash Map retains a permanent historical memory of every character we have ever encountered in the string. If we are currently evaluating the window from index 5 to 10, and we encounter an 'a' at index 10, we check the map. The map might say we saw an 'a' at index 2. Index 2 is physically outside our current window! That old 'a' was mathematically abandoned when the Left pointer advanced past it. If we didn't check `seen[char] >= left`, the algorithm would falsely trigger a collision for a character that isn't even in the current window anymore, destroying the length calculation."

2. Interviewer: "In 'Longest Palindromic Substring', why do we have to call `expand_around_center` TWICE for every index?"
   Senior Answer: "Palindromes exist in two distinct mathematical topologies: Odd-length and Even-length. An Odd palindrome (like 'racecar') pivots around a single solid character (the 'e'). To capture it, we initialize both the left and right pointers on the exact same index (`i`, `i`) and expand outward. An Even palindrome (like 'abba') has a hollow center; it pivots perfectly between the two 'b's. If we only initialized pointers on a single character, we would physically skip the hollow center! We must invoke `expand(i, i+1)` to initialize the left pointer on the first 'b' and the right pointer on the second 'b', covering both geometric possibilities."

3. Interviewer: "Could we solve Longest Palindromic Substring faster than $O(N^2)$?"
   Senior Answer: "Yes, using Manacher's Algorithm, which achieves a flawless $O(N)$ Time Complexity. However, Manacher's Algorithm requires complex string preprocessing (injecting dummy '#' characters between every letter to force all palindromes into Odd-length topology) and an array to cache expansion boundaries to bypass redundant checks. It is notoriously complex and prone to implementation errors under interview pressure. Center Expansion ($O(N^2)$ Time, $O(1)$ Space) is universally accepted by FAANG interviewers as the optimal balance of engineering readability, memory constraint satisfaction, and execution speed."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Problem Sets (String Medium) Completed.")
