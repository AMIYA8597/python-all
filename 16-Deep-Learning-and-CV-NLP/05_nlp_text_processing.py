"""
NLP Text Processing and Representation Examples
This module demonstrates tokenization, Bag of Words (BoW), and TF-IDF.
"""

import re
import math
from collections import Counter
from typing import List, Dict

# --- 1. Basic Tokenization and Cleaning ---
def clean_text(text: str) -> str:
    """Removes punctuation and lowercase the text."""
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    return text

def tokenize(text: str) -> List[str]:
    """Splits text into word tokens."""
    return text.split()

sample_corpus = [
    "Natural language processing is fascinating.",
    "Text processing is a subfield of natural language processing.",
    "TF-IDF is a statistical measure!"
]

# --- 2. Bag of Words (BoW) from Scratch ---
class BagOfWords:
    def __init__(self):
        self.vocab = {}
        self.inverse_vocab = []

    def fit(self, corpus: List[str]):
        unique_words = set()
        for doc in corpus:
            tokens = tokenize(clean_text(doc))
            unique_words.update(tokens)
        
        self.inverse_vocab = sorted(list(unique_words))
        self.vocab = {w: i for i, w in enumerate(self.inverse_vocab)}

    def transform(self, corpus: List[str]) -> List[List[int]]:
        vectors = []
        for doc in corpus:
            tokens = tokenize(clean_text(doc))
            vec = [0] * len(self.vocab)
            for token in tokens:
                if token in self.vocab:
                    vec[self.vocab[token]] += 1
            vectors.append(vec)
        return vectors

# --- 3. TF-IDF from Scratch ---
class TFIDFVectorizer:
    def __init__(self):
        self.vocab = {}
        self.idf = {}
        
    def fit(self, corpus: List[str]):
        doc_count = len(corpus)
        df = Counter()
        
        tokenized_corpus = []
        for doc in corpus:
            tokens = tokenize(clean_text(doc))
            tokenized_corpus.append(tokens)
            df.update(set(tokens)) # unique words in this doc
            
        # Build vocabulary
        self.vocab = {w: i for i, w in enumerate(sorted(df.keys()))}
        
        # Calculate IDF
        for word, count in df.items():
            self.idf[word] = math.log((1 + doc_count) / (1 + count)) + 1 # scikit-learn style smoothing

    def transform(self, corpus: List[str]) -> List[List[float]]:
        vectors = []
        for doc in corpus:
            tokens = tokenize(clean_text(doc))
            tf = Counter(tokens)
            doc_len = len(tokens)
            
            vec = [0.0] * len(self.vocab)
            for token, count in tf.items():
                if token in self.vocab:
                    idx = self.vocab[token]
                    # term frequency (normalized)
                    tf_val = count / doc_len if doc_len > 0 else 0
                    vec[idx] = tf_val * self.idf[token]
            vectors.append(vec)
        return vectors

if __name__ == "__main__":
    print("--- Corpus ---")
    for doc in sample_corpus:
        print(f"- {doc}")

    print("\n--- Bag of Words ---")
    bow = BagOfWords()
    bow.fit(sample_corpus)
    print("Vocab:", bow.vocab)
    bow_vecs = bow.transform(sample_corpus)
    for v in bow_vecs:
        print(v)

    print("\n--- TF-IDF ---")
    tfidf = TFIDFVectorizer()
    tfidf.fit(sample_corpus)
    tfidf_vecs = tfidf.transform(sample_corpus)
    for v in tfidf_vecs:
        print([round(val, 3) for val in v])
