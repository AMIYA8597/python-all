#!/usr/bin/env python3
"""
Distributed Systems Applications with Data Structures and Algorithms
====================================================================

This module demonstrates how data structures and algorithms are used in
distributed systems, including load balancing, consistent hashing,
distributed caching, consensus algorithms, and fault tolerance.

Author: Python DSA Master
Date: 2024
"""

import json
import time
import math
import random
import hashlib
import heapq
import threading
from typing import Dict, List, Tuple, Any, Optional, Set, Union
from collections import defaultdict, deque, Counter
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta
import socket

# ==============================================================================
# CONSISTENT HASHING
# ==============================================================================

class ConsistentHashRing:
    """
    Consistent hashing implementation for distributed systems.
    Minimizes key redistribution when nodes are added/removed.
    """
    
    def __init__(self, replicas: int = 3):
        self.replicas = replicas
        self.ring = {}  # hash -> node
        self.sorted_hashes = []
        self.nodes = set()
    
    def _hash(self, key: str) -> int:
        """Generate hash for a key."""
        return int(hashlib.md5(key.encode()).hexdigest(), 16)
    
    def add_node(self, node: str) -> None:
        """Add a node to the hash ring."""
        if node in self.nodes:
            return
        
        self.nodes.add(node)
        
        # Add replicas to increase distribution uniformity
        for i in range(self.replicas):
            replica_key = f"{node}:{i}"
            hash_val = self._hash(replica_key)
            self.ring[hash_val] = node
            self.sorted_hashes.append(hash_val)
        
        self.sorted_hashes.sort()
    
    def remove_node(self, node: str) -> None:
        """Remove a node from the hash ring."""
        if node not in self.nodes:
            return
        
        self.nodes.remove(node)
        
        # Remove all replicas
        for i in range(self.replicas):
            replica_key = f"{node}:{i}"
            hash_val = self._hash(replica_key)
            if hash_val in self.ring:
                del self.ring[hash_val]
                self.sorted_hashes.remove(hash_val)
    
    def get_node(self, key: str) -> Optional[str]:
        """Get the node responsible for a key."""
        if not self.ring:
            return None
        
        key_hash = self._hash(key)
        
        # Binary search for the first node with hash >= key_hash
        left, right = 0, len(self.sorted_hashes) - 1
        
        while left <= right:
            mid = (left + right) // 2
            if self.sorted_hashes[mid] >= key_hash:
                right = mid - 1
            else:
                left = mid + 1
        
        # Wrap around if necessary
        if left >= len(self.sorted_hashes):
            left = 0
        
        return self.ring[self.sorted_hashes[left]]
    
    def get_nodes(self, key: str, count: int = 1) -> List[str]:
        """Get multiple nodes for replication."""
        if not self.ring or count <= 0:
            return []
        
        key_hash = self._hash(key)
        result = []
        seen_nodes = set()
        
        # Find starting position
        start_idx = 0
        for i, hash_val in enumerate(self.sorted_hashes):
            if hash_val >= key_hash:
                start_idx = i
                break
        
        # Collect unique nodes
        idx = start_idx
        while len(result) < count and len(seen_nodes) < len(self.nodes):
            if idx >= len(self.sorted_hashes):
                idx = 0
            
            node = self.ring[self.sorted_hashes[idx]]
            if node not in seen_nodes:
                result.append(node)
                seen_nodes.add(node)
            
            idx += 1
        
        return result
    
    def get_load_distribution(self) -> Dict[str, float]:
        """Analyze load distribution across nodes."""
        if not self.sorted_hashes:
            return {}
        
        node_loads = defaultdict(float)
        total_range = 2 ** 128  # MD5 hash range
        
        for i in range(len(self.sorted_hashes)):
            current_hash = self.sorted_hashes[i]
            next_hash = self.sorted_hashes[(i + 1) % len(self.sorted_hashes)]
            
            if next_hash < current_hash:  # Wrap around
                range_size = (total_range - current_hash) + next_hash
            else:
                range_size = next_hash - current_hash
            
            node = self.ring[current_hash]
            node_loads[node] += range_size / total_range
        
        return dict(node_loads)

# ==============================================================================
# LOAD BALANCING
# ==============================================================================

class LoadBalancer:
    """
    Advanced load balancer with multiple algorithms.
    """
    
    def __init__(self, algorithm: str = "weighted_round_robin"):
        self.algorithm = algorithm
        self.servers = {}  # server_id -> server_info
        self.current_index = 0
        self.request_counts = defaultdict(int)
        self.response_times = defaultdict(list)
        self.health_status = defaultdict(bool)
        
        # For least connections
        self.active_connections = defaultdict(int)
        
        # For weighted algorithms
        self.weights = defaultdict(lambda: 1)
        self.current_weights = defaultdict(int)
    
    @dataclass
    class ServerInfo:
        server_id: str
        address: str
        port: int
        weight: int = 1
        max_connections: int = 1000
        current_connections: int = 0
        avg_response_time: float = 0.0
        last_health_check: datetime = field(default_factory=datetime.now)
        
    def add_server(self, server_id: str, address: str, port: int, weight: int = 1) -> None:
        """Add a server to the load balancer."""
        server_info = self.ServerInfo(server_id, address, port, weight)
        self.servers[server_id] = server_info
        self.weights[server_id] = weight
        self.current_weights[server_id] = 0
        self.health_status[server_id] = True
    
    def remove_server(self, server_id: str) -> None:
        """Remove a server from the load balancer."""
        if server_id in self.servers:
            del self.servers[server_id]
            del self.weights[server_id]
            del self.current_weights[server_id]
            del self.health_status[server_id]
    
    def get_healthy_servers(self) -> List[str]:
        """Get list of healthy servers."""
        return [sid for sid, healthy in self.health_status.items() if healthy]
    
    def round_robin(self) -> Optional[str]:
        """Simple round-robin selection."""
        healthy_servers = self.get_healthy_servers()
        if not healthy_servers:
            return None
        
        server = healthy_servers[self.current_index % len(healthy_servers)]
        self.current_index += 1
        return server
    
    def weighted_round_robin(self) -> Optional[str]:
        """Weighted round-robin selection using smooth algorithm."""
        healthy_servers = self.get_healthy_servers()
        if not healthy_servers:
            return None
        
        # Smooth weighted round-robin algorithm
        best_server = None
        best_weight = -1
        total_weight = 0
        
        for server_id in healthy_servers:
            weight = self.weights[server_id]
            self.current_weights[server_id] += weight
            total_weight += weight
            
            if self.current_weights[server_id] > best_weight:
                best_weight = self.current_weights[server_id]
                best_server = server_id
        
        if best_server:
            self.current_weights[best_server] -= total_weight
        
        return best_server
    
    def least_connections(self) -> Optional[str]:
        """Select server with least active connections."""
        healthy_servers = self.get_healthy_servers()
        if not healthy_servers:
            return None
        
        min_connections = float('inf')
        best_server = None
        
        for server_id in healthy_servers:
            connections = self.active_connections[server_id]
            if connections < min_connections:
                min_connections = connections
                best_server = server_id
        
        return best_server
    
    def weighted_least_connections(self) -> Optional[str]:
        """Select server with lowest connections-to-weight ratio."""
        healthy_servers = self.get_healthy_servers()
        if not healthy_servers:
            return None
        
        min_ratio = float('inf')
        best_server = None
        
        for server_id in healthy_servers:
            connections = self.active_connections[server_id]
            weight = self.weights[server_id]
            ratio = connections / weight if weight > 0 else float('inf')
            
            if ratio < min_ratio:
                min_ratio = ratio
                best_server = server_id
        
        return best_server
    
    def least_response_time(self) -> Optional[str]:
        """Select server with lowest average response time."""
        healthy_servers = self.get_healthy_servers()
        if not healthy_servers:
            return None
        
        min_response_time = float('inf')
        best_server = None
        
        for server_id in healthy_servers:
            response_times = self.response_times[server_id]
            if response_times:
                avg_time = sum(response_times) / len(response_times)
            else:
                avg_time = 0  # New server gets priority
            
            if avg_time < min_response_time:
                min_response_time = avg_time
                best_server = server_id
        
        return best_server
    
    def select_server(self) -> Optional[str]:
        """Select a server based on the configured algorithm."""
        if self.algorithm == "round_robin":
            return self.round_robin()
        elif self.algorithm == "weighted_round_robin":
            return self.weighted_round_robin()
        elif self.algorithm == "least_connections":
            return self.least_connections()
        elif self.algorithm == "weighted_least_connections":
            return self.weighted_least_connections()
        elif self.algorithm == "least_response_time":
            return self.least_response_time()
        else:
            return self.round_robin()
    
    def record_request(self, server_id: str, response_time: float) -> None:
        """Record request statistics."""
        self.request_counts[server_id] += 1
        self.response_times[server_id].append(response_time)
        
        # Keep only recent response times (sliding window)
        if len(self.response_times[server_id]) > 100:
            self.response_times[server_id] = self.response_times[server_id][-50:]
    
    def start_connection(self, server_id: str) -> None:
        """Record start of connection."""
        self.active_connections[server_id] += 1
    
    def end_connection(self, server_id: str) -> None:
        """Record end of connection."""
        if self.active_connections[server_id] > 0:
            self.active_connections[server_id] -= 1
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get load balancer statistics."""
        stats = {
            'algorithm': self.algorithm,
            'total_servers': len(self.servers),
            'healthy_servers': len(self.get_healthy_servers()),
            'server_stats': {}
        }
        
        for server_id, server_info in self.servers.items():
            response_times = self.response_times[server_id]
            avg_response_time = sum(response_times) / len(response_times) if response_times else 0
            
            stats['server_stats'][server_id] = {
                'healthy': self.health_status[server_id],
                'weight': self.weights[server_id],
                'active_connections': self.active_connections[server_id],
                'total_requests': self.request_counts[server_id],
                'avg_response_time': avg_response_time,
                'current_weight': self.current_weights[server_id]
            }
        
        return stats

# ==============================================================================
# DISTRIBUTED CACHE
# ==============================================================================

class DistributedCache:
    """
    Distributed cache using consistent hashing with replication.
    """
    
    def __init__(self, replication_factor: int = 3):
        self.hash_ring = ConsistentHashRing(replicas=150)  # More replicas for better distribution
        self.replication_factor = replication_factor
        self.node_caches = {}  # node_id -> local cache
        self.node_stats = defaultdict(lambda: {'hits': 0, 'misses': 0, 'sets': 0})
        
    @dataclass
    class CacheEntry:
        value: Any
        timestamp: datetime
        ttl: Optional[int] = None  # Time to live in seconds
        version: int = 1
        
        def is_expired(self) -> bool:
            if self.ttl is None:
                return False
            return datetime.now() > self.timestamp + timedelta(seconds=self.ttl)
    
    def add_node(self, node_id: str) -> None:
        """Add a cache node."""
        self.hash_ring.add_node(node_id)
        self.node_caches[node_id] = {}
    
    def remove_node(self, node_id: str) -> None:
        """Remove a cache node."""
        self.hash_ring.remove_node(node_id)
        if node_id in self.node_caches:
            del self.node_caches[node_id]
        if node_id in self.node_stats:
            del self.node_stats[node_id]
    
    def _get_replica_nodes(self, key: str) -> List[str]:
        """Get nodes that should store replicas of the key."""
        return self.hash_ring.get_nodes(key, self.replication_factor)
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """Set a key-value pair in the distributed cache."""
        nodes = self._get_replica_nodes(key)
        if not nodes:
            return False
        
        entry = self.CacheEntry(value, datetime.now(), ttl)
        success_count = 0
        
        for node_id in nodes:
            if node_id in self.node_caches:
                self.node_caches[node_id][key] = entry
                self.node_stats[node_id]['sets'] += 1
                success_count += 1
        
        # Require majority of replicas to succeed
        return success_count >= (len(nodes) + 1) // 2
    
    def get(self, key: str) -> Tuple[Any, bool]:
        """Get a value from the distributed cache."""
        nodes = self._get_replica_nodes(key)
        if not nodes:
            return None, False
        
        # Try nodes in order until we find the value
        for node_id in nodes:
            if node_id not in self.node_caches:
                continue
            
            if key in self.node_caches[node_id]:
                entry = self.node_caches[node_id][key]
                
                if entry.is_expired():
                    # Remove expired entry
                    del self.node_caches[node_id][key]
                    self.node_stats[node_id]['misses'] += 1
                    continue
                
                self.node_stats[node_id]['hits'] += 1
                return entry.value, True
            else:
                self.node_stats[node_id]['misses'] += 1
        
        return None, False
    
    def delete(self, key: str) -> bool:
        """Delete a key from all replica nodes."""
        nodes = self._get_replica_nodes(key)
        if not nodes:
            return False
        
        success_count = 0
        
        for node_id in nodes:
            if node_id in self.node_caches and key in self.node_caches[node_id]:
                del self.node_caches[node_id][key]
                success_count += 1
        
        return success_count > 0
    
    def get_node_stats(self) -> Dict[str, Dict[str, Any]]:
        """Get statistics for all cache nodes."""
        stats = {}
        
        for node_id, cache in self.node_caches.items():
            node_stats = dict(self.node_stats[node_id])
            node_stats['cache_size'] = len(cache)
            
            # Calculate hit ratio
            total_requests = node_stats['hits'] + node_stats['misses']
            node_stats['hit_ratio'] = (
                node_stats['hits'] / total_requests if total_requests > 0 else 0
            )
            
            # Calculate memory usage (approximate)
            memory_usage = 0
            for entry in cache.values():
                memory_usage += len(str(entry.value))
            node_stats['memory_usage_bytes'] = memory_usage
            
            stats[node_id] = node_stats
        
        return stats
    
    def cleanup_expired(self) -> int:
        """Remove expired entries from all nodes."""
        removed_count = 0
        
        for node_id, cache in self.node_caches.items():
            expired_keys = []
            
            for key, entry in cache.items():
                if entry.is_expired():
                    expired_keys.append(key)
            
            for key in expired_keys:
                del cache[key]
                removed_count += 1
        
        return removed_count

# ==============================================================================
# CONSENSUS ALGORITHMS
# ==============================================================================

class RaftNode:
    """
    Simplified implementation of Raft consensus algorithm.
    """
    
    class State(Enum):
        FOLLOWER = "follower"
        CANDIDATE = "candidate"
        LEADER = "leader"
    
    @dataclass
    class LogEntry:
        term: int
        index: int
        command: str
        timestamp: datetime = field(default_factory=datetime.now)
    
    def __init__(self, node_id: str, cluster_nodes: List[str]):
        self.node_id = node_id
        self.cluster_nodes = cluster_nodes
        self.state = self.State.FOLLOWER
        
        # Persistent state
        self.current_term = 0
        self.voted_for: Optional[str] = None
        self.log: List[self.LogEntry] = []
        
        # Volatile state
        self.commit_index = -1
        self.last_applied = -1
        
        # Leader state
        self.next_index = {}  # For each server, index to send next
        self.match_index = {}  # For each server, highest index known to be replicated
        
        # Timing
        self.last_heartbeat = datetime.now()
        self.election_timeout = random.uniform(150, 300) / 1000  # 150-300ms
        self.heartbeat_interval = 50 / 1000  # 50ms
        
        # Statistics
        self.votes_received = set()
        self.message_log = []
    
    def start_election(self) -> None:
        """Start leader election process."""
        self.state = self.State.CANDIDATE
        self.current_term += 1
        self.voted_for = self.node_id
        self.votes_received = {self.node_id}
        self.last_heartbeat = datetime.now()
        
        self.message_log.append(f"Node {self.node_id} started election for term {self.current_term}")
        
        # In real implementation, would send RequestVote RPCs to all other nodes
        # Here we simulate the process
    
    def receive_vote(self, voter_id: str, term: int) -> bool:
        """Receive a vote from another node."""
        if term != self.current_term or self.state != self.State.CANDIDATE:
            return False
        
        self.votes_received.add(voter_id)
        majority = len(self.cluster_nodes) // 2 + 1
        
        if len(self.votes_received) >= majority:
            self.become_leader()
            return True
        
        return False
    
    def become_leader(self) -> None:
        """Transition to leader state."""
        self.state = self.State.LEADER
        self.message_log.append(f"Node {self.node_id} became leader for term {self.current_term}")
        
        # Initialize leader state
        last_log_index = len(self.log) - 1
        for node_id in self.cluster_nodes:
            if node_id != self.node_id:
                self.next_index[node_id] = last_log_index + 1
                self.match_index[node_id] = -1
    
    def append_entry(self, command: str) -> bool:
        """Append a new log entry (leader only)."""
        if self.state != self.State.LEADER:
            return False
        
        entry = self.LogEntry(self.current_term, len(self.log), command)
        self.log.append(entry)
        
        self.message_log.append(f"Leader {self.node_id} appended entry: {command}")
        return True
    
    def receive_heartbeat(self, leader_id: str, term: int) -> None:
        """Receive heartbeat from leader."""
        if term >= self.current_term:
            self.current_term = term
            self.state = self.State.FOLLOWER
            self.voted_for = None
            self.last_heartbeat = datetime.now()
    
    def check_election_timeout(self) -> bool:
        """Check if election timeout has occurred."""
        time_since_heartbeat = (datetime.now() - self.last_heartbeat).total_seconds()
        return time_since_heartbeat > self.election_timeout
    
    def get_status(self) -> Dict[str, Any]:
        """Get current node status."""
        return {
            'node_id': self.node_id,
            'state': self.state.value,
            'current_term': self.current_term,
            'voted_for': self.voted_for,
            'log_length': len(self.log),
            'commit_index': self.commit_index,
            'votes_received': len(self.votes_received),
            'last_heartbeat': self.last_heartbeat.isoformat()
        }

# ==============================================================================
# FAULT TOLERANCE
# ==============================================================================

class CircuitBreaker:
    """
    Circuit breaker pattern for fault tolerance.
    """
    
    class State(Enum):
        CLOSED = "closed"
        OPEN = "open"
        HALF_OPEN = "half_open"
    
    def __init__(self, failure_threshold: int = 5, timeout: int = 60):
        self.failure_threshold = failure_threshold
        self.timeout = timeout  # Seconds before trying half-open
        
        self.state = self.State.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time: Optional[datetime] = None
        
        # Statistics
        self.total_requests = 0
        self.total_failures = 0
        self.state_changes = []
    
    def call(self, func, *args, **kwargs) -> Tuple[Any, bool]:
        """Execute function through circuit breaker."""
        self.total_requests += 1
        
        if self.state == self.State.OPEN:
            if self._should_attempt_reset():
                self._transition_to_half_open()
            else:
                return None, False  # Circuit is open, fail fast
        
        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result, True
        
        except Exception as e:
            self._on_failure()
            return None, False
    
    def _should_attempt_reset(self) -> bool:
        """Check if enough time has passed to attempt reset."""
        if self.last_failure_time is None:
            return True
        
        time_since_failure = (datetime.now() - self.last_failure_time).total_seconds()
        return time_since_failure >= self.timeout
    
    def _transition_to_half_open(self) -> None:
        """Transition to half-open state."""
        self.state = self.State.HALF_OPEN
        self.success_count = 0
        self.state_changes.append({
            'state': self.state.value,
            'timestamp': datetime.now(),
            'reason': 'timeout_expired'
        })
    
    def _on_success(self) -> None:
        """Handle successful function call."""
        self.failure_count = 0
        
        if self.state == self.State.HALF_OPEN:
            self.success_count += 1
            if self.success_count >= 3:  # Require multiple successes
                self._transition_to_closed()
    
    def _on_failure(self) -> None:
        """Handle failed function call."""
        self.failure_count += 1
        self.total_failures += 1
        self.last_failure_time = datetime.now()
        
        if self.state == self.State.HALF_OPEN:
            self._transition_to_open()
        elif self.state == self.State.CLOSED and self.failure_count >= self.failure_threshold:
            self._transition_to_open()
    
    def _transition_to_closed(self) -> None:
        """Transition to closed state."""
        self.state = self.State.CLOSED
        self.failure_count = 0
        self.state_changes.append({
            'state': self.state.value,
            'timestamp': datetime.now(),
            'reason': 'success_threshold_met'
        })
    
    def _transition_to_open(self) -> None:
        """Transition to open state."""
        self.state = self.State.OPEN
        self.state_changes.append({
            'state': self.state.value,
            'timestamp': datetime.now(),
            'reason': 'failure_threshold_exceeded'
        })
    
    def get_stats(self) -> Dict[str, Any]:
        """Get circuit breaker statistics."""
        failure_rate = self.total_failures / self.total_requests if self.total_requests > 0 else 0
        
        return {
            'state': self.state.value,
            'failure_count': self.failure_count,
            'total_requests': self.total_requests,
            'total_failures': self.total_failures,
            'failure_rate': failure_rate,
            'last_failure_time': self.last_failure_time.isoformat() if self.last_failure_time else None,
            'state_changes': len(self.state_changes)
        }

# ==============================================================================
# DEMONSTRATION AND BENCHMARKING
# ==============================================================================

def demo_consistent_hashing():
    """Demonstrate consistent hashing."""
    print("Consistent Hashing Demo")
    print("=" * 30)
    
    # Create hash ring and add nodes
    hash_ring = ConsistentHashRing(replicas=3)
    nodes = ["server1", "server2", "server3", "server4"]
    
    for node in nodes:
        hash_ring.add_node(node)
    
    print(f"Added {len(nodes)} nodes to hash ring")
    
    # Test key distribution
    keys = [f"key_{i}" for i in range(1000)]
    distribution = defaultdict(int)
    
    for key in keys:
        node = hash_ring.get_node(key)
        distribution[node] += 1
    
    print("\nKey distribution:")
    for node, count in distribution.items():
        print(f"  {node}: {count} keys ({count/len(keys)*100:.1f}%)")
    
    # Test load distribution
    load_dist = hash_ring.get_load_distribution()
    print("\nTheoretical load distribution:")
    for node, load in load_dist.items():
        print(f"  {node}: {load:.4f} ({load*100:.2f}%)")
    
    # Test node removal
    print(f"\nRemoving {nodes[0]}...")
    hash_ring.remove_node(nodes[0])
    
    redistributed = 0
    new_distribution = defaultdict(int)
    
    for key in keys:
        new_node = hash_ring.get_node(key)
        new_distribution[new_node] += 1
        if new_node != distribution.get(key):
            redistributed += 1
    
    print(f"Redistributed {redistributed} keys ({redistributed/len(keys)*100:.1f}%)")
    print("New distribution:")
    for node, count in new_distribution.items():
        print(f"  {node}: {count} keys ({count/len(keys)*100:.1f}%)")

def demo_load_balancing():
    """Demonstrate load balancing algorithms."""
    print("\nLoad Balancing Demo")
    print("=" * 30)
    
    # Create load balancer
    lb = LoadBalancer(algorithm="weighted_round_robin")
    
    # Add servers with different weights
    servers = [
        ("server1", "192.168.1.1", 8080, 3),
        ("server2", "192.168.1.2", 8080, 2),
        ("server3", "192.168.1.3", 8080, 1),
        ("server4", "192.168.1.4", 8080, 2)
    ]
    
    for server_id, address, port, weight in servers:
        lb.add_server(server_id, address, port, weight)
    
    print(f"Added {len(servers)} servers")
    
    # Simulate requests
    requests = 100
    request_distribution = defaultdict(int)
    
    for i in range(requests):
        server = lb.select_server()
        if server:
            request_distribution[server] += 1
            
            # Simulate request processing
            response_time = random.uniform(50, 200)  # ms
            lb.start_connection(server)
            lb.record_request(server, response_time)
            lb.end_connection(server)
    
    print(f"\nProcessed {requests} requests")
    print("Request distribution:")
    for server_id, count in request_distribution.items():
        weight = lb.weights[server_id]
        print(f"  {server_id} (weight={weight}): {count} requests ({count/requests*100:.1f}%)")
    
    # Test different algorithms
    algorithms = ["round_robin", "least_connections", "least_response_time"]
    
    for algorithm in algorithms:
        lb.algorithm = algorithm
        lb.current_index = 0
        
        alg_distribution = defaultdict(int)
        for i in range(50):
            server = lb.select_server()
            if server:
                alg_distribution[server] += 1
        
        print(f"\n{algorithm.replace('_', ' ').title()} (50 requests):")
        for server_id, count in alg_distribution.items():
            print(f"  {server_id}: {count} requests")

def demo_distributed_cache():
    """Demonstrate distributed caching."""
    print("\nDistributed Cache Demo")
    print("=" * 30)
    
    # Create distributed cache
    cache = DistributedCache(replication_factor=2)
    
    # Add cache nodes
    nodes = ["cache1", "cache2", "cache3", "cache4"]
    for node in nodes:
        cache.add_node(node)
    
    print(f"Added {len(nodes)} cache nodes")
    
    # Test cache operations
    test_data = {
        "user:1001": {"name": "Alice", "email": "alice@example.com"},
        "user:1002": {"name": "Bob", "email": "bob@example.com"},
        "config:db": {"host": "db.example.com", "port": 5432},
        "session:abc123": {"user_id": 1001, "expires": "2024-12-31"}
    }
    
    # Set values
    set_count = 0
    for key, value in test_data.items():
        if cache.set(key, value, ttl=3600):  # 1 hour TTL
            set_count += 1
    
    print(f"Successfully set {set_count}/{len(test_data)} cache entries")
    
    # Get values
    hit_count = 0
    for key in test_data.keys():
        value, found = cache.get(key)
        if found:
            hit_count += 1
    
    print(f"Cache hits: {hit_count}/{len(test_data)} ({hit_count/len(test_data)*100:.1f}%)")
    
    # Test with missing keys
    missing_keys = ["user:9999", "nonexistent", "missing:key"]
    miss_count = 0
    for key in missing_keys:
        value, found = cache.get(key)
        if not found:
            miss_count += 1
    
    print(f"Cache misses for non-existent keys: {miss_count}/{len(missing_keys)}")
    
    # Show node statistics
    stats = cache.get_node_stats()
    print("\nCache node statistics:")
    for node_id, node_stats in stats.items():
        print(f"  {node_id}:")
        print(f"    Cache size: {node_stats['cache_size']} entries")
        print(f"    Hit ratio: {node_stats['hit_ratio']:.2f}")
        print(f"    Memory usage: {node_stats['memory_usage_bytes']} bytes")

def demo_raft_consensus():
    """Demonstrate Raft consensus algorithm."""
    print("\nRaft Consensus Demo")
    print("=" * 30)
    
    # Create cluster nodes
    cluster_nodes = ["node1", "node2", "node3", "node4", "node5"]
    nodes = {}
    
    for node_id in cluster_nodes:
        nodes[node_id] = RaftNode(node_id, cluster_nodes)
    
    print(f"Created Raft cluster with {len(nodes)} nodes")
    
    # Simulate leader election
    print("\nSimulating leader election...")
    
    # Start election on node1
    nodes["node1"].start_election()
    
    # Simulate voting process
    for voter in ["node2", "node3", "node4"]:  # Need majority (3/5)
        nodes["node1"].receive_vote(voter, nodes["node1"].current_term)
        if nodes["node1"].state == RaftNode.State.LEADER:
            break
    
    # Show node statuses
    print("\nNode statuses after election:")
    for node_id, node in nodes.items():
        status = node.get_status()
        print(f"  {node_id}: {status['state']}, term {status['current_term']}")
    
    # Leader appends entries
    if nodes["node1"].state == RaftNode.State.LEADER:
        commands = ["SET x=1", "SET y=2", "DELETE z", "SET x=3"]
        print(f"\nLeader appending {len(commands)} log entries...")
        
        for command in commands:
            nodes["node1"].append_entry(command)
        
        print(f"Leader log length: {len(nodes['node1'].log)}")
        
        # Show recent log entries
        print("Recent log entries:")
        for entry in nodes["node1"].log[-3:]:
            print(f"  Term {entry.term}, Index {entry.index}: {entry.command}")

def demo_circuit_breaker():
    """Demonstrate circuit breaker pattern."""
    print("\nCircuit Breaker Demo")
    print("=" * 30)
    
    # Create circuit breaker
    circuit_breaker = CircuitBreaker(failure_threshold=3, timeout=2)
    
    # Simulate unreliable service
    def unreliable_service(fail_rate: float = 0.3):
        if random.random() < fail_rate:
            raise Exception("Service unavailable")
        return "Success"
    
    print("Testing circuit breaker with unreliable service...")
    
    # Test with high failure rate
    results = {"success": 0, "failure": 0, "circuit_open": 0}
    
    for i in range(20):
        result, success = circuit_breaker.call(unreliable_service, fail_rate=0.7)
        
        if success:
            results["success"] += 1
        elif circuit_breaker.state == CircuitBreaker.State.OPEN:
            results["circuit_open"] += 1
        else:
            results["failure"] += 1
        
        # Show state changes
        if i < 10:  # Show first 10 attempts
            print(f"  Attempt {i+1}: {'Success' if success else 'Failed'} "
                  f"(Circuit: {circuit_breaker.state.value})")
    
    print(f"\nResults after 20 attempts:")
    print(f"  Successes: {results['success']}")
    print(f"  Failures: {results['failure']}")
    print(f"  Circuit open rejections: {results['circuit_open']}")
    
    # Show statistics
    stats = circuit_breaker.get_stats()
    print(f"\nCircuit breaker statistics:")
    print(f"  Current state: {stats['state']}")
    print(f"  Total requests: {stats['total_requests']}")
    print(f"  Failure rate: {stats['failure_rate']:.2%}")
    print(f"  State changes: {stats['state_changes']}")

def main():
    """Run all demonstrations."""
    print("Distributed Systems Applications with DSA - Comprehensive Demo")
    print("=" * 70)
    
    # Run all demos
    demo_consistent_hashing()
    demo_load_balancing()
    demo_distributed_cache()
    demo_raft_consensus()
    demo_circuit_breaker()
    
    print("\n" + "=" * 70)
    print("All demonstrations completed successfully!")
    
    print("\nKey Concepts Demonstrated:")
    print("- Consistent hashing minimizes data movement during scaling")
    print("- Load balancing distributes requests optimally across servers")
    print("- Distributed caching provides scalable data access")
    print("- Consensus algorithms ensure consistency in distributed systems")
    print("- Circuit breakers provide fault tolerance and prevent cascade failures")

if __name__ == "__main__":
    main()
