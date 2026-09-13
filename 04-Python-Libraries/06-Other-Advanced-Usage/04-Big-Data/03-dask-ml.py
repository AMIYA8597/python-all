"""
# ==============================================================================
# LABORATORY: PYTHON-NATIVE BIG DATA (DASK)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Apache Spark (PySpark) is incredible, but it is built on the Java Virtual 
# Machine (JVM). If your PySpark code crashes, you get a 500-line Java stack 
# trace that is completely incomprehensible to a Python developer.
#
# Furthermore, Spark requires you to rewrite all of your beloved Pandas and 
# Scikit-Learn code using the completely different Spark API.
#
# Enter Dask.
#
# Dask is a massive distributed computing library built 100% natively in Python.
# It mathematically perfectly mimics the Pandas and Scikit-Learn APIs! You can 
# take a standard Pandas script, change `import pandas as pd` to `import dask.dataframe as dd`, 
# and instantly scale your script across a 1,000-node supercomputer with almost zero code changes!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the architecture of Dask (Task Graphs).
# - Execute Pandas-style data manipulation using Dask DataFrames.
# - Execute Scikit-Learn distributed Machine Learning using Dask-ML.
#
# ==============================================================================
"""

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. DASK ARCHITECTURE & TASK GRAPHS
# ==============================================================================
def demonstrate_dask_architecture():
    section_header("Dask Architecture & Task Graphs")
    
    print("How does Dask scale Pandas to 500 Terabytes?")
    
    print("\n--- The Partitioning Illusion ---")
    print("A Dask DataFrame is not a new data structure. It is literally just ")
    print("10,000 standard Pandas DataFrames glued together!")
    print("If you have a 500GB CSV file, Dask chops it into 1,000 separate ")
    print("500MB chunks. It assigns each chunk to a single CPU core. Each core ")
    print("loads its 500MB chunk into a perfectly standard Pandas DataFrame.")
    
    print("\n--- Task Graphs (Lazy Evaluation) ---")
    print("Like Spark, Dask uses Lazy Evaluation.")
    print("When you type `df.groupby('city').mean()`, Dask does not calculate anything.")
    print("Instead, it builds a massive 'Task Graph' (a recipe):")
    print("1. Tell Core #1 to group its Pandas DataFrame.")
    print("2. Tell Core #2 to group its Pandas DataFrame.")
    print("3. Tell Core #3 to collect the results from Core 1 and 2 and average them.")
    
    print("\nWhen you finally call `df.compute()`, the Dask Scheduler fires ")
    print("up all the CPU cores, executes the Task Graph in parallel, and ")
    print("returns a single, tiny, aggregated Pandas DataFrame to your screen.")


# ==============================================================================
# 4. DASK DATAFRAMES (PANDAS SYNTAX)
# ==============================================================================
def demonstrate_dask_dataframes():
    section_header("Dask DataFrames (Zero-Learning-Curve Syntax)")
    
    print("If you know Pandas, you already know Dask.\n")
    
    print("```python")
    print("import dask.dataframe as dd")
    print("\n# Read a massively distributed dataset (Note the wildcard '*')")
    print("df = dd.read_csv('s3://my-bucket/sales_data_2023_*.csv')")
    
    print("\n# Perform standard Pandas syntax!")
    print("# This is instantly distributed across all 32 cores of your machine,")
    print("# or all 100 machines in your AWS cluster!")
    print("filtered_df = df[df['amount'] > 1000]")
    print("grouped_df = filtered_df.groupby('store_id')['amount'].sum()")
    
    print("\n# Nothing has executed yet! It is just a Task Graph.")
    print("# We trigger execution using .compute()")
    print("final_pandas_result = grouped_df.compute()")
    print("```")
    
    print("\nNotice how there is NO `VectorAssembler` or weird Java syntax.")
    print("It is pure, beautiful, Pythonic Pandas.")


# ==============================================================================
# 5. DASK-ML (SCIKIT-LEARN ON STEROIDS)
# ==============================================================================
def demonstrate_dask_ml():
    section_header("Dask-ML (Distributed Scikit-Learn)")
    
    print("Dask-ML mathematically perfectly mimics the Scikit-Learn API.\n")
    
    print("```python")
    print("from dask_ml.model_selection import train_test_split")
    print("from dask_ml.linear_model import LogisticRegression")
    print("import joblib")
    
    print("\n# 1. Split the massive Dask DataFrame")
    print("X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)")
    
    print("\n# 2. Initialize the Dask-ML Algorithm")
    print("# This algorithm is explicitly rewritten to calculate gradients across ")
    print("# 100 computers in parallel!")
    print("model = LogisticRegression()")
    
    print("\n# 3. Train the Model")
    print("model.fit(X_train, y_train)")
    
    print("\n# --- ALTERNATIVE: SCALING STANDARD SCIKIT-LEARN ---")
    print("# What if you want to use a standard Scikit-Learn Random Forest, but ")
    print("# you want to train the 100 Trees in parallel across your massive cluster?")
    
    print("\nfrom sklearn.ensemble import RandomForestClassifier")
    print("\nrf = RandomForestClassifier(n_estimators=100)")
    
    print("\n# Wrap the normal Sklearn fit call in a Dask Joblib context!")
    print("with joblib.parallel_backend('dask'):")
    print("    rf.fit(X_pandas, y_pandas)")
    
    print("```")
    print("\nThe `joblib` context manager magically hijacks the internal Scikit-Learn ")
    print("threading system. Instead of training the trees on your 4 local CPU cores, ")
    print("it blasts the workload out to the 1,000 CPU cores in your Dask cluster, ")
    print("dropping training time from 3 hours to 3 minutes!")


def run_all_labs():
    demonstrate_dask_architecture()
    demonstrate_dask_dataframes()
    demonstrate_dask_ml()


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. What is the architectural difference between a Spark DataFrame and a Dask DataFrame?
   Answer: Spark is built on the Java Virtual Machine (JVM). A Spark DataFrame is a distributed collection of Row objects managed entirely by the Scala/Java engine. When you write PySpark, you are just sending string commands via a socket to the underlying Java process. A Dask DataFrame is completely Python-native. It is literally just a collection of standard Pandas DataFrames mathematically mapped across multiple CPU cores. Dask simply orchestrates which CPU core executes which Pandas function, allowing Python developers to leverage the exact same C-optimized Pandas syntax they already know without dealing with JVM overhead.

2. Explain how `.compute()` triggers Lazy Evaluation in Dask.
   Answer: When you write standard code in Dask (`df = df[df['price'] > 10]`), Dask does absolutely no data processing. It merely constructs a mathematical blueprint called a "Task Graph" (a Directed Acyclic Graph - DAG) representing the steps required. The `.compute()` method is the Action trigger. It takes the massive Task Graph, sends it to the Dask Scheduler, and the Scheduler optimizes the execution order and physically assigns the tasks to the available CPU cores (or cloud workers), finally returning the actual materialized data to your screen as a standard Pandas DataFrame.

3. How does `joblib.parallel_backend('dask')` allow you to scale standard Scikit-Learn models to a massive cloud cluster?
   Answer: Many Scikit-Learn algorithms (like RandomForest or GridSearchCV) support internal parallelization using the `n_jobs=-1` parameter. Under the hood, Scikit-Learn uses a library called `joblib` to spawn multiple threads across your local laptop's CPU cores. By explicitly opening a `with joblib.parallel_backend('dask'):` context manager, you completely hijack Scikit-Learn's internal threading system. When Scikit-Learn tries to spawn a thread to build Tree #42, the Dask backend intercepts it and sends the computational task across the network to a massive cloud cluster, training the standard Scikit-Learn model 100x faster without rewriting the algorithm!
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Python-Native Big Data (Dask) Completed.")
