"""
Module: 02-spark-ml
Description: A textbook-grade interactive lesson on Apache Spark MLlib (Machine Learning Library) using PySpark.

================================================================================
LEARNING OBJECTIVES:
1. Understand the architecture and core abstractions of Spark MLlib (DataFrames, 
   Transformers, Estimators, and Pipelines).
2. Learn the mathematical foundations of distributed machine learning algorithms.
3. Master Big-O complexity analysis in the context of distributed systems.
4. Build a complete, end-to-end Machine Learning pipeline using PySpark.
5. Explore real-world applications and edge cases of Big Data ML.

================================================================================
THEORETICAL FOUNDATION & MATHEMATICAL BACKGROUND:

Apache Spark MLlib is designed to scale machine learning algorithms across clusters
of computers. Unlike traditional tools like scikit-learn that mostly operate in-memory
on a single node, MLlib utilizes Spark's distributed computing paradigm.

Key Components of Spark ML:
1. **DataFrame**: The core data structure, conceptually similar to a Pandas DataFrame
   or a relational database table, but distributed across the cluster.
2. **Transformer**: An algorithm that transforms one DataFrame into another.
   Mathematically, it's a function T: DataFrame -> DataFrame.
   (e.g., Tokenizer, StringIndexer, VectorAssembler).
3. **Estimator**: An algorithm that can be fit on a DataFrame to produce a Transformer
   (specifically, a Model). Functionally, E: DataFrame -> Model (where Model is a Transformer).
   (e.g., LogisticRegression, RandomForestClassifier).
4. **Pipeline**: Chains multiple Transformers and Estimators together to specify an ML workflow.

Mathematical Example: Logistic Regression
Logistic Regression models the probability that an instance belongs to a particular class.
For a feature vector $x \in \mathbb{R}^d$ and weights $w \in \mathbb{R}^d$, the probability is:
    P(y=1 | x; w) = \sigma(w^T x) = 1 / (1 + exp(-w^T x))

In Spark, the objective is to minimize the loss function over a distributed dataset D:
    L(w) = \sum_{i=1}^N \log(1 + \exp(-y_i w^T x_i)) + \lambda R(w)
Where $R(w)$ is the regularization term (L1, L2, or ElasticNet). Spark solves this
optimization problem using distributed solvers like L-BFGS or IRLS.

================================================================================
BIG-O ANALYSIS (DISTRIBUTED ML):

When analyzing Big Data algorithms, we must consider both Time Complexity and 
Communication Complexity (data shuffled across the network).

1. Feature Extraction (e.g., HashingTF):
   - Time Complexity: O(N * L) where N is the number of rows and L is the avg length of text.
   - Space Complexity: O(1) per executor (since hashing is stateless).
   - Communication: O(1) - Embarrassingly parallel, no shuffling required.

2. Model Training (e.g., Logistic Regression via L-BFGS):
   - Time Complexity per iteration: O(N * d) where N is the number of samples and 
     d is the number of features.
   - Network Communication per iteration: O(d) or O(d * log(P)) where P is the number 
     of partitions, primarily due to tree aggregation of gradients.
   - Overall: Highly scalable for large N, but can struggle if d (features) is extremely 
     large (e.g., billions) due to driver memory limits when collecting gradients.

================================================================================
REAL-WORLD APPLICATIONS:
1. **Churn Prediction**: Predicting if a customer will leave a subscription service 
   by analyzing terabytes of log data.
2. **Recommendation Systems**: Using Alternating Least Squares (ALS) on user-item 
   interaction matrices to recommend products (e.g., Netflix, Amazon).
3. **Fraud Detection**: Streaming transaction data and using RandomForest to classify 
   anomalous behavior in real-time.

"""

import sys
import time
from typing import Any, Dict, List, Optional, Tuple

# We encapsulate PySpark imports in a try-except block to gracefully handle 
# environments where PySpark might not be installed, preserving the educational
# value of the script.
try:
    from pyspark.sql import SparkSession
    from pyspark.sql import DataFrame
    from pyspark.ml import Pipeline, PipelineModel
    from pyspark.ml.feature import Tokenizer, HashingTF, IDF, StringIndexer, VectorAssembler
    from pyspark.ml.classification import LogisticRegression
    from pyspark.ml.evaluation import MulticlassClassificationEvaluator
    PYSPARK_AVAILABLE = True
except ImportError:
    PYSPARK_AVAILABLE = False
    SparkSession = Any
    DataFrame = Any


def initialize_spark_session(app_name: str = "PySpark_ML_Lesson") -> Optional[SparkSession]:
    """
    Initializes and returns a SparkSession.
    
    A SparkSession is the entry point to programming Spark with the Dataset and DataFrame API.
    
    Args:
        app_name (str): The name of the Spark application.
        
    Returns:
        Optional[SparkSession]: The initialized SparkSession, or None if PySpark is not available.
    """
    if not PYSPARK_AVAILABLE:
        print("[WARNING] PySpark is not installed. Returning None for SparkSession.")
        return None

    print(f"Initializing Spark Session: {app_name}...")
    # .master("local[*]") means run Spark locally with as many worker threads as logical cores
    spark = SparkSession.builder \
        .appName(app_name) \
        .master("local[*]") \
        .config("spark.driver.memory", "2g") \
        .getOrCreate()
    
    # Suppress verbose logging for clarity in the console
    spark.sparkContext.setLogLevel("ERROR")
    return spark


def create_sample_data(spark: SparkSession) -> DataFrame:
    """
    Creates a sample distributed DataFrame simulating a document classification task.
    
    Args:
        spark (SparkSession): The active SparkSession.
        
    Returns:
        DataFrame: A PySpark DataFrame containing IDs, text, and labels.
    """
    print("Creating sample Big Data DataFrame...")
    # Real-world equivalent: spark.read.parquet("hdfs://cluster/path/to/data")
    data = [
        (0, "Spark is an amazing framework for Big Data", "technology"),
        (1, "Machine learning models require huge datasets", "technology"),
        (2, "Python is a versatile programming language", "technology"),
        (3, "The stock market saw a massive drop today", "finance"),
        (4, "Investing in index funds is a safe long-term strategy", "finance"),
        (5, "Interest rates are determined by the central bank", "finance"),
        (6, "Distributed computing handles massive scale", "technology"),
        (7, "Dividend yields are attractive to value investors", "finance")
    ]
    
    columns = ["id", "text", "category"]
    df = spark.createDataFrame(data, columns)
    
    print("Sample Data Created:")
    df.show(truncate=False)
    return df


def build_ml_pipeline() -> Tuple[Pipeline, Dict[str, Any]]:
    """
    Constructs a PySpark ML Pipeline for text classification.
    
    The pipeline consists of multiple stages:
    1. Tokenizer: Splits text into individual words.
    2. HashingTF: Maps a sequence of terms to their term frequencies using the hashing trick.
    3. IDF: Rescales feature vectors, down-weighting features which appear frequently.
    4. StringIndexer: Encodes the categorical label into label indices.
    5. LogisticRegression: The Estimator that learns the classification model.
    
    Returns:
        Tuple[Pipeline, Dict[str, Any]]: The un-fitted ML pipeline and metadata about stages.
    """
    print("Building Spark ML Pipeline...")
    
    # Stage 1: Tokenization
    # O(N * L) time where N is documents, L is average words per document.
    tokenizer = Tokenizer(inputCol="text", outputCol="words")
    
    # Stage 2: Term Frequency via Hashing
    # Using 1000 features for demonstration. Real-world might use 2^18 or 2^20.
    hashing_tf = HashingTF(inputCol=tokenizer.getOutputCol(), outputCol="rawFeatures", numFeatures=1000)
    
    # Stage 3: Inverse Document Frequency
    idf = IDF(inputCol=hashing_tf.getOutputCol(), outputCol="features")
    
    # Stage 4: Label Indexing (converts string categories to float labels expected by ML algorithms)
    label_indexer = StringIndexer(inputCol="category", outputCol="label")
    
    # Stage 5: Estimator - Logistic Regression
    # We use multinomial logistic regression in case we have >2 classes.
    lr = LogisticRegression(maxIter=10, regParam=0.01, featuresCol="features", labelCol="label")
    
    # Combine stages into a Pipeline
    pipeline = Pipeline(stages=[tokenizer, hashing_tf, idf, label_indexer, lr])
    
    metadata = {
        "num_stages": 5,
        "estimator": "LogisticRegression",
        "feature_count": 1000
    }
    
    print(f"Pipeline created with {metadata['num_stages']} stages.")
    return pipeline, metadata


def train_and_evaluate_model(pipeline: Any, data: Any) -> Any:
    """
    Splits the data, trains the pipeline model, and evaluates its performance.
    
    Args:
        pipeline (Pipeline): The Spark ML Pipeline.
        data (DataFrame): The dataset to train and test on.
        
    Returns:
        PipelineModel: The fitted ML model.
    """
    print("Splitting data into training and test sets (80/20)...")
    # In distributed systems, random splits are deterministic if a seed is provided
    train_data, test_data = data.randomSplit([0.8, 0.2], seed=42)
    
    print("Training the ML model on the distributed cluster...")
    start_time = time.time()
    
    # Fitting the pipeline triggers Spark Actions, causing distributed execution
    model = pipeline.fit(train_data)
    
    end_time = time.time()
    print(f"Model training completed in {end_time - start_time:.4f} seconds.")
    
    print("Making predictions on the test set...")
    predictions = model.transform(test_data)
    
    # Show subset of columns to verify predictions
    print("Prediction Results:")
    predictions.select("id", "text", "category", "label", "prediction", "probability").show(truncate=False)
    
    print("Evaluating Model Accuracy...")
    evaluator = MulticlassClassificationEvaluator(
        labelCol="label", predictionCol="prediction", metricName="accuracy"
    )
    accuracy = evaluator.evaluate(predictions)
    print(f"Test Set Accuracy: {accuracy * 100:.2f}%\n")
    
    return model


def interview_challenge_distributed_word_count(spark: SparkSession) -> None:
    """
    Common Big Data Interview Challenge: Implement Word Count using Spark DataFrames.
    
    While traditional word count uses RDDs (map-reduce), modern Spark encourages
    using the DataFrame/SQL API for better optimization via Catalyst.
    
    Args:
        spark (SparkSession): Active SparkSession.
    """
    print("--- Interview Challenge: Distributed Word Count ---")
    print("Task: Count the frequency of each word in a corpus using DataFrame API.")
    
    # 1. Create a dummy corpus
    corpus = spark.createDataFrame([
        ("Spark is fast",),
        ("Spark is distributed",),
        ("Big Data with Spark is amazing",)
    ], ["sentence"])
    
    import pyspark.sql.functions as F
    
    # 2. Big-O Complexity:
    # Splitting words: O(N) where N is total characters.
    # Explode: O(W) where W is total words.
    # GroupBy + Count: Requires a Shuffle. Network Communication O(W). 
    #   Time Complexity: O(W * log(W)) or O(W) depending on hash vs sort aggregation.
    
    print("Executing operations: lowercasing -> splitting -> exploding -> grouping -> counting")
    word_counts = corpus \
        .select(F.explode(F.split(F.lower(F.col("sentence")), " ")).alias("word")) \
        .groupBy("word") \
        .count() \
        .orderBy(F.desc("count"))
    
    word_counts.show()
    print("Challenge completed successfully.\n")


def run_all() -> None:
    """
    Main orchestrator function that strings together the entire lesson.
    """
    print("========== Exploring SPARK MLLIB ==========\n")
    
    spark = initialize_spark_session()
    
    if spark is None:
        print("[NOTICE] Skipping execution of PySpark specific code because pyspark is not installed.")
        print("To run this lesson fully, install PySpark: pip install pyspark")
        return
        
    try:
        # 1. Prepare Data
        df = create_sample_data(spark)
        
        # 2. Build Pipeline
        pipeline, metadata = build_ml_pipeline()
        
        # 3. Train and Evaluate
        model = train_and_evaluate_model(pipeline, df)
        
        # 4. Interview Challenge
        interview_challenge_distributed_word_count(spark)
        
        print("Stopping Spark Session...")
        spark.stop()
        
    except Exception as e:
        print(f"An error occurred during PySpark execution: {e}")
        import traceback
        traceback.print_exc()

    print(f"========== END OF SPARK MLLIB LESSON ==========\n")


if __name__ == "__main__":
    run_all()
