"""
# ==============================================================================
# LABORATORY: SYSTEM DESIGN (ALGORITHMIC OPTIMIZATION)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# System Design is not just drawing boxes on a whiteboard. It requires 
# highly advanced algorithmic engines under the hood.
#
# Scenario A: You have a database of 10 Billion malicious URLs. When a user 
# clicks a link, you must check if it is malicious. Doing a SQL `SELECT` takes 
# 10ms. Too slow. Caching 10 Billion strings in Redis requires 500 GB of RAM. 
# Too expensive. You must use a "Bloom Filter" to mathematically compress the 
# 10 Billion URLs into a 2 GB bit-array that can be queried in 0.01ms!
#
# Scenario B: You sharded your database across 4 servers using `Hash(id) % 4`. 
# Server 1 crashes. You now have 3 servers. If you do `Hash(id) % 3`, the 
# destination for EVERY SINGLE USER mathematically changes. You would have to 
# migrate 100% of your data across the network, causing a total system outage.
# You must use "Consistent Hashing" to map servers onto a mathematical ring, 
# ensuring that if a server dies, only 1/N of the data moves!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master Consistent Hashing (The Hash Ring).
# - Understand Virtual Nodes in Consistent Hashing.
# - Master Bloom Filters (Probabilistic Set Membership).
#
# ==============================================================================
"""

import hashlib
import bisect

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. CONSISTENT HASHING (THE RING)
# ==============================================================================
class ConsistentHashingRing:
    """
    Solves the "Resharding Nightmare".
    Instead of `hash % N`, we map both Servers AND Data onto a massive 
    mathematical ring (0 to 2^256-1). Data belongs to the first Server it hits 
    by walking clockwise around the ring!
    """
    def __init__(self, num_replicas: int = 3):
        # num_replicas = Virtual Nodes! 
        # If we only place 3 physical servers on a massive ring, they might clump 
        # together, causing uneven load. We create N "Virtual" copies of each server 
        # to spread them evenly across the mathematical space!
        self.num_replicas = num_replicas
        
        # A sorted list of hash values (The Ring!)
        self.ring = []
        # Maps a hash value on the ring to the actual physical server name
        self.hash_to_server = {}

    def _hash(self, key: str) -> int:
        """Cryptographic hash to map a string to a massive integer space."""
        return int(hashlib.md5(key.encode()).hexdigest(), 16)

    def add_server(self, server_name: str) -> None:
        """Places a server (and its virtual clones) onto the ring."""
        for i in range(self.num_replicas):
            virtual_node_name = f"{server_name}_Virtual_{i}"
            ring_position = self._hash(virtual_node_name)
            
            self.ring.append(ring_position)
            self.hash_to_server[ring_position] = server_name
            
        # The ring must remain strictly sorted to allow Binary Search (Clockwise walking)!
        self.ring.sort()
        print(f"[RING] Added Server: {server_name} (with {self.num_replicas} Virtual Nodes)")

    def remove_server(self, server_name: str) -> None:
        """Violently removes a server from the ring."""
        for i in range(self.num_replicas):
            virtual_node_name = f"{server_name}_Virtual_{i}"
            ring_position = self._hash(virtual_node_name)
            
            self.ring.remove(ring_position)
            del self.hash_to_server[ring_position]
            
        print(f"[RING] [WARNING] Server {server_name} CRASHED and was removed!")

    def get_server_for_data(self, data_key: str) -> str:
        """
        Maps Data onto the ring, then walks clockwise to find the first server!
        Uses Binary Search (bisect) for O(log V) speed!
        """
        if not self.ring: return "None"
        
        data_position = self._hash(data_key)
        
        # Binary search to find the first server position >= data position
        idx = bisect.bisect_right(self.ring, data_position)
        
        # If we went past the end of the list, wrap around to the beginning (Clockwise Ring!)
        if idx == len(self.ring):
            idx = 0
            
        server_position = self.ring[idx]
        return self.hash_to_server[server_position]

def demonstrate_consistent_hashing():
    section_header("Consistent Hashing (Distributed DBs)")
    
    ch = ConsistentHashingRing(num_replicas=3)
    ch.add_server("DB-Alpha")
    ch.add_server("DB-Beta")
    ch.add_server("DB-Gamma")
    
    data_keys = ["user_1", "user_2", "user_3", "user_4", "user_5"]
    print("\nInitial Routing:")
    for key in data_keys:
        print(f"  {key} -> {ch.get_server_for_data(key)}")
        
    print("\nDISASTER STRIKES! DB-Beta catches fire.")
    ch.remove_server("DB-Beta")
    
    print("\nNew Routing after crash:")
    for key in data_keys:
        print(f"  {key} -> {ch.get_server_for_data(key)}")
        
    print("\nNotice that users who were on DB-Alpha or DB-Gamma did NOT MOVE!")
    print("Only the users on the dead DB-Beta migrated. Massive data migration averted!")


# ==============================================================================
# 4. BLOOM FILTERS (PROBABILISTIC DATA STRUCTURES)
# ==============================================================================
class BloomFilter:
    """
    A Probabilistic Set. 
    It can tell you if an item is "Definitely NOT in the set" (100% accurate).
    It can tell you if an item is "PROBABLY in the set" (e.g., 99% accurate).
    It achieves this by replacing Strings with Hash bits, saving 99% of RAM!
    """
    def __init__(self, size: int):
        self.size = size
        # A raw bit array (simulated with a list of booleans)
        self.bit_array = [False] * size

    def _hash_1(self, item: str) -> int:
        return int(hashlib.md5(item.encode()).hexdigest(), 16) % self.size

    def _hash_2(self, item: str) -> int:
        return int(hashlib.sha1(item.encode()).hexdigest(), 16) % self.size
        
    def _hash_3(self, item: str) -> int:
        return int(hashlib.sha256(item.encode()).hexdigest(), 16) % self.size

    def add(self, item: str) -> None:
        """To add an item, pass it through multiple hash functions and flip the bits to True!"""
        self.bit_array[self._hash_1(item)] = True
        self.bit_array[self._hash_2(item)] = True
        self.bit_array[self._hash_3(item)] = True

    def check(self, item: str) -> str:
        """
        To check an item, pass it through the hashes. 
        If ANY bit is False, the item is DEFINITELY NOT in the filter!
        If ALL bits are True, the item is PROBABLY in the filter! (False Positives exist).
        """
        b1 = self.bit_array[self._hash_1(item)]
        b2 = self.bit_array[self._hash_2(item)]
        b3 = self.bit_array[self._hash_3(item)]
        
        if not b1 or not b2 or not b3:
            return "DEFINITELY NOT IN SET (100% Guarantee)"
        else:
            return "PROBABLY IN SET (Potential False Positive)"

def demonstrate_bloom_filter():
    section_header("Bloom Filters (Ultra-Fast RAM Caching)")
    
    # 20 bit array! In reality, this would be billions of bits.
    bf = BloomFilter(size=20)
    
    print("Database of known Malicious URLs:")
    malicious = ["evil.com", "phishing.org"]
    for m in malicious:
        bf.add(m)
        print(f"  Added: {m}")
        
    print("\nIncoming User Clicks:")
    
    test_1 = "google.com"
    print(f"Check '{test_1}': {bf.check(test_1)}")
    # Because it returns "Definitely Not", we allow the user to proceed instantly!
    # We saved a 50ms database lookup!
    
    test_2 = "evil.com"
    print(f"Check '{test_2}': {bf.check(test_2)}")
    # Because it returns "Probably", we halt the user! We then do a slow, careful 
    # SQL query to 100% confirm it. But we only do the slow query when absolutely necessary!


def run_all_labs():
    demonstrate_consistent_hashing()
    demonstrate_bloom_filter()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Explain the "Resharding Nightmare" in Modulo Hashing, and how Consistent Hashing fixes it.
   Answer: In Modulo Hashing (`hash % N`), the divisor `N` is hardcoded. If you have 4 servers and one dies, `N` becomes 3. Suddenly, `hash % 3` produces completely different answers for *every single piece of data in the system*. 100% of your data must physically migrate across the network. Consistent Hashing fixes this by abandoning the divisor. It places servers on a massive $360^\circ$ ring (0 to $2^{256}$). Data is hashed onto the ring, and simply walks clockwise to the nearest server. If a server dies, only the specific block of data it was holding walks clockwise to the next surviving server. The other 99% of the ring is completely undisturbed!

2. Why are "Virtual Nodes" absolutely critical for Consistent Hashing?
   Answer: Cryptographic hashes are random. If you only place 3 physical servers on a $360^\circ$ ring, by pure chance, they might land at $10^\circ$, $15^\circ$, and $20^\circ$. They are clumped together! The server at $10^\circ$ will handle the entire $350^\circ$ gap behind it, receiving 99% of the world's traffic and instantly melting, while the others sit idle. By giving each physical server 1,000 "Virtual" clones and randomly scattering all 3,000 clones across the ring, the mathematical law of large numbers guarantees an ultra-smooth, perfectly even distribution of traffic.

3. How does a Bloom Filter save RAM, and why must you accept "False Positives"?
   Answer: Storing the string "https://www.verylongmaliciousurl.com" takes 50 bytes. Storing 10 Billion of them takes 500 GB of RAM. A Bloom Filter abandons the strings. It hashes the string into 3 random integer indices and flips 3 microscopic Bits to `1`. It compresses 50 bytes into 3 bits! However, because you are cramming data into a finite bit-array, eventually two completely innocent URLs might coincidentally hash to the exact same 3 bits that an evil URL previously flipped to `1`. The filter sees the `1`s and screams "Malicious!". This is a False Positive. The Bloom Filter is mathematically incapable of False Negatives, but it mandates handling False Positives.
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: System Design (Algorithmic Optimization) Completed.")
