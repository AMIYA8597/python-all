import heapq
from collections import Counter
from typing import Dict, Optional


class HuffmanNode:
    """
    Represents a node in the Huffman Tree.
    """
    def __init__(self, char: Optional[str], freq: int):
        self.char = char
        self.freq = freq
        self.left: Optional['HuffmanNode'] = None
        self.right: Optional['HuffmanNode'] = None

    # Define comparison operators for the min-heap to order by frequency
    def __lt__(self, other: 'HuffmanNode') -> bool:
        return self.freq < other.freq

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, HuffmanNode):
            return NotImplemented
        return self.freq == other.freq


class HuffmanCoding:
    """
    A professional implementation of the Huffman Coding compression algorithm.
    """
    def __init__(self, text: str):
        if not text:
            raise ValueError("Input text cannot be empty.")
        self.text = text
        self.heap: list[HuffmanNode] = []
        self.codes: Dict[str, str] = {}
        self.reverse_mapping: Dict[str, str] = {}
        self.root: Optional[HuffmanNode] = None

    def _build_frequency_dict(self) -> Dict[str, int]:
        """Calculates frequency of each character."""
        return dict(Counter(self.text))

    def _build_heap(self, frequency: Dict[str, int]) -> None:
        """Constructs a priority queue (min-heap) from frequencies."""
        for char, freq in frequency.items():
            node = HuffmanNode(char, freq)
            heapq.heappush(self.heap, node)

    def _build_tree(self) -> None:
        """Builds the Huffman tree by merging lowest frequency nodes."""
        while len(self.heap) > 1:
            node1 = heapq.heappop(self.heap)
            node2 = heapq.heappop(self.heap)

            # Internal node has no character
            merged = HuffmanNode(None, node1.freq + node2.freq)
            merged.left = node1
            merged.right = node2

            heapq.heappush(self.heap, merged)

        if self.heap:
            self.root = heapq.heappop(self.heap)

    def _generate_codes_recursive(self, root: Optional[HuffmanNode], current_code: str) -> None:
        """Recursively traverses the tree to assign binary codes to leaves."""
        if root is None:
            return

        if root.char is not None:
            self.codes[root.char] = current_code
            self.reverse_mapping[current_code] = root.char
            return

        self._generate_codes_recursive(root.left, current_code + "0")
        self._generate_codes_recursive(root.right, current_code + "1")

    def _build_codes(self) -> None:
        """Wrapper to initiate code generation."""
        # Edge case: if there's only one unique character
        if self.root and self.root.char is not None:
            self.codes[self.root.char] = "0"
            self.reverse_mapping["0"] = self.root.char
            return
            
        self._generate_codes_recursive(self.root, "")

    def compress(self) -> str:
        """
        Compresses the text into a binary string representation.
        
        Returns:
            str: String of 0s and 1s representing compressed data.
        """
        frequency = self._build_frequency_dict()
        self._build_heap(frequency)
        self._build_tree()
        self._build_codes()

        encoded_text = "".join([self.codes[char] for char in self.text])
        return encoded_text

    def decompress(self, encoded_text: str) -> str:
        """
        Decompresses the binary string back to original text.
        
        Args:
            encoded_text: String of 0s and 1s.
            
        Returns:
            str: Original text.
        """
        current_code = ""
        decoded_text = ""

        for bit in encoded_text:
            current_code += bit
            if current_code in self.reverse_mapping:
                decoded_text += self.reverse_mapping[current_code]
                current_code = ""

        return decoded_text


# ==========================================
# Testing & Execution
# ==========================================
if __name__ == "__main__":
    import sys

    sample_text = "this is an example for huffman encoding"
    print(f"Original Text: '{sample_text}'")
    print(f"Original Size (approx): {len(sample_text) * 8} bits")

    huffman = HuffmanCoding(sample_text)
    
    # 1. Compress
    compressed_text = huffman.compress()
    print(f"\nCompressed Binary String: {compressed_text}")
    print(f"Compressed Size: {len(compressed_text)} bits")
    
    # 2. Dictionary / Mapping
    print("\nHuffman Codes Dictionary:")
    for char, code in huffman.codes.items():
        print(f" '{char}': {code}")

    # 3. Decompress
    decompressed_text = huffman.decompress(compressed_text)
    print(f"\nDecompressed Text: '{decompressed_text}'")

    # Verification
    assert sample_text == decompressed_text, "Decompression failed! Output does not match original."
    print("\n✅ Compression and Decompression successful.")

    compression_ratio = len(compressed_text) / (len(sample_text) * 8)
    print(f"Compression Ratio: {compression_ratio:.2%}")
