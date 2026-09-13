# LLM Deployment

## Prerequisites
- Basic understanding of Large Language Models (LLMs) and Transformer architecture.
- Familiarity with deep learning concepts and Python programming.
- Understanding of basic deployment concepts (REST APIs, Docker, GPU instances).

## Objectives
- Understand the challenges in deploying Large Language Models for inference.
- Learn about Continuous Batching and its role in maximizing GPU utilization.
- Explore memory management techniques like PagedAttention and KV Caching.
- Gain practical knowledge of prominent deployment frameworks: vLLM and Hugging Face Text Generation Inference (TGI).

## Intuition
Deploying LLMs is not like deploying traditional machine learning models or web applications. LLMs are massive (often tens or hundreds of gigabytes) and generate output token by token in an autoregressive manner. The primary bottleneck in LLM inference is usually memory bandwidth, not just compute. 
To serve many users efficiently, we need systems that can batch requests together. However, traditional static batching fails because different requests take different amounts of time to complete. We need dynamic systems that can manage memory efficiently and stream tokens as they are generated.

## Architecture & Core Concepts

### 1. The KV Cache
During autoregressive generation, a transformer predicts the next token based on all previous tokens. Recomputing the Key (K) and Value (V) vectors for all previous tokens at every step is computationally expensive. 
**KV Caching** stores these vectors for past tokens. When generating the next token, the model only computes the K and V for the newly generated token and appends them to the cache. This turns an $O(N^2)$ operation into an $O(N)$ operation for generation, but it consumes a massive amount of GPU memory.

### 2. PagedAttention
Proposed by the creators of vLLM, PagedAttention solves the memory fragmentation issue of the KV Cache.
Traditional KV caches allocate contiguous memory blocks for the maximum possible sequence length, leading to massive internal fragmentation (wasted memory) because most requests don't use their full allocated length.
PagedAttention maps continuous logical blocks (representing sequences of tokens) to non-continuous physical blocks in GPU memory, much like virtual memory paging in operating systems. This allows for near-zero waste and enables efficient memory sharing (e.g., in beam search or parallel sampling).

### 3. Continuous Batching (Iteration-Level Scheduling)
Traditional batching waits for a set of requests to finish before processing the next batch. In LLMs, a batch finishes only when the longest sequence completes, wasting GPU cycles on early-finished sequences.
Continuous Batching (or Orca-style batching) schedules requests at the *iteration level* (token level). When a request finishes generating, its slot in the batch is immediately filled with a waiting request. This dramatically increases throughput.

### 4. Frameworks: vLLM vs TGI
- **vLLM**: An open-source library focused on high throughput and memory efficiency, pioneering PagedAttention. Great for serving models with high concurrency.
- **TGI (Text Generation Inference)**: Developed by Hugging Face, optimized for deployment in production with features like tensor parallelism, continuous batching, and native support for many HF models.

## Code Examples

### Serving a model using vLLM (Python API)
```python
from vllm import LLM, SamplingParams

# 1. Initialize the LLM (downloads and loads the model into GPU memory)
llm = LLM(model="facebook/opt-125m")

# 2. Define sampling parameters
sampling_params = SamplingParams(temperature=0.8, top_p=0.95, max_tokens=100)

# 3. Define prompts
prompts = [
    "Hello, my name is",
    "The capital of France is",
    "The future of AI is"
]

# 4. Generate outputs (vLLM automatically handles batching and memory)
outputs = llm.generate(prompts, sampling_params)

# 5. Print results
for output in outputs:
    prompt = output.prompt
    generated_text = output.outputs[0].text
    print(f"Prompt: {prompt!r}, Generated text: {generated_text!r}")
```

### Launching an API server using vLLM
```bash
# Launch a scalable OpenAI-compatible API server
python -m vllm.entrypoints.openai.api_server \
    --model meta-llama/Llama-2-7b-chat-hf \
    --dtype bfloat16 \
    --max-model-len 2048 \
    --gpu-memory-utilization 0.9
```

### Launching TGI using Docker
```bash
# Launch TGI on port 8080 with 1 GPU
docker run --gpus all --shm-size 1g -p 8080:80 \
  -v $PWD/data:/data \
  ghcr.io/huggingface/text-generation-inference:latest \
  --model-id mistralai/Mistral-7B-Instruct-v0.2
```

## Interview Questions
1. **Explain the difference between compute-bound and memory-bandwidth-bound operations in LLM inference.**
   *Answer Hint*: Prefill phase (processing the prompt) is typically compute-bound (dense matrix multiplications). Decode phase (generating tokens one by one) is memory-bandwidth-bound because weights and KV cache must be loaded from memory to compute for a single token.
2. **What problem does PagedAttention solve?**
   *Answer Hint*: It solves memory fragmentation in the KV cache by dividing it into blocks that are mapped dynamically, similar to OS virtual memory, allowing batch sizes to increase significantly.
3. **How does Continuous Batching improve throughput compared to static batching?**
   *Answer Hint*: Static batching waits for the longest request in a batch to finish. Continuous batching evicts completed requests and inserts new ones at every token generation step, keeping GPU utilization consistently high.
4. **Why is the KV Cache size a limiting factor for LLM deployment?**
   *Answer Hint*: The KV Cache grows with the batch size and sequence length. For large contexts and high concurrency, the KV cache can easily exceed the size of the model weights themselves, running out of GPU VRAM.
