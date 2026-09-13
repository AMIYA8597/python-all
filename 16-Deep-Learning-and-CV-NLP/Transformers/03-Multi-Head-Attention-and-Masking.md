# Module 3: Multi-Head Attention and Masking

## Prerequisites
- Module 2 (Self-Attention, Q, K, V)

## Objectives
- Understand why a single attention head is insufficient and how **Multi-Head Attention** solves this.
- Learn the mechanics of **Causal Masking** (Look-ahead mask) for autoregressive generation.
- Understand **Padding Masks**.

## Intuition

### Multi-Head Attention
If we only have one set of Q, K, V matrices (one "head"), the model can only focus on one specific aspect of the sequence at a time. Words, however, relate to each other in multiple ways (e.g., grammatical structure, semantic meaning, pronoun reference). 
By having multiple "heads" (multiple parallel sets of Q, K, V matrices), the Transformer can jointly attend to information from different representation subspaces at different positions. One head might learn to look at the next word, another might look at the subject of a verb, etc.

### Causal Masking (Look-ahead Masking)
During training of a Decoder (like GPT), we predict the next word based on the previous words. However, the attention mechanism naturally looks at the *entire* sequence simultaneously. We must hide (mask) future tokens from the current token so the model can't "cheat" by looking ahead.

## Mathematics

### Multi-Head Attention
Instead of performing a single attention function with $d$-dimensional keys, values, and queries, we linearly project the queries, keys, and values $h$ times with different, learned linear projections to $d_k, d_k,$ and $d_v$ dimensions.

1. **Split into heads:** 
   For each head $i = 1, \dots, h$:
   $$ \text{head}_i = \text{Attention}(X W_i^Q, X W_i^K, X W_i^V) $$

2. **Concatenate:**
   Concatenate the outputs of all $h$ heads.
   $$ \text{MultiHead}(Q, K, V) = \text{Concat}(\text{head}_1, \dots, \text{head}_h) W^O $$
   Where $W^O$ is a final linear projection matrix.

Typically, $d_k = d_v = d_{model} / h$. This keeps the total computational cost similar to single-head attention with full dimensionality.

### Causal Masking
We apply a mask to the $Q K^T$ matrix before the softmax. The mask is an upper-triangular matrix filled with $-\infty$.

Let raw scores $S = \frac{Q K^T}{\sqrt{d_k}}$.
$$ M = \begin{bmatrix} 0 & -\infty & -\infty \\ 0 & 0 & -\infty \\ 0 & 0 & 0 \end{bmatrix} $$
$$ S_{masked} = S + M $$

When we apply softmax to $-\infty$, $e^{-\infty} = 0$. Therefore, attention to future tokens becomes exactly 0.

## Numerical Example (Masking)
Let $S = \begin{bmatrix} 2 & 4 \\ 1 & 3 \end{bmatrix}$ (Raw scores, seq_len=2)

Add the mask $M = \begin{bmatrix} 0 & -\infty \\ 0 & 0 \end{bmatrix}$:
$$ S_{masked} = \begin{bmatrix} 2 & 4 \\ 1 & 3 \end{bmatrix} + \begin{bmatrix} 0 & -\infty \\ 0 & 0 \end{bmatrix} = \begin{bmatrix} 2 & -\infty \\ 1 & 3 \end{bmatrix} $$

Apply Softmax row-wise:
- Row 1: Softmax(2, $-\infty$) $\rightarrow e^2 / (e^2 + 0) = 1.0$, $0 / (e^2 + 0) = 0.0$. Output = $[1.0, 0.0]$
- Row 2: Softmax(1, 3) $\rightarrow e^1 / (e^1 + e^3) \approx 0.12$, $e^3 / (e^1 + e^3) \approx 0.88$. Output = $[0.12, 0.88]$

Notice how row 1 (the first word) now puts 100% of its attention on itself, completely ignoring word 2!

## Interview Questions
1. **Why does multi-head attention not significantly increase computation compared to single-head attention?**
   *Answer:* Because we split the embedding dimension $d_{model}$ by the number of heads $h$. Each head operates on a smaller dimension $d_k = d_{model}/h$. The matrix multiplications are smaller, and when combined, the total FLOPs are roughly equivalent to a single head operating on the full dimension.
2. **What is a padding mask?**
   *Answer:* In practice, we batch sequences of different lengths by padding shorter sequences with a `<PAD>` token. We don't want the model to attend to these meaningless pad tokens. A padding mask applies $-\infty$ to the attention scores corresponding to `<PAD>` token positions across the entire sequence.
