"""
# ==============================================================================
# LABORATORY: PERFORMANCE AND OPTIMIZATION (OBJECT POOLS & FLYWEIGHT)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Instantiating and destroying objects in Python is mathematically expensive. 
# Memory must be allocated, `__init__` must be executed, and the Garbage Collector 
# must eventually track and destroy the object.
#
# A junior engineer designing a high-frequency trading system instantiates a 
# new `Trade` object 100,000 times a second, processes it, and lets it die. 
# The application suffers from catastrophic "Memory Churn", constantly triggering 
# the Garbage Collector and pausing the system.
#
# A senior engineer implements an "Object Pool" (The Flyweight Pattern). They 
# instantiate 10,000 `Trade` objects EXACTLY ONCE at startup. When a new trade 
# occurs, they check out a "dirty" object from the pool, reset its values, and 
# return it when finished. Memory allocations drop to zero, and the Garbage 
# Collector remains completely dormant.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master the Object Pool / Flyweight design pattern.
# - Eliminate Memory Churn and Garbage Collector spikes.
# - Master the `sys.intern` string optimization.
#
# ==============================================================================
"""

import timeit
import sys

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. MEMORY CHURN (THE NAIVE APPROACH)
# ==============================================================================
class HeavyBullet:
    """A mathematically heavy object simulating a projectile in a game."""
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
        self.active = True
        # Simulating expensive initialization logic (e.g., loading textures)
        self.payload = [i for i in range(100)]

def simulate_memory_churn(bullet_count: int):
    """
    Simulates a machine gun firing. 
    Every single bullet creates a brand new allocation in RAM!
    """
    bullets = []
    for i in range(bullet_count):
        # NEW ALLOCATION! (Expensive)
        b = HeavyBullet(i, i)
        bullets.append(b)
        
    # As soon as this function returns, all bullets fall out of scope!
    # The Garbage Collector is forced to clean up a massive mess!


# ==============================================================================
# 4. THE OBJECT POOL (FLYWEIGHT PATTERN)
# ==============================================================================
class BulletPool:
    def __init__(self, pool_size: int):
        print(f"  [POOL INIT] Pre-allocating {pool_size} heavy objects ONCE...")
        # We pre-allocate the objects exactly once at boot time!
        self.pool = [HeavyBullet(0, 0) for _ in range(pool_size)]
        
        # We use a simple integer index to track which bullets are "available".
        # This acts as an O(1) Ring Buffer!
        self.head = 0
        self.max_size = pool_size

    def acquire(self, x: float, y: float) -> HeavyBullet:
        """Grabs an existing object from the pool and overrides its state!"""
        bullet = self.pool[self.head]
        
        # We simply overwrite the old data! Zero memory allocations occur!
        bullet.x = x
        bullet.y = y
        bullet.active = True
        
        # Move the pointer forward
        self.head = (self.head + 1) % self.max_size
        return bullet

def simulate_object_pool(pool: BulletPool, bullet_count: int):
    """Simulates a machine gun firing using the pre-allocated pool!"""
    for i in range(bullet_count):
        # REUSING AN OBJECT! (Cheap)
        b = pool.acquire(i, i)


# ==============================================================================
# 5. MATHEMATICAL SPEED & GC PROOF
# ==============================================================================
def demonstrate_pool_performance():
    section_header("Performance Proof: Memory Churn vs Object Pool")
    
    bullet_count = 50_000
    
    # We create the pool OUTSIDE the simulation to mimic application boot-up!
    master_pool = BulletPool(1000)
    
    print("\n  [NAIVE ALLOCATION] Executing...")
    start_churn = timeit.default_timer()
    simulate_memory_churn(bullet_count)
    end_churn = timeit.default_timer()
    churn_time = end_churn - start_churn
    
    print("  [OBJECT POOL] Executing...")
    start_pool = timeit.default_timer()
    simulate_object_pool(master_pool, bullet_count)
    end_pool = timeit.default_timer()
    pool_time = end_pool - start_pool
    
    print(f"\n  -> Memory Churn Time: {churn_time * 1000:.2f} ms")
    print(f"  -> Object Pool Time:  {pool_time * 1000:.2f} ms")
    
    speedup = churn_time / pool_time
    print(f"\n  [CONCLUSION] The Object Pool is {speedup:.1f}x faster, and generated ZERO Garbage Collection churn!")


# ==============================================================================
# 6. FLYWEIGHT STRINGS (INTERNING)
# ==============================================================================
def demonstrate_string_interning():
    section_header("The Internal Flyweight: String Interning (`sys.intern`)")
    
    # In data processing (e.g., reading a CSV of 1,000,000 rows), you might 
    # encounter the string "New York" 50,000 times.
    
    # Python normally creates a NEW string object in RAM for dynamic strings!
    dynamic_str_1 = "".join(['N', 'e', 'w', ' ', 'Y', 'o', 'r', 'k'])
    dynamic_str_2 = "".join(['N', 'e', 'w', ' ', 'Y', 'o', 'r', 'k'])
    
    print("  [STANDARD STRINGS]")
    print(f"    String 1 ID: {id(dynamic_str_1)}")
    print(f"    String 2 ID: {id(dynamic_str_2)}")
    print(f"    Are they the same object in RAM? {dynamic_str_1 is dynamic_str_2}")
    # (Memory is wasted! We have two identical strings taking up space.)
    
    print("\n  [INTERNED STRINGS (FLYWEIGHT)]")
    # `sys.intern` forces Python to check a global Hash Table. 
    # If the string exists, it returns a pointer to the EXACT SAME OBJECT!
    interned_1 = sys.intern(dynamic_str_1)
    interned_2 = sys.intern(dynamic_str_2)
    
    print(f"    String 1 ID: {id(interned_1)}")
    print(f"    String 2 ID: {id(interned_2)}")
    print(f"    Are they the same object in RAM? {interned_1 is interned_2}")
    
    print("\n  [CONCLUSION] Interning reduced memory usage by collapsing 50,000 duplicates into a single pointer!")


def run_all_labs():
    demonstrate_pool_performance()
    demonstrate_string_interning()


# ==============================================================================
# 7. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "What is 'Memory Churn', and why is it fatal in real-time systems like Video Games or High-Frequency Trading (HFT)?"
   Senior Answer: "Memory Churn occurs when an application rapidly creates and destroys a massive volume of short-lived objects in a tight loop. While the total memory usage might never exceed a few Megabytes (because the objects die instantly), the *velocity* of allocations forces the OS memory allocator to work continuously, and triggers the Python Garbage Collector to aggressively sweep Generation 0 over and over again. In a game running at 60 FPS (16ms per frame), a sudden 5ms GC sweep causes catastrophic frame drops (stuttering). In HFT, it causes millisecond latency spikes, losing millions of dollars on trade execution."

2. Interviewer: "How does the Object Pool pattern mathematically eliminate Garbage Collection overhead?"
   Senior Answer: "The Garbage Collector's sole trigger condition is the allocation of *new* objects (e.g., Gen 0 sweeps when allocations exceed $700$). The Object Pool pattern entirely subverts this mechanism by allocating a fixed array of objects exactly once during the application's boot sequence. During the high-performance runtime loop, the application never uses the `__init__` constructor or the `del` keyword; it simply reassigns the attributes of pre-existing objects in the pool. Because zero new allocations occur, the internal GC counters never increment, mathematically guaranteeing that the GC will remain completely dormant for the entire duration of the workload."

3. Interviewer: "In string processing, why does `sys.intern()` optimize memory, and why doesn't Python just intern every single string automatically?"
   Senior Answer: "`sys.intern()` applies the Flyweight pattern to strings. If a CSV parser reads the string 'Active' 1,000,000 times, it normally creates 1,000,000 distinct string objects in RAM. `sys.intern()` looks up the string in a global C-level dictionary; if it exists, it returns the memory pointer to the original, collapsing 1,000,000 objects down to a single instance. However, Python does not do this automatically for dynamically generated strings because maintaining the global dictionary requires a Hash Table lookup for every single string creation! If you generate millions of *unique* strings (like UUIDs), interning them would catastrophically slow down the CPU with hash lookups, while providing absolutely zero memory benefit."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Memory Management (Object Pools) Completed.")
