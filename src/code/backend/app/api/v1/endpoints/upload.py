import uuid
import shutil
import logging
from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from app.core.config import settings
from app.db.database import db
from app.services.inference import run_inference
from pydantic import BaseModel

logger = logging.getLogger(__name__)

class UploadResponse(BaseModel):
    study_id: int
    status: str
    message: str

router = APIRouter(prefix="/upload", tags=["upload"])

async def _process_study(study_id: int, input_path, output_path):
    try:
        await run_inference(input_path, output_path)
        with db.get_connection() as conn:
            conn.execute(
                "UPDATE studies SET status = ?, result_path = ? WHERE id = ?",
                ("completed", str(output_path), study_id)
            )
            conn.commit()
    except Exception as e:
        logger.error("Inference failed for study %d: %s", study_id, e, exc_info=True)
        with db.get_connection() as conn:
            conn.execute(
                "UPDATE studies SET status = ? WHERE id = ?",
                ("failed", study_id)
            )
            conn.commit()

@router.post("/", response_model=UploadResponse)
async def upload_file(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    # 1. Валидация формата
    supported_formats = ('.dcm', '.nii', '.nii.gz')
    if not any(file.filename.endswith(fmt) for fmt in supported_formats):
        raise HTTPException(400, f"Only {supported_formats} files are supported")

    # 2. Сохраняем файл
    unique_id = str(uuid.uuid4())
    file_ext = '.nii.gz' if file.filename.endswith('.nii.gz') else file.filename.split('.')[-1]
    input_path = settings.DICOM_DIR / f"{unique_id}.{file_ext}"

    with open(input_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    # 3. Создаём запись в БД
    with db.get_connection() as conn:
        cursor = conn.execute(
            "INSERT INTO studies (filename, dicom_path, status) VALUES (?, ?, ?)",
            (file.filename, str(input_path), "processing")
        )
        study_id = cursor.lastrowid
        conn.commit()

    # 4. Запускаем обработку в фоне и сразу возвращаем ответ
    output_path = settings.RESULTS_DIR / f"{unique_id}.nii.gz"
    background_tasks.add_task(_process_study, study_id, input_path, output_path)

    return {
        "study_id": study_id,
        "status": "processing",
        "message": "File uploaded, processing started"
    }