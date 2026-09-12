"""
Module: Systems Programming Interview Questions
Learning Objectives:
1. Understand core concepts of systems programming in Python.
2. Implement a basic Thread Pool from scratch.
3. Handle concurrency, locks, and task queues.

Concept Explanation:
Systems programming questions test your understanding of OS-level concepts, concurrency,
memory management, and I/O. In Python, this often involves the `threading` or `multiprocessing` modules.
Building a Thread Pool demonstrates understanding of worker threads, task queues, and thread synchronization.
"""

import threading
import queue
import time
from typing import Callable, Any, List

class Worker(threading.Thread):
    """
    A worker thread that continuously polls a queue for tasks to execute.
    """
    def __init__(self, task_queue: queue.Queue):
        super().__init__()
        self.task_queue = task_queue
        self.daemon = True # Allows program to exit even if threads are running
        self.start()

    def run(self):
        while True:
            func, args, kwargs = self.task_queue.get()
            try:
                func(*args, **kwargs)
            except Exception as e:
                print(f"Task raised an exception: {e}")
            finally:
                self.task_queue.task_done()

class ThreadPool:
    """
    A simple thread pool implementation.
    """
    def __init__(self, num_threads: int):
        self.task_queue = queue.Queue()
        self.workers = [Worker(self.task_queue) for _ in range(num_threads)]

    def add_task(self, func: Callable, *args, **kwargs):
        """Add a task to the queue."""
        self.task_queue.put((func, args, kwargs))

    def wait_completion(self):
        """Wait for all tasks in the queue to be processed."""
        self.task_queue.join()

# --- Performance Analysis & Edge Cases ---
# This implementation uses daemon threads so they automatically exit when main finishes.
# Edge cases: Queue getting too large (memory issue) -> we could add a maxsize to the Queue.
# Exceptions in threads are caught so they don't crash the worker thread.

def sample_task(task_id: int, duration: float):
    print(f"Task {task_id} starting...")
    time.sleep(duration)
    print(f"Task {task_id} completed.")

def main():
    print("Initializing thread pool with 3 workers.")
    pool = ThreadPool(num_threads=3)
    
    # Adding 5 tasks
    for i in range(5):
        pool.add_task(sample_task, i, 1.0)
        
    print("Tasks added. Waiting for completion...")
    pool.wait_completion()
    print("All tasks completed.")

if __name__ == "__main__":
    main()
