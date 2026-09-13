# Attention Mechanism and Transformers

## Prerequisites
- Sequence Models (RNN/LSTM).
- Matrix multiplication.
- Softmax function.

## Objectives
- Understand the limitation of Seq2Seq models (the bottleneck problem).
- Learn the intuition and math behind the Attention Mechanism.
- Understand Self-Attention.
- Explore the Transformer architecture ("Attention Is All You Need").

## Intuition
In traditional Encoder-Decoder RNNs, the entire source sentence is compressed into a single, fixed-size context vector. For long sentences, this creates an information bottleneck.
**Attention** allows the model to look back at *all* the words in the input sequence and dynamically focus (attend) on the most relevant words for predicting the current target word.
**Self-Attention** applies this concept within a single sequence: for every word, it calculates how relevant every other word in the same sequence is. This allows the model to capture deep contextual relationships (e.g., resolving pronouns like "it" to the correct noun).
**Transformers** completely discard RNNs and rely entirely on self-attention mechanisms. Because there's no sequential recurrence, computation can be heavily parallelized, which led to modern LLMs (BERT, GPT).

## Mathematics
### Scaled Dot-Product Attention
Given matrices for Queries ($Q$), Keys ($K$), and Values ($V$):
1. Compute scores using dot product between $Q$ and $K^T$.
2. Scale the scores by dividing by the square root of the key dimension ($d_k$) to prevent gradients from becoming too small during softmax.
3. Apply Softmax to get attention weights (probabilities summing to 1).
4. Multiply weights by $V$ to get the final output.

$$ \text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V $$

## Code Reference
Refer to `08_nlp_attention.py` for a PyTorch implementation of Scaled Dot-Product Attention.

## Interview Questions
1. **Why do we divide by $\sqrt{d_k}$ in scaled dot-product attention?**
   *Answer:* For large values of $d_k$, the dot products grow large in magnitude, pushing the softmax function into regions where gradients are extremely small. Scaling stabilizes the gradients.
2. **What are Queries, Keys, and Values in attention?**
   *Answer:* Think of it like a search engine. The **Query** is what you are looking for. The **Keys** are the labels/descriptions of the items in the database. The **Values** are the actual items. Attention calculates how well the Query matches each Key, and returns a weighted sum of the Values.
3. **Why do Transformers require Positional Encoding?**
   *Answer:* Unlike RNNs, Transformers process all words simultaneously in parallel (no sequential steps). Without positional encodings, the model would treat the input as a Bag of Words, having no idea about the order of words in the sentence.
