"""
# ==============================================================================
# LABORATORY: SUFFIX TREES & SUFFIX ARRAYS
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# If you want to search a massive DNA sequence (3 billion characters) for a 
# specific 10-character gene pattern, standard string matching (O(N*M)) or even 
# KMP (O(N+M)) takes too long if you have to perform thousands of queries.
# A Suffix Tree pre-processes the text in O(N) time. After that, ANY substring 
# query takes exactly O(M) time, where M is the length of the query! 
# (It completely ignores the length of the text N during the query).
# 
# Because true Suffix Trees (Ukkonen's Algorithm) are notoriously complex and 
# memory-heavy, modern competitive programming and genomics use Suffix Arrays instead.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand what a Suffix is, and how storing all suffixes allows substring search.
# - Build a naive Suffix Array in Python.
# - Perform an O(M log N) Binary Search on a Suffix Array to find a substring.
#
# ==============================================================================
"""

from typing import List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. CONCEPT: WHAT IS A SUFFIX?
# ==============================================================================
def explain_suffixes():
    section_header("The Concept of Suffixes")
    
    text = "banana$"
    print(f"Original Text: {text}")
    print("The '$' is a special terminal character (lexicographically smallest).")
    
    print("\nAll possible suffixes:")
    for i in range(len(text)):
        print(f"  Index {i}: {text[i:]}")
        
    print("\nWhy do this?")
    print("Every possible SUBSTRING of 'banana' is a PREFIX of one of these SUFFIXES.")
    print("For example, the substring 'nan' is a prefix of the suffix 'nana$'.")
    print("If we sort these suffixes alphabetically, we can use Binary Search to")
    print("find ANY substring instantly!")


# ==============================================================================
# 4. SUFFIX ARRAY IMPLEMENTATION
# ==============================================================================
class SuffixArray:
    """
    A memory-efficient alternative to a Suffix Tree.
    Instead of storing actual strings, we just store the starting integer indices 
    of the sorted suffixes.
    """
    def __init__(self, text: str):
        # We append a terminal character that is smaller than any standard char
        self.text = text + "$"
        self.n = len(self.text)
        
        # 1. Generate all suffixes (represented as index, string pairs)
        suffixes = [(i, self.text[i:]) for i in range(self.n)]
        
        # 2. Sort them alphabetically by the string
        # (Note: In production, we use O(N log N) algorithms like Prefix Doubling.
        # This naive sort takes O(N^2 log N) because comparing strings takes O(N) time).
        suffixes.sort(key=lambda x: x[1])
        
        # 3. Extract just the original indices
        self.suffix_array = [i for i, _ in suffixes]
        
    def display(self):
        print("Suffix Array Layout:")
        for idx in self.suffix_array:
            print(f"  SA[{idx:2}]: {self.text[idx:]}")

    def search(self, pattern: str) -> List[int]:
        """
        Binary Searches the Suffix Array for the pattern.
        Time Complexity: O(M * log N) where M is pattern length.
        Returns a list of all starting indices in the original text where pattern occurs.
        """
        m = len(pattern)
        
        # 1. Binary Search to find the FIRST occurrence
        left, right = 0, self.n - 1
        first_match = -1
        
        while left <= right:
            mid = (left + right) // 2
            suffix_idx = self.suffix_array[mid]
            # Extract the prefix of the suffix (length m) to compare with pattern
            current_prefix = self.text[suffix_idx : suffix_idx + m]
            
            if current_prefix == pattern:
                first_match = mid
                # We found a match, but there might be more to the left!
                right = mid - 1
            elif current_prefix < pattern:
                left = mid + 1
            else:
                right = mid - 1
                
        if first_match == -1:
            return []
            
        # 2. We found the first match. Since the array is sorted, any OTHER matches 
        # must be immediately to the right of it. Let's collect them all.
        results = []
        curr = first_match
        while curr < self.n:
            suffix_idx = self.suffix_array[curr]
            if self.text[suffix_idx : suffix_idx + m] == pattern:
                results.append(suffix_idx)
                curr += 1
            else:
                break
                
        # Return the original starting indices, sorted numerically
        return sorted(results)

def demonstrate_suffix_array():
    section_header("Algorithm: Suffix Array Generation & Search")
    
    text = "abracadabra"
    print(f"Building Suffix Array for: '{text}'...")
    sa = SuffixArray(text)
    
    sa.display()
    
    print("\n--- Searching ---")
    
    pattern1 = "abr"
    res1 = sa.search(pattern1)
    print(f"Search for '{pattern1}': Found at indices {res1}")
    
    pattern2 = "a"
    res2 = sa.search(pattern2)
    print(f"Search for '{pattern2}': Found at indices {res2}")
    
    pattern3 = "zebra"
    res3 = sa.search(pattern3)
    print(f"Search for '{pattern3}': Found at indices {res3} (Not Found)")


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. What is the relationship between Substrings and Suffixes?
   Answer: Every possible substring of a text is simply a prefix of one of its suffixes. Therefore, if you generate all suffixes, sort them, and perform a binary search, you can find any substring instantly.

2. Why use a terminal character like `$` at the end of the text?
   Answer: It ensures that no suffix is a prefix of another suffix in the tree representation, pushing smaller suffixes higher up the lexicographical sort order cleanly.

3. Why is a Suffix Array preferred over a Suffix Tree in modern computing?
   Answer: Suffix Trees are incredibly memory-intensive (requiring complex Node objects, edges, and pointers) and have notoriously poor CPU cache locality. A Suffix Array is just a contiguous array of integers. Even though binary searching it takes O(M log N) compared to the Tree's O(M), the Array is dramatically smaller and faster in reality due to hardware cache optimization.
"""

if __name__ == "__main__":
    explain_suffixes()
    demonstrate_suffix_array()
    print("\n[SUCCESS] Laboratory: Suffix Trees & Arrays Completed.")
