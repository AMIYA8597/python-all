"""
# ==============================================================================
# LABORATORY: LOCK-FREE DATA STRUCTURES & ATOMICS
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Traditional multithreading uses Locks (Mutexes) to prevent race conditions 
# (e.g., `queue.Queue`). However, Locks cause severe performance bottlenecks 
# (threads sleep while waiting for the lock, causing OS Context Switching overhead) 
# and introduce the risk of Deadlocks. High-Frequency Trading (HFT) and ultra-low 
# latency systems use "Lock-Free" data structures based on hardware-level Atomic 
# operations like Compare-And-Swap (CAS).
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the overhead and dangers of standard Mutex Locks.
# - Understand Hardware Atomics and Compare-And-Swap (CAS).
# - Understand why Python's GIL complicates Lock-Free programming.
# - Simulate a Lock-Free counter using a CAS conceptual loop.
#
# ==============================================================================
"""

import time
import threading

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE PROBLEM WITH LOCKS (MUTEXES)
# ==============================================================================
def demonstrate_mutex_overhead():
    """
    When a thread hits a Locked Mutex, the Operating System physically pauses 
    the thread (Context Switch), saves its CPU registers, and wakes it up later. 
    This takes microseconds. In systems processing millions of events per second, 
    this OS overhead destroys throughput.
    """
    section_header("The Overhead of Locks")
    
    counter = 0
    lock = threading.Lock()
    
    def worker_with_lock():
        nonlocal counter
        for _ in range(1_000_000):
            # The Lock guarantees safety, but acts as a massive bottleneck
            with lock:
                counter += 1
                
    start = time.perf_counter()
    t1 = threading.Thread(target=worker_with_lock)
    t2 = threading.Thread(target=worker_with_lock)
    t1.start(); t2.start()
    t1.join(); t2.join()
    
    print(f"Mutex locked counter reached {counter} in {time.perf_counter() - start:.4f}s")
    print("If one thread held the lock and crashed (or slept), the other thread")
    print("would be stuck forever (Deadlock).")


# ==============================================================================
# 4. HARDWARE ATOMICS & COMPARE-AND-SWAP (CAS)
# ==============================================================================
"""
In a true compiled language (C++, Rust, Java), you can use CPU-level atomic 
instructions. The most famous is Compare-And-Swap (CAS).

A CAS operation takes 3 arguments:
1. The memory address (variable).
2. The expected old value.
3. The new value.

The CPU locks the memory bus for a single clock cycle, checks if the variable 
STILL equals the expected old value, and if so, updates it to the new value. 
If it doesn't match (meaning another thread changed it), it fails.
"""

class SimulatedAtomicInteger:
    def __init__(self, initial_value: int):
        self._value = initial_value
        # We use a lock ONLY to simulate the hardware-level CPU bus lock
        self._cpu_lock = threading.Lock()
        
    def compare_and_swap(self, expected_value: int, new_value: int) -> bool:
        """
        Simulates a CPU-level atomic CAS instruction.
        In C++, this is `std::atomic_compare_exchange_weak`.
        """
        with self._cpu_lock: # Simulating hardware lock
            if self._value == expected_value:
                self._value = new_value
                return True
            return False
            
    def get(self) -> int:
        return self._value


def demonstrate_lock_free_cas():
    """
    In a Lock-Free structure, threads NEVER go to sleep. 
    Instead, they read the current value, compute the new value, and attempt 
    to CAS it. If the CAS fails, they simply loop and try again.
    This is called a "Spin Loop".
    """
    section_header("Lock-Free Compare-And-Swap (CAS) Simulation")
    
    atomic_counter = SimulatedAtomicInteger(0)
    
    def lock_free_worker():
        for _ in range(10_000):
            while True:
                # 1. Read current value
                current_val = atomic_counter.get()
                
                # 2. Compute the new value (e.g., adding 1)
                new_val = current_val + 1
                
                # 3. Attempt the hardware-atomic swap!
                # If no other thread changed the value in the last millisecond, it succeeds.
                if atomic_counter.compare_and_swap(current_val, new_val):
                    break # Success! Exit the spin loop.
                # If it failed, we loop instantly and try again.
                
    start = time.perf_counter()
    t1 = threading.Thread(target=lock_free_worker)
    t2 = threading.Thread(target=lock_free_worker)
    t1.start(); t2.start()
    t1.join(); t2.join()
    
    print(f"Lock-Free CAS counter reached {atomic_counter.get()} in {time.perf_counter() - start:.4f}s")
    print("Notice: No thread was ever put to sleep by the OS. If one thread")
    print("crashed, the other thread would continue completely unaffected!")


# ==============================================================================
# 5. PYTHON'S GIL AND TRUE LOCK-FREE STRUCTURES
# ==============================================================================
def explain_python_gil():
    section_header("Python's GIL and Lock-Free Reality")
    print("""
Can we write true Lock-Free structures in pure Python?
Not really. The Global Interpreter Lock (GIL) already acts as a massive Mutex 
that prevents multiple Python bytecodes from executing simultaneously on 
different CPU cores.

If you need true Lock-Free concurrency in Python:
1. You must use the `multiprocessing` module.
2. You must allocate raw memory using `multiprocessing.Value` or `ctypes`.
3. You must write C-extensions (or Cython/Rust bindings) that release the GIL 
   (`with nogil:`) and issue raw hardware CAS instructions.

For 99% of Python applications, `queue.Queue` (which uses standard Mutexes) 
is perfectly fine because the bottleneck is Network/Disk I/O, not CPU instruction 
contention.
    """)


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. What is the fundamental problem with using Mutex Locks in high-throughput systems?
   Answer: When a thread is blocked by a lock, the OS performs a Context Switch (putting the thread to sleep and waking it later). This introduces massive latency. Additionally, locks can cause Deadlocks if a thread crashes while holding the lock.

2. How does a Compare-And-Swap (CAS) loop achieve "Lock-Free" thread safety?
   Answer: Instead of locking the data, a thread reads the data, computes the update, and asks the CPU to atomically swap the old value with the new value ONLY IF the old value hasn't changed. If it has changed (another thread won the race), the CPU rejects the swap, and the thread simply loops and tries again (Spin Loop) without ever going to sleep.

3. Why are true Lock-Free data structures rarely written in pure Python?
   Answer: Python's Global Interpreter Lock (GIL) prevents true multi-core parallel execution of Python bytecode anyway. To get the benefits of Lock-Free CPU architectures, you must use C/Rust extensions or `multiprocessing` with raw `ctypes` memory.
"""

if __name__ == "__main__":
    demonstrate_mutex_overhead()
    demonstrate_lock_free_cas()
    explain_python_gil()
    print("\n[SUCCESS] Laboratory: Lock-Free Structures Completed.")
