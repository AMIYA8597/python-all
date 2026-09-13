"""
# ==============================================================================
# LABORATORY: SENTIMENT ANALYSIS & TEXT VECTORIZATION
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You work for a massive e-commerce company. You receive 10,000 product reviews 
# every single hour. Your CEO wants a live dashboard showing if customers are 
# happy or angry.
#
# You cannot read them manually. You must use Sentiment Analysis.
#
# 1. Rules-Based Sentiment (VADER): Extremely fast, zero training required. 
#    Uses a massive pre-programmed dictionary where "excellent" is +3.0 and 
#    "terrible" is -3.0. It perfectly handles emojis and punctuation!
#
# 2. Machine Learning Sentiment (TF-IDF + Random Forest): What if the rules 
#    fail on domain-specific sarcasm? You must mathematically convert the 
#    English text into a Vector Matrix (TF-IDF) and train a real Machine Learning 
#    algorithm (like Naive Bayes or Random Forest) to classify the text based 
#    on your proprietary training data.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Execute VADER for zero-shot social media sentiment analysis.
# - Understand TF-IDF (Term Frequency - Inverse Document Frequency).
# - Execute a full NLP Machine Learning Pipeline using Scikit-Learn.
#
# ==============================================================================
"""

import numpy as np

# In a real environment: pip install nltk scikit-learn
try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.naive_bayes import MultinomialNB
    from sklearn.pipeline import Pipeline
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. VADER SENTIMENT (RULES-BASED)
# ==============================================================================
def demonstrate_vader():
    section_header("Rules-Based Sentiment Analysis (VADER)")
    
    print("VADER (Valence Aware Dictionary and sEntiment Reasoner) is explicitly ")
    print("engineered for Social Media text. It does not require a GPU or any ")
    print("training. It just works out of the box!\n")
    
    print("Consider the sentence: 'The food was okay, but the service was TERRIBLE!!! 😡'")
    
    print("\nVADER is smart enough to understand:")
    print("1. 'okay' is slightly positive.")
    print("2. 'but' causes a mathematical polarity shift, weighing the second half heavily.")
    print("3. 'TERRIBLE' in ALL CAPS multiplies the negative mathematical weight.")
    print("4. '!!!' punctuation multiplies the weight again.")
    print("5. '😡' emoji adds massive negative polarity.")
    
    print("\nVADER Outputs a Compound Score between -1.0 (Extreme Negative) ")
    print("and +1.0 (Extreme Positive).")
    
    print("\nFor the sentence above, VADER would output roughly: -0.85 (Very Negative).")
    print("This runs in microseconds, allowing you to process 10,000 tweets per second.")


# ==============================================================================
# 4. TF-IDF VECTORIZATION
# ==============================================================================
def demonstrate_tfidf():
    section_header("TF-IDF (Converting Text to Math)")
    
    if not HAS_SKLEARN:
        print("[WARNING] Scikit-Learn not installed.")
        return
        
    print("Standard ML algorithms (like Random Forest) cannot read English.")
    print("We must convert sentences into mathematical arrays. We use TF-IDF:")
    print("Term Frequency (TF): How often does a word appear in THIS document?")
    print("Inverse Document Frequency (IDF): How RARE is this word across ALL documents?\n")
    
    corpus = [
        "This product is amazing and I love it.",
        "Terrible product, completely broken.",
        "The delivery was fast but the product is broken."
    ]
    
    # 1. Initialize the Vectorizer
    # stop_words='english' automatically deletes 'is', 'and', 'the', etc.
    vectorizer = TfidfVectorizer(stop_words='english')
    
    # 2. Fit and Transform the Corpus
    tfidf_matrix = vectorizer.fit_transform(corpus)
    
    print("Vocabulary Learned by the Vectorizer:")
    print(vectorizer.get_feature_names_out())
    
    print("\nTF-IDF Matrix Shape:")
    print(f"{tfidf_matrix.shape} (3 Documents, {tfidf_matrix.shape[1]} unique vocabulary words)")
    
    print("\nDocument 1 Vector:")
    print(np.round(tfidf_matrix.toarray()[0], 2))
    print("Notice how the math has heavily weighted the words 'amazing' and 'love'!")


# ==============================================================================
# 5. NLP MACHINE LEARNING PIPELINE
# ==============================================================================
def demonstrate_nlp_pipeline():
    section_header("End-to-End NLP ML Pipeline")
    
    if not HAS_SKLEARN: return
    
    print("We will combine TF-IDF and a Naive Bayes Classifier into a single Pipeline!\n")
    
    # 1. Synthetic Dataset
    X = [
        "I absolutely love this phone.", "Best purchase ever!", "Amazing battery life.",
        "Terrible, it broke immediately.", "Worst customer service.", "Do not buy this trash."
    ]
    # 1 = Positive, 0 = Negative
    y = [1, 1, 1, 0, 0, 0]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)
    
    # 2. Build the Pipeline
    # Data flows from Raw String -> TF-IDF Matrix -> Naive Bayes Classifier
    nlp_pipeline = Pipeline([
        ('vectorizer', TfidfVectorizer(stop_words='english')),
        ('classifier', MultinomialNB())
    ])
    
    # 3. Train the Model (Using RAW STRINGS!)
    nlp_pipeline.fit(X_train, y_train)
    
    # 4. Predict on the Test Set
    preds = nlp_pipeline.predict(X_test)
    
    print("Predictions on Test Set:")
    for text, pred in zip(X_test, preds):
        sentiment = "Positive" if pred == 1 else "Negative"
        print(f"'{text}' -> {sentiment}")
        
    print(f"\nPipeline Accuracy: {accuracy_score(y_test, preds)*100:.1f}%")
    
    print("\nYou can now `joblib.dump(nlp_pipeline, 'model.pkl')` and deploy ")
    print("it to a Web Server! The Pipeline will automatically handle the TF-IDF ")
    print("math for all incoming live user reviews!")


def run_all_labs():
    demonstrate_vader()
    demonstrate_tfidf()
    demonstrate_nlp_pipeline()


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. What specific problem does TF-IDF solve compared to a simple "Bag of Words" (CountVectorizer)?
   Answer: A simple CountVectorizer just counts the frequency of words. If the word "good" appears 10 times, it gets a weight of 10. The problem is that common words completely overwhelm the matrix. TF-IDF (Term Frequency - Inverse Document Frequency) solves this by mathematically penalizing words that appear in *every single document*. If the word "battery" appears 5 times in Document A (High TF), but it also appears in 99% of all other documents in the corpus (Low IDF), the math heavily suppresses its weight. If the word "defective" appears 3 times in Document B (High TF), but is extremely rare across the rest of the corpus (High IDF), its mathematical weight violently spikes, signaling to the Machine Learning model that this is a critically important feature.

2. Why is Naive Bayes (MultinomialNB) the industry standard baseline algorithm for Text Classification?
   Answer: Text data is highly dimensional. If your training dataset has 50,000 unique words, your TF-IDF matrix will have 50,000 columns! Algorithms like K-Nearest Neighbors or Support Vector Machines suffer catastrophic slowdowns (The Curse of Dimensionality) when dealing with 50,000 dimensions. Naive Bayes relies on simple Bayesian probability math ($P(A|B)$), which scales linearly. It is blindingly fast to train on massive text matrices, highly resistant to overfitting on sparse data, and performs shockingly well as a baseline for spam detection and sentiment analysis.

3. Why is it absolutely critical to put the `TfidfVectorizer` and the Classifier inside a Scikit-Learn `Pipeline`?
   Answer: Data Leakage and Deployment Architecture. If you run `TfidfVectorizer.fit_transform()` on your *entire* dataset before splitting it into Train and Test sets, the IDF mathematical calculation has "leaked" information from the secret Test set into the Training set, invalidating your accuracy metrics. By using a `Pipeline`, Scikit-Learn guarantees that the Vectorizer is strictly fitted *only* on the Training data during `pipeline.fit()`. Furthermore, in production, a web server receives raw strings, not matrices. If you don't save them as a unified Pipeline object, you have to write manual, error-prone code on the web server to load the Vectorizer, transform the text, load the model, and predict. The Pipeline handles everything dynamically.
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Sentiment Analysis & NLP Pipelines Completed.")
