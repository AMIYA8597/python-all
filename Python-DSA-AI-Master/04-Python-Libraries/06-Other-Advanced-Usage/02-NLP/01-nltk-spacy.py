"""
Natural Language Processing (NLP) Masterclass: NLTK vs SpaCy
============================================================

## A. Concept Introduction
Natural Language Processing (NLP) is a subfield of linguistics, computer science, and artificial intelligence
concerned with the interactions between computers and human language. The goal is to program computers to 
process and analyze large amounts of natural language data.

In the Python ecosystem, two titans dominate the NLP landscape:
1. **NLTK (Natural Language Toolkit):** A comprehensive, classic library meant for teaching, research, and 
   prototyping. It offers many algorithms to solve the same problem (e.g., dozens of stemmers).
2. **SpaCy:** A modern, blazing-fast library built specifically for production. It offers the *best* algorithm
   for a problem (opinionated), leveraging heavily optimized Cython and deep learning pipelines under the hood.

## B. Mathematical and Theoretical Background

### 1. Tokenization
Tokenization is the process of splitting text into smaller pieces called tokens (words, subwords, or sentences).
- **Time Complexity:** O(N) where N is the number of characters in the string, as it involves a single pass 
  or regex matches.
- **Space Complexity:** O(N) to store the generated tokens.

### 2. Stemming vs Lemmatization
- **Stemming:** A heuristic process that chops off the ends of words in the hope of achieving the goal correctly 
  most of the time. (e.g., "running" -> "run", "better" -> "bett"). Fast (O(L) per word, L = word length), 
  but often inaccurate.
- **Lemmatization:** Uses a vocabulary and morphological analysis of words to return the base or dictionary 
  form of a word, known as the lemma (e.g., "better" -> "good"). Slower but highly accurate.

### 3. Part-of-Speech (POS) Tagging
Assigning parts of speech (noun, verb, adjective, etc.) to each word.
Modern taggers (like SpaCy's) use neural networks (e.g., CNNs or Transformers) or Conditional Random Fields (CRFs).
If V is the number of hidden states (tags) and T is the sequence length, Viterbi decoding for CRFs takes O(T * V^2).

### 4. Word Vectors (Embeddings)
Representing words in a dense, low-dimensional vector space (e.g., 300 dimensions) where geometrically 
close vectors represent semantically related words.
- **Cosine Similarity:** Used to measure the similarity between two vectors A and B.
  Formula: cos(theta) = (A \cdot B) / (||A|| * ||B||)

## C. Use Cases
1. **Sentiment Analysis:** Classifying reviews as positive or negative.
2. **Named Entity Recognition (NER):** Extracting people, organizations, dates from documents.
3. **Information Extraction:** Parsing resumes or medical records automatically.
4. **Chatbots:** Understanding user intent and entities.

## D. Common Pitfalls
- **Memory Leaks:** Processing massive datasets in SpaCy without using `nlp.pipe()`.
- **NLTK for Production:** Using NLTK's slow Python-based processing for millions of documents instead of SpaCy.
- **Missing Models:** Forgetting to download `en_core_web_sm` for SpaCy or `punkt`/`wordnet` for NLTK.

## E. Interview Questions
1. **Why might you choose NLTK over SpaCy?**
   *Answer:* If I am doing academic research, need access to a very specific legacy algorithm (like a particular stemmer), or want to explore multiple different approaches to a problem. SpaCy is opinionated and only gives you one (the best) way.
2. **Explain the difference between Stemming and Lemmatization.**
   *Answer:* Stemming blindly chops word endings; lemmatization uses a dictionary to find the morphological root.
3. **What is a "stop word"? Why remove them?**
   *Answer:* Common words like "the", "is", "in" that carry little semantic meaning. Removing them reduces the dimensional space and speeds up downstream processing like TF-IDF or text classification.

## F. Advanced Setup
Ensure you have the required packages:
`pip install nltk spacy`
`python -m spacy download en_core_web_sm`
`python -c "import nltk; nltk.download('punkt'); nltk.download('averaged_perceptron_tagger'); nltk.download('wordnet'); nltk.download('omw-1.4')"`
"""

import time
import re
from typing import List, Dict, Any, Tuple, Optional
from collections import Counter
import math

try:
    import nltk
    from nltk.tokenize import word_tokenize, sent_tokenize
    from nltk.stem import PorterStemmer, WordNetLemmatizer
    from nltk.corpus import stopwords
    from nltk import pos_tag
    NLTK_AVAILABLE = True
except ImportError:
    NLTK_AVAILABLE = False

try:
    import spacy
    # Load the small English model. If not found, fall back gracefully.
    try:
        nlp = spacy.load("en_core_web_sm")
        SPACY_AVAILABLE = True
    except OSError:
        nlp = None
        SPACY_AVAILABLE = False
except ImportError:
    SPACY_AVAILABLE = False


# =====================================================================
# 1. NLTK Implementation: The Research Approach
# =====================================================================

class NLTKProcessor:
    """
    A class encapsulating common NLTK operations.
    NLTK is great for exploring algorithms and string processing.
    """

    def __init__(self):
        if not NLTK_AVAILABLE:
            raise ImportError("NLTK is not installed or models are missing.")
        self.stemmer = PorterStemmer()
        self.lemmatizer = WordNetLemmatizer()
        
        # Download stopwords if not present, then load them
        try:
            self.stop_words = set(stopwords.words('english'))
        except LookupError:
            nltk.download('stopwords')
            self.stop_words = set(stopwords.words('english'))

    def tokenize_text(self, text: str) -> Dict[str, List[str]]:
        """
        Tokenizes text into sentences and words.
        
        Time Complexity: O(N) where N is length of string.
        Space Complexity: O(N) for storing tokens.
        """
        # sentence tokenization is usually rule-based (regex)
        sentences = sent_tokenize(text)
        # word tokenization separates punctuation and words
        words = word_tokenize(text)
        
        return {
            "sentences": sentences,
            "words": words
        }

    def stem_vs_lemmatize(self, words: List[str]) -> List[Dict[str, str]]:
        """
        Demonstrates the difference between stemming and lemmatization.
        
        Stemming: Fast O(L), rule-based chopping.
        Lemmatization: Slower O(L), dictionary lookup.
        """
        results = []
        for word in words:
            # WordNetLemmatizer assumes noun by default, POS tag can be passed for verbs
            results.append({
                "original": word,
                "stemmed": self.stemmer.stem(word),
                "lemmatized": self.lemmatizer.lemmatize(word, pos='v') # 'v' for verb
            })
        return results

    def process_pipeline(self, text: str) -> List[Tuple[str, str]]:
        """
        A full NLTK pipeline: tokenize -> remove stopwords -> POS tagging.
        """
        words = word_tokenize(text)
        # Filter stopwords and non-alphabetic tokens
        clean_words = [w for w in words if w.lower() not in self.stop_words and w.isalpha()]
        # Part-of-Speech tagging
        tagged = pos_tag(clean_words)
        return tagged


# =====================================================================
# 2. SpaCy Implementation: The Production Approach
# =====================================================================

class SpacyProcessor:
    """
    A class encapsulating common SpaCy operations.
    SpaCy is optimized for speed and production pipelines.
    """

    def __init__(self):
        if not SPACY_AVAILABLE or nlp is None:
            raise ImportError("SpaCy or the en_core_web_sm model is not installed.")
        self.nlp = nlp

    def process_text(self, text: str) -> List[Dict[str, Any]]:
        """
        Passes text through the complete SpaCy pipeline.
        SpaCy does Tokenization, POS tagging, Dependency Parsing, and NER in one C-optimized pass.
        
        Time Complexity: O(N) empirically, using highly optimized Cython and neural networks.
        """
        # The text is fed into the loaded NLP model pipeline
        doc = self.nlp(text)
        
        results = []
        for token in doc:
            results.append({
                "text": token.text,
                "lemma": token.lemma_,      # Built-in lemmatization
                "pos": token.pos_,          # Coarse-grained POS (e.g., NOUN, VERB)
                "tag": token.tag_,          # Fine-grained POS
                "dep": token.dep_,          # Dependency role
                "is_stop": token.is_stop    # Built-in stop word detection
            })
        return results

    def extract_entities(self, text: str) -> List[Tuple[str, str]]:
        """
        Extracts Named Entities (NER) like Persons, Organizations, Locations.
        """
        doc = self.nlp(text)
        return [(ent.text, ent.label_) for ent in doc.ents]
    
    def process_large_corpus(self, texts: List[str]) -> List[int]:
        """
        Best Practice: Using nlp.pipe() for large datasets.
        This batches the inputs to Cython, bypassing the Python GIL, making it much faster.
        """
        token_counts = []
        # disable components we don't need to speed up pipeline
        for doc in self.nlp.pipe(texts, disable=["parser", "ner"]):
            token_counts.append(len(doc))
        return token_counts


# =====================================================================
# 3. Mathematical Concept: TF-IDF and Cosine Similarity
# =====================================================================

def cosine_similarity(vec_a: Dict[str, float], vec_b: Dict[str, float]) -> float:
    """
    Computes cosine similarity between two sparse vectors represented as dictionaries.
    
    Formula: (A \cdot B) / (||A|| * ||B||)
    Time Complexity: O(K) where K is the number of non-zero elements.
    """
    intersection = set(vec_a.keys()) & set(vec_b.keys())
    numerator = sum([vec_a[x] * vec_b[x] for x in intersection])

    sum1 = sum([val**2 for val in vec_a.values()])
    sum2 = sum([val**2 for val in vec_b.values()])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator

def bag_of_words(text: str) -> Dict[str, float]:
    """
    Converts text to a simple bag-of-words frequency vector.
    """
    words = re.findall(r'\w+', text.lower())
    count = Counter(words)
    return {word: float(c) for word, c in count.items()}


# =====================================================================
# 4. Benchmarking and Edge Cases
# =====================================================================

def benchmark_nlp_libraries(text: str, iterations: int = 100) -> None:
    """
    Compares the execution time of NLTK vs SpaCy for processing a text snippet.
    """
    print(f"\n--- Benchmarking Libraries ({iterations} iterations) ---")
    
    if NLTK_AVAILABLE:
        start = time.perf_counter()
        for _ in range(iterations):
            tokens = word_tokenize(text)
            pos_tag(tokens)
        nltk_time = time.perf_counter() - start
        print(f"NLTK POS Tagging Time: {nltk_time:.4f} seconds")
    
    if SPACY_AVAILABLE:
        start = time.perf_counter()
        for _ in range(iterations):
            # We process using standard __call__
            _ = nlp(text)
        spacy_time = time.perf_counter() - start
        print(f"SpaCy Full Pipeline Time: {spacy_time:.4f} seconds")
        
        # Now with pipe for batch processing (the proper way to do many docs)
        texts = [text] * iterations
        start = time.perf_counter()
        # list() to force evaluation of the generator
        _ = list(nlp.pipe(texts))
        spacy_pipe_time = time.perf_counter() - start
        print(f"SpaCy nlp.pipe() Time:    {spacy_pipe_time:.4f} seconds (Notice the speedup for batching!)")


# =====================================================================
# 5. Testing and Validation
# =====================================================================

def run_tests():
    """
    Test suite to validate core logic and mathematical functions.
    """
    print("\n--- Running Tests ---")
    # Test Cosine Similarity
    v1 = {"apple": 1.0, "banana": 2.0}
    v2 = {"apple": 1.0, "banana": 2.0}
    assert math.isclose(cosine_similarity(v1, v2), 1.0), "Identical vectors should have similarity 1.0"
    
    v3 = {"orange": 1.0}
    assert cosine_similarity(v1, v3) == 0.0, "Orthogonal vectors should have similarity 0.0"
    
    # Test Bag of Words
    text = "Hello hello world"
    bow = bag_of_words(text)
    assert bow["hello"] == 2.0
    assert bow["world"] == 1.0
    
    print("All unit tests passed successfully!")


# =====================================================================
# 6. Main Execution Block
# =====================================================================

if __name__ == "__main__":
    print("========== EXPLORING NLP WITH NLTK AND SPACY ==========\n")
    
    sample_text = "Apple is looking at buying U.K. startup for $1 billion. The executives were running quickly."
    print(f"Sample Text: '{sample_text}'\n")

    if NLTK_AVAILABLE:
        print("--- NLTK Demonstration ---")
        try:
            # We wrap this in a try-except block to catch LookupErrors if user hasn't downloaded models
            nltk_proc = NLTKProcessor()
            
            # 1. Tokenization
            tokens = nltk_proc.tokenize_text(sample_text)
            print("NLTK Sentences:", tokens["sentences"])
            print("NLTK Words:", tokens["words"][:10], "...")
            
            # 2. Stemming vs Lemmatization
            verbs = ["running", "ran", "runs", "better", "am"]
            stem_lem = nltk_proc.stem_vs_lemmatize(verbs)
            print("\nStemming vs Lemmatization:")
            for item in stem_lem:
                print(f"  {item['original']:<8} -> Stem: {item['stemmed']:<8} | Lemma: {item['lemmatized']}")
                
            # 3. Full Pipeline
            print("\nNLTK POS Tagging (Cleaned):")
            print(nltk_proc.process_pipeline(sample_text)[:5], "...")
        except LookupError as e:
            print(f"NLTK Models missing. Please run: python -m nltk.downloader all")
            print(f"Error: {e}")
    else:
        print("NLTK is not available. Skipping NLTK demo.")
        
    print("\n" + "="*50 + "\n")

    if SPACY_AVAILABLE:
        print("--- SpaCy Demonstration ---")
        spacy_proc = SpacyProcessor()
        
        # 1. Full Text Processing
        doc_analysis = spacy_proc.process_text(sample_text)
        print("SpaCy Token Analysis (First 5 tokens):")
        for token in doc_analysis[:5]:
            print(f"  Text: {token['text']:<7} | Lemma: {token['lemma']:<7} | POS: {token['pos']:<5} | Stopword: {token['is_stop']}")
            
        # 2. Named Entity Recognition
        entities = spacy_proc.extract_entities(sample_text)
        print("\nSpaCy Named Entities:")
        for ent, label in entities:
            print(f"  Entity: {ent:<12} | Label: {label}")
            
    else:
        print("SpaCy is not available or model missing. Skipping SpaCy demo.")
        
    print("\n" + "="*50)
    
    # Cosine Similarity Demo
    print("\n--- Cosine Similarity Demo ---")
    s1 = "The cat sat on the mat"
    s2 = "The dog sat on the rug"
    v1 = bag_of_words(s1)
    v2 = bag_of_words(s2)
    sim = cosine_similarity(v1, v2)
    print(f"Sentence 1: {s1}")
    print(f"Sentence 2: {s2}")
    print(f"Cosine Similarity: {sim:.4f}")

    # Benchmarking
    if NLTK_AVAILABLE or SPACY_AVAILABLE:
        benchmark_nlp_libraries(sample_text, iterations=50)

    # Testing
    run_tests()
    
    print("\n========== END OF NLP LESSON ==========\n")
