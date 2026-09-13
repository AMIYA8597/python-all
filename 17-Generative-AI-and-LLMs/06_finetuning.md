# Fine-Tuning and Parameter-Efficient Fine-Tuning (PEFT)

## 1. Prerequisites
- **Deep Learning Fundamentals:** Understanding of weights, gradients, backpropagation, and loss functions.
- **LLM Fundamentals:** Understanding the difference between a base model (next-token predictor) and an instruction-tuned model.
- **Matrix Multiplication:** Basic intuition that linear layers in neural networks are massive matrix multiplications.

## 2. Learning Objectives
- Differentiate between Prompting, RAG, and Fine-Tuning, and know when to use each.
- Understand the mechanics and cost of Full Fine-Tuning.
- Master the theory and math behind LoRA (Low-Rank Adaptation).
- Understand Quantization and how QLoRA enables fine-tuning massive models on consumer hardware.
- Learn the end-to-end dataset creation and fine-tuning workflow.
- Identify failure modes like Overfitting and Catastrophic Forgetting.

## 3. Why This Topic Exists
While Prompt Engineering and RAG are powerful, they have limits. 
- Prompting takes up valuable context window space and increases per-token costs. 
- RAG provides facts, but doesn't change the model's fundamental *behavior, tone, or ability to perform complex, highly-formatted tasks*.

When you need an LLM to consistently output SQL queries in a highly specific proprietary dialect, or answer medical questions in the exact tone of a specific doctor, you need to change the model's actual "brain" (its neural network weights). This is **Fine-Tuning**.

## 4. The Decision Matrix: Prompting vs. RAG vs. Fine-Tuning

Before fine-tuning, you must justify it.

| Requirement | Prompting (Few-Shot) | RAG | Fine-Tuning |
| :--- | :--- | :--- | :--- |
| **New Factual Knowledge** | Poor (Context limits) | **Excellent** | Poor (Models struggle to memorize facts via weights) |
| **Specific Tone/Format** | Good (If simple) | Poor | **Excellent** (Becomes native to the model) |
| **New Skills / Syntax** | Moderate | Poor | **Excellent** |
| **Cost to Build** | Low | Medium | High (Requires curated data & compute) |
| **Inference Cost** | High (Long prompts) | High | **Low** (Short prompts, behavior is baked in) |

**Rule of Thumb:** Use RAG for *Knowledge*. Use Fine-Tuning for *Behavior, Tone, and Skills*.

## 5. Full Fine-Tuning: The Traditional Approach

In full fine-tuning, you take a pre-trained model and continue training it using backpropagation on your specific dataset.
- **Mechanics:** Every single weight in the network is unfrozen and updated.
- **The Problem:** A 70 Billion parameter model in 16-bit precision takes 140GB of VRAM just to store the weights. During training, you also need to store gradients, optimizer states (like Adam moments), and activations. Training a 70B model fully requires over 1000GB of VRAM (e.g., a cluster of 16x 80GB A100 GPUs). This is financially impossible for most developers.

## 6. PEFT: Parameter-Efficient Fine-Tuning

PEFT methods aim to fine-tune large models while only updating a tiny fraction (often <1%) of the weights.

### LoRA (Low-Rank Adaptation)
LoRA is the breakthrough that democratized fine-tuning.

**The Intuition:** 
A neural network's dense layers are massive weight matrices (let's call one $W$). When fine-tuning, the *updates* to this matrix (let's call the update $\Delta W$) have a low "intrinsic rank". This means the *changes* required to learn a new task don't require the full massive matrix; they can be represented by a much smaller amount of information.

**The Math:**
Instead of updating a $10,000 \times 10,000$ matrix $W$ (100 million parameters), LoRA:
1. **Freezes** the original matrix $W$.
2. Injects two small matrices $A$ and $B$ next to it.
   - $A$ is dimension $(10,000 \times r)$
   - $B$ is dimension $(r \times 10,000)$
   - $r$ is the "rank" (a small number like 8).
3. The number of parameters in $A$ and $B$ combined is $(10,000 \times 8) + (8 \times 10,000) = 160,000$.
4. **Result:** We went from training 100,000,000 parameters to 160,000 (a 99.8% reduction!).

**During Inference:**
$W_{new} = W + (A \times B)$
Because matrix multiplication is associative, we can multiply A and B, add the result to W, and serve the model with **zero added latency**. The resulting LoRA "Adapter" is a tiny file (e.g., 50MB) that you can swap out at runtime.

### Quantization and QLoRA
**Quantization** is the process of compressing weights. Normally, a weight is a 16-bit float (FP16). Quantization maps this down to an 8-bit or 4-bit integer.
- A 7B parameter model in 16-bit takes 14GB VRAM.
- In 4-bit, it takes 3.5GB VRAM.

**QLoRA (Quantized LoRA)** combines both breakthroughs:
1. Load the massive base model $W$ in 4-bit precision (Frozen).
2. Attach 16-bit LoRA adapters ($A$ and $B$) (Trainable).
3. Backpropagate errors through the 4-bit weights to update the 16-bit adapters.
**Result:** You can fine-tune a 70B parameter model on a single 48GB consumer GPU (like an RTX 6000).

## 7. The End-to-End Fine-Tuning Workflow

1. **Data Collection:** Gather examples of perfect inputs and outputs.
2. **Formatting:** Format the data into the exact prompt template the model expects (e.g., ChatML, Alpaca format).
   ```json
   {"messages": [{"role": "user", "content": "Write SQL to find top users."}, {"role": "assistant", "content": "SELECT * FROM users ORDER BY score DESC LIMIT 10;"}]}
   ```
3. **Training:** Run QLoRA. Monitor the Training Loss and Validation Loss.
4. **Evaluation:** Run the base model vs. the fine-tuned model side-by-side (A/B testing) using an LLM-as-a-judge or human evaluators.
5. **Merging:** (Optional) Merge the 50MB LoRA adapter back into the base weights for production deployment.

## 8. Failure Modes

### Overfitting
If you train for too many epochs, the model memorizes your exact training dataset and loses its general intelligence.
*Symptom:* Validation loss starts increasing while training loss decreases.
*Fix:* Use early stopping, higher dropout, or lower learning rates.

### Catastrophic Forgetting
When a model learns a new skill, it overwrites the weights used for its old skills. If you fine-tune an LLM purely on medical data, it might "forget" how to write Python code or speak Spanish.
*Fix:* **Data Blending**. Mix 10% general instruction data (like the Alpaca dataset) into your medical dataset to keep the old circuits alive during training.

## 9. Active Recall
1. Why does full fine-tuning require so much more memory than just doing inference?
2. How does LoRA drastically reduce trainable parameters?
3. What does "Rank" mean in the context of LoRA?
4. If an LLM needs to know the live inventory of your warehouse, should you use RAG or Fine-tuning?

## 10. Interview Questions
**Q: Explain how QLoRA allows backpropagation through 4-bit weights.**
*Answer:* In QLoRA, the forward pass uses the 4-bit weights. During the backward pass, the 4-bit weights are "de-quantized" on the fly back to 16-bit (computationally) so the gradient can pass through them down to the 16-bit LoRA adapters. The base weights themselves are never updated.

**Q: You fine-tuned a model to output JSON. It outputs perfect JSON on the training set, but garbage on new prompts. What happened and how do you fix it?**
*Answer:* The model overfit to the training set. To fix it, I would ensure a proper train/validation split, implement early stopping by monitoring validation loss, increase the diversity of the training data, and possibly lower the LoRA rank ($r$) or increase weight decay/dropout to reduce the model's capacity to memorize.
