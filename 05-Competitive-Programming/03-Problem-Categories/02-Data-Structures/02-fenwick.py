"""
# ==============================================================================
# LABORATORY: COMPETITIVE PROGRAMMING (2D FENWICK TREES)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A standard 1D Fenwick Tree allows you to update an array element and query 
# a 1D range sum in O(log N) time.
#
# But what if the problem is on a 2D Grid (a Matrix)?
# "You have a 1000 x 1000 pixel image. Update the pixel at (X, Y) to value V. 
# Query the sum of all pixels inside the rectangle defined by Top-Left (R1, C1) 
# and Bottom-Right (R2, C2)."
#
# A 2D Segment Tree is a coding nightmare, requiring hundreds of lines of code 
# and massive memory overhead.
#
# A 2D Fenwick Tree extends the bitwise logic (`i & -i`) into two dimensions, 
# utilizing a nested loop structure. It solves 2D Point Updates and 2D Range 
# Queries in exactly O(log N * log M) time using a tiny fraction of code!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the architecture of a 2D Fenwick Tree (Matrix BIT).
# - Understand the 2D Inclusion-Exclusion principle for Range Queries.
# - Implement 2D `add()` and `query()`.
#
# ==============================================================================
"""

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. 2D FENWICK TREE ARCHITECTURE
# ==============================================================================
class FenwickTree2D:
    """
    A 1-indexed 2D Binary Indexed Tree (BIT) for 2D Point Updates and Range Sums.
    Space Complexity: O(R * C)
    Time Complexity: O(log R * log C) for Queries and Updates.
    """
    def __init__(self, rows: int, cols: int):
        self.rows = rows
        self.cols = cols
        
        # Initialize a 2D array of zeros.
        # Dimensions are (rows + 1) x (cols + 1) because Fenwick Trees are 1-indexed.
        self.tree = [[0] * (cols + 1) for _ in range(rows + 1)]
        
    def add(self, r: int, c: int, delta: int) -> None:
        """
        Adds `delta` to the cell at (r, c).
        Updates all subsequent 2D nodes in the matrix hierarchy.
        """
        # Outer loop iterates through the Rows
        i = r
        while i <= self.rows:
            # Inner loop iterates through the Columns for the current Row
            j = c
            while j <= self.cols:
                self.tree[i][j] += delta
                # Bitwise hop to the next responsible Column
                j += j & (-j)
            # Bitwise hop to the next responsible Row
            i += i & (-i)
            
    def query_prefix(self, r: int, c: int) -> int:
        """
        Calculates the sum of all cells in the rectangle from (1, 1) to (r, c).
        """
        total = 0
        i = r
        while i > 0:
            j = c
            while j > 0:
                total += self.tree[i][j]
                # Bitwise hop backwards through the Columns
                j -= j & (-j)
            # Bitwise hop backwards through the Rows
            i -= i & (-i)
        return total
        
    def query_region(self, r1: int, c1: int, r2: int, c2: int) -> int:
        """
        Calculates the sum of the sub-matrix defined by Top-Left (r1, c1) 
        and Bottom-Right (r2, c2).
        
        This relies on the 2D Inclusion-Exclusion Principle!
        Sum = Total - TopRect - LeftRect + TopLeftOverlap
        """
        total = self.query_prefix(r2, c2)
        top_rect = self.query_prefix(r1 - 1, c2)
        left_rect = self.query_prefix(r2, c1 - 1)
        top_left_overlap = self.query_prefix(r1 - 1, c1 - 1)
        
        return total - top_rect - left_rect + top_left_overlap


# ==============================================================================
# 4. EXECUTING THE 2D FENWICK TREE
# ==============================================================================
def demonstrate_2d_fenwick():
    section_header("Executing a 2D Fenwick Tree")
    
    # Let's create a 3x3 Matrix (0-indexed)
    matrix = [
        [3, 0, 1],
        [5, 6, 3],
        [1, 2, 0]
    ]
    
    print("Original Matrix:")
    for row in matrix: print(row)
    
    ROWS = len(matrix)
    COLS = len(matrix[0])
    
    # 1. Initialize the 2D Tree
    bit2d = FenwickTree2D(ROWS, COLS)
    
    # 2. Build the Tree
    # Time: O(R * C * log R * log C)
    for r in range(ROWS):
        for c in range(COLS):
            # Remember: Fenwick Tree MUST be 1-indexed!
            bit2d.add(r + 1, c + 1, matrix[r][c])
            
    print("\n2D Fenwick Tree built successfully.")
    
    # 3. Range Query (Sub-Matrix Sum)
    # Query the bottom-right 2x2 square:
    # 6 3
    # 2 0
    # True Sum: 6 + 3 + 2 + 0 = 11
    # 0-indexed coords: TopLeft(1, 1), BottomRight(2, 2)
    # 1-indexed coords: TopLeft(2, 2), BottomRight(3, 3)
    r1, c1 = 2, 2
    r2, c2 = 3, 3
    
    ans = bit2d.query_region(r1, c1, r2, c2)
    print(f"\nQuery Region (1-indexed) [{r1},{c1}] to [{r2},{c2}]: {ans}")
    
    # 4. Point Update
    # Update the cell at (1, 1) (which is the '6') by adding +4 (making it 10)
    update_r, update_c = 2, 2
    delta = 4
    print(f"\nUpdating cell (1-indexed) [{update_r},{update_c}] with a delta of {delta}...")
    bit2d.add(update_r, update_c, delta)
    
    # Query again
    # True Sum: 10 + 3 + 2 + 0 = 15
    ans2 = bit2d.query_region(r1, c1, r2, c2)
    print(f"Query Region after update: {ans2}")
    
    print("\nThe entire 2D Data Structure is just ~30 lines of code!")


def run_all_labs():
    demonstrate_2d_fenwick()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Explain the Time Complexity of an update in a 2D Fenwick Tree.
   Answer: In a 1D Fenwick Tree, an update takes $O(\log N)$ time because the bitwise `i & -i` trick hops through the array logarithmically. A 2D Fenwick Tree uses nested loops. The outer loop hops through the Rows in $O(\log R)$ time, and for every Row hop, the inner loop hops through the Columns in $O(\log C)$ time. The loops are multiplicative, making the total Time Complexity strictly $O(\log R \times \log C)$. For a massive $1000 \times 1000$ matrix, an update requires at most $10 \times 10 = 100$ operations!

2. Explain the "Inclusion-Exclusion Principle" used in the `query_region()` function.
   Answer: A Fenwick Tree natively only calculates Prefix Sums starting from $(1,1)$ down to $(X,Y)$. If you want the sum of an arbitrary floating sub-matrix defined by Top-Left $(R_1, C_1)$ and Bottom-Right $(R_2, C_2)$, you first calculate the massive Prefix block from $(1,1)$ to $(R_2, C_2)$. However, this block contains too much data. You must subtract the horizontal rectangle above your target (`top_rect`) and the vertical rectangle to the left of your target (`left_rect`). Because you subtracted the overlapping top-left corner *twice* (once via the top rect, once via the left rect), the mathematics are broken. You must add the `top_left_overlap` back exactly once to restore geometric equilibrium. 

3. Why is it impossible to easily implement "Lazy Propagation Range Updates" on a standard Fenwick Tree?
   Answer: A Segment Tree has physical nodes with distinct, non-overlapping geometric boundaries (e.g., a node explicitly represents indices 0-3). This physical boundary allows the algorithm to safely "pause" and store an I.O.U. in a lazy array. A Fenwick Tree does not have explicit boundaries; its ranges heavily overlap and are mathematically entangled via binary indexing. If you try to delay an update, the entanglement completely breaks the bitwise logic for prefix queries. To do Range Updates + Range Queries with a Fenwick Tree, you cannot use a simple lazy array; you must mathematically construct two entirely separate Fenwick Trees and use a complex algebraic offset equation (`BIT1 * index - BIT2`).
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: 2D Fenwick Trees Completed.")
