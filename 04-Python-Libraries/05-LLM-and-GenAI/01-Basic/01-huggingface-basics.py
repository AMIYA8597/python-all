"""
# ==============================================================================
# LABORATORY: NLP AND LLM FOUNDATIONS (HUGGING FACE)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Five years ago, if you wanted to build an AI that could summarize text or 
# analyze sentiment, you had to manually construct complex LSTMs in PyTorch 
# and train them on massive datasets for weeks.
#
# Today, the open-source community has shifted entirely to "Pre-trained Models".
# Mega-corporations (Google, Meta, OpenAI) spend $10,000,000 training massive 
# Transformer architectures on the entire internet, and then upload the finished, 
# "pretrained" weights to the Hugging Face Model Hub.
#
# The Hugging Face `transformers` library allows you to download these massive 
# brains and run them on your local machine in exactly 3 lines of Python code!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Execute zero-shot NLP tasks using the high-level `pipeline` API.
# - Understand how LLMs read text using `AutoTokenizer`.
# - Understand how LLMs process data using `AutoModel`.
#
# ==============================================================================
"""

import os
# Suppress heavy warnings from transformers
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

try:
    from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
    import torch
    HAS_TRANSFORMERS = True
except ImportError:
    HAS_TRANSFORMERS = False

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE PIPELINE API (HIGH-LEVEL ABSTRACTION)
# ==============================================================================
def demonstrate_pipelines():
    section_header("The Hugging Face Pipeline API")
    
    if not HAS_TRANSFORMERS:
        print("[WARNING] transformers library not installed. Install via: pip install transformers torch")
        return
        
    print("The `pipeline` object is the highest level of abstraction.")
    print("You simply ask for a task ('sentiment-analysis'), and Hugging Face ")
    print("automatically downloads the industry-standard model, loads the tokenizer, ")
    print("processes your string, and returns the answer!\n")
    
    # 1. SENTIMENT ANALYSIS
    print("Initializing Sentiment Analysis Pipeline...")
    # NOTE: In a real environment, this triggers a ~250MB model download on the first run!
    # For this laboratory, we use a tiny, fast model explicitely.
    try:
        classifier = pipeline(
            'sentiment-analysis', 
            model="distilbert-base-uncased-finetuned-sst-2-english"
        )
        
        sentences = [
            "This laboratory is incredibly helpful for understanding AI!",
            "I am completely lost and this code keeps crashing."
        ]
        
        results = classifier(sentences)
        
        for i in range(len(sentences)):
            print(f"Text: '{sentences[i]}'")
            print(f"Result: {results[i]['label']} (Confidence: {results[i]['score']*100:.1f}%)\n")
            
    except Exception as e:
        print(f"Pipeline execution skipped due to network/environment limitations: {e}")


# ==============================================================================
# 4. TOKENIZATION (HOW AI READS TEXT)
# ==============================================================================
def demonstrate_tokenization():
    section_header("AutoTokenizer (Sub-Word Encoding)")
    
    if not HAS_TRANSFORMERS: return
    
    print("Neural Networks CANNOT read the letter 'A' or the word 'Apple'.")
    print("They can only do math on Tensors (matrices of numbers).")
    print("A Tokenizer converts English text into an array of integer IDs using ")
    print("a massive dictionary (Vocabulary) that the model memorized during training.\n")
    
    try:
        # Load the Tokenizer for BERT
        tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
        
        text = "Transformer networks revolutionized machine learning!"
        
        # 1. Convert String to Tokens (Words/Subwords)
        tokens = tokenizer.tokenize(text)
        print(f"Raw Text  : {text}")
        print(f"Tokens    : {tokens}")
        print("(Notice how 'revolutionized' was split into 'revolution' and '##ized'. ")
        print("This is Sub-Word Tokenization! It allows the AI to understand the root ")
        print("of a word even if it has never seen the exact full word before!)\n")
        
        # 2. Convert String directly to Math Tensors (What the model actually receives)
        # return_tensors='pt' tells it to return a PyTorch tensor instead of a Python List.
        encoded_input = tokenizer(text, return_tensors='pt')
        
        print("Mathematical Tensor fed to the Neural Network (input_ids):")
        print(encoded_input['input_ids'])
        
        print("\nNotice the [101] at the start and [102] at the end.")
        print("These are special tokens (CLS and SEP) that the Tokenizer automatically ")
        print("injects to tell the AI where the sentence begins and ends!")
        
    except Exception as e:
        print(f"Tokenizer execution skipped: {e}")


# ==============================================================================
# 5. AUTOMODEL (UNDER THE HOOD)
# ==============================================================================
def demonstrate_automodel():
    section_header("AutoModel (Executing the Forward Pass)")
    
    if not HAS_TRANSFORMERS: return
    
    print("The Pipeline API hides the math. Here is what it actually does ")
    print("under the hood using PyTorch!\n")
    
    try:
        model_name = "distilbert-base-uncased-finetuned-sst-2-english"
        
        # 1. Load Tokenizer and the PyTorch Neural Network Weights
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForSequenceClassification.from_pretrained(model_name)
        
        # 2. Tokenize the text
        text = "This is a masterpiece of software engineering."
        inputs = tokenizer(text, return_tensors="pt")
        
        # 3. Execute the PyTorch Forward Pass!
        # We use torch.no_grad() because we are NOT training the model. We don't 
        # need it to track the heavy calculus gradients, which saves massive RAM.
        with torch.no_grad():
            outputs = model(**inputs)
            
        # 4. Extract the Raw Logits (The raw math output from the final Dense layer)
        logits = outputs.logits
        print(f"Raw Logits: {logits}")
        
        # 5. Apply Softmax to convert raw Logits into Probabilities [0.0 - 1.0]
        probabilities = torch.nn.functional.softmax(logits, dim=-1)
        
        print(f"Probabilities: {probabilities}")
        print(f"Probability of NEGATIVE: {probabilities[0][0]*100:.2f}%")
        print(f"Probability of POSITIVE: {probabilities[0][1]*100:.2f}%")
        
    except Exception as e:
        print(f"AutoModel execution skipped: {e}")


def run_all_labs():
    demonstrate_pipelines()
    demonstrate_tokenization()
    demonstrate_automodel()


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. What is the difference between Word-Level Tokenization and Sub-Word Tokenization (BPE/WordPiece)?
   Answer: Word-level tokenization splits text by spaces (e.g., `["I", "love", "coding"]`). This is terrible because the model treats "code", "coding", and "coder" as three completely independent IDs, wasting vocabulary space. Furthermore, if the model sees a new word like "Transformers", it crashes (Out-Of-Vocabulary error). Modern LLMs use Sub-Word tokenization (like Byte-Pair Encoding). They split rare words into common chunks (e.g., `["Transform", "##ers"]`). This keeps the vocabulary small, preserves root-word meanings, and ensures the model can mathematically process literally any word in existence by breaking it down into known letters/subwords.

2. Why do we load models using `AutoModelForSequenceClassification` instead of just `AutoModel`?
   Answer: The base `AutoModel` ONLY returns the "Hidden States" (the raw mathematical embedding of the sentence in high-dimensional space). It does not output an answer! Hugging Face provides specific "Heads" that attach to the top of the base model. By calling `AutoModelForSequenceClassification`, Hugging Face automatically takes the base BERT model, attaches a brand new Fully Connected (Dense) layer to the top, and configures it to output exactly 2 probabilities (Positive/Negative). If you wanted to do Question Answering, you would use `AutoModelForQuestionAnswering` which attaches a completely different geometric Head!

3. Why do we wrap inference calls in `with torch.no_grad():`?
   Answer: By default, PyTorch's Autograd engine aggressively records every single matrix multiplication in memory so it can calculate calculus derivatives later for Backpropagation (Training). If you are deploying an LLM to a web server just to generate answers (Inference), you are not training it! Wrapping the code in `torch.no_grad()` turns off the calculus engine. This drastically speeds up execution time and cuts RAM/VRAM usage in half, preventing Out-Of-Memory (OOM) crashes in production.
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Hugging Face Basics Completed.")
