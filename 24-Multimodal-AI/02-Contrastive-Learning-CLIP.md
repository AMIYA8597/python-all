# 02 - Contrastive Learning & CLIP

## Prerequisites
- Multimodal Fundamentals
- Vision Transformers (ViT)
- Text Transformers (BERT / GPT architectures)

## Objectives
- Understand the principles of Contrastive Learning.
- Dive deep into the architecture and training objective of CLIP (Contrastive Language-Image Pre-training).
- Learn how to use CLIP for zero-shot image classification and cross-modal retrieval.

## Intuition
Historically, vision models were trained to predict a fixed set of predefined categories (e.g., ImageNet's 1000 classes). This is limiting. What if we could train a model to understand images using open-vocabulary natural language? CLIP does exactly this by aligning images and their textual descriptions in a shared latent space using contrastive learning.

## Contrastive Learning Mathematics
Contrastive learning aims to bring positive pairs (e.g., an image and its correct caption) closer together in the embedding space while pushing negative pairs (e.g., an image and a mismatched caption) apart.

Let $I_i$ be an image embedding and $T_i$ be its corresponding text embedding in a batch of size $N$.
The cosine similarity is: $sim(I_i, T_j) = \frac{I_i \cdot T_j}{||I_i|| ||T_j||}$

CLIP uses a symmetric cross-entropy loss over the similarity matrix. For the $i$-th image, the loss to find the correct text is:
$L_i^{(image \to text)} = - \log \frac{\exp(sim(I_i, T_i) / \tau)}{\sum_{j=1}^N \exp(sim(I_i, T_j) / \tau)}$
Where $\tau$ is a learnable temperature parameter.

The total loss is the average of image-to-text and text-to-image losses.

## CLIP Architecture
CLIP consists of two separate encoders:
1. **Image Encoder**: ResNet or Vision Transformer (ViT).
2. **Text Encoder**: A Transformer-based text model.

Both encoders project their inputs into a shared embedding space of dimension $d$. A dot product between the image embedding and text embedding gives the similarity score.

## Code Example: Zero-Shot Classification with CLIP (Hugging Face)

```python
from PIL import Image
import requests
from transformers import CLIPProcessor, CLIPModel

# Load model and processor
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

# Get an image
url = "http://images.cocodataset.org/val2017/000000039769.jpg"
image = Image.open(requests.get(url, stream=True).raw)

# Define classes for zero-shot classification
candidate_labels = ["a photo of a cat", "a photo of a dog", "a photo of a bird"]

# Preprocess and forward pass
inputs = processor(text=candidate_labels, images=image, return_tensors="pt", padding=True)
outputs = model(**inputs)

# Logits per image are the similarities
logits_per_image = outputs.logits_per_image 
probs = logits_per_image.softmax(dim=1)

for label, prob in zip(candidate_labels, probs[0]):
    print(f"{label}: {prob.item():.4f}")
```

## Interview Questions
1. **Q: How does CLIP achieve zero-shot classification?**
   **A**: CLIP represents classes as text descriptions (e.g., "a photo of a dog"). It embeds both the query image and all text descriptions into the same space. The model predicts the class by finding the text embedding that has the highest cosine similarity with the image embedding.
2. **Q: Why does CLIP use a large batch size during training?**
   **A**: Contrastive learning relies on in-batch negatives. A larger batch size provides more negative examples per positive pair, making the task harder and forcing the model to learn more discriminative and robust features.
