"""
# ==============================================================================
# LABORATORY: PROJECT-BASED LEARNING (RAG SYSTEM ARCHITECTURE)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A junior developer wants an LLM to answer questions about their company's 
# proprietary 2024 Financial Report. They ask the LLM directly. The LLM 
# hallucinates a fake answer because it was trained in 2022 and mathematically 
# cannot know about the 2024 report.
#
# A senior AI engineer builds a Retrieval-Augmented Generation (RAG) system. 
# They mathematically shatter the 2024 Report into text chunks, convert them 
# into High-Dimensional Vectors (Embeddings), and store them in a Vector Database. 
# When a user asks a question, the system converts the question into a Vector, 
# executes a mathematical Cosine Similarity search to extract the exact relevant 
# paragraphs from the database, and injects them into the LLM's prompt. The LLM 
# now answers flawlessly with 100% mathematical accuracy.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master High-Dimensional Vector Embeddings architecture.
# - Execute Cosine Similarity calculations to retrieve semantic data.
# - Architect a pure RAG Prompt Pipeline.
#
# ==============================================================================
"""

import math
from typing import List, Dict, Tuple

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE MATHEMATICS ENGINE (COSINE SIMILARITY)
# ==============================================================================
class VectorMath:
    """
    In a real system, you use NumPy for this. 
    We build it from scratch to mathematically prove how it works!
    """
    @staticmethod
    def dot_product(vec_a: List[float], vec_b: List[float]) -> float:
        """Mathematically multiplies corresponding dimensions and sums them."""
        return sum(a * b for a, b in zip(vec_a, vec_b))

    @staticmethod
    def magnitude(vec: List[float]) -> float:
        """Mathematically calculates the absolute length of the vector in N-dimensional space."""
        return math.sqrt(sum(val ** 2 for val in vec))

    @staticmethod
    def cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
        """
        Calculates the exact angle between two vectors.
        1.0 = Mathematically Identical direction (Semantic Match)
        0.0 = Mathematically Orthogonal (No relation)
        -1.0 = Mathematically Opposite (Antonyms)
        """
        mag_a = VectorMath.magnitude(vec_a)
        mag_b = VectorMath.magnitude(vec_b)
        
        if mag_a == 0 or mag_b == 0:
            return 0.0
            
        return VectorMath.dot_product(vec_a, vec_b) / (mag_a * mag_b)


# ==============================================================================
# 4. THE RAG ARCHITECTURE (THE VECTOR DATABASE)
# ==============================================================================
class DummyEmbeddingModel:
    """
    A simulated Embedding Model.
    In Production, you would use OpenAI's `text-embedding-3-small` or HuggingFace.
    This dummy model assigns synthetic 3-dimensional vectors for demonstration.
    """
    @staticmethod
    def embed_text(text: str) -> List[float]:
        text = text.lower()
        # [Finance_Score, Tech_Score, HR_Score]
        if "revenue" in text or "profit" in text or "margin" in text:
            return [0.9, 0.1, 0.0]
        elif "server" in text or "cloud" in text or "latency" in text:
            return [0.1, 0.9, 0.0]
        elif "hiring" in text or "employee" in text or "benefits" in text:
            return [0.0, 0.1, 0.9]
        else:
            return [0.3, 0.3, 0.3] # Generic Vector


class VectorDatabase:
    """A pure Python In-Memory Vector Store."""
    def __init__(self):
        # We store tuples of (Raw Text, Vector Array)
        self.knowledge_base: List[Tuple[str, List[float]]] = []

    def ingest_document(self, text_chunk: str):
        """Mathematically embeds the text and saves it to the DB."""
        vector = DummyEmbeddingModel.embed_text(text_chunk)
        self.knowledge_base.append((text_chunk, vector))
        
    def semantic_search(self, query: str, top_k: int = 1) -> List[Tuple[str, float]]:
        """
        Executes a K-Nearest Neighbors (KNN) Cosine Similarity scan across 
        the entire database to find the mathematically closest matches.
        """
        query_vector = DummyEmbeddingModel.embed_text(query)
        results = []
        
        for doc_text, doc_vector in self.knowledge_base:
            similarity = VectorMath.cosine_similarity(query_vector, doc_vector)
            results.append((doc_text, similarity))
            
        # Mathematically sort by Similarity Score in Descending Order!
        results.sort(key=lambda x: x[1], reverse=True)
        
        return results[:top_k]


# ==============================================================================
# 5. THE RAG PIPELINE (THE SIMULATOR)
# ==============================================================================
class RAGPipeline:
    def __init__(self):
        self.db = VectorDatabase()

    def build_knowledge_base(self):
        """Populates the Vector Database with proprietary company data."""
        documents = [
            "Q3 2024 Financial Report: Gross revenue hit $4.2 Billion, driven by a 15% increase in cloud subscriptions. Profit margins expanded to 32%.",
            "Infrastructure Update: We migrated 5,000 legacy servers to AWS, reducing global latency by 45 milliseconds.",
            "HR Update: Employee benefits for 2025 will include a new 401k match program and extended parental leave."
        ]
        
        for doc in documents:
            self.db.ingest_document(doc)

    def execute_rag_query(self, user_question: str):
        """The absolute core of Retrieval-Augmented Generation."""
        print(f"\n  [USER QUERY] '{user_question}'")
        
        # 1. RETRIEVAL (The 'R' in RAG)
        print("  [PHASE 1: SEMANTIC RETRIEVAL]")
        top_matches = self.db.semantic_search(user_question, top_k=1)
        
        best_text, best_score = top_matches[0]
        print(f"    -> Extracted Context (Similarity {best_score:.2f}): '{best_text}'")
        
        # 2. AUGMENTATION (The 'A' in RAG)
        print("\n  [PHASE 2: PROMPT AUGMENTATION]")
        # We mathematically fuse the User's Question with the Retrieved Context!
        augmented_prompt = f"""
        System: You are an AI assistant. Answer the user's question using ONLY the provided Context. Do not hallucinate.
        
        Context: {best_text}
        
        User Question: {user_question}
        """
        print("    -> Final Payload constructed and ready for LLM injection.")
        
        # 3. GENERATION (The 'G' in RAG)
        print("\n  [PHASE 3: LLM GENERATION]")
        print("    -> [SIMULATED AI RESPONSE]: Based on the Q3 2024 Financial Report, the profit margin expanded to 32%.")


def demonstrate_rag():
    section_header("Project: Retrieval-Augmented Generation (RAG)")
    
    pipeline = RAGPipeline()
    print("  [INIT] Ingesting proprietary documents into Vector Database...")
    pipeline.build_knowledge_base()
    
    pipeline.execute_rag_query("What was our profit margin in Q3?")


def run_all_labs():
    demonstrate_rag()


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "Why do we mathematically require 'Vector Embeddings' for a RAG system? Why can't we just use an SQL `LIKE '%profit%'` query to find the documents?"
   Senior Answer: "Semantic vs Lexical Search. SQL `LIKE` is a Lexical search; it mathematically requires exact character matches. If a user asks 'How much money did we make?', an SQL query for 'money' will fail to find the document if it only contains the word 'Revenue' or 'Profit'. Vector Embeddings project text into High-Dimensional Semantic Space ($1536$ dimensions for OpenAI). The model mathematically understands that the concepts of 'money', 'revenue', 'profit', and 'earnings' all cluster tightly together in that space. Therefore, calculating the Cosine Similarity angle between the question and the documents will successfully retrieve the Financial Report, even if they share zero exact vocabulary words."

2. Interviewer: "If our Vector Database contains $1$ Million documents, and a user asks a question, how long does the Cosine Similarity scan take if we use a standard `for` loop (like we did in the lab)?"
   Senior Answer: "Catastrophic $O(N)$. If we calculate the exact Cosine angle against $1$ Million high-dimensional vectors sequentially in Python, the mathematical operation will take seconds or even minutes, rendering the chat application completely unusable. In Production, we do NOT use linear scans. We use specialized Vector Databases (like Pinecone, Milvus, or pgvector) that implement Approximate Nearest Neighbor (ANN) algorithms, such as HNSW (Hierarchical Navigable Small World) graphs. HNSW mathematically skips $99\\%$ of the database by navigating through a multi-layered graph architecture, dropping the search time from $O(N)$ to $O(\\log N)$, allowing us to search $1$ Billion vectors in under $10$ milliseconds."

3. Interviewer: "What is the architectural purpose of 'Chunking' large PDFs before running them through the Embedding Model?"
   Senior Answer: "Context Window Limits and Semantic Dilution. First, Embedding Models have strict token limits (e.g., $8192$ tokens). You mathematically cannot embed a $500$-page PDF in a single pass. Second, if you embed an entire $50$-page chapter as a single vector, the resulting vector becomes mathematically 'diluted'. It represents the average meaning of all $50$ pages, losing all granularity. If a user asks a highly specific question, the Cosine Similarity will fail because the specific answer is buried inside the generic average. By 'Chunking' the PDF into $500$-word overlapping paragraphs, every paragraph gets its own highly specific vector. When searched, the database acts as a sniper rifle, mathematically pulling the exact $500$-word paragraph that contains the answer."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Capstone Project (RAG System) Completed.")
