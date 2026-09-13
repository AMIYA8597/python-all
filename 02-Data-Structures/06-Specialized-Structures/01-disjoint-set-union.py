"""
# ==============================================================================
# LABORATORY: DISJOINT SET UNION (UNION-FIND MASTERCLASS)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You've seen Union-Find (DSU) used in Kruskal's MST and Graph Cycle Detection.
# It is one of the most elegant and powerful data structures in computer science.
# 
# Why? Because of its Time Complexity.
# If you use Path Compression AND Union by Rank, the time complexity of finding 
# or merging elements drops to `O(α(N))`, where `α` is the Inverse Ackermann Function.
# The Inverse Ackermann function grows so incredibly slowly that for all practical 
# values of N (even N = number of atoms in the universe), `α(N)` is <= 4.
# This means DSU operates in STRICT AMORTIZED O(1) TIME.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand Path Compression (Find).
# - Understand the difference between Union by Rank and Union by Size.
# - Solve "Number of Connected Components" (Social Network).
#
# ==============================================================================
"""

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. DSU WITH UNION BY SIZE
# ==============================================================================
class DisjointSetUnion:
    """
    A production-grade DSU implementation using Path Compression and Union by Size.
    Union by Size is often preferred over Union by Rank because it allows you to 
    instantly answer: "How many nodes are in this specific connected component?"
    """
    def __init__(self, n: int):
        # Every node is initially its own parent
        self.parent = [i for i in range(n)]
        
        # Every node initially represents a component of size 1
        self.size = [1] * n
        
        # Total number of isolated components. Starts at N.
        self.components = n

    def find(self, x: int) -> int:
        """
        O(α(N)) Path Compression.
        Flattens the tree so that every node points DIRECTLY to the absolute root.
        """
        if self.parent[x] == x:
            return x
            
        # RECURSIVE PATH COMPRESSION:
        # 1. Recursively find the absolute root.
        # 2. Re-assign `self.parent[x]` to that absolute root on the way back up!
        self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: int, y: int) -> bool:
        """
        O(α(N)) Union by Size.
        Attaches the smaller tree UNDER the larger tree to keep the structure flat.
        Returns True if a merge happened, False if they were already connected.
        """
        root_x = self.find(x)
        root_y = self.find(y)
        
        if root_x == root_y:
            return False # Already in the same set!
            
        # UNION BY SIZE LOGIC:
        if self.size[root_x] < self.size[root_y]:
            # X's tree is smaller. Attach X under Y.
            self.parent[root_x] = root_y
            self.size[root_y] += self.size[root_x] # Y's size grows
        else:
            # Y's tree is smaller (or equal). Attach Y under X.
            self.parent[root_y] = root_x
            self.size[root_x] += self.size[root_y] # X's size grows
            
        # We successfully merged two components into one!
        self.components -= 1
        return True
        
    def get_component_size(self, x: int) -> int:
        """Returns the total number of nodes in X's connected component."""
        root = self.find(x)
        return self.size[root]


# ==============================================================================
# 4. APPLICATION: SOCIAL NETWORK CONNECTIVITY
# ==============================================================================
def demonstrate_social_network():
    section_header("Application: Social Network Connectivity")
    
    print("Scenario: A new social network launches with 6 users (0 to 5).")
    print("We want to track friend groups and instantly know when everyone")
    print("is fully connected in one giant group.\n")
    
    dsu = DisjointSetUnion(6)
    
    # List of friendships forming over time (timestamp, user_A, user_B)
    events = [
        ("Monday", 0, 1),
        ("Tuesday", 1, 2),
        ("Wednesday", 3, 4),
        ("Thursday", 0, 2), # Redundant, already connected!
        ("Friday", 4, 5),
        ("Saturday", 2, 3)  # This bridge connects the two separate groups!
    ]
    
    for time, u, v in events:
        merged = dsu.union(u, v)
        if merged:
            print(f"[{time}] Users {u} and {v} became friends! (New connection)")
        else:
            print(f"[{time}] Users {u} and {v} became friends! (But they were already in the same group)")
            
        print(f"  -> Total distinct friend groups remaining: {dsu.components}")
        
        # Check if everyone is connected!
        if dsu.components == 1:
            print(f"\n[ALERT] On {time}, all users are now fully connected into a single network!")
            break


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. What is the Inverse Ackermann Function `α(N)`?
   Answer: The Ackermann function `A(x)` grows incomprehensibly fast (faster than exponentials). The Inverse Ackermann `α(N)` is its inverse, meaning it grows incomprehensibly SLOWLY. For N = 10^80 (atoms in the universe), `α(N)` is less than 5. Thus, `O(α(N))` is effectively `O(1)` for all practical software engineering.

2. Why do we need Union by Size (or Rank)? Why not just `parent[root_x] = root_y`?
   Answer: If we arbitrarily attach X to Y every time, the tree might degrade into a straight line (a Linked List). Calling `find()` on the bottom node would take `O(N)` time! By strictly attaching the smaller tree under the larger tree, we guarantee the height of the tree never exceeds `log(N)`, keeping the structure perfectly flat.

3. Can you "un-union" or delete edges from a standard Disjoint Set?
   Answer: NO. DSU is an "incremental" or "additive" data structure. Path compression permanently flattens the tree. If you delete an edge, it is mathematically impossible to know how to reconstruct the sub-trees accurately. (Dynamic Connectivity algorithms that support edge deletion exist, but they are extremely complex, often using Link-Cut Trees).
"""

if __name__ == "__main__":
    demonstrate_social_network()
    print("\n[SUCCESS] Laboratory: Disjoint Set Union Completed.")
