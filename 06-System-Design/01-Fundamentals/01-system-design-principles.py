#!/usr/bin/env python3
"""
System Design Fundamentals - Core Principles and Patterns

This module covers the fundamental principles of designing large-scale distributed
systems. It includes scalability patterns, reliability concepts, performance
optimization, and real-world system design examples commonly asked in technical
interviews at senior engineering levels.

Topics Covered:
- Scalability patterns and techniques
- Load balancing strategies
- Database design and sharding
- Caching systems and strategies
- Microservices architecture
- API design and REST principles
- Distributed system concepts
- Real-world case studies

Author: Python DSA Master
Date: 2024
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any, Protocol
from dataclasses import dataclass, field
from enum import Enum
import time
import random
import json
from collections import defaultdict, deque
import threading
from queue import Queue, PriorityQueue
import hashlib


class LoadBalancingStrategy(Enum):
    """Load balancing strategies for distributing requests."""
    ROUND_ROBIN = "round_robin"
    LEAST_CONNECTIONS = "least_connections"
    WEIGHTED_ROUND_ROBIN = "weighted_round_robin"
    LEAST_RESPONSE_TIME = "least_response_time"
    CONSISTENT_HASHING = "consistent_hashing"


@dataclass
class Server:
    """Represents a server in the system."""
    id: str
    host: str
    port: int
    weight: int = 1
    current_connections: int = 0
    total_requests: int = 0
    avg_response_time: float = 0.0
    is_healthy: bool = True
    
    def process_request(self, request_id: str) -> float:
        """Simulate processing a request and return response time."""
        if not self.is_healthy:
            raise Exception(f"Server {self.id} is unhealthy")
        
        # Simulate request processing time
        processing_time = random.uniform(0.1, 2.0)
        time.sleep(processing_time / 1000)  # Simulate work (scaled down)
        
        self.current_connections += 1
        self.total_requests += 1
        
        # Update average response time
        self.avg_response_time = (
            (self.avg_response_time * (self.total_requests - 1) + processing_time) 
            / self.total_requests
        )
        
        return processing_time


class LoadBalancer:
    """
    Comprehensive Load Balancer Implementation
    
    Implements multiple load balancing strategies for distributing
    requests across multiple servers.
    """
    
    def __init__(self, strategy: LoadBalancingStrategy = LoadBalancingStrategy.ROUND_ROBIN):
        self.strategy = strategy
        self.servers: List[Server] = []
        self.current_index = 0
        self.request_count = 0
        
        # For consistent hashing
        self.hash_ring: Dict[int, str] = {}
        self.virtual_nodes = 100  # Number of virtual nodes per server
    
    def add_server(self, server: Server):
        """Add a server to the load balancer."""
        self.servers.append(server)
        
        if self.strategy == LoadBalancingStrategy.CONSISTENT_HASHING:
            self._add_server_to_hash_ring(server)
    
    def remove_server(self, server_id: str):
        """Remove a server from the load balancer."""
        self.servers = [s for s in self.servers if s.id != server_id]
        
        if self.strategy == LoadBalancingStrategy.CONSISTENT_HASHING:
            self._remove_server_from_hash_ring(server_id)
    
    def get_server(self, request_id: str = None) -> Optional[Server]:
        """Get the next server based on the load balancing strategy."""
        healthy_servers = [s for s in self.servers if s.is_healthy]
        
        if not healthy_servers:
            return None
        
        if self.strategy == LoadBalancingStrategy.ROUND_ROBIN:
            return self._round_robin(healthy_servers)
        elif self.strategy == LoadBalancingStrategy.LEAST_CONNECTIONS:
            return self._least_connections(healthy_servers)
        elif self.strategy == LoadBalancingStrategy.WEIGHTED_ROUND_ROBIN:
            return self._weighted_round_robin(healthy_servers)
        elif self.strategy == LoadBalancingStrategy.LEAST_RESPONSE_TIME:
            return self._least_response_time(healthy_servers)
        elif self.strategy == LoadBalancingStrategy.CONSISTENT_HASHING:
            return self._consistent_hashing(request_id or "default")
        
        return healthy_servers[0]  # Fallback
    
    def _round_robin(self, servers: List[Server]) -> Server:
        """Round robin load balancing."""
        server = servers[self.current_index % len(servers)]
        self.current_index += 1
        return server
    
    def _least_connections(self, servers: List[Server]) -> Server:
        """Least connections load balancing."""
        return min(servers, key=lambda s: s.current_connections)
    
    def _weighted_round_robin(self, servers: List[Server]) -> Server:
        """Weighted round robin load balancing."""
        # Simple weighted round robin implementation
        total_weight = sum(s.weight for s in servers)
        
        for server in servers:
            if self.request_count % total_weight < server.weight:
                self.request_count += 1
                return server
        
        self.request_count += 1
        return servers[0]
    
    def _least_response_time(self, servers: List[Server]) -> Server:
        """Least response time load balancing."""
        return min(servers, key=lambda s: s.avg_response_time)
    
    def _consistent_hashing(self, key: str) -> Server:
        """Consistent hashing load balancing."""
        if not self.hash_ring:
            return self.servers[0] if self.servers else None
        
        hash_value = self._hash(key)
        
        # Find the first server in the ring >= hash_value
        for ring_position in sorted(self.hash_ring.keys()):
            if ring_position >= hash_value:
                server_id = self.hash_ring[ring_position]
                return next(s for s in self.servers if s.id == server_id)
        
        # Wrap around to the first server
        first_position = min(self.hash_ring.keys())
        server_id = self.hash_ring[first_position]
        return next(s for s in self.servers if s.id == server_id)
    
    def _add_server_to_hash_ring(self, server: Server):
        """Add server to consistent hash ring."""
        for i in range(self.virtual_nodes):
            virtual_key = f"{server.id}:{i}"
            hash_value = self._hash(virtual_key)
            self.hash_ring[hash_value] = server.id
    
    def _remove_server_from_hash_ring(self, server_id: str):
        """Remove server from consistent hash ring."""
        keys_to_remove = [
            k for k, v in self.hash_ring.items() 
            if v == server_id
        ]
        for key in keys_to_remove:
            del self.hash_ring[key]
    
    def _hash(self, key: str) -> int:
        """Hash function for consistent hashing."""
        return int(hashlib.md5(key.encode()).hexdigest(), 16)


class CacheStrategy(Enum):
    """Cache eviction strategies."""
    LRU = "lru"
    LFU = "lfu"
    FIFO = "fifo"
    RANDOM = "random"


@dataclass
class CacheItem:
    """Cache item with metadata."""
    key: str
    value: Any
    access_count: int = 0
    last_accessed: float = field(default_factory=time.time)
    created_at: float = field(default_factory=time.time)


class DistributedCache:
    """
    Distributed Cache System Implementation
    
    Implements various caching strategies and patterns commonly
    used in distributed systems for performance optimization.
    """
    
    def __init__(self, max_size: int = 1000, strategy: CacheStrategy = CacheStrategy.LRU):
        self.max_size = max_size
        self.strategy = strategy
        self.cache: Dict[str, CacheItem] = {}
        self.access_order = deque()  # For LRU
        self.frequency_counter = defaultdict(int)  # For LFU
        
        # Statistics
        self.hits = 0
        self.misses = 0
        self.evictions = 0
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        if key in self.cache:
            item = self.cache[key]
            item.access_count += 1
            item.last_accessed = time.time()
            
            if self.strategy == CacheStrategy.LRU:
                self._update_lru_access(key)
            elif self.strategy == CacheStrategy.LFU:
                self.frequency_counter[key] += 1
            
            self.hits += 1
            return item.value
        
        self.misses += 1
        return None
    
    def put(self, key: str, value: Any) -> None:
        """Put value into cache."""
        if key in self.cache:
            # Update existing item
            item = self.cache[key]
            item.value = value
            item.last_accessed = time.time()
            
            if self.strategy == CacheStrategy.LRU:
                self._update_lru_access(key)
            elif self.strategy == CacheStrategy.LFU:
                self.frequency_counter[key] += 1
        else:
            # Add new item
            if len(self.cache) >= self.max_size:
                self._evict()
            
            item = CacheItem(key=key, value=value)
            self.cache[key] = item
            
            if self.strategy == CacheStrategy.LRU:
                self.access_order.append(key)
            elif self.strategy == CacheStrategy.LFU:
                self.frequency_counter[key] = 1
    
    def delete(self, key: str) -> bool:
        """Delete key from cache."""
        if key in self.cache:
            del self.cache[key]
            
            if self.strategy == CacheStrategy.LRU and key in self.access_order:
                self.access_order.remove(key)
            elif self.strategy == CacheStrategy.LFU:
                del self.frequency_counter[key]
            
            return True
        return False
    
    def _evict(self) -> None:
        """Evict item based on strategy."""
        if not self.cache:
            return
        
        if self.strategy == CacheStrategy.LRU:
            key_to_evict = self.access_order.popleft()
        elif self.strategy == CacheStrategy.LFU:
            key_to_evict = min(self.frequency_counter.keys(), 
                             key=lambda k: self.frequency_counter[k])
            del self.frequency_counter[key_to_evict]
        elif self.strategy == CacheStrategy.FIFO:
            key_to_evict = min(self.cache.keys(), 
                             key=lambda k: self.cache[k].created_at)
        else:  # RANDOM
            key_to_evict = random.choice(list(self.cache.keys()))
        
        del self.cache[key_to_evict]
        self.evictions += 1
    
    def _update_lru_access(self, key: str) -> None:
        """Update LRU access order."""
        if key in self.access_order:
            self.access_order.remove(key)
        self.access_order.append(key)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        total_requests = self.hits + self.misses
        hit_rate = (self.hits / total_requests) if total_requests > 0 else 0
        
        return {
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate": hit_rate,
            "evictions": self.evictions,
            "current_size": len(self.cache),
            "max_size": self.max_size
        }


class DatabaseSharding:
    """
    Database Sharding Implementation
    
    Demonstrates horizontal partitioning strategies for scaling
    databases across multiple nodes.
    """
    
    def __init__(self, num_shards: int = 4):
        self.num_shards = num_shards
        self.shards: Dict[int, Dict[str, Any]] = {
            i: {} for i in range(num_shards)
        }
        self.shard_sizes = [0] * num_shards
    
    def hash_shard(self, key: str) -> int:
        """Hash-based sharding strategy."""
        return hash(key) % self.num_shards
    
    def range_shard(self, key: str) -> int:
        """Range-based sharding strategy (simplified)."""
        # Simple alphabetical range sharding
        first_char = key[0].upper() if key else 'A'
        char_value = ord(first_char) - ord('A')
        return min(char_value * self.num_shards // 26, self.num_shards - 1)
    
    def directory_shard(self, key: str, shard_map: Dict[str, int]) -> int:
        """Directory-based sharding using lookup table."""
        return shard_map.get(key, 0)
    
    def put(self, key: str, value: Any, strategy: str = "hash") -> None:
        """Store data in appropriate shard."""
        if strategy == "hash":
            shard_id = self.hash_shard(key)
        elif strategy == "range":
            shard_id = self.range_shard(key)
        else:
            shard_id = 0  # Default
        
        if key not in self.shards[shard_id]:
            self.shard_sizes[shard_id] += 1
        
        self.shards[shard_id][key] = value
    
    def get(self, key: str, strategy: str = "hash") -> Optional[Any]:
        """Retrieve data from appropriate shard."""
        if strategy == "hash":
            shard_id = self.hash_shard(key)
        elif strategy == "range":
            shard_id = self.range_shard(key)
        else:
            shard_id = 0
        
        return self.shards[shard_id].get(key)
    
    def get_shard_stats(self) -> Dict[str, Any]:
        """Get sharding statistics."""
        total_items = sum(self.shard_sizes)
        
        return {
            "total_shards": self.num_shards,
            "total_items": total_items,
            "shard_sizes": self.shard_sizes,
            "avg_shard_size": total_items / self.num_shards if self.num_shards > 0 else 0,
            "load_balance_ratio": max(self.shard_sizes) / max(min(self.shard_sizes), 1)
        }


class APIRateLimiter:
    """
    API Rate Limiting Implementation
    
    Implements various rate limiting algorithms to protect
    APIs from abuse and ensure fair usage.
    """
    
    def __init__(self, max_requests: int, time_window: int):
        self.max_requests = max_requests
        self.time_window = time_window
        
        # Token bucket algorithm
        self.tokens = max_requests
        self.last_refill = time.time()
        
        # Fixed window counter
        self.window_start = time.time()
        self.window_requests = 0
        
        # Sliding window log
        self.request_log = deque()
        
        # Per-client tracking
        self.client_buckets = defaultdict(lambda: {
            'tokens': max_requests,
            'last_refill': time.time(),
            'requests': deque()
        })
    
    def token_bucket_allow(self, client_id: str = None) -> bool:
        """Token bucket rate limiting algorithm."""
        bucket = self.client_buckets[client_id] if client_id else self
        current_time = time.time()
        
        # Refill tokens based on elapsed time
        elapsed = current_time - bucket.get('last_refill', self.last_refill)
        tokens_to_add = elapsed * (self.max_requests / self.time_window)
        
        if client_id:
            bucket['tokens'] = min(
                self.max_requests,
                bucket['tokens'] + tokens_to_add
            )
            bucket['last_refill'] = current_time
            
            if bucket['tokens'] >= 1:
                bucket['tokens'] -= 1
                return True
        else:
            self.tokens = min(self.max_requests, self.tokens + tokens_to_add)
            self.last_refill = current_time
            
            if self.tokens >= 1:
                self.tokens -= 1
                return True
        
        return False
    
    def fixed_window_allow(self) -> bool:
        """Fixed window rate limiting algorithm."""
        current_time = time.time()
        
        # Check if we need to reset the window
        if current_time - self.window_start >= self.time_window:
            self.window_start = current_time
            self.window_requests = 0
        
        if self.window_requests < self.max_requests:
            self.window_requests += 1
            return True
        
        return False
    
    def sliding_window_allow(self, client_id: str = None) -> bool:
        """Sliding window log rate limiting algorithm."""
        current_time = time.time()
        requests = self.client_buckets[client_id]['requests'] if client_id else self.request_log
        
        # Remove old requests outside the window
        while requests and current_time - requests[0] > self.time_window:
            requests.popleft()
        
        if len(requests) < self.max_requests:
            requests.append(current_time)
            return True
        
        return False


class MicroserviceOrchestrator:
    """
    Microservice Orchestration Pattern
    
    Demonstrates service discovery, circuit breaker, and
    orchestration patterns for microservices architecture.
    """
    
    def __init__(self):
        self.services: Dict[str, Dict[str, Any]] = {}
        self.circuit_breakers: Dict[str, Dict[str, Any]] = {}
        self.service_mesh = defaultdict(list)
    
    def register_service(self, name: str, host: str, port: int, health_check_url: str):
        """Register a microservice."""
        self.services[name] = {
            'host': host,
            'port': port,
            'health_check_url': health_check_url,
            'status': 'healthy',
            'last_health_check': time.time()
        }
        
        # Initialize circuit breaker
        self.circuit_breakers[name] = {
            'state': 'CLOSED',  # CLOSED, OPEN, HALF_OPEN
            'failure_count': 0,
            'success_count': 0,
            'last_failure_time': None,
            'timeout': 60,  # seconds
            'failure_threshold': 5
        }
    
    def discover_service(self, name: str) -> Optional[Dict[str, Any]]:
        """Discover a registered service."""
        return self.services.get(name)
    
    def call_service(self, service_name: str, endpoint: str, data: Any = None) -> Dict[str, Any]:
        """Call a microservice with circuit breaker pattern."""
        circuit_breaker = self.circuit_breakers.get(service_name)
        if not circuit_breaker:
            return {"error": "Service not found"}
        
        # Check circuit breaker state
        if circuit_breaker['state'] == 'OPEN':
            if time.time() - circuit_breaker['last_failure_time'] > circuit_breaker['timeout']:
                circuit_breaker['state'] = 'HALF_OPEN'
            else:
                return {"error": "Circuit breaker is OPEN"}
        
        try:
            # Simulate service call
            service_info = self.services.get(service_name)
            if not service_info or service_info['status'] != 'healthy':
                raise Exception(f"Service {service_name} is unhealthy")
            
            # Simulate successful call
            response = {
                "status": "success",
                "service": service_name,
                "endpoint": endpoint,
                "data": data,
                "timestamp": time.time()
            }
            
            # Update circuit breaker on success
            if circuit_breaker['state'] == 'HALF_OPEN':
                circuit_breaker['state'] = 'CLOSED'
            circuit_breaker['success_count'] += 1
            circuit_breaker['failure_count'] = 0
            
            return response
            
        except Exception as e:
            # Update circuit breaker on failure
            circuit_breaker['failure_count'] += 1
            circuit_breaker['last_failure_time'] = time.time()
            
            if circuit_breaker['failure_count'] >= circuit_breaker['failure_threshold']:
                circuit_breaker['state'] = 'OPEN'
            
            return {"error": str(e)}
    
    def health_check(self, service_name: str) -> bool:
        """Perform health check on a service."""
        service = self.services.get(service_name)
        if not service:
            return False
        
        # Simulate health check
        is_healthy = random.random() > 0.1  # 90% healthy
        service['status'] = 'healthy' if is_healthy else 'unhealthy'
        service['last_health_check'] = time.time()
        
        return is_healthy


def demonstrate_load_balancing():
    """Demonstrate different load balancing strategies."""
    print("Load Balancing Demonstration")
    print("=" * 40)
    
    # Create servers
    servers = [
        Server("server-1", "192.168.1.1", 8080, weight=3),
        Server("server-2", "192.168.1.2", 8080, weight=2),
        Server("server-3", "192.168.1.3", 8080, weight=1),
    ]
    
    strategies = [
        LoadBalancingStrategy.ROUND_ROBIN,
        LoadBalancingStrategy.LEAST_CONNECTIONS,
        LoadBalancingStrategy.WEIGHTED_ROUND_ROBIN
    ]
    
    for strategy in strategies:
        print(f"\n{strategy.value.upper()} Strategy:")
        print("-" * 30)
        
        lb = LoadBalancer(strategy)
        for server in servers:
            lb.add_server(server)
        
        # Simulate requests
        request_distribution = defaultdict(int)
        for i in range(12):
            server = lb.get_server(f"request-{i}")
            if server:
                request_distribution[server.id] += 1
                server.current_connections = request_distribution[server.id]
        
        for server_id, count in request_distribution.items():
            print(f"  {server_id}: {count} requests")


def demonstrate_caching():
    """Demonstrate caching strategies and performance."""
    print("\n\nCaching System Demonstration")
    print("=" * 40)
    
    strategies = [CacheStrategy.LRU, CacheStrategy.LFU, CacheStrategy.FIFO]
    
    for strategy in strategies:
        print(f"\n{strategy.value.upper()} Cache Strategy:")
        print("-" * 30)
        
        cache = DistributedCache(max_size=5, strategy=strategy)
        
        # Simulate cache operations
        operations = [
            ("put", "key1", "value1"),
            ("put", "key2", "value2"),
            ("get", "key1", None),
            ("put", "key3", "value3"),
            ("put", "key4", "value4"),
            ("put", "key5", "value5"),
            ("get", "key2", None),
            ("put", "key6", "value6"),  # This should trigger eviction
            ("get", "key1", None),
        ]
        
        for op, key, value in operations:
            if op == "put":
                cache.put(key, value)
                print(f"  PUT {key}: {value}")
            else:
                result = cache.get(key)
                print(f"  GET {key}: {'HIT' if result else 'MISS'}")
        
        stats = cache.get_stats()
        print(f"  Stats: {stats['hit_rate']:.2f} hit rate, {stats['evictions']} evictions")


def demonstrate_sharding():
    """Demonstrate database sharding strategies."""
    print("\n\nDatabase Sharding Demonstration")
    print("=" * 40)
    
    db = DatabaseSharding(num_shards=4)
    
    # Test data
    users = [
        ("alice", {"age": 25, "city": "NYC"}),
        ("bob", {"age": 30, "city": "SF"}),
        ("charlie", {"age": 28, "city": "LA"}),
        ("diana", {"age": 32, "city": "Chicago"}),
        ("eve", {"age": 27, "city": "Boston"}),
        ("frank", {"age": 35, "city": "Seattle"}),
    ]
    
    print("\nHash-based Sharding:")
    for user_id, user_data in users:
        db.put(user_id, user_data, strategy="hash")
        shard_id = db.hash_shard(user_id)
        print(f"  {user_id} -> Shard {shard_id}")
    
    stats = db.get_shard_stats()
    print(f"\nSharding Stats: {stats}")


def demonstrate_microservices():
    """Demonstrate microservice patterns."""
    print("\n\nMicroservice Orchestration Demonstration")
    print("=" * 50)
    
    orchestrator = MicroserviceOrchestrator()
    
    # Register services
    services = [
        ("user-service", "192.168.1.10", 8001, "/health"),
        ("order-service", "192.168.1.11", 8002, "/health"),
        ("payment-service", "192.168.1.12", 8003, "/health"),
    ]
    
    for name, host, port, health_url in services:
        orchestrator.register_service(name, host, port, health_url)
    
    print("Registered Services:")
    for service_name in orchestrator.services:
        service = orchestrator.discover_service(service_name)
        print(f"  {service_name}: {service['host']}:{service['port']}")
    
    print("\nService Calls with Circuit Breaker:")
    calls = [
        ("user-service", "/api/users/123"),
        ("order-service", "/api/orders/456"),
        ("payment-service", "/api/payments/789"),
        ("nonexistent-service", "/api/test"),
    ]
    
    for service, endpoint in calls:
        response = orchestrator.call_service(service, endpoint)
        if "error" in response:
            print(f"  {service}{endpoint}: ERROR - {response['error']}")
        else:
            print(f"  {service}{endpoint}: SUCCESS")


def main():
    """Main demonstration of system design principles."""
    print("System Design Fundamentals Demonstration")
    print("=" * 50)
    
    try:
        demonstrate_load_balancing()
        demonstrate_caching()
        demonstrate_sharding()
        demonstrate_microservices()
        
    except KeyboardInterrupt:
        print("\nDemo interrupted by user")
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()
    
    print(f"\n{'='*50}")
    print("System design demonstration complete!")


if __name__ == "__main__":
    main()


# ============================================================================
# SYSTEM DESIGN BEST PRACTICES AND PATTERNS
# ============================================================================

"""
🏗️ SYSTEM DESIGN BEST PRACTICES:

📈 SCALABILITY PATTERNS:
• Horizontal scaling (scale out) vs Vertical scaling (scale up)
• Load balancing for request distribution
• Database sharding and partitioning
• Caching at multiple layers (CDN, application, database)
• Asynchronous processing with message queues

🔧 RELIABILITY PATTERNS:
• Circuit breaker pattern for fault tolerance
• Retry mechanisms with exponential backoff
• Bulkhead pattern for resource isolation
• Health checks and monitoring
• Graceful degradation and fallback mechanisms

⚡ PERFORMANCE OPTIMIZATION:
• Caching strategies (LRU, LFU, Write-through, Write-back)
• Database indexing and query optimization
• CDN for static content delivery
• Connection pooling and resource management
• Lazy loading and pagination

🏗️ ARCHITECTURAL PATTERNS:
• Microservices vs Monolithic architecture
• Event-driven architecture with message brokers
• CQRS (Command Query Responsibility Segregation)
• API Gateway pattern for service routing
• Service mesh for inter-service communication

📊 DATA MANAGEMENT:
• ACID properties vs BASE (Eventually consistent)
• SQL vs NoSQL database selection
• Data replication strategies (Master-slave, Master-master)
• Consistent hashing for distributed systems
• Event sourcing for audit trails

🔐 SECURITY CONSIDERATIONS:
• Authentication and authorization (OAuth, JWT)
• Rate limiting and throttling
• Input validation and sanitization
• HTTPS/TLS encryption
• API security best practices

📝 MONITORING AND OBSERVABILITY:
• Logging, metrics, and distributed tracing
• Health checks and alerting
• Performance monitoring and profiling
• Capacity planning and resource management
• Incident response and recovery procedures

💡 DESIGN INTERVIEW TIPS:
• Start with requirements gathering and clarification
• Estimate scale (users, requests per second, data size)
• Design high-level architecture first
• Deep dive into specific components
• Discuss trade-offs and alternatives
• Consider failure scenarios and reliability
• Scale the system step by step
• Justify technology choices

🎯 COMMON DESIGN QUESTIONS:
• Design a URL shortener (like bit.ly)
• Design a social media feed (like Twitter)
• Design a chat system (like WhatsApp)
• Design a video streaming service (like Netflix)
• Design a ride-sharing service (like Uber)
• Design a search engine (like Google)
• Design a recommendation system
• Design a distributed cache system
"""
