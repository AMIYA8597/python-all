\"\"\"
Retrieval-Augmented Generation (RAG) System - Main Module

This script demonstrates a from-scratch, local RAG pipeline using 
in-memory vector storage (FAISS concept) and dummy embeddings/LLMs.
In a production setting, you would replace the dummy components with
LangChain/LlamaIndex, OpenAI/HuggingFace embeddings, and a real Vector DB.

Industry Use Cases:
- Building internal enterprise search engines.
- Domain-specific conversational agents.

Concepts Covered:
- Document Chunking.
- Vector Embeddings & Cosine Similarity.
- Contextual Prompt Generation.
\"\"\"

import math
from typing import List, Dict, Tuple
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Document:
    def __init__(self, content: str, metadata: Dict[str, str] = None):
        self.content = content
        self.metadata = metadata or {}

class MockEmbeddingModel:
    \"\"\"
    A mock embedding model that uses basic bag-of-words for demonstration.
    In reality, you'd use sentence-transformers or OpenAI embeddings here.
    \"\"\"
    def __init__(self):
        self.vocab = set()

    def embed_text(self, text: str) -> List[float]:
        # A highly simplistic and fake embedding logic for demonstration purposes
        # It creates a pseudo-vector based on character frequencies
        vector = [0.0] * 26
        for char in text.lower():
            if 'a' <= char <= 'z':
                vector[ord(char) - ord('a')] += 1.0
                
        # Normalize the vector
        magnitude = math.sqrt(sum(v**2 for v in vector))
        if magnitude > 0:
            vector = [v / magnitude for v in vector]
        return vector

def cosine_similarity(v1: List[float], v2: List[float]) -> float:
    \"\"\"Calculate cosine similarity between two vectors.\"\"\"
    dot_product = sum(a * b for a, b in zip(v1, v2))
    mag1 = math.sqrt(sum(a**2 for a in v1))
    mag2 = math.sqrt(sum(b**2 for b in v2))
    if mag1 == 0 or mag2 == 0:
        return 0.0
    return dot_product / (mag1 * mag2)

class VectorStore:
    \"\"\"
    An in-memory vector store that performs exact nearest neighbor search.
    In production, use FAISS, Pinecone, or ChromaDB.
    \"\"\"
    def __init__(self, embedding_model: MockEmbeddingModel):
        self.embedding_model = embedding_model
        self.store: List[Tuple[List[float], Document]] = []

    def add_documents(self, documents: List[Document]) -> None:
        logger.info(f\"Adding {len(documents)} documents to the vector store.\")
        for doc in documents:
            vector = self.embedding_model.embed_text(doc.content)
            self.store.append((vector, doc))

    def similarity_search(self, query: str, k: int = 2) -> List[Document]:
        logger.info(f\"Performing similarity search for query: '{query}'\")
        query_vector = self.embedding_model.embed_text(query)
        
        # Calculate similarities
        scored_docs = []
        for doc_vector, doc in self.store:
            score = cosine_similarity(query_vector, doc_vector)
            scored_docs.append((score, doc))
            
        # Sort by score descending
        scored_docs.sort(key=lambda x: x[0], reverse=True)
        
        # Return top k documents
        return [doc for score, doc in scored_docs[:k]]

class MockLLM:
    \"\"\"
    A mock Large Language Model that simply templates the context and query.
    \"\"\"
    def generate(self, prompt: str) -> str:
        logger.info(\"LLM generating response based on prompt...\")
        # In a real scenario, this makes an API call to OpenAI, Anthropic, or a local model.
        return f\"[Mock LLM Response]\\nBased on the provided context, I have generated an answer to your query.\\n\\nPrompt received:\\n{prompt}\"

class RAGPipeline:
    \"\"\"
    Orchestrates the Retrieval-Augmented Generation process.
    \"\"\"
    def __init__(self, vector_store: VectorStore, llm: MockLLM):
        self.vector_store = vector_store
        self.llm = llm

    def query(self, user_query: str) -> str:
        # 1. Retrieve relevant documents
        retrieved_docs = self.vector_store.similarity_search(user_query, k=2)
        
        # 2. Format the context
        context_parts = [f\"Document {i+1}:\\n{doc.content}\" for i, doc in enumerate(retrieved_docs)]
        context_str = \"\\n\\n\".join(context_parts)
        
        # 3. Construct the prompt
        prompt = f\"\"\"Use the following pieces of context to answer the user's query. 
If you don't know the answer, just say that you don't know, don't try to make up an answer.

Context:
{context_str}

User Query: {user_query}

Answer:\"\"\"
        
        # 4. Generate response
        response = self.llm.generate(prompt)
        return response

def main():
    # Sample Knowledge Base
    raw_texts = [
        \"The company's Q3 revenue grew by 15% year-over-year, driven by strong cloud sales.\",
        \"Our new remote work policy allows employees to work from home up to 3 days a week.\",
        \"The project 'Alpha' launch has been delayed to Q1 2025 due to supply chain issues.\",
        \"Machine learning models require robust data pipelines to function effectively in production.\"
    ]
    
    docs = [Document(content=text, metadata={\"source\": f\"doc_{i}\"}) for i, text in enumerate(raw_texts)]
    
    # Initialize components
    embedder = MockEmbeddingModel()
    vector_db = VectorStore(embedder)
    vector_db.add_documents(docs)
    
    llm = MockLLM()
    rag = RAGPipeline(vector_db, llm)
    
    # Run a query
    question = \"What is the new remote work policy?\"
    print(f\"\\n--- Question ---\\n{question}\\n\")
    
    answer = rag.query(question)
    print(f\"\\n--- Answer ---\\n{answer}\\n\")

if __name__ == \"__main__\":
    main()
