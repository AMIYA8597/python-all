"""
# ==============================================================================
# LABORATORY: TESTING AND DEBUGGING (DEBUGGING STRATEGIES)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A junior developer encounters a bug where their Data Pipeline occasionally 
# outputs the wrong number. They stare at the 5,000 lines of code for 6 hours, 
# trying to mentally hold the entire mathematical state of the program in their 
# head. When they can't figure it out, they randomly change variables, hoping 
# it magically fixes the problem ("Shotgun Debugging"). They make the code worse.
#
# A senior software engineer understands that debugging is an absolute mathematical 
# discipline. They do not stare at the code. They execute "Algorithmic Bisection" 
# (Git Bisect) to find the exact commit that broke the build in O(log N) time. 
# They execute "Divide and Conquer", splitting the data pipeline exactly in half 
# and verifying the state, narrowing down a 5,000-line haystack to a 5-line bug 
# in minutes. They apply rigorous scientific methodology to software failures.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master "Divide and Conquer" (Binary Search) debugging.
# - Execute "Delta Debugging" (Minimizing the Failure Case).
# - Understand the architecture of `git bisect`.
#
# ==============================================================================
"""

import math
from typing import List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE BUSINESS LOGIC (THE DATA PIPELINE)
# ==============================================================================
class DataPipeline:
    """A multi-stage pipeline where a bug is buried deep inside."""
    
    @staticmethod
    def extract_data() -> List[int]:
        # Assume this pulls 1,000 records from an API
        return [i for i in range(1, 1001)]
        
    @staticmethod
    def transform_data(data: List[int]) -> List[int]:
        """Mathematically mutates the data."""
        transformed = []
        for x in data:
            # FATAL BUG: Someone accidentally mutated the formula for exactly ONE number!
            if x == 542:
                transformed.append(x * 0) # The Bug!
            else:
                transformed.append(x * 2)
        return transformed
        
    @staticmethod
    def load_data(data: List[int]) -> int:
        """Calculates the checksum of the pipeline."""
        return sum(data)


# ==============================================================================
# 4. THE DEBUGGING STRATEGY (DIVIDE AND CONQUER)
# ==============================================================================
class StrategyEngine:
    
    @staticmethod
    def debug_via_divide_and_conquer():
        """
        How a Senior Engineer finds a bug in a 1,000-item array.
        Instead of checking item 1, then item 2 (Linear Time O(N)), 
        they cut the array in half mathematically (Logarithmic Time O(log N)).
        """
        print("  [INIT] Executing Divide and Conquer Debugging...")
        
        # 1. We extract the raw data
        raw_data = DataPipeline.extract_data()
        
        # 2. We mathematically know what the sum SHOULD be if the transformation works!
        # If we double numbers 1 to 1000, the sum should be 1,001,000.
        expected_total = sum(x * 2 for x in raw_data)
        
        # 3. We run the buggy pipeline
        transformed = DataPipeline.transform_data(raw_data)
        actual_total = sum(transformed)
        
        if actual_total == expected_total:
            print("  [PASS] Pipeline is flawless.")
            return
            
        print(f"  [ERROR TRAPPED] Expected {expected_total}, Got {actual_total}.")
        print("  [STRATEGY] Commencing Binary Search (O(log N)) to find the corrupted item...")
        
        # THE BINARY SEARCH DEBUGGER
        low = 0
        high = len(raw_data) - 1
        steps = 0
        
        while low <= high:
            steps += 1
            mid = (low + high) // 2
            
            # We test the LEFT half of the array!
            left_slice = raw_data[low:mid+1]
            left_transformed = DataPipeline.transform_data(left_slice)
            
            # What SHOULD the left side equal?
            expected_left = sum(x * 2 for x in left_slice)
            actual_left = sum(left_transformed)
            
            if actual_left != expected_left:
                # The bug is mathematically trapped in the LEFT half!
                # We move our 'high' pointer to ignore the right half completely!
                high = mid
            else:
                # The left side is flawless. The bug MUST be in the RIGHT half!
                low = mid + 1
                
            # If the search space mathematically collapses to 1 item, we found it!
            if low == high:
                broken_item = raw_data[low]
                print(f"    -> [BUG FOUND] In exactly {steps} steps, we isolated the bug.")
                print(f"    -> The anomaly occurs exactly at Number: {broken_item}")
                break


# ==============================================================================
# 5. MATHEMATICAL PROOF (THE SIMULATION)
# ==============================================================================
def demonstrate_strategies():
    section_header("Debugging: Algorithmic Strategies")
    
    StrategyEngine.debug_via_divide_and_conquer()
    
    print("\n  [ARCHITECTURE PROOF]")
    print("  By applying Computer Science theory (Binary Search) to the debugging ")
    print("  process itself, the engineer mathematically located a single broken ")
    print("  item out of 1,000 in just 10 steps (2^10 = 1024), completely eliminating ")
    print("  the need for manual print-statement scanning.")


def run_all_labs():
    demonstrate_strategies()


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "If a massive open-source project like Linux or Django suddenly breaks, and you have no idea which of the last $500$ commits caused the bug, how do you mathematically find the culprit?"
   Senior Answer: "Git Bisect (Algorithmic Bisection). You do not read $500$ commits. You tag the current broken commit as 'bad'. You find an old commit from a month ago that worked, and tag it as 'good'. Git then automatically checks out a commit exactly in the middle (commit $250$). You run your automated test suite. If the tests pass, the bug was introduced in the second half. You tell Git 'good', and it instantly jumps to commit $375$. It executes a perfect Binary Search across the version control history, guaranteeing it will pinpoint the exact line of code that broke the system in exactly $\\log_2(500) \\approx 9$ steps."

2. Interviewer: "What is 'Delta Debugging' (Minimizing the Failure Case), and why is it the first step in solving any complex architectural bug?"
   Senior Answer: "Isolating the Variable. If an API endpoint crashes when processing a $10$ MB JSON payload, you mathematically cannot debug the payload directly. Delta Debugging is the scientific process of halving the payload. You delete the second half of the JSON and re-send it. If it still crashes, you delete half again. You aggressively minimize the input until you have a $3$-line JSON payload that triggers the exact same stack trace. By isolating the failure case to its absolute mathematical minimum, you remove all the noise, exposing the exact data structure that the algorithm fails to handle."

3. Interviewer: "Explain the psychological debugging strategy known as 'Rubber Ducking'."
   Senior Answer: "Cognitive Verbalization. When a developer stares at broken code for hours, their brain begins to read what they *intended* to write, not what they *actually* wrote (Confirmation Bias). 'Rubber Duck Debugging' forces the developer to physically articulate their code line-by-line out loud to an inanimate object (or a coworker). The act of translating visual symbols into vocalized speech forces the brain to process the logic through a different cognitive pathway. As they explain the mathematical constraints out loud, the brain instantly detects the logical discrepancy, causing the developer to solve their own problem without the listener saying a word."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Testing and Debugging (Strategies) Completed.")
