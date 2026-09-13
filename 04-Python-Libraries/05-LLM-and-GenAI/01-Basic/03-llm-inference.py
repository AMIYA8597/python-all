"""
# ==============================================================================
# LABORATORY: LLM INFERENCE (CAUSAL TEXT GENERATION)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You have learned how to use BERT for Classification (reading a sentence and 
# outputting a category). But how does ChatGPT actually write text?
#
# It uses an Autoregressive Causal Language Model (like GPT-2, Llama, or Mistral).
# 
# The architecture is shockingly simple. You feed it a prompt: "The cat sat on the".
# The LLM does a massive matrix multiplication and outputs a probability array 
# for every single word in the English dictionary (e.g. "mat" = 90%, "dog" = 1%).
# 
# The Python script selects "mat", appends it to the sentence, and feeds the 
# entirely new sentence ("The cat sat on the mat") back into the model to predict 
# the next word. This loops forever until it generates a [STOP] token.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand `AutoModelForCausalLM` and Autoregressive generation.
# - Execute `model.generate()`.
# - Control hallucination and creativity using Temperature, Top-K, and Top-P.
#
# ==============================================================================
"""

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

try:
    from transformers import AutoTokenizer, AutoModelForCausalLM
    import torch
    HAS_TRANSFORMERS = True
except ImportError:
    HAS_TRANSFORMERS = False

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. TEXT GENERATION (GREEDY DECODING)
# ==============================================================================
def demonstrate_generation():
    section_header("Autoregressive Generation (Greedy)")
    
    if not HAS_TRANSFORMERS:
        print("[WARNING] transformers not installed.")
        return
        
    print("We will use GPT-2, the grandfather of modern ChatGPT.\n")
    
    try:
        model_id = "gpt2"
        tokenizer = AutoTokenizer.from_pretrained(model_id)
        
        # We use ForCausalLM instead of ForSequenceClassification!
        model = AutoModelForCausalLM.from_pretrained(model_id)
        
        prompt = "The future of artificial intelligence is"
        print(f"PROMPT: '{prompt}'")
        
        # 1. Tokenize the prompt
        inputs = tokenizer(prompt, return_tensors="pt")
        
        # 2. Generate!
        # max_length: Generate up to 30 tokens.
        # This is GREEDY decoding. It always picks the exact #1 highest probability 
        # word mathematically. It is very robotic.
        outputs = model.generate(
            inputs['input_ids'], 
            max_length=30,
            pad_token_id=tokenizer.eos_token_id
        )
        
        # 3. Decode the Tensor back into English string
        result = tokenizer.decode(outputs[0], skip_special_tokens=True)
        print(f"\nGREEDY RESULT: '{result}'")
        
    except Exception as e:
        print(f"Generation execution skipped: {e}")


# ==============================================================================
# 4. CONTROLLING CREATIVITY (TEMPERATURE, TOP-P, TOP-K)
# ==============================================================================
def demonstrate_sampling():
    section_header("Controlling Creativity (Sampling Parameters)")
    
    if not HAS_TRANSFORMERS: return
    
    try:
        model_id = "gpt2"
        tokenizer = AutoTokenizer.from_pretrained(model_id)
        model = AutoModelForCausalLM.from_pretrained(model_id)
        
        prompt = "Once upon a time in a dark forest,"
        inputs = tokenizer(prompt, return_tensors="pt")
        
        print(f"PROMPT: '{prompt}'")
        
        print("\n--- 1. TEMPERATURE ---")
        print("Temperature scales the raw Logits before Softmax.")
        print("T = 0.1: Very strict, robotic, always picks the highest probability.")
        print("T = 2.0: Wild, hallucinates, makes extremely chaotic choices.")
        
        # HIGH TEMPERATURE (Chaotic)
        out_high_temp = model.generate(
            inputs['input_ids'], 
            max_length=40,
            do_sample=True, # MUST BE TRUE to use Temperature!
            temperature=1.5,
            pad_token_id=tokenizer.eos_token_id
        )
        print(f"High Temp (1.5): {tokenizer.decode(out_high_temp[0])}")
        
        print("\n--- 2. TOP-K SAMPLING ---")
        print("Sort the dictionary by probability. Throw away everything except ")
        print("the Top K (e.g. 50) words. Randomly roll a dice to pick one of those 50.")
        
        out_top_k = model.generate(
            inputs['input_ids'], 
            max_length=40,
            do_sample=True,
            top_k=50,
            pad_token_id=tokenizer.eos_token_id
        )
        print(f"Top-K (50)     : {tokenizer.decode(out_top_k[0])}")
        
        print("\n--- 3. TOP-P SAMPLING (NUCLEUS) ---")
        print("Instead of a fixed number of words, dynamically take words until ")
        print("their combined probability reaches P (e.g. 95%). If the model is ")
        print("highly confident, it might only pick from 2 words. If confused, 100 words.")
        
        out_top_p = model.generate(
            inputs['input_ids'], 
            max_length=40,
            do_sample=True,
            top_p=0.92,
            pad_token_id=tokenizer.eos_token_id
        )
        print(f"Top-P (0.92)   : {tokenizer.decode(out_top_p[0])}")
        
    except Exception as e:
        print(f"Generation execution skipped: {e}")


def run_all_labs():
    demonstrate_generation()
    demonstrate_sampling()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. What does `do_sample=True` actually do in the `model.generate()` function?
   Answer: If `do_sample=False` (Greedy Decoding), the model looks at the probability array for the next word and simply selects the single highest number (`argmax`). It is completely deterministic and robotic. If you run it 100 times, it outputs the exact same paragraph 100 times. Setting `do_sample=True` enables probabilistic sampling. If the word "apple" has a 60% probability and "orange" has a 40% probability, the Python code literally rolls a 100-sided mathematical dice. 40% of the time, it will purposely choose "orange" even though it wasn't the #1 highest mathematical choice! This generates highly creative, varied text (like a real human).

2. How does Temperature mathematically alter the output probabilities?
   Answer: Before applying the Softmax function (which turns numbers into percentages), the network outputs raw, unscaled numbers called Logits. Temperature is a scalar divisor applied directly to the Logits: $Logits / T$. 
   If $T = 1.0$, the math is unchanged. 
   If $T = 0.1$ (Low), dividing by a tiny number causes the Logits to mathematically explode in magnitude. The largest Logit becomes astronomical, and after Softmax, its probability shoots to 99.9%, forcing the model to be strict and robotic. 
   If $T = 2.0$ (High), dividing by 2 compresses all Logits closely together. After Softmax, the probabilities level out (e.g., 55% vs 45%), causing the model to make wild, random, hallucinatory choices.

3. Why is Top-P (Nucleus Sampling) generally considered superior to Top-K?
   Answer: Top-K is a hard, static cutoff. If you set $K=50$, it will always look at exactly 50 words. If the model is predicting the sentence "I drove the...", the only logical next word is "car". The probability of "car" might be 99.9%. But because $K=50$, you force the model to keep 49 completely illogical garbage words in the dice roll, risking a catastrophic hallucination! 
   Top-P dynamically adjusts. If you set $P=0.90$, it adds words to the pool until the sum of their probabilities equals 90%. In the "car" example, "car" is 99.9%, which instantly satisfies the 90% threshold! The pool stops at exactly 1 word, mathematically preventing a hallucination. If the sentence was open-ended, the probabilities might be very low, and Top-P would naturally expand the pool to 100 words to encourage creativity.
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: LLM Inference & Text Generation Completed.")
