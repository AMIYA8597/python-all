import math
import random
from collections import defaultdict

class DummyLLM:
    """
    A simulated Large Language Model that demonstrates next token prediction
    using a simple n-gram/transition probability approach for educational purposes.
    """
    def __init__(self):
        # Our "vocabulary" and simulated transition logits
        self.vocab = ["The", "quick", "brown", "fox", "jumps", "over", "the", "lazy", "dog", ".", "<EOS>"]
        
        # Simulated logits mapping (context -> next_token -> logit)
        # Using a default score of -10 for unseen transitions
        self.logits_table = defaultdict(lambda: {word: -10.0 for word in self.vocab})
        
        # Hardcode some sensible transition logits for demonstration
        self._set_logit("The", "quick", 5.0)
        self._set_logit("quick", "brown", 6.0)
        self._set_logit("brown", "fox", 7.0)
        self._set_logit("fox", "jumps", 4.0)
        self._set_logit("jumps", "over", 5.0)
        self._set_logit("over", "the", 6.0)
        self._set_logit("the", "lazy", 4.0)
        self._set_logit("lazy", "dog", 8.0)
        self._set_logit("dog", ".", 5.0)
        self._set_logit(".", "<EOS>", 10.0)

        # Add some randomness to other transitions to show temperature effects
        for ctx in self.vocab:
            for word in self.vocab:
                if self.logits_table[ctx][word] == -10.0:
                    self.logits_table[ctx][word] = random.uniform(-5.0, 0.0)

    def _set_logit(self, context, next_token, logit_value):
        self.logits_table[context][next_token] = logit_value

    def get_logits(self, context_token):
        """Returns the unnormalized logits for the next token given a context."""
        return self.logits_table[context_token]

def softmax(logits_dict, temperature=1.0):
    """Applies softmax to a dictionary of logits, adjusted by temperature."""
    # Prevent division by zero
    temp = max(temperature, 1e-5)
    
    # Scale logits
    scaled_logits = {k: v / temp for k, v in logits_dict.items()}
    
    # Compute exponentiated values
    max_logit = max(scaled_logits.values()) # For numerical stability
    exp_vals = {k: math.exp(v - max_logit) for k, v in scaled_logits.items()}
    
    # Normalize
    total_exp = sum(exp_vals.values())
    probabilities = {k: v / total_exp for k, v in exp_vals.items()}
    
    return probabilities

def sample_token(probabilities, top_k=None):
    """Samples a token based on probability distribution, optionally using Top-K."""
    if top_k is not None:
        # Sort by probability descending and keep top K
        sorted_probs = sorted(probabilities.items(), key=lambda item: item[1], reverse=True)[:top_k]
        
        # Renormalize among top K
        top_k_total = sum(prob for _, prob in sorted_probs)
        probabilities = {k: prob / top_k_total for k, prob in sorted_probs}
    
    # Roulette wheel selection
    rand_val = random.random()
    cumulative = 0.0
    for token, prob in probabilities.items():
        cumulative += prob
        if rand_val <= cumulative:
            return token
    
    # Fallback (shouldn't hit this due to float math usually)
    return list(probabilities.keys())[-1]

def generate_text(model, start_token, max_length=15, temperature=1.0, top_k=None):
    """Generates a sequence of text autoregressively."""
    sequence = [start_token]
    
    print(f"\n--- Generating with Temperature: {temperature}, Top-K: {top_k} ---")
    print(f"Start: {start_token}")
    
    for _ in range(max_length - 1):
        current_token = sequence[-1]
        
        if current_token == "<EOS>":
            break
            
        # 1. Get Logits
        logits = model.get_logits(current_token)
        
        # 2. Apply Softmax with Temperature
        probs = softmax(logits, temperature=temperature)
        
        # 3. Sample next token
        next_token = sample_token(probs, top_k=top_k)
        
        sequence.append(next_token)
        print(f" -> Predict: {next_token} (Prob: {probs[next_token]:.4f})")
        
    return " ".join(sequence)

if __name__ == "__main__":
    llm = DummyLLM()
    
    # 1. Greedy Generation (Very low temperature approaches greedy)
    generate_text(llm, "The", temperature=0.01)
    
    # 2. Standard Generation
    generate_text(llm, "The", temperature=1.0)
    
    # 3. Creative/Random Generation (High temperature)
    generate_text(llm, "The", temperature=2.5)
    
    # 4. Standard with Top-K = 3
    generate_text(llm, "The", temperature=1.5, top_k=3)
