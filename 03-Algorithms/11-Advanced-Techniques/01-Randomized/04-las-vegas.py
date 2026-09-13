"""
# ==============================================================================
# LABORATORY: LAS VEGAS ALGORITHMS (SKIP LISTS)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You learned that Las Vegas algorithms ALWAYS return the correct answer, but 
# their runtime is probabilistic. The most famous example is Randomized Quicksort.
#
# But Randomized Algorithms aren't just for sorting! They can be used to build 
# entirely probabilistic Data Structures!
#
# The Problem with Binary Search Trees (BST):
# If you insert sorted data into a standard BST, it degrades into a $O(N)$ Linked 
# List. To fix this, Computer Scientists invented AVL Trees and Red-Black Trees. 
# But implementing a Red-Black Tree requires 200+ lines of mathematically agonizing 
# Left/Right Rotation logic.
#
# The Solution: The Skip List!
# Invented by William Pugh in 1989, a Skip List is a Linked List stacked on top 
# of other Linked Lists. 
# When you insert a new node, you flip a coin. 
# - Heads: The node grows an extra "level" up into the next list. Flip again!
# - Tails: Stop growing.
#
# Because it relies on 50/50 probability, the top levels contain exponentially 
# fewer nodes. Searching the list is identical to a Binary Search! You start at 
# the top level and skip massive chunks of the list before dropping down a level.
#
# The Skip List achieves expected $O(\log N)$ Search, Insert, and Delete times.
# It is a pure Las Vegas Data Structure! It ALWAYS stores and retrieves the correct 
# data, but the $O(\log N)$ speed is purely based on the coin flip probabilities.
#
# (Fun Fact: Redis, one of the most famous in-memory databases in the world, 
# uses Skip Lists under the hood for its Sorted Sets!).
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand Las Vegas Data Structures.
# - Implement the randomized coin-flip leveling logic.
# - Build a fully functional $O(\log N)$ Skip List.
#
# ==============================================================================
"""

import random
from typing import Optional, List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. SKIP LIST NODE ARCHITECTURE
# ==============================================================================
class SkipNode:
    def __init__(self, value: int, level: int):
        self.value = value
        # Instead of just `self.next`, a SkipNode has an ARRAY of next pointers!
        # `forward[0]` points to the next node on Level 0 (The absolute bottom floor).
        # `forward[1]` points to the next node on Level 1 (The Express lane).
        self.forward: List[Optional['SkipNode']] = [None] * (level + 1)


# ==============================================================================
# 4. SKIP LIST ENGINE
# ==============================================================================
class SkipList:
    def __init__(self, max_level: int = 16, p: float = 0.5):
        self.max_level = max_level
        # The probability of a coin flipping Heads (growing a level)
        self.p = p
        
        # The "Head" node is a dummy node that exists at the maximum possible level.
        self.head = SkipNode(value=-1, level=self.max_level)
        self.current_max_level = 0
        
    def _random_level(self) -> int:
        """
        The Las Vegas Randomizer!
        Flips a coin. If Heads, increases the level. If Tails, stops.
        Mathematically, 50% of nodes are Level 0, 25% are Level 1, 12.5% Level 2...
        """
        lvl = 0
        while random.random() < self.p and lvl < self.max_level:
            lvl += 1
        return lvl

    def search(self, target: int) -> bool:
        """
        Searches the Skip List in expected O(log N) time!
        """
        current = self.head
        
        # 1. Start at the absolute highest floor currently active!
        for i in range(self.current_max_level, -1, -1):
            
            # 2. Walk forward on this specific floor as long as the next node 
            # is SMALLER than our target. (We are skipping massive chunks!)
            while current.forward[i] and current.forward[i].value < target:
                current = current.forward[i]
                
            # 3. If the next node is >= target, we MUST DROP DOWN a floor to 
            # avoid overshooting! (The `for` loop automatically drops `i`).
            
        # We are now on Level 0, directly to the left of where the target should be!
        current = current.forward[0]
        
        return current is not None and current.value == target

    def insert(self, value: int) -> None:
        """
        Inserts a value in expected O(log N) time.
        """
        # `update` array keeps track of the "breadcrumbs" where we dropped down 
        # a level. If we grow a new node, we must update these exact breadcrumbs 
        # to point to the new node!
        update: List[Optional[SkipNode]] = [None] * (self.max_level + 1)
        current = self.head
        
        # Phase 1: Search for the insertion spot and leave breadcrumbs!
        for i in range(self.current_max_level, -1, -1):
            while current.forward[i] and current.forward[i].value < value:
                current = current.forward[i]
            # We are about to drop down. Save this node as a breadcrumb!
            update[i] = current
            
        # Phase 2: Las Vegas Coin Flip!
        new_lvl = self._random_level()
        
        # If the new node grew HIGHER than any existing node, we must update the 
        # Head dummy node to point to it!
        if new_lvl > self.current_max_level:
            for i in range(self.current_max_level + 1, new_lvl + 1):
                update[i] = self.head
            self.current_max_level = new_lvl
            
        # Phase 3: Create the node and splice the pointers!
        new_node = SkipNode(value, new_lvl)
        for i in range(new_lvl + 1):
            # The new node points to what the breadcrumb was pointing to
            new_node.forward[i] = update[i].forward[i]
            # The breadcrumb now points to the new node!
            update[i].forward[i] = new_node
            
    def display(self) -> None:
        """
        Visualizes the layers of the Skip List!
        """
        print("\n--- Skip List Visualization ---")
        for i in range(self.current_max_level, -1, -1):
            node = self.head.forward[i]
            print(f"Level {i}: ", end="")
            while node:
                print(f"{node.value} -> ", end="")
                node = node.forward[i]
            print("NULL")
        print("-------------------------------")


def demonstrate_las_vegas():
    section_header("Algorithm: Skip List (Las Vegas Data Structure)")
    
    sl = SkipList(max_level=4)
    
    print("Inserting ordered data: 10, 20, 30, 40, 50, 60, 70")
    print("In a normal BST, this would mathematically degrade into an O(N) linked list!")
    
    data = [10, 20, 30, 40, 50, 60, 70]
    for d in data:
        sl.insert(d)
        
    print("But thanks to the Las Vegas coin flips, the Skip List randomly self-balances:")
    sl.display()
    
    section_header("Searching the Skip List")
    
    target = 50
    print(f"Searching for {target}...")
    found = sl.search(target)
    print(f"Result: {'FOUND' if found else 'NOT FOUND'}")
    
    missing = 45
    print(f"Searching for {missing}...")
    found = sl.search(missing)
    print(f"Result: {'FOUND' if found else 'NOT FOUND'}")


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why is a Skip List classified as a Las Vegas algorithm and not Monte Carlo?
   Answer: A Monte Carlo algorithm has a bounded runtime, but the answer might be wrong. If a Skip List occasionally "lost" data or returned `False` when searching for an element that physically existed, it would be Monte Carlo. But a Skip List NEVER loses data. `Level 0` is a perfect, unbroken Linked List of every single element. If you search for an element, the algorithm is $100\%$ mathematically guaranteed to find it! Only the Speed (the runtime) is randomized based on the coin flips of the Express Lanes. Correct Answer + Randomized Speed = Las Vegas.

2. Why don't we just mandate that every 2nd node goes to Level 1, every 4th to Level 2?
   Answer: If you rigidly forced a mathematical structure (e.g., "every 2nd node levels up"), you would have to recalculate the levels of EVERY SINGLE NODE in the list whenever you inserted a new element in the middle to maintain the perfect structure! This would require $O(N)$ time for every insert. By using random coin flips, insertion is completely localized. You just drop the new node in, flip a coin, and adjust a few pointers in $O(\log N)$ time without ever touching the rest of the list!

3. How does the Search logic avoid overshooting the target?
   Answer: It never drops a level until it is absolutely forced to! If you are on Level 2 looking for the number 50, and the next node on Level 2 is 80, you KNOW you cannot move forward on Level 2. So you drop down to Level 1. Level 1 might have a node for 40. You move to 40. The next node on Level 1 is 60. You drop down to Level 0. Level 0 has 50! You found it! You move forward as fast as possible on the highest possible lane, and only drop down to a slower lane when you hit a roadblock.
"""

if __name__ == "__main__":
    demonstrate_las_vegas()
    print("\n[SUCCESS] Laboratory: Las Vegas Skip Lists Completed.")
