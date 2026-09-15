"""
# ==============================================================================
# LABORATORY: DATA ANALYTICS (PANDAS & VECTORIZATION)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A junior data analyst loads a massive CSV with 5,000,000 rows containing 
# stock prices. They use a standard Python `for` loop, iterating row-by-row 
# to calculate a 10% tax on every price. Because Python is an interpreted 
# language, the CPU mathematically evaluates the type of the variable 5 million 
# times. The script takes 45 seconds to execute.
#
# A senior data engineer uses Pandas and NumPy. They understand that a Pandas 
# DataFrame is mathematically backed by contiguous C-arrays in RAM. They execute 
# a "Vectorized Operation" (`df['tax'] = df['price'] * 0.10`). The Python 
# interpreter completely bypasses the `for` loop and delegates the math directly 
# to highly optimized C-code utilizing CPU SIMD (Single Instruction, Multiple Data) 
# architecture. The script takes 0.05 seconds. 
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master Pandas DataFrames and Series.
# - Execute Vectorized Mathematics to achieve O(1) Python overhead.
# - Architect Data Selection (`.loc`, `.iloc`) and Boolean Masking.
#
# ==============================================================================
"""

import pandas as pd
import numpy as np
import time

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE BUSINESS LOGIC (THE DATA PIPELINE)
# ==============================================================================
class DataAnalyticsEngine:
    
    def __init__(self, size: int = 1_000_000):
        self.size = size
        self.df = None
        self._generate_mock_data()
        
    def _generate_mock_data(self):
        """Generates a massive dataset in RAM for mathematical testing."""
        print(f"  [INIT] Allocating Pandas DataFrame with {self.size:,} rows...")
        # We use NumPy to generate fast random data!
        data = {
            'id': np.arange(self.size),
            'price': np.random.uniform(10.0, 500.0, self.size),
            'quantity': np.random.randint(1, 100, self.size),
            'category': np.random.choice(['Tech', 'Clothing', 'Food', 'Books'], self.size)
        }
        self.df = pd.DataFrame(data)
        print("  [SUCCESS] Dataset generated and loaded into contiguous C-memory.")


    # --------------------------------------------------------------------------
    # THE ANTI-PATTERN: ITERATION (THE LOOP OF DEATH)
    # --------------------------------------------------------------------------
    def calculate_revenue_slow(self):
        """
        [WARNING] THIS IS CATASTROPHICALLY SLOW.
        Iterating over a DataFrame with `iterrows()` completely destroys 
        the C-level optimizations.
        """
        print("\n  [EXECUTION] Calculating Revenue via O(N) Python iteration (`iterrows`).")
        start = time.time()
        
        # NOTE: We only do 10,000 rows, otherwise we would be here all day!
        small_df = self.df.head(10_000).copy()
        
        total_revenue = []
        for index, row in small_df.iterrows():
            total_revenue.append(row['price'] * row['quantity'])
            
        small_df['revenue'] = total_revenue
        
        elapsed = time.time() - start
        print(f"  -> Processed 10,000 rows in: {elapsed:.4f} seconds.")


    # --------------------------------------------------------------------------
    # THE ARCHITECTURAL PATTERN: VECTORIZATION
    # --------------------------------------------------------------------------
    def calculate_revenue_fast(self):
        """
        [SECURE] Vectorized Execution.
        We multiply the entire column at once. The math happens in C!
        """
        print(f"\n  [EXECUTION] Calculating Revenue via Vectorization for ALL {self.size:,} rows.")
        start = time.time()
        
        # This is a Vectorized Operation!
        self.df['revenue'] = self.df['price'] * self.df['quantity']
        
        elapsed = time.time() - start
        print(f"  -> Processed {self.size:,} rows in: {elapsed:.4f} seconds!")


# ==============================================================================
# 4. MATHEMATICAL PROOF (THE BENCHMARK)
# ==============================================================================
def demonstrate_pandas():
    section_header("Data Analytics: Pandas Vectorization")
    
    # We will simulate 2 Million rows!
    engine = DataAnalyticsEngine(size=2_000_000)
    
    # Run the bad code (only on a subset)
    engine.calculate_revenue_slow()
    
    # Run the good code (on everything)
    engine.calculate_revenue_fast()
    
    print("\n  [ARCHITECTURE PROOF]")
    print("  The Python `for` loop took significantly longer to process 10,000 rows ")
    print("  than the Vectorized operation took to process 2,000,000 rows. By ")
    print("  thinking in 'Columns' instead of 'Rows', the Data Engineer mathematically ")
    print("  unlocked the raw speed of the CPU's C-architecture.")


def run_all_labs():
    demonstrate_pandas()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "What is 'Vectorization' in Pandas, and why is it mathematically faster than a standard Python `for` loop?"
   Senior Answer: "Bypassing the Interpreter. In a standard Python loop, the interpreter must dynamically check the data type of the variable on every single iteration (e.g., 'Is this an integer? A float?'). This creates massive CPU overhead. Pandas Series are backed by NumPy arrays, which are homogeneous, contiguous blocks of C-memory. When you execute `df['A'] * df['B']`, Pandas delegates the operation to pre-compiled C code. The C compiler utilizes CPU SIMD (Single Instruction, Multiple Data) to execute the math on chunks of memory simultaneously, achieving speeds $100x$ to $1000x$ faster than interpreted Python."

2. Interviewer: "Explain the architectural difference between `.loc[]` and `.iloc[]` when querying a DataFrame."
   Senior Answer: "Label vs Integer-Position Indexing. `.loc[]` is mathematically designed to query the explicit *Labels* of the index. If your index consists of Dates (e.g., '2024-01-01'), you use `.loc['2024-01-01']`. It is inclusive on both ends of a slice (`.loc['A':'C']` returns A, B, and C). In contrast, `.iloc[]` strictly uses integer positions (0-based memory offsets), exactly like a standard Python list. You use `.iloc[0:5]` to grab the physical first 5 rows, regardless of what the index labels are. It is exclusive on the upper bound."

3. Interviewer: "If a DataFrame requires 10 Gigabytes of RAM, how can you aggressively optimize its memory footprint without deleting data?"
   Senior Answer: "Downcasting Data Types. By default, Pandas loads integers as `int64` and decimals as `float64`, consuming 8 bytes per cell. If an 'Age' column ranges from $0$ to $100$, allocating an 8-byte `int64` (which can store numbers up to $9$ Quintillion) is a mathematical disaster. By executing `pd.to_numeric(df['Age'], downcast='integer')`, the column is mathematically squashed into an `int8` (1 byte), reducing RAM consumption by $87\\%$. Furthermore, converting string columns with low cardinality (e.g., 'Gender' or 'Country') into Pandas `category` types replaces massive strings with tiny integer pointers under the hood, instantly saving Gigabytes of RAM."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Data Analytics (Pandas Basics) Completed.")
