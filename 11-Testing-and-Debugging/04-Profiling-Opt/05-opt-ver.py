"""
# ==============================================================================
# LABORATORY: PROFILING & OPTIMIZATION (VERIFICATION OF OPTIMIZATION)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A junior developer notices a Financial Calculation takes 20 seconds. They 
# rewrite the algorithm using advanced Bitwise math and NumPy arrays. It now 
# runs in 0.5 seconds! They deploy to Production. The next day, the company 
# loses $50,000 because the "optimized" math rounded floating points incorrectly 
# under specific edge cases. The developer optimized the code, but broke the logic.
#
# A senior software engineer follows the absolute mathematical rule: "Make it work. 
# Make it right. Make it fast." Before optimizing a slow algorithm, they write 
# an exhaustive, parameterized Unit Test suite (The Oracle). They then rewrite 
# the algorithm. Finally, they run the Optimized Code against the Slow Code. 
# If the mathematical outputs of the Fast Algorithm do not perfectly match the 
# Slow Algorithm across 100,000 edge cases, the optimization is violently rejected.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master Optimization Verification (The Oracle Pattern).
# - Execute algorithmic regression testing.
# - Architect safety guardrails for aggressive optimization.
#
# ==============================================================================
"""

import time
import random

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE BUSINESS LOGIC (THE ALGORITHMS)
# ==============================================================================
class MathematicalAlgorithms:
    
    @staticmethod
    def calculate_unique_sum_slow(data: list) -> int:
        """
        The baseline algorithm. It is O(N^2) and extremely slow.
        HOWEVER, we mathematically trust that it is 100% accurate.
        This is our "Test Oracle".
        """
        unique_numbers = []
        for x in data:
            if x not in unique_numbers: # O(N) lookup inside an O(N) loop!
                unique_numbers.append(x)
        return sum(unique_numbers)

    @staticmethod
    def calculate_unique_sum_fast(data: list) -> int:
        """
        The "Optimized" algorithm. It uses a Hash Set for O(1) lookups.
        But wait! A junior developer accidentally wrote a bug in here!
        (They forgot to handle negative numbers in their 'custom' logic).
        """
        unique_set = set()
        total = 0
        for x in data:
            # THE BUG: The 'optimization' accidentally skips negative numbers!
            if x >= 0 and x not in unique_set: 
                unique_set.add(x)
                total += x
        return total


# ==============================================================================
# 4. THE VERIFICATION ARCHITECTURE (THE ORACLE)
# ==============================================================================
class VerificationEngine:
    
    @staticmethod
    def run_regression_suite():
        print("  [INIT] Booting Regression Verification Engine...")
        
        # We generate 1,000 random test cases to bombard both algorithms!
        print("  [EXECUTION] Bombarding both algorithms with random permutations...")
        
        test_cases_passed = 0
        test_cases_failed = 0
        
        for i in range(1, 1001):
            # Generate a random list of integers (including negatives!)
            random_data = [random.randint(-50, 50) for _ in range(100)]
            
            # 1. Execute the Slow (Trusted) Code
            trusted_result = MathematicalAlgorithms.calculate_unique_sum_slow(random_data)
            
            # 2. Execute the Fast (Untrusted) Code
            fast_result = MathematicalAlgorithms.calculate_unique_sum_fast(random_data)
            
            # 3. THE MATHEMATICAL ASSERTION
            if trusted_result != fast_result:
                test_cases_failed += 1
                if test_cases_failed == 1:
                    print(f"\n  [FATAL ERROR TRAPPED] Optimization Regression Detected!")
                    print(f"  -> Input Data: {random_data[:5]}... (truncated)")
                    print(f"  -> Trusted Output: {trusted_result}")
                    print(f"  -> Optimized Output: {fast_result}")
            else:
                test_cases_passed += 1
                
        print(f"\n  [VERIFICATION REPORT]")
        print(f"  -> Passed: {test_cases_passed}")
        print(f"  -> Failed: {test_cases_failed}")
        
        if test_cases_failed > 0:
            print("  -> [REJECTED] The optimization broke the business logic. Merge blocked.")


# ==============================================================================
# 5. MATHEMATICAL PROOF (THE SIMULATION)
# ==============================================================================
def demonstrate_verification():
    section_header("Profiling & Optimization: The Test Oracle")
    
    VerificationEngine.run_regression_suite()
    
    print("\n  [ARCHITECTURE PROOF]")
    print("  The junior developer thought they optimized the algorithm. If they had ")
    print("  relied only on `cProfile`, they would have deployed broken math to ")
    print("  production. By utilizing the 'Slow Code' as a Test Oracle, we mathematically ")
    print("  proved the 'Fast Code' was corrupt, saving the system from a fatal bug.")


def run_all_labs():
    demonstrate_verification()


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "What is a 'Test Oracle' in the context of Algorithm Optimization?"
   Senior Answer: "The Absolute Source of Truth. When you rewrite a complex algorithm (e.g., rewriting a Python parser in C++ for speed), you must verify the new C++ code is mathematically flawless. The 'Test Oracle' is the original, un-optimized, slow Python code. You do not manually write assertions. You write a script that generates $1,000,000$ randomized inputs, feeds them into both the Slow Code and the Fast Code simultaneously, and asserts that `slow_output == fast_output`. The slow code becomes the automatic, mathematically perfect judge of the fast code's correctness."

2. Interviewer: "Why does Donald Knuth famously state that 'Premature optimization is the root of all evil'?"
   Senior Answer: "Architectural Complexity vs ROI. When developers optimize code, they usually introduce advanced caching, bitwise math, or complex concurrency. These patterns mathematically destroy code readability and drastically increase the probability of logical bugs. If a developer optimizes a function that only accounts for $0.01\\%$ of the application's execution time, they have introduced massive architectural complexity for zero Return on Investment. You must *first* write clean, slow, readable code. You only optimize *after* a Profiler mathematically proves a specific function is a bottleneck."

3. Interviewer: "When optimizing floating-point math for performance, why might the Test Oracle reject the fast algorithm even if the logic seems flawless?"
   Senior Answer: "IEEE 754 Non-Associativity. Standard mathematical addition is associative: $(a + b) + c = a + (b + c)$. However, due to floating-point precision limits (IEEE 754), this is mathematically false in computer science. If the 'Slow Code' sums a list of $10,000$ floats linearly, and the 'Fast Code' uses Multiprocessing to sum chunks of the list in parallel and combine them, the order of addition is mutated. The Fast Code will output a number that is $0.00000000001$ different from the Slow Code. The strict `assert slow == fast` will violently fail. The architect must use `math.isclose()` to account for mathematically inevitable floating-point drift caused by optimization."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Profiling & Optimization (Verification) Completed.")
