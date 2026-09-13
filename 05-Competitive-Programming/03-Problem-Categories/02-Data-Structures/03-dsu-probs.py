"""
# ==============================================================================
# LABORATORY: COMPETITIVE PROGRAMMING (DISJOINT SET UNION / DSU)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You are given a massive social network of 1,000,000 users. 
# You receive a stream of friend requests: "A is friends with B", "C is friends 
# with D", "B is friends with C".
#
# Suddenly, the system asks: "Is A in the same friend group as D?"
#
# If you try to run a Breadth-First Search (BFS) to answer this query, it will 
# take O(V + E) time. If you receive 100,000 queries, it takes 100 Billion 
# operations (Time Limit Exceeded).
#
# You must use the Disjoint Set Union (DSU) data structure, also known as Union-Find.
# DSU mathematically links groups together and answers "Are they connected?" 
# queries in O(α(N)) time. α (Inverse Ackermann function) is so unbelievably 
# small that for any number in the physical universe, it is <= 4.
# DSU operates in practically O(1) constant time!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the architecture of DSU (Parent Array & Size Array).
# - Master Path Compression (The speed cheat code).
# - Master Union by Size (The balancing act).
#
# ==============================================================================
"""

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. DISJOINT SET UNION (UNION-FIND) ARCHITECTURE
# ==============================================================================
class DSU:
    """
    A flawless Disjoint Set Union implementation using Path Compression 
    and Union by Size.
    
    Time Complexity:
    - find(): O(α(N)) ~ O(1)
    - union(): O(α(N)) ~ O(1)
    Space Complexity: O(N)
    """
    def __init__(self, size: int):
        # 1. PARENT ARRAY
        # Initially, every node is its own boss (it points to itself).
        self.parent = [i for i in range(size)]
        
        # 2. SIZE ARRAY
        # Tracks the physical size (number of nodes) in each set.
        # Initially, every set has a size of 1.
        self.size = [1] * size

    def find(self, x: int) -> int:
        """
        Finds the Ultimate Boss (Root Representative) of node x.
        Applies Path Compression to flatten the tree structure!
        """
        if self.parent[x] == x:
            return x
            
        # PATH COMPRESSION MAGIC
        # Instead of just returning the recursive result, we explicitly overwrite 
        # the current node's parent pointer to point directly to the Ultimate Boss!
        # This flattens a massive, deep tree into a flat Pancake in O(1) amortized time!
        self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: int, y: int) -> bool:
        """
        Merges the sets containing x and y.
        Returns True if a successful merge occurred.
        Returns False if they were ALREADY in the same set (a Cycle detected!).
        """
        root_x = self.find(x)
        root_y = self.find(y)
        
        if root_x == root_y:
            # They already have the same boss. They are already connected!
            return False
            
        # UNION BY SIZE MAGIC
        # We ALWAYS want to attach the smaller tree under the root of the larger tree.
        # This guarantees the tree remains completely balanced and shallow!
        if self.size[root_x] < self.size[root_y]:
            # Tree Y is bigger. Attach X under Y.
            self.parent[root_x] = root_y
            self.size[root_y] += self.size[root_x]
        else:
            # Tree X is bigger (or equal). Attach Y under X.
            self.parent[root_y] = root_x
            self.size[root_x] += self.size[root_y]
            
        return True
        
    def connected(self, x: int, y: int) -> bool:
        """Checks if x and y are in the same set."""
        return self.find(x) == self.find(y)


# ==============================================================================
# 4. EXECUTING DSU (CONNECTED COMPONENTS)
# ==============================================================================
def demonstrate_dsu():
    section_header("Executing DSU on a Social Network")
    
    # 0: Alice, 1: Bob, 2: Charlie, 3: Dave, 4: Eve
    dsu = DSU(5)
    
    print("Initial State: Everyone is isolated.")
    print(f"Are Alice (0) and Bob (1) connected? {dsu.connected(0, 1)}")
    
    print("\nEvent 1: Alice (0) befriends Bob (1).")
    dsu.union(0, 1)
    
    print("Event 2: Charlie (2) befriends Dave (3).")
    dsu.union(2, 3)
    
    print("Event 3: Bob (1) befriends Charlie (2).")
    # This magically bridges the two isolated friend groups!
    dsu.union(1, 2)
    
    print("\nState Check:")
    print("Because Bob connected with Charlie, Alice and Dave should now be connected!")
    print(f"Are Alice (0) and Dave (3) connected? {dsu.connected(0, 3)} (Time: O(1))")
    
    print("\nEvent 4: Dave (3) tries to befriend Alice (0).")
    result = dsu.union(3, 0)
    print(f"Did a new merge happen? {result}")
    print("Because it returned False, DSU instantly detected a Redundant Edge (a Cycle)!")


def run_all_labs():
    demonstrate_dsu()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. What does the "Path Compression" line `self.parent[x] = self.find(self.parent[x])` actually do physically to the data structure?
   Answer: Without path compression, a DSU tree can degrade into a long linked-list (e.g., $A \rightarrow B \rightarrow C \rightarrow D$). Calling `find(A)` would require stepping through all 4 nodes, taking $O(N)$ time. Path compression triggers during the recursive backtracking. After the recursion finally reaches the ultimate root ($D$), it returns $D$ back down the call stack. The `self.parent[x] = root` assignment physically snips the pointers of $C$, $B$, and $A$, and wires them all directly to $D$. The tree instantly flattens into a pancake (Height = 1). All future queries for $A, B$, or $C$ will now execute in $O(1)$ time!

2. Why do we need "Union by Size" (or Union by Rank)? Isn't Path Compression enough?
   Answer: Path compression only flattens the tree *after* a `find()` query is executed. If a malicious test case provides 100,000 `union()` operations in a row that form a straight line, and never calls `find()`, path compression never triggers! The tree height grows to 100,000, and a final `find()` query will crash Python with a `RecursionError: maximum recursion depth exceeded`. "Union by Size" prevents this by always attaching the smaller tree under the larger tree. This mathematical rule mathematically guarantees that the tree depth can *never* exceed $O(\log N)$, completely protecting against Stack Overflow crashes even before path compression runs!

3. When would you use DSU instead of BFS/DFS?
   Answer: 
   1. Dynamic Graph Connectivity: If edges are being continuously *added* to the graph (an online algorithm) and you need to answer connectivity queries interleavingly. BFS would require $O(V+E)$ re-calculation every time an edge is added, whereas DSU handles dynamic merges instantly.
   2. Cycle Detection in Undirected Graphs: DSU is vastly shorter to code and less error-prone than maintaining visited sets and parent pointers in DFS.
   3. Kruskal's Minimum Spanning Tree (MST): DSU is the mandatory foundational data structure required to execute Kruskal's algorithm, tracking which nodes are already merged into the MST to prevent cycles.
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Disjoint Set Union (DSU) Completed.")
