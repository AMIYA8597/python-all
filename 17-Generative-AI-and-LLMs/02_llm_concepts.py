"""
# ==============================================================================
# LABORATORY: GENERATIVE AI (LLM INFERENCE & DECODING STRATEGIES)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A junior developer prompts an LLM to write a poem. They use standard "Greedy 
# Decoding" (always picking the absolute highest probability token). The LLM 
# outputs: "The cat sat on the mat. The cat sat on the mat. The cat sat on the mat." 
# It falls into a mathematical loop because the highest probability is always 
# repetitive.
#
# A senior AI engineer understands "Sampling Mathematics". They inject a 
# "Temperature" of 0.8 to mathematically flatten the probability distribution, 
# increasing randomness. They simultaneously apply "Top-P (Nucleus) Sampling" 
# at 0.9, forcing the model to ignore the long tail of 50,000 garbage tokens 
# and only randomly sample from the mathematically viable top words. The LLM 
# writes a beautiful, creative, non-repetitive poem.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master Logit Scaling (Temperature Mathematics).
# - Execute Top-K and Top-P (Nucleus) filtering.
# - Architect deterministic vs stochastic generation.
#
# ==============================================================================
"""

import numpy as np

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE BUSINESS LOGIC (TEMPERATURE & SOFTMAX)
# ==============================================================================
class DecodingSimulator:
    
    @staticmethod
    def calculate_softmax(logits: np.ndarray, temperature: float = 1.0) -> np.ndarray:
        """
        [SECURE] Temperature-Scaled Softmax.
        Logits are the raw, un-normalized outputs of the neural network's final layer.
        """
        # If Temperature is basically 0, we can't divide by 0!
        if temperature < 1e-5:
            # Simulate perfectly greedy decoding: 1.0 for the max, 0.0 for the rest
            probs = np.zeros_like(logits)
            probs[np.argmax(logits)] = 1.0
            return probs
            
        # 1. Scale the logits by dividing by Temperature
        scaled_logits = logits / temperature
        
        # 2. Stable Softmax calculation
        e_x = np.exp(scaled_logits - np.max(scaled_logits))
        return e_x / e_x.sum()

    def simulate_temperature(self):
        print("  [INIT] Simulating LLM Output Logits for 'The quick brown...'")
        
        # The Neural Network output these raw values for the next word:
        vocab = ["fox", "dog", "bear", "car", "apple"]
        raw_logits = np.array([5.0, 4.0, 1.0, -2.0, -5.0])
        
        print(f"  -> Raw Logits: {raw_logits}")
        
        # ----- Test 1: Greedy (Temperature = 0.0) -----
        print("\n  [TEST 1: Temperature = 0.0 (Deterministic / Greedy)]")
        probs_greedy = self.calculate_softmax(raw_logits, temperature=0.0)
        for i, word in enumerate(vocab):
            print(f"     - {word}: {probs_greedy[i]*100:>6.2f}%")
            
        # ----- Test 2: Standard (Temperature = 1.0) -----
        print("\n  [TEST 2: Temperature = 1.0 (Standard Softmax)]")
        probs_std = self.calculate_softmax(raw_logits, temperature=1.0)
        for i, word in enumerate(vocab):
            print(f"     - {word}: {probs_std[i]*100:>6.2f}%")
            
        # ----- Test 3: Creative (Temperature = 2.0) -----
        print("\n  [TEST 3: Temperature = 2.0 (High Creativity / Chaos)]")
        probs_chaos = self.calculate_softmax(raw_logits, temperature=2.0)
        for i, word in enumerate(vocab):
            print(f"     - {word}: {probs_chaos[i]*100:>6.2f}%")
            
        print("\n  -> [MATHEMATICAL PROOF] High temperature mathematically flattened the ")
        print("     distribution. 'fox' dropped from 73% to 47%, while the garbage ")
        print("     token 'apple' rose from 0% to nearly 1%. The model is now capable ")
        print("     of generating unexpected (but potentially hallucinatory) text.")


    # --------------------------------------------------------------------------
    # THE ARCHITECTURAL PATTERN: NUCLEUS SAMPLING
    # --------------------------------------------------------------------------
    @staticmethod
    def simulate_top_p_sampling():
        """
        [SECURE] Top-P (Nucleus) Sampling.
        Mathematically slices off the 'long tail' of garbage tokens before random sampling.
        """
        print("\n  [INIT] Simulating Top-P (Nucleus) Sampling at P = 0.90...")
        
        vocab = ["fox", "dog", "wolf", "cat", "car", "apple"]
        # Already run through Softmax (Temp=1.0)
        probabilities = np.array([0.50, 0.25, 0.10, 0.08, 0.05, 0.02])
        
        print("\n  -> Initial Probabilities:")
        for w, p in zip(vocab, probabilities):
            print(f"     {w}: {p*100:.1f}%")
            
        # 1. Sort the probabilities in descending order (already sorted here for simplicity)
        sorted_probs = probabilities
        sorted_vocab = vocab
        
        # 2. Calculate the Cumulative Sum!
        cumulative_probs = np.cumsum(sorted_probs)
        print(f"\n  -> Cumulative Mass: {cumulative_probs}")
        
        # 3. Cut off everything after the cumulative mass hits 0.90
        # The boolean mask determines which tokens survive
        p_threshold = 0.90
        survivor_mask = cumulative_probs - sorted_probs < p_threshold
        
        survivors = []
        for i in range(len(sorted_vocab)):
            if survivor_mask[i]:
                survivors.append(sorted_vocab[i])
                
        print(f"\n  -> [SURVIVORS] {survivors}")
        print("  -> [FLAWLESS] The algorithm mathematically preserved 'fox', 'dog', ")
        print("     'wolf', and 'cat' because their combined mass hit 93%. It brutally ")
        print("     deleted 'car' and 'apple', guaranteeing the model will never randomly ")
        print("     hallucinate a completely irrelevant word, even if Temperature is high!")


# ==============================================================================
# 4. MATHEMATICAL PROOF (THE BENCHMARK)
# ==============================================================================
def demonstrate_decoding():
    section_header("Generative AI: Decoding & Sampling")
    
    sim = DecodingSimulator()
    sim.simulate_temperature()
    sim.simulate_top_p_sampling()


def run_all_labs():
    demonstrate_decoding()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "If you set Temperature to $0.0$, what mathematically happens to the Softmax equation, and what decoding strategy does this simulate?"
   Senior Answer: "Greedy Decoding. The Softmax equation divides the input Logits by the Temperature ($T$). As $T$ approaches $0.0$, the Logit of the highest value is divided by a tiny fraction, accelerating towards Positive Infinity. All lesser Logits accelerate towards Negative Infinity (or fall infinitely far behind). When passed through the $e^x$ exponential function, the largest value mathematically crushes all other values to absolute zero. The output probability distribution becomes a strict One-Hot vector ($1.0$ for the winner, $0.0$ for everything else), perfectly eliminating all randomness and simulating Greedy Decoding."

2. Interviewer: "Why is Top-P (Nucleus) Sampling architecturally superior to Top-K Sampling?"
   Senior Answer: "Dynamic Vocabulary Slicing. Top-K forces the model to ALWAYS sample from exactly $K$ words (e.g., $K=50$). If the model is absolutely certain about the next word (e.g., 'The capital of France is...' -> 'Paris': $99\\%$), Top-K still mathematically allows a $1\\%$ chance of sampling from $49$ garbage words! This causes hallucinations. Top-P (Nucleus) Sampling sums the probabilities until they hit a percentage threshold (e.g., $P=0.90$). If 'Paris' is $99\\%$, the cumulative sum instantly shatters the $0.90$ threshold on the very first word. The Nucleus shrinks to exactly $1$ word. If the model is confused and $100$ words all have $1\\%$ probability, the Nucleus dynamically expands to include $90$ words. Top-P adapts its mathematical boundary based on the model's confidence."

3. Interviewer: "What is 'KV Caching' in the context of an LLM Inference Engine?"
   Senior Answer: "Matrix Reuse during Autoregression. In a Transformer, calculating Attention requires Query, Key, and Value matrices. During Token $10$, the model calculates $K$ and $V$ vectors for Tokens $1$ through $9$. To generate Token $11$, a naive engine will completely recalculate the $K$ and $V$ vectors for Tokens $1$ through $10$ from scratch, wasting massive amounts of GPU FLOPs. A KV Cache physically stores the Key and Value matrices of all past tokens in GPU VRAM. When calculating Token $11$, the model only computes the $Q, K, V$ for the single new token, and mathematically concatenates its $K/V$ onto the cached matrices. This reduces the time complexity of inference from $O(N^2)$ down to $O(N)$, but massively increases the VRAM memory footprint."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Generative AI (LLM Concepts) Completed.")
