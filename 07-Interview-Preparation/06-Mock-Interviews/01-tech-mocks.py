"""
# ==============================================================================
# LABORATORY: INTERVIEW PREPARATION (MOCK INTERVIEWS - TECHNICAL SIMULATION)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You can know every algorithm in existence, but if you cannot communicate 
# your thoughts while coding under pressure, you will fail the interview.
# FAANG interviewers grade you on 4 pillars: Problem Solving, Coding, 
# Communication, and Verification (Testing).
#
# A junior engineer reads the problem and immediately starts typing code in 
# absolute silence, gets stuck on an edge case, panics, and fails.
#
# A senior engineer uses the 'REACT' methodology:
# - Requirements: Clarify constraints (Empty arrays? Negative numbers?)
# - Explore: Propose 2 solutions (Naive O(N^2), Optimal O(N))
# - Architecture: verbally explain the data structures before typing
# - Code: Type out the solution while narrating the logic
# - Test: Manually dry-run the code with a test case
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master the 'REACT' verbal communication methodology.
# - Master on-the-fly constraint extraction.
# - Master manual dry-run verification.
#
# ==============================================================================
"""

import time
import sys

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")

def simulate_typing(text: str, delay: float = 0.02):
    """Simulates real-time terminal output for interview realism."""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()


# ==============================================================================
# 3. THE REACT METHODOLOGY: A LIVE SIMULATION
# ==============================================================================
def mock_interview_simulation():
    section_header("Live Simulation: The REACT Framework")
    
    simulate_typing("INTERVIEWER: 'Given an array of integers, return the indices of the two numbers that add up to a specific target.'")
    
    simulate_typing("\n[STAGE 1: REQUIREMENTS (Clarifying Constraints)]")
    simulate_typing("CANDIDATE: 'Before I begin, let me clarify a few constraints.'")
    simulate_typing("CANDIDATE: '1. Are the numbers sorted? (No)'")
    simulate_typing("CANDIDATE: '2. Can there be negative numbers? (Yes)'")
    simulate_typing("CANDIDATE: '3. Is there guaranteed to be exactly one solution? (Yes)'")
    simulate_typing("CANDIDATE: '4. Can I use the same element twice? (No)'")
    simulate_typing("INTERVIEWER: 'Correct on all counts. Proceed.'")
    
    simulate_typing("\n[STAGE 2: EXPLORE (Propose Solutions)]")
    simulate_typing("CANDIDATE: 'The brute-force approach would be to use two nested loops, checking every pair. This takes O(N^2) Time and O(1) Space. That's too slow.'")
    simulate_typing("CANDIDATE: 'To optimize the Time Complexity, we can sacrifice Space Complexity. We can use a Hash Map.'")
    
    simulate_typing("\n[STAGE 3: ARCHITECTURE (Verbalize the Design)]")
    simulate_typing("CANDIDATE: 'As I iterate through the array, I will mathematically calculate the complement needed (`target - current_num`).'")
    simulate_typing("CANDIDATE: 'I will check if this complement exists in the Hash Map in O(1) time.'")
    simulate_typing("CANDIDATE: 'If it doesn't, I will store the `current_num` and its `index` in the map for future numbers to use.'")
    simulate_typing("INTERVIEWER: 'That sounds optimal. O(N) Time and Space. Please code it.'")
    
    simulate_typing("\n[STAGE 4: CODE (Narrated Typing)]")
    
    # --------------------------------------------------------------------------
    # CANDIDATE'S CODE
    # --------------------------------------------------------------------------
    def two_sum(nums, target):
        # "I am initializing the Hash Map to map Values to Indices."
        seen = {}
        
        # "Iterating over the array using enumerate to capture the index."
        for i, num in enumerate(nums):
            # "Calculating the mathematical complement."
            complement = target - num
            
            # "O(1) lookup check."
            if complement in seen:
                # "Match found! Returning the cached index and the current index."
                return [seen[complement], i]
                
            # "Caching the current number for future iterations."
            seen[num] = i
            
        return []
    # --------------------------------------------------------------------------
    
    simulate_typing("CANDIDATE: 'The code is written. Before you run it, I will manually dry-run it to ensure it is flawless.'")
    
    simulate_typing("\n[STAGE 5: TEST (Manual Dry Run)]")
    simulate_typing("CANDIDATE: 'Let's trace: nums = [3, 2, 4], target = 6'")
    simulate_typing("CANDIDATE: 'i=0, num=3. Complement = 6 - 3 = 3. `seen` is empty. Adding {3: 0}.'")
    simulate_typing("CANDIDATE: 'i=1, num=2. Complement = 6 - 2 = 4. 4 is not in `seen`. Adding {2: 1}.'")
    simulate_typing("CANDIDATE: 'i=2, num=4. Complement = 6 - 4 = 2. 2 IS in `seen`! It maps to index 1.'")
    simulate_typing("CANDIDATE: 'Returning [1, 2]. The logic is perfectly sound.'")
    
    simulate_typing("\nINTERVIEWER: 'Excellent execution. You're hired.'")


# ==============================================================================
# 4. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "During the Requirements phase, why is it critical to explicitly ask about negative numbers or data types, even if the problem seems obvious?"
   Senior Answer: "Technical questions are deliberately vague. If a candidate assumes all numbers are positive, they might incorrectly attempt to optimize a Sliding Window problem or prune a DFS search based on a false 'monotonic growth' assumption. If negative numbers exist, those optimizations mathematically break, and the code fails. Asking constraint questions proves to the interviewer that you possess Senior-level defensive engineering instincts, anticipating Edge Cases before a single line of code is written."

2. Interviewer: "Why should you explicitly state the Brute-Force solution first, instead of just immediately typing out the optimal O(N) solution?"
   Senior Answer: "Stating the Brute-Force solution takes 10 seconds and guarantees that you receive baseline 'Problem Solving' points from the interviewer. It demonstrates that you understand the raw mechanics of the problem. More importantly, it establishes a theoretical baseline (e.g., $O(N^2)$), allowing you to mathematically justify *why* your optimal solution ($O(N)$ Hash Map) is superior. If you immediately type the optimal solution, the interviewer might think you just memorized the problem from LeetCode, removing your opportunity to showcase algorithmic reasoning."

3. Interviewer: "During the Testing phase, why must you dry-run the code manually instead of just clicking 'Run' or relying on the compiler?"
   Senior Answer: "In a real FAANG whiteboard interview, or in platforms like Google Docs, there is no compiler! The interviewer is grading your ability to execute code in your own brain. If you find a bug during your manual dry-run and fix it, it is considered a massive positive signal (Self-Correction). If you confidently say 'I'm done', click Run, and it crashes with an `IndexError`, it proves you do not possess internal verification skills, severely damaging your score."
"""

if __name__ == "__main__":
    mock_interview_simulation()
    print("\n[SUCCESS] Laboratory: Mock Interviews (Technical Simulation) Completed.")
