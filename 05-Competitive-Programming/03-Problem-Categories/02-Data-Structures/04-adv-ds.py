"""
# ==============================================================================
# LABORATORY: COMPETITIVE PROGRAMMING (ADVANCED DATA STRUCTURES)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A Hash Map allows you to check if a Word exists in exactly O(1) time. 
# But what if you want to know: "Do any words in the dictionary START WITH 'app'?"
#
# A Hash Map cannot answer this without scanning every single word, taking O(N) 
# time. If you are building the Autocomplete feature for Google Search, scanning 
# 10 Billion words takes 5 minutes per keystroke. You will be fired.
#
# You must use a Trie (Prefix Tree). A Trie physically structures strings letter 
# by letter. It finds prefixes in O(K) time, where K is the length of the prefix (e.g., 3)!
#
# Furthermore, what if you have a massive static array, and you need to answer 
# 10 Million Range Minimum Queries (RMQ)? A Segment Tree answers in O(log N). 
# A Sparse Table answers in mathematically perfect O(1) time!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the architecture of a Trie (Prefix Tree).
# - Understand the architecture of a Sparse Table (O(1) Range Queries).
#
# ==============================================================================
"""

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. TRIE (PREFIX TREE)
# ==============================================================================
class TrieNode:
    def __init__(self):
        # A hash map mapping a character (e.g. 'a') to the next TrieNode.
        # This is dynamically sized, saving memory compared to a fixed [None]*26 array.
        self.children = {}
        # Boolean flag to mark the absolute end of a valid dictionary word.
        self.is_word = False

class Trie:
    """
    Time Complexity: Insert O(L), Search O(L), StartsWith O(L) 
    where L is the length of the string.
    """
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        node = self.root
        for char in word:
            # If the character path doesn't exist, create it!
            if char not in node.children:
                node.children[char] = TrieNode()
            # Step down into the child node
            node = node.children[char]
        # We finished inserting the string. Mark the final node as a valid word.
        node.is_word = True

    def search(self, word: str) -> bool:
        """Returns True if the exact word exists."""
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        # Did the path end exactly on a valid word flag?
        return node.is_word

    def starts_with(self, prefix: str) -> bool:
        """Returns True if ANY word starts with this prefix."""
        node = self.root
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        # If we successfully traversed the entire prefix, it exists!
        return True


def demonstrate_trie():
    section_header("Trie (Prefix Tree) Autocomplete")
    
    trie = Trie()
    words = ["apple", "app", "apricot", "banana"]
    
    print(f"Inserting words into Trie: {words}")
    for word in words:
        trie.insert(word)
        
    print("\nExecuting Queries:")
    print(f"Search exact 'apple': {trie.search('apple')} (Expected: True)")
    print(f"Search exact 'appl': {trie.search('appl')} (Expected: False - 'appl' is not a full word)")
    print(f"Starts with 'app': {trie.starts_with('app')} (Expected: True - powers Autocomplete!)")
    print(f"Starts with 'bat': {trie.starts_with('bat')} (Expected: False)")


# ==============================================================================
# 4. SPARSE TABLE (O(1) RANGE MINIMUM QUERY)
# ==============================================================================
import math

class SparseTable:
    """
    Solves Static Range Minimum Query (RMQ) in exactly O(1) time.
    Drawback: The array must be STATIC. No updates allowed!
    Build Time: O(N log N)
    Space Complexity: O(N log N)
    """
    def __init__(self, arr: list[int]):
        self.n = len(arr)
        # Log base 2 of N (e.g. for N=1000, max_pow is 9)
        self.max_pow = int(math.log2(self.n)) + 1
        
        # Initialize a 2D Matrix of size (N) x (max_pow)
        # st[i][j] will store the Minimum value in the range starting at 
        # index `i` of length `2^j`.
        self.st = [[0] * self.max_pow for _ in range(self.n)]
        
        # 1. Base Case: Intervals of length 2^0 (length 1)
        for i in range(self.n):
            self.st[i][0] = arr[i]
            
        # 2. Dynamic Programming: Build larger intervals by combining two smaller halves!
        for j in range(1, self.max_pow):
            # The length of the interval we are building is 2^j.
            # E.g., if j=1, length is 2. If j=2, length is 4.
            interval_length = 1 << j 
            half_length = 1 << (j - 1)
            
            i = 0
            while i + interval_length <= self.n:
                # The minimum of a block of 4 elements is simply the minimum of 
                # the first 2 elements and the minimum of the second 2 elements!
                self.st[i][j] = min(
                    self.st[i][j - 1], 
                    self.st[i + half_length][j - 1]
                )
                i += 1

    def query(self, L: int, R: int) -> int:
        """Finds the minimum in the range [L, R] in O(1) time!"""
        # Find the largest power of 2 that fits inside the range [L, R]
        length = R - L + 1
        j = int(math.log2(length))
        
        # The magic of overlapping:
        # We query the block of size 2^j starting from L, and the block of size 
        # 2^j ending at R. They overlap, but since we are looking for the Minimum, 
        # checking the middle numbers twice doesn't change the mathematical result!
        return min(
            self.st[L][j], 
            self.st[R - (1 << j) + 1][j]
        )


def demonstrate_sparse_table():
    section_header("Sparse Table (O(1) Range Minimum Query)")
    
    # Indices:    0  1  2  3   4  5  6  7
    arr =        [5, 2, 4, 7, -3, 8, 1, 9]
    print(f"Original Array: {arr}")
    
    # Build Table: O(N log N)
    st = SparseTable(arr)
    print("Sparse Table Built using Dynamic Programming.")
    
    # Query: Minimum from index 1 to 3 -> min(2, 4, 7) = 2
    L, R = 1, 3
    print(f"\nQuery Minimum [idx {L} to {R}]: {st.query(L, R)} (Expected: 2) -> Executed in O(1) time!")
    
    # Query: Minimum from index 2 to 5 -> min(4, 7, -3, 8) = -3
    L, R = 2, 5
    print(f"Query Minimum [idx {L} to {R}]: {st.query(L, R)} (Expected: -3) -> Executed in O(1) time!")
    
    print("\nA Segment Tree would have taken O(log N) time for these queries.")


def run_all_labs():
    demonstrate_trie()
    demonstrate_sparse_table()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. In a Trie, why do we use `self.is_word = True` instead of just checking if the node has no children?
   Answer: Prefixes are often completely valid words on their own. If you insert "apple", the 'e' node has no children, so it's a word. If you then insert "app", the 'p' node *does* have a child (the 'l' in apple). If you relied on "having no children" to determine if a string is a word, "app" would not be recognized as a valid dictionary word, breaking the algorithm. The explicit boolean flag guarantees the exact termination point of every inserted string regardless of downstream children.

2. A Sparse Table solves RMQ in exactly $O(1)$ time by exploiting "Idempotency". What does that mean, and why does a Sparse Table fail for Range SUM Queries?
   Answer: Idempotency is a mathematical property where applying an operation multiple times does not change the result beyond the initial application (e.g., $f(f(x)) = f(x)$). Finding the Minimum is idempotent: `min(A, A) = A`. A Sparse Table queries a range of length 7 by asking for the precalculated Minimum of length 4 from the Left, and the precalculated Minimum of length 4 from the Right. These two blocks overlap by 1 element in the middle. Because `min()` is idempotent, evaluating the middle element twice is completely safe. Summation is NOT idempotent (`A + A = 2A`). If you overlap two blocks for a Sum query, the overlapping elements are double-counted, mathematically corrupting the answer. Sparse Tables can only be used for Idempotent functions (Min, Max, GCD, Bitwise OR/AND).

3. If a Sparse Table answers queries exponentially faster ($O(1)$) than a Segment Tree ($O(\log N)$), why aren't Segment Trees obsolete?
   Answer: Mutability. A Segment Tree handles dynamic updates (`arr[3] = 99`) in $O(\log N)$ time. A Sparse Table is a static, rigid 2D Matrix of Dynamic Programming results. If you change a single element in the original array, you mathematically corrupt $O(N \log N)$ overlapping blocks in the Sparse Table. To fix it, you have to completely rebuild the entire 2D matrix from scratch, taking $O(N \log N)$ time per update. Sparse Tables are only useful for 100% static, immutable arrays.
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Advanced Data Structures Completed.")
