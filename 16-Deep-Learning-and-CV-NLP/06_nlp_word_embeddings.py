"""
# ==============================================================================
# LABORATORY: NLP (WORD EMBEDDINGS & SEMANTIC SEARCH)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A junior developer builds a recommendation engine for an e-commerce site. A 
# user searches for "Running Shoes". The backend runs a standard SQL `LIKE` query 
# and returns 0 results because the database only has items labeled "Sneakers". 
# The user assumes the store is empty and leaves.
#
# A senior AI engineer understands "Vector Embeddings". They convert the search 
# query "Running Shoes" into a 300-Dimensional floating-point array using Word2Vec. 
# They convert the inventory item "Sneakers" into a 300-Dimensional array. They 
# execute a Cosine Similarity calculation (Dot Product). The GPU mathematically 
# proves that "Running Shoes" and "Sneakers" live in the exact same mathematical 
# coordinate space in the universe, despite sharing zero letters. The search engine 
# successfully returns the Sneakers.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master continuous Vector representations of discrete text.
# - Execute Vector Mathematics (Addition, Subtraction) for analogies.
# - Architect a basic Semantic Search Engine using Cosine Distance.
#
# ==============================================================================
"""

import numpy as np

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE BUSINESS LOGIC (THE EMBEDDING SPACE)
# ==============================================================================
class VectorDatabase:
    """
    Simulates a Vector Database (like Pinecone or Milvus) storing pre-trained Word2Vec embeddings.
    For visual comprehension, we compress them into a 4-Dimensional semantic space.
    Dimensions: [Royalty, Masculinity, Age, Power]
    """
    
    def __init__(self):
        # [Royalty, Masculinity, Age, Power]
        self.embeddings = {
            "King":    np.array([ 0.95,  0.90,  0.80,  0.90]),
            "Queen":   np.array([ 0.95, -0.90,  0.80,  0.90]),
            "Prince":  np.array([ 0.95,  0.90, -0.80,  0.50]),
            "Princess":np.array([ 0.95, -0.90, -0.80,  0.50]),
            "Man":     np.array([ 0.05,  0.90,  0.80,  0.20]),
            "Woman":   np.array([ 0.05, -0.90,  0.80,  0.20]),
            "Boy":     np.array([ 0.05,  0.90, -0.80,  0.05]),
            "Girl":    np.array([ 0.05, -0.90, -0.80,  0.05]),
            "Apple":   np.array([ 0.01,  0.00,  0.00,  0.01]) # Unrelated concept
        }
        
    @staticmethod
    def cosine_similarity(vec_a: np.ndarray, vec_b: np.ndarray) -> float:
        """Calculates the normalized angle between two vectors."""
        dot_product = np.dot(vec_a, vec_b)
        norm_a = np.linalg.norm(vec_a)
        norm_b = np.linalg.norm(vec_b)
        
        if norm_a == 0 or norm_b == 0:
            return 0.0
            
        return dot_product / (norm_a * norm_b)
        
    def find_closest_word(self, target_vector: np.ndarray, exclude_words: list = []) -> str:
        """
        Executes a 'K-Nearest Neighbors' search to find the closest word in the database.
        """
        best_word = None
        best_score = -1.0 # Cosine similarity ranges from -1 to 1
        
        for word, vector in self.embeddings.items():
            if word in exclude_words:
                continue
                
            score = self.cosine_similarity(target_vector, vector)
            if score > best_score:
                best_score = score
                best_word = word
                
        return best_word, best_score


# ==============================================================================
# 4. THE ARCHITECTURAL EXECUTION
# ==============================================================================
class EmbeddingSimulator:
    
    def __init__(self):
        self.db = VectorDatabase()
        
    def execute_analogies(self):
        """
        [SECURE] Vector Arithmetic.
        If the neural network perfectly learned human semantics, we can do math with words.
        """
        print("\n  [EXECUTION] Testing Semantic Mathematics (Analogies)...")
        
        # Test 1: King - Man + Woman = ?
        print("\n  -> Test 1: Vector('King') - Vector('Man') + Vector('Woman')")
        vec_test_1 = self.db.embeddings["King"] - self.db.embeddings["Man"] + self.db.embeddings["Woman"]
        
        # We must exclude the input words from the search so it doesn't just return 'King'
        result, score = self.db.find_closest_word(vec_test_1, exclude_words=["King", "Man", "Woman"])
        print(f"     [MATHEMATICAL RESULT] '{result}' (Confidence: {score:.4f})")
        
        # Test 2: Man - Boy + Girl = ?
        print("\n  -> Test 2: Vector('Man') - Vector('Boy') + Vector('Girl')")
        vec_test_2 = self.db.embeddings["Man"] - self.db.embeddings["Boy"] + self.db.embeddings["Girl"]
        
        result, score = self.db.find_closest_word(vec_test_2, exclude_words=["Man", "Boy", "Girl"])
        print(f"     [MATHEMATICAL RESULT] '{result}' (Confidence: {score:.4f})")

    def execute_semantic_search(self):
        """
        [SECURE] Information Retrieval without exact keyword matching.
        """
        print("\n  [EXECUTION] Executing Semantic Search...")
        
        # Suppose a user searches for something that conceptually maps to [High Power, Low Age, High Royalty, Female]
        # Even if they didn't type the word, we convert their query into a vector!
        query_vector = np.array([0.9, -0.8, -0.9, 0.6]) 
        
        result, score = self.db.find_closest_word(query_vector)
        print(f"\n  -> Searching Database with conceptual vector: {query_vector}")
        print(f"  -> Best Match Found: '{result}' (Similarity: {score:.4f})")
        print("  -> [FLAWLESS] The search engine returned 'Princess' based purely on ")
        print("     mathematical semantic alignment, zero keyword matching required.")


# ==============================================================================
# 5. MATHEMATICAL PROOF (THE BENCHMARK)
# ==============================================================================
def demonstrate_embeddings():
    section_header("Deep Learning NLP: Word Embeddings")
    
    sim = EmbeddingSimulator()
    sim.execute_analogies()
    sim.execute_semantic_search()


def run_all_labs():
    demonstrate_embeddings()


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "What is the architectural difference between Word2Vec (CBOW) and Word2Vec (Skip-Gram)?"
   Senior Answer: "Target vs Context Prediction. Both algorithms are shallow Neural Networks designed solely to learn the embedding weights, throwing away the final layer. CBOW (Continuous Bag of Words) takes the surrounding Context words (e.g., 'The', 'sat', 'on', 'the') and tries to predict the missing Target word ('cat'). Skip-Gram inverses this mathematically. It takes the single Target word ('cat') and tries to predict the surrounding Context words. Because Skip-Gram forces a single word to generate multiple outputs, it structurally forces the network to learn much richer, higher-quality representations for rare words, making it the preferred architecture in modern pipelines."

2. Interviewer: "Why does the GloVe (Global Vectors) algorithm sometimes mathematically outperform Word2Vec?"
   Senior Answer: "Global Matrix Factorization vs Local Context Windows. Word2Vec trains entirely by sliding a tiny $5$-word window across a document. It only learns about words that physically sit next to each other (Local Context). It mathematically ignores the global statistics of the entire corpus. GloVe builds a massive global Co-occurrence Matrix (a $N \\times N$ grid of how many times every word appears near every other word across the entire Wikipedia). It then uses Singular Value Decomposition (SVD) and Matrix Factorization to compress this massive global grid down to $300$ dimensions. By mathematically anchoring the training on Global statistics rather than just Local sliding windows, GloVe often generates more stable semantic topologies."

3. Interviewer: "If a user inputs a typo ('Pwincess'), how does a standard Word2Vec model handle it compared to FastText?"
   Senior Answer: "The OOV Collapse vs Character N-Grams. Word2Vec operates strictly at the whole-word level. If it never saw 'Pwincess' during training, it is Out-Of-Vocabulary (OOV) and the model violently crashes or returns a useless zero-vector. Facebook's FastText algorithm mathematically solves this by breaking words into Character N-Grams. During training, it learns the embedding for the word 'Princess', but it also learns embeddings for the chunks `<pr`, `rin`, `inc`, `ces`, `ess>`. When it encounters the typo 'Pwincess', it mathematically constructs a brand new vector on the fly by summing the vectors of the known chunks (`<pw`, `win`, `inc`, `ces`, `ess>`). Because it shares $60\\%$ of the exact same N-Gram vectors as 'Princess', the resulting typo vector lands perfectly next to the true word in semantic space."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: NLP (Word Embeddings) Completed.")
