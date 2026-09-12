"""
Module: 04-nlp-advanced
Description: Comprehensive textbook-grade interactive lesson on Advanced Natural Language Processing (NLP) in Python.

===========================================================================
ADVANCED NATURAL LANGUAGE PROCESSING (NLP)
===========================================================================

Natural Language Processing (NLP) sits at the intersection of computer science, 
artificial intelligence, and computational linguistics. Advanced NLP involves 
moving beyond basic text processing (like tokenization or stop-word removal) 
into sophisticated mathematical modeling of text semantics, syntactic structures, 
and context.

Learning Objectives:
1. Understand the mathematical foundations of Advanced NLP (TF-IDF, Attention).
2. Implement Term Frequency-Inverse Document Frequency (TF-IDF) from scratch.
3. Construct a Self-Attention Mechanism (the core of Transformers) mathematically.
4. Develop a TextRank algorithm for Extractive Text Summarization.
5. Analyze the Big-O time and space complexity of these algorithms.
6. Solve an advanced string alignment/NLP interview challenge: Levenshtein Distance.

===========================================================================
MATHEMATICAL BACKGROUND
===========================================================================

1. TF-IDF (Term Frequency-Inverse Document Frequency)
----------------------------------------------------
TF-IDF reflects how important a word is to a document in a collection or corpus.

Formulas:
- Term Frequency (TF): 
  TF(t, d) = (Number of times term t appears in document d) / (Total number of words in document d)
- Inverse Document Frequency (IDF): 
  IDF(t, D) = log_e(Total number of documents / Number of documents containing term t)
- TF-IDF:
  TF-IDF(t, d, D) = TF(t, d) * IDF(t, D)

2. Self-Attention (Scaled Dot-Product Attention)
------------------------------------------------
The foundational mechanism of the Transformer architecture.

Formula:
Attention(Q, K, V) = softmax( (Q * K^T) / sqrt(d_k) ) * V
Where:
- Q = Queries matrix
- K = Keys matrix
- V = Values matrix
- d_k = Dimension of the keys (used as a scaling factor to stabilize gradients)

3. Levenshtein Distance (Edit Distance)
---------------------------------------
A string metric for measuring the difference between two sequences.
Mathematical recurrence:
if min(i, j) == 0:
    lev(a, b) = max(i, j)
else:
    lev(a, b) = min(
        lev(a-1, b) + 1,        # Deletion
        lev(a, b-1) + 1,        # Insertion
        lev(a-1, b-1) + cost    # Substitution
    )
where cost is 0 if a[i] == b[j] else 1.

===========================================================================
"""

import sys
import time
import math
import collections
from typing import List, Dict, Tuple, Any, Optional, Union
import re


# =============================================================================
# 1. TF-IDF IMPLEMENTATION FROM SCRATCH
# =============================================================================

class AdvancedTFIDF:
    """
    Advanced implementation of Term Frequency-Inverse Document Frequency (TF-IDF).
    
    Time Complexity:
    - Fitting (building vocab and IDF): O(N * L) where N is number of documents, 
      and L is the average length of a document.
    - Transforming (computing TF-IDF): O(N * L).
    Space Complexity: O(V + N * V) where V is vocabulary size.
    """
    
    def __init__(self) -> None:
        """Initialize the TF-IDF vectorizer."""
        self.vocab: Dict[str, int] = {}
        self.idf: Dict[str, float] = {}
        self.vocab_size: int = 0
        self.doc_count: int = 0

    def _tokenize(self, text: str) -> List[str]:
        """
        Tokenizes the text into lowercase words, removing punctuation.
        
        Args:
            text (str): Input text string.
            
        Returns:
            List[str]: List of tokens.
        """
        # Using regex to find all alphanumeric character sequences
        return re.findall(r'\b\w+\b', text.lower())

    def fit(self, corpus: List[str]) -> None:
        """
        Learns the vocabulary and IDF from the corpus.
        
        Args:
            corpus (List[str]): List of text documents.
        """
        print("\n--- Fitting TF-IDF Model ---")
        self.doc_count = len(corpus)
        document_frequencies: Dict[str, int] = collections.defaultdict(int)
        
        # Build vocabulary and document frequencies
        for document in corpus:
            tokens = set(self._tokenize(document))
            for token in tokens:
                document_frequencies[token] += 1
                if token not in self.vocab:
                    self.vocab[token] = self.vocab_size
                    self.vocab_size += 1
                    
        # Calculate IDF
        # Standard formula: log(N / df(t)). We use natural log.
        # Adding 1 to the denominator to prevent division by zero.
        for token, df in document_frequencies.items():
            # Smoothing IDF: log( (N + 1) / (df + 1) ) + 1
            self.idf[token] = math.log((self.doc_count + 1) / (df + 1)) + 1.0
            
        print(f"Vocabulary size: {self.vocab_size}")
        print(f"Computed IDF for {len(self.idf)} terms.")

    def transform(self, corpus: List[str]) -> List[List[float]]:
        """
        Transforms the corpus into TF-IDF vectors.
        
        Args:
            corpus (List[str]): List of text documents.
            
        Returns:
            List[List[float]]: Dense TF-IDF matrix (list of lists).
        """
        print("\n--- Transforming Corpus using TF-IDF ---")
        tfidf_matrix: List[List[float]] = []
        
        for document in corpus:
            tokens = self._tokenize(document)
            total_tokens = len(tokens)
            
            # Compute TF
            term_frequencies: Dict[str, int] = collections.Counter(tokens)
            
            # Initialize vector with zeros
            vector = [0.0] * self.vocab_size
            
            for token, count in term_frequencies.items():
                if token in self.vocab:
                    # TF = count / total_tokens
                    tf = count / total_tokens
                    # TF-IDF = TF * IDF
                    tfidf = tf * self.idf[token]
                    # Assign to correct index in vector
                    vector[self.vocab[token]] = tfidf
                    
            # L2 Normalization (optional but standard practice)
            norm = math.sqrt(sum(val ** 2 for val in vector))
            if norm > 0:
                vector = [val / norm for val in vector]
                
            tfidf_matrix.append(vector)
            
        print(f"Transformed {len(corpus)} documents into vectors of size {self.vocab_size}.")
        return tfidf_matrix


# =============================================================================
# 2. SELF-ATTENTION MECHANISM (SCALED DOT-PRODUCT)
# =============================================================================

def softmax(vector: List[float]) -> List[float]:
    """
    Computes the softmax of a vector.
    
    Args:
        vector (List[float]): Input vector.
        
    Returns:
        List[float]: Softmax probabilities.
    """
    max_val = max(vector)
    # Subtract max_val for numerical stability
    exp_vector = [math.exp(x - max_val) for x in vector]
    sum_exp = sum(exp_vector)
    return [x / sum_exp for x in exp_vector]

def dot_product(v1: List[float], v2: List[float]) -> float:
    """Computes the dot product of two vectors."""
    return sum(x * y for x, y in zip(v1, v2))

def matrix_multiply(A: List[List[float]], B: List[List[float]]) -> List[List[float]]:
    """
    Multiplies matrix A (m x n) and matrix B (n x p).
    
    Returns:
        List[List[float]]: Resulting matrix (m x p).
    """
    m = len(A)
    n = len(A[0])
    p = len(B[0])
    
    result = [[0.0] * p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            result[i][j] = sum(A[i][k] * B[k][j] for k in range(n))
    return result

def transpose(matrix: List[List[float]]) -> List[List[float]]:
    """Transposes a matrix."""
    return [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]

def scaled_dot_product_attention(
    Q: List[List[float]], 
    K: List[List[float]], 
    V: List[List[float]]
) -> Tuple[List[List[float]], List[List[float]]]:
    """
    Calculates Scaled Dot-Product Attention from scratch.
    
    Formula: Attention(Q, K, V) = softmax( (Q * K^T) / sqrt(d_k) ) * V
    
    Args:
        Q: Queries matrix (sequence_length x d_k)
        K: Keys matrix (sequence_length x d_k)
        V: Values matrix (sequence_length x d_v)
        
    Returns:
        Tuple containing:
            - Attention Output matrix
            - Attention Weights matrix
    """
    print("\n--- Computing Scaled Dot-Product Attention ---")
    d_k = len(K[0])
    
    # Step 1: Compute Q * K^T
    K_T = transpose(K)
    scores = matrix_multiply(Q, K_T)
    
    # Step 2: Scale the scores by sqrt(d_k)
    scale = math.sqrt(d_k)
    scaled_scores = [[val / scale for val in row] for row in scores]
    
    # Step 3: Apply Softmax row-wise to get attention weights
    attention_weights = [softmax(row) for row in scaled_scores]
    
    # Step 4: Multiply by V
    attention_output = matrix_multiply(attention_weights, V)
    
    print("Attention computation complete.")
    return attention_output, attention_weights


# =============================================================================
# 3. TEXTRANK ALGORITHM FOR SUMMARIZATION
# =============================================================================
# TextRank is a graph-based ranking model for text processing, based on PageRank.

def cosine_similarity(v1: List[float], v2: List[float]) -> float:
    """Computes cosine similarity between two vectors."""
    dot = dot_product(v1, v2)
    norm1 = math.sqrt(dot_product(v1, v1))
    norm2 = math.sqrt(dot_product(v2, v2))
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return dot / (norm1 * norm2)

class TextRankSummarizer:
    """
    Extractive summarization using TextRank.
    """
    
    def __init__(self, damping_factor: float = 0.85, max_iter: int = 100, tol: float = 1e-4):
        self.damping_factor = damping_factor
        self.max_iter = max_iter
        self.tol = tol

    def split_sentences(self, text: str) -> List[str]:
        """Naively splits text into sentences."""
        # Split on '.', '!', '?'
        sentences = re.split(r'(?<=[.!?]) +', text)
        return [s.strip() for s in sentences if len(s.strip()) > 0]

    def summarize(self, text: str, num_sentences: int = 3) -> str:
        """
        Summarizes the text by extracting the most salient sentences.
        
        Algorithm:
        1. Split text into sentences.
        2. Create TF-IDF representation of sentences.
        3. Build similarity matrix (graph).
        4. Apply PageRank on the graph.
        5. Extract top-ranked sentences.
        """
        print("\n--- Running TextRank Summarization ---")
        sentences = self.split_sentences(text)
        
        if len(sentences) <= num_sentences:
            return text
            
        # Step 2: TF-IDF
        vectorizer = AdvancedTFIDF()
        vectorizer.fit(sentences)
        tfidf_vectors = vectorizer.transform(sentences)
        
        num_sents = len(sentences)
        
        # Step 3: Build Similarity Graph
        similarity_matrix = [[0.0] * num_sents for _ in range(num_sents)]
        for i in range(num_sents):
            for j in range(num_sents):
                if i != j:
                    similarity_matrix[i][j] = cosine_similarity(tfidf_vectors[i], tfidf_vectors[j])
                    
        # Normalize the similarity matrix rows to sum to 1
        for i in range(num_sents):
            row_sum = sum(similarity_matrix[i])
            if row_sum > 0:
                similarity_matrix[i] = [val / row_sum for val in similarity_matrix[i]]
                
        # Step 4: PageRank calculation
        # Initialize scores uniformly
        scores = [1.0 / num_sents] * num_sents
        
        for iteration in range(self.max_iter):
            prev_scores = list(scores)
            for i in range(num_sents):
                sum_inbound = 0.0
                for j in range(num_sents):
                    if i != j:
                        # similarity_matrix[j][i] is the transition probability from j to i
                        sum_inbound += similarity_matrix[j][i] * prev_scores[j]
                
                scores[i] = (1 - self.damping_factor) / num_sents + self.damping_factor * sum_inbound
                
            # Check convergence
            diff = sum(abs(scores[i] - prev_scores[i]) for i in range(num_sents))
            if diff < self.tol:
                print(f"TextRank converged after {iteration + 1} iterations.")
                break
                
        # Step 5: Extract top sentences
        # Create list of (score, sentence_index)
        ranked_sentences = [(scores[i], i) for i in range(num_sents)]
        # Sort by score descending
        ranked_sentences.sort(reverse=True, key=lambda x: x[0])
        
        # Select top num_sentences
        top_indices = [idx for score, idx in ranked_sentences[:num_sentences]]
        # Sort indices to maintain original order in text
        top_indices.sort()
        
        summary = " ".join([sentences[idx] for idx in top_indices])
        print(f"Reduced {num_sents} sentences to {num_sentences} sentences.")
        return summary


# =============================================================================
# 4. INTERVIEW CHALLENGE: LEVENSHTEIN DISTANCE
# =============================================================================

def edit_distance(word1: str, word2: str) -> int:
    """
    Computes the Levenshtein edit distance between two strings using Dynamic Programming.
    
    Operations allowed: Insertion, Deletion, Substitution.
    
    Time Complexity: O(m * n) where m = len(word1) and n = len(word2)
    Space Complexity: O(m * n) - Can be optimized to O(min(m, n))
    
    Args:
        word1 (str): First string.
        word2 (str): Second string.
        
    Returns:
        int: Minimum number of edits required.
    """
    m, n = len(word1), len(word2)
    
    # dp[i][j] will be the edit distance between word1[:i] and word2[:j]
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # Base cases
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
        
    # Build DP table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]  # No operation needed
            else:
                dp[i][j] = 1 + min(
                    dp[i - 1][j],    # Deletion from word1
                    dp[i][j - 1],    # Insertion into word1
                    dp[i - 1][j - 1] # Substitution
                )
                
    return dp[m][n]


# =============================================================================
# 5. PERFORMANCE AND EDGE CASES ANALYSIS
# =============================================================================

def analyze_performance_and_edge_cases() -> None:
    """
    Analyzes performance bottlenecks and discusses edge cases in Advanced NLP.
    """
    print("\n--- Performance Analysis & Edge Cases ---")
    
    print("1. TF-IDF Performance:")
    print("   - Vocabulary size grows aggressively with corpus size.")
    print("   - In production, min_df (minimum document frequency) and max_df are used to limit vocab.")
    print("   - Sparse matrices (e.g., from scipy) are crucial to save memory; our list of lists uses O(N*V) dense memory.")
    
    print("\n2. Self-Attention Complexity:")
    print("   - Time and Space complexity is O(L^2 * d) where L is sequence length and d is representation dimension.")
    print("   - For long documents, this quadratic scaling is a massive bottleneck (hence models like Longformer, Reformer).")
    
    print("\n3. TextRank Edge Cases:")
    print("   - Small texts: If sentences <= target_summary_length, it should return the original text.")
    print("   - Dead ends in graph: Damping factor (default 0.85) ensures the random surfer doesn't get stuck in disconnected components.")
    
    print("\n4. Edit Distance Edge Cases:")
    print("   - Empty strings: Handled elegantly by the DP base cases.")
    print("   - Large strings: O(m*n) space can lead to OutOfMemory errors. Space optimization to O(min(m, n)) by keeping only 2 rows of the DP table is recommended for production.\n")


# =============================================================================
# 6. TEST SUITE
# =============================================================================

def run_tests() -> None:
    """
    Test suite to validate all NLP implementations.
    """
    print("\n--- Running Tests ---")
    
    # 1. Test TF-IDF
    corpus = ["the cat sat on the mat", "the dog ate my homework", "cat and dog are pets"]
    tfidf = AdvancedTFIDF()
    tfidf.fit(corpus)
    vectors = tfidf.transform(corpus)
    assert len(vectors) == 3
    assert len(vectors[0]) == tfidf.vocab_size
    assert round(sum(v**2 for v in vectors[0]), 5) == 1.0  # L2 Normalized
    print("✓ TF-IDF tests passed.")
    
    # 2. Test Scaled Dot-Product Attention
    # 2 sequences, d_k = 3
    Q = [[1.0, 0.0, 1.0], [0.0, 1.0, 0.0]]
    K = [[1.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
    V = [[1.0, 2.0], [3.0, 4.0]]
    out, weights = scaled_dot_product_attention(Q, K, V)
    assert len(out) == 2 and len(out[0]) == 2
    assert len(weights) == 2 and len(weights[0]) == 2
    # Softmax rows should sum to 1
    assert round(sum(weights[0]), 5) == 1.0
    print("✓ Self-Attention tests passed.")
    
    # 3. Test Levenshtein Edit Distance
    assert edit_distance("kitten", "sitting") == 3
    assert edit_distance("flaw", "lawn") == 2
    assert edit_distance("", "test") == 4
    assert edit_distance("same", "same") == 0
    print("✓ Edit Distance tests passed.")
    
    print("All tests passed successfully!\n")


# =============================================================================
# MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":
    print(f"========== Exploring ADVANCED NLP ==========\n")
    
    # 1. Run TF-IDF Example
    sample_corpus = [
        "Machine learning is fascinating.",
        "Natural language processing allows computers to understand text.",
        "Deep learning is a subset of machine learning.",
        "Computers can process language using deep learning models."
    ]
    vectorizer = AdvancedTFIDF()
    vectorizer.fit(sample_corpus)
    matrix = vectorizer.transform(sample_corpus)
    print("Example TF-IDF vector for document 1 (first 5 features):")
    print([round(x, 4) for x in matrix[0][:5]])
    
    # 2. Run Self-Attention Example
    print("\nExample Context: 3 words, embedding dimension = 4")
    # Simulate queries, keys, values for 3 words
    q = [[1.2, 0.5, 0.0, -1.0], [0.2, 1.5, 1.0, 0.0], [0.0, 0.0, 0.5, 1.5]]
    k = [[1.0, 0.5, 0.0, -1.0], [0.0, 1.0, 1.0, 0.0], [0.0, 0.0, 0.5, 1.5]]
    v = [[1.0, 0.0], [0.0, 1.0], [1.0, 1.0]]  # value dim = 2
    
    attention_out, attn_weights = scaled_dot_product_attention(q, k, v)
    print("Attention Weights (how much each word attends to other words):")
    for row in attn_weights:
        print([round(w, 4) for w in row])
        
    # 3. Run TextRank Summarization Example
    article = (
        "Artificial intelligence is intelligence demonstrated by machines, as opposed to natural intelligence displayed by animals including humans. "
        "Leading AI textbooks define the field as the study of intelligent agents: any system that perceives its environment and takes actions that maximize its chance of achieving its goals. "
        "Some popular accounts use the term artificial intelligence to describe machines that mimic cognitive functions that humans associate with the human mind, such as learning and problem solving, however, this definition is rejected by major AI researchers. "
        "AI applications include advanced web search engines, recommendation systems, understanding human speech, self-driving cars, automated decision-making and competing at the highest level in strategic game systems."
    )
    summarizer = TextRankSummarizer()
    summary = summarizer.summarize(article, num_sentences=2)
    print("\nOriginal Text Length:", len(article))
    print("Summary Length:", len(summary))
    print("Summary:", summary)
    
    # 4. Run Interview Challenge
    print("\n--- Interview Challenge ---")
    w1, w2 = "intention", "execution"
    dist = edit_distance(w1, w2)
    print(f"Edit distance between '{w1}' and '{w2}' is: {dist}")
    
    # 5. Performance & Edge Cases
    analyze_performance_and_edge_cases()
    
    # 6. Run Tests
    run_tests()
    
    print(f"========== END OF ADVANCED NLP ==========\n")
