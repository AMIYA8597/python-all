# Comprehensive Glossary of Python, DSA, ML, and AI

This glossary serves as a central dictionary for all technical terms you will encounter while traversing the Python-DSA-AI-Master repository.

## Python Core

* **CPython**: The default, most widely used implementation of the Python programming language, written in C.
* **Decorator**: A design pattern in Python that allows a user to add new functionality to an existing object without modifying its structure.
* **Duck Typing**: A concept related to dynamic typing, where the type or the class of an object is less important than the methods it defines ("If it walks like a duck and quacks like a duck, it is a duck").
* **Generator**: A function that returns an iterator that produces a sequence of values when iterated over. Uses the `yield` keyword.
* **GIL (Global Interpreter Lock)**: A mutex that protects access to Python objects, preventing multiple threads from executing Python bytecodes at once.
* **List Comprehension**: An elegant way to define and create lists based on existing lists.
* **Metaclass**: A class whose instances are classes.
* **Monkey Patching**: Dynamic modifications of a class or module at runtime.
* **Pickling**: The process whereby a Python object hierarchy is converted into a byte stream.

## Data Structures & Algorithms (DSA)

* **Adjacency List**: A collection of unordered lists used to represent a finite graph. Each list describes the set of neighbors of a vertex in the graph.
* **AVL Tree**: A self-balancing binary search tree where the difference between heights of left and right subtrees cannot be more than one for all nodes.
* **BFS (Breadth-First Search)**: An algorithm for searching a tree data structure for a node that satisfies a given property. Starts at the tree root and explores all nodes at the present depth prior to moving on to the nodes at the next depth level.
* **Big O Notation**: Mathematical notation that describes the limiting behavior of a function when the argument tends towards a particular value or infinity. Used to classify algorithms according to how their run time or space requirements grow as the input size grows.
* **Bipartite Graph**: A graph whose vertices can be divided into two disjoint and independent sets.
* **DFS (Depth-First Search)**: An algorithm for traversing or searching tree or graph data structures. Starts at the root node and explores as far as possible along each branch before backtracking.
* **Dynamic Programming (DP)**: A method for solving a complex problem by breaking it down into a collection of simpler subproblems, solving each of those subproblems just once, and storing their solutions using a memory-based data structure (array, map,etc).
* **Hash Table**: A data structure that implements an associative array abstract data type, a structure that can map keys to values. Uses a hash function to compute an index.
* **Heap**: A specialized tree-based data structure which is essentially an almost complete tree that satisfies the heap property.
* **Memoization**: An optimization technique used primarily to speed up computer programs by storing the results of expensive function calls.
* **Trie**: A type of k-ary search tree, a tree data structure used for locating specific keys from within a set.

## Machine Learning (ML)

* **Bias-Variance Tradeoff**: The property of a set of predictive models whereby models with a lower bias in parameter estimation have a higher variance of the parameter estimates across samples, and vice versa.
* **Cross-Validation**: A resampling procedure used to evaluate machine learning models on a limited data sample.
* **Ensemble Learning**: A machine learning paradigm where multiple models (often called "weak learners") are trained to solve the same problem and combined to get better results.
* **Gradient Descent**: A first-order iterative optimization algorithm for finding a local minimum of a differentiable function.
* **Hyperparameter**: A parameter whose value is used to control the learning process. By contrast, the values of other parameters (typically node weights) are derived via training.
* **Overfitting**: The production of an analysis that corresponds too closely or exactly to a particular set of data, and may therefore fail to fit additional data or predict future observations reliably.
* **Random Forest**: An ensemble learning method for classification, regression and other tasks that operates by constructing a multitude of decision trees at training time.
* **Support Vector Machine (SVM)**: Supervised learning models with associated learning algorithms that analyze data for classification and regression analysis.
* **Underfitting**: When a statistical model or a machine learning algorithm cannot capture the underlying trend of the data.

## Artificial Intelligence & Generative AI

* **Attention Mechanism**: A technique that mimics cognitive attention. The effect enhances some parts of the input data while diminishing other parts — the thought being that the network should devote more focus to the small, but important, parts of the data.
* **Backpropagation**: A widely used algorithm for training feedforward neural networks. It computes the gradient of the loss function with respect to the weights of the network.
* **Convolutional Neural Network (CNN)**: A class of artificial neural network, most commonly applied to analyze visual imagery.
* **Embedding**: A relatively low-dimensional space into which you can translate high-dimensional vectors. Embeddings make it easier to do machine learning on large inputs like sparse vectors representing words.
* **Fine-Tuning**: An approach to transfer learning in which the weights of a pre-trained model are trained on new data.
* **Large Language Model (LLM)**: A language model consisting of a neural network with many parameters, trained on large quantities of unlabeled text using self-supervised learning or semi-supervised learning.
* **Prompt Engineering**: The process of structuring text that can be interpreted and understood by a generative AI model.
* **Retrieval-Augmented Generation (RAG)**: An AI framework for retrieving facts from an external knowledge base to ground large language models (LLMs) on the most accurate, up-to-date information and to give users insight into LLMs' generative process.
* **Transformer**: A deep learning architecture based on the attention mechanism, proposed in a 2017 paper "Attention Is All You Need".
* **Vector Database**: A database designed to store, manage and index massive quantities of high-dimensional vector data efficiently.

---
*Note: This glossary is a living document. Add to it as you discover new concepts across the repository.*
