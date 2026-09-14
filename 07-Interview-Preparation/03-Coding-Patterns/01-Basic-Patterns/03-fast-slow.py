"""
# ==============================================================================
# LABORATORY: INTERVIEW PREPARATION (CODING PATTERNS - FAST & SLOW POINTERS)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Interviewer: "Determine if a Linked List contains a cycle in O(1) Memory."
#
# A junior engineer uses a Hash Set to store the memory addresses of visited 
# nodes. If they see the same address twice, a cycle exists. This requires 
# O(N) memory. If the Linked List has 1 Billion nodes, you just crashed the 
# server with an Out-Of-Memory exception. You fail.
#
# A senior engineer uses Floyd's Cycle Detection Algorithm (The Tortoise and 
# the Hare). Two pointers traverse the list simultaneously. One moves 1 step 
# at a time (Slow), the other moves 2 steps at a time (Fast). If a cycle exists, 
# it is mathematically guaranteed that the Fast pointer will eventually "lap" 
# the Slow pointer and land on the exact same physical node. This requires 
# exactly O(1) memory!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master Floyd's Cycle Detection (Tortoise and Hare).
# - Master finding the EXACT Start Node of a cycle mathematically.
# - Master finding the exact Middle Node of a Linked List.
#
# ==============================================================================
"""

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. LINKED LIST ARCHITECTURE
# ==============================================================================
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def build_cyclic_list() -> ListNode:
    """Builds a Linked List: 1 -> 2 -> 3 -> 4 -> 5 -> (points back to 3)"""
    head = ListNode(1)
    n2 = ListNode(2)
    n3 = ListNode(3)
    n4 = ListNode(4)
    n5 = ListNode(5)
    
    head.next = n2
    n2.next = n3
    n3.next = n4
    n4.next = n5
    
    # THE FATAL CYCLE!
    n5.next = n3 
    return head


# ==============================================================================
# 4. FLOYD'S CYCLE DETECTION
# ==============================================================================
def has_cycle(head: ListNode) -> bool:
    """
    Time: O(N) | Space: O(1)
    The Fast pointer will mathematically catch the Slow pointer if a cycle exists.
    """
    if not head or not head.next: return False
    
    slow = head
    fast = head
    
    steps = 0
    while fast and fast.next:
        steps += 1
        slow = slow.next          # Moves 1 step
        fast = fast.next.next     # Moves 2 steps
        
        print(f"  Step {steps}: Slow is at [{slow.val}], Fast is at [{fast.val}]")
        
        # We compare physical memory addresses!
        if slow is fast:
            print("  -> [COLLISION] Fast pointer lapped the Slow pointer!")
            return True
            
    return False

def demonstrate_cycle_detection():
    section_header("Floyd's Cycle Detection (Tortoise & Hare)")
    print("Graph: 1 -> 2 -> 3 -> 4 -> 5 -> [points back to 3]\n")
    
    head = build_cyclic_list()
    result = has_cycle(head)
    print(f"\nResult: Contains Cycle? {result}")


# ==============================================================================
# 5. FINDING THE MIDDLE OF A LINKED LIST
# ==============================================================================
def build_linear_list() -> ListNode:
    """Builds a Linked List: 10 -> 20 -> 30 -> 40 -> 50"""
    head = ListNode(10)
    curr = head
    for val in [20, 30, 40, 50]:
        curr.next = ListNode(val)
        curr = curr.next
    return head

def find_middle(head: ListNode) -> ListNode:
    """
    Time: O(N) | Space: O(1)
    If Fast moves 2x speed, when Fast reaches the end, Slow MUST be exactly in the middle!
    """
    slow = head
    fast = head
    
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        
    return slow

def demonstrate_find_middle():
    section_header("Finding the Middle Node")
    print("Graph: 10 -> 20 -> 30 -> 40 -> 50")
    print("Expected Middle: 30\n")
    
    head = build_linear_list()
    mid_node = find_middle(head)
    
    print(f"Result: Middle Node is [{mid_node.val}]")
    print("This works perfectly in exactly 1 mathematical pass!")


def run_all_labs():
    demonstrate_cycle_detection()
    demonstrate_find_middle()


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "Why does the Fast pointer moving at 2x speed mathematically guarantee it will not 'skip over' the Slow pointer inside a cycle?"
   Senior Answer: "If the Fast pointer is moving at 2 nodes per step, and the Slow pointer is moving at 1 node per step, the relative mathematical velocity between them is exactly 1 node per step (2 - 1 = 1). This means the Fast pointer is effectively closing the gap on the Slow pointer by exactly 1 node per cycle iteration. Because the gap decreases by exactly 1, it is mathematically impossible for the Fast pointer to 'skip' the Slow pointer. It will perfectly collide with it."

2. Interviewer: "Once Floyd's algorithm detects a cycle by finding a collision point, how do you mathematically find the EXACT node where the cycle begins (e.g., node 3)?"
   Senior Answer: "This requires deep mathematical proof. Let $L$ be the distance from the Head to the Cycle Start, $X$ be the distance from the Cycle Start to the Collision Point, and $C$ be the total length of the cycle. When they collide, the Fast pointer has traveled exactly twice the distance of the Slow pointer: $2(L + X) = L + X + C \\implies L + X = C \\implies L = C - X$. This mathematically proves that the distance from the Head to the Cycle Start ($L$) is perfectly equal to the distance from the Collision Point to the Cycle Start ($C - X$)! Therefore, to find the Cycle Start, we leave the Fast pointer at the Collision Point, we teleport the Slow pointer back to the Head, and we move BOTH pointers at 1x speed. The exact node where they collide again is the Cycle Start."

3. Interviewer: "Why is the Fast/Slow pointer pattern superior for finding the Middle of a Linked List, compared to just traversing the whole list to count $N$, and then traversing again to $N/2$?"
   Senior Answer: "Traversing to count $N$, and then traversing again to $N/2$, requires roughly $1.5 \\times N$ total node visits. The Fast/Slow pointer pattern requires the Fast pointer to visit $N$ nodes, and the Slow pointer to visit $N/2$ nodes simultaneously. The algorithmic complexity is fundamentally identical (both are $O(N)$), however, the Fast/Slow pointer pattern completes the task in exactly one single physical pass through the data structure. In a highly concurrent system, or if the Linked List is streaming data from a network socket where you cannot traverse backwards, a one-pass algorithm is structurally mandatory."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Interview Prep (Fast & Slow Pointers) Completed.")
