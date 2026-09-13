# 04-genai-app.py
"""
Generative AI Basics

This script demonstrates text generation using a simple Markov Chain model.
While modern GenAI uses deep neural networks (like Transformers), Markov chains
provide a fundamental understanding of predicting the next token based on context.

Topics Covered:
1. Building a state transition dictionary (n-grams).
2. Generating sequences step-by-step.
"""

import random

class MarkovChainGenerator:
    def __init__(self):
        self.transitions = {}

    def train(self, text):
        """Trains the Markov Chain on the provided text."""
        words = text.split()
        for i in range(len(words) - 1):
            current_word = words[i]
            next_word = words[i + 1]
            if current_word not in self.transitions:
                self.transitions[current_word] = []
            self.transitions[current_word].append(next_word)

    def generate(self, start_word, length=10):
        """Generates text starting with the given word."""
        if start_word not in self.transitions:
            return "Start word not found in training data."
            
        current_word = start_word
        result = [current_word]
        
        for _ in range(length - 1):
            if current_word in self.transitions:
                next_word = random.choice(self.transitions[current_word])
                result.append(next_word)
                current_word = next_word
            else:
                break
                
        return " ".join(result)

if __name__ == "__main__":
    training_text = """
    generative artificial intelligence is a type of ai that can create new content.
    generative models learn the patterns and structure of their input data and then
    generate new data that has similar characteristics.
    artificial intelligence is transforming the world.
    """
    
    print("Training Markov Chain...")
    gen = MarkovChainGenerator()
    gen.train(training_text.lower())
    
    print("\nGenerated Text (Start word: 'generative'):")
    # Set seed for reproducible results if desired
    # random.seed(42) 
    generated = gen.generate("generative", length=12)
    print(generated)
