# Inference Optimization

## Prerequisites
- Understanding of LLM inference architecture (Prefill vs. Decode phases).
- Knowledge of the KV Cache concept.
- Familiarity with performance metrics: Time to First Token (TTFT), Inter-Token Latency (ITL), and Throughput.

## Objectives
- Master techniques for optimizing LLM inference speed and resource utilization.
- Deep dive into KV Cache optimization techniques (Quantization, GQA).
- Understand the mechanics and benefits of Speculative Decoding.
- Learn about model quantization strategies for inference (AWQ, GPTQ).

## Intuition
As LLMs grow in size, running them efficiently becomes a massive engineering challenge. The inference process is predominantly limited by memory bandwidth during the decoding phase. To make inference faster and cheaper, we must reduce the amount of data moved from VRAM to compute cores and reduce the latency of generating sequential tokens. 
Optimizations broadly fall into two categories:
1. **Memory Optimizations**: Reducing the size of weights and KV cache (Quantization, Grouped Query Attention).
2. **Latency Optimizations**: Accelerating the sequential decoding process (Speculative Decoding).

## Architecture & Core Concepts

### 1. Deep Dive: KV Caching & Its Bottlenecks
The KV cache stores the Key and Value states for every token generated or processed. 
Size calculation per token: `2 (K and V) * num_layers * hidden_size * bytes_per_param`.
For a 70B model, processing a 32K context length for a single request can consume over 10GB of VRAM just for the KV cache.
**Optimizations**:
- **Grouped Query Attention (GQA)**: Architectural change where multiple query heads share a single KV head, drastically reducing the KV cache size by a factor of 4x to 8x.
- **KV Cache Quantization**: Storing the KV cache in FP8 or INT8 instead of FP16, halving the memory footprint and doubling the memory bandwidth efficiency.

### 2. Speculative Decoding
LLM generation is autoregressive (token $i$ requires token $i-1$), making it strictly sequential and memory-bandwidth bound.
**Speculative Decoding** breaks this sequential bottleneck using a small, fast "draft" model alongside the large "target" model.
1. **Drafting**: The small draft model rapidly generates a sequence of $K$ "guess" tokens.
2. **Verification**: The large target model processes all $K$ guess tokens in a single parallel forward pass (similar to the prefill phase). 
3. **Acceptance**: The target model evaluates the probabilities of the drafted tokens. If they match the target model's distribution, they are accepted. If a token is rejected, the target model corrects it, discards subsequent drafted tokens, and the process repeats.

Since checking tokens in parallel is much faster than generating them sequentially on the large model, this technique can provide 2x-3x speedups without degrading the output quality (it guarantees the exact same output distribution as the target model).

### 3. Weight Quantization (GPTQ, AWQ)
Quantization reduces the precision of model weights from 16-bit floats to 8-bit or 4-bit integers.
- **GPTQ (Post-Training Quantization)**: Uses a calibration dataset to quantize weights in a way that minimizes the output error. Good for 4-bit quantization.
- **AWQ (Activation-aware Weight Quantization)**: Observes activations during a calibration phase and protects the most "salient" (important) weights from quantization (keeping them in FP16), quantizing the rest to 4-bit. Often yields better accuracy than GPTQ.

## Code Examples

### Enabling KV Cache Quantization in vLLM
```python
from vllm import LLM, SamplingParams

# Initialize vLLM with FP8 KV cache to save memory
llm = LLM(
    model="meta-llama/Llama-2-7b-hf",
    kv_cache_dtype="fp8" # Compresses KV cache to 8-bit
)

prompts = ["Explain quantum computing in simple terms."]
sampling_params = SamplingParams(max_tokens=200)
outputs = llm.generate(prompts, sampling_params)
print(outputs[0].outputs[0].text)
```

### Speculative Decoding with Hugging Face Transformers
```python
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

device = "cuda" if torch.cuda.is_available() else "cpu"

# 1. Load Target Model (Large, Slow)
target_model_name = "meta-llama/Llama-2-13b-chat-hf"
target_model = AutoModelForCausalLM.from_pretrained(target_model_name, torch_dtype=torch.float16).to(device)

# 2. Load Draft Model (Small, Fast)
draft_model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
draft_model = AutoModelForCausalLM.from_pretrained(draft_model_name, torch_dtype=torch.float16).to(device)

tokenizer = AutoTokenizer.from_pretrained(target_model_name)
prompt = "The history of the Roman Empire is characterized by"
inputs = tokenizer(prompt, return_tensors="pt").to(device)

# 3. Generate with Speculative Decoding (assisted_generation)
outputs = target_model.generate(
    **inputs,
    max_new_tokens=100,
    assistant_model=draft_model, # Enables speculative decoding
    do_sample=True,
    temperature=0.7
)

print(tokenizer.decode(outputs[0], skip_special_tokens=True))
```

## Interview Questions
1. **Explain the mechanism of Speculative Decoding. Does it change the output of the model?**
   *Answer Hint*: It uses a small draft model to guess $K$ tokens, and the large target model verifies them in parallel. It does NOT change the output distribution; if implemented correctly, the output is mathematically identical to using the target model alone (lossless).
2. **What is the difference between Multi-Head Attention (MHA), Multi-Query Attention (MQA), and Grouped Query Attention (GQA)?**
   *Answer Hint*: MHA has a K and V head for every Q head. MQA has a single K and V head shared across all Q heads. GQA is the middle ground, where groups of Q heads share a single K and V head. MQA and GQA significantly reduce KV cache memory.
3. **When would Speculative Decoding fail to provide a speedup?**
   *Answer Hint*: If the draft model is too inaccurate (high rejection rate) or too slow, the overhead of drafting and verifying will outweigh the benefits. It also provides less benefit when the system is heavily batched and compute-bound rather than memory-bandwidth bound.
4. **Why do we quantize the KV cache?**
   *Answer Hint*: To increase the maximum batch size and sequence length that can fit into GPU VRAM, and to reduce the memory bandwidth required to read the KV cache during the decode phase, thereby increasing tokens/second.
