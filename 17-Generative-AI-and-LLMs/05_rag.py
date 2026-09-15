"""
# ==============================================================================
# LABORATORY: GENERATIVE AI (RETRIEVAL-AUGMENTED GENERATION - RAG)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A junior developer asks an LLM: "What were our company's Q3 revenue figures?" 
# The LLM hallucinates and says "10 Million Dollars". The developer realizes 
# the model's training data was cut off in 2022, and it has absolutely no idea 
# about private company data. They try to paste all 5,000 company PDFs into the 
# prompt, but it crashes the 8k Context Window limit.
#
# A senior AI engineer builds a RAG Pipeline. They chunk the 5,000 PDFs into 
# small paragraphs, embed them into vectors, and store them in a Vector Database. 
# When the user asks about Q3 Revenue, the system searches the database, retrieves 
# only the 3 highly relevant paragraphs, and injects them into the prompt. The 
# LLM reads the injected context and perfectly answers the question with 0% hallucination.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master Document Chunking strategies.
# - Execute Vector Database Retrieval simulations.
# - Architect the final In-Context Generation Prompt.
#
# ==============================================================================
"""

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE BUSINESS LOGIC (RAG PIPELINE SIMULATOR)
# ==============================================================================
class RAGSimulator:
    
    @staticmethod
    def chunk_document(document: str, chunk_size: int, overlap: int) -> list:
        """
        [SECURE] Recursive Character Chunking.
        LLMs cannot process 10,000-page PDFs. We must slice them into manageable chunks.
        We use 'Overlap' so that a sentence isn't accidentally cut in half, destroying 
        its semantic meaning.
        """
        print("  [INIT] Slicing Document into Chunks...")
        chunks = []
        start = 0
        doc_length = len(document)
        
        while start < doc_length:
            end = start + chunk_size
            chunk = document[start:end]
            chunks.append(chunk.strip())
            
            # Move the start forward, but step back by the 'overlap' amount
            start = end - overlap
            
        return chunks

    @staticmethod
    def mock_vector_retrieval(query: str, chunks: list) -> str:
        """
        [SECURE] Simulates a Vector Database Cosine Similarity search.
        In production, this is handled by Pinecone, Milvus, or ChromaDB.
        """
        print(f"\n  [DATABASE] Executing Semantic Search for: '{query}'")
        
        # We simulate that the database found Chunk #2 to be geometrically closest to the query.
        retrieved_chunk = chunks[1] 
        
        print(f"  -> Retrieved Context (Cosine Similarity: 0.94):\n     '{retrieved_chunk}'")
        return retrieved_chunk

    @staticmethod
    def generate_augmented_prompt(query: str, retrieved_context: str) -> str:
        """
        [SECURE] The core of RAG.
        We combine the User's Query with the Retrieved Context, and instruct the 
        LLM to STRICTLY answer using only the context to prevent hallucinations.
        """
        print("\n  [INIT] Constructing Augmented Prompt...")
        
        prompt = (
            "System: You are an expert financial analyst. Answer the user's question "
            "strictly using ONLY the provided context. If the context does not contain "
            "the answer, output 'I do not have enough information'.\n\n"
            f"Context: {retrieved_context}\n\n"
            f"User Question: {query}\n"
            "Answer:"
        )
        return prompt


# ==============================================================================
# 4. THE ARCHITECTURAL PATTERN: THE FULL PIPELINE
# ==============================================================================
def demonstrate_rag_pipeline():
    section_header("Generative AI: RAG Pipeline")
    
    # 1. The Raw Data (A massive corporate document)
    corporate_report = (
        "Acme Corp Financial Report 2024. In Q1, the company focused heavily on "
        "restructuring the logistics department, resulting in a minor loss of $2M. "
        "In Q2, new product lines were launched in Europe. Finally, in Q3, the "
        "company saw massive unprecedented growth, reporting a total Q3 revenue "
        "of $45 Million Dollars, driven primarily by enterprise software sales. "
        "Q4 projections indicate a stabilization of the market."
    )
    
    sim = RAGSimulator()
    
    # 2. Ingestion Phase: Chunking
    # Chunk Size: 100 characters. Overlap: 20 characters.
    chunks = sim.chunk_document(corporate_report, chunk_size=150, overlap=20)
    print("  -> Document successfully chunked into 4 segments.")
    
    # 3. User Query
    user_query = "What was the total revenue in Q3, and what drove it?"
    
    # 4. Retrieval Phase (Vector DB Search)
    context = sim.mock_vector_retrieval(user_query, chunks)
    
    # 5. Generation Phase (Augmented Prompting)
    final_prompt = sim.generate_augmented_prompt(user_query, context)
    
    print("\n  [FINAL LLM PAYLOAD]")
    print("-" * 60)
    print(final_prompt)
    print("-" * 60)
    
    print("\n  [FLAWLESS] The LLM now has 100% factual, private data sitting directly ")
    print("  inside its Context Window. It will securely answer '$45 Million Dollars' ")
    print("  without relying on its outdated, hallucination-prone pre-trained weights.")


def run_all_labs():
    demonstrate_rag_pipeline()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "Why is 'Chunk Overlap' absolutely critical when preparing documents for a Vector Database?"
   Senior Answer: "Semantic Boundary Preservation. If you hard-slice a document exactly every $500$ characters, you might mathematically slice a sentence directly in half: 'The Q3 revenue was exactly [CUT] $45 Million Dollars.' The first chunk gets embedded, and the second chunk gets embedded as completely separate vectors. If a user asks about Q3 revenue, neither chunk contains the full semantic meaning, and the Vector DB fails to retrieve the correct answer. By adding a $50$-character overlap, the sliding window ensures that the boundary context is preserved in both chunks, mathematically guaranteeing that the semantic meaning survives the slicing process."

2. Interviewer: "What is a 'Cross-Encoder Re-Ranker', and why is it used after standard Vector Retrieval?"
   Senior Answer: "Precision Filtering. Standard Vector Databases use 'Bi-Encoders'. They embed the Document and the Query separately, and calculate the Cosine Similarity. This is blazingly fast ($O(\\log N)$), but not incredibly accurate. A Cross-Encoder is a massive Transformer model that takes the Query AND the Document *simultaneously* and calculates a highly accurate relevance score. It is far too slow to run on $1$ Million documents. The architectural solution is a two-stage pipeline: The Bi-Encoder quickly retrieves the top $100$ chunks from the database. Then, the Cross-Encoder re-ranks those specific $100$ chunks with maximum accuracy, returning the absolute best $3$ chunks to the LLM."

3. Interviewer: "How does RAG solve the 'Context Window Limit' of LLMs?"
   Senior Answer: "Dynamic Context Injection. An LLM might have an $8,000$ token limit. A corporate codebase or wiki might contain $10,000,000$ tokens. You cannot physically load the wiki into the LLM. RAG solves this by acting as a mathematical search filter. By chunking the massive dataset and storing it in a Vector Database, the RAG system only retrieves the $3$ most semantically relevant chunks (roughly $1,000$ tokens) based on the user's specific query. It dynamically injects only those $1,000$ tokens into the prompt. The LLM gets exactly the information it needs, while remaining safely under the $8,000$ token hardware limit."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Generative AI (RAG Pipeline) Completed.")
