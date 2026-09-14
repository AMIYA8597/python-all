"""
# ==============================================================================
# LABORATORY: COMPETITIVE PROGRAMMING (SWEEP LINE ALGORITHMS)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You are given 100,000 intervals (e.g., flight departure and arrival times). 
# You need to find the maximum number of airplanes in the air at the exact same time.
#
# If you create an array of every single minute in the day and increment the 
# count for every minute of a flight (`arr[start:end] += 1`), and the timeline 
# stretches for $10^9$ seconds, you will run out of memory and trigger a Time 
# Limit Exceeded (TLE) crash.
#
# You must use a "Sweep Line" algorithm.
# A Sweep Line algorithm does not simulate the passage of time second-by-second. 
# It jumps INSTANTLY from one significant Event (a takeoff) to the next significant 
# Event (a landing). It reduces a $10^9$ timeline into an $O(N \log N)$ algorithm!
#
# This same logic extends to 2D Geometry. How do you find the total Area of 
# 100 overlapping rectangles? You sweep a vertical line horizontally across the 
# rectangles, processing "Left Edges" and "Right Edges" as Events!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand Event-Driven Architecture.
# - Solve 1D Meeting Rooms (Max Overlap).
# - Understand the blueprint for 2D Area of Overlapping Rectangles.
#
# ==============================================================================
"""

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. 1D SWEEP LINE (MEETING ROOMS / MAX OVERLAP)
# ==============================================================================
def max_overlapping_intervals(intervals: list[list[int]]) -> int:
    """
    Finds the maximum number of overlapping intervals at any point in time.
    Time Complexity: O(N log N)
    Space Complexity: O(N)
    """
    events = []
    
    # 1. Deconstruct intervals into individual "Events"
    for start, end in intervals:
        # +1 means an interval STARTED (We need another room!)
        events.append((start, +1))
        # -1 means an interval ENDED (A room freed up!)
        events.append((end, -1))
        
    # 2. Sort the Events by Time!
    # If a start and end happen at the EXACT SAME TIME (e.g., [1, 2] and [2, 3]),
    # should they overlap? Usually, no. 
    # Because we used -1 for ending and +1 for starting, Python's default tuple 
    # sorting will sort the -1 BEFORE the +1 if the times are identical!
    # This automatically processes the "Landing" before the "Takeoff", perfectly 
    # preventing artificial overlaps.
    events.sort()
    
    max_overlap = 0
    current_overlap = 0
    
    # 3. Sweep the Line across the sorted events
    for time, delta in events:
        current_overlap += delta
        max_overlap = max(max_overlap, current_overlap)
        
    return max_overlap

def demonstrate_1d_sweepline():
    section_header("1D Sweep Line (Maximum Overlap)")
    
    intervals = [[1, 5], [2, 6], [8, 10], [5, 8], [3, 4]]
    print(f"Intervals (Start, End): {intervals}")
    
    max_rooms = max_overlapping_intervals(intervals)
    
    print(f"\nMaximum Overlap: {max_rooms}")
    print("Expected: 3 (Because intervals [1, 5], [2, 6], and [3, 4] all overlap around time 3.5)")


# ==============================================================================
# 4. 2D SWEEP LINE (AREA OF RECTANGLES)
# ==============================================================================
def area_of_rectangles(rectangles: list[list[int]]) -> int:
    """
    Calculates the total Area covered by a list of intersecting rectangles.
    Rectangles are given as: [x1, y1, x2, y2] (bottom-left and top-right).
    
    Time Complexity: O(N^2) for basic implementation. 
    (Can be optimized to O(N log N) with a Segment Tree).
    """
    # 1. Deconstruct into Vertical Line Events!
    events = []
    for x1, y1, x2, y2 in rectangles:
        # Event: (X_coordinate, Edge_Type, Bottom_Y, Top_Y)
        # Type +1 = Left Edge of a rectangle (Entering)
        events.append((x1, 1, y1, y2))
        # Type -1 = Right Edge of a rectangle (Leaving)
        events.append((x2, -1, y1, y2))
        
    events.sort()
    
    def calculate_active_y_length(active_intervals: list[tuple[int, int]]) -> int:
        """Helper to find the total length of Y segments currently active."""
        if not active_intervals: return 0
        
        # Sort active intervals by bottom Y
        active_intervals.sort()
        
        length = 0
        current_bottom = active_intervals[0][0]
        current_top = active_intervals[0][1]
        
        for y1, y2 in active_intervals[1:]:
            if y1 <= current_top:
                # They overlap, just extend the current top
                current_top = max(current_top, y2)
            else:
                # They are disconnected. Tally the current block and start a new one!
                length += (current_top - current_bottom)
                current_bottom = y1
                current_top = y2
                
        length += (current_top - current_bottom)
        return length

    total_area = 0
    active_intervals = []
    last_x = events[0][0]
    
    # 2. Sweep the Vertical Line from Left to Right
    for x, edge_type, y1, y2 in events:
        
        # Calculate the area generated since the last vertical event
        delta_x = x - last_x
        active_y = calculate_active_y_length(active_intervals)
        
        total_area += delta_x * active_y
        
        # Update active intervals
        if edge_type == 1:
            active_intervals.append((y1, y2))
        else:
            active_intervals.remove((y1, y2))
            
        last_x = x
        
    return total_area

def demonstrate_2d_sweepline():
    section_header("2D Sweep Line (Area of Union of Rectangles)")
    
    # Two overlapping rectangles
    # Rect 1: x1=0, y1=0, x2=4, y2=4 (Area 16)
    # Rect 2: x1=2, y1=2, x2=6, y2=6 (Area 16)
    # Overlap: 2x2 = Area 4. Total Area = 16 + 16 - 4 = 28.
    rectangles = [
        [0, 0, 4, 4],
        [2, 2, 6, 6]
    ]
    
    print(f"Rectangles: {rectangles}")
    
    area = area_of_rectangles(rectangles)
    
    print(f"\nTotal Area of Union: {area}")
    print("Expected: 28")


def run_all_labs():
    demonstrate_1d_sweepline()
    demonstrate_2d_sweepline()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. In a 1D Sweep Line processing time intervals, what is the exact behavior of Python's `sort()` when an Interval Start Time and an Interval End Time land on the exact same second?
   Answer: Python sorts tuples element by element. It first checks the Time. If the Time is identical, it checks the Delta. Because we assigned `-1` to End Events (Leaving) and `+1` to Start Events (Entering), Python mathematically sorts `-1` before `+1`. The algorithm will explicitly subtract a room from the overlap count *before* adding a new room. This mathematically guarantees that intervals like `[1, 2]` and `[2, 3]` do NOT trigger an overlap at Time 2, saving you from writing messy edge-case `if` statements.

2. Explain the fundamental philosophy of a Sweep Line algorithm. Why does it avoid Time Limit Exceeded (TLE) errors?
   Answer: A naive algorithm simulates continuous space or time. If a flight takes off at Second 1 and lands at Second 1,000,000, a naive loop iterates 1,000,000 times, doing absolutely nothing of value in the middle. A Sweep Line is strictly "Event-Driven". It ignores the empty space. It extracts only the Start and End points, sorts them, and "teleports" directly from one meaningful event to the next. The timeline is collapsed from an unbounded length of $O(T)$ down strictly to $O(N \log N)$ where $N$ is the number of intervals, mathematically immunizing the algorithm against massive time scales.

3. How could you optimize the 2D Sweep Line Area algorithm from $O(N^2)$ to $O(N \log N)$?
   Answer: In the $O(N^2)$ implementation, every time the vertical line moves horizontally to a new event, we recalculate the length of the Active Y-Intervals by sorting them, which takes $O(N \log N)$ for *every single step*. To optimize this to $O(N \log N)$ globally, we replace the `active_intervals` list with a 1D Segment Tree (or Lazy Segment Tree). When a Left Edge arrives, we perform a Range Update (`+1`) on the Y-axis. When a Right Edge arrives, we perform a Range Update (`-1`). The Segment Tree's root node instantly tracks the total length of Y-segments $>0$ in exactly $O(\log N)$ time per step!
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Sweep Line Algorithms Completed.")
