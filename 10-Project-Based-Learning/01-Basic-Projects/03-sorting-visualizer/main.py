"""
# ==============================================================================
# LABORATORY: PROJECT-BASED LEARNING (ALGORITHM VISUALIZER)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A junior computer science student tries to understand how "Bubble Sort" actually 
# moves data. They write `print(array)` inside the nested loops. The terminal 
# floods with 10,000 lines of unreadable numbers. They learn nothing.
#
# A senior algorithm architect builds a "Sorting Visualizer". They mathematically 
# decouple the Sorting Algorithm from the User Interface using Python Generators 
# (`yield`). Every time the algorithm swaps two numbers, it yields the exact 
# array state back to a Matplotlib or Pygame frontend. The developer watches 
# in real-time as the bars physically rearrange themselves on screen, proving 
# the O(N^2) mathematical inefficiency of Bubble Sort visually.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master Generator Functions (`yield`) for algorithmic state suspension.
# - Execute classic Sorting Algorithms (Bubble Sort, Insertion Sort).
# - Understand Big-O Notation through state mutation tracking.
#
# ==============================================================================
"""

import random
import time

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE GENERATOR ARCHITECTURE (THE ALGORITHMS)
# ==============================================================================
# We do NOT use `return`! If we `return`, the algorithm finishes instantly.
# We use `yield` to mathematically freeze the algorithm in time, hand the array 
# state to the UI, and then resume exactly where we left off!

def bubble_sort_generator(arr: list):
    """
    Bubble Sort: O(N^2) Time Complexity.
    Mathematically compares adjacent elements and swaps them if they are in the wrong order.
    The largest elements "bubble" to the end of the array.
    """
    n = len(arr)
    for i in range(n):
        swapped = False
        # The last `i` elements are mathematically guaranteed to be sorted already!
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                # Pythonic Tuple Unpacking for the Swap!
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
                # FREEZE! Yield the current array state and the indices we just touched!
                yield arr, [j, j + 1]
                
        if not swapped:
            # Mathematical optimization: If no swaps occurred in a full pass, 
            # the array is already perfectly sorted. We can terminate early!
            break


def insertion_sort_generator(arr: list):
    """
    Insertion Sort: O(N^2) Time Complexity (but O(N) for nearly sorted data).
    Mathematically builds the final sorted array one item at a time by 
    sliding elements down until they find their perfect position.
    """
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
            # FREEZE! Yield state during the slide!
            yield arr, [j + 1, i]
            
        arr[j + 1] = key
        # FREEZE! Yield state after final insertion!
        yield arr, [j + 1, i]


# ==============================================================================
# 4. THE VISUALIZATION ENGINE (THE UI SIMULATOR)
# ==============================================================================
def visualize_algorithm(algo_name: str, generator, array_size: int = 15):
    """
    Simulates a GUI frontend (like Pygame or Matplotlib) in the Terminal.
    It mathematically maps the integer values to ASCII bar charts.
    """
    section_header(f"Algorithm Visualizer: {algo_name}")
    
    print("  [INIT] Generating chaotic mathematical array...")
    arr = [random.randint(1, 20) for _ in range(array_size)]
    
    print(f"  [START STATE] {arr}\n")
    
    # We iterate over the Generator! The algorithm gives us control back every Swap!
    swap_count = 0
    for current_arr, active_indices in generator(arr):
        swap_count += 1
        
        # We only print the first few and last few to prevent terminal flooding
        if swap_count <= 3 or swap_count % 10 == 0:
            print(f"  [STEP {swap_count:03d}] Swapping Indices {active_indices}")
            # We mathematically render the array as ASCII bars!
            visual_representation = ""
            for idx, val in enumerate(current_arr):
                # If this index was just swapped, color it with `[*]`!
                if idx in active_indices:
                    visual_representation += f"[{val:02d}] "
                else:
                    visual_representation += f" {val:02d}  "
            print(f"            {visual_representation}")
            
    print(f"\n  [FINAL STATE] {arr}")
    print(f"  [METRICS] Total Operations Executed: {swap_count}")
    print("  [SUCCESS] Mathematical array is perfectly sorted.")


def demonstrate_visualizer():
    visualize_algorithm("Bubble Sort (O(N^2))", bubble_sort_generator, array_size=10)
    visualize_algorithm("Insertion Sort (O(N^2))", insertion_sort_generator, array_size=10)


def run_all_labs():
    demonstrate_visualizer()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "Why must we use the `yield` keyword (a Generator) when architecting an Algorithm Visualizer? Why can't we just update the Pygame UI directly inside the Bubble Sort `for` loop?"
   Senior Answer: "Separation of Concerns and Architectural Coupling. If you inject `pygame.display.update()` directly into the Bubble Sort algorithm, the mathematical algorithm becomes permanently coupled to the GUI framework. You cannot test the algorithm on a Linux server without a monitor, and you cannot swap Pygame for Matplotlib. By using a Generator (`yield`), the mathematical algorithm remains $100\\%$ pure. It simply executes a swap, pauses its execution state in RAM, and hands the data back to the caller. The Caller (the GUI Engine) updates the screen, sleeps for $0.1$ seconds, and then asks the Generator to resume. This completely decouples the heavy math from the visual rendering."

2. Interviewer: "Bubble Sort and Insertion Sort are both mathematically $O(N^2)$ in their Worst-Case scenarios. Why is Insertion Sort universally preferred in production implementations (like Python's Timsort) over Bubble Sort?"
   Senior Answer: "Algorithmic constants and 'Best-Case' optimization. Bubble Sort is mathematically atrocious because it always requires extensive sweeping passes, even if the array is mostly sorted. Insertion Sort is highly optimized for 'Nearly Sorted' data. If you run Insertion Sort on an array that is already sorted, the inner `while` loop mathematically fails on the very first check every single time. It executes exactly one operation per element, collapsing the Time Complexity from $O(N^2)$ down to a flawless $O(N)$. Python's native `sort()` (Timsort) specifically relies on Insertion Sort to instantly sort small, fragmented sub-arrays because of this exact mathematical property."

3. Interviewer: "In Python, we executed the swap using `arr[j], arr[j+1] = arr[j+1], arr[j]`. Under the hood in the CPython interpreter, how does this bypass the need for a temporary holding variable?"
   Senior Answer: "It utilizes 'Tuple Packing and Unpacking' via the C-level stack. In languages like C or Java, you must write `temp = a; a = b; b = temp`. In Python, the right side of the assignment (`arr[j+1], arr[j]`) is mathematically evaluated first. The CPython interpreter packs those two values into an immutable C-Tuple in RAM. Then, it unpacks that Tuple directly into the variables on the left side of the assignment. Because the Tuple was firmly established in memory before the left side was modified, the variables are swapped perfectly without requiring the developer to instantiate an explicit `temp` variable, resulting in cleaner and mathematically safer code."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Capstone Project (Sorting Visualizer) Completed.")
