"""
# ==============================================================================
# LABORATORY: PARALLEL ALGORITHMS (MULTI-CORE BFS GRAPH SEARCH)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Searching a sorted array is incredibly fast using Binary Search $O(\log N)$. 
# Parallelizing an array search is usually a waste of time.
#
# But what about searching a massive GRAPH?
# Imagine you work at Facebook (Meta). You need to calculate the "Degrees of Separation" 
# between User A and User B. The Social Graph has 3 Billion nodes and 500 Billion edges. 
# A single-core Breadth-First Search (BFS) will take days to traverse this graph!
#
# The Solution: Parallel Breadth-First Search!
#
# In standard BFS, you maintain a Queue. You pop ONE node, process its neighbors, 
# and push them back. 
# In Parallel BFS, you maintain a FRONTIER.
# - Level 1 Frontier: The origin node.
# - Level 2 Frontier: The 500 friends of the origin node.
# 
# Instead of processing those 500 friends one by one, we distribute the Frontier 
# across 16 CPU Cores! 
# - Core 1 processes the first 30 friends.
# - Core 2 processes the next 30 friends.
# 
# All cores simultaneously scan their assigned friends and dump the newly discovered 
# "Friends of Friends" into a massive "Next Frontier" bucket. 
# We wait for all cores to finish (Synchronization Barrier), swap the Next Frontier 
# to be the Current Frontier, and loop again!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the difference between a BFS Queue and a BFS Frontier.
# - Implement chunking logic for graph nodes.
# - Execute a Parallel BFS using Python `multiprocessing`.
#
# ==============================================================================
"""

import time
import multiprocessing
from typing import List, Set, Dict

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. SINGLE-CORE BFS (BASELINE)
# ==============================================================================
def standard_bfs(graph: Dict[int, List[int]], start_node: int) -> Dict[int, int]:
    """
    Standard single-core Breadth-First Search.
    Returns a dictionary mapping {NodeID: DistanceFromStart}.
    """
    distances = {start_node: 0}
    
    # We use the "Frontier" architecture even for the single-core version 
    # to perfectly mirror the parallel algorithm's logic.
    frontier = [start_node]
    current_distance = 0
    
    while frontier:
        current_distance += 1
        next_frontier = []
        
        for u in frontier:
            for v in graph.get(u, []):
                # If we haven't visited this node yet...
                if v not in distances:
                    distances[v] = current_distance
                    next_frontier.append(v)
                    
        frontier = next_frontier
        
    return distances


# ==============================================================================
# 4. PARALLEL BFS WORKER ENGINE
# ==============================================================================
def process_frontier_chunk(chunk_data: tuple) -> tuple:
    """
    This function is executed simultaneously by multiple CPU Cores!
    Because Python `multiprocessing` forces memory isolation, we must pack all 
    required data into a single argument and unpack it inside the worker.
    """
    chunk, graph, current_distance = chunk_data
    
    # The worker discovers new neighbors and tracks their distances!
    local_next_frontier = []
    local_distances = {}
    
    for u in chunk:
        for v in graph.get(u, []):
            # We don't know the GLOBAL visited state perfectly, so we just blindly 
            # return the nodes we found. The master process will filter duplicates!
            local_distances[v] = current_distance
            local_next_frontier.append(v)
            
    return (local_distances, local_next_frontier)


def parallel_bfs(graph: Dict[int, List[int]], start_node: int, num_processes: int = None) -> Dict[int, int]:
    """
    Multi-Core Breadth-First Search.
    """
    if num_processes is None:
        num_processes = multiprocessing.cpu_count()
        
    distances = {start_node: 0}
    frontier = [start_node]
    current_distance = 0
    
    # We spin up the Pool ONCE for the entire algorithm!
    # Spinning up pools is slow; doing it inside the while loop would crash performance.
    with multiprocessing.Pool(processes=num_processes) as pool:
        
        while frontier:
            current_distance += 1
            
            # 1. DIVIDE THE FRONTIER
            # Break the current level into chunks for each CPU core.
            import math
            chunk_size = max(1, math.ceil(len(frontier) / num_processes))
            chunks = [frontier[i : i + chunk_size] for i in range(0, len(frontier), chunk_size)]
            
            # Pack the arguments for the workers
            worker_args = [(c, graph, current_distance) for c in chunks]
            
            # 2. PARALLEL EXECUTION (Synchronization Barrier)
            # The `map` function automatically pauses the master thread until 
            # EVERY single CPU core has finished processing its chunk!
            results = pool.map(process_frontier_chunk, worker_args)
            
            # 3. MERGE RESULTS (The Master Thread consolidates)
            next_frontier = []
            
            for local_dists, local_next in results:
                for v in local_next:
                    # Critical Check: Was this node already visited?
                    # Since workers can't see the master `distances` dict, they might 
                    # return duplicates or previously visited nodes! We filter them here.
                    if v not in distances:
                        distances[v] = current_distance
                        next_frontier.append(v)
                        
            # Remove exact duplicates within the next_frontier itself 
            # (e.g., Core 1 and Core 2 both found the same shared friend).
            frontier = list(set(next_frontier))
            
    return distances


def demonstrate_parallel_bfs():
    section_header("Algorithm: Multi-Core Parallel BFS")
    
    print("Generating a massive highly-connected Social Graph...")
    # Generate a massive tree/graph
    # To see true parallel speedup, we need a massive branching factor.
    graph = {}
    nodes = 100_000
    branch_factor = 20
    
    # Build a pseudo-random graph
    import random
    for i in range(nodes):
        graph[i] = random.sample(range(nodes), branch_factor)
        
    print(f"Nodes: {nodes:,} | Edges: {nodes * branch_factor:,}")
    
    # 1. Single Core Benchmark
    print("\nExecuting Single-Core BFS...")
    start_time = time.time()
    single_dists = standard_bfs(graph, 0)
    single_duration = time.time() - start_time
    print(f"Time: {single_duration:.4f} seconds")
    print(f"Nodes reached: {len(single_dists):,}")
    
    # 2. Multi-Core Benchmark
    print("\nExecuting Multi-Core Parallel BFS...")
    start_time = time.time()
    multi_dists = parallel_bfs(graph, 0)
    multi_duration = time.time() - start_time
    print(f"Time: {multi_duration:.4f} seconds")
    print(f"Nodes reached: {len(multi_dists):,}")
    
    if multi_duration < single_duration:
        speedup = single_duration / multi_duration
        print(f"\nMulti-Core was {speedup:.2f}x faster!")
    else:
        print("\nNote: Parallel BFS suffers from massive IPC (Inter-Process Communication) ")
        print("overhead in Python. Passing massive graph dictionaries back and forth ")
        print("between OS memory boundaries destroys the multi-core speedup.")
        print("In C++ or Rust using Shared Memory Threads, Parallel BFS provides ")
        print("near-linear speedup!")


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why does Parallel BFS use a "Frontier" Array instead of a traditional Queue?
   Answer: A standard Queue `pop()` is fundamentally sequential. If 16 CPU cores all try to `pop()` from the same physical queue simultaneously in memory, it causes massive "Lock Contention" (they have to wait in line to safely extract an item). By using a Frontier Array, the master thread can slice the array mathematically (`array[0:1000]`, `array[1000:2000]`) and hand a totally independent slice to each core! No locking is required because the memory regions never overlap.

2. What is a "Synchronization Barrier"?
   Answer: In Parallel BFS, the algorithm explores Level 1, then Level 2, then Level 3. A CPU core processing Level 2 is mathematically NOT ALLOWED to begin processing Level 3 nodes until EVERY OTHER CPU core has completely finished processing their Level 2 nodes! If Core A races ahead and discovers a node at Level 3, it might record its distance as 3. But Core B might have found a shorter path to that exact same node at Level 2, but it was just running slower! The "Barrier" physically pauses fast cores, forcing them to wait for slow cores, guaranteeing the absolute shortest-path integrity of BFS.

3. Why do workers return duplicates that the Master Thread has to filter?
   Answer: Memory Isolation! In a true Shared Memory architecture (like C++ `std::thread`), every core has instant access to the master `visited` array. They can check it in $O(1)$ time. In Python's `multiprocessing`, each OS process gets a cloned snapshot of the data. They don't know what the other cores are doing! If Core 1 and Core 2 both discover Node $X$ simultaneously, they both think they are the first to find it! They both return it. The Master Thread, which holds the single source of truth, must filter out the duplicates.
"""

if __name__ == "__main__":
    demonstrate_parallel_bfs()
    print("\n[SUCCESS] Laboratory: Parallel BFS Completed.")
