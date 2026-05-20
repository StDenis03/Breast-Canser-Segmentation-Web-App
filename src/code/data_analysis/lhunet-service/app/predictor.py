import os
import shutil
import subprocess
import tempfile
import uuid
from pathlib import Path

from fastapi import HTTPException

from app.settings import (
    CONFIGURATION,
    DATASET_ID,
    MODEL_DIR,
    MODEL_TO_CHECKPOINT,
    MODEL_TO_PLANS,
    MODEL_TO_TRAINER,
    NNUNET_EXT_TRAINER,
    NNUNET_PREPROCESSED,
    NNUNET_RAW,
    TORCH_LIB_PATH,
)

def ensure_supported_file(filename: str) -> str:
    name = Path(filename).name
    if name.endswith(".nii.gz") or name.endswith(".nii"):
        return name
    raise HTTPException(status_code=400, detail="Only .nii or .nii.gz are supported")

def to_nnunet_input_name(filename: str) -> str:
    name = ensure_supported_file(filename)
    if name.endswith("_0000.nii.gz") or name.endswith("_0000.nii"):
        return name
    if name.endswith(".nii.gz"):
        return name[:-7] + "_0000.nii.gz"
    return name[:-4] + "_0000.nii"

def output_name_from_input(input_name: str) -> str:
    if input_name.endswith("_0000.nii.gz"):
        return input_name.replace("_0000.nii.gz", ".nii.gz")
    if input_name.endswith("_0000.nii"):
        return input_name.replace("_0000.nii", ".nii.gz")
    raise RuntimeError(f"Unexpected input name: {input_name}")

def prepare_model_layout(model: str, work_dir: Path) -> Path:
    trainer = MODEL_TO_TRAINER[model]
    checkpoint_name = MODEL_TO_CHECKPOINT[model]
    plans_name = MODEL_TO_PLANS[model]

    src_ckpt = MODEL_DIR / checkpoint_name
    src_plans = MODEL_DIR / plans_name
    src_dataset = MODEL_DIR / "dataset.json"

    model_root = work_dir / "nnunet_results" / f"Dataset{DATASET_ID}_BreastCT" / f"{trainer}__nnUNetPlans__{CONFIGURATION}"
    fold_dir = model_root / "fold_0"
    fold_dir.mkdir(parents=True, exist_ok=True)

    shutil.copy2(src_ckpt, fold_dir / "checkpoint_best.pth")
    shutil.copy2(src_plans, model_root / "plans.json")
    shutil.copy2(src_dataset, model_root / "dataset.json")

    return work_dir / "nnunet_results"

def run_inference(input_file: Path, model: str) -> Path:
    if model not in MODEL_TO_TRAINER:
        raise HTTPException(status_code=400, detail=f"Unsupported model: {model}")

    with tempfile.TemporaryDirectory(prefix=f"lhunet_{uuid.uuid4().hex[:12]}_") as tmp:
        tmp_dir = Path(tmp)
        input_dir = tmp_dir / "input"
        output_dir = tmp_dir / "output"
        input_dir.mkdir(parents=True, exist_ok=True)
        output_dir.mkdir(parents=True, exist_ok=True)

        nnunet_input_name = to_nnunet_input_name(input_file.name)
        local_input = input_dir / nnunet_input_name
        shutil.copy2(input_file, local_input)

        local_results_root = prepare_model_layout(model, tmp_dir)

        env = os.environ.copy()
        env["nnUNet_raw"] = NNUNET_RAW
        env["nnUNet_preprocessed"] = NNUNET_PREPROCESSED
        env["nnUNet_results"] = str(local_results_root)
        env["nnUNet_extTrainer"] = NNUNET_EXT_TRAINER
        env["TORCH_LIB_PATH"] = TORCH_LIB_PATH
        env["LD_LIBRARY_PATH"] = f"{TORCH_LIB_PATH}:{env.get('LD_LIBRARY_PATH', '')}"

        cmd = [
            "nnUNetv2_predict",
            "-i", str(input_dir),
            "-o", str(output_dir),
            "-d", DATASET_ID,
            "-c", CONFIGURATION,
            "-f", "0",
            "-tr", MODEL_TO_TRAINER[model],
            "-chk", "checkpoint_best.pth",
        ]

        result = subprocess.run(cmd, env=env, capture_output=True, text=True)
        if result.returncode != 0:
            raise HTTPException(
                status_code=500,
                detail={
                    "message": "Inference failed",
                    "stdout": result.stdout[-4000:],
                    "stderr": result.stderr[-4000:],
                },
            )

        pred_name = output_name_from_input(nnunet_input_name)
        pred_path = output_dir / pred_name
        if not pred_path.exists():
            candidates = sorted(output_dir.glob("*.nii.gz"))
            if not candidates:
                raise HTTPException(status_code=500, detail="No prediction file produced")
            pred_path = candidates[0]

        final_pred = Path(tempfile.gettempdir()) / f"{uuid.uuid4().hex[:8]}_{pred_path.name}"
        shutil.copy2(pred_path, final_pred)
        return final_pred
