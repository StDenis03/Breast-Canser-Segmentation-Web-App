import nibabel as nib
import numpy as np
import pydicom
from PIL import Image
import os
from typing import Any, Callable

def ct_preprocessing(
    volume: np.ndarray,
    metadata: dict[str, Any],
) -> tuple[np.ndarray, dict[str, Any]]:
    """
    Пример preprocessing для КТ.
    Ожидается, что volume уже переведён в HU.
    """
    result = volume.astype(np.float32, copy=True)


    hu_min = -1000
    hu_max = 1000
    result = np.clip(result, hu_min, hu_max)

    min_val = float(result.min())
    max_val = float(result.max())
    if max_val > min_val:
        result = (result - min_val) / (max_val - min_val)


    return result
