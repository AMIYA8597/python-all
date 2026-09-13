"""
# ==============================================================================
# LABORATORY: PSEUDO-RANDOM NUMBER GENERATION (PRNG & CSPRNG)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Computers are fundamentally deterministic machines. If you give a CPU the exact 
# same inputs, it mathematically must return the exact same outputs. 
# 
# How does a computer generate a "Random" number for a video game or Monte Carlo 
# simulation? It cheats! 
# 
# The Python `random` module uses the "Mersenne Twister" algorithm. It is a 
# Pseudo-Random Number Generator (PRNG). It starts with a hidden "Seed" (usually 
# the current system time in nanoseconds). It runs that seed through a massive, 
# chaotic mathematical equation to generate a sequence of numbers that *appear* 
# to have no pattern.
#
# CRITICAL SECURITY WARNING:
# Because the Mersenne Twister is just a mathematical equation, if a hacker 
# observes 624 random numbers from your server, they can reverse-engineer the 
# state of the equation and perfectly predict every future "random" number your 
# server will ever generate! 
# YOU MUST NEVER USE THE `random` MODULE FOR PASSWORDS OR CRYPTOGRAPHY!
#
# For security, you must use the `secrets` module, which taps directly into 
# your Operating System's hardware-level cryptographic entropy pool (CSPRNG).
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand PRNG Determinism using `random.seed()`.
# - Execute sampling, shuffling, and probabilistic distributions.
# - Generate secure cryptographic tokens using the `secrets` module.
#
# ==============================================================================
"""

import random
import secrets

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. DETERMINISM AND THE MERSENNE TWISTER
# ==============================================================================
def demonstrate_determinism():
    section_header("Determinism & Seeding")
    
    print("If we 'seed' the PRNG with a hardcoded number, the resulting chaotic ")
    print("sequence is mathematically forced to be perfectly identical every time!\n")
    
    random.seed(42)
    print("Seeded with 42:")
    print(f"Roll 1: {random.randint(1, 100)}") # Always 82
    print(f"Roll 2: {random.randint(1, 100)}") # Always 15
    print(f"Roll 3: {random.randint(1, 100)}") # Always 4
    
    print("\nRe-seeding with 42 resets the mathematical equation:")
    random.seed(42)
    print(f"Roll 1: {random.randint(1, 100)}") # 82 again!
    
    # Best Practice: Always clear the seed when done to restore true chaos!
    random.seed(None) # Reseeds using OS Time


# ==============================================================================
# 4. RANDOM SAMPLING AND SHUFFLING
# ==============================================================================
def demonstrate_sequences():
    section_header("Sequence Randomization")
    
    deck = ["Ace", "King", "Queen", "Jack", "Ten"]
    print(f"Original Deck: {deck}")
    
    # 1. SHUFFLE (In-Place Mutation)
    # Uses the Fisher-Yates shuffle algorithm. O(N) time complexity!
    random.shuffle(deck)
    print(f"Shuffled Deck: {deck}")
    
    # 2. CHOICE (Pick 1 element)
    print(f"Random single draw: {random.choice(deck)}")
    
    # 3. CHOICES (Pick N elements WITH replacement)
    # It might pick "Ace" 3 times!
    print(f"Pick 3 (With Replacement)   : {random.choices(deck, k=3)}")
    
    # 4. SAMPLE (Pick N elements WITHOUT replacement)
    # Guaranteed unique elements. Will raise error if k > len(deck)
    print(f"Pick 3 (Without Replacement): {random.sample(deck, k=3)}")


# ==============================================================================
# 5. PROBABILITY DISTRIBUTIONS
# ==============================================================================
def demonstrate_distributions():
    section_header("Probability Distributions")
    
    # 1. UNIFORM DISTRIBUTION
    # Every decimal float between A and B has exactly equal probability.
    print(f"Uniform Float [1.0, 5.0]: {random.uniform(1.0, 5.0):.4f}")
    
    # 2. GAUSSIAN (NORMAL) DISTRIBUTION
    # The Bell Curve! (mu = Mean, sigma = Standard Deviation).
    # e.g., Generating heights of adult men (Mean 70 inches, SD 3 inches).
    print(f"Gaussian (Normal) Float : {random.gauss(mu=70.0, sigma=3.0):.4f}")


# ==============================================================================
# 6. SECURE HARDWARE CHAOS (THE `secrets` MODULE)
# ==============================================================================
def demonstrate_cryptography():
    section_header("Cryptographically Secure RNG (CSPRNG)")
    
    print("The `secrets` module bypasses the predictable Mersenne Twister equation.")
    print("It asks the Operating System (Windows CryptGenRandom or Linux /dev/urandom) ")
    print("for pure hardware entropy (e.g., microscopic voltage fluctuations in the CPU).\n")
    
    # Generating a massive hex token for a Password Reset link or API Key!
    secure_token = secrets.token_hex(32) # 32 bytes = 64 hex characters
    print(f"Secure Password Reset Token: {secure_token}")
    
    # Generating a highly secure URL-safe Base64 token
    url_token = secrets.token_urlsafe(32)
    print(f"Secure URL-safe Token      : {url_token}")
    
    # Picking a secure random choice (e.g. generating a secure password)
    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*"
    secure_password = ''.join(secrets.choice(alphabet) for _ in range(16))
    print(f"Hardware-Generated Password: {secure_password}")


def run_all_labs():
    demonstrate_determinism()
    demonstrate_sequences()
    demonstrate_distributions()
    demonstrate_cryptography()


# ==============================================================================
# 7. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why does `random.seed(42)` force the output to be identical every time?
   Answer: The Python `random` module uses the Mersenne Twister PRNG. A PRNG is fundamentally not random; it is a complex, deterministic mathematical formula. The "Seed" is the initial variable injected into the formula. If you provide the exact same initial mathematical variable (`42`), the equation is forced to compute the exact same subsequent sequence of values. (This is incredibly useful for writing Unit Tests or reproducing Machine Learning training runs!).

2. If the `secrets` module is perfectly secure, why don't we use it for everything?
   Answer: Performance and Hardware Limits! The `secrets` module is a CSPRNG. It physically requests hardware entropy from the Operating System. This requires crossing the software/hardware boundary, which is extremely slow compared to just evaluating a mathematical equation in CPU cache. Additionally, the OS only has a limited "pool" of hardware entropy (collected from mouse movements, network timings, etc.). If you drain the pool too fast, the OS will block your thread until it can generate more entropy! We use `random` for speed (Games/Simulations), and `secrets` for security (Cryptography/Passwords).

3. What is the difference between `random.choices()` and `random.sample()`?
   Answer: `random.choices(data, k=3)` samples WITH replacement. It is like rolling a 6-sided die three times; you could roll `[5, 5, 5]`. `random.sample(data, k=3)` samples WITHOUT replacement. It is like dealing three cards from a standard deck. It is physically impossible to deal the Ace of Spades twice. The output is guaranteed to contain mathematically unique items.
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Pseudo-Random Number Generation Completed.")
