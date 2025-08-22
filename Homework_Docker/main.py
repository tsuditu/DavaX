from fastapi import FastAPI
from datetime import datetime

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Salut din Docker & Kubernetes 🚀"}

@app.get("/time")
def read_time():
    return {"time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
