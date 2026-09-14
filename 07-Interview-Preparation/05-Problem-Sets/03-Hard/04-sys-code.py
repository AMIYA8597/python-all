"""
# ==============================================================================
# LABORATORY: INTERVIEW PREPARATION (PROBLEM SETS - SYSTEMS CODING HARD)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# "Systems Coding" questions test your ability to architect mini-applications 
# inside a single class. You are not just solving an algorithm; you are designing 
# an API. These questions judge object-oriented design, encapsulated state 
# management, and O(1) performance tuning.
#
# A junior engineer designs Tic-Tac-Toe by maintaining an N x N 2D array and 
# running a loop to check the entire row, column, and diagonal every single 
# turn, yielding O(N) time complexity per move.
#
# A senior engineer mathematically collapses the board into 1D integer arrays 
# (`rows`, `cols`). When a player moves, they increment the integer for that 
# row. If the integer perfectly hits +N (or -N), that player wins instantly in 
# strict O(1) time complexity.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master O(1) State Aggregation (Design Tic-Tac-Toe).
# - Master Doubly-Linked-List + Hash Map coordination (LRU Cache).
# - Master Multi-Tiered Data Structures (LFU Cache).
#
# ==============================================================================
"""

import collections

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. DESIGN TIC-TAC-TOE (O(1) STATE AGGREGATION)
# ==============================================================================
class TicTacToe:
    """
    Time: O(1) per move | Space: O(N)
    Assume the following rules:
    1. A move is guaranteed to be valid and is placed on an empty block.
    2. Once a winning condition is reached, no more moves are allowed.
    3. A player who succeeds in placing n of their marks in a horizontal, vertical, 
       or diagonal row wins the game.
    """
    def __init__(self, n: int):
        self.n = n
        # Instead of an NxN grid, we just track the SUM of the marks!
        # Player 1 is +1. Player 2 is -1.
        self.rows = [0] * n
        self.cols = [0] * n
        self.diagonal = 0
        self.anti_diagonal = 0
        self.winner = 0

    def move(self, row: int, col: int, player: int) -> int:
        if self.winner != 0:
            print("  -> Game is already over!")
            return self.winner
            
        # Player 1 adds 1. Player 2 subtracts 1.
        val = 1 if player == 1 else -1
        
        # 1. UPDATE THE STATE COUNTERS
        self.rows[row] += val
        self.cols[col] += val
        
        # Is it on the main diagonal (\)? Mathematical rule: row == col
        if row == col:
            self.diagonal += val
            
        # Is it on the anti-diagonal (/)? Mathematical rule: row + col == n - 1
        if row + col == self.n - 1:
            self.anti_diagonal += val
            
        print(f"  [MOVE] Player {player} plays at ({row}, {col}).")
        
        # 2. O(1) WIN CONDITION CHECK!
        # If any counter hits EXACTLY +n, Player 1 wins!
        # If any counter hits EXACTLY -n, Player 2 wins!
        # We use absolute value to check both simultaneously!
        if (abs(self.rows[row]) == self.n or 
            abs(self.cols[col]) == self.n or 
            abs(self.diagonal) == self.n or 
            abs(self.anti_diagonal) == self.n):
            
            self.winner = player
            print(f"    -> [VICTORY] Player {player} wins the game!")
            return player
            
        return 0

def demonstrate_tic_tac_toe():
    section_header("Hard: Design Tic-Tac-Toe (O(1) State Tracking)")
    
    game = TicTacToe(3)
    game.move(0, 0, 1) # Player 1 (Top-Left)
    game.move(0, 2, 2) # Player 2 (Top-Right)
    game.move(1, 1, 1) # Player 1 (Center)
    game.move(2, 2, 2) # Player 2 (Bottom-Right)
    ans = game.move(2, 0, 1) # Player 1 (Bottom-Left - Anti-Diagonal Complete!)
    
    print(f"\nResult: Winner is Player {ans} (Expected: 1)")


# ==============================================================================
# 4. LRU CACHE (DOUBLY-LINKED LIST + HASH MAP)
# ==============================================================================
class ListNode:
    # A standard node, but it holds BOTH Key and Value!
    def __init__(self, key, val):
        self.key = key
        self.val = val
        self.prev = None
        self.next = None

class LRUCache:
    """
    Time: O(1) for GET and PUT | Space: O(Capacity)
    Design a Least Recently Used (LRU) Cache.
    
    A Hash Map provides O(1) lookups.
    A Doubly-Linked List provides O(1) removals and insertions.
    By physically fusing them together, we achieve perfect O(1) caching!
    """
    def __init__(self, capacity: int):
        self.capacity = capacity
        # The routing table! Key -> ListNode Memory Address!
        self.cache = {}
        
        # Dummy nodes to anchor the boundaries of the Doubly-Linked List!
        # `left` represents the LEAST recently used (the garbage dump).
        # `right` represents the MOST recently used (the fresh data).
        self.left, self.right = ListNode(0, 0), ListNode(0, 0)
        self.left.next = self.right
        self.right.prev = self.left

    def _remove(self, node: ListNode):
        """Physically rips a node out of the Linked List in O(1)."""
        prev_node = node.prev
        nxt_node = node.next
        prev_node.next = nxt_node
        nxt_node.prev = prev_node

    def _insert(self, node: ListNode):
        """Surgically inserts a node directly before the Right Dummy Node in O(1)."""
        prev_node = self.right.prev
        prev_node.next = node
        node.prev = prev_node
        node.next = self.right
        self.right.prev = node

    def get(self, key: int) -> int:
        if key in self.cache:
            # We accessed it! It must become the MOST recently used!
            node = self.cache[key]
            # Rip it out of its current physical location...
            self._remove(node)
            # ...and teleport it to the absolute right side of the list!
            self._insert(node)
            print(f"  [GET] Key {key} found. Value: {node.val}. Promoted to Most Recently Used.")
            return node.val
        print(f"  [GET] Key {key} NOT FOUND.")
        return -1

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            # The key exists! Rip the old node out completely!
            self._remove(self.cache[key])
            
        # Create a brand new node!
        new_node = ListNode(key, value)
        self.cache[key] = new_node
        self._insert(new_node)
        print(f"  [PUT] Key {key} -> Value {value} inserted.")
        
        # CAPACITY CHECK: Did we exceed the RAM limit?
        if len(self.cache) > self.capacity:
            # The LEAST recently used node is always parked exactly next to the Left Dummy!
            lru_node = self.left.next
            self._remove(lru_node)
            del self.cache[lru_node.key]
            print(f"    -> [EVICT] Capacity exceeded! Evicted Key {lru_node.key}.")

def demonstrate_lru():
    section_header("Hard: LRU Cache (Hash Map + Doubly-Linked List)")
    
    lru = LRUCache(2)
    lru.put(1, 100)
    lru.put(2, 200)
    lru.get(1)       # Accesses 1, making it fresh!
    lru.put(3, 300)  # Exceeds capacity! Evicts 2 (Least recently used).
    ans = lru.get(2) # -1 (Not found)
    
    print(f"\nResult of get(2): {ans} (Expected: -1)")


def run_all_labs():
    demonstrate_tic_tac_toe()
    demonstrate_lru()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "In Tic-Tac-Toe, how does mathematically summing the rows and columns into 1D arrays perfectly simulate the state of the board in $O(1)$ time?"
   Senior Answer: "If Player 1 is $+1$ and Player 2 is $-1$, placing a piece mathematically applies a localized vector force to the grid. If Player 1 plays 3 times in Row 0, the integer at `rows[0]` mathematically increments to $3$. Since the board size $N$ is 3, hitting exactly $+3$ physically proves that Player 1 occupies every single cell in that row. If Player 2 blocks the row, the integer receives a $-1$, dropping the sum to $+1$. It is mathematically impossible for that row to ever reach $+3$ or $-3$ again, flawlessly simulating the 'blocked' state without ever needing to iterate over a 2D array!"

2. Interviewer: "In the LRU Cache, why must the nodes be a **Doubly**-Linked List? Could we just use a Singly-Linked List?"
   Senior Answer: "If we used a Singly-Linked List, we could look up the Node's memory address in $O(1)$ time using the Hash Map, but we would have absolutely no way to remove it from the list! To remove a node in a Linked List, you must mathematically rewire the `next` pointer of the *Previous* node. A Singly-Linked List does not possess backwards pointers. We would be forced to iterate from the Head of the list to find the Previous node, degrading the `get()` and `put()` Time Complexity to a catastrophic $O(N)$. A Doubly-Linked List provides the `.prev` pointer, allowing us to surgically sever the node from both sides simultaneously in flawless $O(1)$ constant time."

3. Interviewer: "Why does the `ListNode` inside the LRU Cache store BOTH the Key and the Value, when the Hash Map already stores the Key?"
   Senior Answer: "When the cache exceeds its physical capacity, we must evict the Least Recently Used node. We can easily find the physical node because it sits right next to the Left Dummy node in our Doubly-Linked List. However, removing it from the List is only half the battle; we must also delete its routing entry from the Hash Map! The Hash Map requires the actual *Key* to execute `del map[key]`. If the node only stored the Value, we would have the physical node, but absolutely no idea what Key it belonged to in the Hash Map! By storing the Key inside the Node, it carries its own metadata, allowing for atomic $O(1)$ eviction across both Data Structures."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Problem Sets (Systems Coding Hard) Completed.")
