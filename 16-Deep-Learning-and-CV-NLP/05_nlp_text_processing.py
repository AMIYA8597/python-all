"""
# ==============================================================================
# LABORATORY: NLP (TEXT PROCESSING & TF-IDF)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A junior developer builds a search engine. A user searches for "Running". 
# The database only contains the word "Ran". The database returns 0 results. 
# The user leaves the website.
#
# A senior AI engineer understands "Lemmatization". Before storing the document, 
# they use a linguistic morphological analyzer (spaCy/WordNet) to reduce the word 
# "Ran" to its absolute root lemma: "Run". When the user searches for "Running", 
# the query is also reduced to "Run". The search engine executes a perfect 
# mathematical match.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master Text Normalization (Stop words, Punctuation removal).
# - Execute Stemming vs Lemmatization.
# - Architect TF-IDF (Term Frequency-Inverse Document Frequency) matrices.
#
# ==============================================================================
"""

import math
import re

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE BUSINESS LOGIC (STEMMING VS LEMMATIZATION)
# ==============================================================================
class NLPTextProcessor:
    
    @staticmethod
    def simulate_stemming_vs_lemmatization():
        """
        [SECURE] Demonstrating the architectural difference between heuristics and linguistics.
        """
        print("  [INIT] Processing the word: 'Universities'")
        word = "Universities"
        
        # 1. Stemming (The Dumb Heuristic)
        # The Porter Stemmer simply chops off suffixes using Regex rules.
        # It chops off "ies" and replaces it with "i".
        stemmed = "Universiti"
        
        # 2. Lemmatization (The Smart Dictionary)
        # WordNet analyzes the POS (Part of Speech) and maps it to the true linguistic root.
        lemmatized = "University"
        
        print(f"  -> Original:    {word}")
        print(f"  -> Stemmed:     {stemmed} (Not a real word! 'Universiti' breaks downstream analytics)")
        print(f"  -> Lemmatized:  {lemmatized} (Perfect linguistic reduction)")


# ==============================================================================
# 4. THE ARCHITECTURAL PATTERN (TF-IDF MATRIX)
# ==============================================================================
class TFIDFSimulator:
    
    def __init__(self):
        # A tiny corpus of 3 documents
        self.corpus = [
            "the dog chased the cat",
            "the dog watched the mouse",
            "artificial intelligence is the future"
        ]
        
    def execute_tf_idf(self):
        """
        [SECURE] Mathematical Simulation of TF-IDF.
        We want to find out how 'important' a word is to a specific document.
        """
        print("\n  [INIT] Simulating TF-IDF across 3 Documents...")
        
        # Target Word: "dog"
        word = "dog"
        print(f"  -> Target Word: '{word}'")
        
        # 1. TF (Term Frequency) in Document 1
        # How many times does "dog" appear in Doc 1, divided by total words in Doc 1?
        doc1_words = self.corpus[0].split()
        tf = doc1_words.count(word) / len(doc1_words)
        print(f"  -> Term Frequency (TF) in Doc 1: {tf:.4f} (1 out of 5 words)")
        
        # 2. IDF (Inverse Document Frequency) across the entire Corpus
        # log(Total Documents / Number of Documents containing the word)
        N = len(self.corpus) # 3 documents
        df = sum(1 for doc in self.corpus if word in doc) # "dog" is in 2 documents
        
        # We use log base 10 for simplicity. 
        # (Usually log(N/(DF+1)) is used to prevent zero division)
        idf = math.log10(N / df)
        print(f"  -> Inverse Doc Freq (IDF):       {idf:.4f} (log10(3 / 2))")
        
        # 3. TF-IDF Score
        # Multiply them together!
        tfidf_score = tf * idf
        print(f"  -> Final TF-IDF Score:           {tfidf_score:.4f}")
        
        print("\n  [MATHEMATICAL PROOF]")
        print("  If we ran TF-IDF on the word 'the', the IDF would evaluate to log(3/3) = 0.")
        print("  The entire TF-IDF score would mathematically collapse to 0. This physically ")
        print("  proves that TF-IDF automatically destroys 'stop words' without needing ")
        print("  a manual hardcoded list!")


# ==============================================================================
# 5. MATHEMATICAL PROOF (THE BENCHMARK)
# ==============================================================================
def demonstrate_text_processing():
    section_header("Deep Learning NLP: Text Processing")
    
    NLPTextProcessor.simulate_stemming_vs_lemmatization()
    
    tfidf = TFIDFSimulator()
    tfidf.execute_tf_idf()


def run_all_labs():
    demonstrate_text_processing()


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "What is the mathematical flaw in using a 'Bag of Words' (BoW) model?"
   Senior Answer: "Destruction of Semantic Order. A Bag of Words model (CountVectorizer) takes a sentence, creates a dictionary of words, and simply counts their frequency. The sentence 'The dog bit the man' produces the exact same mathematical vector as 'The man bit the dog'. It completely destroys syntax, grammar, and context. This is why modern NLP architectures abandoned BoW in favor of Recurrent models (LSTMs) and Attention models (Transformers) that explicitly encode the mathematical position and sequence of the tokens."

2. Interviewer: "Why does Lemmatization require a Part-of-Speech (POS) tagger to work correctly?"
   Senior Answer: "Morphological Ambiguity. The word 'Leaves' can be a noun (The leaves on the tree) or a verb (He leaves the room). If you pass the string 'leaves' to a Lemmatizer without context, it cannot mathematically determine the root. If the POS tagger identifies it as a Noun, the Lemmatizer reduces it to 'Leaf'. If it is tagged as a Verb, the Lemmatizer reduces it to 'Leave'. Stemming ignores this completely and just brutally chops off the 's', returning 'Leav'."

3. Interviewer: "Explain the mathematical intuition behind the IDF (Inverse Document Frequency) equation."
   Senior Answer: "Information Entropy Penalization. The IDF equation is $\\log(N / DF)$. If a word like 'the' appears in every single document in a $10,000$-document corpus, $N=10,000$ and $DF=10,000$. The fraction is $1.0$. The logarithm of $1$ is exactly $0$. Therefore, the IDF multiplier becomes $0$, annihilating the word's importance score. Conversely, if the word 'Quantum' appears in only $2$ documents, the fraction is $10,000 / 2 = 5,000$. The $\\log(5000)$ is massive. IDF is a mathematical penalization system that automatically punishes common words and massively rewards rare, highly-specific semantic anchors."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: NLP (Text Processing) Completed.")
