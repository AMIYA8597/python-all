"""
## A. Concept Name
System Design Basics

## B. Why it exists
To introduce foundational concepts for designing large-scale distributed systems.

## C. Industry Use Cases
- Architecting scalable web services (e.g., Netflix, Uber).
- Designing fault-tolerant databases and caching layers.

## D. Learning Objectives
1. Understand core principles: Scalability, Availability, Reliability.
2. Master the CAP Theorem (Consistency, Availability, Partition Tolerance).
3. Learn standard components: Load Balancers, API Gateways, Caches, Message Queues, Databases (SQL vs NoSQL).
4. Implement a conceptual Load Balancer and Consistent Hashing scheme.

## E. Beginner Explanation
System design is like building a city. A single computer (server) is a house. As more people come, one house isn't enough. We need multiple houses (horizontal scaling), a traffic cop to direct people (Load Balancer), quick access to popular items (Cache), and a massive organized storage facility (Database).

## F. Advanced Explanation
Distributed systems inherently face network failures. The CAP theorem dictates that in the presence of a network partition (P), a system can only guarantee either Consistency (C) or Availability (A). 
Scaling involves Load Balancing (Round Robin, Least Connections) and Data Partitioning (Sharding). Consistent hashing minimizes key reassignment when nodes join or leave, making it ideal for distributed caches like Memcached or DynamoDB.

## G. Performance Considerations
- Caching: 80/20 rule. Caching the most accessed 20% of data can serve 80% of requests.
- Consistent Hashing: O(log N) lookup time for a node, reducing cache misses during rebalancing.

## H. Common Pitfalls
- Single Point of Failure (SPOF): Designing systems where the failure of one component brings down the whole system.
- Premature Optimization: Overcomplicating a system before understanding the actual bottlenecks.

## X. Project Connection
These principles form the foundation for designing robust applications and backend services capable of handling growing traffic and data volumes within real-world projects.
"""
import hashlib
import bisect
from typing import List, Dict, Callable

class LoadBalancer:
    """
    A conceptual Load Balancer using Round Robin scheduling.
    \"\"\"
    def __init__(self, servers: List[str]):
        self.servers = servers
        self.index = 0

    def get_server(self) -> str:
        if not self.servers:
            raise ValueError(\"No servers available\")
        server = self.servers[self.index]
        self.index = (self.index + 1) % len(self.servers)
        return server

class ConsistentHashRing:
    \"\"\"
    Professional Implementation of Consistent Hashing.
    Used for distributed caching to minimize key reassignment when nodes change.
    \"\"\"
    def __init__(self, replicas: int = 3):
        self.replicas = replicas
        self.ring: Dict[int, str] = {}
        self.sorted_keys: List[int] = []

    def _hash(self, key: str) -> int:
        # Use SHA-256 for a uniform distribution
        return int(hashlib.sha256(key.encode('utf-8')).hexdigest(), 16)

    def add_node(self, node: str) -> None:
        \"\"\"Adds a node with multiple virtual replicas to the ring.\"\"\"
        for i in range(self.replicas):
            virtual_node_name = f\"{node}#vnode{i}\"
            hash_key = self._hash(virtual_node_name)
            self.ring[hash_key] = node
            bisect.insort(self.sorted_keys, hash_key)

    def remove_node(self, node: str) -> None:
        \"\"\"Removes a node and its virtual replicas from the ring.\"\"\"
        for i in range(self.replicas):
            virtual_node_name = f\"{node}#vnode{i}\"
            hash_key = self._hash(virtual_node_name)
            if hash_key in self.ring:
                del self.ring[hash_key]
                self.sorted_keys.remove(hash_key)

    def get_node(self, key: str) -> str:
        \"\"\"Finds the responsible node for a given string key.\"\"\"
        if not self.ring:
            return None
        hash_key = self._hash(key)
        # Find the first node on the ring with a hash >= the key's hash
        idx = bisect.bisect_left(self.sorted_keys, hash_key)
        # If the key hash is greater than the highest node hash, wrap around
        if idx == len(self.sorted_keys):
            idx = 0
        return self.ring[self.sorted_keys[idx]]


if __name__ == '__main__':
    print(\"--- System Design Basics: Component Tests ---\")
    
    # 1. Round Robin Load Balancer
    lb = LoadBalancer([\"Server_A\", \"Server_B\", \"Server_C\"])
    assert lb.get_server() == \"Server_A\"
    assert lb.get_server() == \"Server_B\"
    assert lb.get_server() == \"Server_C\"
    assert lb.get_server() == \"Server_A\"
    print(\"Load Balancer Round Robin passed.\")
    
    # 2. Consistent Hashing
    ch = ConsistentHashRing(replicas=5)
    ch.add_node(\"Cache_Server_1\")
    ch.add_node(\"Cache_Server_2\")
    ch.add_node(\"Cache_Server_3\")
    
    # Map a user session to a cache server
    user_key = \"user_12345_session_data\"
    node_assigned = ch.get_node(user_key)
    print(f\"User {user_key} mapped to {node_assigned}\")
    
    # Remove a node and observe reassignment
    ch.remove_node(node_assigned)
    new_node_assigned = ch.get_node(user_key)
    print(f\"After removal, user {user_key} mapped to {new_node_assigned}\")
    assert node_assigned != new_node_assigned
    
    print(\"Consistent Hashing tests passed!\")

\"\"\"
Interview Challenge:
Question: Design a Rate Limiter for an API.
Solution: Implement the Token Bucket or Leaky Bucket algorithm. In distributed environments, use Redis (with Lua scripts for atomicity) to maintain token counts per user ID across multiple application servers.
\"\"\"
