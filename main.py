from fastapi import FastAPI

app = FastAPI(
    title="GASC Face Attendance Backend",
    version="1.0.0"
)

@app.get("/")
def home():
    return {
        "status": "success",
        "message": "GASC Backend is running"
    }

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }
