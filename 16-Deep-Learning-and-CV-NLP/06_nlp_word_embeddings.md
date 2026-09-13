# Word Embeddings (Word2Vec, GloVe, FastText)

## Prerequisites
- Knowledge of vector spaces and dot products.
- Understanding of neural network fundamentals (weights, activation functions).
- Basic NLP text processing (Tokenization).

## Objectives
- Understand the concept of dense vector representations for words.
- Learn the theory behind Word2Vec (CBOW and Skip-gram).
- Understand how GloVe and FastText differ from Word2Vec.
- Compute cosine similarity to measure semantic similarity.

## Intuition
While TF-IDF provides a numerical representation of text, it results in highly sparse vectors where the dimensionality equals the vocabulary size. More importantly, it fails to capture semantic relationships (e.g., "king" and "queen" are just distinct dimensions).
Word embeddings map words to dense, low-dimensional vectors (e.g., 300 dimensions) where geometrically close vectors represent semantically similar words. 
*Word2Vec* learns these vectors by predicting a word given its context (CBOW) or predicting context given a word (Skip-gram).
*GloVe* learns by factorizing the global word co-occurrence matrix.
*FastText* represents words as bags of character n-grams, enabling embeddings for out-of-vocabulary words.

## Mathematics
### Cosine Similarity
To measure how similar two words are, we compute the cosine of the angle between their embedding vectors $\mathbf{u}$ and $\mathbf{v}$:
$$ \text{Cosine Similarity}(\mathbf{u}, \mathbf{v}) = \frac{\mathbf{u} \cdot \mathbf{v}}{\|\mathbf{u}\| \|\mathbf{v}\|} $$
Values range from -1 (opposite) to 1 (identical).

### Skip-gram Objective
Given a sequence of words $w_1, w_2, ..., w_T$, the objective is to maximize the average log probability of the context words given the center word:
$$ J = \frac{1}{T} \sum_{t=1}^{T} \sum_{-c \le j \le c, j \neq 0} \log P(w_{t+j} | w_t) $$

## Code Reference
Refer to `06_nlp_word_embeddings.py` for examples of using pre-trained embeddings and calculating semantic similarity.

## Interview Questions
1. **Explain the difference between CBOW and Skip-gram.**
   *Answer:* CBOW predicts the target word from a window of context words. Skip-gram predicts the context words from a given target word. Skip-gram works better for infrequent words.
2. **How does FastText improve upon Word2Vec?**
   *Answer:* FastText learns embeddings for character n-grams rather than just whole words. This allows it to generate embeddings for unseen words (OOV) by combining the embeddings of their subword n-grams.
3. **What is the significance of $v_{\text{king}} - v_{\text{man}} + v_{\text{woman}} \approx v_{\text{queen}}$?**
   *Answer:* It demonstrates that word embeddings capture complex linear analogies and relational semantics in their vector space.
