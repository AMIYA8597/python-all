"""
## A. Concept Name
Activity Selection Problem

## B. Intuition and Core Logic
The Activity Selection Problem is an optimization problem where we need to select the maximum number of non-overlapping activities. The greedy strategy works perfectly here: if we always pick the activity that finishes earliest (and doesn't overlap with the already selected activities), it leaves the maximum possible time for remaining activities.

## C. Time and Space Complexity
- Time Complexity: O(N log N) if the activities are not sorted by their finish times, where N is the number of activities. If already sorted, it takes O(N) time.
- Space Complexity: O(N) to store the result, or O(1) if we just print/count.

## D. Implementation Details
1. Sort the activities based on their finish times.
2. Select the first activity from the sorted list.
3. For all remaining activities, if the start time of the activity is greater than or equal to the finish time of the previously selected activity, select it.

## X. Project Connection
This greedy algorithm is frequently used in scheduling systems, resource allocation, and time-management modules where maximizing the utilization of a single resource (like a meeting room, CPU, or a person's time) is critical.
"""

def get_max_activities(activities):
    """
    activities: A list of tuples, where each tuple represents an activity as (start_time, finish_time).
    Returns a list of the maximum number of non-overlapping activities.
    """
    if not activities:
        return []

    # Sort activities by finish time
    sorted_activities = sorted(activities, key=lambda x: x[1])
    
    selected = [sorted_activities[0]]
    last_finish_time = sorted_activities[0][1]
    
    for i in range(1, len(sorted_activities)):
        # If this activity starts after or when the last selected activity finished
        if sorted_activities[i][0] >= last_finish_time:
            selected.append(sorted_activities[i])
            last_finish_time = sorted_activities[i][1]
            
    return selected

if __name__ == '__main__':
    # Example: Unsorted activities
    # (start, finish)
    activities = [
        (1, 2), 
        (3, 4), 
        (0, 6), 
        (5, 7), 
        (8, 9), 
        (5, 9)
    ]
    selected_acts = get_max_activities(activities)
    print(f"Maximum number of activities: {len(selected_acts)}")
    print("Selected activities:", selected_acts)
