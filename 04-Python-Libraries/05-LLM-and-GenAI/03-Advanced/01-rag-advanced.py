"""
# ==============================================================================
# LABORATORY: ADVANCED RAG (RE-RANKING & HYDE)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Basic RAG is flawed. If a user searches "What are the side effects of Aspirin?",
# the Bi-Encoder embedding model (which converts sentences to vectors) calculates 
# mathematical similarity. It might retrieve the sentence: "What are the side 
# effects of Tylenol?", because the structure and words are 90% identical!
#
# The Bi-Encoder is incredibly fast (scaling to billions of vectors), but it 
# lacks deep semantic understanding.
#
# To achieve production-grade 99% retrieval accuracy, we use Advanced RAG pipelines:
# 1. Multi-Query: The LLM rewrites the user's question 5 different ways to 
#    maximize semantic coverage in the Vector DB.
# 2. Re-Ranking (Cross-Encoders): We fetch the top 20 results using the fast 
#    Bi-Encoder. Then, we use a massive, slow, highly accurate Cross-Encoder 
#    model to physically read the query AND the 20 results simultaneously, 
#    scoring their exact logical relevance, and re-sorting them to find the true Top 3.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the architectural difference between Bi-Encoders and Cross-Encoders.
# - Understand the Re-Ranking pipeline.
# - Understand Hypothetical Document Embeddings (HyDE).
#
# ==============================================================================
"""

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. HYPOTHETICAL DOCUMENT EMBEDDINGS (HyDE)
# ==============================================================================
def demonstrate_hyde():
    section_header("HyDE: Overcoming Lexical Mismatch")
    
    print("User Query: 'How do I fix a leaky faucet?'")
    print("\nIn a standard Vector DB, the user's short query is converted to a vector.")
    print("But the actual PDF document doesn't say 'How do I fix a leaky faucet?'.")
    print("The PDF says: 'To replace a worn O-ring in a compression valve, turn ")
    print("off the water supply...'.")
    print("\nBecause the vocabulary is completely different (Lexical Mismatch), ")
    print("the vectors might be far apart, and the search will fail!")
    
    print("\n--- The HyDE Solution ---")
    print("1. We send the User Query to an LLM with the prompt:")
    print("   'Write a paragraph answering this question: How do I fix a leaky faucet?'")
    
    print("2. The LLM hallucinates an answer (because it doesn't have the PDF yet):")
    print("   'To fix a leaky faucet, you usually need to replace the O-ring or ")
    print("    the washer inside the valve assembly...'")
    
    print("3. We take the HALLUCINATED PARAGRAPH and convert IT into a Vector!")
    print("4. We search the Vector DB using the Hallucinated Vector.")
    
    print("\nWhy does this work? Because the hallucinated paragraph shares the ")
    print("exact same dense vocabulary (O-ring, valve, washer) as the real PDF! ")
    print("The vectors perfectly align, allowing us to retrieve the factual document ")
    print("and correct the hallucination in the final generation step.")


# ==============================================================================
# 4. CROSS-ENCODER RE-RANKING
# ==============================================================================
def demonstrate_reranking():
    section_header("The Two-Stage Retrieval Pipeline (Re-Ranking)")
    
    print("A Bi-Encoder processes Document A and Document B completely separately.")
    print("It calculates their vectors, caches them in RAM, and uses fast Cosine ")
    print("Similarity. It is lightning fast, but semantically shallow.\n")
    
    print("A Cross-Encoder concatenates Document A and Document B into a single string:")
    print("[CLS] User Query [SEP] PDF Document [SEP]")
    print("It feeds both into the Transformer simultaneously. The Self-Attention ")
    print("heads physically calculate the exact logical relationships between every ")
    print("word in the query and every word in the document.")
    print("This is unbelievably accurate, but incredibly slow. You cannot run ")
    print("a Cross-Encoder on 100,000 documents. It would take hours.\n")
    
    print("--- The Production Pipeline ---")
    print("Step 1 (Fast Search): User asks 'Side effects of Aspirin?'.")
    print("Step 2 (Bi-Encoder): ChromaDB instantly searches 10,000,000 vectors ")
    print("       and retrieves the Top 20 broadly related chunks.")
    print("       (Results might include Aspirin, Tylenol, Advil).")
    
    print("\nStep 3 (Re-Ranking): We pass the User Query AND the 20 chunks ")
    print("       into the slow, powerful Cross-Encoder model (e.g. `bge-reranker`).")
    print("       The Cross-Encoder assigns a logical score (0.0 to 1.0) to all 20.")
    
    print("Step 4 (Final Selection): We sort the 20 chunks by the Cross-Encoder ")
    print("       score. The top 3 chunks (which are now guaranteed to be specifically ")
    print("       about Aspirin) are injected into the final LLM Prompt!")


def run_all_labs():
    demonstrate_hyde()
    demonstrate_reranking()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. What is "Multi-Query Retrieval" and what specific problem does it solve?
   Answer: Multi-Query Retrieval solves the problem of "User Query Fragility". If a user searches "Why is the sky blue?", the Vector DB retrieves specific vectors. If they search "What causes the color of the atmosphere?", the semantic meaning is identical, but the Vector DB might return completely different results because the geometric starting point is altered. Multi-Query uses an LLM to automatically rewrite the user's single query into 5 different variations (e.g., "Reason for blue sky", "Atmospheric scattering"). It executes 5 separate Vector DB searches, combines all retrieved chunks, deduplicates them, and feeds the massive context to the final LLM. This guarantees high recall regardless of how poorly the user phrased the initial question.

2. Why can't we just use a Cross-Encoder for the entire database search to get perfect accuracy?
   Answer: Computational Complexity ($O(N)$ vs $O(1)$). A standard Vector DB (Bi-Encoder) pre-calculates the 100,000 document vectors offline. At search time, it only has to embed the single User Query ($O(1)$ Neural Network pass) and then do a blazing-fast dot-product math operation against the database. A Cross-Encoder requires both the Query and the Document to be passed through the deep Neural Network *together*. To search 100,000 documents, you would literally have to execute the massive Neural Network forward pass 100,000 times! It is computationally impossible for real-time search.

3. Explain the architecture of a "Parent Document Retriever".
   Answer: In standard RAG, if you split a PDF into tiny 100-word chunks, the Vector Search is highly accurate (because small chunks have focused semantic vectors). However, the final LLM generation suffers because 100 words lacks broad context. If you split into massive 1,000-word chunks, the LLM has great context, but the Vector Search fails (because massive chunks average out to a noisy, generic vector). 
   The Parent Document Retriever solves this by splitting the PDF twice. It creates massive "Parent" chunks (1,000 words), and then chops those into 10 tiny "Child" chunks (100 words). The Vector DB *only* embeds and searches the tiny Child chunks. When a Child chunk matches the user query, the database does NOT return the Child. Instead, it looks up the ID of the massive Parent chunk and returns the entire 1,000-word Parent to the LLM. You get the perfect accuracy of micro-search, combined with the massive context of macro-generation!
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Advanced RAG Completed.")
