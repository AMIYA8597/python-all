"""
## A. Concept Name
Distributed Hashing

## B. Motivation
As systems scale beyond a single machine, a single hash table cannot hold all data. Distributed hashing enables the distribution of data across multiple nodes seamlessly.

## C. Learning Objectives
1. Understand distributed hashing beyond simple modulus.
2. Implement a basic Distributed Hash Table (DHT) abstraction.
3. Understand routing and key placement in a network of nodes.

## D. Concept Explanation
Distributed hashing allows multiple nodes in a network to form a unified hash table. Each node is responsible for a portion of the hash space. Algorithms like Chord use a ring topology and consistent hashing to efficiently locate the node responsible for any given key.

## E. Real-World Analogy
Imagine a library where books are distributed across multiple branch libraries. A master index (or consistent rule) tells you exactly which branch holds the book you need without having to search all branches.

## F. System Architecture
A peer-to-peer network of DHT nodes where each node is assigned a unique identifier in the hash space. 

## G. Core Mechanism
Hashing both keys and node IDs into the same hash space (e.g., a ring). Keys are assigned to the node whose hash ID is equal to or immediately follows the key's hash ID.

## H. Performance Analysis (Time & Space Complexity)
- Time Complexity: O(N) to find a node in this naive linear implementation. Advanced implementations like Chord achieve O(log N) routing.
- Space Complexity: O(K) where K is the number of keys stored per node. Overall network space is O(Total Keys).

## I. Edge Cases & Handling
- Node failures: Addressed by data replication across successor nodes.
- Network partitions: Addressed by eventual consistency protocols.

## J. Scalability & Distribution
New nodes can join the network with minimal disruption, as only a small fraction of keys (from the immediate successor) need to be reassigned.

## K. Common Pitfalls
- Unbalanced hash spaces leading to hot spots.
- Ignoring virtual nodes, which help balance the load evenly.

## L. Best Practices
Use virtual nodes (vnodes) to ensure an even distribution of the keyspace even if physical nodes are few.

## M. Troubleshooting & Debugging
Log node join/leave events and verify key redistribution to ensure no data is lost during transitions.

## N. Alternative Approaches
Centralized directory servers (like early Napster) or master-worker topologies, which have single points of failure compared to DHTs.

## O. Test Cases & Validation
- Validating correct node assignment for given keys.
- Checking data retrieval matches data stored.

## P. Interview Challenge
Design the finger table for a Chord DHT node to improve routing from O(N) to O(log N).

## Q. Code Implementation Details
The `DHTNode` class handles individual storage. The `SimpleDHTNetwork` manages routing.

## R. Deployment Considerations
Nodes must have stable IDs and reliable heartbeat mechanisms to detect departures.

## S. Security Implications
Sybil attacks where a malicious user creates many nodes to control the DHT. Addressed by tying node IDs to IP addresses or certificates.

## T. Future Enhancements
Implement a real `O(log N)` routing mechanism (Chord/Kademlia) and data replication.

## U. Glossary of Terms
- DHT: Distributed Hash Table
- Node ID: Unique identifier for a machine/process in the network.
- Consistent Hashing: A hashing technique that minimizes reorganization when nodes are added or removed.

## V. References & Further Reading
- "Chord: A Scalable Peer-to-peer Lookup Service for Internet Applications" by Stoica et al.

## W. Exercises & Challenges
Implement node removal and key handoff in the `SimpleDHTNetwork`.

## X. Project Connection
Distributed hashing is foundational for implementing highly available, scalable backend storage systems, caching layers (like Memcached architectures), and peer-to-peer networking in AI distributed training clusters.
"""

import hashlib

class DHTNode:
    def __init__(self, node_id: str):
        self.node_id = node_id
        self.hash_id = self._hash(node_id)
        self.data = {}

    def _hash(self, key: str) -> int:
        return int(hashlib.md5(key.encode()).hexdigest(), 16) % 1000

    def store(self, key: str, value: str):
        self.data[key] = value

    def retrieve(self, key: str) -> str:
        return self.data.get(key, None)

class SimpleDHTNetwork:
    def __init__(self):
        self.nodes = []

    def add_node(self, node: DHTNode):
        self.nodes.append(node)
        self.nodes.sort(key=lambda n: n.hash_id)

    def _hash(self, key: str) -> int:
        return int(hashlib.md5(key.encode()).hexdigest(), 16) % 1000

    def get_responsible_node(self, key: str) -> DHTNode:
        k_hash = self._hash(key)
        for node in self.nodes:
            if node.hash_id >= k_hash:
                return node
        return self.nodes[0] if self.nodes else None

# Tests
def test_distributed_hashing():
    network = SimpleDHTNetwork()
    n1, n2, n3 = DHTNode("Node1"), DHTNode("Node2"), DHTNode("Node3")
    network.add_node(n1)
    network.add_node(n2)
    network.add_node(n3)
    
    key = "user_data_abc"
    target_node = network.get_responsible_node(key)
    target_node.store(key, "value_abc")
    
    fetch_node = network.get_responsible_node(key)
    assert fetch_node.retrieve(key) == "value_abc"

if __name__ == "__main__":
    test_distributed_hashing()
    print("03-distributed-hashing.py tests passed successfully!")
