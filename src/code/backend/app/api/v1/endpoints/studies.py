from fastapi import APIRouter
from app.db.database import db

router = APIRouter(prefix="/studies", tags=["studies"])

@router.get("/")
async def list_studies():
    with db.get_connection() as conn:
        studies = conn.execute(
            "SELECT id, filename, status, created_at FROM studies ORDER BY created_at DESC"
        ).fetchall()
    
    return {
        "studies": [
            {
                "id": s["id"],
                "filename": s["filename"],
                "status": s["status"],
                "created_at": s["created_at"]
            }
            for s in studies
        ]
    }