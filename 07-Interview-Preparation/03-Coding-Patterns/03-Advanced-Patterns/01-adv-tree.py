"""
# ==============================================================================
# LABORATORY: INTERVIEW PREPARATION (CODING PATTERNS - ADVANCED TREES)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Interviewer: "I have a dictionary of 1 Million English words. I need an 
# auto-complete feature that instantly finds all words starting with 'app'."
#
# If you iterate through a List `if word.startswith('app')`, you write O(N*K) 
# and destroy the server. If you use a Hash Set, it only supports exact matches 
# (O(1)), it cannot perform prefix searches! 
# You MUST use a Prefix Tree (Trie). A Trie compresses all 1 Million words into 
# a graph where overlapping prefixes share physical memory nodes. Searching takes 
# strictly O(K) where K is the length of the prefix.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master the Trie (Prefix Tree) Architecture.
# - Implement Trie Insertion and Prefix Search.
# - Understand the horrific memory footprint of an un-optimized Trie.
#
# ==============================================================================
"""

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. TRIE ARCHITECTURE (THE PREFIX TREE)
# ==============================================================================
class TrieNode:
    def __init__(self):
        # A Hash Map routing to child nodes! 
        # (e.g., {'a': TrieNode, 'b': TrieNode})
        self.children = {}
        # A Boolean flag to mark the absolute end of a valid word.
        self.is_end_of_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        """
        Time: O(K) where K is length of the word.
        Space: O(K) if it's a brand new word with no shared prefixes.
        """
        current = self.root
        
        for char in word:
            # If the physical path doesn't exist, build a new Node!
            if char not in current.children:
                current.children[char] = TrieNode()
            # Traverse mathematically down the tree
            current = current.children[char]
            
        # Lock in the state machine!
        current.is_end_of_word = True
        print(f"    [TRIE] Inserted word: '{word}'")

    def search(self, word: str) -> bool:
        """
        Returns True if the EXACT word is in the Trie.
        Time: O(K)
        """
        current = self.root
        
        for char in word:
            if char not in current.children:
                return False
            current = current.children[char]
            
        return current.is_end_of_word

    def starts_with(self, prefix: str) -> bool:
        """
        Returns True if ANY word in the Trie starts with the given prefix.
        Time: O(K)
        """
        current = self.root
        
        for char in prefix:
            if char not in current.children:
                return False
            current = current.children[char]
            
        return True

def demonstrate_trie():
    section_header("Trie (Auto-Complete Engine)")
    
    trie = Trie()
    print("Building the Dictionary Database...")
    trie.insert("apple")
    trie.insert("app")
    trie.insert("application")
    trie.insert("banana")
    
    print("\nExecuting Queries:")
    
    print("  Q1: Search exactly 'apple'")
    print(f"      Result: {trie.search('apple')} (Expected: True)")
    
    print("  Q2: Search exactly 'app'")
    print(f"      Result: {trie.search('app')} (Expected: True)")
    
    print("  Q3: Search exactly 'appl'")
    print(f"      Result: {trie.search('appl')} (Expected: False - It's a prefix, not a full word!)")
    
    print("  Q4: Starts with 'appl'")
    print(f"      Result: {trie.starts_with('appl')} (Expected: True)")
    
    print("  Q5: Starts with 'cat'")
    print(f"      Result: {trie.starts_with('cat')} (Expected: False)")


def run_all_labs():
    demonstrate_trie()


# ==============================================================================
# 4. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "Why is a Trie faster than a Hash Set for 'startswith' queries, but slower than a Hash Set for 'exact match' queries?"
   Senior Answer: "A Hash Set computes a mathematical hash of the entire word and looks up the exact RAM location in $O(1)$ time. However, a Hash Set completely destroys the physical structure of the word. 'apple' and 'app' produce totally unrelated, chaotic integers. Therefore, finding a 'prefix' in a Hash Set is mathematically impossible without iterating over every single word ($O(N)$). A Trie physically models the characters as a Directed Graph. To find a prefix, it just walks down the tree character by character. Searching takes exactly $O(K)$ time (where $K$ is the length of the string). While $O(K)$ is infinitely faster than $O(N)$ for prefix matching, it is technically slower than the $O(1)$ instantaneous exact-match speed of a Hash Set."

2. Interviewer: "What is the catastrophic memory flaw of a standard Trie implementation?"
   Senior Answer: "A standard Trie uses a Hash Map (or a 26-element Array) at every single Node to point to its children. If you insert 1 Million long, completely unique words (e.g., DNA sequences) with zero overlapping prefixes, the Trie will allocate millions of individual Node objects and millions of Hash Tables. The Object/Hash overhead in languages like Python will violently consume Gigabytes of RAM, causing a catastrophic memory leak compared to just storing the raw strings in a List. Tries are only memory-efficient when the dataset has massive amounts of heavily overlapping prefixes (like English dictionaries)."

3. Interviewer: "How do you optimize a Trie's memory to fix the overhead?"
   Senior Answer: "To fix the memory explosion, we use a 'Radix Tree' (or Patricia Trie). Instead of forcing every Node to store exactly one character, a Radix Tree mathematically compresses non-branching paths into a single String. If the Trie has a straight path `r -> e -> e -> t`, a Radix Tree crushes those 4 Nodes into a single Node containing the raw string `'reet'`. This eliminates the massive Object allocation overhead, vastly accelerating both time and space complexity."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Interview Prep (Advanced Trees) Completed.")
