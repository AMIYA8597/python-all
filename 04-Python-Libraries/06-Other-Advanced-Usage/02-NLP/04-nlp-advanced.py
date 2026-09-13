"""
# ==============================================================================
# LABORATORY: ADVANCED TRADITIONAL NLP (LDA & WORD2VEC)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# If you have 10,000 documents, and you want to know what they are about, 
# you cannot use a classification algorithm, because you don't have any labels!
#
# You must use Unsupervised Learning (Topic Modeling). Latent Dirichlet 
# Allocation (LDA) will mathematically scan the 10,000 documents and group 
# the vocabulary into distinct "Topics" without ever being told what the topics are.
#
# Furthermore, TF-IDF is powerful, but it has no semantic understanding. 
# In TF-IDF, the word "King" and "Queen" are mathematically treated as completely 
# unrelated strings. To capture true semantic meaning without a massive LLM, 
# we use Word Embeddings like Word2Vec. Word2Vec compresses English words into 
# dense vectors where the geometry perfectly mirrors human logic: 
# [King] - [Man] + [Woman] = [Queen]!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand Topic Modeling using Latent Dirichlet Allocation (LDA).
# - Understand the architecture and math of Word2Vec (CBOW vs Skip-Gram).
# - Calculate Semantic Similarity using Cosine Similarity.
#
# ==============================================================================
"""

import numpy as np

# In a real environment: pip install scikit-learn gensim
try:
    from sklearn.feature_extraction.text import CountVectorizer
    from sklearn.decomposition import LatentDirichletAllocation
    from sklearn.metrics.pairwise import cosine_similarity
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. TOPIC MODELING (LATENT DIRICHLET ALLOCATION - LDA)
# ==============================================================================
def demonstrate_lda():
    section_header("Topic Modeling (LDA)")
    
    if not HAS_SKLEARN:
        print("[WARNING] Scikit-Learn not installed.")
        return
        
    print("LDA assumes that every Document is a mixture of Topics, and every ")
    print("Topic is a mixture of Words.\n")
    
    corpus = [
        "The economy is growing, stocks are up, and banks are profitable.",
        "The Federal Reserve lowered interest rates to boost the economy.",
        "The new deep learning neural network achieved state-of-the-art accuracy.",
        "Machine learning algorithms are revolutionizing artificial intelligence.",
        "The CPU and GPU hardware are essential for training the AI."
    ]
    
    # 1. Vectorize the text (LDA strictly requires Raw Counts, NOT TF-IDF!)
    vectorizer = CountVectorizer(stop_words='english')
    X = vectorizer.fit_transform(corpus)
    
    # 2. Initialize LDA (We mathematically force it to find exactly 2 Topics)
    lda_model = LatentDirichletAllocation(n_components=2, random_state=42)
    lda_model.fit(X)
    
    # 3. Display the Topics
    feature_names = vectorizer.get_feature_names_out()
    
    print("The Unsupervised Algorithm Discovered 2 distinct Topics:\n")
    for topic_idx, topic in enumerate(lda_model.components_):
        # Sort the topic weights to find the top 4 words
        top_words_idx = topic.argsort()[:-5:-1]
        top_words = [feature_names[i] for i in top_words_idx]
        print(f"Topic #{topic_idx + 1}: {', '.join(top_words)}")
        
    print("\nNotice how Topic 1 perfectly clustered 'economy, banks, rates'.")
    print("Notice how Topic 2 perfectly clustered 'learning, ai, network'.")
    print("We did NOT give it any labels! It found this purely through math!")


# ==============================================================================
# 4. WORD EMBEDDINGS (WORD2VEC)
# ==============================================================================
def demonstrate_word2vec():
    section_header("Word2Vec & Dense Embeddings")
    
    print("TF-IDF creates Sparse Matrices (Mostly zeroes). If your vocabulary is ")
    print("50,000 words, every word is represented by a vector of length 50,000.")
    print("Word2Vec creates Dense Matrices. It compresses every word in the ")
    print("dictionary down to exactly 300 floating-point numbers.\n")
    
    print("--- How Word2Vec Trains (Skip-Gram) ---")
    print("It uses a tiny, shallow Neural Network with 1 hidden layer.")
    print("Input: A target word (e.g., 'Apple').")
    print("Output: Predict the surrounding context words (e.g., 'eat', 'tasty').")
    
    print("\nBecause 'Apple' and 'Banana' share the exact same context words ")
    print("(both appear near 'eat', 'peel', 'tasty'), the Neural Network's ")
    print("backpropagation physically forces the 300-dimensional vector for 'Apple' ")
    print("and 'Banana' to become mathematically identical!")
    
    print("\n--- The Geometry of Language ---")
    print("Once trained, you can perform actual Vector Algebra on English words:")
    print("Vector('Paris') - Vector('France') + Vector('Italy') = Vector('Rome')")
    
    print("\nBy stripping out 'France' (removing the concept of French geography) ")
    print("and adding 'Italy', the resulting vector perfectly lands on the coordinates ")
    print("for the word 'Rome' in the 300-dimensional space!")


# ==============================================================================
# 5. SEMANTIC SIMILARITY (COSINE SIMILARITY)
# ==============================================================================
def demonstrate_cosine_similarity():
    section_header("Semantic Similarity (Cosine Similarity)")
    
    if not HAS_SKLEARN: return
    
    print("How do we measure the distance between two Word2Vec vectors?")
    print("We DO NOT use Euclidean Distance (measuring the straight line between them).")
    print("We use Cosine Similarity (measuring the Angle between the vectors).\n")
    
    # Synthetic 2D vectors for demonstration
    vector_king  = np.array([[ 0.8,  0.5]])
    vector_queen = np.array([[ 0.9,  0.6]])
    vector_car   = np.array([[-0.8, -0.5]])
    
    # Calculate Cosine Similarity (1.0 is identical, -1.0 is completely opposite)
    sim_royalty = cosine_similarity(vector_king, vector_queen)[0][0]
    sim_unrelated = cosine_similarity(vector_king, vector_car)[0][0]
    
    print(f"Angle Similarity (King vs Queen): {sim_royalty:.2f} (Highly related!)")
    print(f"Angle Similarity (King vs Car)  : {sim_unrelated:.2f} (Opposite!)")
    
    print("\nCosine Similarity ignores the *Magnitude* (length) of the vector, ")
    print("and focuses purely on the *Direction*. If 'King' appears 10,000 times ")
    print("in the text (huge magnitude) and 'Queen' appears 10 times (tiny magnitude), ")
    print("Euclidean distance would say they are far apart. Cosine Similarity ")
    print("correctly says they are identical because they point in the same direction!")


def run_all_labs():
    demonstrate_lda()
    demonstrate_word2vec()
    demonstrate_cosine_similarity()


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why must you use `CountVectorizer` (raw counts) instead of `TfidfVectorizer` when training an LDA Topic Model?
   Answer: Latent Dirichlet Allocation (LDA) is a generative probabilistic model heavily rooted in Bayesian statistics. It mathematically assumes that documents are generated by rolling loaded dice to select a Topic, and then rolling another loaded die to select a Word from that Topic. It relies fundamentally on the absolute integer frequencies (the raw counts) of the words to calculate the Dirichlet distributions. TF-IDF transforms integers into normalized floating-point numbers (destroying the raw probability counts) and artificially penalizes frequent words, which completely shatters the underlying statistical assumptions of the LDA mathematical engine, causing catastrophic failure in topic generation.

2. Explain the architectural difference between Word2Vec's "CBOW" and "Skip-Gram" models.
   Answer: Word2Vec can be trained using two different architectures. 
   - CBOW (Continuous Bag of Words): The Neural Network takes the surrounding context words as the Input (e.g., "The", "quick", "fox", "jumps") and attempts to predict the single missing target word in the middle ("brown"). CBOW is faster to train and works very well for frequent words.
   - Skip-Gram: The exact opposite. The Neural Network takes the single target word as the Input ("brown") and attempts to predict the surrounding context words ("The", "quick", "fox", "jumps"). Skip-Gram is much slower to train but fundamentally produces much higher quality, deeply semantic vector embeddings, particularly for rare words.

3. Why is Cosine Similarity the undisputed industry standard for comparing text embeddings over Euclidean Distance?
   Answer: In high-dimensional vector space (like 300D Word2Vec or 1536D OpenAI Embeddings), the *magnitude* (length) of the vector is often corrupted by document length or absolute word frequency. If Document A is a 5-word sentence about finance, and Document B is a 5,000-word textbook about finance, their Euclidean Distance will be massive because the vector for Document B is physically much longer. Cosine Similarity entirely ignores magnitude and mathematically calculates only the Angle $\theta$ between the two vectors ($\cos(\theta) = \frac{A \cdot B}{||A|| ||B||}$). Because they are both about finance, their vectors will point in the exact same geometric direction, yielding a perfect Cosine Similarity of $1.0$, making it robust against text-length variations.
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Advanced NLP Completed.")
