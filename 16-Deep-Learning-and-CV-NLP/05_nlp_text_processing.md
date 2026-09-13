# NLP Text Processing and Representation

## Prerequisites
- Basic understanding of Python strings and lists.
- Familiarity with probability and statistics (frequencies).
- Basic linear algebra (vectors).

## Objectives
- Understand how text is normalized and cleaned.
- Learn tokenization techniques (word, character, subword).
- Understand Count Vectorization (Bag of Words) and its limitations.
- Learn Term Frequency-Inverse Document Frequency (TF-IDF) scoring.
- Implement text representation pipelines.

## Intuition
Machine learning models, particularly deep learning models, operate on numbers, not text. Therefore, to process human language, we must first translate words and sentences into numerical formats. 
The journey begins by standardizing the text (making it lowercase, removing punctuation), breaking it into manageable pieces (tokens), and then representing these tokens as vectors.
Bag of Words simply counts occurrences, treating a document as an unordered collection of words. TF-IDF improves on this by highlighting words that are frequent in a specific document but rare across all documents, thereby capturing the "importance" of a word.

## Mathematics
### Term Frequency (TF)
The number of times a term $t$ appears in a document $d$, sometimes normalized by the total number of words in the document.
$$ \text{TF}(t, d) = \frac{\text{count of } t \text{ in } d}{\text{total words in } d} $$

### Inverse Document Frequency (IDF)
Measures how much information the word provides. It's the logarithm of the total number of documents $N$ divided by the number of documents containing the term $t$.
$$ \text{IDF}(t) = \log\left(\frac{N}{|\{d \in D : t \in d\}|}\right) $$

### TF-IDF
$$ \text{TF-IDF}(t, d) = \text{TF}(t, d) \times \text{IDF}(t) $$

## Code Reference
Refer to `05_nlp_text_processing.py` for Python implementations of tokenization, Bag of Words, and TF-IDF from scratch and using `scikit-learn`.

## Interview Questions
1. **What is tokenization, and why is subword tokenization preferred in modern NLP?**
   *Answer:* Tokenization is splitting text into units. Subword tokenization (like BPE) handles out-of-vocabulary words better by breaking unknown words into known subword pieces.
2. **What is the main limitation of Bag of Words?**
   *Answer:* It completely ignores word order and context, and often results in highly sparse matrices.
3. **How does TF-IDF improve over simple Count Vectorization?**
   *Answer:* It penalizes highly frequent, uninformative words (like "the", "and") while assigning higher weights to rare, context-specific words.
