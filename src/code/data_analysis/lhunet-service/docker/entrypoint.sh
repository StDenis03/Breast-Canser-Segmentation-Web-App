#!/usr/bin/env bash
set -euo pipefail

export PYTHONPATH="/opt/service:/opt/LHUNet/nnUNet:${PYTHONPATH:-}"
export nnUNet_extTrainer="${nnUNet_extTrainer:-/opt/LHUNet/src}"

exec uvicorn app.app:app --host "${HOST:-0.0.0.0}" --port "${PORT:-8000}"
