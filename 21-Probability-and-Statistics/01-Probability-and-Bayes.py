"""
# 01 - Probability: Distributions, Expected Value, and Bayes' Theorem

## A. Concept Name
Probability Theory, Random Variables, Expected Value, and Bayes' Theorem for Machine Learning.

## B. One-Sentence Definition
Probability theory provides the mathematical framework for quantifying uncertainty; in AI, every prediction a model makes is actually just a probability distribution over possible answers, updated continuously using Bayes' Theorem.

## C. Why Does This Exist?
Machine Learning models don't "know" anything with 100% certainty.
When an LLM generates the next word, it doesn't just pick one word. It outputs a probability distribution (e.g., "apple": 80%, "banana": 15%, "car": 5%).
When a spam filter flags an email, it's calculating `P(Spam | Words)`.
Understanding probability is the key to understanding how AI handles noise, uncertainty, and decision-making.

## D. Intuition & Real-World Analogy
Imagine you are trying to guess if it will rain today.
- **Prior Probability**: You know it rains 10% of the time in this city. `P(Rain) = 0.1`
- **Evidence**: You look out the window and see dark clouds. 
- **Likelihood**: When it rains, it's almost always cloudy. `P(Clouds | Rain) = 0.9`
- **Posterior Probability (Bayes' Theorem)**: What is the probability of rain GIVEN that you see clouds? `P(Rain | Clouds) = ?`

AI models (especially Naive Bayes classifiers) use this exact logic to update their beliefs when they see new data.

## E. Core Mathematical Concepts

### 1. Random Variables & Expected Value
A Random Variable represents a numerical outcome of an uncertain event.
The Expected Value (E[X]) is the long-term average.
Formula: `E[X] = sum(x * P(x))`
In AI: Reinforcement Learning (like AlphaGo) is entirely based on maximizing the *Expected Value* of future rewards.

### 2. Conditional Probability
The probability of event A happening, given that event B has already happened.
Formula: `P(A | B) = P(A and B) / P(B)`
In AI: Language models are literally calculating `P(Word_N | Word_1, Word_2, ... Word_N-1)`.

### 3. Bayes' Theorem
A principled way to update your beliefs based on new evidence.
Formula: `P(A | B) = [P(B | A) * P(A)] / P(B)`
Where:
- `P(A)` is the Prior (what you believed before)
- `P(B | A)` is the Likelihood (how likely the evidence is, if your hypothesis is true)
- `P(B)` is the Evidence (how common the evidence is overall)
- `P(A | B)` is the Posterior (your updated belief)

## F. Common Mistakes & Anti-Patterns
1. **The Base Rate Fallacy**: Forgetting to account for the Prior `P(A)`. If a disease affects 1 in 10,000 people, and a test is 99% accurate, a positive test STILL means you probably don't have the disease, because the base rate is so overwhelmingly low! (Most positives will be false positives).
2. **Confusing P(A|B) with P(B|A)**: The probability that a person is pregnant given they are a woman is very different from the probability that a person is a woman given they are pregnant.

## G. Interview Connection
**Q: "Explain how a Naive Bayes classifier works."**
A: "It applies Bayes' Theorem to predict the class of a data point based on its features. It calculates the posterior probability of each class given the features. It's called 'naive' because it makes the strong assumption that all features are completely independent of each other given the class, which simplifies the math to just multiplying probabilities."

## H. Implementation & Guided Practice
"""

# ==========================================
# 1. Calculating Expected Value
# ==========================================
def demonstrate_expected_value():
    print("--- 1. Expected Value (RL Foundation) ---")
    
    # Imagine an AI playing a game. It has 3 possible moves.
    # Move A: 50% chance to get +10 points, 50% chance to get 0.
    # Move B: 100% chance to get +4 points.
    # Move C: 10% chance to get +100 points, 90% chance to lose -5.
    
    expected_value_A = (0.5 * 10) + (0.5 * 0)
    expected_value_B = (1.0 * 4)
    expected_value_C = (0.1 * 100) + (0.9 * -5)
    
    print(f"EV of Move A: {expected_value_A}")
    print(f"EV of Move B: {expected_value_B}")
    print(f"EV of Move C: {expected_value_C}")
    print("The AI will choose Move C because it maximizes Expected Value, even though it's risky!")


# ==========================================
# 2. Bayes' Theorem in Action (Medical Test)
# ==========================================
def demonstrate_bayes_theorem():
    print("\n--- 2. Bayes' Theorem (The Base Rate Fallacy) ---")
    
    # Scenario: A rare disease affects 0.1% of the population.
    # The test for the disease is 99% accurate.
    # If a random person tests positive, what is the ACTUAL probability they have it?
    
    p_disease = 0.001           # P(Disease) -> The Prior
    p_no_disease = 0.999        # P(No Disease)
    
    p_positive_given_disease = 0.99       # P(Pos | Disease) -> True Positive Rate
    p_positive_given_no_disease = 0.01    # P(Pos | No Disease) -> False Positive Rate
    
    # Calculate Total Probability of testing positive P(Positive)
    # You can test positive by HAVING the disease, OR by NOT having it (false positive)
    p_positive = (p_positive_given_disease * p_disease) + (p_positive_given_no_disease * p_no_disease)
    
    # Bayes Theorem: P(Disease | Positive) = [P(Positive | Disease) * P(Disease)] / P(Positive)
    p_disease_given_positive = (p_positive_given_disease * p_disease) / p_positive
    
    print(f"Disease Prevalence (Prior): {p_disease * 100}%")
    print(f"Test Accuracy: {p_positive_given_disease * 100}%")
    print(f"Chance you actually have the disease if you test positive: {p_disease_given_positive * 100:.2f}% !!")
    print("Why so low? Because the disease is so rare, the 1% false positives completely outnumber the true positives.")


# ==========================================
# 3. Naive Bayes Classifier (Spam Filter)
# ==========================================
def naive_bayes_spam_filter():
    print("\n--- 3. Toy Naive Bayes Spam Filter ---")
    
    # We want to know: P(Spam | Contains "Win", "Money")
    
    # 1. Priors
    p_spam = 0.2
    p_ham = 0.8
    
    # 2. Likelihoods (Training Data)
    # P(Word | Class)
    p_win_given_spam = 0.6
    p_win_given_ham = 0.05
    
    p_money_given_spam = 0.8
    p_money_given_ham = 0.1
    
    # 3. Applying Bayes Theorem (with the "Naive" assumption)
    # We assume "Win" and "Money" appear independently.
    # So P("Win", "Money" | Spam) = P("Win" | Spam) * P("Money" | Spam)
    
    # Numerator for Spam
    score_spam = p_spam * (p_win_given_spam * p_money_given_spam)
    
    # Numerator for Ham
    score_ham = p_ham * (p_win_given_ham * p_money_given_ham)
    
    # Normalize to get actual probabilities (they must sum to 1.0)
    total_score = score_spam + score_ham
    prob_spam = score_spam / total_score
    prob_ham = score_ham / total_score
    
    print(f"Email contains: 'Win', 'Money'")
    print(f"Probability it is SPAM: {prob_spam * 100:.1f}%")
    print(f"Probability it is HAM : {prob_ham * 100:.1f}%")


## I. Active Recall Questions
"""
1. In Reinforcement Learning, what mathematical concept is an agent trying to maximize?
   *Answer: Expected Value (Expected Future Reward).*
2. What makes a Naive Bayes classifier "naive"?
   *Answer: It assumes that every feature is completely independent of every other feature given the class. In reality, the words "Win" and "Money" often appear together, but Naive Bayes ignores this correlation.*
3. What is the Base Rate Fallacy?
   *Answer: Ignoring the prior probability (the base rate) when evaluating evidence, leading to vastly incorrect conclusions (e.g., overestimating the chance of having a rare disease after a positive test).*
"""

if __name__ == "__main__":
    print("========== PROBABILITY & BAYES MASTERCLASS ==========\n")
    demonstrate_expected_value()
    demonstrate_bayes_theorem()
    naive_bayes_spam_filter()
    print("\n========== MASTERCLASS COMPLETE ==========")
