from pathlib import Path

import nibabel as nib
import numpy as np
from PIL import Image


def nifti_to_png_slices(
    nifti_path: str,
    output_dir: str,
    normalize: bool = True,
) -> list[str]:
    """
    Конвертирует NIfTI в набор PNG (по одному на срез).

    Args:
        nifti_path: путь к .nii / .nii.gz
        output_dir: куда сохранять PNG
        normalize: нормализовать ли значения в [0, 255]

    Returns:
        список путей к PNG-файлам
    """
    nifti_img = nib.load(nifti_path)
    volume = nifti_img.get_fdata()

    if volume.ndim == 2:
        volume = volume[:, :, np.newaxis]
    elif volume.ndim != 3:
        raise ValueError(f"Unsupported shape: {volume.shape}")

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    saved_files = []

    for i in range(volume.shape[2]):
        slice_2d = volume[:, :, i]

        if normalize:
            min_val = slice_2d.min()
            max_val = slice_2d.max()

            if max_val > min_val:
                slice_2d = (slice_2d - min_val) / (max_val - min_val)

            slice_2d = (slice_2d * 255).astype(np.uint8)
        else:
            slice_2d = slice_2d.astype(np.uint8)

        img = Image.fromarray(slice_2d)

        file_path = output_path / f"slice_{i:04d}.png"
        img.save(file_path)

        saved_files.append(str(file_path))

    return saved_files