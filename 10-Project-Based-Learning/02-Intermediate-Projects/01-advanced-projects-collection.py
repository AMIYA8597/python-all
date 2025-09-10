#!/usr/bin/env python3
"""
Advanced DSA Projects Collection - Intermediate Level
====================================================

This module contains intermediate-level projects that demonstrate
advanced data structures and algorithms concepts including caching systems,
search engines, routing algorithms, and distributed systems.

Author: Python DSA Master
Date: 2024
"""

import json
import time
import math
import random
import heapq
import hashlib
from typing import Dict, List, Tuple, Any, Optional, Set, Union
from collections import defaultdict, deque, Counter
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta

# ==============================================================================
# PROJECT 1: ADVANCED CACHING SYSTEM
# ==============================================================================

class CachePolicy(Enum):
    """Cache replacement policies."""
    LRU = "lru"
    LFU = "lfu"
    FIFO = "fifo"
    RANDOM = "random"

@dataclass
class CacheEntry:
    """Cache entry with metadata."""
    key: str
    value: Any
    access_count: int = 0
    last_accessed: datetime = field(default_factory=datetime.now)
    created_at: datetime = field(default_factory=datetime.now)
    size: int = 1

class AdvancedCacheSystem:
    """
    Multi-level caching system with different replacement policies.
    Uses combination of hash tables and specialized data structures.
    """
    
    def __init__(self, capacity: int = 100, policy: CachePolicy = CachePolicy.LRU):
        self.capacity = capacity
        self.policy = policy
        self.cache: Dict[str, CacheEntry] = {}
        self.size = 0
        
        # For LRU: Use doubly linked list
        self.access_order = deque()  # Most recent at right
        
        # For LFU: Use min heap
        self.frequency_heap = []
        self.freq_counter = Counter()
        
        # Statistics
        self.hits = 0
        self.misses = 0
        self.evictions = 0
        
    def _update_access(self, key: str) -> None:
        """Update access information for different policies."""
        entry = self.cache[key]
        entry.last_accessed = datetime.now()
        entry.access_count += 1
        
        if self.policy == CachePolicy.LRU:
            # Move to end (most recent)
            if key in self.access_order:
                self.access_order.remove(key)
            self.access_order.append(key)
            
        elif self.policy == CachePolicy.LFU:
            self.freq_counter[key] += 1
    
    def _evict(self) -> Optional[str]:
        """Evict an entry based on the policy."""
        if not self.cache:
            return None
        
        evict_key = None
        
        if self.policy == CachePolicy.LRU:
            # Remove least recently used (leftmost)
            evict_key = self.access_order.popleft()
            
        elif self.policy == CachePolicy.LFU:
            # Remove least frequently used
            if self.freq_counter:
                evict_key = self.freq_counter.most_common()[-1][0]
                del self.freq_counter[evict_key]
                
        elif self.policy == CachePolicy.FIFO:
            # Remove first in (oldest)
            evict_key = min(self.cache.keys(), 
                          key=lambda k: self.cache[k].created_at)
            
        elif self.policy == CachePolicy.RANDOM:
            # Remove random entry
            evict_key = random.choice(list(self.cache.keys()))
        
        if evict_key and evict_key in self.cache:
            self.size -= self.cache[evict_key].size
            del self.cache[evict_key]
            self.evictions += 1
            
        return evict_key
    
    def get(self, key: str) -> Tuple[Any, bool]:
        """Get value from cache."""
        if key in self.cache:
            self.hits += 1
            self._update_access(key)
            return self.cache[key].value, True
        else:
            self.misses += 1
            return None, False
    
    def put(self, key: str, value: Any, size: int = 1) -> bool:
        """Put value in cache."""
        # If key exists, update
        if key in self.cache:
            old_size = self.cache[key].size
            self.cache[key].value = value
            self.cache[key].size = size
            self.size += size - old_size
            self._update_access(key)
            return True
        
        # Evict if necessary
        while self.size + size > self.capacity and self.cache:
            self._evict()
        
        # Add new entry
        if self.size + size <= self.capacity:
            entry = CacheEntry(key, value, size=size)
            self.cache[key] = entry
            self.size += size
            
            if self.policy == CachePolicy.LRU:
                self.access_order.append(key)
            elif self.policy == CachePolicy.LFU:
                self.freq_counter[key] = 1
            
            return True
        
        return False
    
    def delete(self, key: str) -> bool:
        """Delete entry from cache."""
        if key in self.cache:
            self.size -= self.cache[key].size
            del self.cache[key]
            
            if self.policy == CachePolicy.LRU and key in self.access_order:
                self.access_order.remove(key)
            elif self.policy == CachePolicy.LFU and key in self.freq_counter:
                del self.freq_counter[key]
            
            return True
        return False
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        total_requests = self.hits + self.misses
        hit_ratio = self.hits / total_requests if total_requests > 0 else 0
        
        return {
            'policy': self.policy.value,
            'capacity': self.capacity,
            'size': self.size,
            'entries': len(self.cache),
            'hits': self.hits,
            'misses': self.misses,
            'evictions': self.evictions,
            'hit_ratio': hit_ratio,
            'utilization': self.size / self.capacity
        }

# ==============================================================================
# PROJECT 2: INTELLIGENT SEARCH ENGINE
# ==============================================================================

@dataclass
class Document:
    """Document with metadata."""
    doc_id: str
    title: str
    content: str
    url: str = ""
    timestamp: datetime = field(default_factory=datetime.now)
    
class SearchEngine:
    """
    Intelligent search engine with ranking, indexing, and query processing.
    Uses inverted index, tf-idf scoring, and advanced data structures.
    """
    
    def __init__(self):
        self.documents: Dict[str, Document] = {}
        self.inverted_index: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
        self.document_frequencies: Dict[str, int] = defaultdict(int)
        self.total_documents = 0
        
        # For query suggestions
        self.query_history = deque(maxlen=1000)
        self.query_trie = self._build_trie()
        
        # Performance metrics
        self.search_times = []
        self.popular_queries = Counter()
    
    class TrieNode:
        """Trie node for query suggestions."""
        def __init__(self):
            self.children = {}
            self.is_end_of_query = False
            self.frequency = 0
    
    def _build_trie(self) -> 'TrieNode':
        """Build trie for query suggestions."""
        return self.TrieNode()
    
    def _tokenize(self, text: str) -> List[str]:
        """Tokenize text into terms."""
        import re
        # Simple tokenization - can be enhanced with stemming, stop words, etc.
        terms = re.findall(r'\b[a-zA-Z]{2,}\b', text.lower())
        return terms
    
    def add_document(self, doc: Document) -> None:
        """Add document to search index."""
        if doc.doc_id in self.documents:
            return  # Document already exists
        
        self.documents[doc.doc_id] = doc
        self.total_documents += 1
        
        # Tokenize and build inverted index
        content_terms = self._tokenize(doc.content)
        title_terms = self._tokenize(doc.title)
        
        # Title terms get higher weight
        all_terms = content_terms + title_terms * 2
        
        for term in set(all_terms):
            self.inverted_index[term][doc.doc_id] = all_terms.count(term)
            if doc.doc_id == list(self.inverted_index[term].keys())[-1]:
                self.document_frequencies[term] += 1
    
    def _calculate_tf_idf(self, term: str, doc_id: str) -> float:
        """Calculate TF-IDF score for term in document."""
        if term not in self.inverted_index or doc_id not in self.inverted_index[term]:
            return 0.0
        
        # Term frequency
        tf = self.inverted_index[term][doc_id]
        doc_terms = sum(self.inverted_index[t][doc_id] 
                       for t in self.inverted_index if doc_id in self.inverted_index[t])
        tf_normalized = tf / doc_terms if doc_terms > 0 else 0
        
        # Inverse document frequency
        df = self.document_frequencies[term]
        idf = math.log(self.total_documents / df) if df > 0 else 0
        
        return tf_normalized * idf
    
    def _add_query_to_trie(self, query: str) -> None:
        """Add query to trie for suggestions."""
        node = self.query_trie
        for char in query.lower():
            if char not in node.children:
                node.children[char] = self.TrieNode()
            node = node.children[char]
        
        node.is_end_of_query = True
        node.frequency += 1
    
    def get_query_suggestions(self, prefix: str, limit: int = 5) -> List[Tuple[str, int]]:
        """Get query suggestions based on prefix."""
        if not prefix:
            return []
        
        # Traverse trie to find prefix
        node = self.query_trie
        for char in prefix.lower():
            if char not in node.children:
                return []
            node = node.children[char]
        
        # Collect all queries with this prefix
        suggestions = []
        
        def dfs(current_node, current_query):
            if current_node.is_end_of_query:
                suggestions.append((current_query, current_node.frequency))
            
            for char, child_node in current_node.children.items():
                dfs(child_node, current_query + char)
        
        dfs(node, prefix.lower())
        
        # Sort by frequency and return top suggestions
        suggestions.sort(key=lambda x: x[1], reverse=True)
        return suggestions[:limit]
    
    def search(self, query: str, limit: int = 10) -> List[Tuple[str, float]]:
        """Search for documents matching query."""
        start_time = time.time()
        
        # Record query
        self.query_history.append(query)
        self.popular_queries[query.lower()] += 1
        self._add_query_to_trie(query)
        
        # Tokenize query
        query_terms = self._tokenize(query)
        if not query_terms:
            return []
        
        # Find candidate documents
        candidate_docs = set()
        for term in query_terms:
            if term in self.inverted_index:
                candidate_docs.update(self.inverted_index[term].keys())
        
        # Score documents
        doc_scores = {}
        for doc_id in candidate_docs:
            score = 0.0
            for term in query_terms:
                score += self._calculate_tf_idf(term, doc_id)
            doc_scores[doc_id] = score
        
        # Sort by score
        results = sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)
        
        # Record search time
        search_time = time.time() - start_time
        self.search_times.append(search_time)
        
        return results[:limit]
    
    def get_search_stats(self) -> Dict[str, Any]:
        """Get search engine statistics."""
        avg_search_time = sum(self.search_times) / len(self.search_times) if self.search_times else 0
        
        return {
            'total_documents': self.total_documents,
            'vocabulary_size': len(self.inverted_index),
            'total_searches': len(self.query_history),
            'avg_search_time': avg_search_time,
            'popular_queries': dict(self.popular_queries.most_common(5)),
            'unique_queries': len(set(self.query_history))
        }

# ==============================================================================
# PROJECT 3: NETWORK ROUTING ALGORITHM
# ==============================================================================

@dataclass
class NetworkNode:
    """Network node with routing information."""
    node_id: str
    ip_address: str
    location: Tuple[float, float]  # (latitude, longitude)
    capacity: int = 100
    current_load: int = 0
    
class NetworkRouter:
    """
    Advanced network routing system using Dijkstra's algorithm with
    dynamic weight adjustment based on network conditions.
    """
    
    def __init__(self):
        self.nodes: Dict[str, NetworkNode] = {}
        self.graph: Dict[str, Dict[str, float]] = defaultdict(lambda: defaultdict(float))
        self.routing_table: Dict[str, Dict[str, Tuple[str, float]]] = {}
        
        # Traffic monitoring
        self.traffic_history: Dict[Tuple[str, str], List[Tuple[datetime, float]]] = defaultdict(list)
        self.congestion_threshold = 0.8
        
        # Performance metrics
        self.route_calculations = 0
        self.total_calculation_time = 0.0
    
    def add_node(self, node: NetworkNode) -> None:
        """Add node to network."""
        self.nodes[node.node_id] = node
    
    def add_connection(self, node1: str, node2: str, base_latency: float, bandwidth: float) -> None:
        """Add bidirectional connection between nodes."""
        if node1 not in self.nodes or node2 not in self.nodes:
            return
        
        # Calculate initial weight based on latency and bandwidth
        weight = base_latency + (1.0 / bandwidth) * 1000  # Higher bandwidth = lower weight
        
        self.graph[node1][node2] = weight
        self.graph[node2][node1] = weight
    
    def _calculate_dynamic_weight(self, node1: str, node2: str, base_weight: float) -> float:
        """Calculate dynamic weight based on current network conditions."""
        if node1 not in self.nodes or node2 not in self.nodes:
            return float('inf')
        
        # Factor in current node loads
        load1 = self.nodes[node1].current_load / self.nodes[node1].capacity
        load2 = self.nodes[node2].current_load / self.nodes[node2].capacity
        
        # Increase weight if nodes are heavily loaded
        load_factor = 1.0 + (load1 + load2)
        
        # Check recent traffic on this link
        link_key = (min(node1, node2), max(node1, node2))
        if link_key in self.traffic_history:
            recent_traffic = [traffic for timestamp, traffic in self.traffic_history[link_key]
                            if datetime.now() - timestamp < timedelta(minutes=5)]
            
            if recent_traffic:
                avg_traffic = sum(recent_traffic) / len(recent_traffic)
                if avg_traffic > self.congestion_threshold:
                    load_factor *= 2.0  # Double weight for congested links
        
        return base_weight * load_factor
    
    def find_shortest_path(self, start: str, end: str) -> Tuple[List[str], float]:
        """Find shortest path using modified Dijkstra's algorithm."""
        if start not in self.nodes or end not in self.nodes:
            return [], float('inf')
        
        start_time = time.time()
        self.route_calculations += 1
        
        # Dijkstra's algorithm with dynamic weights
        distances = {node: float('inf') for node in self.nodes}
        distances[start] = 0.0
        previous = {}
        unvisited = [(0.0, start)]
        visited = set()
        
        while unvisited:
            current_distance, current_node = heapq.heappop(unvisited)
            
            if current_node in visited:
                continue
            
            visited.add(current_node)
            
            if current_node == end:
                break
            
            for neighbor in self.graph[current_node]:
                if neighbor in visited:
                    continue
                
                base_weight = self.graph[current_node][neighbor]
                dynamic_weight = self._calculate_dynamic_weight(current_node, neighbor, base_weight)
                distance = current_distance + dynamic_weight
                
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous[neighbor] = current_node
                    heapq.heappush(unvisited, (distance, neighbor))
        
        # Reconstruct path
        path = []
        current = end
        while current in previous:
            path.append(current)
            current = previous[current]
        
        if path and current == start:
            path.append(start)
            path.reverse()
            
            # Record calculation time
            calculation_time = time.time() - start_time
            self.total_calculation_time += calculation_time
            
            return path, distances[end]
        
        return [], float('inf')
    
    def find_k_shortest_paths(self, start: str, end: str, k: int = 3) -> List[Tuple[List[str], float]]:
        """Find k shortest paths using Yen's algorithm (simplified)."""
        paths = []
        
        # Find shortest path
        shortest_path, shortest_distance = self.find_shortest_path(start, end)
        if shortest_path:
            paths.append((shortest_path, shortest_distance))
        
        # Find alternative paths by removing edges
        for i in range(1, k):
            if not paths:
                break
            
            candidate_paths = []
            
            for j in range(len(paths[-1][0]) - 1):
                # Remove edge temporarily
                node1 = paths[-1][0][j]
                node2 = paths[-1][0][j + 1]
                
                original_weight = self.graph[node1][node2]
                del self.graph[node1][node2]
                del self.graph[node2][node1]
                
                # Find alternative path
                alt_path, alt_distance = self.find_shortest_path(start, end)
                if alt_path:
                    candidate_paths.append((alt_path, alt_distance))
                
                # Restore edge
                self.graph[node1][node2] = original_weight
                self.graph[node2][node1] = original_weight
            
            # Select best alternative
            if candidate_paths:
                candidate_paths.sort(key=lambda x: x[1])
                for path, distance in candidate_paths:
                    if path not in [p[0] for p in paths]:
                        paths.append((path, distance))
                        break
        
        return paths
    
    def update_traffic(self, node1: str, node2: str, traffic_level: float) -> None:
        """Update traffic information for a link."""
        link_key = (min(node1, node2), max(node1, node2))
        self.traffic_history[link_key].append((datetime.now(), traffic_level))
        
        # Keep only recent history
        cutoff_time = datetime.now() - timedelta(hours=1)
        self.traffic_history[link_key] = [
            (timestamp, traffic) for timestamp, traffic in self.traffic_history[link_key]
            if timestamp > cutoff_time
        ]
    
    def update_node_load(self, node_id: str, load: int) -> None:
        """Update current load for a node."""
        if node_id in self.nodes:
            self.nodes[node_id].current_load = min(load, self.nodes[node_id].capacity)
    
    def get_routing_stats(self) -> Dict[str, Any]:
        """Get routing statistics."""
        avg_calculation_time = (self.total_calculation_time / self.route_calculations 
                              if self.route_calculations > 0 else 0)
        
        # Calculate network utilization
        total_capacity = sum(node.capacity for node in self.nodes.values())
        total_load = sum(node.current_load for node in self.nodes.values())
        utilization = total_load / total_capacity if total_capacity > 0 else 0
        
        return {
            'total_nodes': len(self.nodes),
            'total_connections': sum(len(neighbors) for neighbors in self.graph.values()) // 2,
            'route_calculations': self.route_calculations,
            'avg_calculation_time': avg_calculation_time,
            'network_utilization': utilization,
            'congested_links': len([
                link for link, history in self.traffic_history.items()
                if history and any(traffic > self.congestion_threshold 
                                 for _, traffic in history[-5:])
            ])
        }

# ==============================================================================
# DEMONSTRATION AND TESTING
# ==============================================================================

def demo_advanced_caching_system():
    """Demonstrate the advanced caching system."""
    print("Advanced Caching System Demo")
    print("=" * 40)
    
    # Test different cache policies
    policies = [CachePolicy.LRU, CachePolicy.LFU, CachePolicy.FIFO]
    
    for policy in policies:
        print(f"\nTesting {policy.value.upper()} Cache:")
        cache = AdvancedCacheSystem(capacity=50, policy=policy)
        
        # Simulate cache operations
        operations = 200
        for i in range(operations):
            if i < 60:  # Fill cache
                cache.put(f"key_{i}", f"value_{i}", size=1)
            else:  # Mix of gets and puts
                if random.random() < 0.7:  # 70% gets
                    key = f"key_{random.randint(0, 100)}"
                    value, found = cache.get(key)
                else:  # 30% puts
                    cache.put(f"key_{i}", f"value_{i}", size=1)
        
        stats = cache.get_stats()
        print(f"  Capacity: {stats['capacity']}, Entries: {stats['entries']}")
        print(f"  Hit ratio: {stats['hit_ratio']:.3f}")
        print(f"  Evictions: {stats['evictions']}")

def demo_intelligent_search_engine():
    """Demonstrate the intelligent search engine."""
    print("\nIntelligent Search Engine Demo")
    print("=" * 40)
    
    search_engine = SearchEngine()
    
    # Add sample documents
    documents = [
        Document("1", "Python Programming Guide", "Python is a powerful programming language for data science and machine learning. It has excellent libraries for data analysis."),
        Document("2", "Data Structures in Python", "Python provides built-in data structures like lists, dictionaries, and sets. These are essential for efficient programming."),
        Document("3", "Machine Learning with Python", "Machine learning algorithms can be implemented efficiently in Python using libraries like scikit-learn and tensorflow."),
        Document("4", "Web Development with Python", "Python frameworks like Django and Flask make web development straightforward and powerful."),
        Document("5", "Python for Beginners", "Learning Python programming is easy with its simple syntax and comprehensive documentation."),
    ]
    
    for doc in documents:
        search_engine.add_document(doc)
    
    print(f"Added {len(documents)} documents to search index")
    
    # Perform searches
    test_queries = ["python programming", "machine learning", "data structures", "web development"]
    
    for query in test_queries:
        print(f"\nSearch query: '{query}'")
        results = search_engine.search(query, limit=3)
        
        for i, (doc_id, score) in enumerate(results, 1):
            doc = search_engine.documents[doc_id]
            print(f"  {i}. {doc.title} (score: {score:.4f})")
    
    # Test query suggestions
    print(f"\nQuery suggestions for 'py':")
    suggestions = search_engine.get_query_suggestions("py", limit=3)
    for suggestion, freq in suggestions:
        print(f"  {suggestion} (used {freq} times)")
    
    # Show statistics
    stats = search_engine.get_search_stats()
    print(f"\nSearch Engine Statistics:")
    print(f"  Documents: {stats['total_documents']}")
    print(f"  Vocabulary size: {stats['vocabulary_size']}")
    print(f"  Searches performed: {stats['total_searches']}")
    print(f"  Average search time: {stats['avg_search_time']:.6f} seconds")

def demo_network_routing():
    """Demonstrate the network routing system."""
    print("\nNetwork Routing Algorithm Demo")
    print("=" * 40)
    
    router = NetworkRouter()
    
    # Create network topology
    nodes = [
        NetworkNode("A", "192.168.1.1", (40.7128, -74.0060), 100),  # New York
        NetworkNode("B", "192.168.1.2", (34.0522, -118.2437), 80),  # Los Angeles
        NetworkNode("C", "192.168.1.3", (41.8781, -87.6298), 90),   # Chicago
        NetworkNode("D", "192.168.1.4", (29.7604, -95.3698), 70),   # Houston
        NetworkNode("E", "192.168.1.5", (33.4484, -112.0740), 60),  # Phoenix
    ]
    
    for node in nodes:
        router.add_node(node)
    
    # Add connections (latency in ms, bandwidth in Mbps)
    connections = [
        ("A", "B", 70, 100),   # NY to LA
        ("A", "C", 30, 150),   # NY to Chicago
        ("B", "E", 20, 120),   # LA to Phoenix
        ("C", "D", 40, 100),   # Chicago to Houston
        ("D", "E", 35, 80),    # Houston to Phoenix
        ("A", "D", 50, 90),    # NY to Houston
        ("B", "C", 60, 85),    # LA to Chicago
    ]
    
    for node1, node2, latency, bandwidth in connections:
        router.add_connection(node1, node2, latency, bandwidth)
    
    print(f"Created network with {len(nodes)} nodes and {len(connections)} connections")
    
    # Test routing
    test_routes = [("A", "E"), ("B", "D"), ("A", "B")]
    
    for start, end in test_routes:
        print(f"\nRouting from {start} to {end}:")
        
        # Find shortest path
        path, distance = router.find_shortest_path(start, end)
        if path:
            print(f"  Shortest path: {' -> '.join(path)} (cost: {distance:.2f})")
        
        # Find alternative paths
        k_paths = router.find_k_shortest_paths(start, end, k=2)
        if len(k_paths) > 1:
            for i, (alt_path, alt_distance) in enumerate(k_paths[1:], 2):
                print(f"  Alternative {i}: {' -> '.join(alt_path)} (cost: {alt_distance:.2f})")
    
    # Simulate network congestion
    print(f"\nSimulating network congestion...")
    router.update_node_load("C", 85)  # Chicago at 85% capacity
    router.update_traffic("A", "C", 0.9)  # High traffic on NY-Chicago link
    
    # Test routing with congestion
    path_before = router.find_shortest_path("A", "E")
    print(f"Route A->E with congestion: {' -> '.join(path_before[0])}")
    
    # Show statistics
    stats = router.get_routing_stats()
    print(f"\nRouting Statistics:")
    print(f"  Network utilization: {stats['network_utilization']:.2%}")
    print(f"  Route calculations: {stats['route_calculations']}")
    print(f"  Average calculation time: {stats['avg_calculation_time']:.6f} seconds")
    print(f"  Congested links: {stats['congested_links']}")

def main():
    """Run all demonstrations."""
    print("Advanced DSA Projects Collection - Comprehensive Demo")
    print("=" * 60)
    
    # Run all project demos
    demo_advanced_caching_system()
    demo_intelligent_search_engine()
    demo_network_routing()
    
    print("\n" + "=" * 60)
    print("All project demonstrations completed successfully!")
    
    print("\nKey Learning Outcomes:")
    print("- Advanced caching strategies improve system performance")
    print("- Search engines use sophisticated indexing and ranking algorithms")
    print("- Network routing adapts to dynamic conditions for optimal performance")
    print("- Real-world systems combine multiple DSA concepts for complex solutions")
    
    print("\nExtension Ideas:")
    print("- Add machine learning for predictive caching")
    print("- Implement distributed search across multiple nodes")
    print("- Add quality of service (QoS) routing policies")
    print("- Build monitoring and alerting systems")

if __name__ == "__main__":
    main()
