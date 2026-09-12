"""
Module: 06-deployment
Description: A textbook-grade, massive interactive lesson on deploying Large Language Models (LLMs) and Generative AI applications.

Learning Objectives:
1. Understand the theoretical and mathematical foundations of LLM serving (Memory bandwidth, compute-bound vs memory-bound).
2. Learn the techniques for optimizing LLM deployment: KV Caching, Continuous Batching, PagedAttention, and Quantization.
3. Master the architecture of a high-performance Python deployment server (FastAPI, Asyncio, Streaming responses).
4. Analyze the Big-O complexity of transformer inference (Time and Space).
5. Implement a robust simulated inference engine mimicking vLLM/TensorRT-LLM principles.

===========================================================================
MATHEMATICAL BACKGROUND & BIG-O ANALYSIS
===========================================================================
When deploying LLMs, the primary bottlenecks are Memory Bandwidth and GPU VRAM capacity.

1. Memory Requirements for Model Weights
For a model with P parameters and precision bytes (B), the VRAM for weights is:
    VRAM_weights = P * B
For a 7B parameter model in FP16 (2 bytes per parameter):
    7 * 10^9 * 2 = 14 GB.
With quantization (e.g., INT4/AWQ), this drops to 3.5 GB.

2. KV Cache Memory (Space Complexity)
In decoder-only transformers, past Keys and Values must be cached for autoregressive generation.
Space per token = 2 * (Num_Layers) * (Hidden_Size) * (Bytes_Per_Param)
Total KV Cache Space = Space per token * (Batch_Size) * (Sequence_Length)
Big-O Space: O(N * B * L * H), where N=seq_len, B=batch, L=layers, H=hidden

3. Computational Complexity (Time Complexity)
Prefill Phase (Processing the prompt):
    - Compute-bound. Matrix multiplications dominate.
    - Self-attention takes O(N^2 * d) time per layer.
Decode Phase (Generating tokens):
    - Memory-bound. Generating one token at a time.
    - Matrix vector multiplications.
    - Self-attention takes O(N * d) time per layer.

===========================================================================
ADVANCED DEPLOYMENT CONCEPTS
===========================================================================
- **Continuous Batching (Orca/vLLM):** Iteration-level scheduling. Instead of waiting for the longest request in a batch to finish, finished requests are evicted and new ones are swapped in at every step.
- **PagedAttention (vLLM):** Managing KV cache in non-contiguous memory blocks, reducing fragmentation from ~60% down to <4%.
- **Quantization:** GPTQ, AWQ, EXL2 (reducing precision from FP16 to INT8/INT4).
- **Speculative Decoding:** Using a small draft model to generate tokens quickly, then verifying with the large model.
"""

import asyncio
import time
import math
import logging
import random
from dataclasses import dataclass, field
from typing import List, Dict, Any, AsyncGenerator

# Setting up logging for our deployment engine
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("LLM_Deployment")

# ============================================================================
# Core Data Structures for LLM Serving
# ============================================================================

@dataclass
class GenerationRequest:
    """
    Represents an incoming request to the LLM inference server.
    """
    request_id: str
    prompt: str
    max_new_tokens: int = 50
    temperature: float = 1.0
    top_p: float = 0.9
    created_at: float = field(default_factory=time.time)

@dataclass
class GenerationResult:
    """
    Represents the final output of an LLM generation.
    """
    request_id: str
    generated_text: str
    prompt_tokens: int
    completion_tokens: int
    total_time_ms: float
    tokens_per_second: float

# ============================================================================
# Memory Management: Simulating PagedAttention
# ============================================================================

class KVCacheManager:
    """
    Simulates a memory manager for the KV Cache inspired by PagedAttention.
    Instead of pre-allocating contiguous memory for the maximum possible sequence length,
    we allocate blocks of memory (pages).
    
    Time Complexity:
        Allocate: O(1)
        Free: O(1)
    Space Complexity:
        O(Total Blocks)
    """
    def __init__(self, total_blocks: int, block_size: int = 16):
        self.total_blocks = total_blocks
        self.block_size = block_size
        # Track available blocks (in a real system, this manages GPU pointers)
        self.free_blocks: List[int] = list(range(total_blocks))
        self.allocated_blocks: Dict[str, List[int]] = {}
        
    def allocate(self, request_id: str, num_tokens: int) -> bool:
        """
        Allocates blocks for a given number of tokens.
        Returns True if successful, False if out of memory (OOM).
        """
        blocks_needed = math.ceil(num_tokens / self.block_size)
        
        if request_id in self.allocated_blocks:
            current_blocks = len(self.allocated_blocks[request_id])
            if blocks_needed <= current_blocks:
                return True
            blocks_needed -= current_blocks
            
        if len(self.free_blocks) < blocks_needed:
            logger.warning(f"OOM: Not enough KV cache blocks for request {request_id}")
            return False
            
        new_blocks = [self.free_blocks.pop() for _ in range(blocks_needed)]
        if request_id not in self.allocated_blocks:
            self.allocated_blocks[request_id] = []
        self.allocated_blocks[request_id].extend(new_blocks)
        return True
        
    def free(self, request_id: str) -> None:
        """Frees all blocks associated with a request."""
        if request_id in self.allocated_blocks:
            blocks = self.allocated_blocks.pop(request_id)
            self.free_blocks.extend(blocks)
            logger.debug(f"Freed {len(blocks)} blocks for request {request_id}. Total free: {len(self.free_blocks)}")

# ============================================================================
# Inference Engine: Simulating Continuous Batching
# ============================================================================

class LLMInferenceEngine:
    """
    Simulates a high-performance LLM inference engine with Continuous Batching.
    
    In a standard batching setup, we wait for all requests in a batch to finish
    before starting the next batch. In continuous batching, we process requests
    at the iteration (token) level.
    """
    def __init__(self, max_batch_size: int = 4, cache_blocks: int = 100):
        self.max_batch_size = max_batch_size
        self.kv_cache = KVCacheManager(total_blocks=cache_blocks)
        self.waiting_queue: asyncio.Queue[GenerationRequest] = asyncio.Queue()
        self.running_requests: Dict[str, Dict[str, Any]] = {}
        self._is_running = False
        
        # Tokenizer simulation mappings
        self.vocab = [" The", " quick", " brown", " fox", " jumps", " over", " the", " lazy", " dog", ".",
                      " AI", " is", " transforming", " the", " world", " of", " software", " engineering", "!",
                      " Here", " are", " some", " details", " about", " deployment", " and", " scaling", " models"]
        
    def _tokenize(self, text: str) -> int:
        """Simulate tokenization by returning an estimated token count."""
        return max(1, len(text.split()) + 2)
        
    def _generate_token(self) -> str:
        """Simulate generating a single token."""
        # Simulated compute time for decode phase (memory bound)
        # O(1) simulation, real world is O(N * d)
        return random.choice(self.vocab)
        
    async def add_request(self, request: GenerationRequest) -> None:
        """Enqueue a new request."""
        await self.waiting_queue.put(request)
        logger.info(f"Enqueued request {request.request_id} (Prompt: '{request.prompt[:20]}...')")
        
    async def run_loop(self) -> None:
        """
        The main Continuous Batching loop.
        It pulls requests from the waiting queue, runs prefill, and generates tokens step-by-step.
        """
        self._is_running = True
        logger.info("Starting LLM Inference Engine loop...")
        
        while self._is_running:
            # 1. Schedule new requests if we have capacity
            while len(self.running_requests) < self.max_batch_size and not self.waiting_queue.empty():
                try:
                    # Non-blocking get
                    req = self.waiting_queue.get_nowait()
                    prompt_len = self._tokenize(req.prompt)
                    
                    # Try allocating KV Cache for the prompt
                    if self.kv_cache.allocate(req.request_id, prompt_len):
                        self.running_requests[req.request_id] = {
                            "request": req,
                            "generated_tokens": [],
                            "prompt_tokens": prompt_len,
                            "start_time": time.time(),
                            "status": "prefill"
                        }
                        logger.info(f"Scheduled request {req.request_id} for prefill.")
                    else:
                        # OOM, put it back
                        # In a real system, we might preempt other requests
                        await self.waiting_queue.put(req)
                        break
                except asyncio.QueueEmpty:
                    break
                    
            if not self.running_requests:
                await asyncio.sleep(0.01) # Idle sleep
                continue
                
            # 2. Execute a single forward pass for all running requests
            # Simulate the forward pass time (batch processing)
            await asyncio.sleep(0.05) # Simulated GPU latency
            
            finished_requests = []
            
            for req_id, state in self.running_requests.items():
                req = state["request"]
                
                if state["status"] == "prefill":
                    # Prefill completed, transition to decode
                    state["status"] = "decode"
                    # Allocate one more token for the first generated token
                    self.kv_cache.allocate(req_id, state["prompt_tokens"] + 1)
                elif state["status"] == "decode":
                    # Generate one token
                    new_token = self._generate_token()
                    state["generated_tokens"].append(new_token)
                    
                    current_len = state["prompt_tokens"] + len(state["generated_tokens"])
                    # Allocate space for next token in KV cache
                    if not self.kv_cache.allocate(req_id, current_len + 1):
                        logger.warning(f"OOM during decode for {req_id}. Truncating early.")
                        finished_requests.append(req_id)
                        continue
                        
                    # Check stopping conditions
                    if len(state["generated_tokens"]) >= req.max_new_tokens or new_token.strip() == ".":
                        finished_requests.append(req_id)
                        
            # 3. Handle finished requests
            for req_id in finished_requests:
                state = self.running_requests.pop(req_id)
                self.kv_cache.free(req_id)
                
                req = state["request"]
                total_time = (time.time() - state["start_time"]) * 1000 # ms
                comp_tokens = len(state["generated_tokens"])
                tps = comp_tokens / (total_time / 1000) if total_time > 0 else 0
                
                result = GenerationResult(
                    request_id=req_id,
                    generated_text="".join(state["generated_tokens"]),
                    prompt_tokens=state["prompt_tokens"],
                    completion_tokens=comp_tokens,
                    total_time_ms=total_time,
                    tokens_per_second=tps
                )
                # In a real async server, we would resolve a Future here.
                # For simulation, we just log it.
                logger.info(f"Finished {req_id}: {comp_tokens} tokens in {total_time:.1f}ms ({tps:.1f} t/s). Output: '{result.generated_text}'")
                
    def stop(self) -> None:
        self._is_running = False

# ============================================================================
# Real-World Scenario: Async API Server Simulation
# ============================================================================

async def simulate_api_server() -> None:
    """
    Simulates handling multiple concurrent incoming API requests for LLM generation.
    Demonstrates why Continuous Batching and Async IO are critical for high throughput.
    """
    logger.info("--- Starting Async API Server Simulation ---")
    
    engine = LLMInferenceEngine(max_batch_size=3, cache_blocks=50)
    
    # Start the continuous batching loop in the background
    loop_task = asyncio.create_task(engine.run_loop())
    
    # Simulate a burst of incoming requests
    requests_data = [
        ("Explain quantum computing in simple terms.", 10),
        ("Write a Python script for a binary search tree.", 15),
        ("What is the capital of France?", 5),
        ("Summarize the history of AI.", 20),
        ("Translate 'Hello World' to Spanish.", 8)
    ]
    
    # Dispatch requests asynchronously
    for i, (prompt, max_tokens) in enumerate(requests_data):
        req = GenerationRequest(
            request_id=f"req-{i+1:03d}",
            prompt=prompt,
            max_new_tokens=max_tokens
        )
        await engine.add_request(req)
        # Small delay between incoming requests
        await asyncio.sleep(0.1)
        
    # Wait for all requests to be processed
    # In a real app, we'd wait on Future objects returned by add_request
    while not engine.waiting_queue.empty() or len(engine.running_requests) > 0:
        await asyncio.sleep(0.5)
        
    engine.stop()
    await loop_task
    logger.info("--- API Server Simulation Completed ---\n")

# ============================================================================
# Advanced Streaming Output Simulation
# ============================================================================

async def stream_llm_response(prompt: str) -> AsyncGenerator[str, None]:
    """
    Simulates Server-Sent Events (SSE) streaming of LLM output.
    Streaming is vital for UX in Chatbots, reducing Time-To-First-Token (TTFT).
    
    Yields:
        str: Next generated token
    """
    logger.info(f"--- Streaming response for prompt: '{prompt}' ---")
    
    # Simulate Prefill Time
    await asyncio.sleep(0.2)
    
    vocab = [" streaming", " responses", " significantly", " improves", " the", " user", " experience", " by", " reducing", " TTFT", "."]
    
    for token in vocab:
        # Simulate decode latency per token
        await asyncio.sleep(0.05)
        yield token
        
# ============================================================================
# Big-O and Parameter Calculation Utilities
# ============================================================================

def calculate_vram_requirements(parameters_billions: float, quantization_bits: int, 
                                batch_size: int, seq_len: int, num_layers: int, 
                                hidden_size: int) -> Dict[str, float]:
    """
    Calculates the theoretical VRAM requirements for model weights and KV cache.
    
    Args:
        parameters_billions: e.g., 7.0 for a 7B model
        quantization_bits: 16 for FP16, 8 for INT8, 4 for INT4
        batch_size: Current batch size
        seq_len: Sequence length per request
        num_layers: Number of transformer layers
        hidden_size: Hidden dimension size
        
    Returns:
        Dict containing memory requirements in GB
    """
    # 1. Weights Memory
    bytes_per_param = quantization_bits / 8
    weights_vram_gb = (parameters_billions * 1e9 * bytes_per_param) / (1024**3)
    
    # 2. KV Cache Memory
    # 2 (for K and V) * layers * hidden_size * seq_len * batch_size * bytes_per_param
    kv_elements = 2 * num_layers * hidden_size * seq_len * batch_size
    kv_cache_vram_gb = (kv_elements * bytes_per_param) / (1024**3)
    
    return {
        "weights_vram_gb": round(weights_vram_gb, 2),
        "kv_cache_vram_gb": round(kv_cache_vram_gb, 2),
        "total_vram_gb": round(weights_vram_gb + kv_cache_vram_gb, 2)
    }

# ============================================================================
# Main Execution and Testing
# ============================================================================

def run_tests() -> None:
    """
    Test suite for the mathematical calculations and edge cases.
    """
    logger.info("--- Running Tests ---")
    
    # Test Llama-2 7B VRAM calculation at FP16
    res = calculate_vram_requirements(
        parameters_billions=7.0,
        quantization_bits=16, # 2 bytes
        batch_size=1,
        seq_len=2048,
        num_layers=32,
        hidden_size=4096
    )
    
    # 7B * 2B = 14GB ~ 13.04 GiB
    assert 13.0 <= res["weights_vram_gb"] <= 14.0, f"Weights VRAM incorrect: {res['weights_vram_gb']}"
    
    # KV Cache: 2 * 32 * 4096 * 2048 * 1 * 2 = 1,073,741,824 bytes = 1.0 GB
    assert res["kv_cache_vram_gb"] == 1.0, f"KV Cache VRAM incorrect: {res['kv_cache_vram_gb']}"
    
    logger.info("Tests passed successfully.")

async def main_async() -> None:
    """Async entry point for demonstrations."""
    # 1. Demonstrate VRAM Math
    logger.info("--- Calculating VRAM for 7B Model (INT4 Quantization) ---")
    vram_stats = calculate_vram_requirements(
        parameters_billions=7.0,
        quantization_bits=4, # 0.5 bytes per param
        batch_size=16, # High batch size
        seq_len=4096,
        num_layers=32,
        hidden_size=4096
    )
    logger.info(f"VRAM Stats: {vram_stats}\n")
    
    # 2. Run API Simulation with Continuous Batching
    await simulate_api_server()
    
    # 3. Run Streaming Simulation
    print("\nStreaming response:", end="", flush=True)
    async for token in stream_llm_response("What is streaming?"):
        print(token, end="", flush=True)
    print("\n")
    
if __name__ == "__main__":
    print("========== Exploring LLM DEPLOYMENT ==========\n")
    run_tests()
    asyncio.run(main_async())
    print("========== END OF LLM DEPLOYMENT ==========\n")
