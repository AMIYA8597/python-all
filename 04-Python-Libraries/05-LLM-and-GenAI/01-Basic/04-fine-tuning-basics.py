"""
# ==============================================================================
# LABORATORY: LLM FINE-TUNING FOUNDATIONS (HUGGING FACE)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Pre-trained models are incredible, but they are generalized. If you download 
# BERT, it knows standard English. But what if you work for a hospital, and you 
# need it to classify highly complex Medical Research papers? The base model 
# will perform poorly because it has never seen medical terminology.
#
# You must "Fine-Tune" it. You download the massive pre-trained brain (which 
# already knows grammar, syntax, and logic) and you execute a standard PyTorch 
# training loop on your specific medical dataset for a few epochs. 
#
# The model slightly shifts its trillions of weights to adapt to your specific 
# domain. This allows you to achieve 99% accuracy on your proprietary task 
# using only a fraction of the compute power required to train a model from scratch!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the Hugging Face `Trainer` API.
# - Understand `TrainingArguments`.
# - Learn how to freeze base layers to prevent "Catastrophic Forgetting".
#
# ==============================================================================
"""

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

try:
    from transformers import AutoModelForSequenceClassification, TrainingArguments, Trainer
    import torch
    HAS_TRANSFORMERS = True
except ImportError:
    HAS_TRANSFORMERS = False

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. FREEZING THE BASE MODEL
# ==============================================================================
def demonstrate_freezing():
    section_header("Freezing Layers (Preventing Catastrophic Forgetting)")
    
    if not HAS_TRANSFORMERS:
        print("[WARNING] transformers not installed.")
        return
        
    print("When you load `AutoModelForSequenceClassification`, Hugging Face takes ")
    print("the massive pre-trained BERT brain, and literally attaches a brand new, ")
    print("randomly initialized Dense Layer (the 'Head') to the very top.\n")
    
    try:
        model = AutoModelForSequenceClassification.from_pretrained(
            "distilbert-base-uncased", 
            num_labels=2
        )
        
        # If we instantly run Backpropagation, the massive errors from the brand 
        # new, untrained Head will violently propagate backward into the pristine 
        # BERT brain, ripping apart the grammar and logic it spent $1M learning!
        # This is called "Catastrophic Forgetting".
        
        # SOLUTION: We FREEZE the entire base model!
        print("Freezing the Base Model...")
        for name, param in model.distilbert.named_parameters():
            param.requires_grad = False # Turn off the calculus engine for this layer!
            
        # We leave the classifier Head unfrozen!
        for name, param in model.classifier.named_parameters():
            param.requires_grad = True
            
        print("Successfully froze the base architecture.")
        print("During training, ONLY the final classification Head will be modified!\n")
        print("Once the Head is trained, you can unfreeze the base and run a ")
        print("tiny Learning Rate (1e-5) to gently fine-tune the whole structure.")
        
    except Exception as e:
        print(f"Execution skipped: {e}")


# ==============================================================================
# 4. THE TRAINER API
# ==============================================================================
def demonstrate_trainer_api():
    section_header("The Hugging Face Trainer API")
    
    if not HAS_TRANSFORMERS: return
    
    print("Writing a manual PyTorch Training Loop (with zero_grad, backward, ")
    print("and step) is tedious. Hugging Face provides a massive abstraction ")
    print("called the `Trainer` that automates it perfectly for Transformers!\n")
    
    try:
        # 1. DEFINE TRAINING ARGUMENTS
        # This object contains all the MLOps hyperparameters!
        training_args = TrainingArguments(
            output_dir="./results",
            learning_rate=2e-5,          # Very small LR to not destroy the brain
            per_device_train_batch_size=16,
            per_device_eval_batch_size=16,
            num_train_epochs=3,
            weight_decay=0.01,           # Regularization (L2)
            eval_strategy="epoch", # Evaluate at the end of every epoch
            save_strategy="epoch",       # Save checkpoints at the end of every epoch
            logging_dir='./logs',
        )
        
        print("TrainingArguments configured successfully.")
        
        # 2. INSTANTIATE THE TRAINER
        # (We are passing None for datasets just to demonstrate the code structure)
        trainer = Trainer(
            model=None,             # The PyTorch model
            args=training_args,     # The hyperparameters
            train_dataset=None,     # The Tokenized training dataset
            eval_dataset=None,      # The Tokenized validation dataset
        )
        
        print("\nTrainer object instantiated!")
        print("In a real script, calling `trainer.train()` would instantly launch ")
        print("a highly-optimized, multi-GPU training loop with progress bars and ")
        print("automatic checkpoint saving!")
        
    except Exception as e:
        print(f"Execution skipped: {e}")


def run_all_labs():
    demonstrate_freezing()
    demonstrate_trainer_api()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. What is "Catastrophic Forgetting" and how do we prevent it during early Fine-Tuning?
   Answer: When loading a pre-trained LLM for classification, a new, untrained Dense layer (the Head) is bolted onto the top of the network. Because the Head is randomly initialized, its initial predictions are complete garbage, resulting in a massive mathematical Loss. If you run backpropagation normally, those massive error gradients will flow backward through the entire network, violently altering the pristine, pre-trained weights of the base model and causing it to "forget" the English language. To prevent this, you explicitly set `requires_grad = False` on the base model (Freezing it). You train *only* the new Head for a few epochs until it stabilizes. Then, you unfreeze the base model and train the entire network using an extremely small learning rate (e.g., $1e-5$) to gently adapt the base model to the specific domain.

2. Why do we typically use an extremely small Learning Rate (like $2e-5$) when Fine-Tuning a Transformer, compared to standard Neural Networks (like $1e-3$)?
   Answer: A standard Neural Network starts with entirely random, garbage weights. A high learning rate allows it to quickly jump across the loss landscape to find a decent solution. A Pre-Trained Transformer already has mathematically beautiful, highly optimized weights. If you hit those weights with a massive learning rate ($1e-3$), you will blast the network out of its optimal geometric valley and destroy the pre-trained knowledge. You must use a microscopic learning rate so the model only takes tiny, gentle mathematical steps to adapt to your specific dataset without ruining the global architecture.

3. Why is the Hugging Face `Trainer` API preferred over a manual PyTorch loop for LLMs?
   Answer: Training an LLM requires massive MLOps overhead. You must handle half-precision floating point math (FP16) to save VRAM, you must distribute the matrices across multiple GPUs (DataParallel), you must save checkpoints to the hard drive every 500 steps, and you must log metrics to platforms like Weights & Biases or TensorBoard. Writing that manually in PyTorch is 500 lines of highly error-prone Cuda code. The Hugging Face `Trainer` abstracts all of this into a single object. You define `TrainingArguments(fp16=True, save_strategy="epoch")`, and the Trainer automatically handles the multi-GPU distributed Cuda math flawlessly.
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Fine-Tuning Foundations Completed.")
