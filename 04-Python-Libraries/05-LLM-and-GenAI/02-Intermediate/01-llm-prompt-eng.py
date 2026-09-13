"""
# ==============================================================================
# LABORATORY: ADVANCED PROMPT ENGINEERING & CONTEXT DESIGN
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# LLMs are mathematical prediction engines. They do not "think". They predict 
# the most statistically likely next word based on the context window.
#
# If your prompt is: "Solve this math problem.", the model might output the 
# wrong answer because it just immediately guesses the final number. 
#
# If your prompt is: "Solve this math problem. Think step-by-step.", you 
# fundamentally alter the mathematical trajectory of the generation. By forcing 
# the model to generate the intermediate logical steps, those generated steps 
# become part of the Context Window. When it finally predicts the answer, it 
# has the entire mathematical proof sitting in its Context to condition on, 
# resulting in a drastically higher probability of correctness.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the architecture of Chat Templates (System, User, Assistant).
# - Master Few-Shot Prompting (In-Context Learning).
# - Master Chain of Thought (CoT) Prompting.
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
# 3. CHAT TEMPLATES (SYSTEM, USER, ASSISTANT)
# ==============================================================================
def demonstrate_chat_templates():
    section_header("Instruction-Tuned Models & Chat Templates")
    
    if not HAS_TRANSFORMERS:
        print("[WARNING] transformers not installed.")
        return
        
    print("Base models (like base LLaMA) only know how to complete sentences.")
    print("Instruction-Tuned models (like ChatGPT) are explicitly fine-tuned to ")
    print("understand a specific conversational format using special tokens.\n")
    
    try:
        # We load a tokenizer from an Instruction-Tuned model
        tokenizer = AutoTokenizer.from_pretrained("HuggingFaceH4/zephyr-7b-beta")
        
        # We define a standard list of Dictionaries representing the conversation
        messages = [
            {"role": "system", "content": "You are a sarcastic AI assistant."},
            {"role": "user", "content": "What is the capital of France?"},
            {"role": "assistant", "content": "Oh, let me think... it's Paris, obviously."},
            {"role": "user", "content": "What about Japan?"}
        ]
        
        print("Raw Python Message List:")
        for m in messages:
            print(f"[{m['role'].upper()}] {m['content']}")
            
        print("\nApplying the model's specific Chat Template...")
        # apply_chat_template automatically injects the model-specific special 
        # tokens (like <|system|>, <s>, [INST]) into the string!
        formatted_prompt = tokenizer.apply_chat_template(
            messages, 
            tokenize=False, # We want to see the string, not the math tensors
            add_generation_prompt=True # Prepares the string for the AI to reply!
        )
        
        print(f"\nFormatted String sent to the GPU:\n{formatted_prompt}")
        
    except Exception as e:
        print(f"Execution skipped: {e}")


# ==============================================================================
# 4. FEW-SHOT PROMPTING (IN-CONTEXT LEARNING)
# ==============================================================================
def demonstrate_few_shot():
    section_header("Few-Shot Prompting (In-Context Learning)")
    
    print("Zero-Shot Prompting is asking the AI to do a task with no examples.")
    print("Few-Shot Prompting involves passing 3 to 5 perfect examples of the ")
    print("Input and Output directly inside the Prompt. The AI mathematically ")
    print("detects the pattern and perfectly mimics the formatting.\n")
    
    prompt = """
    Convert the following sentences into JSON format containing "intent" and "entity".

    [Example 1]
    Input: "Book a flight to London."
    Output: {"intent": "book_flight", "entity": "London"}

    [Example 2]
    Input: "Cancel my reservation at the Marriott."
    Output: {"intent": "cancel_hotel", "entity": "Marriott"}

    [Task]
    Input: "Order a pizza to 123 Main St."
    Output: 
    """
    
    print(prompt)
    print("The model will now perfectly output the JSON format without ever ")
    print("being explicitly fine-tuned to do so!")


# ==============================================================================
# 5. CHAIN OF THOUGHT (CoT)
# ==============================================================================
def demonstrate_chain_of_thought():
    section_header("Chain of Thought (CoT) Prompting")
    
    print("If you ask a complex logic question, a standard LLM will immediately ")
    print("output the final answer, which is often a hallucination.")
    print("Chain of Thought forces the model to generate the intermediate steps, ")
    print("effectively giving it a 'Scratchpad' in the Context Window to work out ")
    print("the math before finalizing the answer.\n")
    
    bad_prompt = "Q: If John has 5 apples, eats 2, buys 10, and gives half away, how many does he have? A:"
    
    good_prompt = """
    Q: If John has 5 apples, eats 2, buys 10, and gives half away, how many does he have?
    A: Let's think step by step.
    1. John starts with 5 apples.
    2. He eats 2. (5 - 2 = 3).
    3. He buys 10 more. (3 + 10 = 13).
    4. He gives half away. (13 / 2 = 6.5).
    Therefore, the final answer is 6.5.
    
    Q: If Mary has 10 balloons, pops 3, finds 5, and loses a quarter of them, how many does she have?
    A: Let's think step by step.
    """
    
    print("Bad Prompt (Zero-Shot):")
    print(bad_prompt)
    
    print("\nGood Prompt (Few-Shot Chain of Thought):")
    print(good_prompt)


def run_all_labs():
    demonstrate_chat_templates()
    demonstrate_few_shot()
    demonstrate_chain_of_thought()


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. What is the fundamental difference between a "Base" model and an "Instruction-Tuned" model?
   Answer: A Base model (like `Llama-2-7b`) is trained purely on Next-Token Prediction over the internet. If you prompt it with "What is the capital of France?", it might complete the sentence with "...and what is the capital of Spain?". It doesn't know it is supposed to answer you; it just completes the document. An Instruction-Tuned model (like `Llama-2-7b-chat`) takes the Base model and Fine-Tunes it on thousands of specific conversational pairs (User: X, Assistant: Y) using special formatting tokens. This fundamentally alters the model's statistical distribution, forcing it to behave as a helpful conversational agent that answers questions instead of just continuing paragraphs.

2. Mathematically, why does "Chain of Thought" (CoT) prompting increase accuracy on logic puzzles?
   Answer: An LLM is an autoregressive engine. Every time it generates a word, it appends that word to the Context Window, and uses the *entire* Context Window to predict the next word. If you force it to answer immediately, it must mathematically map a complex paragraph directly to a single final number, which is highly prone to error. If you append "Let's think step by step", the model starts generating intermediate logical sentences. Because those intermediate sentences are now physically present in the Context Window, the final matrix multiplication is mathematically conditioned on the correct logical proof, virtually eliminating hallucinations.

3. Why is `apply_chat_template` critical when swapping between different Open-Source models?
   Answer: Every AI company fine-tunes their Instruction models using a completely different string format. LLaMA uses `[INST] Message [/INST]`. Zephyr uses `<|user|>\nMessage</s>`. ChatML uses `<|im_start|>user\nMessage<|im_end|>`. If you pass a LLaMA string into a Zephyr model, the Zephyr model will mathematically freak out because it has literally never seen the `[INST]` token during training! `apply_chat_template` abstracts this. You provide a standard Python list of dictionaries, and the Tokenizer automatically queries the model's configuration file to inject the exact correct special tokens required for that specific architecture.
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Advanced Prompt Engineering Completed.")
