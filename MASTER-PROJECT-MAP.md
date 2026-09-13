# Master Project Map

This document indexes all recommended projects across the curriculum, categorized by difficulty and domain. Completing projects is the only way to synthesize your knowledge.

## Level 1: Beginner (Foundational Syntax & Logic)

*Focus: Core Python, basic data structures, simple control flow.*

*   **[CLI] Password Generator & Manager**: A command-line tool to generate secure passwords and save them to a local, encrypted file.
*   **[CLI] Terminal Tic-Tac-Toe**: A simple game played in the terminal to practice arrays, loops, and win-condition logic.
*   **[Data] Weather API Fetcher**: Use `requests` to fetch data from OpenWeatherMap, parse the JSON, and display a forecast.
*   **[Math] Matrix Operations Library**: Implement matrix addition, multiplication, and transposition from scratch without using NumPy.

## Level 2: Intermediate (Architecture & Libraries)

*Focus: OOP, Web Frameworks, Databases, Pandas, Scikit-Learn.*

*   **[Web] URL Shortener API**: Build a REST API using FastAPI and a SQLite database. Implement routing and data validation.
*   **[Data] E-commerce Sales Dashboard**: Clean a dirty dataset using Pandas, calculate KPIs, and visualize trends using Matplotlib/Seaborn.
*   **[Web] Asynchronous Web Scraper**: Scrape product prices from an e-commerce site using `asyncio` and `BeautifulSoup`/`Playwright`.
*   **[ML] Customer Churn Predictor**: Train a Random Forest classifier to predict customer churn based on historical data. Evaluate using precision/recall.
*   **[DSA] Custom Hash Map Implementation**: Build a fully functional Hash Map class implementing separate chaining for collision resolution.

## Level 3: Advanced (Integration & Deep Learning)

*Focus: Neural Networks, Transformers, System Design, End-to-End pipelines.*

*   **[MLOps] End-to-End ML Pipeline**: Create a pipeline that ingests data, trains an XGBoost model, tracks experiments via MLflow, and deploys as a REST API via Docker.
*   **[Deep Learning] Custom Image Classifier**: Train a CNN (ResNet architecture) using PyTorch on a custom dataset to classify images.
*   **[NLP] Sentiment Analysis API**: Fine-tune a BERT model on Hugging Face for a custom domain (e.g., financial news) and serve it.
*   **[System] Distributed Task Queue**: Build a simplified version of Celery using Redis as a message broker to handle background jobs.

## Level 4: Master (Generative AI & Complex Systems)

*Focus: LLMs, RAG, Agents, Scalability.*

*   **[GenAI] Chat-with-your-Codebase**: Build a Retrieval-Augmented Generation (RAG) system using LangChain, parsing this entire repository, storing embeddings in Pinecone, and answering technical questions.
*   **[GenAI] Autonomous Research Agent**: Create an agentic workflow (using AutoGen or LangGraph) that can take a research prompt, search the web, synthesize findings, and write a report.
*   **[System] Real-time Log Anomaly Detector**: Stream logs into Kafka, process them with PySpark, use an isolation forest to detect anomalies, and trigger alerts.
*   **[GenAI] Local LLM Deployment**: Quantize an open-source model (like Llama 3) to GGUF and serve it locally using vLLM for a privacy-first assistant.

---
**Advice on Projects:**
Do not follow tutorials blindly. Look at the requirements, attempt to build it yourself, and only consult resources when you are stuck. The struggle is where the learning happens.
