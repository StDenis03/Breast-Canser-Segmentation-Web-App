import json
from pathlib import Path
from typing import Any, Callable

import nibabel as nib
import numpy as np
import pydicom
from pydicom.dataset import FileDataset
from pydicom.multival import MultiValue

from backend.utils.preprocessing import ct_preprocessing


def _apply_hu_transform(ds: FileDataset, pixel_array: np.ndarray) -> np.ndarray:
    """
    Преобразование raw пикселей в физические значения через
    RescaleSlope и RescaleIntercept по формуле:
    U = V_row * Slope + Intercept
    """
    arr = pixel_array.astype(np.float32)

    slope = float(getattr(ds, "RescaleSlope", 1.0))
    intercept = float(getattr(ds, "RescaleIntercept", 0.0))

    arr = arr * slope + intercept
    return arr


def _get_pixel_spacing(ds: FileDataset) -> tuple[float, float]:
    if hasattr(ds, "PixelSpacing"):
        spacing = ds.PixelSpacing
        return float(spacing[0]), float(spacing[1])
    return 1.0, 1.0


def _get_slice_spacing(ds: FileDataset) -> float:
    if hasattr(ds, "SpacingBetweenSlices"):
        value = float(ds.SpacingBetweenSlices)
        if value > 0:
            return value

    if hasattr(ds, "SliceThickness"):
        value = float(ds.SliceThickness)
        if value > 0:
            return value

    return 1.0


def _build_affine_single_file(ds: FileDataset, volume_shape: tuple[int, ...]) -> np.ndarray:
    """
    Строит affine для одного DICOM-файла.

    Сценарии:
    1. Обычный 2D DICOM -> NIfTI shape (H, W, 1)
    2. Multi-frame DICOM -> NIfTI shape (H, W, Z)

    DICOM координаты по смыслу LPS.
    Здесь сохраняем affine как есть из DICOM-геометрии.
    """
    row_spacing, col_spacing = _get_pixel_spacing(ds)
    slice_spacing = _get_slice_spacing(ds)

    if hasattr(ds, "ImageOrientationPatient"):
        iop = np.array(ds.ImageOrientationPatient, dtype=np.float64)
        row_cosines = iop[:3]
        col_cosines = iop[3:]
        slice_cosines = np.cross(row_cosines, col_cosines)
    else:
        row_cosines = np.array([1.0, 0.0, 0.0], dtype=np.float64)
        col_cosines = np.array([0.0, 1.0, 0.0], dtype=np.float64)
        slice_cosines = np.array([0.0, 0.0, 1.0], dtype=np.float64)

    if hasattr(ds, "ImagePositionPatient"):
        origin = np.array(ds.ImagePositionPatient, dtype=np.float64)
    else:
        origin = np.array([0.0, 0.0, 0.0], dtype=np.float64)

    affine = np.eye(4, dtype=np.float64)
    affine[:3, 0] = row_cosines * col_spacing
    affine[:3, 1] = col_cosines * row_spacing
    affine[:3, 2] = slice_cosines * slice_spacing
    affine[:3, 3] = origin

    return affine


def dicom_file_to_nifti(
    dicom_path: str,
    nifti_path: str,
    preprocessing_fn: Callable[[np.ndarray, dict[str, Any]], tuple[np.ndarray, dict[str, Any]]],
    metadata_json_path: str | None = None,
    apply_hu_transform: bool = True,
    output_dtype: np.dtype | type = np.float32,
) -> None:
    """
    Конвертирует один DICOM-файл в NIfTI, с вызовом preprocessing между этапами.
    """
    dicom_file = Path(dicom_path)
    if not dicom_file.exists():
        raise FileNotFoundError(f"DICOM file not found: {dicom_path}")

    ds = pydicom.dcmread(str(dicom_file), force=True)

    if not hasattr(ds, "PixelData"):
        raise ValueError("DICOM file does not contain PixelData")

    pixel_array = ds.pixel_array

    if pixel_array.ndim == 2:
        pixels_volume = pixel_array[:, :, np.newaxis]
    elif pixel_array.ndim == 3:
        pixels_volume = np.transpose(pixel_array, (1, 2, 0))
    else:
        raise ValueError(f"Unsupported pixel array shape: {pixel_array.shape}")

    original_dtype = str(pixels_volume.dtype)

    if apply_hu_transform:
        pixels_volume = _apply_hu_transform(ds, pixels_volume)

    pixels_volume = pixels_volume.astype(np.float32, copy=False)

    processed_volume, preprocessing_info = preprocessing_fn(pixels_volume)
    processed_volume = np.asarray(processed_volume)

    # уточнить момент, какой размер будет подаваться на вход
    if processed_volume.ndim == 2:
        processed_volume = processed_volume[:, :, np.newaxis]
    elif processed_volume.ndim != 3:
        raise ValueError(
            f"Preprocessing must return 2D or 3D array, got shape {processed_volume.shape}"
        )

    processed_volume = processed_volume.astype(output_dtype, copy=False)

    affine = _build_affine_single_file(ds, processed_volume.shape)

    nifti_img = nib.Nifti1Image(processed_volume, affine)
    nifti_img.set_qform(affine, code=1)
    nifti_img.set_sform(affine, code=1)

    hdr = nifti_img.header
    row_spacing, col_spacing = _get_pixel_spacing(ds)
    slice_spacing = _get_slice_spacing(ds)

    hdr["pixdim"][1] = col_spacing
    hdr["pixdim"][2] = row_spacing
    hdr["pixdim"][3] = slice_spacing

    nifti_out = Path(nifti_path)
    nifti_out.parent.mkdir(parents=True, exist_ok=True)
    nib.save(nifti_img, str(nifti_out))

if __name__ == "__main__":
    dicom_file_to_nifti(
        "C:\\Users\\stden\\PycharmProjects\\OncoDetect-AI\\scr\\test_data\\IMG-0001-00001.dcm",
        "C:\\Users\\stden\\PycharmProjects\\OncoDetect-AI\\scr\\test_data\\IMG-0001-00001.nii.gz",
        ct_preprocessing,
        "C:\\Users\\stden\\PycharmProjects\\OncoDetect-AI\\scr\\test_data\\IMG-0001-00001.json"
    )
