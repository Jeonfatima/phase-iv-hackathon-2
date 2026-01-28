# Quickstart Guide: Local Kubernetes Deployment for Todo Chatbot

## Overview
This guide provides step-by-step instructions to deploy the Todo Chatbot application to a local Minikube Kubernetes cluster using AI-generated infrastructure.

## Prerequisites
- Docker Desktop with Kubernetes enabled or Minikube
- Helm 3.x
- kubectl
- kubectl-ai plugin
- kagent (Kubernetes AI assistant)
- Gordon AI (for Docker optimization) - optional with fallback
- Node.js 18+ and Python 3.11+ (for local development)

## Environment Setup

### 1. Clone and Navigate to Repository
```bash
git clone <repository-url>
cd <repository-directory>
git checkout 1-k8s-deployment  # Switch to the k8s deployment branch
```

### 2. Set Up Environment Variables
Create a `.env` file in the root directory with your environment variables:

```bash
# .env file
BETTER_AUTH_SECRET=your_jwt_secret_here
COHERE_API_KEY=your_cohere_api_key_here
DATABASE_URL=your_neon_database_url_here
```

## Deployment Steps

### Step 1: Start Minikube Cluster
```bash
# Start Minikube with docker driver and appropriate resources
minikube start --driver=docker --cpus=4 --memory=8192

# Enable ingress addon
minikube addons enable ingress

# Verify cluster is running
kubectl cluster-info
kubectl get nodes
```

### Step 2: Build Docker Images
Using Gordon AI (if available) or manual approach:

```bash
# If Gordon AI is available, use it to generate optimized Dockerfiles
# Otherwise, use the provided Dockerfiles in the docker/ directory

# Build frontend image
docker build -t todo-frontend:latest ./frontend

# Build backend image
docker build -t todo-backend:latest ./backend

# Verify images were built
docker images | grep todo-
```

### Step 3: Create Kubernetes Secrets
```bash
# Create secret from environment variables
kubectl create secret generic todo-secrets \
  --from-literal=BETTER_AUTH_SECRET=$(grep BETTER_AUTH_SECRET .env | cut -d '=' -f2) \
  --from-literal=COHERE_API_KEY=$(grep COHERE_API_KEY .env | cut -d '=' -f2) \
  --from-literal=DATABASE_URL=$(grep DATABASE_URL .env | cut -d '=' -f2)
```

### Step 4: Generate Helm Charts (AI-Assisted)
Using kubectl-ai to generate initial charts:

```bash
# Generate initial Helm chart structure using kubectl-ai
kubectl-ai "generate helm chart for todo app with frontend and backend deployments"

# Alternatively, if using pre-generated charts from charts/ directory:
helm dependency build charts/todo
helm lint charts/todo
```

### Step 5: Deploy Using Helm
```bash
# Install the Helm chart
helm install todo-app ./charts/todo --set image.tag=latest

# Wait for all pods to be ready
kubectl wait --for=condition=Ready pods -l app=todo --timeout=300s

# Verify deployment status
kubectl get pods
kubectl get services
kubectl get ingress
```

### Step 6: Access the Application
```bash
# Method 1: Using minikube tunnel (recommended for ingress)
minikube tunnel  # Run in separate terminal

# The application will be available at:
# Frontend: http://todo.local
# Backend API: http://todo.local/api

# Method 2: Using port forwarding (if ingress issues occur)
kubectl port-forward svc/frontend-service 3000:80
kubectl port-forward svc/backend-service 8000:80
```

## Verification Steps

### 1. Check Pod Status
```bash
kubectl get pods -o wide
kubectl describe pods
```

### 2. Check Service Connectivity
```bash
kubectl get services
kubectl get endpoints
```

### 3. Check Logs
```bash
# View frontend logs
kubectl logs -l app=frontend -f

# View backend logs
kubectl logs -l app=backend -f
```

### 4. Test Application Functionality
Open your browser and navigate to `http://todo.local` to access the Todo Chatbot application.

Verify the following functionality:
- User authentication works
- Task creation and management work
- AI chatbot interactions function properly
- Tasks persist in the database

## Troubleshooting with AI Tools

### Using kubectl-ai for Diagnosis
```bash
# Diagnose pod issues
kubectl-ai "why are my pods not starting?"

# Scale deployments
kubectl-ai "scale backend deployment to 3 replicas"

# Check resource usage
kubectl-ai "show me resource usage for all pods"
```

### Using kagent for Cluster Analysis
```bash
# Analyze cluster health
kagent "analyze cluster health"

# Get optimization suggestions
kagent "suggest optimizations for my deployments"
```

## Scaling and Management

### Scale Deployments
```bash
# Scale frontend
kubectl scale deployment frontend --replicas=3

# Scale backend
kubectl scale deployment backend --replicas=3

# Check current replica counts
kubectl get deployments
```

### Update Application
```bash
# To update the application with new image
helm upgrade todo-app ./charts/todo --set image.tag=new-tag

# Or update with new values
helm upgrade todo-app ./charts/todo --set frontend.replicaCount=3
```

## Cleanup
```bash
# Uninstall Helm release
helm uninstall todo-app

# Delete secrets
kubectl delete secret todo-secrets

# Stop minikube
minikube stop

# Optionally, delete the cluster entirely
minikube delete
```

## Next Steps
- Monitor application performance using kubectl commands
- Set up persistent storage for database if needed
- Configure TLS/SSL for production-like security
- Set up monitoring and alerting
- Optimize resource requests and limits based on actual usage