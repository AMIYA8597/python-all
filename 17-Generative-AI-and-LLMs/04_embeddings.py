"""
# ==============================================================================
# LABORATORY: GENERATIVE AI (VECTOR EMBEDDINGS & COSINE SIMILARITY)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A junior developer tries to build a Search Engine using Keyword matching (SQL 
# `LIKE '%apple%'`). If a user searches for "Macbook", the system returns zero 
# results because the exact string "apple" was not found.
#
# A senior AI engineer builds a Semantic Search Engine. They run the database 
# through an Embedding Model, converting every text snippet into a 1536-dimensional 
# Float Vector. They convert the user's search query ("Macbook") into a vector. 
# They mathematically calculate the Cosine Similarity (the angle between the vectors). 
# Because "Macbook" and "Apple" mathematically point in the exact same geometric 
# direction in 1536-dimensional space, the search perfectly retrieves the result.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master High-Dimensional Vector mathematics.
# - Execute Cosine Similarity distance calculations.
# - Architect Semantic Clustering logic.
#
# ==============================================================================
"""

import numpy as np

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE BUSINESS LOGIC (COSINE SIMILARITY)
# ==============================================================================
class EmbeddingSimulator:
    
    @staticmethod
    def cosine_similarity(vector_a: np.ndarray, vector_b: np.ndarray) -> float:
        """
        [SECURE] Cosine Similarity Formula.
        Calculates the cosine of the angle between two multi-dimensional vectors.
        Formula: (A dot B) / (||A|| * ||B||)
        Result ranges from -1.0 (Opposite) to 1.0 (Identical).
        """
        dot_product = np.dot(vector_a, vector_b)
        
        # Calculate the Magnitude (Length) of each vector using the Pythagorean theorem
        norm_a = np.linalg.norm(vector_a)
        norm_b = np.linalg.norm(vector_b)
        
        # Prevent division by zero
        if norm_a == 0.0 or norm_b == 0.0:
            return 0.0
            
        similarity = dot_product / (norm_a * norm_b)
        return similarity

    def simulate_semantic_search(self):
        print("  [INIT] Simulating 5-Dimensional Semantic Word Embeddings...")
        
        # In a real model (like text-embedding-ada-002), these would be length 1536!
        # Here we manually construct 5-D vectors to prove the geometry.
        # Dimensions conceptually represent: [Tech, Fruit, Animal, Royal, Vehicle]
        
        embeddings = {
            "apple_company": np.array([0.9, 0.1, 0.0, 0.0, 0.0]),
            "macbook":       np.array([0.95, 0.0, 0.0, 0.0, 0.1]),
            "apple_fruit":   np.array([0.0, 0.9, 0.0, 0.0, 0.0]),
            "banana":        np.array([0.0, 0.95, 0.0, 0.0, 0.0]),
            "king":          np.array([0.0, 0.0, 0.0, 0.9, 0.0]),
            "queen":         np.array([0.0, 0.0, 0.0, 0.95, 0.0])
        }
        
        print("\n  [EXECUTION] Calculating Semantic Distances (Cosine Similarity)...")
        
        # Test 1: Similar Tech Concepts
        sim_tech = self.cosine_similarity(embeddings["apple_company"], embeddings["macbook"])
        print(f"  -> Similarity ('Apple Company' vs 'Macbook'):  {sim_tech:.4f}  (High!)")
        
        # Test 2: Similar Fruit Concepts
        sim_fruit = self.cosine_similarity(embeddings["apple_fruit"], embeddings["banana"])
        print(f"  -> Similarity ('Apple Fruit' vs 'Banana'):     {sim_fruit:.4f}  (High!)")
        
        # Test 3: The Disambiguation Test (Lexical vs Semantic)
        sim_lexical = self.cosine_similarity(embeddings["apple_company"], embeddings["apple_fruit"])
        print(f"  -> Similarity ('Apple Company' vs 'Apple Fruit'): {sim_lexical:.4f}  (Low!)")
        
        # Test 4: Completely Unrelated Concepts
        sim_random = self.cosine_similarity(embeddings["macbook"], embeddings["queen"])
        print(f"  -> Similarity ('Macbook' vs 'Queen'):          {sim_random:.4f}  (Zero!)")
        
        print("\n  -> [MATHEMATICAL PROOF] The lexical string 'apple' means nothing to the ")
        print("     mathematics. The vectors successfully disambiguated the Tech Company ")
        print("     from the Fruit based purely on their geometric direction in space.")


# ==============================================================================
# 4. MATHEMATICAL PROOF (THE BENCHMARK)
# ==============================================================================
def demonstrate_embeddings():
    section_header("Generative AI: Vector Embeddings")
    
    sim = EmbeddingSimulator()
    sim.simulate_semantic_search()


def run_all_labs():
    demonstrate_embeddings()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "Why do we use Cosine Similarity instead of Euclidean Distance to measure semantic similarity between two Embeddings?"
   Senior Answer: "Magnitude Independence. Euclidean Distance (the straight-line physical distance between two points in space) is heavily influenced by the *magnitude* (length) of the vectors. If a document mentions the word 'Dog' $50$ times, its vector will be physically very long. If another document mentions 'Dog' $2$ times, its vector is physically short. Their Euclidean distance will be massive, implying they are unrelated. However, Cosine Similarity strictly measures the *angle* between the two vectors, completely ignoring their length. Because both vectors point in the exact same geometric direction (the 'Dog' semantic cluster), Cosine Similarity will evaluate to $1.0$ (perfect match). In NLP, we care about the direction of meaning, not the frequency magnitude."

2. Interviewer: "What is the computational bottleneck of a Vector Database, and how does HNSW (Hierarchical Navigable Small World) solve it?"
   Senior Answer: "The Exhaustive K-Nearest Neighbors (KNN) search. If you have $1$ Billion PDF embeddings in your database, and a user submits a search query, a naive mathematical search (KNN) must calculate the Cosine Similarity against all $1$ Billion vectors ($O(N)$ time complexity). This is physically impossible in real-time. HNSW solves this using an Approximate Nearest Neighbors (ANN) algorithm. It builds a multi-layered graph of vectors. The top layer has very few, highly disconnected nodes (highways). The search starts at the top, quickly jumps to the general geometric neighborhood, and drops down to denser layers until it finds the local cluster. It reduces the time complexity from $O(N)$ to $O(\\log N)$, finding the closest vectors in milliseconds at the cost of a slight loss in perfect accuracy."

3. Interviewer: "What is the 'Curse of Dimensionality' in relation to 1536-dimensional embeddings?"
   Senior Answer: "Distance Homogenization. In low-dimensional space (2D or 3D), points can be 'close' or 'far away'. But as the number of mathematical dimensions expands to $1500+$, the geometric volume of the space explodes exponentially. In this ultra-high-dimensional space, the mathematical distance between *any* two random points approaches a uniform constant. Everything becomes roughly equidistant from everything else. This makes separating clusters extremely difficult for algorithms. Embedding models solve this by intentionally mapping concepts into very tight, hyper-specific narrow cones within that massive space, forcing semantic differentiation despite the geometric curse."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Generative AI (Embeddings) Completed.")
