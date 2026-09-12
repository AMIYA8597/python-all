"""
===========================================================================
Advanced LLM Prompt Engineering: A Comprehensive Guide & Interactive Lesson
===========================================================================

Mathematical Background:
At its core, a Large Language Model (LLM) approximates the probability 
distribution of a sequence of tokens. Given a sequence of tokens 
x_1, x_2, ..., x_t, the model computes the probability of the next token x_{t+1}:

    P(x_{t+1} | x_1, x_2, ..., x_t; \Theta)

where \Theta represents the parameters (weights) of the neural network.
Prompt Engineering is the systematic process of designing and optimizing 
the prefix (x_1, ..., x_t) to steer the output distribution towards the 
desired response.

Big-O Analysis of Generation:
- Time Complexity: O(N * L^2) per token for basic transformer inference, 
  where N is embedding dimension and L is sequence length (in vanilla self-attention).
- Space Complexity: O(L * d) to store KV-caches during generation, where d is the head dimension.

This interactive lesson covers:
1. Zero-shot Prompting
2. Few-shot Prompting
3. Chain-of-Thought (CoT) Prompting
4. ReAct (Reasoning and Acting) Patterns
5. Temperature and Top-P configuration impacts

Usage:
Run this file directly to execute the interactive test cases.
"""

import sys
import time
from typing import List, Dict, Any, Optional

def simulate_llm_response(prompt: str, temperature: float = 0.7) -> str:
    """
    Simulates a response from an LLM based on the prompt structure.
    In a real-world scenario, this would call an API like OpenAI, Anthropic, etc.
    
    Args:
        prompt (str): The input text to condition the model on.
        temperature (float): The sampling temperature.
        
    Returns:
        str: The simulated text response.
    """
    # Simple rule-based mock for educational purposes
    prompt_lower = prompt.lower()
    
    if "step by step" in prompt_lower or "let's think" in prompt_lower:
        return "Step 1: Analyze the input.\nStep 2: Formulate intermediate conclusion.\nStep 3: Final Answer is 42."
    elif "example:" in prompt_lower or "sentiment:" in prompt_lower:
        return "Positive."
    else:
        return "This is a generic zero-shot response."

class PromptTemplate:
    """
    A foundational class for constructing reusable prompt templates.
    """
    def __init__(self, template_str: str):
        """
        Initializes the PromptTemplate.
        
        Args:
            template_str (str): A string with placeholders like {variable}.
        """
        self.template_str = template_str
        
    def format(self, **kwargs: Any) -> str:
        """
        Injects variables into the template string.
        
        Args:
            **kwargs: Key-value pairs to replace in the template.
            
        Returns:
            str: The fully formatted prompt.
        """
        try:
            return self.template_str.format(**kwargs)
        except KeyError as e:
            raise ValueError(f"Missing required prompt variable: {e}")

def run_zero_shot_example() -> None:
    """Demonstrates basic zero-shot prompting."""
    print("\n--- 1. Zero-Shot Prompting ---")
    template = PromptTemplate("Classify the sentiment of this text: '{text}'")
    prompt = template.format(text="I love this new feature!")
    print(f"Prompt:\n{prompt}")
    response = simulate_llm_response(prompt)
    print(f"Response:\n{response}")

def run_few_shot_example() -> None:
    """Demonstrates few-shot prompting with examples."""
    print("\n--- 2. Few-Shot Prompting ---")
    few_shot_prompt = (
        "Text: The food was terrible.\nSentiment: Negative\n"
        "Text: The ambiance is wonderful.\nSentiment: Positive\n"
        "Text: It was okay, nothing special.\nSentiment: Neutral\n"
        "Text: The battery life is completely unacceptable!\nSentiment:"
    )
    print(f"Prompt:\n{few_shot_prompt}")
    response = simulate_llm_response(few_shot_prompt)
    print(f"Response:\n{response}")

def run_chain_of_thought_example() -> None:
    """Demonstrates Chain-of-Thought (CoT) prompting to elicit reasoning."""
    print("\n--- 3. Chain-of-Thought Prompting ---")
    template = PromptTemplate(
        "Question: {question}\n"
        "Let's think step by step to find the answer:"
    )
    prompt = template.format(question="If I have 5 apples and eat 2, then buy 3 more, how many do I have?")
    print(f"Prompt:\n{prompt}")
    response = simulate_llm_response(prompt)
    print(f"Response:\n{response}")

if __name__ == '__main__':
    print("Welcome to the Interactive Prompt Engineering Lesson!")
    time.sleep(1)
    
    run_zero_shot_example()
    time.sleep(1)
    
    run_few_shot_example()
    time.sleep(1)
    
    run_chain_of_thought_example()
    
    print("\nLesson complete. Experiment with different prompt structures to see how they influence the (simulated) LLM!")
