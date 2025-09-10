#!/usr/bin/env python3
"""
Scikit-learn Comprehensive Guide for AI/ML
==========================================

This module provides comprehensive coverage of scikit-learn (sklearn), the most popular
machine learning library in Python. It covers all major algorithms, preprocessing
techniques, model evaluation, and advanced features.

Topics Covered:
1. Data Preprocessing & Feature Engineering
2. Supervised Learning (Classification & Regression)
3. Unsupervised Learning (Clustering & Dimensionality Reduction)
4. Model Selection & Evaluation
5. Pipeline Creation & Automation
6. Advanced Features & Custom Estimators
7. Real-world Examples & Best Practices

Key Libraries:
- sklearn.preprocessing: Data preprocessing
- sklearn.feature_selection: Feature selection
- sklearn.model_selection: Cross-validation, grid search
- sklearn.linear_model: Linear models
- sklearn.ensemble: Ensemble methods
- sklearn.svm: Support Vector Machines
- sklearn.tree: Decision trees
- sklearn.cluster: Clustering algorithms
- sklearn.decomposition: Dimensionality reduction
- sklearn.metrics: Model evaluation metrics

Author: Python DSA Master
Date: 2024
"""

import numpy as np
import pandas as pd
from typing import List, Dict, Tuple, Any, Optional, Union
import warnings
warnings.filterwarnings('ignore')

# Note: This module demonstrates scikit-learn usage patterns and concepts.
# To run the actual code, install: pip install scikit-learn numpy pandas matplotlib

def demonstrate_sklearn_concepts():
    """
    Demonstrate core scikit-learn concepts without requiring installation.
    This shows the patterns and workflow used in scikit-learn.
    """
    print("Scikit-learn Concepts and Patterns")
    print("=" * 50)
    
    # Typical sklearn workflow
    workflow_steps = [
        "1. Data Loading & Exploration",
        "2. Data Preprocessing & Feature Engineering", 
        "3. Train-Test Split",
        "4. Model Selection & Training",
        "5. Model Evaluation",
        "6. Hyperparameter Tuning",
        "7. Final Model & Predictions"
    ]
    
    for step in workflow_steps:
        print(f"   {step}")
    
    print("\nCommon Scikit-learn Import Patterns:")
    imports = [
        "from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV",
        "from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder",
        "from sklearn.linear_model import LogisticRegression, LinearRegression",
        "from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor",
        "from sklearn.svm import SVC, SVR",
        "from sklearn.cluster import KMeans, DBSCAN",
        "from sklearn.decomposition import PCA, TruncatedSVD",
        "from sklearn.metrics import accuracy_score, classification_report, confusion_matrix",
        "from sklearn.pipeline import Pipeline, make_pipeline"
    ]
    
    for imp in imports:
        print(f"   {imp}")

class SklearnDataPreprocessing:
    """Comprehensive data preprocessing techniques in scikit-learn."""
    
    @staticmethod
    def preprocessing_examples():
        """Show common preprocessing patterns."""
        print("\n" + "="*50)
        print("SCIKIT-LEARN DATA PREPROCESSING")
        print("="*50)
        
        print("\n1. SCALING & NORMALIZATION")
        scaling_examples = [
            "# Standardization (mean=0, std=1)",
            "from sklearn.preprocessing import StandardScaler",
            "scaler = StandardScaler()",
            "X_scaled = scaler.fit_transform(X_train)",
            "X_test_scaled = scaler.transform(X_test)",
            "",
            "# Min-Max Scaling (0-1 range)",
            "from sklearn.preprocessing import MinMaxScaler",
            "minmax_scaler = MinMaxScaler()",
            "X_normalized = minmax_scaler.fit_transform(X)",
            "",
            "# Robust Scaling (median-based)",
            "from sklearn.preprocessing import RobustScaler", 
            "robust_scaler = RobustScaler()",
            "X_robust = robust_scaler.fit_transform(X)",
        ]
        
        for line in scaling_examples:
            print(f"   {line}")
        
        print("\n2. CATEGORICAL ENCODING")
        encoding_examples = [
            "# Label Encoding (ordinal)",
            "from sklearn.preprocessing import LabelEncoder",
            "le = LabelEncoder()",
            "y_encoded = le.fit_transform(y)",
            "",
            "# One-Hot Encoding",
            "from sklearn.preprocessing import OneHotEncoder",
            "ohe = OneHotEncoder(sparse_output=False)",
            "X_encoded = ohe.fit_transform(X_categorical)",
            "",
            "# Target Encoding (advanced)",
            "from sklearn.preprocessing import TargetEncoder",
            "te = TargetEncoder()",
            "X_target_encoded = te.fit_transform(X_categorical, y)",
        ]
        
        for line in encoding_examples:
            print(f"   {line}")
            
        print("\n3. FEATURE SELECTION")
        selection_examples = [
            "# Univariate Feature Selection",
            "from sklearn.feature_selection import SelectKBest, f_classif",
            "selector = SelectKBest(score_func=f_classif, k=10)",
            "X_selected = selector.fit_transform(X, y)",
            "",
            "# Recursive Feature Elimination", 
            "from sklearn.feature_selection import RFE",
            "from sklearn.linear_model import LogisticRegression",
            "estimator = LogisticRegression()",
            "rfe = RFE(estimator=estimator, n_features_to_select=10)",
            "X_rfe = rfe.fit_transform(X, y)",
            "",
            "# Feature Selection from Model",
            "from sklearn.feature_selection import SelectFromModel",
            "from sklearn.ensemble import RandomForestClassifier",
            "rf = RandomForestClassifier()",
            "selector = SelectFromModel(rf)",
            "X_model_selected = selector.fit_transform(X, y)",
        ]
        
        for line in selection_examples:
            print(f"   {line}")

class SklearnSupervisedLearning:
    """Comprehensive supervised learning algorithms in scikit-learn."""
    
    @staticmethod
    def classification_examples():
        """Show classification algorithms and usage."""
        print("\n" + "="*50)
        print("CLASSIFICATION ALGORITHMS")
        print("="*50)
        
        algorithms = {
            "Logistic Regression": [
                "from sklearn.linear_model import LogisticRegression",
                "clf = LogisticRegression(max_iter=1000, random_state=42)",
                "clf.fit(X_train, y_train)",
                "y_pred = clf.predict(X_test)",
                "proba = clf.predict_proba(X_test)  # Get probabilities"
            ],
            
            "Random Forest": [
                "from sklearn.ensemble import RandomForestClassifier", 
                "rf = RandomForestClassifier(n_estimators=100, random_state=42)",
                "rf.fit(X_train, y_train)",
                "y_pred = rf.predict(X_test)",
                "feature_importance = rf.feature_importances_"
            ],
            
            "Support Vector Machine": [
                "from sklearn.svm import SVC",
                "svm = SVC(kernel='rbf', C=1.0, random_state=42)",
                "svm.fit(X_train, y_train)",
                "y_pred = svm.predict(X_test)"
            ],
            
            "Gradient Boosting": [
                "from sklearn.ensemble import GradientBoostingClassifier",
                "gb = GradientBoostingClassifier(n_estimators=100, random_state=42)",
                "gb.fit(X_train, y_train)",
                "y_pred = gb.predict(X_test)"
            ],
            
            "XGBoost (if installed)": [
                "from xgboost import XGBClassifier",
                "xgb = XGBClassifier(n_estimators=100, random_state=42)",
                "xgb.fit(X_train, y_train)",
                "y_pred = xgb.predict(X_test)"
            ],
            
            "Neural Network (MLP)": [
                "from sklearn.neural_network import MLPClassifier",
                "mlp = MLPClassifier(hidden_layer_sizes=(100, 50), max_iter=500)",
                "mlp.fit(X_train, y_train)",
                "y_pred = mlp.predict(X_test)"
            ]
        }
        
        for algo, code_lines in algorithms.items():
            print(f"\n{algo}:")
            for line in code_lines:
                print(f"   {line}")
    
    @staticmethod
    def regression_examples():
        """Show regression algorithms and usage."""
        print("\n" + "="*50)
        print("REGRESSION ALGORITHMS")
        print("="*50)
        
        algorithms = {
            "Linear Regression": [
                "from sklearn.linear_model import LinearRegression",
                "lr = LinearRegression()",
                "lr.fit(X_train, y_train)",
                "y_pred = lr.predict(X_test)",
                "coefficients = lr.coef_"
            ],
            
            "Ridge Regression": [
                "from sklearn.linear_model import Ridge",
                "ridge = Ridge(alpha=1.0)",
                "ridge.fit(X_train, y_train)",
                "y_pred = ridge.predict(X_test)"
            ],
            
            "Lasso Regression": [
                "from sklearn.linear_model import Lasso", 
                "lasso = Lasso(alpha=1.0)",
                "lasso.fit(X_train, y_train)",
                "y_pred = lasso.predict(X_test)",
                "# Lasso performs feature selection automatically"
            ],
            
            "Random Forest Regression": [
                "from sklearn.ensemble import RandomForestRegressor",
                "rf_reg = RandomForestRegressor(n_estimators=100, random_state=42)",
                "rf_reg.fit(X_train, y_train)",
                "y_pred = rf_reg.predict(X_test)"
            ],
            
            "Support Vector Regression": [
                "from sklearn.svm import SVR",
                "svr = SVR(kernel='rbf', C=1.0)",
                "svr.fit(X_train, y_train)",
                "y_pred = svr.predict(X_test)"
            ]
        }
        
        for algo, code_lines in algorithms.items():
            print(f"\n{algo}:")
            for line in code_lines:
                print(f"   {line}")

class SklearnUnsupervisedLearning:
    """Comprehensive unsupervised learning algorithms in scikit-learn."""
    
    @staticmethod
    def clustering_examples():
        """Show clustering algorithms and usage."""
        print("\n" + "="*50)
        print("CLUSTERING ALGORITHMS")
        print("="*50)
        
        algorithms = {
            "K-Means Clustering": [
                "from sklearn.cluster import KMeans",
                "kmeans = KMeans(n_clusters=3, random_state=42)",
                "cluster_labels = kmeans.fit_predict(X)",
                "centroids = kmeans.cluster_centers_",
                "inertia = kmeans.inertia_  # Within-cluster sum of squares"
            ],
            
            "Hierarchical Clustering": [
                "from sklearn.cluster import AgglomerativeClustering",
                "hierarchical = AgglomerativeClustering(n_clusters=3)",
                "cluster_labels = hierarchical.fit_predict(X)"
            ],
            
            "DBSCAN": [
                "from sklearn.cluster import DBSCAN",
                "dbscan = DBSCAN(eps=0.5, min_samples=5)",
                "cluster_labels = dbscan.fit_predict(X)",
                "# -1 indicates noise points"
            ],
            
            "Gaussian Mixture Models": [
                "from sklearn.mixture import GaussianMixture",
                "gmm = GaussianMixture(n_components=3, random_state=42)",
                "cluster_labels = gmm.fit_predict(X)",
                "probabilities = gmm.predict_proba(X)"
            ]
        }
        
        for algo, code_lines in algorithms.items():
            print(f"\n{algo}:")
            for line in code_lines:
                print(f"   {line}")
    
    @staticmethod
    def dimensionality_reduction_examples():
        """Show dimensionality reduction techniques."""
        print("\n" + "="*50)
        print("DIMENSIONALITY REDUCTION")
        print("="*50)
        
        techniques = {
            "Principal Component Analysis (PCA)": [
                "from sklearn.decomposition import PCA",
                "pca = PCA(n_components=2)",
                "X_pca = pca.fit_transform(X)",
                "explained_variance = pca.explained_variance_ratio_",
                "# cumulative variance to choose components"
            ],
            
            "t-SNE": [
                "from sklearn.manifold import TSNE",
                "tsne = TSNE(n_components=2, random_state=42)",
                "X_tsne = tsne.fit_transform(X)",
                "# Great for visualization, non-linear"
            ],
            
            "Linear Discriminant Analysis": [
                "from sklearn.discriminant_analysis import LinearDiscriminantAnalysis",
                "lda = LinearDiscriminantAnalysis(n_components=2)",
                "X_lda = lda.fit_transform(X, y)",
                "# Supervised dimensionality reduction"
            ],
            
            "Truncated SVD": [
                "from sklearn.decomposition import TruncatedSVD",
                "svd = TruncatedSVD(n_components=50, random_state=42)",
                "X_svd = svd.fit_transform(X)",
                "# Good for sparse matrices"
            ]
        }
        
        for technique, code_lines in techniques.items():
            print(f"\n{technique}:")
            for line in code_lines:
                print(f"   {line}")

class SklearnModelEvaluation:
    """Comprehensive model evaluation and validation in scikit-learn."""
    
    @staticmethod
    def evaluation_metrics():
        """Show evaluation metrics for different types of problems."""
        print("\n" + "="*50)
        print("MODEL EVALUATION METRICS")
        print("="*50)
        
        print("\nCLASSIFICATION METRICS:")
        classification_metrics = [
            "from sklearn.metrics import (",
            "    accuracy_score, precision_score, recall_score, f1_score,",
            "    classification_report, confusion_matrix, roc_auc_score,",
            "    roc_curve, precision_recall_curve",
            ")",
            "",
            "# Basic metrics",
            "accuracy = accuracy_score(y_true, y_pred)",
            "precision = precision_score(y_true, y_pred, average='weighted')",
            "recall = recall_score(y_true, y_pred, average='weighted')",
            "f1 = f1_score(y_true, y_pred, average='weighted')",
            "",
            "# Detailed report", 
            "report = classification_report(y_true, y_pred)",
            "",
            "# Confusion matrix",
            "cm = confusion_matrix(y_true, y_pred)",
            "",
            "# ROC AUC (for binary/multiclass)",
            "auc = roc_auc_score(y_true, y_proba, multi_class='ovr')"
        ]
        
        for line in classification_metrics:
            print(f"   {line}")
            
        print("\nREGRESSION METRICS:")
        regression_metrics = [
            "from sklearn.metrics import (",
            "    mean_squared_error, mean_absolute_error, r2_score,",
            "    mean_squared_log_error, explained_variance_score",
            ")",
            "",
            "# Basic regression metrics",
            "mse = mean_squared_error(y_true, y_pred)",
            "rmse = np.sqrt(mse)",
            "mae = mean_absolute_error(y_true, y_pred)",
            "r2 = r2_score(y_true, y_pred)",
            "",
            "# Additional metrics",
            "explained_var = explained_variance_score(y_true, y_pred)",
            "msle = mean_squared_log_error(y_true, y_pred)  # For positive targets"
        ]
        
        for line in regression_metrics:
            print(f"   {line}")
    
    @staticmethod
    def cross_validation_examples():
        """Show cross-validation techniques."""
        print("\n" + "="*50)
        print("CROSS-VALIDATION TECHNIQUES")
        print("="*50)
        
        cv_examples = [
            "from sklearn.model_selection import (",
            "    cross_val_score, cross_validate, StratifiedKFold,",
            "    TimeSeriesSplit, LeaveOneOut, ShuffleSplit",
            ")",
            "",
            "# Simple cross-validation",
            "scores = cross_val_score(model, X, y, cv=5, scoring='accuracy')",
            "print(f'CV Accuracy: {scores.mean():.3f} (+/- {scores.std() * 2:.3f})')",
            "",
            "# Detailed cross-validation",
            "cv_results = cross_validate(model, X, y, cv=5, ",
            "                          scoring=['accuracy', 'precision', 'recall'],",
            "                          return_train_score=True)",
            "",
            "# Stratified K-Fold (maintains class distribution)",
            "skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)",
            "scores = cross_val_score(model, X, y, cv=skf, scoring='f1_macro')",
            "",
            "# Time Series Cross-Validation",
            "tscv = TimeSeriesSplit(n_splits=5)",
            "scores = cross_val_score(model, X, y, cv=tscv, scoring='neg_mean_squared_error')"
        ]
        
        for line in cv_examples:
            print(f"   {line}")

class SklearnPipelinesAndAutomation:
    """Pipeline creation and automation in scikit-learn."""
    
    @staticmethod
    def pipeline_examples():
        """Show pipeline creation and usage."""
        print("\n" + "="*50)
        print("SCIKIT-LEARN PIPELINES")
        print("="*50)
        
        print("\nBASIC PIPELINE:")
        basic_pipeline = [
            "from sklearn.pipeline import Pipeline, make_pipeline",
            "from sklearn.preprocessing import StandardScaler",
            "from sklearn.linear_model import LogisticRegression",
            "",
            "# Method 1: Using Pipeline class",
            "pipe = Pipeline([",
            "    ('scaler', StandardScaler()),",
            "    ('classifier', LogisticRegression())",
            "])",
            "",
            "# Method 2: Using make_pipeline (auto-names)",
            "pipe = make_pipeline(StandardScaler(), LogisticRegression())",
            "",
            "# Use pipeline like any estimator",
            "pipe.fit(X_train, y_train)",
            "y_pred = pipe.predict(X_test)",
            "score = pipe.score(X_test, y_test)"
        ]
        
        for line in basic_pipeline:
            print(f"   {line}")
            
        print("\nCOMPLEX PIPELINE WITH FEATURE ENGINEERING:")
        complex_pipeline = [
            "from sklearn.compose import ColumnTransformer",
            "from sklearn.preprocessing import OneHotEncoder, StandardScaler",
            "",
            "# Separate preprocessing for different column types",
            "numeric_features = ['age', 'income', 'score']",
            "categorical_features = ['category', 'region']",
            "",
            "preprocessor = ColumnTransformer(",
            "    transformers=[",
            "        ('num', StandardScaler(), numeric_features),",
            "        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)",
            "    ])",
            "",
            "# Complete pipeline",
            "full_pipeline = Pipeline([",
            "    ('preprocessor', preprocessor),",
            "    ('classifier', RandomForestClassifier())",
            "])"
        ]
        
        for line in complex_pipeline:
            print(f"   {line}")
    
    @staticmethod
    def hyperparameter_tuning():
        """Show hyperparameter tuning techniques."""
        print("\n" + "="*50)
        print("HYPERPARAMETER TUNING")
        print("="*50)
        
        print("\nGRID SEARCH:")
        grid_search = [
            "from sklearn.model_selection import GridSearchCV",
            "",
            "# Define parameter grid",
            "param_grid = {",
            "    'classifier__n_estimators': [50, 100, 200],",
            "    'classifier__max_depth': [3, 5, 7, None],",
            "    'classifier__min_samples_split': [2, 5, 10]",
            "}",
            "",
            "# Grid search with cross-validation",
            "grid_search = GridSearchCV(",
            "    pipe, param_grid, cv=5, scoring='accuracy',",
            "    n_jobs=-1, verbose=1",
            ")",
            "",
            "grid_search.fit(X_train, y_train)",
            "print(f'Best parameters: {grid_search.best_params_}')",
            "print(f'Best score: {grid_search.best_score_:.3f}')"
        ]
        
        for line in grid_search:
            print(f"   {line}")
            
        print("\nRANDOM SEARCH:")
        random_search = [
            "from sklearn.model_selection import RandomizedSearchCV",
            "from scipy.stats import randint, uniform",
            "",
            "# Random parameter distributions",
            "param_dist = {",
            "    'classifier__n_estimators': randint(50, 200),",
            "    'classifier__max_depth': randint(3, 10),",
            "    'classifier__min_samples_split': randint(2, 20),",
            "    'classifier__min_samples_leaf': randint(1, 10)",
            "}",
            "",
            "# Random search",
            "random_search = RandomizedSearchCV(",
            "    pipe, param_dist, n_iter=100, cv=5,",
            "    scoring='accuracy', n_jobs=-1, random_state=42",
            ")",
            "",
            "random_search.fit(X_train, y_train)"
        ]
        
        for line in random_search:
            print(f"   {line}")

class SklearnAdvancedFeatures:
    """Advanced scikit-learn features and techniques."""
    
    @staticmethod
    def custom_estimators():
        """Show how to create custom estimators."""
        print("\n" + "="*50)
        print("CUSTOM ESTIMATORS")
        print("="*50)
        
        custom_estimator = [
            "from sklearn.base import BaseEstimator, TransformerMixin, ClassifierMixin",
            "",
            "class CustomTransformer(BaseEstimator, TransformerMixin):",
            "    def __init__(self, feature_names=None):",
            "        self.feature_names = feature_names",
            "    ",
            "    def fit(self, X, y=None):",
            "        # Learn parameters from training data",
            "        self.feature_means_ = X.mean(axis=0)",
            "        return self",
            "    ",
            "    def transform(self, X):",
            "        # Apply transformation",
            "        return X - self.feature_means_",
            "",
            "# Custom classifier",
            "class CustomClassifier(BaseEstimator, ClassifierMixin):",
            "    def __init__(self, threshold=0.5):",
            "        self.threshold = threshold",
            "    ",
            "    def fit(self, X, y):",
            "        self.classes_ = np.unique(y)",
            "        # Implement your learning algorithm here",
            "        return self",
            "    ",
            "    def predict(self, X):",
            "        # Implement prediction logic",
            "        # This is a dummy implementation",
            "        return np.random.choice(self.classes_, size=len(X))"
        ]
        
        for line in custom_estimator:
            print(f"   {line}")
    
    @staticmethod
    def advanced_techniques():
        """Show advanced scikit-learn techniques."""
        print("\n" + "="*50)
        print("ADVANCED TECHNIQUES")
        print("="*50)
        
        print("\nMULTI-OUTPUT LEARNING:")
        multi_output = [
            "from sklearn.multioutput import MultiOutputClassifier, MultiOutputRegressor",
            "",
            "# Multi-output classification",
            "multi_clf = MultiOutputClassifier(RandomForestClassifier())",
            "multi_clf.fit(X, y_multi)  # y_multi has multiple columns",
            "",
            "# Multi-output regression", 
            "multi_reg = MultiOutputRegressor(LinearRegression())",
            "multi_reg.fit(X, y_multi)"
        ]
        
        for line in multi_output:
            print(f"   {line}")
            
        print("\nCALIBRATION:")
        calibration = [
            "from sklearn.calibration import CalibratedClassifierCV",
            "",
            "# Calibrate classifier probabilities",
            "calibrated_clf = CalibratedClassifierCV(base_classifier, method='isotonic', cv=3)",
            "calibrated_clf.fit(X_train, y_train)",
            "calibrated_proba = calibrated_clf.predict_proba(X_test)"
        ]
        
        for line in calibration:
            print(f"   {line}")
            
        print("\nINCREMENTAL LEARNING:")
        incremental = [
            "from sklearn.linear_model import SGDClassifier",
            "from sklearn.naive_bayes import MultinomialNB",
            "",
            "# Algorithms that support partial_fit",
            "incremental_clf = SGDClassifier()",
            "",
            "# Train in batches",
            "for batch_X, batch_y in get_batches(X, y):",
            "    incremental_clf.partial_fit(batch_X, batch_y, classes=np.unique(y))"
        ]
        
        for line in incremental:
            print(f"   {line}")

def create_sklearn_cheat_sheet():
    """Create a comprehensive sklearn cheat sheet."""
    print("\n" + "="*70)
    print("SCIKIT-LEARN COMPREHENSIVE CHEAT SHEET")
    print("="*70)
    
    sections = {
        "ESSENTIAL IMPORTS": [
            "import numpy as np",
            "import pandas as pd",
            "from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV",
            "from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder",
            "from sklearn.metrics import accuracy_score, classification_report, confusion_matrix",
            "from sklearn.pipeline import Pipeline, make_pipeline"
        ],
        
        "BASIC WORKFLOW": [
            "# 1. Load and explore data",
            "X, y = load_data()",
            "",
            "# 2. Split data",
            "X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)",
            "",
            "# 3. Preprocess", 
            "scaler = StandardScaler()",
            "X_train_scaled = scaler.fit_transform(X_train)",
            "X_test_scaled = scaler.transform(X_test)",
            "",
            "# 4. Train model",
            "model = RandomForestClassifier()",
            "model.fit(X_train_scaled, y_train)",
            "",
            "# 5. Evaluate",
            "y_pred = model.predict(X_test_scaled)",
            "accuracy = accuracy_score(y_test, y_pred)"
        ],
        
        "QUICK ALGORITHM SELECTION": [
            "# Classification:",
            "LogisticRegression()           # Linear, fast, interpretable",
            "RandomForestClassifier()       # Non-linear, robust, feature importance",  
            "SVC()                         # Non-linear, powerful, memory intensive",
            "GradientBoostingClassifier()   # High performance, prone to overfitting",
            "",
            "# Regression:",
            "LinearRegression()            # Simple, fast, interpretable",
            "RandomForestRegressor()       # Non-linear, robust",
            "SVR()                        # Non-linear, good for small datasets",
            "",
            "# Clustering:",
            "KMeans()                     # Fast, assumes spherical clusters",
            "DBSCAN()                     # Finds arbitrary shapes, handles noise",
            "AgglomerativeClustering()    # Hierarchical, no need to specify k"
        ],
        
        "PERFORMANCE TIPS": [
            "# Use pipelines to prevent data leakage",
            "# Scale features for distance-based algorithms (SVM, KNN, Neural Networks)",
            "# Use cross-validation for reliable performance estimates", 
            "# Start with simple models, then increase complexity",
            "# Use n_jobs=-1 for parallel processing when available",
            "# Consider feature selection for high-dimensional data",
            "# Use appropriate metrics for imbalanced datasets",
            "# Always set random_state for reproducibility"
        ]
    }
    
    for section, content in sections.items():
        print(f"\n{section}:")
        print("-" * len(section))
        for line in content:
            print(f"   {line}")

def main():
    """Main function to demonstrate all scikit-learn concepts."""
    print("SCIKIT-LEARN COMPREHENSIVE GUIDE")
    print("=" * 70)
    print("This module covers all major aspects of scikit-learn for AI/ML")
    print("To run actual code, install: pip install scikit-learn numpy pandas matplotlib")
    
    demonstrate_sklearn_concepts()
    SklearnDataPreprocessing.preprocessing_examples()
    SklearnSupervisedLearning.classification_examples()
    SklearnSupervisedLearning.regression_examples()
    SklearnUnsupervisedLearning.clustering_examples()
    SklearnUnsupervisedLearning.dimensionality_reduction_examples()
    SklearnModelEvaluation.evaluation_metrics()
    SklearnModelEvaluation.cross_validation_examples()
    SklearnPipelinesAndAutomation.pipeline_examples()
    SklearnPipelinesAndAutomation.hyperparameter_tuning()
    SklearnAdvancedFeatures.custom_estimators()
    SklearnAdvancedFeatures.advanced_techniques()
    create_sklearn_cheat_sheet()
    
    print(f"\n{'='*70}")
    print("NEXT STEPS:")
    print("1. Install scikit-learn: pip install scikit-learn")
    print("2. Practice with real datasets from sklearn.datasets")
    print("3. Explore advanced topics like ensemble methods and neural networks")
    print("4. Check out scikit-learn documentation: https://scikit-learn.org/")
    print("5. Try Kaggle competitions to apply your knowledge")

if __name__ == "__main__":
    main()
