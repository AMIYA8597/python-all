# 01 - AI Evaluation & Benchmarking

## Prerequisites
- Basic understanding of machine learning evaluation metrics (Accuracy, Precision, Recall).
- Familiarity with Large Language Models (LLMs) and their use cases.
- Python programming skills.

## Objectives
- Understand the difference between offline and online AI evaluation.
- Learn about common benchmarks for LLMs (MMLU, HumanEval, HELM, etc.).
- Build a fundamental evaluation pipeline.

## Intuition / Theory

### Offline vs. Online Evaluation
**Offline Evaluation** is performed before deploying a model to production. It uses static datasets with ground-truth labels (or established reference answers) to measure model performance.
- *Pros:* Safe, reproducible, no impact on real users.
- *Cons:* May not perfectly represent real-world distribution or user behavior (data drift).

**Online Evaluation** occurs in a live production environment. It relies on user telemetry, implicit signals (e.g., click-through rate, session length), and explicit feedback (e.g., thumbs up/down).
- *Pros:* Captures real user behavior and true business value.
- *Cons:* Risk of exposing users to sub-optimal models, harder to attribute causality.

### LLM Benchmarking
Benchmarking involves evaluating LLMs on standardized tasks to compare them against one another.
- **MMLU (Massive Multitask Language Understanding):** Tests knowledge across STEM, humanities, etc.
- **HumanEval:** Evaluates code generation capabilities (Python).
- **HELM (Holistic Evaluation of Language Models):** A comprehensive framework evaluating accuracy, robustness, fairness, bias, and toxicity.

## Code Examples

### Simulating Offline Evaluation (Accuracy)
```python
def evaluate_offline(model_predictions, ground_truths):
    """
    Evaluates exact match accuracy of model predictions against ground truth.
    """
    if len(model_predictions) != len(ground_truths):
        raise ValueError("Mismatched lengths between predictions and ground truths.")
    
    correct = 0
    for pred, truth in zip(model_predictions, ground_truths):
        if pred.strip().lower() == truth.strip().lower():
            correct += 1
            
    accuracy = correct / len(ground_truths) if ground_truths else 0
    return accuracy

predictions = ["Paris", "4", "Blue"]
truths = ["Paris", "4", "Green"]
print(f"Accuracy: {evaluate_offline(predictions, truths):.2f}") # Output: 0.67
```

## Interview Questions
1. **What is the primary difference between offline and online evaluation for LLMs?**
   *Answer:* Offline evaluation happens pre-deployment using static datasets and metrics, ensuring safety and reproducibility. Online evaluation happens post-deployment using live user data (A/B testing, user feedback), reflecting real-world performance.
2. **Why is it challenging to evaluate generative AI models compared to traditional classification models?**
   *Answer:* Generative models produce open-ended text where there isn't a single "correct" answer. Exact match or simple overlap metrics fall short, necessitating semantic similarity, human evaluation, or LLM-as-a-judge approaches.
3. **What does MMLU measure?**
   *Answer:* MMLU measures a model's multitask accuracy in zero-shot and few-shot settings across a wide array of subjects (e.g., mathematics, history, law) to test general knowledge and problem-solving.
