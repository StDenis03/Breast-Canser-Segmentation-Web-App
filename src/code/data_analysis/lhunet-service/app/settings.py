import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))

LTS_TOKEN = os.getenv("LTS_TOKEN", "change-me")
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "v2")

DATASET_ID = os.getenv("DATASET_ID", "721")
CONFIGURATION = os.getenv("CONFIGURATION", "3d_fullres")

MODEL_DIR = Path(os.getenv("MODEL_DIR", str(BASE_DIR / "models" / "lhunet_breastct")))

NNUNET_RAW = os.getenv("nnUNet_raw", "/opt/nnunet/raw")
NNUNET_PREPROCESSED = os.getenv("nnUNet_preprocessed", "/opt/nnunet/preprocessed")
NNUNET_RESULTS = os.getenv("nnUNet_results", "/opt/nnunet/results")
NNUNET_EXT_TRAINER = os.getenv("nnUNet_extTrainer", "/opt/LHUNet/src")
TORCH_LIB_PATH = os.getenv(
    "TORCH_LIB_PATH",
    "/opt/conda/envs/lhunet/lib/python3.12/site-packages/torch/lib",
)

MODEL_TO_TRAINER = {
    "v1": "lhunetBreastTrainer",
    "v2": "lhunetBreastTrainerV2",
}

MODEL_TO_CHECKPOINT = {
    "v1": "lhunetBreastTrainer_fold0_best_v1.pth",
    "v2": "lhunetBreastTrainerV2_fold0_best_v2.pth",
}

MODEL_TO_PLANS = {
    "v1": "plans_v1.json",
    "v2": "plans_v2.json",
}
