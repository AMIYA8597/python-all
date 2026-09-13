# 03 - Vision-Language Models (VLMs)

## Prerequisites
- Transformer Architectures
- Autoregressive Language Modeling (e.g., GPT)
- Contrastive Learning (CLIP)

## Objectives
- Understand how large language models (LLMs) are augmented with vision capabilities to become Vision-Language Models (VLMs).
- Study the mechanisms of cross-attention and projection layers for multimodal fusion.
- Explore state-of-the-art VLM architectures like LLaVA, Flamingo, and BLIP-2.

## Intuition
While CLIP can align images and text in a shared space, it cannot generate text. To build systems that can answer questions about images (VQA) or generate image captions, we need to bridge vision encoders with powerful generative LLMs. VLMs achieve this by treating image features as "soft prompts" or using cross-attention to condition text generation on visual inputs.

## Core Mechanisms for Vision-Language Fusion

### 1. Linear Projection (e.g., LLaVA)
The simplest way to connect a vision encoder (like CLIP's ViT) to an LLM.
- The vision encoder produces a sequence of patch embeddings: $V \in \mathbb{R}^{P \times D_{v}}$
- A simple linear layer or MLP projects these features into the LLM's word embedding space: $V' = V W \in \mathbb{R}^{P \times D_{txt}}$
- $V'$ is then concatenated with the word embeddings of the prompt and fed into the LLM.

### 2. Cross-Attention (e.g., Flamingo)
Instead of prepending visual tokens, the LLM uses cross-attention layers interwoven with self-attention layers.
- The LLM's hidden states act as Queries ($Q$).
- The visual features act as Keys ($K$) and Values ($V$).
- This allows the model to attend to relevant parts of the image at different depths of the network.

### 3. Q-Former (e.g., BLIP-2)
A Querying Transformer (Q-Former) uses a fixed number of learnable queries to extract the most relevant visual features from the frozen image encoder before passing them to the LLM, effectively reducing the sequence length and computational cost.

## Code Example: Image Captioning with BLIP (Hugging Face)

```python
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import requests

# Load BLIP
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

# Load image
img_url = 'https://storage.googleapis.com/sfr-vision-language-research/BLIP/demo.jpg' 
raw_image = Image.open(requests.get(img_url, stream=True).raw).convert('RGB')

# Unconditional image captioning
inputs = processor(raw_image, return_tensors="pt")
out = model.generate(**inputs)
print("Caption:", processor.decode(out[0], skip_special_tokens=True))

# Conditional image captioning (Visual Question Answering context)
text = "a photography of"
inputs = processor(raw_image, text, return_tensors="pt")
out = model.generate(**inputs)
print("Conditional Caption:", processor.decode(out[0], skip_special_tokens=True))
```

## Interview Questions
1. **Q: What is the purpose of the projection layer in LLaVA?**
   **A**: The projection layer bridges the dimensionality gap between the vision encoder's output and the LLM's input embedding space. It translates visual patch embeddings into "visual tokens" that the LLM can process just like text tokens.
2. **Q: Why do VLMs often keep the vision encoder and LLM frozen during initial training?**
   **A**: Training from scratch is extremely expensive and risks catastrophic forgetting. By freezing the pre-trained weights (e.g., CLIP and LLaMA) and only training the connector (like a linear layer or Q-Former), the model efficiently learns to align modalities while retaining its robust vision and language capabilities.
