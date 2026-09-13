"""
# ==============================================================================
# LABORATORY: BIG DATA & CLUSTER COMPUTING (PYSPARK)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Pandas is an incredible tool for Data Science. You load a 2 Gigabyte CSV, 
# Pandas reads it into RAM, and you analyze it.
#
# But what if you work at Netflix, and you need to analyze a 500 Terabyte CSV 
# containing every user click from the last 10 years?
#
# If you run `pd.read_csv('500TB.csv')`, your laptop will instantly crash with 
# an OutOfMemoryError. Your laptop only has 16 Gigabytes of RAM!
#
# You must use Distributed Cluster Computing. Apache Spark allows you to connect 
# 100 separate computers (nodes) together over a network. Spark automatically 
# chops the 500 TB CSV into 100 small chunks, sends one chunk to each computer, 
# processes them all simultaneously in parallel, and merges the results back 
# to you! PySpark is the Python API for this massive engine.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the architecture of Spark (Driver vs Executors).
# - Master Lazy Evaluation and Spark DataFrames.
# - Understand RDDs (Resilient Distributed Datasets).
#
# ==============================================================================
"""

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. SPARK ARCHITECTURE (DRIVER & EXECUTORS)
# ==============================================================================
def demonstrate_architecture():
    section_header("Spark Cluster Architecture")
    
    print("Spark operates on a Master-Slave (Driver-Executor) architecture.")
    
    print("\n1. THE DRIVER (Your Laptop)")
    print("   This is where your Python code runs. The Driver NEVER actually ")
    print("   touches the 500TB of data. Its only job is to mathematically map ")
    print("   out the execution plan and manage the cluster.")
    
    print("\n2. THE CLUSTER MANAGER (YARN / Kubernetes)")
    print("   The middleman. The Driver says 'I need 100 computers with 16GB RAM each!'")
    print("   The Cluster Manager finds those machines in the AWS Cloud and boots them up.")
    
    print("\n3. THE EXECUTORS (The Worker Nodes)")
    print("   These are the 100 physical servers. The Driver sends them the ")
    print("   actual compiled Java/Scala bytecode. The Executors load their 5TB ")
    print("   slice of the data into their local RAM, execute the code, and ")
    print("   report the results back to the Driver.")


# ==============================================================================
# 4. LAZY EVALUATION (THE MAGIC OF SPARK)
# ==============================================================================
def demonstrate_lazy_evaluation():
    section_header("Lazy Evaluation & Spark DataFrames")
    
    print("In Pandas (Eager Evaluation):")
    print("`df = pd.read_csv('data.csv')` -> Pandas IMMEDIATELY loads the data into RAM.")
    
    print("\nIn Spark (Lazy Evaluation):")
    print("`df = spark.read.csv('500TB.csv')` -> Spark does ABSOLUTELY NOTHING!")
    print("It just writes down a note: 'The user wants to read this file eventually.'")
    
    print("\n`df = df.filter(df.age > 18)` -> Spark does ABSOLUTELY NOTHING!")
    print("It adds a note: 'The user also wants to filter by age.'")
    
    print("\n`df = df.select('name')` -> Spark does ABSOLUTELY NOTHING!")
    print("It adds a note: 'The user only wants the name column.'")
    
    print("\n--- The Action Trigger ---")
    print("Nothing executes until you call an ACTION (like `.count()` or `.show()`).")
    print("`df.show()` -> BOOM! Spark springs into action.")
    
    print("\nWhy is this genius?")
    print("Because Spark waited to see the *entire* mathematical plan, the Catalyst ")
    print("Optimizer can rewrite your code! It realizes: 'Wait, the user ONLY wants ")
    print("the name column for people over 18. Therefore, I will instruct the 100 ")
    print("worker nodes to NEVER even load the other 50 columns into RAM!'")
    print("This turns a 50-hour query into a 5-minute query.")


# ==============================================================================
# 5. RDDs vs DATAFRAMES
# ==============================================================================
def demonstrate_rdds():
    section_header("RDDs (Resilient Distributed Datasets)")
    
    print("The core data structure of Spark is the RDD.")
    print("It is a massive, fault-tolerant collection of elements partitioned ")
    print("across the 100 nodes of the cluster.\n")
    
    print("--- 1. Fault Tolerance (Resilient) ---")
    print("What if Worker Node #42 physically catches on fire and dies during ")
    print("the 5-hour calculation? Does the entire job crash?")
    print("NO! Spark RDDs track their mathematical Lineage (the DAG - Directed ")
    print("Acyclic Graph). The Driver realizes Node #42 died. It spins up Node #101, ")
    print("looks at the DAG, and mathematically re-calculates *only* the specific ")
    print("slice of data that was lost in the fire. The job finishes seamlessly!")
    
    print("\n--- 2. DataFrames vs RDDs ---")
    print("In 2014, developers had to write raw RDD code (using ugly map/reduce lambda functions).")
    print("In 2016, Spark introduced DataFrames.")
    print("Spark DataFrames look exactly like Pandas DataFrames, and you can write ")
    print("raw SQL against them (`spark.sql('SELECT * FROM users')`).")
    print("Under the hood, the Catalyst Optimizer compiles your beautiful SQL ")
    print("down into highly-optimized raw RDD Java bytecode, giving you Python ")
    print("syntax with raw C++/Java speed!")


def run_all_labs():
    demonstrate_architecture()
    demonstrate_lazy_evaluation()
    demonstrate_rdds()


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Explain the architectural difference between the "Driver" and the "Executors" in an Apache Spark cluster.
   Answer: The Driver is the central orchestrator (the "brain"). It runs your Python script (`main()`), maintains the SparkSession, and constructs the Directed Acyclic Graph (DAG) of the execution plan. The Driver *never* processes the massive datasets itself. The Executors are the slave worker nodes (the "muscle"). They reside on separate physical computers in the cloud. The Driver serializes the compiled tasks and sends them over the network to the Executors. The Executors read their specific slice (partition) of the data from the hard drive into their local RAM, execute the mathematical calculations, and send the aggregated results back to the Driver.

2. What is "Lazy Evaluation" and how does the Catalyst Optimizer use it to drastically speed up Big Data queries?
   Answer: In standard Python (Eager Evaluation), code executes line-by-line instantly. In Spark (Lazy Evaluation), commands like `.filter()` or `.select()` (Transformations) do not execute immediately; they merely build a logical blueprint (the DAG). The code only physically executes when you call an Action like `.collect()` or `.show()`. By waiting to see the *entire* logical blueprint before acting, Spark's Catalyst Optimizer can mathematically restructure the query. If step 10 of your code drops 90% of the columns, the Optimizer will physically rewrite the Java bytecode to ensure those columns are never loaded from the hard drive at step 1! This prevents massive bottlenecks in disk I/O and network shuffling.

3. How does an RDD (Resilient Distributed Dataset) achieve Fault Tolerance without backing up the data?
   Answer: In traditional databases, fault tolerance is achieved by replicating (copying) the data to 3 different hard drives, which is massively expensive. Spark RDDs achieve fault tolerance through "Lineage". An RDD does not store the physical data; it stores the mathematical recipe (the DAG) of how to *create* the data from the original source file on disk. If a worker node crashes and its RAM is destroyed, Spark simply looks at the Lineage graph, boots up a replacement node, and re-runs the exact mathematical transformations on that specific data partition to perfectly reconstruct the lost RAM state.
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Big Data (PySpark Basics) Completed.")
