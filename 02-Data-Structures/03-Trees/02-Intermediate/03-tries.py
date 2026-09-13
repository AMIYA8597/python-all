"""
# ==============================================================================
# LABORATORY: TRIES (PREFIX TREES)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# If you want to check if a word exists in a dictionary, a Hash Set is O(1). 
# But what if you want to find all words that START with "app"? A Hash Set requires 
# scanning every single word (O(N)). 
# A Trie (Prefix Tree) solves this. It stores characters in a tree structure. 
# Finding all words that start with "app" takes O(K) time, where K is the length 
# of the prefix. Tries are the foundation of Autocomplete, Spell Checkers, and 
# IP Routing (Longest Prefix Match).
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Build a TrieNode using a Hash Map (Dictionary) for O(1) child lookups.
# - Implement `insert`, `search`, and `startswith` methods.
# - Understand the Time and Space Complexity trade-offs.
#
# ==============================================================================
"""

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. TRIE NODE DEFINITION
# ==============================================================================
class TrieNode:
    def __init__(self):
        # Instead of `left` and `right`, a Trie node can have up to 26 children 
        # (for the English alphabet). Using a dictionary gives us O(1) child lookups.
        self.children = {}
        # We must mark when a path forms a complete word. 
        # (e.g., "app" is a prefix, but also a valid word, while "ap" is not).
        self.is_end_of_word = False


# ==============================================================================
# 4. TRIE IMPLEMENTATION
# ==============================================================================
class Trie:
    """
    LeetCode #208: Implement Trie (Prefix Tree)
    """
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        """
        Time Complexity: O(L), where L is the length of the word.
        """
        curr = self.root
        for char in word:
            # If the character path doesn't exist, create it.
            if char not in curr.children:
                curr.children[char] = TrieNode()
            # Move down the tree
            curr = curr.children[char]
            
        # Mark the final node as the end of a valid word
        curr.is_end_of_word = True

    def search(self, word: str) -> bool:
        """
        Returns True ONLY if the EXACT word was inserted.
        Time Complexity: O(L)
        """
        curr = self.root
        for char in word:
            if char not in curr.children:
                return False
            curr = curr.children[char]
            
        # We found the path, but is it a complete word? 
        # (e.g., searching for "ap" when only "apple" was inserted should return False).
        return curr.is_end_of_word

    def startsWith(self, prefix: str) -> bool:
        """
        Returns True if ANY word in the Trie starts with the given prefix.
        Time Complexity: O(L)
        """
        curr = self.root
        for char in prefix:
            if char not in curr.children:
                return False
            curr = curr.children[char]
            
        # We traversed the entire prefix successfully. 
        # We don't care if it's the end of a word or not.
        return True

def demonstrate_trie():
    section_header("Trie Execution: Insert, Search, StartsWith")
    
    trie = Trie()
    
    print("Inserting words: ['apple', 'app', 'apply', 'bat', 'batch']")
    words_to_insert = ["apple", "app", "apply", "bat", "batch"]
    for w in words_to_insert:
        trie.insert(w)
        
    print("\nSearch Tests:")
    print(f" Search 'apple': {trie.search('apple')} (Expected: True)")
    print(f" Search 'app':   {trie.search('app')} (Expected: True)")
    print(f" Search 'appl':  {trie.search('appl')} (Expected: False - Not a full word)")
    print(f" Search 'batman':{trie.search('batman')} (Expected: False - Path breaks)")
    
    print("\nStartsWith (Prefix) Tests:")
    print(f" StartsWith 'app': {trie.startsWith('app')} (Expected: True)")
    print(f" StartsWith 'appl':{trie.startsWith('appl')} (Expected: True)")
    print(f" StartsWith 'c':   {trie.startsWith('c')} (Expected: False)")


# ==============================================================================
# 5. ADVANCED: AUTOCOMPLETE SIMULATION
# ==============================================================================
class AutocompleteTrie(Trie):
    def __init__(self):
        super().__init__()
        
    def get_all_words_from_node(self, node: TrieNode, current_prefix: str, result: list):
        """Helper DFS to find all valid words branching from a specific node."""
        if node.is_end_of_word:
            result.append(current_prefix)
            
        for char, child_node in node.children.items():
            self.get_all_words_from_node(child_node, current_prefix + char, result)
            
    def get_suggestions(self, prefix: str) -> list:
        """Returns a list of all words that start with the prefix."""
        curr = self.root
        
        # 1. Traverse to the end of the prefix
        for char in prefix:
            if char not in curr.children:
                return [] # Prefix doesn't exist
            curr = curr.children[char]
            
        # 2. Run DFS from this node to find all branch endings
        suggestions = []
        self.get_all_words_from_node(curr, prefix, suggestions)
        return suggestions

def demonstrate_autocomplete():
    section_header("Algorithm: Autocomplete Suggestions")
    
    ac = AutocompleteTrie()
    for w in ["cat", "car", "cart", "card", "dog", "door"]:
        ac.insert(w)
        
    print("Finding suggestions for 'ca':")
    print(ac.get_suggestions("ca"))
    
    print("Finding suggestions for 'do':")
    print(ac.get_suggestions("do"))


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why does a Trie node use a Dictionary for its children instead of a List?
   Answer: A dictionary allows O(1) lookup to see if a character path exists. If we used a list, we would have to iterate through the list (O(K)) to find the correct character node.

2. What is the Space Complexity of a Trie?
   Answer: O(N * L * C), where N is the number of words, L is the average word length, and C is the size of the alphabet (if allocating fixed arrays per node). Tries use a MASSIVE amount of memory compared to a Hash Set, trading Space for extremely fast Prefix Searching.

3. Why can't we use a Hash Set for Autocomplete?
   Answer: A Hash Set hashes the ENTIRE string to a specific bucket. If you have "apple" in the set, and you search for "app", the hashes are completely different. You cannot do partial matching with a Hash Set without iterating through every single key.
"""

if __name__ == "__main__":
    demonstrate_trie()
    demonstrate_autocomplete()
    print("\n[SUCCESS] Laboratory: Tries Completed.")
