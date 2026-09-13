"""
# ==============================================================================
# LABORATORY: TRADITIONAL NLP (NLTK & SPACY)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Today, everyone uses LLMs (like GPT-4) for Natural Language Processing.
# However, LLMs are incredibly slow, expensive, and non-deterministic.
#
# If your company needs to scan 100 Million customer reviews overnight to 
# extract every mentioned "Person" or "Organization", using an LLM API will 
# cost $10,000 and take three weeks.
#
# Using traditional NLP libraries like spaCy, you can process 100 Million 
# reviews in 2 hours for $0.00 using pure deterministic Python algorithms!
#
# You must master the foundational concepts of NLP: Lemmatization, Stopwords, 
# Part-of-Speech (POS) tagging, and Named Entity Recognition (NER).
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Clean messy text data using Stopwords and Lemmatization (NLTK/spaCy).
# - Understand the grammatical structure of a sentence (POS Tagging).
# - Extract structured data from unstructured text using NER (spaCy).
#
# ==============================================================================
"""

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. TEXT CLEANING (LEMMATIZATION & STOPWORDS)
# ==============================================================================
def demonstrate_cleaning():
    section_header("Text Normalization (Lemmatization & Stopwords)")
    
    print("If you want to count how many times users mention 'running' in reviews, ")
    print("you must also count 'run', 'ran', and 'runs'.")
    print("Computers treat these as 4 completely different strings!")
    
    print("\n--- 1. Stemming vs Lemmatization ---")
    print("Stemming (NLTK): Brutally chops off the end of words using Regex rules.")
    print("   'running' -> 'run'")
    print("   'better'  -> 'bet' (WRONG!)")
    
    print("\nLemmatization (spaCy): Uses a massive linguistic dictionary and ")
    print("   morphological analysis to find the true dictionary root of the word.")
    print("   'running' -> 'run'")
    print("   'better'  -> 'good' (Perfect!)")
    
    print("\n--- 2. Stopword Removal ---")
    print("Words like 'the', 'is', 'at', 'which', and 'on' provide grammatical ")
    print("glue, but contain zero statistical meaning for machine learning models.")
    print("Standard NLP pipelines mathematically filter out these 'Stopwords' ")
    print("to reduce the size of the dataset and increase the signal-to-noise ratio.")
    
    print("\nOriginal: 'The quick brown foxes were jumping over the lazy dogs.'")
    print("Cleaned : 'quick brown fox jump lazy dog'")


# ==============================================================================
# 4. PART OF SPEECH TAGGING (POS)
# ==============================================================================
def demonstrate_pos_tagging():
    section_header("Part-of-Speech (POS) Tagging")
    
    print("How does a computer know if 'book' is a Noun (a physical book) or ")
    print("a Verb (to book a flight)? It must look at the surrounding context.")
    
    print("\nspaCy uses highly optimized statistical models (Convolutional Neural ")
    print("Networks) to mathematically predict the grammar of every single word.\n")
    
    print("Sentence: 'I want to book a flight to Paris and read a book.'")
    
    print("\nspaCy Output:")
    print("word     | POS   | Explanation")
    print("---------|-------|-------------")
    print("I        | PRON  | Pronoun")
    print("want     | VERB  | Verb")
    print("to       | PART  | Particle")
    print("book     | VERB  | Verb (Correctly identified based on context!)")
    print("a        | DET   | Determiner")
    print("flight   | NOUN  | Noun")
    print("to       | ADP   | Adposition")
    print("Paris    | PROPN | Proper Noun")
    print("and      | CCONJ | Coordinating Conjunction")
    print("read     | VERB  | Verb")
    print("a        | DET   | Determiner")
    print("book     | NOUN  | Noun (Correctly identified based on context!)")


# ==============================================================================
# 5. NAMED ENTITY RECOGNITION (NER)
# ==============================================================================
def demonstrate_ner():
    section_header("Named Entity Recognition (NER)")
    
    print("NER is the most commercially valuable tool in traditional NLP.")
    print("It allows you to extract highly structured JSON data out of raw, ")
    print("unstructured paragraphs.\n")
    
    print("Raw Text:")
    print("'Apple Inc. announced on Tuesday that Tim Cook will visit London ")
    print(" next week to invest $5 Billion in a new AI facility.'")
    
    print("\nspaCy automatically scans the text and outputs:")
    print("Text         | Label | Explanation")
    print("-------------|-------|--------------------------")
    print("Apple Inc.   | ORG   | Companies, agencies, institutions")
    print("Tuesday      | DATE  | Absolute or relative dates")
    print("Tim Cook     | PERSON| People, including fictional")
    print("London       | GPE   | Countries, cities, states")
    print("next week    | DATE  | Absolute or relative dates")
    print("$5 Billion   | MONEY | Monetary values, including unit")
    
    print("\nYou can now write a Python script that scrapes 10,000 news articles, ")
    print("filters for strictly the 'ORG' tags, and builds a database of every ")
    print("single company mentioned in the news today. This runs in seconds, ")
    print("for free, with zero LLM API calls!")


def run_all_labs():
    demonstrate_cleaning()
    demonstrate_pos_tagging()
    demonstrate_ner()


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why is Lemmatization vastly superior to Stemming?
   Answer: Stemming is a dumb, rules-based algorithm that blindly chops suffixes off strings (e.g., chopping "-ing" off "running"). It fails catastrophically on irregular grammar (e.g., stemming "was" to "wa", or "better" to "bet"). Lemmatization uses an actual linguistic dictionary (WordNet) and morphological analysis. It first determines the Part-of-Speech of the word in the context of the sentence, and then looks up the true, grammatically correct dictionary root (e.g., converting "better" to "good", or "am/is/are" to "be"). This produces vastly superior, cleaner data for Machine Learning models.

2. In a Python pipeline processing millions of documents, why would you choose spaCy over OpenAI's GPT-4 for Entity Extraction?
   Answer: Scale, Speed, Cost, and Determinism. GPT-4 is an autoregressive LLM. Processing 1,000,000 documents through an LLM API would cost thousands of dollars, take weeks due to rate limits, and occasionally hallucinate incorrect JSON structures. spaCy uses highly optimized, compiled Cython models under the hood. It runs entirely locally on your CPU (or GPU), costs $0.00, does not require an internet connection, mathematically guarantees a specific output format, and can process tens of thousands of documents per second. For structured data extraction (NER), traditional NLP is almost always the correct engineering choice.

3. Why do we remove "Stopwords" before feeding text into traditional Machine Learning algorithms like Naive Bayes?
   Answer: Traditional ML algorithms (like TF-IDF or Naive Bayes) treat text as a "Bag of Words" and calculate probabilities based on frequency. Words like "the", "and", and "is" are the most frequently used words in the English language. If they are not removed, they mathematically overwhelm the statistical calculations, drowning out the rare, highly important words (like "refund" or "defective"). By filtering out the Stopwords, you drastically reduce the dimensionality of the vector space and massively increase the statistical signal of the meaningful keywords.
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Traditional NLP Completed.")
