# LLM Observability

## Prerequisites
- Familiarity with deploying LLMs and building LLM applications (e.g., using LangChain or LlamaIndex).
- Understanding of traditional software observability concepts (Logging, Metrics, Tracing).

## Objectives
- Understand the unique observability challenges introduced by LLMs.
- Learn how to trace complex LLM chains and agentic workflows.
- Track critical metrics like token usage, cost, and latency (TTFT, ITL).
- Implement observability using tools like LangSmith, Phoenix, or OpenTelemetry.

## Intuition
Traditional application monitoring focuses on CPU usage, memory, HTTP latency, and database query times. While these still matter, LLM applications introduce non-deterministic outputs, complex multi-step reasoning (agents), and token-based pricing models.
When an LLM application fails or responds slowly, you need to know: Was it the vector database retrieval? Did the prompt get truncated? Did the LLM hallucinate? Did we hit a rate limit? 
LLM Observability solves this by capturing detailed traces of prompts, completions, tool calls, and measuring token counts and latency metrics for every step.

## Architecture & Core Concepts

### 1. Tracing LLM Calls
A **Trace** represents a single end-to-end execution of your application (e.g., a user asking a question). A trace is composed of **Spans**, which represent individual operations within the trace (e.g., embedding generation, vector DB retrieval, LLM generation).
By tracing, you can visualize the exact prompt sent to the LLM, the raw output received, and the time taken for each sub-component.

### 2. Key LLM Metrics
- **Time to First Token (TTFT)**: Crucial for streaming user experiences. Measures the time from request submission to the first generated token.
- **Inter-Token Latency (ITL)**: The average time between generated tokens. Affects reading speed.
- **Token Count & Cost**: Tracking prompt tokens and completion tokens to calculate the dollar cost per request.
- **User Feedback / Quality Metrics**: Capturing user upvotes/downvotes or using "LLM-as-a-judge" to score outputs for relevance, toxicity, or hallucination.

### 3. OpenTelemetry vs. Purpose-Built Tools
- **OpenTelemetry (OTel)**: An open standard for observability. You can instrument LLM apps using libraries like `openinference` and send data to generic backends (Datadog, Grafana).
- **Purpose-Built Tools (LangSmith, Phoenix, Langfuse, Weights & Biases)**: Platforms designed specifically for AI. They provide dedicated UIs for viewing prompt inputs/outputs, debugging chains, and curating datasets for fine-tuning.

## Code Examples

### 1. Tracing with Arize Phoenix (Open Source, Local)
Phoenix is a great tool for local observability and debugging.

```python
import phoenix as px
from openinference.instrumentation.openai import OpenAIInstrumentor
from openai import OpenAI

# 1. Launch the Phoenix UI locally
session = px.launch_app()

# 2. Instrument the OpenAI client to capture traces automatically
OpenAIInstrumentor().instrument()

# 3. Make standard OpenAI calls
client = OpenAI()
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Explain observability in 3 sentences."}],
)

print(response.choices[0].message.content)
# View the trace in the Phoenix UI at http://localhost:6006
print(f"View traces at: {session.url}")
```

### 2. Tracing a LangChain Application with LangSmith
LangSmith is deeply integrated with LangChain.

```bash
# Set environment variables for LangSmith
export LANGCHAIN_TRACING_V2="true"
export LANGCHAIN_API_KEY="your_langsmith_api_key"
export LANGCHAIN_PROJECT="llmops-curriculum"
```

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# By simply having the environment variables set, 
# this entire chain will be traced in LangSmith!
llm = ChatOpenAI(model="gpt-4o-mini")
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("user", "What are the core metrics for LLM observability?")
])

chain = prompt | llm | StrOutputParser()

# Execute the chain
result = chain.invoke({})
print(result)
# Navigate to smith.langchain.com to see the execution graph, latency, and tokens.
```

## Interview Questions
1. **What is the difference between TTFT (Time to First Token) and ITL (Inter-Token Latency)? Why do they matter?**
   *Answer Hint*: TTFT measures responsiveness (time to start streaming), while ITL measures the speed of generation. High TTFT feels like the app is hanging, while high ITL makes the text generate too slowly to read.
2. **How would you debug a RAG (Retrieval-Augmented Generation) application that is providing incorrect answers?**
   *Answer Hint*: Use a tracing tool to inspect the spans. First, check the "Retrieval" span to see if the correct documents were fetched. If yes, check the "LLM" span to see the exact prompt constructed and if the LLM hallucinated despite having the right context.
3. **What is OpenInference?**
   *Answer Hint*: It's an open standard (built on top of OpenTelemetry) for capturing traces and metrics specifically for LLM applications, allowing you to avoid vendor lock-in with observability platforms.
4. **How do you monitor the cost of an LLM application in production?**
   *Answer Hint*: By extracting the `prompt_tokens` and `completion_tokens` from the LLM API responses (often found in the `usage` metadata), multiplying them by the model's pricing rates, and aggregating these metrics in an observability dashboard.
