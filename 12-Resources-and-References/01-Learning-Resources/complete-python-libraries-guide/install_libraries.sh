#!/bin/bash
# Complete Python Libraries Installation Script
# For AI, Machine Learning, and Data Science

echo "Installing Python Libraries for AI/ML/Data Science..."
echo "=================================================="

# Update pip
python -m pip install --upgrade pip

# Core Data Science
echo "Installing Core Data Science Libraries..."
pip install numpy pandas matplotlib

# Machine Learning
echo "Installing Machine Learning Libraries..."
pip install scikit-learn xgboost lightgbm

# Deep Learning
echo "Installing Deep Learning Libraries..."
pip install tensorflow torch torchvision torchaudio

# Computer Vision
echo "Installing Computer Vision Libraries..."
pip install opencv-python Pillow scikit-image

# Natural Language Processing
echo "Installing NLP Libraries..."
pip install nltk spacy transformers

# Data Visualization
echo "Installing Visualization Libraries..."
pip install seaborn plotly bokeh

# Statistical Analysis
echo "Installing Statistical Libraries..."
pip install scipy statsmodels

# Big Data
echo "Installing Big Data Libraries..."
pip install "dask[complete]" pyspark

# Specialized ML
echo "Installing MLOps Libraries..."
pip install optuna mlflow wandb

# Deployment
echo "Installing Deployment Libraries..."
pip install fastapi uvicorn streamlit gradio

# Additional useful packages
echo "Installing Additional Tools..."
pip install jupyter jupyterlab pandas-profiling sweetviz

echo "Installation Complete!"
echo "Run 'python -c "import numpy, pandas, sklearn, tensorflow, torch; print('All libraries installed successfully!')"' to verify"
