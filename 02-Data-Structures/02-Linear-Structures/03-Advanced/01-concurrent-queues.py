"""
# ==============================================================================
# LABORATORY: CONCURRENT QUEUES (PRODUCER/CONSUMER)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# When scaling an application (like a web scraper or an image processing pipeline), 
# you cannot run everything synchronously. You must use multithreading. 
# But passing data between threads using a standard `list` or `collections.deque` 
# is dangerous because they are not Thread-Safe (race conditions can corrupt data).
# The `queue` module provides Thread-Safe queues backed by Mutex Locks.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Build a Thread-Safe Producer/Consumer pipeline using `queue.Queue`.
# - Understand blocking operations (`get(block=True)`) to prevent CPU thrashing.
# - Use "Poison Pills" (Sentinel values) to gracefully shut down threads.
# - Use `queue.PriorityQueue` for concurrent task prioritization.
#
# ==============================================================================
"""

import time
import threading
import queue
import random
from typing import Any

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THREAD-SAFE PRODUCER / CONSUMER
# ==============================================================================

# A unique sentinel object to signal threads to shut down
POISON_PILL = object()

def producer_worker(q: queue.Queue, name: str, items_to_produce: int):
    """
    Produces data and puts it into the queue.
    If the queue is full (because maxsize is set), `q.put()` will BLOCK 
    and wait until space is available. This prevents OOM errors.
    """
    for i in range(items_to_produce):
        item = f"Data-{name}-{i}"
        
        # Simulate time taken to generate data (e.g., fetching from API)
        time.sleep(random.uniform(0.1, 0.3))
        
        q.put(item)
        print(f"  [Producer {name}] Put: {item}")
        
    print(f"  [Producer {name}] Finished producing.")

def consumer_worker(q: queue.Queue, name: str):
    """
    Consumes data from the queue.
    `q.get()` will BLOCK if the queue is empty, waiting for data.
    """
    while True:
        # Blocks until an item is available
        item = q.get()
        
        # Check for the shutdown signal
        if item is POISON_PILL:
            print(f"  [Consumer {name}] Swallowed poison pill. Shutting down.")
            q.task_done()
            break
            
        # Simulate time taken to process data (e.g., parsing JSON)
        time.sleep(random.uniform(0.2, 0.5))
        print(f"  [Consumer {name}] Processed: {item}")
        
        # Tell the queue that the item was successfully processed
        q.task_done()

def demonstrate_thread_queue():
    section_header("Producer / Consumer Pipeline (queue.Queue)")
    
    # Bounded queue prevents producers from overwhelming memory if consumers are slow
    task_queue = queue.Queue(maxsize=10)
    
    print("Starting 1 Producer and 2 Consumers...\n")
    
    # Create threads
    producer = threading.Thread(target=producer_worker, args=(task_queue, "P1", 6))
    consumer_a = threading.Thread(target=consumer_worker, args=(task_queue, "C-Alpha"))
    consumer_b = threading.Thread(target=consumer_worker, args=(task_queue, "C-Beta"))
    
    # Start threads
    producer.start()
    consumer_a.start()
    consumer_b.start()
    
    # Wait for the producer to finish generating all items
    producer.join()
    
    # The producer is done, so we send the Poison Pills.
    # We need 1 pill for EVERY active consumer thread.
    task_queue.put(POISON_PILL)
    task_queue.put(POISON_PILL)
    
    # Wait for consumers to finish processing the remaining items in the queue
    consumer_a.join()
    consumer_b.join()
    
    # Final safety check: block until all task_done() calls have been made
    task_queue.join()
    print("\nPipeline executed and shut down gracefully.")


# ==============================================================================
# 4. CONCURRENT PRIORITY QUEUES
# ==============================================================================

def demonstrate_concurrent_priority_queue():
    """
    queue.PriorityQueue combines the thread-safety of queue.Queue with the 
    heap mechanics of heapq. It ensures that consumers always pop the highest 
    priority item available at that exact moment.
    """
    section_header("Concurrent Priority Queue")
    
    pq = queue.PriorityQueue()
    
    print("Main thread pushing tasks out of order...")
    # Priority is the first element of the tuple. Lower number = higher priority.
    pq.put((3, "Background Sync"))
    pq.put((1, "Process Payment"))
    pq.put((2, "Send Confirmation Email"))
    
    print("Main thread popping tasks...")
    # Because it's a priority queue, it will ALWAYS yield the item with priority 1 first.
    while not pq.empty():
        priority, task_name = pq.get()
        print(f" Executing: {task_name} (Priority {priority})")


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why must you use `queue.Queue` instead of `collections.deque` when working with threads?
   Answer: `queue.Queue` implements internal Mutex Locks, making it Thread-Safe. It also provides blocking operations (`get(block=True)`), meaning if the queue is empty, the thread goes to sleep instead of burning 100% CPU in an infinite `while` loop waiting for data.

2. What is a "Poison Pill" (Sentinel Value) in multithreading?
   Answer: Consumer threads usually run inside an infinite `while True:` loop. A poison pill is a unique object injected into the queue by the main thread. When a consumer pops it, it knows no more data is coming, breaks the loop, and allows the thread to terminate gracefully.

3. Why use a `maxsize` parameter when initializing a concurrent queue?
   Answer: To apply Backpressure. If your producers are fetching HTML pages (fast) and your consumers are running heavy ML inference (slow), an unbounded queue will eventually run out of RAM. A bounded queue forces the producers to pause (`put()` blocks) until the consumers catch up.
"""

if __name__ == "__main__":
    demonstrate_thread_queue()
    demonstrate_concurrent_priority_queue()
    print("\n[SUCCESS] Laboratory: Concurrent Queues Completed.")
