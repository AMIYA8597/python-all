"""
# ==============================================================================
# LABORATORY: ADVANCED STRING HASHING (O(1) SUBSTRING CHECKS)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You learned Manacher's Algorithm for Longest Palindrome, and Suffix Arrays 
# for Longest Common Substring. These are brilliant, but notoriously difficult 
# to memorize and code from scratch under the pressure of a 40-minute interview.
#
# What if there was a "Cheat Code" that let you solve almost ANY complex string 
# problem in competitive programming using just a few lines of basic math?
#
# Enter the Prefix Hash Array.
# Instead of a sliding window (Rabin-Karp), what if we pre-calculate the Hash 
# of EVERY single prefix of the string?
# `hash[0]` = Hash("A")
# `hash[1]` = Hash("AP")
# `hash[2]` = Hash("APP")
# `hash[3]` = Hash("APPL")
#
# Because hashes are just polynomial math, we can extract the Hash of ANY 
# arbitrary substring `[L, R]` in strict O(1) time using subtraction!
# `Hash("PL") = hash[3] - (hash[1] * Base^2)`
#
# This O(1) Substring Equality check is a superpower.
# - Longest Palindrome? Hash the string, Hash the reversed string. Binary 
#   Search the length. O(N log N) time. (No Manacher's needed!)
# - Longest Common Substring? Binary Search the length, hash all substrings 
#   of that length into a Set, and check the other string. O(N log N) time. 
#   (No Suffix Array needed!)
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Build the Prefix Hash Array and Inverse Power Array.
# - Extract arbitrary substring hashes in O(1) time.
# - Solve Longest Palindrome using Binary Search + Hashing.
#
# ==============================================================================
"""

from typing import List, Set

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. PREFIX HASH ENGINE (O(N) PRECOMPUTE, O(1) QUERY)
# ==============================================================================
class StringHash:
    def __init__(self, s: str):
        self.n = len(s)
        self.s = s
        
        self.d = 256
        self.q = 1000000007
        
        # 1. PRE-COMPUTE THE PREFIX HASHES
        self.pref_hash = [0] * (self.n + 1)
        
        # 2. PRE-COMPUTE THE POWERS OF THE BASE
        # We need this to mathematically shift the subtracted prefix to the 
        # correct magnitude!
        self.power = [1] * (self.n + 1)
        
        for i in range(self.n):
            # Update Hash
            self.pref_hash[i + 1] = (self.pref_hash[i] * self.d + ord(s[i])) % self.q
            # Update Power
            self.power[i + 1] = (self.power[i] * self.d) % self.q

    def get_hash(self, L: int, R: int) -> int:
        """
        Extracts the hash of the substring s[L...R] inclusive in strict O(1) time!
        """
        # Formula: Hash[0...R] - (Hash[0...L-1] * Base^(Length))
        length = R - L + 1
        
        # We use L and R+1 because pref_hash is 1-indexed to handle L=0 cleanly
        h = (self.pref_hash[R + 1] - self.pref_hash[L] * self.power[length]) % self.q
        
        # Modulo Math Quirk: Ensure positive result
        if h < 0:
            h += self.q
            
        return h


# ==============================================================================
# 4. APPLICATION: O(N LOG N) LONGEST PALINDROME (NO MANACHER'S)
# ==============================================================================
def find_longest_palindrome_hashing(s: str) -> str:
    """
    Finds the Longest Palindromic Substring using Binary Search and O(1) Hashing!
    Time Complexity: O(N log N)
    """
    n = len(s)
    if n == 0: return ""
    
    # 1. We build O(1) Hash extractors for the Forward string AND the Reversed string!
    forward_hash = StringHash(s)
    
    reversed_s = s[::-1]
    reverse_hash = StringHash(reversed_s)
    
    # Helper to map a forward index [L, R] to its exact reversed index!
    def is_palindrome(L: int, R: int) -> bool:
        # The exact length
        length = R - L + 1
        
        # Get forward hash
        h_fwd = forward_hash.get_hash(L, R)
        
        # Calculate the corresponding indices in the reversed string!
        # If string is length 10, index 0 maps to index 9.
        rev_L = n - 1 - R
        rev_R = n - 1 - L
        h_rev = reverse_hash.get_hash(rev_L, rev_R)
        
        return h_fwd == h_rev

    # 2. BINARY SEARCH FOR THE LONGEST ODD PALINDROME
    max_len = 1
    best_L = 0
    
    for i in range(n):
        # We binary search the RADIUS of the palindrome around center `i`.
        # Minimum radius = 0 (Length 1). Maximum radius = min(i, n-1-i).
        low = 0
        high = min(i, n - 1 - i)
        
        while low <= high:
            mid = (low + high) // 2
            
            # O(1) Check!
            if is_palindrome(i - mid, i + mid):
                # Valid palindrome! Can we go bigger?
                current_len = 2 * mid + 1
                if current_len > max_len:
                    max_len = current_len
                    best_L = i - mid
                low = mid + 1
            else:
                # Invalid! We must shrink the radius.
                high = mid - 1
                
    # 3. BINARY SEARCH FOR THE LONGEST EVEN PALINDROME
    for i in range(n - 1):
        # Center is strictly between `i` and `i+1`
        low = 0
        high = min(i, n - 2 - i)
        
        while low <= high:
            mid = (low + high) // 2
            
            if is_palindrome(i - mid, i + 1 + mid):
                current_len = 2 * mid + 2
                if current_len > max_len:
                    max_len = current_len
                    best_L = i - mid
                low = mid + 1
            else:
                high = mid - 1
                
    return s[best_L : best_L + max_len]


def demonstrate_hashing():
    section_header("Algorithm: Prefix Hash Array (O(1) Extraction)")
    
    s = "APPLE"
    print(f"String: {s}")
    
    hasher = StringHash(s)
    print("Pre-calculated Prefix Hashes!")
    
    # Let's extract "APP" (Indices 0 to 2) and "LE" (Indices 3 to 4)
    hash_app = hasher.get_hash(0, 2)
    hash_le = hasher.get_hash(3, 4)
    
    print(f"O(1) Extracted Hash for 'APP': {hash_app}")
    print(f"O(1) Extracted Hash for 'LE' : {hash_le}")
    
    section_header("Application: Longest Palindrome (Binary Search)")
    
    test_strings = [
        "BABAD",
        "CBBD",
        "ACACACACACACA",
        "XYABACABAQ"
    ]
    
    print("Finding palindromes in O(N log N) using Forward/Reverse Hashing (No Manacher's!)...")
    for test_str in test_strings:
        result = find_longest_palindrome_hashing(test_str)
        print(f" -> '{test_str}' : '{result}'")


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Explain the math behind $O(1)$ substring extraction: `hash[R+1] - hash[L] * Base^Len`.
   Answer: Imagine Base 10 instead of Base 256. The string is "123456". 
   `hash[6]` = 123456. (This represents the prefix `[0, 5]`).
   `hash[2]` = 12. (This represents the prefix `[0, 1]`).
   We want to extract the substring "3456" (Indices 2 to 5. Length 4).
   If we do `123456 - 12`, we get 123444. This is wrong. 
   We must shift the 12 over so it aligns with the start of the substring!
   We multiply 12 by Base^(Length). $12 \times 10^4 = 120000$.
   $123456 - 120000 = 3456$. Exactly what we wanted! This exact math works for Polynomial Base 256 hashing.

2. Why use Binary Search for the Palindrome Radius?
   Answer: Palindrome radiuses have a monotonic property. If a string is a palindrome of radius 3 (Length 7), it is mathematically guaranteed that its inner core is a palindrome of radius 2 (Length 5), and radius 1 (Length 3). Because of this strict True/False monotonic boundary (T, T, T, F, F, F), we can perfectly apply Binary Search! Instead of checking all $N/2$ possible radiuses linearly, we only check $\log(N/2)$ radiuses, dropping the time complexity to $O(N \log N)$.

3. Why is this considered a "Cheat Code" for interviews?
   Answer: Building a Suffix Array, LCP Array, Suffix Tree, or Manacher's Algorithm from scratch takes immense memorization and carries a very high risk of off-by-one errors during an interview. The Prefix Hash Array is just a basic `for` loop with a multiplier. Once you have the $O(1)$ `get_hash()` function, you can effortlessly solve dozens of "Hard" LeetCode string problems using standard Binary Search, bypassing the need for complex advanced data structures entirely!
"""

if __name__ == "__main__":
    demonstrate_hashing()
    print("\n[SUCCESS] Laboratory: Advanced String Hashing Completed.")
