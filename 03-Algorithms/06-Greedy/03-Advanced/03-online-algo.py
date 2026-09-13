"""
# ==============================================================================
# LABORATORY: ONLINE ALGORITHMS & COMPETITIVE ANALYSIS
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Thus far, every Greedy Algorithm we have written starts with a magic trick: 
# `array.sort()`. 
# We look at ALL the data, sort it, and make perfect decisions. This is called 
# an "Offline Algorithm".
#
# But in the real world (Stock Markets, Server Caches, Matchmaking apps), you 
# DO NOT HAVE the future data! 
# Data arrives sequentially in real-time. You must make an irrevocable Greedy 
# decision RIGHT NOW. This is called an "Online Algorithm".
#
# Classic Problem: The Secretary Problem (Optimal Stopping Theory)
# You are interviewing 100 candidates for a job. They arrive one by one. 
# After each interview, you must instantly hire them or reject them forever. 
# You cannot go back to a rejected candidate. 
# How do you maximize your probability of hiring the absolute BEST candidate?
#
# If you hire the first one, they might be terrible. If you wait until the 99th, 
# the best one probably already passed by!
#
# Mathematics provides a stunning answer: The "37% Rule" (1/e).
# You unconditionally REJECT the first 37% of candidates, using them purely as 
# a "Baseline". Then, you immediately hire the FIRST candidate who is better 
# than the absolute best person in your baseline!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Differentiate between Online and Offline Algorithms.
# - Understand Competitive Ratios.
# - Implement the 1/e Optimal Stopping Strategy.
#
# ==============================================================================
"""

import math
import random
from typing import List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. OPTIMAL STOPPING (THE SECRETARY PROBLEM)
# ==============================================================================
def simulate_secretary_problem(candidates: List[int]) -> int:
    """
    Candidates is a list of "scores" representing how good a candidate is.
    We receive them sequentially. We cannot sort them!
    Returns the score of the candidate we hired.
    """
    n = len(candidates)
    
    # 1. CALCULATE THE MATHEMATICAL THRESHOLD (1/e)
    # Euler's number (e) is approx 2.718. 
    # 1 / 2.718 is approximately 0.368 (36.8%).
    # We must reject the first 37% of candidates unconditionally.
    reject_threshold = int(n / math.e)
    
    if reject_threshold == 0:
        return candidates[0]
        
    print(f"Total Candidates: {n}")
    print(f"Strategy: Reject the first {reject_threshold} candidates to form a baseline.")
    
    # 2. THE BASELINE PHASE
    best_in_baseline = -1
    for i in range(reject_threshold):
        if candidates[i] > best_in_baseline:
            best_in_baseline = candidates[i]
            
    print(f"Baseline Phase Complete. Best baseline score seen: {best_in_baseline}")
    
    # 3. THE ONLINE SELECTION PHASE
    # Now we continue interviewing. The MOMENT we see someone better than the 
    # baseline, we greedily hire them on the spot!
    for i in range(reject_threshold, n):
        if candidates[i] > best_in_baseline:
            print(f"-> Hired Candidate {i+1} with score {candidates[i]}!")
            return candidates[i]
            
    # If we reach the absolute end of the list and no one beat the baseline, 
    # we are mathematically forced to hire the very last candidate.
    print(f"-> Nobody beat the baseline. Forced to hire the final candidate.")
    return candidates[-1]


def demonstrate_online_algorithms():
    section_header("Algorithm: Online Secretary Problem (37% Rule)")
    
    # Create 100 random candidates with scores between 1 and 1000.
    random.seed(42) # For reproducible results
    candidates = random.sample(range(1, 1001), 100)
    
    # Let's see what an OFFLINE algorithm would do (it can see the future).
    offline_best = max(candidates)
    print(f"Offline Optimal (God Mode): {offline_best}")
    
    # Now let's run our Online Greedy algorithm!
    print("\nExecuting Online Algorithm...")
    hired_score = simulate_secretary_problem(candidates)
    
    print(f"\nResult Summary:")
    print(f"Hired Score: {hired_score}")
    print(f"Absolute Best Existed: {offline_best}")
    
    # Competitive Ratio
    print("\nCompetitive Ratio:")
    print("In Online Algorithms, we measure performance by comparing our result ")
    print("against the 'Offline God Mode' result. ")
    print("Mathematical theory proves that using the 37% rule guarantees we will ")
    print("hire the absolute best candidate exactly ~37% of the time, which is ")
    print("an impossibly good ratio for completely blind sequential data!")


# ==============================================================================
# 4. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. What is the fundamental difference between an Online and Offline algorithm?
   Answer: An Offline algorithm receives the entire dataset in advance, allowing it to sort, build DP tables, and analyze the global structure before making a single decision. An Online algorithm receives data sequentially (like a streaming API) and must make irrevocable decisions at each step without knowing what data will arrive next.

2. What is a "Competitive Ratio"?
   Answer: It is the mathematical metric used to grade Online algorithms. It is defined as: `Score of Online Algorithm / Score of Optimal Offline Algorithm`. An online algorithm is "$C$-competitive" if its score is always within a factor of $C$ of the optimal offline solution. 

3. How does this apply to CPU Caching (LRU Cache)?
   Answer: An operating system deciding which memory page to evict from RAM is an Online Algorithm! It doesn't know what programs the user will open next. The "Offline Optimal" algorithm is Bélády's Algorithm (evict the page that will be needed furthest in the future). Since the OS can't see the future, it uses the LRU (Least Recently Used) heuristic. LRU is proven to have a competitive ratio bound against Bélády's, making it a mathematically sound Online Approximation!
"""

if __name__ == "__main__":
    demonstrate_online_algorithms()
    print("\n[SUCCESS] Laboratory: Online Algorithms Completed.")
