"""
Module: 05-ethics-bias
Description: Comprehensive textbook-grade lesson on Ethics and Bias in Large Language Models (LLMs) and Generative AI.

Learning Objectives:
1. Understand the theoretical and mathematical foundations of bias in machine learning and NLP.
2. Implement metrics to measure fairness (e.g., Demographic Parity, Equalized Odds).
3. Detect stereotypical biases in word embeddings and language models.
4. Apply mitigation techniques such as projection-based debiasing.
5. Analyze the computational complexity of fairness algorithms.

Mathematical Background:
Bias in NLP often manifests in semantic representations. Suppose we have a vector space
representation of words, where each word is represented by a vector $w \\in \\mathbb{R}^d$.
A bias direction can be defined by the difference between two definitional vectors, e.g.,
$v_b = w_{he} - w_{she}$.
To 'neutralize' a conceptually neutral word's representation (e.g., 'doctor') with respect 
to the bias direction, we subtract its projection onto $v_b$:
    $w' = w - \\frac{\\langle w, v_b \\rangle}{\\|v_b\\|^2} v_b$

In classification tasks (e.g., LLM-based text moderation), we measure fairness using
metrics like Demographic Parity. Let A be a protected attribute (e.g., gender, race) and $\\hat{Y}$
be the predicted outcome. Demographic Parity requires:
    $P(\\hat{Y} = 1 | A = 0) = P(\\hat{Y} = 1 | A = 1)$
The disparity is simply $|P(\\hat{Y} = 1 | A = 0) - P(\\hat{Y} = 1 | A = 1)|$.

Big-O Analysis:
- Measuring cosine similarity for bias in embeddings: O(d) where d is the embedding dimension.
- Neutralizing bias for N vocabulary words: O(N * d).
- Calculating Demographic Parity for a dataset of size M: O(M) time and O(1) space.
"""

import sys
import time
import math
import random
from typing import List, Dict, Any, Optional, Tuple

try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False


# ============================================================================
# 1. FAIRNESS METRICS (DEMOGRAPHIC PARITY)
# ============================================================================

def calculate_demographic_parity_difference(
    predictions: List[int],
    protected_attributes: List[int]
) -> float:
    """
    Calculates the Demographic Parity Difference (DPD).
    
    Demographic Parity ensures that the positive prediction rate is equal across 
    different groups of a protected attribute (e.g., A=0 and A=1).
    
    Time Complexity: O(M) where M is the number of samples.
    Space Complexity: O(1) beyond the input arrays.
    
    Args:
        predictions (List[int]): Binary predictions (0 or 1).
        protected_attributes (List[int]): Binary protected attribute (0 or 1).
        
    Returns:
        float: The absolute difference in positive prediction rates.
        
    Raises:
        ValueError: If predictions and protected_attributes lengths mismatch.
    """
    if len(predictions) != len(protected_attributes):
        raise ValueError("Lengths of predictions and protected_attributes must match.")
        
    if not predictions:
        return 0.0

    group_0_pos = 0
    group_0_total = 0
    group_1_pos = 0
    group_1_total = 0

    # Exhaustive inline comments:
    # We iterate through all instances to count the totals and positive outcomes
    # for each demographic group.
    for pred, attr in zip(predictions, protected_attributes):
        if attr == 0:
            group_0_total += 1
            if pred == 1:
                group_0_pos += 1
        elif attr == 1:
            group_1_total += 1
            if pred == 1:
                group_1_pos += 1

    rate_0 = (group_0_pos / group_0_total) if group_0_total > 0 else 0.0
    rate_1 = (group_1_pos / group_1_total) if group_1_total > 0 else 0.0

    return abs(rate_0 - rate_1)


# ============================================================================
# 2. EMBEDDING BIAS DETECTION & MITIGATION
# ============================================================================

class WordEmbeddingDebiaser:
    """
    A class to demonstrate and mitigate bias in vector representations of text.
    
    Language models learn representations (embeddings) from large corpora which
    inherently contain human biases. This class uses a projection-based method 
    to neutralize stereotypical biases.
    """

    def __init__(self, embeddings: Dict[str, List[float]]):
        """
        Initializes the WordEmbeddingDebiaser with a given vocabulary and embeddings.
        
        Args:
            embeddings (Dict[str, List[float]]): A dictionary mapping words to their vectors.
        """
        self.embeddings = embeddings

    def _cosine_similarity(self, vec_a: List[float], vec_b: List[float]) -> float:
        """
        Helper method to compute cosine similarity between two vectors.
        
        Formula: (a . b) / (||a|| * ||b||)
        """
        dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
        norm_a = math.sqrt(sum(a * a for a in vec_a))
        norm_b = math.sqrt(sum(b * b for b in vec_b))
        
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return dot_product / (norm_a * norm_b)

    def identify_bias_direction(self, word1: str, word2: str) -> Optional[List[float]]:
        """
        Calculates the bias direction based on two definitional words (e.g., 'he' and 'she').
        
        Time Complexity: O(d) where d is the embedding dimension.
        Space Complexity: O(d) to store the result vector.
        
        Args:
            word1 (str): The first definitional word.
            word2 (str): The second definitional word.
            
        Returns:
            Optional[List[float]]: The bias direction vector, or None if words are missing.
        """
        if word1 not in self.embeddings or word2 not in self.embeddings:
            print("Error: Definitional words not found in the embedding dictionary.")
            return None
            
        vec1 = self.embeddings[word1]
        vec2 = self.embeddings[word2]
        
        # Bias direction v_b = w_1 - w_2
        bias_direction = [v1 - v2 for v1, v2 in zip(vec1, vec2)]
        return bias_direction

    def measure_bias(self, target_word: str, bias_direction: List[float]) -> float:
        """
        Measures the bias of a target word by calculating its cosine similarity with the bias direction.
        
        Args:
            target_word (str): The word to measure.
            bias_direction (List[float]): The calculated bias vector.
            
        Returns:
            float: Cosine similarity score. Positive means closer to word1, negative means closer to word2.
        """
        if target_word not in self.embeddings:
            return 0.0
            
        target_vec = self.embeddings[target_word]
        return self._cosine_similarity(target_vec, bias_direction)

    def neutralize_bias(self, target_word: str, bias_direction: List[float]) -> Optional[List[float]]:
        """
        Neutralizes the bias of a conceptually neutral target word by removing its 
        projection along the bias direction.
        
        Formula: w' = w - ( (w · v_b) / ||v_b||^2 ) * v_b
        
        Time Complexity: O(d)
        Space Complexity: O(d)
        
        Args:
            target_word (str): The word to neutralize.
            bias_direction (List[float]): The bias vector to project away from.
            
        Returns:
            Optional[List[float]]: The new debiased embedding vector.
        """
        if target_word not in self.embeddings:
            return None
            
        w = self.embeddings[target_word]
        v_b = bias_direction
        
        dot_w_vb = sum(wi * vbi for wi, vbi in zip(w, v_b))
        norm_vb_sq = sum(vbi * vbi for vbi in v_b)
        
        if norm_vb_sq == 0:
            return w
            
        projection_scalar = dot_w_vb / norm_vb_sq
        
        # Subtract the projection from the original vector
        w_prime = [wi - (projection_scalar * vbi) for wi, vbi in zip(w, v_b)]
        
        # Update the embedding representation internally
        self.embeddings[target_word] = w_prime
        
        return w_prime


# ============================================================================
# 3. INTERVIEW CHALLENGE: COUNTERFACTUAL DATA AUGMENTATION
# ============================================================================

def counterfactual_augmentation(sentence: str, flip_dict: Dict[str, str]) -> str:
    """
    Common Interview Challenge: Counterfactual Data Augmentation (CDA).
    
    Problem Statement: 
    Given a string representing a sentence and a dictionary of words to flip 
    (e.g., {'he': 'she', 'man': 'woman', 'him': 'her'}), return a new string 
    where all occurrences of words in the dictionary are replaced by their counterpart.
    This technique is often used to balance datasets for training LLMs.
    
    Constraint: Perform this in O(N) time where N is the length of the string, 
    and maintain the original casing (basic capitalization preservation).
    
    Args:
        sentence (str): The input sentence to augment.
        flip_dict (Dict[str, str]): Dictionary mapping words to their counterfactuals.
        
    Returns:
        str: The counterfactually augmented sentence.
    """
    # Create an extended dictionary to handle bidirectional flips if needed, 
    # but here we strictly follow the flip_dict provided.
    words = sentence.split(' ')
    augmented_words = []
    
    for word in words:
        # Strip punctuation for matching, but keep it for reconstruction
        clean_word = "".join(char for char in word if char.isalpha())
        punctuation_left = word[:word.find(clean_word)] if clean_word else ""
        punctuation_right = word[word.find(clean_word)+len(clean_word):] if clean_word else word
        
        is_title = clean_word.istitle()
        is_upper = clean_word.isupper()
        
        lower_clean = clean_word.lower()
        
        if lower_clean in flip_dict:
            new_clean = flip_dict[lower_clean]
            # Restore casing
            if is_upper:
                new_clean = new_clean.upper()
            elif is_title:
                new_clean = new_clean.title()
                
            augmented_words.append(f"{punctuation_left}{new_clean}{punctuation_right}")
        else:
            augmented_words.append(word)
            
    return " ".join(augmented_words)


# ============================================================================
# 4. TESTS & EXECUTION
# ============================================================================

def run_tests() -> None:
    """
    A comprehensive suite of tests to validate fairness metrics, debiasing, and 
    counterfactual augmentation.
    """
    print("--- Running Tests ---")
    
    # Test 1: Demographic Parity
    preds = [1, 1, 0, 0, 1, 0]
    attrs = [0, 0, 0, 1, 1, 1]
    # Group 0: 3 items, 2 pos -> rate = 2/3
    # Group 1: 3 items, 1 pos -> rate = 1/3
    # DPD = |2/3 - 1/3| = 1/3 ~ 0.3333
    dpd = calculate_demographic_parity_difference(preds, attrs)
    assert math.isclose(dpd, 0.3333333, rel_tol=1e-5), f"Failed DPD test. Got {dpd}"
    print("[PASS] Demographic Parity Calculation")
    
    # Test 2: Word Embedding Debiasing
    mock_embeddings = {
        "he": [1.0, 0.0, 0.0],
        "she": [-1.0, 0.0, 0.0],
        "doctor": [0.5, 1.0, 0.2],   # Biased towards 'he' (positive X)
        "nurse": [-0.5, 0.8, -0.1]   # Biased towards 'she' (negative X)
    }
    debiaser = WordEmbeddingDebiaser(mock_embeddings)
    bias_dir = debiaser.identify_bias_direction("he", "she") # [2.0, 0.0, 0.0]
    
    assert bias_dir == [2.0, 0.0, 0.0], "Failed to identify bias direction."
    
    # Measure initial bias
    initial_doc_bias = debiaser.measure_bias("doctor", bias_dir)
    assert initial_doc_bias > 0, "Doctor should initially be positively biased towards 'he'"
    
    # Neutralize
    debiaser.neutralize_bias("doctor", bias_dir)
    new_doc_bias = debiaser.measure_bias("doctor", bias_dir)
    assert math.isclose(new_doc_bias, 0.0, abs_tol=1e-5), f"Failed to neutralize bias. Got {new_doc_bias}"
    print("[PASS] Word Embedding Bias Neutralization")
    
    # Test 3: Counterfactual Data Augmentation
    sentence = "He is a great leader, but she is a better programmer."
    flip_dict = {"he": "she", "she": "he"}
    augmented = counterfactual_augmentation(sentence, flip_dict)
    expected = "She is a great leader, but he is a better programmer."
    assert augmented == expected, f"Failed CDA. Got: {augmented}"
    
    sentence2 = "He yelled: 'Stop!'"
    augmented2 = counterfactual_augmentation(sentence2, flip_dict)
    expected2 = "She yelled: 'Stop!'"
    assert augmented2 == expected2, f"Failed CDA with punctuation. Got: {augmented2}"
    print("[PASS] Counterfactual Data Augmentation")
    
    print("All tests passed successfully!\n")


if __name__ == "__main__":
    print(f"{'='*60}")
    print(f"========== Exploring ETHICS AND BIAS IN LLMs ==========")
    print(f"{'='*60}\n")
    
    print("1. Demographic Parity (Fairness Metric)")
    print("-" * 40)
    # Simulating LLM classification output (e.g., Toxic = 1, Safe = 0)
    # A=0: Written by demographic A, A=1: Written by demographic B
    simulated_preds = [random.choice([0, 1]) for _ in range(100)]
    simulated_attrs = [random.choice([0, 1]) for _ in range(100)]
    dpd_score = calculate_demographic_parity_difference(simulated_preds, simulated_attrs)
    print(f"Calculated Demographic Parity Difference on random dataset: {dpd_score:.4f}")
    print("Ideal fairness would be a DPD of 0.0.\n")
    
    print("2. Word Embedding Projection Debiasing")
    print("-" * 40)
    mock_model_embeddings = {
        "man": [0.8, 0.2, 0.1],
        "woman": [-0.8, 0.3, 0.1],
        "engineer": [0.6, 0.9, 0.4], # Leans towards 'man'
        "teacher": [-0.5, 0.8, 0.6]  # Leans towards 'woman'
    }
    debiaser_demo = WordEmbeddingDebiaser(mock_model_embeddings)
    v_bias = debiaser_demo.identify_bias_direction("man", "woman")
    print(f"Bias Direction (man - woman): {v_bias}")
    
    b_eng_initial = debiaser_demo.measure_bias("engineer", v_bias)
    print(f"Initial Bias of 'engineer' (Cosine Similarity to bias dir): {b_eng_initial:.4f}")
    
    debiaser_demo.neutralize_bias("engineer", v_bias)
    b_eng_final = debiaser_demo.measure_bias("engineer", v_bias)
    print(f"Final Bias of 'engineer' after Neutralization: {b_eng_final:.4f}")
    print("Note how the bias similarity is reduced practically to zero.\n")
    
    print("3. Counterfactual Data Augmentation")
    print("-" * 40)
    original_text = "The doctor asked the nurse to help him with the patient."
    flips = {"doctor": "nurse", "nurse": "doctor", "him": "her"}
    new_text = counterfactual_augmentation(original_text, flips)
    print(f"Original: {original_text}")
    print(f"Augmented: {new_text}\n")
    
    print("4. Executing Test Suite")
    print("-" * 40)
    run_tests()
    
    print(f"========== END OF LESSON ==========\n")
