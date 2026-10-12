# Diabetes Prediction App with Kubernetes, FastAPI, and Docker

A beginner-friendly Kubernetes and MLOps project that trains a machine learning model to predict whether a patient is diabetic based on common health indicators.

## Overview

This application:
- Trains a Random Forest classifier using the Plotly diabetes dataset
- Exposes a FastAPI service for prediction
- Packages the app in Docker
- Deploys the service to a Kubernetes cluster with Kind

## Features

The model uses the following inputs:
- Pregnancies
- Glucose
- BloodPressure
- BMI
- Age

The API exposes a `/predict` endpoint that returns a simple boolean result indicating whether the person is predicted to be diabetic.

## Tech Stack

- Python
- FastAPI
- scikit-learn
- joblib
- Docker
- Kubernetes (Kind + kubectl)

## Project Structure

```text
.
├── Dockerfile
├── README.md
├── main.py
├── requirements.txt
├── k8s-deploy.yml
├── model/
│   └── diabetes_model.pkl
├── model training script/
│   └── train.py
└── .venv/
```

## Prerequisites

Before you begin, make sure you have the following installed:

- Python 3.10+
- pip
- Docker
- kubectl
- Kind

## Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/TharushiDinushika/Diabetics-Prediction-App-with-Kubernetes.git
cd Diabetics-Prediction-App-with-Kubernetes
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
```

On Windows:

```bash
.venv\Scripts\activate
```

On macOS/Linux:

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Train the model

```bash
python "model training script/train.py"
```

This will save the trained model in the `model/diabetes_model.pkl` file.

### 5. Run the API locally

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Then open:

- http://localhost:8000/
- http://localhost:8000/docs

## Sample API Request

```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "Pregnancies": 1,
    "Glucose": 85,
    "BloodPressure": 66,
    "BMI": 26.6,
    "Age": 31
  }'
```

Example response:

```json
{
  "diabetic": false
}
```

## Docker

Build the Docker image:

```bash
docker build -t diabetes-prediction-app .
```

Run the container:

```bash
docker run -p 8000:8000 diabetes-prediction-app
```

The app will be available at:

```text
http://localhost:8000/docs
```

## Kubernetes Deployment with Kind

### 1. Create a local cluster

```bash
kind create cluster --name diabetes-prediction-app
```

Check the cluster status:

```bash
kubectl get nodes
```

### 2. Build and push the Docker image

```bash
docker build -t diabetes-prediction-app .
```

Copy the image ID produced by Docker, then tag it with your Docker Hub username:

```bash
docker tag <image-id> <your-docker-username>/diabetes-prediction-api:v1
```

Log in to Docker Hub:

```bash
docker login
```

Push the image:

```bash
docker push <your-docker-username>/diabetes-prediction-api:v1
```

Update the image reference in `k8s-deploy.yml` if needed:

```yaml
image: tharushidinushika/diabetes-prediction-api:v1
```
Replace tharushidinushika iwth your docker hub username.

### 3. Deploy to Kubernetes

```bash
kubectl apply -f k8s-deploy.yml
```

Check pod status:

```bash
kubectl get pods -w
```

When the pods are ready, verify the service:

```bash
kubectl get svc
```

### 4. Port-forward the service

```bash
kubectl port-forward svc/diabetes-api-service 1111:80 --address=0.0.0.0
```

Open the API in the browser:

```text
http://localhost:1111/docs
```

## Notes

- The model is trained from the dataset at: https://raw.githubusercontent.com/plotly/datasets/master/diabetes.csv
- The application currently predicts based on the feature set defined in `main.py` and `train.py`
- For production use, you would typically add validation, monitoring, CI/CD, and better deployment configuration
