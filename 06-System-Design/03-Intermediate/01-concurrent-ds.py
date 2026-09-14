"""
# ==============================================================================
# LABORATORY: SYSTEM DESIGN (CONCURRENT DATA STRUCTURES)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You are building the backend for a ticketing system (e.g., Taylor Swift tickets).
# There is exactly ONE VIP ticket left.
# 
# User A and User B both click "Buy" at the exact same millisecond.
# Thread A reads the database: "Tickets = 1".
# Thread B reads the database: "Tickets = 1".
# Thread A thinks: "Great, 1 > 0. I will sell it. Tickets = 0."
# Thread B thinks: "Great, 1 > 0. I will sell it. Tickets = 0."
#
# You just sold the same physical ticket to two different people. You have 
# caused a "Race Condition". Your system is fundamentally broken.
#
# To survive at scale, data structures cannot just be fast; they must be 
# "Thread-Safe". We must use Mutexes (Locks), Semaphores, and Atomic Operations 
# to mathematically force multi-core CPUs into strict sequential order when 
# modifying shared memory.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand Race Conditions and corrupted memory.
# - Master Mutexes (Mutual Exclusion Locks).
# - Master the Producer-Consumer pattern using Thread-Safe Queues.
#
# ==============================================================================
"""

import threading
import time
import queue
import random

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. RACE CONDITIONS & MUTEX LOCKS
# ==============================================================================
class BankAccount:
    """Demonstrates a Race Condition and how a Mutex Lock fixes it."""
    def __init__(self):
        self.balance = 0
        # A Mutual Exclusion Lock (Mutex)
        # When a thread acquires this lock, all other threads must physically FREEZE 
        # and wait until the lock is released!
        self.lock = threading.Lock()

    def deposit_unsafe(self):
        """No locks! Multiple threads will read and write over each other, destroying data!"""
        local_copy = self.balance
        time.sleep(0.0001) # Simulate CPU doing some math... Context switch occurs here!
        local_copy += 1
        self.balance = local_copy

    def deposit_safe(self):
        """Thread-Safe! The Mutex mathematically guarantees atomic execution."""
        with self.lock: # Equiv to: self.lock.acquire() ... try ... finally: self.lock.release()
            local_copy = self.balance
            time.sleep(0.0001) 
            local_copy += 1
            self.balance = local_copy

def run_threads(func, iterations, threads_count):
    threads = []
    for _ in range(threads_count):
        t = threading.Thread(target=lambda: [func() for _ in range(iterations)])
        threads.append(t)
        t.start()
    for t in threads:
        t.join()

def demonstrate_locks():
    section_header("Race Conditions & Mutex Locks")
    
    iters = 100
    num_threads = 10
    expected = iters * num_threads
    
    # 1. Unsafe Execution
    unsafe_account = BankAccount()
    run_threads(unsafe_account.deposit_unsafe, iters, num_threads)
    print(f"[UNSAFE] Expected Balance: ${expected}")
    print(f"[UNSAFE] Actual Balance  : ${unsafe_account.balance}")
    print("Why did it fail? Threads read the balance simultaneously, incremented it locally, ")
    print("and then blindly overwrote each other's work! Money was mathematically deleted.")
    
    # 2. Safe Execution
    safe_account = BankAccount()
    run_threads(safe_account.deposit_safe, iters, num_threads)
    print(f"\n[SAFE] Expected Balance: ${expected}")
    print(f"[SAFE] Actual Balance  : ${safe_account.balance}")
    print("The Mutex Lock forced the massive concurrent mob of threads into a strict ")
    print("single-file line. Perfect mathematical consistency achieved!")


# ==============================================================================
# 4. PRODUCER-CONSUMER (THREAD-SAFE QUEUES)
# ==============================================================================
class MessageQueueSystem:
    """
    If you have 5 web servers receiving requests (Producers) and 5 background 
    workers processing videos (Consumers), you need a middleman to safely 
    transfer the data without dropping it.
    """
    def __init__(self):
        # Python's queue.Queue is implicitly thread-safe using Condition Variables!
        # It handles all the Mutex locks internally.
        self.task_queue = queue.Queue(maxsize=10)
        self.active = True

    def producer(self, p_id: int):
        for i in range(3):
            if not self.active: break
            task = f"Task-{p_id}-{i}"
            try:
                # If the queue is completely full (size=10), the Producer is 
                # mathematically blocked (frozen) until a Consumer makes room!
                self.task_queue.put(task, timeout=2)
                print(f"[Producer {p_id}] Generated: {task}")
                time.sleep(random.uniform(0.01, 0.05))
            except queue.Full:
                print(f"[Producer {p_id}] Queue is FULL! Dropping task.")

    def consumer(self, c_id: int):
        while self.active or not self.task_queue.empty():
            try:
                # If the queue is empty, the Consumer is blocked (frozen) 
                # until a Producer generates a new task!
                task = self.task_queue.get(timeout=0.1)
                print(f"  -> [Consumer {c_id}] Processed: {task}")
                # Signal that the task is 100% complete
                self.task_queue.task_done()
                time.sleep(random.uniform(0.02, 0.06))
            except queue.Empty:
                continue

def demonstrate_producer_consumer():
    section_header("Producer-Consumer Architecture")
    
    system = MessageQueueSystem()
    
    # Create 2 Producers and 3 Consumers
    producers = [threading.Thread(target=system.producer, args=(i,)) for i in range(2)]
    consumers = [threading.Thread(target=system.consumer, args=(i,)) for i in range(3)]
    
    print("Starting massively concurrent Producer/Consumer engine...")
    for c in consumers: c.start()
    for p in producers: p.start()
    
    for p in producers: p.join()
    
    # Wait for the queue to completely empty out
    system.task_queue.join()
    system.active = False
    
    for c in consumers: c.join()
    print("\nEngine shut down. All tasks flawlessly transferred across thread boundaries!")


def run_all_labs():
    demonstrate_locks()
    demonstrate_producer_consumer()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. What is a "Race Condition", and why is it so notoriously difficult to debug?
   Answer: A Race Condition occurs when the final outcome of a program depends on the exact, microscopic timing of CPU thread context switches. E.g., Thread A reads `x`, Thread B reads `x`, Thread A writes `x+1`, Thread B writes `x+1`. The variable only increased by 1 instead of 2. It is notoriously difficult to debug because it is non-deterministic. If you run the code 1,000 times on your local machine, it might work perfectly 999 times! But in production, under heavy load, the CPU schedules the threads slightly differently, and the database suddenly corrupts. You cannot easily replicate or unit-test the exact timing of a CPU scheduler.

2. Explain the fatal flaw of Mutex Locks: "Deadlock".
   Answer: Deadlock is a mathematical checkmate. Imagine Thread A needs Lock 1, and then Lock 2. Thread B needs Lock 2, and then Lock 1. 
   - Time 0: Thread A acquires Lock 1. Thread B acquires Lock 2.
   - Time 1: Thread A tries to acquire Lock 2... but it's held by B. So Thread A freezes and waits.
   - Time 2: Thread B tries to acquire Lock 1... but it's held by A. So Thread B freezes and waits.
   Both threads are permanently frozen, waiting for the other to release the lock, but neither can proceed to release it. The entire server hangs infinitely. The solution is strictly ordering lock acquisition globally (e.g., always acquire Lock 1 before Lock 2).

3. In the Producer-Consumer pattern, why is a bounded queue (e.g., `maxsize=10`) critically important for system stability?
   Answer: "Backpressure". If you have 5 Producers generating tasks (like parsing incoming HTTP requests) at 1,000 per second, but your 2 Consumers (like saving to SQL) can only process 100 per second, an unbounded queue will grow infinitely. Within minutes, the queue will hold 500,000 objects in RAM. The server will run out of memory (OOM) and crash, completely destroying all pending tasks! A bounded queue creates Backpressure. Once the queue hits size 10, the `put()` operation mathematically blocks the Producers! The Producers are forced to stop accepting new HTTP requests, naturally throttling the system and preventing an explosive OOM crash.
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: System Design (Concurrent Data Structures) Completed.")
