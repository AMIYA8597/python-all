"""
# ==============================================================================
# LABORATORY: REAL-WORLD APPLICATIONS (NATURAL LANGUAGE PROCESSING)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A junior engineer is asked to analyze 10,000 Amazon product reviews to 
# determine if the customers are angry or happy. They write a `for` loop that 
# searches the text for the word "good" and "bad". The system marks the phrase 
# "This product is not good at all, it's terrible" as a positive review because 
# it found the word "good".
#
# A senior NLP engineer understands "Linguistics Mathematics". They import 
# `nltk` or `spacy`. They tokenize the text, remove stop words ("is", "at", "it"), 
# reduce words to their mathematical stems ("running" -> "run"), and execute 
# a VADER Sentiment Analysis algorithm that mathematically calculates the polarity 
# of the sentence structure, instantly capturing the true sentiment with 95% accuracy.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master Text Tokenization (Lexical Analysis).
# - Understand Stop Words and Stemming (Dimensionality Reduction).
# - Execute algorithmic Sentiment Analysis (VADER).
#
# ==============================================================================
"""

import math

# Gracefully handle missing dependencies
try:
    import nltk
    from nltk.tokenize import word_tokenize
    from nltk.corpus import stopwords
    from nltk.stem import PorterStemmer
    from nltk.sentiment import SentimentIntensityAnalyzer
    HAS_NLTK = True
except ImportError:
    HAS_NLTK = False

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. ENVIRONMENT PREPARATION
# ==============================================================================
def setup_nltk():
    """Downloads the required linguistic datasets for NLTK."""
    if not HAS_NLTK:
        return
    try:
        # We silently download the mathematical dictionaries needed by the engine.
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
        nltk.download('vader_lexicon', quiet=True)
    except Exception as e:
        print(f"  [WARNING] Failed to download NLTK data: {e}")


# ==============================================================================
# 4. THE NLP PIPELINE (LEXICAL ANALYSIS)
# ==============================================================================
def demonstrate_nlp_pipeline():
    section_header("The Mathematical Sentence: NLP Pipeline")
    
    if not HAS_NLTK:
        print("  [ERROR] NLTK is not installed.")
        print("  Run `pip install nltk` to execute this lab.")
        return
        
    setup_nltk()
    
    # The raw, unstructured human data!
    raw_text = "The quick brown foxes are violently jumping over the lazy dogs, and it is terrible!"
    print(f"  [RAW DATA] \"{raw_text}\"")
    
    
    # --- 1. TOKENIZATION (The Lexical Split) ---
    print("\n  [PHASE 1: TOKENIZATION]")
    # Splitting by spaces `raw_text.split(" ")` is mathematically catastrophic, 
    # because it attaches punctuation to words (e.g., "dogs,").
    # Tokenizers use complex Regex to mathematically isolate the true lexemes!
    tokens = word_tokenize(raw_text.lower())
    print(f"    -> Tokens: {tokens}")
    print(f"    -> Dimensionality: {len(tokens)} words.")


    # --- 2. DIMENSIONALITY REDUCTION (Stop Words) ---
    print("\n  [PHASE 2: STOP WORD REMOVAL]")
    # The words "the", "are", "and", "it", "is" contain absolutely zero semantic 
    # value for sentiment analysis. They are "noise".
    # By mathematically removing them, we reduce the processing load for the ML model!
    
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word.isalnum() and word not in stop_words]
    
    print(f"    -> Filtered: {filtered_tokens}")
    print(f"    -> Dimensionality: {len(filtered_tokens)} words (Noise eliminated!)")


    # --- 3. ALGORITHMIC STEMMING (Morphological Analysis) ---
    print("\n  [PHASE 3: STEMMING]")
    # "Jumping", "Jumps", and "Jumped" are mathematically different strings to a computer!
    # A Stemmer chops off the English suffixes to reduce them to their root "Stem",
    # allowing the ML model to recognize them as the exact same semantic feature!
    
    stemmer = PorterStemmer()
    stemmed_tokens = [stemmer.stem(word) for word in filtered_tokens]
    
    print(f"    -> Stemmed: {stemmed_tokens}")
    print("    -> Notice how 'foxes' became 'fox', and 'violently' became 'violent'.")


    # --- 4. SENTIMENT ANALYSIS (The VADER Algorithm) ---
    print("\n  [PHASE 4: VADER SENTIMENT ANALYSIS]")
    # VADER (Valence Aware Dictionary and sEntiment Reasoner) mathematically 
    # calculates the polarity of the RAW text, understanding punctuation (!!!) 
    # and capitalization (TERRIBLE).
    
    sia = SentimentIntensityAnalyzer()
    
    # We pass the RAW text so VADER can analyze the linguistic structure!
    scores = sia.polarity_scores(raw_text)
    
    print("    -> Mathematical Polarity Matrix:")
    print(f"       Positive: {scores['pos']:.3f}")
    print(f"       Neutral:  {scores['neu']:.3f}")
    print(f"       Negative: {scores['neg']:.3f}")
    print(f"       Compound: {scores['compound']:.3f} (Overall mathematical verdict)")
    
    if scores['compound'] >= 0.05:
        print("\n  [VERDICT] The sentiment is POSITIVE.")
    elif scores['compound'] <= -0.05:
        print("\n  [VERDICT] The sentiment is NEGATIVE.")
    else:
        print("\n  [VERDICT] The sentiment is NEUTRAL.")


def run_all_labs():
    demonstrate_nlp_pipeline()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "Why is simply executing `text.split(' ')` fundamentally dangerous when preparing text for a Machine Learning Model?"
   Senior Answer: "Standard string splitting creates catastrophic dimensionality explosion in the mathematical matrix. If a sentence contains the word `excellent` and another contains `excellent!`, a naive `.split(' ')` creates two entirely different string keys in the vocabulary dictionary. The Machine Learning model has no idea that `excellent` and `excellent!` mean the same thing, destroying its predictive accuracy. A professional NLP Tokenizer (like NLTK or SpaCy) uses advanced Regex to mathematically isolate punctuation as its own standalone token, guaranteeing that the true word is cleanly extracted for the matrix."

2. Interviewer: "What is the architectural difference between 'Stemming' and 'Lemmatization'?"
   Senior Answer: "Stemming (e.g., the Porter Stemmer) is a blunt algorithmic axe. It blindly chops characters off the end of a word using a fixed set of Regex rules (e.g., removing 'ing' or 'es'). Because it is blindly cutting, it often creates non-words (e.g., 'violently' becomes 'violentli'). It is incredibly fast but lacks linguistic accuracy. Lemmatization (e.g., the WordNet Lemmatizer) is a sophisticated dictionary lookup. It mathematically analyzes the word's POS (Part of Speech) context within the sentence, and traces it back to its true linguistic dictionary root (the Lemma). Lemmatization perfectly converts 'better' into 'good', whereas a Stemmer would fail completely. Lemmatization is highly accurate but computationally expensive."

3. Interviewer: "How does an algorithm like VADER (SentimentIntensityAnalyzer) mathematically 'understand' that a sentence is negative without using a massive Deep Learning Neural Network?"
   Senior Answer: "VADER relies on a 'Lexicon and Rule-Based' architecture. The Lexicon is essentially a massive human-validated dictionary where thousands of words are mathematically mapped to a polarity score (e.g., 'good' = $+1.9$, 'terrible' = $-2.1$). When parsing a sentence, it sums the scores of the words. However, the brilliance of VADER lies in its Rule-Based Heuristics. It understands intensifiers (e.g., 'VERY good' mathematically multiplies the $+1.9$ score). It understands negation (e.g., 'NOT good' mathematically flips the $+1.9$ to a negative). It even mathematically weighs punctuation ('good!!!' is weighted higher than 'good.'). It achieves highly accurate sentiment polarity using pure algorithmic mathematics, requiring zero GPU training time."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: AI & ML (Natural Language Processing) Completed.")
