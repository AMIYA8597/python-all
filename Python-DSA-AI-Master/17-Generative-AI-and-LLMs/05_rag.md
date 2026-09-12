# Retrieval-Augmented Generation (RAG)

Large Language Models have two major limitations:
1. **Hallucinations:** They sometimes confidently state false information.
2. **Knowledge Cutoff & Privacy:** They don't know facts that happened after their training data was collected, and they cannot access your private enterprise data.

**RAG (Retrieval-Augmented Generation)** solves this by giving the LLM an open-book test. Instead of relying solely on its internal weights, the LLM is provided with relevant external documents *at generation time*.

## The Standard RAG Pipeline

### Phase 1: Indexing (Data Preparation)
1. **Load Data:** Extract text from PDFs, databases, websites, etc.
2. **Chunking:** Split large documents into smaller, manageable chunks (e.g., 500 words each). LLMs have context limits, and smaller chunks yield more precise embeddings.
3. **Embedding:** Convert each chunk into a vector representation using an embedding model.
4. **Vector Database:** Store the vectors alongside the original text chunks in a Vector DB.

### Phase 2: Retrieval & Generation (Runtime)
1. **User Query:** The user asks a question.
2. **Embed Query:** The user's query is converted into an embedding using the *same* embedding model.
3. **Semantic Search:** The Vector DB retrieves the Top-K document chunks most similar to the query embedding.
4. **Augment Prompt:** The retrieved chunks are injected into the prompt as "Context".
5. **Generation:** The LLM reads the context and answers the user's question based *only* on that context.

*Example Augmented Prompt:*
```
Use the following context to answer the question. If the answer is not in the context, say "I don't know".
Context: [Chunk 1 Text] [Chunk 2 Text]
Question: [User's Question]
Answer:
```

## Advanced RAG Concepts

To improve standard RAG, several advanced techniques are used:
- **Hybrid Search:** Combining Semantic Search (dense vectors) with traditional Keyword Search (sparse vectors like BM25) to get the best of both worlds.
- **Re-ranking:** Retrieving a large number of chunks (e.g., 20) quickly, then using a specialized, more expensive Cross-Encoder model to accurately re-score and select the top 3-5 chunks.
- **Query Transformation:** Modifying the user's query before searching. (e.g., *Query Expansion* expands abbreviations, *HyDE* generates a hypothetical answer and embeds that).
- **Parent-Child Retrieval:** Chunking documents into small chunks for accurate vector retrieval, but passing the larger parent document (or surrounding context) to the LLM to provide broader context.
