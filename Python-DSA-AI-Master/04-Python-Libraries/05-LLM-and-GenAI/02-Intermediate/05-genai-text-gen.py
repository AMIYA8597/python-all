"""
Module: 05-genai-text-gen
Description: A comprehensive textbook-grade lesson on Text Generation in Large Language Models (LLMs).

=========================================================================================
1. Theoretical Background & Mathematical Foundations
=========================================================================================
Text Generation, in the context of modern Generative AI, is framed as an autoregressive 
language modeling task. Given a sequence of prior tokens (context), the model predicts 
the probability distribution of the next token in the vocabulary.

Let the sequence of tokens be X = (x_1, x_2, ..., x_t).
The probability of the next token x_{t+1} is given by:
    P(x_{t+1} | x_1, x_2, ..., x_t)

The overall probability of a generated sequence of length T is:
    P(x_1, ..., x_T) = P(x_1) * P(x_2|x_1) * ... * P(x_T|x_1, ..., x_{T-1})
                     = \prod_{t=1}^{T} P(x_t | x_{<t})

Logits to Probabilities:
The LLM outputs raw scores called "logits" (z_i) for each word in the vocabulary (size V).
These are converted to probabilities using the Softmax function:
    P(x = i) = exp(z_i / T_temp) / \sum_{j=1}^{V} exp(z_j / T_temp)

Where T_temp is the Temperature parameter:
- T_temp = 1.0 : Standard softmax.
- T_temp < 1.0 : Sharpens the distribution (more deterministic/greedy, less random).
- T_temp > 1.0 : Flattens the distribution (more random/creative).
- T_temp -> 0  : Approaches Greedy Decoding (argmax).

=========================================================================================
2. Decoding Strategies
=========================================================================================
Once we have the probability distribution for the next token, how do we select it?

A. Greedy Decoding:
   Always select the token with the highest probability.
   x_{t+1} = argmax( P(x | x_{<t}) )
   Drawback: Can lead to repetitive and generic text, ignoring better long-term sequences.

B. Top-K Sampling:
   Sort the probabilities and keep only the top K most likely tokens.
   Redistribute probability mass among these K tokens and sample from them.
   Drawback: A fixed K might include "bad" words if the distribution is flat, or exclude 
   "good" words if the distribution is sharp.

C. Top-P (Nucleus) Sampling:
   Sort the probabilities in descending order.
   Keep tokens until the cumulative probability exceeds a threshold P (e.g., 0.9).
   Redistribute probability mass among these selected tokens and sample.
   Benefit: Dynamically adjusts the number of choices based on model confidence.

=========================================================================================
3. Big-O Complexity Analysis (Autoregressive Generation)
=========================================================================================
Let:
N = Length of context (input prompt)
T = Number of tokens to generate
L = Number of transformer layers
d = Hidden dimension size

- Generating a single token requires a forward pass through the network.
- Without KV Caching (Naive): O(N^2 * d) for self-attention.
  For T tokens: O(T * (N+T)^2 * d). This is extremely slow.
- With KV Caching (Standard in LLMs):
  We cache the Key and Value matrices of previous tokens.
  Attention per new token becomes O( (N+t) * d ).
  Total generation for T tokens: O( T * (N + T) * d ).
  Space Complexity (KV Cache): O( (N+T) * L * d * batch_size ).

=========================================================================================
4. Real-world Applications
=========================================================================================
- Chatbots & Conversational Agents (ChatGPT, Claude)
- Code Generation (GitHub Copilot)
- Text Summarization and Translation
- Creative Writing and Brainstorming Tools
"""

import math
import random
from typing import List, Dict, Tuple, Optional


class Vocabulary:
    """
    A simple vocabulary class to map words to token IDs and vice versa.
    In real LLMs, this is handled by advanced tokenizers like Byte-Pair Encoding (BPE).
    """
    def __init__(self, words: List[str]):
        # Start with a special End-Of-Sequence token
        self.words = ["<EOS>"] + list(set(words))
        self.word2id = {w: i for i, w in enumerate(self.words)}
        self.id2word = {i: w for i, w in enumerate(self.words)}
        self.eos_id = self.word2id["<EOS>"]

    def __len__(self) -> int:
        return len(self.words)

    def encode(self, text: str) -> List[int]:
        # Very naive splitting for demonstration
        return [self.word2id.get(w, self.word2id["<EOS>"]) for w in text.split()]

    def decode(self, token_ids: List[int]) -> str:
        return " ".join([self.id2word.get(idx, "<UNK>") for idx in token_ids])


def apply_temperature(logits: List[float], temperature: float = 1.0) -> List[float]:
    """
    Applies temperature scaling to raw logits and converts them to probabilities via Softmax.
    
    Time Complexity: O(V) where V is the vocabulary size (length of logits).
    Space Complexity: O(V) to store the new probabilities.
    
    Args:
        logits (List[float]): The raw scores for each token in the vocabulary.
        temperature (float): The temperature parameter.
            - T = 1.0 (no change to logits before softmax)
            - T < 1.0 (makes distribution sharper, less random)
            - T > 1.0 (makes distribution flatter, more random)
    
    Returns:
        List[float]: A probability distribution summing to 1.0.
    """
    if temperature <= 0.0:
        raise ValueError("Temperature must be strictly positive. For T=0, use greedy decoding.")

    # Apply temperature
    scaled_logits = [z / temperature for z in logits]
    
    # Softmax with numerical stability (subtract max)
    max_logit = max(scaled_logits)
    exp_logits = [math.exp(z - max_logit) for z in scaled_logits]
    
    sum_exp = sum(exp_logits)
    probabilities = [e / sum_exp for e in exp_logits]
    
    return probabilities


def greedy_decoding(probabilities: List[float]) -> int:
    """
    Selects the token with the absolute highest probability.
    
    Time Complexity: O(V) to find the max.
    Space Complexity: O(1).
    """
    max_prob = -1.0
    best_token = 0
    for i, prob in enumerate(probabilities):
        if prob > max_prob:
            max_prob = prob
            best_token = i
    return best_token


def top_k_sampling(probabilities: List[float], k: int) -> int:
    """
    Samples a token from the Top-K most probable tokens.
    
    Time Complexity: O(V log(V)) due to sorting.
    Space Complexity: O(V) to store sorted probabilities.
    """
    if k <= 0 or k > len(probabilities):
        raise ValueError("k must be between 1 and vocabulary size.")

    # Pair probabilities with their original token indices
    prob_idx = [(p, i) for i, p in enumerate(probabilities)]
    
    # Sort descending based on probability
    prob_idx.sort(key=lambda x: x[0], reverse=True)
    
    # Keep only the top k
    top_k_probs = prob_idx[:k]
    
    # Re-normalize probabilities among the top k
    sum_top_k = sum(p for p, idx in top_k_probs)
    normalized_probs = [p / sum_top_k for p, idx in top_k_probs]
    
    # Sample using the cumulative distribution function (CDF)
    rand_val = random.random()
    cumulative = 0.0
    for i, p in enumerate(normalized_probs):
        cumulative += p
        if rand_val <= cumulative:
            return top_k_probs[i][1]
            
    return top_k_probs[-1][1]  # Fallback due to floating point inaccuracies


def top_p_sampling(probabilities: List[float], p: float) -> int:
    """
    Samples a token using Nucleus (Top-P) sampling.
    Selects the smallest set of tokens whose cumulative probability exceeds p.
    
    Time Complexity: O(V log(V)) for sorting.
    Space Complexity: O(V).
    """
    if not (0.0 < p <= 1.0):
        raise ValueError("p must be in the range (0.0, 1.0].")

    prob_idx = [(prob, i) for i, prob in enumerate(probabilities)]
    prob_idx.sort(key=lambda x: x[0], reverse=True)
    
    cumulative = 0.0
    selected_tokens = []
    
    # Collect tokens until the cumulative probability exceeds p
    for prob, idx in prob_idx:
        selected_tokens.append((prob, idx))
        cumulative += prob
        if cumulative >= p:
            break
            
    # Re-normalize among selected tokens
    sum_selected = sum(prob for prob, idx in selected_tokens)
    normalized_probs = [prob / sum_selected for prob, idx in selected_tokens]
    
    # Sample from the normalized distribution
    rand_val = random.random()
    curr_cumulative = 0.0
    for i, norm_p in enumerate(normalized_probs):
        curr_cumulative += norm_p
        if rand_val <= curr_cumulative:
            return selected_tokens[i][1]
            
    return selected_tokens[-1][1]


class DummyLanguageModel:
    """
    A simulated Language Model that outputs random logits for demonstration.
    In reality, this would be a massive Transformer model (e.g., GPT, LLaMA).
    """
    def __init__(self, vocab_size: int):
        self.vocab_size = vocab_size

    def get_logits(self, context_ids: List[int]) -> List[float]:
        """
        Simulates a forward pass. 
        Returns a list of logits (one for each token in the vocabulary).
        
        To simulate realistic behavior, we'll assign a higher logit to the EOS 
        token if the context length is large, encouraging the model to stop.
        """
        # Generate random logits in range [-10, 10]
        logits = [random.uniform(-10.0, 10.0) for _ in range(self.vocab_size)]
        
        # Increase the chance of stopping (EOS is token 0) as sequence grows
        if len(context_ids) > 10:
            logits[0] += len(context_ids) * 0.5 
            
        return logits


def generate_text(
    model: DummyLanguageModel, 
    vocab: Vocabulary, 
    prompt: str, 
    max_new_tokens: int = 20, 
    temperature: float = 1.0, 
    strategy: str = 'greedy',
    k: int = 5,
    p: float = 0.9
) -> str:
    """
    The main auto-regressive generation loop.
    
    1. Encode prompt to token IDs.
    2. Loop up to max_new_tokens times:
        a. Get logits from the model given the current context.
        b. Apply temperature and softmax to get probabilities.
        c. Decode/Sample the next token ID based on the chosen strategy.
        d. Append next token ID to the context.
        e. If the token is the End-Of-Sequence (<EOS>) token, break.
    3. Decode the final sequence of token IDs back to a string.
    """
    context_ids = vocab.encode(prompt)
    
    print(f"\n--- Generating text with strategy: {strategy} ---")
    print(f"Initial context: {context_ids}")

    for step in range(max_new_tokens):
        # 1. Forward Pass (Get Logits)
        logits = model.get_logits(context_ids)
        
        # 2. Temperature Scaling & Softmax
        probs = apply_temperature(logits, temperature=temperature)
        
        # 3. Apply Decoding Strategy
        if strategy == 'greedy':
            next_token = greedy_decoding(probs)
        elif strategy == 'top_k':
            next_token = top_k_sampling(probs, k=k)
        elif strategy == 'top_p':
            next_token = top_p_sampling(probs, p=p)
        else:
            raise ValueError(f"Unknown decoding strategy: {strategy}")
            
        # 4. Update Context
        context_ids.append(next_token)
        
        # 5. Check for early stopping
        if next_token == vocab.eos_id:
            print(f"Stopping early at step {step + 1} (generated <EOS> token).")
            break

    generated_text = vocab.decode(context_ids)
    print(f"Final output: {generated_text}")
    return generated_text


# =============================================================================
# Testing and Verification
# =============================================================================

def run_tests():
    print("Running mathematical unit tests...")
    
    # 1. Test Temperature & Softmax
    logits = [10.0, 5.0, 0.0]
    
    # T=1.0
    probs_t1 = apply_temperature(logits, temperature=1.0)
    assert math.isclose(sum(probs_t1), 1.0, rel_tol=1e-5)
    assert probs_t1[0] > probs_t1[1] > probs_t1[2] # Order should be preserved
    
    # High Temperature (Flatter)
    probs_high_t = apply_temperature(logits, temperature=100.0)
    # The probabilities should be very close to uniform (0.33, 0.33, 0.33)
    assert abs(probs_high_t[0] - probs_high_t[1]) < 0.05
    
    # Low Temperature (Sharper)
    probs_low_t = apply_temperature(logits, temperature=0.1)
    # The highest logit should dominate completely
    assert probs_low_t[0] > 0.99
    
    # 2. Test Greedy Decoding
    probs = [0.1, 0.7, 0.2]
    assert greedy_decoding(probs) == 1
    
    # 3. Test Top-K constraints
    # If K=1, it's essentially greedy decoding
    assert top_k_sampling(probs, k=1) == 1
    
    print("All unit tests passed successfully!\n")


if __name__ == "__main__":
    print("="*80)
    print(" GENERATIVE AI: TEXT GENERATION (INTERMEDIATE)")
    print("="*80)
    
    # Run unit tests
    run_tests()
    
    # Create a vocabulary of common words
    words = ["the", "quick", "brown", "fox", "jumps", "over", "lazy", "dog",
             "hello", "world", "AI", "is", "awesome", "Python", "code", "generation"]
    
    vocab = Vocabulary(words)
    model = DummyLanguageModel(vocab_size=len(vocab))
    
    prompt = "hello AI"
    
    # Demonstrate Greedy Decoding (T=1.0)
    # Since model is random, output is random, but it will always pick the max probability token
    generate_text(model, vocab, prompt, max_new_tokens=10, temperature=1.0, strategy='greedy')
    
    # Demonstrate Top-K Sampling (K=3)
    # More diverse than greedy, limits choices to top 3
    generate_text(model, vocab, prompt, max_new_tokens=10, temperature=1.0, strategy='top_k', k=3)
    
    # Demonstrate Top-P / Nucleus Sampling (P=0.8)
    # Dynamically chooses tokens making up 80% of the probability mass
    generate_text(model, vocab, prompt, max_new_tokens=10, temperature=0.8, strategy='top_p', p=0.8)
    
    # Demonstrate Temperature effects
    print("\n--- Testing High Temperature (T=5.0) with Top-P ---")
    # Will likely produce more erratic/random word choices
    generate_text(model, vocab, prompt, max_new_tokens=10, temperature=5.0, strategy='top_p', p=0.9)
    
    print("\n" + "="*80)
    print(" END OF LESSON")
    print("="*80)
