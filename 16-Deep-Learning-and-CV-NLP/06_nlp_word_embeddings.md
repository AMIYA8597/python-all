# Chapter 6: Natural Language Processing - Word Embeddings

## 1. Introduction to Word Representations

In the domain of Natural Language Processing (NLP), representing words in a manner that computers can natively process is a foundational challenge. Traditionally, NLP models relied heavily on symbolic representations, such as one-hot encoding. In a one-hot encoded vector, each word in a vocabulary is represented by a vector of length $|V|$ (where $V$ is the vocabulary size). This vector is entirely composed of zeros except for a single element at the index corresponding to the word, which is set to one.

### 1.1 Limitations of One-Hot Encoding

While simple to understand and implement, one-hot encoding suffers from three catastrophic drawbacks for large-scale language modeling:

1.  **Sparsity and Dimensionality:** A typical English vocabulary contains hundreds of thousands of words. A one-hot encoded matrix for a corpus is extremely sparse, consuming vast amounts of memory and computational resources while providing minimal information density.
2.  **Orthogonality and Lack of Semantic Similarity:** The dot product between any two distinct one-hot encoded vectors is exactly zero. This implies that all words are equally dissimilar. A model using one-hot encoding has no intrinsic way of knowing that the words "dog" and "puppy" are semantically closer than "dog" and "refrigerator".
3.  **Inability to Capture Context:** These representations view words as atomic units isolated from their usage contexts.

### 1.2 Distributional Semantics

The solution to these limitations is rooted in the linguistic theory of **Distributional Semantics**, famously summarized by John Rupert Firth in 1957: *"You shall know a word by the company it keeps."* 

Word embeddings are dense, low-dimensional (typically 50 to 1024 dimensions), real-valued vectors that capture the semantic and syntactic properties of words based on their co-occurrence patterns in large corpora. Instead of words being orthogonal, the spatial distance and directional alignment between vectors in this continuous space correspond directly to their semantic relationships.

---

## 2. Word2Vec: Learning Word Embeddings

Introduced by Tomas Mikolov and his team at Google in 2013, **Word2Vec** revolutionized NLP. It is not a single algorithm, but rather a family of two distinct neural network architectures used to learn word embeddings from raw text: **Continuous Bag-of-Words (CBOW)** and **Skip-Gram**. 

Word2Vec operates on the principle of predicting words based on their local context windows. Unlike deep neural networks, Word2Vec employs a shallow, two-layer neural network (an input layer, a hidden layer, and an output layer). The goal is not the prediction task itself, but rather the side-effect of training: the weights learned in the hidden layer become the word embeddings.

### 2.1 Continuous Bag-of-Words (CBOW)

In the CBOW architecture, the model attempts to predict a **target word** (the center word) given its surrounding **context words**. 

Let a sequence of training words be $w_1, w_2, w_3, \dots, w_T$. The objective of the CBOW model is to maximize the average log probability of predicting the center word $w_t$ given a context window of size $c$:

$$ J = \frac{1}{T} \sum_{t=1}^{T} \log P(w_t \mid w_{t-c}, \dots, w_{t-1}, w_{t+1}, \dots, w_{t+c}) $$

**Architecture Details:**
1.  **Input Layer:** Context words are one-hot encoded.
2.  **Hidden Layer:** The input vectors are multiplied by a weight matrix $W$ (size $V \times N$, where $N$ is the embedding dimension). In CBOW, the hidden layer representation is typically the average of the context word vectors.
3.  **Output Layer:** The hidden vector is multiplied by another weight matrix $W'$ (size $N \times V$) to produce scores for each word in the vocabulary, which are passed through a softmax function to output probabilities.

CBOW is generally faster to train than Skip-Gram and tends to have slightly better accuracy for frequent words, as it smooths over the context distributions.

### 2.2 Skip-Gram Model

The Skip-Gram architecture inverts the CBOW formulation. Instead of predicting the center word from the context, Skip-Gram uses the **center word** to predict the surrounding **context words**.

The objective function for Skip-Gram is to maximize the average log probability of predicting the context words given the center word $w_t$:

$$ J = \frac{1}{T} \sum_{t=1}^{T} \sum_{-c \le j \le c, j \neq 0} \log P(w_{t+j} \mid w_t) $$

**Architecture Details:**
1.  **Input Layer:** The single center word is one-hot encoded.
2.  **Hidden Layer:** Multiplication by matrix $W$ yields the dense vector for the center word.
3.  **Output Layer:** This vector is multiplied by $W'$ to output predictions for the context words via softmax.

Skip-Gram inherently treats each context-target pair as a new observation. This property makes it significantly better at capturing semantics for **infrequent words** and generally yields higher quality embeddings overall, albeit at a higher computational cost.

### 2.3 Mathematical Formulation and Optimization

The standard formulation calculates $P(w_O \mid w_I)$ (probability of output word given input word) using the softmax function:

$$ P(w_O \mid w_I) = \frac{\exp(v_{w_O}'^{\top} v_{w_I})}{\sum_{w=1}^{V} \exp(v_{w}'^{\top} v_{w_I})} $$

Where $v_w$ and $v_w'$ are the "input" and "output" vector representations of the word $w$.

However, computing this softmax is computationally prohibitive because the denominator requires summing over the entire vocabulary $V$ (often millions of words) for every training step. To solve this, Word2Vec implementations use two optimization techniques: **Hierarchical Softmax** and **Negative Sampling**.

#### Negative Sampling
Instead of updating the weights of all words in the vocabulary, Negative Sampling transforms the multi-class classification problem into a binary classification problem using logistic regression. 

For a given context window, we have a "positive" pair (the center word and an actual context word). We then randomly sample $k$ "negative" words from the vocabulary based on a noise distribution $P_n(w)$ (typically the unigram distribution raised to the $3/4$ power to downsample frequent words). 

The new objective becomes maximizing the probability that positive pairs are real and negative pairs are fake:

$$ \log \sigma(v_{w_O}'^{\top} v_{w_I}) + \sum_{i=1}^{k} \mathbb{E}_{w_i \sim P_n(w)} [\log \sigma(-v_{w_i}'^{\top} v_{w_I})] $$

Where $\sigma(x) = 1 / (1 + e^{-x})$ is the sigmoid function. This reduces the time complexity per step from $O(V)$ to $O(k+1)$, making the training of high-dimensional embeddings feasible on massive datasets.

---

## 3. GloVe: Global Vectors for Word Representation

While Word2Vec is a **predictive** model that learns by streaming through local context windows, **GloVe** (developed by Stanford researchers Pennington, Socher, and Manning in 2014) is a **count-based** model. GloVe bridges the gap between global matrix factorization methods (like Latent Semantic Analysis or LSA) and local context window methods (like Skip-Gram).

### 3.1 The Co-occurrence Matrix

GloVe operates directly on the global word-word co-occurrence matrix $X$, where each entry $X_{ij}$ tabulates the number of times word $j$ occurs in the context of word $i$ across the entire corpus. 

Let $P_{ij} = P(j \mid i) = X_{ij} / X_i$ be the probability that word $j$ appears in the context of word $i$. GloVe is built on the crucial insight that **ratios of co-occurrence probabilities** encode semantic meaning far better than the probabilities themselves.

For example, consider the words $i = \text{ice}$ and $j = \text{steam}$. If we examine a context word $k = \text{solid}$, the ratio $P(k \mid \text{ice}) / P(k \mid \text{steam})$ will be large. Conversely, for $k = \text{gas}$, the ratio will be small. For a word $k$ related to both (like $\text{water}$) or related to neither (like $\text{fashion}$), the ratio will be close to 1.

### 3.2 The GloVe Cost Function

GloVe defines a model where the dot product of two word vectors equals the logarithm of their probability of co-occurrence. The function is designed to minimize the squared difference between the dot product of word vectors and the log of their co-occurrence counts.

The weighted least squares regression objective function for GloVe is:

$$ J = \sum_{i,j=1}^{V} f(X_{ij}) (w_i^{\top} \tilde{w}_j + b_i + \tilde{b}_j - \log X_{ij})^2 $$

Where:
*   $w_i$ and $\tilde{w}_j$ are the word vectors for the main and context words.
*   $b_i$ and $\tilde{b}_j$ are scalar biases for the respective words.
*   $f(X_{ij})$ is a weighting function designed to clip the impact of highly frequent word pairs (like "the", "and") while ensuring that rare words do not disproportionately affect the training.

The weighting function is defined as:
$$ f(x) = \begin{cases} (x/x_{\max})^\alpha & \text{if } x < x_{\max} \\ 1 & \text{otherwise} \end{cases} $$
Typically, $\alpha = 3/4$ and $x_{\max} = 100$.

### 3.3 Advantages of GloVe

1.  **Global Statistics:** Because GloVe trains on the aggregated co-occurrence matrix, it efficiently leverages global statistical information, ensuring that overall corpus statistics are strictly respected. Word2Vec, strictly relying on local context windows, can sometimes miss broader statistical trends.
2.  **Training Efficiency:** Computing the co-occurrence matrix is an expensive upfront operation, but once constructed, the training of the vectors on non-zero matrix entries is exceptionally fast and highly parallelizable.

---

## 4. FastText: Subword N-grams

Both Word2Vec and GloVe share a significant architectural flaw: they treat every word as a distinct atomic entity. This leads to the **Out-of-Vocabulary (OOV)** problem. If a model encounters a word during inference that it did not see during training (e.g., a rare misspelling, a newly coined term, or complex morphological derivations), it has no vector representation for it and often defaults to a generic `<UNK>` token. Furthermore, these models cannot share representations across morphologically related words (like "teach", "teacher", "teachers", "teaching").

### 4.1 Subword Representations

Developed by Facebook AI Research (Bojanowski et al., 2017), **FastText** extends the Skip-Gram architecture by representing each word as a **bag of character n-grams**. 

For example, given the word "apple" and taking $n=3$ (trigrams), FastText will add special boundary symbols `<` and `>` to indicate the beginning and end of the word, resulting in `<apple>`. The trigrams extracted are:
`<ap, app, ppl, ple, le>`

In addition to the n-grams, the entire word `<apple>` is also included in the representation. This ensures that frequent words still maintain their specific learned semantics.

### 4.2 Mathematical Changes in Scoring

In FastText, a word is represented by the **sum of the vector representations of its component n-grams**.

Let $\mathcal{G}_w$ be the set of n-grams appearing in word $w$, and let $z_g$ be the vector representation to each n-gram $g$. The scoring function (dot product) between a center word $w$ and a context word $c$, which was previously $w_c^{\top} w_w$ in Skip-Gram, becomes:

$$ s(w, c) = \sum_{g \in \mathcal{G}_w} z_g^{\top} v_c $$

This seemingly minor change yields profound improvements:
1.  **Morphological Richness:** The model implicitly learns suffixes, prefixes, and word roots. Languages with rich morphology (like Finnish, Turkish, or Arabic) benefit massively from FastText.
2.  **Handling OOV Words:** Even if a word has never been seen, FastText can construct a meaningful vector for it on the fly by breaking the unknown word into n-grams, looking up the vectors for those n-grams (which likely were seen during training), and summing them together.

---

## 5. Mathematical Properties of Embeddings

One of the most fascinating discoveries surrounding word embeddings is that they organically learn complex, geometric relationships reflecting human logic. Because vectors exist in continuous affine space, algebraic operations can be performed on words.

### 5.1 Vector Analogies

The classic example of linguistic regularity learned by these models is:
$$ \vec{v}_{\text{King}} - \vec{v}_{\text{Man}} + \vec{v}_{\text{Woman}} \approx \vec{v}_{\text{Queen}} $$

This equation demonstrates that the vector offset (the mathematical difference between vectors) encodes specific semantic relationships. The offset between "King" and "Man" encodes the concept of "Royalty" or "Rulership". When this "Royalty" offset is added to the vector for "Woman", the resulting vector closest in the multidimensional space is the vector for "Queen".

This logic extends to syntax (e.g., singular/plural, verb tenses) and world knowledge (e.g., capitals to countries):
*   $\vec{v}_{\text{Paris}} - \vec{v}_{\text{France}} + \vec{v}_{\text{Italy}} \approx \vec{v}_{\text{Rome}}$
*   $\vec{v}_{\text{walking}} - \vec{v}_{\text{walk}} + \vec{v}_{\text{swim}} \approx \vec{v}_{\text{swimming}}$

### 5.2 Distance Metrics

To query a vector space for semantic similarity, we require a distance metric. While Euclidean distance can be used, it is highly sensitive to vector magnitude. In NLP, the magnitude of a word vector often correlates with the frequency of the word in the corpus, not just its semantic meaning.

Therefore, **Cosine Similarity** is the industry standard for measuring word vector similarity. It measures the cosine of the angle between two vectors, effectively normalizing their magnitudes and focusing purely on their directional alignment.

$$ \text{Cosine Similarity}(u, v) = \frac{u \cdot v}{\|u\| \|v\|} = \frac{\sum_{i=1}^{n} u_i v_i}{\sqrt{\sum_{i=1}^{n} u_i^2} \sqrt{\sum_{i=1}^{n} v_i^2}} $$

Cosine similarity values range from -1 (perfectly opposite) to 1 (identical direction), with 0 indicating orthogonality (no correlation).

---

## 6. Querying Vector Databases for Semantic Search

While word embeddings provided the foundation, modern NLP relies heavily on sentence or document embeddings (generated via Transformers like BERT, Sentence-BERT, or OpenAI's embeddings). Once a vast corpus of documents is converted into dense vectors, the challenge shifts from NLP to high-performance database engineering: how do we quickly find the most semantically similar documents to a user's query?

This is the domain of **Vector Databases** and **Approximate Nearest Neighbor (ANN)** search.

### 6.1 The Challenge of Exact Search

To perform a semantic search, a user query $q$ is embedded into the same vector space, yielding vector $v_q$. The exact nearest neighbor search involves computing the cosine similarity between $v_q$ and every single vector $v_d$ in the database $D$, and returning the top $k$ results. 

If $N$ is the number of documents and $d$ is the vector dimensionality, exact search (often called flat search or brute-force search) takes $O(N \times d)$ time. For a database of a billion vectors with 1024 dimensions, a single query could take seconds or minutes, which is unacceptable for production applications.

### 6.2 Approximate Nearest Neighbors (ANN)

To achieve millisecond latency at the cost of a slight drop in accuracy (recall), vector databases use ANN algorithms. Two of the most dominant algorithms are **Inverted File with Product Quantization (IVFPQ)** and **Hierarchical Navigable Small World (HNSW)**.

#### Inverted File Index (IVF)
IVF partitions the vector space into $V$ Voronoi cells (clusters) using an algorithm like K-Means. During insertion, each document vector is assigned to the nearest cluster centroid. During a query, the system first finds the $nprobe$ nearest cluster centroids to the query vector $v_q$, and then only calculates exact distances against the documents residing within those specific clusters. This dramatically reduces the search space.

#### Product Quantization (PQ)
PQ is a compression technique. It splits a high-dimensional vector into $m$ sub-vectors, and performs clustering on each sub-space independently. Vectors are then represented not by raw floats, but by a sequence of integer IDs corresponding to the nearest centroid in each sub-space. This reduces memory footprint exponentially, allowing massive vector indexes to fit entirely in RAM, which is crucial for fast lookups.

#### Hierarchical Navigable Small World (HNSW)
HNSW is a graph-based approach. It builds a multi-layered graph where the bottom layer contains all vectors connected to their nearest neighbors. Upper layers contain exponentially fewer nodes, forming "skip lists" for routing. A search begins at the top, sparse layer. The algorithm greedily traverses the graph towards the query vector. Once it finds a local minimum in a layer, it drops down to the denser layer below and continues the search. HNSW offers incredibly fast search times and high recall, but consumes significant memory as it does not compress the vectors and must store the graph edges.

### 6.3 Implementation Example: FAISS

Facebook AI Similarity Search (FAISS) is a highly optimized library for efficient similarity search and clustering of dense vectors. Below is an architectural blueprint of how one mathematically implements and queries a vector index using FAISS.

```python
import numpy as np
import faiss

# 1. Configuration
dimension = 768           # Dimensionality of the embeddings (e.g., BERT)
database_size = 1000000   # Number of documents in the database
num_clusters = 1024       # Number of Voronoi cells for IVF
m = 32                    # Number of sub-quantizers for PQ
k = 10                    # Number of nearest neighbors to retrieve

# Generate synthetic document embeddings (normalized for cosine similarity)
np.random.seed(42)
db_vectors = np.random.random((database_size, dimension)).astype('float32')
faiss.normalize_L2(db_vectors) 

# 2. Index Construction (IVFPQ)
# The index consists of an Inverted File (IVF) and a Product Quantizer (PQ)
# Inner product (faiss.METRIC_INNER_PRODUCT) with normalized vectors is mathematically equivalent to cosine similarity.
quantizer = faiss.IndexFlatIP(dimension) 
index = faiss.IndexIVFPQ(quantizer, dimension, num_clusters, m, 8) 
# '8' specifies the number of bits allocated per sub-vector (256 centroids per sub-space)

# 3. Training the Index
# The index must be trained to learn the Voronoi cells and PQ centroids.
# In a real scenario, train on a representative subset of your actual data.
print("Training index...")
index.train(db_vectors[:50000]) # Train on a 50k subset
print(f"Index is trained: {index.is_trained}")

# 4. Adding Vectors
print("Adding vectors to the database...")
index.add(db_vectors)
print(f"Total vectors indexed: {index.ntotal}")

# 5. Querying the Vector Database
# Generate a query vector
query_vector = np.random.random((1, dimension)).astype('float32')
faiss.normalize_L2(query_vector)

# Configure search parameters
# nprobe sets the number of Voronoi cells to visit. Higher nprobe = better accuracy, slower speed.
index.nprobe = 10 

print(f"Searching for the top {k} nearest neighbors...")
# Search returns distances (scores) and the indices of the neighbors in the DB
distances, indices = index.search(query_vector, k)

print("\nSearch Results:")
for i in range(k):
    print(f"Rank {i+1} | Document ID: {indices[0][i]} | Cosine Similarity Score: {distances[0][i]:.4f}")
```

### 6.4 Ecosystem of Vector Databases

While FAISS is a library, the industry has shifted towards managed Vector Databases that wrap ANN libraries with enterprise features like CRUD operations, distributed architecture, High Availability, and Role-Based Access Control.

*   **Milvus:** An open-source, highly scalable vector database built on top of FAISS, HNSWLib, and Annoy. It is designed for massive-scale distributed architectures.
*   **Pinecone:** A managed, cloud-native vector database designed for developer ease of use, eliminating the need to manage infrastructure or tune complex ANN hyperparameters manually.
*   **Qdrant:** An open-source vector search engine written in Rust, utilizing HNSW and custom payload filtering to allow complex SQL-like WHERE clauses alongside vector similarity search.
*   **PostgreSQL with pgvector:** The `pgvector` extension allows PostgreSQL to store dense vectors and perform exact and approximate neighbor search directly within the traditional relational database framework, simplifying tech stacks that don't yet require a dedicated standalone vector database.

### 6.5 Conclusion

The evolution from one-hot encoding to dense word embeddings (Word2Vec, GloVe, FastText) represents the shift from symbolic to continuous mathematics in NLP. By translating human language into multi-dimensional geometry, models acquired the ability to "understand" semantics through spatial proximity. Today, this foundational mathematics powers the entire generative AI revolution, where massive Vector Databases execute billion-scale approximate searches in milliseconds to retrieve context for Large Language Models via Retrieval-Augmented Generation (RAG).
