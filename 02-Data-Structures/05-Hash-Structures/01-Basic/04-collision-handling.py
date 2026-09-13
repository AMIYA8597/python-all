"""
# ==============================================================================
# LABORATORY: ADVANCED COLLISION HANDLING & THE BIRTHDAY PARADOX
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You've learned about Separate Chaining (Linked Lists) and Open Addressing 
# (Linear Probing) to handle collisions. 
# But why do collisions happen so often? If you have an array of size 365, and 
# you insert 23 random items, what is the probability of a collision? 
# The intuitive answer is 23/365 (~6%). The mathematical reality (The Birthday 
# Paradox) is that it is 50%! Collisions are mathematically unavoidable.
#
# Because collisions are so frequent, advanced Open Addressing must fix the flaws 
# of Linear Probing. If 5 items hash to index 1, Linear Probing puts them at 
# 1, 2, 3, 4, and 5. This forms a massive "Primary Cluster". If a new item hashes 
# to 3, it immediately collides with the cluster and makes it even bigger!
# 
# We solve this with Quadratic Probing and Double Hashing.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the Load Factor and Dynamic Rehashing.
# - Implement Quadratic Probing to prevent Primary Clustering.
# - Implement Double Hashing to prevent Secondary Clustering.
#
# ==============================================================================
"""

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE LOAD FACTOR & DYNAMIC REHASHING
# ==============================================================================
def explain_load_factor():
    section_header("Concept: Load Factor & Rehashing")
    print("""
Load Factor (Alpha) = Total Items in Hash Table / Total Capacity of Array.

If you have an array of size 10, and you insert 7 items, the Load Factor is 0.7 (70%).
As the Load Factor approaches 1.0 (100%), the probability of a collision skyrockets 
to near absolute certainty. The O(1) table degrades into an O(N) linear search.

To prevent this, Professional Hash Tables (like Python's `dict` or Java's `HashMap`) 
strictly enforce a MAXIMUM Load Factor (Usually 0.66 or 0.75).

DYNAMIC REHASHING:
When `size / capacity > 0.66`:
1. The table allocates a BRAND NEW array that is exactly 2x the size.
2. It iterates through the old array.
3. It takes every single key, recalculates `hash(key) % NEW_CAPACITY`, and inserts 
   it into the new array.
4. The old array is destroyed by the Garbage Collector.

This operation takes O(N) time! However, because it doubles in size, it happens 
so rarely that the "Amortized" cost of insertion remains exactly O(1).
    """)


# ==============================================================================
# 4. QUADRATIC PROBING
# ==============================================================================
def demonstrate_quadratic_probing():
    section_header("Algorithm: Quadratic Probing")
    
    capacity = 10
    
    print("Scenario: Keys A, B, and C all hash to index 2 (A massive collision).")
    
    print("\nLINEAR PROBING (i + 1):")
    print(f" 'A' hashes to 2 -> Places at index 2.")
    print(f" 'B' hashes to 2 -> index 2 full -> Probes (2 + 1) = 3 -> Places at index 3.")
    print(f" 'C' hashes to 2 -> index 2 full -> Probes (2 + 1)=3 full -> Probes (2 + 2) = 4.")
    print(" Result: Indices 2, 3, and 4 are now a solid block of data (Primary Cluster).")
    
    print("\nQUADRATIC PROBING (i + k^2):")
    print(f" 'A' hashes to 2 -> Places at index (2 + 0^2) = 2.")
    print(f" 'B' hashes to 2 -> index 2 full -> Probes (2 + 1^2) = 3 -> Places at index 3.")
    print(f" 'C' hashes to 2 -> index 2 full -> Probes 3 full -> Probes (2 + 2^2) = 6.")
    print(" Result: 'C' jumped completely over the cluster and landed safely at index 6!")
    print(" This completely eliminates Primary Clustering.")


# ==============================================================================
# 5. DOUBLE HASHING
# ==============================================================================
def demonstrate_double_hashing():
    section_header("Algorithm: Double Hashing")
    
    print("Quadratic Probing fixes Primary Clustering, but it suffers from Secondary Clustering.")
    print("If Keys A, B, and C all hash to 2, they will all follow the EXACT same jump sequence:")
    print(" Jump +1, Jump +4, Jump +9. They will still collide with each other during the jumps.")
    
    print("\nDouble Hashing fixes this by using a SECOND hash function to determine the Jump Size!")
    print(" Probe Formula: (Hash1(key) + attempts * Hash2(key)) % Capacity")
    
    print("\nLet's assume Hash1('Apple') = 2, and Hash1('Banana') = 2.")
    print("But Hash2('Apple') = 3, and Hash2('Banana') = 5.")
    
    print("\nProbing 'Apple':")
    print(" Attempt 0: (2 + 0*3) = 2 (Collision)")
    print(" Attempt 1: (2 + 1*3) = 5 (Placed at 5!)")
    
    print("\nProbing 'Banana':")
    print(" Attempt 0: (2 + 0*5) = 2 (Collision)")
    print(" Attempt 1: (2 + 1*5) = 7 (Placed at 7!)")
    
    print("\nResult: Even though they started at the exact same collision index (2),")
    print("their unique secondary hashes caused them to jump in completely different directions!")


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why does Dynamic Rehashing require us to recalculate the hash modulo (`hash % NEW_CAPACITY`) for every item?
   Answer: If `hash("apple")` is 105, and the old capacity was 10, it was stored at index 5 (105 % 10 = 5). If we just copy index 5 to the new array (capacity 20), it will be broken! Why? Because 105 % 20 is 15! When we try to `get("apple")` later, the table will look at index 15 and find nothing. You MUST recalculate the modulo for the new capacity.

2. What is the fundamental requirement for Hash2 in Double Hashing?
   Answer: `Hash2(key)` MUST NEVER EVALUATE TO 0! If `Hash2` evaluates to 0, the probe sequence becomes `(Hash1 + attempts * 0)`, meaning the algorithm will just check the exact same collided index forever in an infinite loop. `Hash2` must also be relatively prime to the table capacity to ensure it can visit every slot.

3. Which collision resolution strategy does Python's `dict` actually use?
   Answer: It uses a highly customized version of Open Addressing. It uses a pseudo-random number generator (seeded by the hash of the key) to determine the next jump sequence. It acts very much like Double Hashing, but optimized heavily for C arrays.
"""

if __name__ == "__main__":
    explain_load_factor()
    demonstrate_quadratic_probing()
    demonstrate_double_hashing()
    print("\n[SUCCESS] Laboratory: Advanced Collision Handling Completed.")
