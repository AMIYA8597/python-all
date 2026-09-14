"""
# ==============================================================================
# LABORATORY: COMPETITIVE PROGRAMMING (CODEFORCES DIV-2)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Codeforces Division 2 introduces extreme algorithmic pressure.
# You will frequently encounter problems that say: 
# "Find the MAXIMUM possible minimum distance between cows in a barn."
# 
# You cannot mathematically calculate the answer directly. The search space 
# is $10^9$. If you loop through $10^9$ possibilities, you get a Time Limit 
# Exceeded (TLE) crash.
#
# But wait! If the distance 'D' is valid, then 'D-1' is mathematically 
# guaranteed to be valid. If 'D' is invalid, then 'D+1' is mathematically 
# guaranteed to be invalid! The search space is MONOTONIC (True, True, False, False).
#
# Because it is Monotonic, you can perform a Binary Search ON THE ANSWER ITSELF!
# This radically drops a 1-Billion operations loop down to exactly 30 operations,
# solving "impossible" optimization problems in $O(N \log (\text{Range}))$.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master Binary Search on Answer (Optimization Problems).
# - Master Prefix Sums for $O(1)$ Range Queries.
#
# ==============================================================================
"""

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. BINARY SEARCH ON ANSWER (AGGRESSIVE COWS)
# ==============================================================================
def is_valid_distance(stalls: list[int], cows: int, min_dist: int) -> bool:
    """
    Given a proposed minimum distance `min_dist`, can we successfully place 
    all `cows` in the stalls such that NO two cows are closer than `min_dist`?
    Time Complexity: O(N)
    """
    # Place the very first cow in the absolute first stall! (Greedy optimal choice)
    cows_placed = 1
    last_position = stalls[0]
    
    for i in range(1, len(stalls)):
        # If the gap between the current stall and the last placed cow 
        # is greater than or equal to our required `min_dist`...
        if stalls[i] - last_position >= min_dist:
            # We can safely place a cow here!
            cows_placed += 1
            last_position = stalls[i]
            
            # Did we successfully place all cows?
            if cows_placed == cows:
                return True
                
    # We ran out of stalls before we could place all cows. The distance is too strict!
    return False

def max_minimum_distance(stalls: list[int], cows: int) -> int:
    """
    Finds the MAXIMUM possible minimum distance between cows.
    Time Complexity: O(N log(Max_Distance))
    """
    # 1. We MUST sort the stalls first!
    stalls.sort()
    
    # 2. Define the Search Space boundaries
    # The absolute smallest possible distance is 1 (if stalls are at 1 and 2).
    # The absolute largest possible distance is the gap between the first and last stall.
    low = 1
    high = stalls[-1] - stalls[0]
    
    best_ans = 0
    
    # 3. Binary Search ON THE ANSWER
    while low <= high:
        mid = (low + high) // 2
        
        # O(N) check: Is `mid` a mathematically valid distance?
        if is_valid_distance(stalls, cows, mid):
            # It IS valid! But can we push for a LARGER distance?
            # Save this answer, and aggressively search the UPPER half!
            best_ans = mid
            low = mid + 1
        else:
            # It is INVALID! We were too greedy. The distance is impossible.
            # We must search the LOWER half to find a more forgiving distance!
            high = mid - 1
            
    return best_ans

def demonstrate_binary_search_answer():
    section_header("Binary Search on Answer")
    
    stalls = [1, 2, 8, 4, 9]
    cows = 3
    print(f"Stall Locations: {stalls}")
    print(f"Number of Cows to place: {cows}")
    
    ans = max_minimum_distance(stalls, cows)
    
    print(f"\nAbsolute Maximum Minimum Distance: {ans}")
    print("Why? Sort the stalls: [1, 2, 4, 8, 9]")
    print("Place cows at 1, 4, and 8. The gaps are (4-1)=3 and (8-4)=4.")
    print("The minimum gap is 3. If you try to force a gap of 4, you can only fit 2 cows!")


# ==============================================================================
# 4. PREFIX SUMS (O(1) RANGE QUERIES)
# ==============================================================================
def prefix_sum_queries(arr: list[int], queries: list[tuple[int, int]]) -> list[int]:
    """
    Problem: You are given an array of 100,000 numbers.
    You are given 100,000 queries. Each query says: "Find the sum from index L to R".
    
    A naive loop takes O(N) per query -> O(N * Q) = 10 Billion operations (TLE).
    Prefix Sums answers EACH query in exactly O(1) time!
    """
    n = len(arr)
    
    # 1. Build the Prefix Sum array (1-indexed to mathematically avoid L-1 out of bounds)
    # prefix[i] will store the sum of the first `i` elements!
    prefix = [0] * (n + 1)
    
    for i in range(n):
        prefix[i + 1] = prefix[i] + arr[i]
        
    results = []
    
    # 2. O(1) Queries
    for L, R in queries:
        # Sum from L to R is mathematically: Sum(0 to R) - Sum(0 to L-1)
        # Because our prefix array is 1-indexed, we use: prefix[R + 1] - prefix[L]
        range_sum = prefix[R + 1] - prefix[L]
        results.append(range_sum)
        
    return results

def demonstrate_prefix_sums():
    section_header("Prefix Sums (O(1) Queries)")
    
    arr = [2, 4, 6, 8, 10]
    queries = [(0, 2), (1, 4), (3, 3)]
    
    print(f"Array: {arr}")
    print(f"Queries (L, R): {queries}")
    
    ans = prefix_sum_queries(arr, queries)
    
    print(f"\nQuery Results: {ans}")
    print("Query (0, 2) -> 2+4+6 = 12")
    print("Query (1, 4) -> 4+6+8+10 = 28")
    print("The sums were calculated instantly in O(1) time without looping!")


def run_all_labs():
    demonstrate_binary_search_answer()
    demonstrate_prefix_sums()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. What mathematical property MUST be true about a search space before you can use Binary Search on the Answer?
   Answer: The search space MUST be Monotonic. This means the validity of the answers must form a strict, unbroken sequence of `[True, True, True, False, False, False]` or `[False, False, False, True, True]`. If the search space is chaotic `[True, False, True]`, you cannot use Binary Search. In the Aggressive Cows problem, if a distance of 4 is valid, then 3, 2, and 1 are mathematically guaranteed to be valid. If 5 is impossible, then 6, 7, and 8 are mathematically guaranteed to be impossible. Because of this strict threshold, Binary Search can cleanly cut the search space in half at every step!

2. In the `is_valid_distance` function, why is placing the first cow in the absolute first stall (`stalls[0]`) mathematically the correct choice? Could placing it in the second stall ever be better?
   Answer: It is a Greedy mathematical proof! Our goal is to maximize the distance between cows. The absolute furthest you can stretch a set of cows is by maximizing the total span of the array. If you place the first cow in `stalls[1]` instead of `stalls[0]`, you have literally voluntarily surrendered the physical space between stall 0 and stall 1. You have shrunk your available real estate. It is mathematically impossible for shrinking the available real estate to yield a *larger* gap between cows. Therefore, aggressively locking the first cow to the leftmost boundary is always the optimal first move.

3. In the Prefix Sum array construction, why is the array padded with a leading zero (`prefix = [0] * (n + 1)`)?
   Answer: Boundary protection! The formula for a range sum is $Prefix[R] - Prefix[L-1]$. What happens if a query asks for the sum starting from the absolute beginning of the array ($L = 0$)? The formula evaluates $Prefix[0 - 1]$, which translates to $Prefix[-1]$. In Python, index $-1$ wraps around to the back of the array, completely corrupting the math! In C++, it causes a Segmentation Fault. By creating a 1-indexed Prefix Array initialized with a leading $0$, the query becomes $Prefix[R+1] - Prefix[L]$. If $L = 0$, it subtracts $Prefix[0]$, which is exactly $0$. It flawlessly protects the lower boundary without requiring messy `if L == 0:` statements!
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Codeforces Div-2 Completed.")
