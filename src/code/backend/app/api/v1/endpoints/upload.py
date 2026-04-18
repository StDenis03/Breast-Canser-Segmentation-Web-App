import uuid
import shutil
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.core.config import settings
from app.db.database import db
from app.services.inference import run_inference
from pydantic import BaseModel

class UploadResponse(BaseModel):
    study_id: int
    status: str
    message: str

router = APIRouter(prefix="/upload", tags=["upload"])

@router.post("/", response_model=UploadResponse)
async def upload_dicom(file: UploadFile = File(...)):
    # 1. Валидация
    if not file.filename.endswith('.dcm'):
        raise HTTPException(400, "Only .dcm files are supported")
    
    # 2. Сохраняем DICOM
    unique_id = str(uuid.uuid4())
    dicom_path = settings.DICOM_DIR / f"{unique_id}.dcm"
    
    with open(dicom_path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    
    # 3. Создаём запись в БД
    with db.get_connection() as conn:
        cursor = conn.execute(
            "INSERT INTO studies (filename, dicom_path, status) VALUES (?, ?, ?)",
            (file.filename, str(dicom_path), "processing")
        )
        study_id = cursor.lastrowid
        conn.commit()
    
    try:
        # 4. Запускаем обработку
        png_path = settings.RESULTS_DIR / f"{unique_id}.png"
        run_inference(dicom_path, png_path)
        
        # 5. Обновляем запись
        with db.get_connection() as conn:
            conn.execute(
                "UPDATE studies SET status = ?, png_path = ? WHERE id = ?",
                ("completed", str(png_path), study_id)
            )
            conn.commit()
        
        return {
            "study_id": study_id,
            "status": "completed",
            "message": "Segmentation completed"
        }
    
    except Exception as e:
        with db.get_connection() as conn:
            conn.execute(
                "UPDATE studies SET status = ? WHERE id = ?",
                ("failed", study_id)
            )
            conn.commit()
        
        raise HTTPException(500, f"Processing failed: {str(e)}")