"""
# ==============================================================================
# LABORATORY: CONSISTENT HASHING & DISTRIBUTED SYSTEMS
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You are designing a massive Redis cache for a website. You have 3 Servers (A, B, C).
# To decide which server holds a user's data, you use standard hashing:
# `Server_Index = Hash(User_ID) % 3`
#
# Everything works perfectly, until Server C crashes. Now you have 2 servers.
# The math changes to: `Hash(User_ID) % 2`.
# Because the modulo changed, almost EVERY SINGLE USER now points to a different 
# server! Your entire cache is instantly invalidated, causing a massive traffic 
# spike that crashes your main database. (The "Thundering Herd" problem).
#
# "Consistent Hashing" solves this. Instead of modulo math on the number of servers, 
# both the Servers AND the Data are hashed onto a giant, fixed circular "Hash Ring" 
# (e.g., values 0 to 1,000,000). Data is assigned to the first Server it finds 
# by walking clockwise around the ring. 
# 
# If a server crashes, ONLY the data on that specific server is reassigned to the 
# next server in the ring. The rest of the cluster is completely unaffected!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the Flaw of Modulo Hashing in Distributed Systems.
# - Understand the Hash Ring and Clockwise routing.
# - Understand Virtual Nodes (VNodes) for load balancing.
# - Implement a Consistent Hashing ring using Binary Search (bisect).
#
# ==============================================================================
"""

import hashlib
import bisect

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. CONSISTENT HASH RING IMPLEMENTATION
# ==============================================================================
class ConsistentHashRing:
    def __init__(self, num_replicas: int = 3):
        """
        `num_replicas` represents "Virtual Nodes". 
        If we only put 3 physical servers on a massive ring, one server might 
        accidentally cover 70% of the ring, getting overloaded. 
        By creating multiple "Virtual Nodes" for each physical server and scattering 
        them around the ring, we ensure a perfectly even distribution of data!
        """
        self.num_replicas = num_replicas
        
        # The Hash Ring (A sorted list of massive integers)
        self.ring: list[int] = []
        
        # Maps the Ring Integer -> Physical Server Name
        self.server_map: dict[int, str] = {}

    def _hash(self, key: str) -> int:
        """Returns a 32-bit integer representing a position on the ring."""
        return int(hashlib.md5(key.encode('utf-8')).hexdigest(), 16)

    def add_server(self, server_name: str) -> None:
        """Adds a physical server (and its virtual replicas) to the ring."""
        for i in range(self.num_replicas):
            # Create a unique name for each virtual node (e.g., "ServerA-0", "ServerA-1")
            vnode_name = f"{server_name}-{i}"
            vnode_hash = self._hash(vnode_name)
            
            # Insert the hash into the sorted ring
            bisect.insort(self.ring, vnode_hash)
            
            # Map the hash back to the ACTUAL physical server
            self.server_map[vnode_hash] = server_name

    def remove_server(self, server_name: str) -> None:
        """Removes a physical server (and all its virtual replicas) from the ring."""
        for i in range(self.num_replicas):
            vnode_name = f"{server_name}-{i}"
            vnode_hash = self._hash(vnode_name)
            
            # Remove from ring
            self.ring.remove(vnode_hash)
            
            # Remove from map
            del self.server_map[vnode_hash]

    def get_server(self, data_key: str) -> str:
        """
        Routes the data to the correct server.
        1. Hashes the data onto the ring.
        2. Walks clockwise to find the first server.
        """
        if not self.ring:
            raise Exception("No servers in the ring!")
            
        data_hash = self._hash(data_key)
        
        # Binary Search to instantly find the first server hash that is GREATER 
        # than the data hash (Walking clockwise).
        index = bisect.bisect(self.ring, data_hash)
        
        # If the data hash is larger than the very last server on the ring, 
        # we wrap around to the beginning of the circle (index 0).
        if index == len(self.ring):
            index = 0
            
        server_hash = self.ring[index]
        return self.server_map[server_hash]

def demonstrate_consistent_hashing():
    section_header("Algorithm: Consistent Hashing (Distributed Systems)")
    
    # We use 100 virtual nodes per server to ensure smooth load balancing
    ring = ConsistentHashRing(num_replicas=100)
    
    print("Booting up Cluster with 3 Servers (A, B, C)...")
    ring.add_server("Server_A")
    ring.add_server("Server_B")
    ring.add_server("Server_C")
    
    users = ["Alice", "Bob", "Charlie", "David", "Eve", "Frank"]
    
    print("\nRouting Data (Steady State):")
    assignments = {}
    for user in users:
        server = ring.get_server(user)
        assignments[user] = server
        print(f" User '{user}' routed to -> {server}")
        
    print("\n[DISASTER STRÍKES!] Server B crashes and goes offline.")
    ring.remove_server("Server_B")
    
    print("\nRouting Data (After Crash):")
    for user in users:
        new_server = ring.get_server(user)
        
        if assignments[user] == "Server_B":
            print(f" User '{user}' gracefully reassigned to -> {new_server} (Data Migrated)")
        elif assignments[user] == new_server:
            print(f" User '{user}' STILL on -> {new_server} (Unaffected!)")
        else:
            print(f" User '{user}' moved from {assignments[user]} to {new_server} (THIS SHOULD NEVER HAPPEN!)")
            
    print("\nNotice that ONLY the users who were on Server B were moved! The users")
    print("on Server A and Server C stayed exactly where they were. The cache survives.")


# ==============================================================================
# 4. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why does standard modulo hashing (`Hash % N`) fail when a server is added or removed?
   Answer: Modulo math distributes items based on the denominator. If `100 % 3 = 1`, and you change it to `100 % 2 = 0`, the answer changes. When you add/remove a server, `N` changes, which recalculates the destination for nearly 100% of the keys, requiring the entire massive dataset to be migrated simultaneously.

2. How does Consistent Hashing minimize data movement?
   Answer: Instead of recalculating a modulo, the ring is a fixed circle (e.g., 0 to 2^32). A server crash just creates a "gap" in the circle. Only the data that was inside that gap flows clockwise to the next server. All other data on the ring remains perfectly stable. Only `1/N` of the data is moved!

3. Why are Virtual Nodes (VNodes) absolutely required for a production system?
   Answer: If you put exactly 3 physical servers on a giant hash ring, there is a very high probability they will clump together purely by random chance. Server A might own 80% of the circle, while B and C own 10%. By hashing 1,000 "Virtual Nodes" for Server A and scattering them everywhere, the law of large numbers guarantees a perfectly even 33/33/33 load distribution.
"""

if __name__ == "__main__":
    demonstrate_consistent_hashing()
    print("\n[SUCCESS] Laboratory: Consistent Hashing Completed.")
