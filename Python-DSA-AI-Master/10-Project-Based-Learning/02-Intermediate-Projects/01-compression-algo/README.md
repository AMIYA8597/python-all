# Text Compression Algorithm (Huffman Coding)

## Project Overview
This project implements a text compression algorithm using Huffman Coding, a popular lossless data compression technique. It serves as a practical application of Data Structures and Algorithms (DSA) concepts such as Priority Queues (Min-Heaps) and Binary Trees.

## Industry Use Cases
- **File Compression Utilities:** Tools like ZIP, GZIP, and RAR use Huffman coding as part of their compression pipelines (often combined with LZ77/LZ78 algorithms like in Deflate).
- **Multimedia Compression:** Used in JPEG image compression and MP3 audio compression to encode quantized values efficiently.
- **Network Transmission:** Reducing payload size for faster transmission over bandwidth-constrained networks.

## Beginner Explanation
Imagine you have a text file containing mostly the letter 'e' and very few 'z's. In standard encoding (like ASCII), every character takes up 8 bits, regardless of how often it appears. 
Huffman coding is a smart way to assign shorter binary codes to characters that appear frequently, and longer codes to characters that appear rarely. By doing this, the overall size of the file shrinks significantly.

## Technical Explanation (Deep Dive)
Huffman coding is a variable-length prefix coding algorithm. 
1. **Frequency Analysis:** Calculate the frequency of each character in the input data.
2. **Build a Min-Heap:** Create a leaf node for each unique character and insert them into a min-heap based on their frequencies.
3. **Build the Huffman Tree:** Repeatedly extract the two nodes with the lowest frequencies from the heap. Create a new internal node with a frequency equal to the sum of the two nodes' frequencies. Make the two extracted nodes the left and right children of this new node. Insert the new node back into the heap. Repeat until only one node remains in the heap (the root of the Huffman tree).
4. **Generate Prefix Codes:** Traverse the Huffman tree from the root to the leaves. Assign '0' for every left branch taken and '1' for every right branch. The path to a leaf determines the binary code for that character. Since no character is an internal node, no code is a prefix of another (Prefix Rule).
5. **Encoding/Decoding:** Replace characters with their codes to compress. To decompress, read the binary stream and traverse the tree from the root down for each bit until a leaf is reached, output the character, and return to the root.

## Realistic Interview Questions
1. **Why do we use a Min-Heap to build the Huffman Tree?** 
   *Answer:* A min-heap allows us to efficiently extract the two lowest-frequency nodes in $O(\log N)$ time, making the overall tree construction $O(N \log N)$.
2. **What is the Prefix Rule, and why is it essential?**
   *Answer:* The prefix rule states that no code can be a prefix of another code. This ensures that the encoded binary string can be uniquely and unambiguously decoded without needing special delimiter characters.
3. **Can Huffman coding be used on binary files like images or executables?**
   *Answer:* Yes, Huffman coding works on any stream of symbols (e.g., bytes). However, if the symbol frequencies are roughly uniform (high entropy), the compression ratio will be very low or non-existent.

## Practical Exercises
- Modify the algorithm to write the compressed binary string and the serialized Huffman tree dictionary to an actual file on disk.
- Implement a decompression function that reads the file back and reconstructs the original string.
- Compare the compression ratio of this algorithm against Python's built-in `zlib` module.
