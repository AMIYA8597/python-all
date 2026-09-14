"""
# ==============================================================================
# LABORATORY: INTERVIEW PREPARATION (PROBLEM SETS - DATA STRUCTURES HARD)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# "Hard" Data Structure problems require architecting complex systems from scratch. 
# You must combine Heaps with Linked Lists (Merge K Sorted Lists), or invent 
# custom String serialization protocols for complex memory pointers (Serialize Tree), 
# or build fully functional File Systems using hierarchical Trie logic.
#
# A junior engineer serializes a Binary Tree by just storing the values in an 
# array. When deserializing, they have absolutely no way to know which values 
# belonged to the left branch versus the right branch, failing the reconstruct.
#
# A senior engineer uses a Pre-Order Traversal Protocol. They mathematically 
# inject specific "NULL" markers into the string payload. During deserialization, 
# a simple Iterator effortlessly consumes the string, instantly rebuilding the 
# exact physical pointer topology of the original tree!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master Multi-List Priority Queue Routing (Merge k Sorted Lists).
# - Master String Serialization Protocols (Serialize/Deserialize Tree).
# - Master Hierarchical System Design.
#
# ==============================================================================
"""

import heapq
from typing import Optional, List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. MERGE K SORTED LISTS (PRIORITY QUEUE ROUTING)
# ==============================================================================
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
        
    # We must explicitly define __lt__ because the Heapq module will attempt to 
    # compare identical values by falling back to comparing the objects themselves!
    def __lt__(self, other):
        return self.val < other.val

def mergeKLists(lists: List[Optional[ListNode]]) -> Optional[ListNode]:
    """
    Time: O(N log K) | Space: O(K) 
    where N is the total number of nodes, and K is the number of linked lists.
    
    A junior engineer extracts all values, sorts them (O(N log N)), and builds a list.
    A senior engineer pushes the Head of every list into a Min-Heap. The heap 
    will instantly bubble the absolute smallest node to the top. When popped, 
    we inject that node's `next` pointer back into the heap!
    """
    # The Dummy Node anchor!
    dummy = ListNode(-1)
    curr = dummy
    
    # The Min-Heap (Priority Queue)
    min_heap = []
    
    # 1. INITIALIZATION: Push the Head of every single list into the Heap!
    for i in range(len(lists)):
        if lists[i]:
            # Push a Tuple: (Value, Index, Node)
            # Index is included to break ties if two nodes have the exact same Value!
            heapq.heappush(min_heap, (lists[i].val, i, lists[i]))
            
    print(f"  Heap initialized with {len(min_heap)} starting nodes.")
    
    # 2. THE ROUTING ENGINE
    while min_heap:
        # Pop the absolute smallest node currently available!
        val, i, node = heapq.heappop(min_heap)
        
        # Suture it into our merged list!
        curr.next = node
        curr = curr.next
        
        # If the node we just popped has a child, push it into the heap to 
        # replace its parent!
        if node.next:
            heapq.heappush(min_heap, (node.next.val, i, node.next))
            
    return dummy.next

def demonstrate_merge_k():
    section_header("Hard: Merge k Sorted Lists (O(N log K) Priority Queue)")
    
    # List 1: 1 -> 4 -> 5
    l1 = ListNode(1, ListNode(4, ListNode(5)))
    # List 2: 1 -> 3 -> 4
    l2 = ListNode(1, ListNode(3, ListNode(4)))
    # List 3: 2 -> 6
    l3 = ListNode(2, ListNode(6))
    
    merged_head = mergeKLists([l1, l2, l3])
    
    vals = []
    curr = merged_head
    while curr:
        vals.append(str(curr.val))
        curr = curr.next
        
    print(f"\nResult: {' -> '.join(vals)}")


# ==============================================================================
# 4. SERIALIZE AND DESERIALIZE BINARY TREE (PRE-ORDER PROTOCOL)
# ==============================================================================
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

class Codec:
    """
    Time: O(N) | Space: O(N)
    Serialization is the process of converting a data structure or object into a 
    sequence of bits (a String) so that it can be transmitted across a network!
    """

    def serialize(self, root: TreeNode) -> str:
        """Encodes a tree to a single string."""
        res = []
        
        def dfs(node):
            if not node:
                # We mathematically MUST encode the physical absence of a node 
                # (NULL pointers) to preserve the structural topology!
                res.append("N")
                return
            
            # PRE-ORDER TRAVERSAL (Root, Left, Right)
            res.append(str(node.val))
            dfs(node.left)
            dfs(node.right)
            
        dfs(root)
        # Join with commas for easy parsing!
        encoded = ",".join(res)
        print(f"  [SERIALIZE] Payload Generated: {encoded}")
        return encoded

    def deserialize(self, data: str) -> TreeNode:
        """Decodes your encoded data to tree."""
        # Split the string back into an array of values!
        vals = data.split(",")
        # We use a global pointer to track our consumption of the array.
        self.i = 0
        
        def dfs():
            # Base Case: Are we out of bounds? (Should never happen if payload is valid)
            if self.i >= len(vals):
                return None
                
            # If the current token is our 'NULL' marker...
            if vals[self.i] == "N":
                self.i += 1
                return None
                
            # Create the physical Node in RAM!
            node = TreeNode(int(vals[self.i]))
            self.i += 1
            
            # Recursively build the left branch, then the right branch!
            # Because we used Pre-Order to encode, the data is flawlessly aligned 
            # to be consumed via Pre-Order decoding!
            node.left = dfs()
            node.right = dfs()
            
            return node
            
        decoded_root = dfs()
        print("  [DESERIALIZE] Physical Tree perfectly reconstructed in RAM.")
        return decoded_root

def demonstrate_codec():
    section_header("Hard: Serialize and Deserialize Binary Tree")
    
    #      1
    #     / \
    #    2   3
    #       / \
    #      4   5
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.right.left = TreeNode(4)
    root.right.right = TreeNode(5)
    
    codec = Codec()
    payload = codec.serialize(root)
    
    rebuilt_tree = codec.deserialize(payload)
    print(f"\nVerification: Rebuilt Root Value = {rebuilt_tree.val} (Expected: 1)")
    print(f"Verification: Rebuilt Right-Left Value = {rebuilt_tree.right.left.val} (Expected: 4)")


def run_all_labs():
    demonstrate_merge_k()
    demonstrate_codec()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "In 'Merge k Sorted Lists', why do we insert the Tuple `(node.val, index, node)` into the Heap instead of just `(node.val, node)`?"
   Senior Answer: "The Python `heapq` module requires a way to resolve collisions. If you push `(5, node_A)` and `(5, node_B)` into the heap, the engine first compares the integers ($5 == 5$). Because they are identical, it attempts to compare the second elements of the tuple: `node_A < node_B`. Unless you explicitly override the `__lt__` dunder method on the `ListNode` class, Python has absolutely no idea how to mathematically compare two custom Object instances, and it will instantly throw a fatal `TypeError`. By injecting the `index` as a middle element (`5, 2, node_A`), the heap compares the integers, sees a tie, and then falls back to comparing the completely unique List Indices ($2 < 4$), flawlessly resolving the collision without ever attempting to compare the Object memory addresses."

2. Interviewer: "For Tree Serialization, why is PRE-ORDER traversal (Root, Left, Right) mathematically superior to IN-ORDER traversal (Left, Root, Right)?"
   Senior Answer: "Deserialization requires us to reconstruct the tree from the top down. We cannot attach a Left Child to a Parent if the Parent doesn't physically exist in RAM yet! Pre-Order traversal places the Root node at the absolute beginning of the string payload. When we consume the string, we instantly construct the Parent, and then recursively pass its memory pointer down the call stack so the Left and Right children can attach themselves to it. In-Order traversal places the Root somewhere in the middle of the payload, making it structurally impossible to know where to begin reconstruction without executing a chaotic $O(N)$ scanning loop to find the root."

3. Interviewer: "In the Tree Deserializer, you used a class-level variable `self.i` to track the array index. Could you just pass the index as an argument to the recursive `dfs(i)` function?"
   Senior Answer: "No. If you pass `i` as an immutable integer argument, it is passed strictly by value. When `dfs(node.left)` executes and consumes 5 tokens, it returns. The `dfs(node.right)` function will execute using the *exact same* original `i` value that `node.left` started with, completely destroying the chronological token consumption! You MUST use a mutable reference (like a global class variable `self.i`, or passing an array `[0]`) so that the state mutations made deep within the Left branch are permanently preserved and physically visible to the Right branch when it begins its execution."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Problem Sets (Data Structures Hard) Completed.")
