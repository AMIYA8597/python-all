"""
# ==============================================================================
# LABORATORY: TESTING AND DEBUGGING (PERFORMANCE DEBUGGING)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A junior developer writes a web scraper that processes 10,000 URLs. The script 
# takes 45 minutes to execute. They have no idea why it's slow. They guess that 
# the `BeautifulSoup` HTML parser is the bottleneck, so they spend 3 days rewriting 
# the parsing logic using complex Regex. The script still takes 45 minutes to run. 
# They wasted 3 days optimizing the wrong thing because they guessed instead of 
# measuring.
#
# A senior software engineer uses `cProfile`. They execute the script through 
# the C-level Profiler. The Profiler mathematically logs every single function 
# call and records the exact microsecond execution time. The Profiler outputs a 
# report proving that `BeautifulSoup` took 2 seconds, but `requests.get()` took 
# 44.9 minutes. The engineer realizes the bottleneck is Network I/O, not CPU Parsing. 
# They switch to `aiohttp` (AsyncIO), and the script execution time violently 
# collapses to 45 seconds.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master Deterministic Profiling using `cProfile`.
# - Execute statistical analysis of call stacks via `pstats`.
# - Architect algorithmic bottlenecks identification (CPU-bound vs I/O-bound).
#
# ==============================================================================
"""

import time
import cProfile
import pstats
import io

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE BUSINESS LOGIC (THE BOTTLENECKS)
# ==============================================================================
class DataProcessor:
    
    @staticmethod
    def simulate_network_io():
        """Simulates an extremely slow HTTP API request (I/O Bound)."""
        time.sleep(0.5) # The CPU does NOTHING here. It just waits.
        return "200 OK"
        
    @staticmethod
    def simulate_cpu_parsing():
        """Simulates heavy mathematical number crunching (CPU Bound)."""
        total = 0
        for i in range(1_000_000):
            total += (i * i) # The CPU is running at 100% capacity!
        return total
        
    @staticmethod
    def run_pipeline():
        """The main orchestration function."""
        # 1. We make 3 slow network calls
        for _ in range(3):
            DataProcessor.simulate_network_io()
            
        # 2. We do 1 massive CPU parsing job
        DataProcessor.simulate_cpu_parsing()


# ==============================================================================
# 4. THE PROFILING ARCHITECTURE (cProfile)
# ==============================================================================
class ProfilerEngine:
    
    @staticmethod
    def execute_with_profiling():
        print("  [INIT] Booting cProfile Engine...")
        
        # We instantiate the absolute C-level Profiler
        profiler = cProfile.Profile()
        
        # We mathematically enable the profiler, run the logic, and disable it!
        profiler.enable()
        DataProcessor.run_pipeline()
        profiler.disable()
        
        # --- STATISTICAL ANALYSIS ---
        print("\n  [ANALYSIS] Generating Call Stack Statistics...")
        
        # We route the output to a string buffer instead of printing immediately
        string_io = io.StringIO()
        
        # We load the raw binary profiling data into `pstats` for analysis!
        stats = pstats.Stats(profiler, stream=string_io)
        
        # We mathematically sort the functions by CUMULATIVE TIME.
        # This tells us which functions consumed the absolute most time!
        stats.sort_stats(pstats.SortKey.CUMULATIVE)
        
        # We only print the top 10 worst offenders
        stats.print_stats(10)
        
        print(string_io.getvalue())


# ==============================================================================
# 5. MATHEMATICAL PROOF (THE SIMULATION)
# ==============================================================================
def demonstrate_profiling():
    section_header("Debugging: Performance Profiling (cProfile)")
    
    ProfilerEngine.execute_with_profiling()
    
    print("  [ARCHITECTURE PROOF]")
    print("  Look at the table above. It proves exactly where the time was spent:")
    print("  - `tottime` is the time spent inside the function EXCLUDING sub-calls.")
    print("  - `cumtime` is the total time spent inside the function AND all its sub-calls.")
    print("  By sorting by `cumtime`, we mathematically prove that `time.sleep` (Network I/O) ")
    print("  was the true bottleneck, preventing us from wasting days optimizing the CPU logic.")


def run_all_labs():
    demonstrate_profiling()


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "Why must we use `cProfile` instead of the standard `profile` module that comes built into Python?"
   Senior Answer: "Interpreter Overhead. The standard `profile` module is written in pure Python. If you use it to profile a highly recursive function (e.g., $100,000$ function calls), the pure Python profiler introduces so much execution overhead that it mathematically distorts the timing data. A function that takes $1$ millisecond might look like it took $50$ milliseconds purely because the profiler was so slow. `cProfile` is a C-extension. It executes at raw bare-metal speeds, imposing virtually zero execution overhead, guaranteeing that the mathematical timing metrics are statistically valid."

2. Interviewer: "In the `pstats` output, what is the architectural difference between `tottime` and `cumtime`?"
   Senior Answer: "Local vs Deep Execution. `tottime` (Total Time) measures ONLY the time spent executing the exact bytecode inside that specific function. If function A calls function B, the time spent inside B is mathematically excluded from A's `tottime`. `cumtime` (Cumulative Time) includes everything. If `cumtime` is massive, but `tottime` is near zero, it proves that the function itself is blazing fast, but it is calling a highly inefficient sub-function (like a slow database query). This distinction prevents developers from attempting to optimize a 'fast' parent function."

3. Interviewer: "If `cProfile` proves that a function is completely CPU-bound (e.g., a massive `for` loop executing mathematical operations), what are the architectural solutions in Python?"
   Senior Answer: "Bypassing the CPython Interpreter. Standard Python bytecode is mathematically incapable of achieving high-performance CPU speeds. You have three primary architectural exits. $1$) Vectorization: Rewrite the loop using `NumPy` C-arrays. $2$) Just-In-Time Compilation: Inject the `@njit` decorator from `Numba` to compile the function into LLVM Machine Code at runtime. $3$) C-Extensions: Rewrite the specific bottleneck function in pure `Cython`, C, or Rust, and import it back into Python as a binary module. You never rewrite the entire application; you only C-compile the exact function that `cProfile` identified as the bottleneck."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Testing and Debugging (Performance Debugging) Completed.")
