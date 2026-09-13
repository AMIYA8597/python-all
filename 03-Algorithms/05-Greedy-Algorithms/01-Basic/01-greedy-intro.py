"""
# ==============================================================================
# LABORATORY: GREEDY ALGORITHMS (THE LOCAL OPTIMUM PARADIGM)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A "Greedy Algorithm" is the simplest and most intuitive way to solve a problem. 
# At every step, it simply asks: "What is the absolute best move I can make right 
# NOW?" It makes that move, and it NEVER looks back. It never backtracks, and it 
# never re-evaluates past decisions.
#
# Because it never looks back, Greedy Algorithms are blazing fast (usually O(N log N) 
# because you just sort the data, then loop through it in O(N)).
#
# But there is a massive trap: Greedy Algorithms are often mathematically WRONG.
# If you are driving a car and you greedily take the road that looks the fastest 
# right now, it might lead you into a 5-hour traffic jam later. 
# 
# To use a Greedy Algorithm, you must mathematically PROVE that taking the 
# "Locally Optimal Choice" guarantees the "Globally Optimal Solution". 
# (This is called the "Greedy Choice Property").
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the Greedy Choice Property.
# - Differentiate between Fractional Knapsack (Greedy) and 0/1 Knapsack (DP).
# - Implement the classic Interval Scheduling Algorithm (Activity Selection).
#
# ==============================================================================
"""

from typing import List, Tuple

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. GREEDY SUCCESS: INTERVAL SCHEDULING (ACTIVITY SELECTION)
# ==============================================================================
def activity_selection(activities: List[Tuple[str, int, int]]) -> List[Tuple[str, int, int]]:
    """
    Given a list of activities with (Name, Start Time, End Time), find the 
    maximum number of activities you can attend without overlapping.
    
    Time Complexity: O(N log N) for the Sort.
    Space Complexity: O(N) for the results array.
    """
    # 1. THE GREEDY HEURISTIC
    # How should we pick activities? 
    # - Shortest duration first? (Fails: A short activity might block two long ones).
    # - Earliest start time first? (Fails: A massive activity starting at 8 AM 
    #   might block everything else for the entire day).
    # - EARLIEST END TIME FIRST! (Mathematically Proven).
    # If we always pick the activity that finishes the earliest, we leave the 
    # absolute maximum amount of free time available for the rest of the day!
    
    # Sort activities by END TIME (index 2 of the tuple).
    # Python's `sort()` uses Timsort, running in O(N log N).
    activities.sort(key=lambda x: x[2])
    
    selected = []
    
    # 2. THE GREEDY CHOICE LOOP
    last_end_time = -1
    
    for activity in activities:
        name, start_time, end_time = activity
        
        # If this activity starts AFTER (or exactly when) the previous one ended...
        if start_time >= last_end_time:
            
            # --- CHOOSE ---
            # We greedily lock it in!
            selected.append(activity)
            
            # Update the time tracker
            last_end_time = end_time
            
    return selected


def demonstrate_interval_scheduling():
    section_header("Algorithm: Activity Selection (Interval Scheduling)")
    
    # Format: (Name, Start Time, End Time)
    activities = [
        ("Math", 8, 10),
        ("Physics", 9, 11),
        ("Lunch", 11, 12),
        ("Chemistry", 10, 13),
        ("CS", 13, 15),
        ("Art", 12, 14)
    ]
    
    print("Unsorted Activities:")
    for act in activities:
        print(f" {act[0]}: {act[1]}:00 to {act[2]}:00")
        
    print("\nExecuting Greedy Earliest-End-Time Selection...")
    optimal_schedule = activity_selection(activities)
    
    print(f"\nMaximum Activities Attended: {len(optimal_schedule)}")
    for act in optimal_schedule:
        print(f" -> {act[0]}: {act[1]}:00 to {act[2]}:00")
        
    print("\nNotice how picking Math (ends 10), Lunch (ends 12), Art (ends 14)")
    print("is a perfectly valid schedule, but the Greedy algorithm found ")
    print("a way to fit 4 activities (Math, Lunch, Art, CS) by being optimal!")


# ==============================================================================
# 4. GREEDY VS DYNAMIC PROGRAMMING (THE KNAPSACK PARADOX)
# ==============================================================================
def explain_knapsack_paradox():
    section_header("Concept: When Greedy Fails")
    print("""
Why can a Greedy Algorithm solve "Fractional Knapsack" but fail catastrophically 
on "0/1 Knapsack"?

FRACTIONAL KNAPSACK:
You can break items apart. You have 10 lbs of Gold ($50,000) and 20 lbs of 
Silver ($3,000). 
Greedy Heuristic: "Sort by Value/Weight Density".
Gold is $5,000/lb. Silver is $150/lb.
You greedily shove as much Gold into the bag as possible. When you run out of 
Gold, you fill the exact remaining space with crushed Silver powder. 
Because you can perfectly fill the bag to 100.00% capacity using fractions, 
the Greedy Algorithm is mathematically perfect.

0/1 KNAPSACK:
You CANNOT break items apart. You have a 50 lb bag.
Item A: 10 lbs ($60)   -> Density: $6/lb
Item B: 20 lbs ($100)  -> Density: $5/lb
Item C: 30 lbs ($120)  -> Density: $4/lb

Greedy sorts by density and takes Item A (10 lbs). 
Remaining capacity is 40 lbs. 
Greedy takes Item B (20 lbs). 
Remaining capacity is 20 lbs. 
Greedy tries to take Item C, but it's 30 lbs. It doesn't fit. 
Greedy stops. Total Profit: $160. Bag has 20 lbs of empty wasted space.

Dynamic Programming evaluates all combinations and realizes that by SKIPPING 
the highest-density item (Item A), it can perfectly fit Item B (20) and Item C (30) 
into the 50 lb bag, yielding $220!

Rule of Thumb: If a problem has strict physical boundaries that force you to 
leave "wasted space", Greedy will usually fail, and you must use Dynamic Programming.
    """)


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. What are the two properties a problem must have for a Greedy Algorithm to work?
   Answer: 1. Optimal Substructure (an optimal solution to the problem contains optimal solutions to the sub-problems). 2. Greedy Choice Property (a globally optimal solution can be arrived at by selecting a locally optimal choice).

2. In Interval Scheduling, why does sorting by "Earliest Start Time" fail?
   Answer: Imagine Activity A starts at 1:00 PM and ends at 11:00 PM. Activity B starts at 2:00 PM and ends at 3:00 PM. Activity C starts at 4:00 PM and ends at 5:00 PM. If you sort by Start Time, you greedily pick Activity A. But Activity A consumes the entire day! You get 1 total activity. If you sorted by End Time, you would pick Activity B (ends 3:00) and Activity C (ends 5:00), yielding 2 total activities.

3. How does Dijkstra's Algorithm relate to the Greedy paradigm?
   Answer: Dijkstra's Algorithm is a quintessential Greedy Algorithm. It uses a Priority Queue (Min-Heap) to constantly query "What is the absolute shortest node I can step to RIGHT NOW?". It greedily locks in that node's distance. Because all edge weights must be positive, this Greedy Choice is mathematically guaranteed to be correct!
"""

if __name__ == "__main__":
    demonstrate_interval_scheduling()
    explain_knapsack_paradox()
    print("\n[SUCCESS] Laboratory: Greedy Algorithms Completed.")
