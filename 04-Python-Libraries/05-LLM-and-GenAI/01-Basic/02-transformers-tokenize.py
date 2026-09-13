"""
# ==============================================================================
# LABORATORY: ADVANCED TOKENIZATION (ATTENTION MASKS & BATCHING)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# When passing data into a Neural Network, the input MUST be a perfect, 
# rectangular mathematical Matrix (Tensor).
#
# Example Batch:
# Sentence A: "Hello." (1 word)
# Sentence B: "This is a much longer sentence." (6 words)
#
# You cannot feed a jagged, asymmetrical array into a GPU!
# You must "Pad" the short sentences with fake [PAD] tokens (zeros) until they 
# mathematically match the length of the longest sentence in the batch.
#
# But there is a massive problem: If you feed those zeros into the Transformer, 
# the Self-Attention mechanism will do heavy calculus trying to extract the 
# "meaning" and "context" of those fake zeros, destroying the model's accuracy!
#
# The solution is the "Attention Mask".
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand Padding and Truncation.
# - Understand how the Attention Mask isolates signal from noise.
# - Process dynamic batches of varying-length text using `AutoTokenizer`.
#
# ==============================================================================
"""

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

try:
    from transformers import AutoTokenizer
    HAS_TRANSFORMERS = True
except ImportError:
    HAS_TRANSFORMERS = False

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. PADDING AND TRUNCATION
# ==============================================================================
def demonstrate_padding():
    section_header("Rectangular Tensors: Padding & Truncation")
    
    if not HAS_TRANSFORMERS:
        print("[WARNING] transformers not installed.")
        return
        
    try:
        # Load a standard BERT Tokenizer
        tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
        
        # A Batch of exactly 3 strings of wildly different lengths
        batch = [
            "Hello.",
            "This is a medium sentence.",
            "This is an extremely long sentence that will stretch the tensor."
        ]
        
        # 1. THE NAIVE APPROACH (Will Crash)
        # encoded = tokenizer(batch, return_tensors='pt')  # ERROR! Jagged Array!
        
        # 2. THE CORRECT APPROACH (Padding)
        # padding=True tells it to automatically calculate the length of the LONGEST 
        # string in the batch (string #3) and append 0s to strings #1 and #2.
        encoded = tokenizer(batch, padding=True, return_tensors='pt')
        
        print("Successfully generated a perfectly rectangular Tensor!")
        print(f"Tensor Shape: {encoded['input_ids'].shape} (3 sentences, 13 tokens each)\n")
        
        print("Notice the zeros padded to the end of Sentence 1!")
        print(encoded['input_ids'][0])
        
        # 3. TRUNCATION
        # What if a user submits a 10,000-page book? The GPU will run out of VRAM 
        # instantly. BERT has a strict hard limit of 512 tokens.
        # truncation=True forces the Tokenizer to violently chop off any words 
        # beyond the model's maximum context window.
        
        encoded_truncated = tokenizer(
            batch, 
            padding=True, 
            truncation=True, 
            max_length=5, # Artificially truncating to 5 for demonstration
            return_tensors='pt'
        )
        
        print("\nTensor Shape after aggressive Truncation to max_length=5:")
        print(f"{encoded_truncated['input_ids'].shape} (3 sentences, 5 tokens each)")
        
    except Exception as e:
        print(f"Execution skipped: {e}")


# ==============================================================================
# 4. THE ATTENTION MASK
# ==============================================================================
def demonstrate_attention_mask():
    section_header("The Attention Mask (Ignoring Zeros)")
    
    if not HAS_TRANSFORMERS: return
    
    try:
        tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
        
        batch = [
            "Hi.",
            "I love machine learning very much."
        ]
        
        # Process the batch
        encoded = tokenizer(batch, padding=True, return_tensors='pt')
        
        print("Sentence 1 (Input IDs):")
        print(encoded['input_ids'][0])
        print("Sentence 2 (Input IDs):")
        print(encoded['input_ids'][1])
        
        print("\nNotice how Sentence 1 is padded with trailing [PAD] tokens (ID: 0).")
        
        print("\nHere is the Magic: The Attention Mask!")
        print("Sentence 1 (Attention Mask):")
        print(encoded['attention_mask'][0])
        print("Sentence 2 (Attention Mask):")
        print(encoded['attention_mask'][1])
        
        print("\nThe Attention Mask is an exact parallel array of 1s and 0s.")
        print("1 = Real Word (Pay Attention).")
        print("0 = Fake Padding (Ignore Mathematically).")
        print("When the matrix multiplication happens inside the Transformer's ")
        print("Self-Attention heads, the Attention Mask mathematically obliterates ")
        print("the padded zeros before they can poison the context!")
        
    except Exception as e:
        print(f"Execution skipped: {e}")


def run_all_labs():
    demonstrate_padding()
    demonstrate_attention_mask()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why must batches be "padded" before being fed into a Neural Network?
   Answer: A GPU is a massive, highly synchronized matrix multiplication engine. It requires input data to be a perfect, rectangular Matrix (Tensor). You cannot multiply a matrix of shape $(3 \times \text{variable})$ against a Weight matrix. If one sentence has 5 words and another has 12, you must pad the short sentence with 7 fake zeros (`[PAD]` tokens) so that both sentences are mathematically identical in length ($3 \times 12$).

2. If we feed `[PAD]` zeros into the Transformer, won't the AI try to find the semantic "meaning" of a zero?
   Answer: Yes, which is why the Tokenizer outputs a second matrix: the **Attention Mask**. The Attention Mask is a parallel array composed of $1$s (representing real words) and $0$s (representing fake pad tokens). Deep inside the Transformer's architecture, right before the Softmax function calculates the Self-Attention probabilities, it subtracts Infinity ($-\infty$) from every position where the Attention Mask is $0$. The Softmax of $-\infty$ is exactly $0.0$. This completely zeroes out the padding, mathematically guaranteeing that the fake zeros have absolutely zero influence on the final contextual meaning of the sentence.

3. Why is `truncation=True` an absolute necessity for production Web Servers?
   Answer: A standard Transformer model like BERT has a maximum context window of 512 tokens. The mathematical complexity of the Self-Attention mechanism scales quadratically ($O(N^2)$) with the sequence length. If a malicious user pastes a 10,000-word essay into your Sentiment Analysis API and you do not truncate it, the Transformer will attempt to calculate a $10,000 \times 10,000$ attention matrix. This will instantly exceed the GPU's VRAM, crashing the production server with a catastrophic Out-Of-Memory (OOM) error. `truncation=True` enforces a hard mathematical limit, chopping the text safely before it hits the GPU.
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Advanced Tokenization Completed.")
