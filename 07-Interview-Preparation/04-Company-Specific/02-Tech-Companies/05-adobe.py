"""
# ==============================================================================
# LABORATORY: INTERVIEW PREPARATION (ADOBE PYTHON QUESTIONS)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Adobe is the king of Digital Media and PDF processing. Their interviews heavily 
# skew towards Computational Geometry (bounding boxes, overlapping rectangles), 
# intense Matrix/Image processing, and complex String manipulation (rendering).
#
# A junior engineer calculates rectangle overlap by generating a 2D matrix of 
# pixels and manually checking if points intersect. This takes O(Area) time and 
# violently crashes if the coordinates are in the Millions.
#
# A senior engineer uses 1-Dimensional Projection Mathematics. By independently 
# projecting the Rectangles onto the X-axis and Y-axis, they mathematically prove 
# an intersection exists using strict $O(1)$ constant time comparisons!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master Computational Geometry (Rectangle Overlap).
# - Master Image Processing algorithms (Spiral Matrix Traversal).
# - Understand 1D axis projection for mathematical proofs.
#
# ==============================================================================
"""

from typing import List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. COMPUTATIONAL GEOMETRY (RECTANGLE OVERLAP)
# ==============================================================================
def is_rectangle_overlap(rec1: List[int], rec2: List[int]) -> bool:
    """
    Time: O(1) | Space: O(1)
    rec = [x1, y1, x2, y2] (Bottom-Left, Top-Right)
    
    Instead of calculating overlap, we calculate NON-OVERLAP!
    If Rectangle 1 is completely to the LEFT, RIGHT, TOP, or BOTTOM of Rectangle 2, 
    they mathematically cannot intersect.
    """
    # Unpack for mathematical clarity
    r1_x1, r1_y1, r1_x2, r1_y2 = rec1
    r2_x1, r2_y1, r2_x2, r2_y2 = rec2
    
    print(f"  Rec 1: BL({r1_x1},{r1_y1}) TR({r1_x2},{r1_y2})")
    print(f"  Rec 2: BL({r2_x1},{r2_y1}) TR({r2_x2},{r2_y2})")
    
    # 1. Are they completely separated on the X-axis?
    # R1 is strictly to the left of R2 OR R1 is strictly to the right of R2
    left_of = r1_x2 <= r2_x1
    right_of = r1_x1 >= r2_x2
    
    # 2. Are they completely separated on the Y-axis?
    # R1 is strictly below R2 OR R1 is strictly above R2
    below = r1_y2 <= r2_y1
    above = r1_y1 >= r2_y2
    
    # If ANY of these conditions are true, they physically cannot touch!
    if left_of or right_of or below or above:
        print("    -> Rectangles are completely isolated in mathematical space.")
        return False
        
    print("    -> Overlap mathematically proven via 1D Axis Projection!")
    return True

def demonstrate_rectangle_overlap():
    section_header("Adobe: Rectangle Overlap (Computational Geometry)")
    
    # Overlapping!
    rec1 = [0, 0, 2, 2]
    rec2 = [1, 1, 3, 3]
    print(f"Result (Overlap): {is_rectangle_overlap(rec1, rec2)}\n")
    
    # Isolated!
    rec3 = [0, 0, 1, 1]
    rec4 = [1, 0, 2, 1]
    print(f"Result (Isolated): {is_rectangle_overlap(rec3, rec4)}")


# ==============================================================================
# 4. IMAGE PROCESSING (SPIRAL MATRIX TRAVERSAL)
# ==============================================================================
def spiral_order(matrix: List[List[int]]) -> List[int]:
    """
    Time: O(R * C) | Space: O(1) (excluding output array)
    Traverses a 2D Matrix in a perfect Spiral (Clockwise).
    We mathematically maintain 4 dynamic boundaries (Top, Bottom, Left, Right).
    """
    if not matrix: return []
    
    result = []
    top, bottom = 0, len(matrix) - 1
    left, right = 0, len(matrix[0]) - 1
    
    print("  Executing Spiral Rendering Engine...")
    
    while top <= bottom and left <= right:
        # 1. Traverse TOP row (Left -> Right)
        for i in range(left, right + 1):
            result.append(matrix[top][i])
        top += 1 # The top row is consumed! Shrink the boundary!
        
        # 2. Traverse RIGHT column (Top -> Bottom)
        for i in range(top, bottom + 1):
            result.append(matrix[i][right])
        right -= 1 # The right column is consumed! Shrink the boundary!
        
        # CRITICAL CHECK: In a non-square matrix, the top/bottom or left/right 
        # boundaries might have violently crossed over! We MUST verify before 
        # doing the reverse passes!
        if top <= bottom:
            # 3. Traverse BOTTOM row (Right -> Left)
            for i in range(right, left - 1, -1):
                result.append(matrix[bottom][i])
            bottom -= 1
            
        if left <= right:
            # 4. Traverse LEFT column (Bottom -> Top)
            for i in range(bottom, top - 1, -1):
                result.append(matrix[i][left])
            left += 1
            
    return result

def demonstrate_spiral_matrix():
    section_header("Adobe: Spiral Matrix Traversal")
    
    matrix = [
        [1,  2,  3,  4],
        [5,  6,  7,  8],
        [9, 10, 11, 12]
    ]
    
    print("Original Image Matrix:")
    for row in matrix: print(f"  {row}")
    print()
    
    ans = spiral_order(matrix)
    print(f"Spiral Vector Output: {ans}")


def run_all_labs():
    demonstrate_rectangle_overlap()
    demonstrate_spiral_matrix()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "In the Rectangle Overlap problem, why is it algorithmically superior to mathematically prove NON-OVERLAP instead of mathematically proving OVERLAP?"
   Senior Answer: "Proving OVERLAP is an exercise in chaotic permutations. You have to check if the top-left corner of R1 is inside R2, OR if the bottom-right corner is inside, OR if R1 completely swallows R2, OR if they form a perfect cross (+ shape) where no corners are inside each other at all! It requires dozens of complex `if/else` checks. Proving NON-OVERLAP relies on 1-Dimensional Axis Projection. If we flatten the rectangles onto the X-axis, they become 1D lines. If those lines do not touch on the X-axis (`R1.right <= R2.left`), it is a physical law of geometry that the 2D rectangles cannot intersect. By checking exactly 4 simple conditions (Left, Right, Top, Bottom), we mathematically guarantee intersection in strict $O(1)$ time."

2. Interviewer: "In the Spiral Matrix algorithm, why are the `if top <= bottom` and `if left <= right` checks absolutely mandatory before doing the Reverse (Bottom and Left) passes?"
   Senior Answer: "If the matrix is perfectly square ($N \\times N$), those checks are actually redundant. However, Adobe works with images (e.g., $1920 \\times 1080$), which are highly asymmetrical rectangles ($M \\times N$). In an asymmetrical matrix, the algorithm will eventually run out of rows *before* it runs out of columns (or vice versa). If we finish traversing the Right column and `right -= 1` executes, the Top and Bottom boundaries might have already crossed over! If we blindly execute the Bottom row loop without checking `top <= bottom`, we will traverse a row we *already* processed, duplicating data and ruining the vectorization. The `if` statements act as safety valves to terminate the spiral instantly."

3. Interviewer: "How would you find the total Area of Overlap if two rectangles do intersect?"
   Senior Answer: "Once intersection is proven, we use 1D projection again. The overlapping region forms a brand new rectangle! The left side of the overlap is the `max` of the two left sides. The right side is the `min` of the two right sides. Therefore, the overlapping width is `max(0, min(R1.right, R2.right) - max(R1.left, R2.left))`. We apply the exact same mathematical logic to the Y-axis to find the overlapping height. Multiplying the width by the height gives the exact Area of Overlap in perfect $O(1)$ time."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Tech Companies Prep (Adobe) Completed.")
