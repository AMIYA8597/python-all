"""
# =============================================================================
# RETRIEVAL-AUGMENTED GENERATION (RAG) BASICS
# =============================================================================
# 
# ## A. Concept Name
# Retrieval-Augmented Generation (RAG) Basics
# 
# ## B. Educational Objective
# Understand the foundational architecture of RAG. RAG bridges the gap between 
# the static, pre-trained knowledge of Large Language Models (LLMs) and dynamic, 
# domain-specific, or proprietary data. The objective is to build a from-scratch 
# RAG pipeline demonstrating chunking, embedding generation, vector indexing, 
# retrieval, and augmented prompt generation.
# 
# ## C. Mathematical Background & Core Logic
# The retrieval in RAG typically relies on Vector Similarity.
# Text chunks and user queries are converted to high-dimensional vectors (Embeddings).
# 
# 1. **Cosine Similarity**: Measures the cosine of the angle between two non-zero vectors.
#    similarity(A, B) = (A · B) / (||A|| * ||B||)
#    where:
#    - A · B is the dot product: Σ (A_i * B_i)
#    - ||A|| is the L2 norm (magnitude): sqrt(Σ (A_i^2))
#    
# 2. **RAG Pipeline**:
#    - **Document Ingestion**: Parsing text from sources.
#    - **Chunking**: Splitting text into manageable pieces (e.g., overlapping windows).
#    - **Embedding**: Mapping chunks -> Vectors in R^d.
#    - **Vector Store**: Storing Vectors + Metadata.
#    - **Retrieval**: Computing similarity between Query Vector and Document Vectors.
#    - **Generation**: Prompting LLM: "Given context C, answer query Q."
# 
# ## D. Complexity (Time & Space)
# Let N = number of chunks, d = embedding dimensions, k = top-k chunks to retrieve.
# - **Time Complexity (Naive Retrieval)**: O(N * d) to compute similarity for all chunks, 
#   then O(N log k) to find the top k. Total: O(N * d + N log k).
#   (Note: Real systems use Approximate Nearest Neighbor (ANN) like HNSW, reducing this to O(d log N).)
# - **Space Complexity**: O(N * d) for storing vectors. O(N * L) for storing chunk text 
#   (where L is average chunk length).
# 
# ## E. Real-world Application
# Enterprise Knowledge Bases, Customer Support Chatbots, AI coding assistants 
# (where codebases are chunked and queried), and personalized AI tutors.
# =============================================================================
"""

import math
import re
from typing import List, Dict, Any, Tuple, Optional
from dataclasses import dataclass

# =============================================================================
# 1. DATA STRUCTURES
# =============================================================================

@dataclass
class DocumentChunk:
    """
    Represents a chunk of text with its corresponding metadata and vector embedding.
    """
    chunk_id: str
    text: str
    metadata: Dict[str, Any]
    embedding: Optional[List[float]] = None


# =============================================================================
# 2. MOCK EMBEDDING MODEL
# =============================================================================

class MockEmbeddingModel:
    """
    A simulated Embedding Model.
    Real LLM architectures use Transformer-based models (like OpenAI text-embedding-ada-002, 
    or BERT-based models) to produce dense vectors mapping semantic meaning.
    
    Here, we simulate a simple deterministic "bag-of-words" style embedding or a hash-based 
    embedding to generate a vector of fixed dimension `d`.
    """
    
    def __init__(self, dimension: int = 128):
        self.dimension = dimension
        
        # A pseudo-random projection matrix to make embeddings deterministic but distributed
        # seeded for reproducibility.
        import random
        rng = random.Random(42)
        self.projection_matrix = [[rng.uniform(-1.0, 1.0) for _ in range(self.dimension)] 
                                  for _ in range(256)] # support 256 ASCII chars roughly

    def generate_embedding(self, text: str) -> List[float]:
        """
        Generates a deterministic vector of size `self.dimension` based on the text.
        Time Complexity: O(L * d) where L is len(text) and d is dimension.
        """
        vector = [0.0] * self.dimension
        
        # Simple algorithm: average the pseudo-random vectors of the characters
        # Weighted slightly by position to differentiate anagrams
        text = text.lower()
        if not text:
            return vector
            
        for i, char in enumerate(text):
            char_idx = ord(char) % 256
            proj = self.projection_matrix[char_idx]
            weight = 1.0 + (i / len(text))
            
            for d in range(self.dimension):
                vector[d] += proj[d] * weight
                
        # Normalize the vector (L2 norm)
        return self._normalize(vector)
        
    def _normalize(self, vector: List[float]) -> List[float]:
        """
        Normalizes a vector to unit length (L2 norm = 1).
        This makes Cosine Similarity mathematically equivalent to Dot Product.
        """
        magnitude = math.sqrt(sum(v * v for v in vector))
        if magnitude == 0:
            return vector
        return [v / magnitude for v in vector]


# =============================================================================
# 3. MATH & SIMILARITY METRICS
# =============================================================================

def cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
    """
    Computes the cosine similarity between two vectors.
    
    Formula: (A dot B) / (||A|| * ||B||)
    
    Time Complexity: O(d) where d is the number of dimensions.
    Space Complexity: O(1)
    """
    if len(vec_a) != len(vec_b):
        raise ValueError("Vectors must have the same dimensionality.")
        
    dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
    
    norm_a = math.sqrt(sum(a * a for a in vec_a))
    norm_b = math.sqrt(sum(b * b for b in vec_b))
    
    if norm_a == 0 or norm_b == 0:
        return 0.0
        
    return dot_product / (norm_a * norm_b)


# =============================================================================
# 4. CHUNKING STRATEGIES
# =============================================================================

class TextChunker:
    """
    Splits long documents into smaller chunks for the Vector Store.
    Chunking is critical: 
    - Too small: Loses context.
    - Too large: Dilutes semantic meaning (embedding becomes muddy) and hits LLM context limits.
    """
    
    @staticmethod
    def sliding_window_chunking(text: str, chunk_size: int, overlap: int) -> List[str]:
        """
        Splits text into chunks of `chunk_size` characters with `overlap` characters.
        
        Time Complexity: O(N) where N is the length of the text.
        Space Complexity: O(N) to store the chunks.
        """
        if chunk_size <= 0:
            raise ValueError("Chunk size must be positive.")
        if overlap >= chunk_size:
            raise ValueError("Overlap must be less than chunk size.")
            
        chunks = []
        start = 0
        text_length = len(text)
        
        while start < text_length:
            end = min(start + chunk_size, text_length)
            
            # Try to break at a space if we are not at the end of the text
            if end < text_length:
                # Look backwards for a space to avoid breaking words in half
                space_idx = text.rfind(' ', start, end)
                if space_idx != -1 and space_idx > start + chunk_size // 2:
                    end = space_idx + 1 # Include the space
            
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
                
            start = end - overlap
            # Ensure we make progress if overlap logic gets stuck
            if start <= end - chunk_size:
                 start = end
                 
        return chunks


# =============================================================================
# 5. VECTOR DATABASE SIMULATION
# =============================================================================

class SimpleVectorStore:
    """
    A naive, in-memory Vector Database.
    Real-world examples: Pinecone, Weaviate, Milvus, pgvector.
    """
    
    def __init__(self):
        self.documents: Dict[str, DocumentChunk] = {}
        
    def add_documents(self, chunks: List[DocumentChunk]) -> None:
        """
        Indexes a batch of document chunks.
        """
        for chunk in chunks:
            if chunk.embedding is None:
                raise ValueError(f"Chunk {chunk.chunk_id} is missing an embedding.")
            self.documents[chunk.chunk_id] = chunk
            
    def similarity_search(self, query_embedding: List[float], top_k: int = 3) -> List[Tuple[float, DocumentChunk]]:
        """
        Performs a brute-force k-Nearest Neighbors (k-NN) search.
        
        Time Complexity: O(N * d + N log K) where N = number of docs, d = dimension.
        Space Complexity: O(K) for maintaining the top K results.
        """
        results = []
        for chunk in self.documents.values():
            sim_score = cosine_similarity(query_embedding, chunk.embedding)
            results.append((sim_score, chunk))
            
        # Sort by similarity score in descending order
        results.sort(key=lambda x: x[0], reverse=True)
        return results[:top_k]


# =============================================================================
# 6. MOCK LLM GENERATION
# =============================================================================

class MockLLM:
    """
    Simulates a Large Language Model API (like OpenAI GPT-4, Anthropic Claude).
    Instead of actual generation, we use simple keyword matching and string formatting
    to demonstrate how the augmented prompt is constructed and 'processed'.
    """
    
    def generate_response(self, prompt: str) -> str:
        """
        Simulates the model generating a response based ONLY on the provided prompt context.
        """
        print("\n--- [DEBUG: LLM Prompt Received] ---")
        print(prompt[:500] + "...\n(prompt truncated)" if len(prompt) > 500 else prompt)
        print("------------------------------------\n")
        
        # Very crude simulation of reasoning based on context
        lower_prompt = prompt.lower()
        
        # Extract the context part (assuming the prompt follows a specific format)
        context_start = lower_prompt.find("context:")
        query_start = lower_prompt.find("query:")
        
        if context_start != -1 and query_start != -1:
            context = lower_prompt[context_start:query_start]
            query = lower_prompt[query_start:]
            
            # Simple keyword extraction from query
            query_words = set(re.findall(r'\\b\\w+\\b', query))
            important_words = query_words - {"what", "is", "the", "how", "why", "a", "an", "query", "answer"}
            
            # Check if important words are in context
            found_info = False
            for word in important_words:
                if word in context:
                    found_info = True
                    break
                    
            if found_info:
                return f"[MockLLM Synthesis]: Based on the provided context, I can answer your query about {', '.join(important_words)}. The context provides relevant details to address this."
            else:
                return "[MockLLM Synthesis]: I'm sorry, but the provided context does not contain sufficient information to answer your query. I cannot hallucinate an answer outside the given context."
                
        return "[MockLLM Synthesis]: Invalid prompt format."


# =============================================================================
# 7. THE RAG PIPELINE (ORCHESTRATOR)
# =============================================================================

class RAGPipeline:
    """
    Orchestrates the entire Retrieval-Augmented Generation process.
    """
    
    def __init__(self, embedding_model: MockEmbeddingModel, vector_store: SimpleVectorStore, llm: MockLLM):
        self.embedding_model = embedding_model
        self.vector_store = vector_store
        self.llm = llm
        
    def ingest_document(self, source_id: str, raw_text: str, chunk_size: int = 150, overlap: int = 30) -> None:
        """
        Step 1 & 2: Chunking and Embedding Document
        """
        print(f"Ingesting document '{source_id}'...")
        chunks_text = TextChunker.sliding_window_chunking(raw_text, chunk_size, overlap)
        
        doc_chunks = []
        for i, text in enumerate(chunks_text):
            chunk_id = f"{source_id}_chunk_{i}"
            # Generate embedding
            embedding = self.embedding_model.generate_embedding(text)
            
            doc_chunk = DocumentChunk(
                chunk_id=chunk_id,
                text=text,
                metadata={"source": source_id, "chunk_index": i},
                embedding=embedding
            )
            doc_chunks.append(doc_chunk)
            
        # Step 3: Store in Vector DB
        self.vector_store.add_documents(doc_chunks)
        print(f"Successfully ingested {len(doc_chunks)} chunks into the Vector Store.")
        
    def query(self, user_query: str, top_k: int = 3) -> str:
        """
        Step 4, 5 & 6: Query Embedding, Retrieval, and Augmented Generation.
        """
        print(f"\\nProcessing Query: '{user_query}'")
        
        # Step 4: Embed the user query
        query_embedding = self.embedding_model.generate_embedding(user_query)
        
        # Step 5: Retrieval
        # Perform similarity search
        retrieved_results = self.vector_store.similarity_search(query_embedding, top_k)
        
        print(f"Retrieved Top-{top_k} Chunks:")
        for score, chunk in retrieved_results:
            print(f"  - [{score:.4f}] {chunk.chunk_id}: {chunk.text[:50]}...")
            
        # Compile the retrieved text into a context block
        context_block = "\\n\\n".join([f"--- Chunk {chunk.chunk_id} ---\\n{chunk.text}" for _, chunk in retrieved_results])
        
        # Step 6: Generation (Prompt Construction)
        # We construct a prompt that forces the LLM to ground its answer in the context.
        augmented_prompt = f\"\"\"You are a helpful and precise assistant. 
Please answer the user's query based ONLY on the following context. 
If the context does not contain the answer, say "I do not know based on the provided context." Do not guess.

CONTEXT:
{context_block}

QUERY:
{user_query}

ANSWER:\"\"\"

        # Pass to LLM
        final_answer = self.llm.generate_response(augmented_prompt)
        return final_answer


# =============================================================================
# 8. TESTS AND DEMONSTRATION
# =============================================================================

def run_rag_demo():
    """
    End-to-End demonstration of the RAG pipeline.
    """
    print("="*60)
    print(" RAG (Retrieval-Augmented Generation) PIPELINE DEMO")
    print("="*60)
    
    # 1. Initialize Components
    embedding_model = MockEmbeddingModel(dimension=64)
    vector_store = SimpleVectorStore()
    llm = MockLLM()
    
    rag = RAGPipeline(embedding_model, vector_store, llm)
    
    # 2. Raw Documents (Our Knowledge Base)
    doc1 = \"\"\"
    Python is a high-level, interpreted programming language known for its clear syntax and readability. 
    It was created by Guido van Rossum and first released in 1991. Python supports multiple programming paradigms, 
    including procedural, object-oriented, and functional programming.
    \"\"\"
    
    doc2 = \"\"\"
    Retrieval-Augmented Generation (RAG) is an AI framework for improving the quality of LLM-generated responses 
    by grounding the model on external sources of knowledge to supplement the LLM's internal representation of information. 
    RAG has two phases: retrieval and content generation.
    \"\"\"
    
    doc3 = \"\"\"
    The quick brown fox jumps over the lazy dog. This is a pangram, meaning it contains every letter of the 
    English alphabet at least once. It is often used for font testing and typing practice.
    \"\"\"
    
    # 3. Ingestion
    rag.ingest_document("doc_python", doc1, chunk_size=100, overlap=20)
    rag.ingest_document("doc_rag", doc2, chunk_size=100, overlap=20)
    rag.ingest_document("doc_fox", doc3, chunk_size=100, overlap=20)
    
    # 4. Queries
    queries = [
        "Who created the Python programming language?",
        "What are the two phases of RAG?",
        "What is the capital of France?" # This should fail gracefully (hallucination prevention)
    ]
    
    for q in queries:
        answer = rag.query(q, top_k=2)
        print(f"FINAL ANSWER: {answer}")
        print("-" * 40)


def run_tests():
    """
    Unit tests for core mathematical and algorithmic functions.
    """
    print("\\nRunning Unit Tests...")
    
    # Test Cosine Similarity
    v1 = [1.0, 0.0, 0.0]
    v2 = [1.0, 0.0, 0.0]
    assert math.isclose(cosine_similarity(v1, v2), 1.0), "Identical vectors should have similarity 1.0"
    
    v3 = [0.0, 1.0, 0.0]
    assert math.isclose(cosine_similarity(v1, v3), 0.0), "Orthogonal vectors should have similarity 0.0"
    
    v4 = [1.0, 1.0, 0.0]
    # Cosine of 45 degrees is ~0.707
    assert math.isclose(cosine_similarity(v1, v4), 0.7071067811865475), "Similarity calculation incorrect"
    
    # Test Chunking
    text = "A B C D E F G H I J"
    chunks = TextChunker.sliding_window_chunking(text, chunk_size=5, overlap=2)
    # Expected chunks roughly dependent on space logic
    assert len(chunks) > 0, "Chunker failed to produce chunks"
    
    print("All unit tests passed successfully!")

if __name__ == "__main__":
    run_tests()
    run_rag_demo()
