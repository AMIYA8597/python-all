"""
# ==============================================================================
# LABORATORY: HUFFMAN CODING (GREEDY DATA COMPRESSION)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# If you type a 1,000-character text file in English, your computer saves it 
# using ASCII. Every single character takes exactly 8 bits (1 Byte).
# Total size: 8,000 bits.
#
# But wait... the letter 'E' appears all the time. The letter 'Z' almost never 
# appears. Why should 'E' take 8 bits? What if 'E' only took 2 bits?
# 
# In 1952, David Huffman invented a Greedy Algorithm that builds an optimal 
# "Prefix Tree". It analyzes the frequency of every character in your file. 
# It assigns the SHORTEST binary codes to the most frequent characters, and 
# the longest binary codes to the rarest characters.
#
# A 8,000-bit text file suddenly shrinks to 4,500 bits. 
# This exact Greedy Algorithm is the mathematical engine inside `.zip` files, 
# `.mp3` audio compression, and `.jpeg` image compression!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the Greedy "Merge the two smallest" heuristic.
# - Use a Priority Queue (Min-Heap) to build a Binary Tree from the bottom up.
# - Understand what makes a "Prefix-Free Code" decoding-safe.
#
# ==============================================================================
"""

import heapq
from collections import Counter
from typing import Dict, Optional

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. HUFFMAN TREE NODE
# ==============================================================================
class HuffmanNode:
    def __init__(self, char: Optional[str], freq: int):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None
        
    # We must define the Less-Than `<` operator so Python's `heapq` module 
    # knows how to sort our custom objects! It will sort by frequency.
    def __lt__(self, other):
        return self.freq < other.freq


# ==============================================================================
# 4. GREEDY COMPRESSION ALGORITHM
# ==============================================================================
class HuffmanEncoder:
    def __init__(self):
        self.root = None
        self.codes = {}
        
    def build_tree(self, text: str):
        """
        Time Complexity: O(N log N) where N is the unique character count.
        """
        # 1. Calculate frequency of every character
        freq_map = Counter(text)
        
        # 2. Create a Min-Heap of Leaf Nodes
        heap = []
        for char, freq in freq_map.items():
            heapq.heappush(heap, HuffmanNode(char, freq))
            
        # 3. THE GREEDY LOOP
        # We loop until there is only 1 node left in the heap (The Root).
        while len(heap) > 1:
            
            # --- THE GREEDY CHOICE ---
            # Pop the TWO ABSOLUTE SMALLEST frequency nodes!
            left_node = heapq.heappop(heap)
            right_node = heapq.heappop(heap)
            
            # Merge them together into a new internal node.
            # The internal node has NO character, but its frequency is the SUM.
            merged_freq = left_node.freq + right_node.freq
            internal_node = HuffmanNode(None, merged_freq)
            internal_node.left = left_node
            internal_node.right = right_node
            
            # Push the merged node back into the heap!
            heapq.heappush(heap, internal_node)
            
        # The final remaining node is the root of the Huffman Tree.
        self.root = heapq.heappop(heap)
        
    def generate_codes(self, node: HuffmanNode, current_code: str):
        """
        Runs a standard DFS to generate the binary strings for each leaf.
        """
        if node is None:
            return
            
        # If it's a leaf node (it has a character), lock in the code!
        if node.char is not None:
            self.codes[node.char] = current_code
            return
            
        # Left branches add a '0'
        self.generate_codes(node.left, current_code + "0")
        # Right branches add a '1'
        self.generate_codes(node.right, current_code + "1")
        
    def encode(self, text: str) -> str:
        self.build_tree(text)
        self.generate_codes(self.root, "")
        
        # Replace every character with its new binary code
        encoded_string = "".join(self.codes[char] for char in text)
        return encoded_string
        
    def decode(self, encoded_text: str) -> str:
        decoded_string = []
        current_node = self.root
        
        # Traverse the tree bit by bit!
        for bit in encoded_text:
            if bit == '0':
                current_node = current_node.left
            else:
                current_node = current_node.right
                
            # If we hit a leaf, append the character and reset to the root!
            if current_node.char is not None:
                decoded_string.append(current_node.char)
                current_node = self.root
                
        return "".join(decoded_string)


def demonstrate_huffman():
    section_header("Algorithm: Huffman Coding")
    
    text = "BEEP BOOP BEER!"
    print(f"Original Text: '{text}'")
    # ASCII = 8 bits per character
    print(f"ASCII Size: {len(text) * 8} bits.")
    
    encoder = HuffmanEncoder()
    compressed = encoder.encode(text)
    
    print("\nHuffman Dictionary (Prefix Codes):")
    for char, code in sorted(encoder.codes.items(), key=lambda x: len(x[1])):
        char_display = char if char != ' ' else '[SPACE]'
        print(f" '{char_display}' -> {code}")
        
    print(f"\nCompressed Binary: {compressed}")
    print(f"Huffman Size: {len(compressed)} bits.")
    print(f"Compression Ratio: {((len(text)*8 - len(compressed)) / (len(text)*8)) * 100:.1f}% reduction!")
    
    decompressed = encoder.decode(compressed)
    print(f"\nDecompressed Text: '{decompressed}'")
    assert text == decompressed


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why is it physically impossible to decode a string like `0101` if 'E' is `0` and 'Z' is `01`?
   Answer: Ambiguity! If the encoded string starts with `01`, is it an 'E' followed by something else, or is it a 'Z'? A decoder wouldn't know. Huffman Coding mathematically guarantees that no character's code is the prefix of another character's code (It is a "Prefix-Free Code"). This works because characters ONLY exist on the Leaf Nodes of the tree; an internal node is never assigned a character.

2. Why do we push the merged internal nodes back into the Min-Heap?
   Answer: Because the merged internal node represents the combined frequency of a subtree. If we merged 'Z' (freq 1) and 'Q' (freq 1), the internal node has freq 2. That internal node must compete with other rare characters (like 'X' freq 3) to be merged next. The Min-Heap guarantees we are always picking the absolute smallest mathematical weights available, regardless of whether they are individual leaves or massive merged subtrees.

3. Why is the Time Complexity $O(N \\log N)$?
   Answer: Building the frequency map is $O(C)$ where $C$ is the total characters. But inserting the $N$ unique characters into the heap takes $O(N \\log N)$. The `while` loop extracts 2 nodes and inserts 1 node. Heap operations take $O(\\log N)$. The loop runs $N-1$ times. Therefore, the Tree Building phase takes $O(N \\log N)$ time.
"""

if __name__ == "__main__":
    demonstrate_huffman()
    print("\n[SUCCESS] Laboratory: Huffman Coding Completed.")
