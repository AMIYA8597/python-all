"""
# ==============================================================================
# LABORATORY: EXTERNAL SORTING (SYSTEM DESIGN / K-WAY MERGE)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A classic Senior System Design interview question: 
# "You have a 100 Gigabyte log file of IP addresses. Your server only has 
# 2 Gigabytes of RAM. Write an algorithm to sort this file."
#
# You CANNOT use standard Quick Sort or Merge Sort. They require the entire 
# dataset to be loaded into RAM at once. If you try, the OS will trigger an 
# Out Of Memory (OOM) kill.
#
# You must use "External Sorting". The hard drive acts as the primary memory, 
# and RAM is just used as a small computational buffer.
# 
# How it works:
# 1. SPLIT PHASE: Read 2GB of data from the massive file into RAM.
# 2. Sort that 2GB chunk natively in RAM using Quick Sort / Timsort.
# 3. Write that sorted 2GB chunk back to the hard drive as a temporary file.
# 4. Repeat 50 times until you have 50 small, perfectly sorted temporary files.
# 5. MERGE PHASE: Open all 50 files simultaneously. Use a Min-Heap (Priority Queue) 
#    to read the very first (smallest) line from all 50 files. 
#    Continuously pop the absolute minimum from the Heap and write it to the 
#    Final Output file, reading the next line from whichever temp file won.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master K-Way Merging using a Min-Heap.
# - Understand disk I/O constraints vs RAM constraints.
# - Implement a conceptual mock of External Sorting.
#
# ==============================================================================
"""

import heapq
import os
from typing import List, Iterator

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. K-WAY MERGE IMPLEMENTATION
# ==============================================================================
def k_way_merge(sorted_streams: List[Iterator[int]]) -> List[int]:
    """
    Takes a list of multiple sorted data streams (representing files on a hard drive) 
    and merges them into a single continuous sorted stream using a Min-Heap.
    
    Time Complexity: O(N log K), where N is total items and K is number of files.
    Space Complexity: O(K) for the Min-Heap. Extremely memory efficient!
    """
    min_heap = []
    
    # 1. INITIALIZATION
    # Read exactly ONE element from every single file, and push it into the heap.
    # The heap stores a tuple: (value, stream_id) so we know which file to read from next!
    for stream_id, stream in enumerate(sorted_streams):
        try:
            first_val = next(stream)
            heapq.heappush(min_heap, (first_val, stream_id))
        except StopIteration:
            # This file is completely empty, skip it.
            pass
            
    final_sorted_output = []
    
    # 2. CONTINUOUS MERGE
    while min_heap:
        # Pop the absolute smallest value across all files
        val, stream_id = heapq.heappop(min_heap)
        
        # Write it to our final output (In reality, this writes to a file on disk)
        final_sorted_output.append(val)
        
        # We just pulled a value from `stream_id`.
        # We must replace it by reading the NEXT line from that exact same file!
        try:
            next_val = next(sorted_streams[stream_id])
            heapq.heappush(min_heap, (next_val, stream_id))
        except StopIteration:
            # That file has reached EOF (End Of File). We don't push anything back.
            pass
            
    return final_sorted_output


def demonstrate_external_sort():
    section_header("Algorithm: External Sort (K-Way Merge)")
    
    # Imagine these are 3 massive files on your hard drive.
    # They have already been individually sorted during the "Split Phase".
    # We are simulating opening them as streaming Generators (Iterators).
    file_1 = iter([10, 20, 30, 40, 50])
    file_2 = iter([5, 15, 25, 35, 45])
    file_3 = iter([1, 2, 3, 90, 100])
    
    streams = [file_1, file_2, file_3]
    
    print("Files 1, 2, and 3 are on the hard drive and perfectly sorted individually.")
    print("RAM limit is strictly 3 items (The Min-Heap size).\n")
    
    print("Executing K-Way Merge...")
    final_output = k_way_merge(streams)
    
    print(f"\nFinal Merged Output (Written to Disk):")
    print(final_output)
    
    print("\nNotice we perfectly sorted 15 elements, but our RAM (the Min-Heap) NEVER")
    print("held more than exactly 3 elements at any given time!")


# ==============================================================================
# 4. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why do we use a Min-Heap for the K-Way Merge instead of just scanning the 50 files manually every loop?
   Answer: If you have 50 temporary files, manually scanning the top of all 50 files to find the minimum takes $O(K)$ time per element. Doing this for $N$ total elements takes $O(N \\times K)$ time, which is incredibly slow. A Min-Heap extracts the minimum and inserts the new element in $O(\\log K)$ time. The total time drops drastically to $O(N \\log K)$.

2. What is the bottleneck of External Sorting?
   Answer: Disk I/O (Input/Output). Reading and writing from a physical Hard Drive (HDD) or Solid State Drive (SSD) is thousands of times slower than reading from RAM. To optimize this, you don't actually write element by element. You read/write massive 100MB "Blocks" into a RAM buffer, and flush to disk only when the buffer is full.

3. Does MapReduce use External Sorting?
   Answer: Yes! In distributed systems like Hadoop or Spark, the "Shuffle and Sort" phase between the Map and Reduce steps relies heavily on External Sorting. Massive distributed nodes write their sorted chunks to disk, and the Reducer nodes pull them across the network and perform a K-Way Merge to aggregate the final data.
"""

if __name__ == "__main__":
    demonstrate_external_sort()
    print("\n[SUCCESS] Laboratory: External Sort Completed.")
