"""
LLMOps & GenAIOps: Evaluation and Tracing Example

This script demonstrates basic concepts of LLMOps, including:
1. Connecting to an LLM provider (mocked for educational purposes).
2. Tracing the execution of an LLM call.
3. Evaluating the LLM output using simple heuristics and similarity scores.

Prerequisites:
    pip install rapidfuzz # using rapidfuzz as a simple evaluation metric
"""

import time
import logging
from typing import Dict, Any
from rapidfuzz import fuzz

# Setup basic logging for observability
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class MockLLM:
    """A mock LLM class to simulate generating responses."""
    def __init__(self, model_name="mock-gpt-3.5"):
        self.model_name = model_name

    def generate(self, prompt: str) -> str:
        # Simulate network latency
        time.sleep(1)
        
        # Simple rule-based mock responses based on keywords
        prompt_lower = prompt.lower()
        if "capital of france" in prompt_lower:
            return "The capital of France is Paris."
        elif "machine learning" in prompt_lower:
            return "Machine learning is a subset of AI focused on building systems that learn from data."
        else:
            return "I am a helpful AI assistant. I don't know the answer to that."

def trace_llm_call(llm_func):
    """
    A decorator to trace LLM calls.
    In real LLMOps (e.g., using LangSmith, TruLens, or Phoenix), this captures
    the prompt, completion, latency, and tokens.
    """
    def wrapper(*args, **kwargs):
        start_time = time.time()
        
        # Log input prompt (Tracing Request)
        prompt = kwargs.get('prompt') or (args[1] if len(args)>1 else None)
        logger.info(f"[TRACE] LLM Request: {prompt}")
        
        # Execute LLM
        response = llm_func(*args, **kwargs)
        
        latency = time.time() - start_time
        
        # Log output (Tracing Response)
        logger.info(f"[TRACE] LLM Response: {response}")
        logger.info(f"[TRACE] Latency: {latency:.2f} seconds")
        
        # Add metadata to the result for further analysis
        return {
            "prompt": prompt,
            "response": response,
            "latency_seconds": latency,
            # In a real app, you would include token usage here
            "tokens_used": len(response.split()) 
        }
    return wrapper

# Apply tracing to our mock LLM
MockLLM.generate_traced = trace_llm_call(MockLLM.generate)

def evaluate_response(result: Dict[str, Any], ground_truth: str) -> Dict[str, Any]:
    """
    Evaluate the LLM response against a ground truth.
    Real LLMOps uses LLM-as-a-judge (e.g., RAGAS) or complex metrics.
    Here we use a simple string similarity (RapidFuzz).
    """
    response = result["response"]
    
    # Calculate Similarity Score (0 to 100)
    similarity_score = fuzz.ratio(response.lower(), ground_truth.lower())
    
    # Simple heuristic checks (e.g., checking for hallucinations or toxicity)
    is_safe = "hate" not in response.lower()
    
    eval_results = {
        "similarity_score": similarity_score,
        "is_safe": is_safe,
        "passed": similarity_score > 80 and is_safe
    }
    logger.info(f"[EVAL] Score: {similarity_score:.2f}/100, Passed: {eval_results['passed']}")
    return eval_results

if __name__ == "__main__":
    print("--- LLMOps & GenAIOps Demonstration ---\n")
    
    llm = MockLLM()
    
    # Test Case 1
    test_prompt = "What is the capital of France?"
    expected_answer = "Paris is the capital of France."
    
    print("Executing LLM Call...")
    result = llm.generate_traced(prompt=test_prompt)
    
    print("\nEvaluating Response...")
    evaluation = evaluate_response(result, expected_answer)
    
    print("\nSummary:")
    print(f"Prompt: {result['prompt']}")
    print(f"Response: {result['response']}")
    print(f"Evaluation: {'PASSED ✅' if evaluation['passed'] else 'FAILED ❌'}")
    print(f"Latency: {result['latency_seconds']:.2f}s")
