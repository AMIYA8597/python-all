# CI/CD for Machine Learning (MLOps)

Continuous Integration (CI) and Continuous Deployment (CD) are foundational practices in modern software engineering. In traditional software, CI/CD involves testing and deploying code. In Machine Learning (MLOps), CI/CD is significantly more complex because it must handle **Code, Data, and Models**.

This document covers how to implement automated pipelines for ML using GitHub Actions.

## 1. The Complexity of ML CI/CD

In traditional software, if the unit tests pass, the code is safe to deploy.
In ML, code that passes unit tests can still cause a catastrophic failure in production if:
- The data schema changed unexpectedly (e.g., a feature was dropped).
- The model's predictive performance degraded on new data.
- The model behaves unfairly on minority cohorts.

Therefore, an ML CI/CD pipeline must include:
1. **Code Testing**: Syntax formatting, linting, unit testing (pytest).
2. **Data Testing**: Validating the schema, checking for missing values, confirming data distributions.
3. **Model Testing**: Evaluating accuracy metrics against a golden holdout set, checking inference latency, and testing edge cases.
4. **Model Deployment**: Containerization, registry pushing, and deploying to an endpoint.

## 2. Using GitHub Actions for ML

GitHub Actions is a CI/CD platform integrated directly into GitHub. Workflows are defined using YAML files stored in the `.github/workflows/` directory of your repository.

### Scenario: Automated PR Checks
When a Data Scientist opens a Pull Request modifying the model training script or the API code, we want to automatically run tests before allowing the merge.

#### Example YAML: `ci-pipeline.yml`

```yaml
name: ML Integration Pipeline

on:
  pull_request:
    branches: [ "main" ]

jobs:
  test-code-and-model:
    runs-on: ubuntu-latest
    
    steps:
    # 1. Checkout the repository code
    - name: Checkout code
      uses: actions/checkout@v3

    # 2. Set up Python environment
    - name: Set up Python 3.10
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
        cache: 'pip' # Caches dependencies to speed up subsequent runs

    # 3. Install dependencies
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install flake8 pytest pytest-cov
        pip install -r requirements.txt

    # 4. Linting (Check for syntax and style errors)
    - name: Lint with flake8
      run: |
        flake8 src/ tests/ --count --max-line-length=100 --statistics

    # 5. Run Unit Tests on Data and Logic
    - name: Run Pytest
      run: |
        # This will run tests asserting data schemas and API endpoints
        pytest tests/ -v --cov=src/

    # 6. Run Model Evaluation (Shadow Run)
    - name: Evaluate Model Performance
      run: |
        # Run a script that loads the latest model, evaluates it on a 
        # benchmark dataset, and asserts that Accuracy > 85%
        python scripts/evaluate_model.py
      env:
        # Pass secrets safely to access external data or registries
        DB_PASSWORD: ${{ secrets.DB_PASSWORD }}
```

## 3. Data Versioning and Schema Checks

Data is as important as code in ML. You should not test a model on data that has silently changed. 

### Data Validation Tools
Tools like **Great Expectations** or **Pydantic** can be integrated into the CI pipeline (in Step 5 above) to assert data quality.
- *Is the `age` column always an integer between 0 and 120?*
- *Is the `income` column never null?*

### DVC (Data Version Control)
Git is terrible at versioning large binary files (like 50GB CSVs or .pt models). **DVC** works alongside Git. It stores the actual large files in cloud storage (S3/GCS) and commits tiny text pointer files (`.dvc`) into Git.

In a CI pipeline, you can use DVC to fetch the exact dataset corresponding to the current Git commit:
```yaml
    - name: Pull Data via DVC
      run: |
        pip install dvc[s3]
        dvc pull
      env:
        AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
        AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
```

## 4. Continuous Deployment (CD)

Once the PR is merged into the `main` branch, the CD pipeline triggers. Its job is to package the model and deploy it to a staging or production environment.

### Example CD Flow for Dockerized Inference Server

1. **Trigger**: Push to `main` branch.
2. **Build**: Build a Docker image containing the FastAPI inference server and the validated model.
3. **Push**: Tag the image with the Git commit hash and push it to a Container Registry (e.g., Docker Hub, AWS ECR).
4. **Deploy**: Trigger a cloud provider (e.g., AWS SageMaker, Kubernetes cluster, or Google Cloud Run) to pull the new image and perform a rolling update without downtime.

#### CD Step Example: Pushing to Docker Hub
```yaml
    - name: Log in to Docker Hub
      uses: docker/login-action@v2
      with:
        username: ${{ secrets.DOCKER_USERNAME }}
        password: ${{ secrets.DOCKER_PASSWORD }}

    - name: Build and Push Docker Image
      uses: docker/build-push-action@v4
      with:
        context: .
        push: true
        tags: |
          myorg/ml-api:latest
          myorg/ml-api:${{ github.sha }}
```

## 5. Continuous Training (CT)

Advanced MLOps architectures introduce **Continuous Training (CT)**.
Unlike traditional software, ML models degrade over time due to **Data Drift** (the real-world data changes, making the model's assumptions invalid).

A complete MLOps pipeline includes a monitor that tracks production predictions. If the data distribution shifts significantly, an automated trigger initiates a new pipeline that:
1. Retrains the model on the latest data.
2. Evaluates the new model against the old model.
3. If the new model is better, it automatically opens a PR or triggers the CD pipeline to deploy the updated model.

## Summary
- **CI**: Tests your code, validates your data schemas (Great Expectations), and ensures model performance metrics don't degrade.
- **CD**: Automates the building of Docker images and zero-downtime deployments to the cloud.
- **Tools**: GitHub Actions is the orchestrator, Git versions code, DVC versions data/models, and Docker packages the runtime.
