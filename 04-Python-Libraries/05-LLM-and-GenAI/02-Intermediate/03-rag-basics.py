"""
# ==============================================================================
# LABORATORY: RETRIEVAL-AUGMENTED GENERATION (RAG)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# LLMs have two massive flaws:
# 1. Hallucination: If they don't know the answer, they confidently lie.
# 2. Knowledge Cutoff: An LLM trained in 2021 has absolutely zero knowledge of 
#    events that happened in 2023. It also cannot read your company's private, 
#    internal PDF documents.
#
# We solve this using RAG (Retrieval-Augmented Generation).
# Instead of asking the LLM to rely on its internal memory, we:
# 1. Take your private PDF, chop it into 100-word chunks, and convert those 
#    chunks into mathematical Vectors (Embeddings).
# 2. Save the Vectors into a Vector Database.
# 3. When a user asks a question, we convert the question into a Vector.
# 4. We calculate Cosine Similarity to mathematically find the 3 most relevant 
#    PDF chunks from the database.
# 5. We inject those 3 exact paragraphs into the LLM's Prompt and say: 
#    "Answer the user based STRICTLY on the following paragraphs."
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand Document Loaders and Text Splitters (Chunking).
# - Understand Vector Embeddings (Sentence-Transformers).
# - Construct a Vector Database query to retrieve relevant context.
#
# ==============================================================================
"""

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# In a real environment: pip install langchain chromadb sentence-transformers
try:
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    from langchain.docstore.document import Document
    # We use HuggingFace embeddings to keep this open-source and free!
    from langchain_community.embeddings import HuggingFaceEmbeddings
    from langchain_community.vectorstores import Chroma
    HAS_RAG_LIBS = True
except ImportError:
    HAS_RAG_LIBS = False

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. TEXT SPLITTERS (CHUNKING THE DATA)
# ==============================================================================
def demonstrate_chunking():
    section_header("Text Splitting (Chunking the PDF)")
    
    if not HAS_RAG_LIBS:
        print("[WARNING] LangChain/Chroma not installed.")
        return
        
    print("You cannot feed a 1,000-page PDF into an LLM. It violates the Context ")
    print("Limit. You must systematically chop the PDF into overlapping chunks.\n")
    
    # 1. SIMULATE LOADING A DOCUMENT
    raw_text = (
        "Project Titan is a highly classified initiative started in 2024. "
        "Its primary goal is to develop sustainable fusion energy using "
        "laser containment fields. The CEO of Project Titan is Dr. Aris Thorne, "
        "who previously worked at CERN. The project has a budget of 5 Billion dollars."
    )
    
    # 2. THE RECURSIVE CHARACTER TEXT SPLITTER
    # This is the industry standard. It tries to split by paragraphs (\n\n), 
    # then by sentences, then by words, to ensure it doesn't accidentally chop 
    # a sentence directly in half!
    
    # chunk_size: Max characters per chunk.
    # chunk_overlap: Crucial! If a concept spans across two chunks, overlapping 
    # ensures the context is not destroyed at the seam.
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=100, 
        chunk_overlap=20
    )
    
    # 3. EXECUTE THE SPLIT
    chunks = splitter.create_documents([raw_text])
    
    print(f"Original Text Length: {len(raw_text)} characters.")
    print(f"Split into {len(chunks)} Chunks!\n")
    
    for i, chunk in enumerate(chunks):
        print(f"--- Chunk {i+1} ---")
        print(chunk.page_content)


# ==============================================================================
# 4. VECTOR EMBEDDINGS & CHROMADB
# ==============================================================================
def demonstrate_vector_db():
    section_header("Vector Embeddings and ChromaDB")
    
    if not HAS_RAG_LIBS: return
    
    print("We must convert English text into Mathematical Vectors (Embeddings) ")
    print("so we can calculate geometric 'Distance' between concepts.\n")
    
    try:
        # 1. LOAD THE EMBEDDING ENGINE
        # This downloads a tiny, ultra-fast model explicitly trained to turn 
        # sentences into 384-Dimensional vectors.
        print("Loading HuggingFace Embedding Model...")
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        
        # We have 3 chunks of knowledge.
        docs = [
            Document(page_content="Project Titan aims to develop fusion energy."),
            Document(page_content="Dr. Aris Thorne is the CEO of Project Titan."),
            Document(page_content="The budget for the project is 5 Billion dollars.")
        ]
        
        # 2. CREATE THE VECTOR DATABASE (Chroma)
        # Chroma takes the texts, passes them through the Embedding Engine, 
        # calculates the 384D vectors, and stores them in RAM!
        print("Embedding the documents and spinning up ChromaDB...")
        vector_db = Chroma.from_documents(docs, embeddings)
        
        # 3. THE USER QUERY
        query = "Who is the leader of the energy project?"
        print(f"\nUser Query: '{query}'")
        
        # 4. RETRIEVAL (The 'R' in RAG)
        # Chroma embeds the User Query, calculates Cosine Similarity against all 
        # chunks in the database, and returns the top K most mathematically similar chunks!
        print("\nExecuting Vector Search (Cosine Similarity)...")
        results = vector_db.similarity_search(query, k=1)
        
        print(f"Top Matched Document: '{results[0].page_content}'")
        print("\nNow you inject this exact sentence into the LLM's prompt so ")
        print("it can answer the user's question with 100% factual accuracy!")
        
    except Exception as e:
        print(f"Execution skipped: {e}")


def run_all_labs():
    demonstrate_chunking()
    demonstrate_vector_db()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why is `chunk_overlap` mathematically critical when splitting large PDFs?
   Answer: Imagine a PDF contains the sentence: "The CEO of the company is \n\n John Smith." If you set chunk size to 50 and overlap to 0, the text splitter might violently slice the document exactly at the newline. Chunk 1 contains "The CEO of the company is". Chunk 2 contains "John Smith". If a user asks "Who is the CEO?", neither chunk contains the full answer! Chunk 1 has the context but no name. Chunk 2 has a name but no context. By setting an overlap of 20 characters, Chunk 2 will safely copy the end of Chunk 1: "company is John Smith", preserving the semantic linkage across the seam and ensuring the Vector DB can find the correct answer.

2. What exactly is a "Vector Embedding" and how does it enable search?
   Answer: An Embedding model (like `all-MiniLM-L6-v2` or `text-embedding-ada-002`) reads a sentence and outputs an array of floats (e.g., a 384-dimensional vector). During training, these models learn to place semantically similar concepts geometrically close to each other in this 384D space. The words "King" and "Queen" will have vectors that point in almost the exact same direction. Therefore, you do not need keyword matching. If the database contains the chunk "The feline rested on the rug", and the user searches "Did the cat sit on the mat?", the geometric Cosine Similarity between those two vectors will be $0.95+$, allowing you to instantly retrieve the document despite zero overlapping keywords!

3. How does RAG completely eliminate LLM Hallucinations on private data?
   Answer: Without RAG, an LLM relies on parametric memory (the weights it learned during training). If asked about "Project Titan", it will guess based on sci-fi movies, resulting in a hallucination. In a RAG architecture, you use a highly restrictive Prompt Template: 
   `"You are a strict assistant. Answer the User Query using ONLY the following Context. If the Context does not contain the answer, output 'I do not know'. CONTEXT: {retrieved_chunks} QUERY: {user_query}"`
   By forcing the LLM to ground its prediction strictly on the text provided by the Vector Database, you bypass its parametric memory entirely, enforcing 100% factual adherence to your private documents.
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Retrieval-Augmented Generation (RAG) Completed.")
