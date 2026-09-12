# Agentic AI: Memory and Planning

## Introduction

While simple chatbots map inputs directly to outputs, **Agentic AI** requires the ability to pursue complex, multi-step goals over time. To achieve this, an agent needs two critical cognitive architectures: **Memory** (the ability to retain and retrieve past information) and **Planning** (the ability to break down a large goal into manageable, sequential steps).

### Why They Exist
-   **Planning** transforms an LLM from a reactionary text generator into a proactive problem solver. It prevents the model from thrashing aimlessly by providing a roadmap.
-   **Memory** prevents the \"Groundhog Day\" effect. It allows the agent to learn about the user, avoid repeating mistakes, and maintain context across long-running tasks that exceed the standard token limit of the model.

---

## Beginner Explanation

### Planning: The Recipe
Imagine you are asked to bake a cake. You don't just start throwing flour in a bowl. You first write a plan: 1. Find a recipe, 2. Buy ingredients, 3. Mix batter, 4. Bake, 5. Frost. 
Agents do the same thing. Given a task like \"Research AI trends and write a report,\" the agent first uses its reasoning capabilities to draft a step-by-step plan before taking any action.

### Memory: The Notebook
Imagine baking that cake, but every 5 minutes, you completely forget everything that happened previously. You'd constantly re-read the recipe or re-buy ingredients. 
Memory is the agent's notebook. 
-   **Short-term memory:** Remembering what steps of the plan are done and what the immediate next step is (kept in the current conversation).
-   **Long-term memory:** Remembering that you (the user) are allergic to nuts, so it shouldn't buy peanut butter for the cake next time (stored in a database).

---

## Deep Technical Explanation

### 1. Planning Architectures

Planning in AI is an active area of research. Several paradigms have emerged:

#### A. ReAct (Reasoning and Acting)
The most common baseline. The agent alternates between thinking and doing.
*   **Thought:** \"I need to find the user's email address in the database.\"
*   **Action:** `query_db(user=\"John\")`
*   **Observation:** `[email: john@test.com]`
*   **Thought:** \"Now I have the email, I will send the message.\"
ReAct is great for short tasks but can get lost in long horizons.

#### B. Plan-and-Solve (or Plan-and-Execute)
The agent separates planning from execution. 
1.  **Planner:** A call to the LLM specifically to generate a JSON array of steps based on the user's goal.
2.  **Executor:** The agent iterates through the steps sequentially, using ReAct for each individual step.
This is much more stable for complex tasks because the agent always has the high-level roadmap to refer back to.

#### C. Tree of Thoughts (ToT) / Graph of Thoughts (GoT)
For highly complex reasoning (e.g., solving math puzzles), the agent explores multiple possible plans simultaneously (branches), evaluates which branch looks most promising, and explores further down that path, backtracking if a branch fails.

### 2. Memory Architectures

Because LLMs are stateless functions, memory must be managed externally by the orchestrator application.

#### A. Short-Term Memory (Context Window Management)
This is simply the list of messages (`user`, `assistant`, `tool`) passed to the API. 
*   **Challenge:** As the task progresses, the context grows until it hits the model's limit (e.g., 128k tokens) or becomes too noisy, degrading the LLM's reasoning.
*   **Solution:** **Summarization**. When the context hits a threshold, a secondary LLM call summarizes the older messages into a compact paragraph (e.g., \"The agent previously searched the DB and found the user's IP.\") and replaces the old messages with this summary.

#### B. Long-Term Memory (Vector Databases)
To remember things across different sessions (days or weeks later), we use Retrieval-Augmented Generation (RAG) paradigms as memory.
1.  **Write:** When the agent learns an important fact (e.g., \"User prefers Python over Java\"), it generates a text embedding of this fact and stores it in a Vector Database (like Pinecone, Milvus, or Chroma).
2.  **Read:** When the user asks a new question, the system embeds the prompt, does a similarity search in the Vector DB, and injects relevant past memories into the system prompt before calling the LLM.

---

## Advanced Concepts & Internal Details

### Self-Reflection and Correction
A critical part of advanced planning is the ability to replan. If step 2 of a plan fails repeatedly (e.g., an API is down), a rigid executor will crash. Advanced agents include a \"Reflection\" step: the agent analyzes the failure, recognizes the plan is blocked, and generates a *new* plan to route around the obstacle.

### Episodic vs. Semantic Memory
Borrowing from human psychology, advanced AI systems categorize memory:
*   **Episodic:** Remembering specific events sequentially (\"Yesterday, I ran the data pipeline and it failed at 2 PM\"). Often stored as logs or chronological databases.
*   **Semantic:** Generalized facts abstracted from episodes (\"The data pipeline generally struggles with massive CSVs\"). Often stored in Vector DBs or Knowledge Graphs.

---

## Performance and Common Mistakes

*   **Mistake: Infinite Loops.** In ReAct setups, an agent might repeatedly try the same failing tool with the same arguments. 
    *   *Fix:* Implement hard limits on loop iterations (e.g., max 5 steps). Force the LLM to output a `Thought` before an `Action` so it rationalizes *why* it is trying again.
*   **Mistake: Over-planning.** Asking an LLM to plan a 50-step process upfront usually fails because step 40 depends heavily on the exact outcome of step 3. 
    *   *Fix:* Use hierarchical planning. Plan the next 3 high-level milestones, execute them, and then plan the next batch based on current state.
*   **Performance: Memory Retrieval Latency.** Hitting a vector database on every single user turn adds latency.
    *   *Fix:* Use a lightweight classifier model or a heuristic to determine *if* a memory lookup is even necessary based on the user's prompt.

---

## Realistic Interview Questions

1.  **Question:** Explain the difference between ReAct and Plan-and-Execute architectures. When would you use which?
    *   **Expected Answer:** ReAct interleaves reasoning and action step-by-step; good for dynamic, short tasks. Plan-and-Execute generates a full roadmap first, then executes; better for complex, multi-step goals that require foresight, though it may struggle if early steps yield unexpected results requiring a full replan.
2.  **Question:** Your agent has been running a background research task for 4 hours. It crashes with a `Context Length Exceeded` error. How do you redesign the architecture to prevent this?
    *   **Expected Answer:** Implement context window management. Use a sliding window approach, summarize past tool outputs instead of keeping raw data, or write intermediate findings to a local scratchpad file (using tools) rather than keeping them in the chat history.
3.  **Question:** How would you design a memory system so an agent remembers user preferences across sessions without injecting their entire life history into every prompt?
    *   **Expected Answer:** Discuss Vector Databases. Extract key entities and preferences as background tasks. On a new query, use similarity search to retrieve only the top-K relevant memories and inject those into the system prompt context.

---

## Practical Exercises

1.  **The ReAct Loop:** Write a simple Python loop that forces an LLM to output exactly two JSON keys: `Thought` and `Action`. Parse the Action, execute a dummy function, append the result as `Observation`, and loop until the LLM outputs a special `Final_Answer` action.
2.  **Stateful Planner:** Create an `AgentState` object in Python that contains a list called `plan_steps` and an integer `current_step_index`. Write logic that passes only the *current* step to the executor LLM, updating the state when the executor succeeds.
3.  **Memory Injection:** Use a local embedding model (like `sentence-transformers`) and a lightweight vector store (like `faiss`). Hardcode 5 facts about a fictional user into the store. Write a script that takes a user question, searches the store, and builds a prompt that includes \"Relevant context from memory: ...\" before sending it to the LLM.
