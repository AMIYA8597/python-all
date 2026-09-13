# Master Revision Cheat Sheet

Quick reference notes and formulas for rapid review before interviews or exams.

## 1. Python Quick Reference

*   **List Comprehension**: `[expression for item in iterable if condition]`
*   **Dictionary Comprehension**: `{key_expr: value_expr for item in iterable if condition}`
*   **Lambda Function**: `lambda args: expression`
*   **Map**: `map(function, iterable)`
*   **Filter**: `filter(function, iterable)`
*   **Dunder Methods**:
    *   `__init__`: Constructor
    *   `__str__`: User-friendly string representation
    *   `__repr__`: Developer string representation
    *   `__len__`: Returns length
    *   `__getitem__`: Allows indexing (`obj[key]`)

## 2. DSA Time Complexities (Average Case)

| Data Structure | Access | Search | Insertion | Deletion |
| :--- | :--- | :--- | :--- | :--- |
| **Array (Dynamic)** | O(1) | O(n) | O(1) am | O(n) |
| **Linked List** | O(n) | O(n) | O(1) | O(1) |
| **Binary Search Tree**| O(log n)| O(log n)| O(log n) | O(log n) |
| **Hash Table** | N/A | O(1) | O(1) | O(1) |
| **Min/Max Heap** | O(1)* | O(n) | O(log n) | O(log n)*|

*(Note: Accessing min/max is O(1). Deleting min/max is O(log n).)*

| Sorting Algorithm | Time (Best) | Time (Avg) | Time (Worst)| Space |
| :--- | :--- | :--- | :--- | :--- |
| **Quick Sort** | O(n log n) | O(n log n) | O(n^2) | O(log n) |
| **Merge Sort** | O(n log n) | O(n log n) | O(n log n) | O(n) |
| **Heap Sort** | O(n log n) | O(n log n) | O(n log n) | O(1) |

## 3. Machine Learning Formulas

*   **Linear Regression**: `y = wx + b`
*   **Mean Squared Error (MSE)**: `1/n * Σ(y_i - ŷ_i)^2`
*   **Logistic Regression (Sigmoid)**: `σ(z) = 1 / (1 + e^-z)`
*   **Precision**: `TP / (TP + FP)` (Out of all predicted positives, how many were actually positive?)
*   **Recall (Sensitivity)**: `TP / (TP + FN)` (Out of all actual positives, how many did we find?)
*   **F1-Score**: `2 * (Precision * Recall) / (Precision + Recall)` (Harmonic mean of precision and recall)
*   **Entropy**: `-Σ p(x) * log2(p(x))`

## 4. Deep Learning & Transformer Basics

*   **ReLU Activation**: `f(x) = max(0, x)`
*   **Softmax Activation**: `e^z_i / Σ e^z_j` (Converts logits to probabilities)
*   **Self-Attention Equation**: `Attention(Q, K, V) = softmax(QK^T / √d_k)V`
    *   `Q`: Query (What I am looking for)
    *   `K`: Key (What I have to offer)
    *   `V`: Value (What I actually am)
    *   `d_k`: Dimension of key vectors (scaling factor)

## 5. RAG Pipeline Core Steps

1.  **Ingestion**: Load documents (PDFs, Web pages).
2.  **Chunking**: Split documents into semantic chunks (e.g., 512 tokens).
3.  **Embedding**: Convert text chunks into dense vectors using an embedding model (e.g., text-embedding-ada-002).
4.  **Vector DB**: Store vectors in a database (e.g., Pinecone, Chroma).
5.  **Retrieval**: Convert user query to vector, perform cosine similarity search against DB to find top-k chunks.
6.  **Generation**: Pass top-k chunks + original query as context to an LLM to generate the final answer.
