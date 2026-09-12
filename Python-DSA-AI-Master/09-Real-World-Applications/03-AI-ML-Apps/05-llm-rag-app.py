# 05-llm-rag-app.py
"""
Retrieval-Augmented Generation (RAG) Simulation

This script simulates a RAG pipeline. True RAG uses vector embeddings and an LLM,
but the core concept is:
1. Retrieve relevant documents based on a query.
2. Augment the prompt with the retrieved documents.
3. Generate an answer (simulated here).

Topics Covered:
1. Document chunking and storage.
2. Basic retrieval mechanism (TF-IDF/keyword overlap simulation).
3. Prompt construction.
"""

# Dummy Knowledge Base
KNOWLEDGE_BASE = [
    "Python was created by Guido van Rossum and first released in 1991.",
    "FastAPI is a modern, fast web framework for building APIs with Python.",
    "RAG stands for Retrieval-Augmented Generation.",
    "Machine learning models require large amounts of high-quality data."
]

def retrieve(query):
    """Retrieves the most relevant document based on keyword overlap."""
    query_words = set(query.lower().split())
    best_doc = None
    max_overlap = -1
    
    for doc in KNOWLEDGE_BASE:
        doc_words = set(doc.lower().split())
        overlap = len(query_words.intersection(doc_words))
        if overlap > max_overlap:
            max_overlap = overlap
            best_doc = doc
            
    return best_doc if max_overlap > 0 else "No relevant context found."

def simulate_llm(prompt):
    """Simulates an LLM generating a response based on the prompt."""
    # In a real app, you would pass this prompt to OpenAI, Anthropic, etc.
    return f"[Simulated LLM Output based on context]: I found the answer in the context provided."

def run_rag_pipeline(query):
    """Executes the RAG pipeline."""
    print(f"User Query: {query}")
    
    # 1. Retrieval
    context = retrieve(query)
    print(f"Retrieved Context: {context}")
    
    # 2. Augment Prompt
    prompt = f"Answer the user's question using ONLY the following context.\nContext: {context}\nQuestion: {query}"
    
    # 3. Generate
    response = simulate_llm(prompt)
    print(f"Final Answer: {response}\n")

if __name__ == "__main__":
    queries = [
        "Who created Python?",
        "What does RAG stand for?",
        "How do you bake a cake?" # Should find no context
    ]
    
    for q in queries:
        run_rag_pipeline(q)
