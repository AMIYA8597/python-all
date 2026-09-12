# CI/CD for Machine Learning

## What is CI/CD?
- **CI (Continuous Integration)**: The practice of automating the integration of code changes from multiple contributors into a single software project. It involves automatically building and testing the code.
- **CD (Continuous Deployment/Delivery)**: Automating the release and deployment of applications to infrastructure environments (Staging, Production).

## CI/CD in the context of Machine Learning (CT/CD)
Machine Learning adds a layer of complexity because code is not the only artifact that changes. Data and Models change too.

1. **Continuous Integration (CI)**: Testing code, validating data schemas, and testing model logic.
2. **Continuous Training (CT)**: A concept unique to ML. Automatically triggering a pipeline to retrain the model when new data arrives or model performance degrades (Data Drift/Concept Drift).
3. **Continuous Deployment (CD)**: Deploying the newly trained and validated model as a prediction service (API, Edge device, Batch pipeline).

## Typical ML Pipeline Workflow
1. **Developer pushes code**: Triggers GitHub Actions (or GitLab CI, Jenkins).
2. **Linting & Unit Tests**: Ensure code quality (e.g., using `flake8`, `pytest`).
3. **Data Validation**: Ensure incoming data matches expected schemas (e.g., using Great Expectations).
4. **Model Training**: Train model (often on powerful cloud instances) and log metrics to MLflow.
5. **Model Evaluation**: Compare the new model against the current production model.
6. **Containerization**: Build a Docker image containing the code and model.
7. **Deployment**: Push the image to a registry and update the serving infrastructure (e.g., Kubernetes, AWS SageMaker).

## Example GitHub Actions Workflow
The `05_ml_pipeline.yml` file is an example of a GitHub Actions workflow.
It demonstrates:
- Checking out code on push/pull request.
- Setting up Python.
- Running Linters (`flake8`).
- Running Tests (`pytest`).
- Building a Docker image if tests pass.

In a real repository, this file would live in `.github/workflows/ml_pipeline.yml`.
