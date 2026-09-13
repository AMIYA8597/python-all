"""
# ==============================================================================
# LABORATORY: DISTRIBUTED HASH TABLES (CHORD & FINGER TABLES)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You learned about Consistent Hashing, where servers and data are placed on a 
# Hash Ring. That works perfectly for a Redis cluster inside an AWS datacenter, 
# because every server knows the exact location of every other server.
#
# But what if you are building BitTorrent, with millions of anonymous laptops 
# connecting and disconnecting worldwide? No single laptop can possibly memorize 
# the IP addresses of the entire hash ring! 
#
# "Distributed Hash Tables" (DHTs) solve this. The most famous implementation is 
# the "Chord Protocol". 
# In Chord, each node only knows about its immediate successor (the next node) 
# and a small "Finger Table" (O(log N) nodes exponentially far away). 
# This allows any node in a million-node network to route a request to the correct 
# destination in exactly O(log N) hops!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the difference between Consistent Hashing (Centralized) and DHTs (Decentralized).
# - Understand the Chord Ring (modulo 2^M).
# - Implement a Finger Table for O(log N) routing.
#
# ==============================================================================
"""

import math
from typing import List, Optional

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE CHORD PROTOCOL & FINGER TABLES
# ==============================================================================
def explain_chord_protocol():
    section_header("Concept: The Chord Ring & O(log N) Routing")
    print("""
Imagine a Hash Ring from 0 to 63 (M = 6 bits).
We have 3 computers online: Node 10, Node 32, and Node 45.

If Node 10 is looking for Data Key 40, who has it?
Data flows clockwise, so Data 40 belongs to Node 45!

But Node 10 doesn't know Node 45 exists! It only knows its immediate neighbor.
If we only used neighbors, routing would take O(N) hops. (10 asks 32, 32 asks 45).

FINGER TABLES:
Node 10 maintains a table of nodes at exponentially increasing distances:
- Finger 1: Node closest to (10 + 2^0) = 11
- Finger 2: Node closest to (10 + 2^1) = 12
- Finger 3: Node closest to (10 + 2^2) = 14
- Finger 4: Node closest to (10 + 2^3) = 18
- Finger 5: Node closest to (10 + 2^4) = 26
- Finger 6: Node closest to (10 + 2^5) = 42

When Node 10 wants to find Data 40, it looks at its Finger Table.
It sees Finger 6 points to a node that covers region 42. That is extremely close 
to 40! So it instantly forwards the request halfway across the world.
This guarantees O(log N) routing!
    """)


# ==============================================================================
# 4. IMPLEMENTING A DHT NODE
# ==============================================================================
class DHTNode:
    """Represents a single computer in the Peer-to-Peer network."""
    def __init__(self, node_id: int, ring_size: int = 64):
        self.id = node_id
        self.m = int(math.log2(ring_size)) # Number of bits
        self.ring_size = ring_size
        
        # In a real DHT, this would be an IP address over the network.
        self.successor: Optional['DHTNode'] = None
        
        # The Finger Table: A list of DHTNode references
        self.finger_table: List[Optional['DHTNode']] = [None] * self.m

    def in_range(self, key: int, start: int, end: int, inclusive_end: bool = False) -> bool:
        """
        Helper function to handle circular ring logic.
        Checks if `key` is between `start` and `end` on the circle.
        """
        if start < end:
            return start < key < end or (inclusive_end and key == end)
        elif start > end:
            # Wrapped around 0
            return start < key or key < end or (inclusive_end and key == end)
        else: # start == end (Only 1 node in the entire network)
            return True

    def closest_preceding_node(self, key: int) -> 'DHTNode':
        """
        Scans the Finger Table backwards to find the node closest to the target Key,
        without overshooting the key!
        """
        for i in range(self.m - 1, -1, -1):
            finger = self.finger_table[i]
            if finger is not None and self.in_range(finger.id, self.id, key):
                return finger
        # If no finger is closer, we are the closest preceding node!
        return self

    def find_successor(self, key: int) -> 'DHTNode':
        """
        The core routing algorithm.
        Finds the absolute node responsible for the given key.
        """
        # If the key falls between us and our immediate successor, our successor owns it!
        if self.in_range(key, self.id, self.successor.id, inclusive_end=True):
            print(f"   [Node {self.id}] My successor {self.successor.id} owns key {key}!")
            return self.successor
            
        # Otherwise, find the closest node in our Finger Table and ask them to route it!
        closest = self.closest_preceding_node(key)
        
        # Edge case: If we are the closest, ask our successor
        if closest.id == self.id:
            return self.successor.find_successor(key)
            
        print(f"   [Node {self.id}] Forwarding request for {key} to Node {closest.id}")
        return closest.find_successor(key)

def demonstrate_chord_routing():
    section_header("Algorithm: Chord Protocol Routing")
    
    # Create a 64-node ring
    n1 = DHTNode(1, ring_size=64)
    n10 = DHTNode(10, ring_size=64)
    n32 = DHTNode(32, ring_size=64)
    n45 = DHTNode(45, ring_size=64)
    
    # Manually link successors (in reality, protocols handle this automatically when joining)
    n1.successor = n10
    n10.successor = n32
    n32.successor = n45
    n45.successor = n1
    
    # Manually populate Node 10's finger table for demonstration
    # (10 + 2^0) = 11 -> Belongs to 32
    # (10 + 2^1) = 12 -> Belongs to 32
    # (10 + 2^2) = 14 -> Belongs to 32
    # (10 + 2^3) = 18 -> Belongs to 32
    # (10 + 2^4) = 26 -> Belongs to 32
    # (10 + 2^5) = 42 -> Belongs to 45!
    
    n10.finger_table[0] = n32
    n10.finger_table[1] = n32
    n10.finger_table[2] = n32
    n10.finger_table[3] = n32
    n10.finger_table[4] = n32
    n10.finger_table[5] = n45
    
    print("Ring Topology: Node 1 -> Node 10 -> Node 32 -> Node 45 -> Node 1")
    print("\nRouting Test 1: Node 10 searches for Key 30")
    print("Expected: Key 30 falls between 10 and 32. So Node 32 owns it.")
    owner = n10.find_successor(30)
    print(f"Result: Node {owner.id} found!")
    
    print("\nRouting Test 2: Node 10 searches for Key 44")
    print("Expected: Node 10 doesn't know who owns 44, but its Finger 5 points to 45.")
    owner = n10.find_successor(44)
    print(f"Result: Node {owner.id} found!")


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why does Chord use an exponential distance `(ID + 2^i)` for Finger Tables?
   Answer: If a node only knew its neighbors, routing across a million nodes would take 500,000 hops on average. By storing pointers that jump halfway across the ring, then a quarter of the way, then an eighth, the routing algorithms perfectly mimics Binary Search! This guarantees any node can be found in exactly O(log N) hops.

2. In a real P2P network, how do Finger Tables handle computers disconnecting?
   Answer: Every node runs a background thread called `fix_fingers()`. It continuously pings the nodes in its Finger Table to verify they are online. If a node goes offline, the finger table is updated to point to the next alive successor in that region.

3. How is BitTorrent's "Mainline DHT" related to this?
   Answer: BitTorrent uses Kademlia, which is extremely similar to Chord but uses the XOR metric for distance instead of clockwise subtraction. When you open a magnet link, your client uses the DHT (which contains millions of peers) to find the IPs of the few specific computers hosting the file you want, completely bypassing central servers.
"""

if __name__ == "__main__":
    explain_chord_protocol()
    demonstrate_chord_routing()
    print("\n[SUCCESS] Laboratory: Distributed Hash Tables Completed.")
