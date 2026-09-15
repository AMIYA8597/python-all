import os

markdown_text = """
# Agent Memory Architectures and Strategic Planning

## Introduction to Agentic AI Cognitive Architectures

In the rapidly evolving landscape of artificial intelligence, the transition from simple reactive models to fully autonomous, goal-oriented agents represents a monumental paradigm shift. At the core of this transition lies the development of sophisticated **Cognitive Architectures**—frameworks that endow AI agents with the ability to perceive their environment, remember past interactions, plan for the future, and execute complex sequences of actions. Two of the most critical pillars supporting these cognitive architectures are **Agent Memory** and **Strategic Planning**.

This comprehensive textbook-level reference document delves deep into the theoretical foundations, architectural designs, and practical implementations of memory systems and planning mechanisms in Agentic AI. By exploring Short-Term Memory (STM), Long-Term Memory (LTM), the Plan-and-Solve paradigm, and Self-Reflection loops, we provide an exhaustive understanding of how state-of-the-art AI agents operate, reason, and learn over time. The material covered here bridges the gap between academic research papers and production-ready system designs.

---

## Part 1: Agent Memory Architectures

Memory is the bedrock of intelligent behavior. Without memory, an agent is trapped in a perpetual present, unable to learn from mistakes, recall user preferences, or maintain coherence across long interactions. In Agentic AI, memory is typically bifurcated into two primary systems, mimicking human cognitive psychology: Short-Term Memory (STM) and Long-Term Memory (LTM). Each serves a distinct purpose and is governed by different technical constraints and architectural paradigms.

### 1.1 Short-Term Memory (STM): The Context Window

Short-Term Memory in an AI agent refers to the information retained within the current execution context or conversation session. It is the agent's "working memory"—the immediate scratchpad used to process incoming information, hold intermediate reasoning steps, and maintain conversational flow. In human terms, this is equivalent to the few items you can hold in your head while actively solving a problem.

#### 1.1.1 The Mechanics of STM

In Large Language Models (LLMs), STM is fundamentally constrained by the **Context Window**. The context window dictates the maximum number of tokens (words or subwords) the model can process simultaneously. Everything the agent needs to know to generate the next response—including the system prompt, conversation history, retrieved documents, and intermediate tool outputs—must fit within this window.

Technically, STM is often implemented as a list or array of JSON objects, representing the conversation history or a sequence of thoughts and observations. This structure maps directly to the chat completions API format used by major providers like OpenAI, Anthropic, and Google.

```json
[
  {"role": "system", "content": "You are a helpful autonomous agent with advanced planning capabilities. You use your tools to accomplish tasks."},
  {"role": "user", "content": "Analyze the sales data for Q3 and summarize the top three performing regions."},
  {"role": "agent", "content": "I will first query the database for Q3 sales data.", "tool_calls": [{"name": "query_db", "arguments": {"quarter": "Q3"}}]},
  {"role": "tool", "content": "{\\"sales\\": 150000, \\"growth\\": 0.12, \\"regions\\": {\\"NA\\": 50000, \\"EU\\": 60000, \\"APAC\\": 40000}}"},
  {"role": "agent", "content": "The Q3 sales were $150,000, representing a 12% growth. The top regions were EU, NA, and APAC in that order."}
]
```

Every time the agent takes an action or the user speaks, a new JSON object is appended to this array.

#### 1.1.2 Limitations and Management of STM

While recent advancements have expanded context windows (e.g., from 4K tokens in early models to over 1M or even 2M tokens in models like Gemini 1.5 Pro), STM remains a scarce resource for long-running autonomous agents. A 1M token window might seem infinite, but when an agent is independently browsing the web, reading large codebases, or analyzing dense CSV files, that limit can be reached in a matter of hours.

Furthermore, pushing the limits of the context window can lead to:
- **Increased Latency:** Processing millions of tokens for every step takes time. Time-to-first-token (TTFT) increases significantly.
- **Higher Computational Costs:** API costs scale linearly with input token counts. Repeatedly sending a 500K token history for every minor interaction becomes prohibitively expensive.
- **The "Lost in the Middle" Phenomenon:** Extensive research shows that models struggle to retrieve information buried in the middle of a massive prompt, often over-indexing on the very beginning (the system prompt) or the very end (the most recent messages) of the context window.

To effectively manage STM, agents employ several strategies:
- **Summarization:** When the conversation history grows too long, an auxiliary model or routine summarizes older exchanges, replacing raw dialogue with a condensed representation. "User and agent discussed database schemas" replaces 50 lines of back-and-forth.
- **Sliding Windows:** Keeping only the most recent N interactions and discarding older ones, assuming older context is less immediately relevant to the current task.
- **Attention Sinks:** Techniques to maintain model performance even when exceeding theoretical context limits by preserving initial "sink" tokens that absorb disproportionate attention weights.
- **Memory Paging (MemGPT Architecture):** Similar to an operating system managing RAM and disk storage, MemGPT creates an architecture where the LLM can explicitly page information in and out of its context window from external storage using specialized tool calls (e.g., `search_memory`, `archive_memory`).

### 1.2 Long-Term Memory (LTM): Semantic Retrieval

If STM is the agent's working memory, Long-Term Memory (LTM) is its vast experiential knowledge base. LTM allows an agent to recall facts, user preferences, past successes, and failures across distinct sessions, spanning days, weeks, or even years. This is essential for continuous learning, personalization, and creating AI that feels truly persistent.

#### 1.2.1 Vector Databases and Semantic Embedding

The standard architecture for LTM in modern AI agents relies on **Vector Databases** (e.g., Pinecone, Milvus, Qdrant, Chroma, Weaviate, pgvector). The process involves converting textual or multimodal data into high-dimensional numerical vectors, known as **Embeddings**. 

When an agent experiences a significant event, finishes a conversation, or learns a new fact, it passes this information through an embedding model (like OpenAI's `text-embedding-3-large` or open-source equivalents like `all-MiniLM-L6-v2`). The model outputs a dense vector representing the semantic meaning of the text. This vector is then stored in the Vector DB alongside the original text (the payload) and relevant metadata (timestamps, session IDs).

#### 1.2.2 The Retrieval Process (RAG)

When the agent needs to recall information, it employs a mechanism closely related to Retrieval-Augmented Generation (RAG). 

1. **Query Formulation:** The agent recognizes a need for past knowledge and formulates a search query (e.g., "What did the user say their favorite programming language was?"). Often, a sub-agent is responsible solely for translating conversational context into optimal search queries.
2. **Embedding the Query:** The query is embedded into a vector using the exact same embedding model used for storage.
3. **Similarity Search:** The Vector DB computes the similarity between the query vector and all stored vectors in the database.
4. **Context Injection:** The top-K most similar memory fragments are retrieved and injected into the agent's Short-Term Memory (Context Window). This primes the LLM with the necessary historical context to inform its next action.

#### 1.2.3 Advanced LTM Architectures

Beyond simple flat vector retrieval, advanced agentic memories utilize sophisticated structural approaches:
- **Graph Databases (Knowledge Graphs):** Storing entities and explicit relationships (e.g., `[User] -> [Works At] -> [OpenAI]`). This allows for complex, multi-hop reasoning that vector DBs struggle with. For example, answering "Who is the manager of the person I met yesterday?" requires traversing a graph of relationships, which is highly inefficient using pure vector similarity.
- **Hybrid Search:** Combining dense vector search (for semantic meaning) with sparse keyword search (like BM25) to ensure exact matches for specific terminology (like error codes, proper nouns, or unique IDs) are not lost in the semantic approximation.
- **Memory Consolidation:** A background process (often running during agent "downtime" or idle periods) that reviews recent STM, extracts salient facts, resolves contradictions (e.g., "User used to like Python, but now prefers Rust"), and updates LTM. This mimics human sleep-dependent memory consolidation.
- **Episodic vs. Semantic Memory:** Separating specific past events (Episodic: "Yesterday at 3 PM I crashed the production database when running a specific query") from general knowledge (Semantic: "Dropping a table without a backup is a dangerous operation").

---

## Part 2: Strategic Planning and Agent Execution

Equipped with robust memory, an agent can understand its environment and past context. However, to achieve complex, long-horizon goals, an agent must possess **Strategic Planning** capabilities. It must be able to break down a massive task into manageable subtasks, execute them sequentially or in parallel, and adapt dynamically when things go wrong.

### 2.1 The Core Necessity of Planning

Standard LLMs are autoregressive—they generate text one token at a time based on preceding tokens. This architecture excels at immediate, reactive generation but fundamentally struggles with long-term coherence and multi-step reasoning. Without a formal planning architecture, an agent asked to "Research competitive pricing for X, build a dynamic web scraper, deploy it to AWS Lambda, and configure an automated email report" will inevitably fail. 

It will hallucinate steps, lose track of its progress within the context window, or get stuck in an infinite loop of failed tool calls because it lacks a global view of the objective. It acts like a person navigating a maze with a flashlight that only illuminates one step ahead. Planning provides the overhead map.

### 2.2 The Plan-and-Solve Architecture

To overcome the autoregressive limitation, AI researchers introduced the **Plan-and-Solve** paradigm. This is widely instantiated through frameworks like BabyAGI, AutoGPT, HuggingGPT, and modern implementations in LangChain (LangGraph) or Microsoft's AutoGen. 

The fundamental principle is to decouple the act of *deciding what to do* (Planning) from the act of *doing it* (Execution). This separation of concerns allows different models or personas to handle high-level strategy versus low-level implementation.

#### 2.2.1 The Planner Agent (The Orchestrator)

The Planner Agent is responsible for high-level cognitive tasks and global strategy. Given a complex user goal, the Planner's job is to decompose the goal into a structured, Directed Acyclic Graph (DAG) of subtasks or a linear sequence of execution steps. 

**The Planner's Prompt typically involves:**
- The overarching user goal.
- The agent's available tools and skill sets.
- Strict constraints (time limits, budget, specific technologies to use or avoid).
- Formatting instructions to output the plan in a machine-readable format.

**Output of the Planner:**
A concrete plan, often formatted in strict JSON, which the orchestrating framework parses into executable state machines.
```json
{
  "plan": [
    {"step_id": "step_1", "task": "Research Python web scraping libraries focusing on asynchronous capabilities.", "status": "pending"},
    {"step_id": "step_2", "task": "Write the scraping script using aiohttp and BeautifulSoup.", "status": "pending", "dependencies": ["step_1"]},
    {"step_id": "step_3", "task": "Write an AWS Lambda deployment script using Serverless framework.", "status": "pending", "dependencies": ["step_2"]},
    {"step_id": "step_4", "task": "Execute deployment and trigger the scraper to test.", "status": "pending", "dependencies": ["step_3"]}
  ]
}
```

#### 2.2.2 The Executor Agent(s) (The Workers)

Once the Planner generates the plan, the orchestrator passes control to the **Executor Agent**. The Executor is a highly focused, tactical agent. It does not need to understand the entire overarching goal; it only needs to successfully complete the specific subtask assigned to it in the current step.

By isolating the Executor's context to just the current subtask, we prevent cognitive overload, preserve the Short-Term Memory window, and reduce hallucination. If a task is "Write the scraping script," the Executor's prompt is heavily tailored for coding, omitting unnecessary context about AWS deployment. In multi-agent systems, Executors might be specialized (e.g., a "Code Writer Agent", a "Web Searcher Agent", a "QA Agent").

#### 2.2.3 Dynamic Replanning

No plan survives contact with reality. A critical feature of robust strategic planning is **Dynamic Replanning**. If an Executor agent encounters an unrecoverable error (e.g., AWS credentials are invalid, or a website blocks the scraper with CAPTCHAs), it reports back to the Planner with an error state. 

The Planner must then adjust the remaining plan. It takes the original plan, the history of successful steps, and the recent failure as input, and outputs a revised plan. For instance, it might insert a step to request new credentials from the user, or switch to a local execution strategy using Docker instead of AWS Lambda.

### 2.3 Self-Reflection and Metacognition Loops

The most advanced agent architectures incorporate **Metacognition**—the ability to think about one's own thinking. This is operationalized through **Self-Reflection Loops**. An agent that blindly executes code without checking if it works is brittle. An agent that reflects on its output before committing is robust.

#### 2.3.1 The Reflection Process

Before committing to a final answer or concluding a task, an agent can invoke a reflection loop. This involves prompting a secondary model (or the same model adopting a "Critic" persona) to critique the proposed output or execution trajectory.

**Example Reflection Prompt:**
> "You are a senior Principal Engineer and rigorous code reviewer. Review the following Python script generated by a junior agent. Identify any security flaws (like prompt injection vulnerabilities or exposed secrets), edge cases not handled, or logic errors. Do not rewrite the code, only provide a detailed critique and actionable steps for improvement."

The critique is fed back to the original Executor agent, which iteratively refines its work. Techniques like **ReAct** (Reasoning and Acting) intertwine reasoning traces ("Thought: I need to search the web for the error code. Action: WebSearch. Observation: The error means the port is in use.") with actions, naturally facilitating a micro-reflection before every single tool call.

#### 2.3.2 Advanced Reflection: Tree of Thoughts (ToT)

Moving beyond linear Chain-of-Thought (CoT), **Tree of Thoughts (ToT)** allows an agent to explore multiple potential planning branches simultaneously. When faced with a complex decision, the agent generates several possible next steps (branches). It then evaluates the viability of each branch using a self-evaluation prompt, assigning a heuristic score. It selectively explores the most promising paths, and backtracks if a path hits a dead end. 

This search-based approach to planning (similar to A* search or Monte Carlo Tree Search in traditional AI) significantly enhances an agent's ability to solve complex mathematical, logic, or programming puzzles where early mistakes can doom linear progression.

---

## Part 3: Deep Dive into Memory Structures and Vector Mathematics

To build production-grade agentic systems, one must deeply understand the underlying structures governing Long-Term Memory. It is not enough to simply call an API; architects must understand the math and data structures driving these systems.

### 3.1 The Mathematics of Semantic Search
When we say an embedding is a high-dimensional vector, we are referring to an array of floating-point numbers, typically ranging from 384 dimensions (e.g., MiniLM) to 1536 dimensions (e.g., OpenAI's Ada v2), or even up to 4096 dimensions in larger models.

Each dimension in this space represents an abstract, latent feature of the text learned by the neural network during its massive pre-training phase. While these dimensions are not human-interpretable individually (e.g., dimension 42 does not explicitly map to the concept of "plurality" or "technology"), the spatial relationship between vectors in the high-dimensional space is highly meaningful. Concepts that are semantically related cluster together.

#### 3.1.1 Distance Metrics
The most common metric for retrieving memories is **Cosine Similarity**. It measures the cosine of the angle between two vectors in the multi-dimensional space, focusing purely on orientation rather than magnitude.
Formula: 
$similarity(A, B) = \\frac{A \\cdot B}{||A|| ||B||}$

Where $A \\cdot B$ is the dot product of the vectors, and $||A||$ and $||B||$ are their respective magnitudes. A cosine similarity of 1 means the vectors point in the exact same direction (high semantic similarity), 0 means they are orthogonal (unrelated), and -1 means they are diametrically opposed. Other metrics include Euclidean Distance (L2 norm) which accounts for magnitude, and Dot Product, which is computationally fastest when vectors are normalized.

### 3.2 Bridging the Gap: The Working Memory Model
An emerging pattern is the **Working Memory Model**, which acts as a bridge between STM and LTM. Instead of directly injecting LTM search results into the conversation array, the agent has a dedicated "scratchpad" space. The agent can write findings to the scratchpad, read from it, and eventually synthesize it. This prevents the primary conversation flow from becoming cluttered with raw database search results, keeping the agent focused on the user interaction while still having access to deep information.

---

## Part 4: Advanced Strategic Planning Methodologies

### 4.1 Chain of Hindsight (CoH)
Chain of Hindsight is a planning and reflection technique where the agent is explicitly conditioned on past failures. Instead of just trying to generate the correct plan, the agent's prompt includes examples of plans that failed and the explicitly deduced reasons for their failure.

Prompt structure:
> "Goal: Deploy Database to cluster. Past Attempt: [Plan A]. Result: Failed because port 5432 was blocked by the security group. New Plan:"

This forces the model's attention mechanism to route around known obstacles, significantly improving success rates in complex, deterministic environments like terminal execution, infrastructure as code deployment, or code compilation.

### 4.2 Multi-Agent Debate and Consensus
In critical scenarios (e.g., medical diagnosis, financial trading execution, destructive infrastructure changes), relying on a single Planner agent can lead to hallucinations or suboptimal strategies. Modern architectures utilize **Multi-Agent Debate**. 
- **Planner A** generates a strategy based on a conservative persona.
- **Planner B** generates an alternative strategy based on an aggressive/innovative persona.
- A **Critic Agent** reviews both plans, highlighting pros, cons, and potential failure modes.
- A **Consensus Agent** (or a human-in-the-loop) synthesizes the best elements of both into a final, highly robust execution plan.

This mimics human corporate planning committees and leverages the diversity of different LLM personas (or even different foundational models, e.g., using GPT-4 for Strategy A and Claude 3.5 Sonnet for Strategy B) to mitigate the biases inherent in any single model.

### 4.3 Algorithmic Planning and Neuro-Symbolic Integration
While LLMs are excellent at semantic planning and creative problem-solving, they notoriously struggle with strict algorithmic constraints (e.g., the Traveling Salesperson Problem, rigid dependency scheduling, exact resource allocation, or complex math).

To bridge this gap, state-of-the-art architectures implement **Neuro-Symbolic Planning**. The LLM (the neural component) acts as a natural language interface and translator. It parses the user's fuzzy, natural language goal into a strictly formal planning language like PDDL (Planning Domain Definition Language). A traditional, deterministic algorithmic solver (the symbolic component, like a SAT solver or linear programming engine) then computes the mathematically optimal plan. Finally, the LLM translates this symbolic plan back into natural language or API calls for the Executor agents to carry out.

---

## Part 5: Implementation Blueprints for Production Agents

For software engineers and AI architects tasked with building these systems in production, consider the following blueprint for a robust Agentic AI memory and planning engine:

### Step 1: The Memory Manager Middleware
Implement a middleware layer that intercepts every message between the user, the tools, and the LLM. This middleware should:
- Maintain the short-term JSON array representing the conversation.
- Run a token-counting utility (e.g., `tiktoken` for OpenAI models) to ensure the array stays within safe bounds.
- Trigger asynchronous summarization when the token limit hits an 80% threshold, ensuring the system never throws a context length exceeded error during a critical execution step.

### Step 2: The Embedding Pipeline and Vector DB
Set up a background worker (e.g., using Celery, Kafka, or AWS SQS) that consumes the conversational summaries. It generates embeddings via an API and upserts them into a Vector Database. Crucially, attach rich metadata to these vectors (timestamp, user ID, session ID, task category). This allows for **Hybrid Search**—you can filter by `user_id == '123'` (exact match) and then rank the results by semantic similarity to the query, drastically reducing search space and improving accuracy.

### Step 3: The Planner-Executor Loop
Use a framework like LangGraph, LlamaIndex Workflows, or Microsoft AutoGen to construct the DAG of tasks. 
- Define a strong System Prompt for the Planner that demands JSON-formatted plans. Use feature flags like OpenAI's `response_format={ "type": "json_object" }` to guarantee parsing reliability.
- Implement a parsing function that converts the Planner's JSON output into executable Python objects (e.g., Pydantic `Task` classes).
- Create a priority queue for the Executor agent to consume these `Task` objects.
- Implement a rigorous Try/Catch block around the Executor's tool calls. On exception, capture the `stderr` and traceback, pass it to a Reflector agent, which updates the Task object with a `correction_hint`, and re-queues it for execution.

---

## Conclusion: The Future of Cognitive Architectures

The architecture of an autonomous AI agent is a complex orchestration of immediate context, vast historical knowledge, and rigorous strategic foresight. By carefully managing Short-Term Memory limits, leveraging Vector Databases for Long-Term semantic recall, decoupling strategy from execution via the Plan-and-Solve paradigm, and instituting rigorous Self-Reflection loops, developers can build AI systems that are not just reactive chatbots, but persistent, goal-oriented digital entities capable of tackling the world's most complex challenges.

As we look toward the horizon, the distinction between short-term context and long-term storage is beginning to blur. Innovations like Ring Attention and infinite context models (capable of processing millions of tokens) challenge the necessity of complex RAG pipelines for some use cases. However, **computational efficiency**, **latency**, and **information salience** guarantee that structured memory architectures will remain vital. A model might be *able* to read a 10-million-token history for every query, but doing so is neither economically feasible nor cognitively optimal.

Similarly, strategic planning will evolve from static DAGs generated a priori to fluid, continuous reinforcement learning loops. Agents will not just plan; they will simulate the outcomes of their plans in latent space (similar to AlphaGo's Monte Carlo Tree Search) before executing a single line of code in reality. 

The integration of robust Agent Memory Architectures and Strategic Planning is precisely what elevates a Large Language Model from a mere text generator into an active, reasoning, and indispensable digital collaborator.

*This reference guide is designed for developers, researchers, and AI architects tasked with building next-generation agentic workflows. Mastery of these memory and planning paradigms is the prerequisite for pushing the boundaries of autonomous artificial intelligence.*

---

## Appendix A: State-of-the-Art Frameworks for Agent Memory and Planning

To practically apply the concepts of STM, LTM, and Plan-and-Solve architectures, developers rely on several mature frameworks. Understanding the strengths and weaknesses of these frameworks is crucial for selecting the right tool for the job.

### A.1 LangChain and LangGraph
LangChain is arguably the most popular framework for building LLM applications. It provides primitive abstractions for memory (e.g., `ConversationBufferMemory`, `VectorStoreRetrieverMemory`) and tools. However, its most significant contribution to agentic planning is **LangGraph**.
LangGraph allows developers to model agent workflows as graphs. Instead of relying on the LLM to implicitly manage state and sequence, LangGraph makes the state machine explicit. Nodes represent agents or tools, and edges represent the flow of data. This is particularly powerful for implementing the **Plan-and-Solve** architecture, as you can create a dedicated Planner node that routes execution to various Executor nodes, with explicit reflection loops built into the graph structure.

### A.2 LlamaIndex
While LangChain focuses on broad tooling, LlamaIndex excels at data ingestion and structuring—the core of **Long-Term Memory**. It provides advanced abstractions for building indices over unstructured data (documents, code, APIs). For memory, LlamaIndex offers features like Sub-Question Query Engines, which break down a complex query into simpler questions, query the vector DB for each, and synthesize the results. This is highly aligned with the Planner-Executor pattern but focused entirely on data retrieval.

### A.3 Microsoft AutoGen
AutoGen is a framework designed specifically for multi-agent conversations. It shines in implementing the **Multi-Agent Debate and Consensus** patterns discussed in Section 4.2. In AutoGen, you define agents with specific personas (e.g., "User Proxy", "Coder", "Reviewer"). These agents converse with each other to solve a task. AutoGen inherently handles the conversation history (STM) and allows for complex planning through conversational flow rather than rigid DAGs. It is particularly effective for tasks requiring code generation and execution, as the User Proxy agent can automatically run the code generated by the Coder and feed the execution results back into the conversation for reflection.

### A.4 AutoGPT and BabyAGI
These are pioneering projects that popularized the autonomous agent concept. BabyAGI introduced a simple but effective loop: pull the top task from a queue, execute it, evaluate the result, and generate new tasks based on the outcome. This loop is the foundation of dynamic replanning. AutoGPT expanded on this by giving the agent access to a wide array of tools (web search, file I/O) and a workspace. While they are often considered experimental, studying their codebases provides profound insights into the raw mechanics of agentic memory and goal-oriented execution.

### A.5 MemGPT (Memory-GPT)
MemGPT specifically addresses the limitations of the context window. It introduces an architecture inspired by traditional operating systems. The LLM acts as the CPU, the context window is the RAM, and an external database is the Disk. MemGPT agents are trained to recognize when they need information not currently in their context window and use specific tool calls (like `search_memory`) to page that information in from the database. They also use tool calls to archive information before it falls out of the context window. This creates the illusion of infinite memory, making it ideal for persistent virtual companions or long-running support agents.

By combining the theoretical knowledge of cognitive architectures with the practical abstractions provided by these frameworks, developers can rapidly build and deploy highly capable, intelligent agents.

---

## Appendix B: Detailed Code Example - Building a Vector Memory Store

To solidify the concepts of Long-Term Memory (LTM), let us examine a practical implementation using Python, OpenAI embeddings, and a local ChromaDB vector store. This example demonstrates how an agent can store an experience and later retrieve it based on semantic similarity.

```python
import chromadb
from chromadb.utils import embedding_functions

# Initialize the Chroma client and create a collection for our agent's memory
client = chromadb.Client()
openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key="YOUR_API_KEY",
    model_name="text-embedding-3-small"
)

collection = client.create_collection(
    name="agent_long_term_memory",
    embedding_function=openai_ef
)

# Step 1: Memory Formation (Consolidation)
# The agent learns something new and stores it in LTM.
documents = [
    "The user's primary development environment is VS Code on a Mac.",
    "The user prefers deployment scripts written in Bash rather than Python.",
    "Project 'Alpha' is currently blocked by the legal team pending compliance review."
]

# We add metadata to allow for hybrid filtering later.
metadatas = [
    {"source": "conversation", "topic": "preferences", "timestamp": "2023-10-27T10:00:00Z"},
    {"source": "conversation", "topic": "preferences", "timestamp": "2023-10-27T10:05:00Z"},
    {"source": "status_report", "topic": "project_alpha", "timestamp": "2023-10-27T14:30:00Z"}
]

ids = ["mem_001", "mem_002", "mem_003"]

# Insert the memories into the Vector Database
collection.add(
    documents=documents,
    metadatas=metadatas,
    ids=ids
)
print("Memories successfully stored in Vector DB.")

# Step 2: Memory Retrieval (RAG)
# The agent is asked to write a deployment script. It queries its memory for preferences.
query_text = "How should I write the deployment script for the user?"

# The DB automatically embeds the query and performs a cosine similarity search
results = collection.query(
    query_texts=[query_text],
    n_results=1, # Retrieve the top 1 most relevant memory
    where={"topic": "preferences"} # Hybrid search: Semantic + Metadata filter
)

print(f"Query: {query_text}")
print("Retrieved Memory:")
for doc, meta, distance in zip(results['documents'][0], results['metadatas'][0], results['distances'][0]):
    print(f" - Document: {doc}")
    print(f" - Metadata: {meta}")
    print(f" - Distance (lower is closer): {distance}")
```

### Analysis of the Code
In this example, the `embedding_function` handles the transformation of text into vectors transparently. When we call `collection.add()`, the text is sent to the OpenAI API, converted to vectors, and stored alongside the text payload and metadata. 

When the agent needs information (`collection.query()`), the query text is similarly embedded. The crucial feature here is the `where={"topic": "preferences"}` argument. This demonstrates **Hybrid Search**. Before calculating the cosine distance of thousands of vectors, the database filters the candidate pool using deterministic metadata (topic must be 'preferences'). This ensures that the agent doesn't accidentally retrieve a memory about "Project Alpha" just because it coincidentally shares some semantic overlap with the query. 

This tight integration of semantic recall and deterministic filtering is the cornerstone of production-grade agentic memory systems.
"""

word_count = len(markdown_text.split())
print(f"Total word count: {word_count}")

# We need to make sure it's 2000 to 3000 words. Let's make it a bit longer.
if word_count < 2200:
    extra_section2 = """
---

## Appendix C: Debugging Agentic Architectures

When working with these systems, developers will frequently run into scenarios where the agent fails to plan properly or retrieves the wrong memory. Below are some of the most common pitfalls and debugging strategies for cognitive architectures.

### C.1 Context Starvation
**Symptoms:** The agent generates generic or irrelevant plans; the Planner seems to ignore specific constraints provided by the user earlier in the session.
**Diagnosis:** The critical context was truncated or "summarized away."
**Solution:** Implement explicit "pinning" of critical facts. When a user states a hard constraint ("Never use Python 2"), save this in a dedicated `core_memory` block that is always injected at the top of the prompt, immune to rolling summarization.

### C.2 Attention Dilution (Lost in the Middle)
**Symptoms:** The agent is provided with 50 pages of retrieved documents, but its answers completely ignore facts located in pages 10-40.
**Diagnosis:** The LLM's attention mechanism is overwhelmed by the sheer volume of text and naturally focuses on the beginning and end of the prompt.
**Solution:** Before sending raw retrieved documents to the final Executor agent, pass them through a specialized "Extractor" agent. The Extractor takes the documents and the specific query, and outputs a concise bulleted list of only the relevant facts. The Executor then uses this condensed list.

### C.3 Planning Paralysis (Infinite Loops)
**Symptoms:** The agent attempts the same tool call with the same parameters repeatedly, despite receiving error messages.
**Diagnosis:** The agent's Short-Term Memory is filled with its own errors, creating a self-reinforcing loop. It cannot "see" a path out.
**Solution:** Implement a systemic circuit breaker. If the orchestrator detects three identical failed tool calls, it should interrupt the execution loop and force a **Metacognitive Reflection step**. The agent is presented with a trace of its failures and explicitly prompted: "Your last 3 attempts failed. Identify why the strategy is flawed and propose a completely new approach. Do not retry the same action."

By understanding both the theoretical architecture and the practical debugging of these systems, developers can ensure their Agentic AI remains robust and capable in production environments.
"""
    markdown_text += extra_section2

word_count = len(markdown_text.split())
print(f"Final Total word count: {word_count}")

with open(r"d:\work\python-all\18-Agentic-AI\03_memory_and_planning.md", "w", encoding="utf-8") as f:
    f.write(markdown_text)

print("Markdown generated successfully.")
