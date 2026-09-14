"""
# ==============================================================================
# LABORATORY: SYSTEM DESIGN (HIGH-PERFORMANCE COMPUTING)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You are building a physics engine or processing 100GB of financial stock data.
# You write a standard `for` loop in Python. It runs at 100 iterations per second.
# 
# Python is mathematically fundamentally slow. 
# 1. It is Interpreted (the CPU must translate text to binary on the fly).
# 2. It uses Objects (Array of Structures - AoS) which destroys CPU Caching.
# 3. It runs SISD (Single Instruction, Single Data).
#
# High-Performance Computing (HPC) demands absolute hardware mastery.
# If you bypass Python and drop into C/NumPy arrays (Structure of Arrays - SoA), 
# you mathematically align the data into contiguous memory blocks. 
# 
# This triggers two massive hardware accelerations:
# 1. Cache Locality (L1/L2 Cache): The CPU fetches chunks of memory at once.
# 2. SIMD (Single Instruction, Multiple Data): The CPU physically processes 
#    4, 8, or 16 numbers in the exact same clock cycle!
#
# By understanding hardware architecture, your 100 iterations/sec script 
# transforms into 50,000,000 iterations/sec!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand CPU Architecture (L1/L2 Cache and Spatial Locality).
# - Understand AoS (Array of Structures) vs SoA (Structure of Arrays).
# - Understand SIMD Vectorization.
#
# ==============================================================================
"""

import time
import random

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. CACHE LOCALITY: AoS vs SoA
# ==============================================================================

# Array of Structures (AoS) - The Object-Oriented Way
class Particle:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

def process_aos(particles: list[Particle]) -> float:
    """
    To update the X position, the CPU must fetch the Object.
    The Object contains X, Y, Z, and massive Python Object metadata overhead.
    The CPU Cache is instantly filled with useless metadata and Y/Z coordinates!
    When it asks for the next Particle's X, it gets a Cache Miss and must wait 
    for the slow RAM!
    """
    total = 0.0
    for p in particles:
        # We only care about X! But the CPU physically dragged Y, Z, and metadata 
        # into the L1 Cache anyway, wasting massive bandwidth.
        total += p.x * 2.0
    return total

# Structure of Arrays (SoA) - The Data-Oriented Way
class ParticleSystem:
    def __init__(self, num_particles: int):
        # We physically separate X, Y, and Z into massive, contiguous arrays!
        self.x_array = [random.random() for _ in range(num_particles)]
        self.y_array = [random.random() for _ in range(num_particles)]
        self.z_array = [random.random() for _ in range(num_particles)]

def process_soa(system: ParticleSystem) -> float:
    """
    Because all the X coordinates are packed tightly together in memory, 
    when the CPU fetches the first X, it accidentally pulls the next 64 bytes 
    of X coordinates into the L1 Cache for free! (Spatial Locality).
    Zero Cache Misses!
    """
    total = 0.0
    # In pure Python, Lists still have pointer overhead.
    # In C/NumPy, this is a literal contiguous block of C-doubles.
    for x in system.x_array:
        total += x * 2.0
    return total

def demonstrate_cache_locality():
    section_header("Data-Oriented Design (AoS vs SoA)")
    
    num_particles = 1_000_000 # 1 Million particles
    print(f"Task: Update the X coordinate of {num_particles} Particles.")
    
    # 1. AoS Initialization
    print("\nInitializing Array of Structures (Object-Oriented)...")
    aos_particles = [Particle(random.random(), random.random(), random.random()) for _ in range(num_particles)]
    
    start = time.perf_counter()
    process_aos(aos_particles)
    end = time.perf_counter()
    aos_time = end - start
    print(f"  -> AoS Time: {aos_time:.4f} seconds")
    
    # 2. SoA Initialization
    print("\nInitializing Structure of Arrays (Data-Oriented)...")
    soa_system = ParticleSystem(num_particles)
    
    start = time.perf_counter()
    process_soa(soa_system)
    end = time.perf_counter()
    soa_time = end - start
    print(f"  -> SoA Time: {soa_time:.4f} seconds")
    
    if soa_time < aos_time:
        speedup = aos_time / soa_time
        print(f"\nThe SoA architecture was {speedup:.1f}x faster!")
        print("By physically separating the X array, we mathematically maximized ")
        print("the L1 CPU Cache Hit Rate (Spatial Locality)!")


# ==============================================================================
# 4. SIMD VECTORIZATION (CONCEPTUAL)
# ==============================================================================
def demonstrate_simd_concept():
    section_header("SIMD Vectorization (Hardware Magic)")
    
    print("What happens when you use NumPy arrays (which are written in C)?")
    print("NumPy utilizes SIMD (Single Instruction, Multiple Data).")
    print("-" * 60)
    print("Standard Loop (SISD):")
    print("  Cycle 1: x_array[0] * 2.0")
    print("  Cycle 2: x_array[1] * 2.0")
    print("  Cycle 3: x_array[2] * 2.0")
    print("  Cycle 4: x_array[3] * 2.0")
    
    print("\nSIMD Vectorized Execution (AVX-512 Processors):")
    print("  Cycle 1: [x0, x1, x2, x3, x4, x5, x6, x7] * 2.0")
    print("           (The CPU mathematically multiplies all 8 numbers in a SINGLE TICK!)")
    
    print("\nTo unlock SIMD in Python:")
    print("1. Never write `for i in range(len(arr)): arr[i] *= 2`")
    print("2. Always write `arr = arr * 2` (NumPy vectorization)")
    print("The C-backend instantly hijacks the CPU registers and executes SIMD!")


def run_all_labs():
    demonstrate_cache_locality()
    demonstrate_simd_concept()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. What is "Spatial Locality" and how does the CPU L1 Cache exploit it?
   Answer: When the CPU needs a piece of data from the slow Main RAM, it doesn't just grab that exact byte. It grabs the entire "Cache Line" (usually 64 bytes) surrounding that data, assuming you will probably want the nearby data very soon. This is Spatial Locality. If your data is an Array of Objects (AoS), that 64-byte chunk is filled with useless Object metadata, Pointers, and unneeded variables. You only get 1 useful number, and the next loop triggers another slow RAM fetch (Cache Miss). If your data is a contiguous Array of Numbers (SoA), that 64-byte chunk contains exactly 8 perfectly packed 64-bit numbers! The next 7 loops are executed instantly from the blazing-fast L1 Cache with zero RAM delay.

2. Explain the fundamental difference between Object-Oriented Programming (OOP) and Data-Oriented Design (DOD).
   Answer: OOP models the world using human logic: "A Dog is an Object. It barks and has an age." This forces data to be clumped by entity, scattering it chaotically across the RAM heap. It is great for human readability but mathematically destructive to hardware architecture. DOD (used heavily in Game Engines and HPC) models the world based on *how the CPU physically processes memory*. It says: "The CPU needs to update 10,000 ages simultaneously. Therefore, we strip the 'age' out of the Dog object and create one massive, contiguous `ages` array." DOD mathematically aligns software structures with physical hardware realities, sacrificing human readability for raw, unadulterated execution speed.

3. Why can a Python `for` loop never trigger SIMD vectorization natively?
   Answer: Python is a Dynamically Typed, Interpreted language. In a Python `for` loop, the interpreter does not know if `x_array[0]` is an Integer, a Float, a String, or a Custom Object until the exact millisecond it executes it. Because it has to perform heavy Type-Checking on every single iteration, it physically cannot package multiple numbers into a 256-bit SIMD hardware register to be executed simultaneously. SIMD requires mathematical certainty that the next 8 elements are strictly identical 32-bit floats. By using NumPy, you enforce static C-types in memory, giving the C-compiler the mathematical proof it needs to safely compile the loop into SIMD machine code.
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: System Design (High-Performance Computing) Completed.")
