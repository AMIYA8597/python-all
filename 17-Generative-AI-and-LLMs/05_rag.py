"""
## A. Concept Name
Retrieval-Augmented Generation (RAG)

## B. Motivation
Large Language Models (LLMs) have limited knowledge bounded by their training data cut-off and lack access to private or recent information. RAG solves this by retrieving relevant data from an external knowledge base to augment the LLM's prompt, reducing hallucinations and providing accurate, context-specific answers.

## C. How it Works
1. Indexing: Text is split into chunks, embedded into vectors, and stored in a vector database.
2. Retrieval: The user's query is embedded, and the vector database is searched for the most similar chunks (context).
3. Generation: The retrieved context is combined with the original query to form an augmented prompt, which is then fed to the LLM to generate an answer.

## D. Code Example
This module provides a simplified, end-to-end RAG pipeline using mock components (MockEmbeddingModel, MockVectorDB, MockLLM) to illustrate the core mechanics of indexing, retrieval, and generation.

## X. Project Connection
This concept is foundational for building AI assistants, domain-specific chatbots, and document Q&A systems within a larger project architecture.
"""

# A simplified implementation of a Retrieval-Augmented Generation pipeline.

class MockEmbeddingModel:
    """Mock embedder that returns dummy floats based on text length for simplicity."""
    def embed(self, text):
        # Dummy logic: returning a 2D vector based on string length and ascii sum
        val1 = len(text) / 100.0
        val2 = sum(ord(c) for c in text) / 10000.0
        return [val1, val2]

class MockVectorDB:
    """In-memory Vector Database."""
    def __init__(self):
        self.data = []
        
    def add(self, chunk_text, vector):
        self.data.append({"text": chunk_text, "vector": vector})
        
    def search(self, query_vector, top_k=1):
        # Calculate a mock distance (Euclidean-like)
        results = []
        for item in self.data:
            vec = item["vector"]
            distance = ((query_vector[0] - vec[0])**2 + (query_vector[1] - vec[1])**2)**0.5
            results.append((item["text"], distance))
            
        # Sort by shortest distance
        results.sort(key=lambda x: x[1])
        return results[:top_k]

class MockLLM:
    """Simulates an LLM answering based on context."""
    def generate(self, prompt):
        # A simple rule-based generation to simulate LLM comprehension
        prompt_lower = prompt.lower()
        if "policy" in prompt_lower and "remote work" in prompt_lower:
            if "tuesday and thursday" in prompt_lower:
                return "According to the context, employees are allowed to work remotely on Tuesdays and Thursdays."
        if "capital" in prompt_lower and "france" in prompt_lower:
            if "paris" in prompt_lower:
                return "The context states that Paris is the capital of France."
        
        return "I am sorry, but the provided context does not contain the answer to your question."

def main():
    print("--- End-to-End RAG Pipeline Simulation ---")
    
    # 1. Indexing Phase (Data Preparation)
    print("\n[Phase 1: Indexing]")
    knowledge_base = [
        "The capital of France is Paris. It is known for the Eiffel Tower.",
        "Company remote work policy: Employees may work from home on Tuesday and Thursday.",
        "Python is a high-level programming language created by Guido van Rossum."
    ]
    
    embedder = MockEmbeddingModel()
    vector_db = MockVectorDB()
    
    for doc in knowledge_base:
        vector = embedder.embed(doc)
        vector_db.add(doc, vector)
        print(f"Indexed document: '{doc[:30]}...'")

    # 2. Retrieval & Generation Phase (Runtime)
    print("\n[Phase 2: Querying & RAG]")
    llm = MockLLM()
    
    user_questions = [
        "What is the company policy on remote work?",
        "Who is the CEO of the company?" # Testing failure case
    ]
    
    for question in user_questions:
        print(f"\nUser Question: {question}")
        
        # Step A: Embed the query
        query_vector = embedder.embed(question)
        
        # Step B: Retrieve relevant context
        retrieved_results = vector_db.search(query_vector, top_k=1)
        context_text = retrieved_results[0][0] if retrieved_results else ""
        print(f"Retrieved Context: {context_text}")
        
        # Step C: Augment Prompt
        augmented_prompt = f"""Use the following context to answer the question. 
Context: {context_text}
Question: {question}
Answer:"""
        
        # Step D: LLM Generation
        answer = llm.generate(augmented_prompt)
        print(f"LLM Answer: {answer}")

if __name__ == "__main__":
    main()
