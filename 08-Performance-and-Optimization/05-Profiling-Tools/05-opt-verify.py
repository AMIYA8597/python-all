"""
# ==============================================================================
# LABORATORY: PERFORMANCE AND OPTIMIZATION (OPTIMIZATION VERIFICATION)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A junior engineer notices a function is slow. They immediately rewrite the 
# entire module, deploying multi-threading, custom caching, and NumPy arrays. 
# The code balloons from 50 lines to 800 lines of highly complex, unreadable 
# architecture. They run it, and it's 2% faster.
#
# A senior engineer understands the "First Rule of Optimization": DO NOT OPTIMIZE 
# WITHOUT MATHEMATICAL VERIFICATION. Before writing a single line of optimization, 
# they write a regression benchmark. They apply one specific change, mathematically 
# prove it generated a >10% speedup, and if it didn't, they immediately revert 
# the change. Optimization is a scientific method, not a guessing game.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master the Scientific Method of Code Optimization.
# - Differentiate between "Premature Optimization" and "Verified Scaling".
# - Build a custom algorithmic benchmarking suite.
#
# ==============================================================================
"""

import timeit
import math
import random

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE BASELINE (THE UNTOUCHED SCRIPT)
# ==============================================================================
# A real-world scenario: We need to filter a massive list of strings, keeping 
# only the ones that contain a specific substring, and then uppercase them.

def process_data_baseline(data: list, target: str) -> list:
    """
    The untouched, naive implementation.
    """
    result = []
    for item in data:
        if target in item:
            result.append(item.upper())
    return result


# ==============================================================================
# 4. HYPOTHESIS 1: LIST COMPREHENSION (THE MICRO-OPTIMIZATION)
# ==============================================================================
def process_data_hypothesis_1(data: list, target: str) -> list:
    """
    Hypothesis: Using a List Comprehension will bypass `append` overhead.
    Expected Impact: Minor (~10-20% speedup).
    """
    return [item.upper() for item in data if target in item]


# ==============================================================================
# 5. HYPOTHESIS 2: GENERATOR PIPELINE (THE MEMORY OPTIMIZATION)
# ==============================================================================
def process_data_hypothesis_2(data: list, target: str):
    """
    Hypothesis: Returning a Generator will completely eliminate the RAM 
    allocation spike, making it exponentially faster if we only need to iterate.
    Expected Impact: Massive memory drop, but execution speed depends on usage.
    """
    return (item.upper() for item in data if target in item)


# ==============================================================================
# 6. THE MATHEMATICAL VERIFICATION ENGINE
# ==============================================================================
def demonstrate_scientific_optimization():
    section_header("The Scientific Method: Optimization Verification")
    
    # 1. Generate the test dataset! (1,000,000 strings)
    N = 1_000_000
    print(f"  [INIT] Generating {N:,} data points...")
    
    # Randomly inject the target string into about 10% of the data
    dataset = []
    target_str = "CRITICAL_ERROR"
    for i in range(N):
        if random.random() < 0.1:
            dataset.append(f"Log_Entry_{i}: {target_str} encountered.")
        else:
            dataset.append(f"Log_Entry_{i}: Normal execution.")
            
    print("\n  [EXECUTING BASELINE (Control Group)]")
    start_base = timeit.default_timer()
    res_base = process_data_baseline(dataset, target_str)
    end_base = timeit.default_timer()
    time_base = end_base - start_base
    print(f"    -> Time: {time_base:.4f} seconds")
    
    print("\n  [EXECUTING HYPOTHESIS 1 (List Comprehension)]")
    start_h1 = timeit.default_timer()
    res_h1 = process_data_hypothesis_1(dataset, target_str)
    end_h1 = timeit.default_timer()
    time_h1 = end_h1 - start_h1
    print(f"    -> Time: {time_h1:.4f} seconds")
    
    speedup_h1 = ((time_base - time_h1) / time_base) * 100
    print(f"    -> Verdict: Achieved a {speedup_h1:.2f}% speedup. (Accepted!)")
    
    print("\n  [EXECUTING HYPOTHESIS 2 (Generator Pipeline)]")
    start_h2 = timeit.default_timer()
    # It executes instantly because it evaluates nothing!
    res_h2 = process_data_hypothesis_2(dataset, target_str)
    end_h2 = timeit.default_timer()
    time_h2_create = end_h2 - start_h2
    
    # But we MUST verify the execution time! (Iterating through it)
    start_h2_eval = timeit.default_timer()
    # Force evaluation by consuming the generator
    list(res_h2)
    end_h2_eval = timeit.default_timer()
    time_h2_eval = end_h2_eval - start_h2_eval
    
    print(f"    -> Creation Time:   {time_h2_create:.6f} seconds (Instant!)")
    print(f"    -> Evaluation Time: {time_h2_eval:.4f} seconds")
    
    speedup_h2 = ((time_base - time_h2_eval) / time_base) * 100
    if speedup_h2 > 0:
        print(f"    -> Verdict: Achieved a {speedup_h2:.2f}% speedup overall. (Accepted!)")
    else:
        print(f"    -> Verdict: Slower by {abs(speedup_h2):.2f}%. Memory saved, but CPU lost. (Context Dependent!)")
        
    print("\n  [INTEGRITY CHECK]")
    print(f"    -> Baseline returned:   {len(res_base)} items.")
    print(f"    -> Hypothesis 1 returned: {len(res_h1)} items.")
    if len(res_base) == len(res_h1):
        print("    -> PASS: Mathematical integrity preserved.")
    else:
        print("    -> FAIL: The optimization corrupted the data!")


def run_all_labs():
    demonstrate_scientific_optimization()


# ==============================================================================
# 7. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "What is 'Premature Optimization', and why is it considered the root of all evil in Software Engineering?"
   Senior Answer: "Premature Optimization (coined by Donald Knuth) is the act of degrading the readability, maintainability, and architectural simplicity of codebase to achieve theoretical performance gains *before* mathematically proving that a bottleneck exists. A junior engineer might spend 3 days rewriting a clean Python configuration parser into C++ to make it run in $1$ millisecond instead of $5$ milliseconds. But the parser only runs exactly once when the application boots! They sacrificed critical codebase maintainability for a $4$ millisecond gain that a human user will mathematically never perceive. Optimization should strictly occur *after* the application is complete, *after* profiling data identifies the true $90\\%$ bottleneck, and *only* if the business requirements demand it."

2. Interviewer: "Why did Hypothesis 2 (The Generator) evaluate instantly during creation, but take significantly longer when we forced it to execute via `list()`?"
   Senior Answer: "Because of 'Lazy Evaluation'. When we called `process_data_hypothesis_2`, Python executed exactly zero string comparisons. It simply allocated a microscopic State Machine (the Generator Object) in RAM that mathematically *knew how* to calculate the data later. The CPU time was effectively $0.000001$ seconds. However, when we wrapped it in `list()`, we aggressively forced the Generator to sequentially evaluate all $1,000,000$ items and violently dump them into a physical array in RAM all at once. If the business logic actually requires all $100,000$ filtered items in memory at the exact same time, a Generator provides zero benefit and actually adds a tiny layer of internal bytecode overhead. Generators are only optimal if the downstream consumer evaluates the data *one at a time*."

3. Interviewer: "What is the critical failure mode of optimization if you do not run an 'Integrity Check' after rewriting the algorithm?"
   Senior Answer: "You can create an algorithm that is infinitely fast, provided it calculates the wrong answer. If you deploy a complex multi-threading or Vectorization optimization to a financial pricing model without building a strict Mathematical Regression Test (the Integrity Check) to compare the optimized output against the naive Baseline output, you risk introducing catastrophic Race Conditions, float precision errors, or dropped data frames. An optimization is completely invalid and highly dangerous until it mathematically proves $100.00\\%$ data parity with the unoptimized, sequential control group."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Profiling (Optimization Verification) Completed.")
