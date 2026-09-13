"""
# ==============================================================================
# LABORATORY: ADVANCED APPROXIMATION (GREEDY SET COVER)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Problem: You are the CEO of a telecom company. You need to provide 5G cell 
# service to 10,000 specific houses (The Universe). 
# You have 500 possible locations where you can build a cell tower. Building a 
# tower is extremely expensive. Each tower covers a specific set of houses.
# 
# Goal: Pick the absolute MINIMUM number of cell towers required to cover ALL 
# 10,000 houses.
#
# This is the "Set Cover Problem". It is one of Karp's legendary 21 NP-Complete 
# problems. To find the mathematically perfect minimum, you must check all $2^{500}$ 
# combinations of towers. Your computer will crash.
#
# Solution: The Greedy Approximation Algorithm.
# 1. Look at all available towers.
# 2. Pick the tower that covers the MAXIMUM number of CURRENTLY UNCOVERED houses.
# 3. Mark those houses as covered.
# 4. Repeat until all houses are covered.
#
# Does this guarantee the mathematically perfect answer? No.
# But it provides a strict Mathematical Guarantee! The greedy algorithm is proven 
# to return an answer that is at worst $O(\ln N)$ times larger than the optimal answer, 
# where $N$ is the number of houses. 
# If $N = 10,000$, $\ln(10000) \approx 9.2$. The algorithm guarantees it will 
# never build more than 9.2x the optimal number of towers!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the Set Cover NP-Hard problem.
# - Implement the Greedy Approximation logic using Python `set` operations.
# - Understand the logarithmic $\ln(N)$ approximation bound.
#
# ==============================================================================
"""

import math
from typing import List, Set, Dict, Tuple

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. SET COVER ENGINE (GREEDY APPROXIMATION)
# ==============================================================================
def greedy_set_cover(universe: Set[int], subsets: Dict[str, Set[int]]) -> List[str]:
    """
    Approximates the Set Cover problem in O(K * N) time.
    Returns the names (keys) of the chosen subsets.
    Guaranteed to be within O(ln N) of the optimal number of subsets.
    """
    # Track the elements we still need to cover
    uncovered_elements = universe.copy()
    
    # Track the sets we have chosen
    chosen_sets = []
    
    # We loop until the universe is perfectly covered!
    while uncovered_elements:
        
        best_set_name = None
        best_set_coverage = set()
        
        # 1. EVALUATE ALL AVAILABLE SETS
        for set_name, subset_elements in subsets.items():
            
            # We ONLY care about how many UNCOVERED elements this set hits!
            # Math: Intersection of the Subset and the Uncovered Universe.
            # Python's `set.intersection()` is heavily optimized in C.
            current_coverage = uncovered_elements.intersection(subset_elements)
            
            # If this set covers more new elements than the current best...
            if len(current_coverage) > len(best_set_coverage):
                best_set_coverage = current_coverage
                best_set_name = set_name
                
        # 2. THE GREEDY CHOICE
        # If we failed to find any set that covers new elements, it means the 
        # original subsets provided by the user mathematically CANNOT cover the 
        # entire universe. It is an impossible problem.
        if best_set_name is None:
            raise ValueError("The provided subsets cannot cover the entire universe!")
            
        # Add the best set to our final answer
        chosen_sets.append(best_set_name)
        
        # Mark those elements as COVERED by removing them from the tracking set!
        # Math: Uncovered = Uncovered - BestSet
        uncovered_elements.difference_update(best_set_coverage)
        
    return chosen_sets


def demonstrate_set_cover():
    section_header("Algorithm: Greedy Set Cover (Approximation)")
    
    # Our universe: 15 specific houses we must provide 5G service to.
    universe = set(range(1, 16))
    
    # Available cell towers and the specific houses they can reach
    towers = {
        "Tower A": {1, 2, 3, 4, 5, 6},
        "Tower B": {5, 6, 7, 8, 9},
        "Tower C": {1, 4, 7, 10, 13},
        "Tower D": {10, 11, 12, 13, 14, 15},
        "Tower E": {2, 5, 8, 11, 14},
        "Tower F": {3, 6, 9, 12, 15}
    }
    
    print(f"Universe Size: {len(universe)} houses")
    print(f"Available Towers: {len(towers)}")
    
    print("\nExecuting O(K*N) Greedy Approximation...")
    chosen = greedy_set_cover(universe, towers)
    
    print(f"\nFinal Chosen Towers: {chosen}")
    print(f"Total Towers Built : {len(chosen)}")
    
    print("\nVerification:")
    # Prove that the chosen towers mathematically cover every single house!
    test_cover = set()
    for name in chosen:
        test_cover.update(towers[name])
        
    print(f"Houses Covered: {sorted(list(test_cover))}")
    print(f"Success? {test_cover == universe}")


# ==============================================================================
# 4. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why does a Greedy algorithm not guarantee the exact mathematically perfect answer?
   Answer: Imagine the Universe is houses {1, 2, 3, 4, 5, 6}. 
   Tower A covers {1, 2, 3, 4}.
   Tower B covers {1, 2, 5}.
   Tower C covers {3, 4, 6}.
   The Greedy algorithm will pick Tower A first because it covers the maximum number of houses (4). But to cover the remaining houses {5, 6}, you MUST now pick Tower B and Tower C! Total towers built: 3. 
   If you look closely, Tower B and Tower C mathematically cover all 6 houses by themselves! The optimal answer is 2 towers. The Greedy algorithm trapped itself into a sub-optimal path by picking the biggest tower first.

2. What does the $O(\ln N)$ approximation bound mathematically mean?
   Answer: It means that in the absolute worst-case scenario carefully crafted by an adversarial mathematician to trick the Greedy algorithm, the Greedy algorithm will NEVER build more than $\ln(N)$ times the optimal number of towers. If $N = 1000$ elements, $\ln(1000) \approx 6.9$. If the true optimal answer is 10 towers, the Greedy algorithm is mathematically guaranteed to output an answer $\le 69$ towers. This bound was famously proved by Vasek Chvatal in 1979.

3. Why do we accept Approximation bounds for NP-Hard problems?
   Answer: Because exact algorithms like Branch & Bound or $O(2^N)$ Brute Force physically crash due to time or RAM constraints when $N > 100$. If a telecom company needs to place cell towers across New York City ($N = 8,000,000$), computing the exact optimal answer would take longer than the heat death of the universe. An algorithm that runs in $0.5$ seconds and guarantees an answer within a logarithmic factor of optimal is a massive triumph of modern computer science!
"""

if __name__ == "__main__":
    demonstrate_set_cover()
    print("\n[SUCCESS] Laboratory: Advanced Approximation (Set Cover) Completed.")
    print("\n===============================================================")
    print("🎓 [CURRICULUM COMPLETE] YOU HAVE MASTERED ADVANCED ALGORITHMS!")
    print("===============================================================")
