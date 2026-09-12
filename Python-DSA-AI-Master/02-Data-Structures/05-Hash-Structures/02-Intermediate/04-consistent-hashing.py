"""
## A. Concept Name
Consistent Hashing

## B. Problem Statement
How do we distribute data across a dynamic set of nodes without needing to remap all keys when nodes are added or removed?

## C. Learning Objectives
1. Understand distributed hashing concepts.
2. Implement Consistent Hashing with virtual nodes.
3. Understand its application in load balancing and distributed caches.

## D. Concept Explanation
Consistent hashing maps keys and nodes to a circular hash space (a ring). When a node is added or removed, it minimizes the number of keys that need to be remapped. Virtual nodes are used to ensure uniform data distribution.

## E. Real-World Analogy
Imagine a roulette wheel where the numbers are servers and the ball is a piece of data. When data arrives, it spins around the wheel and stops at the closest server going clockwise.

## F. Core Principles
- Circular Hash Space
- Virtual Nodes
- Minimal data relocation

## G. Time Complexity
Add/Remove node O(V log(V*N)), Get Node O(log(V*N)) where V is virtual nodes and N is physical nodes.

## H. Space Complexity
O(V * N) to store the ring and node mappings.

## I. Edge Cases
- Ring with no nodes.
- Uneven distribution due to poor hash function (mitigated by virtual nodes).

## J. Performance Analysis
Consistent hashing scales well as the number of nodes increases. Lookups are fast (logarithmic) because of binary search.

## K. Interview Challenge
Design a distributed cache system using consistent hashing.

## L. Common Mistakes
- Not using virtual nodes, leading to skewed data distribution.
- Using a non-uniform hash function.

## M. Debugging Tips
Print the hash ring state to verify virtual nodes are well-distributed.

## N. Code Implementation Notes
We use `hashlib` for uniform hashing and `bisect` for fast logarithmic lookups in the sorted hash ring.

## O. Advanced Variations
- Bounded loads (Consistent Hashing with Bounded Load)
- Weighted virtual nodes based on server capacity.

## P. Real-World Application
Distributed caches (e.g., Memcached, Redis Cluster), Load balancers, CDNs.

## Q. Alternative Approaches
- Modulo hashing (poor for dynamic node sets)
- Rendezvous hashing

## R. FAQs
Q: Why do we need virtual nodes?
A: To balance the load across physical nodes more evenly.

## S. Prerequisites
- Hash functions
- Binary search

## T. Related Data Structures
- Hash Maps
- Binary Search Trees

## U. Further Reading
- Dynamo: Amazon's Highly Available Key-value Store paper.

## V. Glossary
- Virtual Node: A logical node mapped to a physical server.
- Hash Ring: The circular space of hash values.

## W. Summary
Consistent Hashing provides a scalable way to route requests or store data in a dynamic, distributed environment by minimizing re-hashing when scaling.

## X. Project Connection
This module serves as the foundational load distribution logic for building our scalable distributed AI cache project.
"""

import hashlib
import bisect
from typing import List

class ConsistentHashing:
    def __init__(self, num_replicas: int = 3):
        self.num_replicas = num_replicas
        self.ring: List[int] = []
        self.nodes: dict[int, str] = {}

    def _hash(self, key: str) -> int:
        return int(hashlib.md5(key.encode('utf-8')).hexdigest(), 16)

    def add_node(self, node: str) -> None:
        for i in range(self.num_replicas):
            virtual_node = f"{node}:{i}"
            hash_val = self._hash(virtual_node)
            self.nodes[hash_val] = node
            bisect.insort(self.ring, hash_val)

    def remove_node(self, node: str) -> None:
        for i in range(self.num_replicas):
            virtual_node = f"{node}:{i}"
            hash_val = self._hash(virtual_node)
            if hash_val in self.ring:
                self.ring.remove(hash_val)
            if hash_val in self.nodes:
                del self.nodes[hash_val]

    def get_node(self, key: str) -> str:
        if not self.ring:
            return ""
        hash_val = self._hash(key)
        idx = bisect.bisect(self.ring, hash_val)
        if idx == len(self.ring):
            idx = 0
        return self.nodes[self.ring[idx]]

def test_consistent_hashing():
    ch = ConsistentHashing(num_replicas=5)
    ch.add_node("NodeA")
    ch.add_node("NodeB")
    
    node = ch.get_node("user_123_data")
    assert node in ["NodeA", "NodeB"]
    
    ch.remove_node("NodeA")
    node2 = ch.get_node("user_123_data")
    assert node2 == "NodeB"

if __name__ == "__main__":
    test_consistent_hashing()
    print("04-consistent-hashing.py tests passed successfully!")
