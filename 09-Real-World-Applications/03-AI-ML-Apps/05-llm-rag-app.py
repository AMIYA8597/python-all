"""
# ==============================================================================
# LABORATORY: REAL-WORLD APPLICATIONS (RAG - RETRIEVAL AUGMENTED GENERATION)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A junior developer builds a corporate chatbot using GPT-4. A user asks the bot, 
# "What is the new remote work policy defined yesterday in HR_Doc_42?" The LLM 
# hallucinates, claiming everyone must work in the office. The developer realizes 
# the LLM's neural weights were frozen in 2023, and it mathematically cannot 
# know about a document written yesterday. They attempt to paste the entire 
# 10,000-page HR manual into the prompt, crashing the Token Limit constraint.
#
# A senior AI engineer understands "Retrieval Augmented Generation" (RAG). They 
# mathematically convert all 10,000 pages of HR manuals into "Vector Embeddings". 
# They store these coordinates in a Vector Database (like Pinecone or Chroma). 
# When a user asks a question, the system mathematically calculates the Cosine 
# Similarity of the question against the database, instantly retrieving only the 
# 3 most relevant paragraphs. It injects those 3 paragraphs into the LLM prompt, 
# mathematically forcing the LLM to read the exact truth before answering.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master the mathematical architecture of Vector Embeddings.
# - Understand Cosine Similarity (Semantic Search).
# - Execute a simulated RAG pipeline (Retrieval -> Injection -> Generation).
#
# ==============================================================================
"""

import math

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. MATHEMATICAL FOUNDATION: VECTOR EMBEDDINGS & COSINE SIMILARITY
# ==============================================================================
# An Embedding mathematically translates a human sentence into an array of floating
# point numbers (a vector in high-dimensional space).
# e.g., "The cat sat" -> [0.12, -0.45, 0.89, ... 1536 dimensions]
#
# Sentences with similar SEMANTIC MEANING will be grouped close together in this space!

def calculate_cosine_similarity(vec_a: list, vec_b: list) -> float:
    """
    Calculates the mathematical angle between two vectors in N-dimensional space.
    1.0 = Exact match. 0.0 = Orthogonal (No relation). -1.0 = Opposite meaning.
    """
    dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
    magnitude_a = math.sqrt(sum(a * a for a in vec_a))
    magnitude_b = math.sqrt(sum(b * b for b in vec_b))
    
    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0
        
    return dot_product / (magnitude_a * magnitude_b)


def simulate_embedding_model(text: str) -> list:
    """
    Simulates a heavy API call to `text-embedding-ada-002`.
    We will use a hardcoded 3-dimensional mathematical simulation for the lab.
    Dimension 1: Focuses on 'Animals'
    Dimension 2: Focuses on 'Finance'
    Dimension 3: Focuses on 'Technology'
    """
    text = text.lower()
    
    # We construct a simulated 3D vector based on keywords!
    animal_score = 0.0
    finance_score = 0.0
    tech_score = 0.0
    
    if "dog" in text or "cat" in text or "pet" in text:
        animal_score = 0.9
    if "money" in text or "bank" in text or "interest" in text:
        finance_score = 0.9
    if "server" in text or "computer" in text or "python" in text:
        tech_score = 0.9
        
    return [animal_score, finance_score, tech_score]


# ==============================================================================
# 4. THE RAG PIPELINE
# ==============================================================================
def demonstrate_rag_architecture():
    section_header("Retrieval Augmented Generation (RAG) Architecture")
    
    print("  [PHASE 1: THE KNOWLEDGE BASE (Document Chunking)]")
    # A massive corporation has thousands of documents. We split them into "Chunks".
    corporate_documents = [
        {"id": "doc_1", "text": "Our corporate servers must run Python 3.10 and utilize 16GB of RAM."},
        {"id": "doc_2", "text": "Employees are allowed to bring their pet dog or cat to the office on Fridays."},
        {"id": "doc_3", "text": "The corporate bank account earns 4% interest per year on deposited money."},
        {"id": "doc_4", "text": "The primary database server requires 500GB of SSD storage for Python apps."}
    ]
    
    print("    -> Simulating Embedding Generation for all corporate documents...")
    # We mathematically convert the text into Vectors! (This is stored in a Vector DB)
    vector_database = []
    for doc in corporate_documents:
        vector = simulate_embedding_model(doc["text"])
        vector_database.append({
            "id": doc["id"],
            "text": doc["text"],
            "vector": vector
        })
        print(f"       {doc['id']} Vector: {vector}")


    print("\n  [PHASE 2: THE USER QUERY]")
    # A user asks a question to the Chatbot!
    user_query = "What are the hardware requirements for our tech stack?"
    print(f"    -> User Query: \"{user_query}\"")
    
    # We MUST mathematically embed the user's question into the exact same N-dimensional space!
    query_vector = simulate_embedding_model(user_query)
    print(f"    -> Query Vector: {query_vector}")


    print("\n  [PHASE 3: SEMANTIC SEARCH (Cosine Similarity)]")
    # We scan the Vector Database and mathematically compare the Query Vector against
    # EVERY single Document Vector using Cosine Similarity!
    
    search_results = []
    for doc in vector_database:
        similarity = calculate_cosine_similarity(query_vector, doc["vector"])
        search_results.append((similarity, doc))
        
    # We sort by the highest mathematical match!
    search_results.sort(key=lambda x: x[0], reverse=True)
    
    # We extract the Top 2 most relevant paragraphs!
    top_k = 2
    retrieved_context = ""
    for i in range(top_k):
        score, doc = search_results[i]
        print(f"    -> Match #{i+1} (Score: {score:.2f}) | {doc['id']}: {doc['text']}")
        retrieved_context += f"- {doc['text']}\n"


    print("\n  [PHASE 4: THE AUGMENTED GENERATION]")
    # We architect the final Prompt payload for the LLM!
    # We inject the mathematically retrieved context directly into the prompt,
    # forcing the LLM to read the exact truth before generating an answer.
    
    final_prompt = f"""
System: You are a helpful corporate AI. Use the provided Context to answer the User Query. If the answer is not in the Context, say "I don't know".

Context:
{retrieved_context}

User Query: {user_query}
"""
    
    print("    -> [THE FINAL PROMPT PAYLOAD TRANSMITTED TO LLM]")
    print(final_prompt)
    print("    -> [LLM OUTPUT]")
    print("       Based on the corporate guidelines, our servers must run Python 3.10 with 16GB of RAM, and the primary database server requires 500GB of SSD storage.")


def run_all_labs():
    demonstrate_rag_architecture()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "Why can't we just paste our entire 10,000-page corporate manual into the LLM prompt instead of building a complex Vector Database?"
   Senior Answer: "Context Window limitations and compute costs. Every LLM has a strict physical limit on how many 'Tokens' it can process in a single mathematical pass (e.g., GPT-4 handles $128,000$ tokens, roughly $300$ pages). If you attempt to inject $10,000$ pages, the API will mathematically reject the payload. Furthermore, the Attention Mechanism (the core math of Transformers) scales quadratically ($O(N^2)$). If you double the size of the prompt, the GPU compute cost quadruples. Injecting a massive document for every single user question is catastrophically expensive and slow. RAG solves this by executing a cheap mathematical search ($O(N)$) on a local Vector DB to isolate the $3$ relevant paragraphs, injecting only those $3$ paragraphs into the LLM, reducing latency from $30$ seconds to $2$ seconds and cutting API costs by $99\\%$."

2. Interviewer: "What is the mathematical difference between Keyword Search (Elasticsearch) and Semantic Search (Cosine Similarity on Vector Embeddings)?"
   Senior Answer: "Keyword search operates on exact lexical matches (BM25 algorithms). If a user queries 'Puppy', and the document contains the word 'Dog', a Keyword Search mathematically returns zero results because the strings do not match perfectly. Semantic Search relies on neural Embeddings. An embedding model (like `text-embedding-3`) mathematically maps words based on their underlying semantic context. In the high-dimensional Vector Space, the vector for 'Puppy' and the vector for 'Dog' are physically located right next to each other. When we calculate the Cosine Similarity (the angle between the vectors), it returns a $0.95$ match. Semantic Search retrieves the *meaning* of the question, not the raw characters."

3. Interviewer: "What is the 'Lost in the Middle' phenomenon in LLMs, and how does it impact RAG architectural design?"
   Senior Answer: "Research has proven that if you inject 50 retrieved documents into an LLM's context window, its Attention Mechanism degrades. It perfectly remembers the documents placed at the very beginning of the prompt, and the documents placed at the very end. However, it catastrophically forgets or ignores the documents buried in the 'Middle' of the massive text block. Therefore, a Senior RAG architect must carefully limit 'Top-K' retrieval. Instead of retrieving 20 documents, they aggressively filter it down to the absolute best 3-5 documents to guarantee the LLM mathematically pays attention to all of the injected context."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: AI & ML (RAG Architecture) Completed.")
