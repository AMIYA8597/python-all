#!/usr/bin/env python3
"""
TensorFlow & Keras Comprehensive Guide for Deep Learning
========================================================

This module provides comprehensive coverage of TensorFlow and Keras, the most popular
deep learning frameworks in Python. It covers neural networks, computer vision,
natural language processing, and advanced deep learning techniques.

Topics Covered:
1. TensorFlow Fundamentals & Tensor Operations
2. Keras Model Building & Training
3. Neural Networks (Dense, CNN, RNN, LSTM)
4. Computer Vision with CNNs
5. Natural Language Processing with RNNs
6. Transfer Learning & Pre-trained Models
7. Custom Layers, Loss Functions & Metrics
8. Model Optimization & Deployment
9. Advanced Techniques (GANs, Autoencoders, etc.)

Key Components:
- tf.keras.layers: Neural network layers
- tf.keras.models: Model architectures
- tf.keras.optimizers: Optimization algorithms
- tf.keras.losses: Loss functions
- tf.keras.metrics: Evaluation metrics
- tf.data: Data pipeline
- tf.image: Image processing
- tf.text: Text processing

Author: Python DSA Master
Date: 2024
"""

import numpy as np
from typing import List, Dict, Tuple, Any, Optional, Union
import warnings
warnings.filterwarnings('ignore')

# Note: This module demonstrates TensorFlow/Keras usage patterns and concepts.
# To run the actual code, install: pip install tensorflow numpy matplotlib

def demonstrate_tensorflow_basics():
    """
    Demonstrate core TensorFlow concepts without requiring installation.
    This shows the patterns and workflow used in TensorFlow.
    """
    print("TensorFlow & Keras Concepts and Patterns")
    print("=" * 50)
    
    # Typical TensorFlow workflow
    workflow_steps = [
        "1. Data Loading & Preprocessing",
        "2. Model Architecture Definition", 
        "3. Model Compilation (optimizer, loss, metrics)",
        "4. Model Training (fit)",
        "5. Model Evaluation & Validation",
        "6. Prediction & Inference",
        "7. Model Saving & Deployment"
    ]
    
    for step in workflow_steps:
        print(f"   {step}")
    
    print("\nCommon TensorFlow/Keras Import Patterns:")
    imports = [
        "import tensorflow as tf",
        "from tensorflow import keras",
        "from tensorflow.keras import layers, models, optimizers, losses, metrics",
        "from tensorflow.keras.preprocessing.image import ImageDataGenerator",
        "from tensorflow.keras.preprocessing.text import Tokenizer",
        "from tensorflow.keras.preprocessing.sequence import pad_sequences",
        "from tensorflow.keras.applications import VGG16, ResNet50, BERT",
        "from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau"
    ]
    
    for imp in imports:
        print(f"   {imp}")

class TensorFlowFundamentals:
    """Core TensorFlow operations and tensor manipulations."""
    
    @staticmethod
    def tensor_operations():
        """Show basic tensor operations."""
        print("\n" + "="*50)
        print("TENSORFLOW TENSOR OPERATIONS")
        print("="*50)
        
        print("\n1. TENSOR CREATION")
        tensor_creation = [
            "import tensorflow as tf",
            "",
            "# Create tensors",
            "scalar = tf.constant(5)",
            "vector = tf.constant([1, 2, 3, 4])",
            "matrix = tf.constant([[1, 2], [3, 4]])",
            "tensor_3d = tf.constant([[[1, 2], [3, 4]], [[5, 6], [7, 8]]])",
            "",
            "# Special tensors",
            "zeros = tf.zeros((3, 4))",
            "ones = tf.ones((2, 3))",
            "random_normal = tf.random.normal((2, 3), mean=0.0, stddev=1.0)",
            "random_uniform = tf.random.uniform((2, 3), minval=0, maxval=1)",
            "",
            "# From numpy",
            "import numpy as np",
            "np_array = np.array([1, 2, 3, 4])",
            "tf_tensor = tf.constant(np_array)"
        ]
        
        for line in tensor_creation:
            print(f"   {line}")
        
        print("\n2. TENSOR OPERATIONS")
        tensor_ops = [
            "# Basic arithmetic",
            "a = tf.constant([1, 2, 3])",
            "b = tf.constant([4, 5, 6])",
            "addition = tf.add(a, b)  # or a + b",
            "multiplication = tf.multiply(a, b)  # or a * b",
            "matrix_mult = tf.matmul(matrix1, matrix2)  # or matrix1 @ matrix2",
            "",
            "# Reshaping",
            "tensor = tf.constant([[1, 2, 3], [4, 5, 6]])",
            "reshaped = tf.reshape(tensor, (3, 2))",
            "transposed = tf.transpose(tensor)",
            "",
            "# Reductions",
            "sum_all = tf.reduce_sum(tensor)",
            "sum_axis_0 = tf.reduce_sum(tensor, axis=0)",
            "mean_val = tf.reduce_mean(tensor)",
            "max_val = tf.reduce_max(tensor)",
            "",
            "# Indexing and slicing",
            "slice_tensor = tensor[0:2, 1:3]",
            "gather_indices = tf.gather(tensor, [0, 2], axis=1)"
        ]
        
        for line in tensor_ops:
            print(f"   {line}")
            
        print("\n3. GRADIENTS & AUTODIFF")
        gradients = [
            "# Automatic differentiation",
            "x = tf.Variable(3.0)",
            "",
            "with tf.GradientTape() as tape:",
            "    y = x ** 2",
            "",
            "# Compute gradient dy/dx",
            "grad = tape.gradient(y, x)",
            "print(f'Gradient of x^2 at x=3: {grad}')",
            "",
            "# Multiple variables",
            "x = tf.Variable(2.0)",
            "y = tf.Variable(3.0)",
            "",
            "with tf.GradientTape() as tape:",
            "    z = x**2 + y**2",
            "",
            "gradients = tape.gradient(z, [x, y])"
        ]
        
        for line in gradients:
            print(f"   {line}")

class KerasModelBuilding:
    """Comprehensive Keras model building techniques."""
    
    @staticmethod
    def sequential_models():
        """Show Sequential model patterns."""
        print("\n" + "="*50)
        print("KERAS SEQUENTIAL MODELS")
        print("="*50)
        
        print("\n1. BASIC SEQUENTIAL MODEL")
        sequential_basic = [
            "from tensorflow import keras",
            "from tensorflow.keras import layers",
            "",
            "# Method 1: Add layers one by one",
            "model = keras.Sequential()",
            "model.add(layers.Dense(64, activation='relu', input_shape=(784,)))",
            "model.add(layers.Dropout(0.2))",
            "model.add(layers.Dense(32, activation='relu'))",
            "model.add(layers.Dense(10, activation='softmax'))",
            "",
            "# Method 2: Pass layers as list",
            "model = keras.Sequential([",
            "    layers.Dense(64, activation='relu', input_shape=(784,)),",
            "    layers.Dropout(0.2),",
            "    layers.Dense(32, activation='relu'),",
            "    layers.Dense(10, activation='softmax')",
            "])",
            "",
            "# Model summary",
            "model.summary()"
        ]
        
        for line in sequential_basic:
            print(f"   {line}")
            
        print("\n2. CONVOLUTIONAL NEURAL NETWORK")
        cnn_example = [
            "# CNN for image classification",
            "cnn_model = keras.Sequential([",
            "    layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),",
            "    layers.MaxPooling2D((2, 2)),",
            "    layers.Conv2D(64, (3, 3), activation='relu'),",
            "    layers.MaxPooling2D((2, 2)),",
            "    layers.Conv2D(64, (3, 3), activation='relu'),",
            "    ",
            "    layers.Flatten(),",
            "    layers.Dense(64, activation='relu'),",
            "    layers.Dropout(0.2),",
            "    layers.Dense(10, activation='softmax')",
            "])"
        ]
        
        for line in cnn_example:
            print(f"   {line}")
            
        print("\n3. RECURRENT NEURAL NETWORK")
        rnn_example = [
            "# RNN for sequence data",
            "rnn_model = keras.Sequential([",
            "    layers.Embedding(vocab_size, 64, input_length=max_length),",
            "    layers.LSTM(64, dropout=0.2, recurrent_dropout=0.2),",
            "    layers.Dense(32, activation='relu'),",
            "    layers.Dense(1, activation='sigmoid')",
            "])",
            "",
            "# Bidirectional RNN",
            "bi_rnn_model = keras.Sequential([",
            "    layers.Embedding(vocab_size, 64),",
            "    layers.Bidirectional(layers.LSTM(64)),",
            "    layers.Dense(1, activation='sigmoid')",
            "])"
        ]
        
        for line in rnn_example:
            print(f"   {line}")
    
    @staticmethod
    def functional_api():
        """Show Functional API patterns for complex architectures."""
        print("\n" + "="*50)
        print("KERAS FUNCTIONAL API")
        print("="*50)
        
        print("\n1. BASIC FUNCTIONAL MODEL")
        functional_basic = [
            "from tensorflow.keras import Input, Model",
            "",
            "# Define input",
            "inputs = Input(shape=(784,))",
            "",
            "# Define layers",
            "x = layers.Dense(64, activation='relu')(inputs)",
            "x = layers.Dropout(0.2)(x)",
            "x = layers.Dense(32, activation='relu')(x)",
            "outputs = layers.Dense(10, activation='softmax')(x)",
            "",
            "# Create model",
            "model = Model(inputs=inputs, outputs=outputs)"
        ]
        
        for line in functional_basic:
            print(f"   {line}")
            
        print("\n2. MULTI-INPUT MODEL")
        multi_input = [
            "# Multiple inputs",
            "text_input = Input(shape=(100,), name='text')",
            "image_input = Input(shape=(28, 28, 1), name='image')",
            "",
            "# Process text",
            "text_features = layers.Embedding(vocab_size, 64)(text_input)",
            "text_features = layers.LSTM(32)(text_features)",
            "",
            "# Process image", 
            "image_features = layers.Conv2D(32, 3, activation='relu')(image_input)",
            "image_features = layers.GlobalMaxPooling2D()(image_features)",
            "",
            "# Combine features",
            "combined = layers.concatenate([text_features, image_features])",
            "outputs = layers.Dense(1, activation='sigmoid')(combined)",
            "",
            "model = Model(inputs=[text_input, image_input], outputs=outputs)"
        ]
        
        for line in multi_input:
            print(f"   {line}")
            
        print("\n3. MULTI-OUTPUT MODEL")
        multi_output = [
            "# Shared input",
            "inputs = Input(shape=(784,))",
            "",
            "# Shared layers",
            "shared = layers.Dense(64, activation='relu')(inputs)",
            "shared = layers.Dropout(0.2)(shared)",
            "",
            "# Multiple outputs",
            "classification_output = layers.Dense(10, activation='softmax', name='classification')(shared)",
            "regression_output = layers.Dense(1, name='regression')(shared)",
            "",
            "model = Model(inputs=inputs, outputs=[classification_output, regression_output])"
        ]
        
        for line in multi_output:
            print(f"   {line}")
    
    @staticmethod
    def model_subclassing():
        """Show custom model creation through subclassing."""
        print("\n" + "="*50)
        print("CUSTOM MODELS WITH SUBCLASSING")
        print("="*50)
        
        custom_model = [
            "class CustomModel(keras.Model):",
            "    def __init__(self, num_classes=10):",
            "        super(CustomModel, self).__init__()",
            "        self.dense1 = layers.Dense(32, activation='relu')",
            "        self.dense2 = layers.Dense(64, activation='relu')",
            "        self.dropout = layers.Dropout(0.2)",
            "        self.classifier = layers.Dense(num_classes, activation='softmax')",
            "    ",
            "    def call(self, inputs, training=None):",
            "        x = self.dense1(inputs)",
            "        x = self.dense2(x)",
            "        if training:",
            "            x = self.dropout(x)",
            "        return self.classifier(x)",
            "",
            "# Usage",
            "model = CustomModel(num_classes=10)",
            "model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])"
        ]
        
        for line in custom_model:
            print(f"   {line}")

class KerasTrainingAndOptimization:
    """Comprehensive training, optimization, and callbacks."""
    
    @staticmethod
    def model_compilation():
        """Show model compilation options."""
        print("\n" + "="*50)
        print("MODEL COMPILATION")
        print("="*50)
        
        print("\n1. OPTIMIZERS")
        optimizers_examples = [
            "# Common optimizers",
            "model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])",
            "model.compile(optimizer='sgd', loss='mse', metrics=['mae'])",
            "model.compile(optimizer='rmsprop', loss='binary_crossentropy', metrics=['accuracy'])",
            "",
            "# Custom optimizer parameters",
            "from tensorflow.keras.optimizers import Adam, SGD, RMSprop",
            "model.compile(optimizer=Adam(learning_rate=0.001), loss='sparse_categorical_crossentropy')",
            "model.compile(optimizer=SGD(learning_rate=0.01, momentum=0.9), loss='mse')",
            "model.compile(optimizer=RMSprop(learning_rate=0.001, rho=0.9), loss='binary_crossentropy')"
        ]
        
        for line in optimizers_examples:
            print(f"   {line}")
            
        print("\n2. LOSS FUNCTIONS")
        loss_functions = [
            "# Classification losses",
            "'categorical_crossentropy'      # One-hot encoded labels",
            "'sparse_categorical_crossentropy'  # Integer labels",  
            "'binary_crossentropy'          # Binary classification",
            "",
            "# Regression losses",
            "'mean_squared_error' or 'mse'  # L2 loss",
            "'mean_absolute_error' or 'mae'  # L1 loss",
            "'huber_loss'                   # Robust loss",
            "",
            "# Custom loss function",
            "def custom_loss(y_true, y_pred):",
            "    return tf.reduce_mean(tf.square(y_true - y_pred))",
            "",
            "model.compile(optimizer='adam', loss=custom_loss)"
        ]
        
        for line in loss_functions:
            print(f"   {line}")
            
        print("\n3. METRICS")
        metrics_examples = [
            "# Built-in metrics",
            "['accuracy']                   # Classification accuracy",
            "['mae', 'mse']                # Regression metrics",
            "['precision', 'recall']       # Classification metrics",
            "['auc']                       # Area under ROC curve",
            "",
            "# Custom metrics",
            "def f1_score(y_true, y_pred):",
            "    # Implementation of F1 score",
            "    pass",
            "",
            "model.compile(optimizer='adam', loss='binary_crossentropy', metrics=[f1_score])"
        ]
        
        for line in metrics_examples:
            print(f"   {line}")
    
    @staticmethod
    def training_callbacks():
        """Show training callbacks for monitoring and control."""
        print("\n" + "="*50)
        print("TRAINING CALLBACKS")
        print("="*50)
        
        callbacks_examples = [
            "from tensorflow.keras.callbacks import (",
            "    EarlyStopping, ModelCheckpoint, ReduceLROnPlateau,",
            "    TensorBoard, CSVLogger, LambdaCallback",
            ")",
            "",
            "# Early stopping",
            "early_stopping = EarlyStopping(",
            "    monitor='val_loss',",
            "    patience=5,",
            "    restore_best_weights=True",
            ")",
            "",
            "# Model checkpoint",
            "checkpoint = ModelCheckpoint(",
            "    'best_model.h5',",
            "    monitor='val_accuracy',",
            "    save_best_only=True,",
            "    mode='max'",
            ")",
            "",
            "# Learning rate reduction",
            "lr_reduction = ReduceLROnPlateau(",
            "    monitor='val_loss',",
            "    factor=0.2,",
            "    patience=3,",
            "    min_lr=0.0001",
            ")",
            "",
            "# TensorBoard logging",
            "tensorboard = TensorBoard(log_dir='./logs', histogram_freq=1)",
            "",
            "# CSV logger",
            "csv_logger = CSVLogger('training.log')",
            "",
            "# Custom callback",
            "def on_epoch_end(epoch, logs):",
            "    print(f'Epoch {epoch}: loss = {logs[\"loss\"]:.4f}')",
            "",
            "custom_callback = LambdaCallback(on_epoch_end=on_epoch_end)",
            "",
            "# Use callbacks in training",
            "callbacks = [early_stopping, checkpoint, lr_reduction, tensorboard]",
            "model.fit(X_train, y_train, validation_data=(X_val, y_val), callbacks=callbacks)"
        ]
        
        for line in callbacks_examples:
            print(f"   {line}")
    
    @staticmethod
    def training_techniques():
        """Show advanced training techniques."""
        print("\n" + "="*50)
        print("ADVANCED TRAINING TECHNIQUES")
        print("="*50)
        
        print("\n1. DATA AUGMENTATION")
        data_augmentation = [
            "from tensorflow.keras.preprocessing.image import ImageDataGenerator",
            "",
            "# Image data augmentation",
            "datagen = ImageDataGenerator(",
            "    rotation_range=20,",
            "    width_shift_range=0.2,",
            "    height_shift_range=0.2,",
            "    horizontal_flip=True,",
            "    zoom_range=0.2",
            ")",
            "",
            "# Fit and generate augmented data",
            "datagen.fit(X_train)",
            "model.fit(datagen.flow(X_train, y_train, batch_size=32),",
            "          epochs=50, validation_data=(X_val, y_val))",
            "",
            "# Built-in Keras preprocessing layers (TF 2.x)",
            "data_augmentation = keras.Sequential([",
            "    layers.experimental.preprocessing.RandomFlip('horizontal'),",
            "    layers.experimental.preprocessing.RandomRotation(0.1),",
            "    layers.experimental.preprocessing.RandomZoom(0.1),",
            "])"
        ]
        
        for line in data_augmentation:
            print(f"   {line}")
            
        print("\n2. REGULARIZATION")
        regularization = [
            "# Dropout",
            "model.add(layers.Dropout(0.2))",
            "",
            "# L1 and L2 regularization",
            "from tensorflow.keras.regularizers import l1, l2, l1_l2",
            "",
            "model.add(layers.Dense(64, activation='relu', kernel_regularizer=l2(0.01)))",
            "model.add(layers.Dense(64, activation='relu', kernel_regularizer=l1(0.01)))",
            "model.add(layers.Dense(64, activation='relu', kernel_regularizer=l1_l2(l1=0.01, l2=0.01)))",
            "",
            "# Batch normalization",
            "model.add(layers.BatchNormalization())",
            "",
            "# Early stopping (form of regularization)",
            "early_stopping = EarlyStopping(monitor='val_loss', patience=5)"
        ]
        
        for line in regularization:
            print(f"   {line}")
            
        print("\n3. TRANSFER LEARNING")
        transfer_learning = [
            "from tensorflow.keras.applications import VGG16, ResNet50, MobileNet",
            "",
            "# Load pre-trained model",
            "base_model = VGG16(",
            "    weights='imagenet',  # Pre-trained on ImageNet",
            "    include_top=False,   # Exclude final classification layer",
            "    input_shape=(224, 224, 3)",
            ")",
            "",
            "# Freeze base model",
            "base_model.trainable = False",
            "",
            "# Add custom classification head",
            "model = keras.Sequential([",
            "    base_model,",
            "    layers.GlobalAveragePooling2D(),",
            "    layers.Dense(128, activation='relu'),",
            "    layers.Dropout(0.2),",
            "    layers.Dense(num_classes, activation='softmax')",
            "])",
            "",
            "# Fine-tuning: Unfreeze and train with low learning rate",
            "base_model.trainable = True",
            "model.compile(optimizer=Adam(learning_rate=0.0001/10), loss='categorical_crossentropy')"
        ]
        
        for line in transfer_learning:
            print(f"   {line}")

class TensorFlowDataPipeline:
    """TensorFlow data loading and preprocessing."""
    
    @staticmethod
    def tf_data_examples():
        """Show tf.data pipeline examples."""
        print("\n" + "="*50)
        print("TENSORFLOW DATA PIPELINES")
        print("="*50)
        
        print("\n1. BASIC tf.data USAGE")
        basic_data = [
            "import tensorflow as tf",
            "",
            "# From numpy arrays",
            "dataset = tf.data.Dataset.from_tensor_slices((X_train, y_train))",
            "",
            "# From Python generator",
            "def data_generator():",
            "    for i in range(1000):",
            "        yield (np.random.random((28, 28)), np.random.randint(0, 10))",
            "",
            "dataset = tf.data.Dataset.from_generator(",
            "    data_generator,",
            "    output_signature=(",
            "        tf.TensorSpec(shape=(28, 28), dtype=tf.float32),",
            "        tf.TensorSpec(shape=(), dtype=tf.int32)",
            "    )",
            ")",
            "",
            "# From files",
            "dataset = tf.data.Dataset.list_files('path/to/images/*.jpg')"
        ]
        
        for line in basic_data:
            print(f"   {line}")
            
        print("\n2. DATA PREPROCESSING")
        preprocessing = [
            "# Basic transformations",
            "dataset = dataset.map(lambda x, y: (tf.cast(x, tf.float32) / 255.0, y))",
            "dataset = dataset.batch(32)",
            "dataset = dataset.shuffle(buffer_size=1000)",
            "dataset = dataset.prefetch(tf.data.AUTOTUNE)",
            "",
            "# Image preprocessing",
            "def preprocess_image(image_path, label):",
            "    image = tf.io.read_file(image_path)",
            "    image = tf.image.decode_image(image, channels=3)",
            "    image = tf.image.resize(image, [224, 224])",
            "    image = tf.cast(image, tf.float32) / 255.0",
            "    return image, label",
            "",
            "dataset = dataset.map(preprocess_image, num_parallel_calls=tf.data.AUTOTUNE)",
            "",
            "# Text preprocessing",
            "def preprocess_text(text, label):",
            "    text = tf.strings.lower(text)",
            "    text = tf.strings.regex_replace(text, '[^a-z ]', '')",
            "    return text, label"
        ]
        
        for line in preprocessing:
            print(f"   {line}")
            
        print("\n3. ADVANCED DATA OPERATIONS")
        advanced_ops = [
            "# Data augmentation in pipeline",
            "def augment_image(image, label):",
            "    image = tf.image.random_flip_left_right(image)",
            "    image = tf.image.random_brightness(image, 0.2)",
            "    image = tf.image.random_contrast(image, 0.8, 1.2)",
            "    return image, label",
            "",
            "train_dataset = train_dataset.map(augment_image)",
            "",
            "# Caching and performance",
            "dataset = dataset.cache()  # Cache dataset in memory/disk",
            "dataset = dataset.prefetch(tf.data.AUTOTUNE)  # Prefetch next batch",
            "",
            "# Parallel processing",
            "dataset = dataset.map(preprocess_fn, num_parallel_calls=tf.data.AUTOTUNE)",
            "",
            "# Windowing for time series",
            "def window_dataset(series, window_size, batch_size):",
            "    dataset = tf.data.Dataset.from_tensor_slices(series)",
            "    dataset = dataset.window(window_size + 1, shift=1, drop_remainder=True)",
            "    dataset = dataset.flat_map(lambda w: w.batch(window_size + 1))",
            "    dataset = dataset.map(lambda w: (w[:-1], w[-1]))",
            "    return dataset.batch(batch_size).prefetch(1)"
        ]
        
        for line in advanced_ops:
            print(f"   {line}")

class AdvancedTensorFlowTechniques:
    """Advanced TensorFlow/Keras techniques and applications."""
    
    @staticmethod
    def computer_vision_examples():
        """Show computer vision specific techniques."""
        print("\n" + "="*50)
        print("COMPUTER VISION WITH TENSORFLOW")
        print("="*50)
        
        print("\n1. OBJECT DETECTION SETUP")
        object_detection = [
            "# Using pre-trained models for object detection",
            "import tensorflow_hub as hub",
            "",
            "# Load pre-trained object detection model",
            "detector = hub.load('https://tfhub.dev/tensorflow/ssd_mobilenet_v2/2')",
            "",
            "# Object detection function",
            "def detect_objects(image):",
            "    converted_img = tf.image.convert_image_dtype(image, tf.uint8)[tf.newaxis, ...]",
            "    result = detector(converted_img)",
            "    return result",
            "",
            "# YOLO-style detection (custom implementation)",
            "class YOLOLayer(layers.Layer):",
            "    def __init__(self, anchors, num_classes):",
            "        super(YOLOLayer, self).__init__()",
            "        self.anchors = anchors",
            "        self.num_classes = num_classes",
            "    ",
            "    def call(self, inputs):",
            "        # YOLO detection logic here",
            "        return outputs"
        ]
        
        for line in object_detection:
            print(f"   {line}")
            
        print("\n2. IMAGE SEGMENTATION")
        segmentation = [
            "# U-Net for image segmentation",
            "def unet_model(input_shape):",
            "    inputs = Input(input_shape)",
            "    ",
            "    # Encoder (Contracting path)",
            "    c1 = layers.Conv2D(64, 3, activation='relu', padding='same')(inputs)",
            "    c1 = layers.Conv2D(64, 3, activation='relu', padding='same')(c1)",
            "    p1 = layers.MaxPooling2D(2)(c1)",
            "    ",
            "    c2 = layers.Conv2D(128, 3, activation='relu', padding='same')(p1)",
            "    c2 = layers.Conv2D(128, 3, activation='relu', padding='same')(c2)",
            "    p2 = layers.MaxPooling2D(2)(c2)",
            "    ",
            "    # Bottleneck",
            "    c3 = layers.Conv2D(256, 3, activation='relu', padding='same')(p2)",
            "    c3 = layers.Conv2D(256, 3, activation='relu', padding='same')(c3)",
            "    ",
            "    # Decoder (Expanding path)",
            "    u4 = layers.Conv2DTranspose(128, 2, strides=2, padding='same')(c3)",
            "    u4 = layers.concatenate([u4, c2])",
            "    c4 = layers.Conv2D(128, 3, activation='relu', padding='same')(u4)",
            "    ",
            "    u5 = layers.Conv2DTranspose(64, 2, strides=2, padding='same')(c4)",
            "    u5 = layers.concatenate([u5, c1])",
            "    c5 = layers.Conv2D(64, 3, activation='relu', padding='same')(u5)",
            "    ",
            "    outputs = layers.Conv2D(1, 1, activation='sigmoid')(c5)",
            "    ",
            "    return Model(inputs, outputs)"
        ]
        
        for line in segmentation:
            print(f"   {line}")
    
    @staticmethod
    def nlp_examples():
        """Show NLP specific techniques."""
        print("\n" + "="*50)
        print("NATURAL LANGUAGE PROCESSING")
        print("="*50)
        
        print("\n1. TEXT PREPROCESSING")
        text_preprocessing = [
            "from tensorflow.keras.preprocessing.text import Tokenizer",
            "from tensorflow.keras.preprocessing.sequence import pad_sequences",
            "",
            "# Tokenization",
            "tokenizer = Tokenizer(num_words=10000, oov_token='<OOV>')",
            "tokenizer.fit_on_texts(train_texts)",
            "",
            "# Convert text to sequences",
            "train_sequences = tokenizer.texts_to_sequences(train_texts)",
            "test_sequences = tokenizer.texts_to_sequences(test_texts)",
            "",
            "# Pad sequences",
            "max_length = 100",
            "train_padded = pad_sequences(train_sequences, maxlen=max_length, padding='post')",
            "test_padded = pad_sequences(test_sequences, maxlen=max_length, padding='post')",
            "",
            "# Word embeddings",
            "vocab_size = len(tokenizer.word_index) + 1",
            "embedding_dim = 100",
            "",
            "model = keras.Sequential([",
            "    layers.Embedding(vocab_size, embedding_dim, input_length=max_length),",
            "    layers.LSTM(64),",
            "    layers.Dense(1, activation='sigmoid')",
            "])"
        ]
        
        for line in text_preprocessing:
            print(f"   {line}")
            
        print("\n2. TRANSFORMER ARCHITECTURE")
        transformer = [
            "# Multi-head attention layer",
            "class MultiHeadAttention(layers.Layer):",
            "    def __init__(self, d_model, num_heads):",
            "        super(MultiHeadAttention, self).__init__()",
            "        self.num_heads = num_heads",
            "        self.d_model = d_model",
            "        ",
            "        self.depth = d_model // num_heads",
            "        ",
            "        self.wq = layers.Dense(d_model)",
            "        self.wk = layers.Dense(d_model)",
            "        self.wv = layers.Dense(d_model)",
            "        self.dense = layers.Dense(d_model)",
            "    ",
            "    def split_heads(self, x, batch_size):",
            "        x = tf.reshape(x, (batch_size, -1, self.num_heads, self.depth))",
            "        return tf.transpose(x, perm=[0, 2, 1, 3])",
            "",
            "# Transformer block",
            "def transformer_block(inputs, head_size, num_heads, ff_dim, dropout=0):",
            "    # Attention and Normalization",
            "    attention_layer = layers.MultiHeadAttention(",
            "        key_dim=head_size, num_heads=num_heads, dropout=dropout",
            "    )",
            "    attention_output = attention_layer(inputs, inputs)",
            "    attention_output = layers.Dropout(dropout)(attention_output)",
            "    attention_output = layers.LayerNormalization(epsilon=1e-6)(inputs + attention_output)",
            "    ",
            "    # Feed Forward Network",
            "    ffn = keras.Sequential([",
            "        layers.Dense(ff_dim, activation='relu'),",
            "        layers.Dense(inputs.shape[-1]),",
            "    ])",
            "    ffn_output = ffn(attention_output)",
            "    ffn_output = layers.Dropout(dropout)(ffn_output)",
            "    return layers.LayerNormalization(epsilon=1e-6)(attention_output + ffn_output)"
        ]
        
        for line in transformer:
            print(f"   {line}")
    
    @staticmethod
    def generative_models():
        """Show generative model examples."""
        print("\n" + "="*50)
        print("GENERATIVE MODELS")
        print("="*50)
        
        print("\n1. AUTOENCODER")
        autoencoder = [
            "# Basic Autoencoder",
            "def build_autoencoder(input_dim, encoding_dim):",
            "    # Encoder",
            "    input_layer = Input(shape=(input_dim,))",
            "    encoded = layers.Dense(encoding_dim, activation='relu')(input_layer)",
            "    ",
            "    # Decoder", 
            "    decoded = layers.Dense(input_dim, activation='sigmoid')(encoded)",
            "    ",
            "    # Autoencoder model",
            "    autoencoder = Model(input_layer, decoded)",
            "    ",
            "    # Encoder model",
            "    encoder = Model(input_layer, encoded)",
            "    ",
            "    return autoencoder, encoder",
            "",
            "# Variational Autoencoder (VAE)",
            "class VAE(keras.Model):",
            "    def __init__(self, latent_dim):",
            "        super(VAE, self).__init__()",
            "        self.latent_dim = latent_dim",
            "        self.encoder = keras.Sequential([",
            "            layers.Dense(512, activation='relu'),",
            "            layers.Dense(256, activation='relu'),",
            "            layers.Dense(latent_dim * 2)  # mean and log_var",
            "        ])",
            "        self.decoder = keras.Sequential([",
            "            layers.Dense(256, activation='relu'),",
            "            layers.Dense(512, activation='relu'),",
            "            layers.Dense(784, activation='sigmoid')",
            "        ])"
        ]
        
        for line in autoencoder:
            print(f"   {line}")
            
        print("\n2. GENERATIVE ADVERSARIAL NETWORK (GAN)")
        gan = [
            "# Generator",
            "def build_generator(latent_dim):",
            "    model = keras.Sequential([",
            "        layers.Dense(256, input_dim=latent_dim),",
            "        layers.LeakyReLU(alpha=0.2),",
            "        layers.Dense(512),",
            "        layers.LeakyReLU(alpha=0.2),",
            "        layers.Dense(1024),",
            "        layers.LeakyReLU(alpha=0.2),",
            "        layers.Dense(784, activation='tanh')",
            "        layers.Reshape((28, 28, 1))",
            "    ])",
            "    return model",
            "",
            "# Discriminator",
            "def build_discriminator():",
            "    model = keras.Sequential([",
            "        layers.Flatten(input_shape=(28, 28, 1)),",
            "        layers.Dense(512),",
            "        layers.LeakyReLU(alpha=0.2),",
            "        layers.Dense(256),",
            "        layers.LeakyReLU(alpha=0.2),",
            "        layers.Dense(1, activation='sigmoid')",
            "    ])",
            "    return model",
            "",
            "# GAN training loop",
            "def train_gan(generator, discriminator, dataset, epochs):",
            "    for epoch in range(epochs):",
            "        for batch in dataset:",
            "            # Train discriminator",
            "            with tf.GradientTape() as disc_tape:",
            "                # Discriminator loss calculation",
            "                pass",
            "            ",
            "            # Train generator", 
            "            with tf.GradientTape() as gen_tape:",
            "                # Generator loss calculation",
            "                pass"
        ]
        
        for line in gan:
            print(f"   {line}")

def create_tensorflow_cheat_sheet():
    """Create a comprehensive TensorFlow/Keras cheat sheet."""
    print("\n" + "="*70)
    print("TENSORFLOW & KERAS COMPREHENSIVE CHEAT SHEET")
    print("="*70)
    
    sections = {
        "ESSENTIAL IMPORTS": [
            "import tensorflow as tf",
            "from tensorflow import keras",
            "from tensorflow.keras import layers, models, optimizers, losses, metrics",
            "from tensorflow.keras.preprocessing.image import ImageDataGenerator",
            "from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint"
        ],
        
        "BASIC WORKFLOW": [
            "# 1. Data preparation",
            "train_dataset = tf.data.Dataset.from_tensor_slices((X_train, y_train))",
            "train_dataset = train_dataset.batch(32).prefetch(tf.data.AUTOTUNE)",
            "",
            "# 2. Model creation", 
            "model = keras.Sequential([",
            "    layers.Dense(64, activation='relu', input_shape=(input_dim,)),",
            "    layers.Dropout(0.2),",
            "    layers.Dense(num_classes, activation='softmax')",
            "])",
            "",
            "# 3. Compilation",
            "model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])",
            "",
            "# 4. Training",
            "history = model.fit(train_dataset, epochs=50, validation_data=val_dataset)",
            "",
            "# 5. Evaluation",
            "test_loss, test_accuracy = model.evaluate(test_dataset)"
        ],
        
        "COMMON ARCHITECTURES": [
            "# CNN for images",
            "layers.Conv2D(32, 3, activation='relu')",
            "layers.MaxPooling2D()",
            "layers.Flatten()",
            "",
            "# RNN for sequences",
            "layers.LSTM(64, return_sequences=True)",
            "layers.GRU(32)",
            "layers.SimpleRNN(16)",
            "",
            "# Attention mechanisms",
            "layers.MultiHeadAttention(key_dim=64, num_heads=8)",
            "",
            "# Regularization",
            "layers.Dropout(0.2)",
            "layers.BatchNormalization()",
            "kernel_regularizer=l2(0.01)"
        ],
        
        "PERFORMANCE TIPS": [
            "# Use tf.data for efficient data loading",
            "# Prefetch data with tf.data.AUTOTUNE",
            "# Use mixed precision training for faster training",
            "# Implement gradient accumulation for large batches",
            "# Use tf.function decorator for graph compilation",
            "# Cache datasets when data fits in memory",
            "# Use callbacks for training control",
            "# Implement custom training loops for complex scenarios"
        ]
    }
    
    for section, content in sections.items():
        print(f"\n{section}:")
        print("-" * len(section))
        for line in content:
            print(f"   {line}")

def main():
    """Main function to demonstrate all TensorFlow/Keras concepts."""
    print("TENSORFLOW & KERAS COMPREHENSIVE GUIDE")
    print("=" * 70)
    print("This module covers all major aspects of TensorFlow/Keras for deep learning")
    print("To run actual code, install: pip install tensorflow numpy matplotlib")
    
    demonstrate_tensorflow_basics()
    TensorFlowFundamentals.tensor_operations()
    KerasModelBuilding.sequential_models()
    KerasModelBuilding.functional_api()
    KerasModelBuilding.model_subclassing()
    KerasTrainingAndOptimization.model_compilation()
    KerasTrainingAndOptimization.training_callbacks()
    KerasTrainingAndOptimization.training_techniques()
    TensorFlowDataPipeline.tf_data_examples()
    AdvancedTensorFlowTechniques.computer_vision_examples()
    AdvancedTensorFlowTechniques.nlp_examples()
    AdvancedTensorFlowTechniques.generative_models()
    create_tensorflow_cheat_sheet()
    
    print(f"\n{'='*70}")
    print("NEXT STEPS:")
    print("1. Install TensorFlow: pip install tensorflow")
    print("2. Practice with TensorFlow datasets: tensorflow_datasets")
    print("3. Explore TensorFlow Hub for pre-trained models")
    print("4. Check TensorFlow documentation: https://www.tensorflow.org/")
    print("5. Try Google Colab for free GPU/TPU training")

if __name__ == "__main__":
    main()
