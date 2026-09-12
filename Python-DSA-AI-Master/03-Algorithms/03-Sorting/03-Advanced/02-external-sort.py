"""
External Sort Implementation and Analysis.

Learning Objectives:
1. Understand how to sort data that doesn't fit into memory (RAM).
2. Learn the multi-way merge concept.
3. Implement a simplified disk-based external sort.
4. Analyze the IO complexity.

Concept Explanation:
External sorting is used when the data being sorted is too large to fit in the main memory (RAM).
The most common algorithm is the external merge sort. It involves dividing the large file into
smaller chunks that fit in memory, sorting these chunks, writing them back to disk as temporary files,
and finally merging all these temporary sorted files.

Performance Analysis:
- Time Complexity: O(N log N) where N is the total number of elements.
- Space Complexity: O(M) where M is the memory buffer size.
- IO Complexity: Dominated by read/write operations (passes over the data).

Edge Cases:
- Data fits completely in memory.
- File is empty.
- Very small memory limit.

Interview Challenge:
How do you optimize the merge phase in external sort?
Answer: Use a min-heap (priority queue) to efficiently find the minimum element among the K temporary files during the K-way merge.
"""

import os
import tempfile
import heapq
from typing import List, Iterator

def create_dummy_data(filepath: str, size: int) -> None:
    import random
    with open(filepath, 'w') as f:
        for _ in range(size):
            f.write(f"{random.randint(1, 1000)}\n")

def sort_and_write_chunk(chunk: List[int], temp_dir: str, chunk_index: int) -> str:
    """Sorts a chunk in memory and writes it to a temporary file."""
    chunk.sort()
    filename = os.path.join(temp_dir, f"chunk_{chunk_index}.txt")
    with open(filename, 'w') as f:
        for item in chunk:
            f.write(f"{item}\n")
    return filename

def external_sort(input_file: str, output_file: str, chunk_size: int = 100) -> None:
    """Main external sort function."""
    temp_files = []
    with tempfile.TemporaryDirectory() as temp_dir:
        # Phase 1: Divide and sort chunks
        with open(input_file, 'r') as f:
            chunk: List[int] = []
            chunk_idx = 0
            for line in f:
                if line.strip():
                    chunk.append(int(line.strip()))
                if len(chunk) >= chunk_size:
                    temp_file = sort_and_write_chunk(chunk, temp_dir, chunk_idx)
                    temp_files.append(temp_file)
                    chunk = []
                    chunk_idx += 1
            if chunk:
                 temp_file = sort_and_write_chunk(chunk, temp_dir, chunk_idx)
                 temp_files.append(temp_file)

        # Phase 2: Merge chunks using a min-heap
        merge_files(temp_files, output_file)

def merge_files(temp_files: List[str], output_file: str) -> None:
    """Merges sorted temporary files into the output file."""
    file_handles = [open(tf, 'r') for tf in temp_files]
    heap: List[tuple[int, int]] = []
    
    # Initialize heap with the first element of each file
    for i, f in enumerate(file_handles):
        line = f.readline()
        if line:
            heapq.heappush(heap, (int(line.strip()), i))
            
    with open(output_file, 'w') as out:
        while heap:
            val, file_idx = heapq.heappop(heap)
            out.write(f"{val}\n")
            
            # Read next line from the file that gave the minimum element
            next_line = file_handles[file_idx].readline()
            if next_line:
                heapq.heappush(heap, (int(next_line.strip()), file_idx))
                
    for f in file_handles:
        f.close()

def test_external_sort() -> None:
    """Tests for External Sort."""
    input_file = "test_input.txt"
    output_file = "test_output.txt"
    
    create_dummy_data(input_file, 500)
    external_sort(input_file, output_file, chunk_size=50)
    
    # Verify the output is sorted
    with open(output_file, 'r') as f:
        nums = [int(line.strip()) for line in f if line.strip()]
        assert nums == sorted(nums), "Output file is not sorted correctly"
        
    os.remove(input_file)
    os.remove(output_file)
    print("All External Sort tests passed!")

if __name__ == "__main__":
    test_external_sort()
