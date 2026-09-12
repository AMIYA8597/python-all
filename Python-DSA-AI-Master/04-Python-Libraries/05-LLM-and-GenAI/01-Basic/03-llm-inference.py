"""
Module: 03-llm-inference
Description: Comprehensive textbook-grade lesson on Large Language Model (LLM) Inference.

=============================================================================
LARGE LANGUAGE MODEL (LLM) INFERENCE: A COMPREHENSIVE TEXTBOOK-GRADE LESSON
=============================================================================

Learning Objectives:
1. Understand the core mechanics of how Large Language Models generate text.
2. Implement core components of autoregressive generation: greedy search, top-k sampling, 
   top-p (nucleus) sampling, and temperature scaling.
3. Understand the mathematical foundation of sequence probabilities in Transformers.
4. Grasp the importance and implementation of KV-caching for efficient inference.
5. Analyze Big-O complexity of different decoding strategies and their trade-offs.

-----------------------------------------------------------------------------
1. MATHEMATICAL BACKGROUND
-----------------------------------------------------------------------------
At its core, an LLM is a function that models the probability distribution of a sequence of tokens.
Given a sequence of tokens X = (x_1, x_2, ..., x_n), the probability of the sequence is factorized
using the chain rule of probability:

    P(X) = P(x_1) * P(x_2 | x_1) * P(x_3 | x_1, x_2) * ... * P(x_n | x_1, ..., x_{n-1})

    P(X) = ∏_{i=1}^{n} P(x_i | x_{<i})

During inference, we are typically given a prompt (context) C = (c_1, ..., c_k), and we want to 
generate the most likely continuation Y = (y_1, ..., y_m). We iteratively sample the next token:

    y_t ~ P(y | c_1, ..., c_k, y_1, ..., y_{t-1})

The model outputs logits (raw, unnormalized scores) for each token in the vocabulary. 
These logits are converted into probabilities using the Softmax function:

    Softmax(z_i) = exp(z_i) / Σ_{j} exp(z_j)

Where:
- z_i is the logit for token i
- The denominator sums over the entire vocabulary V.

-----------------------------------------------------------------------------
2. BIG-O COMPLEXITY OF INFERENCE
-----------------------------------------------------------------------------
Time Complexity:
- Without KV Cache: O(N^2 * d) per token, where N is sequence length and d is hidden dimension.
  Generating T tokens takes O(T * (N+T)^2 * d).
- With KV Cache: O(N * d) per token, as we only compute attention for the new token.
  Generating T tokens takes O(T * (N+T) * d).

Space Complexity:
- Without KV Cache: O(N * d) to store the sequence.
- With KV Cache: O(L * H * T_total * D_head), where L is layers, H is heads, T_total is context length.
  This is the primary memory bottleneck in large-scale LLM deployment.

-----------------------------------------------------------------------------
3. DECODING STRATEGIES
-----------------------------------------------------------------------------
- Greedy Search: Pick the token with the absolute highest probability. (Deterministic)
- Temperature Scaling: Divide logits by T before softmax. T < 1 sharpens, T > 1 flattens.
- Top-K Sampling: Keep only the K highest probability tokens and redistribute mass.
- Top-P (Nucleus) Sampling: Keep the smallest set of tokens whose cumulative probability >= P.
"""

import math
import random
import time
from typing import List, Dict, Any, Optional, Tuple, Callable
from dataclasses import dataclass

# =============================================================================
# SIMULATED LLM ENVIRONMENT
# =============================================================================

@dataclass
class Token:
    id: int
    text: str

class MockTokenizer:
    """
    A simulated tokenizer for educational purposes.
    Maps words/characters to integers and back.
    """
    def __init__(self):
        self.vocab = {
            0: "<pad>", 1: "<eos>", 2: "The", 3: "quick", 4: "brown", 
            5: "fox", 6: "jumps", 7: "over", 8: "the", 9: "lazy", 
            10: "dog", 11: ".", 12: "Hello", 13: "world", 14: "AI", 
            15: "is", 16: "fascinating", 17: "and", 18: "powerful"
        }
        self.inverse_vocab = {v: k for k, v in self.vocab.items()}
        
    def encode(self, text: str) -> List[int]:
        """Encodes text to token IDs."""
        tokens = []
        for word in text.replace(".", " .").split():
            if word in self.inverse_vocab:
                tokens.append(self.inverse_vocab[word])
            else:
                # Fallback for unknown words (simplified)
                tokens.append(1) # <eos> as unknown for this mock
        return tokens
        
    def decode(self, token_ids: List[int]) -> str:
        """Decodes token IDs back to text."""
        words = [self.vocab.get(tid, "<unk>") for tid in token_ids]
        # Quick hack to fix punctuation spacing for display
        return " ".join(words).replace(" .", ".")

    @property
    def vocab_size(self) -> int:
        return len(self.vocab)

class MockLLM:
    """
    A mock LLM that generates logits for the next token based on simple rules
    rather than actual neural network computation.
    """
    def __init__(self, vocab_size: int):
        self.vocab_size = vocab_size
        
    def forward(self, input_ids: List[int]) -> List[float]:
        """
        Simulates a forward pass. Returns logits for the next token.
        Time Complexity: O(1) in this mock, O(N * d^2) in real Transformers.
        """
        # Create base random logits
        logits = [random.uniform(-5.0, 5.0) for _ in range(self.vocab_size)]
        
        # Add some heuristic rules to make the output "look" somewhat coherent
        if not input_ids:
            # Start of sentence: capital words more likely
            logits[2] += 10.0 # "The"
            logits[12] += 10.0 # "Hello"
            return logits
            
        last_token = input_ids[-1]
        
        # Simple bigram-like rules
        if last_token == 2: # "The"
            logits[3] += 15.0 # "quick"
            logits[14] += 10.0 # "AI"
        elif last_token == 3: # "quick"
            logits[4] += 15.0 # "brown"
        elif last_token == 4: # "brown"
            logits[5] += 15.0 # "fox"
        elif last_token == 5: # "fox"
            logits[6] += 15.0 # "jumps"
        elif last_token == 6: # "jumps"
            logits[7] += 15.0 # "over"
        elif last_token == 7: # "over"
            logits[8] += 15.0 # "the"
        elif last_token == 8: # "the"
            logits[9] += 15.0 # "lazy"
        elif last_token == 9: # "lazy"
            logits[10] += 15.0 # "dog"
        elif last_token == 10: # "dog"
            logits[11] += 15.0 # "."
        elif last_token == 11: # "."
            logits[1] += 20.0 # "<eos>"
            
        # AI branch
        if last_token == 14: # "AI"
            logits[15] += 15.0 # "is"
        elif last_token == 15: # "is"
            logits[16] += 10.0 # "fascinating"
            logits[18] += 10.0 # "powerful"
        elif last_token == 16: # "fascinating"
            logits[17] += 15.0 # "and"
            logits[11] += 10.0 # "."
        elif last_token == 17: # "and"
            logits[18] += 15.0 # "powerful"
            
        return logits

# =============================================================================
# INFERENCE UTILITIES & MATH FUNCTIONS
# =============================================================================

def softmax(logits: List[float], temperature: float = 1.0) -> List[float]:
    """
    Applies temperature scaling and softmax function to convert logits to probabilities.
    
    Math:
        P(x_i) = exp(x_i / T) / sum(exp(x_j / T))
        
    Args:
        logits: Raw scores from the model.
        temperature: Controls randomness. T=1.0 is default. T<1 makes it more confident.
    """
    if temperature == 0.0:
        # Avoid division by zero. Temperature=0 is equivalent to argmax (greedy).
        probs = [0.0] * len(logits)
        max_idx = logits.index(max(logits))
        probs[max_idx] = 1.0
        return probs
        
    # Apply temperature
    scaled_logits = [l / temperature for l in logits]
    
    # Numerical stability: subtract max before exp
    max_logit = max(scaled_logits)
    exps = [math.exp(l - max_logit) for l in scaled_logits]
    
    sum_exps = sum(exps)
    probs = [e / sum_exps for e in exps]
    return probs

def apply_top_k(probs: List[float], k: int) -> List[float]:
    """
    Keeps only the top k tokens, zeroes out the rest, and renormalizes.
    
    Time Complexity: O(V log K) or O(V) using quickselect, where V is vocab size.
    """
    if k <= 0 or k >= len(probs):
        return probs
        
    # Get indices of top k elements
    # Using sorted for simplicity, though max-heap is theoretically faster for small k
    indexed_probs = list(enumerate(probs))
    sorted_probs = sorted(indexed_probs, key=lambda x: x[1], reverse=True)
    
    # Keep top k, zero out others
    top_k_indices = set(idx for idx, _ in sorted_probs[:k])
    
    filtered_probs = [p if i in top_k_indices else 0.0 for i, p in enumerate(probs)]
    
    # Renormalize
    sum_filtered = sum(filtered_probs)
    if sum_filtered > 0:
        filtered_probs = [p / sum_filtered for p in filtered_probs]
        
    return filtered_probs

def apply_top_p(probs: List[float], p: float) -> List[float]:
    """
    Nucleus sampling: keeps the smallest set of tokens whose cumulative probability >= p.
    
    Time Complexity: O(V log V) to sort the probabilities.
    """
    if p <= 0.0 or p >= 1.0:
        return probs
        
    indexed_probs = list(enumerate(probs))
    sorted_probs = sorted(indexed_probs, key=lambda x: x[1], reverse=True)
    
    cumulative_prob = 0.0
    allowed_indices = set()
    
    for idx, prob in sorted_probs:
        allowed_indices.add(idx)
        cumulative_prob += prob
        if cumulative_prob >= p:
            break
            
    filtered_probs = [prob if i in allowed_indices else 0.0 for i, prob in enumerate(probs)]
    
    # Renormalize
    sum_filtered = sum(filtered_probs)
    if sum_filtered > 0:
        filtered_probs = [prob / sum_filtered for prob in filtered_probs]
        
    return filtered_probs

def sample_from_distribution(probs: List[float]) -> int:
    """
    Samples an index from a probability distribution.
    Time Complexity: O(V) where V is vocabulary size.
    """
    r = random.random()
    cumulative = 0.0
    for i, p in enumerate(probs):
        cumulative += p
        if r <= cumulative:
            return i
    return len(probs) - 1 # Fallback to last token (due to float precision issues)

# =============================================================================
# INFERENCE ENGINE
# =============================================================================

class LLMInferenceEngine:
    def __init__(self, model: MockLLM, tokenizer: MockTokenizer):
        self.model = model
        self.tokenizer = tokenizer
        
    def generate(
        self, 
        prompt: str, 
        max_new_tokens: int = 20, 
        temperature: float = 1.0,
        top_k: int = 0,
        top_p: float = 1.0,
        eos_token_id: int = 1
    ) -> str:
        """
        Autoregressive generation loop.
        
        Args:
            prompt: The input context.
            max_new_tokens: Max number of tokens to generate.
            temperature: Softmax temperature.
            top_k: Top-k sampling parameter (0 disables).
            top_p: Nucleus sampling parameter (1.0 disables).
            eos_token_id: End of sequence token ID to stop generation early.
            
        Returns:
            The complete generated text (prompt + continuation).
        """
        input_ids = self.tokenizer.encode(prompt)
        
        print(f"\n--- Generating text ---")
        print(f"Prompt: '{prompt}'")
        print(f"Params: temp={temperature}, top_k={top_k}, top_p={top_p}")
        print("Tokens generating: ", end="", flush=True)
        
        for step in range(max_new_tokens):
            # 1. Forward pass to get logits for next token
            # In a real model with KV Cache, we'd only pass the last token and the cache
            logits = self.model.forward(input_ids)
            
            # 2. Scale by temperature and apply softmax
            probs = softmax(logits, temperature)
            
            # 3. Apply truncation strategies
            if top_k > 0:
                probs = apply_top_k(probs, top_k)
            if top_p < 1.0:
                probs = apply_top_p(probs, top_p)
                
            # 4. Sample the next token
            next_token_id = sample_from_distribution(probs)
            
            # Print token interactively
            token_str = self.tokenizer.decode([next_token_id])
            print(f"{token_str} ", end="", flush=True)
            
            # 5. Append to context
            input_ids.append(next_token_id)
            
            # 6. Check stopping condition
            if next_token_id == eos_token_id:
                break
                
            time.sleep(0.1) # Simulate computation delay
            
        print("\n--- Generation complete ---\n")
        return self.tokenizer.decode(input_ids)


# =============================================================================
# KV CACHING EXPLANATION & MOCK IMPLEMENTATION
# =============================================================================
# In self-attention:
# Query (Q) = W_q * X
# Key (K) = W_k * X
# Value (V) = W_v * X
# Attention = Softmax(Q * K^T / sqrt(d_k)) * V
#
# Without KV cache, generating the Nth token requires recomputing K and V 
# for all previous N-1 tokens.
# With KV cache, we store K and V at each step. For the Nth token, we only 
# compute Q, K, V for the Nth token, and append the new K, V to the cache.

class MockKVCache:
    """Educational demonstration of a Key-Value cache structure."""
    def __init__(self):
        # In reality, this would be a tensor of shape:
        # (batch_size, num_layers, num_heads, sequence_length, head_dim)
        self.k_cache = [] 
        self.v_cache = []
        
    def update(self, k_new: Any, v_new: Any):
        """Append new keys and values to the cache."""
        self.k_cache.append(k_new)
        self.v_cache.append(v_new)
        
    def get_context_length(self) -> int:
        return len(self.k_cache)
        
    def clear(self):
        self.k_cache = []
        self.v_cache = []


# =============================================================================
# INTERVIEW CHALLENGE: BEAM SEARCH (SIMPLIFIED)
# =============================================================================
# Challenge: Implement a simplified Beam Search decoding.
# Greedy search picks the best token at each step. Beam search keeps track of 
# the 'B' most likely sequences at each step.

@dataclass
class Beam:
    sequence: List[int]
    log_prob: float

def simplified_beam_search(
    model: MockLLM, 
    start_token: int, 
    beam_width: int, 
    max_steps: int
) -> List[int]:
    """
    Simplified Beam Search algorithm.
    Time Complexity: O(max_steps * beam_width * Vocab_Size)
    """
    print(f"--- Running Beam Search (width={beam_width}) ---")
    
    # Initialize beam with the start token
    beams = [Beam(sequence=[start_token], log_prob=0.0)]
    
    for step in range(max_steps):
        all_candidates = []
        
        # Expand each beam
        for beam in beams:
            if beam.sequence[-1] == 1: # <eos>
                # If sequence ended, keep it as is
                all_candidates.append(beam)
                continue
                
            logits = model.forward(beam.sequence)
            probs = softmax(logits, temperature=1.0)
            
            # To avoid underflow, we sum log probabilities
            for vocab_id, prob in enumerate(probs):
                if prob > 1e-10: # avoid log(0)
                    new_seq = list(beam.sequence)
                    new_seq.append(vocab_id)
                    new_log_prob = beam.log_prob + math.log(prob)
                    all_candidates.append(Beam(sequence=new_seq, log_prob=new_log_prob))
                    
        # Sort candidates by probability (highest first)
        ordered = sorted(all_candidates, key=lambda b: b.log_prob, reverse=True)
        
        # Prune to beam width
        beams = ordered[:beam_width]
        
    # Return the sequence of the best beam
    return beams[0].sequence

# =============================================================================
# MAIN EXECUTION AND TEST CASES
# =============================================================================

def run_tests():
    """Unit tests for the math utilities."""
    print("--- Running Unit Tests ---")
    
    # Test Softmax
    logits = [2.0, 1.0, 0.1]
    probs = softmax(logits, temperature=1.0)
    assert abs(sum(probs) - 1.0) < 1e-5, "Softmax must sum to 1"
    assert probs[0] > probs[1] > probs[2], "Order must be preserved"
    
    # Test Temperature scaling
    probs_hot = softmax(logits, temperature=2.0)
    probs_cold = softmax(logits, temperature=0.5)
    
    # Cold temperature should make the distribution sharper (max gets larger)
    assert max(probs_cold) > max(probs)
    # Hot temperature should make the distribution flatter (max gets smaller)
    assert max(probs_hot) < max(probs)
    
    # Test Top-K
    uniform_probs = [0.1, 0.2, 0.3, 0.4]
    top_2 = apply_top_k(uniform_probs, k=2)
    assert top_2[0] == 0.0
    assert top_2[1] == 0.0
    assert top_2[2] > 0.0
    assert top_2[3] > 0.0
    assert abs(sum(top_2) - 1.0) < 1e-5
    
    # Test Top-P
    top_p_probs = apply_top_p(uniform_probs, p=0.6)
    # 0.4 + 0.3 = 0.7 >= 0.6. So indices 3 and 2 should be kept.
    assert top_p_probs[0] == 0.0
    assert top_p_probs[1] == 0.0
    assert top_p_probs[2] > 0.0
    assert top_p_probs[3] > 0.0
    assert abs(sum(top_p_probs) - 1.0) < 1e-5
    
    print("All tests passed successfully!\n")

if __name__ == "__main__":
    print(f"========== EXPLORING LLM INFERENCE ==========\n")
    
    # Run mathematical unit tests
    run_tests()
    
    tokenizer = MockTokenizer()
    model = MockLLM(vocab_size=tokenizer.vocab_size)
    engine = LLMInferenceEngine(model, tokenizer)
    
    # 1. Greedy Search (Deterministic, T=0)
    print("1. GREEDY DECODING (T=0.0)")
    engine.generate("The", temperature=0.0)
    
    # 2. Standard Sampling (T=1.0)
    print("2. STANDARD SAMPLING (T=1.0)")
    engine.generate("AI", temperature=1.0)
    
    # 3. High Temperature (Creative/Random, T=2.0)
    print("3. HIGH TEMPERATURE (T=2.0)")
    engine.generate("The", temperature=2.0)
    
    # 4. Top-K Sampling
    print("4. TOP-K SAMPLING (K=2)")
    engine.generate("AI", top_k=2)
    
    # 5. Top-P (Nucleus) Sampling
    print("5. TOP-P SAMPLING (P=0.9)")
    engine.generate("The", top_p=0.9)
    
    # 6. Beam Search (Interview Challenge)
    best_seq = simplified_beam_search(model, start_token=2, beam_width=3, max_steps=5)
    print(f"Best beam sequence IDs: {best_seq}")
    print(f"Decoded: {tokenizer.decode(best_seq)}")
    
    print(f"\n========== END OF LLM INFERENCE LESSON ==========\n")
