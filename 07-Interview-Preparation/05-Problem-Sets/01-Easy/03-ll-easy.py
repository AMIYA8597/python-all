"""
# ==============================================================================
# LABORATORY: INTERVIEW PREPARATION (PROBLEM SETS - LINKED LIST EASY)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Linked Lists are the ultimate test of Pointer Manipulation. Unlike an Array, 
# a Linked List cannot be accessed by an index (e.g., `list[5]`). To reach the 
# 5th element, you must physically traverse memory pointers from node to node.
#
# A junior engineer merges two sorted lists by extracting all values into a 
# Python Array, sorting the array, and building a brand new Linked List. 
# This wastes O(N) Space and fails the core objective of the question.
#
# A senior engineer performs an In-Place Merge. They initialize a Dummy Node 
# to anchor the memory, and mathematically rewire the `next` pointers of the 
# existing nodes in strict O(1) Space, physically zippering the two lists 
# together without allocating any new nodes.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master the Dummy Node anchor pattern.
# - Master In-Place Pointer Rewiring (Merge Sorted Lists).
# - Master Floyd's Cycle-Finding Algorithm (Fast & Slow Pointers).
#
# ==============================================================================
"""

from typing import Optional, List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. LINKED LIST ARCHITECTURE & HELPERS
# ==============================================================================
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def build_list(values: List[int]) -> Optional[ListNode]:
    if not values: return None
    head = ListNode(values[0])
    curr = head
    for val in values[1:]:
        curr.next = ListNode(val)
        curr = curr.next
    return head

def print_list(head: Optional[ListNode], prefix: str = ""):
    vals = []
    curr = head
    while curr:
        vals.append(str(curr.val))
        curr = curr.next
    print(f"{prefix}{' -> '.join(vals)}")


# ==============================================================================
# 4. MERGE TWO SORTED LISTS (IN-PLACE ZIPPER)
# ==============================================================================
def merge_two_lists(l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
    """
    Time: O(N + M) | Space: O(1)
    Merges two sorted linked lists and returns it as a sorted list.
    """
    # THE DUMMY NODE ANCHOR!
    # By creating a dummy node, we avoid writing chaotic if/else statements 
    # to figure out which node should be the absolute Head of the new list.
    dummy = ListNode(-1)
    
    # `curr` is the active sewing needle, zippering the lists together!
    curr = dummy
    
    print("  Zippering lists together...")
    while l1 and l2:
        if l1.val <= l2.val:
            curr.next = l1
            l1 = l1.next
            print("    -> Attached from List 1")
        else:
            curr.next = l2
            l2 = l2.next
            print("    -> Attached from List 2")
            
        # Move the needle forward!
        curr = curr.next
        
    # One of the lists might be exhausted before the other!
    # Because they are already sorted, we can just attach the entire remaining 
    # subset of the surviving list in one mathematical O(1) operation!
    if l1:
        curr.next = l1
        print("    -> Appended remaining tail of List 1")
    elif l2:
        curr.next = l2
        print("    -> Appended remaining tail of List 2")
        
    # The true head of the merged list is the node immediately AFTER the dummy!
    return dummy.next

def demonstrate_merge():
    section_header("Easy: Merge Two Sorted Lists (O(1) Space)")
    
    l1 = build_list([1, 2, 4])
    l2 = build_list([1, 3, 4])
    
    print_list(l1, "  List 1: ")
    print_list(l2, "  List 2: ")
    print()
    
    merged_head = merge_two_lists(l1, l2)
    print_list(merged_head, "\n  Merged: ")


# ==============================================================================
# 5. LINKED LIST CYCLE (FLOYD's ALGORITHM)
# ==============================================================================
def has_cycle(head: Optional[ListNode]) -> bool:
    """
    Time: O(N) | Space: O(1)
    Determine if a linked list has a cycle in it.
    
    We could use a Hash Set to track memory addresses, but that requires O(N) RAM.
    Floyd's algorithm uses Physics (Fast and Slow runners) to detect cycles in O(1) RAM!
    """
    if not head or not head.next:
        return False
        
    slow = head
    fast = head.next
    
    print("  Initializing Fast and Slow Pointers...")
    
    # If there is no cycle, `fast` will hit the end of the list (None) and terminate.
    while fast and fast.next:
        # If they physically collide, a cycle MUST exist!
        if slow == fast:
            print("    -> [COLLISION] Fast pointer lapped the Slow pointer. Cycle Detected!")
            return True
            
        # Slow moves 1 step
        slow = slow.next
        # Fast moves 2 steps!
        fast = fast.next.next
        
    print("    -> [NO CYCLE] Fast pointer hit NULL. The track is straight.")
    return False

def demonstrate_cycle():
    section_header("Easy: Linked List Cycle (Floyd's Algorithm)")
    
    # Build a list: 3 -> 2 -> 0 -> -4
    node1 = ListNode(3)
    node2 = ListNode(2)
    node3 = ListNode(0)
    node4 = ListNode(-4)
    
    node1.next = node2
    node2.next = node3
    node3.next = node4
    
    # Create the cycle! -4 points back to 2!
    node4.next = node2
    
    print("  Built a Linked List where the Tail (-4) points back to Node (2).")
    ans = has_cycle(node1)
    print(f"\nResult: {ans} (Expected: True)")


def run_all_labs():
    demonstrate_merge()
    demonstrate_cycle()


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "In 'Merge Two Sorted Lists', why is the Dummy Node structurally superior to standard Head initialization?"
   Senior Answer: "Without a Dummy Node, we are forced to explicitly check which of the two input nodes is smaller *just to initialize the new Head pointer*. We must write an ugly `if l1.val < l2.val: head = l1; curr = head` block before the main loop even begins, duplicating logic and introducing Edge Cases if one of the lists is `None`. By initializing a Dummy Node (`ListNode(-1)`), the `curr` pointer has an indestructible mathematical anchor in RAM. The `while` loop cleanly handles all the logic uniformly, and we simply return `dummy.next` at the end, bypassing all Head-initialization Edge Cases."

2. Interviewer: "In 'Merge Two Sorted Lists', when one list is exhausted, why don't we need a `while` loop to attach the remaining elements of the surviving list?"
   Senior Answer: "Because a Linked List is held together by physical pointers. If `l1` is completely exhausted, the `curr` needle is pointing to the absolute end of our merged chain. If `l2` still has 50 nodes left, those 50 nodes are *already physically linked to each other* in perfectly sorted order! We do not need to traverse them. We simply execute a single $O(1)$ assignment: `curr.next = l2`. We surgically attach the entire remaining 50-node chain to the tail of our merged list in one instantaneous mathematical operation."

3. Interviewer: "In Floyd's Cycle-Finding Algorithm (Fast and Slow Pointers), mathematically prove why the Fast pointer will definitively collide with the Slow pointer instead of just infinitely jumping over it."
   Senior Answer: "If the list has a cycle, the Fast and Slow pointers are trapped in a loop. Think of it as a racetrack. The Fast pointer moves 2 steps, and the Slow pointer moves 1 step. Relative to the Slow pointer, the Fast pointer is approaching from behind at a speed of exactly +1 step per iteration. Because the relative distance between them is decreasing by exactly 1 unit per tick, it is mathematically impossible for the Fast pointer to 'skip' the Slow pointer. If the distance is 2, it becomes 1. If it is 1, it becomes 0. A distance of 0 means a flawless memory collision, proving the cycle."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Problem Sets (Linked List Easy) Completed.")
