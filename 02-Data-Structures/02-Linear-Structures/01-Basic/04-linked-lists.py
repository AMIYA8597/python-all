"""
# ==============================================================================
# LABORATORY: LINKED LISTS
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Linked Lists are the foundation of dynamic memory allocation. While Python 
# abstracts this away with its dynamic `list`, understanding Linked Lists is 
# absolutely mandatory for technical interviews (FAANG) and for understanding 
# how complex structures (like Trees and Graphs) are physically connected in RAM.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Build a Node class and a Singly Linked List class.
# - Master O(N) traversal and O(1) insertion (when pointer is known).
# - Solve a classic FAANG interview problem: Reverse a Linked List.
# - Solve a classic FAANG interview problem: Detect a Cycle (Floyd's Algorithm).
#
# ==============================================================================
"""

from typing import Any, Optional

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. NODE AND LINKED LIST IMPLEMENTATION
# ==============================================================================
class Node:
    """The fundamental building block. It holds data and a reference to the next Node."""
    def __init__(self, data: Any):
        self.data = data
        self.next: Optional['Node'] = None

class LinkedList:
    def __init__(self):
        self.head: Optional[Node] = None
        
    def append(self, data: Any):
        """Adds a node to the end of the list. O(N) time because we must traverse."""
        new_node = Node(data)
        
        # If the list is empty, the new node becomes the head
        if not self.head:
            self.head = new_node
            return
            
        # Otherwise, traverse to the very end
        curr = self.head
        while curr.next:
            curr = curr.next
            
        # Attach the new node to the last node's `next` pointer
        curr.next = new_node
        
    def insert_at_beginning(self, data: Any):
        """Adds a node to the front. O(1) time."""
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node
        
    def display(self):
        """Traverses the list and prints it."""
        elements = []
        curr = self.head
        while curr:
            elements.append(str(curr.data))
            curr = curr.next
        print(" -> ".join(elements) + " -> None")

def demonstrate_linked_list():
    section_header("Singly Linked List Implementation")
    
    ll = LinkedList()
    ll.append(10)
    ll.append(20)
    ll.append(30)
    
    print("Initial List:")
    ll.display()
    
    print("\nInserting 5 at the beginning (O(1)):")
    ll.insert_at_beginning(5)
    ll.display()


# ==============================================================================
# 4. CLASSIC INTERVIEW PROBLEM: REVERSE A LINKED LIST
# ==============================================================================
def reverse_linked_list(head: Optional[Node]) -> Optional[Node]:
    """
    LeetCode #206: Reverse Linked List
    Time Complexity: O(N)
    Space Complexity: O(1) (In-place pointer manipulation)
    
    The Trick: We need 3 pointers (prev, curr, next_node) because when we change 
    curr.next to point backwards, we lose the reference to the rest of the list!
    """
    prev = None
    curr = head
    
    while curr:
        # 1. Save the rest of the list
        next_node = curr.next
        
        # 2. Reverse the pointer of the current node
        curr.next = prev
        
        # 3. Move the 'prev' and 'curr' pointers one step forward
        prev = curr
        curr = next_node
        
    # At the end, 'curr' is None, and 'prev' is the new head of the reversed list
    return prev

def demonstrate_reverse():
    section_header("Algorithm: Reverse a Linked List")
    
    ll = LinkedList()
    for i in range(1, 6):
        ll.append(i)
        
    print("Original List:")
    ll.display()
    
    print("\nReversing in O(N) time and O(1) space...")
    ll.head = reverse_linked_list(ll.head)
    
    print("Reversed List:")
    ll.display()


# ==============================================================================
# 5. CLASSIC INTERVIEW PROBLEM: DETECT A CYCLE
# ==============================================================================
def has_cycle(head: Optional[Node]) -> bool:
    """
    LeetCode #141: Linked List Cycle
    Time Complexity: O(N)
    Space Complexity: O(1)
    
    Floyd's Tortoise and Hare Algorithm:
    We use two pointers. One moves 1 step at a time (slow), the other moves 2 
    steps at a time (fast). If there is a cycle (an infinite loop in the list), 
    the fast pointer will eventually "lap" the slow pointer and they will equal 
    each other.
    """
    if not head or not head.next:
        return False
        
    slow = head
    fast = head
    
    while fast and fast.next:
        slow = slow.next          # Moves 1 step
        fast = fast.next.next     # Moves 2 steps
        
        if slow == fast:
            return True # The fast pointer lapped the slow pointer!
            
    return False # Fast pointer hit the end of the list (None)

def demonstrate_cycle_detection():
    section_header("Algorithm: Detect a Cycle (Floyd's Tortoise and Hare)")
    
    # Create a normal list: 1 -> 2 -> 3 -> 4
    n1 = Node(1)
    n2 = Node(2)
    n3 = Node(3)
    n4 = Node(4)
    n1.next = n2
    n2.next = n3
    n3.next = n4
    
    print(f"Normal list has cycle? {has_cycle(n1)}")
    
    # Introduce a cycle: 4 points back to 2
    n4.next = n2
    print("Introduced a cycle (Node 4 points to Node 2).")
    print(f"Cyclic list has cycle? {has_cycle(n1)}")


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why does `LinkedList.append()` take O(N) time in a standard Singly Linked List?
   Answer: Because we only have a reference to the `head` node. To add an item to the end, we must traverse the entire list node-by-node until we find the node whose `next` pointer is `None`. (This can be fixed to O(1) by maintaining a `tail` pointer).

2. How do you reverse a Linked List in O(1) auxiliary space?
   Answer: You iterate through the list using three pointers (`prev`, `curr`, `next_node`). You temporarily save `curr.next` into `next_node`, change `curr.next` to point to `prev`, and then shift `prev` and `curr` forward.

3. How does Floyd's Cycle Detection (Tortoise and Hare) work?
   Answer: You use a `slow` pointer (moves 1 step) and a `fast` pointer (moves 2 steps). If there is a cycle, the `fast` pointer will loop around and eventually land on the exact same node as the `slow` pointer. If there is no cycle, the `fast` pointer will hit `None`.
"""

if __name__ == "__main__":
    demonstrate_linked_list()
    demonstrate_reverse()
    demonstrate_cycle_detection()
    print("\n[SUCCESS] Laboratory: Linked Lists Completed.")
