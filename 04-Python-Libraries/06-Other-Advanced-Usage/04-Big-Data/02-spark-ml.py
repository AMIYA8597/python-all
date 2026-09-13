"""
# ==============================================================================
# LABORATORY: DISTRIBUTED MACHINE LEARNING (SPARK MLLIB)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You have a 10 Terabyte CSV file containing 500 Million rows of credit card 
# transactions. You want to train a Random Forest model to detect Fraud.
#
# If you try to use `scikit-learn`, your code will instantly crash because 
# `sklearn` runs on a single computer and mathematically requires the entire 
# dataset to fit inside the RAM of that single computer.
#
# You must use Spark MLlib (Machine Learning Library).
# MLlib algorithms are completely rewritten from the ground up to execute in 
# parallel across a cluster of 100 computers. It mathematically calculates the 
# Random Forest splits asynchronously across the 100 nodes, and merges the 
# decision trees at the Driver.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the architecture of Distributed Machine Learning.
# - Master the `VectorAssembler` (Spark's required tensor format).
# - Execute a distributed Machine Learning Pipeline.
#
# ==============================================================================
"""

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. SPARK ML ARCHITECTURE & VECTOR ASSEMBLER
# ==============================================================================
def demonstrate_spark_ml_architecture():
    section_header("The Spark MLlib Architecture")
    
    print("In Scikit-Learn, you pass a Pandas DataFrame directly into `model.fit()`.")
    print("Spark MLlib STRICTLY FORBIDS THIS!")
    
    print("\n--- The VectorAssembler ---")
    print("Spark requires all Machine Learning features to be mathematically ")
    print("collapsed into a SINGLE column containing a massive Vector array.\n")
    
    print("Bad Spark DataFrame (Fails to Train):")
    print("Row 1: [Age: 25, Income: 50k, Score: 700] -> Label: Fraud")
    print("Row 2: [Age: 40, Income: 80k, Score: 800] -> Label: Not Fraud")
    
    print("\nCorrect Spark DataFrame (Trains perfectly):")
    print("Row 1: [features: [25, 50000, 700]] -> Label: Fraud")
    print("Row 2: [features: [40, 80000, 800]] -> Label: Not Fraud")
    
    print("\nTo achieve this, we use the `VectorAssembler` transformer.")
    print("It physically crushes the multiple independent columns into a single ")
    print("DenseVector structure, which the distributed Java/Scala linear algebra ")
    print("libraries process with blazing speed.")


# ==============================================================================
# 4. DISTRIBUTED MACHINE LEARNING PIPELINES
# ==============================================================================
def demonstrate_ml_pipeline():
    section_header("Executing a Distributed ML Pipeline")
    
    print("Because we cannot easily spin up a 100-node Hadoop cluster in this ")
    print("Python script, we will conceptually review the exact code required ")
    print("to train a distributed model at scale.\n")
    
    print("```python")
    print("from pyspark.sql import SparkSession")
    print("from pyspark.ml.feature import StringIndexer, VectorAssembler")
    print("from pyspark.ml.classification import RandomForestClassifier")
    print("from pyspark.ml import Pipeline")
    
    print("\n# 1. Initialize Distributed Cluster")
    print("spark = SparkSession.builder.appName('FraudDetector').getOrCreate()")
    
    print("\n# 2. Lazy Load 10 Terabytes of Data")
    print("df = spark.read.parquet('s3://my-bucket/massive_fraud_data/')")
    
    print("\n# 3. Feature Engineering Transformers")
    print("# Convert string labels ('Fraud', 'Safe') into integers (1, 0)")
    print("indexer = StringIndexer(inputCol='category', outputCol='label')")
    
    print("\n# Crush features into the single required Vector column")
    print("assembler = VectorAssembler(")
    print("    inputCols=['age', 'transaction_amount', 'distance_from_home'],")
    print("    outputCol='features'")
    print(")")
    
    print("\n# 4. The Distributed Algorithm")
    print("rf = RandomForestClassifier(")
    print("    featuresCol='features', ")
    print("    labelCol='label', ")
    print("    numTrees=100")
    print(")")
    
    print("\n# 5. Build the Pipeline")
    print("pipeline = Pipeline(stages=[indexer, assembler, rf])")
    
    print("\n# 6. TRIGGER THE CLUSTER (ACTION)")
    print("# This line takes 5 hours! The Driver sends the code to the 100 nodes.")
    print("# The nodes build the 100 Decision Trees locally on their 5TB data slices,")
    print("# and send the finished Trees back to the Driver to assemble the Forest!")
    print("model = pipeline.fit(df)")
    print("```")
    
    print("\nThis exact architecture powers the recommendation engines at Netflix ")
    print("and the fraud detection algorithms at Visa!")


def run_all_labs():
    demonstrate_spark_ml_architecture()
    demonstrate_ml_pipeline()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why does Scikit-Learn fail on Big Data, and how does Spark MLlib solve this?
   Answer: Scikit-Learn is designed for Single-Node, In-Memory computation. When you call `model.fit(X, y)`, Scikit-Learn mathematically requires the entire dataset `X` to fit contiguously into the physical RAM of the single computer running the Python script. If the CSV is 500 Gigabytes and the laptop has 16 Gigabytes of RAM, the OS throws an OutOfMemoryError and crashes. Spark MLlib solves this using Distributed Computing. It partitions the 500GB dataset across 100 separate computers in a cloud cluster. The MLlib algorithms are explicitly rewritten to use MapReduce paradigms, calculating mathematical gradients and decision tree splits locally on each node's small chunk of data in parallel, and aggregating the results over the network.

2. Why must you use a `VectorAssembler` before passing data into a Spark MLlib algorithm?
   Answer: In Pandas/Scikit-Learn, you can pass a DataFrame with 10 separate columns directly into the model. The underlying Spark MLlib engine is written in highly optimized Scala and Java, and utilizes a specialized linear algebra library (Breeze). For computational speed and API consistency across the distributed cluster, MLlib strictly requires the input features to be represented as a single mathematical Vector object. The `VectorAssembler` physically merges the 10 separate integer/float columns into a single column containing a unified `DenseVector` (or `SparseVector`), satisfying the mathematical requirements of the Scala backend.

3. In a distributed Random Forest algorithm, how does Spark train the trees across 100 separate computers?
   Answer: In a traditional Random Forest, you build 100 trees using Bootstrapped samples of the data. In Spark, the dataset is physically split across 100 worker nodes. Spark does NOT move all the data to one node (which would crash the network). Instead, it implements distributed training algorithms (like PLANET). The worker nodes calculate the mathematical statistical histograms for their local chunk of data (e.g., finding the best Gini impurity split for 'Age < 30') and send only those tiny aggregated statistics back to the Driver. The Driver chooses the global best split, updates the central Decision Tree structure, and broadcasts the new tree branches back to the workers for the next iteration!
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Spark MLlib Completed.")
