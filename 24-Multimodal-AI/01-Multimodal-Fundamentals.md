# 01 - Multimodal Fundamentals

## Prerequisites
- Deep Learning Basics (Neural Networks, Backpropagation)
- Fundamentals of Convolutional Neural Networks (CNNs) for vision
- Fundamentals of Transformers for Natural Language Processing (NLP)

## Objectives
- Understand the definition and scope of Multimodal AI.
- Learn the core challenges of Multimodal AI: Representation, Translation, Alignment, Fusion, and Co-learning.
- Explore basic approaches to multimodal fusion (early, late, and hybrid fusion).

## Intuition
Human perception is inherently multimodal. We don't just see the world; we hear, touch, and smell it. Multimodal AI aims to replicate this by building systems that can process and relate information from multiple different modalities (e.g., text, images, audio, video) simultaneously.

## Core Challenges in Multimodal AI
1. **Representation**: How do we represent data from different modalities such that they can be easily compared or combined? (e.g., mapping text and images to a shared latent space).
2. **Translation/Mapping**: Translating data from one modality to another (e.g., Image Captioning - translating image to text).
3. **Alignment**: Identifying the direct relations between sub-elements from two or more modalities (e.g., aligning a spoken word in an audio track with the corresponding frame in a video).
4. **Fusion**: Joining information from two or more modalities to perform a prediction task (e.g., using both audio and video for emotion recognition).
5. **Co-learning**: Transferring knowledge between modalities, especially useful when one modality has limited resources.

## Architecture & Fusion Strategies
### 1. Early Fusion (Data-level or Feature-level)
Combines features immediately after they are extracted.
- **Math**: $h = f( [x_{audio}, x_{video}] )$
- **Pros**: Can learn cross-modal interactions at the lowest level.
- **Cons**: High dimensionality, hard to align features of different frequencies/types.

### 2. Late Fusion (Decision-level)
Each modality is processed independently to make a prediction, and the final predictions are aggregated (e.g., voting, averaging).
- **Math**: $p_{audio} = f_{audio}(x_{audio})$, $p_{video} = f_{video}(x_{video})$, Final Prediction = $Agg(p_{audio}, p_{video})$
- **Pros**: Easy to implement, robust to missing modalities at inference time.
- **Cons**: Ignores low-level interactions between modalities.

### 3. Intermediate/Hybrid Fusion
Fuses features at multiple levels of a deep neural network, often using cross-attention mechanisms in Transformers.

## Code Example: Simple Late Fusion (PyTorch)

```python
import torch
import torch.nn as nn

class LateFusionModel(nn.Module):
    def __init__(self, num_classes):
        super().__init__()
        # Text branch
        self.text_model = nn.Sequential(
            nn.Linear(768, 256),
            nn.ReLU(),
            nn.Linear(256, num_classes)
        )
        # Image branch
        self.image_model = nn.Sequential(
            nn.Linear(2048, 256),
            nn.ReLU(),
            nn.Linear(256, num_classes)
        )

    def forward(self, text_features, image_features):
        # Independent predictions
        pred_text = self.text_model(text_features)
        pred_image = self.image_model(image_features)
        
        # Late fusion (Averaging)
        fused_pred = (pred_text + pred_image) / 2.0
        return fused_pred

# Dummy data
text_feats = torch.randn(16, 768)
image_feats = torch.randn(16, 2048)
model = LateFusionModel(num_classes=10)
outputs = model(text_feats, image_feats)
print("Fused Output Shape:", outputs.shape)
```

## Interview Questions
1. **Q: What is the difference between early fusion and late fusion?**
   **A**: Early fusion combines features at the input or low-level feature extraction stage, allowing the model to learn cross-modal interactions early. Late fusion combines the final decisions or predictions of separate modality-specific models, which is easier to train but might miss complex low-level interactions.
2. **Q: Explain the "alignment" challenge in Multimodal AI.**
   **A**: Alignment refers to finding correspondences between sub-components of different modalities, such as aligning a bounding box in an image with a specific noun phrase in a sentence, or aligning audio utterances with video frames.
