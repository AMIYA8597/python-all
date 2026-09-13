"""
# 01 - Linear Algebra: Vectors and Embeddings

## A. Concept Name
Vectors, Vector Spaces, Dot Products, Norms, and Cosine Similarity.

## B. One-Sentence Definition
A vector is an ordered list of numbers that represents a point in a multidimensional space (or a magnitude and direction), serving as the fundamental data structure for all modern AI, including Neural Networks and LLM Embeddings.

## C. Why Does This Exist?
Computers cannot understand "words" or "images" directly. To make an AI understand the concept of a "Cat", we must translate the image or the word into an array of numbers (a Vector). Once data is converted into vectors, we can use Linear Algebra to calculate how similar two concepts are, or apply transformations to learn patterns. Linear algebra provides the mathematical rules for moving and comparing these numerical representations.

## D. Intuition & Real-World Analogy
Imagine a GPS coordinate: [Latitude, Longitude]. That is a 2-dimensional vector. 
If you want to know how far apart New York and London are, you calculate the distance between their two vectors.
Now imagine a coordinate system for meaning: [Fluffiness, Barking, Meowing]. 
A Dog might be [0.9, 1.0, 0.0]. 
A Cat might be [0.9, 0.0, 1.0].
By measuring the distance or angle between these two "meaning vectors" (Embeddings), an AI mathematically concludes that dogs and cats are somewhat similar (both fluffy), but distinct in their sounds.

## E. Core Mathematical Concepts

### 1. Vector Magnitude (L2 Norm)
The length of a vector from the origin (0,0).
Formula: `||v|| = sqrt(v1^2 + v2^2 + ... + vn^2)`
In AI: Used to normalize vectors so that we only compare their *direction* (meaning), ignoring their *magnitude* (e.g., how frequently a word appeared).

### 2. Dot Product
The sum of the products of corresponding entries of two vectors.
Formula: `A · B = (a1*b1) + (a2*b2) + ... + (an*bn)`
In AI: The dot product is the core engine of Neural Networks. A single neuron calculates `Weights · Inputs`. It measures how much two vectors "align".

### 3. Cosine Similarity
Measures the angle between two vectors, ranging from -1 (completely opposite) to 1 (exactly the same direction).
Formula: `cos(theta) = (A · B) / (||A|| * ||B||)`
In AI: This is how Vector Databases (like Pinecone, Milvus) and RAG (Retrieval-Augmented Generation) find documents that are semantically similar to your prompt.

## F. Common Mistakes & Anti-Patterns
1. **Confusing Python Lists with Math Vectors**: A Python `list` is just a container. If you do `[1, 2] + [3, 4]`, Python concatenates them into `[1, 2, 3, 4]`. To do vector addition `[4, 6]`, you MUST use NumPy arrays.
2. **Forgetting to Normalize before Dot Product**: If you use raw Dot Product to measure similarity, a very long vector (a very long document) might score higher simply because its numbers are bigger. Cosine Similarity divides by the magnitudes to fix this.

## G. Interview Connection
**Q: "Explain how a Vector Database retrieves similar documents for a RAG system."**
A: "Documents are passed through an embedding model which converts them into high-dimensional vectors (e.g., 768 or 1536 dimensions). These vectors are stored in the database. When a user asks a query, the query is also embedded into a vector. The database then calculates the Cosine Similarity (or Dot Product if normalized) between the query vector and all stored vectors, returning the K documents with the highest similarity scores."

## H. Implementation & Guided Practice
"""

import math
from typing import List

# ==========================================
# 1. From-Scratch Pure Python Implementation
# ==========================================
class VectorMath:
    @staticmethod
    def add(v1: List[float], v2: List[float]) -> List[float]:
        """Adds two vectors element-wise."""
        assert len(v1) == len(v2), "Vectors must be of the same dimension."
        return [x + y for x, y in zip(v1, v2)]

    @staticmethod
    def dot_product(v1: List[float], v2: List[float]) -> float:
        """Calculates the dot product."""
        assert len(v1) == len(v2), "Vectors must be of the same dimension."
        return sum(x * y for x, y in zip(v1, v2))

    @staticmethod
    def magnitude(v: List[float]) -> float:
        """Calculates the L2 Norm (length) of a vector."""
        return math.sqrt(sum(x**2 for x in v))

    @staticmethod
    def cosine_similarity(v1: List[float], v2: List[float]) -> float:
        """Calculates cosine similarity between -1.0 and 1.0."""
        dot = VectorMath.dot_product(v1, v2)
        mag_v1 = VectorMath.magnitude(v1)
        mag_v2 = VectorMath.magnitude(v2)
        
        if mag_v1 == 0 or mag_v2 == 0:
            return 0.0 # Prevent division by zero
            
        return dot / (mag_v1 * mag_v2)


# ==========================================
# 2. Industry Standard: NumPy
# ==========================================
import numpy as np

def demonstrate_numpy():
    """
    In production AI, we NEVER write raw loops for vector math. 
    We use NumPy, which runs heavily optimized C and Fortran code (BLAS/LAPACK) 
    using CPU vectorization (SIMD) to do this millions of times faster.
    """
    print("\n--- 2. NumPy Implementation (Production Standard) ---")
    
    # 1. Create vectors
    v1 = np.array([1.0, 2.0, 3.0])
    v2 = np.array([4.0, 5.0, 6.0])
    print(f"v1: {v1}, v2: {v2}")
    
    # 2. Vector Addition (Notice no loops! NumPy handles it)
    print(f"Addition: {v1 + v2}")
    
    # 3. Dot Product
    dot = np.dot(v1, v2)
    print(f"Dot Product: {dot}")
    
    # 4. Magnitude (Norm)
    mag = np.linalg.norm(v1)
    print(f"Magnitude of v1: {mag:.4f}")
    
    # 5. Cosine Similarity
    cos_sim = dot / (np.linalg.norm(v1) * np.linalg.norm(v2))
    print(f"Cosine Similarity: {cos_sim:.4f}")


# ==========================================
# 3. Real-World AI Application: Semantic Search
# ==========================================
def semantic_search_example():
    print("\n--- 3. AI Application: Semantic Search (Toy Example) ---")
    
    # Imagine a tiny embedding model outputted these 3-dimensional vectors for words
    # Dimensions might represent: [Pet-ness, Royalty, Fluffiness]
    word_embeddings = {
        "dog":   [0.9, 0.1, 0.8],
        "cat":   [0.9, 0.2, 0.9],
        "king":  [0.0, 0.9, 0.1],
        "queen": [0.0, 1.0, 0.2]
    }
    
    target_word = "puppy"
    target_vector = [0.9, 0.0, 0.9] # High pet-ness, high fluffiness
    
    print(f"Target word 'puppy' vector: {target_vector}")
    
    results = []
    for word, vector in word_embeddings.items():
        sim = VectorMath.cosine_similarity(target_vector, vector)
        results.append((word, sim))
        
    # Sort by similarity descending
    results.sort(key=lambda x: x[1], reverse=True)
    
    print("Search Results (Cosine Similarity):")
    for word, score in results:
        print(f" - {word}: {score:.4f}")
    
    print("\nNotice how 'dog' and 'cat' score very high, while 'king' and 'queen' score low!")


## I. Active Recall Questions
"""
1. Why do we prefer Cosine Similarity over Euclidean Distance for text embeddings?
   *Answer: Because document embeddings can have different magnitudes depending on document length or word frequencies. Cosine similarity only measures the ANGLE (the semantic direction), making it immune to magnitude differences.*
2. How does a single Artificial Neuron use the Dot Product?
   *Answer: A neuron receives an input vector `X` and holds a weight vector `W`. It calculates the dot product `X · W`, adds a bias, and passes the result through an activation function.*
3. What is the difference between `[1, 2] + [3, 4]` in standard Python vs NumPy?
   *Answer: Standard Python concatenates lists to `[1, 2, 3, 4]`. NumPy performs vector addition resulting in `[4, 6]`.*
"""

if __name__ == "__main__":
    print("========== LINEAR ALGEBRA: VECTORS MASTERCLASS ==========")
    
    print("\n--- 1. From-Scratch Python ---")
    vA = [1.0, 2.0, 3.0]
    vB = [4.0, 5.0, 6.0]
    print(f"vA: {vA}, vB: {vB}")
    print(f"Dot Product: {VectorMath.dot_product(vA, vB)}")
    print(f"Cosine Sim:  {VectorMath.cosine_similarity(vA, vB):.4f}")
    
    demonstrate_numpy()
    semantic_search_example()
    
    print("\n========== MASTERCLASS COMPLETE ==========")
