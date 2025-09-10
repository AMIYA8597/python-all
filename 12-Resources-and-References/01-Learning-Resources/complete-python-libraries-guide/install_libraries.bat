@echo off
REM Complete Python Libraries Installation Script
REM For AI, Machine Learning, and Data Science

echo Installing Python Libraries for AI/ML/Data Science...
echo ==================================================

REM Update pip
python -m pip install --upgrade pip

REM Core Data Science
echo Installing Core Data Science Libraries...
pip install numpy pandas matplotlib

REM Machine Learning
echo Installing Machine Learning Libraries...
pip install scikit-learn xgboost lightgbm

REM Deep Learning
echo Installing Deep Learning Libraries...
pip install tensorflow torch torchvision torchaudio

REM Computer Vision
echo Installing Computer Vision Libraries...
pip install opencv-python Pillow scikit-image

REM Natural Language Processing
echo Installing NLP Libraries...
pip install nltk spacy transformers

REM Data Visualization
echo Installing Visualization Libraries...
pip install seaborn plotly bokeh

REM Statistical Analysis
echo Installing Statistical Libraries...
pip install scipy statsmodels

REM Big Data
echo Installing Big Data Libraries...
pip install "dask[complete]" pyspark

REM Specialized ML
echo Installing MLOps Libraries...
pip install optuna mlflow wandb

REM Deployment
echo Installing Deployment Libraries...
pip install fastapi uvicorn streamlit gradio

REM Additional useful packages
echo Installing Additional Tools...
pip install jupyter jupyterlab pandas-profiling sweetviz

echo Installation Complete!
echo Run 'python -c "import numpy, pandas, sklearn, tensorflow, torch; print('All libraries installed successfully!')"' to verify
