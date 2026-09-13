"""
# ==============================================================================
# LABORATORY: COMPETITIVE PROGRAMMING (STRING MANIPULATION)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Strings are immutable in Python. Every time you slice, concatenate, or modify 
# a string in a loop, Python asks the OS for new memory, physical copies the 
# data, and deletes the old memory.
# 
# A junior developer writing `result += s[i]` in a loop of $10^6$ characters 
# will cause a catastrophic $O(N^2)$ Time Limit Exceeded (TLE) crash.
#
# To master String problems (Anagrams, Palindromes, Substrings), you must 
# master Hash Maps (`collections.Counter`), ASCII character math (`ord()`), 
# and Sliding Windows.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master Anagram detection using $O(N)$ Hash Maps.
# - Group Anagrams using Tuples as Dictionary Keys.
# - Understand the foundational logic of Substring Searching (Sliding Window).
#
# ==============================================================================
"""

from collections import Counter, defaultdict

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. ANAGRAM DETECTION (THE COUNTER TRICK)
# ==============================================================================
def is_anagram(s: str, t: str) -> bool:
    """
    Checks if `t` is an exact anagram of `s`.
    Naive: return sorted(s) == sorted(t) -> Time: O(N log N)
    Optimal: Hash Map (Counter) -> Time: O(N), Space: O(1) (Only 26 letters max)
    """
    if len(s) != len(t):
        return False
        
    # The Counter natively tallies frequencies in C-optimized code!
    return Counter(s) == Counter(t)

def demonstrate_anagrams():
    section_header("O(N) Anagram Detection")
    
    s = "listen"
    t = "silent"
    print(f"String 1: '{s}'")
    print(f"String 2: '{t}'")
    
    print(f"Is Anagram? {is_anagram(s, t)}")
    
    print("\nUnder the hood, `Counter(s)` creates:")
    print(dict(Counter(s)))


# ==============================================================================
# 4. GROUPING ANAGRAMS (TUPLES AS KEYS)
# ==============================================================================
def group_anagrams(strs: list[str]) -> list[list[str]]:
    """
    Given an array of strings, group the anagrams together.
    Time Complexity: O(N * K) where N is strings, K is max string length.
    
    Trick: We cannot use a Dictionary as a Dictionary Key!
    We MUST use an immutable Tuple of length 26 (representing a-z frequencies)
    as the mathematical signature for each string.
    """
    # Maps a Tuple signature to a List of words
    anagram_map = defaultdict(list)
    
    for word in strs:
        # Create a frequency array of 26 zeroes
        count = [0] * 26
        
        # Populate the frequencies using ASCII math
        for char in word:
            # ord('a') is 97. ord('b') - ord('a') = 1.
            count[ord(char) - ord('a')] += 1
            
        # Lists cannot be dictionary keys (they are mutable).
        # We must cast it to a Tuple!
        signature = tuple(count)
        
        anagram_map[signature].append(word)
        
    return list(anagram_map.values())

def demonstrate_group_anagrams():
    section_header("Grouping Anagrams (Tuple Signatures)")
    
    words = ["eat", "tea", "tan", "ate", "nat", "bat"]
    print(f"Input Words: {words}\n")
    
    groups = group_anagrams(words)
    
    for idx, group in enumerate(groups):
        print(f"Group {idx + 1}: {group}")


# ==============================================================================
# 5. SUBSTRING SEARCHING (FIXED SLIDING WINDOW)
# ==============================================================================
def find_all_anagrams(s: str, p: str) -> list[int]:
    """
    Finds all start indices of p's anagrams in s.
    Time Complexity: O(N), Space Complexity: O(1).
    
    This uses a Fixed-Size Sliding Window.
    """
    if len(p) > len(s): return []
    
    p_count = Counter(p)
    window_count = Counter(s[:len(p)])
    result = []
    
    # Check the very first window
    if p_count == window_count:
        result.append(0)
        
    # Slide the window across the rest of the string
    left = 0
    for right in range(len(p), len(s)):
        # 1. ADD the new character on the right
        window_count[s[right]] += 1
        
        # 2. REMOVE the old character on the left
        left_char = s[left]
        window_count[left_char] -= 1
        
        # 3. CLEANUP: If count hits 0, delete it from the dictionary 
        # so the `==` comparison perfectly matches keys.
        if window_count[left_char] == 0:
            del window_count[left_char]
            
        left += 1
        
        # 4. CHECK validity
        if window_count == p_count:
            result.append(left)
            
    return result

def demonstrate_sliding_window_anagrams():
    section_header("Substring Search (Fixed Sliding Window)")
    
    s = "cbaebabacd"
    p = "abc"
    
    print(f"Search String: '{s}'")
    print(f"Target Pattern: '{p}'")
    
    indices = find_all_anagrams(s, p)
    print(f"Anagrams found starting at indices: {indices}")
    
    print("\nBy adding 1 char on the right, and removing 1 char on the left, ")
    print("we updated the Hash Map in exactly O(1) time instead of rebuilding ")
    print("it from scratch for every substring!")


def run_all_labs():
    demonstrate_anagrams()
    demonstrate_group_anagrams()
    demonstrate_sliding_window_anagrams()


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. When checking if two strings are anagrams, why is `Counter(s) == Counter(t)` superior to `sorted(s) == sorted(t)`?
   Answer: Time Complexity. Sorting a string requires comparing the characters, resulting in an $O(N \log N)$ mathematical cost. A Hash Map (or `collections.Counter`) scans the string exactly once to tally the frequencies, achieving mathematically perfect $O(N)$ linear time. Furthermore, because the English alphabet only has 26 lowercase letters, the Hash Map will never exceed 26 keys. Therefore, the Space Complexity is effectively $O(1)$, making the Counter approach vastly superior in both speed and memory.

2. In the "Group Anagrams" problem, why must we convert the frequency list `[0]*26` into a `tuple` before using it as a dictionary key?
   Answer: In Python, dictionary keys must be Hashable (Immutable). A Python `list` is a dynamic, mutable object. If you were allowed to use a list as a dictionary key, and later mutated the list (`my_list.append(5)`), the physical hash of the object would change, permanently corrupting the internal $O(1)$ memory mapping of the Hash Table. A `tuple` is strictly immutable; it can never be changed after creation. By casting the list to a tuple, we satisfy Python's strict hashing requirements and safely use the 26-element integer signature as the key.

3. In a Fixed-Size Sliding Window over a string (e.g., finding anagrams), why is it critical to explicitly execute `del window_count[char]` when a character's frequency drops to 0?
   Answer: Dictionary Equality math. In Python, checking `dict_A == dict_B` compares both the Keys and the Values. Suppose the target pattern $P$ is "abc" (`{'a':1, 'b':1, 'c':1}`). If our sliding window drops the letter "d", our window dictionary becomes `{'a':1, 'b':1, 'c':1, 'd':0}`. Even though the mathematical frequency of "d" is 0 (meaning it's not in the window), the string literal "d" still physically exists as a Key in the Hash Map. The equality check will see 4 keys vs 3 keys, instantly return `False`, and completely miss a valid anagram. Deleting the key purges the memory and perfectly synchronizes the maps.
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: String Manipulation Completed.")
