# Module 2: Self-Attention Mechanism

## Prerequisites
- Module 1 (Tokens, Embeddings, Positional Encoding)
- Matrix multiplication properties
- Softmax function

## Objectives
- Understand the concepts of **Queries (Q)**, **Keys (K)**, and **Values (V)**.
- Learn how **Attention Scores** are computed and scaled.
- Manually trace through a numerical matrix example of self-attention.

## Intuition

Imagine you are at a library. 
- You have a question in mind: **Query (Q)** (e.g., "Machine Learning Basics").
- You look at the titles on the spine of the books: **Keys (K)**.
- Based on how well your Query matches a Key, you assign a relevance score (Attention Score).
- You extract the actual content of the books: **Values (V)**, weighted by their relevance score.

In Self-Attention, every word in a sentence looks at every other word to understand its context. For example, in "The bank of the river", the word "bank" uses its Query to check the Keys of other words. It heavily matches with "river", so it aggregates the Value of "river" to contextualize itself as a geographic feature rather than a financial institution.

## Mathematics

Given an input matrix $X \in \mathbb{R}^{N \times d}$ (where $N$ is sequence length, $d$ is embedding dimension).
We have three learned weight matrices: $W^Q \in \mathbb{R}^{d \times d_k}$, $W^K \in \mathbb{R}^{d \times d_k}$, and $W^V \in \mathbb{R}^{d \times d_v}$.

1. **Compute Q, K, V:**
   $$ Q = X W^Q $$
   $$ K = X W^K $$
   $$ V = X W^V $$

2. **Compute Raw Attention Scores:**
   We compute the dot product of every Query with every Key:
   $$ \text{Scores} = Q K^T $$
   This results in an $N \times N$ matrix.

3. **Scale the Scores:**
   We divide the scores by $\sqrt{d_k}$ to prevent the dot products from growing too large, which pushes the softmax function into regions with extremely small gradients (vanishing gradients).
   $$ \text{Scaled Scores} = \frac{Q K^T}{\sqrt{d_k}} $$

4. **Apply Softmax:**
   Apply softmax along the last dimension to get a probability distribution (weights sum to 1).
   $$ A = \text{softmax}\left(\frac{Q K^T}{\sqrt{d_k}}\right) $$

5. **Compute the Output:**
   Multiply the attention weights by the Values.
   $$ \text{Output} = A V $$

**Complete Equation:**
$$ \text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V $$

## Numerical Example

Let sequence length $N = 2$ (e.g., "Hello World"), embedding dimension $d=2$.
Assume our generated $Q, K, V$ (after multiplying $X$ by the weights) are:

$$ Q = \begin{bmatrix} 1 & 0 \\ 0 & 2 \end{bmatrix}, K = \begin{bmatrix} 1 & 1 \\ 0 & 2 \end{bmatrix}, V = \begin{bmatrix} 10 & 20 \\ 30 & 40 \end{bmatrix} $$

Here $d_k = 2$, so $\sqrt{d_k} \approx 1.414$.

**Step 1: Q K^T**
$$ K^T = \begin{bmatrix} 1 & 0 \\ 1 & 2 \end{bmatrix} $$
$$ Q K^T = \begin{bmatrix} 1 & 0 \\ 0 & 2 \end{bmatrix} \begin{bmatrix} 1 & 0 \\ 1 & 2 \end{bmatrix} = \begin{bmatrix} (1\cdot1 + 0\cdot1) & (1\cdot0 + 0\cdot2) \\ (0\cdot1 + 2\cdot1) & (0\cdot0 + 2\cdot2) \end{bmatrix} = \begin{bmatrix} 1 & 0 \\ 2 & 4 \end{bmatrix} $$

**Step 2: Scale**
$$ \frac{Q K^T}{1.414} = \begin{bmatrix} 0.707 & 0 \\ 1.414 & 2.828 \end{bmatrix} $$

**Step 3: Softmax (row-wise)**
For row 1 $[0.707, 0]$: $e^{0.707} \approx 2.03, e^0 = 1$. Sum $\approx 3.03$. Softmax $\approx [0.67, 0.33]$.
For row 2 $[1.414, 2.828]$: $e^{1.414} \approx 4.11, e^{2.828} \approx 16.9$. Sum $\approx 21.01$. Softmax $\approx [0.20, 0.80]$.

$$ A = \begin{bmatrix} 0.67 & 0.33 \\ 0.20 & 0.80 \end{bmatrix} $$

*(Notice: Row 1 attends mostly to word 1. Row 2 attends mostly to word 2).*

**Step 4: Multiply by V**
$$ \text{Output} = \begin{bmatrix} 0.67 & 0.33 \\ 0.20 & 0.80 \end{bmatrix} \begin{bmatrix} 10 & 20 \\ 30 & 40 \end{bmatrix} = \begin{bmatrix} 16.6 & 26.6 \\ 26.0 & 36.0 \end{bmatrix} $$

## Interview Questions
1. **Why do we scale the dot product by $\sqrt{d_k}$?**
   *Answer:* As the dimension $d_k$ grows, the dot products tend to grow large in magnitude. Large values passed into the softmax function result in gradients extremely close to 0, hindering weight updates. Scaling ensures the variance of the dot product remains close to 1 (assuming Q and K have mean 0 and variance 1).
2. **What is the time complexity of Self-Attention?**
   *Answer:* Computing $Q K^T$ takes $O(N^2 \cdot d)$. Thus, self-attention scales quadratically with sequence length $N$, which becomes a bottleneck for long documents.
