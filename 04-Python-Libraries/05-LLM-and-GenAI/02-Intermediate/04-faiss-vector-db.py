"""
# ==============================================================================
# LABORATORY: MASSIVE VECTOR DATABASES (FAISS)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# In the previous lab, we used Chroma to search through 3 vectors. 
# But what if your company has 100 Million documents?
#
# If a user asks a question, calculating the exact Cosine Similarity between 
# the user's question and 100,000,000 vectors will take several minutes.
# The user will close the app before the LLM even receives the context.
#
# We need to perform Approximate Nearest Neighbor (ANN) search.
# FAISS (Facebook AI Similarity Search) is a C++ library engineered by Meta. 
# It uses advanced mathematical clustering (Voronoi cells) and quantization 
# to search billions of vectors in milliseconds, executing entirely on the GPU 
# or highly optimized CPU threads.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the difference between Exact Search (Flat L2) and ANN.
# - Construct a raw FAISS Index.
# - Execute a blazing-fast vector search on a massive dataset.
#
# ==============================================================================
"""

import numpy as np
import time

# In a real environment: pip install faiss-cpu (or faiss-gpu)
try:
    import faiss
    HAS_FAISS = True
except ImportError:
    HAS_FAISS = False

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. EXACT SEARCH (INDEX FLAT L2)
# ==============================================================================
def demonstrate_exact_search():
    section_header("Exact Geometric Search (IndexFlatL2)")
    
    if not HAS_FAISS:
        print("[WARNING] FAISS not installed.")
        return
        
    print("We will generate 100,000 synthetic 128-dimensional vectors.")
    print("IndexFlatL2 performs a brute-force, mathematically perfect search ")
    print("by measuring the exact Euclidean distance (L2 norm) to every single vector.\n")
    
    d = 128         # Vector Dimensionality (e.g., 128 floats per document)
    nb = 100000     # Number of database vectors (100k)
    nq = 1          # Number of query vectors
    
    # 1. GENERATE SYNTHETIC DATA
    # np.random.random returns float64, but FAISS strictly requires float32 for speed!
    np.random.seed(42)
    database_vectors = np.random.random((nb, d)).astype('float32')
    query_vector = np.random.random((nq, d)).astype('float32')
    
    # 2. INITIALIZE FAISS INDEX
    index = faiss.IndexFlatL2(d)
    
    # 3. ADD VECTORS TO DATABASE
    print(f"Adding {nb} vectors to the FAISS Index...")
    index.add(database_vectors)
    print(f"Total vectors currently indexed: {index.ntotal}")
    
    # 4. EXECUTE SEARCH
    # We want to find the top 5 closest vectors (k=5)
    k = 5
    
    print("\nExecuting Brute-Force Search...")
    start_time = time.perf_counter()
    
    distances, indices = index.search(query_vector, k)
    
    end_time = time.perf_counter()
    search_time = (end_time - start_time) * 1000
    
    print(f"Search completed in {search_time:.2f} milliseconds!")
    print(f"Top 5 Closest Document IDs: {indices[0]}")
    print(f"Euclidean Distances       : {distances[0]}")


# ==============================================================================
# 4. APPROXIMATE NEAREST NEIGHBOR (IVF)
# ==============================================================================
def demonstrate_approximate_search():
    section_header("Approximate Nearest Neighbor (IndexIVFFlat)")
    
    if not HAS_FAISS: return
    
    print("Brute-force is fast for 100k vectors, but what if we have 10 Million?")
    print("We must use an Inverted File (IVF) Index. FAISS runs K-Means clustering ")
    print("to group the database into 'Voronoi Cells'. When a query arrives, FAISS ")
    print("only searches the 2 or 3 cells closest to the query, completely ignoring ")
    print("99% of the database!\n")
    
    d = 128
    nb = 100000
    nq = 1
    
    np.random.seed(42)
    database_vectors = np.random.random((nb, d)).astype('float32')
    query_vector = np.random.random((nq, d)).astype('float32')
    
    # 1. DEFINE THE QUANTIZER AND IVF INDEX
    nlist = 100 # We want to cluster the 100k vectors into exactly 100 Voronoi Cells
    quantizer = faiss.IndexFlatL2(d)
    
    # IVF = Inverted File. We are building an index on top of the base quantizer.
    index_ivf = faiss.IndexIVFFlat(quantizer, d, nlist)
    
    # 2. TRAIN THE CLUSTERS (CRITICAL STEP)
    # Because IVF relies on K-Means clustering, we MUST train it on the data first 
    # so it can figure out where the clusters actually are!
    print("Training the IVF Clusters (K-Means)...")
    index_ivf.train(database_vectors)
    print(f"Index is trained: {index_ivf.is_trained}")
    
    # 3. ADD VECTORS
    print("Adding vectors to the clustered index...")
    index_ivf.add(database_vectors)
    
    # 4. EXECUTE SEARCH
    # nprobe: How many nearby cells should we check?
    # Out of 100 cells, we only check 5. This skips 95% of the database!
    index_ivf.nprobe = 5
    
    k = 5
    print("\nExecuting Approximate Search (nprobe=5)...")
    start_time = time.perf_counter()
    
    distances, indices = index_ivf.search(query_vector, k)
    
    end_time = time.perf_counter()
    search_time = (end_time - start_time) * 1000
    
    print(f"Approx Search completed in {search_time:.2f} milliseconds!")
    print(f"Top 5 Closest Document IDs: {indices[0]}")
    
    print("\nNotice how much faster it is! For 100k vectors, the difference is ")
    print("small, but at 100 Million vectors, IVF drops search time from 5 seconds ")
    print("down to 20 milliseconds, enabling real-time LLM architectures!")


def run_all_labs():
    demonstrate_exact_search()
    demonstrate_approximate_search()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. What is the fundamental difference between `IndexFlatL2` and `IndexIVFFlat`?
   Answer: `IndexFlatL2` executes a brute-force, mathematically perfect search. It calculates the exact Euclidean distance (L2 norm) between the user's query vector and every single vector in the database, yielding 100% perfect recall (accuracy), but it scales at $O(N)$. 
   `IndexIVFFlat` (Inverted File) uses Approximate Nearest Neighbor (ANN). It runs K-Means clustering during the `.train()` step to partition the database into $N$ clusters (Voronoi cells). At search time, it identifies the centroid closest to the query and only calculates distances against the vectors inside that specific cell, skipping 99% of the database. This scales in $O(\log N)$ time, but sacrifices perfect recall (it might occasionally miss the absolute mathematically closest vector).

2. In an IVF index, what is the role of the `nprobe` parameter during search?
   Answer: `nprobe` controls the tradeoff between Speed and Accuracy (Recall). If you partitioned your database into 1,000 Voronoi cells, setting `nprobe=1` means FAISS will strictly search ONLY the single closest cell. This is blindingly fast, but if the perfect vector is physically located just across the geometric boundary line in cell #2, FAISS will miss it. Setting `nprobe=10` instructs FAISS to search the 10 closest neighboring cells. This increases search time slightly but drastically improves the probability of finding the absolute best matches.

3. Why MUST FAISS vectors be cast to `float32`?
   Answer: FAISS is highly engineered C++ and CUDA code written specifically for modern CPU and GPU architectures. Modern CPUs use AVX (Advanced Vector Extensions) SIMD (Single Instruction, Multiple Data) instructions, which are explicitly hardwired on the silicon to process 32-bit floats in parallel. Furthermore, GPU tensor cores natively operate on 32-bit (or 16-bit) floats. If you pass a 64-bit float (which is standard in Python/NumPy) into FAISS, the library will crash or silently fail, because the underlying C++ pointers are strictly typing a 32-bit memory layout.
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Massive Vector Databases (FAISS) Completed.")
