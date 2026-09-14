"""
# ==============================================================================
# LABORATORY: SYSTEM DESIGN (CUSTOM ALLOCATORS & OBJECT POOLS)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You are building a High-Frequency Trading (HFT) engine or a 60-FPS video game.
# 
# In a video game, you shoot a machine gun, spawning 1,000 Bullet objects per 
# second. 1,000 Bullets hit the wall and are destroyed.
# 
# When you say `Bullet()`, the Operating System (OS) physically stops your program, 
# searches the RAM for free space, locks it, and hands it back (Memory Allocation).
# When the bullet dies, the Garbage Collector (GC) kicks in, freezes your entire 
# game (GC Pause), and deletes the bullets.
#
# Doing this 1,000 times a second causes catastrophic frame drops (stuttering).
#
# To survive, you must use an Object Pool (Custom Allocator). 
# When the game starts, you pre-allocate exactly 10,000 Bullets in a massive array.
# When a gun fires, you do NOT ask the OS for memory! You simply grab an inactive 
# Bullet from your pre-allocated Pool and flip a boolean to `active=True`.
# When the bullet hits a wall, you do NOT delete it! You flip `active=False`.
#
# The GC is completely bypassed. OS Allocation is bypassed. You achieve 
# absolute $O(1)$ zero-allocation rendering!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the horrific latency of OS `malloc()` and GC Pauses.
# - Master the Object Pool (Flyweight) Design Pattern.
# - Implement $O(1)$ memory recycling.
#
# ==============================================================================
"""

import time

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. NAIVE ALLOCATION (THE STUTTERING GAME)
# ==============================================================================
class NaiveBullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.active = True
        
def simulate_naive_spawning(num_bullets: int) -> float:
    """
    Simulates destroying and recreating objects constantly.
    This triggers massive OS Allocation and Garbage Collection overhead!
    """
    start = time.perf_counter()
    bullets = []
    
    # 1. Spawn them
    for i in range(num_bullets):
        bullets.append(NaiveBullet(i, i))
        
    # 2. "Destroy" them (Delete the array, triggering Garbage Collection)
    bullets.clear()
    
    end = time.perf_counter()
    return end - start


# ==============================================================================
# 4. OBJECT POOL (ZERO-ALLOCATION ENGINE)
# ==============================================================================
class PooledBullet:
    def __init__(self):
        # Starts "dead".
        self.active = False
        self.x = 0
        self.y = 0
        
    def reset(self, x, y):
        """Instead of creating a new object, we just overwrite the old data!"""
        self.x = x
        self.y = y
        self.active = True

class BulletPool:
    def __init__(self, pool_size: int):
        # PRE-ALLOCATION! We do all the expensive OS memory requests right now, 
        # before the game even starts!
        self.pool = [PooledBullet() for _ in range(pool_size)]
        
        # We maintain a list of strictly INACTIVE bullets for O(1) fetching.
        self.available = list(range(pool_size))
        
    def spawn(self, x, y) -> PooledBullet:
        if not self.available:
            raise Exception("Pool Exhausted! Out of pre-allocated memory!")
            
        # 1. Grab a pre-existing dead bullet in O(1) time!
        bullet_idx = self.available.pop()
        bullet = self.pool[bullet_idx]
        
        # 2. Resurrect it!
        bullet.reset(x, y)
        # Store its index inside itself so it knows how to return to the pool
        bullet._pool_idx = bullet_idx 
        
        return bullet
        
    def kill(self, bullet: PooledBullet) -> None:
        """Does NOT delete the object! Just flags it as dead and returns it to the pool."""
        bullet.active = False
        self.available.append(bullet._pool_idx)

def simulate_pooled_spawning(pool: BulletPool, num_bullets: int) -> float:
    """
    Simulates spawning using the Object Pool.
    ZERO OS `malloc` calls. ZERO Garbage Collection!
    """
    start = time.perf_counter()
    active_bullets = []
    
    # 1. Spawn them (Recycle from Pool)
    for i in range(num_bullets):
        active_bullets.append(pool.spawn(i, i))
        
    # 2. "Destroy" them (Return to Pool)
    for b in active_bullets:
        pool.kill(b)
        
    end = time.perf_counter()
    return end - start

def demonstrate_object_pools():
    section_header("Custom Allocators (Object Pools)")
    
    num_bullets = 500_000
    print(f"Task: Spawn and destroy {num_bullets} objects as fast as possible.")
    
    # 1. Naive OS Allocation
    print("\nRunning Naive OS Allocation (triggers GC)...")
    naive_time = simulate_naive_spawning(num_bullets)
    print(f"  -> Time taken: {naive_time:.4f} seconds")
    
    # 2. Pre-allocated Object Pool
    print("\nPre-allocating Bullet Pool... (Occurs during loading screen)")
    pool = BulletPool(num_bullets)
    
    print("Running Pooled Allocation (bypasses OS and GC)...")
    pooled_time = simulate_pooled_spawning(pool, num_bullets)
    print(f"  -> Time taken: {pooled_time:.4f} seconds")
    
    # Python is already highly optimized, but Object Pooling often yields 2x-5x 
    # speedups in languages like C# (Unity) or C++ due to bypassing OS sys-calls!
    if pooled_time < naive_time:
        speedup = naive_time / pooled_time
        print(f"\nThe Object Pool was {speedup:.1f}x faster!")


def run_all_labs():
    demonstrate_object_pools()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why is requesting memory from the Operating System (`malloc` / `new`) so mathematically slow?
   Answer: When your application says `new Object()`, it doesn't just instantly claim RAM. It triggers a "System Call" (Context Switch) into the OS Kernel. The Kernel must physically scan its Memory Management Unit (MMU) pagetables, find a continuous block of unassigned RAM that fits your object size, lock that memory to prevent other programs from stealing it, and hand the physical hardware address back to your application. If memory is heavily fragmented, this search takes massive amounts of CPU cycles. Doing this thousands of times a second destroys performance.

2. Explain the "GC Pause" (Stop-The-World) phenomenon, and how Object Pools prevent it.
   Answer: A Tracing Garbage Collector (like in Java, C#, or Python's cycle detector) cannot safely analyze memory while the application is actively modifying it. To hunt down dead objects, the GC must literally "Stop The World" — physically freezing all application threads. In a 60-FPS video game, you have exactly 16 milliseconds to render a frame. A heavy GC pause takes 50-100ms! The game stutters violently. Object Pools completely bypass the GC because the Objects *never actually die*. The Array of objects is permanently anchored to the Root of the application. The GC looks at the Pool, sees all 10,000 objects are safely referenced by the Array, and instantly ignores them, taking 0ms!

3. What is the fundamental trade-off of the Object Pool architecture?
   Answer: The trade-off is Memory vs CPU. By pre-allocating 10,000 bullets, you guarantee blazing fast CPU execution ($O(1)$ spawning). However, you are permanently locking up the RAM required for 10,000 bullets, even if the player is currently standing perfectly still in a safe room! If you guess the Pool Size incorrectly (e.g., you pre-allocate 1,000, but the player uses a glitch to fire 1,500 bullets), the Pool violently crashes with a "Pool Exhausted" error. You must over-provision RAM to prevent crashes, wasting massive amounts of physical memory to guarantee CPU speed.
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: System Design (Custom Allocators) Completed.")
