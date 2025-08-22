# Kubernetes Deployment for Docker Homework

This folder contains the Kubernetes manifests to deploy the **hello-fastapi** app into a local Rancher Desktop Kubernetes cluster.

---

## ⚙️ Steps to Deploy

### 1. Apply Deployment and Service
```bash
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml

### 2. Verify
kubectl get pods
kubectl get svc

You should see:
- 2 pods running (because replicas: 2)
- A service called fastapi-service exposing port 8080

### 3. Accessing the Application (Port Forwarding)
kubectl port-forward service/fastapi-service 8080:8080

Now you can open:
http://localhost:8080/
 → JSON message "Hello from Docker & Kubernetes"
http://localhost:8080/time
 → current server time


