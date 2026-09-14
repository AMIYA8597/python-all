"""
# ==============================================================================
# LABORATORY: PROJECT-BASED LEARNING (HUFFMAN COMPRESSION)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A junior developer needs to store a 1,000,000-character DNA sequence consisting 
# only of 'A', 'C', 'T', 'G'. They use a standard ASCII Text File. ASCII 
# mathematically forces every single character to consume exactly 8 bits (1 Byte). 
# The file size is 1.0 Megabytes.
#
# A senior software architect understands "Information Theory" and "Huffman Coding". 
# They realize that if there are only 4 possible characters in the entire file, 
# it mathematically only requires 2 bits to uniquely identify them (00, 01, 10, 11). 
# They build a custom Huffman Tree, compress the DNA sequence down to 2 bits per 
# character, and the file size violently collapses to 250 Kilobytes—a flawless 
# 75% reduction without losing a single drop of data (Lossless Compression).
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master the mathematics of Lossless Data Compression.
# - Execute a dynamic Priority Queue (Min-Heap) to construct an Abstract Syntax Tree.
# - Execute Binary Tree Traversal to generate optimal Bit Prefixes.
#
# ==============================================================================
"""

import heapq
from collections import Counter
from typing import Dict, Optional

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE TREE NODE ARCHITECTURE
# ==============================================================================
class HuffmanNode:
    """
    A mathematical structural node for the Huffman Tree.
    We must implement `__lt__` (Less Than) so the Python `heapq` module knows 
    how to mathematically sort the nodes based on their Frequency!
    """
    def __init__(self, char: Optional[str], freq: int):
        self.char = char
        self.freq = freq
        self.left: Optional['HuffmanNode'] = None
        self.right: Optional['HuffmanNode'] = None

    def __lt__(self, other: 'HuffmanNode') -> bool:
        # The Min-Heap will ALWAYS put the lowest frequency nodes at the top!
        return self.freq < other.freq


# ==============================================================================
# 4. THE COMPRESSION ENGINE
# ==============================================================================
class HuffmanCompressor:
    def __init__(self):
        self.encoding_map: Dict[str, str] = {}
        self.decoding_map: Dict[str, str] = {}

    def _build_huffman_tree(self, text: str) -> HuffmanNode:
        """
        Mathematically constructs the optimal Binary Tree.
        The most frequent characters will be placed at the very top of the tree 
        (requiring the fewest bits). The rarest characters will be buried deep 
        at the bottom (requiring the most bits).
        """
        # 1. Mathematically count the frequency of every character O(N)
        frequencies = Counter(text)
        
        # 2. Push every character into a Min-Heap O(N log N)
        priority_queue = [HuffmanNode(char, freq) for char, freq in frequencies.items()]
        heapq.heapify(priority_queue)

        # 3. The Core Algorithm! 
        # We continually pop the two lowest frequency nodes, fuse them together 
        # into a new parent node, and push the parent back into the heap!
        while len(priority_queue) > 1:
            left_node = heapq.heappop(priority_queue)
            right_node = heapq.heappop(priority_queue)

            # The parent has NO character payload, its frequency is the sum of its children!
            merged_parent = HuffmanNode(None, left_node.freq + right_node.freq)
            merged_parent.left = left_node
            merged_parent.right = right_node

            heapq.heappush(priority_queue, merged_parent)

        # The final node remaining in the heap is the absolute Root of the Tree!
        return heapq.heappop(priority_queue)

    def _generate_bit_codes(self, node: Optional[HuffmanNode], current_bits: str):
        """
        A Recursive Depth-First Search (DFS) that walks the tree.
        Every time we go LEFT, we mathematically append a '0'.
        Every time we go RIGHT, we mathematically append a '1'.
        """
        if node is None:
            return

        # If we hit a Leaf Node (it has a character payload), we lock in the Bit Code!
        if node.char is not None:
            self.encoding_map[node.char] = current_bits
            self.decoding_map[current_bits] = node.char
            return

        self._generate_bit_codes(node.left, current_bits + "0")
        self._generate_bit_codes(node.right, current_bits + "1")

    def compress(self, text: str) -> str:
        """Executes the full mathematical compression."""
        if not text:
            return ""

        # 1. Build the Tree
        root = self._build_huffman_tree(text)
        
        # 2. Traverse the Tree to generate the '01001' bit mappings
        self.encoding_map.clear()
        self.decoding_map.clear()
        self._generate_bit_codes(root, "")

        # 3. Mathematically swap the ASCII characters for the new compressed bits!
        compressed_bits = "".join([self.encoding_map[char] for char in text])
        return compressed_bits

    def decompress(self, compressed_bits: str) -> str:
        """
        Executes the exact mathematical reverse.
        Because Huffman Codes are "Prefix-Free", it is mathematically impossible 
        to misinterpret where one character ends and the next begins!
        """
        current_bit_sequence = ""
        decompressed_text = ""

        for bit in compressed_bits:
            current_bit_sequence += bit
            # The millisecond we find a valid match in our dictionary, we lock it in!
            if current_bit_sequence in self.decoding_map:
                decompressed_text += self.decoding_map[current_bit_sequence]
                current_bit_sequence = "" # Reset for the next character!

        return decompressed_text


# ==============================================================================
# 5. MATHEMATICAL PROOF (THE SIMULATION)
# ==============================================================================
def demonstrate_compression():
    section_header("Project: Huffman Lossless Compression")
    
    compressor = HuffmanCompressor()
    
    # We create a string heavily skewed towards the letter 'E'.
    # A standard ASCII file forces 'E' to consume 8 bits, just like 'Z'.
    raw_text = "E" * 15 + "A" * 7 + "B" * 6 + "C" * 2 + "D" * 1
    
    print("  [PHASE 1: THE RAW DATA]")
    print(f"    -> Payload: {raw_text}")
    print(f"    -> ASCII Mathematical Size: {len(raw_text) * 8} Bits (8 bits per char)")
    
    # We mathematically compress it!
    compressed_bits = compressor.compress(raw_text)
    
    print("\n  [PHASE 2: THE HUFFMAN DICTIONARY]")
    for char, bits in compressor.encoding_map.items():
        print(f"    -> Char '{char}' mapped to: {bits} (Length: {len(bits)} bits)")
        
    print("\n  [PHASE 3: THE COMPRESSION PROOF]")
    print(f"    -> Binary Output: {compressed_bits}")
    print(f"    -> Huffman Mathematical Size: {len(compressed_bits)} Bits")
    
    reduction = 100 - ((len(compressed_bits) / (len(raw_text) * 8)) * 100)
    print(f"    -> [SUCCESS] Payload size violently reduced by {reduction:.1f}%!")
    
    print("\n  [PHASE 4: THE DECOMPRESSION PROOF]")
    recovered_text = compressor.decompress(compressed_bits)
    
    if recovered_text == raw_text:
        print("    -> [FLAWLESS] The decompressed text perfectly matches the original payload.")
        print("    -> Zero data loss occurred during the mathematical translation.")


def run_all_labs():
    demonstrate_compression()


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "Why does the Huffman algorithm mathematically guarantee that the most frequent characters get the shortest bit codes?"
   Senior Answer: "The algorithm uses a Min-Heap. The Min-Heap mathematically forces the lowest frequency characters to be popped first. Because they are popped first, they are pushed to the very bottom of the Binary Tree. Every time you go down a level in the tree, you add another bit to the character's code (e.g., $101101$). The most frequent characters (like the letter 'E' in English) have massive mathematical frequencies. They remain sitting in the Min-Heap until the very end, meaning they are placed at the absolute top of the tree, directly beneath the Root. They only require $1$ or $2$ bits (e.g., $0$ or $11$) to traverse, maximizing the overall compression of the file."

2. Interviewer: "What is a 'Prefix-Free Code', and why is it mathematically mandatory for decompression to work without commas or spaces?"
   Senior Answer: "If 'A' is mapped to $1$ and 'B' is mapped to $10$, the system is mathematically broken. If the decompressor reads a $1$, it doesn't know if it should instantly output 'A', or wait to see if the next bit is a $0$ to output 'B'. This ambiguity destroys the file. A 'Prefix-Free Code' is a mathematical guarantee that no complete bit code is a prefix of any other bit code. Because Huffman Codes are generated by traversing to the absolute dead-end Leaf Nodes of a Binary Tree, it is physically impossible for a shorter path to overlap a longer path. This allows the decompressor to read a continuous stream of bits ($101100010$) and instantly lock in the characters the exact millisecond it hits a leaf node, requiring absolutely zero separator characters."

3. Interviewer: "If Huffman Compression is so mathematically flawless, why don't we run ZIP compression algorithms on JPEG or MP4 files to make them even smaller?"
   Senior Answer: "The Entropy Limit (Shannon's Source Coding Theorem). Huffman Compression relies on finding massive mathematical redundancies (e.g., the letter 'E' appearing $15$ times). JPEG and MP4 files are already aggressively mathematically compressed. The algorithms that created them (like Discrete Cosine Transforms) have already annihilated all the redundancies, leaving behind pure, high-entropy mathematical noise. If you run a ZIP algorithm on high-entropy data, there are no patterns left for the Huffman Tree to exploit. The tree overhead will actually make the file slightly LARGER. Lossless compression mathematically cannot compress random noise."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Capstone Project (Huffman Compression) Completed.")
