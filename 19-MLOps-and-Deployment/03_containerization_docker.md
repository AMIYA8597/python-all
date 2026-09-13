# Containerization and Docker for ML Inference

Machine Learning models often suffer from the "It works on my machine" problem. A model trained on a data scientist's laptop using specific versions of Python, PyTorch, CUDA, and Linux drivers might completely fail when deployed to a production server with a slightly different environment.

**Containerization** solves this by packaging the application, its dependencies, runtime, and system libraries into a single, isolated, portable unit called a container. 

This document covers Docker fundamentals with a specific focus on packaging Machine Learning models for inference serving.

## 1. Core Concepts: Images vs. Containers

- **Docker Image**: A read-only, static template that contains everything needed to run an application. Think of it as a class in object-oriented programming, or an ISO file.
- **Docker Container**: A running, instantiated instance of a Docker Image. Think of it as an object created from a class, or a running virtual machine (though containers are much more lightweight than VMs).

## 2. The Dockerfile for ML Serving

A `Dockerfile` is a text document containing the commands needed to assemble a Docker Image. 

When building an image for ML inference (e.g., serving a model using FastAPI and Uvicorn), you must carefully manage dependencies and layer caching to keep image sizes manageable.

### Example: FastAPI + Scikit-Learn Inference Dockerfile

```dockerfile
# 1. Base Image: Use a slim, official Python image to reduce size.
# For Deep Learning, you might use nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04
FROM python:3.10-slim-buster

# 2. Set environment variables to optimize Python in Docker
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    MODEL_PATH=/app/models/random_forest.pkl

# 3. Create and set the working directory
WORKDIR /app

# 4. Install system dependencies (if required by ML libraries like OpenCV)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 5. Dependency caching layer. 
# We copy ONLY requirements first. If requirements don't change, 
# Docker caches this layer, saving huge amounts of build time.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copy the application code and model artifacts
COPY ./app /app/app
COPY ./models /app/models

# 7. Expose the port the app runs on (Documentation purpose)
EXPOSE 8000

# 8. Define the command to run the inference server
# Using Uvicorn to serve the FastAPI app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Docker Layer Caching (Critical for ML)
Docker builds images in layers (each `RUN`, `COPY`, `ADD` creates a layer). 
If a layer's contents haven't changed, Docker reuses it from the cache. Because ML dependencies (PyTorch, TensorFlow) are huge and take minutes to download, you should **always copy `requirements.txt` and run `pip install` before copying your application code**. 
If you copy the code first, any tiny change to a `.py` file will invalidate the cache for the `pip install` step.

## 3. Networking and Port Mapping

By default, a running container is completely isolated from the host machine's network. Even if your FastAPI app inside the container is running on port 8000, you cannot access it from your browser.

You must map a port on your host machine to the exposed port in the container using the `-p` flag.

```bash
# Build the image and tag it as 'ml-api'
docker build -t ml-api:v1 .

# Run the container in detached mode (-d)
# Map Host port 8080 to Container port 8000 (-p)
docker run -d -p 8080:8000 --name prediction_service ml-api:v1
```
Now, you can send inference requests to `http://localhost:8080/predict`.

## 4. Storage and Volumes

Containers are ephemeral. If a container crashes or is deleted, any data written inside its filesystem is lost forever. 

While an inference server is mostly stateless (processing requests), you often need to deal with files, such as:
1. **Model Updates**: You want to update the `.pkl` or `.pt` model file without rebuilding the entire massive Docker image.
2. **Logs**: You need to persist prediction logs for monitoring and drift detection.

**Volumes** allow you to mount a directory from the host machine into the container.

### Example: Mounting a Model Directory
Suppose your host machine downloads new models to `/data/ml_models/`. You can mount this into the container so the API always loads the latest model.

```bash
docker run -d \
  -p 8080:8000 \
  -v /data/ml_models:/app/models \
  --name prediction_service \
  ml-api:v1
```
Now, the `/app/models` directory inside the container is actually a direct window to `/data/ml_models` on the host. If a data engineer replaces the `.pkl` file on the host, the container sees the new file immediately.

## 5. Best Practices for ML Containers

1. **Minimize Image Size**: Don't use `ubuntu:latest` as a base image if `python:3.10-slim` is enough. Huge images take longer to push, pull, and deploy.
2. **Avoid Development Tools**: Do not install Jupyter, Matplotlib, or training datasets in an inference image. Keep it strictly limited to what is needed for serving.
3. **Use Multi-stage Builds**: If your deployment requires compiling C++ extensions or Rust code, use multi-stage builds to compile in one stage, and only copy the compiled binaries to the final, lightweight serving stage.
4. **GPU Support**: To use GPUs inside a container, you must install the NVIDIA Container Toolkit on the host and run the container with the `--gpus all` flag. Use `nvidia/cuda` base images provided by NVIDIA.
