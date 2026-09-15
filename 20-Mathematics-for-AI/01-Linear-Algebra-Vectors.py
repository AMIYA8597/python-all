"""
# ==============================================================================
# LABORATORY: MATHEMATICS FOR AI (LINEAR ALGEBRA & VECTORS)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A junior developer tries to build a search engine by checking if "dog" is in 
# a sentence. If the user searches for "puppy", the search fails. 
#
# A senior AI engineer understands "Vector Geometry". They map every word into 
# a 300-dimensional coordinate space. "Dog" is mathematically placed at [0.5, 0.2, ...]. 
# "Puppy" is mathematically placed at [0.49, 0.21, ...]. By calculating the 
# Angle (Cosine Similarity) between the two Vectors, the engineer mathematically 
# proves they mean the same thing, despite having zero overlapping letters. 
# AI is just Geometry in high dimensions.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master High-Dimensional Vector mathematics.
# - Execute Vector Magnitudes (L2 Norm).
# - Architect Cosine Similarity (Dot Product over Magnitudes).
#
# ==============================================================================
"""

import numpy as np

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE BUSINESS LOGIC (VECTOR MATHEMATICS)
# ==============================================================================
class VectorSpace:
    
    @staticmethod
    def calculate_magnitude():
        """
        [SECURE] The L2 Norm (Euclidean Length).
        Formula: ||v|| = sqrt(v1^2 + v2^2 + ... + vn^2)
        """
        print("  [INIT] Calculating Vector Magnitude...")
        
        # A 3-dimensional vector (e.g., [x, y, z])
        v = np.array([3.0, 4.0, 0.0])
        print(f"  -> Vector V: {v}")
        
        # Manual calculation
        manual_norm = np.sqrt(v[0]**2 + v[1]**2 + v[2]**2)
        
        # NumPy calculation
        np_norm = np.linalg.norm(v)
        
        print(f"  -> Manual Magnitude: {manual_norm}")
        print(f"  -> NumPy Magnitude:  {np_norm}")
        print("  [FLAWLESS] The length of the vector in space is exactly 5.0 (Pythagorean Theorem).")

    @staticmethod
    def calculate_cosine_similarity():
        """
        [SECURE] The Cosine Similarity.
        Formula: cos(theta) = (A dot B) / (||A|| * ||B||)
        Used universally in RAG, Vector Databases, and LLMs.
        """
        print("\n  [INIT] Calculating Cosine Similarity (Semantic Angle)...")
        
        # Imagine these are Word Embeddings (Coordinates in Space)
        vector_dog = np.array([0.8, 0.2, 0.1])
        vector_puppy = np.array([0.7, 0.3, 0.1])
        vector_car = np.array([0.1, 0.0, 0.9])
        
        # 1. The Dot Product (Numerator)
        dot_dog_puppy = np.dot(vector_dog, vector_puppy)
        dot_dog_car = np.dot(vector_dog, vector_car)
        
        # 2. The Magnitudes (Denominator)
        norm_dog = np.linalg.norm(vector_dog)
        norm_puppy = np.linalg.norm(vector_puppy)
        norm_car = np.linalg.norm(vector_car)
        
        # 3. The Final Cosine Similarity
        # Range is -1.0 (Opposite) to 1.0 (Identical)
        sim_puppy = dot_dog_puppy / (norm_dog * norm_puppy)
        sim_car = dot_dog_car / (norm_dog * norm_car)
        
        print(f"  -> Similarity (Dog vs Puppy): {sim_puppy:.4f} (Highly Semantic)")
        print(f"  -> Similarity (Dog vs Car):   {sim_car:.4f} (Orthogonal / Unrelated)")
        
        print("\n  [MATHEMATICAL PROOF] The geometry perfectly maps human semantic meaning.")
        print("  'Dog' and 'Puppy' point in almost the exact same mathematical direction.")


# ==============================================================================
# 4. MATHEMATICAL PROOF (THE BENCHMARK)
# ==============================================================================
def demonstrate_vectors():
    section_header("Mathematics for AI: Vectors")
    
    space = VectorSpace()
    space.calculate_magnitude()
    space.calculate_cosine_similarity()


def run_all_labs():
    demonstrate_vectors()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "Why do we use Cosine Similarity instead of Euclidean Distance to measure text similarity in LLMs?"
   Senior Answer: "Magnitude Independence. Euclidean distance measures the absolute physical distance between two points in space. If a document about 'Dogs' is 10,000 words long, and another document about 'Dogs' is 50 words long, their vectors will have vastly different Magnitudes (Lengths). Euclidean distance will say they are extremely far apart. Cosine Similarity entirely ignores the length of the vectors and only measures the 'Angle' between them. Because both documents point in the 'Dog' direction, Cosine Similarity correctly identifies them as semantically identical, regardless of document length."

2. Interviewer: "Explain the mathematical concept of 'Orthogonality' in a Vector Database."
   Senior Answer: "Zero Correlation. If two vectors are orthogonal, they intersect at exactly a 90-degree angle. Mathematically, the Dot Product of two orthogonal vectors evaluates precisely to $0.0$. In semantic AI space, if the vector for 'Quantum Physics' and the vector for 'Baking a Cake' have a dot product of $0.0$, the Neural Network mathematically proves that these two concepts share absolutely zero semantic overlap. They are statistically independent dimensions."

3. Interviewer: "What is the computational complexity of querying a Vector Database, and how do we solve the bottleneck?"
   Senior Answer: "The Exact K-Nearest Neighbors (KNN) Bottleneck. To find the most similar document to a user's query, you must mathematically calculate the Dot Product between the query vector and *every single document vector in the database* (e.g., $O(N)$). If you have 1 Billion vectors, calculating 1 Billion Dot Products per search is computationally impossible. We solve this using ANN (Approximate Nearest Neighbors) algorithms like HNSW (Hierarchical Navigable Small World graphs), which navigate probabilistic layers to find the closest vector in $O(log N)$ time, sacrificing $1\\%$ accuracy for a $1000\\times$ speedup."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Mathematics for AI (Vectors) Completed.")
