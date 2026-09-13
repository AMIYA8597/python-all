\"\"\"
Natural Language Processing (NLP) Application Fundamentals

What is NLP?
Natural Language Processing is a subfield of linguistics, computer science, and AI concerned with 
the interactions between computers and human language. The goal is to process and analyze large 
amounts of natural language data.
Industry use cases include sentiment analysis, machine translation, chatbots (like ChatGPT), 
spam detection, and text summarization.

Learning Objectives:
1. Understand tokenization, stop words, and vocabulary building.
2. Implement basic rule-based text processing and frequency analysis.
3. Build a professional-grade NLP pipeline with extensible components and typing.
4. Grasp the theoretical foundations of embedding and vector spaces (Advanced).

Concept Explanation:
Text data is unstructured. To make it machine-readable, we must convert text into numbers. 
A foundational step is 'Tokenization'—splitting a sentence into words (tokens). Then, we often 
remove 'Stop words' (common words like 'the', 'is', 'in' that hold little semantic value). 
Finally, we can count frequencies (Bag of Words) or convert tokens to dense vectors (Word Embeddings).

Beginner Explanation:
Imagine you want to know what a book is about. You wouldn't care about the word 'and' or 'the'. 
You'd look for the words that appear most often, like 'magic', 'wizard', or 'school'. NLP starts 
by teaching the computer to ignore the boring words and count the important ones.

Advanced Explanation:
Modern NLP relies heavily on Transformer architectures and attention mechanisms. Instead of simple 
frequency counts (TF-IDF), words are mapped to high-dimensional continuous vector spaces (e.g., 
Word2Vec, BERT embeddings). In this space, semantic relationships are preserved as geometric distances 
(e.g., Vector(\"King\") - Vector(\"Man\") + Vector(\"Woman\") ≈ Vector(\"Queen\")).

Performance Considerations:
- Memory: Storing massive vocabularies and embedding matrices requires high RAM.
- Speed: String operations in native Python are slow. Use optimized libraries like spaCy or tokenizers 
  (Rust-based) for high-throughput processing.

Security Concerns:
- Prompt Injection: In modern LLM-based NLP apps, malicious users can craft inputs that trick the model 
  into executing unauthorized commands or leaking sensitive data.
- Bias & Fairness: NLP models can inherit and amplify societal biases present in their training data.
\"\"\"

import re
import math
from typing import List, Dict, Set, Optional
from collections import Counter
import logging

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# ---------------------------------------------------------
# Basic Implementation
# ---------------------------------------------------------

def basic_sentiment_analyzer(text: str) -> str:
    \"\"\"
    A naive, rule-based sentiment analyzer using keyword counting.
    
    Args:
        text (str): The input text to analyze.
        
    Returns:
        str: 'Positive', 'Negative', or 'Neutral'
    \"\"\"
    positive_words = {'good', 'great', 'excellent', 'amazing', 'love', 'happy'}
    negative_words = {'bad', 'terrible', 'awful', 'hate', 'sad', 'angry'}
    
    # Convert to lowercase and split by whitespace
    words = text.lower().split()
    
    score = 0
    for word in words:
        # Simple punctuation stripping
        clean_word = word.strip('.,!?')
        if clean_word in positive_words:
            score += 1
        elif clean_word in negative_words:
            score -= 1
            
    if score > 0:
        return \"Positive\"
    elif score < 0:
        return \"Negative\"
    else:
        return \"Neutral\"

# ---------------------------------------------------------
# Professional Implementation
# ---------------------------------------------------------

class TextProcessor:
    \"\"\"
    A professional-grade text processing pipeline.
    Implements tokenization, stop word removal, and Term Frequency (TF) calculation.
    \"\"\"
    
    DEFAULT_STOP_WORDS: Set[str] = {
        'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your',
        'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she',
        'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their',
        'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that',
        'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
        'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an',
        'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of',
        'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through',
        'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down',
        'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then',
        'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any',
        'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor',
        'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can',
        'will', 'just', 'don', 'should', 'now'
    }

    def __init__(self, custom_stop_words: Optional[Set[str]] = None):
        \"\"\"
        Initializes the text processor.
        
        Args:
            custom_stop_words: Optional set of custom stop words to supplement the default list.
        \"\"\"
        self.stop_words = self.DEFAULT_STOP_WORDS.copy()
        if custom_stop_words:
            self.stop_words.update(custom_stop_words)
            
        logging.info(f\"TextProcessor initialized with {len(self.stop_words)} stop words.\")

    def tokenize(self, text: str) -> List[str]:
        \"\"\"
        Tokenizes text by lowercasing and extracting alphabetic sequences.
        
        Args:
            text: The raw input string.
            
        Returns:
            List of normalized tokens.
        \"\"\"
        if not text:
            return []
        
        # Use regex to find all alphabetic sequences (ignores numbers and punctuation)
        text = text.lower()
        tokens = re.findall(r'\\b[a-z]+\\b', text)
        return tokens

    def remove_stop_words(self, tokens: List[str]) -> List[str]:
        \"\"\"
        Filters out stop words from a list of tokens.
        \"\"\"
        return [token for token in tokens if token not in self.stop_words]

    def compute_term_frequency(self, tokens: List[str]) -> Dict[str, float]:
        \"\"\"
        Computes the Term Frequency (TF) of tokens.
        TF(t) = (Number of times term t appears in a document) / (Total number of words in that document)
        
        Args:
            tokens: A list of processed tokens.
            
        Returns:
            Dictionary mapping term to its frequency score.
        \"\"\"
        if not tokens:
            return {}
            
        total_tokens = len(tokens)
        counts = Counter(tokens)
        
        tf_dict = {term: count / total_tokens for term, count in counts.items()}
        return tf_dict

    def process_pipeline(self, text: str) -> Dict[str, float]:
        \"\"\"
        Executes the full NLP preprocessing pipeline.
        
        Args:
            text: Raw input document.
            
        Returns:
            TF dictionary of the processed text.
        \"\"\"
        tokens = self.tokenize(text)
        filtered_tokens = self.remove_stop_words(tokens)
        tf_scores = self.compute_term_frequency(filtered_tokens)
        return tf_scores


# ---------------------------------------------------------
# Complexity Analysis & Interview Challenge
# ---------------------------------------------------------
\"\"\"
Complexity Analysis (TextProcessor.process_pipeline):
- Tokenize: O(N) time where N is the length of the string (Regex engine sweeps the string).
- Remove Stop Words: O(M) time where M is the number of tokens, because set lookup is O(1).
- Compute TF: O(M) time to count and create the dictionary.
- Total Time Complexity: O(N). Space Complexity: O(M) to store the tokens and dictionaries.

Interview Challenge:
Question: You are building an autocomplete system for a search engine. Users type a prefix, and 
you must return the top 5 most common query completions. How would you design the data structure 
to make this extremely fast, assuming millions of historical queries?

Answer Guide:
1. Data Structure: A Trie (Prefix Tree) is optimal for prefix matching.
2. Optimization: To avoid traversing the whole sub-tree to find the top 5, cache the top 5 queries 
   at every single node during the construction phase.
3. Space Trade-off: Caching at every node increases memory usage significantly, but search time 
   becomes O(L) where L is the length of the prefix, enabling lightning-fast autocompletion.
\"\"\"

# ---------------------------------------------------------
# Example Usage and Tests (Main Guard)
# ---------------------------------------------------------
if __name__ == \"__main__\":
    print(\"\\n=== NLP App Execution ===\")
    
    # 1. Test Basic Analyzer
    sample_text_1 = \"This product is absolutely amazing and I love it!\"
    sample_text_2 = \"Terrible service, very bad experience, angry.\"
    
    print(\"--- Basic Analyzer ---\")
    res1 = basic_sentiment_analyzer(sample_text_1)
    res2 = basic_sentiment_analyzer(sample_text_2)
    print(f\"Text 1 Sentiment: {res1}\")
    print(f\"Text 2 Sentiment: {res2}\")
    
    assert res1 == \"Positive\"
    assert res2 == \"Negative\"
    
    # 2. Test Professional Pipeline
    print(\"\\n--- Professional Pipeline ---\")
    corpus = \"\"\"
    Natural language processing (NLP) is a subfield of linguistics, computer science, 
    and artificial intelligence concerned with the interactions between computers and human language, 
    in particular how to program computers to process and analyze large amounts of natural language data.
    \"\"\"
    
    processor = TextProcessor(custom_stop_words={'particular'})
    tf_scores = processor.process_pipeline(corpus)
    
    # Sort and display top 5 terms
    top_terms = sorted(tf_scores.items(), key=lambda item: item[1], reverse=True)[:5]
    print(\"Top 5 terms by Term Frequency:\")
    for term, score in top_terms:
        print(f\" - {term}: {score:.4f}\")
        
    # Assertions
    assert 'nlp' in tf_scores
    assert 'the' not in tf_scores, \"Stop word 'the' should have been removed.\"
    assert 'particular' not in tf_scores, \"Custom stop word 'particular' should have been removed.\"
    assert sum(tf_scores.values()) > 0.999, \"TF scores should sum approximately to 1.0\"
    
    print(\"\\nAll assertions passed successfully! NLP pipeline works.\")
    print(\"=== Execution Complete ===\")
