"""
# ==============================================================================
# LABORATORY: INTERVIEW PREPARATION (FAANG - APPLE PYTHON QUESTIONS)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Apple interviews are highly hardware and OS-centric. They care deeply about 
# Concurrency, Multi-threading, and extreme memory efficiency on edge devices 
# (iPhones, IoT). You will be asked to design Thread-Safe Data Structures and 
# optimize algorithms for strict hardware constraints.
#
# A junior engineer uses standard Python arrays and doesn't consider the Global 
# Interpreter Lock (GIL) or Thread Racing conditions, leading to data corruption 
# in production.
# 
# A senior engineer implements strict Mutex Locking (`threading.Lock`), recognizes 
# when to use Deques for O(1) Queue operations, and understands how to safely 
# execute Multi-Threaded Producer/Consumer models without Deadlocks.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master Thread-Safe Data Structures (Bounded Blocking Queue).
# - Master Deadlock prevention via Mutex Locking and Condition Variables.
# - Understand strict memory bounding (`maxsize`).
#
# ==============================================================================
"""

import time
import threading
import collections
from typing import Any

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THREAD-SAFE BOUNDED BLOCKING QUEUE (PRODUCER / CONSUMER)
# ==============================================================================
class BoundedBlockingQueue:
    """
    Time: O(1) for enqueue/dequeue | Space: O(Capacity)
    A queue that safely handles multiple Threads trying to read/write simultaneously.
    If the queue is full, Producers MUST freeze (Block) and wait.
    If the queue is empty, Consumers MUST freeze (Block) and wait.
    """
    def __init__(self, capacity: int):
        self.capacity = capacity
        # We use deque for mathematically perfect O(1) pops from the left!
        self.queue = collections.deque()
        
        # A Condition Variable is a Mutex Lock coupled with a Waiting Area.
        # It allows threads to "Sleep" and be mathematically "Woken Up" by other threads!
        self.condition = threading.Condition()

    def enqueue(self, element: Any) -> None:
        """Producer executes this!"""
        # ACQUIRE THE LOCK: No other thread can touch the queue now!
        with self.condition:
            # If the queue is FULL, the Producer must mathematically SLEEP.
            # We use a `while` loop (not an `if`) to prevent Spurious Wakeups!
            while len(self.queue) >= self.capacity:
                print(f"    [PRODUCER] Queue is full! Thread sleeping...")
                # Releases the lock and puts the thread to sleep!
                self.condition.wait()
                
            # The thread woke up, and there is space!
            self.queue.append(element)
            print(f"  [PRODUCER] Inserted {element}. Size: {len(self.queue)}")
            
            # WAKE UP all sleeping Consumers! (There is finally data to read!)
            self.condition.notify_all()
            
        # The Lock is automatically released here due to the `with` statement.

    def dequeue(self) -> Any:
        """Consumer executes this!"""
        with self.condition:
            # If the queue is EMPTY, the Consumer must mathematically SLEEP.
            while len(self.queue) == 0:
                print(f"    [CONSUMER] Queue is empty! Thread sleeping...")
                self.condition.wait()
                
            # The thread woke up, and there is data!
            element = self.queue.popleft()
            print(f"  [CONSUMER] Removed {element}. Size: {len(self.queue)}")
            
            # WAKE UP all sleeping Producers! (There is finally empty space!)
            self.condition.notify_all()
            
            return element

def demonstrate_thread_safe_queue():
    section_header("Apple: Thread-Safe Bounded Queue")
    
    # Strictly bounded to 2 items!
    q = BoundedBlockingQueue(capacity=2)
    
    def producer_worker():
        for i in range(1, 6):
            q.enqueue(f"Data-{i}")
            time.sleep(0.1) # Simulate network delay
            
    def consumer_worker():
        for _ in range(5):
            q.dequeue()
            time.sleep(0.3) # Consumer is SLOWER than Producer!
            
    # Launch Threads!
    producer_thread = threading.Thread(target=producer_worker)
    consumer_thread = threading.Thread(target=consumer_worker)
    
    print("Launching Producer (Fast) and Consumer (Slow) Threads...\n")
    producer_thread.start()
    consumer_thread.start()
    
    # Main thread waits for them to finish
    producer_thread.join()
    consumer_thread.join()
    print("\nAll threads completed safely! No race conditions.")


# ==============================================================================
# 4. HARDWARE OPTIMIZATION: FINDING THE MAJORITY ELEMENT
# ==============================================================================
def majority_element_boyer_moore(nums: List[int]) -> int:
    """
    Time: O(N) | Space: O(1)
    Given an array of size N, find the majority element.
    The majority element is the element that appears MORE than ⌊N / 2⌋ times.
    
    Apple constraint: Do it in strictly O(1) Space (No Hash Maps allowed!)
    
    Algorithm: Boyer-Moore Voting Algorithm.
    If a number truly appears more than N/2 times, it will mathematically 
    survive if every OTHER number "votes against it" and cancels it out.
    """
    candidate = None
    votes = 0
    
    print("  Executing Boyer-Moore Voting Algorithm...")
    for num in nums:
        # If votes hit 0, the current candidate has been completely annihilated!
        # We mathematically assign a brand NEW candidate.
        if votes == 0:
            candidate = num
            print(f"    -> [NEW CANDIDATE] {candidate}")
            
        # If the number matches the candidate, it gains a vote!
        # If it's a different number, it physically attacks the candidate, reducing a vote!
        if num == candidate:
            votes += 1
        else:
            votes -= 1
            
    # Because the Majority Element mathematically occupies > 50% of the array,
    # it is mathematically impossible for its votes to be fully depleted by the 
    # minority elements. It is guaranteed to be the final standing candidate!
    return candidate

def demonstrate_boyer_moore():
    section_header("Apple: Boyer-Moore Majority Element (O(1) Space)")
    
    nums = [2, 2, 1, 1, 1, 2, 2]
    print(f"Array: {nums}\n")
    
    result = majority_element_boyer_moore(nums)
    print(f"\nResult: Majority Element is {result}")


def run_all_labs():
    demonstrate_thread_safe_queue()
    demonstrate_boyer_moore()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "In the Bounded Blocking Queue, why do we use a `while len(queue) == 0:` loop to check the condition, instead of a simple `if len(queue) == 0:`?"
   Senior Answer: "If we use an `if` statement, we expose the system to a catastrophic bug known as a 'Spurious Wakeup'. When `condition.notify_all()` is fired, the OS might wake up MULTIPLE sleeping Consumer threads simultaneously. The first Consumer acquires the lock, pops the only item in the queue, and releases the lock. The second Consumer then acquires the lock. If it used an `if` statement, it assumes there is still data because it already passed the `if` check before it went to sleep! It attempts to execute `popleft()` on a mathematically empty queue, violently crashing the server. By using a `while` loop, the thread is forced to re-verify the mathematical state of the queue the absolute millisecond it wakes up."

2. Interviewer: "What happens if a Producer forgets to call `condition.notify_all()` after enqueuing data?"
   Senior Answer: "This triggers an algorithmic Deadlock. If the queue was empty, all Consumer threads are permanently suspended in the OS Wait State. The Producer adds an item, but fails to send the OS Wake Signal. The Consumers continue to sleep indefinitely. Eventually, the Producer fills the queue to absolute maximum capacity and is forced to sleep as well. Now, both Producers and Consumers are permanently asleep, waiting for signals that will never arrive. The entire application freezes until the process is manually killed."

3. Interviewer: "Why does the Boyer-Moore Voting Algorithm mathematically guarantee it will find the Majority Element, and what is its fatal flaw?"
   Senior Answer: "The algorithm operates on mutual annihilation. Every time a minority element is paired against the Majority element, they mathematically destroy each other (`votes -= 1`). Because the definition of a Majority Element strictly requires it to appear $> N/2$ times, the combined sum of all minority elements is mathematically $\\le N/2$. Therefore, the minority elements physically do not possess enough 'ammunition' to reduce the Majority Element's vote count to zero. The fatal flaw is that the algorithm ONLY works if a Majority Element is strictly guaranteed to exist. If there is no Majority Element (e.g., `[1, 2, 3]`), it will confidently return a completely false candidate (e.g., `3`)!"
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: FAANG Prep (Apple) Completed.")
