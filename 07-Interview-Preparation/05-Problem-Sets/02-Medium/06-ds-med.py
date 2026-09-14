"""
# ==============================================================================
# LABORATORY: INTERVIEW PREPARATION (PROBLEM SETS - DATA STRUCTURES MEDIUM)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Designing custom Data Structures requires combining primitive types (Arrays, 
# Hash Maps, Linked Lists) to mathematically guarantee specific Time Complexities.
#
# A junior engineer implements a Trie (Prefix Tree) by creating a massive Python 
# List of strings and running `startswith()` in a loop. Time Complexity: O(N * M), 
# completely failing autocomplete system designs.
#
# A senior engineer builds a true nested Node dictionary architecture, where 
# every character is an explicit pointer to the next character. Searching for a 
# 10-letter word among 100 Million dictionary words takes exactly 10 operations, 
# crushing the Time Complexity to a flawless O(M), independent of N.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master Prefix Trees (Implement Trie).
# - Master Multi-Stack coordination (Min Stack).
# - Understand constant-time O(1) state tracking.
#
# ==============================================================================
"""

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. IMPLEMENT TRIE (PREFIX TREE)
# ==============================================================================
class TrieNode:
    def __init__(self):
        # A Hash Map routing to children nodes! (Character -> TrieNode)
        self.children = {}
        # Mathematically flags if a complete word terminates at this specific node!
        self.is_end_of_word = False

class Trie:
    """
    Time: O(M) where M is the length of the word | Space: O(M)
    A tree data structure used to efficiently store and retrieve keys in a dataset 
    of strings (Auto-Complete Engine).
    """
    def __init__(self):
        # The absolute root of the tree starts empty.
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        curr = self.root
        for char in word:
            # If the character path doesn't exist, build it!
            if char not in curr.children:
                curr.children[char] = TrieNode()
            # Traverse DOWN the tree!
            curr = curr.children[char]
            
        # We finished injecting the word. Lock the final node!
        curr.is_end_of_word = True
        print(f"  [INSERT] Word '{word}' injected into Trie Engine.")

    def search(self, word: str) -> bool:
        curr = self.root
        for char in word:
            if char not in curr.children:
                print(f"    -> [SEARCH MISS] Path broke at character '{char}'")
                return False
            curr = curr.children[char]
            
        # The path exists, but is it a COMPLETE word? (e.g., searching 'app' when only 'apple' was inserted!)
        is_complete = curr.is_end_of_word
        print(f"    -> [SEARCH] Path for '{word}' found. Is complete word? {is_complete}")
        return is_complete

    def startsWith(self, prefix: str) -> bool:
        curr = self.root
        for char in prefix:
            if char not in curr.children:
                print(f"    -> [PREFIX MISS] Path broke at character '{char}'")
                return False
            curr = curr.children[char]
            
        # We only care if the PATH exists, not if it's a complete word!
        print(f"    -> [PREFIX MATCH] The prefix '{prefix}' exists in the engine.")
        return True

def demonstrate_trie():
    section_header("Medium: Implement Trie (Prefix Tree)")
    
    trie = Trie()
    trie.insert("apple")
    
    trie.search("apple")   # True
    trie.search("app")     # False (Not a complete word!)
    trie.startsWith("app") # True (It is a valid prefix!)
    
    trie.insert("app")
    trie.search("app")     # True (Now it is a complete word!)


# ==============================================================================
# 4. MIN STACK (O(1) STATE TRACKING)
# ==============================================================================
class MinStack:
    """
    Time: O(1) for ALL operations | Space: O(N)
    Design a stack that supports push, pop, top, and retrieving the minimum element 
    in constant time.
    
    If we just used a variable `self.min`, when the minimum element is popped off 
    the stack, we would have NO IDEA what the previous minimum was! We would have 
    to scan the whole stack (O(N)), instantly failing the O(1) constraint.
    """
    def __init__(self):
        # We use a SINGLE stack, but we store Tuples: (Value, Current_Minimum)
        # This permanently mathematically binds the absolute minimum state of the 
        # entire system to the specific node at the exact time it was inserted!
        self.stack = []

    def push(self, val: int) -> None:
        if not self.stack:
            self.stack.append((val, val))
            print(f"  [PUSH] {val}. Global Min: {val}")
            return
            
        # Mathematically compare the incoming value against the PREVIOUS system minimum!
        current_min = self.stack[-1][1]
        new_min = min(val, current_min)
        
        self.stack.append((val, new_min))
        print(f"  [PUSH] {val}. Global Min: {new_min}")

    def pop(self) -> None:
        if self.stack:
            val, _ = self.stack.pop()
            print(f"  [POP] Removed {val}.")

    def top(self) -> int:
        return self.stack[-1][0] if self.stack else -1

    def getMin(self) -> int:
        if self.stack:
            current_min = self.stack[-1][1]
            print(f"    -> [GET MIN] Absolute Minimum is {current_min}")
            return current_min
        return -1

def demonstrate_min_stack():
    section_header("Medium: Min Stack (O(1) Historical State Tracking)")
    
    ms = MinStack()
    ms.push(-2)
    ms.push(0)
    ms.push(-3) # Min is now -3!
    
    ms.getMin() # Returns -3
    ms.pop()    # Removes -3! The system must mathematically revert to -2!
    
    ms.getMin() # Returns -2! (Perfectly restored in O(1) time!)


def run_all_labs():
    demonstrate_trie()
    demonstrate_min_stack()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "In the Trie implementation, why do we use a Hash Map (`self.children = {}`) instead of an Array of size 26 (`self.children = [None] * 26`)?"
   Senior Answer: "If the dataset is strictly limited to lowercase English letters ('a'-'z'), an Array of size 26 is mathematically faster because index lookups (e.g., `ord(char) - ord('a')`) execute directly on the ALU in a single clock cycle, bypassing the chaotic memory hashing overhead of a Dictionary. However, if the Trie must support Unicode, Chinese characters, emojis, or punctuation, allocating an array for every possible UTF-8 character ($1,112,064$ slots) per node would catastrophically exhaust physical RAM. A Hash Map scales dynamically, consuming memory ONLY for characters that physically exist in the dataset, making it vastly superior for real-world production constraints."

2. Interviewer: "In the Min Stack, why is storing a Tuple `(Value, Min)` superior to maintaining two entirely separate stacks (one for Values, one for Mins)?"
   Senior Answer: "Maintaining two separate stacks is a perfectly valid architectural pattern, but it introduces parallel desynchronization risks. If a developer modifies the `pop()` method and forgets to pop from the secondary `min_stack`, the historical state of the system is permanently corrupted, leading to fatal false-minimums. By physically fusing the Value and the Minimum into an atomic Tuple `(Value, Min)` within a single Stack, the state becomes mathematically immutable. When a node is popped, both the value and its exact historical minimum context are guaranteed to be obliterated simultaneously, making the architecture structurally bulletproof."

3. Interviewer: "If I asked you to design a 'Max Stack' instead, how would the architecture change?"
   Senior Answer: "The architecture would be mathematically identical, simply reversing the comparative operator. Instead of tracking the local minimum via `min(val, current_min)`, we track the local maximum via `max(val, current_max)`. Every element pushed would store `(Value, Current_Maximum)`. The $O(1)$ constant-time constraints, historical state binding, and chronological reversion upon `pop()` would remain structurally flawless."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Problem Sets (Data Structures Medium) Completed.")
