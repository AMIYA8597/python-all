# 🏆 Master Capability Test & Diagnostic System

This is your final diagnostic system. To genuinely consider yourself **Production-Ready**, you must be able to complete this test *without* copying from documentation or LLMs. 

Use this as a checklist for your active recall sessions.

---

## 🟢 PHASE 1: Python & DSA
- [ ] **1. Write Python without copying:** Can you write a generator function that yields Fibonacci numbers, using proper type hints?
- [ ] **2. Solve basic DSA:** Can you implement a Thread-safe LRU Cache from memory using a Doubly Linked List and a Hash Map?
- [ ] **3. Complexity Analysis:** Can you explain why `O(N log N)` is the lower bound for comparison-based sorting, and how Radix sort bypasses this?

## 🟡 PHASE 2: Data & SQL
- [ ] **4. Query databases:** Write a SQL query using a CTE and a Window Function (e.g., `RANK() OVER`) to find the top 3 highest-paid employees per department.
- [ ] **5. Analyze datasets:** Explain how you would identify and handle data leakage in a time-series dataset.
- [ ] **6. Use NumPy:** Can you broadcast a 1D array across a 2D matrix without writing a `for` loop?
- [ ] **7. Use Pandas:** How do you perform a left join handling missing values using `merge` and `fillna`?
- [ ] **8. Visualize data:** Explain the statistical difference between a Box Plot and a Violin Plot.
- [ ] **9. Explain statistics:** Explain the p-value in an A/B test to a non-technical product manager.

## 🟠 PHASE 3: Machine Learning & Deep Learning
- [ ] **10. Train ML models:** Write pseudo-code for a scikit-learn Pipeline that imputes missing data, scales features, and trains a RandomForest.
- [ ] **11. Evaluate ML models:** When would you prioritize PR-AUC over ROC-AUC in a classification problem?
- [ ] **12. Explain Neural Networks:** Draw the computational graph of a single perceptron and explain how the chain rule updates the weights during backpropagation.
- [ ] **13. Use PyTorch:** Implement a simple PyTorch `nn.Module` with one Linear layer, one ReLU, and a dropout layer.
- [ ] **14. Explain Transformers:** Explain the purpose of Query, Key, and Value matrices in Self-Attention.

## 🔴 PHASE 4: Generative AI & RAG
- [ ] **15. Explain LLMs:** Explain what "next token prediction" means mathematically (Logits → Softmax → Sampling with Temperature).
- [ ] **16. Use embeddings:** Explain the difference between dense embeddings (e.g., OpenAI `text-embedding-3`) and sparse retrieval (BM25).
- [ ] **17. Build vector search:** How does Hierarchical Navigable Small World (HNSW) make vector search fast in a Vector DB?
- [ ] **18. Build RAG:** Draw the architecture of a standard RAG pipeline.
- [ ] **19. Evaluate RAG:** How do you mathematically evaluate if your RAG context retrieval is actually relevant to the user's query?

## 🟣 PHASE 5: Agentic AI
- [ ] **20. Use tools/function calling:** Write a JSON schema representing a tool that an LLM can call to fetch the weather.
- [ ] **21. Build an AI agent:** Explain the ReAct (Reasoning and Acting) loop. What is the state machine doing?
- [ ] **22. Evaluate an agent:** How do you test if an agent is stuck in an infinite loop?
- [ ] **23. Secure an agent:** What is Prompt Injection, and how do you sandbox an agent's code-execution tool to prevent it from deleting your database?

## 🟤 PHASE 6: MLOps & System Design
- [ ] **24. Deploy an AI application:** Explain how to wrap an ML model inference function in a FastAPI endpoint.
- [ ] **25. Monitor an AI system:** What is Data Drift vs Concept Drift? How do you monitor it in production?
- [ ] **26. Design a production AI architecture:** Design a system that ingests 10,000 PDF documents a day, chunks them, embeds them, and serves them to a highly concurrent GenAI chatbot.
- [ ] **27. Explain projects in interviews:** Use the STAR method (Situation, Task, Action, Result) to explain the hardest bug you fixed in your Capstone Project.

---

*If you can check every box confidently, you are ready for a Senior AI/ML Engineering role.*
