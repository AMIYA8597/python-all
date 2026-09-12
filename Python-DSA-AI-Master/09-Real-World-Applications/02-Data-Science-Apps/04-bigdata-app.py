"""
Module: Big Data Processing Applications

Learning Objectives:
1. Understand the MapReduce paradigm and how it applies to Big Data processing.
2. Implement memory-efficient data processing using generators and chunking.
3. Utilize parallel processing (multiprocessing) to speed up computations.
4. Handle datasets that are significantly larger than available RAM.

Concept Explanation:
In Big Data, datasets often exceed the capacity of a single machine's RAM. 
Trying to load a 50GB CSV file into memory using standard techniques will crash the application.
Instead, data scientists use strategies like Chunking (reading data in small, manageable pieces) 
and parallel processing (MapReduce). The MapReduce paradigm splits processing into two phases:
- Map: Apply a function to independent chunks of data concurrently.
- Reduce: Combine the results from the Map phase into a final aggregated output.

===========================================================================
Basic Implementation
===========================================================================
The basic approach attempts to load everything into memory and process sequentially.
This is prone to MemoryError and is highly inefficient for large datasets.
"""

import os
from typing import Iterator, List, Dict, Any, Callable, TypeVar, Generic
from collections import defaultdict
import multiprocessing

T = TypeVar('T')
U = TypeVar('U')
V = TypeVar('V')

# ---------------------------------------------------------------------------
# Basic Approach
# ---------------------------------------------------------------------------
def process_large_data_basic(file_path: str) -> Dict[str, int]:
    """
    Basic processing: Reads the entire file into memory at once.
    Counts the occurrences of words. Will crash if the file is larger than RAM.
    """
    try:
        with open(file_path, 'r') as f:
            content = f.read()  # DANGER: Loads entire file into RAM
            
        word_counts: Dict[str, int] = defaultdict(int)
        for word in content.split():
            word_counts[word.lower()] += 1
        return dict(word_counts)
    except FileNotFoundError:
        return {}


# ===========================================================================
# Professional Implementation
# ===========================================================================

class BigDataProcessor:
    """
    Professional implementation using Generators for chunking and 
    Multiprocessing for a localized MapReduce simulation.
    """
    
    @staticmethod
    def read_in_chunks(file_path: str, chunk_size: int = 1024 * 1024) -> Iterator[str]:
        """
        Generator that reads a file piece by piece (chunk_size bytes).
        Ensures constant memory usage regardless of file size.
        """
        with open(file_path, 'r') as f:
            while True:
                data = f.read(chunk_size)
                if not data:
                    break
                yield data
                
    @staticmethod
    def _map_word_count(chunk: str) -> Dict[str, int]:
        """
        The MAP function: Processes a single chunk of text and returns a local count.
        """
        local_counts: Dict[str, int] = defaultdict(int)
        for word in chunk.split():
            # Stripping punctuation would go here in a production app
            local_counts[word.lower()] += 1
        return dict(local_counts)

    @classmethod
    def process_map_reduce(cls, file_path: str, chunk_size: int = 1024 * 1024, num_workers: int = 4) -> Dict[str, int]:
        """
        The complete MapReduce pipeline:
        1. Reads data in chunks using a generator (Memory Efficient)
        2. Distributes the mapping function across multiple CPU cores (Time Efficient)
        3. Reduces (merges) the results back into a single dictionary.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File {file_path} not found.")

        # 1 & 2. Map Phase
        chunks = cls.read_in_chunks(file_path, chunk_size)
        
        # Using a Process Pool to execute _map_word_count concurrently
        with multiprocessing.Pool(processes=num_workers) as pool:
            # imap yields results as soon as they are ready, keeping memory low
            map_results = pool.imap_unordered(cls._map_word_count, chunks)
            
            # 3. Reduce Phase
            final_counts: Dict[str, int] = defaultdict(int)
            for local_result in map_results:
                for word, count in local_result.items():
                    final_counts[word] += count
                    
        return dict(final_counts)


# ===========================================================================
# Complexity Analysis & Interview Challenge
# ===========================================================================
"""
Complexity Analysis:
- process_large_data_basic:
  Time Complexity: O(N) where N is the number of characters in the file.
  Space Complexity: O(N) since the entire file is loaded into memory as a string, 
                    plus the dictionary space.

- BigDataProcessor.process_map_reduce:
  Time Complexity: O(N / W) where W is the number of worker processes. Actual time 
                   is bounded by disk I/O and inter-process communication overhead.
  Space Complexity: O(C + U) where C is the chunk size and U is the number of 
                    unique words. The memory usage is strictly bounded and will not 
                    grow with the file size N.

Interview Challenge:
Question: You are given a log file that is 500GB in size. You need to find the top 10 
          most frequent IP addresses. You have 8GB of RAM. How do you design this?
Answer:
1. Chunking: Read the file line by line (or in fixed byte chunks) using a generator.
2. Mapping: Parse each line to extract the IP address and keep a local count in memory 
   (using a dictionary). Since there are at most ~4.3 billion IPv4 addresses, and in practice 
   much fewer, the dictionary might fit in memory.
3. If the dictionary exceeds memory, use External Sorting or write intermediate key-value 
   pairs to disk in partitioned files (e.g., hash(IP) % 100), then process each partition 
   sequentially to find the top IPs per partition, and finally merge them.
"""

# ===========================================================================
# Example Usage & Tests
# ===========================================================================
if __name__ == "__main__":
    print("Testing Big Data Processing Pipeline...")
    
    # Create a dummy large-ish file for testing
    test_file = "dummy_big_data.txt"
    with open(test_file, "w") as f:
        # Write enough data to create multiple chunks
        for _ in range(100):
            f.write("apple banana orange apple grape\n")
            f.write("banana apple orange kiwi\n")
    
    try:
        # Test Basic
        basic_counts = process_large_data_basic(test_file)
        assert basic_counts['apple'] == 200
        assert basic_counts['banana'] == 200
        assert basic_counts['kiwi'] == 100
        
        # Test Professional MapReduce Pipeline
        # Use a very small chunk size to force multiple chunks for the test
        processor = BigDataProcessor()
        pro_counts = processor.process_map_reduce(test_file, chunk_size=128, num_workers=2)
        
        assert pro_counts['apple'] == 200
        assert pro_counts['banana'] == 200
        assert pro_counts['kiwi'] == 100
        assert basic_counts == pro_counts
        print("All tests passed successfully!")
        
    finally:
        # Cleanup
        if os.path.exists(test_file):
            os.remove(test_file)
