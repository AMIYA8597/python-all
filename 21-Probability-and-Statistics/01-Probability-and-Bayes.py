"""
# ==============================================================================
# LABORATORY: PROBABILITY & STATISTICS (BAYES' THEOREM)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A junior developer builds a spam filter using 'if/else' statements. If an 
# email contains the word "Viagra", they flag it as spam. The CEO's email 
# about a Pfizer stock purchase gets blocked. 
#
# A senior AI engineer understands "Probabilistic Machine Learning". They use 
# Bayes' Theorem to calculate the *probability* that an email is spam, GIVEN 
# that it contains the word "Viagra", factoring in the Baseline Probability 
# (Prior) that any random email is spam. If the calculated probability is 99%, 
# it gets blocked. If the email contains "Viagra" but also "Q3 Earnings" and 
# "Stock", the Naive Bayes algorithm mathematically lowers the spam probability 
# to 2%, letting it through. AI does not deal in absolute certainties; it deals 
# strictly in conditional probabilities.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master Conditional Probability P(A|B).
# - Execute Bayes' Theorem mathematics.
# - Architect a Probabilistic reasoning engine.
#
# ==============================================================================
"""

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE BUSINESS LOGIC (BAYESIAN MATHEMATICS)
# ==============================================================================
class BayesianMathematics:
    
    @staticmethod
    def simulate_bayes_theorem():
        """
        [SECURE] Bayes' Theorem.
        Formula: P(A|B) = [P(B|A) * P(A)] / P(B)
        
        Scenario: Medical Testing
        A disease affects 1% of the population. A test is 99% accurate.
        If you test POSITIVE, what is the actual probability you HAVE the disease?
        (Spoiler: It is NOT 99%).
        """
        print("  [INIT] Calculating Conditional Probability via Bayes' Theorem...")
        
        # 1. P(A): The Prior Probability (Base rate of the disease)
        # Only 1% of people actually have it.
        p_disease = 0.01
        p_no_disease = 0.99
        
        # 2. P(B|A): The Likelihood (True Positive Rate)
        # If you HAVE the disease, the test is 99% likely to be positive.
        p_positive_given_disease = 0.99
        
        # 3. P(B|Not A): The False Positive Rate
        # If you DO NOT have the disease, the test is still 5% likely to be positive (Error).
        p_positive_given_no_disease = 0.05
        
        # 4. P(B): The Marginal Likelihood (Total Probability of testing positive)
        # You can test positive by actually having it, OR by getting a false positive.
        p_positive = (p_positive_given_disease * p_disease) + (p_positive_given_no_disease * p_no_disease)
        
        # 5. P(A|B): The Posterior Probability (What we actually care about)
        # Given that you tested positive, what is the probability you actually have it?
        p_disease_given_positive = (p_positive_given_disease * p_disease) / p_positive
        
        print("\n  [EXECUTION] Medical Test Results:")
        print(f"  -> Prior Probability (Disease):   {p_disease * 100:.1f}%")
        print(f"  -> Test Accuracy (True Pos):      {p_positive_given_disease * 100:.1f}%")
        print(f"  -> False Positive Rate:           {p_positive_given_no_disease * 100:.1f}%")
        
        print("\n  [MATHEMATICAL PROOF] The Bayesian Update:")
        print(f"  -> You tested POSITIVE. Your chance of having the disease is: {p_disease_given_positive * 100:.2f}%")
        print("  Even though the test is 99% accurate, because the disease is so incredibly ")
        print("  rare (1%), the vast majority of positive tests are actually False Positives! ")
        print("  This is why AI must use Bayesian priors, not just absolute metrics.")


# ==============================================================================
# 4. MATHEMATICAL PROOF (THE BENCHMARK)
# ==============================================================================
def demonstrate_probability():
    section_header("Probability & Statistics: Bayes' Theorem")
    
    math = BayesianMathematics()
    math.simulate_bayes_theorem()


def run_all_labs():
    demonstrate_probability()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "What is the difference between a 'Frequentist' and a 'Bayesian' approach in Machine Learning?"
   Senior Answer: "Fixed vs Fluid Parameters. A Frequentist believes that the true parameters of a dataset (e.g., the true average height of humans) are fixed, absolute numbers. We just don't have enough data to see them perfectly. A Bayesian believes that parameters are probabilistic distributions. We start with a 'Prior' belief (e.g., humans are probably between 4 and 7 feet tall). As we observe new data, we mathematically update our belief to form a 'Posterior' distribution. Bayesian Neural Networks don't output a single absolute prediction (e.g., $95.5\\%$); they output a probabilistic range (e.g., $95.5\\% \\pm 2\\%$), allowing the AI to mathematically quantify its own Uncertainty."

2. Interviewer: "Explain the 'Naive' assumption in the Naive Bayes classification algorithm."
   Senior Answer: "Absolute Feature Independence. If we are predicting whether an email is Spam, the algorithm looks at the words 'Bank' and 'Account'. In reality, these words are highly correlated (if you see 'Bank', you are very likely to see 'Account'). The Naive Bayes algorithm mathematically ignores this reality. It 'naively' assumes that the probability of seeing 'Bank' is completely mathematically independent of seeing 'Account'. This allows the algorithm to simply multiply the individual probabilities together ($P(Bank) \\cdot P(Account)$). Despite this mathematically false assumption, the algorithm is shockingly accurate and incredibly fast to compute."

3. Interviewer: "What is the 'Base Rate Fallacy' (also known as Prior Probability ignorance)?"
   Senior Answer: "Ignoring the denominator in Bayes' Theorem. If an AI facial recognition scanner is $99\\%$ accurate at identifying terrorists, and it flags a random person at an airport, the security team assumes the person is $99\\%$ likely to be a terrorist. They ignored the Base Rate (the Prior). There are $300$ million people, and maybe $100$ terrorists. The Prior $P(Terrorist)$ is $0.0000003$. Because the Base Rate is so mathematically close to zero, a $99\\%$ accurate scanner will flag $3$ million innocent people as False Positives. AI systems must mathematically encode the Base Rate, or they will destroy production systems with false alerts."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Probability (Bayes' Theorem) Completed.")
