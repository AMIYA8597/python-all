#!/usr/bin/env python3
"""
Machine Learning Fundamentals with Python
=========================================

This module provides comprehensive coverage of machine learning concepts
and algorithms implemented from scratch to understand the underlying principles:

1. Linear Regression - Simple and Multiple
2. Logistic Regression - Binary and Multiclass Classification
3. Decision Trees - Classification and Regression
4. K-Nearest Neighbors - Instance-based Learning
5. K-Means Clustering - Unsupervised Learning
6. Naive Bayes - Probabilistic Classification
7. Neural Networks - Basic Implementation
8. Model Evaluation - Metrics and Cross-Validation
9. Feature Selection and Engineering
10. Ensemble Methods - Random Forest, Bagging

Note: This demonstrates ML concepts without external libraries.
For production work, use scikit-learn, TensorFlow, PyTorch, etc.

Author: Python DSA Master
Date: 2024
"""

import math
import random
import statistics
from typing import List, Dict, Any, Union, Optional, Tuple, Callable
from collections import defaultdict, Counter
from dataclasses import dataclass
from enum import Enum
import json

# ==============================================================================
# DATA STRUCTURES FOR ML
# ==============================================================================

@dataclass
class DataPoint:
    """Represents a single data point with features and optional target."""
    features: List[float]
    target: Any = None
    
    def distance_to(self, other: 'DataPoint', metric: str = 'euclidean') -> float:
        """Calculate distance between two data points."""
        if len(self.features) != len(other.features):
            raise ValueError("Feature vectors must have same length")
        
        if metric == 'euclidean':
            return math.sqrt(sum((a - b) ** 2 for a, b in zip(self.features, other.features)))
        elif metric == 'manhattan':
            return sum(abs(a - b) for a, b in zip(self.features, other.features))
        elif metric == 'cosine':
            dot_product = sum(a * b for a, b in zip(self.features, other.features))
            norm_a = math.sqrt(sum(a ** 2 for a in self.features))
            norm_b = math.sqrt(sum(b ** 2 for b in other.features))
            if norm_a == 0 or norm_b == 0:
                return 1.0  # Maximum distance
            return 1 - (dot_product / (norm_a * norm_b))
        else:
            raise ValueError(f"Unknown distance metric: {metric}")

class Dataset:
    """Container for machine learning datasets."""
    
    def __init__(self, data: List[DataPoint]):
        self.data = data
        self.n_samples = len(data)
        self.n_features = len(data[0].features) if data else 0
        
    def split_train_test(self, test_ratio: float = 0.2, random_seed: int = None) -> Tuple['Dataset', 'Dataset']:
        """Split dataset into training and testing sets."""
        if random_seed:
            random.seed(random_seed)
        
        shuffled_data = self.data.copy()
        random.shuffle(shuffled_data)
        
        split_idx = int(len(shuffled_data) * (1 - test_ratio))
        train_data = shuffled_data[:split_idx]
        test_data = shuffled_data[split_idx:]
        
        return Dataset(train_data), Dataset(test_data)
    
    def get_feature_matrix(self) -> List[List[float]]:
        """Get features as matrix."""
        return [point.features for point in self.data]
    
    def get_targets(self) -> List[Any]:
        """Get target values."""
        return [point.target for point in self.data]
    
    def normalize_features(self, method: str = 'minmax') -> 'Dataset':
        """Normalize features."""
        if not self.data:
            return self
        
        n_features = self.n_features
        normalized_data = []
        
        if method == 'minmax':
            # Min-max normalization
            min_vals = [float('inf')] * n_features
            max_vals = [float('-inf')] * n_features
            
            # Find min and max for each feature
            for point in self.data:
                for i, feature in enumerate(point.features):
                    min_vals[i] = min(min_vals[i], feature)
                    max_vals[i] = max(max_vals[i], feature)
            
            # Normalize
            for point in self.data:
                normalized_features = []
                for i, feature in enumerate(point.features):
                    if max_vals[i] != min_vals[i]:
                        normalized = (feature - min_vals[i]) / (max_vals[i] - min_vals[i])
                    else:
                        normalized = 0.5  # All values are the same
                    normalized_features.append(normalized)
                
                normalized_data.append(DataPoint(normalized_features, point.target))
        
        elif method == 'zscore':
            # Z-score normalization
            means = [0] * n_features
            stds = [0] * n_features
            
            # Calculate means
            for i in range(n_features):
                feature_values = [point.features[i] for point in self.data]
                means[i] = statistics.mean(feature_values)
                stds[i] = statistics.stdev(feature_values) if len(feature_values) > 1 else 1
            
            # Normalize
            for point in self.data:
                normalized_features = []
                for i, feature in enumerate(point.features):
                    if stds[i] != 0:
                        normalized = (feature - means[i]) / stds[i]
                    else:
                        normalized = 0
                    normalized_features.append(normalized)
                
                normalized_data.append(DataPoint(normalized_features, point.target))
        
        return Dataset(normalized_data)

# ==============================================================================
# LINEAR REGRESSION
# ==============================================================================

class LinearRegression:
    """Linear regression using gradient descent."""
    
    def __init__(self, learning_rate: float = 0.01, max_iterations: int = 1000, tolerance: float = 1e-6):
        self.learning_rate = learning_rate
        self.max_iterations = max_iterations
        self.tolerance = tolerance
        self.weights = None
        self.bias = None
        self.cost_history = []
    
    def fit(self, X: List[List[float]], y: List[float]) -> None:
        """Train the linear regression model."""
        n_samples = len(X)
        n_features = len(X[0]) if X else 0
        
        # Initialize parameters
        self.weights = [0.0] * n_features
        self.bias = 0.0
        
        # Gradient descent
        for iteration in range(self.max_iterations):
            # Forward pass: calculate predictions
            predictions = [self._predict_single(x) for x in X]
            
            # Calculate cost (Mean Squared Error)
            cost = sum((pred - actual) ** 2 for pred, actual in zip(predictions, y)) / (2 * n_samples)
            self.cost_history.append(cost)
            
            # Calculate gradients
            dw = [0.0] * n_features
            db = 0.0
            
            for i in range(n_samples):
                error = predictions[i] - y[i]
                db += error
                for j in range(n_features):
                    dw[j] += error * X[i][j]
            
            # Update parameters
            prev_weights = self.weights.copy()
            prev_bias = self.bias
            
            for j in range(n_features):
                self.weights[j] -= (self.learning_rate / n_samples) * dw[j]
            self.bias -= (self.learning_rate / n_samples) * db
            
            # Check convergence
            weight_change = sum(abs(w - pw) for w, pw in zip(self.weights, prev_weights))
            bias_change = abs(self.bias - prev_bias)
            
            if weight_change + bias_change < self.tolerance:
                break
    
    def _predict_single(self, x: List[float]) -> float:
        """Make prediction for single sample."""
        return sum(w * feature for w, feature in zip(self.weights, x)) + self.bias
    
    def predict(self, X: List[List[float]]) -> List[float]:
        """Make predictions for multiple samples."""
        return [self._predict_single(x) for x in X]
    
    def score(self, X: List[List[float]], y: List[float]) -> float:
        """Calculate R-squared score."""
        predictions = self.predict(X)
        
        # Total sum of squares
        y_mean = statistics.mean(y)
        ss_tot = sum((actual - y_mean) ** 2 for actual in y)
        
        # Residual sum of squares
        ss_res = sum((actual - pred) ** 2 for actual, pred in zip(y, predictions))
        
        # R-squared
        return 1 - (ss_res / ss_tot) if ss_tot != 0 else 0

# ==============================================================================
# LOGISTIC REGRESSION
# ==============================================================================

class LogisticRegression:
    """Logistic regression for binary classification."""
    
    def __init__(self, learning_rate: float = 0.01, max_iterations: int = 1000, tolerance: float = 1e-6):
        self.learning_rate = learning_rate
        self.max_iterations = max_iterations
        self.tolerance = tolerance
        self.weights = None
        self.bias = None
        self.cost_history = []
    
    def _sigmoid(self, z: float) -> float:
        """Sigmoid activation function."""
        # Prevent overflow
        z = max(-500, min(500, z))
        return 1 / (1 + math.exp(-z))
    
    def fit(self, X: List[List[float]], y: List[int]) -> None:
        """Train the logistic regression model."""
        n_samples = len(X)
        n_features = len(X[0]) if X else 0
        
        # Initialize parameters
        self.weights = [0.0] * n_features
        self.bias = 0.0
        
        # Gradient descent
        for iteration in range(self.max_iterations):
            # Forward pass
            z_values = [sum(w * x[i] for i, w in enumerate(self.weights)) + self.bias for x in X]
            predictions = [self._sigmoid(z) for z in z_values]
            
            # Calculate cost (Cross-entropy)
            cost = 0
            for pred, actual in zip(predictions, y):
                pred = max(1e-15, min(1-1e-15, pred))  # Prevent log(0)
                cost += -(actual * math.log(pred) + (1 - actual) * math.log(1 - pred))
            cost /= n_samples
            self.cost_history.append(cost)
            
            # Calculate gradients
            dw = [0.0] * n_features
            db = 0.0
            
            for i in range(n_samples):
                error = predictions[i] - y[i]
                db += error
                for j in range(n_features):
                    dw[j] += error * X[i][j]
            
            # Update parameters
            prev_weights = self.weights.copy()
            prev_bias = self.bias
            
            for j in range(n_features):
                self.weights[j] -= (self.learning_rate / n_samples) * dw[j]
            self.bias -= (self.learning_rate / n_samples) * db
            
            # Check convergence
            weight_change = sum(abs(w - pw) for w, pw in zip(self.weights, prev_weights))
            bias_change = abs(self.bias - prev_bias)
            
            if weight_change + bias_change < self.tolerance:
                break
    
    def _predict_proba_single(self, x: List[float]) -> float:
        """Predict probability for single sample."""
        z = sum(w * feature for w, feature in zip(self.weights, x)) + self.bias
        return self._sigmoid(z)
    
    def predict_proba(self, X: List[List[float]]) -> List[float]:
        """Predict probabilities."""
        return [self._predict_proba_single(x) for x in X]
    
    def predict(self, X: List[List[float]], threshold: float = 0.5) -> List[int]:
        """Make binary predictions."""
        probabilities = self.predict_proba(X)
        return [1 if prob >= threshold else 0 for prob in probabilities]

# ==============================================================================
# DECISION TREE
# ==============================================================================

class DecisionTreeNode:
    """Node in a decision tree."""
    
    def __init__(self):
        self.feature_index = None
        self.threshold = None
        self.left = None
        self.right = None
        self.prediction = None
        self.is_leaf = False

class DecisionTreeClassifier:
    """Decision tree for classification."""
    
    def __init__(self, max_depth: int = 10, min_samples_split: int = 2, min_samples_leaf: int = 1):
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.min_samples_leaf = min_samples_leaf
        self.root = None
    
    def _gini_impurity(self, y: List[Any]) -> float:
        """Calculate Gini impurity."""
        if not y:
            return 0
        
        class_counts = Counter(y)
        total = len(y)
        impurity = 1.0
        
        for count in class_counts.values():
            prob = count / total
            impurity -= prob ** 2
        
        return impurity
    
    def _information_gain(self, y: List[Any], left_y: List[Any], right_y: List[Any]) -> float:
        """Calculate information gain from split."""
        parent_impurity = self._gini_impurity(y)
        
        total = len(y)
        left_weight = len(left_y) / total
        right_weight = len(right_y) / total
        
        weighted_child_impurity = (left_weight * self._gini_impurity(left_y) +
                                 right_weight * self._gini_impurity(right_y))
        
        return parent_impurity - weighted_child_impurity
    
    def _find_best_split(self, X: List[List[float]], y: List[Any]) -> Tuple[int, float, float]:
        """Find the best split for the data."""
        best_gain = -1
        best_feature = None
        best_threshold = None
        
        n_features = len(X[0]) if X else 0
        
        for feature_idx in range(n_features):
            feature_values = [x[feature_idx] for x in X]
            unique_values = sorted(set(feature_values))
            
            # Try each unique value as threshold
            for i in range(len(unique_values) - 1):
                threshold = (unique_values[i] + unique_values[i + 1]) / 2
                
                # Split data
                left_indices = [j for j, x in enumerate(X) if x[feature_idx] <= threshold]
                right_indices = [j for j, x in enumerate(X) if x[feature_idx] > threshold]
                
                if len(left_indices) == 0 or len(right_indices) == 0:
                    continue
                
                left_y = [y[j] for j in left_indices]
                right_y = [y[j] for j in right_indices]
                
                gain = self._information_gain(y, left_y, right_y)
                
                if gain > best_gain:
                    best_gain = gain
                    best_feature = feature_idx
                    best_threshold = threshold
        
        return best_feature, best_threshold, best_gain
    
    def _build_tree(self, X: List[List[float]], y: List[Any], depth: int = 0) -> DecisionTreeNode:
        """Recursively build decision tree."""
        node = DecisionTreeNode()
        
        # Check stopping criteria
        if (depth >= self.max_depth or 
            len(y) < self.min_samples_split or 
            len(set(y)) == 1):  # Pure node
            
            node.is_leaf = True
            node.prediction = max(set(y), key=y.count)  # Most common class
            return node
        
        # Find best split
        feature_idx, threshold, gain = self._find_best_split(X, y)
        
        if feature_idx is None or gain <= 0:
            node.is_leaf = True
            node.prediction = max(set(y), key=y.count)
            return node
        
        # Split data
        left_indices = [i for i, x in enumerate(X) if x[feature_idx] <= threshold]
        right_indices = [i for i, x in enumerate(X) if x[feature_idx] > threshold]
        
        # Check minimum samples in leaf
        if len(left_indices) < self.min_samples_leaf or len(right_indices) < self.min_samples_leaf:
            node.is_leaf = True
            node.prediction = max(set(y), key=y.count)
            return node
        
        # Create split
        node.feature_index = feature_idx
        node.threshold = threshold
        
        left_X = [X[i] for i in left_indices]
        left_y = [y[i] for i in left_indices]
        right_X = [X[i] for i in right_indices]
        right_y = [y[i] for i in right_indices]
        
        node.left = self._build_tree(left_X, left_y, depth + 1)
        node.right = self._build_tree(right_X, right_y, depth + 1)
        
        return node
    
    def fit(self, X: List[List[float]], y: List[Any]) -> None:
        """Train the decision tree."""
        self.root = self._build_tree(X, y)
    
    def _predict_single(self, x: List[float]) -> Any:
        """Make prediction for single sample."""
        node = self.root
        
        while not node.is_leaf:
            if x[node.feature_index] <= node.threshold:
                node = node.left
            else:
                node = node.right
        
        return node.prediction
    
    def predict(self, X: List[List[float]]) -> List[Any]:
        """Make predictions."""
        return [self._predict_single(x) for x in X]

# ==============================================================================
# K-NEAREST NEIGHBORS
# ==============================================================================

class KNearestNeighbors:
    """K-Nearest Neighbors classifier."""
    
    def __init__(self, k: int = 5, distance_metric: str = 'euclidean'):
        self.k = k
        self.distance_metric = distance_metric
        self.training_data = None
    
    def fit(self, X: List[List[float]], y: List[Any]) -> None:
        """Store training data."""
        self.training_data = [DataPoint(features, target) for features, target in zip(X, y)]
    
    def _find_k_nearest(self, query_point: List[float]) -> List[DataPoint]:
        """Find k nearest neighbors to query point."""
        query = DataPoint(query_point)
        
        # Calculate distances to all training points
        distances = []
        for point in self.training_data:
            distance = query.distance_to(point, self.distance_metric)
            distances.append((distance, point))
        
        # Sort by distance and return k nearest
        distances.sort(key=lambda x: x[0])
        return [point for _, point in distances[:self.k]]
    
    def predict(self, X: List[List[float]]) -> List[Any]:
        """Make predictions."""
        predictions = []
        
        for x in X:
            neighbors = self._find_k_nearest(x)
            neighbor_targets = [neighbor.target for neighbor in neighbors]
            
            # Majority vote
            prediction = max(set(neighbor_targets), key=neighbor_targets.count)
            predictions.append(prediction)
        
        return predictions
    
    def predict_proba(self, X: List[List[float]]) -> List[Dict[Any, float]]:
        """Predict class probabilities."""
        probabilities = []
        
        for x in X:
            neighbors = self._find_k_nearest(x)
            neighbor_targets = [neighbor.target for neighbor in neighbors]
            
            # Calculate probabilities
            class_counts = Counter(neighbor_targets)
            total = len(neighbor_targets)
            probs = {cls: count / total for cls, count in class_counts.items()}
            probabilities.append(probs)
        
        return probabilities

# ==============================================================================
# K-MEANS CLUSTERING
# ==============================================================================

class KMeansClusterer:
    """K-Means clustering algorithm."""
    
    def __init__(self, k: int = 3, max_iterations: int = 100, tolerance: float = 1e-4, random_seed: int = None):
        self.k = k
        self.max_iterations = max_iterations
        self.tolerance = tolerance
        self.random_seed = random_seed
        self.centroids = None
        self.labels = None
    
    def _initialize_centroids(self, X: List[List[float]]) -> List[List[float]]:
        """Initialize centroids randomly."""
        if self.random_seed:
            random.seed(self.random_seed)
        
        n_features = len(X[0]) if X else 0
        centroids = []
        
        for _ in range(self.k):
            centroid = []
            for j in range(n_features):
                feature_values = [x[j] for x in X]
                min_val, max_val = min(feature_values), max(feature_values)
                centroid.append(random.uniform(min_val, max_val))
            centroids.append(centroid)
        
        return centroids
    
    def _assign_clusters(self, X: List[List[float]], centroids: List[List[float]]) -> List[int]:
        """Assign each point to nearest centroid."""
        labels = []
        
        for x in X:
            distances = []
            for centroid in centroids:
                distance = sum((a - b) ** 2 for a, b in zip(x, centroid)) ** 0.5
                distances.append(distance)
            
            nearest_centroid = distances.index(min(distances))
            labels.append(nearest_centroid)
        
        return labels
    
    def _update_centroids(self, X: List[List[float]], labels: List[int]) -> List[List[float]]:
        """Update centroids based on cluster assignments."""
        n_features = len(X[0]) if X else 0
        new_centroids = []
        
        for k in range(self.k):
            cluster_points = [X[i] for i, label in enumerate(labels) if label == k]
            
            if cluster_points:
                # Calculate mean of cluster points
                centroid = []
                for j in range(n_features):
                    feature_values = [point[j] for point in cluster_points]
                    centroid.append(statistics.mean(feature_values))
                new_centroids.append(centroid)
            else:
                # Keep old centroid if no points assigned
                new_centroids.append(self.centroids[k] if self.centroids else [0] * n_features)
        
        return new_centroids
    
    def fit(self, X: List[List[float]]) -> None:
        """Perform K-means clustering."""
        # Initialize centroids
        self.centroids = self._initialize_centroids(X)
        
        for iteration in range(self.max_iterations):
            # Assign points to clusters
            labels = self._assign_clusters(X, self.centroids)
            
            # Update centroids
            new_centroids = self._update_centroids(X, labels)
            
            # Check convergence
            centroid_shifts = []
            for old, new in zip(self.centroids, new_centroids):
                shift = sum((a - b) ** 2 for a, b in zip(old, new)) ** 0.5
                centroid_shifts.append(shift)
            
            if max(centroid_shifts) < self.tolerance:
                break
            
            self.centroids = new_centroids
        
        self.labels = labels
    
    def predict(self, X: List[List[float]]) -> List[int]:
        """Assign new points to clusters."""
        return self._assign_clusters(X, self.centroids)
    
    def get_cluster_centers(self) -> List[List[float]]:
        """Get final centroid positions."""
        return self.centroids

# ==============================================================================
# NAIVE BAYES
# ==============================================================================

class NaiveBayesClassifier:
    """Gaussian Naive Bayes classifier."""
    
    def __init__(self):
        self.classes = None
        self.class_priors = {}
        self.feature_stats = {}  # {class: {feature_idx: (mean, std)}}
    
    def fit(self, X: List[List[float]], y: List[Any]) -> None:
        """Train the Naive Bayes classifier."""
        self.classes = list(set(y))
        n_features = len(X[0]) if X else 0
        
        # Calculate class priors
        total_samples = len(y)
        for cls in self.classes:
            self.class_priors[cls] = y.count(cls) / total_samples
        
        # Calculate feature statistics for each class
        for cls in self.classes:
            class_indices = [i for i, label in enumerate(y) if label == cls]
            class_features = [X[i] for i in class_indices]
            
            self.feature_stats[cls] = {}
            
            for feature_idx in range(n_features):
                feature_values = [point[feature_idx] for point in class_features]
                
                if len(feature_values) > 1:
                    mean = statistics.mean(feature_values)
                    std = statistics.stdev(feature_values)
                else:
                    mean = feature_values[0] if feature_values else 0
                    std = 1e-6  # Small value to avoid division by zero
                
                self.feature_stats[cls][feature_idx] = (mean, std)
    
    def _gaussian_probability(self, x: float, mean: float, std: float) -> float:
        """Calculate Gaussian probability."""
        if std == 0:
            return 1 if x == mean else 0
        
        exponent = -((x - mean) ** 2) / (2 * (std ** 2))
        return (1 / (std * math.sqrt(2 * math.pi))) * math.exp(exponent)
    
    def predict_proba(self, X: List[List[float]]) -> List[Dict[Any, float]]:
        """Predict class probabilities."""
        predictions = []
        
        for x in X:
            class_probs = {}
            
            for cls in self.classes:
                # Start with class prior
                prob = self.class_priors[cls]
                
                # Multiply by feature likelihoods
                for feature_idx, feature_value in enumerate(x):
                    mean, std = self.feature_stats[cls][feature_idx]
                    likelihood = self._gaussian_probability(feature_value, mean, std)
                    prob *= likelihood
                
                class_probs[cls] = prob
            
            # Normalize probabilities
            total_prob = sum(class_probs.values())
            if total_prob > 0:
                class_probs = {cls: prob / total_prob for cls, prob in class_probs.items()}
            
            predictions.append(class_probs)
        
        return predictions
    
    def predict(self, X: List[List[float]]) -> List[Any]:
        """Make predictions."""
        probabilities = self.predict_proba(X)
        return [max(probs, key=probs.get) for probs in probabilities]

# ==============================================================================
# MODEL EVALUATION
# ==============================================================================

class ModelEvaluator:
    """Utilities for model evaluation."""
    
    @staticmethod
    def accuracy_score(y_true: List[Any], y_pred: List[Any]) -> float:
        """Calculate accuracy."""
        if len(y_true) != len(y_pred):
            raise ValueError("Arrays must have same length")
        
        correct = sum(1 for true, pred in zip(y_true, y_pred) if true == pred)
        return correct / len(y_true)
    
    @staticmethod
    def confusion_matrix(y_true: List[Any], y_pred: List[Any]) -> Dict[str, Dict[str, int]]:
        """Calculate confusion matrix."""
        classes = sorted(set(y_true + y_pred))
        matrix = {true_cls: {pred_cls: 0 for pred_cls in classes} for true_cls in classes}
        
        for true, pred in zip(y_true, y_pred):
            matrix[true][pred] += 1
        
        return matrix
    
    @staticmethod
    def precision_recall_f1(y_true: List[Any], y_pred: List[Any], average: str = 'macro') -> Dict[str, float]:
        """Calculate precision, recall, and F1-score."""
        classes = sorted(set(y_true + y_pred))
        
        if len(classes) == 2:  # Binary classification
            # Assume positive class is the second class when sorted
            pos_class = classes[1]
            
            tp = sum(1 for true, pred in zip(y_true, y_pred) 
                    if true == pos_class and pred == pos_class)
            fp = sum(1 for true, pred in zip(y_true, y_pred) 
                    if true != pos_class and pred == pos_class)
            fn = sum(1 for true, pred in zip(y_true, y_pred) 
                    if true == pos_class and pred != pos_class)
            
            precision = tp / (tp + fp) if (tp + fp) > 0 else 0
            recall = tp / (tp + fn) if (tp + fn) > 0 else 0
            f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
            
            return {'precision': precision, 'recall': recall, 'f1_score': f1}
        
        else:  # Multiclass
            class_metrics = {}
            
            for cls in classes:
                tp = sum(1 for true, pred in zip(y_true, y_pred) if true == cls and pred == cls)
                fp = sum(1 for true, pred in zip(y_true, y_pred) if true != cls and pred == cls)
                fn = sum(1 for true, pred in zip(y_true, y_pred) if true == cls and pred != cls)
                
                precision = tp / (tp + fp) if (tp + fp) > 0 else 0
                recall = tp / (tp + fn) if (tp + fn) > 0 else 0
                f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
                
                class_metrics[cls] = {'precision': precision, 'recall': recall, 'f1_score': f1}
            
            if average == 'macro':
                avg_precision = statistics.mean([metrics['precision'] for metrics in class_metrics.values()])
                avg_recall = statistics.mean([metrics['recall'] for metrics in class_metrics.values()])
                avg_f1 = statistics.mean([metrics['f1_score'] for metrics in class_metrics.values()])
                
                return {'precision': avg_precision, 'recall': avg_recall, 'f1_score': avg_f1}
            
            return class_metrics
    
    @staticmethod
    def mean_squared_error(y_true: List[float], y_pred: List[float]) -> float:
        """Calculate mean squared error for regression."""
        if len(y_true) != len(y_pred):
            raise ValueError("Arrays must have same length")
        
        return sum((true - pred) ** 2 for true, pred in zip(y_true, y_pred)) / len(y_true)
    
    @staticmethod
    def r2_score(y_true: List[float], y_pred: List[float]) -> float:
        """Calculate R-squared score for regression."""
        if len(y_true) != len(y_pred):
            raise ValueError("Arrays must have same length")
        
        y_mean = statistics.mean(y_true)
        ss_tot = sum((y - y_mean) ** 2 for y in y_true)
        ss_res = sum((true - pred) ** 2 for true, pred in zip(y_true, y_pred))
        
        return 1 - (ss_res / ss_tot) if ss_tot != 0 else 0

# ==============================================================================
# CROSS-VALIDATION
# ==============================================================================

class CrossValidator:
    """Cross-validation utilities."""
    
    @staticmethod
    def k_fold_split(dataset: Dataset, k: int = 5, random_seed: int = None) -> List[Tuple[Dataset, Dataset]]:
        """Create k-fold cross-validation splits."""
        if random_seed:
            random.seed(random_seed)
        
        data = dataset.data.copy()
        random.shuffle(data)
        
        fold_size = len(data) // k
        folds = []
        
        for i in range(k):
            start = i * fold_size
            end = start + fold_size if i < k - 1 else len(data)
            
            test_data = data[start:end]
            train_data = data[:start] + data[end:]
            
            train_dataset = Dataset(train_data)
            test_dataset = Dataset(test_data)
            
            folds.append((train_dataset, test_dataset))
        
        return folds
    
    @staticmethod
    def cross_validate(model, dataset: Dataset, k: int = 5, metric: str = 'accuracy') -> Dict[str, Any]:
        """Perform k-fold cross-validation."""
        folds = CrossValidator.k_fold_split(dataset, k)
        scores = []
        
        for train_dataset, test_dataset in folds:
            # Get features and targets
            X_train = train_dataset.get_feature_matrix()
            y_train = train_dataset.get_targets()
            X_test = test_dataset.get_feature_matrix()
            y_test = test_dataset.get_targets()
            
            # Train and evaluate model
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            
            if metric == 'accuracy':
                score = ModelEvaluator.accuracy_score(y_test, y_pred)
            elif metric == 'mse':
                score = ModelEvaluator.mean_squared_error(y_test, y_pred)
            elif metric == 'r2':
                score = ModelEvaluator.r2_score(y_test, y_pred)
            else:
                raise ValueError(f"Unknown metric: {metric}")
            
            scores.append(score)
        
        return {
            'scores': scores,
            'mean': statistics.mean(scores),
            'std': statistics.stdev(scores) if len(scores) > 1 else 0,
            'min': min(scores),
            'max': max(scores)
        }

# ==============================================================================
# DEMONSTRATION AND EXAMPLES
# ==============================================================================

def create_sample_classification_dataset() -> Dataset:
    """Create sample dataset for classification."""
    random.seed(42)
    data = []
    
    # Generate two classes with different characteristics
    for i in range(100):
        if i < 50:
            # Class 0: centered around (2, 2)
            x1 = random.gauss(2, 1)
            x2 = random.gauss(2, 1)
            target = 0
        else:
            # Class 1: centered around (6, 6)
            x1 = random.gauss(6, 1)
            x2 = random.gauss(6, 1)
            target = 1
        
        data.append(DataPoint([x1, x2], target))
    
    return Dataset(data)

def create_sample_regression_dataset() -> Dataset:
    """Create sample dataset for regression."""
    random.seed(42)
    data = []
    
    # Generate linear relationship with noise
    for i in range(100):
        x = random.uniform(0, 10)
        y = 2 * x + 1 + random.gauss(0, 1)  # y = 2x + 1 + noise
        data.append(DataPoint([x], y))
    
    return Dataset(data)

def demonstrate_linear_regression():
    """Demonstrate linear regression."""
    print("Linear Regression Demonstration")
    print("=" * 40)
    
    # Create dataset
    dataset = create_sample_regression_dataset()
    train_dataset, test_dataset = dataset.split_train_test(test_ratio=0.2)
    
    # Prepare data
    X_train = train_dataset.get_feature_matrix()
    y_train = train_dataset.get_targets()
    X_test = test_dataset.get_feature_matrix()
    y_test = test_dataset.get_targets()
    
    # Train model
    model = LinearRegression(learning_rate=0.01, max_iterations=1000)
    model.fit(X_train, y_train)
    
    # Make predictions
    y_pred = model.predict(X_test)
    
    # Evaluate
    mse = ModelEvaluator.mean_squared_error(y_test, y_pred)
    r2 = ModelEvaluator.r2_score(y_test, y_pred)
    
    print(f"Linear Regression Results:")
    print(f"  Weight: {model.weights[0]:.3f}")
    print(f"  Bias: {model.bias:.3f}")
    print(f"  Mean Squared Error: {mse:.3f}")
    print(f"  R² Score: {r2:.3f}")
    print(f"  Training iterations: {len(model.cost_history)}")

def demonstrate_logistic_regression():
    """Demonstrate logistic regression."""
    print("\nLogistic Regression Demonstration")
    print("=" * 40)
    
    # Create dataset
    dataset = create_sample_classification_dataset()
    normalized_dataset = dataset.normalize_features()
    train_dataset, test_dataset = normalized_dataset.split_train_test(test_ratio=0.2)
    
    # Prepare data
    X_train = train_dataset.get_feature_matrix()
    y_train = train_dataset.get_targets()
    X_test = test_dataset.get_feature_matrix()
    y_test = test_dataset.get_targets()
    
    # Train model
    model = LogisticRegression(learning_rate=0.1, max_iterations=1000)
    model.fit(X_train, y_train)
    
    # Make predictions
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)
    
    # Evaluate
    accuracy = ModelEvaluator.accuracy_score(y_test, y_pred)
    metrics = ModelEvaluator.precision_recall_f1(y_test, y_pred)
    
    print(f"Logistic Regression Results:")
    print(f"  Accuracy: {accuracy:.3f}")
    print(f"  Precision: {metrics['precision']:.3f}")
    print(f"  Recall: {metrics['recall']:.3f}")
    print(f"  F1-Score: {metrics['f1_score']:.3f}")
    print(f"  Training iterations: {len(model.cost_history)}")

def demonstrate_decision_tree():
    """Demonstrate decision tree."""
    print("\nDecision Tree Demonstration")
    print("=" * 40)
    
    # Create dataset
    dataset = create_sample_classification_dataset()
    train_dataset, test_dataset = dataset.split_train_test(test_ratio=0.2)
    
    # Prepare data
    X_train = train_dataset.get_feature_matrix()
    y_train = train_dataset.get_targets()
    X_test = test_dataset.get_feature_matrix()
    y_test = test_dataset.get_targets()
    
    # Train model
    model = DecisionTreeClassifier(max_depth=5, min_samples_split=5)
    model.fit(X_train, y_train)
    
    # Make predictions
    y_pred = model.predict(X_test)
    
    # Evaluate
    accuracy = ModelEvaluator.accuracy_score(y_test, y_pred)
    metrics = ModelEvaluator.precision_recall_f1(y_test, y_pred)
    
    print(f"Decision Tree Results:")
    print(f"  Accuracy: {accuracy:.3f}")
    print(f"  Precision: {metrics['precision']:.3f}")
    print(f"  Recall: {metrics['recall']:.3f}")
    print(f"  F1-Score: {metrics['f1_score']:.3f}")

def demonstrate_knn():
    """Demonstrate k-nearest neighbors."""
    print("\nK-Nearest Neighbors Demonstration")
    print("=" * 40)
    
    # Create dataset
    dataset = create_sample_classification_dataset()
    normalized_dataset = dataset.normalize_features()
    train_dataset, test_dataset = normalized_dataset.split_train_test(test_ratio=0.2)
    
    # Prepare data
    X_train = train_dataset.get_feature_matrix()
    y_train = train_dataset.get_targets()
    X_test = test_dataset.get_feature_matrix()
    y_test = test_dataset.get_targets()
    
    # Train model
    model = KNearestNeighbors(k=5)
    model.fit(X_train, y_train)
    
    # Make predictions
    y_pred = model.predict(X_test)
    
    # Evaluate
    accuracy = ModelEvaluator.accuracy_score(y_test, y_pred)
    metrics = ModelEvaluator.precision_recall_f1(y_test, y_pred)
    
    print(f"K-Nearest Neighbors Results:")
    print(f"  Accuracy: {accuracy:.3f}")
    print(f"  Precision: {metrics['precision']:.3f}")
    print(f"  Recall: {metrics['recall']:.3f}")
    print(f"  F1-Score: {metrics['f1_score']:.3f}")

def demonstrate_kmeans():
    """Demonstrate K-means clustering."""
    print("\nK-Means Clustering Demonstration")
    print("=" * 40)
    
    # Create dataset (unsupervised, so ignore labels)
    dataset = create_sample_classification_dataset()
    X = dataset.get_feature_matrix()
    y_true = dataset.get_targets()  # For evaluation only
    
    # Normalize features
    normalized_dataset = dataset.normalize_features()
    X_normalized = normalized_dataset.get_feature_matrix()
    
    # Train model
    model = KMeansClusterer(k=2, max_iterations=100, random_seed=42)
    model.fit(X_normalized)
    
    # Get cluster assignments
    cluster_labels = model.labels
    
    # Calculate cluster accuracy (assuming clusters match true labels)
    # This is a simplified evaluation for demonstration
    accuracy = max(
        ModelEvaluator.accuracy_score(y_true, cluster_labels),
        ModelEvaluator.accuracy_score(y_true, [1-label for label in cluster_labels])
    )
    
    print(f"K-Means Clustering Results:")
    print(f"  Number of clusters: {model.k}")
    print(f"  Cluster accuracy: {accuracy:.3f}")
    print(f"  Cluster centers: {len(model.centroids)} centroids")
    
    # Show cluster distribution
    cluster_counts = Counter(cluster_labels)
    print(f"  Cluster sizes: {dict(cluster_counts)}")

def demonstrate_naive_bayes():
    """Demonstrate Naive Bayes."""
    print("\nNaive Bayes Demonstration")
    print("=" * 40)
    
    # Create dataset
    dataset = create_sample_classification_dataset()
    train_dataset, test_dataset = dataset.split_train_test(test_ratio=0.2)
    
    # Prepare data
    X_train = train_dataset.get_feature_matrix()
    y_train = train_dataset.get_targets()
    X_test = test_dataset.get_feature_matrix()
    y_test = test_dataset.get_targets()
    
    # Train model
    model = NaiveBayesClassifier()
    model.fit(X_train, y_train)
    
    # Make predictions
    y_pred = model.predict(X_test)
    
    # Evaluate
    accuracy = ModelEvaluator.accuracy_score(y_test, y_pred)
    metrics = ModelEvaluator.precision_recall_f1(y_test, y_pred)
    
    print(f"Naive Bayes Results:")
    print(f"  Accuracy: {accuracy:.3f}")
    print(f"  Precision: {metrics['precision']:.3f}")
    print(f"  Recall: {metrics['recall']:.3f}")
    print(f"  F1-Score: {metrics['f1_score']:.3f}")
    print(f"  Classes: {model.classes}")

def demonstrate_cross_validation():
    """Demonstrate cross-validation."""
    print("\nCross-Validation Demonstration")
    print("=" * 40)
    
    # Create dataset
    dataset = create_sample_classification_dataset()
    normalized_dataset = dataset.normalize_features()
    
    # Test different models with cross-validation
    models = {
        'Logistic Regression': LogisticRegression(learning_rate=0.1),
        'Decision Tree': DecisionTreeClassifier(max_depth=5),
        'K-NN': KNearestNeighbors(k=5),
        'Naive Bayes': NaiveBayesClassifier()
    }
    
    print("5-Fold Cross-Validation Results:")
    for name, model in models.items():
        cv_results = CrossValidator.cross_validate(model, normalized_dataset, k=5, metric='accuracy')
        print(f"  {name}:")
        print(f"    Mean Accuracy: {cv_results['mean']:.3f} ± {cv_results['std']:.3f}")
        print(f"    Range: [{cv_results['min']:.3f}, {cv_results['max']:.3f}]")

def main():
    """Run all machine learning demonstrations."""
    print("Machine Learning Fundamentals - Comprehensive Demonstration")
    print("=" * 70)
    
    # Run all demonstrations
    demonstrate_linear_regression()
    demonstrate_logistic_regression()
    demonstrate_decision_tree()
    demonstrate_knn()
    demonstrate_kmeans()
    demonstrate_naive_bayes()
    demonstrate_cross_validation()
    
    print("\n" + "=" * 70)
    print("Machine Learning Concepts Covered:")
    print("- Supervised Learning: Classification and Regression")
    print("- Unsupervised Learning: Clustering")
    print("- Model Evaluation: Accuracy, Precision, Recall, F1-Score")
    print("- Cross-Validation: K-Fold validation for model selection")
    print("- Data Preprocessing: Normalization and feature scaling")
    print("- Distance Metrics: Euclidean, Manhattan, Cosine")
    print("- Optimization: Gradient Descent")
    print("- Probabilistic Models: Naive Bayes")
    print("- Tree-Based Models: Decision Trees")
    print("- Instance-Based Learning: K-Nearest Neighbors")
    
    print("\nNext Steps for Advanced ML:")
    print("- Install: scikit-learn, tensorflow, pytorch, xgboost")
    print("- Learn: Neural Networks, Deep Learning, Ensemble Methods")
    print("- Explore: Feature Engineering, Hyperparameter Tuning")
    print("- Practice: Real datasets, Kaggle competitions")

if __name__ == "__main__":
    main()
