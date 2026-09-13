"""
Real-Time Systems in Python: Advanced System Design

1. WHAT IS IT?
Real-time systems are computing systems that must respond to events or stimuli within a specified time constraint (deadline). 
Correctness depends not just on the logical result of the computation, but also on the time at which the results are produced.

2. INDUSTRY USE CASES
- Hard Real-Time: Missing a deadline causes total system failure or catastrophic consequences (e.g., pacemakers, anti-lock brakes, avionics flight control).
- Firm Real-Time: Infrequent missed deadlines are tolerable, but the result is useless after the deadline (e.g., high-frequency trading, real-time database updates).
- Soft Real-Time: Missing a deadline degrades performance but the system remains functional and results may still have value (e.g., video streaming, online gaming).

3. BEGINNER EXPLANATION
Imagine you are a chef in a busy restaurant. If a customer orders a soft-boiled egg, it needs exactly 6 minutes. 
If you take 10 minutes, the egg is hard-boiled (deadline missed, wrong output - firm/hard real-time).
If someone orders a soup and it arrives 5 minutes late, they might be annoyed, but they will still eat it (soft real-time).
Real-time systems manage tasks to ensure these time constraints are met.

4. TECHNICAL EXPLANATION
While Standard CPython is NOT designed for hard real-time systems due to:
1. The Global Interpreter Lock (GIL) introducing unpredictable thread context switching.
2. Garbage Collection (GC) pauses (mark-and-sweep can block execution unpredictably).
3. Operating System scheduler (Linux/Windows are general-purpose, not RTOS).

However, Python is frequently used in Soft/Firm real-time systems (IoT gateways, algorithmic trading, test automation) by:
- Disabling or manually triggering the GC (`gc.disable()`, `gc.collect()`).
- Pinning processes to specific CPU cores.
- Using `asyncio` for deterministic, single-threaded cooperative multitasking.
- Interfacing with C/C++ or an RTOS for the critical real-time components while Python handles high-level logic.

5. ADVANCED CONCEPTS: PRIORITY INVERSION
A classic real-time problem where a high-priority task is indirectly preempted by a lower-priority task holding a shared resource.
Solution: Priority Inheritance (temporarily elevating the low-priority task's priority).

6. INTERVIEW QUESTIONS
- Q: Can CPython be used for hard real-time systems?
  A: No, due to unpredictable pauses from the garbage collector and GIL, and standard OS scheduling.
- Q: How would you minimize latency in a Python trading application?
  A: Use `asyncio` or multiprocess with core pinning, bypass standard GC, use memoryviews/bytearrays to avoid allocations, and use PyPy or Cython for hot paths.

Below is a simulation of a Soft Real-Time Task Scheduler using `asyncio` demonstrating deadline monitoring and prioritization.
"""

import asyncio
import time
import heapq
import random
from typing import Callable, Coroutine, Any
from dataclasses import dataclass, field

# ==========================================
# Real-Time Task Scheduler Simulation
# ==========================================

@dataclass(order=True)
class RealTimeTask:
    """
    Represents a task with a priority and a strict deadline.
    Lower priority number means higher urgency (e.g., 1 is higher than 10).
    """
    priority: int
    deadline_timestamp: float
    name: str = field(compare=False)
    coroutine_func: Callable[[], Coroutine[Any, Any, Any]] = field(compare=False)
    
    def __str__(self) -> str:
        return f"Task(name={self.name}, priority={self.priority}, deadline={self.deadline_timestamp:.4f})"


class RealTimeScheduler:
    """
    A priority-based scheduler for soft real-time tasks.
    It executes tasks based on priority and checks if they met their deadlines.
    """
    def __init__(self):
        self.task_queue: list[RealTimeTask] = []
        self._running = False
        self.missed_deadlines = 0
        self.met_deadlines = 0

    def add_task(self, name: str, priority: int, deadline_ms: int, func: Callable):
        """
        Add a task to the priority queue.
        deadline_ms is relative to the time the task is added.
        """
        deadline_timestamp = time.perf_counter() + (deadline_ms / 1000.0)
        task = RealTimeTask(priority, deadline_timestamp, name, func)
        heapq.heappush(self.task_queue, task)
        print(f"[{time.perf_counter():.4f}] Scheduled {task}")

    async def run(self):
        self._running = True
        print("\n--- Starting Real-Time Scheduler ---")
        
        while self.task_queue and self._running:
            # Pop the highest priority task (lowest priority number)
            current_task = heapq.heappop(self.task_queue)
            
            start_time = time.perf_counter()
            print(f"[{start_time:.4f}] Executing {current_task.name} (Priority {current_task.priority})")
            
            try:
                # Await the actual task execution
                await current_task.coroutine_func()
            except Exception as e:
                print(f"[{time.perf_counter():.4f}] Task {current_task.name} FAILED: {e}")
                
            end_time = time.perf_counter()
            
            # Deadline Analysis
            if end_time <= current_task.deadline_timestamp:
                self.met_deadlines += 1
                slack = current_task.deadline_timestamp - end_time
                print(f"[{end_time:.4f}] Task {current_task.name} COMPLETED. Met deadline. Slack: {slack*1000:.2f}ms\n")
            else:
                self.missed_deadlines += 1
                overdue = end_time - current_task.deadline_timestamp
                print(f"[{end_time:.4f}] Task {current_task.name} COMPLETED but MISSED DEADLINE by {overdue*1000:.2f}ms\n")
                
            # Simulate slight overhead/delay in scheduler tick
            await asyncio.sleep(0.001)

        print("--- Scheduler Finished ---")
        print(f"Stats: {self.met_deadlines} met, {self.missed_deadlines} missed.")


# ==========================================
# Simulated Payload Functions
# ==========================================

async def read_sensor_fast():
    """Simulates a fast hardware read."""
    await asyncio.sleep(0.01) # 10ms execution

async def complex_control_algorithm():
    """Simulates a CPU-intensive calculation (simulated via sleep for asyncio compatibility)."""
    # In a real app, blocking the event loop is bad. We simulate the time taken.
    await asyncio.sleep(0.05) # 50ms execution

async def unpredictable_network_call():
    """Simulates a network call with jitter."""
    delay = random.uniform(0.02, 0.1)
    await asyncio.sleep(delay)


async def main():
    scheduler = RealTimeScheduler()
    
    # Task 1: High priority, very tight deadline (20ms)
    scheduler.add_task(
        name="AntiLockBrake_Sensor", 
        priority=1, 
        deadline_ms=20, 
        func=read_sensor_fast
    )
    
    # Task 2: Medium priority, relaxed deadline (150ms)
    scheduler.add_task(
        name="Engine_Telemetry", 
        priority=5, 
        deadline_ms=150, 
        func=unpredictable_network_call
    )
    
    # Task 3: Highest priority, moderate deadline (80ms). 
    # Will be popped first despite being added last.
    scheduler.add_task(
        name="Airbag_Deployment_Check", 
        priority=0, 
        deadline_ms=80, 
        func=complex_control_algorithm
    )

    await scheduler.run()

if __name__ == "__main__":
    # In Python 3.11+, asyncio.run is the standard entry point.
    asyncio.run(main())

"""
COMMON MISTAKES & SECURITY CONCERNS:
1. Blocking the Event Loop: Using `time.sleep()` or standard `requests` inside an async real-time loop will block all other tasks, guaranteeing missed deadlines.
2. GC Pauses: Failing to account for garbage collection spikes. Use object pooling or memoryviews.
3. Priority Inversion: Failing to implement priority inheritance when locking shared resources (e.g., using a standard `asyncio.Lock`).
4. Clock Skew: Relying on `time.time()` (wall-clock time) instead of `time.perf_counter()` (monotonic). Wall-clock time can jump backwards due to NTP syncs.
"""
