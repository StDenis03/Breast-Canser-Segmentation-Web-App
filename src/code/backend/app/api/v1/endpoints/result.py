from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from app.db.database import db

router = APIRouter(prefix="/result", tags=["result"])

@router.get("/{study_id}")
async def get_result(study_id: int):
    with db.get_connection() as conn:
        study = conn.execute(
            "SELECT * FROM studies WHERE id = ?",
            (study_id,)
        ).fetchone()
    
    if not study:
        raise HTTPException(404, "Study not found")
    
    if study["status"] == "completed":
        return FileResponse(
            study["png_path"],
            media_type="image/png",
            filename=f"segmentation_{study_id}.png"
        )
    elif study["status"] == "processing":
        return {"status": "processing", "study_id": study_id}
    else:
        return {"status": "failed", "study_id": study_id}