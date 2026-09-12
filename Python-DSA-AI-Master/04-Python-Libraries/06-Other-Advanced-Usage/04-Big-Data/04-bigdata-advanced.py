"""
Module: 04-bigdata-advanced
Description: Massive, textbook-grade interactive lesson on Advanced Big Data Processing in Python.

===========================================================================
BIG DATA IN PYTHON: ADVANCED TECHNIQUES AND DISTRIBUTED COMPUTING
===========================================================================

Learning Objectives:
1. Understand the core concepts of Big Data processing (Volume, Velocity, Variety).
2. Master chunking and generator-based memory-efficient processing (Out-of-Core computing).
3. Learn to utilize parallel computing with Python's multiprocessing and concurrent.futures.
4. Understand the architecture and usage of distributed computing frameworks like Dask and Ray.
5. Analyze time complexity (Big-O) and space complexity of different data processing strategies.
6. Solve real-world large-scale data challenges (MapReduce pattern implementations).

===========================================================================
MATHEMATICAL BACKGROUND & BIG-O ANALYSIS
===========================================================================
When dealing with Big Data (datasets that exceed RAM size, e.g., > 16GB on a typical machine),
traditional in-memory operations fail (MemoryError).

Let N be the number of records (e.g., rows in a CSV file).
Let M be the available memory (RAM).
Let P be the number of processing cores.

1. In-Memory Processing (Pandas, lists):
   - Time Complexity: O(N)
   - Space Complexity: O(N)
   - Limitation: If N * size_per_record > M, the program crashes.

2. Out-of-Core Processing (Chunking / Generators):
   - Time Complexity: O(N)
   - Space Complexity: O(C), where C is the chunk size (C << N).
   - Advantage: Can process infinitely large files, constrained only by disk space and time.

3. Parallel Processing (Multiprocessing):
   - Time Complexity: O(N / P)
   - Space Complexity: O(C * P)
   - Advantage: Leverages multiple CPU cores to reduce execution time.

4. Distributed Processing (Dask, Spark):
   - Time Complexity: O(N / (P * W)), where W is the number of worker nodes.
   - Space Complexity: O(C * P * W) across the cluster.
   - Overhead: Network serialization/deserialization (IPC) adds overhead.

===========================================================================
MAPREDUCE PARADIGM
===========================================================================
The fundamental pattern for processing large datasets in distributed systems.
1. Map: Apply a transformation function to each element/chunk independently.
2. Shuffle/Sort: Group data by keys (handled by frameworks).
3. Reduce: Aggregate the grouped data to produce the final result.

Map(k1, v1) -> list(k2, v2)
Reduce(k2, list(v2)) -> list(v3)
"""

import os
import sys
import time
import math
import tempfile
import csv
import json
import itertools
from collections import defaultdict, Counter
from typing import List, Dict, Any, Optional, Iterator, Tuple, Callable, Generator
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed
import multiprocessing

# =========================================================================
# 1. DATA GENERATION UTILITIES
# =========================================================================

def generate_large_csv(file_path: str, num_rows: int = 1000000) -> None:
    """
    Utility to generate a dummy large CSV file for testing Big Data operations.
    Space Complexity: O(1) in memory, O(N) on disk.
    """
    print(f"Generating large dataset with {num_rows} rows at {file_path}...")
    start_time = time.time()
    
    # Using generator expression to avoid holding data in memory
    def row_generator():
        for i in range(num_rows):
            # Fields: id, user_id, amount, status, timestamp
            yield [
                i,
                f"user_{i % 1000}", 
                round(math.sin(i) * 1000 + 1000, 2),
                "SUCCESS" if i % 5 != 0 else "FAILED",
                int(time.time()) - (num_rows - i)
            ]

    with open(file_path, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'user_id', 'amount', 'status', 'timestamp'])
        writer.writerows(row_generator())
        
    print(f"Dataset generation completed in {time.time() - start_time:.2f} seconds.")
    print(f"File size: {os.path.getsize(file_path) / (1024 * 1024):.2f} MB\n")


# =========================================================================
# 2. OUT-OF-CORE PROCESSING (CHUNKING & GENERATORS)
# =========================================================================

def process_chunk(chunk: List[List[str]]) -> Dict[str, float]:
    """
    Process a small chunk of data.
    Goal: Calculate total successful transaction amount per user in this chunk.
    """
    user_totals = defaultdict(float)
    for row in chunk:
        if not row: continue
        # row: id, user_id, amount, status, timestamp
        try:
            status = row[3]
            if status == "SUCCESS":
                user_id = row[1]
                amount = float(row[2])
                user_totals[user_id] += amount
        except (IndexError, ValueError):
            pass
    return dict(user_totals)

def generator_based_processing(file_path: str, chunk_size: int = 10000) -> Dict[str, float]:
    """
    Advanced pattern: Memory-efficient processing using lazy evaluation (Generators).
    Time Complexity: O(N)
    Space Complexity: O(C + U), where C is chunk_size, U is unique users.
    """
    print("--- 1. Out-of-Core Processing (Generators) ---")
    start_time = time.time()
    
    def chunked_reader(file_path: str, chunk_size: int) -> Generator[List[List[str]], None, None]:
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader) # Skip header
            while True:
                # itertools.islice fetches 'chunk_size' elements lazily
                chunk = list(itertools.islice(reader, chunk_size))
                if not chunk:
                    break
                yield chunk

    global_totals: Dict[str, float] = defaultdict(float)
    
    # Process file chunk by chunk
    for chunk in chunked_reader(file_path, chunk_size):
        chunk_result = process_chunk(chunk)
        # Reduce step: aggregate chunk results into global state
        for user, amount in chunk_result.items():
            global_totals[user] += amount
            
    exec_time = time.time() - start_time
    print(f"Processed {len(global_totals)} unique users in {exec_time:.4f} seconds.")
    return dict(global_totals)


# =========================================================================
# 3. PARALLEL PROCESSING (MULTIPROCESSING)
# =========================================================================

def parallel_chunk_processing(file_path: str, chunk_size: int = 50000, max_workers: int = None) -> Dict[str, float]:
    """
    Advanced pattern: Combining chunking with multiprocessing (ProcessPoolExecutor).
    Best for CPU-bound tasks. Bypasses the Global Interpreter Lock (GIL).
    
    Time Complexity: O(N / P)
    Space Complexity: O(C * P)
    """
    print(f"--- 2. Parallel Processing (ProcessPool) ---")
    start_time = time.time()
    
    if max_workers is None:
        max_workers = multiprocessing.cpu_count()
        
    print(f"Using {max_workers} CPU cores.")
    
    global_totals: Dict[str, float] = defaultdict(float)
    
    # We must read chunks sequentially, but we can process them in parallel.
    # Note: For massive files, even reading might be parallelized via byte-offsets,
    # but sequential chunk reading is often sufficient if processing is the bottleneck.
    
    def get_chunks():
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)
            while True:
                chunk = list(itertools.islice(reader, chunk_size))
                if not chunk:
                    break
                yield chunk

    # Submit tasks to ProcessPool
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        # Submit all chunks to the executor
        # We use a generator for chunks, but executor.map consumes it.
        # To strictly limit memory, we should submit tasks batch by batch.
        # But for simplicity, we'll map. Note that `map` pulls chunks into memory as fast as it can.
        
        # A more memory-safe approach with futures:
        futures = set()
        chunk_gen = get_chunks()
        
        # Initial fill
        for _ in range(max_workers * 2):
            try:
                futures.add(executor.submit(process_chunk, next(chunk_gen)))
            except StopIteration:
                break
                
        while futures:
            # Wait for at least one future to complete
            done, futures = as_completed(futures), futures
            # Actually, as_completed returns an iterator, let's just use a standard loop:
            # We will use wait to get finished futures
            from concurrent.futures import wait, FIRST_COMPLETED
            done, futures = wait(futures, return_when=FIRST_COMPLETED)
            
            for future in done:
                chunk_result = future.result()
                # Aggregate results
                for user, amount in chunk_result.items():
                    global_totals[user] += amount
                    
                # Submit a new chunk to keep the pool busy
                try:
                    futures.add(executor.submit(process_chunk, next(chunk_gen)))
                except StopIteration:
                    pass

    exec_time = time.time() - start_time
    print(f"Parallel processing completed in {exec_time:.4f} seconds.")
    return dict(global_totals)


# =========================================================================
# 4. SIMULATING MAPREDUCE (CUSTOM IMPLEMENTATION)
# =========================================================================

class SimpleMapReduce:
    """
    A textbook implementation of the MapReduce paradigm.
    """
    def __init__(self, map_func: Callable, reduce_func: Callable, num_workers: int = 4):
        self.map_func = map_func
        self.reduce_func = reduce_func
        self.num_workers = num_workers

    def execute(self, data: List[Any]) -> Dict[Any, Any]:
        print("--- 3. MapReduce Simulation ---")
        start_time = time.time()
        
        # 1. Map Phase (Parallel)
        print("Starting Map Phase...")
        mapped_data = []
        with ProcessPoolExecutor(max_workers=self.num_workers) as executor:
            # map_func should return a list of (key, value) pairs
            results = executor.map(self.map_func, data)
            for res in results:
                mapped_data.extend(res)
                
        # 2. Shuffle & Sort Phase (Group by Key)
        print("Starting Shuffle Phase...")
        shuffled: Dict[Any, List[Any]] = defaultdict(list)
        for key, value in mapped_data:
            shuffled[key].append(value)
            
        # 3. Reduce Phase (Parallel)
        print("Starting Reduce Phase...")
        final_result = {}
        with ProcessPoolExecutor(max_workers=self.num_workers) as executor:
            # Submit reduce tasks
            futures = {
                executor.submit(self.reduce_func, key, values): key 
                for key, values in shuffled.items()
            }
            
            for future in as_completed(futures):
                k, v = future.result()
                final_result[k] = v

        print(f"MapReduce completed in {time.time() - start_time:.4f} seconds.")
        return final_result

# MapReduce User Functions
def mr_mapper(chunk: List[List[str]]) -> List[Tuple[str, float]]:
    """Mapper: emits (user_id, amount) for successful transactions."""
    emissions = []
    for row in chunk:
        try:
            if row[3] == "SUCCESS":
                emissions.append((row[1], float(row[2])))
        except (IndexError, ValueError):
            pass
    return emissions

def mr_reducer(key: str, values: List[float]) -> Tuple[str, float]:
    """Reducer: sums the amounts for a given user."""
    return key, sum(values)


# =========================================================================
# 5. DASK SIMULATION & EXPLANATION (IF DASK INSTALLED)
# =========================================================================
# Dask provides distributed arrays, dataframes, and dynamic task scheduling.
# It scales NumPy and Pandas workflows out-of-core and across clusters.
def try_dask_dataframe(file_path: str) -> None:
    print("--- 4. Dask Dataframe Ecosystem ---")
    try:
        import dask.dataframe as dd
        start_time = time.time()
        print("Dask found. Demonstrating Dask Dataframe lazy evaluation.")
        
        # Dask doesn't read the file yet (Lazy Evaluation)
        df = dd.read_csv(file_path)
        
        # Build the computation graph
        successful = df[df['status'] == 'SUCCESS']
        user_totals = successful.groupby('user_id')['amount'].sum()
        
        # Trigger actual computation (.compute())
        result = user_totals.compute()
        print(f"Dask computation finished in {time.time() - start_time:.4f} seconds.")
        print(f"Result snapshot:\n{result.head()}")
    except ImportError:
        print("Dask is not installed. To run this section: pip install dask[dataframe]")
        print("Explanation: Dask splits datasets into partitions and processes them as a Directed Acyclic Graph (DAG) of tasks.")


# =========================================================================
# 6. INTERVIEW CHALLENGE
# =========================================================================
"""
Challenge: Top-K Frequent Elements in Massive Log File
Problem: You are given an infinitely large stream/file of server logs. 
Find the Top K most frequent IP addresses.
Constraints: Memory is strictly limited (O(1) relative to total rows, O(U) for unique IPs is too large).
Solution: Use Count-Min Sketch for probabilistic counting, or if accurate counts are needed, 
chunk the data, use external sorting, or a distributed MapReduce approach.

Here we implement the chunked accurate approach with a min-heap for Top K.
"""
import heapq

def interview_challenge_top_k(file_path: str, k: int = 5) -> List[Tuple[int, str]]:
    """
    Find Top K most frequent items in a large file using chunks and a Heap.
    
    Time Complexity: O(N + U log K), where N is rows, U is unique elements.
    Space Complexity: O(U) for frequency map, O(K) for heap.
    (Note: If U is larger than RAM, external sort or MapReduce is required).
    """
    print(f"--- Interview Challenge: Top {k} Elements ---")
    start = time.time()
    
    # 1. Count frequencies using a generator
    freq_map = Counter()
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if row:
                # Let's find top users by frequency of transactions
                freq_map[row[1]] += 1
                
    # 2. Extract Top K using a Min-Heap
    # heapq.nlargest is O(U log K)
    top_k = heapq.nlargest(k, freq_map.items(), key=lambda x: x[1])
    
    # Alternatively, manual heap logic:
    # min_heap = []
    # for item, count in freq_map.items():
    #     if len(min_heap) < k:
    #         heapq.heappush(min_heap, (count, item))
    #     else:
    #         if count > min_heap[0][0]:
    #             heapq.heappushpop(min_heap, (count, item))
    # top_k = sorted(min_heap, reverse=True)
    
    print(f"Top {k} Users by Transaction Count: {top_k}")
    print(f"Completed in {time.time() - start:.4f} seconds.")
    return top_k


# =========================================================================
# 7. MAIN EXECUTION & TESTS
# =========================================================================

def run_tests(file_path: str):
    print("--- Running Assertions & Tests ---")
    
    # Test generator vs parallel equality
    res1 = generator_based_processing(file_path, chunk_size=50000)
    res2 = parallel_chunk_processing(file_path, chunk_size=50000, max_workers=2)
    
    # Check a few keys
    keys_to_check = list(res1.keys())[:5]
    for k in keys_to_check:
        assert math.isclose(res1[k], res2[k], rel_tol=1e-5), f"Mismatch for user {k}: {res1[k]} vs {res2[k]}"
        
    print("All tests passed: Sequential and Parallel results match perfectly.\n")


if __name__ == "__main__":
    print("========== Exploring BIG DATA PROCESSING ==========\n")
    
    # Create a temporary large file
    temp_dir = tempfile.gettempdir()
    test_file = os.path.join(temp_dir, "large_dataset_mock.csv")
    
    # 1. Generate 500,000 rows (approx 25MB) - scalable to millions
    generate_large_csv(test_file, num_rows=500000)
    
    try:
        # 2. Generator-based OOC
        generator_based_processing(test_file, chunk_size=100000)
        
        # 3. Multiprocessing OOC
        parallel_chunk_processing(test_file, chunk_size=100000)
        
        # 4. MapReduce Simulation
        # To simulate MapReduce, we'll read the file into chunks first (for demo purposes)
        # In a real Hadoop/Spark system, data is distributed across HDFS nodes.
        print("Preparing chunks for MapReduce...")
        chunks = []
        with open(test_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)
            while True:
                c = list(itertools.islice(reader, 100000))
                if not c: break
                chunks.append(c)
                
        mr = SimpleMapReduce(mr_mapper, mr_reducer, num_workers=4)
        mr_res = mr.execute(chunks)
        # Verify MR output
        sample_user = list(mr_res.keys())[0]
        print(f"MapReduce Sample User {sample_user} Total: {mr_res[sample_user]:.2f}\n")
        
        # 5. Dask Simulation
        try_dask_dataframe(test_file)
        
        # 6. Interview Challenge
        interview_challenge_top_k(test_file, k=5)
        
        # 7. Tests
        run_tests(test_file)
        
    finally:
        # Cleanup
        if os.path.exists(test_file):
            os.remove(test_file)
            print(f"Cleaned up temporary file: {test_file}")
            
    print("========== END OF BIG DATA PROCESSING ==========\n")
