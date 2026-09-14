"""
# ==============================================================================
# LABORATORY: COMPETITIVE PROGRAMMING (CONTEST PRACTICE: MEDIUM)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# "Medium" problems are the gatekeepers of software engineering interviews.
# They require combining two different data structures, or recognizing a hidden 
# algorithm disguised as a real-world scenario.
#
# If a problem asks you to find the "Longest substring without repeating characters", 
# you cannot check every substring in O(N^2) time. You must invent a dynamic 
# "Sliding Window" using two pointers that expands and contracts like an accordion 
# in exactly O(N) time.
#
# If a problem asks you to find the "Number of Islands" on a 2D grid, you 
# cannot use normal loops. You must view the grid as an implicit Graph and 
# execute a recursive Depth-First Search (DFS) to physically sink (mutate) the 
# islands as you count them.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master the Sliding Window accordion technique.
# - Master Implicit Graph Traversal (DFS on a 2D Matrix).
#
# ==============================================================================
"""

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE SLIDING WINDOW (LONGEST SUBSTRING)
# ==============================================================================
def length_of_longest_substring(s: str) -> int:
    """
    Problem: Find the length of the longest substring without repeating characters.
    Time Complexity: O(N)
    Space Complexity: O(min(N, Alphabet_Size))
    """
    # Dictionary to store the MOST RECENT index of every character we've seen
    char_index_map = {}
    
    left = 0
    max_length = 0
    
    for right in range(len(s)):
        char = s[right]
        
        # If we have seen this character BEFORE, and its last known location 
        # is strictly INSIDE our current window... we have a collision!
        if char in char_index_map and char_index_map[char] >= left:
            # We must contract the left side of the window!
            # We teleport the left pointer exactly one step past the collision point.
            # This instantly resolves the duplicate without any slow `while` loops!
            left = char_index_map[char] + 1
            
        # Record/Update the character's most recent location
        char_index_map[char] = right
        
        # Update our mathematical maximum length
        current_window_length = right - left + 1
        max_length = max(max_length, current_window_length)
        
    return max_length

def demonstrate_sliding_window():
    section_header("Sliding Window (Longest Substring)")
    
    text = "abcabcbb"
    print(f"String: '{text}'")
    
    ans = length_of_longest_substring(text)
    
    print(f"\nLongest Substring Length: {ans}")
    print("Why? 'abc' is length 3. When the second 'a' arrives, the window ")
    print("instantly contracts its left side, discarding the first 'a'!")


# ==============================================================================
# 4. IMPLICIT GRAPH TRAVERSAL (NUMBER OF ISLANDS)
# ==============================================================================
def num_islands(grid: list[list[str]]) -> int:
    """
    Problem: Given a 2D grid of '1's (land) and '0's (water), count the number of islands.
    An island is surrounded by water and is formed by connecting adjacent lands 
    horizontally or vertically.
    
    Time Complexity: O(R * C) where R is rows, C is columns.
    Space Complexity: O(R * C) for the DFS recursion stack in the worst case.
    """
    if not grid:
        return 0
        
    rows = len(grid)
    cols = len(grid[0])
    island_count = 0
    
    def sink_island(r: int, c: int) -> None:
        """
        A recursive DFS that physically mutates the grid to '0' to prevent 
        double-counting the exact same island later!
        """
        # Base Case / Boundary Check:
        # If we step off the edge of the map, or we step in water ('0'), Stop!
        if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] == '0':
            return
            
        # SINK THE LAND!
        grid[r][c] = '0'
        
        # Recursively explore all 4 cardinal directions (N, S, E, W)
        sink_island(r - 1, c) # Up
        sink_island(r + 1, c) # Down
        sink_island(r, c - 1) # Left
        sink_island(r, c + 1) # Right

    # Scan every single coordinate on the map
    for r in range(rows):
        for c in range(cols):
            # If we find land...
            if grid[r][c] == '1':
                # We found a completely new island!
                island_count += 1
                
                # Launch the DFS to violently sink this entire island so we 
                # never count any part of it again!
                sink_island(r, c)
                
    return island_count

def demonstrate_dfs_matrix():
    section_header("Implicit Graph DFS (Number of Islands)")
    
    # We use lists of characters. 
    # Notice there are 3 distinct islands.
    grid = [
        ['1', '1', '0', '0', '0'],
        ['1', '1', '0', '0', '0'],
        ['0', '0', '1', '0', '0'],
        ['0', '0', '0', '1', '1']
    ]
    
    print("Grid Map:")
    for row in grid:
        print(" ".join(row))
        
    ans = num_islands(grid)
    
    print(f"\nNumber of Islands Found: {ans}")
    print("The DFS triggered exactly 3 times. Each time it triggered, it acted ")
    print("like an infection, turning all connected '1's into '0's!")


def run_all_labs():
    demonstrate_sliding_window()
    demonstrate_dfs_matrix()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Explain the "Accordion" mathematical behavior of the Sliding Window pointer `left = char_index_map[char] + 1`. Why do we avoid a `while` loop?
   Answer: A naive sliding window uses a `while` loop to slowly increment `left` one step at a time, checking the string until the duplicate character falls out of the window. This works, but it's slow. We can achieve strict $O(N)$ time by using a Hash Map to store the *exact index* where every character was last seen. If we encounter a duplicate 'a', and the Hash Map says the previous 'a' was at index 5, we mathematically know that indices 0, 1, 2, 3, and 4 are absolutely useless to us. The window MUST shrink past index 5 to survive. We instantly teleport `left = 5 + 1 = 6`. This eliminates the `while` loop and makes the algorithm blindingly fast.

2. In the "Number of Islands" DFS, why do we aggressively mutate the input grid (`grid[r][c] = '0'`) instead of keeping a separate `visited` array?
   Answer: Space Complexity optimization! If the grid is $10,000 \times 10,000$, a separate `visited` boolean matrix requires allocating an additional 100 Million booleans in RAM. This wastes memory. Since the problem rarely strictly forbids modifying the input (and if it does, you clarify with the interviewer), we can use the input grid itself as the state tracker! By physically "sinking" the island (overwriting '1' with '0'), we mathematically guarantee that the outer `for` loops will never accidentally trigger a new island count on a piece of land we already explored. It achieves the exact same state-tracking with $O(1)$ auxiliary memory!

3. When executing a DFS on a 2D Matrix, what is the absolute most critical first line of code inside the recursive function?
   Answer: The Boundary Check! `if r < 0 or r >= rows or c < 0 or c >= cols:` If you are at `grid[0][0]` and you attempt to explore "Up" (`r - 1`), you pass `-1` into the recursion. If you do not have a boundary check, Python will mathematically interpret `grid[-1][0]` as wrapping around to the absolute bottom row of the matrix! This will cause your DFS to teleport across the map and erroneously connect islands that are miles apart. In languages like C++, it will trigger an immediate Segmentation Fault and crash. The boundary check mathematically enforces the physical edges of the 2D plane.
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Contest Practice (Medium) Completed.")
