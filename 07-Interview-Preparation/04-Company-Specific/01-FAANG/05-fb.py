"""
# ==============================================================================
# LABORATORY: INTERVIEW PREPARATION (FAANG - META / FACEBOOK)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Meta (Facebook) interviews heavily emphasize clean, highly readable, production-
# ready code under tight time constraints (often 2 distinct problems in 45 mins). 
# They frequently test Deep Copying of Graphs, extreme Array manipulations, and 
# custom Iterators.
#
# A junior engineer trying to deep copy a Graph with cycles will get trapped in 
# an infinite recursive loop, instantly failing the interview.
# 
# A senior engineer understands Graph State Management. They deploy a Hash Map 
# mapping `OriginalNode -> ClonedNode` to mathematically guarantee that any 
# node in a cycle is cloned exactly once, instantly breaking the infinite loop.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master Deep Copying of cyclic Graphs (Clone Graph).
# - Master the execution of Custom Iterators (Flatten Nested List Iterator).
# - Master production-grade code readability and edge-case handling.
#
# ==============================================================================
"""

import collections
from typing import List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. CLONE GRAPH (DEEP COPY WITH CYCLES)
# ==============================================================================
class Node:
    def __init__(self, val=0, neighbors=None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []

def clone_graph(node: 'Node') -> 'Node':
    """
    Time: O(V + E) | Space: O(V)
    Returns a mathematically perfect Deep Copy of the entire Graph.
    Because Graphs can contain CYCLES, we MUST use a Hash Map to track which 
    nodes have already been cloned to prevent infinite recursion!
    """
    if not node:
        return None
        
    # The absolute most critical component!
    # Map: Original Node Memory Address -> Cloned Node Memory Address
    cloned_map = {}
    
    def dfs(original_node: 'Node') -> 'Node':
        # 1. CYCLE PREVENTION: Have we ALREADY cloned this specific node?
        if original_node in cloned_map:
            # Return the ALREADY CLONED instance of it!
            return cloned_map[original_node]
            
        # 2. Create the brand new Cloned Node
        clone = Node(original_node.val)
        
        # 3. IMMEDIATELY add it to the map BEFORE traversing its neighbors!
        # If we wait until after the traversal, the cycle prevention mechanism 
        # won't exist yet, and we will crash!
        cloned_map[original_node] = clone
        
        # 4. Recursively clone all neighbors
        for neighbor in original_node.neighbors:
            clone.neighbors.append(dfs(neighbor))
            
        return clone
        
    return dfs(node)

def demonstrate_clone_graph():
    section_header("Meta: Clone Graph (Deep Copy with Cycles)")
    
    print("Building a Cyclic Graph: Node 1 <-> Node 2")
    node1 = Node(1)
    node2 = Node(2)
    node1.neighbors.append(node2)
    node2.neighbors.append(node1) # The Fatal Cycle!
    
    print("Cloning Graph...")
    cloned_node1 = clone_graph(node1)
    
    print("\nVerification:")
    print(f"Original Node 1 Address: {hex(id(node1))}")
    print(f"Cloned   Node 1 Address: {hex(id(cloned_node1))}")
    print(f"Are they different physical objects? {node1 is not cloned_node1}")
    print(f"Does the cloned node properly point to a cloned neighbor? {len(cloned_node1.neighbors) == 1}")


# ==============================================================================
# 4. FLATTEN NESTED LIST ITERATOR (CUSTOM ITERATORS)
# ==============================================================================
class NestedInteger:
    """A mock interface given in the actual Meta interview."""
    def __init__(self, is_integer: bool, value=None, list_val=None):
        self._is_integer = is_integer
        self._value = value
        self._list = list_val if list_val else []
        
    def isInteger(self) -> bool:
        return self._is_integer
        
    def getInteger(self) -> int:
        return self._value
        
    def getList(self) -> List['NestedInteger']:
        return self._list

class NestedIterator:
    """
    Given a nested list of integers (e.g., [[1,1],2,[1,1]]), implement an iterator 
    to flatten it.
    
    A junior engineer recursively flattens the ENTIRE list in the `__init__` method.
    This fails because if the list contains 10 Billion items, the constructor 
    will take 5 hours and crash the RAM!
    
    A senior engineer uses a Stack to evaluate the list LAZILY, extracting exactly 
    one integer at a time, exactly when it is requested!
    """
    def __init__(self, nestedList: List[NestedInteger]):
        # We push the absolute highest-level list onto the stack backwards!
        # Why backwards? So that when we pop(), we get the FIRST element!
        self.stack = list(reversed(nestedList))
        
    def next(self) -> int:
        # According to the Iterator spec, `hasNext()` is always called before `next()`.
        # Therefore, we mathematically guarantee the top of the stack is a raw Integer!
        return self.stack.pop().getInteger()
        
    def hasNext(self) -> bool:
        # We must unpack the stack until we find a raw Integer!
        while self.stack:
            top = self.stack[-1]
            
            if top.isInteger():
                return True
                
            # It's a list! We must physically pop the list off the stack, 
            # crack it open, and push its internal contents back onto the stack 
            # in reverse order!
            nested_list = self.stack.pop().getList()
            for i in reversed(nested_list):
                self.stack.append(i)
                
        return False

def demonstrate_nested_iterator():
    section_header("Meta: Flatten Nested List Iterator (Lazy Evaluation)")
    
    # Simulating: [[1, 2], 3, [4, [5]]]
    nested = [
        NestedInteger(False, list_val=[NestedInteger(True, value=1), NestedInteger(True, value=2)]),
        NestedInteger(True, value=3),
        NestedInteger(False, list_val=[
            NestedInteger(True, value=4),
            NestedInteger(False, list_val=[NestedInteger(True, value=5)])
        ])
    ]
    
    print("Flattening: [[1, 2], 3, [4, [5]]] lazily...")
    
    iterator = NestedIterator(nested)
    result = []
    
    while iterator.hasNext():
        result.append(iterator.next())
        
    print(f"\nResult: {result} (Expected: [1, 2, 3, 4, 5])")


def run_all_labs():
    demonstrate_clone_graph()
    demonstrate_nested_iterator()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "In the Clone Graph problem, why must we insert the newly cloned Node into the `cloned_map` BEFORE we execute the recursive `dfs` on its neighbors?"
   Senior Answer: "If the Graph contains a Cycle (e.g., A points to B, and B points to A), and we wait until *after* the `dfs` completes to update the Hash Map, node A will call `dfs(B)`. Node B will see that A is not in the Hash Map yet, so B will call `dfs(A)`. A will call `dfs(B)`. This triggers an infinite recursive paradox, violently crashing the server with a `RecursionError`. By inserting node A into the map the absolute millisecond it is instantiated in RAM, when B recursively looks back at A, it instantly detects the cached object, terminates the recursion, and flawlessly seals the cycle."

2. Interviewer: "In the Flatten Nested List Iterator, why is it structurally incorrect to just recursively flatten the entire input array into a 1D Python list inside the `__init__` constructor?"
   Senior Answer: "An Iterator is fundamentally designed for Lazy Evaluation. The consumer of the Iterator might only want to read the first 3 elements of a massive 10-Terabyte nested stream. If you recursively flatten the entire structure inside `__init__`, you force the CPU to perform 10 Terabytes of processing and allocate 10 Terabytes of physical RAM before returning control to the user! By using a Stack, we completely defer the computational cost. We mathematically crack open exactly enough lists to extract exactly one integer at a time, achieving $O(1)$ amortized memory usage and instantaneous startup time."

3. Interviewer: "Why do we push the lists onto the Stack in `reversed` order?"
   Senior Answer: "A Stack is a Last-In, First-Out (LIFO) data structure. If we have the array `[1, 2, 3]` and we push it sequentially onto the stack, the top of the stack will be `3`. When the user calls `next()`, they expect to receive `1`, but they will incorrectly receive `3`. By pushing the elements in strictly reversed order (`3`, then `2`, then `1`), the element `1` is physically placed at the absolute top of the Stack, mathematically guaranteeing that a $O(1)$ `.pop()` operation retrieves the chronologically correct item."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: FAANG Prep (Meta) Completed.")
