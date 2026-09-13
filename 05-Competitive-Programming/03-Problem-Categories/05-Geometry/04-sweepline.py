"""
================================================================================
Sweep Line Algorithms in Computational Geometry
================================================================================

This module provides a textbook-grade, interactive lesson on the Sweep Line
algorithm—a powerful algorithmic paradigm in Computational Geometry. 

--------------------------------------------------------------------------------
1. INTRODUCTION & MATHEMATICAL BACKGROUND
--------------------------------------------------------------------------------
The "Sweep Line" (or "Plane Sweep") technique involves an imaginary line (often 
vertical) that moves ("sweeps") across the plane from left to right (or top to 
bottom). As the sweep line moves, it stops at certain predefined "event points",
updating a data structure that maintains the state of the system at the current
sweep line position.

Key Components of a Sweep Line Algorithm:
1. **Event Queue**: A priority queue or sorted list containing the points where 
   the sweep line must pause. These are typically the x-coordinates of the objects 
   being processed.
2. **Active State Structure**: A dynamic data structure (like a Balanced Binary 
   Search Tree) that maintains the set of active objects intersecting the sweep 
   line.

Common problems solved using Sweep Line:
- Closest Pair of Points in a 2D plane: O(N log N)
- Line Segment Intersection (Bentley-Ottmann): O((N + K) log N), K = intersections
- Area/Perimeter of Union of Rectangles: O(N log N)
- Convex Hull (e.g., Graham Scan utilizes a pseudo-sweep angularly/x-coordinate)

--------------------------------------------------------------------------------
2. ALGORITHMIC ANALYSIS (BIG-O)
--------------------------------------------------------------------------------
Time Complexity: 
Generally dominated by sorting the events O(N log N) and updating the active state 
O(log N) for each of the O(N) events. 
Overall: O(N log N).

Space Complexity:
- Event Queue: O(N) memory to store event points.
- Active State: O(N) memory at most for currently active segments/points.
Overall: O(N).

--------------------------------------------------------------------------------
3. REAL-WORLD APPLICATIONS
--------------------------------------------------------------------------------
1. Computer Graphics: Rendering polygons, visibility determination, and clipping.
2. Geographic Information Systems (GIS): Map overlays, finding intersecting roads.
3. VLSI Design: Circuit board routing, detecting overlapping wires/components.
4. Collision Detection: Broad-phase collision detection in 2D physics engines.

================================================================================
"""

import math
from typing import List, Tuple, Optional, Set
from dataclasses import dataclass
from operator import attrgetter
import bisect

# ==============================================================================
# ALGORITHM 1: CLOSEST PAIR OF POINTS
# ==============================================================================
# Mathematical Concept: Given N points, find the pair with the smallest Euclidean
# distance. Naive approach is O(N^2). Sweep line solves this in O(N log N).

@dataclass(frozen=True)
class Point:
    """
    Represents a 2D point.
    """
    x: float
    y: float

    def distance_to(self, other: 'Point') -> float:
        """
        Calculates the Euclidean distance to another point.
        d = sqrt((x2 - x1)^2 + (y2 - y1)^2)
        """
        return math.hypot(self.x - other.x, self.y - other.y)

def closest_pair_sweep_line(points: List[Point]) -> Tuple[float, Optional[Tuple[Point, Point]]]:
    """
    Find the closest pair of points in a 2D plane using a Sweep Line approach.
    
    Time Complexity: O(N log N)
    Space Complexity: O(N)
    
    Parameters:
        points (List[Point]): A list of 2D points.
        
    Returns:
        Tuple[float, Optional[Tuple[Point, Point]]]: Minimum distance and the pair of points.
    """
    if len(points) < 2:
        return float('inf'), None

    # Step 1: Sort points by x-coordinate (the event points)
    # This takes O(N log N) time.
    sorted_points = sorted(points, key=lambda p: (p.x, p.y))
    
    min_dist = float('inf')
    best_pair = None
    
    # Active set of points, sorted by y-coordinate.
    # In Python, we can simulate this with a sorted list (bisect) or a balanced BST.
    # We use a standard list and bisect for simplicity and efficiency in small ranges.
    active_set: List[Point] = []
    
    left = 0
    
    for i in range(len(sorted_points)):
        current_point = sorted_points[i]
        
        # Remove points from the active set that are further left than current_point.x - min_dist.
        # This keeps the active set size small (at most 6 points in the band theoretically).
        while left < i and (current_point.x - sorted_points[left].x) >= min_dist:
            # We must find and remove the left point from the active set.
            # Since active_set is sorted by y, we use a linear search to remove (or binary search).
            # Note: For strict O(N log N) worst-case, active_set must be a balanced BST.
            # Python's list removal takes O(K), but K is bounded.
            remove_p = sorted_points[left]
            # Find and remove
            for j in range(len(active_set)):
                if active_set[j] == remove_p:
                    active_set.pop(j)
                    break
            left += 1
            
        # Check points in the active set whose y-coordinates are within [current_point.y - min_dist, current_point.y + min_dist]
        # We can use binary search to find the lower bound.
        # To use bisect, we create dummy points or just extract y.
        # Here we just iterate through the active set, which is small due to the mathematical properties of the grid.
        
        # Instead of strict binary search for simplicity, we just filter.
        # A true implementation would binary search by Y.
        y_lower = current_point.y - min_dist
        y_upper = current_point.y + min_dist
        
        # We iterate in reverse to check the closest y's first
        for active_p in active_set:
            if active_p.y < y_lower:
                continue
            if active_p.y > y_upper:
                # Since active_set is sorted by y, we can break early if we exceed the upper bound.
                # Actually, our active set isn't guaranteed perfectly sorted by y here unless we maintain it.
                pass
                
            dist = current_point.distance_to(active_p)
            if dist < min_dist:
                min_dist = dist
                best_pair = (active_p, current_point)
                
        # Insert current point into active set, maintaining sorted order by Y
        # O(N) insertion for list, but bounded.
        active_set.append(current_point)
        active_set.sort(key=lambda p: p.y)

    return min_dist, best_pair


# ==============================================================================
# ALGORITHM 2: INTERSECTION OF ORTHOGONAL LINE SEGMENTS
# ==============================================================================
# Mathematical Concept: Given horizontal and vertical line segments, find all points 
# where a horizontal segment crosses a vertical segment. 
# Using a sweep line, we move left to right.
# - Left endpoint of horizontal: Insert its Y into active set.
# - Right endpoint of horizontal: Remove its Y from active set.
# - Vertical segment: Query the active set for Ys between bottom and top endpoints.

@dataclass
class Segment:
    """
    Represents an orthogonal line segment (either purely horizontal or purely vertical).
    """
    x1: float
    y1: float
    x2: float
    y2: float
    
    def is_horizontal(self) -> bool:
        return self.y1 == self.y2
        
    def is_vertical(self) -> bool:
        return self.x1 == self.x2
        
    def normalize(self):
        """ Ensure coordinates go left-to-right, bottom-to-top. """
        if self.x1 > self.x2:
            self.x1, self.x2 = self.x2, self.x1
        if self.y1 > self.y2:
            self.y1, self.y2 = self.y2, self.y1

class EventType:
    LEFT_ENDPOINT = 0
    VERTICAL_SEG = 1
    RIGHT_ENDPOINT = 2

@dataclass
class Event:
    x: float
    type: int
    segment: Segment

def find_orthogonal_intersections(segments: List[Segment]) -> List[Point]:
    """
    Finds all intersections between horizontal and vertical segments.
    Time Complexity: O((N + K) log N) where K is number of intersections.
    Space Complexity: O(N)
    """
    events: List[Event] = []
    
    # Pre-process segments
    for seg in segments:
        seg.normalize()
        if seg.is_horizontal():
            events.append(Event(seg.x1, EventType.LEFT_ENDPOINT, seg))
            events.append(Event(seg.x2, EventType.RIGHT_ENDPOINT, seg))
        elif seg.is_vertical():
            events.append(Event(seg.x1, EventType.VERTICAL_SEG, seg))
            
    # Sort events by X coordinate.
    # If X is same, process LEFT before VERTICAL before RIGHT to catch boundary intersections.
    events.sort(key=lambda e: (e.x, e.type))
    
    intersections = []
    # Active horizontal segments, sorted by Y
    # Represented as a simple list for educational purposes.
    active_y: List[float] = []
    
    for event in events:
        if event.type == EventType.LEFT_ENDPOINT:
            # Insert y into active structure
            bisect.insort(active_y, event.segment.y1)
        elif event.type == EventType.RIGHT_ENDPOINT:
            # Remove y from active structure
            # Binary search to find and remove
            idx = bisect.bisect_left(active_y, event.segment.y1)
            if idx < len(active_y) and active_y[idx] == event.segment.y1:
                active_y.pop(idx)
        elif event.type == EventType.VERTICAL_SEG:
            # Query all active Ys that fall between the vertical segment's bottom and top
            y_bottom = event.segment.y1
            y_top = event.segment.y2
            
            # Find range
            start_idx = bisect.bisect_left(active_y, y_bottom)
            end_idx = bisect.bisect_right(active_y, y_top)
            
            for i in range(start_idx, end_idx):
                intersections.append(Point(event.x, active_y[i]))
                
    return intersections

# ==============================================================================
# ALGORITHM 3: AREA OF UNION OF RECTANGLES
# ==============================================================================
# Problem: Given N rectangles aligned with axes, compute total area of their union.
# Technique: Sweep line left to right. Maintain the total length of the sweep line
# that is currently covered by rectangles. Area += length_covered * delta_X.

@dataclass
class Rectangle:
    x_min: float
    y_min: float
    x_max: float
    y_max: float

@dataclass
class RectEvent:
    x: float
    is_left: bool
    y_min: float
    y_max: float

def union_area_rectangles(rectangles: List[Rectangle]) -> float:
    """
    Computes the total area covered by the union of axes-aligned rectangles.
    Time Complexity: O(N^2) with simple active list, O(N log N) with Segment Tree.
    Space Complexity: O(N)
    """
    events: List[RectEvent] = []
    
    for r in rectangles:
        events.append(RectEvent(r.x_min, True, r.y_min, r.y_max))
        events.append(RectEvent(r.x_max, False, r.y_min, r.y_max))
        
    events.sort(key=lambda e: e.x)
    
    def compute_covered_length(active_intervals: List[Tuple[float, float]]) -> float:
        if not active_intervals:
            return 0.0
        # Sort intervals by start
        active_intervals.sort(key=lambda intv: intv[0])
        covered = 0.0
        current_start, current_end = active_intervals[0]
        
        for start, end in active_intervals[1:]:
            if start <= current_end:
                current_end = max(current_end, end)
            else:
                covered += (current_end - current_start)
                current_start = start
                current_end = end
                
        covered += (current_end - current_start)
        return covered

    total_area = 0.0
    active_intervals = []
    last_x = 0.0
    
    for i, event in enumerate(events):
        if i > 0:
            delta_x = event.x - last_x
            covered_y = compute_covered_length(active_intervals)
            total_area += delta_x * covered_y
            
        if event.is_left:
            active_intervals.append((event.y_min, event.y_max))
        else:
            active_intervals.remove((event.y_min, event.y_max))
            
        last_x = event.x
        
    return total_area

# ==============================================================================
# MAIN TEST CASES
# ==============================================================================
if __name__ == '__main__':
    print("="*60)
    print("SWEEP LINE ALGORITHMS - INTERACTIVE TEST SUITE")
    print("="*60)
    
    # ---------------------------------------------------------
    # Test 1: Closest Pair of Points
    # ---------------------------------------------------------
    print("\n[1] Testing Closest Pair of Points...")
    points = [
        Point(2, 3), Point(12, 30), Point(40, 50),
        Point(5, 1), Point(12, 10), Point(3, 4)
    ]
    min_d, pair = closest_pair_sweep_line(points)
    print(f"Points: {points}")
    if pair:
        print(f"Closest Pair: ({pair[0].x}, {pair[0].y}) and ({pair[1].x}, {pair[1].y})")
        print(f"Distance: {min_d:.4f}")
    assert math.isclose(min_d, 1.41421356), "Closest pair test failed!"
    print("-> Closest pair test PASSED.")

    # ---------------------------------------------------------
    # Test 2: Orthogonal Segments Intersection
    # ---------------------------------------------------------
    print("\n[2] Testing Orthogonal Segments Intersection...")
    segments = [
        Segment(1, 2, 5, 2),   # Horizontal
        Segment(3, 1, 3, 4),   # Vertical (intersects at 3,2)
        Segment(2, 5, 6, 5),   # Horizontal
        Segment(5, 0, 5, 6)    # Vertical (intersects horizontal 1 at 5,2 and horizontal 2 at 5,5)
    ]
    intersections = find_orthogonal_intersections(segments)
    print(f"Found {len(intersections)} intersections:")
    for pt in intersections:
        print(f"  Intersection at: ({pt.x}, {pt.y})")
    assert len(intersections) == 3, "Intersection test failed!"
    print("-> Orthogonal intersection test PASSED.")

    # ---------------------------------------------------------
    # Test 3: Area of Union of Rectangles
    # ---------------------------------------------------------
    print("\n[3] Testing Area of Union of Rectangles...")
    rectangles = [
        Rectangle(0, 0, 2, 2),  # Area = 4
        Rectangle(1, 1, 3, 3)   # Area = 4, Overlap = 1 -> Total Union = 7
    ]
    area = union_area_rectangles(rectangles)
    print(f"Rectangles: {rectangles}")
    print(f"Total Union Area: {area}")
    assert math.isclose(area, 7.0), "Rectangle union area test failed!"
    print("-> Rectangle union area test PASSED.")
    
    print("\n" + "="*60)
    print("ALL TESTS PASSED SUCCESSFULLY!")
    print("="*60)
