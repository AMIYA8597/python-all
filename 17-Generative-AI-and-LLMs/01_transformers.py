"""
# ==============================================================================
# LABORATORY: GENERATIVE AI (AUTOREGRESSIVE GENERATION LOOP)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A junior developer believes that when they type a prompt into ChatGPT, the 
# model instantly "thinks" of the entire paragraph and returns it all at once.
#
# A senior AI engineer understands "Autoregressive Generation". They know that 
# ChatGPT is fundamentally a mathematical "Next-Token Predictor". If the prompt 
# is "The cat sat", the model executes a massive Matrix Multiplication to predict 
# exactly ONE token: "on". The engineer knows the context window must now physically 
# append "on" to the input, becoming "The cat sat on". The massive Matrix Multiplication 
# runs *again from scratch* to predict "the". The loop continues until the model 
# predicts the special `<EOS>` (End Of Sequence) token.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master the Autoregressive Decoding loop.
# - Execute Context Window appending.
# - Architect a simulated Next-Token Prediction pipeline.
#
# ==============================================================================
"""

import time
import random

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE BUSINESS LOGIC (THE LLM SIMULATOR)
# ==============================================================================
class LLMSimulator:
    """
    Simulates a 1-Billion Parameter Generative Pre-trained Transformer.
    """
    def __init__(self):
        # A tiny simulated vocabulary and transition probabilities
        # Format: { "context": { "next_word": probability } }
        self.vocabulary_weights = {
            "The": {"quick": 0.8, "lazy": 0.2},
            "The quick": {"brown": 0.9, "red": 0.1},
            "The quick brown": {"fox": 0.95, "dog": 0.05},
            "The quick brown fox": {"jumps": 0.7, "sleeps": 0.3},
            "The quick brown fox jumps": {"over": 0.99},
            "The quick brown fox jumps over": {"the": 1.0},
            "The quick brown fox jumps over the": {"lazy": 0.8, "fence": 0.2},
            "The quick brown fox jumps over the lazy": {"dog": 0.9, "cat": 0.1},
            "The quick brown fox jumps over the lazy dog": {"<EOS>": 1.0}
        }
        
        self.context_window_limit = 2048 # Maximum tokens it can remember

    def predict_next_token(self, current_context: str) -> str:
        """
        [SECURE] The core of ChatGPT.
        Takes the entire current context, pushes it through the Transformer 
        Matrix Multiplications, and outputs exactly ONE token.
        """
        # Simulate GPU computation time (Forward Pass)
        time.sleep(0.5) 
        
        # If the context is in our simulated weights, pick the highest probability token (Greedy Decoding)
        if current_context in self.vocabulary_weights:
            possible_next_tokens = self.vocabulary_weights[current_context]
            
            # Find the token with the maximum probability (Simulating Argmax over Softmax)
            best_token = max(possible_next_tokens, key=possible_next_tokens.get)
            confidence = possible_next_tokens[best_token]
            
            print(f"     [GPU] Forward pass complete. Softmax confidence for '{best_token}': {confidence*100:.1f}%")
            return best_token
            
        return "<EOS>"


# ==============================================================================
# 4. THE ARCHITECTURAL PATTERN: THE AUTOREGRESSIVE LOOP
# ==============================================================================
class InferenceEngine:
    
    def __init__(self, model: LLMSimulator):
        self.model = model
        
    def generate_text(self, prompt: str, max_tokens: int = 10):
        """
        [SECURE] The Autoregressive Generation Loop.
        """
        print(f"\n  [USER PROMPT] '{prompt}'")
        print("  [SYSTEM] Initializing Autoregressive Generation Loop...\n")
        
        current_context = prompt
        generated_tokens = []
        
        for step in range(1, max_tokens + 1):
            print(f"  -> Step {step}: Context Buffer = ['{current_context}']")
            
            # 1. Ask the model for exactly ONE token
            next_token = self.model.predict_next_token(current_context)
            
            # 2. Check for the End Of Sequence token
            if next_token == "<EOS>":
                print(f"  -> Step {step}: Model generated <EOS>. Halting generation.")
                break
                
            # 3. Append the new token to the Context Window!
            # THIS is why generating 1,000 words takes longer than generating 10 words.
            # The context gets longer, making the matrix multiplication heavier every step.
            current_context = current_context + " " + next_token
            generated_tokens.append(next_token)
            
        print(f"\n  [FINAL OUTPUT] {prompt} " + " ".join(generated_tokens))
        print("\n  [FLAWLESS] The LLM mathematically constructed the sentence one token ")
        print("  at a time, perfectly maintaining semantic coherence across the entire loop.")


# ==============================================================================
# 5. MATHEMATICAL PROOF (THE BENCHMARK)
# ==============================================================================
def demonstrate_autoregressive_generation():
    section_header("Generative AI: The Autoregressive Loop")
    
    model = LLMSimulator()
    engine = InferenceEngine(model)
    
    # Start the generation!
    engine.generate_text(prompt="The", max_tokens=15)


def run_all_labs():
    demonstrate_autoregressive_generation()


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "Why does the generation speed (Tokens Per Second) of an LLM slow down as the generated response gets longer?"
   Senior Answer: "The $O(N^2)$ Context Window Bottleneck. An LLM is Autoregressive. To generate Token $100$, it must push Tokens $1$ through $99$ through the massive Self-Attention matrix ($Q \\cdot K^T$). The computational complexity of Self-Attention is mathematically $O(N^2)$ with respect to the sequence length. To generate Token $101$, it must push Tokens $1$ through $100$ through the matrix. The physical size of the matrix multiplication grows quadratically with every single step. This is why a $4,000$-token response takes significantly more GPU compute per token at the end of the response than at the beginning."

2. Interviewer: "What is the physical significance of the `<EOS>` (End Of Sequence) token?"
   Senior Answer: "Mathematical Halting. A Transformer matrix multiplication has no biological concept of 'being finished'. If you put numbers into the matrix, it will output a prediction for the next number infinitely. During pre-training, datasets are physically appended with a special `<EOS>` token at the end of documents. The model mathematically learns the semantic conditions that signify a completed thought, and outputs the `<EOS>` vector. The Inference Engine running the `for` loop contains a hardcoded `if token == '<EOS>': break` statement. Without this token, the model would hallucinate infinitely until it hit the hard max-token limit."

3. Interviewer: "Explain the difference between Pre-Training and Inference in terms of the Context Window."
   Senior Answer: "Parallel vs Sequential. During Pre-Training, we know the entire document in advance. We can utilize Teacher Forcing and Causal Masking to mathematically train the model on predicting *every single next token in the document simultaneously* in one massive parallel matrix multiplication on the GPU. During Inference (serving the model to users), we do not know the future tokens. We must physically wait for the model to generate Token $N$, append it to RAM, and then execute a brand new forward pass to predict Token $N+1$. Pre-training is perfectly parallelizable; Inference is strictly sequential and autoregressive."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Generative AI (Autoregressive Loop) Completed.")
