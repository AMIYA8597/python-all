"""
# ==============================================================================
# LABORATORY: INTERVIEW PREPARATION (CODING PATTERNS - MERGE INTERVALS)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Interviewer: "You are building a Calendar App. Users submit meeting times. 
# Some meetings overlap. Merge all overlapping meetings into contiguous blocks."
#
# If you don't know the Merge Intervals pattern, you will attempt to compare 
# every meeting against every other meeting using a nested loop, creating an 
# O(N^2) algorithm that crashes when 10,000 users sync their calendars.
#
# A senior engineer knows the master trick: SORT BY START TIME.
# The moment the array of intervals is sorted by start time, the algorithm 
# miraculously collapses into a lightning-fast O(N) linear scan, because 
# overlapping intervals are mathematically forced to sit directly adjacent to 
# each other in the array!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master sorting tuples/lists by the 0th index.
# - Master the mathematical overlap condition (`current.start <= previous.end`).
# - Master merging logic (`new_end = max(current.end, previous.end)`).
#
# ==============================================================================
"""

from typing import List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. MERGE INTERVALS (THE CORE PATTERN)
# ==============================================================================
def merge_intervals(intervals: List[List[int]]) -> List[List[int]]:
    """
    Time: O(N log N) [due to sorting] | Space: O(N) [for output array]
    Merges all overlapping intervals in the dataset.
    """
    if len(intervals) <= 1:
        return intervals
        
    # CRITICAL STEP 1: Sort by Start Time
    # In Python, `sort()` on a list of lists automatically sorts by the 0th index.
    intervals.sort(key=lambda x: x[0])
    print(f"  [Sorted] {intervals}")
    
    # CRITICAL STEP 2: Initialize output with the first interval
    merged = [intervals[0]]
    
    for current in intervals[1:]:
        # We always compare the 'current' interval with the LAST merged interval
        last_merged = merged[-1]
        
        print(f"\n  Comparing: Last Merged {last_merged} vs Current {current}")
        
        # THE OVERLAP CONDITION: 
        # Does the current interval start BEFORE the last interval ends?
        if current[0] <= last_merged[1]:
            print(f"    -> OVERLAP DETECTED! ({current[0]} <= {last_merged[1]})")
            
            # THE MERGE LOGIC:
            # We don't just take the current end time, because one interval 
            # might completely swallow the other (e.g., [1, 10] and [2, 5]).
            # We take the MAXIMUM of both end times!
            new_end = max(last_merged[1], current[1])
            last_merged[1] = new_end
            
            print(f"    -> Merged into: {last_merged}")
        else:
            print("    -> NO OVERLAP. Appending as a new independent block.")
            merged.append(current)
            
    return merged

def demonstrate_merge_intervals():
    section_header("Merge Intervals (Calendar App)")
    
    # Unsorted and messy!
    intervals = [[1, 3], [8, 10], [2, 6], [15, 18]]
    print(f"Original Meetings: {intervals}\n")
    
    result = merge_intervals(intervals)
    print(f"\nFinal Consolidated Meetings: {result}")


# ==============================================================================
# 4. INSERT INTERVAL (EDGE CASE MANIPULATION)
# ==============================================================================
def insert_interval(intervals: List[List[int]], new_interval: List[int]) -> List[List[int]]:
    """
    Time: O(N) | Space: O(N)
    Given a list of NON-OVERLAPPING intervals sorted by start time, insert a 
    new interval and merge if necessary.
    Because it's already sorted, we can do this in O(N) instead of O(N log N)!
    """
    merged = []
    i = 0
    n = len(intervals)
    
    # Step 1: Add all intervals that end BEFORE the new interval starts.
    while i < n and intervals[i][1] < new_interval[0]:
        merged.append(intervals[i])
        i += 1
        
    # Step 2: Merge all intervals that overlap with the new interval!
    # Overlap condition: Current starts BEFORE or exactly WHEN the new ends.
    while i < n and intervals[i][0] <= new_interval[1]:
        # Mutate the new_interval to swallow all overlaps!
        new_interval[0] = min(new_interval[0], intervals[i][0])
        new_interval[1] = max(new_interval[1], intervals[i][1])
        i += 1
    
    merged.append(new_interval)
    
    # Step 3: Add all remaining intervals that start AFTER the new interval ends.
    while i < n:
        merged.append(intervals[i])
        i += 1
        
    return merged

def demonstrate_insert_interval():
    section_header("Insert Interval (O(N) Optimization)")
    
    intervals = [[1, 2], [3, 5], [6, 7], [8, 10], [12, 16]]
    new_meeting = [4, 8]
    
    print(f"Existing Schedule (Sorted): {intervals}")
    print(f"New Meeting to Insert: {new_meeting}")
    print(f"  -> Notice the new meeting overlaps with [3,5], [6,7], and [8,10]!")
    
    result = insert_interval(intervals, new_meeting)
    print(f"\nFinal Schedule: {result}")


def run_all_labs():
    demonstrate_merge_intervals()
    demonstrate_insert_interval()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "Why does sorting the array by Start Time magically reduce the merging logic to a single $O(N)$ linear scan?"
   Senior Answer: "If the array is unsorted, interval $[10, 15]$ could be at index 0, and interval $[11, 12]$ could be at index 100, forcing you to compare every single element against every other element ($O(N^2)$). By sorting by Start Time, you mathematically guarantee a chronological progression. If interval $A$ starts before interval $B$, and interval $A$ ends before interval $B$ even begins, it is mathematically impossible for interval $A$ to overlap with $B$, $C$, $D$, or any subsequent interval in the entire array! Therefore, we only ever need to check the 'Current' interval against the absolute 'Last Merged' interval in our output array, collapsing the logic into a pure $O(N)$ scan."

2. Interviewer: "When merging two overlapping intervals $A$ and $B$, why can't we just set the new End Time to `B.end`?"
   Senior Answer: "Because sorting by Start Time does not guarantee anything about the End Times. If $A = [1, 10]$ and $B = [2, 5]$, they clearly overlap because $B$ starts before $A$ ends ($2 \\le 10$). However, interval $A$ completely swallows interval $B$. If you blindly set the merged End Time to `B.end` (which is 5), you just corrupted the data by shrinking the meeting block! You must always take the mathematical maximum: `new_end = max(A.end, B.end)`."

3. Interviewer: "In the 'Insert Interval' problem, the input array is already sorted. Could we just append the new interval to the array, call `.sort()`, and run the standard Merge algorithm?"
   Senior Answer: "Yes, you could, but you would fail the interview. Calling `.sort()` forces the algorithmic time complexity to $O(N \\log N)$. Because the interviewer explicitly stated the array is already sorted and non-overlapping, you are expected to leverage that state to achieve a strict $O(N)$ solution. By using a 3-phase `while` loop (Phase 1: safely append everything before, Phase 2: sequentially swallow all overlaps into a single megablock, Phase 3: append everything after), we execute the insertion perfectly without ever triggering the heavy $O(N \\log N)$ sorting engine."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Interview Prep (Merge Intervals) Completed.")
