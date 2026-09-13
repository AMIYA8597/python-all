"""
# ==============================================================================
# LABORATORY: ADVANCED BIG DATA (PARQUET, ICEBERG, STREAMING)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You can have a 1,000-node Spark cluster, but if you store your 100 Terabytes 
# of data as a CSV file, your system will be unbelievably slow.
# CSV is row-based. If you only want to analyze the 'Price' column, the hard 
# drive is physically forced to read the entire row (Name, Address, Email, Price), 
# throwing away 90% of the data it just read. This destroys Disk I/O.
# 
# You MUST use Columnar Storage formats like Apache Parquet.
#
# Furthermore, what if 5 Data Scientists try to write to the 100 TB Parquet 
# file at the exact same time? It corrupts the data! Data Lakes lack ACID 
# transactions. You must upgrade to a Lakehouse architecture (Delta Lake or 
# Apache Iceberg).
#
# Finally, what if the data is arriving at 10,000 messages per second (like 
# credit card swipes)? You cannot use batch files. You must use Message Queues 
# (Kafka) and Structured Streaming.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the math of Columnar Storage (Apache Parquet).
# - Understand Lakehouse Architectures (Delta Lake & ACID transactions).
# - Understand Real-Time Data Streaming (Kafka & Spark Streaming).
#
# ==============================================================================
"""

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. COLUMNAR STORAGE (APACHE PARQUET)
# ==============================================================================
def demonstrate_parquet():
    section_header("Apache Parquet (Columnar Storage)")
    
    print("CSV files store data row-by-row on the physical hard drive platter:")
    print("[Row 1: John, 25, $500] [Row 2: Jane, 30, $600]")
    
    print("\nIf your query is: `SELECT SUM(salary) FROM table;`")
    print("The hard drive must physically scan over 'John' and '25' just to reach '$500'.")
    print("This requires 100 Terabytes of Disk I/O!")
    
    print("\n--- The Columnar Solution ---")
    print("Parquet stores data COLUMN-BY-COLUMN on the physical hard drive:")
    print("[Column Names: John, Jane] [Column Ages: 25, 30] [Column Salaries: $500, $600]")
    
    print("\nWhen you query `SUM(salary)`, Spark directly jumps to the physical ")
    print("memory address of the 'Salaries' block. It completely skips the Names ")
    print("and Ages blocks. Disk I/O drops from 100 Terabytes to 2 Terabytes!")
    
    print("\n--- Predicate Pushdown ---")
    print("Parquet stores mathematical metadata at the end of every block ")
    print("(e.g., Block 1 Salaries: MIN=$40k, MAX=$90k).")
    print("If your query is: `SELECT * WHERE salary > $100k`, Spark reads the metadata, ")
    print("realizes Block 1 maxes out at 90k, and physically REFUSES to load ")
    print("the block into RAM. It is a massive performance cheat code!")


# ==============================================================================
# 4. DATA LAKEHOUSES (DELTA LAKE / ICEBERG)
# ==============================================================================
def demonstrate_lakehouses():
    section_header("Data Lakehouse (Delta Lake & Apache Iceberg)")
    
    print("A Data Warehouse (like Snowflake/Redshift) is highly structured and ")
    print("supports ACID transactions, but it is incredibly expensive.")
    print("A Data Lake (AWS S3 full of Parquet files) is cheap and flexible, ")
    print("but if a job crashes halfway through writing a Parquet file, the ")
    print("Data Lake becomes permanently corrupted. You cannot ROLLBACK.")
    
    print("\n--- The Lakehouse Architecture ---")
    print("Technologies like Delta Lake (by Databricks) or Apache Iceberg sit ")
    print("directly on top of your raw Parquet files in S3.")
    
    print("\nThey add a 'Transaction Log'.")
    print("When Spark writes a new Parquet file, it does not immediately expose it ")
    print("to the users. It writes the data, verifies the math is 100% correct, ")
    print("and THEN atomically updates the Transaction Log. (This is ACID Compliance).")
    
    print("\n--- Time Travel ---")
    print("Because Iceberg tracks every single change in the Transaction Log, ")
    print("you can execute 'Time Travel' queries!")
    print("`spark.read.option('asOfTimestamp', '2023-01-01').parquet('s3://data')`")
    print("Spark will instantly recreate the exact state of the 100TB database ")
    print("as it existed on January 1st, allowing you to debug old ML models!")


# ==============================================================================
# 5. STREAMING (KAFKA & SPARK STRUCTURED STREAMING)
# ==============================================================================
def demonstrate_streaming():
    section_header("Streaming Data (Kafka & Spark Structured Streaming)")
    
    print("Standard Spark jobs are 'Batch'. You wake up at 2 AM, read yesterday's ")
    print("files, and train the model. This is too slow for Credit Card Fraud.")
    print("You need sub-second Latency. You must use Streaming.\n")
    
    print("--- Apache Kafka (The Message Queue) ---")
    print("Kafka is a distributed append-only log. When a user swipes a credit card, ")
    print("the Point-of-Sale terminal pushes a tiny JSON message into a Kafka 'Topic'.")
    print("Kafka can handle Millions of messages per second without crashing.")
    
    print("\n--- Spark Structured Streaming ---")
    print("Instead of reading a static Parquet file, Spark connects directly to Kafka!")
    print("Spark treats the infinite stream of Kafka messages as an 'Unbounded Table'.")
    
    print("\n```python")
    print("streaming_df = spark.readStream.format('kafka') \\")
    print("    .option('kafka.bootstrap.servers', 'host1:port1') \\")
    print("    .option('subscribe', 'credit_card_swipes') \\")
    print("    .load()")
    
    print("\n# Perform ML inference on the live stream!")
    print("predictions = fraud_model.transform(streaming_df)")
    
    print("\n# Write the predictions back out in real-time!")
    print("query = predictions.writeStream \\")
    print("    .outputMode('append') \\")
    print("    .format('console') \\")
    print("    .start()")
    print("```")
    print("\nThis creates a permanent, infinite cluster job that processes data ")
    print("in Micro-Batches every 500 milliseconds, achieving real-time ML execution!")


def run_all_labs():
    demonstrate_parquet()
    demonstrate_lakehouses()
    demonstrate_streaming()


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Explain how "Predicate Pushdown" in Apache Parquet accelerates Big Data queries.
   Answer: Parquet is a columnar storage format that breaks data into "Row Groups" and stores massive amounts of metadata (MIN, MAX, COUNT, NULLs) for every column block. If a user executes a SQL query like `SELECT * FROM users WHERE age > 50`, the Spark engine reads the Parquet metadata first. If a specific block's metadata says `MIN=18, MAX=35`, Spark mathematically proves that no row in that block can satisfy the query. Spark forcefully bypasses the entire block (Predicate Pushdown), physically refusing to load the Gigabytes of data into RAM or read it from disk. This drops Disk I/O and query time exponentially.

2. What is the fundamental difference between a Data Lake and a Data Lakehouse (e.g., Delta Lake)?
   Answer: A standard Data Lake is just a massive folder in the cloud (AWS S3) filled with raw CSV or Parquet files. It has no transactional guarantees. If a Spark job crashes while writing, it leaves behind corrupted, half-written files. If a user reads the directory simultaneously, they get garbage data (No ACID compliance). A Data Lakehouse (Delta Lake / Apache Iceberg) sits on top of the Data Lake and adds a highly structured Transaction Log. It guarantees Atomicity (a job fully completes or completely rolls back) and allows multiple users to safely read and write to the same petabyte-scale directory concurrently without corruption.

3. Why do we place Apache Kafka in front of Spark Structured Streaming? Why not just send the API data directly into Spark?
   Answer: Spark is an analytical processing engine, not a high-throughput message ingestion buffer. If a Black Friday spike causes credit card transactions to jump from 1,000/sec to 500,000/sec, sending that directly into Spark will instantly overload the executors and crash the cluster, permanently dropping the data. Apache Kafka acts as a massive, distributed, fault-tolerant shock absorber. It persists the 500,000/sec messages safely to its own hard drives instantly. Spark Streaming then comfortably reads from Kafka at its own maximum processing speed (e.g., 50,000/sec). Spark will slowly catch up over the next hour, but exactly zero data is lost during the spike.
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Advanced Big Data Completed.")
