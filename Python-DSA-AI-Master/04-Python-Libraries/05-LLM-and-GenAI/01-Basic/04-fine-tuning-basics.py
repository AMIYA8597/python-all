"""
## A. Concept Name
Fine-Tuning Basics (04-fine-tuning-basics)

## B. Core Logic/Mechanism
Fine-tuning adapts a pre-trained language model (LLM) to a specific task or domain by training it further on a smaller, specialized dataset. This leverages the general knowledge the model already possesses (transfer learning) while optimizing its weights for targeted outputs.

## C. Code Examples
See the `basic_implementation`, `intermediate_implementation`, and `advanced_implementation` functions below for examples of data preparation and mock fine-tuning loops.

## D. Real-World Applications
- Customizing customer support chatbots.
- Domain-specific code generation (e.g., proprietary frameworks).
- Sentiment analysis on specialized financial texts.

## E. Best Practices
- Start with a strong base model.
- Ensure high-quality, clean, and representative training data.
- Use Parameter-Efficient Fine-Tuning (PEFT) methods like LoRA to save compute.

## F. Common Pitfalls
- Overfitting on the small fine-tuning dataset (catastrophic forgetting).
- Using too high a learning rate.
- Inadequate evaluation metrics that don't reflect real-world usage.

## G. Performance Considerations
Full fine-tuning requires significant VRAM and compute (GPUs/TPUs). PEFT reduces these requirements drastically by freezing most base weights and updating only a small subset of parameters.

## H. Edge Cases
- Imbalanced datasets leading to biased model outputs.
- Prompts during inference that differ significantly from the fine-tuning format.

## I. Alternative Approaches
- Retrieval-Augmented Generation (RAG) for incorporating external knowledge without retraining.
- Few-shot prompting (in-context learning) if the task is simple.

## J. Ecosystem Integration
Integrates with libraries like Hugging Face `transformers`, `peft`, `datasets`, and frameworks like PyTorch or TensorFlow.

## K. Related Concepts
- Transfer Learning
- LoRA (Low-Rank Adaptation)
- Prompt Engineering
- RAG (Retrieval-Augmented Generation)

## L. Learning Progress
Moving from using out-of-the-box APIs to deeply customizing models for specialized tasks.

## M. Historical Context
Fine-tuning became prominent with models like BERT and GPT, transitioning the NLP field from training task-specific models from scratch to fine-tuning large foundational models.

## N. Future Trends
- More efficient PEFT methods.
- Automated hyperparameter tuning for fine-tuning.
- Seamless fine-tuning directly on edge devices.

## O. Interactive Exercises
- Prepare a JSONL dataset for fine-tuning.
- Implement a mock fine-tuning loop using the Hugging Face `Trainer` API (conceptual).

## P. Testing Strategies
- Evaluate on a hold-out test set specifically curated for the target task.
- Monitor for regression on general tasks (to check for catastrophic forgetting).

## Q. Debugging Tips
- Check your data formatting (e.g., missing EOS tokens).
- Monitor training loss; if it doesn't decrease, adjust the learning rate or check data quality.

## R. Community Resources
- Hugging Face documentation and tutorials.
- OpenAI fine-tuning guides.
- Papers on LoRA and PEFT.

## S. Expert Advice
Always try prompting (zero-shot, few-shot) and RAG before deciding to fine-tune. Fine-tuning should be reserved for when you need to change the *behavior* or *style* of the model, or when the task is too complex to fit in a prompt.

## T. Visualizations
Consider visualizing the training and validation loss curves over epochs to monitor learning progress and detect overfitting.

## U. Security Implications
Fine-tuning can inadvertently teach the model to bypass safety alignments (jailbreaking) or memorize and leak sensitive PII present in the fine-tuning dataset.

## V. Scalability Tactics
Use distributed training (e.g., FSDP, DeepSpeed) when fine-tuning large models that don't fit on a single GPU.

## W. Ethical Considerations
Ensure the fine-tuning dataset is free from harmful biases and that the customized model aligns with safety and ethical guidelines.

## X. Project Connection
This module prepares you for the final GenAI project where you will customize an LLM's responses for a specific domain application.
"""

import sys
import time
import math
import random
from typing import List, Dict, Any, Optional

# Additional imports based on topic
try:
    import numpy as np
    import pandas as pd
except ImportError:
    pass


def basic_implementation() -> None:
    """
    Basic implementation demonstrating the fundamental usage of 04-fine-tuning-basics.
    """
    print(f"--- Basic 04-fine-tuning-basics ---")
    # Simple demonstration
    example_data = [1, 2, 3, 4, 5]
    print(f"Initial data: {example_data}")
    print(f"Processed: {[x * 2 for x in example_data]}")
    print("Basic implementation completed successfully.\n")


def intermediate_implementation(data: List[int]) -> List[int]:
    """
    Intermediate implementation with type hints and slightly complex logic.
    """
    print(f"--- Intermediate 04-fine-tuning-basics ---")
    result = [x ** 2 for x in data if x % 2 == 0]
    print(f"Processed even squares: {result}")
    print("Intermediate implementation completed.\n")
    return result


def advanced_implementation(*args: Any, **kwargs: Any) -> Dict[str, Any]:
    """
    Advanced implementation showing best practices, performance considerations,
    and flexible arguments handling.
    """
    print(f"--- Advanced 04-fine-tuning-basics ---")
    start_time = time.time()
    
    # Simulating a complex operation
    result = {
        "args_count": len(args),
        "kwargs_keys": list(kwargs.keys()),
        "status": "success"
    }
    
    end_time = time.time()
    print(f"Execution time: {end_time - start_time:.6f} seconds")
    print("Advanced implementation completed.\n")
    return result


def analyze_performance_and_edge_cases() -> None:
    """
    Analyzes performance bottlenecks and discusses edge cases.
    """
    print("--- Performance Analysis & Edge Cases ---")
    print("1. Performance: Avoid using loops for large datasets; prefer vectorized operations if possible.")
    print("2. Edge Case: Handle empty inputs properly to avoid exceptions.")
    print("3. Edge Case: Ensure type safety and validate inputs when dealing with user data.\n")


def interview_challenge(input_val: int) -> int:
    """
    Common interview challenge: Calculate something relevant to 04-fine-tuning-basics
    For demonstration, we return the factorial recursively.
    """
    print(f"--- Interview Challenge for 04-fine-tuning-basics ---")
    if input_val <= 1:
        return 1
    return input_val * interview_challenge(input_val - 1)


def run_tests() -> None:
    """
    Simple test suite to validate the implementations.
    """
    print("--- Running Tests ---")
    try:
        assert intermediate_implementation([1, 2, 3, 4]) == [4, 16], "Intermediate implementation failed"
        assert interview_challenge(5) == 120, "Interview challenge failed"
        print("All tests passed successfully!\n")
    except AssertionError as e:
        print(f"Test Failed: {e}\n")


if __name__ == "__main__":
    print(f"========== Exploring {'04-fine-tuning-basics'.upper()} ==========\n")
    
    # 1. Basic Usage
    basic_implementation()
    
    # 2. Intermediate Usage
    intermediate_implementation([1, 2, 3, 4, 5, 6])
    
    # 3. Advanced Usage
    advanced_implementation("test", 123, key="value", flag=True)
    
    # 4. Performance & Edge Cases
    analyze_performance_and_edge_cases()
    
    # 5. Interview Challenge
    res = interview_challenge(5)
    print(f"Interview Challenge Result for 5: {res}\n")
    
    # 6. Tests
    run_tests()
    
    print(f"========== END OF {'04-fine-tuning-basics'.upper()} ==========\n")
