"""
# ==============================================================================
# LABORATORY: ADVANCED LLM FINE-TUNING (LoRA & QLoRA)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# In the Basic Fine-Tuning lab, we froze a tiny BERT model (110M parameters) 
# and trained a new classification head. 
#
# But what if you want to fine-tune a massive LLaMA-3 model (8 Billion parameters) 
# to act like a specific character or learn your proprietary company code?
#
# A standard "Full Fine-Tune" requires unfreezing all 8 Billion weights. To 
# calculate the calculus gradients and Adam optimizer states for 8 Billion weights, 
# you need roughly 120 GB of VRAM. You would need to rent a cluster of 8x A100 GPUs 
# costing $30/hour.
#
# We solve this using PEFT (Parameter-Efficient Fine-Tuning), specifically LoRA 
# and QLoRA. This mathematical breakthrough allows you to fine-tune a massive 
# 8-Billion parameter LLM on a single consumer graphics card (like an RTX 3090 
# or a Colab T4) in just a few hours!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the Mathematics of LoRA (Low-Rank Adaptation).
# - Understand QLoRA (4-bit Quantization).
# - Understand how to merge LoRA adapters back into the Base Model.
#
# ==============================================================================
"""

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. LoRA (LOW-RANK ADAPTATION)
# ==============================================================================
def demonstrate_lora_math():
    section_header("The Mathematics of LoRA")
    
    print("Imagine the Attention Layer of an LLM. It is a massive square Matrix ")
    print("of weights, e.g., 4096 x 4096. That is 16.7 Million parameters for ")
    print("just ONE layer!")
    
    print("\nIf we unfreeze it, we have to train 16.7M weights. (Impossible on 1 GPU).")
    
    print("\n--- The LoRA Solution ---")
    print("1. We completely FREEZE the massive 4096 x 4096 base matrix.")
    print("2. We inject two tiny, new matrices next to it:")
    print("   Matrix A: Shape (4096 x 8)")
    print("   Matrix B: Shape (8 x 4096)")
    print("   (The '8' is the 'Rank' or 'r'. It is the bottleneck).")
    
    print("\nLet's calculate the parameters:")
    print("Matrix A: 4096 * 8 = 32,768 weights")
    print("Matrix B: 8 * 4096 = 32,768 weights")
    print("Total trainable weights: 65,536.")
    
    print("\nWe reduced the training burden from 16,700,000 weights down to 65,000!")
    print("That is a 99.6% reduction in VRAM requirement!")
    
    print("\nDuring the forward pass, data flows through the frozen Base Matrix, ")
    print("AND simultaneously flows through Matrix A -> Matrix B. The outputs ")
    print("are simply added together. We train ONLY the tiny A and B matrices!")


# ==============================================================================
# 4. QLoRA (QUANTIZED LoRA)
# ==============================================================================
def demonstrate_qlora():
    section_header("QLoRA (4-bit Quantization)")
    
    print("LoRA reduces the *training* (gradient) VRAM, but you still have to ")
    print("load the massive 8 Billion parameter Base Model into RAM just to ")
    print("execute the forward pass! At 16-bit float (FP16), an 8B model ")
    print("requires 16 GB of VRAM just to sit idle.")
    
    print("\n--- The QLoRA Solution (bitsandbytes) ---")
    print("Quantization is the process of crushing high-precision numbers into ")
    print("low-precision integers.")
    
    print("\n1. FP16 (16 bits): Can represent numbers like 3.14159...")
    print("2. INT8  (8 bits): Can represent integers from -128 to 127.")
    print("3. NF4   (4 bits): Can represent exactly 16 specific numbers!")
    
    print("\nQLoRA violently crushes the frozen 8 Billion parameter Base Model ")
    print("down to 4-bit precision! The model size shrinks from 16 GB to 4 GB!")
    
    print("\nWait, doesn't crushing the math ruin the LLM's brain?")
    print("Yes! It heavily degrades performance. BUT...")
    print("Because we are simultaneously training the FP16 LoRA adapters (A and B), ")
    print("the tiny, high-precision LoRA matrices mathematically 'correct' the ")
    print("errors introduced by the 4-bit base model during backpropagation!")
    
    print("\nResult: You get 99% of the performance of a Full FP16 Fine-Tune, ")
    print("but it fits on a single, cheap 8 GB graphics card!")


# ==============================================================================
# 5. PEFT CONFIGURATION & ADAPTER MERGING
# ==============================================================================
def demonstrate_peft():
    section_header("PEFT and Adapter Merging")
    
    print("In PyTorch/Hugging Face, you implement this using the PEFT library.")
    print("(Parameter-Efficient Fine-Tuning).\n")
    
    print("```python")
    print("from peft import LoraConfig, get_peft_model")
    print("from transformers import BitsAndBytesConfig")
    print("\n# 1. Configure 4-bit Quantization for the Base Model")
    print("bnb_config = BitsAndBytesConfig(")
    print("    load_in_4bit=True,")
    print("    bnb_4bit_quant_type='nf4',")
    print("    bnb_4bit_compute_dtype=torch.float16")
    print(")")
    print("\n# 2. Configure the LoRA Matrices")
    print("lora_config = LoraConfig(")
    print("    r=8,               # The Bottleneck dimension")
    print("    lora_alpha=16,     # Scaling factor")
    print("    target_modules=['q_proj', 'v_proj'], # Which Attention matrices to attach to")
    print("    bias='none',")
    print("    task_type='CAUSAL_LM'")
    print(")")
    print("\n# 3. Wrap the Model")
    print("model = get_peft_model(base_model, lora_config)")
    print("```")
    
    print("\n--- ADAPTER MERGING ---")
    print("When training finishes, you do NOT save an 8 Billion parameter model!")
    print("You save the LoRA adapter (the A and B matrices). It is a tiny ")
    print("30 Megabyte file! You can email it to a friend.")
    print("\nTo use it in production:")
    print("1. Load the pristine Base Model.")
    print("2. Load the 30MB LoRA adapter.")
    print("3. Multiply A * B to get a (4096 x 4096) matrix.")
    print("4. Physically ADD that matrix into the frozen Base Matrix.")
    print("The weights are permanently 'Merged' into a single architecture, ")
    print("meaning inference speed is 100% identical to the base model with zero latency!")


def run_all_labs():
    demonstrate_lora_math()
    demonstrate_qlora()
    demonstrate_peft()


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Mathematically, why do we use two matrices ($A$ and $B$) in LoRA instead of just creating one small matrix?
   Answer: Matrix multiplication defines dimensionality. If the base Attention layer expects an input vector of length 4096 and outputs a vector of length 4096, the weight matrix MUST be $4096 \times 4096$. You cannot just add a $100 \times 100$ matrix to it; the tensor shapes will crash. LoRA uses Matrix Decomposition. Matrix $A$ ($4096 \times 8$) compresses the 4096-dimensional input down to 8 dimensions. Matrix $B$ ($8 \times 4096$) decompresses it back to 4096. When multiplied together ($A \times B$), the resulting matrix is exactly $4096 \times 4096$, allowing it to be seamlessly added to the base weights, while only requiring us to train $65,000$ parameters instead of $16.7$ million!

2. What is the difference between LoRA and QLoRA?
   Answer: LoRA solves the *Gradient* VRAM problem by drastically reducing the number of trainable parameters (from billions to millions). However, LoRA still requires the Base Model to be loaded into VRAM at full 16-bit or 32-bit precision, which is impossible for an 8B model on a consumer GPU. QLoRA solves the *Base Model* VRAM problem. It uses `bitsandbytes` to Quantize (compress) the frozen Base Model down to 4-bit (NF4) precision. This shrinks the model size by 75%. QLoRA combines the 4-bit base model with 16-bit LoRA adapters, unlocking the ability to fine-tune massive LLMs on a single 12GB GPU.

3. Why is Adapter Merging critical for production inference?
   Answer: During training, the Base Model and the LoRA adapters exist as separate mathematical entities. For every token generated, the data must pass through the Base Matrix, *and* pass through Matrix A, *and* pass through Matrix B, and then the results are summed. This adds significant latency. Because matrix addition is mathematically distributive ($Wx + \Delta Wx = (W + \Delta W)x$), we can permanently multiply $A \times B$ to get $\Delta W$, and physically add it to the base weights $W$. The LoRA adapter vanishes, the architecture becomes a standard single-matrix LLM again, and inference speed returns to absolute maximum with zero overhead.
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Advanced LLM Fine-Tuning (LoRA) Completed.")
