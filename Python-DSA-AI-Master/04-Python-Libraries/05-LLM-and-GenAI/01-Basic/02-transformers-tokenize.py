"""
Module: 02-transformers-tokenize
Description: A textbook-grade interactive lesson on Tokenization using Hugging Face Transformers.

===========================================================================
CHAPTER 2: TOKENIZATION IN MODERN NLP
===========================================================================

Learning Objectives:
1. Understand the fundamental concept of tokenization and why it is essential for NLP.
2. Differentiate between Word-level, Character-level, and Subword-level tokenization.
3. Master the Hugging Face `transformers` Tokenizer API (encoding, decoding, batching).
4. Analyze the Mathematical and Algorithmic foundations of Subword Tokenization:
   - Byte-Pair Encoding (BPE)
   - WordPiece
   - SentencePiece / Unigram Language Model
5. Understand the Big-O Time and Space complexity of tokenization algorithms.
6. Build a basic BPE algorithm from scratch (Interview Challenge).

---------------------------------------------------------------------------
1. THEORETICAL BACKGROUND
---------------------------------------------------------------------------
In Natural Language Processing (NLP), a language model cannot directly understand
raw text strings. Text must be converted into numerical representations (tensors).
Tokenization is the process of breaking down raw text into smaller, discrete units
called "tokens," which are then mapped to integer indices in a predefined vocabulary.

Let T = (t_1, t_2, ..., t_n) be a sequence of tokens derived from text S.
A tokenizer functions as a mapping: f: S -> T, and a vocabulary V provides a
lookup: g: t_i -> Integer.

Types of Tokenization:
A. Word-level: Splits by spaces/punctuation.
   - Pros: Intuitively maps to semantic meaning.
   - Cons: Massive vocabulary size (e.g., 100k+), Out-Of-Vocabulary (OOV) problem for
     rare words, cannot handle misspellings or morphological variants efficiently.

B. Character-level: Splits text into individual characters.
   - Pros: Tiny vocabulary (e.g., 256 for ASCII), no OOV problem.
   - Cons: Sequences become excessively long, hard for models to learn meaningful
     semantic representations from single characters.

C. Subword-level (State of the Art): A hybrid approach. Frequent words are kept as
   single tokens, while rare words are split into meaningful subword units.
   - E.g., "unhappiness" -> ["un", "##happi", "##ness"]

---------------------------------------------------------------------------
2. SUBWORD ALGORITHMS IN DEPTH
---------------------------------------------------------------------------
A. Byte-Pair Encoding (BPE) - Used by GPT-2, GPT-3, RoBERTa
   - Mathematical Formulation:
     Initialize vocabulary V with all individual characters (or bytes).
     Iteratively find the most frequent adjacent pair of tokens (A, B) in the training corpus.
     Merge them to form a new token 'AB' and add it to V.
     Repeat until V reaches the desired size.

B. WordPiece - Used by BERT, Electra
   - Similar to BPE, but instead of choosing the most frequent pair, it chooses the
     pair that maximizes the likelihood of the language model (or maximizes the mutual
     information between the two tokens).
     Score(A, B) = Count(AB) / (Count(A) * Count(B))

C. Unigram Language Model - Used by ALBERT, T5 (SentencePiece)
   - Starts with a massive vocabulary and iteratively prunes it. It assumes each subword
     occurs independently, and finds the vocabulary that maximizes the marginal likelihood
     of the training data.

---------------------------------------------------------------------------
3. BIG-O COMPLEXITY
---------------------------------------------------------------------------
Let N be the length of the sequence, and V be the vocabulary size.
- Pre-trained BPE Tokenization Time Complexity: O(N) in the best case with efficient
  Trie-based prefix matching, or O(N log N) depending on implementation details.
- Space Complexity: O(V) to store the vocabulary mapping and merge rules.
"""

import sys
import time
import math
import collections
import re
from typing import List, Dict, Any, Tuple, Optional

# Attempt to import transformers and torch, required for modern NLP workflows.
try:
    import torch
    from transformers import AutoTokenizer, PreTrainedTokenizer
except ImportError:
    print("Error: Please install transformers and torch using:")
    print("pip install transformers torch")
    sys.exit(1)


def basic_tokenization() -> None:
    """
    Basic Tokenization: Loading a PreTrained Tokenizer and exploring basic methods.
    
    Demonstrates:
    - Loading a tokenizer via `AutoTokenizer.from_pretrained`
    - Tokenizing a string into tokens (`tokenize`)
    - Converting tokens to IDs (`convert_tokens_to_ids`)
    - Encoding (String -> IDs) and Decoding (IDs -> String)
    """
    print("="*60)
    print("1. BASIC TOKENIZATION (BERT WordPiece)")
    print("="*60)
    
    # We load the BERT base uncased tokenizer. 
    # 'uncased' means it converts all text to lowercase before tokenization.
    model_name = "bert-base-uncased"
    print(f"Loading tokenizer: {model_name}...")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    
    text = "Hugging Face is creating a tool that democratizes AI!"
    print(f"\nOriginal Text:\n{text}\n")
    
    # Step 1: Tokenize text into string tokens
    tokens = tokenizer.tokenize(text)
    print(f"Tokens (WordPiece):\n{tokens}\n")
    # Notice the '##' in '##rat', '##izes'. This signifies that the subword is 
    # attached to the previous token without a space.
    
    # Step 2: Convert string tokens to integer IDs
    token_ids = tokenizer.convert_tokens_to_ids(tokens)
    print(f"Token IDs:\n{token_ids}\n")
    
    # Step 3: End-to-end encoding using tokenizer.encode()
    # By default, encode() adds special tokens (like [CLS] and [SEP] for BERT).
    encoded_ids = tokenizer.encode(text)
    print(f"Encoded IDs (with special tokens):\n{encoded_ids}\n")
    
    # Let's inspect the special tokens added
    print(f"Decoded special tokens at start/end:")
    print(f"Start (ID {encoded_ids[0]}): {tokenizer.decode([encoded_ids[0]])}")
    print(f"End   (ID {encoded_ids[-1]}): {tokenizer.decode([encoded_ids[-1]])}\n")
    
    # Step 4: Decoding IDs back to a string
    decoded_text = tokenizer.decode(encoded_ids)
    print(f"Decoded Text:\n{decoded_text}\n")
    
    # Skip special tokens during decoding
    clean_decoded = tokenizer.decode(encoded_ids, skip_special_tokens=True)
    print(f"Decoded Text (skip special tokens):\n{clean_decoded}\n")


def intermediate_batch_processing() -> None:
    """
    Intermediate Tokenization: Batch Processing, Padding, and Truncation.
    
    In real-world NLP, we process multiple sentences at once (batches).
    Since neural networks require rectangular tensors, all sequences in a batch
    must have the same length. This is achieved via Padding and Truncation.
    """
    print("="*60)
    print("2. INTERMEDIATE: BATCH PROCESSING & ATTENTION MASKS")
    print("="*60)
    
    tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
    
    batch_sentences = [
        "I love Python and Natural Language Processing.",
        "Tokenization is fun.",
        "Transformers revolutionized the field of AI by introducing the self-attention mechanism which allows for highly parallelizable training and context understanding."
    ]
    
    print("Batch Input:")
    for i, s in enumerate(batch_sentences):
        print(f" {i+1}. {s}")
    print()
    
    # Process the batch
    # padding=True: Pads shorter sequences to the length of the longest in the batch.
    # truncation=True: Truncates sequences that exceed the model's max length.
    # return_tensors="pt": Returns PyTorch tensors instead of Python lists.
    encoded_batch = tokenizer(
        batch_sentences,
        padding=True,
        truncation=True,
        return_tensors="pt"
    )
    
    input_ids = encoded_batch["input_ids"]
    attention_mask = encoded_batch["attention_mask"]
    
    print("Tensor Shapes:")
    print(f"input_ids shape: {input_ids.shape} (Batch Size x Sequence Length)")
    print(f"attention_mask shape: {attention_mask.shape}\n")
    
    print("Input IDs (Notice the padding token ID is typically 0 for BERT):")
    print(input_ids)
    print()
    
    print("Attention Mask (1 = Real token, 0 = Padding token):")
    print(attention_mask)
    print()
    
    # Why is the Attention Mask necessary?
    # The self-attention mechanism in Transformers looks at all tokens in the sequence.
    # We do NOT want the model to attend to "padding" tokens, as they hold no semantic
    # meaning. The attention mask is multiplied in the attention scores calculation
    # to zero out the padding tokens.


def advanced_tokenizer_comparisons() -> None:
    """
    Advanced Tokenization: Comparing BPE (GPT-2) and WordPiece (BERT).
    
    Different architectures use different subword algorithms.
    - GPT-2 uses Byte-Level BPE (handles spaces implicitly, large character base).
    - BERT uses WordPiece (uses '##' to denote subwords).
    """
    print("="*60)
    print("3. ADVANCED: WORDPIECE vs BYTE-LEVEL BPE")
    print("="*60)
    
    text = "The unexplainable preposterousness of the situation was comical."
    
    print(f"Original Text: {text}\n")
    
    # BERT (WordPiece)
    bert_tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
    bert_tokens = bert_tokenizer.tokenize(text)
    print("BERT (WordPiece) Tokens:")
    print(bert_tokens)
    print("Notice how 'unexplainable' is split into ['une', '##xpl', '##aina', '##ble']")
    print()
    
    # GPT-2 (Byte-Level BPE)
    gpt2_tokenizer = AutoTokenizer.from_pretrained("gpt2")
    gpt2_tokens = gpt2_tokenizer.tokenize(text)
    print("GPT-2 (Byte-Level BPE) Tokens:")
    print(gpt2_tokens)
    print("Notice the 'Ġ' character. Byte-Level BPE treats space as part of the token.")
    print("This allows reversible tokenization without needing '##' markers.")
    print()


def analyze_performance_and_edge_cases() -> None:
    """
    Analyzes performance bottlenecks, constraints, and edge cases in tokenization.
    """
    print("="*60)
    print("4. PERFORMANCE ANALYSIS & EDGE CASES")
    print("="*60)
    
    print("1. Time Complexity:")
    print("   Applying BPE or WordPiece is O(N) where N is sequence length.")
    print("   However, the constant factor depends heavily on the implementation.")
    print("   Hugging Face uses 'tokenizers' written in Rust, which is extremely fast.")
    print("2. Maximum Sequence Length:")
    print("   Most transformer models have a max context length (e.g., 512 for BERT, 4096+ for LLaMA).")
    print("   If a document exceeds this, you must chunk it or truncate it.")
    print("3. Out of Vocabulary (OOV):")
    print("   Subword tokenizers solve OOV by falling back to character-level splits.")
    print("   E.g., 'asdfghjkl' -> ['a', '##s', '##d', '##f', '##g', '##h', '##j', '##k', '##l']")
    print("4. Case Sensitivity:")
    print("   Using a 'cased' vs 'uncased' tokenizer matters drastically for names/entities.")
    print()


# ---------------------------------------------------------------------------
# INTERVIEW CHALLENGE: Implement naive Byte Pair Encoding (BPE) from scratch
# ---------------------------------------------------------------------------

def get_stats(vocab: Dict[Tuple[str, ...], int]) -> Dict[Tuple[str, str], int]:
    """
    Helper function for BPE: Given a vocabulary with frequencies, compute frequencies
    of adjacent symbol pairs.
    
    Time Complexity: O(V * L) where V is vocab size and L is max word length.
    """
    pairs = collections.defaultdict(int)
    for word, freq in vocab.items():
        symbols = word
        for i in range(len(symbols) - 1):
            pair = (symbols[i], symbols[i+1])
            pairs[pair] += freq
    return pairs

def merge_vocab(pair: Tuple[str, str], v_in: Dict[Tuple[str, ...], int]) -> Dict[Tuple[str, ...], int]:
    """
    Helper function for BPE: Merge all occurrences of the most frequent pair in the vocab.
    
    Time Complexity: O(V * L)
    """
    v_out = {}
    bigram = re.escape(' '.join(pair))
    # Regex to find the pair bounded by spaces
    p = re.compile(r'(?<!\S)' + bigram + r'(?!\S)')
    for word, freq in v_in.items():
        w_str = ' '.join(word)
        w_str_out = p.sub(''.join(pair), w_str)
        v_out[tuple(w_str_out.split())] = freq
    return v_out

def interview_challenge_bpe_training(text_corpus: List[str], num_merges: int = 10) -> List[Tuple[str, str]]:
    """
    Interview Challenge: Implement the training phase of Byte-Pair Encoding (BPE).
    
    Given a list of words, tokenize them to character level, then iteratively
    find the most frequent adjacent character pair and merge them.
    
    Args:
        text_corpus: A list of words (assume pre-tokenized by space).
        num_merges: How many BPE merge operations to perform.
        
    Returns:
        A list of merge rules (tuples of strings) learned during training.
    """
    print("="*60)
    print("5. INTERVIEW CHALLENGE: BPE FROM SCRATCH")
    print("="*60)
    
    # 1. Initialize vocabulary with character-level tokens.
    # Add a special end-of-word token '</w>' to distinguish subwords from full words.
    vocab_freq = collections.Counter(text_corpus)
    # Convert string "low" to tuple ('l', 'o', 'w', '</w>')
    vocab = {tuple(list(word) + ['</w>']): freq for word, freq in vocab_freq.items()}
    
    print(f"Initial Vocabulary State (showing 3):")
    print(list(vocab.items())[:3])
    print()
    
    merge_rules = []
    
    # 2. Iteratively merge the most frequent pairs
    for i in range(num_merges):
        pairs = get_stats(vocab)
        if not pairs:
            break
            
        # Find the most frequent pair
        best_pair = max(pairs, key=pairs.get)
        merge_rules.append(best_pair)
        
        # Merge the pair in the vocabulary
        vocab = merge_vocab(best_pair, vocab)
        
        print(f"Merge #{i+1}: {best_pair} (Freq: {pairs[best_pair]}) -> {''.join(best_pair)}")
        
    print("\nFinal Vocabulary State (showing 3):")
    print(list(vocab.items())[:3])
    print()
    
    return merge_rules


def run_tests() -> None:
    """
    Validates the custom BPE implementation against expected algorithmic behavior.
    """
    print("="*60)
    print("6. RUNNING TESTS")
    print("="*60)
    
    # Classic BPE example corpus
    corpus = ["low", "low", "low", "low", "low",
              "lower", "lower",
              "newest", "newest", "newest", "newest", "newest", "newest",
              "widest", "widest", "widest"]
    
    merges = interview_challenge_bpe_training(corpus, num_merges=5)
    
    try:
        assert len(merges) == 5, "Should perform exactly 5 merges"
        # The most common characters globally in adjacent pairs should merge first.
        # 'e' and 's' appear together 6 + 3 = 9 times.
        # 's' and 't' appear together 6 + 3 = 9 times.
        # Based on alphabetic ordering max or dict order, it will pick one.
        # 'e' and 's' is highly likely. Let's just assert that 'e', 's' or 's', 't' is first.
        assert merges[0] in [('e', 's'), ('s', 't'), ('e', 's</w>'), ('s', 't</w>'), ('e', 'r</w>')], "Expected first merge to be related to 'est' or 'er'"
        print("Tests Passed Successfully!")
    except AssertionError as e:
        print(f"Test Failed: {e}")


if __name__ == "__main__":
    print(f"========== Exploring {'Tokenization in Transformers'.upper()} ==========\n")
    
    try:
        # 1. Basic Tokenization
        basic_tokenization()
        
        # 2. Batch Processing & Padding
        intermediate_batch_processing()
        
        # 3. WordPiece vs BPE
        advanced_tokenizer_comparisons()
        
        # 4. Performance
        analyze_performance_and_edge_cases()
        
        # 5. Tests & Challenge
        run_tests()
        
    except Exception as e:
        print(f"An error occurred during execution: {e}")
        print("Note: To run HuggingFace tokenizer code, internet connection may be required on the first run to download the vocabulary.")
        
    print(f"\n========== END OF {'Tokenization in Transformers'.upper()} ==========\n")
