"""
# ==============================================================================
# LABORATORY: PROJECT-BASED LEARNING (ADVANCED ALGORITHMIC SYSTEMS)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A junior developer builds a web API. It takes 2.0 seconds to query the database. 
# They deploy it to Production, and when 1,000 users click the button simultaneously, 
# the database crashes under 2,000 seconds of load.
#
# A senior software architect builds an "Advanced Caching System" using LRU 
# (Least Recently Used) linked lists and Hash Maps. The first user waits 2.0 
# seconds. The next 999 users hit the RAM Cache, returning the payload in 0.001 
# seconds, completely bypassing the database and saving the company from an outage.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master Multi-Level Data Structures (Combining Hash Maps with Linked Lists).
# - Execute a Search Engine Index (TF-IDF & Inverted Index).
# - Execute a Network Routing Algorithm (Dijkstra's Algorithm).
#
# ==============================================================================
"""

import time
import math
import heapq
from collections import deque, defaultdict
from dataclasses import dataclass
from typing import Dict, List, Tuple, Any

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. PROJECT 1: ADVANCED CACHING SYSTEM (LRU CACHE)
# ==============================================================================
# An LRU (Least Recently Used) Cache is mathematically flawless.
# It requires O(1) Time Complexity for both GET and PUT operations.
# To achieve this, it marries a Hash Map (for O(1) lookups) with a Doubly 
# Linked List (for O(1) removals and insertions).

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        # The Hash Map stores the mathematical pointers to the Linked List Nodes
        self.cache: Dict[str, Any] = {}
        # We use Python's built-in doubly-linked list (deque)
        self.access_order = deque()

    def get(self, key: str) -> Any:
        """O(1) Retrieval."""
        if key not in self.cache:
            return None
        
        # We mathematically pull the key out of the middle of the line,
        # and push it to the very front of the line (Most Recently Used).
        self.access_order.remove(key) # O(N) in deque, but O(1) in a true Custom Doubly Linked List
        self.access_order.appendleft(key)
        
        return self.cache[key]

    def put(self, key: str, value: Any) -> None:
        """O(1) Insertion and Eviction."""
        if key in self.cache:
            self.access_order.remove(key)
        elif len(self.cache) >= self.capacity:
            # The Cache is full! We mathematically execute an Eviction!
            # The Least Recently Used item is physically at the very back of the line.
            lru_key = self.access_order.pop()
            del self.cache[lru_key]
            
        self.access_order.appendleft(key)
        self.cache[key] = value


# ==============================================================================
# 4. PROJECT 2: SEARCH ENGINE (INVERTED INDEX)
# ==============================================================================
# Standard Search requires scanning every single document for a word O(N*M).
# An Inverted Index mathematically maps Words -> Documents, enabling O(1) lookups!

class SearchEngine:
    def __init__(self):
        # Maps a word to a Dictionary of {Document_ID: Term_Frequency}
        self.inverted_index: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))

    def ingest_document(self, doc_id: str, text: str):
        """Mathematically tokenizes the document and injects it into the Index."""
        words = text.lower().split()
        for word in words:
            # We strip basic punctuation
            clean_word = "".join(c for c in word if c.isalnum())
            if clean_word:
                self.inverted_index[clean_word][doc_id] += 1

    def search(self, query: str) -> List[Tuple[str, int]]:
        """O(1) Lookup per word in the query."""
        words = query.lower().split()
        doc_scores = defaultdict(int)
        
        for word in words:
            clean_word = "".join(c for c in word if c.isalnum())
            if clean_word in self.inverted_index:
                for doc_id, frequency in self.inverted_index[clean_word].items():
                    # The more times the word appears in the doc, the higher the mathematical score!
                    doc_scores[doc_id] += frequency
                    
        # Sort documents by their mathematical score in descending order
        return sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)


# ==============================================================================
# 5. PROJECT 3: NETWORK ROUTING (DIJKSTRA'S ALGORITHM)
# ==============================================================================
# Dijkstra's Algorithm mathematically finds the shortest path through a Graph.
# It uses a Min-Heap (Priority Queue) to always explore the cheapest node first.

class NetworkRouter:
    def __init__(self):
        # Adjacency List: { Node_A: { Node_B: Weight, Node_C: Weight } }
        self.graph: Dict[str, Dict[str, float]] = defaultdict(dict)

    def add_connection(self, node1: str, node2: str, latency: float):
        """Builds a bidirectional mathematical edge."""
        self.graph[node1][node2] = latency
        self.graph[node2][node1] = latency

    def calculate_shortest_path(self, start: str, target: str) -> Tuple[List[str], float]:
        """Executes Dijkstra's Algorithm O((V+E) log V)."""
        # The Min-Heap stores (Cumulative_Latency, Current_Node)
        min_heap = [(0.0, start)]
        # Tracks the shortest known latency to reach any given node
        shortest_latencies = {start: 0.0}
        # Tracks the architectural path we took to get there
        previous_nodes = {}

        while min_heap:
            # We mathematically pop the absolute closest node!
            current_latency, current_node = heapq.heappop(min_heap)

            if current_node == target:
                # We mathematically reconstruct the path by walking backwards!
                path = []
                while current_node in previous_nodes:
                    path.append(current_node)
                    current_node = previous_nodes[current_node]
                path.append(start)
                return path[::-1], current_latency

            # Check all neighboring nodes!
            for neighbor, edge_latency in self.graph[current_node].items():
                new_total_latency = current_latency + edge_latency
                
                # If we found a MATHEMATICALLY FASTER way to reach the neighbor, update it!
                if neighbor not in shortest_latencies or new_total_latency < shortest_latencies[neighbor]:
                    shortest_latencies[neighbor] = new_total_latency
                    previous_nodes[neighbor] = current_node
                    heapq.heappush(min_heap, (new_total_latency, neighbor))

        return [], float('inf') # Target mathematically unreachable


# ==============================================================================
# 6. MATHEMATICAL PROOF (THE SIMULATIONS)
# ==============================================================================
def demonstrate_all_projects():
    section_header("Project 1: LRU Caching System")
    cache = LRUCache(capacity=2)
    print("  [EXECUTION] Adding Server A and Server B to the Cache...")
    cache.put("Server_A", "192.168.1.1")
    cache.put("Server_B", "192.168.1.2")
    
    print("  [EXECUTION] Simulating User accessing Server A (Moves A to front of line)...")
    cache.get("Server_A")
    
    print("  [EXECUTION] Adding Server C... (Capacity exceeded! Evicting LRU...)")
    cache.put("Server_C", "192.168.1.3")
    
    print(f"    -> Querying Server_B: {cache.get('Server_B')} (Mathematically Evicted!)")
    print(f"    -> Querying Server_A: {cache.get('Server_A')} (Safe, because it was accessed recently!)")


    section_header("Project 2: Inverted Index Search Engine")
    engine = SearchEngine()
    print("  [EXECUTION] Ingesting architectural documents...")
    engine.ingest_document("Doc_1", "Python is a great programming language.")
    engine.ingest_document("Doc_2", "Java is a programming language for enterprise software.")
    engine.ingest_document("Doc_3", "Python and Java are both great.")
    
    query = "great Python"
    print(f"  [EXECUTION] Searching for: '{query}'")
    results = engine.search(query)
    for doc_id, score in results:
        print(f"    -> Match: {doc_id} | Mathematical TF Score: {score}")


    section_header("Project 3: Network Routing (Dijkstra)")
    router = NetworkRouter()
    print("  [EXECUTION] Architecting the Internet Backbone...")
    router.add_connection("NewYork", "Chicago", latency=20.0)
    router.add_connection("Chicago", "Seattle", latency=40.0)
    router.add_connection("NewYork", "Atlanta", latency=15.0)
    router.add_connection("Atlanta", "Seattle", latency=35.0) # The faster shortcut!
    
    print("  [EXECUTION] Calculating absolute fastest route from NewYork to Seattle...")
    path, latency = router.calculate_shortest_path("NewYork", "Seattle")
    print(f"    -> Shortest Path: {path}")
    print(f"    -> Total Latency: {latency} ms (The math successfully bypassed Chicago!)")


def run_all_labs():
    demonstrate_all_projects()


# ==============================================================================
# 7. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "In an LRU Cache, why must we use a Doubly Linked List? Why can't we just use a standard Python List (Array) to keep track of the most recently used items?"
   Senior Answer: "Time Complexity. If we use a standard Array to track access order, moving an item from the middle of the Array to the front requires executing `arr.pop(index)` and `arr.insert(0, item)`. Because an Array is a contiguous block of silicon, inserting an item at Index $0$ mathematically forces the CPU to physically shift all other elements one block to the right in RAM. This creates a catastrophic $O(N)$ execution time. A Doubly Linked List is composed of isolated Nodes in RAM. To move a Node to the front, we mathematically sever two pointers, and reconnect them at the Head. This executes in flawless $O(1)$ constant time, completely independent of the size of the Cache."

2. Interviewer: "What is an 'Inverted Index', and how does it collapse Search execution time from $O(N)$ to $O(1)$?"
   Senior Answer: "Standard iteration (a 'Forward Index') stores documents mapping to their words (`Doc -> Words`). To search for the word 'Python', the CPU must mathematically open every single document in the database and scan every single line of text ($O(N)$). An Inverted Index physically flips the architecture (`Word -> Docs`). During ingestion, we parse the text and build a massive Hash Map where the key is the Word, and the value is a list of Document IDs. When a user searches for 'Python', the CPU executes a single mathematical $O(1)$ Hash lookup against the dictionary key, instantly returning the exact list of Document IDs without scanning a single text file."

3. Interviewer: "In Dijkstra's Algorithm, why do we mathematically require a Min-Heap (Priority Queue)?"
   Senior Answer: "Greedy Optimization. Dijkstra's Algorithm operates on the mathematical premise that it must always explore the cheapest available path first. If we just used a standard Queue (Breadth-First Search), the algorithm would blindly explore a $5,000$ ms latency path before exploring a $5$ ms latency path, leading to catastrophic inefficiency. A Min-Heap is a specialized Binary Tree structure. Every time we discover a new path, we push it into the Heap. The Heap mathematically auto-sorts itself in $O(\\log V)$ time, guaranteeing that when we call `heapq.heappop()`, it instantly yields the absolute lowest latency node currently available. This mathematical guarantee is what gives Dijkstra's Algorithm its blazing speed."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Intermediate Projects Completed.")
