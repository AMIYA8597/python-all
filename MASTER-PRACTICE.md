# Master Practice Hub

This document serves as the central hub for practicing concepts learned in the repository. Theory is useless without deliberate practice.

## Daily Practice Routine

1.  **Anki Review (15 mins)**: Review flashcards for syntax, definitions, and algorithmic patterns.
2.  **Algorithmic Warmup (30 mins)**: Solve 1 Easy and 1 Medium DSA problem related to the current topic.
3.  **Core Learning/Coding (90 mins)**: Read theory, write implementation code, or work on a project.
4.  **Debugging/Refactoring (30 mins)**: Review yesterday's code, add tests, or optimize it.

## 1. Python Practice

*   **Syntax & Basics**: Complete exercises in `Phase1-Python/practice/basics/`.
*   **OOP**: Build the "Library Management System" (see Project Map). Focus on clean class design.
*   **Concurrency**: Write a web scraper that fetches URLs synchronously, then refactor it using `threading`, and finally using `asyncio`. Compare the execution times.
*   **Recommended External Site**: [Exercism Python Track](https://exercism.org/tracks/python)

## 2. DSA Practice (LeetCode Mapping)

Focus on *patterns*, not just solving random problems.

| Pattern | Easy | Medium | Hard |
| :--- | :--- | :--- | :--- |
| **Two Pointers** | Valid Palindrome | 3Sum | Trapping Rain Water |
| **Sliding Window** | Best Time to Buy/Sell Stock | Longest Substring Without Repeating Chars | Minimum Window Substring |
| **Fast & Slow Pointers**| Linked List Cycle | Find the Duplicate Number | - |
| **Merge Intervals** | - | Merge Intervals | Insert Interval |
| **Cyclic Sort** | Missing Number | Find All Duplicates | First Missing Positive |
| **In-place Reversal** | Reverse Linked List | Reverse Linked List II | Reverse Nodes in k-Group |
| **BFS (Trees)** | Level Order Traversal | Binary Tree Right Side View | - |
| **DFS (Trees)** | Maximum Depth | Lowest Common Ancestor | Binary Tree Maximum Path Sum |
| **Two Heaps** | - | Find Median from Data Stream | Sliding Window Median |
| **Subsets (Backtracking)**| - | Subsets, Permutations | N-Queens |
| **Binary Search** | Binary Search | Search in Rotated Sorted Array | Median of Two Sorted Arrays |
| **Top 'K' Elements** | Kth Largest Element | Top K Frequent Elements | Merge K Sorted Lists |
| **DP (1D)** | Climbing Stairs | Coin Change | Word Break |
| **DP (2D)** | Unique Paths | Longest Common Subsequence | Edit Distance |
| **Graphs** | Number of Islands | Clone Graph | Alien Dictionary |

## 3. Machine Learning Practice

*   **Data Wrangling**: Use the Titanic Dataset on Kaggle. Focus purely on EDA and Feature Engineering.
*   **Model Building**: Predict housing prices. Compare Linear Regression, Random Forest, and XGBoost.
*   **Hyperparameter Tuning**: Use GridSearch and RandomSearch on the above model.
*   **Recommended External Site**: [Kaggle Competitions (Playground Series)](https://www.kaggle.com/competitions)

## 4. Generative AI Practice

*   **API Interactions**: Write a script to chat with the OpenAI/Anthropic API.
*   **Prompt Engineering**: Try to get an LLM to output a specific JSON format purely through prompting.
*   **RAG Implementation**: Build a script that reads a PDF, chunks it, stores it in ChromaDB, and answers questions using LangChain.
*   **Recommended External Site**: [Hugging Face Tasks](https://huggingface.co/tasks)
