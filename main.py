import os
from fastapi import FastAPI, UploadFile, File, Header, HTTPException
from supabase import create_client, Client

app = FastAPI(title="GASC College Management Backend")

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


@app.post("/register-photo")
async def register_photo(
    photo: UploadFile = File(...),
    authorization: str = Header(...)
):
    try:
        if not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Invalid token")

        token = authorization.replace("Bearer ", "", 1)
        user_response = supabase.auth.get_user(token)
        user = user_response.user

        if not user:
            raise HTTPException(status_code=401, detail="Unauthorized")

        if photo.content_type not in ["image/jpeg", "image/png", "image/webp"]:
            raise HTTPException(status_code=400, detail="Invalid image format")

        image_data = await photo.read()

        if len(image_data) > 5 * 1024 * 1024:
            raise HTTPException(status_code=400, detail="Image exceeds 5 MB")

        file_path = f"{user.id}/registration-photo"

        supabase.storage.from_("profile-photos").upload(
            file_path,
            image_data,
            file_options={
                "content-type": photo.content_type,
                "upsert": "true"
            }
        )

        return {
            "status": "success",
            "message": "Photo registered successfully",
            "photo_path": file_path
        }

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Photo registration failed"
        )
