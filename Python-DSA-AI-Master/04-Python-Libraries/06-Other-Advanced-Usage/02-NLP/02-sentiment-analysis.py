"""
Module: 02-sentiment-analysis
Description: Comprehensive textbook-grade interactive lesson on Sentiment Analysis in Natural Language Processing.

Learning Objectives:
1. Understand the theoretical and mathematical foundations of sentiment analysis.
2. Implement lexicon-based (rule-based) sentiment analysis using pure Python.
3. Understand and implement statistical / machine-learning based sentiment analysis.
4. Grasp the probability mathematics behind classification.
5. Analyze time and space complexity (Big-O) for each approach.

Mathematical Background:
1. Lexicon-Based Scoring (e.g., VADER):
   A document D consists of words w_1, w_2, ..., w_n.
   Each word w_i has a predefined sentiment score s(w_i) in a lexicon L.
   Total Sentiment S(D) = sum(s(w_i) * mod(w_i))
   where mod(w_i) is a modifier (e.g., negations or intensifiers).
   Normalized score: S_norm(D) = S(D) / sqrt(S(D)^2 + alpha)

2. Naive Bayes (Probabilistic Approach):
   P(c | D) = P(D | c) * P(c) / P(D)
   where c in {Positive, Negative, Neutral}.
   With bag-of-words assumption:
   c_hat = argmax_c P(c) * Product(P(w_i | c))
   Log-probabilities are used to prevent underflow:
   c_hat = argmax_c [ log(P(c)) + Sum(log(P(w_i | c))) ]

3. Transformers / Neural Networks (Concept):
   Given input tokens X = [x_1, x_2, ..., x_n].
   Embeddings E = EmbeddingLayer(X)
   Contextualized embeddings H = TransformerBlocks(E)
   Logits Z = LinearLayer(H_[CLS])
   Probabilities P = Softmax(Z)
   where Softmax(z_i) = exp(z_i) / Sum(exp(z_j))

Complexity Analysis:
- Lexicon-Based:
  Time Complexity: O(N) where N is the number of words in the document. We do a simple lookup.
  Space Complexity: O(V) where V is the size of the vocabulary in the lexicon dictionary.
- Naive Bayes:
  Training Time Complexity: O(M * N) where M is number of documents and N is average words per document.
  Inference Time Complexity: O(N) per document.
  Space Complexity: O(V * C) where V is vocabulary size and C is number of classes.

Real-world Applications:
- Brand monitoring and social media listening.
- Customer support ticket routing and prioritization.
- Market research and product feedback analysis.
- Algorithmic trading based on financial news sentiment.
"""

import math
import re
from typing import List, Dict, Tuple, Any, Optional

# ============================================================================
# 1. Lexicon-Based Sentiment Analysis (From Scratch)
# ============================================================================

class LexiconSentimentAnalyzer:
    """
    A basic rule-based (lexicon-based) sentiment analyzer.
    This simulates how libraries like VADER or TextBlob work internally.
    """
    
    def __init__(self):
        # A mock lexicon mapping words to polarity scores between -1.0 and 1.0
        self.lexicon: Dict[str, float] = {
            "good": 0.5, "great": 0.8, "excellent": 1.0, "awesome": 0.9,
            "happy": 0.6, "love": 0.7, "best": 0.8,
            "bad": -0.5, "terrible": -0.9, "awful": -0.8, "hate": -0.7,
            "sad": -0.6, "worst": -0.9, "poor": -0.5,
        }
        
        # Modifiers that alter the score of the subsequent word
        self.intensifiers: Dict[str, float] = {
            "very": 1.5, "extremely": 2.0, "absolutely": 2.0,
            "slightly": 0.5, "somewhat": 0.8
        }
        
        # Negation words that reverse polarity
        self.negations: set = {
            "not", "never", "no", "neither", "nor", "none", "cannot",
            "isn't", "aren't", "wasn't", "weren't", "haven't", "hasn't",
            "hadn't", "won't", "wouldn't", "don't", "doesn't", "didn't",
            "can't", "couldn't", "shouldn't", "mightn't", "mustn't"
        }

    def _tokenize(self, text: str) -> List[str]:
        """
        Convert text to lower case and extract alphabetic words.
        Time Complexity: O(N) where N is the length of the string.
        """
        text = text.lower()
        # Find all sequences of word characters
        return re.findall(r'\b[a-z\']+\b', text)

    def analyze(self, text: str) -> Dict[str, Any]:
        """
        Analyzes the sentiment of the given text.
        
        Algorithm:
        1. Tokenize the text.
        2. Iterate over tokens.
        3. Check for negations and intensifiers modifying the next sentiment word.
        4. Sum the scores and normalize.
        
        Time Complexity: O(N) where N is the number of tokens.
        Space Complexity: O(N) to store tokens.
        """
        tokens = self._tokenize(text)
        total_score = 0.0
        word_count = 0
        
        i = 0
        while i < len(tokens):
            word = tokens[i]
            
            # Check for negation (lookahead up to 2 words)
            is_negated = False
            multiplier = 1.0
            
            # Look behind for modifiers
            if i > 0:
                prev_word = tokens[i-1]
                if prev_word in self.negations:
                    is_negated = True
                elif prev_word in self.intensifiers:
                    multiplier = self.intensifiers[prev_word]
                    
                # Look further back for "not very" cases
                if i > 1 and tokens[i-2] in self.negations and prev_word in self.intensifiers:
                    is_negated = True
            
            if word in self.lexicon:
                base_score = self.lexicon[word]
                
                # Apply multipliers and negations
                final_score = base_score * multiplier
                if is_negated:
                    final_score *= -1.0 # Reverse polarity
                    
                total_score += final_score
                word_count += 1
                
            i += 1
            
        # Normalization: x / sqrt(x^2 + alpha)
        # We use alpha = 15 as a smoothing constant similar to VADER
        alpha = 15.0
        normalized_score = total_score / math.sqrt((total_score ** 2) + alpha)
        
        # Determine discrete class
        if normalized_score >= 0.05:
            sentiment_class = "Positive"
        elif normalized_score <= -0.05:
            sentiment_class = "Negative"
        else:
            sentiment_class = "Neutral"
            
        return {
            "compound_score": round(normalized_score, 4),
            "raw_score": round(total_score, 4),
            "sentiment": sentiment_class,
            "scored_words": word_count
        }


# ============================================================================
# 2. Machine Learning Based Sentiment Analysis (Naive Bayes)
# ============================================================================

class NaiveBayesSentiment:
    """
    Multinomial Naive Bayes implementation for text classification.
    """
    
    def __init__(self, alpha: float = 1.0):
        self.alpha = alpha # Laplace smoothing parameter
        self.vocab: set = set()
        self.class_word_counts: Dict[str, Dict[str, int]] = {}
        self.class_totals: Dict[str, int] = {}
        self.class_doc_counts: Dict[str, int] = {}
        self.total_docs: int = 0
        self.classes: List[str] = ["Positive", "Negative"]
        
        for c in self.classes:
            self.class_word_counts[c] = {}
            self.class_totals[c] = 0
            self.class_doc_counts[c] = 0

    def _tokenize(self, text: str) -> List[str]:
        return re.findall(r'\b[a-z]+\b', text.lower())

    def train(self, corpus: List[Tuple[str, str]]) -> None:
        """
        Trains the Naive Bayes model on a labeled corpus.
        
        Time Complexity: O(M * N) where M is documents and N is words per doc.
        Space Complexity: O(V * C) where V is vocab size and C is number of classes.
        """
        self.total_docs = len(corpus)
        
        for text, label in corpus:
            if label not in self.classes:
                continue
                
            self.class_doc_counts[label] += 1
            tokens = self._tokenize(text)
            
            for token in tokens:
                self.vocab.add(token)
                self.class_word_counts[label][token] = self.class_word_counts[label].get(token, 0) + 1
                self.class_totals[label] += 1

    def predict(self, text: str) -> Dict[str, Any]:
        """
        Predicts the sentiment of a given text using log probabilities.
        """
        if self.total_docs == 0:
            raise ValueError("Model has not been trained yet.")
            
        tokens = self._tokenize(text)
        vocab_size = len(self.vocab)
        
        scores: Dict[str, float] = {}
        
        for c in self.classes:
            # Prior probability P(c)
            prior = math.log(self.class_doc_counts[c] / self.total_docs)
            
            # Likelihood P(w|c) for each word
            likelihood = 0.0
            for token in tokens:
                if token in self.vocab:
                    count_w_c = self.class_word_counts[c].get(token, 0)
                    # Laplace smoothing
                    prob_w_c = (count_w_c + self.alpha) / (self.class_totals[c] + self.alpha * vocab_size)
                    likelihood += math.log(prob_w_c)
                    
            scores[c] = prior + likelihood
            
        predicted_class = max(scores, key=scores.get) # type: ignore
        
        # Convert log probabilities to normalized probabilities (Softmax-like approach)
        max_log_prob = max(scores.values())
        exp_scores = {c: math.exp(score - max_log_prob) for c, score in scores.items()}
        sum_exp = sum(exp_scores.values())
        probabilities = {c: round(score / sum_exp, 4) for c, score in exp_scores.items()}
        
        return {
            "prediction": predicted_class,
            "probabilities": probabilities,
            "log_scores": scores
        }


# ============================================================================
# 3. Demonstration & Real-World Simulation
# ============================================================================

def simulate_social_media_listening() -> None:
    """
    Simulates a real-world scenario where a company monitors social media
    for mentions of their new product and analyzes the sentiment.
    """
    print("\n" + "="*60)
    print("🌍 Real-World Application: Social Media Listening")
    print("="*60)
    
    tweets = [
        "The new UI is absolutely great! I love it.",
        "Terrible experience. The app crashes every time I open it. Worst update.",
        "It's okay, not very good but not completely awful either.",
        "I am extremely happy with the new features.",
        "Customer support was unhelpful and rude. Never using this again."
    ]
    
    analyzer = LexiconSentimentAnalyzer()
    
    print("\n--- Lexicon-Based Sentiment Analysis ---")
    for idx, tweet in enumerate(tweets, 1):
        result = analyzer.analyze(tweet)
        print(f"\nTweet #{idx}: '{tweet}'")
        print(f"  └─ Sentiment: {result['sentiment']}")
        print(f"  └─ Score: {result['compound_score']}")


def train_and_test_ml_model() -> None:
    """
    Trains the Naive Bayes classifier on a small dataset and tests it.
    """
    print("\n" + "="*60)
    print("🧠 Machine Learning Application: Naive Bayes Classification")
    print("="*60)
    
    # Tiny training corpus
    training_data = [
        ("I love this product, it is amazing", "Positive"),
        ("Best purchase ever, highly recommended", "Positive"),
        ("Great battery life and awesome display", "Positive"),
        ("Good quality for the price", "Positive"),
        ("I hate this thing, it broke immediately", "Negative"),
        ("Terrible customer service, very disappointing", "Negative"),
        ("Worst phone I have ever bought", "Negative"),
        ("Do not buy this, it is a scam", "Negative")
    ]
    
    test_data = [
        "This is an amazing and great product",
        "Terrible and disappointing experience",
        "It is not good, I hate it"
    ]
    
    nb_model = NaiveBayesSentiment(alpha=1.0)
    print(f"Training Naive Bayes model on {len(training_data)} samples...")
    nb_model.train(training_data)
    
    print(f"Vocabulary size: {len(nb_model.vocab)}")
    
    print("\n--- Naive Bayes Inference ---")
    for text in test_data:
        result = nb_model.predict(text)
        print(f"\nText: '{text}'")
        print(f"  └─ Prediction: {result['prediction']}")
        print(f"  └─ Probabilities: {result['probabilities']}")


# ============================================================================
# 4. Interview Challenge
# ============================================================================

def interview_challenge_longest_palindrome_sentiment(text: str) -> Tuple[str, Dict[str, Any]]:
    """
    Interview Challenge:
    Given a text, find the longest palindromic substring (words only, ignoring spaces and punctuation)
    and perform sentiment analysis on the entire text.
    
    Algorithm for Longest Palindrome: Expand around center.
    Time Complexity: O(N^2) where N is length of cleaned string.
    Space Complexity: O(1) beyond the string copies.
    """
    print("\n" + "="*60)
    print("🎯 Interview Challenge: Longest Palindrome + Sentiment")
    print("="*60)
    
    # 1. Clean the string to only characters
    cleaned_chars = [c.lower() for c in text if c.isalpha()]
    cleaned_text = "".join(cleaned_chars)
    
    # 2. Find longest palindrome
    if not cleaned_text:
        longest_pal = ""
    else:
        def expand_around_center(s: str, left: int, right: int) -> str:
            while left >= 0 and right < len(s) and s[left] == s[right]:
                left -= 1
                right += 1
            return s[left + 1:right]
            
        longest_pal = ""
        for i in range(len(cleaned_text)):
            # Odd length palindrome
            pal1 = expand_around_center(cleaned_text, i, i)
            # Even length palindrome
            pal2 = expand_around_center(cleaned_text, i, i + 1)
            
            if len(pal1) > len(longest_pal):
                longest_pal = pal1
            if len(pal2) > len(longest_pal):
                longest_pal = pal2
                
    # 3. Get sentiment
    analyzer = LexiconSentimentAnalyzer()
    sentiment_res = analyzer.analyze(text)
    
    return longest_pal, sentiment_res


# ============================================================================
# 5. Testing Suite
# ============================================================================

def run_tests() -> None:
    """
    Test suite to validate the correctness of the algorithms.
    """
    print("\n" + "="*60)
    print("🧪 Running Unit Tests")
    print("="*60)
    
    # Test Lexicon Analyzer
    analyzer = LexiconSentimentAnalyzer()
    
    res1 = analyzer.analyze("I love this absolutely great product!")
    assert res1["sentiment"] == "Positive", f"Expected Positive, got {res1['sentiment']}"
    
    res2 = analyzer.analyze("This is a terrible and awful mistake.")
    assert res2["sentiment"] == "Negative", f"Expected Negative, got {res2['sentiment']}"
    
    # Test Negation Handling
    res3 = analyzer.analyze("This is not good.")
    assert res3["sentiment"] == "Negative", f"Negation failed, got {res3['sentiment']}"
    
    # Test Interview Challenge
    pal, sent = interview_challenge_longest_palindrome_sentiment("A man, a plan, a canal: Panama. It is great!")
    assert pal == "amanaplanacanalpanama", f"Palindrome extraction failed: {pal}"
    assert sent["sentiment"] == "Positive", "Sentiment extraction failed"
    
    print("✅ All tests passed successfully!")


if __name__ == "__main__":
    print("="*70)
    print("🚀 PYTHON DSA & AI MASTERCLASS: SENTIMENT ANALYSIS".center(70))
    print("="*70)
    
    # 1. Simulate Social Media Listening
    simulate_social_media_listening()
    
    # 2. Train and Test ML Model
    train_and_test_ml_model()
    
    # 3. Interview Challenge
    sample_text = "Was it a car or a cat I saw? I am extremely happy about it!"
    pal, sent = interview_challenge_longest_palindrome_sentiment(sample_text)
    print(f"\nInput Text: '{sample_text}'")
    print(f"Longest Palindromic Substring (Cleaned): '{pal}'")
    print(f"Overall Sentiment: {sent['sentiment']} (Score: {sent['compound_score']})")
    
    # 4. Run Tests
    run_tests()
    
    print("\n" + "="*70)
    print("🏁 End of Sentiment Analysis Lesson".center(70))
    print("="*70)
