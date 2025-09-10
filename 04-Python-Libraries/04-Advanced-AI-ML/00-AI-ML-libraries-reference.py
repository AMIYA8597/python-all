#!/usr/bin/env python3
"""
Comprehensive AI/ML Libraries Reference Guide
=============================================

This module provides a complete reference guide to all major Python libraries used in
Artificial Intelligence, Machine Learning, and Data Science. It serves as a quick
reference for developers and researchers working in these fields.

Categories Covered:
1. Core Data Science Libraries (NumPy, Pandas, Matplotlib)
2. Machine Learning Frameworks (Scikit-learn, XGBoost, LightGBM)
3. Deep Learning Frameworks (TensorFlow, PyTorch, Keras)
4. Computer Vision (OpenCV, Pillow, scikit-image)
5. Natural Language Processing (NLTK, spaCy, Transformers)
6. Data Visualization (Matplotlib, Seaborn, Plotly)
7. Statistical Analysis (SciPy, Statsmodels)
8. Big Data & Distributed Computing (Dask, PySpark)
9. Specialized ML Libraries (Optuna, MLflow, Weights & Biases)
10. Deployment & Production (FastAPI, Streamlit, Docker)

Installation Commands:
All installation commands are provided for each library.

Author: Python DSA Master
Date: 2024
"""

from typing import Dict, List, Tuple, Any
import warnings
warnings.filterwarnings('ignore')

class AIMLLibrariesReference:
    """Comprehensive reference for AI/ML libraries in Python."""
    
    def __init__(self):
        self.categories = self._initialize_library_categories()
    
    def _initialize_library_categories(self) -> Dict[str, Dict[str, Any]]:
        """Initialize comprehensive library categorization."""
        return {
            "core_data_science": {
                "title": "Core Data Science Libraries",
                "description": "Essential libraries for data manipulation and analysis",
                "libraries": {
                    "numpy": {
                        "name": "NumPy",
                        "description": "Fundamental package for numerical computing",
                        "install": "pip install numpy",
                        "import_pattern": "import numpy as np",
                        "key_features": [
                            "N-dimensional arrays",
                            "Mathematical functions",
                            "Linear algebra operations",
                            "Random number generation",
                            "Fourier transforms"
                        ],
                        "example": """
import numpy as np
arr = np.array([1, 2, 3, 4, 5])
matrix = np.array([[1, 2], [3, 4]])
result = np.dot(matrix, matrix)
"""
                    },
                    "pandas": {
                        "name": "Pandas",
                        "description": "Data structures and data analysis tools",
                        "install": "pip install pandas",
                        "import_pattern": "import pandas as pd",
                        "key_features": [
                            "DataFrame and Series objects",
                            "Data cleaning and preprocessing",
                            "File I/O (CSV, Excel, JSON, SQL)",
                            "Data aggregation and grouping",
                            "Time series analysis"
                        ],
                        "example": """
import pandas as pd
df = pd.read_csv('data.csv')
summary = df.describe()
grouped = df.groupby('category').mean()
"""
                    },
                    "matplotlib": {
                        "name": "Matplotlib",
                        "description": "Plotting library for creating static, animated, and interactive visualizations",
                        "install": "pip install matplotlib",
                        "import_pattern": "import matplotlib.pyplot as plt",
                        "key_features": [
                            "Line plots, scatter plots, bar charts",
                            "Histograms and distributions",
                            "3D plotting",
                            "Interactive widgets",
                            "Publication-quality figures"
                        ],
                        "example": """
import matplotlib.pyplot as plt
import numpy as np
x = np.linspace(0, 10, 100)
y = np.sin(x)
plt.plot(x, y)
plt.show()
"""
                    }
                }
            },
            
            "machine_learning": {
                "title": "Machine Learning Frameworks",
                "description": "Libraries for traditional machine learning algorithms",
                "libraries": {
                    "scikit-learn": {
                        "name": "Scikit-learn",
                        "description": "Machine learning library with simple and efficient tools",
                        "install": "pip install scikit-learn",
                        "import_pattern": "from sklearn import *",
                        "key_features": [
                            "Classification and regression algorithms",
                            "Clustering and dimensionality reduction",
                            "Model selection and evaluation",
                            "Data preprocessing",
                            "Pipeline creation"
                        ],
                        "example": """
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
clf = RandomForestClassifier(n_estimators=100)
clf.fit(X_train, y_train)
accuracy = clf.score(X_test, y_test)
"""
                    },
                    "xgboost": {
                        "name": "XGBoost",
                        "description": "Optimized gradient boosting framework",
                        "install": "pip install xgboost",
                        "import_pattern": "import xgboost as xgb",
                        "key_features": [
                            "Gradient boosting algorithms",
                            "High performance and efficiency",
                            "Feature importance",
                            "Cross-validation support",
                            "GPU acceleration"
                        ],
                        "example": """
import xgboost as xgb
dtrain = xgb.DMatrix(X_train, label=y_train)
params = {'objective': 'reg:squarederror', 'max_depth': 6}
model = xgb.train(params, dtrain, num_boost_round=100)
"""
                    },
                    "lightgbm": {
                        "name": "LightGBM",
                        "description": "Fast, distributed, high performance gradient boosting framework",
                        "install": "pip install lightgbm",
                        "import_pattern": "import lightgbm as lgb",
                        "key_features": [
                            "Fast training speed",
                            "Lower memory usage",
                            "Better accuracy",
                            "Support for parallel learning",
                            "GPU support"
                        ],
                        "example": """
import lightgbm as lgb
train_data = lgb.Dataset(X_train, label=y_train)
params = {'objective': 'regression', 'metric': 'rmse'}
model = lgb.train(params, train_data, num_boost_round=100)
"""
                    }
                }
            },
            
            "deep_learning": {
                "title": "Deep Learning Frameworks",
                "description": "Libraries for building and training neural networks",
                "libraries": {
                    "tensorflow": {
                        "name": "TensorFlow",
                        "description": "End-to-end open source platform for machine learning",
                        "install": "pip install tensorflow",
                        "import_pattern": "import tensorflow as tf",
                        "key_features": [
                            "Neural network building (Keras API)",
                            "Automatic differentiation",
                            "Distributed training",
                            "TensorBoard visualization",
                            "Mobile and web deployment"
                        ],
                        "example": """
import tensorflow as tf
from tensorflow import keras
model = keras.Sequential([
    keras.layers.Dense(64, activation='relu'),
    keras.layers.Dense(10, activation='softmax')
])
model.compile(optimizer='adam', loss='categorical_crossentropy')
model.fit(X_train, y_train, epochs=10)
"""
                    },
                    "pytorch": {
                        "name": "PyTorch",
                        "description": "Dynamic deep learning framework with Python-first approach",
                        "install": "pip install torch torchvision torchaudio",
                        "import_pattern": "import torch",
                        "key_features": [
                            "Dynamic computation graphs",
                            "Pythonic interface",
                            "Strong GPU acceleration",
                            "Research-friendly design",
                            "TorchScript for deployment"
                        ],
                        "example": """
import torch
import torch.nn as nn
class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.fc1 = nn.Linear(784, 64)
        self.fc2 = nn.Linear(64, 10)
    
    def forward(self, x):
        x = torch.relu(self.fc1(x))
        return self.fc2(x)
"""
                    },
                    "keras": {
                        "name": "Keras",
                        "description": "High-level neural networks API (now part of TensorFlow)",
                        "install": "pip install tensorflow  # Keras is included",
                        "import_pattern": "from tensorflow import keras",
                        "key_features": [
                            "User-friendly API",
                            "Modular and composable",
                            "Easy prototyping",
                            "Supports multiple backends",
                            "Extensive pre-trained models"
                        ],
                        "example": """
from tensorflow import keras
from tensorflow.keras import layers
model = keras.Sequential([
    layers.Dense(64, activation='relu', input_shape=(784,)),
    layers.Dropout(0.2),
    layers.Dense(10, activation='softmax')
])
"""
                    }
                }
            },
            
            "computer_vision": {
                "title": "Computer Vision Libraries",
                "description": "Libraries for image processing and computer vision",
                "libraries": {
                    "opencv": {
                        "name": "OpenCV",
                        "description": "Open source computer vision and machine learning library",
                        "install": "pip install opencv-python",
                        "import_pattern": "import cv2",
                        "key_features": [
                            "Image and video processing",
                            "Object detection and recognition",
                            "Feature detection",
                            "Camera calibration",
                            "Machine learning algorithms"
                        ],
                        "example": """
import cv2
import numpy as np
image = cv2.imread('image.jpg')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray, 100, 200)
cv2.imshow('Edges', edges)
"""
                    },
                    "pillow": {
                        "name": "Pillow (PIL)",
                        "description": "Python Imaging Library for image processing",
                        "install": "pip install Pillow",
                        "import_pattern": "from PIL import Image",
                        "key_features": [
                            "Image file I/O",
                            "Basic image processing",
                            "Image filtering and enhancement",
                            "Format conversions",
                            "Drawing capabilities"
                        ],
                        "example": """
from PIL import Image, ImageFilter
image = Image.open('image.jpg')
resized = image.resize((800, 600))
blurred = image.filter(ImageFilter.BLUR)
"""
                    },
                    "scikit-image": {
                        "name": "scikit-image",
                        "description": "Image processing in Python",
                        "install": "pip install scikit-image",
                        "import_pattern": "from skimage import *",
                        "key_features": [
                            "Image segmentation",
                            "Geometric transformations",
                            "Color space conversions",
                            "Feature detection",
                            "Morphological operations"
                        ],
                        "example": """
from skimage import io, filters, segmentation
image = io.imread('image.jpg')
edges = filters.sobel(image)
segments = segmentation.slic(image, n_segments=100)
"""
                    }
                }
            },
            
            "nlp": {
                "title": "Natural Language Processing",
                "description": "Libraries for text processing and NLP",
                "libraries": {
                    "nltk": {
                        "name": "NLTK",
                        "description": "Natural Language Toolkit for text processing",
                        "install": "pip install nltk",
                        "import_pattern": "import nltk",
                        "key_features": [
                            "Tokenization and stemming",
                            "Part-of-speech tagging",
                            "Named entity recognition",
                            "Sentiment analysis",
                            "Corpora and lexical resources"
                        ],
                        "example": """
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
nltk.download('punkt')
nltk.download('stopwords')
tokens = word_tokenize("Hello, world!")
stop_words = set(stopwords.words('english'))
"""
                    },
                    "spacy": {
                        "name": "spaCy",
                        "description": "Industrial-strength NLP library",
                        "install": "pip install spacy",
                        "import_pattern": "import spacy",
                        "key_features": [
                            "Fast tokenization",
                            "Named entity recognition",
                            "Dependency parsing",
                            "Word vectors",
                            "Pre-trained models"
                        ],
                        "example": """
import spacy
nlp = spacy.load("en_core_web_sm")
doc = nlp("Apple is looking at buying U.K. startup for $1 billion")
for ent in doc.ents:
    print(ent.text, ent.label_)
"""
                    },
                    "transformers": {
                        "name": "Transformers",
                        "description": "State-of-the-art Natural Language Processing for PyTorch and TensorFlow",
                        "install": "pip install transformers",
                        "import_pattern": "from transformers import *",
                        "key_features": [
                            "Pre-trained transformer models",
                            "BERT, GPT, RoBERTa, T5, etc.",
                            "Easy fine-tuning",
                            "Tokenization utilities",
                            "Model hub integration"
                        ],
                        "example": """
from transformers import pipeline
classifier = pipeline("sentiment-analysis")
result = classifier("I love this library!")
print(result)  # [{'label': 'POSITIVE', 'score': 0.999}]
"""
                    }
                }
            },
            
            "visualization": {
                "title": "Data Visualization Libraries",
                "description": "Libraries for creating charts, plots, and interactive visualizations",
                "libraries": {
                    "seaborn": {
                        "name": "Seaborn",
                        "description": "Statistical data visualization based on matplotlib",
                        "install": "pip install seaborn",
                        "import_pattern": "import seaborn as sns",
                        "key_features": [
                            "Statistical plotting",
                            "Beautiful default styles",
                            "Built-in themes",
                            "Complex visualizations",
                            "Automatic legend generation"
                        ],
                        "example": """
import seaborn as sns
import matplotlib.pyplot as plt
sns.set_style("whitegrid")
sns.scatterplot(data=df, x="height", y="weight")
plt.show()
"""
                    },
                    "plotly": {
                        "name": "Plotly",
                        "description": "Interactive graphing library",
                        "install": "pip install plotly",
                        "import_pattern": "import plotly.express as px",
                        "key_features": [
                            "Interactive plots",
                            "Web-based visualizations",
                            "3D plotting",
                            "Animation support",
                            "Dashboard creation"
                        ],
                        "example": """
import plotly.express as px
fig = px.scatter(df, x="height", y="weight", color="gender")
fig.show()
"""
                    },
                    "bokeh": {
                        "name": "Bokeh",
                        "description": "Interactive visualization library for web browsers",
                        "install": "pip install bokeh",
                        "import_pattern": "from bokeh.plotting import figure",
                        "key_features": [
                            "Interactive visualizations",
                            "Large dataset handling",
                            "Server applications",
                            "Custom widgets",
                            "Real-time streaming"
                        ],
                        "example": """
from bokeh.plotting import figure, show
p = figure(title="Simple line example")
p.line([1, 2, 3, 4, 5], [6, 7, 2, 4, 5])
show(p)
"""
                    }
                }
            },
            
            "statistical_analysis": {
                "title": "Statistical Analysis Libraries",
                "description": "Libraries for statistical computing and analysis",
                "libraries": {
                    "scipy": {
                        "name": "SciPy",
                        "description": "Scientific computing library",
                        "install": "pip install scipy",
                        "import_pattern": "import scipy",
                        "key_features": [
                            "Statistical functions",
                            "Optimization algorithms",
                            "Signal processing",
                            "Linear algebra",
                            "Integration and ODEs"
                        ],
                        "example": """
from scipy import stats
import numpy as np
data = np.random.normal(0, 1, 1000)
t_stat, p_value = stats.ttest_1samp(data, 0)
"""
                    },
                    "statsmodels": {
                        "name": "Statsmodels",
                        "description": "Statistical modeling and econometrics",
                        "install": "pip install statsmodels",
                        "import_pattern": "import statsmodels.api as sm",
                        "key_features": [
                            "Linear and non-linear regression",
                            "Time series analysis",
                            "Hypothesis testing",
                            "ANOVA",
                            "Generalized linear models"
                        ],
                        "example": """
import statsmodels.api as sm
X = sm.add_constant(X)  # Add intercept
model = sm.OLS(y, X)
results = model.fit()
print(results.summary())
"""
                    }
                }
            },
            
            "big_data": {
                "title": "Big Data & Distributed Computing",
                "description": "Libraries for handling large datasets and distributed computing",
                "libraries": {
                    "dask": {
                        "name": "Dask",
                        "description": "Parallel computing with task scheduling",
                        "install": "pip install dask[complete]",
                        "import_pattern": "import dask.dataframe as dd",
                        "key_features": [
                            "Parallel arrays and dataframes",
                            "Task scheduling",
                            "Lazy evaluation",
                            "Scalable computing",
                            "Integration with NumPy/Pandas"
                        ],
                        "example": """
import dask.dataframe as dd
df = dd.read_csv('large_file.csv')
result = df.groupby('column').value.mean().compute()
"""
                    },
                    "pyspark": {
                        "name": "PySpark",
                        "description": "Python API for Apache Spark",
                        "install": "pip install pyspark",
                        "import_pattern": "from pyspark.sql import SparkSession",
                        "key_features": [
                            "Distributed data processing",
                            "SQL queries",
                            "Machine learning (MLlib)",
                            "Streaming data",
                            "Graph processing"
                        ],
                        "example": """
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("MyApp").getOrCreate()
df = spark.read.csv("data.csv", header=True, inferSchema=True)
df.show()
"""
                    }
                }
            },
            
            "specialized_ml": {
                "title": "Specialized ML Libraries",
                "description": "Specialized libraries for ML operations and MLOps",
                "libraries": {
                    "optuna": {
                        "name": "Optuna",
                        "description": "Hyperparameter optimization framework",
                        "install": "pip install optuna",
                        "import_pattern": "import optuna",
                        "key_features": [
                            "Efficient hyperparameter tuning",
                            "Pruning of unpromising trials",
                            "Multiple sampling algorithms",
                            "Visualization tools",
                            "Distributed optimization"
                        ],
                        "example": """
import optuna
def objective(trial):
    x = trial.suggest_float('x', -10, 10)
    return (x - 2) ** 2
study = optuna.create_study()
study.optimize(objective, n_trials=100)
"""
                    },
                    "mlflow": {
                        "name": "MLflow",
                        "description": "Machine learning lifecycle management",
                        "install": "pip install mlflow",
                        "import_pattern": "import mlflow",
                        "key_features": [
                            "Experiment tracking",
                            "Model registry",
                            "Model serving",
                            "Project packaging",
                            "Artifact storage"
                        ],
                        "example": """
import mlflow
import mlflow.sklearn
with mlflow.start_run():
    mlflow.log_param("alpha", alpha)
    mlflow.log_metric("rmse", rmse)
    mlflow.sklearn.log_model(model, "model")
"""
                    },
                    "wandb": {
                        "name": "Weights & Biases",
                        "description": "Experiment tracking and model management",
                        "install": "pip install wandb",
                        "import_pattern": "import wandb",
                        "key_features": [
                            "Experiment tracking",
                            "Hyperparameter tuning",
                            "Model versioning",
                            "Collaborative workspace",
                            "Production monitoring"
                        ],
                        "example": """
import wandb
wandb.init(project="my-project")
wandb.config.learning_rate = 0.01
wandb.log({"loss": loss, "accuracy": accuracy})
"""
                    }
                }
            },
            
            "deployment": {
                "title": "Deployment & Production Libraries",
                "description": "Libraries for deploying ML models and creating applications",
                "libraries": {
                    "fastapi": {
                        "name": "FastAPI",
                        "description": "Modern, fast web framework for building APIs",
                        "install": "pip install fastapi uvicorn",
                        "import_pattern": "from fastapi import FastAPI",
                        "key_features": [
                            "High performance",
                            "Easy to use",
                            "Automatic API documentation",
                            "Type hints support",
                            "Async support"
                        ],
                        "example": """
from fastapi import FastAPI
app = FastAPI()
@app.post("/predict")
async def predict(data: InputData):
    prediction = model.predict(data.features)
    return {"prediction": prediction}
"""
                    },
                    "streamlit": {
                        "name": "Streamlit",
                        "description": "Framework for building ML web applications",
                        "install": "pip install streamlit",
                        "import_pattern": "import streamlit as st",
                        "key_features": [
                            "Easy web app creation",
                            "Interactive widgets",
                            "Data visualization",
                            "Real-time updates",
                            "Sharing and deployment"
                        ],
                        "example": """
import streamlit as st
import pandas as pd
st.title("My ML App")
uploaded_file = st.file_uploader("Choose a CSV file")
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write(df)
"""
                    },
                    "gradio": {
                        "name": "Gradio",
                        "description": "Build machine learning demos and web applications",
                        "install": "pip install gradio",
                        "import_pattern": "import gradio as gr",
                        "key_features": [
                            "Quick demo creation",
                            "Multiple input/output types",
                            "Share demos easily",
                            "Customizable interface",
                            "Integration with Hugging Face"
                        ],
                        "example": """
import gradio as gr
def predict(image):
    return model.predict(image)
interface = gr.Interface(fn=predict, inputs="image", outputs="label")
interface.launch()
"""
                    }
                }
            }
        }
    
    def display_category(self, category_key: str) -> None:
        """Display information about a specific category."""
        if category_key not in self.categories:
            print(f"Category '{category_key}' not found.")
            return
        
        category = self.categories[category_key]
        print(f"\n{'='*70}")
        print(f"{category['title'].upper()}")
        print(f"{'='*70}")
        print(f"Description: {category['description']}")
        
        for lib_key, lib_info in category['libraries'].items():
            print(f"\n{'-'*50}")
            print(f"📚 {lib_info['name']}")
            print(f"{'-'*50}")
            print(f"Description: {lib_info['description']}")
            print(f"Installation: {lib_info['install']}")
            print(f"Import Pattern: {lib_info['import_pattern']}")
            
            print(f"\nKey Features:")
            for feature in lib_info['key_features']:
                print(f"  • {feature}")
            
            print(f"\nExample Usage:{lib_info['example']}")
    
    def display_all_categories(self) -> None:
        """Display all categories and their libraries."""
        print("AI/ML LIBRARIES COMPREHENSIVE REFERENCE GUIDE")
        print("=" * 70)
        
        for category_key in self.categories:
            self.display_category(category_key)
    
    def get_installation_commands(self) -> Dict[str, str]:
        """Get all installation commands organized by category."""
        installation_commands = {}
        
        for category_key, category in self.categories.items():
            commands = []
            for lib_key, lib_info in category['libraries'].items():
                commands.append(f"# {lib_info['name']}")
                commands.append(lib_info['install'])
                commands.append("")
            
            installation_commands[category['title']] = "\n".join(commands)
        
        return installation_commands
    
    def create_quick_reference(self) -> str:
        """Create a quick reference sheet."""
        quick_ref = []
        quick_ref.append("AI/ML LIBRARIES QUICK REFERENCE")
        quick_ref.append("=" * 50)
        
        for category_key, category in self.categories.items():
            quick_ref.append(f"\n{category['title'].upper()}:")
            quick_ref.append("-" * len(category['title']))
            
            for lib_key, lib_info in category['libraries'].items():
                quick_ref.append(f"• {lib_info['name']}: {lib_info['description']}")
                quick_ref.append(f"  Install: {lib_info['install']}")
                quick_ref.append(f"  Import: {lib_info['import_pattern']}")
                quick_ref.append("")
        
        return "\n".join(quick_ref)

def create_complete_installation_script():
    """Create a complete installation script for all libraries."""
    ref = AIMLLibrariesReference()
    
    print("\n" + "="*70)
    print("COMPLETE AI/ML LIBRARIES INSTALLATION SCRIPT")
    print("="*70)
    
    print("""
# This script installs all major AI/ML libraries mentioned in this guide
# Run sections as needed based on your requirements

# Note: Some libraries may have specific system requirements
# It's recommended to use a virtual environment

# Create virtual environment (optional but recommended)
# python -m venv ml_env
# source ml_env/bin/activate  # On Windows: ml_env\\Scripts\\activate
""")
    
    all_commands = ref.get_installation_commands()
    
    for category, commands in all_commands.items():
        print(f"\n# {category.upper()}")
        print("#" + "="*(len(category)+2))
        print(commands)
    
    print("""
# Additional useful commands:

# Update all packages
pip install --upgrade pip

# Install Jupyter for interactive development
pip install jupyter jupyterlab

# Install additional data science tools
pip install pandas-profiling sweetviz

# GPU acceleration (optional, requires compatible hardware)
# pip install tensorflow-gpu  # For TensorFlow GPU
# pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu116  # PyTorch CUDA

# Verify installations
python -c "import numpy, pandas, matplotlib, sklearn, tensorflow, torch; print('All core libraries installed successfully!')"
""")

def demonstrate_library_workflows():
    """Demonstrate common workflows using multiple libraries together."""
    print("\n" + "="*70)
    print("COMMON AI/ML WORKFLOWS WITH MULTIPLE LIBRARIES")
    print("="*70)
    
    workflows = {
        "Data Science Pipeline": """
# Complete data science pipeline
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

# 1. Data loading and exploration
df = pd.read_csv('data.csv')
print(df.info())
print(df.describe())

# 2. Data visualization
plt.figure(figsize=(12, 8))
sns.heatmap(df.corr(), annot=True, cmap='coolwarm')
plt.show()

# 3. Data preprocessing
X = df.drop('target', axis=1)
y = df['target']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. Model training
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 5. Model evaluation
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))
""",
        
        "Deep Learning with Computer Vision": """
# Computer vision with deep learning
import cv2
import numpy as np
import tensorflow as tf
from tensorflow import keras
from PIL import Image
import matplotlib.pyplot as plt

# 1. Image preprocessing
def preprocess_image(image_path):
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (224, 224))
    image = image / 255.0
    return image

# 2. Load pre-trained model
model = keras.applications.VGG16(weights='imagenet', include_top=True)

# 3. Make predictions
image = preprocess_image('image.jpg')
image_batch = np.expand_dims(image, axis=0)
predictions = model.predict(image_batch)
decoded_predictions = keras.applications.imagenet_utils.decode_predictions(predictions, top=3)[0]

# 4. Display results
plt.imshow(image)
plt.title(f"Prediction: {decoded_predictions[0][1]} ({decoded_predictions[0][2]:.2f})")
plt.show()
""",
        
        "NLP Pipeline": """
# Natural language processing pipeline
import nltk
import spacy
from transformers import pipeline
import pandas as pd

# 1. Text preprocessing with NLTK
nltk.download('punkt')
nltk.download('stopwords')
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

def preprocess_text(text):
    tokens = word_tokenize(text.lower())
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words and token.isalpha()]
    return ' '.join(tokens)

# 2. Advanced NLP with spaCy
nlp = spacy.load("en_core_web_sm")
def extract_entities(text):
    doc = nlp(text)
    return [(ent.text, ent.label_) for ent in doc.ents]

# 3. Sentiment analysis with Transformers
classifier = pipeline("sentiment-analysis")

# 4. Process data
texts = ["I love this product!", "This is terrible.", "It's okay, nothing special."]
results = []

for text in texts:
    processed_text = preprocess_text(text)
    entities = extract_entities(text)
    sentiment = classifier(text)[0]
    
    results.append({
        'original_text': text,
        'processed_text': processed_text,
        'entities': entities,
        'sentiment': sentiment['label'],
        'confidence': sentiment['score']
    })

df_results = pd.DataFrame(results)
print(df_results)
""",
        
        "MLOps Pipeline": """
# MLOps pipeline with experiment tracking
import mlflow
import mlflow.sklearn
import optuna
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
from sklearn.datasets import load_iris

# 1. Load data
X, y = load_iris(return_X_y=True)

# 2. Hyperparameter optimization with Optuna
def objective(trial):
    n_estimators = trial.suggest_int('n_estimators', 10, 100)
    max_depth = trial.suggest_int('max_depth', 1, 10)
    
    model = RandomForestClassifier(
        n_estimators=n_estimators,
        max_depth=max_depth,
        random_state=42
    )
    
    scores = cross_val_score(model, X, y, cv=5)
    return scores.mean()

study = optuna.create_study(direction='maximize')
study.optimize(objective, n_trials=20)

# 3. Train best model with MLflow tracking
mlflow.start_run()

best_params = study.best_params
model = RandomForestClassifier(**best_params, random_state=42)
model.fit(X, y)

# Log parameters and metrics
mlflow.log_params(best_params)
mlflow.log_metric("accuracy", study.best_value)

# Log model
mlflow.sklearn.log_model(model, "random_forest_model")

mlflow.end_run()

print(f"Best parameters: {best_params}")
print(f"Best score: {study.best_value}")
"""
    }
    
    for workflow_name, code in workflows.items():
        print(f"\n{workflow_name.upper()}")
        print("-" * len(workflow_name))
        print(code)
        print()

def main():
    """Main function to display the comprehensive AI/ML libraries reference."""
    print("COMPREHENSIVE AI/ML LIBRARIES REFERENCE GUIDE")
    print("=" * 70)
    print("This guide covers all major Python libraries used in AI, ML, and Data Science")
    print()
    
    # Initialize reference
    ref = AIMLLibrariesReference()
    
    # Display all categories
    ref.display_all_categories()
    
    # Create installation script
    create_complete_installation_script()
    
    # Show common workflows
    demonstrate_library_workflows()
    
    # Quick reference
    print("\n" + "="*70)
    print("QUICK REFERENCE SUMMARY")
    print("="*70)
    quick_ref = ref.create_quick_reference()
    print(quick_ref)
    
    print("\n" + "="*70)
    print("RECOMMENDATIONS FOR GETTING STARTED")
    print("="*70)
    print("""
1. BEGINNERS:
   - Start with: NumPy, Pandas, Matplotlib, Scikit-learn
   - Learn order: NumPy → Pandas → Matplotlib → Scikit-learn

2. DEEP LEARNING:
   - Choose one: TensorFlow/Keras OR PyTorch
   - Add: NumPy, Matplotlib for data handling and visualization

3. COMPUTER VISION:
   - Core: OpenCV, Pillow
   - Deep Learning: TensorFlow/PyTorch + torchvision/tf-keras-preprocessing
   - Advanced: scikit-image

4. NLP:
   - Traditional: NLTK, spaCy
   - Modern: Transformers (Hugging Face)
   - Deep Learning: TensorFlow/PyTorch

5. DATA SCIENCE:
   - Essential: NumPy, Pandas, Matplotlib, Seaborn, Scikit-learn
   - Statistical: SciPy, Statsmodels
   - Interactive: Jupyter, Plotly

6. PRODUCTION/DEPLOYMENT:
   - APIs: FastAPI, Flask
   - Web Apps: Streamlit, Gradio
   - Tracking: MLflow, Weights & Biases
   - Containerization: Docker

7. BIG DATA:
   - Start with: Dask (pandas-like interface)
   - Scale to: PySpark for very large datasets

Remember: You don't need all libraries at once!
Choose based on your specific project requirements.
""")

if __name__ == "__main__":
    main()
