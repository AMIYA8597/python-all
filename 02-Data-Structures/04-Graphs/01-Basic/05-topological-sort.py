"""
# ==============================================================================
# LABORATORY: ADVANCED TOPOLOGICAL SORT APPLICATIONS
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You already know how to perform a Topological Sort using DFS (Post-Order) or 
# BFS (Kahn's Algorithm with In-Degrees). 
# However, standard Topological Sort only gives you ONE valid execution order. 
# What if a scheduler needs to evaluate ALL possible valid execution orders to 
# find the one that minimizes context switching? 
# Furthermore, Topological Sort is the secret behind the infamous "Alien Dictionary" 
# problem (LeetCode #269), arguably the most frequently asked FAANG hard question.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand that a DAG can have MULTIPLE valid Topological Sorts.
# - Generate ALL valid Topological Sorts using Backtracking.
# - Master the "Alien Dictionary" problem by extracting edges from sorted strings.
#
# ==============================================================================
"""

from collections import defaultdict, deque
from typing import List, Dict

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. GENERATING ALL VALID TOPOLOGICAL SORTS
# ==============================================================================
def all_topological_sorts(num_nodes: int, edges: List[List[int]]) -> List[List[int]]:
    """
    If Node A requires nothing, and Node B requires nothing, the valid execution 
    orders are [A, B] and [B, A].
    We use Kahn's Algorithm + Backtracking to find ALL valid combinations.
    """
    adj = defaultdict(list)
    in_degree = [0] * num_nodes
    
    for src, dst in edges:
        adj[src].append(dst)
        in_degree[dst] += 1
        
    all_results = []
    current_path = []
    visited = [False] * num_nodes
    
    def backtrack():
        # Base case: if we have added all nodes, we found a valid sort!
        if len(current_path) == num_nodes:
            all_results.append(list(current_path))
            return
            
        # Try picking ANY node that currently has an in-degree of 0
        for i in range(num_nodes):
            if in_degree[i] == 0 and not visited[i]:
                # 1. Choose this node
                visited[i] = True
                current_path.append(i)
                # Temporarily remove its edges (decrement neighbor in-degrees)
                for neighbor in adj[i]:
                    in_degree[neighbor] -= 1
                    
                # 2. Recurse to find the rest of the path
                backtrack()
                
                # 3. Undo (Backtrack) to try the next possible combination
                for neighbor in adj[i]:
                    in_degree[neighbor] += 1
                current_path.pop()
                visited[i] = False

    backtrack()
    return all_results

def demonstrate_all_sorts():
    section_header("Algorithm: All Possible Topological Sorts")
    
    # Graph:
    # 0 -> 2
    # 1 -> 2
    # Both 0 and 1 have NO prerequisites. 2 requires BOTH.
    edges = [[0, 2], [1, 2]]
    
    print("Graph Dependencies:")
    print(" Node 0 -> Node 2")
    print(" Node 1 -> Node 2")
    
    results = all_topological_sorts(3, edges)
    
    print(f"\nFound {len(results)} valid execution orders:")
    for order in results:
        print(f"  {order}")
    print("Notice how 0 and 1 can be executed in any order, but 2 MUST be last.")


# ==============================================================================
# 4. ALIEN DICTIONARY (LEETCODE HARD)
# ==============================================================================
def alien_dictionary(words: List[str]) -> str:
    """
    LeetCode #269: Alien Dictionary
    You are given a list of words sorted in "Alien Alphabetical Order".
    Determine the correct alphabetical order of the alien letters.
    
    Example Words: ["wrt", "wrf", "er", "ett", "rftt"]
    
    Algorithm:
    1. Extract Graph Edges: Compare adjacent words. The FIRST character that differs 
       tells you the exact alphabetical order. (e.g., "wrt" before "wrf" means 't' 
       comes before 'f'. Edge: t -> f).
    2. Run Topological Sort on this generated graph.
    """
    # 1. Initialize Adjacency List and In-Degrees for EVERY unique character
    adj = {char: set() for word in words for char in word}
    in_degree = {char: 0 for word in words for char in word}
    
    # 2. Extract Edges by comparing adjacent words
    for i in range(len(words) - 1):
        word1 = words[i]
        word2 = words[i + 1]
        
        # Edge Case: If word1 is longer than word2 but matches completely ("abc" vs "ab"), 
        # it is invalid dictionary sorting.
        if len(word1) > len(word2) and word1[:len(word2)] == word2:
            return ""
            
        # Find the first character that differs
        for c1, c2 in zip(word1, word2):
            if c1 != c2:
                # We found a rule! c1 comes before c2.
                if c2 not in adj[c1]:
                    adj[c1].add(c2)
                    in_degree[c2] += 1
                break # We ONLY care about the first differing character!
                
    # 3. Topological Sort (Kahn's BFS)
    queue = deque([char for char in in_degree if in_degree[char] == 0])
    result = []
    
    while queue:
        char = queue.popleft()
        result.append(char)
        
        for neighbor in adj[char]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
                
    # 4. Validation: If result doesn't contain all characters, a cycle exists
    if len(result) != len(in_degree):
        return ""
        
    return "".join(result)

def demonstrate_alien_dictionary():
    section_header("Algorithm: Alien Dictionary (Extracting Edges)")
    
    words = ["wrt", "wrf", "er", "ett", "rftt"]
    
    print(f"Given words sorted in alien order: {words}")
    
    # "wrt" vs "wrf" -> 't' comes before 'f'
    # "wrf" vs "er"  -> 'w' comes before 'e'
    # "er"  vs "ett" -> 'r' comes before 't'
    # "ett" vs "rftt"-> 'e' comes before 'r'
    #
    # Graph: w -> e -> r -> t -> f
    
    order = alien_dictionary(words)
    print(f"Derived Alien Alphabetical Order: '{order}'")


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. When finding ALL Topological Sorts, why do we use Backtracking?
   Answer: Because at any given step, there might be multiple nodes with an In-Degree of 0 (ready to execute). Standard Kahn's algorithm just picks the first one it sees. Backtracking forces the algorithm to explore the timeline where it picks node A first, then UNDOES that choice, and explores the timeline where it picks node B first.

2. In the Alien Dictionary problem, why do we `break` immediately after finding the first differing character between two adjacent words?
   Answer: In standard alphabetical sorting, words are sorted strictly by the FIRST character that differs. For example, in English, "apple" comes before "apply" purely because 'e' comes before 'y'. The fact that the next letters might be different is completely irrelevant.

3. What does it mean if the Alien Dictionary returns an empty string (Cycle detected)?
   Answer: It means the input list is contradictory. For example, if the input dictates that 'a' comes before 'b', but a later word dictates that 'b' comes before 'a', the alphabetical rules are impossible to satisfy.
"""

if __name__ == "__main__":
    demonstrate_all_sorts()
    demonstrate_alien_dictionary()
    print("\n[SUCCESS] Laboratory: Advanced Topological Sort Completed.")
