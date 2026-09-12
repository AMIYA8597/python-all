# Containerization for ML Models (Docker)

## What is Containerization?
Containerization involves packaging a machine learning application and all its dependencies (libraries, framework, configuration files) into a single artifact called a **container**. This ensures that the application runs consistently regardless of the computing environment (development, testing, or production).

## Why Docker for ML?
Machine Learning applications are notoriously difficult to reproduce due to complex dependency trees (e.g., specific versions of Python, CUDA drivers, TensorFlow/PyTorch, scikit-learn).
Docker solves the "it works on my machine" problem.

### Benefits:
1. **Reproducibility**: Exact same environment everywhere.
2. **Isolation**: Avoid conflicts with other applications or libraries on the host system.
3. **Portability**: Run locally, on a server, or in the cloud (AWS, GCP, Azure).
4. **Scalability**: Easily scale up by deploying multiple containers using Kubernetes (K8s).

## Key Docker Concepts
- **Dockerfile**: A text document containing all the commands to assemble an image.
- **Docker Image**: A read-only template with instructions for creating a Docker container (built from the Dockerfile).
- **Docker Container**: A runnable instance of an image.
- **Docker Hub / Container Registry**: A place to store and share your Docker images (like GitHub for code).

## How to use the provided `03_Dockerfile`

1. **Build the Docker Image:**
   Open your terminal in the directory containing `03_Dockerfile` and `02_fastapi_serving.py`.
   Run the following command to build the image and tag it as `iris-classifier`:
   ```bash
   docker build -f 03_Dockerfile -t iris-classifier:latest .
   ```

2. **Run the Docker Container:**
   Once built, you can run the container and map port 8000 of the container to port 8000 of your host machine.
   ```bash
   docker run -p 8000:8000 iris-classifier:latest
   ```

3. **Test the Application:**
   Open your browser to `http://127.0.0.1:8000/docs` to see the FastAPI Swagger UI running from inside the Docker container!
