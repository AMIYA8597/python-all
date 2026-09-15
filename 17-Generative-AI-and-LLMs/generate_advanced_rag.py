import os

markdown_content = """# Advanced Retrieval-Augmented Generation (RAG) Architectures

Retrieval-Augmented Generation (RAG) has rapidly emerged as the de facto standard for building enterprise-grade Large Language Model (LLM) applications. By grounding LLM responses in external, domain-specific knowledge bases, naive RAG systems alleviate hallucinations, ensure data privacy, and allow for real-time information updates without the prohibitive costs of model fine-tuning. However, as organizations transition from prototype to production, the limitations of "naive RAG"—which typically involves simple semantic similarity search over fixed-size text chunks—become painfully apparent. 

Naive RAG pipelines often struggle with complex queries, retrieve irrelevant or contradictory context, and fail to synthesize information scattered across multiple documents. To achieve textbook depth in generative AI systems, developers must employ Advanced RAG Architectures. These advanced patterns optimize every stage of the RAG pipeline: pre-retrieval (query routing and expansion), retrieval (advanced chunking and search strategies), and post-retrieval (re-ranking and reflection).

This comprehensive guide delves into four critical advanced RAG techniques:
1. **Query Expansion (HyDE)**: Enhancing retrieval by translating queries into hypothetical answers.
2. **Parent-Child Chunking**: Decoupling the retrieval chunk size from the synthesis chunk size.
3. **Self-RAG**: Enabling LLMs to critique and reflect on their own retrieved context.
4. **GraphRAG**: Fusing vector databases with Knowledge Graphs for deep, multi-hop reasoning.

---

## 1. The Limitations of Naive RAG

Before exploring advanced techniques, it is essential to understand why naive RAG fails in complex scenarios. A standard RAG pipeline operates as follows:
1. **Document Ingestion**: Documents are split into fixed-size chunks (e.g., 500 tokens) and embedded using an embedding model.
2. **Query Embedding**: The user's query is embedded using the same model.
3. **Retrieval**: A vector database performs a k-Nearest Neighbors (k-NN) or cosine similarity search to retrieve the top-k chunks.
4. **Generation**: The top-k chunks are concatenated and injected into the LLM prompt to generate an answer.

### Failure Modes of Naive RAG
- **Semantic Mismatch**: User queries are typically short, question-oriented strings (e.g., "What is the company's revenue?"), while document chunks are long, declarative statements. Embedding models often struggle to map these two different semantic spaces effectively.
- **Context Fragmentation**: Fixed-size chunking can arbitrarily slice through semantic boundaries, leaving a chunk without its necessary surrounding context (e.g., a pronoun without its antecedent).
- **The "Lost in the Middle" Phenomenon**: Providing too many chunks to the LLM can cause the model to ignore context located in the middle of the prompt.
- **Lack of Multi-Hop Reasoning**: Naive RAG cannot easily connect the dots between entity A in document 1 and entity C in document 10.

Advanced RAG architectures are specifically designed to overcome these failure modes.

---

## 2. Query Expansion: Hypothetical Document Embeddings (HyDE)

One of the most profound challenges in retrieval is the "vocabulary mismatch" or "semantic asymmetry" between a user's concise question and the verbose, detailed nature of the target document. Query Expansion techniques aim to rewrite, expand, or augment the user's query before it hits the vector database.

### What is HyDE?
Hypothetical Document Embeddings (HyDE), introduced by Gao et al. (2022), is a highly effective pre-retrieval technique. Instead of embedding the user's query directly, HyDE uses an LLM to generate a *hypothetical* (and potentially factually incorrect) answer to the query. This hypothetical document is then embedded and used to search the vector database.

### The Intuition Behind HyDE
Why does embedding a hallucinated answer yield better retrieval results than the original query? 
1. **Symmetry**: The hypothetical answer is in the same semantic space and structural format as the target documents in the corpus.
2. **Dense Keyword Population**: The LLM naturally populates the hypothetical answer with relevant domain terminology, synonyms, and context that the user might have omitted from their terse query.

Even if the hypothetical document contains factual errors (hallucinations), its *embedding* acts as a highly effective gravitational center in the vector space, pulling in the actual, factually correct documents from the database.

### Architecture of a HyDE Pipeline
1. **Instruction Formulation**: The user query is wrapped in a prompt template: `Please write a short document answering the following question: {query}`.
2. **Hypothetical Generation**: A fast, inexpensive LLM (like GPT-3.5 or Claude 3 Haiku) generates a hypothetical response.
3. **Embedding**: The hypothetical response is vectorized.
4. **Retrieval**: The vector is used to query the Vector DB.
5. **Final Generation**: The retrieved *real* documents are passed to the primary LLM to generate the final, grounded answer.

### Python Implementation Example

```python
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

# 1. Define the HyDE prompt
hyde_prompt = PromptTemplate.from_template(
    "Write a short, hypothetical textbook snippet that answers the following question. "
    "Do not worry about exact factual accuracy, focus on using the right terminology.\n"
    "Question: {question}\n"
    "Hypothetical Answer:"
)

# 2. Setup the LLM and Embedding Model
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)
embeddings = OpenAIEmbeddings()

# 3. Create the HyDE generation chain
hyde_chain = hyde_prompt | llm | StrOutputParser()

# Function to execute HyDE retrieval
def hyde_retrieval(query: str, vectorstore: FAISS, k: int = 4):
    # Generate the hypothetical document
    hypothetical_doc = hyde_chain.invoke({"question": query})
    print(f"--- Hypothetical Document ---\n{hypothetical_doc}\n---------------------------")
    
    # Retrieve based on the hypothetical document's embedding
    retrieved_docs = vectorstore.similarity_search(hypothetical_doc, k=k)
    return retrieved_docs
```

### When to use HyDE
HyDE is particularly powerful for exploratory queries, zero-shot search domains, and audio transcripts where vocabulary might be noisy. However, it adds latency (due to the extra LLM call) and may not perform well on exact-match or highly specific ID lookups (e.g., "Find invoice #12345").

---

## 3. Context Enrichment: Parent-Child Chunking

In naive RAG, there is a fundamental tension when choosing a chunk size:
- **Small chunks** (e.g., 100 tokens) yield highly accurate and precise vector search results because the embedding vectors are tightly focused on a single concept. However, they lack surrounding context, meaning the LLM receives an isolated sentence that might be impossible to synthesize.
- **Large chunks** (e.g., 1000 tokens) provide excellent context for the LLM to generate a coherent answer, but they dilute the embedding vector. A chunk containing 5 different concepts will have an averaged embedding that struggles to match a specific query.

### The Small-to-Big Retrieval Strategy
**Parent-Child Chunking** (also known as the Auto-Merging Retriever or Small-to-Big Retrieval) resolves this tension by decoupling the *retrieval unit* from the *synthesis unit*.

The core idea is to embed small chunks for highly precise retrieval, but when a small chunk is matched, the system returns its larger parent chunk to the LLM for generation.

### Architecture and Implementation
1. **Hierarchical Document Splitting**: A source document is first split into large "Parent" chunks (e.g., 1000 tokens, representing a full section or page).
2. **Child Splitting**: Each Parent chunk is further subdivided into smaller "Child" chunks (e.g., 100 tokens, representing single sentences or paragraphs).
3. **Metadata Linking**: Every Child chunk is tagged with a `parent_id` pointing back to its corresponding Parent chunk.
4. **Vectorization**: *Only* the Child chunks are embedded and stored in the vector database. The Parent chunks are stored in a standard document store (like a NoSQL DB or an in-memory dictionary).
5. **Retrieval**: The user query searches the Child chunks.
6. **Context Injection**: For the top-k retrieved Child chunks, the system looks up their `parent_id`s, fetches the full Parent chunks, deduplicates them (in case multiple child chunks from the same parent were retrieved), and feeds the Parent chunks to the LLM.

### Example Architecture Logic

```python
import uuid
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document

# Initialize splitters
parent_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
child_splitter = RecursiveCharacterTextSplitter(chunk_size=125, chunk_overlap=25)

# Document storage
vector_db = [] # Represents our Vector Store (stores Child chunks)
doc_store = {} # Represents our Document Store (stores Parent chunks)

def process_document(text: str):
    # 1. Create Parent Chunks
    parent_chunks = parent_splitter.split_text(text)
    
    for p_chunk in parent_chunks:
        parent_id = str(uuid.uuid4())
        # Store parent in document store
        doc_store[parent_id] = p_chunk
        
        # 2. Create Child Chunks
        child_chunks = child_splitter.split_text(p_chunk)
        
        for c_chunk in child_chunks:
            # 3. Link child to parent via metadata
            child_doc = Document(
                page_content=c_chunk, 
                metadata={"parent_id": parent_id}
            )
            # Add to vector DB for embedding
            vector_db.append(child_doc)

def retrieve_with_parent_context(query: str, vector_store, doc_store):
    # Retrieve top 5 child chunks
    child_matches = vector_store.similarity_search(query, k=5)
    
    parent_ids = set()
    for child in child_matches:
        parent_ids.add(child.metadata["parent_id"])
        
    # Fetch full parent context
    full_context = [doc_store[pid] for pid in parent_ids]
    return "\\n\\n".join(full_context)
```

By retrieving at a small scale and injecting context at a large scale, Parent-Child chunking drastically reduces hallucinations caused by missing context while maintaining razor-sharp retrieval accuracy.

---

## 4. Self-RAG: Self-Reflective Retrieval-Augmented Generation

As RAG applications are deployed in critical environments (e.g., legal or medical domains), the risk of the LLM generating plausible but incorrect answers based on flawed retrieval becomes unacceptable. Traditional RAG is a linear, feed-forward mechanism: Query -> Retrieve -> Generate. 

**Self-RAG** (Self-Reflective Retrieval-Augmented Generation), introduced by Asai et al. (2023), transforms this linear pipeline into a dynamic, reflective loop. It trains or prompts the LLM to actively judge its own retrieval and generation processes using "critique tokens."

### Core Mechanisms of Self-RAG
Self-RAG enables the LLM to ask itself three fundamental questions during the generation process:
1. **Retrieve?**: Does this query actually require external retrieval, or can I answer it from internal weights?
2. **Is Relevant?**: (After retrieval) Are the retrieved documents actually relevant to the user's query? If not, the system should discard them or rewrite the query to try again.
3. **Is Supported?**: (During generation) Is the sentence I am about to generate fully supported by the retrieved context, or am I hallucinating?
4. **Is Useful?**: Does the final answer directly address the user's core query?

### Implementing Self-RAG via Agentic Workflows
While the original Self-RAG paper involved fine-tuning an open-source model (like Llama-2) to emit special critique tokens (e.g., `[Retrieve=Yes]`, `[Relevant=No]`), modern developers implement Self-RAG using Agentic frameworks like LangGraph or AutoGen.

In an agentic Self-RAG pipeline, the system uses an LLM as an evaluator in a state machine:

1. **Retrieval Evaluator Node**: After the vector DB returns chunks, a "Grader" LLM evaluates each chunk against the query.
   - *Prompt*: "You are a grader assessing relevance. Does this document contain keywords or semantic meaning relevant to the query? Answer strictly 'yes' or 'no'."
2. **Fallback Loop**: If the Grader says 'no' to all documents, the graph routes to a "Query Rewriter" node, alters the search terms, and queries the vector DB again.
3. **Hallucination Checker Node**: After the final answer is generated, another Grader LLM checks the answer against the retrieved documents.
   - *Prompt*: "Does the following generated answer contain any information not explicitly stated in the source documents? Answer 'yes' (hallucination) or 'no' (grounded)."
4. **Correction Loop**: If a hallucination is detected, the graph loops back to the generation node with a strict instruction to stick to the text.

### The Value of Reflection
Self-RAG essentially acts as a runtime alignment framework. By enforcing strict constraints and allowing the system to retry failed retrievals or hallucinated drafts, Self-RAG ensures absolute fidelity to the source documents. The trade-off is computational cost and latency, as a single user query might invoke the LLM 4 to 5 times in the background before returning an answer.

---

## 5. GraphRAG: Knowledge Graphs Meet Vector Databases

Perhaps the most significant limitation of Vector-based RAG is its inability to perform multi-hop reasoning over structured relationships. Vector databases are excellent at finding text that is *semantically similar* to a query, but they are poor at traversing explicit logical relationships.

**Example**: Suppose a corpus contains two separate documents:
1. "Company Alpha recently acquired Startup Beta."
2. "John Doe is the CEO of Startup Beta."

If a user asks, *"Who is the CEO of the company acquired by Company Alpha?"*, a standard Vector DB will struggle. Document 1 is highly similar to "Company Alpha acquired", and Document 2 is similar to "Who is the CEO". But neither document alone answers the question, and the vector search lacks the structural awareness to link "Company Alpha" -> "Startup Beta" -> "John Doe".

### Enter GraphRAG
**GraphRAG** fuses the semantic search capabilities of Vector Databases with the structured, relational logic of Knowledge Graphs (KGs). A Knowledge Graph stores data as a network of **Nodes** (entities like People, Companies, Concepts) and **Edges** (relationships like 'ACQUIRED', 'IS_CEO_OF', 'DEPENDS_ON').

### How GraphRAG Works
Implementing GraphRAG involves a complex ingestion pipeline and a dual-retrieval query pipeline.

#### Phase 1: Knowledge Extraction (Ingestion)
Instead of just chunking and embedding text, GraphRAG uses an LLM to parse the text and extract triplets: `(Subject) -[Predicate]-> (Object)`.
- *Input text*: "John Doe is the CEO of Startup Beta."
- *LLM Extraction*: `(John Doe) -[IS_CEO_OF]-> (Startup Beta)`

These entities and relationships are stored in a Graph Database (such as Neo4j). Simultaneously, the original text chunks are embedded and stored in a Vector DB. Furthermore, the nodes in the Graph DB can also hold embedding vectors of their descriptions.

#### Phase 2: Hybrid Retrieval
When a user submits a complex multi-hop query:
1. **Entity Extraction**: An LLM extracts key entities from the user's query (e.g., "Company Alpha").
2. **Graph Traversal**: The system queries the Knowledge Graph (using a language like Cypher) to traverse the relationships connected to "Company Alpha". The graph returns the linked node "Startup Beta" and subsequently "John Doe".
3. **Vector Search (Optional/Hybrid)**: The system simultaneously performs a standard vector search to find any unstructured nuance.
4. **Context Aggregation**: The structural data retrieved from the Graph (often converted back into natural language sentences like "Startup Beta has CEO John Doe") is combined with the vector chunks.
5. **Generation**: The LLM synthesizes the final answer using this vastly enriched context.

### The Microsoft GraphRAG Approach
Recently, Microsoft Research formalized an advanced GraphRAG approach. During ingestion, their system not only builds a knowledge graph of entities but also uses clustering algorithms (like Leiden) to group nodes into hierarchical "Communities." The LLM then generates a summary for every community.

When a user asks a global question like *"What are the overarching themes in this dataset?"*, naive RAG fails completely (it just retrieves a few random chunks). Microsoft's GraphRAG, however, retrieves the high-level **Community Summaries** from the knowledge graph, allowing the LLM to answer holistic, global questions with unprecedented accuracy.

### Trade-offs of GraphRAG
GraphRAG represents the pinnacle of current retrieval architectures, offering unparalleled accuracy for complex, relational queries. However, it requires significant upfront computation. Extracting entities and relationships from millions of documents via an LLM is expensive and time-consuming. Additionally, maintaining schema consistency (ensuring the LLM doesn't extract "CEO", "Chief Executive", and "Head" as three separate relationship types) requires careful prompt engineering and ontology management.

---

## Conclusion

The evolution from naive RAG to Advanced RAG Architectures marks the maturation of Generative AI applications. 

By employing **HyDE**, developers bridge the semantic gap between terse queries and verbose documents. Through **Parent-Child Chunking**, applications achieve pinpoint retrieval accuracy without sacrificing the surrounding context necessary for coherent generation. With **Self-RAG**, systems gain the introspection required to catch hallucinations and correct retrieval failures dynamically. Finally, by integrating **GraphRAG**, enterprise applications can transcend simple similarity search, enabling multi-hop reasoning and holistic data comprehension over massive, interconnected datasets.

Building a production-ready RAG system is no longer just about piping an OpenAI embedding into a vector store. It is an exercise in data engineering, retrieval optimization, and agentic orchestration. Mastering these advanced patterns is essential for any AI engineer looking to build reliable, scalable, and deeply intelligent systems.
"""

# Ensure the directory exists
import os
directory = r"d:\work\python-all\17-Generative-AI-and-LLMs"
os.makedirs(directory, exist_ok=True)

# Write to the specified file
file_path = os.path.join(directory, "07_advanced_rag.md")
with open(file_path, "w", encoding="utf-8") as f:
    f.write(markdown_content)

print(f"Successfully generated {file_path}")
