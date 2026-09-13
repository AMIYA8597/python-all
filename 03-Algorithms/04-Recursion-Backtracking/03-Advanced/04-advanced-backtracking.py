"""
# ==============================================================================
# LABORATORY: ADVANCED BACKTRACKING (BOGGLE & TRIE PRUNING)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You know how to traverse a 2D Grid using Backtracking (like Sudoku or Maze).
# But what if the problem asks you to search a grid of letters (Boggle) to find 
# ALL valid dictionary words from a massive list of 100,000 words?
#
# A naive algorithm would run a full DFS for every single word in the dictionary, 
# resulting in O(W * 4^(N^2)) time. It would take years.
#
# How do we optimize it? We combine Backtracking with a **Trie** (Prefix Tree).
# 
# We load all 100,000 dictionary words into a single Trie.
# As our Backtracking algorithm steps from letter to letter on the grid, it 
# simultaneously traverses the Trie! 
# If the Trie says "There are ZERO words in the entire English language that 
# start with the prefix 'X-Q-Z'", the Backtracking algorithm instantly Prunes 
# that branch and stops!
#
# This is a classic FAANG architectural interview question, demonstrating how 
# Data Structures and Algorithms synergize to shatter exponential time limits.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Build a Trie specifically for Backtracking support.
# - Master Grid DFS traversal.
# - Pass the Trie Node down the Call Stack!
#
# ==============================================================================
"""

from typing import List, Set, Dict

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE TRIE STRUCTURE
# ==============================================================================
class TrieNode:
    def __init__(self):
        self.children: Dict[str, 'TrieNode'] = {}
        # Instead of just storing True/False, we store the full word string!
        # This makes it O(1) to append the solved word to our final results array.
        self.word: str = ""

def build_trie(words: List[str]) -> TrieNode:
    root = TrieNode()
    for word in words:
        node = root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        # Mark the end of the word
        node.word = word
    return root


# ==============================================================================
# 4. THE BACKTRACKING ENGINE
# ==============================================================================
def find_words(board: List[List[str]], words: List[str]) -> List[str]:
    """
    Time Complexity: O(M * N * 4^L) where L is max length of word.
    Space Complexity: O(Total Letters in Dictionary) for Trie.
    """
    # 1. Build the Trie
    root = build_trie(words)
    
    rows = len(board)
    cols = len(board[0])
    
    # We use a Set to automatically handle deduplication 
    # (in case the board has multiple ways to spell the same word).
    found_words: Set[str] = set()
    
    def backtrack(r: int, c: int, parent_node: TrieNode):
        # 1. PRUNING: Bounds check & Visited check
        # We mark visited cells with a "#" to avoid infinite loops
        if r < 0 or r >= rows or c < 0 or c >= cols or board[r][c] == "#":
            return
            
        char = board[r][c]
        
        # 2. PRUNING: The Trie Check!
        # If the Trie says this prefix doesn't exist, instantly abort!
        if char not in parent_node.children:
            return
            
        # Move the Trie pointer deeper
        current_node = parent_node.children[char]
        
        # 3. BASE CASE: Did we find a word?
        if current_node.word != "":
            found_words.add(current_node.word)
            # OPTIMIZATION: We can instantly delete the word from the Trie 
            # so we never waste time finding it again!
            current_node.word = ""
            
        # --- CHOOSE ---
        # Mark the current cell as Visited to prevent revisiting in this path
        board[r][c] = "#"
        
        # --- EXPLORE ---
        # Dive into all 4 cardinal directions (Up, Down, Left, Right)
        backtrack(r - 1, c, current_node) # UP
        backtrack(r + 1, c, current_node) # DOWN
        backtrack(r, c - 1, current_node) # LEFT
        backtrack(r, c + 1, current_node) # RIGHT
        
        # --- UNCHOOSE ---
        # The recursion returned. Un-mark the cell so other branches can use it!
        board[r][c] = char


    # Kick off the Backtracking from EVERY SINGLE SQUARE on the board!
    for r in range(rows):
        for c in range(cols):
            # Only start if the very first letter exists in the Trie root!
            if board[r][c] in root.children:
                backtrack(r, c, root)
                
    return list(found_words)


def demonstrate_word_search():
    section_header("Algorithm: Word Search (Boggle + Trie)")
    
    board = [
        ['o', 'a', 'a', 'n'],
        ['e', 't', 'a', 'e'],
        ['i', 'h', 'k', 'r'],
        ['i', 'f', 'l', 'v']
    ]
    
    dictionary = ["oath", "pea", "eat", "rain", "hike", "vfl"]
    
    print("Board:")
    for row in board:
        print(f" {row}")
        
    print(f"\nDictionary: {dictionary}\n")
    
    print("Executing Backtracking Trie Search...")
    results = find_words(board, dictionary)
    
    print(f"\nFound Valid Words: {results}")


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why did we pass the `TrieNode` down into the recursive function `backtrack(..., parent_node)`?
   Answer: If we didn't pass the Node, every recursive call would have to re-evaluate the ENTIRE string from the absolute Root of the Trie! That takes $O(L)$ time. By passing the `parent_node` reference down the stack, we instantly know the current state in $O(1)$ time. 

2. Why did we mutate the board `board[r][c] = "#"` instead of using a `visited` Set?
   Answer: Passing a `visited` Set down the Call Stack, or hashing/adding coordinates to a Set at every recursive step, causes massive Memory and CPU overhead. Mutating the original grid In-Place to an invalid character like `#`, and then restoring it on the Unchoose step, provides strict $O(1)$ visited checking with absolutely zero auxiliary memory footprint.

3. Why did we set `current_node.word = ""` after finding a word?
   Answer: If the board is full of identical letters (e.g. all 'A's), the Backtracking engine might find the word "AAA" millions of times through different snake-like paths. By deleting the word from the Trie the microsecond it is found, any future paths that accidentally construct "AAA" will simply pass right through without triggering the `add(word)` logic again.
"""

if __name__ == "__main__":
    demonstrate_word_search()
    print("\n[SUCCESS] Laboratory: Advanced Backtracking Completed.")
