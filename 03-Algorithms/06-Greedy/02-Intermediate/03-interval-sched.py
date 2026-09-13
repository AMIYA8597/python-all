"""
# ==============================================================================
# LABORATORY: INTERVAL PARTITIONING (MEETING ROOMS II)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You already know two ways to schedule activities:
# 1. Maximize Activities (Activity Selection): Sort by END TIME. Greedily pick.
# 2. Minimum Platforms (Timeline Sweep): Sort Arrivals and Departures independently, 
#    and use a Two-Pointer +1/-1 algorithm.
#
# But there is a 3rd highly advanced scheduling problem: "Interval Partitioning" 
# (often famous on LeetCode as "Meeting Rooms II").
# Given N meetings `[start, end]`, what is the minimum number of conference 
# rooms required to schedule all of them?
#
# Wait, isn't this literally identical to "Minimum Platforms"?
# Yes. The Two-Pointer algorithm solves this perfectly.
#
# However, the Two-Pointer algorithm CANNOT tell you WHICH meeting is in WHICH 
# room. It scrambles the data and only counts the raw volume.
# If an interviewer asks: "Give me the exact schedule of which meetings happen 
# in Room 1 and Room 2", the Two-Pointer fails!
#
# To solve this, we use the Greedy Min-Heap Algorithm.
# We sort by START TIME. Then, we use a Priority Queue (Min-Heap) to constantly 
# track the END TIMES of the currently occupied rooms.
# This assigns specific rooms to specific meetings in O(N log N) time!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand why the Two-Pointer sweep destroys meeting identities.
# - Combine Sorting (by Start Time) with a Min-Heap (for End Times).
# - Master the allocation of physical resources (Rooms) to overlapping intervals.
#
# ==============================================================================
"""

import heapq
from typing import List, Tuple

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. GREEDY MIN-HEAP PARTITIONING (O(N log N))
# ==============================================================================
def min_meeting_rooms(meetings: List[Tuple[int, int]]) -> int:
    """
    Input: List of (start_time, end_time)
    Time Complexity: O(N log N) (Sorting the array, plus N heap push/pops).
    Space Complexity: O(N) (For the Min-Heap tracking active rooms).
    """
    if not meetings:
        return 0
        
    # 1. THE GREEDY HEURISTIC: SORT BY START TIME
    # We MUST process the meetings chronologically as they begin.
    meetings.sort(key=lambda x: x[0])
    
    # 2. THE MIN-HEAP (ACTIVE ROOMS)
    # The heap will store the END TIMES of the meetings currently happening.
    # The absolute smallest element in the heap will ALWAYS be the room that 
    # finishes the earliest!
    active_rooms_heap = []
    
    # Push the end time of the very first meeting into the heap (Room 1).
    heapq.heappush(active_rooms_heap, meetings[0][1])
    
    # 3. THE GREEDY ALLOCATION LOOP
    for i in range(1, len(meetings)):
        current_start, current_end = meetings[i]
        
        # Check the room that finishes the EARLIEST (at the top of the Min-Heap).
        earliest_room_end = active_rooms_heap[0]
        
        # --- THE GREEDY CHOICE ---
        # Did that earliest room finish before (or exactly when) our current meeting starts?
        if current_start >= earliest_room_end:
            # YES! The room is empty. 
            # We can reuse this EXACT room.
            # Pop the old meeting's end time out of the heap...
            heapq.heappop(active_rooms_heap)
            
        # If the earliest room hasn't finished yet, it means EVERY OTHER ROOM 
        # is also still occupied! We are FORCED to allocate a brand new room.
        # (We just push a new end time into the heap without popping anything).
        
        # Regardless of whether we reused a room or created a new one, this 
        # meeting is now happening, so we push its End Time into the heap!
        heapq.heappush(active_rooms_heap, current_end)
        
    # The number of elements currently in the heap is exactly the number of 
    # physical rooms we had to allocate!
    return len(active_rooms_heap)


def demonstrate_meeting_rooms():
    section_header("Algorithm: Meeting Rooms II (Min-Heap Partitioning)")
    
    # Format: (Start, End)
    meetings = [(0, 30), (5, 10), (15, 20)]
    
    print("Meeting Schedule:")
    for m in meetings:
        print(f" Meeting: {m[0]:2d} to {m[1]:2d}")
        
    print("\nExecuting Min-Heap Partitioning...")
    ans = min_meeting_rooms(meetings.copy())
    
    print(f"\nMinimum Rooms Required: {ans} (Expected: 2)")
    print("Explanation:")
    print(" 0: Meeting (0,30) starts. Room 1 created. Heap: [30]")
    print(" 5: Meeting (5,10) starts. Earliest room is 30. Conflict! Room 2 created. Heap: [10, 30]")
    print("15: Meeting (15,20) starts. Earliest room is 10. Room is free! Pop 10, Push 20. Heap: [20, 30]")
    
    print("\nMore complex schedule:")
    meetings2 = [(7, 10), (2, 4), (1, 5), (6, 8)]
    ans2 = min_meeting_rooms(meetings2)
    print(f"{meetings2} -> {ans2} Rooms Required (Expected: 2)")


# ==============================================================================
# 4. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why does `active_rooms_heap[0]` guarantee we find a free room if one exists?
   Answer: Because it is a Min-Heap! It inherently maintains the absolute smallest value at index 0 in $O(1)$ time. The smallest value represents the meeting that finishes the earliest. If the meeting that finishes the earliest is STILL occupying the room when our new meeting starts, it is mathematically guaranteed that every other meeting in the building is also still occupying their rooms! We instantly know we must build a new room.

2. How would you modify this code to output the actual Schedule (which meeting goes to which room)?
   Answer: Instead of just storing the integer `current_end` in the heap, store a Tuple: `(current_end, room_id)`. Also, maintain a list `schedules = [[] for _ in range(num_rooms)]`. When you pop a free room from the heap, you extract its `room_id`, append the new meeting to `schedules[room_id]`, and push `(new_end, room_id)` back into the heap!

3. Which is better: The Two-Pointer $+1/-1$ Sweep, or the Min-Heap?
   Answer: Both are mathematically $O(N \\log N)$ time and $O(N)$ space. The Two-Pointer sweep is slightly faster in raw CPU cycles because it only requires sorting, whereas the Heap requires continuous logarithmic tree re-balancing. However, the Heap is strictly superior if you need to track the identities of the resources (the actual rooms/platforms) rather than just the aggregate volume.
"""

if __name__ == "__main__":
    demonstrate_meeting_rooms()
    print("\n[SUCCESS] Laboratory: Interval Partitioning Completed.")
