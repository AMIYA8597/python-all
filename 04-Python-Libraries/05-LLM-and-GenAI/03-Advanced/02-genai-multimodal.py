"""
# ==============================================================================
# LABORATORY: MULTIMODAL GEN-AI (VISION & TEXT)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# The world is not just text. It is images, audio, and video.
# Standard LLMs (like GPT-3) were strictly unimodal. They could only read 
# and output text tokens.
#
# Multimodal AI shatters this barrier. 
# 1. CLIP (Contrastive Language-Image Pretraining): A breakthrough architecture 
#    by OpenAI that aligns Image Vectors and Text Vectors into the exact same 
#    mathematical space. This allows you to type "A photo of a dog" and 
#    mathematically search a database of raw JPEG images!
# 
# 2. VLMs (Vision-Language Models like LLaVA or GPT-4V): These models stitch a 
#    Vision Encoder (like CLIP) directly into the brain of a Large Language Model.
#    You can upload a photo of a broken bicycle, and the LLM can literally "see" 
#    it, reason about the broken chain, and output English instructions on how 
#    to fix it!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the architecture of CLIP (Joint Embedding Space).
# - Understand how VLMs process Image Patches into Tokens.
# - Conceptually build a Multimodal RAG system.
#
# ==============================================================================
"""

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. CLIP (CONTRASTIVE LANGUAGE-IMAGE PRETRAINING)
# ==============================================================================
def demonstrate_clip():
    section_header("CLIP: The Foundation of Multimodal AI")
    
    print("Before CLIP, Image classification was strict. You trained a ResNet50 ")
    print("model to output exactly 1,000 specific classes (Dog, Cat, Car).")
    print("If you uploaded a photo of a 'Space Shuttle', the model crashed because ")
    print("it was not in the 1,000 hardcoded classes.\n")
    
    print("--- How CLIP Works ---")
    print("OpenAI scraped 400 Million (Image, Text-Caption) pairs from the internet.")
    print("1. An Image Encoder processes the JPEG into a 512-Dimensional Vector.")
    print("2. A Text Encoder processes the Caption into a 512-Dimensional Vector.")
    print("3. The Loss Function violently forces the Image Vector and the Text ")
    print("   Vector to physically overlap in 512D space!")
    
    print("\n--- Zero-Shot Image Classification ---")
    print("Because the vectors share the same geometric universe, we can do magic.")
    print("Upload a photo of a Space Shuttle.")
    print("CLIP Image Encoder outputs: Vector [0.4, 0.9, -0.2]")
    
    print("\nProvide a list of dynamic text labels: ['A dog', 'A space shuttle', 'A car']")
    print("CLIP Text Encoder outputs:")
    print("  'A dog' -> Vector [0.1, -0.8, 0.5]")
    print("  'A space shuttle' -> Vector [0.4, 0.8, -0.1]")
    
    print("\nWe calculate Cosine Similarity between the Image Vector and the Text Vectors.")
    print("The 'Space Shuttle' text vector is geometrically identical to the Image vector!")
    print("We just classified an image without EVER training a classification head!")


# ==============================================================================
# 4. VISION-LANGUAGE MODELS (VLMs)
# ==============================================================================
def demonstrate_vlm():
    section_header("Vision-Language Models (LLaVA / GPT-4V)")
    
    print("How do we give a standard LLM (which only understands text tokens) ")
    print("eyesight? We cannot feed a 1080p JPEG directly into a Transformer.\n")
    
    print("--- The LLaVA Architecture ---")
    print("1. Take an HD Image (e.g., 336x336 pixels).")
    print("2. Chop the image into a grid of tiny 14x14 pixel 'Patches'.")
    print("3. Pass every single Patch through a Vision Encoder (like CLIP-ViT).")
    print("4. Each Patch is mathematically compressed into a single 1D Vector.")
    print("5. We now have a sequence of 576 Vectors (representing the image).")
    
    print("\nHere is the magic:")
    print("We use a small Linear Projection layer to mathematically transform ")
    print("those Vision Vectors so they perfectly mimic the mathematical shape ")
    print("of standard English Word Vectors!")
    
    print("\nNow, we just concatenate them!")
    print("LLM Input: [Vision_Token_1] [Vision_Token_2] ... [Vision_Token_576] 'What is in this photo?'")
    
    print("\nThe LLM's Self-Attention mechanism treats the Image Patches exactly ")
    print("like words in a sentence! It calculates the logical relationship ")
    print("between the user's question and the pixels, allowing it to write ")
    print("a highly complex, reasoning-based response.")


# ==============================================================================
# 5. MULTIMODAL RAG
# ==============================================================================
def demonstrate_multimodal_rag():
    section_header("Multimodal RAG (Retrieving Images via Text)")
    
    print("Standard RAG converts PDFs to text vectors. But what if the PDF ")
    print("contains a complex Engineering Diagram (Chart)? The text extractor ")
    print("will just read garbage numbers, destroying the context.\n")
    
    print("--- The Multimodal RAG Pipeline ---")
    print("1. You extract all the raw JPEGs/Charts from the PDF.")
    print("2. You pass them through the CLIP Image Encoder to get Image Vectors.")
    print("3. You save them in the Vector Database (Chroma/FAISS).")
    
    print("\nUser Query: 'Show me the diagram of the nuclear reactor core.'")
    
    print("\n4. You pass the user query through the CLIP Text Encoder to get a Text Vector.")
    print("5. You execute a Vector Search. Because CLIP aligns text and images, ")
    print("   the Text Vector will find the exact JPEG Vector of the reactor core!")
    
    print("\n6. You retrieve the physical JPEG file.")
    print("7. You feed BOTH the JPEG and the User Query into a Vision-Language ")
    print("   Model (like GPT-4V). The AI 'looks' at the retrieved diagram and ")
    print("   explains it to the user!")


def run_all_labs():
    demonstrate_clip()
    demonstrate_vlm()
    demonstrate_multimodal_rag()


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. What is the fundamental breakthrough of CLIP's "Contrastive" loss function?
   Answer: Previous models were trained predictively (given an image, output exactly one correct class ID). CLIP is trained *contrastively* on massive batches of pairs (e.g., a batch of 32,000 images and their 32,000 text captions). The loss function creates a $32k \times 32k$ matrix. It geometrically pulls the correct (Image, Text) pairs toward each other in vector space (maximizing the diagonal of the matrix), while simultaneously violently pushing the millions of incorrect pairings away from each other. This mathematically forces the Vision Encoder and the Text Encoder to build an identical, unified mapping of the universe.

2. In a Vision-Language Model (VLM), how does the LLM actually "read" the image?
   Answer: The LLM does not read pixels. The image is chopped into patches (e.g., $16 \times 16$ pixels). A Vision Transformer (ViT) processes those patches into dense numerical embeddings (vectors). A "Projection Layer" (often just a simple Linear matrix multiplication) translates those Vision Vectors into the exact mathematical dimensionality of the LLM's standard word embeddings. The LLM is tricked into thinking it is just reading a sequence of very weird, highly-dense "words". The Self-Attention mechanism simply processes the visual tokens alongside the text tokens, allowing it to reason across modalities.

3. Why is Multimodal RAG vastly superior to standard Text RAG for enterprise documents?
   Answer: Enterprise documents (Financial Reports, Engineering Manuals, Medical Records) are heavily visual. A standard PDF text extractor will completely mangle a complex financial bar chart, extracting a meaningless string of random numbers. Text RAG is blind to this data. Multimodal RAG captures the physical image of the chart, stores it using CLIP embeddings, and retrieves it visually. When passed to a VLM (like GPT-4o), the AI can visually trace the bars on the chart, read the legend, and calculate trends, unlocking 100% of the document's information.
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Multimodal GenAI Completed.")
