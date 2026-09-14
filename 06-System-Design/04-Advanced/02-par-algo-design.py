"""
# ==============================================================================
# LABORATORY: SYSTEM DESIGN (PARALLEL ALGORITHM DESIGN)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You work at Google. You need to count the frequency of every word across 
# 10 Billion web pages. 
#
# Doing this sequentially on a single computer will take 10 years.
# So, you buy 1,000 servers to run the algorithm in parallel. 
# But wait... does that mean the job will finish 1,000x faster?
# 
# According to Amdahl's Law, the answer is mathematically NO. 
# If even 5% of your algorithm requires sequential execution (e.g., merging the 
# final results together), the absolute maximum theoretical speedup you can 
# EVER achieve, even with an INFINITE number of servers, is strictly 20x.
#
# To bypass this, you must completely redesign the algorithm from the ground up 
# using the "MapReduce" architecture. 
# MapReduce forces you to write code in two isolated phases:
# 1. MAP: Completely independent chunks of work (100% parallelizable).
# 2. REDUCE: Grouping and merging those chunks safely.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the strict mathematical boundaries of Amdahl's Law.
# - Master the MapReduce architectural pattern.
# - Implement a highly concurrent Fork-Join simulation.
#
# ==============================================================================
"""

import math
import multiprocessing
from collections import defaultdict
import time

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. AMDAHL'S LAW (THE MATHEMATICAL CEILING)
# ==============================================================================
def calculate_amdahls_law(parallel_portion: float, num_processors: int) -> float:
    """
    S = 1 / ((1 - P) + P/N)
    S = Max Speedup
    P = Proportion of program that can be parallelized (0.0 to 1.0)
    N = Number of processors
    """
    sequential_portion = 1.0 - parallel_portion
    speedup = 1.0 / (sequential_portion + (parallel_portion / num_processors))
    return speedup

def demonstrate_amdahls_law():
    section_header("Amdahl's Law (The Limits of Parallelization)")
    
    print("If 95% of your code is perfectly parallelizable, and 5% is sequential:")
    p = 0.95
    
    servers = [10, 100, 1000, 1000000]
    for n in servers:
        speedup = calculate_amdahls_law(p, n)
        print(f"  {n:>7} Servers -> Maximum Speedup: {speedup:>5.2f}x")
        
    print("\nNotice the mathematical asymptote! Even with 1 MILLION servers, you ")
    print("can NEVER exceed a 20x speedup! The 5% sequential bottleneck completely ")
    print("dominates the physical time of the universe at massive scales.")


# ==============================================================================
# 4. MAPREDUCE ARCHITECTURE (WORD COUNT)
# ==============================================================================
def map_phase(text_chunk: str) -> list[tuple[str, int]]:
    """
    The MAP Phase.
    Takes a massive chunk of data and breaks it down into intermediate Key-Value pairs.
    This function is 100% independent. It requires ZERO locks. It can be run on 
    10,000 different servers simultaneously.
    """
    # Simulate CPU work
    time.sleep(0.01)
    
    results = []
    words = text_chunk.lower().split()
    for word in words:
        # We emit a "1" for every single word we see!
        results.append((word, 1))
        
    return results

def reduce_phase(mapped_data_lists: list[list[tuple[str, int]]]) -> dict[str, int]:
    """
    The REDUCE Phase (and implicit Shuffle).
    Takes the massive output of all the Map nodes, groups them by Key, and 
    mathematically aggregates (reduces) them into the final answer.
    """
    # Simulate CPU work
    time.sleep(0.01)
    
    # 1. The "Shuffle" Step (Grouping by Key)
    grouped_data = defaultdict(list)
    for mapped_list in mapped_data_lists:
        for key, value in mapped_list:
            grouped_data[key].append(value)
            
    # 2. The "Reduce" Step (Aggregating the lists)
    final_counts = {}
    for key, values_list in grouped_data.items():
        # Values list looks like: [1, 1, 1, 1]
        # We reduce it by summing it up!
        final_counts[key] = sum(values_list)
        
    return dict(final_counts)

def demonstrate_mapreduce():
    section_header("MapReduce Architecture (Fork-Join)")
    
    document = [
        "the quick brown fox",
        "jumps over the lazy dog",
        "the dog barks at the fox",
        "the quick dog is lazy"
    ]
    
    print("Simulating a 4-Node Hadoop Cluster executing MapReduce...")
    
    start = time.perf_counter()
    
    # FORK (Scatter the data across 4 independent CPU cores)
    # This physically maps the 4 sentences to 4 isolated Python processes!
    with multiprocessing.Pool(processes=4) as pool:
        mapped_results = pool.map(map_phase, document)
        
    # We now have 4 separate lists of emitted tuples.
    # e.g., [[('the', 1), ('quick', 1)...], [('jumps', 1)...]]
    
    # JOIN (Gather and Reduce)
    # The Master node collects the isolated results and merges them safely.
    final_result = reduce_phase(mapped_results)
    
    end = time.perf_counter()
    
    print(f"\nFinal Word Count computed in {end - start:.4f} seconds:")
    for word, count in sorted(final_result.items(), key=lambda x: x[1], reverse=True):
        print(f"  '{word}': {count}")
        
    print("\nMapReduce completely bypasses Race Conditions by enforcing a strict ")
    print("functional architecture (Immutable Inputs -> Emitted Outputs), allowing ")
    print("infinite horizontal scaling without a single Mutex Lock!")


def run_all_labs():
    demonstrate_amdahls_law()
    demonstrate_mapreduce()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. What is the fundamental mathematical lesson of Amdahl's Law?
   Answer: Amdahl's Law mathematically proves that the theoretical speedup of any parallel program is strictly limited by its *sequential bottleneck*. If you have a task that takes 100 seconds, and 5 seconds of it CANNOT be parallelized (like merging arrays, writing the final result to disk, or acquiring a global Mutex lock), the absolute fastest the program can EVER run is 5 seconds. Even if you deploy an infinite number of $10,000 servers to drop the 95 parallelizable seconds to 0 seconds, you are forever trapped by the 5-second sequential floor. You cannot blindly throw hardware at a problem; you must redesign the algorithm to destroy the sequential dependencies.

2. In the MapReduce architecture, why is the "Map" phase mathematically forbidden from using global variables or modifying shared state?
   Answer: To achieve infinite horizontal scaling! If the Map function required access to a global database or a shared Counter variable in RAM, you would have to wrap it in a Mutex Lock. If 10,000 servers all try to acquire the same Mutex Lock, you instantly create a massive sequential bottleneck, triggering Amdahl's Law and crashing the system speed to zero. By enforcing "Pure Functions" (Data goes in $\to$ Data comes out, with absolutely zero Side Effects), the Map phase requires zero locks. 10,000 servers can operate at 100% CPU capacity simultaneously, achieving perfect parallel execution.

3. Explain the invisible "Shuffle" phase that occurs between Map and Reduce.
   Answer: The Map nodes emit raw tuples (e.g., Server A emits `("apple", 1)`, Server B emits `("apple", 1)`). The Reduce nodes expect all data for a specific Key to arrive at the same place (e.g., `reduce("apple", [1, 1])`). The "Shuffle" is the terrifying network phase in between. The Hadoop framework must physically route all tuples across the network switches so that every tuple containing the key `"apple"` lands on the *exact same physical Reduce server*. This requires massive network bandwidth and algorithmic routing (Consistent Hashing). The Shuffle phase is often the hidden bottleneck that kills poorly designed MapReduce jobs!
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: System Design (Parallel Algo Design) Completed.")
