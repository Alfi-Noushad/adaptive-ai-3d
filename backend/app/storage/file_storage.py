import os
import uuid
from pathlib import Path
from fastapi import UploadFile, HTTPException, status

ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}
ALLOWED_MIME_TYPES = {"image/png", "image/jpeg", "image/webp"}
MAX_FILE_SIZE_BYTES = 15 * 1024 * 1024  # 15 MB

STORAGE_DIR = Path("storage/uploads")
STORAGE_DIR.mkdir(parents=True, exist_ok=True)

def save_uploaded_image(file: UploadFile) -> dict:
    original_ext = Path(file.filename).suffix.lower()
    if original_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file format '{original_ext}'. Allowed formats: PNG, JPEG, WEBP."
        )

    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid content type '{file.content_type}'. Must be an image."
        )

    unique_filename = f"{uuid.uuid4().hex}{original_ext}"
    target_path = STORAGE_DIR / unique_filename

    bytes_written = 0
    with open(target_path, "wb") as buffer:
        while chunk := file.file.read(1024 * 1024):
            bytes_written += len(chunk)
            if bytes_written > MAX_FILE_SIZE_BYTES:
                buffer.close()
                if target_path.exists():
                    os.remove(target_path)
                raise HTTPException(
                    status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                    detail="File exceeds maximum permissible size of 15 MB."
                )
            buffer.write(chunk)

    return {
        "filename": unique_filename,
        "storage_path": str(target_path),
        "format": original_ext.replace(".", "").upper(),
        "file_size_bytes": bytes_written
    }
