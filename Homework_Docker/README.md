# Docker Hello App (DevOps Homework)

This project demonstrates the basics of working with **Docker**:  
- Writing a simple web application (FastAPI)  
- Creating a `Dockerfile` to build an image  
- Running a container locally using Rancher Desktop (or Docker Engine)  
- Accessing the application in the browser  

---

## 📂 Project Structure
hello-docker/
├── main.py
├── requirements.txt
└── Dockerfile

### Steps to Run
1. Build the Docker image
docker build -t hello-fastapi .

2. Run the container
docker run -d --name hello-fastapi-c -p 8080:8080 hello-fastapi

3. Verify that it is running
docker ps
docker logs -f hello-fastapi-c

### Accessing the Application
Once the container is running, the app is available at:

http://localhost:8080/
 → JSON response with "Hello from Docker & Kubernetes 🚀"

http://localhost:8080/time
 → shows the current server time

 