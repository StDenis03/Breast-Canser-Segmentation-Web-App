from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from app.db.database import db
from pathlib import Path

router = APIRouter(prefix="/result", tags=["result"])

def _get_study_or_404(study_id: int):
    with db.get_connection() as conn:
        study = conn.execute(
            "SELECT * FROM studies WHERE id = ?",
            (study_id,)
        ).fetchone()
    if not study:
        raise HTTPException(404, "Study not found")
    return study

@router.get("/{study_id}/status")
async def get_status(study_id: int):
    study = _get_study_or_404(study_id)
    return {"status": study["status"], "study_id": study_id}

@router.get("/{study_id}")
async def get_result(study_id: int):
    study = _get_study_or_404(study_id)

    if study["status"] != "completed":
        raise HTTPException(400, f"Study is not completed (status: {study['status']})")

    result_path = Path(study["result_path"])
    if not result_path.exists():
        raise HTTPException(500, "Result file not found on disk")

    return FileResponse(
        result_path,
        media_type="application/gzip",
        filename=f"segmentation_{study_id}.nii.gz"
    )