"""
# ==============================================================================
# LABORATORY: ARTICULATION POINTS & BRIDGES (NETWORK VULNERABILITY)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You are a Site Reliability Engineer (SRE) for AWS. You have an UNDIRECTED 
# graph representing thousands of data centers and fiber-optic cables.
# 
# Vulnerability 1: "Cut Vertices" (Articulation Points). 
# If a specific Data Center goes offline, does it completely sever communication 
# between the East Coast and West Coast? If removing a single node splits the 
# network into disjoint islands, that node is an Articulation Point.
#
# Vulnerability 2: "Cut Edges" (Bridges).
# If a backhoe physically cuts a specific fiber-optic cable, does the network 
# split in half? That cable is a Bridge.
#
# A naive algorithm would simulate deleting every single node one by one and 
# running DFS/BFS to check connectivity. That takes O(V * (V+E)) time.
#
# Enter Tarjan (again). 
# Using the exact same `discovery_time` and `low_link` logic from the SCC 
# algorithm, we can find EVERY single vulnerability in the entire global network 
# in a single O(V + E) DFS pass!
#
# The Mathematical Trigger:
# When DFS explores from U to V:
# - If V's `low_link` is strictly GREATER than U's `discovery_time`, it proves 
#   V failed to find any secret back-doors leading back to U (or higher). 
#   Therefore, the pipe U-V is the ONLY way in or out. It is a Bridge!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Adapt Tarjan's SCC logic for Undirected Graphs.
# - Understand the `low_link > discovery_time` trigger for Bridges.
# - Understand the `low_link >= discovery_time` trigger for Articulation Points.
# - Handle the special "DFS Root Node" edge case.
#
# ==============================================================================
"""

from typing import Dict, List, Set, Tuple

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. TARJAN'S VULNERABILITY ENGINE (O(V + E))
# ==============================================================================
class NetworkVulnerabilityScanner:
    def __init__(self, vertices: int, graph: Dict[int, List[int]]):
        self.V = vertices
        self.graph = graph
        
        self.time = 0
        self.discovery_time = [-1] * vertices
        self.low_link = [-1] * vertices
        
        # Results
        self.bridges: List[Tuple[int, int]] = []
        self.articulation_points: Set[int] = set()
        
    def _dfs(self, u: int, parent: int):
        self.discovery_time[u] = self.time
        self.low_link[u] = self.time
        self.time += 1
        
        # Special edge case: If the node is the absolute Root of the DFS tree, 
        # it is ONLY an Articulation Point if it spawns >1 completely independent 
        # sub-trees! (If it only spawns 1 child, removing the Root just creates 
        # a slightly smaller tree, it doesn't split it into pieces).
        children = 0
        
        for v in self.graph.get(u, []):
            # Because this is an UNDIRECTED graph, U connects to V, and V connects 
            # to U. We must prevent the DFS from stupidly thinking the parent 
            # it just came from is a valid "back-edge"!
            if v == parent:
                continue
                
            # Case A: Unvisited Neighbor
            if self.discovery_time[v] == -1:
                children += 1
                self._dfs(v, u)
                
                # When recursion returns, U absorbs V's low-link if it's better
                self.low_link[u] = min(self.low_link[u], self.low_link[v])
                
                # --------------------------------------------------------------
                # VULNERABILITY DETECTION MATHEMATICS
                # --------------------------------------------------------------
                
                # 1. BRIDGE DETECTION
                # If V's lowest reachable point is strictly AFTER U's discovery 
                # time, it means V has absolutely no alternative paths leading 
                # back up the tree. The edge U-V is a critical bridge!
                if self.low_link[v] > self.discovery_time[u]:
                    self.bridges.append((u, v))
                    
                # 2. ARTICULATION POINT DETECTION
                # If V's lowest reachable point is >= U's discovery time, it means 
                # V is completely trapped BELOW U. If we delete U, V is severed 
                # from the rest of the world!
                # (Note: We ignore the Root node here, handled separately).
                if parent != -1 and self.low_link[v] >= self.discovery_time[u]:
                    self.articulation_points.add(u)
                    
            # Case B: Visited Neighbor (Valid Back-Edge found!)
            else:
                self.low_link[u] = min(self.low_link[u], self.discovery_time[v])
                
        # Handle the special Root Node edge case!
        if parent == -1 and children > 1:
            self.articulation_points.add(u)


    def scan_network(self):
        """Scans the entire graph, handling disconnected islands."""
        for i in range(self.V):
            if self.discovery_time[i] == -1:
                self._dfs(i, -1)


def demonstrate_vulnerabilities():
    section_header("Algorithm: Articulation Points & Bridges")
    
    vertices = 5
    # Undirected Graph
    # 0 - 1, 1 - 2, 2 - 0 (This is a triangle cycle. High redundancy!)
    # 0 - 3 (Wait, 3 is hanging off 0. The edge 0-3 is a Bridge!)
    # 3 - 4 (Wait, 4 is hanging off 3. The edge 3-4 is a Bridge!)
    graph = {
        0: [1, 2, 3],
        1: [0, 2],
        2: [0, 1],
        3: [0, 4],
        4: [3]
    }
    
    print("Executing Network Vulnerability Scanner (Single-Pass DFS)...")
    scanner = NetworkVulnerabilityScanner(vertices, graph)
    scanner.scan_network()
    
    print(f"\nCRITICAL BRIDGES (Single Point of Failure Wires):")
    for u, v in scanner.bridges:
        print(f" -> Severing Edge ({u} - {v}) will split the network!")
        
    print(f"\nARTICULATION POINTS (Single Point of Failure Data Centers):")
    for node in scanner.articulation_points:
        print(f" -> Node {node} going offline will split the network!")
        
    print("\nObservation:")
    print("Notice how Node 0 connects the robust triangle (0,1,2) to the fragile line (3,4).")
    print("Deleting Node 0 splits the network perfectly. Deleting Node 3 splits Node 4 off!")


# ==============================================================================
# 4. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. What is the difference between `>=` and `>` in the vulnerability triggers?
   Answer: 
   - Bridge: `low_link[v] > discovery_time[u]`. If V's low-link is STRICTLY greater, V has no way to reach U or anything above U. The wire U-V is a Bridge.
   - Articulation Point: `low_link[v] >= discovery_time[u]`. If V's low-link equals U's discovery time, it means V found a back-edge that points exactly to U, but NO HIGHER. Therefore, if you delete U, you sever V from the rest of the world! So U is an Articulation Point. But the wire U-V is NOT a bridge, because there are multiple ways for V to reach U.

2. Why must we explicitly ignore the `parent` node in Undirected Graphs?
   Answer: In an undirected graph, if I walk from Node 1 to Node 2, the adjacency list for Node 2 will contain Node 1. If the DFS looks at Node 1 and says "Ah! I've already visited Node 1! This is a back-edge!", it will incorrectly update Node 2's `low_link`. We must programmatically block the DFS from looking backward down the exact pipe it just traversed.

3. Why is the DFS Root Node treated specially for Articulation Points?
   Answer: The mathematical formula `low_link[v] >= discovery_time[u]` is mathematically guaranteed to trigger for the Root node, because NO node can possibly have a discovery time less than the Root! Therefore, the formula will falsely flag the Root as an AP every single time. Instead, the Root is ONLY an AP if it physically spawns $2$ or more completely disconnected children during the DFS tree expansion.
"""

if __name__ == "__main__":
    demonstrate_vulnerabilities()
    print("\n[SUCCESS] Laboratory: Articulation Points & Bridges Completed.")
