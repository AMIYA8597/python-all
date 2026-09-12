# Fine-Tuning and Parameter-Efficient Fine-Tuning (PEFT)

While prompting and RAG are great, sometimes an LLM needs to deeply learn a new style, specific domain vocabulary, or complex task formatting. This requires updating the model's neural network weights, a process known as **Fine-Tuning**.

## 1. Full Fine-Tuning
In full fine-tuning, you take a pre-trained model and continue training it on your specific dataset. 
- **Pros:** Maximum adaptation to the new data.
- **Cons:** Extremely expensive. If the model has 70 Billion parameters, you need to load all 70B parameters, their gradients, and optimizer states into GPU memory. This requires massive compute clusters.

## 2. Instruction Fine-Tuning
A specific type of fine-tuning where the model is trained on pairs of `(Instruction, Output)` to teach it to follow commands (e.g., turning a base next-token predictor like LLaMA into an assistant like ChatGPT).

## 3. PEFT (Parameter-Efficient Fine-Tuning)
PEFT methods aim to fine-tune large models while only updating a very small fraction of the weights. This drastically reduces GPU memory requirements, allowing you to fine-tune massive models on a single consumer GPU.

### LoRA (Low-Rank Adaptation)
LoRA is the most popular PEFT technique.
Instead of updating the massive weight matrix $W$ directly (where $W$ might be 10,000 x 10,000), LoRA freezes the original matrix and injects two smaller, train-able "low-rank" matrices, $A$ and $B$.
- Matrix $A$ is dimensions $(10,000 \times r)$
- Matrix $B$ is dimensions $(r \times 10,000)$
Where $r$ is the "rank" (a small number like 8 or 16).

During training, $W$ is frozen. Only $A$ and $B$ are updated. 
During inference, you simply calculate $W_{new} = W + (A \times B)$. The modified weights are used as usual with no added latency!
- **Benefits:** Reduces trainable parameters by up to 99.9%. The final LoRA adapter is a tiny file (e.g., 50MB) that can be swapped in and out easily.

### QLoRA (Quantized LoRA)
Takes LoRA a step further by quantizing (compressing) the base model $W$ down to 4-bit precision, while keeping the $A$ and $B$ adapters in 16-bit precision. This allows a 70B parameter model to be fine-tuned on a single 48GB GPU.
