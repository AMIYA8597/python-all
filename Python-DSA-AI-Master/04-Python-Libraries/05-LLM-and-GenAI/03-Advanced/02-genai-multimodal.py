"""
Module: 02-genai-multimodal
Description: A comprehensive, textbook-grade interactive lesson on Multimodal Generative AI using Python.

===========================================================================
📚 TEXTBOOK: MULTIMODAL GENERATIVE ARTIFICIAL INTELLIGENCE
===========================================================================

1. INTRODUCTION TO MULTIMODAL GENAI
------------------------------------
Traditional Natural Language Processing (NLP) models are "unimodal," meaning they
process and generate only one type of data (usually text). Computer Vision models
process only images or video. Multimodal Generative AI (GenAI) breaks these 
silos by processing, understanding, and generating multiple modalities (text, 
image, audio, video, 3D, and structured data) simultaneously.

Why is this a breakthrough?
Human perception is inherently multimodal. We don't just read; we see, hear, 
and touch. To build AGI (Artificial General Intelligence) or highly capable 
AI assistants, models must reason across different data types. 

Examples of Multimodal GenAI:
- OpenAI's GPT-4o, GPT-4V (Text + Image in, Text out)
- Google's Gemini (Native Multimodal: Text, Image, Audio, Video)
- Anthropic's Claude 3 (Vision + Text)
- Midjourney / DALL-E 3 (Text in, Image out)
- Meta's ImageBind (Aligns text, image, audio, depth, thermal, and IMU data)

2. CORE ARCHITECTURES & MATHEMATICAL BACKGROUND
-----------------------------------------------
How do we make text and images "talk" to each other?
The cornerstone of multimodal AI is creating a "shared representation space" 
where different modalities can be mapped to the same mathematical vectors.

A foundational architecture is CLIP (Contrastive Language-Image Pre-training) by OpenAI.

### CLIP Mathematics (Contrastive Learning)
Let `I` be an image and `T` be a corresponding text description.
We have an Image Encoder `E_I` and a Text Encoder `E_T`.
The encodings are:
v_I = E_I(I)  (Image vector)
v_T = E_T(T)  (Text vector)

We compute the cosine similarity between the two vectors:
similarity = (v_I · v_T) / (||v_I|| * ||v_T||)

During training with a batch of N (Image, Text) pairs, we want to maximize the 
cosine similarity of the N correct pairs (the diagonal of an N x N matrix) and 
minimize the similarity of the N*(N-1) incorrect pairs.
This loss is called InfoNCE (Noise Contrastive Estimation).

### LLaVA (Large Language and Vision Assistant)
LLaVA connects a Vision Encoder (like ViT from CLIP) to a Large Language Model (like LLaMA).
1. Image -> ViT -> Visual Tokens.
2. A linear projection layer maps visual tokens to the LLM's word embedding space.
3. The LLM processes [Visual Tokens] + [Text Prompt Tokens] to generate a Text response.

3. BIG-O COMPLEXITY OF MULTIMODAL INFERENCE
-------------------------------------------
Let `N` be the sequence length (number of text tokens + image patches).
Let `d` be the hidden dimension size of the Transformer model.

- Time Complexity (Self-Attention): O(N^2 * d)
  Because every token must attend to every other token (both text and image patches).
  High-res images produce MANY patches, making O(N^2) a massive bottleneck.
- Space Complexity (KV Cache during generation): O(N * d * L)
  Where L is the number of transformer layers.
  Storing the KV cache for thousands of image tokens takes gigabytes of VRAM.

4. LEARNING OBJECTIVES IN THIS MODULE
-------------------------------------
1. Understand and simulate shared embedding spaces (CLIP-style).
2. Implement basic multimodal inference using Mock APIs (representing GPT-4V/Gemini).
3. Build a complex processing pipeline for a "Multimodal RAG" (Retrieval-Augmented Generation).
4. Analyze performance bottlenecks in Multimodal AI.
5. Solve an interview challenge involving cross-modal alignment.
===========================================================================
"""

import sys
import time
import math
import random
import json
import base64
from typing import List, Dict, Any, Optional, Tuple, Union
from dataclasses import dataclass

# Attempt to import libraries commonly used in Multimodal AI
try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False
    print("WARNING: numpy is not installed. Some mathematical simulations will use pure Python fallbacks.")


# =========================================================================
# UTILITIES & MOCKS
# =========================================================================

def cosine_similarity_pure_python(v1: List[float], v2: List[float]) -> float:
    """
    Compute cosine similarity between two vectors without NumPy.
    
    Time Complexity: O(d) where d is the dimension of the vectors.
    Space Complexity: O(1) auxiliary space.
    """
    if len(v1) != len(v2):
        raise ValueError("Vectors must have the same length.")
    
    dot_product = sum(x * y for x, y in zip(v1, v2))
    norm_v1 = math.sqrt(sum(x * x for x in v1))
    norm_v2 = math.sqrt(sum(y * y for y in v2))
    
    if norm_v1 == 0 or norm_v2 == 0:
        return 0.0
    
    return dot_product / (norm_v1 * norm_v2)


@dataclass
class MultimodalInput:
    """
    Represents an input containing multiple modalities.
    """
    text: Optional[str] = None
    image_base64: Optional[str] = None
    audio_path: Optional[str] = None
    
    def summary(self) -> str:
        parts = []
        if self.text: parts.append(f"Text({len(self.text)} chars)")
        if self.image_base64: parts.append("Image(Base64)")
        if self.audio_path: parts.append(f"Audio({self.audio_path})")
        return " + ".join(parts) if parts else "Empty Input"


# =========================================================================
# 1. BASIC IMPLEMENTATION: SHARED EMBEDDING SPACE (MOCK CLIP)
# =========================================================================

class MockCLIPModel:
    """
    A simulated CLIP model that generates vectors for texts and images.
    In a real scenario, this would load 'openai/clip-vit-base-patch32' via Hugging Face.
    """
    
    def __init__(self, embedding_dim: int = 512):
        self.embedding_dim = embedding_dim
        # A mock semantic map to force some vectors to be similar
        self.semantic_map = {
            "cat": [0.9, 0.1, 0.0],
            "dog": [0.8, 0.2, 0.0],
            "car": [0.0, 0.9, 0.1],
            "beach": [0.1, 0.1, 0.9]
        }
        print(f"[MockCLIPModel] Initialized with embedding dimension {self.embedding_dim}.")

    def _generate_mock_vector(self, keyword: str) -> List[float]:
        """Generates a reproducible, normalized pseudo-random vector influenced by the keyword."""
        # Check if keyword matches our semantic map roughly
        base = [random.uniform(0, 1) for _ in range(self.embedding_dim)]
        
        for k, weight_pattern in self.semantic_map.items():
            if k in keyword.lower():
                # Strongly bias the vector towards a specific sub-space
                for i in range(self.embedding_dim):
                    section = i // (self.embedding_dim // 3)
                    if section < 3:
                        base[i] += weight_pattern[section] * 5.0
                break
                
        # Normalize
        norm = math.sqrt(sum(x*x for x in base))
        return [x / norm for x in base]

    def encode_text(self, text: str) -> List[float]:
        """Encodes text into the shared multimodal space."""
        # In reality: text -> Tokenizer -> Transformer -> Projection -> L2 Norm -> Vector
        return self._generate_mock_vector(text)

    def encode_image(self, image_description: str) -> List[float]:
        """
        Encodes image into the shared multimodal space.
        (We pass a description to mock the image content visually).
        """
        # In reality: image -> ResNet/ViT -> Projection -> L2 Norm -> Vector
        return self._generate_mock_vector(image_description)


def basic_implementation() -> None:
    """
    Demonstrates the fundamental concept of Multimodal AI:
    Mapping Text and Image to a shared embedding space for Zero-Shot classification.
    """
    print("\n" + "="*50)
    print("1. BASIC MULTIMODAL GENAI: SHARED EMBEDDING SPACE")
    print("="*50)
    
    # Initialize the model
    clip = MockCLIPModel(embedding_dim=256)
    
    # 1. We have an image (mocked as its semantic content)
    target_image_content = "A cute ginger cat sitting on a couch"
    print(f"Target Image Content: '{target_image_content}'")
    
    image_emb = clip.encode_image(target_image_content)
    
    # 2. We want to classify it among these labels
    candidate_labels = [
        "A photo of a cat",
        "A photo of a dog",
        "A photo of a fast car",
        "A beautiful sunny beach"
    ]
    
    print("\nPerforming Zero-Shot Image Classification (Text-to-Image matching):")
    best_label = ""
    best_score = -1.0
    
    for label in candidate_labels:
        text_emb = clip.encode_text(label)
        
        # Calculate cosine similarity
        score = cosine_similarity_pure_python(image_emb, text_emb)
        print(f" - Similarity with '{label}': {score:.4f}")
        
        if score > best_score:
            best_score = score
            best_label = label
            
    print(f"\n[Result] The model predicts the image is: '{best_label}'")
    print("Basic implementation completed successfully.")


# =========================================================================
# 2. INTERMEDIATE IMPLEMENTATION: MULTIMODAL INFERENCE PIPELINE
# =========================================================================

class MockMultimodalLLM:
    """
    Simulates a Large Multimodal Model (LMM) like GPT-4V or Gemini Pro Vision.
    """
    def __init__(self, model_name: str = "gpt-4-vision-mock"):
        self.model_name = model_name
        self.token_cost = 0.00001
        
    def generate_content(self, inputs: List[MultimodalInput], max_tokens: int = 100) -> str:
        """
        Takes a list of MultimodalInputs and generates a text response.
        """
        print(f"\n[{self.model_name}] Processing prompt with {len(inputs)} elements...")
        
        has_image = any(inp.image_base64 for inp in inputs)
        has_audio = any(inp.audio_path for inp in inputs)
        texts = [inp.text for inp in inputs if inp.text]
        
        combined_text = " ".join(texts).lower()
        
        # Simulated reasoning engine
        time.sleep(0.5) # simulate latency
        
        response = ""
        if has_image and "describe" in combined_text:
            response = "I can see the image provided. It appears to contain detailed visual elements matching your query. The colors are vibrant and the subject is in focus."
        elif has_image and "extract" in combined_text:
            response = '{"extracted_data": "Mock data extracted from image"}'
        elif has_audio:
            response = "Based on the audio transcript, the speaker is expressing a positive sentiment about the topic."
        else:
            response = "This is a generic response to your text-only query."
            
        print(f"[{self.model_name}] Generation complete.")
        return response


def intermediate_implementation() -> None:
    """
    Demonstrates sending mixed modalities to a unified generative model.
    """
    print("\n" + "="*50)
    print("2. INTERMEDIATE: MULTIMODAL LLM INFERENCE")
    print("="*50)
    
    llm = MockMultimodalLLM(model_name="gemini-1.5-pro-mock")
    
    # Scenario 1: Visual Question Answering (VQA)
    print("\n--- Scenario 1: Visual Question Answering ---")
    vqa_inputs = [
        MultimodalInput(text="Please describe this image in detail and identify any animals."),
        MultimodalInput(image_base64="/9j/4AAQSkZJRgABAQEAAAAAA... (Mocked Base64)")
    ]
    
    response = llm.generate_content(vqa_inputs)
    print(f"Assistant: {response}")
    
    # Scenario 2: Multimodal Context (Audio + Text)
    print("\n--- Scenario 2: Audio Summarization ---")
    audio_inputs = [
        MultimodalInput(text="Summarize the attached meeting recording."),
        MultimodalInput(audio_path="s3://meeting_recordings/q3_review.mp3")
    ]
    
    response = llm.generate_content(audio_inputs)
    print(f"Assistant: {response}")


# =========================================================================
# 3. ADVANCED IMPLEMENTATION: MULTIMODAL RAG (Retrieval-Augmented Gen)
# =========================================================================

class VectorDatabase:
    """
    A simple in-memory vector database for storing and retrieving multimodal embeddings.
    """
    def __init__(self):
        self.embeddings: List[List[float]] = []
        self.metadata: List[Dict[str, Any]] = []
        
    def add(self, vector: List[float], meta: Dict[str, Any]) -> None:
        self.embeddings.append(vector)
        self.metadata.append(meta)
        
    def search(self, query_vector: List[float], top_k: int = 2) -> List[Tuple[float, Dict[str, Any]]]:
        """
        O(N * d) linear scan search where N is number of docs and d is vector dim.
        In production, use HNSW (Hierarchical Navigable Small World) for O(log N) search.
        """
        results = []
        for i, emb in enumerate(self.embeddings):
            score = cosine_similarity_pure_python(query_vector, emb)
            results.append((score, self.metadata[i]))
            
        # Sort descending by score
        results.sort(key=lambda x: x[0], reverse=True)
        return results[:top_k]

def advanced_implementation() -> None:
    """
    Builds a Multimodal RAG pipeline.
    Concept:
    1. We have a database of images (e.g., a product catalog).
    2. We embed all images using a vision encoder into a Vector DB.
    3. User queries with text (e.g., "I want a red sports car").
    4. We embed the text, search the Vector DB, find top images.
    5. We pass the retrieved images + user query to a Multimodal LLM to generate a personalized sales pitch.
    """
    print("\n" + "="*50)
    print("3. ADVANCED: MULTIMODAL RAG (Retrieval-Augmented Generation)")
    print("="*50)
    
    embedder = MockCLIPModel(embedding_dim=256)
    vdb = VectorDatabase()
    llm = MockMultimodalLLM(model_name="gpt-4o-mock")
    
    # Step 1 & 2: Ingesting the Multimodal Knowledge Base
    print("[Advanced] Ingesting product catalog into Vector Database...")
    catalog = [
        {"id": 101, "desc": "A fast red sports car", "type": "image"},
        {"id": 102, "desc": "A slow blue minivan", "type": "image"},
        {"id": 103, "desc": "A cute fluffy cat toy", "type": "image"},
        {"id": 104, "desc": "A high-end gaming laptop", "type": "image"}
    ]
    
    for item in catalog:
        # We embed the "image". We use the desc string as a proxy for the image pixels.
        vec = embedder.encode_image(item["desc"])
        vdb.add(vec, item)
        print(f"  - Indexed Document {item['id']}: {item['desc']}")
        
    # Step 3: User Query
    user_query = "I'm looking for a fast vehicle, preferably red. What do you recommend?"
    print(f"\n[Advanced] User Query: '{user_query}'")
    
    # Step 4: Retrieval
    print("[Advanced] Retrieving relevant modalities based on text query...")
    query_vec = embedder.encode_text(user_query)
    top_results = vdb.search(query_vec, top_k=1)
    
    best_score, best_meta = top_results[0]
    print(f"[Advanced] Retrieved Product ID {best_meta['id']} (Score: {best_score:.4f})")
    
    # Step 5: Augmented Generation
    print("[Advanced] Synthesizing final response with Multimodal LLM...")
    
    prompt_text = (
        f"The user asked: '{user_query}'. "
        f"We retrieved this item from the database. "
        f"Write a persuasive response."
    )
    
    # Constructing the multimodal prompt (Text + Retrieved Image)
    # Here we mock the image bytes with its description for the mock LLM to understand.
    prompt = [
        MultimodalInput(text=prompt_text),
        MultimodalInput(image_base64=f"<Base64 of image {best_meta['id']}: {best_meta['desc']}>")
    ]
    
    final_response = llm.generate_content(prompt)
    print(f"\nFinal AI Agent Output:\n{final_response}")


# =========================================================================
# 4. PERFORMANCE ANALYSIS & EDGE CASES
# =========================================================================

def analyze_performance_and_edge_cases() -> None:
    """
    Discusses Big-O, Token Economics, and robustness in Multimodal AI.
    """
    print("\n" + "="*50)
    print("4. PERFORMANCE ANALYSIS & EDGE CASES")
    print("="*50)
    
    print("""
PERFORMANCE BOTTLENECKS:
1. Token Explosion: Images are token-heavy.
   - A standard text query might be 50 tokens.
   - An image passed to GPT-4V might be split into 512x512 tiles, generating 
     upwards of 1,000 to 2,000 visual tokens per image.
   - Since Self-Attention is O(N^2), adding one image severely increases compute and memory usage.

2. KV Cache Exhaustion:
   - In deployment, LLMs cache Keys and Values (O(N) memory per sequence) to speed up decoding.
   - Multimodal inputs flood the KV cache. Processing 10 images in a single prompt 
     can easily OOM (Out Of Memory) a standard GPU server.

EDGE CASES:
1. Hallucination across modalities:
   - The model might accurately read text but fail to align it with the image 
     (e.g., describing a red car as blue because 'blue' was prominent in the text prompt).
2. Resolution mismatch:
   - Small text in an image might be unreadable if the Vision Encoder (ViT) downsizes 
     the image before patching.
3. Multimodal Jailbreaks:
   - Users can hide malicious text prompts inside images (steganography) to bypass 
     the LLM's text-based safety filters.
    """)


# =========================================================================
# 5. INTERVIEW CHALLENGE
# =========================================================================

def interview_challenge(text_queries: List[str], image_descriptions: List[str]) -> Dict[str, str]:
    """
    Common Interview Challenge: Cross-Modal Matching Optimization.
    
    Problem Statement:
    You are given a list of N text queries and M image descriptions. 
    You have a CLIP model. Find the best matching image for EVERY text query.
    
    Naive approach: For every text, embed it, then loop through all M images, embed them, 
    and find the highest similarity. 
    Time Complexity: O(N * M * (T_embed_img + T_embed_txt + d))
    This is extremely slow because image embedding (T_embed_img) is computationally expensive.
    
    Optimized approach:
    1. Pre-compute and cache the embeddings for all M images: O(M * T_embed_img)
    2. Compute the embeddings for all N texts: O(N * T_embed_txt)
    3. Compute a similarity matrix (N x M): O(N * M * d)
    
    Overall Time Complexity: O(M*T_embed_img + N*T_embed_txt + N*M*d)
    
    Returns: A dictionary mapping {text_query: best_matching_image_description}
    """
    print("\n" + "="*50)
    print("5. INTERVIEW CHALLENGE: EFFICIENT CROSS-MODAL ALIGNMENT")
    print("="*50)
    
    clip = MockCLIPModel(embedding_dim=64) # Smaller dim for speed
    
    # 1. Pre-compute Image Embeddings (Vectorized / Cached)
    print("Pre-computing image embeddings...")
    image_embeddings = []
    for img in image_descriptions:
        image_embeddings.append(clip.encode_image(img))
        
    results = {}
    
    # 2. Iterate queries, embed text once, and calculate similarities
    print("Processing queries...")
    for text in text_queries:
        text_emb = clip.encode_text(text)
        
        best_score = -float('inf')
        best_image = None
        
        for idx, img_emb in enumerate(image_embeddings):
            # O(d) dot product
            score = cosine_similarity_pure_python(text_emb, img_emb)
            if score > best_score:
                best_score = score
                best_image = image_descriptions[idx]
                
        results[text] = best_image
        
    return results

def run_tests() -> None:
    """
    Test suite ensuring that our mocked mathematical properties hold up.
    """
    print("\n" + "="*50)
    print("6. RUNNING TESTS")
    print("="*50)
    
    try:
        # Test 1: Cosine Similarity properties
        v1 = [1.0, 0.0]
        v2 = [0.0, 1.0]
        v3 = [1.0, 0.0]
        v4 = [-1.0, 0.0]
        
        assert math.isclose(cosine_similarity_pure_python(v1, v2), 0.0, abs_tol=1e-9), "Orthogonal vectors should have 0 similarity."
        assert math.isclose(cosine_similarity_pure_python(v1, v3), 1.0, abs_tol=1e-9), "Identical vectors should have 1 similarity."
        assert math.isclose(cosine_similarity_pure_python(v1, v4), -1.0, abs_tol=1e-9), "Opposite vectors should have -1 similarity."
        
        # Test 2: Interview Challenge logic
        texts = ["I want a dog", "I want a car"]
        images = ["A happy dog playing", "A fast sports car", "A lazy cat"]
        
        mapping = interview_challenge(texts, images)
        print("\nChallenge Output mapping:")
        for t, i in mapping.items():
            print(f"  '{t}' -> '{i}'")
            
        # Due to our mock CLIP logic mapping "dog" to "dog" and "car" to "car", we expect:
        assert "dog" in mapping["I want a dog"].lower(), "Failed to map dog."
        assert "car" in mapping["I want a car"].lower(), "Failed to map car."
        
        print("\n[SUCCESS] All mathematical and functional tests passed!")
        
    except AssertionError as e:
        print(f"\n[ERROR] Test Failed: {e}")


if __name__ == "__main__":
    print(f"\n{'='*70}")
    print(f"🚀 EXPLORING PYTHON MULTIMODAL GENAI MASTERCLASS 🚀")
    print(f"{'='*70}\n")
    
    # Section 1
    basic_implementation()
    
    # Section 2
    intermediate_implementation()
    
    # Section 3
    advanced_implementation()
    
    # Section 4
    analyze_performance_and_edge_cases()
    
    # Section 5 & 6
    run_tests()
    
    print(f"\n{'='*70}")
    print(f"🏁 END OF LESSON 🏁")
    print(f"{'='*70}\n")
