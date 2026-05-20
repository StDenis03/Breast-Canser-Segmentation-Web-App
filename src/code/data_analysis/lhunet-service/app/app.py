import tempfile
from pathlib import Path

from fastapi import FastAPI, File, Form, Header, HTTPException, UploadFile
from fastapi.responses import FileResponse

from app.predictor import run_inference
from app.settings import DEFAULT_MODEL, LTS_TOKEN, MODEL_TO_TRAINER

app = FastAPI(title="LHUNet Inference Service")

def check_token(authorization: str | None) -> None:
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")
    if authorization.strip() != f"Bearer {LTS_TOKEN}":
        raise HTTPException(status_code=403, detail="Invalid token")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/models")
def models():
    return {"available_models": list(MODEL_TO_TRAINER.keys()), "default_model": DEFAULT_MODEL}

@app.post("/predict")
async def predict(
    file: UploadFile = File(...),
    model: str = Form(DEFAULT_MODEL),
    authorization: str | None = Header(default=None),
):
    check_token(authorization)

    suffix = ".nii.gz" if file.filename.endswith(".nii.gz") else ".nii"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp_path = Path(tmp.name)
        while True:
            chunk = await file.read(1024 * 1024)
            if not chunk:
                break
            tmp.write(chunk)

    final_input = tmp_path.with_name(Path(file.filename).name)
    tmp_path.rename(final_input)

    pred_path = run_inference(final_input, model=model)

    return FileResponse(
        path=pred_path,
        media_type="application/gzip",
        filename=pred_path.name,
    )
