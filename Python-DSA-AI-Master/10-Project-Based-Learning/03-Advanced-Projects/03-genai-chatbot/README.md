# Project: Generative AI Chatbot Integration

## 1. Project Overview

### What is this project?
In this advanced project, you will build a sophisticated Generative AI chatbot from scratch using Python. Rather than just making simple API calls, this project focuses on building a production-ready conversational agent. It includes maintaining conversational state (memory), handling streaming responses for low latency, implementing system prompts (personas), and integrating RAG (Retrieval-Augmented Generation) concepts for providing the LLM with custom context.

### Why does it exist?
Generative AI (Large Language Models like GPT-4, Claude, Gemini) is transforming software engineering. However, building reliable applications on top of LLMs requires more than a single prompt. Developers must handle:
- **Context Windows & Memory Management:** LLMs are stateless. You must pass the conversation history in every API call, but without exceeding token limits.
- **Structured Output:** Forcing the LLM to reply in a parseable format (like JSON) to integrate with backend systems.
- **RAG (Retrieval-Augmented Generation):** Connecting LLMs to private databases or documents so they don't hallucinate facts.

### Industry Use Cases
- **Customer Support Agents:** Automating tier-1 customer support queries by connecting LLMs to company knowledge bases.
- **Internal Knowledge Retrieval:** Building tools for employees to "chat" with their corporate wikis, HR policies, or internal codebase.
- **AI Assistants & Copilots:** Integrating specialized assistants directly into existing SaaS platforms.

---

## 2. Technical Architecture & Concepts

### The Conversational Loop
A chatbot is essentially a `while True` loop that receives user input, constructs a payload, calls an LLM API, and processes the response.
- **Roles:** LLM APIs differentiate between roles: 
  - `system`: The overarching instructions and persona of the bot.
  - `user`: The human typing messages.
  - `assistant`: The LLM's previous replies.

### Memory Systems
To maintain a conversation, you need a Memory module.
- **Buffer Memory:** Stores the entire history. Simple, but quickly exceeds token limits on long chats.
- **Window Memory:** Stores only the last $N$ turns (e.g., last 5 messages).
- **Summary Memory:** Periodically asks the LLM to summarize older parts of the conversation to save space while retaining context.

### RAG (Retrieval-Augmented Generation) - Overview
If a user asks about proprietary data, the LLM won't know. 
1. **Index:** Convert your custom documents into embeddings (numerical vectors) and store them in a Vector Database (like Chroma, FAISS, or Pinecone).
2. **Retrieve:** When a user asks a question, convert the question to a vector, and perform a similarity search in the database to find relevant document chunks.
3. **Generate:** Inject those relevant chunks into the LLM prompt alongside the user's question, instructing the LLM to answer *based on the provided context*.

---

## 3. Implementation Steps

1. **Phase 1: Basic API Integration:**
   Set up your environment with the `openai`, `google-generativeai`, or `anthropic` SDK. Create a simple script that sends a prompt and prints the response.
2. **Phase 2: The Conversational Class & Memory:**
   Create a `Chatbot` class. Implement a `ConversationHistory` object that stores `{"role": ..., "content": ...}` dictionaries. Ensure the class passes this history on every interaction.
3. **Phase 3: System Prompts & Guardrails:**
   Inject a strong system prompt to define a specific persona (e.g., "You are a senior database engineer"). Add validation logic to catch and reject inappropriate inputs before they hit the API.
4. **Phase 4: Streaming & UX:**
   Modify the API call to request a stream. Iterate over the stream chunks and print them to the console in real-time, simulating typing. This drastically reduces perceived latency.

---

## 4. Advanced Concepts & Best Practices

- **Token Counting:** Use libraries like `tiktoken` to accurately count tokens in your prompt before sending them, avoiding unexpected API errors or cost overruns.
- **Rate Limiting & Retries:** Network calls fail. LLM APIs often rate-limit. Implement robust exponential backoff retries using libraries like `tenacity`.
- **Function Calling / Tools:** Advanced usage involves giving the LLM descriptions of Python functions you have written (e.g., `get_weather(location)`). The LLM can then choose to "call" that function, returning a structured JSON requesting you to execute the code and return the result to it.

---

## 5. Realistic Interview Questions

1. **Architecture:** "How would you handle user session memory in a highly concurrent web application serving thousands of chatbot users?" (Answer: Use a distributed cache like Redis to store conversation histories, keyed by Session ID, rather than in-memory Python variables).
2. **RAG:** "What are the common failure modes of a RAG system and how do you mitigate them?" (Answer: Bad retrieval quality. Mitigation includes better chunking strategies, hybrid search (keyword + semantic), and re-ranking models).
3. **Prompt Engineering:** "How do you prevent Prompt Injection attacks where a user tries to override your system prompt to make the bot say bad things?"

---

## 6. Practical Exercises

- **Exercise 1:** Modify the chatbot to stream responses character by character in the terminal.
- **Exercise 2:** Implement a rudimentary "Tool": allow the user to type "What time is it?", intercept this, execute Python's `datetime`, and pass that as context to the LLM.
- **Exercise 3:** Build a simple Streamlit UI or Gradio interface over your Python class so you can interact with it via a web browser.
