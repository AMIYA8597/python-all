"""
# ==============================================================================
# LABORATORY: PERFORMANCE AND OPTIMIZATION (CONCURRENCY - THREAD POOLS)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A junior engineer learns about threading and writes a script to scrape 10,000 
# images from an S3 bucket. They spawn 10,000 threads simultaneously (`t.start()`). 
# Their computer violently crashes with a `RuntimeError: can't start new thread` 
# because they exhausted the OS-level thread limit, and their IP address gets 
# blacklisted by AWS for initiating a DDoS attack.
#
# A senior engineer uses a `ThreadPoolExecutor` and a `BoundedSemaphore`. They 
# mathematically limit the application to exactly 50 concurrent active threads. 
# The Thread Pool acts as a self-regulating pipeline, aggressively maximizing 
# network throughput while guaranteeing the hardware and the target API are 
# perfectly protected from overload.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master `concurrent.futures.ThreadPoolExecutor`.
# - Master context management for clean thread shutdown.
# - Master OS-level concurrency throttling using `threading.Semaphore`.
#
# ==============================================================================
"""

import time
import timeit
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE THREAD POOL PIPELINE
# ==============================================================================
def simulated_download(task_id: int) -> str:
    """Simulates downloading a file (I/O Bound)."""
    # Sleep simulates waiting for the HTTP response
    time.sleep(0.5) 
    return f"File_{task_id}.jpg"

def demonstrate_thread_pool():
    section_header("The Self-Regulating Pipeline: ThreadPoolExecutor")
    
    # We have 20 massive files to download!
    total_tasks = 20
    print(f"  [INIT] We need to download {total_tasks} files.")
    print("  (A sequential loop would take exactly 10.0 seconds.)")
    
    # We mathematically constrain the OS to 5 concurrent threads!
    MAX_WORKERS = 5
    
    print(f"\n  [EXECUTION] Booting Thread Pool with {MAX_WORKERS} workers...")
    start_time = timeit.default_timer()
    
    # The 'with' statement guarantees the OS threads are cleanly destroyed (joined)
    # when the block exits!
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        
        # We submit all 20 tasks to the executor instantly!
        # The executor queues them up, but ONLY allows 5 to execute simultaneously.
        futures = {executor.submit(simulated_download, i): i for i in range(total_tasks)}
        
        print("  [MONITOR] Tasks queued. Waiting for completion...")
        
        # `as_completed` yields the futures the exact millisecond they finish!
        completed_count = 0
        for future in as_completed(futures):
            result = future.result()
            completed_count += 1
            if completed_count % 5 == 0:
                print(f"    -> Finished {completed_count}/{total_tasks}...")
                
    end_time = timeit.default_timer()
    total_time = end_time - start_time
    
    print(f"\n  [CONCLUSION] All {total_tasks} downloads finished in {total_time:.2f} seconds!")
    print(f"  (Math: 20 tasks / 5 workers = 4 batches. 4 * 0.5s = 2.0s.)")
    print("  The pool mathematically regulated the execution speed flawlessly.")


# ==============================================================================
# 4. HARDWARE THROTTLING (THE SEMAPHORE)
# ==============================================================================
# What if we need to throttle a highly specific sub-resource, 
# even *within* a thread pool?
# E.g., We have 50 worker threads parsing HTML, but we are mathematically 
# constrained to only 3 concurrent Database connections!

# A Semaphore is a mathematical OS-level bouncer. It holds a finite number of "Tickets".
DB_CONNECTION_LIMIT = 3
db_semaphore = threading.BoundedSemaphore(DB_CONNECTION_LIMIT)
active_db_connections = 0 # Strictly for logging purposes

def data_processing_pipeline(worker_id: int):
    global active_db_connections
    
    # STEP 1: Fast work (Unrestricted!)
    time.sleep(0.1) 
    
    # STEP 2: The Database Insertion (Restricted to 3 concurrent access!)
    # A thread must mathematically ACQUIRE a ticket from the Semaphore.
    # If tickets = 0, the OS forces the thread to sleep until one opens up!
    with db_semaphore:
        active_db_connections += 1
        print(f"    [DB ACQUIRED] Worker {worker_id} writing... (Active DB Threads: {active_db_connections})")
        
        # Simulating slow database write
        time.sleep(0.3)
        
        active_db_connections -= 1
        # When the 'with' block exits, the ticket is instantly RELEASED!

def demonstrate_semaphores():
    section_header("Hardware Throttling: The Bounded Semaphore")
    
    print(f"  [INIT] We have 10 fast worker threads, but ONLY {DB_CONNECTION_LIMIT} Database Connections!")
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        # We blast all 10 workers at once!
        futures = [executor.submit(data_processing_pipeline, i) for i in range(10)]
        
        # They will all rush the Semaphore simultaneously, but it will physically
        # block them, ensuring `active_db_connections` NEVER exceeds 3!


def run_all_labs():
    demonstrate_thread_pool()
    demonstrate_semaphores()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "Why should you use a `ThreadPoolExecutor` instead of manually spawning OS threads using `threading.Thread(target=...)`?"
   Senior Answer: "Manual thread spawning is catastrophically dangerous in production. If a server receives a spike of $5,000$ concurrent HTTP requests, manually spawning $5,000$ threads instantly consumes $40$ GB of RAM, triggering an OS-level OOM crash. The `ThreadPoolExecutor` implements the 'Queue + Worker Pool' architectural pattern. It pre-allocates a mathematically fixed ceiling of threads (e.g., `max_workers=50`). If $5,000$ requests arrive, it safely queues them in an internal deque. The $50$ threads aggressively process the queue without ever exceeding the hardware memory limits. Furthermore, it cleanly manages the OS thread teardown (`.join()`) via Python's Context Manager (`with`), preventing orphaned zombie threads from leaking RAM."

2. Interviewer: "What is `as_completed()`, and why is it superior to just calling `future.result()` in a linear list comprehension?"
   Senior Answer: "If you submit $10$ tasks, Task 1 might take $50$ seconds, while Tasks 2 through 10 take $1$ second each. If you iterate through the list of Futures linearly (`[f.result() for f in futures]`), your application physically halts on Task 1 for $50$ seconds! You completely blind yourself to the fact that Tasks 2-10 have already finished. `as_completed(futures)` solves this by acting as an asynchronous Event Generator. It yields the specific Future the exact millisecond it finishes execution, regardless of the original submission order. This allows you to stream results back to the client or write them to the DB in real-time, drastically reducing perceived application latency."

3. Interviewer: "What is the architectural difference between a `Lock` (Mutex) and a `Semaphore`?"
   Senior Answer: "A `Lock` (Mutex) is a boolean primitive: `1` or `0`. It strictly enforces Mutual Exclusion, guaranteeing that exactly ONE thread can access a specific variable (like appending to a list) at any given time to prevent Race Conditions. A `Semaphore` is a hardware integer counter (e.g., $3$). It enforces Rate Limiting or Connection Pooling. It allows exactly N threads to access a resource simultaneously, mathematically rejecting the $N+1$ thread. You use a Lock to protect shared memory, and a Semaphore to protect finite physical infrastructure (like a Database Connection Pool or a strict API Rate Limit)."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Concurrency (Thread Pools) Completed.")
