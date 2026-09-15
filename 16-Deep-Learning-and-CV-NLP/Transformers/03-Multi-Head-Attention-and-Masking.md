# Multi-Head Attention and Masking in Transformers: A Deep Mathematical Dive

## 1. Introduction to the Attention Paradigm
The advent of the Transformer architecture, heralded by Vaswani et al. in the landmark 2017 paper *"Attention Is All You Need"*, orchestrated a paradigm shift across the landscape of deep learning. Prior to the Transformer, sequence modeling was dominated by Recurrent Neural Networks (RNNs) and Long Short-Term Memory (LSTM) networks. While effective, these recurrent architectures were bottlenecked by their sequential nature—processing token $t$ inherently required the hidden state from token $t-1$. This sequential dependency precluded parallelization across the sequence length, stifling training efficiency on modern parallel hardware like GPUs and TPUs.

The Transformer eradicated this bottleneck by entirely discarding recurrence in favor of the **Attention Mechanism**, specifically *Scaled Dot-Product Attention* and its highly parallelizable extension, *Multi-Head Attention*. By allowing the model to look at the entire sequence simultaneously and compute the relevance (or "attention") of every token with respect to every other token in $O(1)$ sequential operations, Transformers unlocked unprecedented scaling capabilities.

However, the raw attention mechanism is, in a sense, *too* powerful and *too* unconstrained. It indiscriminately connects every element in the sequence. In real-world applications, this unrestricted information flow is often problematic. 
1. **The Autoregressive Problem:** In generative tasks (like language modeling in GPT), predicting the $t$-th token must depend *only* on the tokens preceding it. If the attention mechanism can "look ahead" into the future tokens during training, the model will "cheat," learning a trivial identity mapping rather than the underlying language distribution.
2. **The Variable-Length Problem:** Real-world data comes in variable lengths, but hardware accelerators require fixed-size, rectangular matrices (tensors) for efficient batching. This necessitates padding shorter sequences with dummy tokens. Without intervention, the attention mechanism will mistakenly incorporate these meaningless padding tokens into the representation of actual words.

To tame the raw power of attention and enforce these critical structural and logical constraints, we introduce **Masking**. Masking is not merely a software trick; it is a fundamental mathematical operation integrated directly into the attention formulation.

In this extensive guide, we will embark on a rigorous mathematical deconstruction of Masking and Multi-Head Attention. We will detail the mechanics of Causal (Autoregressive) Masking and Padding Masking, dissecting how negative infinity matrices manipulate the softmax function to sever unwanted connections. We will then transition into Multi-Head Attention, providing a comprehensive tensor-level breakdown of how the embedding space is shattered into subspaces, processed in parallel, and definitively reconstructed through concatenation and final linear projections to restore the original dimensionality.


## 2. Scaled Dot-Product Attention: The Mathematical Primitives
To understand how masking modifies attention, we must first establish the baseline mathematical primitives of the unmasked Scaled Dot-Product Attention.

The core intuition of attention is akin to a differentiable database retrieval system. You have a **Query**, and you want to retrieve information from a database of **Key-Value** pairs. The attention mechanism calculates the similarity between your Query and all Keys, and uses these similarity scores to return a weighted average of the corresponding Values.

Let us define the dimensions:
- $d_{model}$: The dimension of the input embeddings (e.g., 512 in the original Transformer).
- $N$: The sequence length of the queries.
- $M$: The sequence length of the keys and values (in self-attention, $N = M$).
- $d_k$: The dimension of the queries and keys.
- $d_v$: The dimension of the values.

We operate on three matrices derived from the input representations via learned linear transformations:
1.  **Query Matrix $Q \in \mathbb{R}^{N \times d_k}$**
2.  **Key Matrix $K \in \mathbb{R}^{M \times d_k}$**
3.  **Value Matrix $V \in \mathbb{R}^{M \times d_v}$**

The unmasked Scaled Dot-Product Attention is formally defined as:

$$ \text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V $$

### 2.1 The Alignment Score Matrix
The operation begins with the matrix multiplication $QK^T$.
$Q$ has shape $(N, d_k)$ and $K^T$ has shape $(d_k, M)$. Their product yields a matrix $E \in \mathbb{R}^{N \times M}$:

$$ E = QK^T $$

Each element $e_{ij}$ in matrix $E$ represents the raw dot product (similarity) between the $i$-th query vector $q_i$ and the $j$-th key vector $k_j$.
$$ e_{ij} = q_i \cdot k_j = \sum_{d=1}^{d_k} q_{id} k_{jd} $$

This $N \times M$ matrix $E$ is the "alignment score matrix". It dictates how much "attention" query $i$ wants to pay to key $j$.

### 2.2 The Scaling Factor
If $d_k$ is large, the dot products $q_i \cdot k_j$ can grow extremely large in magnitude. To see why, consider two independent vectors $q$ and $k$ whose components are random variables with mean 0 and variance 1. The variance of their dot product $q \cdot k = \sum_{i=1}^{d_k} q_i k_i$ is exactly $d_k$. As $d_k$ increases, the variance, and thus the expected magnitude of the dot product, scales linearly with $d_k$.

Large magnitude values in the alignment matrix are problematic for the subsequent softmax function. The softmax function amplifies the largest values and suppresses smaller ones. If the input values are very large, the softmax output becomes extremely peaked (one value close to 1, the rest close to 0). In these saturated regions, the gradient of the softmax function approaches zero, leading to the notorious **vanishing gradient problem** during backpropagation, halting the training process.

To counteract this, the raw alignment scores are divided by the square root of the key dimension, $\sqrt{d_k}$. This scaling ensures that the variance of the scaled dot products remains approximately 1, regardless of the dimension $d_k$.

$$ S = \frac{E}{\sqrt{d_k}} = \frac{QK^T}{\sqrt{d_k}} $$

### 2.3 The Softmax Transformation
The scaled alignment matrix $S$ is then passed through the row-wise softmax function to yield the Attention Weight Matrix $A \in \mathbb{R}^{N \times M}$.

$$ A_{ij} = \text{softmax}(S_{ij}) = \frac{\exp(S_{ij})}{\sum_{m=1}^{M} \exp(S_{im})} $$

The softmax function ensures two critical properties:
1.  **Positivity:** All attention weights $A_{ij}$ are strictly between 0 and 1.
2.  **Normalization:** Every row in $A$ sums exactly to 1 ($\sum_{m} A_{im} = 1$).

This transforms the raw similarities into a valid probability distribution over the keys for every query.

### 2.4 Context Vector Aggregation
Finally, the attention weight matrix $A$ is multiplied by the Value matrix $V$.
$A$ is $(N, M)$ and $V$ is $(M, d_v)$. The resulting matrix $O \in \mathbb{R}^{N \times d_v}$ represents the output context vectors.

$$ O = AV $$

The $i$-th row of $O$ (the context vector for the $i$-th query) is a convex combination (a weighted average) of all the value vectors $v_j$, where the weights are dictated by the probability distribution in the $i$-th row of $A$.

$$ o_i = \sum_{j=1}^{M} A_{ij} v_j $$

In this pristine formulation, every $o_i$ incorporates information from every $v_j$. To selectively break these connections, we introduce Masking.


## 3. The Mathematics of Masking: The Power of Negative Infinity
Masking modifies the core attention equation by injecting a matrix of constraints *before* the softmax operation. The masked attention formulation is:

$$ \text{Attention}(Q, K, V, M_{ask}) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}} + M_{ask}\right)V $$

Where $M_{ask} \in \mathbb{R}^{N \times M}$ is the masking matrix.

### 3.1 Exploiting the Softmax Asymptote
The goal of masking is to force specific attention weights $A_{ij}$ to be exactly zero, effectively erasing any flow of information from value $v_j$ to output $o_i$.

Because the attention weights are derived via the softmax function, we must engineer the inputs to the softmax to yield zero. Let's revisit the softmax formula for an individual element:

$$ A_{ij} = \frac{\exp(x_{ij})}{\sum_m \exp(x_{im})} $$

To make $A_{ij} = 0$, the numerator $\exp(x_{ij})$ must be $0$.
The exponential function $\exp(x)$ is strictly positive for all real numbers $x$. It only approaches $0$ asymptotically as $x$ approaches negative infinity ($-\infty$).

$$ \lim_{x \to -\infty} \exp(x) = 0 $$

Therefore, to completely mask out the connection between query $i$ and key $j$, we must ensure that the pre-softmax score for that pair is $-\infty$.

### 3.2 Constructing the Mask Matrix
We define the masking matrix $M_{ask}$ such that it acts as an additive filter:
-   If the connection from key $j$ to query $i$ is **allowed**, we add **0**. Adding 0 leaves the scaled dot-product unchanged.
-   If the connection from key $j$ to query $i$ is **prohibited**, we add **$-\infty$** (in practical computational frameworks, this is often a very large negative float, such as `-1e9` or the minimum representable value of the floating-point type).

$$
M_{ask}[i, j] =
\begin{cases}
0 & \text{if connection } (i, j) \text{ is unmasked / allowed} \\
-\infty & \text{if connection } (i, j) \text{ is masked / prohibited}
\end{cases}
$$

Let the scaled dot-product matrix be $S = \frac{QK^T}{\sqrt{d_k}}$. We compute the masked pre-scores $S_{masked} = S + M_{ask}$:

$$
S_{masked}[i, j] =
\begin{cases}
S[i, j] + 0 = S[i, j] & \text{if allowed} \\
S[i, j] - \infty = -\infty & \text{if prohibited}
\end{cases}
$$

When the softmax function is applied row-wise to $S_{masked}$:
- For prohibited connections, $\exp(-\infty) = 0$. The numerator is 0, so the resulting attention weight is $0$.
- For allowed connections, the denominator $\sum \exp(S_{masked})$ sums only over the $\exp(S[i,k])$ of the *allowed* connections, because the prohibited connections contribute exactly $0$ to the sum.

Thus, the probability mass is redistributed exclusively among the allowed connections, completely isolating the query from the masked keys.


## 4. Causal (Autoregressive) Masking
The most structurally rigorous application of this principle is **Causal Masking**, crucial for training autoregressive sequence models (like the decoders in GPT-3, LLaMA, etc.).

### 4.1 The Autoregressive Imperative
Language generation is fundamentally a left-to-right, autoregressive process. Given a prompt, the model predicts the first token. It then takes that token, appends it to the prompt, and predicts the second token, and so forth. Mathematically, it models the joint probability of a sequence $X = (x_1, x_2, \dots, x_N)$ via the chain rule of probability:

$$ P(X) = \prod_{t=1}^{N} P(x_t \mid x_1, \dots, x_{t-1}) $$

During training, we want to maximize this likelihood. However, processing one token at a time sequentially is egregiously slow. The breakthrough of the Transformer decoder is its ability to train on the entire sequence $X$ in parallel. We pass the whole sequence into the model simultaneously.

Here lies the paradox: if we pass the whole sequence at once, the standard self-attention mechanism will allow the representation of token $x_t$ (the query) to attend to the key of token $x_{t+1}$ (the future). The model would simply "look ahead" at the target token it is supposed to predict, yielding near-zero loss during training but catastrophically failing during inference when the future tokens are unavailable.

We must break the symmetry of time. We must ensure that query $t$ can only attend to keys $1, 2, \dots, t$.

### 4.2 The Lower Triangular Mask
In self-attention, queries and keys are derived from the same input sequence, so the alignment matrix $S$ is a square $N \times N$ matrix. The index $i$ corresponds to the current query position, and $j$ corresponds to the key position.

The causal constraint states: Query at position $i$ cannot attend to Key at position $j$ if $j > i$.

This maps perfectly to a matrix constraint: the upper triangular portion (above the main diagonal) of the attention matrix must be masked out. The main diagonal ($j=i$) and the lower triangular portion ($j < i$) are allowed.

The Causal Mask $M_{causal} \in \mathbb{R}^{N \times N}$ is rigorously defined as:

$$
M_{causal}[i, j] =
\begin{cases}
0 & \text{if } i \ge j \text{ (past and present)} \\
-\infty & \text{if } i < j \text{ (future)}
\end{cases}
$$

Let's visualize this for a sequence of 4 tokens ($N=4$):

$$
M_{causal} = \begin{bmatrix}
0 & -\infty & -\infty & -\infty \\
0 & 0 & -\infty & -\infty \\
0 & 0 & 0 & -\infty \\
0 & 0 & 0 & 0
\end{bmatrix}
$$

### 4.3 Execution Step-by-Step
Let's trace the computation. Assume our scaled dot-product matrix $S$ is:

$$
S = \begin{bmatrix}
2.1 & 1.5 & -0.5 & 3.0 \\
-1.2 & 0.8 & 1.1 & 0.4 \\
3.3 & -2.0 & 0.5 & 1.8 \\
0.1 & 1.4 & -0.9 & 2.2
\end{bmatrix}
$$

We apply the additive causal mask:

$$
S_{masked} = S + M_{causal} = \begin{bmatrix}
2.1 & -\infty & -\infty & -\infty \\
-1.2 & 0.8 & -\infty & -\infty \\
3.3 & -2.0 & 0.5 & -\infty \\
0.1 & 1.4 & -0.9 & 2.2
\end{bmatrix}
$$

Now, we apply the row-wise softmax. Let's calculate it for the second row ($i=2$):
The pre-softmax values are $[-1.2, 0.8, -\infty, -\infty]$.
The exponentials are $[e^{-1.2}, e^{0.8}, e^{-\infty}, e^{-\infty}] \approx [0.301, 2.225, 0, 0]$.
The sum of exponentials is $0.301 + 2.225 = 2.526$.
The normalized probabilities are $[0.301/2.526, 2.225/2.526, 0, 0] = [0.119, 0.881, 0, 0]$.

The resulting Attention Weight matrix $A$ looks like this:

$$
A = \text{softmax}(S_{masked}) = \begin{bmatrix}
1.000 & 0 & 0 & 0 \\
0.119 & 0.881 & 0 & 0 \\
0.932 & 0.005 & 0.063 & 0 \\
0.076 & 0.278 & 0.028 & 0.618
\end{bmatrix}
$$

The mathematical purity is absolute. The upper triangle is strictly zero. Token 1 pays 100% of its attention to itself. Token 2 distributes its attention between tokens 1 and 2, but structurally ignores 3 and 4. The causality constraint is perfectly satisfied in a single, parallelizable tensor operation.

### 4.4 PyTorch Implementation of Causal Masking
In PyTorch, creating a causal mask leverages the `torch.tril` (lower triangle) function.

```python
import torch

def create_causal_mask(seq_len):
    # Create an N x N matrix of ones
    ones = torch.ones(seq_len, seq_len)
    # Extract the lower triangular part (including diagonal)
    mask = torch.tril(ones)
    # Replace 0s with -inf, and 1s with 0
    # mask == 0 creates a boolean tensor where upper triangle is True
    # masked_fill_ fills those True positions with -infinity
    causal_mask = torch.zeros(seq_len, seq_len).masked_fill_(mask == 0, float('-inf'))
    return causal_mask

seq_length = 4
causal_mask = create_causal_mask(seq_length)
print(causal_mask)
# Output:
# tensor([[0., -inf, -inf, -inf],
#         [0., 0., -inf, -inf],
#         [0., 0., 0., -inf],
#         [0., 0., 0., 0.]])
```


## 5. Padding Masking: Handling Data Asymmetry
While causal masking deals with the logic of time, **Padding Masking** deals with the realities of hardware.

### 5.1 The Batching Constraint
GPUs process data in fixed-dimensional tensors. To train efficiently, we process data in mini-batches. However, sentences in a dataset have varying lengths.
Consider a batch of two sentences:
1. "The cat sat." (3 tokens)
2. "The quick brown fox jumped over the lazy dog." (9 tokens)

To tensorize this batch, we must determine a maximum sequence length (e.g., 9) and pad the shorter sentence with meaningless `<PAD>` tokens to match this dimension.
Sentence 1 becomes: `["The", "cat", "sat", ".", "<PAD>", "<PAD>", "<PAD>", "<PAD>", "<PAD>"]`.

### 5.2 The Corrupting Influence of Padding
If we apply standard attention, the tokens "The", "cat", and "sat" will compute their dot-products against the keys of the `<PAD>` tokens. Because neural networks initialize with random weights, these dot-products won't be zero. After softmax, the probability distribution will assign a non-zero weight to the `<PAD>` tokens.
Consequently, the context vector $o_i$ for the word "cat" will mix in the Value vectors associated with the `<PAD>` tokens. The representation of "cat" becomes corrupted by meaningless noise, severely degrading model accuracy.

We must explicitly block any query from attending to any key that corresponds to a `<PAD>` token.

### 5.3 Structuring the Padding Mask
Unlike the causal mask, which is purely geometric ($i$ vs $j$), the padding mask is data-dependent. We must look at the input sequence and identify which positions contain pad tokens.

Let $P$ be a boolean vector of length $M$ representing the keys, where $P_j = \text{True}$ if the $j$-th key is a `<PAD>` token, and $\text{False}$ otherwise.

The padding mask matrix $M_{pad} \in \mathbb{R}^{N \times M}$ broadcasts this boolean condition across all $N$ queries. If key $j$ is a pad token, *no* query should attend to it. Therefore, the entire $j$-th column of the attention matrix must be masked.

$$
M_{pad}[i, j] =
\begin{cases}
-\infty & \text{if } P_j \text{ is True (the key is a pad token)} \\
0 & \text{if } P_j \text{ is False (the key is a real token)}
\end{cases}
$$

Notice that the row index $i$ does not affect the condition. We mask entire columns corresponding to padded keys.

*Note on Query Padding:* If a query itself is a pad token, its resulting context vector doesn't matter because the loss function will mask out predictions at pad positions anyway. However, for thoroughness, frameworks often mask pad-queries from attending to anything but themselves to prevent NaNs during computation. But the primary concern is masking the keys.

### 5.4 Synthesizing Masks
In a decoder, both Causal and Padding masks are active simultaneously. We must combine them. Because both utilize the additive $-\infty$ paradigm, combining them is trivial.

A connection is blocked if it violates causality OR if it is a pad token.
Therefore, the combined mask is simply the element-wise minimum of the two masks, or equivalently, an element-wise logical OR operation converted to $-\infty$/0.

$$ M_{combined}[i, j] = \min(M_{causal}[i, j], M_{pad}[i, j]) $$

Any position that is $-\infty$ in either mask becomes $-\infty$ in the combined mask. The attention mechanism flawlessly respects both constraints.


## 6. Multi-Head Attention: Dimensionality and Subspaces
We now shift our focus from the constraints of masking to the expressive expansion provided by **Multi-Head Attention** (MHA).

### 6.1 The Fallacy of Monolithic Attention
Single-head (Scaled Dot-Product) attention computes a single, scalar attention weight $A_{ij}$ between a query and a key. This implies that there is only one "type" of relationship that the network can learn.

However, language is a deeply multi-faceted phenomenon. Consider the sentence:
*"The company fired the CEO because he embezzled funds."*

When analyzing the token *"he"*, the model needs to understand two completely orthogonal relationships simultaneously:
1.  **Syntactic/Grammatical:** "he" is the subject of the verb "embezzled" (looking forward).
2.  **Semantic/Coreference:** "he" refers back to the entity "the CEO" (looking backward).

If the model has only a single attention head, it must compromise. The attention distribution must average out to capture both, resulting in a diffuse, muddy representation that masters neither relationship.

Multi-Head Attention solves this by explicitly partitioning the computational space, allowing the model to project the queries, keys, and values into multiple distinct, lower-dimensional "subspaces," and performing attention in each subspace in parallel.

### 6.2 Linear Projections: Shattering the Embedding
Let the original embedding dimension of our tokens be $d_{model}$ (e.g., 512).
We define a hyperparameter $h$, the number of attention "heads" (e.g., 8).
We define the dimension of each subspace for queries/keys as $d_k$ and for values as $d_v$.
In the standard Transformer, we set $d_k = d_v = d_{model} / h = 512 / 8 = 64$.

For each head $i \in \{1, 2, \dots, h\}$, we define three learned projection weight matrices:
-   $W_i^Q \in \mathbb{R}^{d_{model} \times d_k}$
-   $W_i^K \in \mathbb{R}^{d_{model} \times d_k}$
-   $W_i^V \in \mathbb{R}^{d_{model} \times d_v}$

Let $Q_{in}, K_{in}, V_{in}$ be the input matrices of shape $(N, d_{model})$.
We project the inputs into the $i$-th subspace:
$$ Q_i = Q_{in} W_i^Q \quad \in \mathbb{R}^{N \times d_k} $$
$$ K_i = K_{in} W_i^K \quad \in \mathbb{R}^{M \times d_k} $$
$$ V_i = V_{in} W_i^V \quad \in \mathbb{R}^{M \times d_v} $$

Because the projection matrices are distinct for each head $i$, each head learns to project the $d_{model}$-dimensional input into a different 64-dimensional feature space. Head 1's projection might isolate syntactic markers, while Head 2's isolates noun genders.

### 6.3 Parallel Attention Execution
Once projected, we apply the standard masked Scaled Dot-Product Attention independently to each of the $h$ heads:

$$ \text{head}_i = \text{Attention}(Q_i, K_i, V_i, M_{ask}) = \text{softmax}\left(\frac{Q_i K_i^T}{\sqrt{d_k}} + M_{ask}\right)V_i $$

The output of each head, $\text{head}_i$, is a matrix of shape $(N, d_v)$.
We now have $h$ distinct output matrices, each capturing a unique contextualized interpretation of the sequence within its specific $d_v$-dimensional subspace.


## 7. Concatenation and Final Projection: Reassembling the Embedding
The objective of a Transformer layer (e.g., an Encoder block) is to take a sequence of vectors of dimension $d_{model}$ and output a sequence of updated vectors of the same dimension $d_{model}$, so they can be fed into the next layer or the Feed-Forward Network.

We currently have $h$ independent matrices of shape $(N, d_v)$. We must recombine them.

### 7.1 The Mechanism of Concatenation
The standard procedure is to **concatenate** the outputs of all $h$ heads along the feature dimension (the columns).

Let $H = \text{Concat}(\text{head}_1, \text{head}_2, \dots, \text{head}_h)$.

Mathematically, for the $j$-th token in the sequence, its representation in $\text{head}_1$ is a vector of length $d_v$. Its representation in $\text{head}_2$ is another vector of length $d_v$. Concatenation stitches these vectors together end-to-end.

Since we have $h$ heads, and each produces a vector of length $d_v$, the concatenated vector for each token has a length of $h \times d_v$.

Because we rigorously enforced $d_k = d_v = d_{model} / h$ during the design of the architecture, we have:
$$ h \times d_v = h \times (d_{model} / h) = d_{model} $$

Thus, the concatenated matrix $H$ has the shape $(N, d_{model})$. The original dimensionality has been perfectly restored.

For example, with $d_{model} = 512$ and $h=8$:
Each head produces a $(N, 64)$ matrix.
Concatenating 8 of these along the column axis yields a $(N, 512)$ matrix.

### 7.2 Why Concatenate? The Geometry of Disjoint Features
Why do we concatenate instead of, say, summing or averaging the head outputs?

If we were to sum the outputs of the heads ($\sum_{i=1}^h \text{head}_i$), we would be performing vector addition in a $d_v$-dimensional space. This would fundamentally conflict with the purpose of MHA.
If Head 1 is capturing "verb-object" dependencies and Head 2 is capturing "pronoun-antecedent" dependencies, adding their output vectors together would scramble these distinct semantic signals into a single confused vector. It implies that a "verb-object" signal is directly comparable and additive to a "pronoun" signal.

Concatenation avoids this destruction of information. It enforces a strict partitioning of the vector space.
In the concatenated 512-dimensional vector, dimensions 0-63 are exclusively reserved for the features learned by Head 1. Dimensions 64-127 belong exclusively to Head 2. The distinct, specialized insights gathered by each independent attention mechanism are preserved intact, side-by-side, within the macroscopic $d_{model}$ vector.

### 7.3 The Final Linear Transformation ($W^O$)
While concatenation restores the dimensionality and preserves information, it leaves the features disjoint. The features in dimensions 0-63 (Head 1) have not computationally interacted with the features in dimensions 64-127 (Head 2).

To synthesize a truly unified, comprehensive representation of the token, we apply one final learned linear transformation to the concatenated matrix. We define an output weight matrix $W^O \in \mathbb{R}^{d_{model} \times d_{model}}$.

$$ \text{MultiHead}(Q_{in}, K_{in}, V_{in}) = \text{Concat}(\text{head}_1, \dots, \text{head}_h) W^O $$

The matrix $W^O$ projects the partitioned, concatenated vector back into a dense, mixed $d_{model}$-dimensional space.
During training, $W^O$ learns how to intelligently combine the disparate signals from the different heads. It might learn that for a specific downstream task (like sentiment analysis), the signals from the "adjective-noun" head (Head 3) and the "negation" head (Head 7) should be heavily weighted and combined, while the signal from the "punctuation" head (Head 8) should be suppressed.

$W^O$ is the crucial mixing layer that transforms a collection of isolated subspace observations into a single, highly refined context vector.

### 7.4 Vectorization: The Reshape Trick
In deep learning frameworks, we do not actually run a `for` loop over the $h$ heads. That would be slow and fail to utilize the massive parallel architecture of GPUs. Instead, we use tensor reshaping to compute all heads simultaneously.

Rather than $h$ distinct weight matrices $W_i^Q$ of size $(d_{model}, d_k)$, we define a single monolithic weight matrix $W^Q$ of size $(d_{model}, d_{model})$.
1.  **Monolithic Projection:** $Q_{proj} = Q_{in} W^Q$. Shape: $(N, d_{model})$.
2.  **Reshape:** We reshape $Q_{proj}$ into a 3D tensor to separate the heads. Shape: $(N, h, d_k)$.
3.  **Transpose:** We permute the dimensions to bring the head dimension to the front, treating it as an auxiliary batch dimension. Shape: $(h, N, d_k)$.

When we do this for Queries, Keys, and Values, we can perform a single batched matrix multiplication:
`torch.bmm(Q, K.transpose(-2, -1))`
This operation computes the $(N, N)$ alignment matrix for all $h$ heads simultaneously. Shape of resulting scaled score matrix: $(h, N, N)$.

After applying masks and softmax, we multiply by $V$, yielding an output of shape $(h, N, d_k)$.
We transpose back to $(N, h, d_k)$.
To perform the **Concatenation**, we simply execute a memory reshape operation, flattening the last two dimensions: $(N, h \times d_k) \rightarrow (N, d_{model})$.
This single, virtually zero-cost reshape operation mathematically replicates the explicit concatenation of $h$ separate matrices. Finally, we multiply by $W^O$.


## 8. Putting It All Together: A PyTorch Implementation
To solidify the theory, let us examine a complete, vectorized implementation of Masked Multi-Head Attention in PyTorch, highlighting the precise mechanics of masking, reshaping, and concatenation.

```python
import torch
import torch.nn as nn
import math

class MultiHeadAttention(nn.Module):
    def __init__(self, d_model, num_heads):
        super(MultiHeadAttention, self).__init__()
        assert d_model % num_heads == 0, "d_model must be divisible by num_heads"
        
        self.d_model = d_model
        self.num_heads = num_heads
        self.d_k = d_model // num_heads
        
        # Monolithic linear projections for Q, K, V
        self.W_q = nn.Linear(d_model, d_model)
        self.W_k = nn.Linear(d_model, d_model)
        self.W_v = nn.Linear(d_model, d_model)
        
        # Final linear projection W_O
        self.W_o = nn.Linear(d_model, d_model)
        
    def scaled_dot_product_attention(self, Q, K, V, mask=None):
        # Q, K, V shape: (batch_size, num_heads, seq_len, d_k)
        
        # 1. Dot product Q and K^T. 
        # K.transpose(-2, -1) swaps the last two dims: (..., seq_len, d_k) -> (..., d_k, seq_len)
        # Resulting scores shape: (batch_size, num_heads, seq_len, seq_len)
        scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(self.d_k)
        
        # 2. Apply Masking (Causal or Padding)
        if mask is not None:
            # Mask must be broadcastable to (batch_size, num_heads, seq_len, seq_len)
            # The mask tensor contains 0 for allowed, 1 for prohibited
            # masked_fill_ replaces elements where mask == 1 with -infinity
            scores = scores.masked_fill_(mask == 1, float('-inf'))
            
        # 3. Softmax to get probabilities
        # Apply softmax along the last dimension (the keys)
        attention_weights = torch.softmax(scores, dim=-1)
        
        # 4. Multiply by V
        # Result shape: (batch_size, num_heads, seq_len, d_k)
        output = torch.matmul(attention_weights, V)
        
        return output, attention_weights

    def split_heads(self, x):
        '''
        Reshapes tensor from (batch_size, seq_len, d_model) 
        to (batch_size, num_heads, seq_len, d_k)
        '''
        batch_size, seq_len, _ = x.size()
        # Reshape to (batch_size, seq_len, num_heads, d_k)
        x = x.view(batch_size, seq_len, self.num_heads, self.d_k)
        # Transpose to (batch_size, num_heads, seq_len, d_k) for batched attention
        return x.transpose(1, 2)

    def forward(self, query, key, value, mask=None):
        batch_size = query.size(0)
        
        # 1. Apply monolithic linear projections
        # Shape: (batch_size, seq_len, d_model)
        Q = self.W_q(query)
        K = self.W_k(key)
        V = self.W_v(value)
        
        # 2. Split heads via reshape and transpose
        # Shape: (batch_size, num_heads, seq_len, d_k)
        Q = self.split_heads(Q)
        K = self.split_heads(K)
        V = self.split_heads(V)
        
        # 3. Compute Scaled Dot-Product Attention (parallelized across heads)
        # attn_output shape: (batch_size, num_heads, seq_len, d_k)
        attn_output, _ = self.scaled_dot_product_attention(Q, K, V, mask)
        
        # 4. Concatenation: Transpose back and Reshape
        # Transpose back: (batch_size, seq_len, num_heads, d_k)
        # .contiguous() is required in PyTorch before view() if memory layout was changed by transpose
        attn_output = attn_output.transpose(1, 2).contiguous()
        
        # Reshape to explicitly concatenate the heads: (batch_size, seq_len, num_heads * d_k)
        # Since num_heads * d_k = d_model, this restores the original dimensionality perfectly.
        concat_output = attn_output.view(batch_size, -1, self.d_model)
        
        # 5. Final Linear Transformation W_O
        # Shape: (batch_size, seq_len, d_model)
        output = self.W_o(concat_output)
        
        return output
```


## 9. Conclusion
The elegance of the Transformer architecture lies not just in the attention mechanism itself, but in the sophisticated mathematical tooling built around it.

**Masking** transforms attention from a chaotic, fully-connected graph into a highly controllable mechanism. By exploiting the asymptotic properties of the exponential function, negative infinity masking cleanly severs the flow of information without disrupting parallel matrix operations. Causal masking enforces the Arrow of Time, making autoregressive generation possible, while padding masking prevents hardware-necessitated batching artifacts from poisoning the model's semantic representations.

**Multi-Head Attention** amplifies the model's capacity by shattering the input embedding into distinct dimensional subspaces. By performing attention in parallel across these subspaces, the model can scrutinize the sequence through multiple independent lenses—syntactic, semantic, geometric. Finally, the mathematically guaranteed reconstruction through sequence **concatenation** ensures that these disjoint insights are preserved identically and side-by-side, perfectly restoring the $d_{model}$ dimensionality. The final projection $W^O$ then harmonizes these insights into the dense, contextualized representations that have driven modern AI to unprecedented heights.
