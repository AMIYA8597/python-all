"""
Module: 03-dask-ml
Description: Comprehensive textbook-grade interactive lesson on Dask-ML.

===========================================================================
DASK-ML: SCALABLE MACHINE LEARNING IN PYTHON
===========================================================================

Learning Objectives:
1. Understand the theoretical foundations of distributed machine learning.
2. Master Dask-ML estimators, transformers, and the Dask integration with Scikit-Learn.
3. Comprehend the mathematical underpinnings of block-wise operations and ADMM 
   (Alternating Direction Method of Multipliers) used in distributed optimization.
4. Implement hyperparameter tuning at scale using Dask.
5. Solve advanced data scaling challenges that exceed single-machine memory.
6. Evaluate algorithmic complexities (Big-O) in distributed contexts.

---------------------------------------------------------------------------
1. THEORETICAL BACKGROUND
---------------------------------------------------------------------------
Traditional machine learning tools (like scikit-learn) load data completely 
into RAM and execute algorithms that expect random access to the entire dataset. 
When data sizes exceed available memory (Big Data), we need a paradigm shift.

Dask provides two primary ways to scale machine learning:
a) Scaling Model Size (Compute Bound):
   When your model takes too long to train or hyperparameter tuning is too slow,
   Dask parallelizes the compute over a cluster using tools like `joblib` backend 
   for scikit-learn.

b) Scaling Data Size (Memory Bound):
   When your data doesn't fit in RAM, Dask-ML provides native estimators that
   work on Dask Arrays and Dask DataFrames (lazy, chunked data structures).

---------------------------------------------------------------------------
2. MATHEMATICAL FOUNDATIONS OF DISTRIBUTED OPTIMIZATION
---------------------------------------------------------------------------
Many ML algorithms (e.g., Linear/Logistic Regression) boil down to convex optimization.
To optimize a loss function L(w) over a dataset X that is split across M machines:

L(w) = (1/N) * SUM_{i=1}^N l(w; x_i, y_i) + lambda * R(w)

In Dask-ML, algorithms like ADMM or proximal gradient descent are used to 
distribute this computation. Dask-ML's Generalized Linear Models (GLMs) use
solvers like L-BFGS or ADMM.

ADMM splits the problem into local subproblems:
Minimize L_m(w_m) for each chunk m, subject to a consensus constraint w_m = z.
The update rules per iteration:
1. w_m^(k+1) = argmin_{w_m} { L_m(w_m) + (rho/2) || w_m - z^k + u_m^k ||_2^2 }
2. z^(k+1) = (1/M) SUM_{m=1}^M (w_m^(k+1) + u_m^k)
3. u_m^(k+1) = u_m^k + w_m^(k+1) - z^(k+1)

This allows each worker (chunk) to compute gradients and updates locally, 
exchanging only the parameter vectors w_m, dramatically reducing network I/O.

---------------------------------------------------------------------------
3. BIG-O COMPLEXITY IN DISTRIBUTED CONTEXTS
---------------------------------------------------------------------------
Consider a dataset with N samples and D features, distributed across W workers.
- Traditional OLS closed-form: O(N * D^2 + D^3)
- Distributed OLS (Block matrix multiplication):
  Each worker computes X_m^T X_m in O((N/W) * D^2).
  Reduction step: sum M matrices of size DxD in O(W * D^2).
  Inversion step: O(D^3) on the head node.
  Total Time: O((N/W)*D^2 + W*D^2 + D^3).

Network Communication Overhead:
O(W * D) per gradient step for iterative solvers. 
Dask minimizes this overhead through tree-reductions.

---------------------------------------------------------------------------
4. REAL-WORLD APPLICATIONS
---------------------------------------------------------------------------
- Ad-Tech: Predicting Click-Through Rates (CTR) on terabytes of event logs.
- Finance: Training fraud detection models on massive transaction histories.
- E-commerce: Grid searching hyperparameter spaces across hundreds of models.
"""

import sys
import time
import math
import random
import logging
import warnings
from typing import List, Dict, Any, Tuple, Optional, Callable

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
warnings.filterwarnings('ignore')

# Try importing Dask and related ML libraries
try:
    import numpy as np
    import pandas as pd
    import dask
    import dask.array as da
    import dask.dataframe as dd
    from dask.distributed import Client, LocalCluster
    import joblib
    from sklearn.datasets import make_classification, make_regression
    from sklearn.linear_model import LogisticRegression, LinearRegression
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.model_selection import train_test_split as sklearn_train_test_split
    from sklearn.metrics import accuracy_score, mean_squared_error
    
    # Try importing Dask-ML (might not be installed in all environments, so we gracefully degrade)
    try:
        import dask_ml
        import dask_ml.datasets
        import dask_ml.cluster
        from dask_ml.linear_model import LogisticRegression as DaskLogisticRegression
        from dask_ml.model_selection import train_test_split, GridSearchCV
        from dask_ml.preprocessing import StandardScaler, CategoricalEncoder
        from dask_ml.wrappers import Incremental
        DASK_ML_AVAILABLE = True
    except ImportError:
        DASK_ML_AVAILABLE = False
        logging.warning("dask_ml package is not installed. Some examples will be mocked or skipped.")

    LIBRARIES_AVAILABLE = True
except ImportError as e:
    LIBRARIES_AVAILABLE = False
    logging.error(f"Required libraries are not fully installed: {e}")
    logging.info("Please install: pip install numpy pandas scikit-learn dask[complete] dask-ml")


# ==============================================================================
# SECTION 1: DASK CLIENT & CLUSTER MANAGEMENT
# ==============================================================================

def setup_dask_cluster() -> Optional["Client"]:
    """
    Sets up a local Dask cluster. In a real-world scenario, you might connect
    to an external cluster (e.g., Kubernetes, YARN, AWS ECS).
    
    Returns:
        Client: A connected Dask Client, or None if imports failed.
    """
    if not LIBRARIES_AVAILABLE:
        return None
        
    print("\n" + "="*50)
    print("INITIALIZING DASK DISTRIBUTED CLIENT")
    print("="*50)
    
    try:
        # We start a LocalCluster. It creates workers on the local machine.
        # For heavy ML workloads, you can restrict the number of threads per worker
        # to prevent thread contention with NumPy/BLAS.
        cluster = LocalCluster(
            n_workers=2, 
            threads_per_worker=2,
            memory_limit='2GB'  # Artificial limit for demonstration
        )
        client = Client(cluster)
        print(f"Dask Client running at: {client.dashboard_link}")
        print(client)
        return client
    except Exception as e:
        print(f"Failed to start Dask cluster: {e}")
        return None


# ==============================================================================
# SECTION 2: SCALING COMPUTE WITH SCOKIT-LEARN & JOBLIB
# ==============================================================================

def parallel_hyperparameter_tuning(client: "Client") -> None:
    """
    Demonstrates how Dask can scale compute-bound tasks, specifically 
    hyperparameter tuning in scikit-learn, using the joblib backend.
    
    Complexity Analysis:
    - Normal GridSearch: O(K * F * T(N, D)) where K is hyperparameter combinations, 
      F is folds, and T() is training time.
    - Dask GridSearch: O(K * F * T(N, D) / W) where W is number of workers.
    """
    print("\n" + "-"*50)
    print("SCALING COMPUTE: Dask + scikit-learn (Joblib Backend)")
    print("-"*50)
    
    if not LIBRARIES_AVAILABLE:
        print("Libraries not available. Skipping.")
        return

    # 1. Create a medium-sized dataset that fits in memory
    print("Generating synthetic data...")
    X, y = make_classification(n_samples=5000, n_features=20, random_state=42)
    
    # 2. Define a traditional scikit-learn model and grid search
    from sklearn.model_selection import GridSearchCV as SklearnGridSearchCV
    from sklearn.svm import SVC
    
    param_grid = {
        'C': [0.1, 1, 10, 50],
        'gamma': [0.001, 0.01, 0.1, 1],
        'kernel': ['rbf']
    }
    
    svc = SVC()
    grid_search = SklearnGridSearchCV(svc, param_grid, cv=3, n_jobs=-1) # Normally n_jobs=-1 uses local cores
    
    print(f"Parameter grid space size: {len(param_grid['C']) * len(param_grid['gamma'])} combinations")
    
    # 3. Train using Dask's joblib backend
    # This automatically distributes the independent CV fits across the Dask cluster.
    print("Training GridSearchCV distributedly via joblib + dask backend...")
    start_time = time.time()
    
    with joblib.parallel_backend('dask'):
        grid_search.fit(X, y)
        
    end_time = time.time()
    print(f"Best parameters: {grid_search.best_params_}")
    print(f"Best cross-validation score: {grid_search.best_score_:.4f}")
    print(f"Time taken (distributed): {end_time - start_time:.2f} seconds")
    print("Note: The true speedup is visible on much larger datasets and external clusters.")


# ==============================================================================
# SECTION 3: SCALING DATA WITH DASK-ML
# ==============================================================================

def distributed_data_modeling() -> None:
    """
    Demonstrates training models on datasets that are partitioned across 
    workers (out-of-core / distributed datasets).
    """
    print("\n" + "-"*50)
    print("SCALING DATA: Dask-ML Estimators on Dask Arrays")
    print("-"*50)
    
    if not LIBRARIES_AVAILABLE or not DASK_ML_AVAILABLE:
        print("dask_ml not available. Skipping Dask-ML specific example.")
        return

    # 1. Generate large chunked synthetic data
    # In reality, this would be `dd.read_parquet('s3://my-bucket/massive_data.parquet')`
    print("Generating 1,000,000 rows of chunked synthetic data...")
    X, y = dask_ml.datasets.make_classification(
        n_samples=1_000_000,
        n_features=20,
        chunks=100_000, # Each chunk is 100k rows
        random_state=42
    )
    
    print(f"X dask array:\n{X}")
    print(f"Total size in memory if realized: {X.nbytes / 1e6:.2f} MB")
    print(f"Chunk size: {X.blocks[0].nbytes / 1e6:.2f} MB per block")
    
    # 2. Split data lazily
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    
    # 3. Define and train a Dask-ML Logistic Regression model
    # This uses ADMM (Alternating Direction Method of Multipliers) or L-BFGS
    # designed specifically for chunked data.
    lr = DaskLogisticRegression(
        penalty='l2', 
        solver='admm',
        max_iter=10
    )
    
    print("\nTraining Distributed Logistic Regression (ADMM solver)...")
    start_time = time.time()
    
    # .fit() triggers the lazy computation graph
    lr.fit(X_train, y_train)
    
    end_time = time.time()
    print(f"Training complete in {end_time - start_time:.2f} seconds.")
    print(f"Learned Coefficients (first 5): {lr.coef_[0][:5]}")
    
    # 4. Predict and evaluate lazily
    print("Evaluating model...")
    y_pred = lr.predict(X_test)
    
    # We must explicitly compute the score as accuracy_score requires materialization
    # Dask-ML's accuracy_score handles dask arrays natively if dask_ml.metrics is used,
    # but here we show a standard approach using compute().
    from dask_ml.metrics import accuracy_score as dask_accuracy
    acc = dask_accuracy(y_test, y_pred)
    
    print(f"Test Accuracy: {acc:.4f}")


# ==============================================================================
# SECTION 4: INCREMENTAL LEARNING FOR MASSIVE DATA
# ==============================================================================

def incremental_learning_example() -> None:
    """
    Demonstrates incremental learning (partial_fit) using Dask-ML wrappers.
    This is useful for online learning or when algorithms support streaming data
    (like SGDClassifier, MiniBatchKMeans).
    """
    print("\n" + "-"*50)
    print("INCREMENTAL LEARNING: dask_ml.wrappers.Incremental")
    print("-"*50)
    
    if not LIBRARIES_AVAILABLE or not DASK_ML_AVAILABLE:
        print("dask_ml not available. Skipping Incremental Learning example.")
        return
        
    from sklearn.linear_model import SGDClassifier
    from dask_ml.wrappers import Incremental
    
    # 1. Generate chunked data
    X, y = dask_ml.datasets.make_classification(
        n_samples=500_000,
        n_features=15,
        chunks=50_000,
        random_state=99
    )
    
    # 2. Wrap a scikit-learn estimator that supports `partial_fit`
    # Incremental wrapper will sequentially pass chunks of Dask arrays to the 
    # underlying scikit-learn estimator's partial_fit method.
    estimator = SGDClassifier(random_state=42, loss='log_loss', penalty='l2')
    inc = Incremental(estimator, scoring='accuracy')
    
    print("Training via Incremental Wrapper (SGD partial_fit over chunks)...")
    start_time = time.time()
    
    # Note: we need to specify classes for partial_fit to know the full target space
    inc.fit(X, y, classes=[0, 1])
    
    end_time = time.time()
    print(f"Incremental training finished in {end_time - start_time:.2f} seconds.")
    print(f"Wrapped estimator coef_: {inc.estimator_.coef_[0][:5]}")


# ==============================================================================
# SECTION 5: DISTRIBUTED PREPROCESSING
# ==============================================================================

def distributed_preprocessing() -> None:
    """
    Shows how to scale standard preprocessing tasks (like scaling, encoding)
    across a cluster using Dask DataFrames.
    """
    print("\n" + "-"*50)
    print("DISTRIBUTED PREPROCESSING: Dask DataFrames & Scalers")
    print("-"*50)
    
    if not LIBRARIES_AVAILABLE or not DASK_ML_AVAILABLE:
        print("dask_ml not available. Skipping Preprocessing example.")
        return

    # Create a synthetic Pandas DataFrame and convert to Dask DataFrame
    print("Creating Dask DataFrame...")
    pdf = pd.DataFrame({
        'age': np.random.randint(18, 80, size=100000),
        'salary': np.random.lognormal(mean=10, sigma=1, size=100000),
        'city': np.random.choice(['NY', 'LA', 'SF', 'CHI'], size=100000)
    })
    
    ddf = dd.from_pandas(pdf, npartitions=4)
    print(f"Dask DataFrame Partitions: {ddf.npartitions}")
    
    # 1. Dask-ML StandardScaler
    print("\nApplying Distributed StandardScaler...")
    scaler = StandardScaler()
    
    # We select numerical columns
    num_cols = ['age', 'salary']
    
    # Fit computes the mean and variance across partitions via map-reduce
    scaler.fit(ddf[num_cols])
    print(f"Computed Means: {scaler.mean_}")
    print(f"Computed Variances: {scaler.var_}")
    
    # Transform scales the data lazily
    scaled_ddf = scaler.transform(ddf[num_cols])
    
    print("First 5 scaled rows:")
    print(scaled_ddf.head(5))
    
    # 2. Categorical Encoding
    # Dask-ML's DummyEncoder scales pd.get_dummies
    from dask_ml.preprocessing import DummyEncoder
    print("\nApplying Distributed DummyEncoder...")
    
    # Needs categorical dtypes
    ddf = ddf.categorize(columns=['city'])
    encoder = DummyEncoder()
    encoded_ddf = encoder.fit_transform(ddf[['city']])
    
    print("First 5 encoded categorical rows:")
    print(encoded_ddf.head(5))


# ==============================================================================
# SECTION 6: ALGORITHMIC IMPLEMENTATION CHALLENGE
# ==============================================================================

def implement_map_reduce_mean() -> None:
    """
    INTERVIEW CHALLENGE:
    Implement a simple "Map-Reduce" style algorithm to calculate the mean 
    of a massive distributed dataset without loading it entirely into memory.
    
    This illustrates the core concept behind how Dask-ML calculates statistics
    on distributed arrays.
    
    Mathematical Foundation:
    Mean = Sum(x) / Count(x)
    For partitions P_1...P_k:
    Sum_total = Sum_1 + Sum_2 + ... + Sum_k
    Count_total = N_1 + N_2 + ... + N_k
    Mean = Sum_total / Count_total
    """
    print("\n" + "-"*50)
    print("INTERVIEW CHALLENGE: Map-Reduce Mean")
    print("-"*50)
    
    # Mock partitions representing data chunks on different nodes
    partitions = [
        [10, 20, 30],         # Node 1
        [15, 25, 35, 45, 55], # Node 2
        [100, 200],           # Node 3
        [1, 2, 3, 4]          # Node 4
    ]
    
    print(f"Partitions: {partitions}")
    
    # --- Map Step ---
    # Each node calculates the sum and count of its own data locally
    def map_func(chunk: List[int]) -> Tuple[float, int]:
        """Calculates (sum, count) for a chunk."""
        return sum(chunk), len(chunk)
    
    print("Executing Map phase...")
    map_results = [map_func(chunk) for chunk in partitions]
    print(f"Map Results (sum, count) per partition: {map_results}")
    
    # --- Reduce Step ---
    # Head node aggregates the local sums and counts
    def reduce_func(mapped_data: List[Tuple[float, int]]) -> float:
        """Aggregates intermediate results to find global mean."""
        total_sum = 0.0
        total_count = 0
        for s, c in mapped_data:
            total_sum += s
            total_count += c
            
        if total_count == 0:
            return 0.0
        return total_sum / total_count
        
    print("Executing Reduce phase...")
    global_mean = reduce_func(map_results)
    
    print(f"Global Mean Calculated: {global_mean}")
    
    # Verify against flattened data
    flat_data = [item for sublist in partitions for item in sublist]
    true_mean = sum(flat_data) / len(flat_data)
    print(f"True Mean (flattened): {true_mean}")
    assert math.isclose(global_mean, true_mean), "Map-Reduce Mean logic failed!"
    print("Map-Reduce Mean successfully validated.")


# ==============================================================================
# SECTION 7: TESTING & VALIDATION
# ==============================================================================

def run_comprehensive_tests() -> None:
    """
    Runs automated tests to validate the mocked structures and core logic.
    """
    print("\n" + "-"*50)
    print("RUNNING UNIT TESTS")
    print("-"*50)
    
    # Test Map-Reduce Challenge logic in isolation
    def mock_map(c: List[int]) -> Tuple[int, int]: return sum(c), len(c)
    def mock_reduce(m: List[Tuple[int, int]]) -> float: 
        return sum(x[0] for x in m) / sum(x[1] for x in m)
        
    assert mock_reduce([mock_map([1,2,3]), mock_map([4,5,6])]) == 3.5, "Map Reduce failed"
    print("[PASS] Custom Map-Reduce Test")
    
    if LIBRARIES_AVAILABLE:
        # Test Dask Array Lazy evaluation properties
        a = da.ones((100, 100), chunks=(50, 50))
        assert a.npartitions == 4, "Dask Array partitioning logic failed"
        assert a.sum().compute() == 10000, "Dask Array reduction failed"
        print("[PASS] Dask Array Mechanics")
        
    print("All tests passed successfully.")


# ==============================================================================
# MAIN EXECUTION
# ==============================================================================

def main():
    print("=======================================================================")
    print(" DASK-ML INTERACTIVE LESSON: SCALABLE MACHINE LEARNING")
    print("=======================================================================")
    
    client = setup_dask_cluster()
    
    try:
        # 1. Scale Scikit-Learn Compute via Dask backend
        parallel_hyperparameter_tuning(client)
        
        # 2. Distribute large datasets natively with Dask-ML
        distributed_data_modeling()
        
        # 3. Handle streams of massive chunks incrementally
        incremental_learning_example()
        
        # 4. Distributed Data Preprocessing
        distributed_preprocessing()
        
        # 5. Core algorithmic logic for Big Data
        implement_map_reduce_mean()
        
        # 6. Run verification
        run_comprehensive_tests()
        
    finally:
        if client:
            print("\nClosing Dask Client and shutting down local cluster...")
            client.close()
            
    print("\n=======================================================================")
    print(" END OF DASK-ML LESSON")
    print("=======================================================================")

if __name__ == "__main__":
    main()
