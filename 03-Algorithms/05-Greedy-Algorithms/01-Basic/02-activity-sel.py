"""
# ==============================================================================
# LABORATORY: ACTIVITY SELECTION (MINIMUM RAILWAY PLATFORMS)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You already know how to pick the maximum number of activities that don't overlap 
# (Interval Scheduling via Earliest End Time).
#
# But what if you MUST schedule every single activity? 
# Example: You manage a Railway Station. Trains are arriving and departing. 
# You CANNOT tell a train to stay away. If a train arrives while another train 
# is still at the platform, you MUST build a second platform.
#
# Problem: What is the absolute MINIMUM number of platforms you need to build 
# so that no train ever has to wait?
#
# This is a classic FAANG Greedy Algorithm question.
# The naive approach checks for intersections taking O(N^2) time.
# The genius Greedy approach sorts the Arrival Times and Departure Times 
# COMPLETELY SEPARATELY. It treats the timeline as a sequence of events 
# (+1 train, -1 train), running in O(N log N) time!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Transform intervals into independent chronological events.
# - Use the Two-Pointer technique on sorted arrays.
# - Master the "Maximum Overlap" interval pattern.
#
# ==============================================================================
"""

from typing import List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE GREEDY EVENT ENGINE (TWO POINTERS)
# ==============================================================================
def find_min_platforms(arrivals: List[int], departures: List[int]) -> int:
    """
    Time Complexity: O(N log N) due to the sorting step.
    Space Complexity: O(1) auxiliary (assuming in-place sorting).
    """
    # 1. THE GREEDY TRICK
    # In standard Activity Selection, we kept the Arrival and Departure tied 
    # together in a Tuple (e.g. `(900, 930)`). 
    # For Platform counting, WE BREAK THEM APART. 
    # We sort arrivals and departures completely independently!
    # Why? Because we only care about "How many trains are physically present at 
    # any given chronological millisecond in time."
    arrivals.sort()
    departures.sort()
    
    n = len(arrivals)
    
    # 2. TWO POINTERS
    arr_idx = 0
    dep_idx = 0
    
    current_platforms_in_use = 0
    max_platforms_needed = 0
    
    # 3. CHRONOLOGICAL TRAVERSAL
    # We step through time by moving whichever pointer is earlier!
    while arr_idx < n and dep_idx < n:
        
        # Event A: A train is ARRIVING before (or exactly when) the next train departs.
        if arrivals[arr_idx] <= departures[dep_idx]:
            # A train pulled into the station!
            current_platforms_in_use += 1
            # Did this push us to a new all-time high of congestion?
            max_platforms_needed = max(max_platforms_needed, current_platforms_in_use)
            
            # Move the arrival pointer forward in time
            arr_idx += 1
            
        # Event B: A train is DEPARTING before the next train arrives.
        else:
            # A train left! A platform just opened up.
            current_platforms_in_use -= 1
            
            # Move the departure pointer forward in time
            dep_idx += 1
            
    # Note: We don't need to finish the `dep_idx` pointer if `arr_idx` finishes first.
    # If all trains have arrived, the station congestion can only decrease from 
    # this point forward. The `max_platforms_needed` is already locked in!
    
    return max_platforms_needed


def demonstrate_min_platforms():
    section_header("Algorithm: Minimum Railway Platforms")
    
    # Times are represented as integers (e.g. 900 = 9:00 AM, 1100 = 11:00 AM)
    arrivals =   [900,  940, 950,  1100, 1500, 1800]
    departures = [910, 1200, 1120, 1130, 1900, 2000]
    
    print("Train Schedules:")
    for i in range(len(arrivals)):
        print(f" Train {i+1}: Arrives {arrivals[i]}, Departs {departures[i]}")
        
    print("\nExecuting Independent Event Sorting (O(N log N))...")
    ans = find_min_platforms(arrivals, departures)
    
    print(f"\nMinimum Platforms Required: {ans} (Expected: 3)")
    print("Explanation:")
    print(" 9:00 -> Train 1 arrives (1 platform in use)")
    print(" 9:10 -> Train 1 departs (0 platforms in use)")
    print(" 9:40 -> Train 2 arrives (1 platform in use)")
    print(" 9:50 -> Train 3 arrives (2 platforms in use)")
    print("11:00 -> Train 4 arrives (3 platforms in use!) <-- MAX CONGESTION")
    print("11:20 -> Train 3 departs (2 platforms in use)")


# ==============================================================================
# 4. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Wait, if we sort Arrivals and Departures independently, don't we scramble the data? Train 3's departure might get mixed up with Train 1!
   Answer: YES, the data gets scrambled, and that is exactly the mathematical genius of this algorithm. We DO NOT CARE which specific train is leaving. We only care about the physical state of the Station. If a train leaves, a platform becomes empty. Period. By treating arrivals and departures as generic $+1$ and $-1$ chronological events, we perfectly track the aggregate volume of the station without needing to track individual train IDs.

2. What if a train arrives at the EXACT SAME MINUTE another train departs?
   Answer: Look at the `if arrivals[arr_idx] <= departures[dep_idx]:` logic. The `<=` sign means the Arrival is processed FIRST. This means the station handles the incoming train (requiring a new platform) before the outgoing train is fully cleared. If the rules of the railway state that a platform opens up instantly, you should change it to `<` so the Departure event triggers first, freeing up a platform before the new train claims it!

3. Could we solve this using an Array of size 2359 (minutes in a day)?
   Answer: Yes! That is called the "Line Sweep" or "Prefix Sum Array" technique. Create an array `timeline = [0] * 2400`. For every train, do `timeline[arrive] += 1` and `timeline[depart + 1] -= 1`. Then loop through the array, keeping a running sum, and record the absolute maximum. This runs in $O(N + T)$ time where $T$ is 2400. However, if the times were Unix Epoch Timestamps (massive numbers), the array would require gigabytes of RAM, making the Two-Pointer sorting technique mathematically superior for unbounded time domains.
"""

if __name__ == "__main__":
    demonstrate_min_platforms()
    print("\n[SUCCESS] Laboratory: Minimum Platforms Completed.")
