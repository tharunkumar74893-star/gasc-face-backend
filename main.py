import os
from fastapi import FastAPI
from supabase import create_client, Client

app = FastAPI(title="GASC Face Attendance Backend")

supabase: Client = create_client(
    os.environ["SUPABASE_URL"],
    os.environ["SUPABASE_KEY"]
)

@app.get("/")
def home():
    return {
        "status": "success",
        "message": "GASC Backend is running"
    }

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/supabase-check")
def supabase_check():
    try:
        supabase.table("profiles").select("id").limit(1).execute()
        return {"status": "connected"}
    except Exception:
        return {"status": "connection_failed"}
