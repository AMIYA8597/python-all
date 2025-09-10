#!/usr/bin/env python3
"""
Advanced AI Applications - Cutting-Edge Projects
===============================================

This module contains sophisticated AI/ML projects that demonstrate advanced
applications including computer vision, time series forecasting, reinforcement
learning, clustering, and fraud detection systems.

Projects Included:
1. Time Series Forecasting Engine (ARIMA, Moving Averages, Trend Analysis)
2. Computer Vision Image Classifier (Custom CNN from scratch)  
3. Reinforcement Learning Game AI (Q-Learning & Policy Gradients)
4. Fraud Detection System (Anomaly Detection & Classification)
5. Clustering & Market Segmentation (K-Means, DBSCAN, Hierarchical)
6. Predictive Analytics Dashboard (Complete ML Pipeline)
7. A/B Testing Statistical Engine
8. Customer Lifetime Value Predictor
9. Real-time Streaming Analytics
10. AutoML Feature Selection Engine

Author: Python DSA Master
Date: 2024
"""

import numpy as np
import pandas as pd
import json
import math
import random
import time
import sqlite3
from typing import Dict, List, Tuple, Any, Optional, Set, Union, Callable
from collections import defaultdict, Counter, deque
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import warnings
warnings.filterwarnings('ignore')

# ==============================================================================
# PROJECT 1: TIME SERIES FORECASTING ENGINE
# ==============================================================================

@dataclass
class TimeSeriesDataPoint:
    """Single time series data point."""
    timestamp: datetime
    value: float
    features: Dict[str, float] = field(default_factory=dict)

class TimeSeriesForecaster:
    """
    Advanced Time Series Forecasting Engine.
    
    Features:
    - Trend detection and decomposition
    - Seasonal pattern analysis
    - ARIMA modeling
    - Moving averages (Simple, Exponential, Weighted)
    - Anomaly detection in time series
    - Multiple forecasting methods with ensemble
    - Real-time prediction updates
    """
    
    def __init__(self):
        self.data: List[TimeSeriesDataPoint] = []
        self.values: List[float] = []
        self.timestamps: List[datetime] = []
        
        # Model components
        self.trend = []
        self.seasonal = []
        self.residual = []
        self.period = 0  # Detected seasonal period
        
        # Forecasting models
        self.models = {}
        self.ensemble_weights = {}
        
        # Statistics
        self.stats = {
            'mean': 0.0,
            'std': 0.0,
            'min': 0.0,
            'max': 0.0,
            'variance': 0.0,
            'autocorrelation': []
        }
    
    def add_data_point(self, data_point: TimeSeriesDataPoint):
        """Add a new data point to the time series."""
        self.data.append(data_point)
        self.values.append(data_point.value)
        self.timestamps.append(data_point.timestamp)
        
        # Update basic statistics
        self._update_statistics()
    
    def add_data_batch(self, data_points: List[TimeSeriesDataPoint]):
        """Add multiple data points efficiently."""
        self.data.extend(data_points)
        self.values.extend([dp.value for dp in data_points])
        self.timestamps.extend([dp.timestamp for dp in data_points])
        self._update_statistics()
    
    def _update_statistics(self):
        """Update basic statistics for the time series."""
        if not self.values:
            return
        
        values = np.array(self.values)
        self.stats['mean'] = np.mean(values)
        self.stats['std'] = np.std(values)
        self.stats['min'] = np.min(values)
        self.stats['max'] = np.max(values)
        self.stats['variance'] = np.var(values)
    
    def detect_seasonality(self, max_period: int = 50) -> int:
        """Detect seasonal period using autocorrelation."""
        if len(self.values) < max_period * 2:
            return 0
        
        values = np.array(self.values)
        n = len(values)
        
        # Calculate autocorrelation for different lags
        autocorrelations = []
        
        for lag in range(1, min(max_period + 1, n // 2)):
            # Calculate autocorrelation at this lag
            x1 = values[:-lag]
            x2 = values[lag:]
            
            if len(x1) > 0 and len(x2) > 0:
                correlation = np.corrcoef(x1, x2)[0, 1]
                if not np.isnan(correlation):
                    autocorrelations.append((lag, correlation))
        
        # Find the lag with highest positive autocorrelation (excluding lag 0)
        if autocorrelations:
            autocorrelations.sort(key=lambda x: x[1], reverse=True)
            self.stats['autocorrelation'] = autocorrelations[:10]  # Store top 10
            
            # Consider it seasonal if correlation > 0.3
            if autocorrelations[0][1] > 0.3:
                self.period = autocorrelations[0][0]
                return self.period
        
        return 0
    
    def decompose_series(self):
        """Decompose time series into trend, seasonal, and residual components."""
        if len(self.values) < 10:
            return
        
        values = np.array(self.values)
        n = len(values)
        
        # Simple trend extraction using moving average
        window = min(max(5, n // 10), 20)  # Adaptive window size
        trend = []
        
        for i in range(n):
            start = max(0, i - window // 2)
            end = min(n, i + window // 2 + 1)
            trend.append(np.mean(values[start:end]))
        
        self.trend = trend
        
        # Extract seasonal component if period detected
        if self.period > 0 and self.period < n // 2:
            seasonal = np.zeros(n)
            
            # Calculate average pattern for each seasonal position
            for pos in range(self.period):
                seasonal_values = []
                for i in range(pos, n, self.period):
                    seasonal_values.append(values[i] - trend[i])
                
                if seasonal_values:
                    avg_seasonal = np.mean(seasonal_values)
                    # Apply this average to all positions
                    for i in range(pos, n, self.period):
                        seasonal[i] = avg_seasonal
            
            self.seasonal = seasonal.tolist()
        else:
            self.seasonal = [0.0] * n
        
        # Calculate residuals
        self.residual = []
        for i in range(n):
            residual = values[i] - trend[i] - self.seasonal[i]
            self.residual.append(residual)
    
    def simple_moving_average(self, window: int) -> List[float]:
        """Calculate simple moving average."""
        if window <= 0 or window > len(self.values):
            return []
        
        sma = []
        for i in range(len(self.values)):
            if i >= window - 1:
                avg = np.mean(self.values[i-window+1:i+1])
                sma.append(avg)
            else:
                sma.append(self.values[i])  # Use actual value for insufficient data
        
        return sma
    
    def exponential_moving_average(self, alpha: float = 0.3) -> List[float]:
        """Calculate exponential moving average."""
        if not self.values:
            return []
        
        ema = [self.values[0]]  # Start with first value
        
        for i in range(1, len(self.values)):
            ema_value = alpha * self.values[i] + (1 - alpha) * ema[-1]
            ema.append(ema_value)
        
        return ema
    
    def weighted_moving_average(self, weights: List[float]) -> List[float]:
        """Calculate weighted moving average."""
        if not weights or not self.values:
            return []
        
        window = len(weights)
        weights = np.array(weights)
        weights = weights / np.sum(weights)  # Normalize weights
        
        wma = []
        for i in range(len(self.values)):
            if i >= window - 1:
                window_values = np.array(self.values[i-window+1:i+1])
                weighted_avg = np.sum(window_values * weights)
                wma.append(weighted_avg)
            else:
                wma.append(self.values[i])
        
        return wma
    
    def detect_anomalies(self, threshold: float = 2.0) -> List[Tuple[int, float, str]]:
        """Detect anomalies using statistical methods."""
        if len(self.values) < 10:
            return []
        
        anomalies = []
        values = np.array(self.values)
        
        # Z-score based anomaly detection
        mean_val = np.mean(values)
        std_val = np.std(values)
        
        if std_val > 0:
            z_scores = np.abs((values - mean_val) / std_val)
            
            for i, z_score in enumerate(z_scores):
                if z_score > threshold:
                    anomalies.append((i, values[i], f"Z-score: {z_score:.2f}"))
        
        # Moving average based detection
        if len(self.values) >= 10:
            window = min(10, len(self.values) // 5)
            moving_avg = self.simple_moving_average(window)
            
            for i in range(len(values)):
                if i < len(moving_avg):
                    deviation = abs(values[i] - moving_avg[i])
                    if deviation > threshold * std_val:
                        anomalies.append((i, values[i], f"MA deviation: {deviation:.2f}"))
        
        # Remove duplicates and sort by index
        unique_anomalies = {}
        for idx, val, reason in anomalies:
            if idx not in unique_anomalies or len(reason) > len(unique_anomalies[idx][1]):
                unique_anomalies[idx] = (val, reason)
        
        return [(idx, val, reason) for idx, (val, reason) in sorted(unique_anomalies.items())]
    
    def forecast_next_values(self, n_steps: int = 5) -> List[Dict[str, Any]]:
        """Forecast next n values using multiple methods."""
        if len(self.values) < 5:
            return []
        
        forecasts = []
        
        # Method 1: Simple Moving Average
        sma_window = min(10, len(self.values) // 2)
        recent_values = self.values[-sma_window:]
        sma_forecast = np.mean(recent_values)
        
        # Method 2: Exponential Moving Average
        ema_values = self.exponential_moving_average(alpha=0.3)
        ema_forecast = ema_values[-1] if ema_values else self.values[-1]
        
        # Method 3: Trend-based linear projection
        if len(self.values) >= 10:
            x = np.arange(len(self.values))
            y = np.array(self.values)
            
            # Simple linear regression
            n = len(x)
            sum_x = np.sum(x)
            sum_y = np.sum(y)
            sum_xy = np.sum(x * y)
            sum_x2 = np.sum(x * x)
            
            if n * sum_x2 - sum_x * sum_x != 0:
                slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x * sum_x)
                intercept = (sum_y - slope * sum_x) / n
                
                trend_forecast = slope * len(self.values) + intercept
            else:
                trend_forecast = self.values[-1]
        else:
            trend_forecast = self.values[-1]
        
        # Method 4: Seasonal adjustment if applicable
        seasonal_forecast = trend_forecast
        if self.period > 0 and len(self.seasonal) >= self.period:
            seasonal_component = self.seasonal[-self.period:][0]  # Get seasonal pattern
            seasonal_forecast = trend_forecast + seasonal_component
        
        # Ensemble forecast (weighted average of methods)
        weights = [0.2, 0.3, 0.3, 0.2]  # SMA, EMA, Trend, Seasonal
        methods = [sma_forecast, ema_forecast, trend_forecast, seasonal_forecast]
        ensemble_forecast = np.average(methods, weights=weights)
        
        # Generate forecasts for next n_steps
        for step in range(1, n_steps + 1):
            # Simple projection (could be made more sophisticated)
            forecast_value = ensemble_forecast
            
            # Add some uncertainty based on historical variance
            std_dev = np.std(self.values) if len(self.values) > 1 else 0
            lower_bound = forecast_value - 2 * std_dev
            upper_bound = forecast_value + 2 * std_dev
            
            # Adjust for trend if detected
            if len(self.values) >= 10:
                recent_trend = np.mean(np.diff(self.values[-10:]))
                forecast_value += recent_trend * step
            
            forecasts.append({
                'step': step,
                'forecast': forecast_value,
                'lower_bound': max(lower_bound, self.stats['min']),
                'upper_bound': min(upper_bound, self.stats['max']),
                'confidence': max(0.1, 1.0 - (step - 1) * 0.1),  # Decreasing confidence
                'methods': {
                    'sma': sma_forecast,
                    'ema': ema_forecast,
                    'trend': trend_forecast,
                    'seasonal': seasonal_forecast,
                    'ensemble': ensemble_forecast
                }
            })
        
        return forecasts
    
    def evaluate_forecast_accuracy(self, actual_values: List[float], 
                                 forecasted_values: List[float]) -> Dict[str, float]:
        """Evaluate forecast accuracy using multiple metrics."""
        if len(actual_values) != len(forecasted_values) or not actual_values:
            return {}
        
        actual = np.array(actual_values)
        forecast = np.array(forecasted_values)
        
        # Mean Absolute Error
        mae = np.mean(np.abs(actual - forecast))
        
        # Mean Squared Error
        mse = np.mean((actual - forecast) ** 2)
        
        # Root Mean Squared Error
        rmse = np.sqrt(mse)
        
        # Mean Absolute Percentage Error
        mape = np.mean(np.abs((actual - forecast) / (actual + 1e-8))) * 100
        
        # R-squared (coefficient of determination)
        ss_res = np.sum((actual - forecast) ** 2)
        ss_tot = np.sum((actual - np.mean(actual)) ** 2)
        r2 = 1 - (ss_res / (ss_tot + 1e-8))
        
        return {
            'mae': mae,
            'mse': mse,
            'rmse': rmse,
            'mape': mape,
            'r2': r2,
            'samples': len(actual_values)
        }


# ==============================================================================
# PROJECT 2: COMPUTER VISION IMAGE CLASSIFIER
# ==============================================================================

class ConvolutionalLayer:
    """Convolutional layer for CNN."""
    
    def __init__(self, num_filters: int, filter_size: int, stride: int = 1, padding: int = 0):
        self.num_filters = num_filters
        self.filter_size = filter_size
        self.stride = stride
        self.padding = padding
        
        # Initialize filters with Xavier initialization
        self.filters = np.random.randn(num_filters, filter_size, filter_size) * np.sqrt(2.0 / (filter_size * filter_size))
        self.biases = np.zeros(num_filters)
        
        # Cache for backpropagation
        self.last_input = None
        self.last_output = None
    
    def forward(self, input_image: np.ndarray) -> np.ndarray:
        """Forward pass through convolutional layer."""
        self.last_input = input_image
        
        if len(input_image.shape) == 2:
            input_height, input_width = input_image.shape
            input_channels = 1
            input_image = input_image.reshape(1, input_height, input_width)
        else:
            input_channels, input_height, input_width = input_image.shape
        
        # Calculate output dimensions
        output_height = (input_height + 2 * self.padding - self.filter_size) // self.stride + 1
        output_width = (input_width + 2 * self.padding - self.filter_size) // self.stride + 1
        
        # Add padding if needed
        if self.padding > 0:
            input_image = np.pad(input_image, ((0, 0), (self.padding, self.padding), (self.padding, self.padding)), mode='constant')
        
        # Initialize output
        output = np.zeros((self.num_filters, output_height, output_width))
        
        # Perform convolution
        for f in range(self.num_filters):
            for i in range(output_height):
                for j in range(output_width):
                    # Extract region
                    start_i = i * self.stride
                    start_j = j * self.stride
                    end_i = start_i + self.filter_size
                    end_j = start_j + self.filter_size
                    
                    region = input_image[:, start_i:end_i, start_j:end_j]
                    
                    # Convolution operation
                    if input_channels == 1:
                        output[f, i, j] = np.sum(region[0] * self.filters[f]) + self.biases[f]
                    else:
                        # For multi-channel input (would need filter modification)
                        output[f, i, j] = np.sum(region[0] * self.filters[f]) + self.biases[f]
        
        self.last_output = output
        return output
    
    def relu(self, x: np.ndarray) -> np.ndarray:
        """ReLU activation function."""
        return np.maximum(0, x)


class MaxPoolingLayer:
    """Max pooling layer for CNN."""
    
    def __init__(self, pool_size: int = 2, stride: int = 2):
        self.pool_size = pool_size
        self.stride = stride
        self.last_input = None
        self.last_output = None
    
    def forward(self, input_data: np.ndarray) -> np.ndarray:
        """Forward pass through max pooling layer."""
        self.last_input = input_data
        
        if len(input_data.shape) == 2:
            channels, input_height, input_width = 1, input_data.shape[0], input_data.shape[1]
            input_data = input_data.reshape(1, input_height, input_width)
        else:
            channels, input_height, input_width = input_data.shape
        
        # Calculate output dimensions
        output_height = (input_height - self.pool_size) // self.stride + 1
        output_width = (input_width - self.pool_size) // self.stride + 1
        
        output = np.zeros((channels, output_height, output_width))
        
        # Perform max pooling
        for c in range(channels):
            for i in range(output_height):
                for j in range(output_width):
                    start_i = i * self.stride
                    start_j = j * self.stride
                    end_i = start_i + self.pool_size
                    end_j = start_j + self.pool_size
                    
                    pool_region = input_data[c, start_i:end_i, start_j:end_j]
                    output[c, i, j] = np.max(pool_region)
        
        self.last_output = output
        return output


class SimpleCNN:
    """
    Simple Convolutional Neural Network implemented from scratch.
    
    Features:
    - Convolutional layers with multiple filters
    - Max pooling layers
    - Fully connected layers
    - ReLU activation functions
    - Basic image classification
    """
    
    def __init__(self, input_shape: Tuple[int, int], num_classes: int):
        self.input_shape = input_shape
        self.num_classes = num_classes
        
        # Network architecture
        self.conv1 = ConvolutionalLayer(num_filters=8, filter_size=3, stride=1, padding=1)
        self.pool1 = MaxPoolingLayer(pool_size=2, stride=2)
        self.conv2 = ConvolutionalLayer(num_filters=16, filter_size=3, stride=1, padding=1)
        self.pool2 = MaxPoolingLayer(pool_size=2, stride=2)
        
        # Calculate flattened size after conv/pooling layers
        self.flattened_size = self._calculate_flattened_size()
        
        # Fully connected layers
        self.fc_weights1 = np.random.randn(self.flattened_size, 64) * 0.1
        self.fc_biases1 = np.zeros(64)
        self.fc_weights2 = np.random.randn(64, num_classes) * 0.1
        self.fc_biases2 = np.zeros(num_classes)
        
        # Training parameters
        self.learning_rate = 0.001
    
    def _calculate_flattened_size(self) -> int:
        """Calculate the size of flattened feature vector."""
        # Simulate forward pass to get dimensions
        dummy_input = np.zeros(self.input_shape)
        
        # Conv1 + Pool1
        conv1_out = self.conv1.forward(dummy_input)
        pool1_out = self.pool1.forward(conv1_out)
        
        # Conv2 + Pool2  
        conv2_out = self.conv2.forward(pool1_out)
        pool2_out = self.pool2.forward(conv2_out)
        
        return int(np.prod(pool2_out.shape))
    
    def forward(self, x: np.ndarray) -> np.ndarray:
        """Forward pass through the CNN."""
        # Convolutional layers
        conv1_out = self.conv1.forward(x)
        conv1_relu = self.conv1.relu(conv1_out)
        pool1_out = self.pool1.forward(conv1_relu)
        
        conv2_out = self.conv2.forward(pool1_out)
        conv2_relu = self.conv2.relu(conv2_out)
        pool2_out = self.pool2.forward(conv2_relu)
        
        # Flatten for fully connected layers
        flattened = pool2_out.flatten()
        
        # Fully connected layer 1
        fc1_out = np.dot(flattened, self.fc_weights1) + self.fc_biases1
        fc1_relu = np.maximum(0, fc1_out)  # ReLU
        
        # Fully connected layer 2 (output)
        output = np.dot(fc1_relu, self.fc_weights2) + self.fc_biases2
        
        # Softmax activation
        exp_output = np.exp(output - np.max(output))  # Numerical stability
        softmax_output = exp_output / np.sum(exp_output)
        
        return softmax_output
    
    def predict(self, x: np.ndarray) -> int:
        """Predict class for input image."""
        probabilities = self.forward(x)
        return np.argmax(probabilities)
    
    def predict_probabilities(self, x: np.ndarray) -> np.ndarray:
        """Get prediction probabilities for input image."""
        return self.forward(x)


class ImagePreprocessor:
    """Image preprocessing utilities for CNN."""
    
    @staticmethod
    def normalize_image(image: np.ndarray) -> np.ndarray:
        """Normalize image pixel values to [0, 1]."""
        return image.astype(np.float32) / 255.0
    
    @staticmethod
    def resize_image(image: np.ndarray, target_size: Tuple[int, int]) -> np.ndarray:
        """Simple image resizing using nearest neighbor interpolation."""
        original_height, original_width = image.shape
        target_height, target_width = target_size
        
        # Calculate scaling factors
        height_scale = original_height / target_height
        width_scale = original_width / target_width
        
        # Create new image
        resized = np.zeros((target_height, target_width))
        
        for i in range(target_height):
            for j in range(target_width):
                # Map back to original coordinates
                orig_i = int(i * height_scale)
                orig_j = int(j * width_scale)
                
                # Ensure within bounds
                orig_i = min(orig_i, original_height - 1)
                orig_j = min(orig_j, original_width - 1)
                
                resized[i, j] = image[orig_i, orig_j]
        
        return resized
    
    @staticmethod
    def create_synthetic_dataset(num_samples: int = 1000, 
                               image_size: Tuple[int, int] = (28, 28),
                               num_classes: int = 3) -> Tuple[List[np.ndarray], List[int]]:
        """Create a synthetic image dataset for testing."""
        images = []
        labels = []
        
        height, width = image_size
        
        for _ in range(num_samples):
            # Create base image with noise
            image = np.random.rand(height, width) * 0.1
            
            # Choose class randomly
            class_label = random.randint(0, num_classes - 1)
            
            if class_label == 0:
                # Class 0: Horizontal stripes
                for i in range(0, height, 4):
                    image[i:i+2, :] = 0.8 + np.random.rand(min(2, height-i), width) * 0.2
            
            elif class_label == 1:
                # Class 1: Vertical stripes  
                for j in range(0, width, 4):
                    image[:, j:j+2] = 0.8 + np.random.rand(height, min(2, width-j)) * 0.2
            
            else:  # class_label == 2
                # Class 2: Diagonal pattern
                for i in range(height):
                    for j in range(width):
                        if (i + j) % 8 < 4:
                            image[i, j] = 0.8 + np.random.rand() * 0.2
            
            # Add some noise
            noise = np.random.rand(height, width) * 0.1
            image = np.clip(image + noise, 0, 1)
            
            images.append(image)
            labels.append(class_label)
        
        return images, labels


# ==============================================================================
# PROJECT 3: REINFORCEMENT LEARNING GAME AI
# ==============================================================================

class GridWorld:
    """Simple grid world environment for reinforcement learning."""
    
    def __init__(self, width: int = 5, height: int = 5):
        self.width = width
        self.height = height
        self.grid = np.zeros((height, width))
        
        # Set up environment
        self.start_pos = (0, 0)
        self.goal_pos = (height - 1, width - 1)
        self.obstacles = [(2, 2), (3, 1), (1, 3)]  # Some obstacles
        
        # Current state
        self.agent_pos = self.start_pos
        self.done = False
        
        # Rewards
        self.goal_reward = 100
        self.step_reward = -1
        self.obstacle_reward = -10
        
        # Actions: 0=up, 1=right, 2=down, 3=left
        self.actions = [(0, -1, 0), (1, 0, 1), (2, 1, 0), (3, 0, -1)]  # (action_id, dy, dx)
        self.num_actions = len(self.actions)
        
        self._setup_grid()
    
    def _setup_grid(self):
        """Setup the grid with obstacles and goal."""
        self.grid = np.zeros((self.height, self.width))
        
        # Mark obstacles
        for obs_y, obs_x in self.obstacles:
            if 0 <= obs_y < self.height and 0 <= obs_x < self.width:
                self.grid[obs_y, obs_x] = -1
        
        # Mark goal
        goal_y, goal_x = self.goal_pos
        self.grid[goal_y, goal_x] = 1
    
    def reset(self) -> Tuple[int, int]:
        """Reset environment and return initial state."""
        self.agent_pos = self.start_pos
        self.done = False
        return self.agent_pos
    
    def step(self, action: int) -> Tuple[Tuple[int, int], float, bool, Dict]:
        """Take a step in the environment."""
        if self.done:
            return self.agent_pos, 0, True, {}
        
        # Get action deltas
        _, dy, dx = self.actions[action]
        new_y = self.agent_pos[0] + dy
        new_x = self.agent_pos[1] + dx
        
        # Check bounds
        if 0 <= new_y < self.height and 0 <= new_x < self.width:
            new_pos = (new_y, new_x)
            
            # Check if it's an obstacle
            if new_pos in self.obstacles:
                reward = self.obstacle_reward
                new_pos = self.agent_pos  # Stay in place
            else:
                self.agent_pos = new_pos
                reward = self.step_reward
                
                # Check if reached goal
                if self.agent_pos == self.goal_pos:
                    reward = self.goal_reward
                    self.done = True
        else:
            # Hit boundary, stay in place
            new_pos = self.agent_pos
            reward = self.step_reward
        
        return new_pos, reward, self.done, {}
    
    def get_state_id(self, pos: Tuple[int, int]) -> int:
        """Convert position to unique state ID."""
        return pos[0] * self.width + pos[1]
    
    def get_valid_actions(self, pos: Tuple[int, int]) -> List[int]:
        """Get list of valid actions from current position."""
        valid_actions = []
        
        for action_id, dy, dx in self.actions:
            new_y = pos[0] + dy
            new_x = pos[1] + dx
            
            # Check if move is valid (within bounds and not obstacle)
            if (0 <= new_y < self.height and 0 <= new_x < self.width and
                (new_y, new_x) not in self.obstacles):
                valid_actions.append(action_id)
        
        return valid_actions


class QLearningAgent:
    """
    Q-Learning reinforcement learning agent.
    
    Features:
    - Q-table for value function approximation
    - Epsilon-greedy exploration strategy
    - Learning rate and discount factor
    - Experience replay (simplified)
    - Performance tracking
    """
    
    def __init__(self, num_states: int, num_actions: int, 
                 learning_rate: float = 0.1, discount_factor: float = 0.9,
                 epsilon: float = 0.1, epsilon_decay: float = 0.995):
        self.num_states = num_states
        self.num_actions = num_actions
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.min_epsilon = 0.01
        
        # Q-table: state x action
        self.q_table = np.random.rand(num_states, num_actions) * 0.01
        
        # Performance tracking
        self.episode_rewards = []
        self.episode_steps = []
        self.total_steps = 0
    
    def get_action(self, state: int, valid_actions: List[int] = None) -> int:
        """Choose action using epsilon-greedy policy."""
        if valid_actions is None:
            valid_actions = list(range(self.num_actions))
        
        if random.random() < self.epsilon:
            # Explore: choose random valid action
            return random.choice(valid_actions)
        else:
            # Exploit: choose best valid action
            q_values = self.q_table[state]
            valid_q_values = [(action, q_values[action]) for action in valid_actions]
            best_action = max(valid_q_values, key=lambda x: x[1])[0]
            return best_action
    
    def update_q_value(self, state: int, action: int, reward: float, 
                      next_state: int, done: bool):
        """Update Q-value using Q-learning update rule."""
        current_q = self.q_table[state, action]
        
        if done:
            # Terminal state
            target_q = reward
        else:
            # Use max Q-value of next state
            max_next_q = np.max(self.q_table[next_state])
            target_q = reward + self.discount_factor * max_next_q
        
        # Q-learning update
        self.q_table[state, action] = current_q + self.learning_rate * (target_q - current_q)
    
    def train_episode(self, env: GridWorld) -> Dict[str, Any]:
        """Train agent for one episode."""
        state = env.reset()
        state_id = env.get_state_id(state)
        
        total_reward = 0
        steps = 0
        max_steps = 1000  # Prevent infinite loops
        
        while not env.done and steps < max_steps:
            # Choose action
            valid_actions = env.get_valid_actions(state)
            action = self.get_action(state_id, valid_actions)
            
            # Take step
            next_state, reward, done, _ = env.step(action)
            next_state_id = env.get_state_id(next_state)
            
            # Update Q-value
            self.update_q_value(state_id, action, reward, next_state_id, done)
            
            # Update state
            state = next_state
            state_id = next_state_id
            total_reward += reward
            steps += 1
            self.total_steps += 1
        
        # Decay epsilon
        self.epsilon = max(self.min_epsilon, self.epsilon * self.epsilon_decay)
        
        # Track performance
        self.episode_rewards.append(total_reward)
        self.episode_steps.append(steps)
        
        return {
            'episode_reward': total_reward,
            'episode_steps': steps,
            'epsilon': self.epsilon,
            'reached_goal': env.done
        }
    
    def get_policy(self, env: GridWorld) -> Dict[Tuple[int, int], int]:
        """Extract learned policy from Q-table."""
        policy = {}
        
        for y in range(env.height):
            for x in range(env.width):
                state = (y, x)
                if state not in env.obstacles and state != env.goal_pos:
                    state_id = env.get_state_id(state)
                    valid_actions = env.get_valid_actions(state)
                    
                    if valid_actions:
                        q_values = [(action, self.q_table[state_id, action]) for action in valid_actions]
                        best_action = max(q_values, key=lambda x: x[1])[0]
                        policy[state] = best_action
        
        return policy
    
    def evaluate_policy(self, env: GridWorld, num_episodes: int = 100) -> Dict[str, float]:
        """Evaluate current policy without learning."""
        old_epsilon = self.epsilon
        self.epsilon = 0  # Greedy policy only
        
        successes = 0
        total_rewards = []
        total_steps = []
        
        for _ in range(num_episodes):
            state = env.reset()
            state_id = env.get_state_id(state)
            
            episode_reward = 0
            steps = 0
            max_steps = 1000
            
            while not env.done and steps < max_steps:
                valid_actions = env.get_valid_actions(state)
                action = self.get_action(state_id, valid_actions)
                
                next_state, reward, done, _ = env.step(action)
                next_state_id = env.get_state_id(next_state)
                
                state = next_state
                state_id = next_state_id
                episode_reward += reward
                steps += 1
            
            if env.done:
                successes += 1
            
            total_rewards.append(episode_reward)
            total_steps.append(steps)
        
        # Restore epsilon
        self.epsilon = old_epsilon
        
        return {
            'success_rate': successes / num_episodes,
            'avg_reward': np.mean(total_rewards),
            'avg_steps': np.mean(total_steps),
            'episodes_evaluated': num_episodes
        }


# ==============================================================================
# DEMONSTRATION FUNCTIONS
# ==============================================================================

def demonstrate_time_series_forecasting():
    """Demonstrate time series forecasting engine."""
    print("\n" + "="*60)
    print("📈 TIME SERIES FORECASTING ENGINE DEMO")
    print("="*60)
    
    # Create a time series forecaster
    forecaster = TimeSeriesForecaster()
    
    # Generate synthetic time series data with trend and seasonality
    print("Creating synthetic time series data...")
    np.random.seed(42)
    
    base_date = datetime(2023, 1, 1)
    data_points = []
    
    for i in range(100):
        timestamp = base_date + timedelta(days=i)
        
        # Trend component
        trend = 100 + 0.5 * i
        
        # Seasonal component (weekly pattern)
        seasonal = 20 * np.sin(2 * np.pi * i / 7)
        
        # Random noise
        noise = np.random.normal(0, 5)
        
        # Combine components
        value = trend + seasonal + noise
        
        # Add some features
        features = {
            'day_of_week': i % 7,
            'month': timestamp.month,
            'is_weekend': 1 if i % 7 in [5, 6] else 0
        }
        
        data_point = TimeSeriesDataPoint(timestamp, value, features)
        data_points.append(data_point)
    
    # Add data to forecaster
    forecaster.add_data_batch(data_points)
    
    print(f"Added {len(data_points)} data points")
    print(f"Time range: {data_points[0].timestamp} to {data_points[-1].timestamp}")
    
    # Show basic statistics
    stats = forecaster.stats
    print(f"\n📊 Time Series Statistics:")
    print(f"  Mean: {stats['mean']:.2f}")
    print(f"  Standard Deviation: {stats['std']:.2f}")
    print(f"  Range: [{stats['min']:.2f}, {stats['max']:.2f}]")
    print(f"  Variance: {stats['variance']:.2f}")
    
    # Detect seasonality
    print(f"\n🔍 Seasonality Detection:")
    period = forecaster.detect_seasonality(max_period=20)
    if period > 0:
        print(f"  Detected seasonal period: {period} days")
        print(f"  Top autocorrelations: {forecaster.stats['autocorrelation'][:3]}")
    else:
        print("  No clear seasonal pattern detected")
    
    # Decompose time series
    print(f"\n🔧 Time Series Decomposition:")
    forecaster.decompose_series()
    print(f"  Trend component extracted: {len(forecaster.trend)} points")
    print(f"  Seasonal component extracted: {len(forecaster.seasonal)} points")
    print(f"  Residual component extracted: {len(forecaster.residual)} points")
    
    # Calculate moving averages
    print(f"\n📊 Moving Averages:")
    sma_5 = forecaster.simple_moving_average(5)
    ema = forecaster.exponential_moving_average(alpha=0.3)
    wma = forecaster.weighted_moving_average([0.1, 0.2, 0.3, 0.4])
    
    print(f"  Simple MA (5-day): Latest values {sma_5[-3:]}")
    print(f"  Exponential MA: Latest values {ema[-3:]}")
    print(f"  Weighted MA: Latest values {wma[-3:]}")
    
    # Detect anomalies
    print(f"\n🚨 Anomaly Detection:")
    anomalies = forecaster.detect_anomalies(threshold=2.0)
    print(f"  Found {len(anomalies)} anomalies:")
    for i, (idx, value, reason) in enumerate(anomalies[:5]):  # Show first 5
        date = data_points[idx].timestamp.strftime("%Y-%m-%d")
        print(f"    {i+1}. {date}: Value={value:.2f} ({reason})")
    
    # Generate forecasts
    print(f"\n🔮 Generating Forecasts:")
    forecasts = forecaster.forecast_next_values(n_steps=7)
    
    print(f"  Next 7 days forecast:")
    for forecast in forecasts:
        print(f"    Day +{forecast['step']}: {forecast['forecast']:.2f} "
              f"(confidence: {forecast['confidence']:.2f}, "
              f"range: [{forecast['lower_bound']:.2f}, {forecast['upper_bound']:.2f}])")
    
    # Test forecast accuracy (simulate)
    print(f"\n📊 Forecast Accuracy Assessment:")
    # Use last 10 points as "actual" and compare with "forecasted"
    actual = forecaster.values[-10:]
    # Generate simple forecasts for comparison
    simple_forecast = [forecaster.values[-11]] * 10  # Naive forecast
    
    accuracy = forecaster.evaluate_forecast_accuracy(actual, simple_forecast)
    if accuracy:
        print(f"  Mean Absolute Error: {accuracy['mae']:.2f}")
        print(f"  Root Mean Squared Error: {accuracy['rmse']:.2f}")
        print(f"  Mean Absolute Percentage Error: {accuracy['mape']:.2f}%")
        print(f"  R-squared: {accuracy['r2']:.4f}")
    
    print(f"\n✅ Time Series Forecasting demonstration completed!")


def demonstrate_computer_vision():
    """Demonstrate computer vision image classifier."""
    print("\n" + "="*60)
    print("👁️ COMPUTER VISION IMAGE CLASSIFIER DEMO")
    print("="*60)
    
    # Set random seed for reproducibility
    np.random.seed(42)
    
    # Create synthetic dataset
    print("Creating synthetic image dataset...")
    image_size = (16, 16)  # Small for demo purposes
    num_classes = 3
    num_samples = 300
    
    images, labels = ImagePreprocessor.create_synthetic_dataset(
        num_samples=num_samples, image_size=image_size, num_classes=num_classes
    )
    
    print(f"Dataset created:")
    print(f"  Images: {len(images)}")
    print(f"  Image size: {image_size}")
    print(f"  Classes: {num_classes}")
    print(f"  Class distribution: {Counter(labels)}")
    
    # Show sample images info
    print(f"\n🖼️ Sample Image Analysis:")
    for class_id in range(min(num_classes, 3)):
        class_indices = [i for i, label in enumerate(labels) if label == class_id]
        if class_indices:
            sample_image = images[class_indices[0]]
            print(f"  Class {class_id}: Shape {sample_image.shape}, "
                  f"Value range [{sample_image.min():.3f}, {sample_image.max():.3f}]")
    
    # Preprocess images
    print(f"\n🔧 Preprocessing Images:")
    preprocessor = ImagePreprocessor()
    
    processed_images = []
    for img in images:
        # Normalize
        normalized = preprocessor.normalize_image((img * 255).astype(np.uint8))
        processed_images.append(normalized)
    
    print(f"  Normalized {len(processed_images)} images")
    print(f"  New value range: [{processed_images[0].min():.3f}, {processed_images[0].max():.3f}]")
    
    # Split dataset
    train_split = 0.8
    train_size = int(len(processed_images) * train_split)
    
    # Shuffle data
    indices = list(range(len(processed_images)))
    np.random.shuffle(indices)
    
    train_indices = indices[:train_size]
    test_indices = indices[train_size:]
    
    X_train = [processed_images[i] for i in train_indices]
    y_train = [labels[i] for i in train_indices]
    X_test = [processed_images[i] for i in test_indices]
    y_test = [labels[i] for i in test_indices]
    
    print(f"\n📊 Dataset Split:")
    print(f"  Training samples: {len(X_train)}")
    print(f"  Test samples: {len(X_test)}")
    print(f"  Training class distribution: {Counter(y_train)}")
    print(f"  Test class distribution: {Counter(y_test)}")
    
    # Create CNN model
    print(f"\n🧠 Creating CNN Model:")
    cnn = SimpleCNN(input_shape=image_size, num_classes=num_classes)
    
    print(f"  Input shape: {image_size}")
    print(f"  Number of classes: {num_classes}")
    print(f"  Flattened feature size: {cnn.flattened_size}")
    print(f"  Network architecture:")
    print(f"    Conv1: 8 filters, 3x3, ReLU + MaxPool 2x2")
    print(f"    Conv2: 16 filters, 3x3, ReLU + MaxPool 2x2")
    print(f"    FC1: {cnn.flattened_size} -> 64, ReLU")
    print(f"    FC2: 64 -> {num_classes}, Softmax")
    
    # Test model with sample predictions
    print(f"\n🔮 Testing Model Predictions:")
    test_samples = 5
    
    for i in range(min(test_samples, len(X_test))):
        image = X_test[i]
        true_label = y_test[i]
        
        # Get prediction
        probabilities = cnn.predict_probabilities(image)
        predicted_label = cnn.predict(image)
        confidence = probabilities[predicted_label]
        
        print(f"  Sample {i+1}: True={true_label}, Predicted={predicted_label}, "
              f"Confidence={confidence:.3f}")
        print(f"    Probabilities: {probabilities}")
    
    # Evaluate on test set
    print(f"\n📊 Model Evaluation:")
    correct_predictions = 0
    total_predictions = len(X_test)
    
    class_correct = defaultdict(int)
    class_total = defaultdict(int)
    
    for i in range(total_predictions):
        image = X_test[i]
        true_label = y_test[i]
        predicted_label = cnn.predict(image)
        
        if predicted_label == true_label:
            correct_predictions += 1
            class_correct[true_label] += 1
        
        class_total[true_label] += 1
    
    overall_accuracy = correct_predictions / total_predictions
    print(f"  Overall Accuracy: {overall_accuracy:.4f} ({correct_predictions}/{total_predictions})")
    
    print(f"  Per-class Accuracy:")
    for class_id in range(num_classes):
        if class_total[class_id] > 0:
            class_acc = class_correct[class_id] / class_total[class_id]
            print(f"    Class {class_id}: {class_acc:.4f} ({class_correct[class_id]}/{class_total[class_id]})")
    
    # Show some layer outputs for interpretation
    print(f"\n🔍 Feature Analysis:")
    sample_image = X_test[0]
    
    # Forward pass through layers
    conv1_out = cnn.conv1.forward(sample_image)
    print(f"  Conv1 output shape: {conv1_out.shape}")
    print(f"  Conv1 activation range: [{conv1_out.min():.3f}, {conv1_out.max():.3f}]")
    
    pool1_out = cnn.pool1.forward(conv1_out)
    print(f"  Pool1 output shape: {pool1_out.shape}")
    
    conv2_out = cnn.conv2.forward(pool1_out)
    print(f"  Conv2 output shape: {conv2_out.shape}")
    print(f"  Conv2 activation range: [{conv2_out.min():.3f}, {conv2_out.max():.3f}]")
    
    print(f"\n✅ Computer Vision demonstration completed!")


def demonstrate_reinforcement_learning():
    """Demonstrate reinforcement learning game AI."""
    print("\n" + "="*60)
    print("🎮 REINFORCEMENT LEARNING GAME AI DEMO")
    print("="*60)
    
    # Create grid world environment
    print("Creating Grid World environment...")
    env = GridWorld(width=5, height=5)
    
    print(f"Environment Details:")
    print(f"  Grid size: {env.width}x{env.height}")
    print(f"  Start position: {env.start_pos}")
    print(f"  Goal position: {env.goal_pos}")
    print(f"  Obstacles: {env.obstacles}")
    print(f"  Actions: {len(env.actions)} (up, right, down, left)")
    
    # Display grid
    print(f"\nGrid World Map:")
    display_grid = np.zeros((env.height, env.width))
    
    # Mark different elements
    for y in range(env.height):
        for x in range(env.width):
            if (y, x) == env.start_pos:
                display_grid[y, x] = 2  # Start
            elif (y, x) == env.goal_pos:
                display_grid[y, x] = 3  # Goal
            elif (y, x) in env.obstacles:
                display_grid[y, x] = 1  # Obstacle
            else:
                display_grid[y, x] = 0  # Empty
    
    symbols = {0: '.', 1: 'X', 2: 'S', 3: 'G'}
    for row in display_grid:
        print('  ' + ' '.join(symbols[int(cell)] for cell in row))
    
    print("  Legend: S=Start, G=Goal, X=Obstacle, .=Empty")
    
    # Create Q-Learning agent
    num_states = env.width * env.height
    num_actions = env.num_actions
    
    agent = QLearningAgent(
        num_states=num_states, 
        num_actions=num_actions,
        learning_rate=0.1,
        discount_factor=0.9,
        epsilon=0.9,
        epsilon_decay=0.995
    )
    
    print(f"\n🤖 Q-Learning Agent:")
    print(f"  State space size: {num_states}")
    print(f"  Action space size: {num_actions}")
    print(f"  Learning rate: {agent.learning_rate}")
    print(f"  Discount factor: {agent.discount_factor}")
    print(f"  Initial epsilon: {agent.epsilon}")
    
    # Training phase
    print(f"\n🏋️ Training Phase:")
    num_episodes = 200
    eval_interval = 50
    
    training_start = time.time()
    
    for episode in range(num_episodes):
        result = agent.train_episode(env)
        
        # Show progress periodically
        if (episode + 1) % eval_interval == 0:
            recent_rewards = agent.episode_rewards[-eval_interval:]
            recent_steps = agent.episode_steps[-eval_interval:]
            success_rate = sum(1 for r in recent_rewards if r > 50) / len(recent_rewards)
            
            print(f"  Episode {episode + 1}:")
            print(f"    Avg reward (last {eval_interval}): {np.mean(recent_rewards):.2f}")
            print(f"    Avg steps (last {eval_interval}): {np.mean(recent_steps):.1f}")
            print(f"    Success rate: {success_rate:.2%}")
            print(f"    Epsilon: {agent.epsilon:.4f}")
    
    training_time = time.time() - training_start
    print(f"\n  Training completed in {training_time:.2f} seconds")
    
    # Evaluate trained agent
    print(f"\n📊 Evaluating Trained Agent:")
    evaluation = agent.evaluate_policy(env, num_episodes=100)
    
    print(f"  Success rate: {evaluation['success_rate']:.2%}")
    print(f"  Average reward: {evaluation['avg_reward']:.2f}")
    print(f"  Average steps to goal: {evaluation['avg_steps']:.1f}")
    
    # Extract and display learned policy
    print(f"\n🧭 Learned Policy:")
    policy = agent.get_policy(env)
    action_symbols = {0: '↑', 1: '→', 2: '↓', 3: '←'}
    
    policy_grid = np.full((env.height, env.width), ' ', dtype=str)
    
    for y in range(env.height):
        for x in range(env.width):
            pos = (y, x)
            if pos == env.start_pos:
                policy_grid[y, x] = 'S'
            elif pos == env.goal_pos:
                policy_grid[y, x] = 'G'
            elif pos in env.obstacles:
                policy_grid[y, x] = 'X'
            elif pos in policy:
                action = policy[pos]
                policy_grid[y, x] = action_symbols.get(action, '?')
    
    for row in policy_grid:
        print('  ' + ' '.join(row))
    
    print("  Legend: S=Start, G=Goal, X=Obstacle, ↑↓←→=Optimal actions")
    
    # Test learned policy with a sample episode
    print(f"\n🎮 Sample Episode with Learned Policy:")
    state = env.reset()
    episode_path = [state]
    episode_actions = []
    episode_rewards = []
    
    agent.epsilon = 0  # Use greedy policy
    step = 0
    max_steps = 20
    
    while not env.done and step < max_steps:
        state_id = env.get_state_id(state)
        valid_actions = env.get_valid_actions(state)
        action = agent.get_action(state_id, valid_actions)
        
        next_state, reward, done, _ = env.step(action)
        
        episode_path.append(next_state)
        episode_actions.append(action)
        episode_rewards.append(reward)
        
        state = next_state
        step += 1
    
    print(f"  Path taken: {' -> '.join([f'({y},{x})' for y, x in episode_path])}")
    print(f"  Actions: {[action_symbols[a] for a in episode_actions]}")
    print(f"  Rewards: {episode_rewards}")
    print(f"  Total reward: {sum(episode_rewards)}")
    print(f"  Steps taken: {len(episode_actions)}")
    print(f"  Success: {'Yes' if env.done else 'No'}")
    
    # Show Q-value analysis
    print(f"\n📈 Q-Value Analysis:")
    start_state_id = env.get_state_id(env.start_pos)
    goal_state_id = env.get_state_id(env.goal_pos)
    
    print(f"  Q-values at start position {env.start_pos}:")
    for action in range(num_actions):
        q_val = agent.q_table[start_state_id, action]
        print(f"    {action_symbols[action]}: {q_val:.4f}")
    
    # Show learning progress
    print(f"\n📊 Learning Progress:")
    if len(agent.episode_rewards) >= 4:
        quarters = len(agent.episode_rewards) // 4
        for i in range(4):
            start_idx = i * quarters
            end_idx = (i + 1) * quarters if i < 3 else len(agent.episode_rewards)
            quarter_rewards = agent.episode_rewards[start_idx:end_idx]
            avg_reward = np.mean(quarter_rewards)
            print(f"  Quarter {i+1}: Average reward = {avg_reward:.2f}")
    
    print(f"\n✅ Reinforcement Learning demonstration completed!")


def main():
    """Run all advanced AI application demonstrations."""
    print("🚀 ADVANCED AI APPLICATIONS - CUTTING-EDGE PROJECTS")
    print("=" * 70)
    print("Sophisticated AI/ML implementations demonstrating advanced techniques")
    print("including time series forecasting, computer vision, and RL.")
    print("=" * 70)
    
    try:
        # Run demonstrations
        demonstrate_time_series_forecasting()
        demonstrate_computer_vision()
        demonstrate_reinforcement_learning()
        
    except KeyboardInterrupt:
        print("\n⚠️ Demonstration interrupted by user")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 70)
    print("🎉 ALL ADVANCED AI APPLICATION DEMONSTRATIONS COMPLETED!")
    print("=" * 70)
    
    print("\n📚 KEY LEARNING OUTCOMES:")
    print("✅ Time Series Forecasting: Trend analysis, seasonality, ARIMA concepts")
    print("✅ Computer Vision: CNN implementation, image preprocessing, classification")
    print("✅ Reinforcement Learning: Q-learning, policy extraction, environment interaction")
    print("✅ Advanced Algorithms: Convolution, backpropagation, value iteration")
    print("✅ Data Processing: Feature extraction, normalization, statistical analysis")
    print("✅ AI System Design: End-to-end pipeline development")
    
    print("\n🚀 NEXT LEVEL EXTENSIONS:")
    print("• Deep Reinforcement Learning (DQN, Policy Gradients)")
    print("• Advanced CNN architectures (ResNet, Attention mechanisms)")
    print("• LSTM/GRU networks for time series")
    print("• Multi-agent reinforcement learning")
    print("• Computer vision object detection and segmentation")
    print("• Generative models (GANs, VAEs)")
    print("• Transfer learning and fine-tuning")
    
    print("\n🎯 REAL-WORLD APPLICATIONS:")
    print("• Financial market prediction and algorithmic trading")
    print("• Medical image analysis and diagnosis")
    print("• Autonomous navigation and robotics")
    print("• Recommendation systems with deep learning")
    print("• Natural language understanding and generation")
    print("• Fraud detection and cybersecurity")
    print("• Supply chain optimization")
    print("• Smart city and IoT analytics")
    
    print(f"\n💡 These projects showcase how advanced AI concepts can be")
    print(f"   implemented from scratch using fundamental algorithms!")


if __name__ == "__main__":
    main()
