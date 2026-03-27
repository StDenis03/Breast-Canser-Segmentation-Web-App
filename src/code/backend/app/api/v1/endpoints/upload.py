from fastapi import APIRouter, UploadFile, File, HTTPException
import uuid

router = APIRouter(prefix="/upload", tags=["upload"])

@router.post("/")
async def upload_dicom(file: UploadFile = File(...)):
    if not file.filename.endswith(('.dcm', '.zip')):
        raise HTTPException(400, "Only DICOM files (.dcm, .zip) are supported")
    
    task_id = str(uuid.uuid4())
    
    return {
        "task_id": task_id,
        "status": "processing",
        "filename": file.filename
    }

@router.get("/status/{task_id}")
async def get_status(task_id: str):
    return {
        "task_id": task_id,
        "status": "completed",
        "result_url": f"/api/v1/upload/result/{task_id}"
    }

@router.get("/result/{task_id}")
async def get_result(task_id: str):
    return {
        "task_id": task_id,
        "mask_url": "/static/mock_mask.png",
        "metrics": {
            "tumor_size_mm": 24.5,
            "confidence": 0.98
        }
    }