"""
# ==============================================================================
# LABORATORY: HASH FUNCTIONS & SECURITY
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You know that Hash Tables require a "Hash Function" to convert a Key into an 
# integer. But writing a GOOD Hash Function is incredibly difficult.
# 
# If your hash function is bad (e.g., just adding up the ASCII values of the 
# string), then "cat" (99+97+116=312) and "act" (97+99+116=312) will collide. 
# If too many items collide, your O(1) Hash Table degrades into an O(N) Linked 
# List!
#
# Furthermore, if an attacker knows your Hash Function, they can intentionally 
# send you 100,000 strings that ALL collide to the exact same index. This freezes 
# your server (a Hash DoS attack). Python 3.3+ solved this by randomly seeding 
# the `hash()` function every time Python starts!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the 4 rules of a good Hash Function.
# - Implement a Polynomial Rolling Hash (used in Rabin-Karp).
# - Understand Hash DoS Attacks and Python's SIPHash.
#
# ==============================================================================
"""

import hashlib
import sys

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. IMPLEMENTING A POLYNOMIAL ROLLING HASH
# ==============================================================================
def polynomial_rolling_hash(s: str) -> int:
    """
    A classic, highly effective hash function for strings.
    Instead of just adding ASCII values (where "cat" == "act"), we multiply 
    each character by a prime number raised to a power based on its position.
    
    Formula: (s[0]*P^0 + s[1]*P^1 + s[2]*P^2 ...) % M
    
    P (Prime multiplier): Usually 31 or 53. (31 is good for lowercase english).
    M (Modulo): A large prime number to prevent integer overflow (e.g., 10^9 + 9).
    """
    P = 31
    M = 10**9 + 9
    
    hash_value = 0
    p_power = 1
    
    for char in s:
        # ord() gets the ASCII integer of the character (e.g., 'a' = 97)
        # We subtract 96 so 'a' = 1, 'b' = 2, etc. (Optional, but keeps numbers smaller)
        char_val = ord(char) - ord('a') + 1
        
        # Add to hash value
        hash_value = (hash_value + char_val * p_power) % M
        
        # Increase the power of P for the next character
        p_power = (p_power * P) % M
        
    return hash_value

def demonstrate_polynomial_hash():
    section_header("Algorithm: Polynomial Rolling Hash")
    
    # 1. Basic Addition Hash (BAD)
    print("If we use a BAD hash function (sum of ASCII):")
    print(f" 'cat' -> {sum(ord(c) for c in 'cat')}")
    print(f" 'act' -> {sum(ord(c) for c in 'act')}")
    print("  -> COLLISION!\n")
    
    # 2. Polynomial Rolling Hash (GOOD)
    print("If we use the Polynomial Rolling Hash (Position matters):")
    hash_cat = polynomial_rolling_hash('cat')
    hash_act = polynomial_rolling_hash('act')
    
    print(f" 'cat' -> {hash_cat}")
    print(f" 'act' -> {hash_act}")
    print("  -> NO COLLISION! The prime multiplier separated them.")


# ==============================================================================
# 4. PYTHON'S HASH() & SIPHASH (SECURITY)
# ==============================================================================
def explain_python_hash():
    section_header("Security: The Hash DoS Attack")
    print("""
Prior to Python 3.3, `hash("apple")` ALWAYS returned the exact same integer on 
every computer in the world.

ATTACK SCENARIO:
1. An attacker downloads Python 3.2.
2. They write a script to find 100,000 different strings that ALL hash to 
   the exact same index in a dictionary of size 100,000.
3. They send a JSON payload with those 100,000 keys to your Python web server.
4. Your server tries to parse the JSON into a dictionary.
5. EVERY SINGLE KEY collides at index 0.
6. The O(1) Hash Table becomes an O(N) Linked List of length 100,000.
7. Inserting 100k items into a 100k Linked List takes O(N^2) time (10 Billion operations).
8. Your server CPU hits 100% and crashes. (Hash Denial of Service Attack).

THE FIX (SIPHASH):
In Python 3.3+, when the Python interpreter starts, it generates a RANDOM internal 
seed. The built-in `hash()` function uses this seed.
""")
    
    val = "apple"
    print(f"If you restart this script, the hash of '{val}' will change every time!")
    print(f"Current hash('{val}'): {hash(val)}")
    
    print("\nBecause the seed is random and secret, the attacker cannot pre-calculate collisions!")


# ==============================================================================
# 5. CRYPTOGRAPHIC VS NON-CRYPTOGRAPHIC
# ==============================================================================
def demonstrate_hash_types():
    section_header("Concept: Cryptographic vs Non-Cryptographic")
    
    print("1. Non-Cryptographic (MurmurHash, CityHash, Python's SipHash)")
    print("   Goal: Blistering fast, evenly distributed, used for Hash Tables.")
    print("   Reversibility: Easy to reverse or intentionally cause collisions if you know the seed.")
    
    print("\n2. Cryptographic (SHA-256, SHA-3, Argon2)")
    print("   Goal: The Avalanche Effect (changing 1 bit changes 50% of the output).")
    print("   Goal: Pre-image resistance (mathematically impossible to reverse).")
    print("   Goal: Collision resistance (mathematically impossible to find two strings with the same hash).")
    print("   Speed: INTENTIONALLY SLOW. Used for passwords and blockchain.")
    
    # Example of SHA-256 Avalanche Effect
    s1 = "The quick brown fox jumps over the lazy dog."
    s2 = "The quick brown fox jumps over the lazy dog" # Removed the period
    
    hash1 = hashlib.sha256(s1.encode()).hexdigest()
    hash2 = hashlib.sha256(s2.encode()).hexdigest()
    
    print("\nDemonstrating the Avalanche Effect (SHA-256):")
    print(f"String 1: {s1}")
    print(f"Hash 1  : {hash1}")
    print(f"\nString 2: {s2}")
    print(f"Hash 2  : {hash2}")
    print("\nNotice how removing ONE period completely and unpredictably scrambled the entire hash.")


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why does the Polynomial Rolling Hash multiply by a Prime Number (like 31)?
   Answer: Prime numbers minimize common factors when using the modulo operator. If you multiply by an even number (like 32), the bitwise shifting causes data loss (zeros fill the right side), increasing collisions. A prime number mathematically ensures that the resulting bits are distributed as uniformly and randomly as possible.

2. Why can't we use SHA-256 for a Hash Table dictionary?
   Answer: SHA-256 is mathematically designed to be slow to prevent brute-force password cracking. A dictionary requires millions of lookups per second. A non-cryptographic hash (like SipHash) is thousands of times faster, which is what `dict` needs.

3. Why is `hash(10)` exactly `10` in Python, but `hash("10")` is a massive random number?
   Answer: For small integers, the most perfectly uniform, collision-free hash function is simply the integer itself! `hash(x) == x` for integers is a massive performance optimization in Python. Strings are complex, so they must be passed through SipHash.
"""

if __name__ == "__main__":
    demonstrate_polynomial_hash()
    explain_python_hash()
    demonstrate_hash_types()
    print("\n[SUCCESS] Laboratory: Hash Functions & Security Completed.")
