"""
## A. Concept Name
Prime Numbers and Primality Testing

## B. Core Logic
Understanding how to efficiently check if a number is prime and how to generate all primes up to a limit using the Sieve of Eratosthenes.

## C. Code Examples
The implementation provides `is_prime` for O(sqrt(N)) primality testing and `sieve_of_eratosthenes` for O(N log log N) prime generation.

## D. Common Pitfalls
- Iterating up to N instead of sqrt(N) for primality checks.
- Not handling edge cases like numbers less than or equal to 1.

## X. Project Connection
Prime numbers are fundamental for cryptography (e.g., RSA), hash functions, and competitive programming algorithms.
"""

import math

def is_prime(n: int) -> bool:
    """Check if a number is prime."""
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    
    limit = int(math.sqrt(n))
    for i in range(5, limit + 1, 6):
        if n % i == 0 or n % (i + 2) == 0:
            return False
            
    return True

def sieve_of_eratosthenes(limit: int) -> list[int]:
    """Generate all primes up to 'limit' using Sieve of Eratosthenes."""
    if limit < 2:
        return []
        
    sieve = [True] * (limit + 1)
    sieve[0] = sieve[1] = False
    
    for p in range(2, int(math.sqrt(limit)) + 1):
        if sieve[p]:
            for i in range(p * p, limit + 1, p):
                sieve[i] = False
                
    return [p for p in range(limit + 1) if sieve[p]]

if __name__ == "__main__":
    print("Testing is_prime(29):", is_prime(29))
    print("Primes up to 50:", sieve_of_eratosthenes(50))
