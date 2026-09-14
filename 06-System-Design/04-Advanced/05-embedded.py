"""
# ==============================================================================
# LABORATORY: SYSTEM DESIGN (EMBEDDED SYSTEMS & IOT)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You are programming the braking system for an autonomous car.
# 
# If you use standard Python on a standard Linux OS, the Garbage Collector 
# might randomly pause execution for 50ms right when a child steps into the road. 
# Or the OS Scheduler might decide to run an antivirus update, stealing CPU 
# priority away from the brakes for 200ms. The car crashes.
#
# Standard OS schedulers are "Fair" (they try to give every program a turn). 
# Embedded Systems require "Real-Time Operating Systems" (RTOS). 
# An RTOS is "Deterministic". If a high-priority hardware interrupt fires 
# (e.g., Radar detects an object), the RTOS will violently preempt and freeze 
# every other process in the system in exactly 10 microseconds to guarantee the 
# brakes activate instantly.
#
# Furthermore, Embedded IoT (Internet of Things) devices like smart thermostats 
# run on coin-cell batteries with 256 KB of RAM. They cannot afford the massive 
# overhead of HTTP/JSON. They must use lightweight, binary-packed protocols 
# like MQTT over Pub/Sub.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand Hard Real-Time vs Soft Real-Time constraints.
# - Differentiate Fair Schedulers (Linux) vs Deterministic Schedulers (RTOS).
# - Master the MQTT protocol for low-power IoT devices.
#
# ==============================================================================
"""

import time
import random
import queue

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. DETERMINISTIC SCHEDULING (RTOS SIMULATION)
# ==============================================================================
class RTOS_Task:
    def __init__(self, name: str, priority: int, duration_ms: int):
        self.name = name
        self.priority = priority # 1 (Lowest) to 100 (Highest)
        self.duration_ms = duration_ms

class RTOS_Scheduler:
    """
    Simulates a Strict Priority-Based Preemptive Scheduler.
    Higher priority tasks instantly freeze lower priority tasks!
    """
    def __init__(self):
        # A priority queue mathematically sorts by lowest number first.
        # We store negative priority to force Highest Priority (100) to the top!
        self.task_queue = queue.PriorityQueue()
        
    def add_task(self, task: RTOS_Task):
        self.task_queue.put((-task.priority, task))
        
    def run(self):
        while not self.task_queue.empty():
            _, task = self.task_queue.get()
            print(f"[RTOS] Executing [PRIORITY {task.priority:3}] {task.name}...")
            # Simulate precise execution time
            time.sleep(task.duration_ms / 1000.0)
            print(f"       -> {task.name} completed perfectly on time.")

def demonstrate_rtos():
    section_header("RTOS (Hard Real-Time Schedulers)")
    
    print("Scenario: An Autonomous Vehicle CPU.")
    
    scheduler = RTOS_Scheduler()
    
    # 1. Background Tasks
    scheduler.add_task(RTOS_Task("Update GPS Maps", priority=10, duration_ms=50))
    scheduler.add_task(RTOS_Task("Play Spotify Music", priority=5, duration_ms=20))
    scheduler.add_task(RTOS_Task("Adjust AC Temp", priority=15, duration_ms=10))
    
    # 2. CRITICAL Hardware Interrupt fires!
    print("!!! [HARDWARE INTERRUPT] Radar detects child in the road! !!!")
    scheduler.add_task(RTOS_Task("ACTIVATE EMERGENCY BRAKES", priority=100, duration_ms=5))
    
    print("\n[Scheduler takes over. Notice the strict deterministic execution order:]")
    scheduler.run()
    
    print("\nThe RTOS mathematically guaranteed that the Brakes executed BEFORE ")
    print("the GPS update, bypassing 'Fairness' to guarantee absolute safety!")


# ==============================================================================
# 4. MQTT (LOW POWER IOT PROTOCOL)
# ==============================================================================
def demonstrate_mqtt():
    section_header("MQTT (IoT Communication Protocol)")
    
    print("A battery-powered Smart Thermostat needs to send the temperature to AWS.")
    print("-" * 60)
    
    print("Option A: HTTP (Heavyweight)")
    print("  1. Open TCP Connection (3-way handshake)")
    print("  2. Open TLS/SSL Connection (Heavy Crypto math, burns battery)")
    print("  3. Send HTTP Headers (500 Bytes of useless text like 'User-Agent: Mozilla')")
    print("  4. Send JSON Payload (50 Bytes): {'temp': 72.5}")
    print("  5. Keep connection alive, burning Wi-Fi radio power.")
    print("  -> Total Data Transferred: ~2,000 Bytes per message.")
    
    print("\nOption B: MQTT (Lightweight Pub/Sub)")
    print("  1. Maintain a tiny, persistent binary TCP connection.")
    print("  2. Send a packed binary packet (Header is exactly 2 Bytes!)")
    print("  3. Topic: 'home/living_room/temp'")
    print("  4. Payload: 72.5")
    print("  -> Total Data Transferred: ~30 Bytes per message.")
    
    print("\nMQTT reduces data overhead by 98%, allowing coin-cell batteries ")
    print("to last for 5 years instead of 5 weeks!")


def run_all_labs():
    demonstrate_rtos()
    demonstrate_mqtt()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Explain the difference between "Hard Real-Time" and "Soft Real-Time" constraints.
   Answer: A "Soft" Real-Time system degrades in usefulness if it misses a deadline, but nobody dies. (e.g., A live video stream buffer. If the CPU is late by 100ms, the video drops a frame. The user is annoyed, but the system survives). A "Hard" Real-Time system results in catastrophic failure if a deadline is missed by even 1 microsecond. (e.g., Deploying an airbag, activating a pacemaker, or adjusting the control fins on a supersonic rocket). Hard Real-Time requires strict RTOS architectures that mathematically guarantee maximum execution latency.

2. Why is Python (CPython) fundamentally unsuited for Hard Real-Time Embedded Systems?
   Answer: CPython is mathematically Non-Deterministic. First, the Global Interpreter Lock (GIL) can arbitrarily pause threads, making it impossible to guarantee that a specific thread will run at a specific microsecond. Second, Python's Garbage Collector runs on its own schedule. If it decides to run a Tracing GC sweep right when a critical interrupt fires, the entire program physically freezes for 50ms (Stop-The-World pause). You cannot use a language with a non-deterministic Garbage Collector for Hard Real-Time systems; you must use C/C++ or Rust where memory deallocation is explicitly controlled and perfectly predictable.

3. Explain how the MQTT "Quality of Service (QoS)" levels solve unstable IoT networks.
   Answer: IoT devices often live in areas with terrible network reception (e.g., a sensor in a basement). If a sensor sends a message via raw UDP, it might be lost forever. MQTT offers three QoS levels directly baked into the protocol:
   - QoS 0 (At most once): "Fire and Forget." Fastest, but messages can be lost.
   - QoS 1 (At least once): The sender resends the message until it gets an explicit Acknowledgment (ACK). Guarantees delivery, but might deliver the same message twice.
   - QoS 2 (Exactly once): A complex 4-step handshake guarantees the message is delivered exactly one time. Safest, but consumes the most battery and bandwidth.
   This allows engineers to surgically trade off Battery Life vs Data Reliability.
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: System Design (Embedded & IoT) Completed.")
